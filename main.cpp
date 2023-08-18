#include <iostream>
#include <fstream>
#include <curl/curl.h>
#include <string>
#include <vector>
#include <sstream>

#ifdef _WIN32
#include <winrt/Windows.Foundation.h>
#include <winrt/Windows.UI.Notifications.h>
#endif

#ifdef __APPLE__

extern "C" void sendNotification(const char* text, const char* path);

#endif


size_t WriteCallback(void* contents, size_t size, size_t nmemb, void* userp) {
    std::ofstream* file = static_cast<std::ofstream*>(userp);
    if (file) {
        file->write(static_cast<char*>(contents), size * nmemb);
        return size * nmemb;
    }
    return 0;
}

std::vector<std::string> lire_rss(std::string &rssContent){
    // Recherche du titre du canal
    size_t titleStart = rssContent.find("<title>") + 7;
    size_t titleEnd = rssContent.find("</title>", titleStart);
    std::string channelTitle = rssContent.substr(titleStart, titleEnd - titleStart);

    // Recherche du lien du canal
    size_t linkStart = rssContent.find("<link>") + 6;
    size_t linkEnd = rssContent.find("</link>", linkStart);
    std::string channelLink = rssContent.substr(linkStart, linkEnd - linkStart);

    std::cout << "Titre du canal : " << channelTitle << std::endl;
    std::cout << "Lien du canal : " << channelLink << std::endl;

    size_t itemStart = 0;
    std::vector<std::string> resultat;
    while ((itemStart = rssContent.find("<item>", itemStart)) != std::string::npos) {
        size_t itemEnd = rssContent.find("</item>", itemStart);
        std::string item = rssContent.substr(itemStart, itemEnd - itemStart);

        // Recherche du titre de l'article
        size_t itemTitleStart = item.find("<title>") + 7;
        size_t itemTitleEnd = item.find("</title>", itemTitleStart);
        std::string itemTitle = item.substr(itemTitleStart, itemTitleEnd - itemTitleStart);

        // Recherche du lien de l'article
        size_t itemLinkStart = item.find("<link>") + 6;
        size_t itemLinkEnd = item.find("</link>", itemLinkStart);
        std::string itemLink = item.substr(itemLinkStart, itemLinkEnd - itemLinkStart);

        std::cout << "Titre de l'article : " << itemTitle << std::endl;
        std::cout << "Lien de l'article : " << itemLink << std::endl;
        resultat.push_back(itemTitle += "~"+itemLink);
        itemStart = itemEnd + 7; // +7 pour passer après "</item>"
    }
    return resultat;
}

void rec_RSS(std::string &outputPath){
    CURL* curl = curl_easy_init();
    if (curl) {
        curl_easy_setopt(curl, CURLOPT_URL, "https://lachampagneviticole.fr/feed/");

        std::ofstream outFile(outputPath + "flux_rss.xml", std::ios::binary);
        if (outFile.is_open()) {
            curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteCallback);
            curl_easy_setopt(curl, CURLOPT_WRITEDATA, &outFile);

            CURLcode res = curl_easy_perform(curl);
            if (res != CURLE_OK) {
                std::cerr << "Failed to fetch RSS: " << curl_easy_strerror(res) << std::endl;
            } else {
                std::cout << "RSS enregistré dans le fichier 'flux_rss.xml'" << std::endl;
            }

            outFile.close();
        } else {
            std::cerr << "Failed to open file for writing" << std::endl;
        }

        curl_easy_cleanup(curl);
    }
}

int main(int argc, char* argv[]) {

    std::string programPath = argv[0];
    size_t lastSlashPos = programPath.find_last_of('/');
    std::string outputPath = programPath.substr(0, lastSlashPos + 1);

    rec_RSS(outputPath);

    // Récupération du contenu
    std::ifstream file(outputPath + "flux_rss.xml");
    std::vector<std::string> resultat;
    if (file){
        std::string contenu;
        std::string line;
        while (std::getline(file, line)){
            contenu += line;
        }
        resultat = lire_rss(contenu);
        file.close();
    }
    // Récupération des logs
    std::ifstream log_file(outputPath+"log_Agreg_Papi.txt");
    std::vector<std::string> contenu_log;
    if (log_file){
        std::string line;
        while(std::getline(log_file, line)){
            contenu_log.push_back(line);
        }
        log_file.close();
    }else{
        // Création du fichier log s'il n'existe pas
        std::ofstream new_log_file(outputPath+"log_Agreg_Papi.txt");
        for(auto &i: resultat){
            new_log_file << i << std::endl;
        }
        new_log_file.close();
    }
    // Comparaison des deux sources
    if (resultat.size() != contenu_log.size()){
        // Notification
        int nouveauxArticles = resultat.size() - contenu_log.size();
        std::stringstream ss;
        ss << "Il y a " << nouveauxArticles << " Nouveaux articles";
        std::string notificationText = ss.str();

        #ifdef _WIN32
            winrt::init_apartment();

            // Créer une notification Windows
            winrt::Windows::UI::Notifications::ToastNotificationManager::CreateToastNotifier().Show(
                winrt::Windows::UI::Notifications::ToastNotification(winrt::Windows::UI::Notifications::ToastTemplateType::ToastText01)
                    .Content(winrt::Windows::Data::Xml::Dom::XmlDocument::CreateToastXml(L"<toast><visual><binding template=\"ToastText01\"><text id=\"1\">" + winrt::to_hstring(notificationText) + L"</text></binding></visual></toast>")));
        #endif

        #ifdef __APPLE__
                sendNotification(notificationText.c_str(), outputPath.c_str());
        #endif
    }
    std::ofstream new_log_file(outputPath+"log_Agreg_Papi");
    if (new_log_file){
        for(auto &i: resultat){
            new_log_file << i << std::endl;
        }
    }
    return 0;
}




