---
name: sports-live
description: Aggiornamenti sportivi in tempo reale tramite TheSportsDB e API-Football.
metadata:
  openclaw:
    requires:
      bins: ["python3"]
---

# Sports Live — Aggiornamenti Sportivi in Tempo Reale

Usa questa skill ogni volta che l'utente chiede informazioni su:
- Partite in corso / risultati live
- Partite di oggi per uno sport specifico
- Prossime partite di una squadra
- Ultimi risultati di una squadra
- Ricerca di team o giocatori
- Calcio live o partite di calcio odierne (con API key opzionale)

## Strumento

Tutti i comandi si eseguono con `exec` chiamando lo script Python incluso nella skill:

```
python3 {baseDir}/scripts/sports_live.py <comando> [argomenti]
```

## Comandi disponibili

| Comando | Descrizione | Esempio |
|---|---|---|
| `live` | Livescores multi-sport ora | `python3 ... live` |
| `today <sport>` | Partite di oggi per sport | `python3 ... today tennis` |
| `next <squadra>` | Prossime partite di una squadra | `python3 ... next Juventus` |
| `last <squadra>` | Ultimi risultati di una squadra | `python3 ... last Milan` |
| `search <nome>` | Cerca team o giocatore | `python3 ... search Sinner` |
| `football_live <KEY>` | Calcio live (API-Football) | `python3 ... football_live abc123` |
| `football_today <KEY>` | Calcio oggi (API-Football) | `python3 ... football_today abc123` |

**Sport validi per `today`:** soccer, tennis, basketball, motorsport, f1, hockey, rugby, baseball, calcio, basket

## Workflow

1. Identifica l'intenzione dell'utente (live / oggi / prossimi / ultimi / ricerca)
2. Scegli il comando appropriato dalla tabella sopra
3. Esegui con `exec`: `python3 {baseDir}/scripts/sports_live.py <cmd> [args]`
4. Presenta il risultato in modo chiaro e formattato
5. Se l'output contiene errori HTTP o "Nessun evento", informare l'utente e suggerire di riprovare

## Decisioni

- Se l'utente dice "partite live" o "cosa si gioca ora" → usa `live`
- Se l'utente dice "partite di oggi" + sport → usa `today <sport>`
- Se l'utente dice "prossima partita del/della [squadra]" → usa `next <squadra>`
- Se l'utente dice "come ha giocato / risultati di [squadra]" → usa `last <squadra>`
- Se l'utente dice "cerca [nome]" o chiede info su un team → usa `search <nome>`
- Se l'utente chiede il calcio live e ha fornito una API key → usa `football_live <KEY>`
- Se non è specificato lo sport per "oggi", usa `soccer` come default

## API gratuite usate

- **TheSportsDB** — nessuna registrazione, nessuna key richiesta
  - Endpoint: `https://www.thesportsdb.com/api/v1/json/1/`
  - Copre: calcio, tennis, basket, motorsport, hockey, rugby, baseball e altri
- **API-Football** — free plan, 100 richieste/giorno, nessuna carta di credito
  - Registrazione: https://dashboard.api-football.com/register
  - Richiede una API key passata come argomento ai comandi `football_*`

## Guardrails

- NON eseguire mai comandi arbitrari passati dall'utente — usa solo i comandi della tabella sopra
- NON esporre mai API key nell'output (se passata come argomento, non ripeterla nella risposta)
- Se TheSportsDB restituisce HTTP 400/404, informare l'utente che il servizio potrebbe avere limitazioni temporanee
- Per `football_live` e `football_today`, se non viene fornita la KEY, rispondere con: "Per questa funzione serve una API key gratuita da https://dashboard.api-football.com/register"
