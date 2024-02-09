import requests
import datetime
import sys

def pobierz_kursy_walut_na_dzien(data):
    """
    Funkcja pobierająca kursy walut dla podanej daty z API NBP.

    Parametry:
        data (str): Data w formacie 'RRRR-MM-DD'.

    Zwraca:
        list: Lista zawierająca kursy walut dla podanej daty.
    """
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
    """
    Funkcja przeliczająca podaną kwotę z jednej waluty na inną.

    Parametry:
        kwota (float): Kwota do przeliczenia.
        waluta_poczatkowa (str): Waluta początkowa.
        waluta_docelowa (str): Waluta docelowa.
        kursy_walut (list): Lista kursów walut.

    Zwraca:
        float: Przeliczona kwota.
    """
    kurs_poczatkowy = next((waluta['mid'] for waluta in kursy_walut if waluta['code'] == waluta_poczatkowa), 1.0)
    kurs_docelowy = next((waluta['mid'] for waluta in kursy_walut if waluta['code'] == waluta_docelowa), 1.0)

    kwota_przeliczona = kwota * (kurs_poczatkowy / kurs_docelowy)
    return kwota_przeliczona

def oblicz_roznice_kursowe(kursy_walut, stara_kwota, stara_waluta):
    """
    Funkcja obliczająca różnice kursowe.

    Parametry:
        kursy_walut (list): Lista kursów walut.
        stara_kwota (float): Stara kwota.
        stara_waluta (str): Stara waluta.

    Zwraca:
        list: Lista zawierająca różnice kursowe.
    """
    roznice = []
    return roznice

def zapisz_do_pliku(nazwa_pliku, dane):
    """
    Funkcja zapisująca dane do pliku.

    Parametry:
        nazwa_pliku (str): Nazwa pliku.
        dane (list): Lista danych do zapisania.
    """
    with open(nazwa_pliku, 'w') as plik:
        for linia in dane:
            plik.write(linia + '\n')

def odczytaj_kwote_faktury_z_pliku(nazwa_pliku):
    """
    Funkcja odczytująca kwotę faktury i walutę z pliku.

    Parametry:
        nazwa_pliku (str): Nazwa pliku.

    Zwraca:
        tuple: Krotka zawierająca kwotę faktury i jej walutę.
    """
    with open(nazwa_pliku, 'r') as plik:
        linie = plik.readlines()
        kwota_faktury = float(linie[0].split(": ")[1].split(" ")[0])  # Pobranie kwoty z pierwszej linii
        waluta_faktury = linie[1].split(": ")[1].strip()  # Pobranie waluty z drugiej linii
        return kwota_faktury, waluta_faktury

def dodaj_fakture_do_pliku(nazwa_pliku, kwota_faktury, waluta_faktury, data_faktury):
    """
    Funkcja dodająca fakturę do pliku.

    Parametry:
        nazwa_pliku (str): Nazwa pliku.
        kwota_faktury (float): Kwota faktury.
        waluta_faktury (str): Waluta faktury.
        data_faktury (str): Data faktury w formacie 'RRRR-MM-DD'.
    """
    with open(nazwa_pliku, 'w') as plik:
        plik.write(f"Kwota faktury: {kwota_faktury} {waluta_faktury}\n")
        plik.write(f"Waluta faktury: {waluta_faktury}\n")  # Dodanie informacji o walucie faktury
        plik.write(f"Data faktury: {data_faktury}\n")

def aktualizuj_kwote_faktury_w_pliku(nazwa_pliku, nowa_kwota):
    """
    Funkcja aktualizująca kwotę faktury w pliku.

    Parametry:
        nazwa_pliku (str): Nazwa pliku.
        nowa_kwota (float): Nowa kwota faktury.
    """
    with open(nazwa_pliku, 'r') as plik:
        linie = plik.readlines()
    linie[0] = f"Kwota faktury: {nowa_kwota}\n"
    with open(nazwa_pliku, 'w') as plik:
        plik.writelines(linie)

def wyswietl_faktury():
    """
    Funkcja wyświetlająca zapisane faktury.
    """
    try:
        with open("faktura.txt", "r") as plik:
            print(plik.read())
    except FileNotFoundError:
        print("Brak zapisanych faktur.")

def wyswietl_instrukcje():
    """
    Funkcja wyświetlająca instrukcję obsługi programu.
    """
    print("[1] Dodaj fakturę")
    print("[2] Spłać wybraną fakturę")
    print("[3] Wyświetl faktury")
    print("[4] Zakończ program")

