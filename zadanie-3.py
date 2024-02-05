import datetime

# Wprowadzanie kwoty przez uzytkownika
while True:
    try:
        kwota = float(input("Wprowadź kwotę: "))
        break
    except ValueError:
        print("Nieprawidłowe dane. Wprowadź liczbę.")

# Walidacja waluty
waluty_poprawne = ["USD", "EUR", "PLN"]
waluta = input("Wybierz walutę (USD, EUR, PLN): ")

while waluta not in waluty_poprawne:
    print("Nieprawidłowa waluta. Wybierz spośród: USD, EUR, PLN.")
    waluta = input("Wybierz walutę: ")

# Wprowadzanie daty przez użytkownika
while True:
    try:
        data_wstawienia_str = input("Wprowadź datę w formacie RRRR-MM-DD: ")
        data_wstawienia = datetime.datetime.strptime(data_wstawienia_str, "%Y-%m-%d").date()
        break
    except ValueError:
        print("Nieprawidłowy format daty. Wprowadź datę w formacie RRRR-MM-DD.")

print(f"Wprowadzona kwota: {kwota} {waluta}")
print(f"Data wstawienia faktury: {data_wstawienia}")
