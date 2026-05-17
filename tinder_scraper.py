import os
import cv2
import requests
import time
import random
import tkinter as tk
from tkinter import messagebox
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

# Modello facciale locale scaricato manualmente
CASCADE_FILE = "haarcascade_frontalface_default.xml"
if not os.path.exists(CASCADE_FILE):
    print(f"ERRORE: Il file '{CASCADE_FILE}' non è stato trovato nella cartella del progetto.")
    exit()

face_cascade = cv2.CascadeClassifier(CASCADE_FILE)

# --- NOTIFICA POP-UP ---
def mostra_avviso_match(percentuale, nome_profilo, percorso_file):
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    messaggio = f"❤️ MATCH IDENTIFICATO!\n\nNome: {nome_profilo}\nSomiglianza Massima: {percentuale:.2%}\n\nArchiviato in:\n{percorso_file}"
    messagebox.showinfo("TINDER MATCH DETECTOR", messaggio)
    root.destroy()

# --- ALLERTA ACUSTICA E PAUSA PER CAPTCHA ---
def gestisci_blocco_captcha():
    # Emette 3 beep sonori su Windows per avvisarti
    for _ in range(3):
        print("\a", end="", flush=True)  # Carattere di controllo per il beep di sistema
        time.sleep(0.5)
        
    print("\n⚠️ [BLOCCO CAPTCHA RILEVATO / VERIFICA UMANA]")
    print("Tinder ha interrotto gli swipe richiedendo una verifica.")
    print("-> Risolvi il puzzle visivo direttamente nella finestra del browser.")
    input("👉 Una volta superato il CAPTCHA, premi INVIO qui nel terminale per riprendere...")

# --- ANALISI FACCIALE ---
def extract_face(image_or_path, is_path=True):
    if is_path:
        img = cv2.imread(image_or_path)
    else:
        img = image_or_path
        
    if img is None: return None
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(50, 50))
    
    if len(faces) == 0: return None
    x, y, w, h = faces
    return img[y:y+h, x:x+w]

def sorted_images(cartella_target):
    volti_validi = []
    if not os.path.exists(cartella_target): return volti_validi
    estensioni_valide = ('.jpg', '.jpeg', '.png', '.webp')
    for file in os.listdir(cartella_target):
        if file.lower().endswith(estensioni_valide):
            percorso = os.path.join(cartella_target, file)
            volto = extract_face(percorso, is_path=True)
            if volto is not None:
                volti_validi.append(volto)
                print(f"-> Volto estratto da: {file}")
            else:
                print(f"-> ATTENZIONE: Nessun volto rilevato in {file}. Saltato.")
    return volti_validi

def calcola_somiglianza_multi_foto(elenco_volti_target, scraped_img_path):
    scraped_face = extract_face(scraped_img_path, is_path=True)
    if scraped_face is None: return None
    
    punteggi = []
    face2 = cv2.resize(scraped_face, (200, 200))
    hsv2 = cv2.cvtColor(face2, cv2.COLOR_BGR2HSV)
    
    hist2 = cv2.calcHist([hsv2], [0, 1], None, [180, 256], [0, 180, 0, 256])
    cv2.normalize(hist2, hist2, 0, 1, cv2.NORM_MINMAX)
    
    for target_face in elenco_volti_target:
        face1 = cv2.resize(target_face, (200, 200))
        hsv1 = cv2.cvtColor(face1, cv2.COLOR_BGR2HSV)
        
        hist1 = cv2.calcHist([hsv1], [0, 1], None, [180, 256], [0, 180, 0, 256])
        cv2.normalize(hist1, hist1, 0, 1, cv2.NORM_MINMAX)
        
        similarity = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)
        punteggi.append(similarity)
        
    return max(punteggi) if punteggi else 0.0

