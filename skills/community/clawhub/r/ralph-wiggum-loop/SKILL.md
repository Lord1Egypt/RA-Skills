# Ralph Wiggum - AI Loop Technique

Iteracyjny system doskonalenia kodu i outputów AI. Nazwany na cześć Ralpha Wigguma z Simpsons - bo "mówi jak dziecko, ale myśli jak krytyk".

## Architektura

```
┌─────────────┐
│  Generator  │ → Tworzy początkowy output
└──────┬──────┘
       ▼
┌─────────────┐
│   Krytyk    │ → Szuka błędów, optymalizacji, problemów
└──────┬──────┘
       ▼
┌─────────────┐
│  Naprawiacz │ → Poprawia zgłoszone problemy
└──────┬──────┘
       ▼
┌─────────────┐
│ Weryfikator │ → Sprawdza czy poprawki działają
└──────┬──────┘
       │
       ├─ Problemy? → Wraca do Krytyka (max 3 iteracje)
       ▼
   [OUTPUT]
```

## Wymagania

- LM Studio uruchomione na `http://127.0.0.1:1234/v1`
- Model preferowany: uncensored/liberated (np. dolphin, wizard-vicuna)
- Python 3.9+
- curl / wget

## Instalacja

```bash
# Skill jest gotowy do użycia po sklonowaniu
# Sprawdź czy LM Studio działa:
curl http://127.0.0.1:1234/v1/models
```

## Użycie

### Podstawowe

```bash
# Ulepsz kod z pliku
ralph-loop.sh -f input.py -o output.py

# Ulepsz kod inline
ralph-loop.sh -c "def hello(): print('world')"

# Ulepsz z promptem kontekstowym
ralph-loop.sh -f input.py -p "Optymalizuj pod kątem wydajności"
```

### Opcje

| Flag | Opis |
|------|------|
| `-f FILE` | Plik wejściowy |
| `-c CODE` | Kod inline (zamiast pliku) |
| `-o FILE` | Plik wyjściowy (domyślnie: stdout) |
| `-p PROMPT` | Dodatkowy kontekst/prompt |
| `-i N` | Max iteracji (domyślnie: 3) |
| `-m MODEL` | Nazwa modelu w LM Studio |
| `-v` | Verbose - pokaż proces |
| `--json` | Output w formacie JSON |

## Przykłady

### Przykład 1: Refaktoryzacja kodu

```bash
ralph-loop.sh -f examples/bad_code.py -o fixed.py -v
```

### Przykład 2: Generowanie od zera

```bash
ralph-loop.sh -c "Napisz funkcję sortowania quicksort w Python" \
  -o quicksort.py -p "Dodaj type hints i docstrings"
```

### Przykład 3: Analiza tekstu

```bash
ralph-loop.sh -f examples/article.txt -o analysis.json --json
```

## Jak to działa

1. **Generator** (generator.py)
   - Tworzy początkowy output używając LLM
   - Używa promptu systemowego z kontekstem zadania

2. **Krytyk** (critic.py)
   - Analizuje kod pod kątem:
     - Błędów składniowych i logicznych
     - OPTYMALIZACJI (złożoność, wydajność)
     - BEZPIECZEŃSTWA (podatności, injection)
     - STYLU (PEP8, czytelność, konwencje)
     - DOKUMENTACJI (docstrings, komentarze)
   - Zwraca listę problemów w formacie JSON

3. **Naprawiacz** (część ralph-loop.sh)
   - Wysyła kod + listę problemów do LLM
   - Prosi o poprawienie wszystkich zgłoszonych problemów

4. **Weryfikator** (część ralph-loop.sh)
   - Sprawdza czy poprawki faktycznie rozwiązują problemy
   - Ocenia czy kod jest gotowy czy potrzebna kolejna iteracja

5. **Pętla**
   - Jeśli weryfikator znajdzie nowe problemy → wraca do Krytyka
   - Max 3 iteracje (konfigurowalne)

## Prompt Engineering

System używa specyficznych promptów dla każdej roli:

### Prompt Generatora
```
Jesteś ekspertem programistą. Twoim zadaniem jest {task}.
Stwórz najlepszy możliwy kod/tekst. Używaj najnowszych praktyk.
{context}
```

### Prompt Krytyka
```
Jesteś bezwzględnym code reviewerem. Twoim zadaniem jest znalezienie
WSZYSTKICH problemów w podanym kodzie. Sprawdź:
- Błędy składniowe i logiczne
- Optymalizację (czasowa i pamięciowa)
- Bezpieczeństwo (SQL injection, XSS, etc.)
- Styl kodu (PEP8, konwencje)
- Dokumentację

Zwróć listę problemów w formacie JSON:
{
  "issues": [
    {"severity": "high|medium|low", "category": "...", "description": "...", "suggestion": "..."}
  ]
}
```

### Prompt Naprawiacza
```
Otrzymałeś kod i listę problemów do naprawy. Napraw KAŻDY problem
z listy. Nie dodawaj nowych funkcji - tylko napraw.

KOD:
{code}

PROBLEMY:
{issues}

Zwróć TYLKO poprawiony kod, bez dodatkowych komentarzy.
```

## API (Python)

Możesz używać modułów bezpośrednio w Pythonie:

```python
from ralph_loop import Generator, Critic, Verifier

gen = Generator(model="qwen2.5-coder-32b")
code = gen.generate("Napisz funkcję FizzBuzz", context="Użyj list comprehension")

critic = Critic()
issues = critic.analyze(code)

verifier = Verifier()
result = verifier.verify(code, issues)
```

## Debugowanie

```bash
# Sprawdź czy LM Studio działa
curl http://127.0.0.1:1234/v1/models | jq .

# Testuj pojedynczy komponent
python scripts/generator.py -t "Napisz hello world"
python scripts/critic.py -f test.py

# Verbose mode
ralph-loop.sh -f input.py -vvv
```

## Troubleshooting

### "Connection refused"
- Upewnij się że LM Studio jest uruchomione
- Sprawdź czy API jest włączone w ustawieniach LM Studio
- Domyślny port: 1234

### "Model not found"
- Sprawdź dostępne modele: `curl http://127.0.0.1:1234/v1/models`
- Użyj flagi `-m` aby wskazać konkretny model

### Słaba jakość outputu
- Użyj lepszego modelu (min. 7B parametrów)
- Zwiększ max iteracji: `-i 5`
- Dodaj szczegółowy kontekst: `-p "Szczegółowe wymagania"`

## Autor

Stworzone jako narzędzie OpenClaw.
Nazwa inspirowana Ralphem Wiggumem - "I'm helping!"
