#!/bin/bash
#
# Ralph Wiggum - AI Loop Technique
# Iteracyjny system doskonalenia kodu
#

set -euo pipefail

# Konfiguracja
LMSTUDIO_URL="${LMSTUDIO_URL:-http://127.0.0.1:1234/v1}"
MODEL="${RALPH_MODEL:-qwen3.5-35b-a3b-uncensored-hauhaucs-aggressive}"
MAX_ITERATIONS="${RALPH_MAX_ITER:-3}"
VERBOSE=0
JSON_OUTPUT=0

# Kolory
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Parsowanie argumentów
usage() {
    echo "Użycie: $0 [-f FILE] [-c CODE] [-o FILE] [-p PROMPT] [-i N] [-m MODEL] [-v] [--json]"
    echo ""
    echo "Opcje:"
    echo "  -f FILE      Plik wejściowy z kodem"
    echo "  -c CODE      Kod inline (zamiast pliku)"
    echo "  -o FILE      Plik wyjściowy (domyślnie: stdout)"
    echo "  -p PROMPT    Dodatkowy kontekst/prompt"
    echo "  -i N         Max iteracji (domyślnie: 3)"
    echo "  -m MODEL     Nazwa modelu w LM Studio"
    echo "  -v           Verbose - pokaż proces"
    echo "  --json       Output w formacie JSON"
    echo "  -h           Pomoc"
    exit 1
}

log() {
    if [[ $VERBOSE -ge 1 ]]; then
        echo -e "${BLUE}[RALPH]${NC} $1" >&2
    fi
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1" >&2
}

log_success() {
    echo -e "${GREEN}[OK]${NC} $1" >&2
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1" >&2
}

# Sprawdź czy LM Studio działa
check_lmstudio() {
    if ! curl -s "$LMSTUDIO_URL/models" > /dev/null 2>&1; then
        log_error "LM Studio nie odpowiada na $LMSTUDIO_URL"
        log_error "Upewnij się że LM Studio jest uruchomione z włączonym API"
        exit 1
    fi
    log "LM Studio OK"
}

# Generator - tworzy początkowy output
generate() {
    local task="$1"
    local context="${2:-}"
    
    log "Generator: tworzenie outputu..."
    
    local system_prompt="Jesteś ekspertem programistą. Tworzysz najwyższej jakości kod. Używaj najnowszych praktyk, type hints, docstrings, obsługi błędów."
    
    local user_prompt="$task"
    if [[ -n "$context" ]]; then
        user_prompt="$user_prompt

Kontekst: $context"
    fi
    
    python3 "$(dirname "$0")/generator.py" -u "$LMSTUDIO_URL" -m "$MODEL" -t "$user_prompt" -s "$system_prompt"
}

# Krytyk - analizuje kod i znajduje problemy
criticize() {
    local code="$1"
    
    log "Krytyk: analiza kodu..."
    
    python3 "$(dirname "$0")/critic.py" -u "$LMSTUDIO_URL" -m "$MODEL" -c "$code"
}

