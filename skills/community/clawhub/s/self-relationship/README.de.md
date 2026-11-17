# Self-Relationship Skill · 与自己对话

[English](README.md) | [中文](README.zh-CN.md) | **Deutsch** | [Español](README.es.md) | [Русский](README.ru.md) | [日本語](README.ja.md) | [한국어](README.ko.md)

> Hilf Menschen, sich selbst klarer zu verstehen, sich selbst anzunehmen, ohne das Wachstum aufzugeben, und Entscheidungen zu treffen, die zu ihrem tatsächlichen Leben passen.
>
> 帮助一个人更好地理解自己、接纳自己、调整自己，并在现实中做出更适合自己的选择。

Ein AI-Skill, der auf positiver Psychologie basiert: Wenn Nutzer über „Selbstbeziehung", „Selbstakzeptanz", „sich selbst verstehen", „persönliches Wachstum" und ähnliche Themen sprechen, leitet er sie an, zuerst zu verstehen und dann zu verändern – statt vorschnell Ratschläge oder Etiketten zu geben.

## Kernphilosophie

- **Verstehe dich selbst, bevor du dich veränderst**: urteile nicht vorschnell; frage zuerst „Was ist passiert, was erlebe ich gerade, was bedeutet das für mich?"
- **Ein Zustand ist keine Identität**: „Ich bin gerade ängstlich" ≠ „Ich bin ein ängstlicher Mensch"
- **Akzeptanz bedeutet nicht, Veränderung aufzugeben**: entscheide den nächsten Schritt auf der Grundlage der Realität
- **Tests sind Werkzeuge zum Verstehen, keine Etiketten, die dich definieren**: Persönlichkeitstests, MBTI und die Big Five sind Spiegel, um sich selbst kennenzulernen
- **Mach Psychologie nicht zu einem neuen Werkzeug der Selbstverurteilung**: keine erfundene Gewissheit, keine erfundenen Erlebnisse, keine erzwungene Positivität

## Funktionen

- Zweisprachiger Inhalt (vollständiger chinesischer Text + englische Version in `SKILL.md`)
- Strukturierter Selbstreflexions-Rahmen: Fakten → Gefühle → Interpretation → Urteil → Wahl
- Klare Ausdrucksprinzipien und Grenzen, die den Ton eines „KI-Psychologie-Artikels" vermeiden
- Keine Diagnosen, keine Etiketten, keine großen Lebensentscheidungen im Namen des Nutzers

## Installation

Kopiere dieses Verzeichnis (oder `SKILL.md`) in das Skills-Verzeichnis deines Agents:

```bash
# Für Agents, die Skills unterstützen, z. B. Claude Code, Trae usw.
# Kopiere das self-relationship-Verzeichnis in dein Skills-Verzeichnis
cp -r self-relationship ~/.claude/skills/
```

Nach der Installation lädt der Skill automatisch, wenn der Nutzer Themen wie „Selbstbeziehung", „Selbstakzeptanz", „sich selbst verstehen", „persönliches Wachstum" oder die chinesischen Entsprechungen 「与自己相处」「自我关系」「自我接纳」「自我理解」「认识自己」「自我成长」 erwähnt.

## Verwendung

Sprich einfach mit deinem Agent, zum Beispiel:

- „Ich kann nicht aufhören, mich selbst zu kritisieren. Was soll ich tun?"
- „Ich fühle mich wie ein Versager. Stimmt etwas mit meiner Persönlichkeit nicht?"
- „Ich habe den MBTI gemacht, aber ich fühle mich dadurch definiert."
- „Ich bin mir nicht sicher, was ich wirklich will."

Der Agent folgt den im Skill definierten Gesprächsprinzipien: verstehen → klären → Perspektive anbieten → Wahlmöglichkeiten aufzeigen.

## Verzeichnisstruktur

```
self-relationship/
├── README.md        # Diese Datei (Englisch, wird auf GitHub standardmäßig angezeigt)
├── README.zh-CN.md  # 中文说明 (Chinesische Version)
├── README.de.md     # Diese Datei (Deutsch)
├── README.es.md     # Español (Spanische Version)
├── README.ru.md     # Русский (Russische Version)
├── README.ja.md     # 日本語 (Japanische Version)
├── README.ko.md     # 한국어 (Koreanische Version)
└── SKILL.md         # Skill-Inhalt (zweisprachig, mit Auslösebeschreibung im Frontmatter)
```

## Inhaltsrahmen

1. **Kernphilosophie** — 10 Grundprinzipien (Zustand ≠ Identität, Akzeptanz ≠ Aufgeben, Fokus auf Tendenzen usw.)
2. **Selbstreflexions-Rahmen** — fünf Ebenen: Fakten → Gefühle → Interpretation → Urteil → Wahl
3. **Wichtige Unterscheidungen** — Fakten vs. Interpretationen, Gefühle vs. Urteile, Akzeptanz vs. Resignation usw.
4. **Gesprächsprinzipien** — erst verstehen, dann beraten; Unsicherheit zulassen; Widersprüche zulassen; das Kontrollierbare finden
5. **Ausdrucksprinzipien** — 13 Prinzipien (KI-Ton vermeiden, weniger Aphorismen, niemals Erlebnisse erfinden)
6. **Antwortausrichtung** — verstehen → klären → Perspektive anbieten → Wahlmöglichkeiten aufzeigen
7. **Grenzen** — keine Diagnosen, keine Pathologisierung, keine Entscheidungen im Namen des Nutzers

## Haftungsausschluss

Dieser Skill dient nur der Bildung und Selbstreflexion. Er stellt keine medizinische, psychologische oder klinische Diagnose dar. Wenn du unter ernsthafter psychischer Belastung oder in einer Krise steckst, suche bitte qualifizierte professionelle Hilfe (z. B. einen Therapeuten, Psychiater oder eine lokale Krisenhotline).

## Lizenz

Für dieses Projekt ist keine Open-Source-Lizenz festgelegt. Für kommerzielle Nutzung oder Weiterverbreitung kontaktiere bitte den Autor.
