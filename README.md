## Setup:


1. Åben terminalen og installer relevante pip's: 

- pip3 install PyQt5
- pip3 install PyQtWebEngine
- pip3 install mysql-connecter-python
- pip3 install folium

2. Åben serverinfo.py og indsæt egen server informationer

3. Kør SharePlugDB.py I terminalen (Her importeres MySQL database til lokal mysql server)

4. Kør main.py i terminalen (SharePlug app)

## Brugermanual:

- Åben MySQL Workbench og opdatér listen "SCHEMAS" i din MySQL WorkBench og kontrollér tabellernes synlighed
- Start med at opret en bruger
- Vælg din bilmærke og tryk "vælg bil"
- Herefter ser du en liste over tilgængelige ladestationer
- Se øverst i højre hjørne knappen "maps" - Her åbnes et kort over ladestationer
- Dernæst vælg en ladestation til reservation i dropdown menuen nederst og tryk "Reservér"
- Nu får du en kvittering - Tryk dernæst på profilikonet øverst til højre (Her kan du slette samt foretage nye reservationer
- Du kan til enhver tid nu trykke på indstillingsikonet og foretage ændringer til din kundeprofil
- Gå tilbage til MySQL Workbench og tjek følgende tabeller: Bruger (Er du oprettet?), Bil (Hvilken bil har du valgt?) samt mellemleddet Reservation, og se om det stemmer overens med dine informationer

Tillykke, du har nu reserveret en ladestation passende din elbil

#### OBS: 
##### Ved uventet fejl eller problemer under kørsel af kode, er videoen "SharePlug.mov" vedlagt som ekstramateriale på WiseFlow som dokumentation. Her dokumenteres brugergrænsefladens funktionalitet. Mappen "Ressourcer" må IKKE udpakkes/udfoldes, ellers fungerer main.py ikke

