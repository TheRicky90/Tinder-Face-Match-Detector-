# Tinder Face Match Detector 🕵️‍♂️🔥

[English version below] | [Versione Italiana sotto]

---

## 🇺🇸 English Version

An automated Python application designed for real-time scraping and biometric analysis of suggested Tinder profiles. The software compares the faces of suggested users with a local database of target photos (Multi-Photo support), triggers an on-screen pop-up alert upon a successful match, and archives the results in an organized folder structure.

### ✨ Features
- **Multi-Photo Analysis:** Supports loading multiple images of the target subject to increase recognition accuracy across different lighting conditions, angles, and facial expressions.
- **Real-Time Detection:** Instantly downloads, analyzes, and purges the image cache profile-by-profile during navigation to optimize storage space.
- **Anti-Ban Protections:** Integrates human-like randomized swipe intervals (`2.5s - 5.5s`) and strips browser automation indicators (`AutomationControlled`).
- **Intelligent CAPTCHA Handling:** Detects human verification blocks (such as ArkoseLabs/FunCaptcha) or challenge URLs. The system triggers an acoustic system alert (Beep) and pauses execution, allowing you to solve it manually in the browser window before resuming without crashes.
- **Automatic Resume:** Match notification pop-ups do not terminate the loop; as soon as you dismiss the alert, the script resumes swiping automatically.

### 🛠️ Prerequisites & Installation

Ensure you have [Python](https://python.org) installed on Windows and added to your system environment variables (PATH).

1. Clone or download this repository to your computer.
2. Open your Command Prompt (or PowerShell) inside the project folder and install the dependencies using the explicit Python execution flag to avoid PATH errors:
   ```bash
   python -m pip install playwright opencv-python pillow requests beautifulsoup4
   ```
3. Install the required browser binaries for Playwright automation:
   ```bash
   python -m playwright install
   ```

### 🚀 How to Use It

1. Create a folder named `target_faces` in the root directory of the project.
2. Put the pictures of the person you are looking for inside the `target_faces` folder.
3. Manually download the OpenCV model file (haarcascade_frontalface_default.xml) is already included in the repository root.
4. Run the script from the terminal:
   ```bash
   python tinder_scraper.py
   ```
5. Log in manually via SMS verification in the opened browser window. Once you are on the main profile deck screen, return to the terminal and press **Enter**.

---

## 🇮🇹 Versione Italiana

Un'applicazione in Python progettata per automatizzare lo scraping e l'analisi biometrica in tempo reale dei profili di Tinder. Il software confronta i volti dei profili suggeriti con un database locale di foto target (Multi-Foto), inviando notifiche su schermo in caso di corrispondenza e archiviando i risultati in modo ordinato.

### ✨ Funzionalità
- **Analisi Multi-Foto:** Supporta il caricamento di più immagini del soggetto per aumentare l'accuratezza del riconoscimento facciale basandosi sulle variazioni di luce e angolazione.
- **Rilevamento in Tempo Reale:** Scarica, analizza e pulisce la cache istantaneamente profilo per profilo durante la navigazione.
- **Tecniche Anti-Ban:** Integra tempi di swipe casuali (`2.5s - 5.5s`) ed esclude i flag di automazione del browser (`AutomationControlled`).
- **Gestione CAPTCHA Intelligente:** Rileva la comparsa di blocchi di verifica visiva (ArkoseLabs/FunCaptcha) o cambi di URL di verifica. Il sistema attiva un segnale acustico (Beep) di allerta e sospende temporaneamente lo scraping per consentire la risoluzione manuale nel browser, riprendendo poi l'esecuzione senza far crashare il programma.
- **Ripresa Automatica (Resume):** I pop-up di notifica dei match non bloccano il ciclo; alla chiusura dell'avviso, lo script prosegue autonomamente.

### 🛠️ Requisiti e Installazione

Assicurati di avere [Python](https://python.org) installato su Windows e configurato nelle variabili d'ambiente (PATH).

1. Clona o scarica questa repository sul tuo computer.
2. Apri il Prompt dei comandi (o PowerShell) all'interno della cartella del progetto ed esegui l'installazione delle dipendenze utilizzando l'esecutore esplicito di Python per evitare errori di PATH:
   ```bash
   python -m pip install playwright opencv-python pillow requests beautifulsoup4
   ```
3. Installa i binari dei browser necessari per l'automazione richiamando Playwright tramite il modulo Python:
   ```bash
   python -m playwright install
   ```

### 🚀 Come Utilizzarlo

1. Crea una cartella denominata `target_faces` nella directory principale del progetto.
2. Inserisci all'interno di `target_faces` le immagini della persona che stai cercando.
3. Il modello di OpenCV necessario (haarcascade_frontalface_default.xml) è già incluso nella cartella principale della repository.
4. Avvia lo script da terminale:
   ```bash
   python tinder_scraper.py
   ```
5. Esegui il login manuale tramite SMS nella finestra del browser che si aprirà. Quando sei sulla schermata dei profili da scorrere, torna sul terminale e premi **Invio**.

---

## 📜 Open Source Credits & Resources / Crediti

This project was made possible by combining the following open-source libraries / Questo progetto è stato realizzato unendo le seguenti librerie open-source:

*   **[OpenCV](https://opencv.org)** (*Apache 2.0*) - Image processing, HSV histogram extractions, and Cascade Classifier face tracking / Elaborazione d'immagine, estrazione istogrammi HSV e tracking facciale.
*   **[Playwright for Python](https://playwright.dev)** (*Apache 2.0*) - Web navigation automation and JavaScript execution / Automazione della navigazione ed esecuzione JavaScript.
*   **[BeautifulSoup4](https://crummy.com)** (*MIT*) - HTML parsing and image URL extraction / Parsing del DOM HTML ed estrazione URL.
*   **[Pillow](https://python-pillow.org)** (*HPND*) - Image format support handler / Gestione e supporto dei formati d'immagine.
*   **[Requests](https://readthedocs.io)** (*Apache 2.0*) - Secure binary stream download from Tinder CDN / Download sicuro dei flussi binari dal CDN di Tinder.

*Disclaimer: This project was developed strictly for educational purposes regarding web automation and computer vision. Use at your own discretion in compliance with the platform's Terms of Service.*  
*Nota: Questo progetto è stato sviluppato a puro scopo di studio tecnico. L'utilizzo deve rispettare i Termini di Servizio della piattaforma.*
