# Project Help & Onboarding

## FIRST_MESSAGE — Show this when creating a new project for a group

When you create a new empty project for a Telegram group (first message ever from that group), include this onboarding message AS PART of your reply. Answer the user's actual question first, then add this below with a separator:

---

**📁 OpenClaw PROJECTS**

Ab jetzt habt ihr **Projekte** zur Verfügung! Die funktionieren ähnlich wie Projekte in ChatGPT oder Claude — nur eben direkt in Telegram.

Ein Projekt ist **einzigartig für diese Gruppe** und wächst mit euch mit. Alles was ihr hinzufügt, vergesse ich nie — auch nach Wochen nicht.

**Was ein Projekt hat:**

```
┌─────────────────── DEIN PROJEKT ───────────────────┐
│                                                      │
│  📋 INSTRUCTIONS                                    │
│  ┌────────────────────────────────────────────┐     │
│  │ Werden IMMER geladen. Jede Nachricht.      │     │
│  │ Hier rein: Regeln, Sprache, Persona,       │     │
│  │ alles was IMMER gelten soll.               │     │
│  └────────────────────────────────────────────┘     │
│                                                      │
│  📚 KNOWLEDGE                                       │
│  ┌────────────────────────────────────────────┐     │
│  │ Klein (< 5K Tokens)                        │     │
│  │ → Wird komplett geladen, jede Nachricht    │     │
│  │                                            │     │
│  │ Mittel (5 - 20K Tokens)                    │     │
│  │ → Glossar + relevante Teile werden geladen │     │
│  │                                            │     │
│  │ Groß (> 20K Tokens)                        │     │
│  │ → Glossar + intelligente Vektorsuche       │     │
│  │   Ich finde das Relevante automatisch.     │     │
│  └────────────────────────────────────────────┘     │
│                                                      │
└──────────────────────────────────────────────────────┘
```

**So funktioniert jede Nachricht:**

```
  Du schreibst
       │
       ▼
  ┌─────────────┐    ┌──────────────┐
  │ Instructions │───▶│ Immer dabei  │
  └─────────────┘    └──────────────┘
       │
       ▼
  ┌─────────────┐    ┌──────────────┐
  │  Knowledge   │───▶│ Nach Größe   │
  └─────────────┘    └──────────────┘
       │
       ▼
  ┌─────────────┐
  │  Ich antworte │
  │  mit vollem   │
  │  Kontext 🧠   │
  └───────────────┘
```

**Die wichtigsten Befehle:**

```
 /instructions set [text]  → Permanente Regeln setzen
 /knowledge add [text]     → Wissen hinzufügen
 /project info             → Projekt-Status anzeigen
 /project help             → Diese Hilfe nochmal zeigen
```

Oder einfach sagen: *"permanentes Knowledge: ..."* — dann füge ich es hinzu.

**Tipp:** Startet mit Instructions! z.B.:
`/instructions set Wir sprechen Deutsch. Antworte immer kurz und präzise.`

---

## HELP — Show this when user says /project help or asks about projects

Show the same content as above, but without the intro paragraph ("Ab jetzt habt ihr..."). Just the diagrams, commands, and tips.
