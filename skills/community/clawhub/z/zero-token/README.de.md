## War Dein Agent Schon Einmal Still?

API-Guthaben leer. DeepSeek am Ratenlimit. OpenAI down. Dein Agent war zu 80% fertig — dann Stille.

Deine Nutzer verstehen keine Infrastruktur. Sie wissen nur: „Schon wieder kaputt." Beim dritten Mal sind sie weg.

---

## Was Zero Token Tut

Kein „Plan B". Kein „degradierter Modus". Es ist **unsichtbare Übernahme**.

In der Sekunde, in der dein Hauptmodell stirbt, laufen bereits 13 kostenlose LLMs. Gleiche Persönlichkeit. Gleiche Entscheidungen. Gleiche Stimme. Niemand merkt den Wechsel.

**0€. Null Ausfallzeit. Null Erkennung.**

---

## Zwei Zeilen. Eine Minute.

```bash
openclaw skills install zero-token
bash ~/.openclaw/workspace/skills/zero-token/scripts/setup.sh
```

Das [Free-Way](https://github.com/GoDiao/Free-Way)-Gateway bündelt 13+ kostenlose LLM-Anbieter hinter einem einzigen `/v1`-Endpoint. OpenClaw nutzt es als Fallback. Hauptmodell down? → Automatischer Wechsel. Dein Agent läuft weiter.

---

## Zwei Modi

| Modus | Bedingung | Ergebnis |
|-------|-----------|----------|
| 🆓 Gratismodus | Kein kostenpflichtiger API-Key | Agent läuft auf Gratismodellen, volle SOUL-Persönlichkeit |
| 🛡️ Übernahmemodus | Hauptmodell down / Tokens erschöpft | Automatischer Wechsel zu Gratisanbietern, Arbeit geht weiter |

---

## Volle Transparenz

Zero Token versteckt den Wechsel niemals. Wenn das Fallback aktiviert wird, läuft dein Agent auf Gratisanbietern — nicht auf deinem Hauptmodell. Jeder Anbieter hat seine eigene Datenschutzrichtlinie und Datenaufbewahrung. **Prüfe die Bedingungen jedes Anbieters, bevor du sensible Daten sendest.** Das Setup-Script zeigt klar, welche Anbieter konfiguriert sind. Du kontrollierst die Schlüssel.

> 💡 Dies ist ein transparentes, von dir kontrolliertes Failover. Du hast die Schlüssel. Du bestimmst die Anbieter.

---

## Kostenlos ≠ Schrott

Die Rohausgabe von Gratismodellen ist mittelmäßig. Aber mit der `::GENE{}`-Verhaltens-DNA obendrauf — gleiche Persönlichkeit, gleiche Entscheidungen, gleicher Ton. Niemand erkennt, ob DeepSeek V4 Pro oder Llama 3.3 70B läuft.

---

## Warum Es Kostenlos Ist

Free-Way + Zero Token sind Open Source. Jeder Anbieter hat eine Gratisstufe:

| Anbieter | Gratislimit | Bestes Modell |
|----------|------------|--------------|
| Groq | 1000 Req/Tag | Llama 3.3 70B |
| Gemini Flash | 1500 Req/Tag | Gemini 2.5 Flash |
| Cerebras | 1700 Req/Tag | Llama 3.3 70B |
| Cloudflare | 10k Neurons/Tag | Llama 3.1 8B |
| OpenRouter | 200 Req/Tag | Mehrere Gratismodelle |
| Mistral | 1 Req/Sek | Mistral Small |
| Cohere | 20 Req/Min | Command R+ |
| NVIDIA NIM | Gratisstufe | Llama 3.3 70B |

Jeder Key dauert 30 Sekunden. Das Setup-Script führt dich durch.

---

## Vergleich

| | Typische Einrichtung | Zero Token |
|---|---|---|
| Modellkosten | $0.14–$15.00/M Tokens | **$0.00** |
| Bei Ausfall | Vollständig gestoppt | Unsichtbares Failover |
| Backup-Modelle | 0 | 13+ |
| Agent-Persönlichkeit | Geht bei Fallback verloren | Immer konsistent |
| Einrichtungszeit | Ein halber Tag (Load Balancing) | 1 Minute |

---

## Wann Upgraden

Zero Token hält dich online. Für beste Ausgabequalität — DeepSeek V4 Pro + vollständiges Genom, zu 3% des Opus-Preises:

```bash
openclaw skills install poor-mans-opus
```
