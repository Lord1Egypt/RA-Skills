#!/bin/bash

# Skills Finder - Multi-Source Skill Discovery Engine
# Supports: ClawHub (clawhub.ai) + Skills.sh
# Supports ANY language for user input

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_FINDER_DIR="$(dirname "$SCRIPT_DIR")"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

print_status() {
    echo -e "${BLUE}[skills-finder]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

print_source() {
    echo -e "${CYAN}[$1]${NC}"
}

# Universal language detection using Unicode ranges
detect_language() {
    local query="$1"
    
    # Chinese
    if echo "$query" | grep -qE '[\x{4E00}-\x{9FFF}]'; then
        echo "zh"
        return
    fi
    
    # Japanese
    if echo "$query" | grep -qE '[\x{3040}-\x{30FF}\x{4E00}-\x{9FFF}]'; then
        echo "ja"
        return
    fi
    
    # Korean
    if echo "$query" | grep -qE '[\x{AC00}-\x{D7AF}\x{1100}-\x{11FF}]'; then
        echo "ko"
        return
    fi
    
    # Arabic
    if echo "$query" | grep -qE '[\x{0600}-\x{06FF}\x{0750}-\x{077F}]'; then
        echo "ar"
        return
    fi
    
    # Hebrew
    if echo "$query" | grep -qE '[\x{0590}-\x{05FF}]'; then
        echo "he"
        return
    fi
    
    # Cyrillic
    if echo "$query" | grep -qE '[\x{0400}-\x{04FF}]'; then
        echo "ru"
        return
    fi
    
    # Thai
    if echo "$query" | grep -qE '[\x{0E00}-\x{0E7F}]'; then
        echo "th"
        return
    fi
    
    # Devanagari
    if echo "$query" | grep -qE '[\x{0900}-\x{097F}]'; then
        echo "hi"
        return
    fi
    
    # Latin-based
    if echo "$query" | grep -qE '[a-zA-Z]'; then
        if echo "$query" | grep -qiE 'buscar|skill|herramienta|instalar|el|la|un|una'; then
            echo "es"
            return
        fi
        if echo "$query" | grep -qiE 'trouver|chercher|outil|installer|le|la|un|une'; then
            echo "fr"
            return
        fi
        echo "en"
        return
    fi
    
    echo "en"
}

# Check if task requires chaining
detect_chain_needed() {
    local query="$1"
    local chain_keywords="and|和|と|그리고|y enviar|send to|发送到|送信|+|→"
    
    if echo "$query" | grep -qiE "$chain_keywords"; then
        echo "true"
    else
        echo "false"
    fi
}

# Search ClawHub
search_clawhub() {
    local query="$1"
    local limit="$2"
    
    print_source "ClawHub"
    echo "Searching: '$query'"
    
    npx clawhub@latest search "$query" --limit "$limit" 2>&1 || {
        print_warning "ClawHub search failed or rate limited"
    fi
}

# Search Skills.sh
search_skills() {
    local query="$1"
    
    print_source "Skills.sh"
    echo "Searching: '$query'"
    
    npx skills find "$query" 2>&1 || {
        print_warning "Skills.sh search failed"
    fi
}

# Show usage
usage() {
    cat << EOF
Skills Finder - Multi-Source Skill Discovery (v1.6.0)

Supported Sources: ClawHub (clawhub.ai) + Skills.sh (skills.sh)
Supported Languages: ALL

Usage: skills-finder <command> [options]

Commands:
    search <query>     Search skills (default: both sources)
    install <name>     Install a skill
    list               List installed skills
    sources            Show available skill sources

Options:
    --source <name>   Source: clawhub, skills, or all (default: all)
    --limit N         Limit results (default: 10)
    --exact           Exact name match
    --verbose         Detailed output

Examples:
    # Search both sources
    skills-finder search "weather"
    skills-finder search "github integration"
    
    # Search specific source
    skills-finder search "weather" --source clawhub
    skills-finder search "weather" --source skills
    
    # Install
    skills-finder install weather --source clawhub
    skills-finder install @skills/weather --source skills

EOF
    exit 1
}

# Search command
cmd_search() {
    local query=""
    local limit=10
    local source="all"
    local exact=false
    local verbose=false

    while [[ $# -gt 0 ]]; do
        case $1 in
            --source)
                source="$2"
                shift 2
                ;;
            --limit)
                limit="$2"
                shift 2
                ;;
            --exact)
                exact=true
                shift
                ;;
            --verbose)
                verbose=true
                shift
                ;;
            -*)
                echo "Unknown: $1"
                usage
                ;;
            *)
                query="$1"
                shift
                ;;
        esac
    done

    if [[ -z "$query" ]]; then
        print_error "Query required"
        usage
    fi

    local lang=$(detect_language "$query")
    local needs_chain=$(detect_chain_needed "$query")

    print_status "Searching for: '$query' (lang: $lang, source: $source)"
    echo ""

    case "$source" in
        clawhub)
            search_clawhub "$query" "$limit"
            ;;
        skills)
            search_skills "$query"
            ;;
        all)
            search_clawhub "$query" "$limit"
            echo ""
            search_skills "$query"
            ;;
        *)
            print_error "Unknown source: $source"
            usage
            ;;
    esac

    echo ""
    if [[ "$needs_chain" == "true" ]]; then
        print_status "Multi-step task detected"
    fi
}

# Install command
cmd_install() {
    local name="$1"
    local source="all"

    while [[ $# -gt 0 ]]; do
        case $1 in
            --source)
                source="$2"
                shift 2
                ;;
            *)
                name="$1"
                shift
                ;;
        esac
    done

    if [[ -z "$name" ]]; then
        print_error "Skill name required"
        usage
    fi

    print_status "Installing: $name from $source"
    echo ""

    case "$source" in
        clawhub)
            npx clawhub@latest install "$name" 2>&1
            ;;
        skills)
            npx skills add "$name" 2>&1
            ;;
        all)
            print_status "Trying ClawHub first..."
            npx clawhub@latest install "$name" 2>&1 || {
                print_status "Trying Skills.sh..."
                npx skills add "$name" 2>&1
            }
            ;;
    esac
}

# List command
cmd_list() {
    print_status "Installed skills:"
    echo ""
    print_source "ClawHub"
    npx clawhub@latest list 2>&1 || echo "(none)"
    echo ""
    print_source "Skills.sh"
    npx skills list 2>&1 || echo "(none)"
}

# Sources command
cmd_sources() {
    echo "Available Skill Sources:"
    echo ""
    echo "1. ClawHub (clawhub.ai)"
    echo "   - 5,400+ AI assistant skills"
    echo "   - npx clawhub@latest search <query>"
    echo ""
    echo "2. Skills.sh (skills.sh)"
    echo "   - Modular agent skill packages"
    echo "   - npx skills find <query>"
    echo ""
    echo "Default: Search both sources"
}

# Main
main() {
    if [[ $# -eq 0 ]]; then
        usage
    fi

    local cmd="$1"
    shift

    case "$cmd" in
        search)
            cmd_search "$@"
            ;;
        install)
            cmd_install "$@"
            ;;
        list)
            cmd_list
            ;;
        sources)
            cmd_sources
            ;;
        help|--help|-h)
            usage
            ;;
        *)
            print_error "Unknown: $cmd"
            usage
            ;;
    esac
}

main "$@"
