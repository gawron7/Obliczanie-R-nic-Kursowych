# Obliczanie-roznic-kursowych

#Program do zarządzania fakturami

Prosty program do dodawania faktur, spłacania faktur oraz wyświetlania zapisanych faktur. Program korzysta z kursów walut z API NBP do przeliczania kwot między różnymi walutami.

## Instalacja

Aby uruchomić program, należy pobrać pliki źródłowe z tego repozytorium. Następnie można uruchomić program za pomocą interpretera Pythona.

## Uruchomienie

Program można uruchomić w terminalu za pomocą polecenia:

``bash
python program.py

## Uzytkowanie
Po uruchomieniu programu użytkownik może wybierać z różnych opcji:

Dodaj fakturę: Pozwala dodać nową fakturę.
Spłać wybraną fakturę: Pozwala spłacić wybraną fakturę.
Wyświetl faktury: Wyświetla wszystkie zapisane faktury.
Zakończ program: Kończy działanie programu.
W przypadku opcji 1 i 2, użytkownik zostanie poproszony o wprowadzenie odpowiednich danych, takich jak kwota faktury, waluta faktury i data wystawienia faktury. Program przeliczy kwoty między różnymi walutami na podstawie aktualnych kursów walut pobranych z API NBP.

## Wymagania
Program wymaga zainstalowania pakietu requests. Można go zainstalować za pomocą polecenia:

bash
Copy code
pip install requests