import json
import math
import statistics
from pyproj import CRS, Transformer


# Načtení souborů, odhalení nekorektních vstupů
try:
    with open('kontejnery.geojson', encoding= 'utf-8') as f:
        kontejnery_json= json.load(f)

except FileNotFoundError: 
    print('Nebyl nalezen soubor s kontejnery.')
    exit()
except ValueError:
    print('Soubor s kontejnery je chybný.')
    exit()
except PermissionError:
    exit("Není přístup k souboru s kontejnery.")
 
try:
    with open('adresy.geojson', encoding = 'utf-8') as f:
        adresy_json = json.load(f)

except FileNotFoundError: 
    print('Nebyl nalezen soubor s adresami.')
    exit()
except ValueError:
    print('Soubor s adresami je chybný.')
    exit()
except PermissionError:
    exit("Není přístup k souboru s adresami.")


# Změna souřadnicového systému
crs_wgs = CRS.from_epsg(4326) # WGS-84
crs_jtsk = CRS.from_epsg(5514) # S-JTSK
wgs2jtsk = Transformer.from_crs(crs_wgs,crs_jtsk)

def adresy(adresy_json):
    """ Funkce prohodí pozici zeměpisné délky a šířky, převede souřadnicový systém z WGS-84 na S-JTSK"""
    adresy_nazvy = []
    adresy_cp = []
    adresy_souradnice = []
    for adresa in adresy_json["features"]:
        souradnice_adres = adresa["geometry"]["coordinates"]
        ulice = adresa["properties"]["addr:street"]
        cislo= adresa["properties"]["addr:housenumber"]

        sirka, delka = wgs2jtsk.transform(souradnice_adres[1],souradnice_adres[0])
        adresy_nazvy.append(ulice)
        adresy_cp.append(cislo)
        adresy_souradnice.append([sirka,delka])
           
    return adresy_nazvy, adresy_cp, adresy_souradnice

def kontejnery_verejne(kontejnery_json):
    """Funkce vybere jen kontejnery s veřejným přístupem"""
    verejne_kont = []
    for kontejnery in kontejnery_json["features"]:
        pristup = kontejnery["properties"]["PRISTUP"]

        if pristup == "volně":
            souradnice = kontejnery["geometry"]["coordinates"]

            verejne_kont.append(souradnice)

    return verejne_kont

def vzdalenost (souradnice_ver_kontejneru, souradnice_adresy):
    """ Funkce vypočítá z načtených souřadnic vzdálenost mezi nimi v metrech."""
    seznam_vzdalenosti = []

    for adresy_sour in souradnice_adresy:
        max_vzdalenost = 10000

        for kontejnery_sour in souradnice_ver_kontejneru:

            vzdalenost = math.sqrt(((adresy_sour[0]-kontejnery_sour [0])**2)+((adresy_sour[1]-kontejnery_sour[1])**2))

            if vzdalenost < max_vzdalenost:
                max_vzdalenost = vzdalenost

        if max_vzdalenost > 10000:
            print("Nějaký kontejner je k nejbližší adrese dále než 10 km, konec programu.")
            exit()

        seznam_vzdalenosti.append(max_vzdalenost)
        

    return seznam_vzdalenosti

# uložení výstupů fonkcí do proměnných
nazvy_ulice, cp, souradnice_adresy = adresy(adresy_json)
souradnice_ver_kontejneru= kontejnery_verejne(kontejnery_json)
vzdalenost_adres_a_kontejneru = vzdalenost(souradnice_ver_kontejneru, souradnice_adresy)

# nalezení maximální nejbližší vzdálenosti adresního bodu a kontejneru  
# a oindexování pro následný výpis dané ulice a čísla popisného
max_nalezena_vzdalenost = max(vzdalenost_adres_a_kontejneru)
index = vzdalenost_adres_a_kontejneru.index(max(vzdalenost_adres_a_kontejneru))

# výpočet průměru a mediánu vzdálenosti
prumer = statistics.mean(vzdalenost_adres_a_kontejneru)
median = statistics.median(vzdalenost_adres_a_kontejneru)


print(f"Načteno {len(nazvy_ulice)} adresních bodů.")
print(f"Načteno {len(souradnice_ver_kontejneru)} kontejnerů na tříděný odpad.")
print()
print(f"Průměrná vzdálenost adresního bodu k veřejnemu kontejneru je {prumer:.0f} metrů.")
print(f"Medián vzdálenosti adresních boů k veřejnému kontejneru je {median:.0f} metrů.")
print()
print(f"Nejdále ke kontejneru je z adresy {nazvy_ulice[index]} {cp[index] } a to {max_nalezena_vzdalenost:.0f} metrů.")


            
