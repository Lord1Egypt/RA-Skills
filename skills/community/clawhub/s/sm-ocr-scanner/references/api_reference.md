# Referenz: lokale OCR-Werkzeuge

Dieser Skill ruft ausschließlich lokal installierte Binaries auf. Es gibt keine
HTTP-Schnittstelle und keinen API-Key. Die folgende Referenz dokumentiert die
verwendeten Kommandos und die relevanten Parameter.

## tesseract

```
tesseract <input> <outputbase|stdout> [-l LANG] [--psm N] [--oem N] [configfile]
```

| Parameter | Bedeutung |
|---|---|
| `<input>` | Bilddatei (jpg, png, bmp, gif, tiff, webp) oder `-` für STDIN |
| `<outputbase>` | Basisname der Ausgabedatei ohne Endung, oder `stdout` |
| `-l LANG` | Sprachmodell, mehrere mit `+` verknüpft, z. B. `deu+eng` |
| `--psm N` | Page Segmentation Mode, 0–13 |
| `--oem N` | OCR Engine Mode: 0 Legacy, 1 LSTM, 2 kombiniert, 3 Default |
| `configfile` | Ausgabeformat: `txt` (Default), `pdf`, `tsv`, `hocr`, `alto` |

### Page Segmentation Modes (Auswahl)

| PSM | Anwendungsfall |
|---|---|
| 3 | vollautomatische Segmentierung ohne Orientierungserkennung (Default) |
| 4 | einzelne Spalte variabler Textgrößen — gut für Formulare |
| 6 | ein einheitlicher Textblock — gut für Fließtext-Scans |
| 7 | eine einzelne Textzeile |
| 8 | ein einzelnes Wort |
| 11 | spärlicher Text, beliebige Reihenfolge — gut für Screenshots und Diagramme |
| 13 | Rohzeile, ohne Tesseract-spezifische Vorverarbeitung |

### TSV-Ausgabe

`-f tsv` erzeugt tabulatorgetrennte Zeilen mit den Spalten:

```
level page_num block_num par_num line_num word_num left top width height conf text
```

Spalte 11 (`conf`) ist die Konfidenz in Prozent (`-1` für Strukturzeilen). Sie eignet
sich zur automatisierten Qualitätsprüfung, z. B. Ablehnung eines Scans bei
Durchschnittskonfidenz < 70.

### Sprachmodelle

```bash
tesseract --list-langs                 # installierte Modelle anzeigen
apt install tesseract-ocr-deu          # deutsches Modell nachinstallieren
```

Modelle liegen unter `/usr/share/tesseract-ocr/*/tessdata/` bzw. dem Pfad in `$TESSDATA_PREFIX`.

## poppler-utils

| Kommando | Verwendung im Skill |
|---|---|
| `pdfinfo -- <pdf>` | Seitenzahl vorab ermitteln, Abgleich mit `--max-pages` |
| `pdftotext -q -l 3 -- <pdf> -` | Probe der ersten drei Seiten: Gibt es schon einen Textlayer? |
| `pdftotext -q -layout -l <max> -- <pdf> -` | verlustfreie Extraktion, wenn das PDF bereits einen Textlayer hat |
| `pdftoppm -png -r <dpi> -f 1 -l <max> -- <pdf> <prefix>` | Rasterung jeder Seite zu `prefix-1.png`, `prefix-2.png`, … |
| `pdfunite <a.pdf> <b.pdf> … <out.pdf>` | Zusammenführen der pro Seite erzeugten OCR-PDFs |

## ocrmypdf (optional, empfohlen für `--format pdf`)

```
ocrmypdf --language deu+eng --image-dpi 300 --output-type pdf --quiet [--skip-text|--force-ocr] -- in.pdf out.pdf
```

Vorteil gegenüber dem Fallback: Original-Bildqualität, Metadaten und PDF/A-Konformität
bleiben erhalten, `--skip-text` überspringt Seiten, die bereits Text enthalten. Der Skill
startet `ocrmypdf` mit `TMPDIR` auf seinem privaten Temp-Verzeichnis, damit auch dessen
Zwischendateien dort landen und mit ihm gelöscht werden.

## timeout (coreutils, empfohlen)

```
timeout -k 10 <sekunden> <kommando …>
```

Jeder Aufruf der oben genannten Werkzeuge läuft unter `timeout`, sofern es installiert ist.
Grenze je Seite ist `--timeout` (Default 300 s). Für Aufrufe über ein ganzes Dokument gilt
das Produkt aus Grenze und Seitenzahl. Nach Ablauf folgt `SIGTERM`, zehn Sekunden später
`SIGKILL`. Der Skill meldet das als Exit 3.

## Hinweis zur Historie

Die Versionen 1.0.x dieses Skills dokumentierten hier die HTTP-Schnittstelle eines
externen OCR-Webdienstes. Dieser Weg übertrug Dokumentinhalte an einen Drittanbieter
und wurde mit 1.1.0 ersatzlos entfernt.
