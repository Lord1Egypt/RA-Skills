#!/usr/bin/env bash
# tar — Archive management tool
# Powered by BytesAgain | bytesagain.com | hello@bytesagain.com
set -euo pipefail
VERSION="3.0.1"

BOLD='\033[1m'; GREEN='\033[0;32m'; RED='\033[0;31m'; DIM='\033[2m'; RESET='\033[0m'
die() { echo -e "${RED}Error: $1${RESET}" >&2; exit 1; }
info() { echo -e "${GREEN}✓${RESET} $1"; }

# === create: create tar archive ===
cmd_create() {
    local archive="${1:?Usage: tar create <archive.tar.gz> <files...>}"
    shift
    [ $# -eq 0 ] && die "No files specified"

    local compress=""
    case "$archive" in
        *.tar.gz|*.tgz)   compress="z" ;;
        *.tar.bz2|*.tbz2) compress="j" ;;
        *.tar.xz|*.txz)   compress="J" ;;
        *.tar)             compress="" ;;
        *) die "Unknown format: $archive (use .tar, .tar.gz, .tar.bz2, .tar.xz)" ;;
    esac

    tar -c${compress}vf "$archive" "$@" 2>&1 | while IFS= read -r line; do
        echo "  + $line"
    done

    local size
    size=$(du -h "$archive" | cut -f1)
    local count=$#
    info "Created $archive ($size, $count items)"
}

# === extract: extract tar archive ===
cmd_extract() {
    local archive="${1:?Usage: tar extract <archive> [output-dir]}"
    local outdir="${2:-.}"
    [ ! -f "$archive" ] && die "File not found: $archive"

    local compress=""
    case "$archive" in
        *.tar.gz|*.tgz)   compress="z" ;;
        *.tar.bz2|*.tbz2) compress="j" ;;
        *.tar.xz|*.txz)   compress="J" ;;
        *.tar)             compress="" ;;
    esac

    mkdir -p "$outdir"
    tar -x${compress}vf "$archive" -C "$outdir" 2>&1 | while IFS= read -r line; do
        echo "  - $line"
    done

    local count
    count=$(tar -t${compress}f "$archive" 2>/dev/null | wc -l)
    info "Extracted $count items to $outdir"
}

# === list: list archive contents ===
cmd_list() {
    local archive="${1:?Usage: tar list <archive>}"
    [ ! -f "$archive" ] && die "File not found: $archive"

    local compress=""
    case "$archive" in
        *.tar.gz|*.tgz)   compress="z" ;;
        *.tar.bz2|*.tbz2) compress="j" ;;
        *.tar.xz|*.txz)   compress="J" ;;
        *.tar)             compress="" ;;
    esac

    echo -e "${BOLD}Contents of $archive${RESET}"
    echo ""
    tar -t${compress}vf "$archive" 2>/dev/null | while IFS= read -r line; do
        echo "  $line"
    done

    local count
    count=$(tar -t${compress}f "$archive" 2>/dev/null | wc -l)
    echo ""
    echo "  Total: $count entries"
}

# === add: add files to existing archive ===
cmd_add() {
    local archive="${1:?Usage: tar add <archive.tar> <files...>}"
    shift
    [ $# -eq 0 ] && die "No files specified"
    [ ! -f "$archive" ] && die "Archive not found: $archive"

    case "$archive" in
        *.tar) ;;
        *) die "Can only append to uncompressed .tar archives" ;;
    esac

    tar -rvf "$archive" "$@" 2>&1 | while IFS= read -r line; do
        echo "  + $line"
    done
    info "Added $# items to $archive"
}

# === diff: compare two archives ===
cmd_diff() {
    local a1="${1:?Usage: tar diff <archive1> <archive2>}"
    local a2="${2:?Missing second archive}"
    [ ! -f "$a1" ] && die "Not found: $a1"
    [ ! -f "$a2" ] && die "Not found: $a2"

    echo -e "${BOLD}Comparing archives${RESET}"
    echo "  A: $a1"
    echo "  B: $a2"
    echo ""

    local tmp1 tmp2
    tmp1=$(mktemp)
    tmp2=$(mktemp)

    local c1="" c2=""
    case "$a1" in *.tar.gz|*.tgz) c1="z";; *.tar.bz2) c1="j";; *.tar.xz) c1="J";; esac
    case "$a2" in *.tar.gz|*.tgz) c2="z";; *.tar.bz2) c2="j";; *.tar.xz) c2="J";; esac

    tar -t${c1}f "$a1" 2>/dev/null | sort > "$tmp1"
    tar -t${c2}f "$a2" 2>/dev/null | sort > "$tmp2"

    local only1 only2 common
    only1=$(comm -23 "$tmp1" "$tmp2" | wc -l)
    only2=$(comm -13 "$tmp1" "$tmp2" | wc -l)
    common=$(comm -12 "$tmp1" "$tmp2" | wc -l)

    echo "  Common:  $common files"
    echo "  Only A:  $only1 files"
    echo "  Only B:  $only2 files"

    if [ "$only1" -gt 0 ]; then
        echo ""
        echo "  Only in A:"
        comm -23 "$tmp1" "$tmp2" | head -20 | while read -r f; do echo "    - $f"; done
    fi
    if [ "$only2" -gt 0 ]; then
        echo ""
        echo "  Only in B:"
        comm -13 "$tmp1" "$tmp2" | head -20 | while read -r f; do echo "    + $f"; done
    fi

    rm -f "$tmp1" "$tmp2"
}

