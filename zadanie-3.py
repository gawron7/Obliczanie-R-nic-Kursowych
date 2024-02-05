import requests
import datetime

def pobierz_kursy_walut_na_dzien(data):
    url = f'http://api.nbp.pl/api/exchangerates/tables/A/{data}/'
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data[0]['rates']
    except requests.exceptions.RequestException as e:
        print(f"Błąd podczas pobierania kursów walut: {e}")
        return None

def przelicz_kwote(kwota, waluta_poczatkowa, waluta_docelowa, kursy_walut):
    kurs_poczatkowy = next((waluta['mid'] for waluta in kursy_walut if waluta['code'] == waluta_poczatkowa), 1.0)
    kurs_docelowy = next((waluta['mid'] for waluta in kursy_walut if waluta['code'] == waluta_docelowa), 1.0)

    kwota_przeliczona = kwota * (kurs_poczatkowy / kurs_docelowy)
    return kwota_przeliczona

def oblicz_roznice_kursowe(kursy_walut, stara_kwota, stara_waluta):
    roznice = []
    for waluta in kursy_walut:
        kurs = waluta['mid']
        roznica = (kurs - stara_kwota) / stara_kwota * 100
        roznice.append(f"{waluta['code']}: {roznica:.2f}%")
    return roznice

def zapisz_do_pliku(nazwa_pliku, dane):
    with open(nazwa_pliku, 'w') as plik:
        for linia in dane:
            plik.write(linia + '\n')

while True:
    try:
        kwota_faktury = float(input("Wprowadź kwotę faktury: "))
    except ValueError:
        print("Nieprawidłowe dane. Wprowadź liczbę.")
        continue

    while True:
        waluty_poprawne = ["USD", "EUR", "PLN"]
        waluta_faktury = input("Wybierz walutę faktury (USD, EUR, PLN): ")

        while waluta_faktury not in waluty_poprawne:
            print("Nieprawidłowa waluta. Wybierz spośród: USD, EUR, PLN.")
            waluta_faktury = input("Wybierz walutę faktury: ")

        while True:
            try:
                data_faktury_str = input("Wprowadź datę faktury w formacie RRRR-MM-DD: ")
                data_faktury = datetime.datetime.strptime(data_faktury_str, "%Y-%m-%d").date()
            except ValueError:
                print("Nieprawidłowy format daty. Wprowadź datę faktury w formacie RRRR-MM-DD.")
                continue
            else:
                break

        print(f"Wprowadzona kwota faktury: {kwota_faktury} {waluta_faktury}")
        print(f"Data faktury: {data_faktury}")

        kwota_splaty = float(input("Wprowadź kwotę spłaty faktury: "))

        while True:
            waluta_splaty = input("Wybierz walutę spłaty faktury (USD, EUR, PLN): ")

            while waluta_splaty not in waluty_poprawne:
                print("Nieprawidłowa waluta. Wybierz spośród: USD, EUR, PLN.")
                waluta_splaty = input("Wybierz walutę spłaty faktury: ")

            try:
                data_splaty_str = input("Wprowadź datę spłaty faktury w formacie RRRR-MM-DD: ")
                data_splaty = datetime.datetime.strptime(data_splaty_str, "%Y-%m-%d").date()
            except ValueError:
                print("Nieprawidłowy format daty. Wprowadź datę spłaty faktury w formacie RRRR-MM-DD.")
                continue

            break

        print(f"Wprowadzona kwota spłaty faktury: {kwota_splaty} {waluta_splaty}")
        print(f"Data spłaty faktury: {data_splaty}")

        kursy_walut_faktura = pobierz_kursy_walut_na_dzien(data_faktury)
        kursy_walut_splaty = pobierz_kursy_walut_na_dzien(data_splaty)

        if kursy_walut_faktura and kursy_walut_splaty:
            roznice_faktura = oblicz_roznice_kursowe(kursy_walut_faktura, kwota_faktury, waluta_faktury)
            roznice_splaty = oblicz_roznice_kursowe(kursy_walut_splaty, kwota_splaty, waluta_splaty)

            print("Różnice kursowe dla daty faktury:")
            for linia in roznice_faktura:
                print(linia)

            print("Różnice kursowe dla daty spłaty:")
            for linia in roznice_splaty:
                print(linia)

            # Przelicz kwotę spłaty na walutę faktury
            kwota_splaty_przeliczona = przelicz_kwote(kwota_splaty, waluta_splaty, waluta_faktury, kursy_walut_splaty)

            # Zapisz do plików
            zapisz_do_pliku("roznice_faktura.txt", roznice_faktura)
            zapisz_do_pliku("roznice_splaty.txt", roznice_splaty)

            # Oblicz i wyświetl ile pozostało do spłaty
            roznica_kwoty = kwota_faktury - kwota_splaty_przeliczona
            print(f"Ilość pozostałej do spłaty: {roznica_kwoty} {waluta_faktury}")

        kolejna_faktura = input("Czy chcesz wprowadzić kolejną fakturę? (Tak/Nie): ").lower()
        if kolejna_faktura != 'tak':
            break
