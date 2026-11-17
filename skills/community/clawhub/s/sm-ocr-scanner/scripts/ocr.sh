#!/usr/bin/env bash
#
# sm-ocr-scanner - lokale OCR fuer Bilder und PDFs
#
# Verarbeitet ausschliesslich lokal via Tesseract. Es verlaesst kein Byte
# das System - keine Cloud-API, kein Netzwerkzugriff.
#
# Deklarierter Datenfluss:
#   liest     nur die als Argument uebergebenen Dateien
#   schreibt  STDOUT, die mit --out benannte Datei, ein privates Temp-Verzeichnis
#   startet   tesseract, file, pdfinfo, pdftotext, pdftoppm, pdfunite,
#             ocrmypdf (optional), timeout (optional), env
#
# Lizenz: MIT-0
#
# bash >= 4.4 noetig (mapfile, leere Arrays unter set -u). Pruefung in bash-3-Syntax.
if [ -z "${BASH_VERSINFO:-}" ] || [ "${BASH_VERSINFO[0]}" -lt 4 ] || \
   { [ "${BASH_VERSINFO[0]}" -eq 4 ] && [ "${BASH_VERSINFO[1]}" -lt 4 ]; }; then
  echo "sm-ocr-scanner: bash >= 4.4 erforderlich (gefunden: ${BASH_VERSION:-unbekannt})" >&2
  exit 2
fi
set -Eeuo pipefail
umask 077             # alle Ausgaben und Temp-Dateien nur fuer den Aufrufer lesbar

readonly SCRIPT_NAME="${0##*/}"
readonly VERSION="1.2.2"

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
readonly SCRIPT_DIR
readonly SKILL_DIR="${SCRIPT_DIR%/*}"
readonly BUNDLE_TESSDATA="$SKILL_DIR/assets/tessdata"

# ---------------------------------------------------------------- Defaults --
# Default-Sprache deu+eng: Der Skill richtet sich bewusst an den deutschsprachigen
# Raum (DACH). Jede installierte Sprache ist per -l/--lang oder $OCR_LANG waehlbar.
# Default language deu+eng: intentionally German-focused (DACH region); any
# installed language can be selected with -l/--lang or $OCR_LANG.
OCR_LANG_DEFAULT="deu+eng"
LANGS="${OCR_LANG:-$OCR_LANG_DEFAULT}"
# explizit gesetzte Sprache -> harter Fehler bei fehlendem Modell;
# Default -> fehlende Modelle werden mit Warnung uebersprungen
LANG_EXPLICIT=0; [[ -n "${OCR_LANG:-}" ]] && LANG_EXPLICIT=1
DPI="${OCR_DPI:-300}"
PSM="${OCR_PSM:-3}"
OEM="${OCR_OEM:-3}"
MAX_PAGES="${OCR_MAX_PAGES:-200}"   # Obergrenze Seiten je PDF (Schutz vor Ressourcenerschoepfung)
TIMEOUT="${OCR_TIMEOUT:-300}"       # Sekunden je Seite bzw. Werkzeugaufruf, 0 = aus
FORMAT="txt"          # txt | pdf | tsv
OUTFILE=""
OVERWRITE=0
FORCE_OCR=0           # PDF mit vorhandenem Textlayer trotzdem rastern
VERBOSE=0
QUIET=0
TMPWORK=""
TMPOUT=""
PDF_PAGES=""

# Rasterformate, die der Skill annimmt (deckungsgleich mit der Beschreibung)
readonly IMAGE_MIMES=" image/png image/jpeg image/tiff image/bmp image/x-ms-bmp image/gif image/webp "

# ------------------------------------------------------------------ Helper --
log()  { [[ $VERBOSE -eq 1 ]] && printf '[%s] %s\n' "$SCRIPT_NAME" "$*" >&2 || true; }
note() { [[ $QUIET -eq 1 ]] || printf '[%s] HINWEIS: %s\n' "$SCRIPT_NAME" "$*" >&2; }
warn() { printf '[%s] WARN: %s\n' "$SCRIPT_NAME" "$*" >&2; }
die()  { local m="$1"; printf '[%s] ERROR: %s\n' "$SCRIPT_NAME" "$m" >&2; exit "${2:-1}"; }