# Naprawiacz - poprawia zgłoszone problemy
fix_code() {
    local code="$1"
    local issues="$2"
    
    log "Naprawiacz: poprawianie problemów..."
    
    local prompt="Otrzymałeś kod i listę problemów do naprawy. Napraw KAŻDY problem z listy. Nie dodawaj nowych funkcji - tylko napraw.

KOD:
\`\`\`python
$code
\`\`\`

PROBLEMY DO NAPRAWY:
$issues

Zwróć TYLKO poprawiony kod, bez dodatkowych komentarzy, bez markdown code blocks."

    curl -s "$LMSTUDIO_URL/chat/completions" \
        -H "Content-Type: application/json" \
        -d "{
            \"model\": \"$MODEL\",
            \"messages\": [
                {\"role\": \"system\", \"content\": \"Jesteś ekspertem programistą. Naprawiasz kod. Zwracasz tylko kod, bez wyjaśnień.\"},
                {\"role\": \"user\", \"content\": \"$prompt\"}
            ],
            \"temperature\": 0.2
        }" | jq -r '.choices[0].message.content' 2>/dev/null || echo "$code"
}

# Weryfikator - sprawdza czy poprawki działają
verify() {
    local code="$1"
    local original_issues="$2"
    
    log "Weryfikator: sprawdzanie poprawek..."
    
    # Sprawdź czy kod się kompiluje (dla Python)
    if echo "$code" | python3 -m py_compile - 2>/dev/null; then
        log "✓ Kod się kompiluje"
    else
        log_warn "✗ Błąd kompilacji"
        return 1
    fi
    
    # Sprawdź czy są nowe problemy
    local new_issues
    new_issues=$(criticize "$code")
    
    local issue_count
    issue_count=$(echo "$new_issues" | jq '.issues | length')
    
    if [[ "$issue_count" -eq 0 ]]; then
        log_success "Brak nowych problemów"
        return 0
    else
        log_warn "Znaleziono $issue_count nowych problemów"
        echo "$new_issues"
        return 1
    fi
}

# Główna pętla
main() {
    local input_file=""
    local code_inline=""
    local output_file=""
    local prompt_context=""
    
    # Parsowanie argumentów
    while [[ $# -gt 0 ]]; do
        case $1 in
            -f)
                input_file="$2"
                shift 2
                ;;
            -c)
                code_inline="$2"
                shift 2
                ;;
            -o)
                output_file="$2"
                shift 2
                ;;
            -p)
                prompt_context="$2"
                shift 2
                ;;
            -i)
                MAX_ITERATIONS="$2"
                shift 2
                ;;
            -m)
                MODEL="$2"
                shift 2
                ;;
            -v)
                VERBOSE=1
                shift
                ;;
            -vv)
                VERBOSE=2
                shift
                ;;
            --json)
                JSON_OUTPUT=1
                shift
                ;;
            -h|--help)
                usage
                ;;
            *)
                log_error "Nieznana opcja: $1"
                usage
                ;;
        esac
    done
    
    # Walidacja
    if [[ -z "$input_file" && -z "$code_inline" ]]; then
        log_error "Wymagany -f FILE lub -c CODE"
        usage
    fi
    
    # Sprawdź LM Studio
    check_lmstudio
    
    # Pobierz kod wejściowy
    local input_code
    if [[ -n "$input_file" ]]; then
        input_code=$(cat "$input_file")
        log "Wczytano kod z: $input_file"
    else
        input_code="$code_inline"
        log "Użyto kodu inline"
    fi
    
    # Pętla doskonaląca
    local current_code="$input_code"
    local iteration=0
    local all_issues="[]"
    
    while [[ $iteration -lt $MAX_ITERATIONS ]]; do
        iteration=$((iteration + 1))
        log "=== Iteracja $iteration/$MAX_ITERATIONS ==="
        
        # Krytyk
        local issues
        issues=$(criticize "$current_code")
        local issue_count
        issue_count=$(echo "$issues" | jq '.issues | length')
        
        if [[ "$issue_count" -eq 0 ]]; then
            log_success "Brak problemów do naprawy!"
            break
        fi
        
        log "Znaleziono $issue_count problemów"
        
        # Naprawiacz
        current_code=$(fix_code "$current_code" "$issues")
        
        # Weryfikator
        if verify "$current_code" "$issues"; then
            log_success "Weryfikacja OK"
            break
        else
            log_warn "Wymagana kolejna iteracja"
        fi
    done
    
    # Output
    if [[ $JSON_OUTPUT -eq 1 ]]; then
        local result
        result=$(jq -n \
            --arg code "$current_code" \
            --argjson iterations "$iteration" \
            --arg model "$MODEL" \
            '{code: $code, iterations: $iterations, model: $model}')
        
        if [[ -n "$output_file" ]]; then
            echo "$result" > "$output_file"
            log_success "Zapisano JSON do: $output_file"
        else
            echo "$result"
        fi
    else
        if [[ -n "$output_file" ]]; then
            echo "$current_code" > "$output_file"
            log_success "Zapisano kod do: $output_file"
        else
            echo "$current_code"
        fi
    fi
}

main "$@"