# === info: archive metadata ===
cmd_info() {
    local archive="${1:?Usage: tar info <archive>}"
    [ ! -f "$archive" ] && die "Not found: $archive"

    local compress=""
    case "$archive" in
        *.tar.gz|*.tgz)   compress="z" ;;
        *.tar.bz2|*.tbz2) compress="j" ;;
        *.tar.xz|*.txz)   compress="J" ;;
        *.tar)             compress="" ;;
    esac

    local size
    size=$(du -h "$archive" | cut -f1)
    local count
    count=$(tar -t${compress}f "$archive" 2>/dev/null | wc -l)
    local dirs
    dirs=$(tar -t${compress}f "$archive" 2>/dev/null | grep '/$' | wc -l)
    local files=$((count - dirs))
    local mod
    mod=$(stat -c '%y' "$archive" | cut -d. -f1)

    echo -e "${BOLD}Archive Info${RESET}"
    echo "  File:       $archive"
    echo "  Size:       $size"
    echo "  Format:     $(file --brief "$archive" 2>/dev/null || echo 'unknown')"
    echo "  Entries:    $count ($files files, $dirs directories)"
    echo "  Modified:   $mod"
}

# === verify: check archive integrity ===
cmd_verify() {
    local archive="${1:?Usage: tar verify <archive>}"
    [ ! -f "$archive" ] && die "Not found: $archive"

    local compress=""
    case "$archive" in
        *.tar.gz|*.tgz)   compress="z" ;;
        *.tar.bz2|*.tbz2) compress="j" ;;
        *.tar.xz|*.txz)   compress="J" ;;
        *.tar)             compress="" ;;
    esac

    if tar -t${compress}f "$archive" > /dev/null 2>&1; then
        local count
        count=$(tar -t${compress}f "$archive" | wc -l)
        info "Archive OK — $count entries, no corruption detected"
    else
        die "Archive is corrupted or invalid"
    fi
}

# === find: search for file in archive ===
cmd_find() {
    local archive="${1:?Usage: tar find <archive> <pattern>}"
    local pattern="${2:?Missing search pattern}"
    [ ! -f "$archive" ] && die "Not found: $archive"

    local compress=""
    case "$archive" in *.tar.gz|*.tgz) compress="z";; *.tar.bz2) compress="j";; *.tar.xz) compress="J";; esac

    echo -e "${BOLD}Searching '$pattern' in $archive${RESET}"
    local found=0
    tar -t${compress}f "$archive" 2>/dev/null | grep -i "$pattern" | while IFS= read -r match; do
        echo "  $match"
        found=$((found + 1))
    done
    echo ""
}

show_help() {
    cat << EOF
tar v$VERSION — Archive management tool

Usage: tar <command> [args]

Archive Operations:
  create <archive> <files...>    Create tar archive (.tar/.tar.gz/.tar.bz2/.tar.xz)
  extract <archive> [dir]        Extract archive contents
  list <archive>                 List archive contents with details
  add <archive.tar> <files...>   Add files to uncompressed .tar archive

Analysis:
  info <archive>                 Show archive metadata (size, entries, format)
  diff <a1> <a2>                 Compare contents of two archives
  verify <archive>               Check archive integrity
  find <archive> <pattern>       Search for files matching pattern

  help                           Show this help
  version                        Show version

Supported formats: .tar, .tar.gz/.tgz, .tar.bz2/.tbz2, .tar.xz/.txz

Requires: tar, file
EOF
}

[ $# -eq 0 ] && { show_help; exit 0; }

case "$1" in
    create)   shift; cmd_create "$@" ;;
    extract)  shift; cmd_extract "$@" ;;
    list)     cmd_list "$2" ;;
    add)      shift; cmd_add "$@" ;;
    diff)     shift; cmd_diff "$@" ;;
    info)     cmd_info "$2" ;;
    verify)   cmd_verify "$2" ;;
    find)     shift; cmd_find "$@" ;;
    help|-h)  show_help ;;
    version|-v) echo "tar v$VERSION"; echo "Powered by BytesAgain | bytesagain.com | hello@bytesagain.com" ;;
    *)        echo "Unknown: $1"; show_help; exit 1 ;;
esac
