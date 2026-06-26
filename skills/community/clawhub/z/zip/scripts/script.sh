#!/usr/bin/env bash
# zip — ZIP archive tool
# Powered by BytesAgain | bytesagain.com | hello@bytesagain.com
set -euo pipefail
VERSION="3.0.1"

BOLD='\033[1m'; GREEN='\033[0;32m'; RED='\033[0;31m'; RESET='\033[0m'
die() { echo -e "${RED}Error: $1${RESET}" >&2; exit 1; }
info() { echo -e "${GREEN}✓${RESET} $1"; }

check_deps() {
    command -v zip >/dev/null 2>&1 || die "zip not installed. Install: apt install zip / yum install zip"
    command -v unzip >/dev/null 2>&1 || die "unzip not installed. Install: apt install unzip / yum install unzip"
}

# === create: create zip archive ===
cmd_create() {
    check_deps
    local archive="${1:?Usage: zip create <archive.zip> <files...>}"
    shift
    [ $# -eq 0 ] && die "No files specified"

    zip -rv "$archive" "$@" 2>&1 | while IFS= read -r line; do
        echo "  $line"
    done

    local size
    size=$(du -h "$archive" | cut -f1)
    info "Created $archive ($size)"
}

# === extract: extract zip archive ===
cmd_extract() {
    check_deps
    local archive="${1:?Usage: zip extract <archive.zip> [output-dir]}"
    local outdir="${2:-.}"
    [ ! -f "$archive" ] && die "Not found: $archive"

    mkdir -p "$outdir"
    unzip -o "$archive" -d "$outdir" 2>&1 | while IFS= read -r line; do
        echo "  $line"
    done
    info "Extracted to $outdir"
}

# === list: list zip contents ===
cmd_list() {
    check_deps
    local archive="${1:?Usage: zip list <archive.zip>}"
    [ ! -f "$archive" ] && die "Not found: $archive"

    echo -e "${BOLD}Contents of $archive${RESET}"
    echo ""
    unzip -l "$archive" 2>/dev/null | tail -n +4 | while IFS= read -r line; do
        echo "  $line"
    done
}

# === add: add files to zip ===
cmd_add() {
    check_deps
    local archive="${1:?Usage: zip add <archive.zip> <files...>}"
    shift
    [ $# -eq 0 ] && die "No files specified"
    [ ! -f "$archive" ] && die "Archive not found: $archive"

    zip -rv "$archive" "$@" 2>&1 | while IFS= read -r line; do
        echo "  $line"
    done
    info "Added $# items to $archive"
}

# === info: show archive info ===
cmd_info() {
    check_deps
    local archive="${1:?Usage: zip info <archive.zip>}"
    [ ! -f "$archive" ] && die "Not found: $archive"

    local size
    size=$(du -h "$archive" | cut -f1)
    local count
    count=$(unzip -l "$archive" 2>/dev/null | tail -1 | awk '{print $2}')
    local uncompressed
    uncompressed=$(unzip -l "$archive" 2>/dev/null | tail -1 | awk '{print $1}')

    echo -e "${BOLD}Archive Info${RESET}"
    echo "  File:         $archive"
    echo "  Size:         $size"
    echo "  Files:        $count"
    echo "  Uncompressed: $(echo "$uncompressed" | awk '{printf "%.1f KB\n", $1/1024}')"

    # Compression ratio
    local comp_size
    comp_size=$(stat -c %s "$archive")
    if [ "$uncompressed" -gt 0 ] 2>/dev/null; then
        local ratio
        ratio=$(echo "$comp_size $uncompressed" | awk '{printf "%.1f", (1 - $1/$2) * 100}')
        echo "  Compression:  ${ratio}%"
    fi
    echo "  Modified:     $(stat -c '%y' "$archive" | cut -d. -f1)"
}

# === password: create password-protected zip ===
cmd_password() {
    check_deps
    local archive="${1:?Usage: zip password <archive.zip> <password> <files...>}"
    local pass="${2:?Missing password}"
    shift 2
    [ $# -eq 0 ] && die "No files specified"

    zip -e -P "$pass" -rv "$archive" "$@" 2>&1 | while IFS= read -r line; do
        echo "  $line"
    done
    info "Created encrypted $archive"
}

# === test: test archive integrity ===
cmd_test() {
    check_deps
    local archive="${1:?Usage: zip test <archive.zip>}"
    [ ! -f "$archive" ] && die "Not found: $archive"

    if unzip -t "$archive" > /dev/null 2>&1; then
        info "Archive OK — no errors detected"
    else
        die "Archive is corrupted"
    fi
}

# === find: search in archive ===
cmd_find() {
    check_deps
    local archive="${1:?Usage: zip find <archive.zip> <pattern>}"
    local pattern="${2:?Missing pattern}"
    [ ! -f "$archive" ] && die "Not found: $archive"

    echo -e "${BOLD}Searching '$pattern' in $archive${RESET}"
    unzip -l "$archive" 2>/dev/null | grep -i "$pattern" | while IFS= read -r line; do
        echo "  $line"
    done
}

# === diff: compare two zip archives ===
cmd_diff() {
    check_deps
    local a1="${1:?Usage: zip diff <archive1.zip> <archive2.zip>}"
    local a2="${2:?Missing second archive}"
    [ ! -f "$a1" ] && die "Not found: $a1"
    [ ! -f "$a2" ] && die "Not found: $a2"

    local tmp1 tmp2
    tmp1=$(mktemp)
    tmp2=$(mktemp)

    unzip -l "$a1" 2>/dev/null | tail -n +4 | head -n -2 | awk '{print $NF}' | sort > "$tmp1"
    unzip -l "$a2" 2>/dev/null | tail -n +4 | head -n -2 | awk '{print $NF}' | sort > "$tmp2"

    echo -e "${BOLD}Comparing archives${RESET}"
    echo "  A: $a1"
    echo "  B: $a2"

    local only1 only2 common
    only1=$(comm -23 "$tmp1" "$tmp2" | wc -l)
    only2=$(comm -13 "$tmp1" "$tmp2" | wc -l)
    common=$(comm -12 "$tmp1" "$tmp2" | wc -l)

    echo "  Common: $common | Only A: $only1 | Only B: $only2"

    if [ "$only1" -gt 0 ]; then
        echo "  Only in A:"
        comm -23 "$tmp1" "$tmp2" | head -10 | while read -r f; do echo "    - $f"; done
    fi
    if [ "$only2" -gt 0 ]; then
        echo "  Only in B:"
        comm -13 "$tmp1" "$tmp2" | head -10 | while read -r f; do echo "    + $f"; done
    fi

    rm -f "$tmp1" "$tmp2"
}

show_help() {
    cat << EOF
zip v$VERSION — ZIP archive tool

Usage: zip <command> [args]

Archive Operations:
  create <archive.zip> <files...>        Create ZIP archive
  extract <archive.zip> [dir]            Extract archive
  list <archive.zip>                     List contents
  add <archive.zip> <files...>           Add files to archive
  password <archive> <pass> <files...>   Create encrypted ZIP

Analysis:
  info <archive.zip>                     Archive metadata
  test <archive.zip>                     Test integrity
  find <archive.zip> <pattern>           Search for files
  diff <a1.zip> <a2.zip>                 Compare two archives

  help                                   Show this help
  version                                Show version

Requires: zip, unzip
EOF
}

[ $# -eq 0 ] && { show_help; exit 0; }

case "$1" in
    create)   shift; cmd_create "$@" ;;
    extract)  shift; cmd_extract "$@" ;;
    list)     cmd_list "$2" ;;
    add)      shift; cmd_add "$@" ;;
    info)     cmd_info "$2" ;;
    password) shift; cmd_password "$@" ;;
    test)     cmd_test "$2" ;;
    find)     shift; cmd_find "$@" ;;
    diff)     shift; cmd_diff "$@" ;;
    help|-h)  show_help ;;
    version|-v) echo "zip v$VERSION"; echo "Powered by BytesAgain | bytesagain.com | hello@bytesagain.com" ;;
    *)        echo "Unknown: $1"; show_help; exit 1 ;;
esac
