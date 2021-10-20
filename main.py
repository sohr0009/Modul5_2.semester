'''
Hvad handler vores program om?:
- Sript skal dokumentere sammenkoblingen mellem MySQL og Python
- Programmets funktioner og brug:
    1. Bruger kan oprette en profil eller logge ind
    2. Bruger skal vælge sin bilmærke
    3. Bruger tilgår ladestationer passende til den valgte bil
    4. Bruger kan reservere en ladestation

Script info:
Dev: Gruppe 2
Startdato: 28.09.2021
Sidst redigeret: 19.09.2021
'''


######### Programstruktur #########

## Importering
# Scriptets forudsætning er at relevante moduler er tilstede
import os
import sys
import datetime
from typing import Type
import mysql.connector as mc
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem, QLineEdit
from PyQt5.uic import loadUi
from serverinfo import *



## Globale variabler - Disse variabler er forhåndsdefinerede, så de kan tages i brug i interne funktioner og klasse 
DATABASE = "SharePlug"
nu = datetime.datetime.now().time()



## Main funktion - Den interaktive system start til slut
def main():

    '''Herunder defineres klasser
       Klasse betegnes som programmets visuelle vindue(r)
       Hertil Instansieres attributter og metoder
    '''

    # Forside - Her får brugeren mulighed for at logge ind eller oprette en bruger 
    class Forside(QMainWindow):
        def __init__(self):
            super(Forside, self).__init__()
            loadUi("ressourcer/Forside.ui", self)

            # Forside-vinduets knapper udpejes og kobles til funtioner
            self.loginknap.clicked.connect(self.login)                                                 # Ved at Login trykkes, forbindes en funktion hertil
            self.opretknap.clicked.connect(self.opret)                                                 # Ved at Opret trykkes, forbindes en funktion hertil

        # Loginfunktionen viderestiller brugeren til Login-vinduet
        def login(self):
            widget.addWidget(Login())
            widget.setCurrentIndex(widget.currentIndex()+1)

        # Opretfunktionen viderestiller brugeren til Oprettelses-vinduet
        def opret(self):
            widget.addWidget(Opret())
            widget.setCurrentIndex(widget.currentIndex()+1)

    # Login - Før brugeren kan logge ind, skal loginoplysninger angives
    class Login(QMainWindow):
        def __init__(self):
            super(Login, self).__init__()
            loadUi("ressourcer/loginside.ui", self)
            self.adgangskode_input.setEchoMode(QLineEdit.EchoMode.Password)                              # Indputfelt for adgangskode
            self.loginknap.clicked.connect(self.loginfunktion)                                           # Ved at 'Login' trykkes, forbindes hertil en funktion
            self.tilbageknap.clicked.connect(self.tilbage)                                               # Ved at 'Tilbage' trykkes, forbindes hertil en funktion


        # Loginfunktionen skal validere brugeren
        def loginfunktion(self):
            global Global_email                                                                          # Programmet globaliserer variablen "Global_email" for at huske brugeres indtastede email senere i programmet
            Global_email = self.email_input.text().lower()                                               # Email feltet gemmer brugerens indtastning i variablen Global_email
            adgangskode = self.adgangskode_input.text()                                                  # Det samme er gældende for adgangskode

            # Programemt definerer en forbindelse til local MySQL-server
            mydb = mc.connect(
                host=HOSTNAME,         # HOSTNAME hentes fra serverinfo.py
                user=HOSTUSER,         # HOSTUSER hentes fra serverinfo.py
                password=HOSTPASS,     # HOSTPASS hentes fra serverinfo.py
                database=DATABASE   # Det er en forudsætning, at SharePlugDB.py er eksekveret, før denne variabel kan tage effekt
                )

            cursor = mydb.cursor()                                                                       # Cursor defineres og fungerer som en pegepind - Hvis en pegepind ikke er til stede, vil programmet ikke handle på vegne af databasen
            cursor.execute('SELECT Email FROM Bruger')                                                   # For at validere brugerens eksistens, eksekveres en DQL-syntaks og alle eksisterende emailadresser fra tabellen "Bruger" hentes
            brugere = [i[0] for i in cursor.fetchall()]                                                  # Heraf oprettes variablen "brugere" - som ifølge af en for-loop og fetchall() gemmer alle eksisterende email-adresser

            # If/else statements oprettes for håndtering af login betingelser
            if len(Global_email) == 0 or len(adgangskode) == 0:                                          # Programmet kræver inputfelterne ikke efterlades tomme
                self.error.setText("Udfyld venligst alle felter")                                        # Hvis det er tilfældet, vil en fejlmeddelelse blive synlig

            elif Global_email not in brugere:                                                            # Programemt tjekker efter, om den angivne email eksisterer i bruger variablen
                self.error.setText("Bruger eksisterer ikke.")                                            # Hvis ikke, synliggøres endnu en fejlmeddelelse


            else:                                                                                         # Hvis første betingelser opfyldes betyder det, at brugeren eksisterer i databasen

                cursor.execute("SELECT Adgangskode FROM Bruger WHERE Email = '{}'".format(Global_email))  # Dernæst vil programmet gerne verificerer brugeren. Dette gøres via DQL-syntaks ved at brugeres adgangskode hentes med en WHERE clause
                result_pass = cursor.fetchone()[0]                                                        # Ved hjælp af teknikken fetchone, kan vi udplukke indhold for kolonnen "adgangskode"


                if result_pass == adgangskode:                                                            # Hvis brugerens indtastede adgangskode stemmer overens med dataet i databasen logges brugeren ind
                    print("Logger ind...")
                    self.error.setText("Du er logget ind")

                    cursor.execute("SELECT Bruger_ID FROM Bil")                                           # Programmet vil nu se efter, hvis brugeren har valgt en bil tidligere
                    registrerede_biler_liste = [i[0] for i in cursor.fetchall()]                          # Der oprettes en liste af alle registrerede biler i variablen "registrerede_biler_liste"

                    cursor.execute(f"SELECT ID FROM Bruger WHERE Email = '{Global_email}'")               # Herefter eksekveres, hvor alle brugernes ID bliver udplukket
                    for x in cursor.fetchone():
                        global bruger_ID                                                                  
                        bruger_ID = x                                                                     # Værdien gemmes i variablen "buger_ID" og globaliseres for videre brug

                    if bruger_ID in registrerede_biler_liste:                                             # Hvis brugerens ID eksisterer som fremmednøgle i bilentiteten, skal brugeren direkte viderestilles til profilsiden
                        widget.addWidget(Profil())                                                       
                        widget.setCurrentIndex(widget.currentIndex()+1)


                    else:
                        widget.addWidget(Valg_af_bil())                                                   # Hvis ikke brugerens ID eksisterer i bilentiteten, viderestilles brugeren og skal herefter vælge sin bilmærke
                        widget.setCurrentIndex(widget.currentIndex()+1)

                else:
                    self.error.setText("Forkert kodeord prøv igen")                                       # Hvis brugeren indtaster en forkert adgangskode ved login, vil en fejlmeddelelse synliggøres



        
        # Tilbagefunktionen tilbagesender brugeren til Forsiden
        def tilbage(self):
            widget.addWidget(Forside())
            widget.setCurrentIndex(widget.currentIndex()+1)

    # Profil - Brugerens profil indeholder mange funktioner relateret til brugeren herunder: Reservationer, profilindstillinger etc.
    class Profil(QMainWindow):
        def __init__(self):
            super(Profil, self).__init__()
            loadUi("ressourcer/Profil.ui", self)
            self.ny_reservation.clicked.connect(self.nyReservation)                         # Trykkes "Ny reservation", forbindes en funktion hertil
            self.slet_reserveration.clicked.connect(self.sletReservation)                   # Trykkes "Slet reservation", forbindes en funktion hertil
            self.log_ud.clicked.connect(self.logud)                                         # Trykkes "Log ud", forbindes en funktion hertil
            self.profil_indstillinger.clicked.connect(self.profilsetup)                     # Trykkes profilikonet, forbindes en funktion hertil


            # Programemt definerer en forbindelse til local MySQL-server
            mydb = mc.connect(
                host=HOSTNAME,         # HOSTNAME hentes fra serverinfo.py
                user=HOSTUSER,         # HOSTUSER hentes fra serverinfo.py
                password=HOSTPASS,     # HOSTPASS hentes fra serverinfo.py
                database=DATABASE   # Det er en forudsætning, at SharePlugDB.py er eksekveret, før denne variabel kan tage effekt
                )

            cursor = mydb.cursor()                                                                                                  # Cursor defineres og fungerer som en pegepind - Hvis en pegepind ikke er til stede, vil programmet ikke handle på vegne af databasen

            cursor.execute(f"SELECT concat(Fornavn, ' ', Efternavn) FROM `Bruger` WHERE `Email` = '{Global_email}'")                # En eksekvering defineres ud fra en DQL-syntaks og en Where Clause for indhentning af brugeres fornavn og efternavn (Concatenating)
            for navn in cursor.fetchone():                                                                                          # For-loop sørger for at gå igennem indholdet af Fetchone-teknikken og dermed udplukke indholdet uden specieltegn
                self.bruger.setText(f"{navn}")                                                                                      # Brugerens navn synliggøres profiltitlen 

            # I profilsiden, vil programmet gerne indhente oplysninger relateret til den specifikke bruger
            cursor.execute("SELECT Bil_ID FROM Reservation")                                                                        # En eksekvering foretages, for at alle Bil_ID udplukkes fra reservationstabellen
            biler_i_reservation = [i[0] for i in cursor.fetchall()]                                                                 # Dette gemmes som en liste i vatiablen "biler_i_reservation"
            cursor.execute(f"SELECT ID FROM Bruger WHERE Email = '{Global_email}'")                                                 # Endnu en eksekvering foretages, hvor brugerens ID hentes ud fra den globale email (den email ssom ystemet hidtid er kørt på) 
            for x in cursor.fetchone():                                                                                             # Forloop henter indholdet uden specialtegn
                bruger_ID = x                                                                                                       # Dette gemmes i variablen "bruger_ID"               

            cursor.execute(f"SELECT ID FROM Bil WHERE Bruger_ID = '{bruger_ID}'")                                                   # Brugeres Bil ID udplukkes og gemmes i variablen "bruger_bil"
            for x in cursor.fetchone(): 
                global bruger_bil
                bruger_bil = x



            # Hvis brugerens bil eksisterer i reservationstabellen, vises en kvittering med brugerens reservation 
            if bruger_bil in biler_i_reservation:

                cursor.execute(f"SELECT Starttidspunkt FROM Reservation WHERE Bil_ID = '{bruger_bil}'")                             
                for start in cursor.fetchone():
                    self.start.setText(f"Start: {start}")

                cursor.execute(f"SELECT Sluttidspunkt FROM Reservation WHERE Bil_ID = '{bruger_bil}'")
                for slut in cursor.fetchone():
                    self.slut.setText(f"Slut: {slut}")

                cursor.execute(f"SELECT `Ladestation_ID` FROM Reservation WHERE Bil_ID = '{bruger_bil}'")
                for x in cursor.fetchone():
                    ladestation = x


                cursor.execute(f"SELECT Adresse FROM Ladestation WHERE ID = '{ladestation}'")
                for adresse in cursor.fetchone():
                    self.adresse.setText(f"Adresse: {adresse}")



            # Hvis brugerens bil ikke eksisterer i reservationstabellen, er det lig med at brugeren har en bil men ikke en reservation
            # Herefter viderstilles brugeren til reservationsiden
            else:
                cursor.execute(f"SELECT Opladningstype FROM Bil WHERE ID = {bruger_bil}")           # Programmet udplukker brugerens biltype
                for x in cursor.fetchone():
                    biltype = x

                if biltype == 'Type2':
                    widget.addWidget(Type2())
                    widget.setCurrentIndex(widget.currentIndex()+1)

                else:
                    widget.addWidget(Type_all())
                    widget.setCurrentIndex(widget.currentIndex()+1)






        # Trykkes knappen "Ny reservation" vil progammet give brugeren denne mulighed
        def nyReservation(self):
            # Programemt definerer en forbindelse til local MySQL-server
            mydb = mc.connect(
                host=HOSTNAME,         # HOSTNAME hentes fra serverinfo.py
                user=HOSTUSER,         # HOSTUSER hentes fra serverinfo.py
                password=HOSTPASS,     # HOSTPASS hentes fra serverinfo.py
                database=DATABASE   # Det er en forudsætning, at SharePlugDB.py er eksekveret, før denne variabel kan tage effekt
                )


            cursor = mydb.cursor()                                                                                               # Cursor defineres og fungerer som en pegepind - Hvis en pegepind ikke er til stede, vil programmet ikke handle på vegne af databasen
            cursor.execute("SELECT Bil_ID FROM Reservation")
            bil_ireservationer = [i[0] for i in cursor.fetchall()]

            if bruger_bil in bil_ireservationer:
                self.error.setText("Ny reservation kan ikke foretages,  før den eksisterende slettes")


            else:
                cursor.execute(f"SELECT Opladningstype FROM Bil WHERE ID = '{bruger_bil}'")

                for x in cursor.fetchone():
                    type = x

                if type == 'Type2':

                    widget.addWidget(Type2())
                    widget.setCurrentIndex(widget.currentIndex()+1)

                else:
                    widget.addWidget(Type_all())
                    widget.setCurrentIndex(widget.currentIndex()+1)

        # Trykkes knappen "Slet reservation" vil programmet slette brugerens eksisterende reservation
        def sletReservation(self):
            # Programemt definerer en forbindelse til local MySQL-server
            mydb = mc.connect(
                host=HOSTNAME,         # HOSTNAME hentes fra serverinfo.py
                user=HOSTUSER,         # HOSTUSER hentes fra serverinfo.py
                password=HOSTPASS,     # HOSTPASS hentes fra serverinfo.py
                database=DATABASE   # Det er en forudsætning, at SharePlugDB.py er eksekveret, før denne variabel kan tage effekt
                )


            cursor = mydb.cursor()                                                                                               # Cursor defineres og fungerer som en pegepind - Hvis en pegepind ikke er til stede, vil programmet ikke handle på vegne af databasen
            cursor.execute("SELECT Bil_ID FROM Reservation")
            alle_reservationer = [i[0] for i in cursor.fetchall()]

            if bruger_bil in alle_reservationer:
                cursor.execute(f"DELETE FROM Reservation WHERE Bil_ID = '{bruger_bil}'")
                mydb.commit()
                mydb.close()
                self.noterror.setText(f"Reservation slettet: {datetime.datetime.now().strftime('%H:%M:%S')}")
                self.adresse.setText("Adresse: Ingen")
                self.start.setText("Start: Ingen")
                self.slut.setText("Slut: Ingen")


            else:
                self.error.setText("Reservation findes ikke")


        def logud(self):
            widget.addWidget(Forside())
            widget.setCurrentIndex(widget.currentIndex() + 1)


        def profilsetup(self):
            widget.addWidget(Profilsetup())
            widget.setCurrentIndex(widget.currentIndex() + 1)


    # Opret - Brugeren kan oprette en profil
    class Opret(QMainWindow):
        def __init__(self):
            super(Opret, self).__init__()
            loadUi("ressourcer/Opretside.ui", self)
            self.adgangskode_input.setEchoMode(QLineEdit.EchoMode.Password)
            self.confirmpass.setEchoMode(QLineEdit.EchoMode.Password)
            self.fortsaetknap.clicked.connect(self.fortsaet)
            self.tilbage_knap.clicked.connect(self.tilbage)


        # Opret-vinduets knapper udpejes og kobles til en funktioner
        def fortsaet(self):
            global Global_email                                                                             # Programmet globaliserer variablen "Global_email" for at kommende funktioner husker denne
            Global_email = self.email_input.text().lower()                                                  # Brugers indtastning i emailfeltet gemmes i variablen Global_email
            adgangskode = self.adgangskode_input.text()                                                     # Brugers indtastning i adgangskodefeltet gemmes i variablen adgangskode
            confirm_pass = self.confirmpass.text()                                                          # Brugers indtastning i bekræft-adgangskodefeltet gemmes i variablen confirmpass

            # Programmet definerer en forbindelse til mysql server
            mydb = mc.connect(
                host=HOSTNAME,         # HOSTNAME hentes fra serverinfo.py
                user=HOSTUSER,         # HOSTUSER hentes fra serverinfo.py
                password=HOSTPASS,     # HOSTPASS hentes fra serverinfo.py
                database=DATABASE      # DATABASE er globalt defineret - linje 38-30
            )
            cursor = mydb.cursor()                                                                          # Cursor defineres og fungerer som en pegepind - Hvis en pegepind ikke er til stede, vil programmet ikke handle på vegne af databasen



            # If/else statements oprettes for håndtering af oprettelsesbetingelser
            if len(Global_email) == 0 or len(adgangskode) == 0:                                             # Programmet kræver inputfelterne ikke efterlades tomme
                self.error.setText("Udfyld venligst alle felter")                                           # Hvis dette er tilfældet, vil en fejlmeddelelse synliggøres


            elif "@" not in Global_email:
                self.error.setText("Indtast en gyldig email")

            elif adgangskode != confirm_pass:
                self.error.setText("Adgangskode er ikke ens")                                               # Hvis indtastning af adgangskode og bekræft adgangskode ikke er ens synliggøres en fejlmeddelelse

            else:
                brugerInfo = [(Global_email, adgangskode)]                                                  # Hvis ovenstående betingelser opfyldes, gemmes brugerens info i variablen brugerInfo i form af en liste
                query = 'INSERT INTO Bruger (Email, Adgangskode) VALUES (%s,%s)'                            # Herefter defineres en DML-syntax for indsættelse af en ny rækker i Brugertabellen

                cursor.executemany(query, brugerInfo)                                                       # Herefter oprettes en pegepind rettet imod en 'mængde-eksekvering'. Ved anvendelse af denne teknik, vil eksekveringen tage udgangspunkt både SQL syntaksten og brugerInfo-variablens indhold
                mydb.commit()                                                                               # Med commit() vil databasen kunne ændres
                mydb.close()                                                                                # Dernæst slukkes forbindelsen

                print("Bruger oprettet")
                widget.addWidget(PersonligeInfo())                                                          # Viderestiller brugeren til PersonligeInfo-vinduet
                widget.setCurrentIndex(widget.currentIndex()+1)

        # Tilbagefunktionen tilbagesender brugeren til forside-vinduet
        def tilbage(self):
            widget.addWidget(Forside())
            widget.setCurrentIndex(widget.currentIndex()+1)

    # Udfyld personlige informationer
    class PersonligeInfo(QMainWindow):
        def __init__(self):
            super(PersonligeInfo, self).__init__()
            loadUi("ressourcer/PersonligeInfo.ui", self)
            self.fortsaetknap.clicked.connect(self.fortsaet)                                                # Ved at 'Fortsæt' trykkes, forbindes hertil en funktion


        # Funktionen for fortsætknappen
        def fortsaet(self):
            fornavn_input = self.fornavn_input.text().title()                                               # Inputfeltet af fornavn
            efternavn_input = self.efternavn_input.text().title()                                           # Inputfeltet af efternavn
            tlf_input = self.tlf_input.text()                                                               # Inputfeltet af telefon

            # Programmet definerer en forbindelse til mysql server
            mydb = mc.connect(
                host=HOSTNAME,         # HOSTNAME hentes fra serverinfo.py
                user=HOSTUSER,         # HOSTUSER hentes fra serverinfo.py
                password=HOSTPASS,     # HOSTPASS hentes fra serverinfo.py
                database=DATABASE      # DATABASE er globalt defineret - linje 38-30
            )

            cursor = mydb.cursor()                                                                          # Cursor defineres og fungerer som en pegepind - Hvis en pegepind ikke er til stede, vil programmet ikke handle på vegne af databasen


            # If/else statements oprettes for håndtering af betingelser
            if len(fornavn_input) == 0 or len(efternavn_input) == 0 or len(tlf_input) == 0:                 # Programmet kræver inputfelterne ikke efterlades tomme
                self.error.setText("Udfyld venligst alle felter")                                           # Hvis dette er tilfældet, vil en fejlmeddelelse synliggøres



            else:                                                                                           # Hvis ovenstående betingelser opfyldes, defineres en eksekvering om at brugerens øvrige informationer ved DML script skal opdateres baseret på tidligere variabler
                cursor.execute(f'''UPDATE `Bruger` SET
                `Fornavn` = "{fornavn_input}",
                `Efternavn` = "{efternavn_input}",
                `Telefon` = "{tlf_input}"
                WHERE `Email` = "{Global_email}"''')
                mydb.commit()                                                                               # Med commit() vil ændringer kunne foretages i databasen
                mydb.close()                                                                                # Forbindelsen afbrydes



                print("bruger opdateret")
                widget.addWidget(Valg_af_bil())                                                             # Viderstiller brugeren til valg_af_bil-vinduet
                widget.setCurrentIndex(widget.currentIndex()+1)

    # Vælg din bil - Brugeren får muligheden for at vælge sin fortrukne bil ifølge af en "Drop-down menu"
    class Valg_af_bil(QMainWindow):
        def __init__(self):
            super(Valg_af_bil, self).__init__()
            loadUi("ressourcer/Valg_af_bil.ui", self)
            self.fortsaetknap2.clicked.connect(self.fortsaet)                                               # Når 'Fortsæt' trykkes, forbindes hertil en funktion
            self.logud_knap.clicked.connect(self.logud)                                                     # Når 'Log ud' trykkes, forbindes hertil en funktion


        # Funktionen for fortsætknappen
        def fortsaet(self):
            valg_af_bil = self.combo_bil.currentText()

            if valg_af_bil == "Audi":                                                                       # Hvis brugeren vælger Audi, videresendes brugeren til Audi-vinduet
                widget.addWidget(Audi())
                widget.setCurrentIndex(widget.currentIndex()+1)

            elif valg_af_bil == "BMW":                                                                      # Hvis brugeren vælger Audi, videresendes brugeren til BMW-vinduet
                widget.addWidget(BMW())
                widget.setCurrentIndex(widget.currentIndex()+1)

            elif valg_af_bil == "Citroen":                                                                  # Hvis brugeren vælger Audi, videresendes brugeren til Citroen-vinduet
                widget.addWidget(Citroen())
                widget.setCurrentIndex(widget.currentIndex()+1)

            elif valg_af_bil == "Hyundai":                                                                  # Hvis brugeren vælger Audi, videresendes brugeren til Hyundai-vinduet
                widget.addWidget(Hyundai())
                widget.setCurrentIndex(widget.currentIndex()+1)

            elif valg_af_bil == "Mercedes":                                                                 # Hvis brugeren vælger Audi, videresendes brugeren til Mercedes-vinduet
                widget.addWidget(Mercedes())
                widget.setCurrentIndex(widget.currentIndex()+1)

            elif valg_af_bil == "Toyota":                                                                   # Hvis brugeren vælger Audi, videresendes brugeren til Toyota-vinduet
                widget.addWidget(Toyota())
                widget.setCurrentIndex(widget.currentIndex()+1)

        # Funktionen for logudknappen
        def logud(self):
            widget.addWidget(Forside())
            widget.setCurrentIndex(widget.currentIndex()+1)


    '''Herunder udvalgte biler opstillet
       Disse vinduer har til formål at tilknytte bilen til brugeren
       Kun klassen Audi er kommenteret, og øvrige biler undladt, da programstrukturets grundlæggende funktioner er identiske
    '''

    class Audi(QMainWindow):

        def __init__(self):
            super(Audi, self).__init__()
            loadUi("ressourcer/Audi.ui", self)
            self.done_knap.clicked.connect(self.faerdig)                                                    # Trykkes 'Færdig', forbindes hertil en funktion
            self.tilbageknap.clicked.connect(self.tilbage)                                                  # Trykkes 'Tilbage', forbindes hertil en funktion


        # Tilbagefunktionen tilbagesendes brugeren til valg af bil
        def tilbage(self):
            widget.addWidget(Valg_af_bil())
            widget.setCurrentIndex(widget.currentIndex()+1)


        # Færdigfunktionen sættes samtlige processer igang
        def faerdig(self):
            # Programmet definerer en forbindelse til mysql server
            mydb = mc.connect(
                host=HOSTNAME,         # HOSTNAME hentes fra serverinfo.py
                user=HOSTUSER,         # HOSTUSER hentes fra serverinfo.py
                password=HOSTPASS,     # HOSTPASS hentes fra serverinfo.py
                database=DATABASE      # DATABASE er globalt defineret - linje 38-30
            )

            cursor = mydb.cursor()                                                                         # Cursor defineres og fungerer som en pegepind - Hvis en pegepind ikke er til stede, vil programmet ikke handle på vegne af databasen
            cursor.execute("SELECT `ID` FROM `Bruger` WHERE `Email` = '{}'".format(Global_email))          # En eksekvering defineres ud fra en DQL-syntaks og en Where Clause for indhentning af brugeres 'ID'
            for value in cursor.fetchone():                                                                # For-loop sørger for at gå igennem indholdet af Fetchone-teknikken og dermed udplukke tallet dvs "1" og ikke ("1")
                brugerID = value                                                                           # Værdien gemmes i variablen brugerID


            cursor.execute(f"INSERT INTO `Bil` (`Mærke`, `Model`, `Opladningstype`, `Bruger_ID`) VALUES ('Audi','A3', 'Type2', {brugerID})")   # Programmet indsætter en ny række i Bil tabellen. Den fortrukne bil tilføjes tabllen med brugerens ID

            mydb.commit()                                                                                  # Med commit() vil ændringer kunne foretages i databasen
            mydb.close()                                                                                   # Forbindelsen afbrydes


            widget.addWidget(Type2())                                                                      # Viderstiller brugeren til vinduet Type2 (Ladestandere for kun Type 2 plug)
            widget.setCurrentIndex(widget.currentIndex()+1)

            print("Bil tilføjet")

    class BMW(QMainWindow):

        def __init__(self):
            super(BMW, self).__init__()
            loadUi("ressourcer/BMW.ui", self)
            self.done_knap.clicked.connect(self.faerdig)
            self.tilbageknap.clicked.connect(self.tilbage)



        def tilbage(self):
            widget.addWidget(Valg_af_bil())
            widget.setCurrentIndex(widget.currentIndex()+1)


        def faerdig(self):
            mydb = mc.connect(host=HOSTNAME, user=HOSTUSER, password=HOSTPASS, database=DATABASE)
            cursor = mydb.cursor()

            cursor.execute("SELECT `ID` FROM `Bruger` WHERE `Email` = '{}'".format(Global_email))
            for value in cursor.fetchone():
                brugerID = value


            ## Nåede hertil
            cursor.execute("INSERT INTO `Bil` (`Mærke`, `Model`, `Opladningstype`, `Bruger_ID`) VALUES ('BMW','225xe', 'Type2', {})".format(brugerID))

            mydb.commit()
            mydb.close()


            widget.addWidget(Type2())
            widget.setCurrentIndex(widget.currentIndex()+1)

            print("Bil tilføjet")

    class Citroen(QMainWindow):
        def __init__(self):
            super(Citroen, self).__init__()
            loadUi("ressourcer/Citroen.ui", self)
            self.done_knap.clicked.connect(self.faerdig)
            self.tilbageknap.clicked.connect(self.tilbage)



        def tilbage(self):
            widget.addWidget(Valg_af_bil())
            widget.setCurrentIndex(widget.currentIndex()+1)


        def faerdig(self):
            mydb = mc.connect(host=HOSTNAME, user=HOSTUSER, password=HOSTPASS, database=DATABASE)
            cursor = mydb.cursor()

            cursor.execute("SELECT `ID` FROM `Bruger` WHERE `Email` = '{}'".format(Global_email))
            for value in cursor.fetchone():
                brugerID = value


            ## Nåede hertil
            cursor.execute("INSERT INTO `Bil` (`Mærke`, `Model`, `Opladningstype`, `Bruger_ID`) VALUES ('Citroën','C-Zero', 'Type2', {})".format(brugerID))

            mydb.commit()
            mydb.close()


            widget.addWidget(Type2())
            widget.setCurrentIndex(widget.currentIndex()+1)

            print("Bil tilføjet")

    class Hyundai(QMainWindow):
        def __init__(self):
            super(Hyundai, self).__init__()
            loadUi("ressourcer/Hyundai.ui", self)
            self.done_knap.clicked.connect(self.faerdig)
            self.tilbageknap.clicked.connect(self.tilbage)



        def tilbage(self):
            widget.addWidget(Valg_af_bil())
            widget.setCurrentIndex(widget.currentIndex()+1)

        def faerdig(self):
            mydb = mc.connect(host=HOSTNAME, user=HOSTUSER, password=HOSTPASS, database=DATABASE)
            cursor = mydb.cursor()

            cursor.execute("SELECT `ID` FROM `Bruger` WHERE `Email` = '{}'".format(Global_email))
            for value in cursor.fetchone():
                brugerID = value


            ## Nåede hertil
            cursor.execute("INSERT INTO `Bil` (`Mærke`, `Model`, `Opladningstype`, `Bruger_ID`) VALUES ('Hyundai','IONIQ5', 'CHAdeMO', {})".format(brugerID))

            mydb.commit()
            mydb.close()


            widget.addWidget(Type_all())
            widget.setCurrentIndex(widget.currentIndex()+1)

            print("Bil tilføjet")

    class Mercedes(QMainWindow):
        def __init__(self):
            super(Mercedes, self).__init__()
            loadUi("ressourcer/Mercedes.ui", self)
            self.done_knap.clicked.connect(self.faerdig)
            self.tilbageknap.clicked.connect(self.tilbage)



        def tilbage(self):
            widget.addWidget(Valg_af_bil())
            widget.setCurrentIndex(widget.currentIndex()+1)


        def faerdig(self):
            mydb = mc.connect(host=HOSTNAME, user=HOSTUSER, password=HOSTPASS, database=DATABASE)
            cursor = mydb.cursor()

            cursor.execute("SELECT `ID` FROM `Bruger` WHERE `Email` = '{}'".format(Global_email))
            for value in cursor.fetchone():
                brugerID = value


            ## Nåede hertil
            cursor.execute("INSERT INTO `Bil` (`Mærke`, `Model`, `Opladningstype`, `Bruger_ID`) VALUES ('Mercedes','A250e', 'Type2', {})".format(brugerID))

            mydb.commit()
            mydb.close()


            widget.addWidget(Type2())
            widget.setCurrentIndex(widget.currentIndex()+1)

            print("Bil tilføjet")

    class Toyota(QMainWindow):
        def __init__(self):
            super(Toyota, self).__init__()
            loadUi("ressourcer/Toyota.ui", self)
            self.done_knap.clicked.connect(self.faerdig)
            self.tilbageknap.clicked.connect(self.tilbage)



        def tilbage(self):
            widget.addWidget(Valg_af_bil())
            widget.setCurrentIndex(widget.currentIndex()+1)


        def faerdig(self):
            mydb = mc.connect(host=HOSTNAME, user=HOSTUSER, password=HOSTPASS, database=DATABASE)
            cursor = mydb.cursor()

            cursor.execute("SELECT `ID` FROM `Bruger` WHERE `Email` = '{}'".format(Global_email))
            for value in cursor.fetchone():
                brugerID = value


            ## Nåede hertil
            cursor.execute(f"INSERT INTO `Bil` (`Mærke`, `Model`, `Opladningstype`, `Bruger_ID`) VALUES ('Toyota','Prius', 'Type2', {brugerID})")

            mydb.commit()
            mydb.close()


            widget.addWidget(Type2())
            widget.setCurrentIndex(widget.currentIndex()+1)

            print("Bil tilføjet")

    '''
    Herunder defineres vinduer som skal vise tilgængelige ladestandere for forskellige plug-in biler.
    Dernæst har disse vinduer funtionaliteten for reservationsprocessen.
    Det tilgængeliggøres for brugeren at tilgå Leaflet (Google maps), hvor ladestandere ses over et geografisk kort.
    Klassen Type2 og Type_all er identisk opbygget, så Type2 er kun kommeteret
    '''

    # Ladestandere for Type2 plugs
    class Type2(QMainWindow):
        def __init__(self):
            super(Type2, self).__init__()
            loadUi("ressourcer/Type2.ui", self)
            self.tableWidget.setColumnWidth(0,30)
            self.tableWidget.setColumnWidth(1,70)
            self.tableWidget.setColumnWidth(2,70)
            self.tableWidget.setColumnWidth(3,70)
            self.tableWidget.setColumnWidth(4,210)
            self.reserver.clicked.connect(self.reservation)                                                   # Trykkes 'Reservér', forbindes en funktion hertil
            self.tilbageknap.clicked.connect(self.tilbage)                                                    # Trykkes 'Afslut', forbindes en funktion hertil
            self.maps.clicked.connect(self.open_maps)                                                         # Trykkes på ikonet 'Maps', forbindes en funktion hertil



            # Programmet definerer en forbindelse til mysql server
            mydb = mc.connect(
                host=HOSTNAME,         # HOSTNAME hentes fra serverinfo.py
                user=HOSTUSER,         # HOSTUSER hentes fra serverinfo.py
                password=HOSTPASS,     # HOSTPASS hentes fra serverinfo.py
                database=DATABASE      # DATABASE er globalt defineret - linje 38-30
            )

            cursor = mydb.cursor()                                                                            # Cursor defineres og fungerer som en pegepind - Hvis en pegepind ikke er til stede, vil programmet ikke handle på vegne af databasen
            #cursor.execute('SELECT concat("" + ID + "") FROM Ladestation where Opladningstype = "Type2"')
            cursor.execute("SELECT ID FROM Ladestation where Type = 'Type2'")
            ladestationer_INT = [i[0] for i in cursor.fetchall()]
            ladestationer = [str(x) for x in ladestationer_INT]                                               # Konvertering fra INT til STR

            for x in ladestationer:
                self.ladestander_id.addItem(x)


            cursor.execute("SELECT * FROM Ladestation where Type = 'Type2'")                                                                                                 # Ved fetchall-teknikken udplukkes de specifikke ladestandere og gemmes i variablen 'ladestandere'
            self.tableWidget.setRowCount(0)

            for row_number, row_data in enumerate(cursor.fetchall()):                                           # Ved anvendelse af en For-loop vil antal rækker og rækkeindhold tælles
                self.tableWidget.insertRow(row_number)                                                          # Disse indsættes i den visuelle tabel

                for column_number, data in enumerate(row_data):                                                 # Dernæst udplukkes kolonners længde og kolonners indhold
                    self.tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data)))            # Disse indsættes i den visuelle tabel

        # Reservationsfunktionen - Brugerens valg gemmes i tabellen 'Reservation'
        def reservation(self):
            ladestation_combobox = self.ladestander_id.currentText()                                                                              # Variablen ladestanderID globaliseres, den er placeret uden for funktionen. Programmet vil gemme nyt data undervejs
            Startidspunkt = datetime.datetime.now().strftime('%H:%M:%S')                                                                          # Starttidspunkt defineres udfra systemets lokale tid ved brug af 'Datetime'-modulet
            Sluttidspunkt = (datetime.datetime.combine(datetime.date(1,1,1), nu) + datetime.timedelta(hours = 1)).time().strftime('%H:%M:%S')     # Sluttidspunkt defineres som resultat af starttidspunkt + delta (Delta er = 1 time, da reservatinen vil udløbe efterfølgende)

            # Programemt definerer en forbindelse til local MySQL-server
            mydb = mc.connect(
                host=HOSTNAME,         # HOSTNAME hentes fra serverinfo.py
                user=HOSTUSER,         # HOSTUSER hentes fra serverinfo.py
                password=HOSTPASS,     # HOSTPASS hentes fra serverinfo.py
                database=DATABASE   # Det er en forudsætning, at SharePlugDB.py er eksekveret, før denne variabel kan tage effekt
                )


            cursor = mydb.cursor()                                                                            # Cursor defineres og fungerer som en pegepind - Hvis en pegepind ikke er til stede, vil programmet ikke handle på vegne af databasen

            cursor.execute('SELECT concat("" + Ladestation_ID + "") FROM Reservation')
            Reserverede_ladestationer = [i[0] for i in cursor.fetchall()]

            if ladestation_combobox in Reserverede_ladestationer:

                self.error.setText("Ladestander er i brug")

            else:
                for value in [int(x) for x in ladestation_combobox]:
                    global ladestationID
                    ladestationID = value


                cursor.execute(f"SELECT `ID` FROM `Bruger` WHERE `Email` = '{Global_email}'")                # En eksekvering defineres ud fra en DQL-syntaks og en Where Clause for indhentning af brugeres 'ID' ved den hidtil brugte email (Dvs. systemets bruger)
                for value in cursor.fetchone():                                                              # For-loop sørger for at gå igennem indholdet af Fetchone-teknikken og dermed udplukke tallet dvs "1" og ikke ("1")
                    brugerID = value                                                                         # Værdien gemmes i variablen brugerID

                # Nu vil vi gerne udtrække bilens ID som er knyttet til den specifikke bruger
                cursor.execute(f"SELECT `ID` FROM `Bil` WHERE `Bruger_ID` = '{brugerID}'")                     # En eksekvering defineres ud fra en DQL-syntaks og en Where Clause for indhentning af brugeres valgte bil
                for value in cursor.fetchone():
                    Bil_ID = value

                cursor.execute(f"INSERT INTO `Reservation` (Ladestation_ID, Bil_ID, Starttidspunkt, Sluttidspunkt) VALUES ({ladestationID}, {Bil_ID}, '{Startidspunkt}', '{Sluttidspunkt}')")

                mydb.commit()                                                                                  # Med commit() vil ændringer kunne foretages i databasen
                mydb.close()                                                                                   # Forbindelsen afbrydes

                print(f"Ladestander '{ladestation_combobox}' reserveret")

                widget.addWidget(Kvittering())                                                                 # Brugeren viderestilles til kvitterings-vinduet
                widget.setCurrentIndex(widget.currentIndex()+1)

        def tilbage(self):
            widget.addWidget(Profil())                                                                         # Brugeren tilbagesendes til profil
            widget.setCurrentIndex(widget.currentIndex()+1)


        def open_maps(self):                                                                                   # Programemt åbner filen leafletMaps.py fra mappen "ressourcer"

            os.system('python3 ressourcer/leafletMaps.py')

    # Ladestationer for alle typer af plugs
    class Type_all(QMainWindow):
        def __init__(self):
            super(Type_all, self).__init__()
            loadUi("ressourcer/Type_all.ui", self)
            self.tableWidget.setColumnWidth(0,30)
            self.tableWidget.setColumnWidth(1,70)
            self.tableWidget.setColumnWidth(2,70)
            self.tableWidget.setColumnWidth(3,70)
            self.tableWidget.setColumnWidth(4,210)
            self.reserver.clicked.connect(self.reservation)                                                   # Trykkes 'Reservér', forbindes en funktion hertil
            self.tilbageknap.clicked.connect(self.tilbage)                                                    # Trykkes 'tilbage', forbindes en funktion hertil
            self.maps.clicked.connect(self.open_maps)                                                         # Trykkes på ikonet 'Maps', forbindes en funktion hertil

            # Programemt definerer en forbindelse til local MySQL-server
            mydb = mc.connect(
                host=HOSTNAME,         # HOSTNAME hentes fra serverinfo.py
                user=HOSTUSER,         # HOSTUSER hentes fra serverinfo.py
                password=HOSTPASS,     # HOSTPASS hentes fra serverinfo.py
                database=DATABASE   # Det er en forudsætning, at SharePlugDB.py er eksekveret, før denne variabel kan tage effekt
                )


            cursor = mydb.cursor()                                                                            # Cursor defineres og fungerer som en pegepind - Hvis en pegepind ikke er til stede, vil programmet ikke handle på vegne af databasen
            cursor.execute("SELECT ID FROM Ladestation")
            ladestationer_INT = [i[0] for i in cursor.fetchall()]
            ladestationer = [str(x) for x in ladestationer_INT]                                               # Konvertering fra INT til STR

            for x in ladestationer:
                self.ladestander_id.addItem(x)


            cursor.execute("SELECT * FROM Ladestation")                                                       # Ved fetchall-teknikken udplukkes de specifikke ladestandere og gemmes i variablen 'ladestandere'
            self.tableWidget.setRowCount(0)

            for row_number, row_data in enumerate(cursor.fetchall()):                                         # Ved anvendelse af en For-loop vil antal rækker og rækkeindhold tælles
                self.tableWidget.insertRow(row_number)                                                        # Disse indsættes i den visuelle tabel

                for column_number, data in enumerate(row_data):                                               # Dernæst udplukkes kolonners længde og kolonners indhold
                    self.tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data)))          # Disse indsættes i den visuelle tabel

        # Reservationsfunktionen - Brugerens valg gemmes i tabellen 'Reservation'
        def reservation(self):
            ladestation_combobox = self.ladestander_id.currentText()                                                        # Variablen ladestanderID globaliseres, den er placeret uden for funktionen. Programmet vil gemme nyt data undervejs
            Startidspunkt = datetime.datetime.now().strftime('%H:%M:%S')                                                    # Starttidspunkt defineres udfra systemets lokale tid ved brug af 'Datetime'-modulet
            Sluttidspunkt = (datetime.datetime.combine(datetime.date(1,1,1), nu) + datetime.timedelta(hours = 1)).time().strftime('%H:%M:%S')     # Sluttidspunkt defineres som resultat af starttidspunkt + delta (Delta er = 1 time, da reservatinen vil udløbe efterfølgende)


            # Programemt definerer en forbindelse til local MySQL-server
            mydb = mc.connect(
                host=HOSTNAME,         # HOSTNAME hentes fra serverinfo.py
                user=HOSTUSER,         # HOSTUSER hentes fra serverinfo.py
                password=HOSTPASS,     # HOSTPASS hentes fra serverinfo.py
                database=DATABASE   # Det er en forudsætning, at SharePlugDB.py er eksekveret, før denne variabel kan tage effekt
                )

        
            cursor = mydb.cursor()                                                                                          # Cursor defineres og fungerer som en pegepind - Hvis en pegepind ikke er til stede, vil programmet ikke handle på vegne af databasen

            cursor.execute('SELECT concat("" + Ladestation_ID + "") FROM Reservation')
            Reserverede_ladestationer = [i[0] for i in cursor.fetchall()]

            if ladestation_combobox in Reserverede_ladestationer:
                self.error.setText("Ladestation er i brug")

            else:
                for value in [int(x) for x in ladestation_combobox]:
                    global ladestationID
                    ladestationID = value


                cursor.execute(f"SELECT `ID` FROM `Bruger` WHERE `Email` = '{Global_email}'")                # En eksekvering defineres ud fra en DQL-syntaks og en Where Clause for indhentning af brugeres 'ID' ved den hidtil brugte email (Dvs. systemets bruger)
                for value in cursor.fetchone():                                                              # For-loop sørger for at gå igennem indholdet af Fetchone-teknikken og dermed udplukke tallet dvs "1" og ikke ("1")
                    brugerID = value                                                                         # Værdien gemmes i variablen brugerID

                cursor.execute(f"SELECT `ID` FROM `Bil` WHERE `Bruger_ID` = '{brugerID}'")                     # En eksekvering defineres ud fra en DQL-syntaks og en Where Clause for indhentning af brugeres valgte bil
                for value in cursor.fetchone():
                    Bil_ID = value

                cursor.execute(f"INSERT INTO `Reservation` (Ladestation_ID, Bil_ID, Starttidspunkt, Sluttidspunkt) VALUES ({ladestationID}, {Bil_ID}, '{Startidspunkt}', '{Sluttidspunkt}')")
                mydb.commit()                                                                                  # Med commit() vil ændringer kunne foretages i databasen
                mydb.close()                                                                                   # Forbindelsen afbrydes

                print(f"Ladestander '{ladestation_combobox}' reserveret")

                widget.addWidget(Kvittering())                                                                 # Brugeren viderestilles til kvitterings-vinduet
                widget.setCurrentIndex(widget.currentIndex()+1)

        def tilbage(self):
            widget.addWidget(Profil())                                                                         # Brugeren tilbagesendes til profil
            widget.setCurrentIndex(widget.currentIndex()+1)


        def open_maps(self):

            os.system('python3 ressourcer/leafletMaps.py')



    class Kvittering(QMainWindow):
        def __init__(self):
            super(Kvittering, self).__init__()
            loadUi("ressourcer/Kvittering.ui", self)
            self.afslutknap.clicked.connect(self.afslutapp)                                               # Trykkes 'Afslut', forbindes en funktion hertil
            self.log_ud.clicked.connect(self.logud)
            self.profil_indstillinger.clicked.connect(self.go_til_profil)

            # Programemt definerer en forbindelse til local MySQL-server
            mydb = mc.connect(
                host=HOSTNAME,         # HOSTNAME hentes fra serverinfo.py
                user=HOSTUSER,         # HOSTUSER hentes fra serverinfo.py
                password=HOSTPASS,     # HOSTPASS hentes fra serverinfo.py
                database=DATABASE   # Det er en forudsætning, at SharePlugDB.py er eksekveret, før denne variabel kan tage effekt
                )


            cursor = mydb.cursor()                                                                         # Cursor defineres og fungerer som en pegepind - Hvis en pegepind ikke er til stede, vil programmet ikke handle på vegne af databasen

            # En kvittering oprettes med følgende informationer af reservationen
            cursor.execute(f"SELECT concat(Fornavn, ' ', Efternavn) FROM `Bruger` WHERE `Email` = '{Global_email}'")             # En eksekvering defineres ud fra en DQL-syntaks og en Where Clause for indhentning af brugeres 'Fornavn'
            for x in cursor.fetchone():                                                                    # For-loop sørger for at gå igennem indholdet af Fetchone-teknikken og dermed udplukke indholdet uden specieltegn
                self.bruger.setText(f"Bruger: {x}")



            cursor.execute(f"SELECT Adresse FROM Ladestation WHERE ID = '{ladestationID}'")      # Variablen 'adresse' definerer eksekveringen ud fra en DQL-syntaks og en Where Clause for indhentning af ladestanderens 'Adresse'
            for x in cursor.fetchone():                                                                    # For-loop sørger for at gå igennem indholdet af Fetchone-teknikken og dermed udplukke indholdet uden specieltegn
                self.adresse.setText(f"Adresse: {x}")


            Startidspunkt = datetime.datetime.now().strftime('%H:%M:%S')                                                                      # Starttidspunkt defineres udfra systemets lokale tid ved brug af 'Datetime'-modulet
            Sluttidspunkt = (datetime.datetime.combine(datetime.date(1,1,1), nu) + datetime.timedelta(hours = 1)).time().strftime('%H:%M:%S') # Sluttidspunkt defineres ud fra starttidspunkt + delta (Delta er = 1 time, da reservatinen vil udløbe efterfølgende)
            self.start.setText(f"Start: {Startidspunkt}")
            self.slut.setText(f"Slut: {Sluttidspunkt}")


        def afslutapp(self):
            exit()

        def logud(self):
            widget.addWidget(Forside())
            widget.setCurrentIndex(widget.currentIndex()+1)

        def go_til_profil(self):
            widget.addWidget(Profil())
            widget.setCurrentIndex(widget.currentIndex()+1)


    class Profilsetup(QMainWindow):
        def __init__(self):
            super(Profilsetup, self).__init__()
            loadUi("ressourcer/profilsetup.ui", self)
            self.opdater.clicked.connect(self.opdaterprofil)
            self.tilbage.clicked.connect(self.tilbagetilprofil)
            self.slet_profil.clicked.connect(self.slet)


            # Programemt definerer en forbindelse til local MySQL-server
            mydb = mc.connect(
                host=HOSTNAME,         # HOSTNAME hentes fra serverinfo.py
                user=HOSTUSER,         # HOSTUSER hentes fra serverinfo.py
                password=HOSTPASS,     # HOSTPASS hentes fra serverinfo.py
                database=DATABASE   # Det er en forudsætning, at SharePlugDB.py er eksekveret, før denne variabel kan tage effekt
                )

            cursor = mydb.cursor()
            cursor.execute(f"SELECT concat(Fornavn, ' ', Efternavn) FROM Bruger WHERE Email = '{Global_email}'")
            for x in cursor.fetchone():
                self.bruger.setText(f"{x}")


        def opdaterprofil(self):
            input = self.input_vaerdi.text()

            # Programemt definerer en forbindelse til local MySQL-server
            mydb = mc.connect(
                host=HOSTNAME,         # HOSTNAME hentes fra serverinfo.py
                user=HOSTUSER,         # HOSTUSER hentes fra serverinfo.py
                password=HOSTPASS,     # HOSTPASS hentes fra serverinfo.py
                database=DATABASE   # Det er en forudsætning, at SharePlugDB.py er eksekveret, før denne variabel kan tage effekt
                )

            cursor = mydb.cursor()

            cursor.execute(f"SELECT concat(Fornavn, ' ', Efternavn) FROM Bruger WHERE Email = '{Global_email}'")
            for x in cursor.fetchone():
                self.bruger.setText(f"{x}")

            if self.fornavn_radio.isChecked():
                cursor.execute(f"UPDATE Bruger SET Fornavn = '{input.title()}' WHERE Email = '{Global_email}'")
                mydb.commit()

                cursor.execute(f"SELECT concat(Fornavn, ' ', Efternavn) FROM Bruger WHERE Email = '{Global_email}'")
                for x in cursor.fetchone():
                    self.bruger.setText(f"{x.title()}")
                self.noterror.setText("Fornavn opdateret")


            elif self.efternavn_radio.isChecked():
                cursor.execute(f"UPDATE Bruger SET Efternavn = '{input.title()}' WHERE Email = '{Global_email}'")
                mydb.commit()
                cursor.execute(f"SELECT concat(Fornavn, ' ', Efternavn) FROM Bruger WHERE Email = '{Global_email}'")
                for x in cursor.fetchone():
                    self.bruger.setText(f"{x.title()}")
                self.noterror.setText("Efternavn opdateret")

            elif self.adgangskode_radio.isChecked():
                cursor.execute(f"UPDATE Bruger SET Adgangskode = '{input}' WHERE Email = '{Global_email}'")
                mydb.commit()
                self.noterror.setText("Adgangskode opdateret")

            elif self.tlf_radio.isChecked():
                cursor.execute(f"UPDATE Bruger SET Telefon = '{input}' WHERE Email = '{Global_email}'")
                mydb.commit()
                self.noterror.setText("Telefon nr. opdateret")

            mydb.close()


        def slet(self):

            # Programemt definerer en forbindelse til local MySQL-server
            mydb = mc.connect(
                host=HOSTNAME,         # HOSTNAME hentes fra serverinfo.py
                user=HOSTUSER,         # HOSTUSER hentes fra serverinfo.py
                password=HOSTPASS,     # HOSTPASS hentes fra serverinfo.py
                database=DATABASE   # Det er en forudsætning, at SharePlugDB.py er eksekveret, før denne variabel kan tage effekt
                )

            cursor = mydb.cursor()
            cursor.execute(f"SELECT ID FROM Bruger WHERE Email = '{Global_email}'")
            for x in cursor.fetchone():
                bruger_ID = x


            cursor.execute(f"DELETE FROM Reservation WHERE Bil_ID = {bruger_bil} ")
            cursor.execute(f"DELETE FROM Bil WHERE Bruger_ID = {bruger_ID} ")
            cursor.execute(f"DELETE FROM Bruger WHERE Email = '{Global_email}' ")
            mydb.commit()
            mydb.close()
            print(f"Bruger: {Global_email} er nu slettet")
            widget.addWidget(Forside())                                                                 # Brugeren viderestilles til forside
            widget.setCurrentIndex(widget.currentIndex()+1)


        def tilbagetilprofil(self):
            widget.addWidget(Profil())                                                                 # Brugeren tilbagesendes til deres profil
            widget.setCurrentIndex(widget.currentIndex()+1)

    ################ APP indstillinger ################## 
    app = QApplication(sys.argv)
    mainWindow=Forside()
    widget = QtWidgets.QStackedWidget()
    widget.addWidget(mainWindow)
    widget.setFixedWidth(500)
    widget.setFixedHeight(800)
    widget.setWindowTitle("SharePlug")
    widget.show()
    app.exec()
    ################ APP indstillinger ##################

main()
