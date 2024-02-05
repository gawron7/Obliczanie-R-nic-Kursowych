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

def oblicz_roznice_kursowe(kursy_walut, stara_kwota, stara_waluta):
    print("\nObliczanie różnic kursowych:")
    for waluta in kursy_walut:
        kurs = waluta['mid']
        roznica = (kurs - stara_kwota) / stara_kwota * 100
        print(f"{waluta['code']}: {roznica:.2f}%")

while True:
    try:
        kwota = float(input("Wprowadź kwotę: "))
    except ValueError:
        print("Nieprawidłowe dane. Wprowadź liczbę.")
        continue

    while True:
        # Walidacja waluty
        waluty_poprawne = ["USD", "EUR", "PLN"]
        waluta = input("Wybierz walutę (USD, EUR, PLN): ")

        while waluta not in waluty_poprawne:
            print("Nieprawidłowa waluta. Wybierz spośród: USD, EUR, PLN.")
            waluta = input("Wybierz walutę: ")

        # Wprowadzanie daty faktury przez użytkownika
        while True:
            try:
                data_faktury_str = input("Wprowadź datę faktury w formacie RRRR-MM-DD: ")
                data_faktury = datetime.datetime.strptime(data_faktury_str, "%Y-%m-%d").date()
            except ValueError:
                print("Nieprawidłowy format daty. Wprowadź datę w formacie RRRR-MM-DD.")
                continue
            else:
                break

        # Wprowadzanie daty zapłaty przez użytkownika
        while True:
            try:
                data_zaplaty_str = input("Wprowadź datę zapłaty w formacie RRRR-MM-DD: ")
                data_zaplaty = datetime.datetime.strptime(data_zaplaty_str, "%Y-%m-%d").date()
            except ValueError:
                print("Nieprawidłowy format daty. Wprowadź datę w formacie RRRR-MM-DD.")
                continue
            else:
                break

        print(f"Wprowadzona kwota: {kwota} {waluta}")
        print(f"Data faktury: {data_faktury}")
        print(f"Data zapłaty: {data_zaplaty}")

        # Pobranie aktualnych kursów walut na dzień faktury
        kursy_walut_faktura = pobierz_kursy_walut_na_dzien(data_faktury)

        if kursy_walut_faktura:
            # Obliczenie różnic kursowych dla daty faktury
            print("Różnice kursowe dla daty faktury:")
            oblicz_roznice_kursowe(kursy_walut_faktura, kwota, waluta)

        # Pobranie aktualnych kursów walut na dzień zapłaty
        kursy_walut_zaplaty = pobierz_kursy_walut_na_dzien(data_zaplaty)

        if kursy_walut_zaplaty:
            # Obliczenie różnic kursowych dla daty zapłaty
            print("Różnice kursowe dla daty zapłaty:")
            oblicz_roznice_kursowe(kursy_walut_zaplaty, kwota, waluta)

        # Pytanie użytkownika, czy chce wprowadzić kolejną fakturę
        kolejna_faktura = input("Czy chcesz wprowadzić kolejną fakturę? (Tak/Nie): ").lower()
        if kolejna_faktura != 'tak':
            break  # Jeśli użytkownik nie chce wprowadzać kolejnych faktur, wyjdź z pętli wewnętrznej
