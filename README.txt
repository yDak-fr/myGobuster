TLS CONTEXT — CO TO JEST?
==========================
Kod:
    context = ssl.create_default_context()
    
Context to obiekt, który przechowuje zasady bezpiecznego połączenia TLS.
Nie łączy się sam z serwerem i nie wysyła danych. Jest raczej konfiguracją,
którą Python wykorzysta później przy tworzeniu połączenia.

Można to porównać do instrukcji bezpieczeństwa:
    raw_sock     - zwykły kanał TCP do internetu
    context      - zasady ochrony tego kanału
    tls_socket   - kanał TCP opakowany szyfrowaniem TLS
Funkcja ssl.create_default_context() tworzy bezpieczne ustawienia domyślne.

W szczególności context wie:
  - którym urzędom certyfikacji ufa;
  - jak sprawdzić certyfikat serwera;
  - które wersje TLS wolno użyć;
  - jakie algorytmy szyfrowania są dozwolone.
Następnie context jest używany tutaj:
    tls_socket = context.wrap_socket(raw_sock, server_hostname=host)

wrap_socket() bierze zwykły socket i tworzy wokół niego warstwę TLS,
stosując zasady zapisane w context. Dopiero gdy wywołasz connect(),
rozpocznie się połączenie TCP oraz uzgadnianie TLS z serwerem.

Ważne:
create_default_context() to zalecany punkt startowy. Weryfikuje certyfikat
serwera i pomaga wykryć fałszywy albo źle skonfigurowany serwer. Nie warto
wyłączać tej weryfikacji tylko po to, aby ukryć błąd certyfikatu.
Jeden context można wykorzystać ponownie dla wielu połączeń TLS.

______________________________

INFO DO PROGARMU:

- aby wywolac poprawnie program trzeba uzyc:
	
	python (nazwa programu) (dane url strony) (plik z katalogami)

DZIALANIE PROGRAMU:

- program wyszukuje ukryte podkatalogi danej strony internetowej

