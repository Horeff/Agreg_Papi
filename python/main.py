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
    import xml.etree.ElementTree as ET
except ImportError:
    print("La bibliothèque 'bs4' est manquante. Installation en cours...")
    subprocess.call([sys.executable, "-m", "pip", "install", "beautifulsoup4"])
    print("Bibliothèque 'bs4' installée avec succès!")
    import xml.etree.ElementTree as ET

try:
    import webbrowser
except ImportError:
    print("La bibliothèque 'webbrowser' est manquante. Installation en cours...")
    subprocess.call([sys.executable, "-m", "pip", "install", "webbrowser"])
    print("Bibliothèque 'webbrowser' installée avec succès!")
    import webbrowser

if platform.system() == "Windows":
    Path = str(sys.argv[0])
    Path = Path.split('\\')
    Path = "/".join(Path[:-1])
else:
    Path = sys.argv[0].split('/')
    Path = "/".join(Path[:-1])

print("Executé : ", Path, "sur : ", platform.system())

if platform.system() == 'Windows':
    try:
        from win10toast_click import ToastNotifier
    except ImportError:
        print("La bibliothèque 'win10toast_click' est manquante. Installation en cours...")
        subprocess.call([sys.executable, "-m", "pip", "install", "win10toast-click"])
        print("Bibliothèque 'win10toast_click' installée avec succès!")
        from win10toast_click import ToastNotifier

    def open_LaChamp():
        webbrowser.open("https://lachampagneviticole.fr/le-magazine/")

    def send_notification(title, message, icon_path):
        try:
            toaster = ToastNotifier()
            toaster.show_toast(title, message, icon_path=icon_path, callback_on_click=open_LaChamp)
        except Exception as e:
            print("Erreur lors de l'affichage de la notification:", e)

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
    resultat = []

    tree = ET.parse(path)
    root = tree.getroot()

    channel_title = root.find(".//channel/title").text
    channel_link = root.find(".//channel/link").text
    print("Titre du canal :", channel_title)
    print("Lien du canal :", channel_link)

    for item in root.findall(".//item"):
        item_title = item.find("title").text
        item_link = item.find("link").text
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
        with open(path+"/log_rss", "r", encoding='utf-8') as file:
            contenu = file.read()
        return contenu.split("\n")
    except:
        return []

def dump_log(path, contenu):
    with open(path+"/log_rss", "w", encoding='utf-8') as file:
        file.write(contenu)

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
    dump_log(Path, "\n".join(resultat))
    if len(resultat) != len(log_cont) or diff_listes(resultat, log_cont, True):
        nb = diff_listes(resultat, log_cont, False)
        if nb == 1:
            notif("Il y a " + str(nb) + " nouvel article")
        else:
            notif("Il y a " + str(nb) + " nouveaux articles")

main()