def obsluga_bledow_kwoty(kwota):
    """
    Funkcja obsługująca błędy związane z kwotą faktury.

    Parametry:
        kwota (float): Kwota faktury.

    Zwraca:
        bool: True, jeśli kwota jest poprawna; False w przeciwnym razie.
    """
    if kwota == 0:
        print("Kwota faktury nie może być równa zero.")
        return False
    return True

while True:
    wyswietl_instrukcje()
    wybor = input("Wybierz opcję: ")

    if wybor == '1':
        try:
            kwota_faktury = float(input("Wprowadź kwotę faktury: "))
            if not obsluga_bledow_kwoty(kwota_faktury):
                continue
        except ValueError:
            print("Nieprawidłowe dane. Wprowadź liczbę.")
            continue

        while True:
            waluty_poprawne = ["USD", "EUR", "PLN"]
            waluta_faktury = input("Wybierz walutę faktury (USD, EUR, PLN): ")
            if waluta_faktury == '0':
                print("Waluta faktury nie może być równa zero.")
                continue

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

            # Zapisuje fakturę do pliku
            dodaj_fakture_do_pliku("faktura.txt", kwota_faktury, waluta_faktury, data_faktury)
            break

    elif wybor == '2':
        kwota_faktury, waluta_faktury = odczytaj_kwote_faktury_z_pliku("faktura.txt")

        try:
            kwota_splaty = float(input("Wprowadź kwotę spłaty faktury: "))
            if not obsluga_bledow_kwoty(kwota_splaty):
                continue
        except ValueError:
            print("Nieprawidłowe dane. Wprowadź liczbę.")
            continue

        while True:
            waluty_poprawne = ["USD", "EUR", "PLN"]
            waluta_splaty = input("Wybierz walutę spłaty faktury (USD, EUR, PLN): ")
            if waluta_splaty == '0':
                print("Waluta spłaty faktury nie może być równa zero.")
                continue

            while waluta_splaty not in waluty_poprawne:
                print("Nieprawidłowa waluta. Wybierz spośród: USD, EUR, PLN.")
                waluta_splaty = input("Wybierz walutę spłaty faktury: ")

            while True:
                try:
                    data_splaty_str = input("Wprowadź datę spłaty faktury w formacie RRRR-MM-DD: ")
                    data_splaty = datetime.datetime.strptime(data_splaty_str, "%Y-%m-%d").date()
                except ValueError:
                    print("Nieprawidłowy format daty. Wprowadź datę spłaty faktury w formacie RRRR-MM-DD.")
                    continue
                else:
                    break

            print(f"Wprowadzona kwota spłaty faktury: {kwota_splaty} {waluta_splaty}")
            print(f"Data spłaty faktury: {data_splaty}")

            kursy_walut_faktura = pobierz_kursy_walut_na_dzien(data_faktury)
            kursy_walut_splaty = pobierz_kursy_walut_na_dzien(data_splaty)

            if kursy_walut_faktura and kursy_walut_splaty:
                roznice_faktura = oblicz_roznice_kursowe(kursy_walut_faktura, kwota_faktury, waluta_faktury)
                roznice_splaty = oblicz_roznice_kursowe(kursy_walut_splaty, kwota_splaty, waluta_splaty)

                # Przelicz kwotę spłaty na walutę faktury
                kwota_splaty_przeliczona = przelicz_kwote(kwota_splaty, waluta_splaty, waluta_faktury, kursy_walut_splaty)

                # Zapis do plików
                zapisz_do_pliku("roznice_faktura.txt", roznice_faktura)
                zapisz_do_pliku("roznice_splaty.txt", roznice_splaty)

                # Oblicza stan płatności
                stan_platnosci = kwota_faktury - kwota_splaty_przeliczona
                if stan_platnosci == 0:
                    print("Faktura została opłacona w całości.")
                elif stan_platnosci > 0:
                    print(f"Do opłacenia pozostało: {stan_platnosci} {waluta_faktury}")
                else:
                    print(f"Nadpłata: {-stan_platnosci} {waluta_faktury}")

                # Aktualizuje kwotę faktury w pliku
                aktualizuj_kwote_faktury_w_pliku("faktura.txt", stan_platnosci)
            break

    elif wybor == '3':
        wyswietl_faktury()

    elif wybor == '4':
        print("Koniec programu.")
        break

    else:
        print("Nieprawidłowy wybór. Wybierz opcję 1, 2, 3 lub 4.")