# --- PIPELINE DI SCANSIONE AD OLTRANZA ---
def start_infinite_search(elenco_volti_target, match_folder="tinder_matches", temp_folder="tinder_temp"):
    if not os.path.exists(match_folder): os.makedirs(match_folder)
    if not os.path.exists(temp_folder): os.makedirs(temp_folder)

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            args=["--disable-blink-features=AutomationControlled"]
        ) 
        
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 720},
            permissions=["geolocation"]
        )
        
        page = context.new_page()
        
        print("Apertura di Tinder...")
        page.goto("https://tinder.com")
        
        print("\n[AZIONE RICHIESTA]")
        print("1. Effettua l'accesso inserendo il codice SMS nel browser.")
        print("2. Quando sei pronto sulla schermata dei profili...")
        input("Premere INVIO in questo terminale per avvire lo scraping...")
        
        profilo_count = 0
        
        while True:
            html = page.content()
            
            # 🔍 CONTROLLO PRESENZA CAPTCHA NELL'HTML
            # Cerca elementi tipici dei framework di verifica (ArkoseLabs, FunCaptcha, iframe di verifica)
            if "arkoselabs" in html.lower() or "funcaptcha" in html.lower() or "challenge" in page.url.lower():
                gestisci_blocco_captcha()
                continue  # Salta il ciclo attuale e ricontrolla se il captcha è sparito prima di swippare
                
            profilo_count += 1
            print(f"\n---------------------------------------------")
            print(f"Analisi Profilo n° {profilo_count}...")
            
            tempo_attesa = random.uniform(2.5, 5.5)
            print(f"Attesa di sicurezza: {tempo_attesa:.2f} secondi...")
            time.sleep(tempo_attesa)
            
            soup = BeautifulSoup(html, 'html.parser')
            
            if "Trova altre persone" in html or "Nessuno nelle vicinanze" in html:
                print("\n[FINE] Tinder ha esaurito i profili nella tua zona.")
                break
            
            nome_tag = soup.find('h1', {'itemprop': 'name'})
            nome_profilo = nome_tag.get_text().strip() if nome_tag else f"Utente_{profilo_count}"
            print(f"Profilo individuato: {nome_profilo}")
            
            img_tags = soup.find_all('img')
            foto_scaricate_profilo = []
            
            for idx, img in enumerate(img_tags):
                src = img.get('src')
                if src and "://gotinder.com" in src:
                    try:
                        img_data = requests.get(src, timeout=5).content
                        file_path = os.path.join(temp_folder, f"temp_{profilo_count}_{idx}.jpg")
                        with open(file_path, 'wb') as handler:
                            handler.write(img_data)
                        foto_scaricate_profilo.append(file_path)
                    except Exception:
                        continue
            
            for foto_path in foto_scaricate_profilo:
                score = calcola_somiglianza_multi_foto(elenco_volti_target, foto_path)
                
                if score is not None:
                    print(f" -> Verifica Viso | Somiglianza Massima: {score:.2%}")
                    
                    if score > 0.78:
                        print(f" [!] MATCH TROVATO CON {nome_profilo}!")
                        nome_pulito = "".join([c for c in nome_profilo if c.isalpha() or c.isdigit() or c==' ']).rstrip()
                        nuovo_percorso = os.path.join(match_folder, f"MATCH_{nome_pulito}_{score:.0%}.jpg")
                        
                        try:
                            os.rename(foto_path, nuovo_percorso)
                            foto_path = nuovo_percorso
                        except Exception:
                            pass
                        
                        mostra_avviso_match(score, nome_profilo, foto_path)
                        
                if os.path.exists(foto_path) and match_folder not in foto_path:
                    try: os.remove(foto_path)
                    except: pass
            
            print("Passaggio al prossimo profilo...")
            page.keyboard.press("ArrowLeft")
            
        browser.close()

if __name__ == "__main__":
    CARTELLA_TARGET = "target_faces"
    print("Inizializzazione database dei volti target...")
    elenco_volti = sorted_images(CARTELLA_TARGET)
    
    if len(elenco_volti) == 0:
        print(f"Errore: Inserisci foto valide dentro la cartella '{CARTELLA_TARGET}'.")
    else:
        print(f"Database pronto. Caricati {len(elenco_volti)} volti.")
        start_infinite_search(elenco_volti)
