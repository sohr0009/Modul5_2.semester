# Dette python script importerer Clever databasen med tilhørende tabeller
# Scriptet skal køres før main.py kan

import mysql.connector as mc

from serverinfo import *



def import_SharePlugDB():
        mydb = mc.connect(host=HOSTNAME, user=HOSTUSER, password=HOSTPASS, database="sys")
        cursor = mydb.cursor()

        # oprettelsen af databasen
        cursor.execute("CREATE SCHEMA `SharePlug`;")

        # Først oprettes Brugertabellen
        cursor.execute('''
        CREATE TABLE `SharePlug`.`Bruger` (
        `ID` INT NOT NULL AUTO_INCREMENT,
        `Fornavn` VARCHAR(45) NULL,
        `Efternavn` VARCHAR(45) NULL,
        `Telefon` VARCHAR(45) NULL,
        `Email` VARCHAR(45) NULL,
        `Adgangskode` VARCHAR(45) NULL,
        PRIMARY KEY (`ID`));''')

        # Oprettelse af Biltabellen
        cursor.execute('''
            CREATE TABLE `SharePlug`.`Bil` (
            `ID` INT NOT NULL AUTO_INCREMENT,
            `Mærke` VARCHAR(45) NOT NULL,
            `Model` VARCHAR(45) NOT NULL,
            `Opladningstype` VARCHAR(45) NOT NULL,
            `Bruger_ID` INT NOT NULL,
            PRIMARY KEY (`ID`),
            INDEX `Bruger_ID_idx` (`Bruger_ID` ASC) VISIBLE,
            CONSTRAINT `Bruger_ID`
                FOREIGN KEY (`Bruger_ID`)
                REFERENCES `SharePlug`.`Bruger` (`ID`)
                ON DELETE NO ACTION
                ON UPDATE NO ACTION);''')

        # Oprettelse af Ladestation tabellen
        cursor.execute('''

            CREATE TABLE `SharePlug`.`Ladestation` (
            `ID` INT NOT NULL AUTO_INCREMENT,
            `Leverandør` VARCHAR(45) NULL,
            `Type` VARCHAR(45) NULL,
            `Parkering` VARCHAR(45) NULL,
            `Adresse` VARCHAR(45) NULL,
            PRIMARY KEY (`ID`));''')



        # Indsættelse af data i ladestation tabellen
        cursor.execute('''

            INSERT INTO `SharePlug`.`Ladestation` (`ID`,`Leverandør`,`Type`,`Parkering`, `Adresse`)
            VALUES
            ('1','Virta', 'Type2', 'Ja', 'Dronningens Tværgade 43, 1302 Kbh'),
            ('2','Virta', 'Type2', 'Ja', 'Adelgade, Kbh'),
            ('3','Virta', 'Type2', 'Nej', 'Nyropsgade 13, 1602 Kbh'),
            ('4','Virta', 'CHAdeMO', 'Nej', 'Nyropsgade 13, 1602 Kbh'),
            ('5','Virta', 'CHAdeMO', 'Ja', 'Bernstorffsgade 29, 1577 Kbh'),
            ('6','Virta', 'CCS', 'Ja', 'Bernstorffsgade 29, 1577 Kbh'),
            ('7','Tesla', 'Tesla', 'Ja', 'Søtorvet 5, 1371 Kbh'),
            ('8','Tesla', 'Tesla', 'Ja', 'Søtorvet, 1371 Kbh'),
            ('9','Tesla', 'Tesla', 'Ja', 'Nørregade, 1165 Kbh'),
            ('11','Clever ', 'Type2', 'Nej', 'Fredensgade, Kbh'),
            ('12','Clever', 'Type2', 'Nej', 'Wesselsgade 18B, 2200 Kbh'),
            ('13','Clever', 'Type2', 'Ja', 'Nørre Farimagsgade 39, 1364 Kbh'),
            ('14','Clever', 'Type2', 'Ja', 'Vester Farimagsgade, 1606 Kbh'),
            ('15','Clever', 'CHAdeMO', 'Ja', 'Vester Farimagsgade, 1606 Kbh'),
            ('16','Clever', 'CCS', 'Ja', 'Vester Farimagsgade, 1606 Kbh'),
            ('17','E.ON', 'Type2', 'Nej', 'Nørre Allé, 2200 Kbh'),
            ('18','E.ON', 'Type2', 'Ja', 'Fiolstræde 1, 1171 Kbh'),
            ('19','E.ON', 'Type2', 'Nej', 'Bryghusgade, 1473 Kbh'),
            ('21','E.ON', 'Type2', 'Ja', 'Fiolstræde 8, 1171 Kbh'),
            ('22','E.ON', 'Type2', 'Ja', 'Klerkegade 2, Kbh');''')

        # Oprettelse af reservationstabellen
        cursor.execute('''

            CREATE TABLE `SharePlug`.`Reservation` (
            `ID` INT NOT NULL AUTO_INCREMENT,
            `Ladestation_ID` INT NULL,
            `Bil_ID` INT NULL,
            `Starttidspunkt` VARCHAR(45) NULL,
            `Sluttidspunkt` VARCHAR(45) NULL,
            PRIMARY KEY (`ID`));''')

        mydb.commit()
        mydb.close()

        print(f"\nDatabasen 'SharePlug' er oprettet i {HOSTNAME}:\nTabeller:\n-Bruger\n-Bil\n-Ladestation\n-Reservation")



import_SharePlugDB()