# purge_dir <verzeichnis> - loescht ein eigenes Arbeitsverzeichnis samt Inhalt.
# Greift nur innerhalb des eigenen mktemp-Verzeichnisses, nie auf einen Symlink;
# find -P folgt keinem Link (die tessdata-Links zeigen auf Systemverzeichnisse).
purge_dir() {
  local d="$1"
  [[ -n "$TMPWORK" && "$TMPWORK" == */sm-ocr-* ]] || return 0
  [[ "$d" == "$TMPWORK" || "$d" == "$TMPWORK"/* ]] || return 0
  [[ -d "$d" && ! -L "$d" ]] || return 0
  find -P "$d" -depth -delete 2>/dev/null || true
}

cleanup() {
  local rc=$?
  purge_dir "$TMPWORK"
  return $rc
}
trap cleanup EXIT
trap 'die "abgebrochen (Signal)" 130' INT TERM HUP

usage() {
  cat <<'USAGE'
sm-ocr-scanner - lokale OCR fuer Bilder und PDFs (Tesseract)

VERWENDUNG
  ocr.sh [OPTIONEN] <datei> [<datei> ...]

OPTIONEN
  -l, --lang <code>    Tesseract-Sprache(n), z. B. deu, eng, deu+eng
                       (Default: deu+eng, ueberschreibbar via $OCR_LANG)
  -r, --dpi <zahl>     Rasterisierungs-DPI fuer PDF-Seiten, 70..1200 (Default: 300)
      --psm <0-13>     Tesseract Page Segmentation Mode (Default: 3)
      --oem <0-3>      Tesseract OCR Engine Mode (Default: 3)
  -f, --format <fmt>   txt (Default) | pdf (durchsuchbares PDF) | tsv
  -o, --out <datei>    Ausgabedatei statt STDOUT (bei pdf zwingend)
      --overwrite      vorhandene Ausgabedatei ueberschreiben
      --force-ocr      PDFs auch dann rastern, wenn bereits Text enthalten ist
      --max-pages <n>  hoechstens n Seiten je PDF, 1..10000 (Default: 200)
      --timeout <s>    Zeitlimit je Seite in Sekunden, 0 = aus (Default: 300)
      --check          Umgebung pruefen (Abhaengigkeiten, Sprachmodelle) und beenden
  -q, --quiet          Hinweise zu temporaeren Dateien unterdruecken
  -v, --verbose        Diagnoseausgaben auf STDERR
  -V, --version        Version ausgeben
  -h, --help           diese Hilfe

DATENSCHUTZ
  Keine Netzwerkverbindung. Beim Rastern eines PDF entstehen Seitenbilder mit
  dem vollen Dokumentinhalt in einem privaten Temp-Verzeichnis (Modus 700).
  Sie werden nach jedem PDF und bei Programmende - auch bei Fehler oder
  Signal - geloescht. Ablageort ueber $TMPDIR waehlbar.

UMGEBUNGSVARIABLEN
  OCR_LANG, OCR_DPI, OCR_PSM, OCR_OEM   Defaults ueberschreiben
  OCR_MAX_PAGES, OCR_TIMEOUT            Ressourcengrenzen
  OCR_TEXTLAYER_MIN                     Schwelle Textlayer-Erkennung (Default 120)
  TMPDIR                                Ablage temporaerer Seitenbilder
  TESSDATA_PREFIX                       eigenes tessdata-Verzeichnis

BEISPIELE
  ocr.sh rechnung.png
  ocr.sh -l deu scan.pdf
  ocr.sh -l deu -f pdf -o scan_ocr.pdf scan.pdf
  ocr.sh *.jpg > alle.txt
  OCR_LANG=eng ocr.sh screenshot.png

EXIT-CODES
  0 Erfolg | 1 Nutzungs-/Eingabefehler | 2 fehlende Abhaengigkeit
  3 OCR-Fehler | 130 Abbruch durch Signal
USAGE
}

need() {
  command -v "$1" >/dev/null 2>&1 || die "'$1' nicht gefunden. $2" 2
}

# limit <sekunden> <cmd...> - Laufzeitgrenze gegen praeparierte Eingaben.
# 0 oder fehlendes timeout(1) -> ohne Grenze.
limit() {
  local secs="$1"; shift
  if (( secs > 0 )) && command -v timeout >/dev/null 2>&1; then
    timeout -k 10 "$secs" "$@"
  else
    "$@"
  fi
}

list_langs() { tesseract --list-langs 2>/dev/null | tail -n +2; }

# in_list <wert> <eintrag...> - Mitgliedschaft ohne Pipe (grep -q + pipefail
# kann per SIGPIPE faelschlich scheitern)
in_list() {
  local x="$1" i; shift
  for i in "$@"; do [[ "$i" == "$x" ]] && return 0; done
  return 1
}

# Systemseitiges tessdata-Verzeichnis ermitteln
sys_tessdata() {
  local d
  if [[ -n "${TESSDATA_PREFIX:-}" && -d "${TESSDATA_PREFIX}" ]]; then
    printf '%s' "$TESSDATA_PREFIX"; return 0
  fi
  for d in /usr/share/tesseract-ocr/*/tessdata /usr/share/tessdata \
           /usr/local/share/tessdata /opt/homebrew/share/tessdata; do
    [[ -d "$d" ]] && { printf '%s' "$d"; return 0; }
  done
  return 1
}

# Fehlende Sprachmodelle aus assets/tessdata nachziehen, ohne die
# Systemmodelle zu verlieren: Merge-Verzeichnis aus Symlinks im Tempdir.
merge_tessdata() {
  local want=("$@") missing=() have=() l
  mapfile -t have < <(list_langs)
  for l in "${want[@]}"; do
    in_list "$l" "${have[@]}" || missing+=("$l")
  done
  (( ${#missing[@]} > 0 )) || return 0
  [[ -d "$BUNDLE_TESSDATA" ]] || return 0

  local usable=0
  for l in "${missing[@]}"; do
    [[ -r "$BUNDLE_TESSDATA/$l.traineddata" ]] && usable=1
  done
  (( usable == 1 )) || return 0

  local merged="$TMPWORK/tessdata" sysdir
  mkdir -p "$merged"
  if sysdir="$(sys_tessdata)"; then
    ln -sf -- "$sysdir"/*.traineddata "$merged/" 2>/dev/null || true
    [[ -d "$sysdir/configs" ]] && ln -sf -- "$sysdir/configs" "$merged/" 2>/dev/null || true
    [[ -d "$sysdir/tessconfigs" ]] && ln -sf -- "$sysdir/tessconfigs" "$merged/" 2>/dev/null || true
  fi
  ln -sf -- "$BUNDLE_TESSDATA"/*.traineddata "$merged/" 2>/dev/null || true
  export TESSDATA_PREFIX="$merged"
  log "lokale Sprachmodelle aus assets/tessdata eingebunden: $BUNDLE_TESSDATA -> $merged"
}

do_check() {
  local rc=0
  printf 'sm-ocr-scanner %s - Umgebungspruefung\n\n' "$VERSION"
  printf '%-14s %s\n' "Skill-Pfad:" "$SKILL_DIR"
  local c
  for c in tesseract file pdfinfo pdftoppm pdftotext pdfunite ocrmypdf timeout; do
    if command -v "$c" >/dev/null 2>&1; then
      printf '  [ok]   %-10s %s\n' "$c" "$(command -v "$c")"
    else
      case "$c" in
        tesseract) printf '  [FEHLT] %-10s PFLICHT - apt install tesseract-ocr\n' "$c"; rc=2 ;;
        file)      printf '  [FEHLT] %-10s PFLICHT - apt install file\n' "$c"; rc=2 ;;
        ocrmypdf)  printf '  [opt]  %-10s optional - bessere PDF-Ausgabe (apt install ocrmypdf)\n' "$c" ;;
        timeout)   printf '  [opt]  %-10s optional - Laufzeitgrenze je Seite (coreutils)\n' "$c" ;;
        *)         printf '  [opt]  %-10s noetig fuer PDF - apt install poppler-utils\n' "$c" ;;
      esac
    fi
  done
  if command -v tesseract >/dev/null 2>&1; then
    printf '\nTesseract:     %s\n' "$(tesseract --version 2>&1 | head -1)"
    printf 'tessdata:      %s\n' "$(sys_tessdata || echo '<nicht gefunden>')"
    printf 'Systemmodelle: %s\n' "$(list_langs | tr '\n' ' ')"
  fi
  if [[ -d "$BUNDLE_TESSDATA" ]]; then
    local b; b="$(cd "$BUNDLE_TESSDATA" && ls -1 ./*.traineddata 2>/dev/null | sed 's#^\./##;s#\.traineddata$##' | tr '\n' ' ')"
    printf 'Bundle-Modelle: %s\n' "${b:-<keine>}"
  fi
  printf '\nDefault-Sprache: %s\n' "$OCR_LANG_DEFAULT"
  printf 'Grenzen:         %s Seiten je PDF, %s s je Seite\n' "$MAX_PAGES" "$TIMEOUT"
  printf 'Netzwerk:        keiner - ocr.sh startet kein Netzwerkwerkzeug\n'
  return $rc
}

# --------------------------------------------------------------- Argparsing --
declare -a INPUTS=()
DO_CHECK=0
while [[ $# -gt 0 ]]; do
  case "$1" in
    -l|--lang)      [[ $# -ge 2 ]] || die "--lang benoetigt einen Wert"; LANGS="$2"; LANG_EXPLICIT=1; shift 2 ;;
    -r|--dpi)       [[ $# -ge 2 ]] || die "--dpi benoetigt einen Wert";  DPI="$2";   shift 2 ;;
    --psm)          [[ $# -ge 2 ]] || die "--psm benoetigt einen Wert";  PSM="$2";   shift 2 ;;
    --oem)          [[ $# -ge 2 ]] || die "--oem benoetigt einen Wert";  OEM="$2";   shift 2 ;;
    -f|--format)    [[ $# -ge 2 ]] || die "--format benoetigt einen Wert"; FORMAT="$2"; shift 2 ;;
    -o|--out)       [[ $# -ge 2 ]] || die "--out benoetigt einen Wert"; OUTFILE="$2"; shift 2 ;;
    --max-pages)    [[ $# -ge 2 ]] || die "--max-pages benoetigt einen Wert"; MAX_PAGES="$2"; shift 2 ;;
    --timeout)      [[ $# -ge 2 ]] || die "--timeout benoetigt einen Wert"; TIMEOUT="$2"; shift 2 ;;
    --overwrite)    OVERWRITE=1; shift ;;
    --force-ocr)    FORCE_OCR=1; shift ;;
    --check)        DO_CHECK=1; shift ;;
    -q|--quiet)     QUIET=1; shift ;;
    -v|--verbose)   VERBOSE=1; shift ;;
    -V|--version)   printf '%s %s\n' "$SCRIPT_NAME" "$VERSION"; exit 0 ;;
    -h|--help)      usage; exit 0 ;;
    --)             shift; while [[ $# -gt 0 ]]; do INPUTS+=("$1"); shift; done ;;
    -*)             die "unbekannte Option: $1" ;;
    *)              INPUTS+=("$1"); shift ;;
  esac
done

# ------------------------------------------------------------- Validierung --
# Zahlen ohne fuehrende Null (sonst Oktal-Auswertung in Bash-Arithmetik)
[[ "$DPI" =~ ^[1-9][0-9]{0,4}$ ]] && (( DPI >= 70 && DPI <= 1200 )) \
  || die "--dpi muss 70..1200 sein (ist: $DPI)"
[[ "$PSM" =~ ^([0-9]|1[0-3])$ ]] || die "--psm muss 0..13 sein (ist: $PSM)"
[[ "$OEM" =~ ^[0-3]$ ]]          || die "--oem muss 0..3 sein (ist: $OEM)"
[[ "$MAX_PAGES" =~ ^[1-9][0-9]{0,4}$ ]] && (( MAX_PAGES <= 10000 )) \
  || die "--max-pages muss 1..10000 sein (ist: $MAX_PAGES)"
[[ "$TIMEOUT" =~ ^(0|[1-9][0-9]{0,4})$ ]] && (( TIMEOUT <= 86400 )) \
  || die "--timeout muss 0..86400 sein (ist: $TIMEOUT)"
[[ "$LANGS" =~ ^[A-Za-z_]{3,}(\+[A-Za-z_]{3,})*$ ]] || die "ungueltige Sprachangabe: $LANGS"
case "$FORMAT" in txt|pdf|tsv) ;; *) die "--format muss txt, pdf oder tsv sein (ist: $FORMAT)" ;; esac

if [[ $DO_CHECK -eq 1 ]]; then do_check; exit $?; fi
[[ ${#INPUTS[@]} -gt 0 ]] || { usage >&2; exit 1; }

need tesseract "Installation: apt install tesseract-ocr tesseract-ocr-deu"
need file      "Installation: apt install file"

if [[ "$FORMAT" == "pdf" && -z "$OUTFILE" ]]; then
  die "--format pdf erfordert --out <datei.pdf>"
fi
if [[ -n "$OUTFILE" ]]; then
  [[ -d "$OUTFILE" ]] && die "Ausgabeziel ist ein Verzeichnis: $OUTFILE"
  if [[ ( -e "$OUTFILE" || -L "$OUTFILE" ) && $OVERWRITE -eq 0 ]]; then
    die "Ausgabedatei existiert bereits: $OUTFILE (--overwrite zum Ueberschreiben)"
  fi
fi
if [[ ${#INPUTS[@]} -gt 1 && "$FORMAT" == "pdf" ]]; then
  die "--format pdf verarbeitet nur eine Eingabedatei"
fi

# mktemp -d legt das Verzeichnis mit Modus 700 an (unter umask 077 ohnehin)
TMPWORK="$(mktemp -d "${TMPDIR:-/tmp}/sm-ocr-XXXXXXXX")"
log "Temp-Verzeichnis: $TMPWORK"

# Sprachmodelle aufloesen: erst Bundle einbinden, dann pruefen.
# --psm 0/1 (Orientierungs- und Schrifterkennung) braucht zusaetzlich osd.
NEED_OSD=""; (( PSM <= 1 )) && NEED_OSD="osd"
# shellcheck disable=SC2086
merge_tessdata ${LANGS//+/ } $NEED_OSD
mapfile -t AVAIL < <(list_langs)
if [[ -n "$NEED_OSD" ]] && ! in_list osd "${AVAIL[@]}"; then
  die "--psm $PSM braucht osd.traineddata. Installation: apt install tesseract-ocr-osd (oder scripts/install.sh --portable --lang osd)" 2
fi
declare -a KEEP=()
for l in ${LANGS//+/ }; do
  if in_list "$l" "${AVAIL[@]}"; then
    KEEP+=("$l")
  elif [[ $LANG_EXPLICIT -eq 1 ]]; then
    die "Sprachpaket '$l' fehlt. Verfuegbar: ${AVAIL[*]:-keine}. Installation: apt install tesseract-ocr-$l (oder scripts/install.sh)" 2
  else
    warn "Sprachpaket '$l' nicht installiert - wird uebersprungen (scripts/install.sh installiert es)"
  fi
done
(( ${#KEEP[@]} > 0 )) || die "kein nutzbares Sprachpaket. Verfuegbar: ${AVAIL[*]:-keine}" 2
LANGS="$(IFS=+; printf '%s' "${KEEP[*]}")"
log "Sprache=$LANGS DPI=$DPI PSM=$PSM OEM=$OEM Format=$FORMAT MaxSeiten=$MAX_PAGES Timeout=$TIMEOUT"

# -------------------------------------------------------------- OCR-Kernel --
tess() {                       # tess <input> <outbase|stdout> <configs...>
  local in="$1" out="$2"; shift 2
  limit "$TIMEOUT" tesseract "$in" "$out" -l "$LANGS" --psm "$PSM" --oem "$OEM" "$@" \
    2>>"$TMPWORK/tess.log"
}

# Zeitbudget fuer Aufrufe, die ein ganzes Dokument verarbeiten
doc_timeout() {
  local n="$MAX_PAGES"
  [[ "$PDF_PAGES" =~ ^[0-9]+$ ]] && n="$PDF_PAGES"
  printf '%s' $(( TIMEOUT * n ))
}

ocr_image_txt() {
  local img="$1" rc=0
  tess "$img" stdout "$FORMAT" || rc=$?
  if (( rc != 0 )); then
    if (( rc == 124 || rc == 137 )); then
      warn "Zeitlimit von $TIMEOUT s ueberschritten: $img"
    else
      warn "OCR fehlgeschlagen fuer: $img"
    fi
    [[ -s "$TMPWORK/tess.log" ]] && sed 's/^/  tesseract: /' "$TMPWORK/tess.log" >&2
    : > "$TMPWORK/tess.log"
    return 3
  fi
}

# Seitenzahl ermitteln und gegen --max-pages pruefen. Setzt PDF_PAGES.
check_page_limit() {
  local pdf="$1" pages=""
  PDF_PAGES=""
  if command -v pdfinfo >/dev/null 2>&1; then
    pages="$(limit "$TIMEOUT" pdfinfo -- "$pdf" 2>/dev/null | awk '/^Pages:/{print $2; exit}' || true)"
  fi
  if [[ "$pages" =~ ^[0-9]+$ ]]; then
    if (( pages > MAX_PAGES )); then
      warn "'$pdf' hat $pages Seiten, Grenze ist $MAX_PAGES (--max-pages oder \$OCR_MAX_PAGES anheben)"
      return 1
    fi
    PDF_PAGES="$pages"
  else
    warn "Seitenzahl von '$pdf' nicht ermittelbar (pdfinfo fehlt?) - verarbeite hoechstens $MAX_PAGES Seiten"
  fi
}

# PDF-Seiten in ein frisches, privates Unterverzeichnis rastern. Das Verzeichnis
# wird vor jedem PDF geleert, damit sich Seiten verschiedener Dokumente im
# Stapelbetrieb nicht vermischen.
rasterize_pdf() {
  local pdf="$1" pagedir="$TMPWORK/pages"
  need pdftoppm "Installation: apt install poppler-utils"
  purge_dir "$pagedir"; mkdir -p "$pagedir"
  note "rastere ${PDF_PAGES:-bis zu $MAX_PAGES} Seite(n) mit $DPI dpi als PNG in ein privates Temp-Verzeichnis (Modus 700, wird danach geloescht)"
  log "Seitenbilder: $pagedir"
  limit "$(doc_timeout)" pdftoppm -png -r "$DPI" -f 1 -l "$MAX_PAGES" -- "$pdf" "$pagedir/page" \
    || { warn "pdftoppm konnte '$pdf' nicht rastern"; return 3; }
}

pdf_has_textlayer() {
  local pdf="$1"
  command -v pdftotext >/dev/null 2>&1 || return 1
  local chars min="${OCR_TEXTLAYER_MIN:-120}"
  [[ "$min" =~ ^[0-9]{1,6}$ ]] || min=120
  chars="$(limit "$TIMEOUT" pdftotext -q -l 3 -- "$pdf" - 2>/dev/null | tr -d '[:space:]' | wc -c || true)"
  chars="${chars//[^0-9]/}"
  log "vorhandener Textlayer: ${chars:-0} Zeichen (Schwelle: $min)"
  (( ${chars:-0} > min ))
}

process_pdf_txt() {
  local pdf="$1"
  check_page_limit "$pdf" || return 1
  if [[ $FORCE_OCR -eq 0 ]] && pdf_has_textlayer "$pdf"; then
    log "PDF enthaelt bereits einen Textlayer - extrahiere verlustfrei (--force-ocr erzwingt OCR)"
    limit "$(doc_timeout)" pdftotext -q -layout -l "$MAX_PAGES" -- "$pdf" - \
      || { warn "pdftotext fehlgeschlagen: $pdf"; return 3; }
    return 0
  fi
  rasterize_pdf "$pdf" || return $?
  shopt -s nullglob
  local imgs=("$TMPWORK/pages"/page-*.png)
  shopt -u nullglob
  (( ${#imgs[@]} > 0 )) || { warn "keine Seiten aus '$pdf' extrahiert"; return 3; }
  local rc=0 img
  for img in "${imgs[@]}"; do
    printf -- '--- Seite %s ---\n' "$(basename "$img" .png | sed 's/^page-0*//')"
    ocr_image_txt "$img" || rc=3
  done
  purge_dir "$TMPWORK/pages"
  return $rc
}

process_pdf_searchable() {     # -> durchsuchbares PDF nach $TMPOUT
  local pdf="$1"
  check_page_limit "$pdf" || return 1
  if command -v ocrmypdf >/dev/null 2>&1; then
    log "verwende ocrmypdf"
    note "ocrmypdf verarbeitet '$pdf' lokal, Zwischendateien im privaten Temp-Verzeichnis"
    local args=(--language "$LANGS" --image-dpi "$DPI" --output-type pdf --quiet)
    if [[ $FORCE_OCR -eq 1 ]]; then args+=(--force-ocr); else args+=(--skip-text); fi
    limit "$(doc_timeout)" env TMPDIR="$TMPWORK" ocrmypdf "${args[@]}" -- "$pdf" "$TMPOUT" \
      || { warn "ocrmypdf fehlgeschlagen: $pdf"; return 3; }
    return 0
  fi
  log "ocrmypdf nicht installiert - Fallback pdftoppm + tesseract + pdfunite"
  need pdfunite "Installation: apt install poppler-utils (oder ocrmypdf verwenden)"
  rasterize_pdf "$pdf" || return $?
  shopt -s nullglob
  local imgs=("$TMPWORK/pages"/page-*.png)
  shopt -u nullglob
  (( ${#imgs[@]} > 0 )) || { warn "keine Seiten extrahiert: $pdf"; return 3; }
  local img
  for img in "${imgs[@]}"; do
    tess "$img" "${img%.png}" pdf || { warn "OCR fehlgeschlagen: $img"; return 3; }
  done
  limit "$TIMEOUT" pdfunite "$TMPWORK/pages"/page-*.pdf "$TMPOUT" \
    || { warn "pdfunite fehlgeschlagen"; return 3; }
  purge_dir "$TMPWORK/pages"
}

process_one() {
  local f="$1"
  [[ -e "$f" ]] || { warn "Datei nicht gefunden: $f"; return 1; }
  [[ -f "$f" ]] || { warn "keine regulaere Datei: $f"; return 1; }
  [[ -r "$f" ]] || { warn "nicht lesbar: $f";          return 1; }
  [[ -s "$f" ]] || { warn "Datei ist leer: $f";        return 1; }
  # relative Namen mit fuehrendem '-' nie als Option an ein Werkzeug reichen
  [[ "$f" == -* ]] && f="./$f"

  local mime; mime="$(file -b --mime-type -- "$f" 2>/dev/null || echo unknown)"
  log "$f -> MIME $mime"

  if [[ "$mime" == "application/pdf" ]]; then
    if [[ "$FORMAT" == "pdf" ]]; then process_pdf_searchable "$f"
    else                              process_pdf_txt "$f"; fi
  elif [[ "$IMAGE_MIMES" == *" $mime "* ]]; then
    if [[ "$FORMAT" == "pdf" ]]; then
      tess "$f" "${TMPOUT%.pdf}" pdf || { warn "OCR fehlgeschlagen: $f"; return 3; }
    else
      ocr_image_txt "$f"
    fi
  else
    warn "nicht unterstuetzter Typ '$mime': $f (erwartet: jpg, png, bmp, gif, tiff, webp oder PDF)"
    return 1
  fi
}

# Ergebnis aus dem Temp-Verzeichnis an das Ziel uebergeben. Ohne --overwrite
# per noclobber (O_EXCL): kein Ueberschreiben, kein Folgen eines Symlinks.
place_output() {
  [[ -e "$TMPOUT" ]] || return 0
  if [[ $OVERWRITE -eq 1 ]]; then
    mv -f -- "$TMPOUT" "$OUTFILE" || die "Ausgabedatei nicht schreibbar: $OUTFILE"
  else
    ( set -o noclobber; cat -- "$TMPOUT" > "$OUTFILE" ) 2>/dev/null \
      || die "Ausgabedatei existiert bereits oder ist nicht schreibbar: $OUTFILE"
  fi
  log "geschrieben: $OUTFILE"
}

# ------------------------------------------------------------------- Ablauf --
run_all() {
  local rc=0 f
  for f in "${INPUTS[@]}"; do
    (( ${#INPUTS[@]} > 1 )) && printf -- '===== %s =====\n' "$f"
    process_one "$f" || rc=$?
  done
  return $rc
}

RC=0
if [[ -z "$OUTFILE" ]]; then
  run_all || RC=$?
elif [[ "$FORMAT" == "pdf" ]]; then
  TMPOUT="$TMPWORK/out.pdf"
  run_all || RC=$?
  if (( RC == 0 )); then
    [[ -s "$TMPOUT" ]] || die "kein PDF erzeugt" 3
    place_output
  fi
else
  # Text/TSV auch bei Teilfehlern im Stapel schreiben; Exit-Code meldet den Fehler
  TMPOUT="$TMPWORK/out.txt"
  run_all > "$TMPOUT" || RC=$?
  place_output
fi
exit "$RC"
