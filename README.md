# Vzdálenost adresních bodů ke kontejnerům na tříděný odpad

## Zadání 

Pro zvolenou množinu adresních bodů a množinu kontejnerů na tříděný odpad zjistěte průměrnou a maximální vzdálenost k nejbližšímu veřejnému kontejneru na tříděný odpad. Pro každý adresní bod tedy určete nejbližší veřejný kontejner na tříděný odpad a následně z těchto vzdáleností spočtěte průměr a maximum. Průměr a maximum vypište, pro maximum vypište i adresu, která má nejbližší veřejný kontejner nejdále.

## Vstupní data

Vstupem programu jsou 2 soubory GeoJSON. 

Soubor obsahující adresní body musí být uložen jako `adresy.geojson` a musí obsahovat atributy `addr:street`, `addr:housenumber` a `coordinates` označující souřadnice. Pro správnou funkčnost programu musí být souřadnice adresních bodů v systému WGS 84. Soubor je možné stáhnout z [Overpass Turbo](http://overpass-turbo.eu/).

Soubor obsahující kontejnery musí být uložen jako `kontejnery.geojson` a musí obsahovat atributy `PRISTUP` a `coordinates` označující souřadnice. Pro správnou funkčnost programu musí být souřadnice adresních bodů v systému S-JTSK. Soubor je možné stáhnout z [pražského Geoportálu](https://www.geoportalpraha.cz/cs/data/otevrena-data/8726EF0E-0834-463B-9E5F-FE09E62D73FB).

## Výstup

Program vypíše kolik je pro výpočet zvoleno adresních bodů a kontejnerů. Následně vypíše průměrnou vzdálenost a medián adresního bodu ke kontejneru v metrech. Jako poslední vypíše ulici a číslo popisné adresního bodu, který to má ke kontejneru nejdále a danou vzdálenost vypíše v metrech.

## Princip fungování
Program načte 2 soubory GeoJSON. Při nenalezení souboru či chybě program skončí. 

Ze souboru `adresy.geojson` si funkce vezme souřadnice, kde prohodí pozici zeměpisné délky a šířky a následně převede souřadnicový systém z WGS 84 na S-JTSK. K jednotlivým souřadnicím si vezme informaci o názvu ulice a čísle popisném.

Ze souboru `kontejnery.geojson` funkce vytřídí jen kontejnery, které mají veřejný přístup. Z těchto vybraných kontejnerů si vezme jejich souřadnice.


Ve funkci vzdálenost, kde jsou vstupní parametry souřadnice adresních bodů a kontejnerů, probíhá výpočet vzdálenosti pomocí pythagorovy věty každého adresního bodu od kontejneru. Ve funkci je následně ošetřena chyba dat, kde kdyby byl nejbližší kontejner od adresního bodu vzdálen více jak 10 km, tak by program skončil.

Dále program hledá maximální vzdálenost nejbližšího kontejneru a počítá průměr a medián.

Vybrané charakteristiky jsou programem vypsány.
