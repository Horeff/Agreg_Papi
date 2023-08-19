import sys
import platform
import subprocess

try:
    import requests
except ImportError:
    print("La bibliothèque 'requests' est manquante. Installation en cours...")
    subprocess.call([sys.executable, "-m", "pip", "install", "requests"])
    print("Bibliothèque 'requests' installée avec succès!")
    import requests

try:
    from bs4 import BeautifulSoup
except ImportError:
    print("La bibliothèque 'bs4' est manquante. Installation en cours...")
    subprocess.call([sys.executable, "-m", "pip", "install", "beautifulsoup4"])
    print("Bibliothèque 'bs4' installée avec succès!")
    from bs4 import BeautifulSoup

try:
    import webbrowser
except ImportError:
    print("La bibliothèque 'webbrowser' est manquante. Installation en cours...")
    subprocess.call([sys.executable, "-m", "pip", "install", "webbrowser"])
    print("Bibliothèque 'webbrowser' installée avec succès!")
    import webbrowser

Path = sys.argv[0].split('/')
Path = "/".join(Path[:-1])

if platform.system() == 'Windows':
    #try:
    #    from win10toast_click import ToastNotifier
    #except ImportError:
    #    print("La bibliothèque 'win10toast_click' est manquante. Installation en cours...")
    #    subprocess.call([sys.executable, "-m", "pip", "install", "win10toast-click"])
    #    print("Bibliothèque 'win10toast_click' installée avec succès!")
    #    from win10toast_click import ToastNotifier

    def open_LaChamp():
        webbrowser.open("https://lachampagneviticole.fr/le-magazin")

    #def send_notification(title, message, icon_path):
    #    toaster = ToastNotifier()
    #    toaster.show_toast(title, message, icon_path=icon_path, callback_on_click = open_LaChamp)
    pass

elif platform.system() == 'Darwin':
    try:
        from pync import Notifier
    except ImportError:
        print("La bibliothèque 'pync' est manquante. Installation en cours...")
        subprocess.call([sys.executable, "-m", "pip", "install", "pync"])
        print("Bibliothèque 'pync' installée avec succès!")
        from pync import Notifier

    def send_notification(title, message, icon_path):
        Notifier.notify(message, title=title, appIcon=icon_path, open='https://lachampagneviticole.fr/le-magazin')

else:
    def send_notification(title, message, icon_path):
        print(f"Notifications not supported on {platform.system()}")

def lire_rss(path):
    with open(path, 'r') as file:
        rssContent = file.read()

    resultat = []

    soup = BeautifulSoup(rssContent)  # Utilisez 'xml' comme analyseur

    channel_title = soup.find('title').text
    channel_link = soup.find('link').text
    print("Titre du canal :", channel_title)
    print("Lien du canal :", channel_link)

    items = soup.find_all('item')
    for item in items:
        item_title = item.find('title').text
        item_link = item.find('link').text
        print("Titre de l'article :", item_title)
        print("Lien de l'article :", item_link)
        resultat.append(item_title + "~" + item_link)

    return resultat

def rec_RSS(outputPath):
    url = "https://lachampagneviticole.fr/feed/"

    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open(outputPath + "/flux_rss.xml", "wb") as outFile:
                outFile.write(response.content)
                print("RSS enregistré dans le fichier 'flux_rss.xml'")
        else:
            print("Failed to fetch RSS. Status code:", response.status_code)
    except requests.exceptions.RequestException as e:
        print("Failed to fetch RSS:", e)

def get_logs(path):
    try:
        with open(path+"/log_rss", "r") as file:
            contenu = file.read()
        return contenu.split("\n")
    except:
        return []

def dump_log(path, contenu):
    with open(path+"/log_rss", "w") as file:
        file.write(str(contenu))

def diff_listes(A, B, arg = True):
    if len(A) != len(B):
        if arg is True:
            return True
    if len(B) == 0:
        return len(A) - 1
    i = 1
    while i <= len(A) and A[len(A) - i] != B[-1]:
        i += 1
    if arg:
        if i != 1:
            return True
        else:
            return False
    else:
        if i == 1:
            return 0
        else:
            return i-1

def notif(text):
    # Utilisation de la fonction send_notification
    notification_title = "La Champagne Viticole"
    icon_path = Path + "/icone.ico"
    send_notification(notification_title, text, icon_path)


def main():
    rec_RSS(Path)
    resultat = lire_rss(Path+"/flux_rss.xml")
    log_cont = get_logs(Path)

    if len(resultat) != len(log_cont) or diff_listes(resultat, log_cont, True):
        nb = diff_listes(resultat, log_cont, False)
        if nb == 1:
            notif("Il y a " + str(nb) + " nouvel article")
        else:
            notif("Il y a " + str(nb) + " nouveaux articles")

    dump_log(Path, "\n".join(resultat))

main()