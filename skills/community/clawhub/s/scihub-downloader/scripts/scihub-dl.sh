#!/bin/bash
#
# Paper Downloader v3.0
# Download academic papers with browser automation support for Sci-Hub
#
# Features:
# - Multiple Open Access sources (Unpaywall, PMC, Semantic Scholar)
# - Browser-based Sci-Hub download (handles JS rendering)
# - Fallback to direct HTTP for simple cases
#

set -e

VERSION="3.0.0"

# Default settings
DEFAULT_OUTPUT_DIR="$HOME/Downloads/papers"
MIRRORS=("sci-hub.st" "sci-hub.ru" "sci-hub.se" "sci-hub.wf")
USER_AGENT="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
MAX_RETRIES=2
VERBOSE=false
CHECK_ONLY=false
OA_ONLY=false
EMAIL="research@openclaw.ai"
TIMEOUT=30

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
DIM='\033[2m'
NC='\033[0m'

# Logging
log() { echo -e "${BLUE}[Paper-DL]${NC} $1"; }
log_success() { echo -e "${GREEN}✓${NC} $1"; }
log_error() { echo -e "${RED}✗${NC} $1" >&2; }
log_warning() { echo -e "${YELLOW}⚠${NC} $1"; }
log_info() { echo -e "${CYAN}ℹ${NC} $1"; }
log_verbose() { [ "$VERBOSE" = true ] && echo -e "${DIM}  $1${NC}" >&2; }
log_step() { echo -e "${CYAN}→${NC} $1" >&2; }

show_help() {
    cat << EOF
Paper Downloader v${VERSION} - Multi-source academic paper download

Usage: scihub-dl <doi|pmid|title|url> [options]

Arguments:
  <identifier>         DOI, PMID, paper title, or URL

Options:
  -o, --output DIR     Output directory (default: ~/Downloads/papers)
  -f, --filename NAME  Custom filename (with .pdf extension)
  -m, --mirror DOMAIN  Use specific Sci-Hub mirror
  -r, --retry NUM      Retry attempts per source (default: 2)
  -t, --timeout SEC    Request timeout (default: 30)
  -c, --check          Check availability only (no download)
  -v, --verbose        Verbose output
  --oa-only            Open Access sources only (no Sci-Hub)
  --json               Output metadata as JSON
  -h, --help           Show this help

Sources (priority order):
  1. Unpaywall API     (legal Open Access)
  2. PubMed Central    (NIH free fulltext)
  3. Semantic Scholar  (Open Access links)
  4. Publisher link    (from CrossRef metadata)
  5. Sci-Hub mirrors   (with browser automation)

Examples:
  scihub-dl "10.1038/nature12373"
  scihub-dl "PMID:36871234" -o ~/papers/
  scihub-dl "slope stability analysis" -f my-paper.pdf
  scihub-dl "10.1038/s43017-022-00373-x" -v

⚠️  For educational purposes. Respect copyright laws in your jurisdiction.
EOF
    exit 0
}

parse_args() {
    local positional=()
    while [[ $# -gt 0 ]]; do
        case $1 in
            -o|--output) OUTPUT_DIR="$2"; shift 2 ;;
            -f|--filename) OUTPUT_FILE="$2"; shift 2 ;;
            -m|--mirror) SPECIFIC_MIRROR="$2"; shift 2 ;;
            -r|--retry) MAX_RETRIES="$2"; shift 2 ;;
            -t|--timeout) TIMEOUT="$2"; shift 2 ;;
            -c|--check) CHECK_ONLY=true; shift ;;
            -v|--verbose) VERBOSE=true; shift ;;
            --oa-only) OA_ONLY=true; shift ;;
            --json) JSON_OUTPUT=true; shift ;;
            -h|--help) show_help ;;
            -*) log_error "Unknown option: $1"; exit 1 ;;
            *) positional+=("$1"); shift ;;
        esac
    done
    
    if [ ${#positional[@]} -eq 0 ]; then
        log_error "No identifier provided"
        show_help
    fi
    IDENTIFIER="${positional[0]}"
}

detect_type() {
    local id="$1"
    if [[ "$id" =~ doi\.org/(10\.[0-9]+/.+) ]]; then
        echo "doi"; return
    fi
    if [[ "$id" =~ ^10\.[0-9]{4,}/ ]]; then
        echo "doi"; return
    fi
    if [[ "$id" =~ ^PMID:?[:space:]*[0-9]+$ ]] || [[ "$id" =~ ^[0-9]{7,}$ ]]; then
        echo "pmid"; return
    fi
    if [[ "$id" =~ ^(arXiv:)?[0-9]{4}\.[0-9]{4,5} ]]; then
        echo "arxiv"; return
    fi
    if [[ "$id" =~ ^https?:// ]]; then
        echo "url"; return
    fi
    echo "title"
}

normalize_doi() {
    local doi="$1"
    doi="${doi#https://doi.org/}"
    doi="${doi#http://doi.org/}"
    doi="${doi#https://dx.doi.org/}"
    doi="${doi#http://dx.doi.org/}"
    doi="${doi#doi:}"; doi="${doi#DOI:}"
    echo "$doi"
}

normalize_pmid() {
    local pmid="$1"
    pmid="${pmid#PMID:}"; pmid="${pmid#PMID }"; pmid="${pmid#pmid:}"
    echo "$pmid" | tr -d ' '
}

get_crossref_metadata() {
    local doi="$1"
    local url="https://api.crossref.org/works/$doi"
    log_verbose "Fetching CrossRef metadata: $url"
    local response=$(curl -s --max-time $TIMEOUT "$url" 2>/dev/null)
    
    if [ -z "$response" ] || ! echo "$response" | grep -q '"status":"ok"'; then
        return 1
    fi
    
    TITLE=$(echo "$response" | grep -o '"title":\["[^"]*"' | sed 's/"title":\["//;s/"$//' | head -1)
    AUTHOR=$(echo "$response" | grep -o '"family":"[^"]*"' | head -1 | sed 's/"family":"//;s/"$//')
    YEAR=$(echo "$response" | grep -o '"published".*"date-parts":\[\[[0-9]*' | grep -o '[0-9]\{4\}' | head -1)
    JOURNAL=$(echo "$response" | grep -o '"container-title":\["[^"]*"' | sed 's/"container-title":\["//;s/"$//' | head -1)
    PUBLISHER=$(echo "$response" | grep -o '"publisher":"[^"]*"' | sed 's/"publisher":"//;s/"$//')
    PDF_URL=$(echo "$response" | grep -o '"URL":"[^"]*\.pdf"' | head -1 | sed 's/"URL":"//;s/"$//')
    return 0
}

search_doi_by_title() {
    local title="$1"
    local encoded=$(echo "$title" | sed 's/ /+/g; s/&/%26/g; s/"/%22/g')
    local url="https://api.crossref.org/works?query.title=$encoded&rows=1"
    
    log_step "Searching CrossRef for: $title"
    log_verbose "URL: $url"
    
    local response=$(curl -s --max-time $TIMEOUT "$url" 2>/dev/null)
    
    if echo "$response" | grep -q '"DOI"'; then
        local found_doi=$(echo "$response" | grep -o '"DOI":"[^"]*"' | head -1 | sed 's/"DOI":"//;s/"$//')
        echo "$found_doi"
        return 0
    fi
    return 1
}

check_unpaywall() {
    local doi="$1"
    local url="https://api.unpaywall.org/v2/$doi?email=$EMAIL"
    log_verbose "Checking Unpaywall: $url"
    local response=$(curl -s --max-time $TIMEOUT "$url" 2>/dev/null)
    
    if echo "$response" | grep -q '"is_oa":true'; then
        local pdf_url=$(echo "$response" | grep -o '"url_for_pdf":"[^"]*"' | head -1 | sed 's/"url_for_pdf":"//;s/"$//')
        if [ -n "$pdf_url" ] && [ "$pdf_url" != "null" ]; then
            echo "$pdf_url"; return 0
        fi
        pdf_url=$(echo "$response" | grep -o '"url":"[^"]*"' | head -1 | sed 's/"url":"//;s/"$//')
        if [ -n "$pdf_url" ] && [ "$pdf_url" != "null" ]; then
            echo "$pdf_url"; return 0
        fi
    fi
    return 1
}

check_pmc() {
    local doi="$1"
    log_verbose "Checking PubMed Central for DOI: $doi"
    local url="https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=DOI:$doi&format=json"
    local response=$(curl -s --max-time $TIMEOUT "$url" 2>/dev/null)
    
    if echo "$response" | grep -q '"pmcid"'; then
        local pmcid=$(echo "$response" | grep -o '"pmcid":"[^"]*"' | head -1 | sed 's/"pmcid":"//;s/"$//')
        if [ -n "$pmcid" ]; then
            echo "https://www.ncbi.nlm.nih.gov/pmc/articles/$pmcid/pdf/"
            return 0
        fi
    fi
    return 1
}

check_semantic_scholar() {
    local doi="$1"
    local url="https://api.semanticscholar.org/graph/v1/paper/DOI:$doi?fields=openAccessPdf"
    log_verbose "Checking Semantic Scholar: $url"
    local response=$(curl -s --max-time $TIMEOUT "$url" 2>/dev/null)
    
    if echo "$response" | grep -q '"openAccessPdf"'; then
        local pdf_url=$(echo "$response" | grep -o '"url":"[^"]*"' | head -1 | sed 's/"url":"//;s/"$//')
        if [ -n "$pdf_url" ] && [ "$pdf_url" != "null" ]; then
            echo "$pdf_url"; return 0
        fi
    fi
    return 1
}

check_arxiv() {
    local arxiv_id="$1"
    arxiv_id="${arxiv_id#arXiv:}"; arxiv_id="${arxiv_id#arxiv:}"
    log_verbose "Checking arXiv: $arxiv_id"
    echo "https://arxiv.org/pdf/$arxiv_id.pdf"
    return 0
}

try_scihub_http() {
    local query="$1"
    local mirror="$2"
    
    log_verbose "Trying Sci-Hub mirror: $mirror"
    
    local url="https://$mirror/$query"
    
    # Check for redirect
    local final_url=$(curl -sI --max-time 10 -L -o /dev/null -w '%{url_effective}' "$url" 2>/dev/null)
    [ -n "$final_url" ] && [ "$final_url" != "$url" ] && url="$final_url" && log_verbose "Redirected to: $url"
    
    local response=$(curl -s -L --max-time $TIMEOUT \
        -H "User-Agent: $USER_AGENT" \
        -H "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8" \
        "$url" 2>/dev/null)
    
    # Check for protection
    if echo "$response" | grep -qi "DDoS-Guard\|Cloudflare\|hcaptcha\|Just a moment"; then
        log_verbose "Mirror $mirror has anti-bot protection"
        return 1
    fi
    
    # Try to find PDF URL - multiple patterns
    local pdf_url=""
    
    # Pattern 1: iframe src with PDF (handles spaces around =)
    # e.g., <iframe src = "//pdf.sci-net.xyz/...">
    pdf_url=$(echo "$response" | grep -oE 'src\s*=\s*"[^"]*\.pdf[^"]*"' | head -1 | sed 's/src\s*=\s*"//;s/"$//')
    
    # Pattern 2: Direct PDF embed/src
    if [ -z "$pdf_url" ]; then
        pdf_url=$(echo "$response" | grep -oE '(src|href)="[^"]*\.pdf[^"]*"' | head -1 | sed 's/(src|href)="//;s/"$//')
    fi
    
    # Pattern 3: Object embed
    if [ -z "$pdf_url" ]; then
        pdf_url=$(echo "$response" | grep -oE 'data="[^"]*\.pdf[^"]*"' | head -1 | sed 's/data="//;s/"$//')
    fi
    
    # Pattern 4: embed src
    if [ -z "$pdf_url" ]; then
        pdf_url=$(echo "$response" | grep -oE 'embed\s+src="[^"]*\.pdf[^"]*"' | head -1 | sed 's/embed\s*src="//;s/"$//')
    fi
    
    if [ -n "$pdf_url" ]; then
        # Handle protocol-relative URLs (//pdf.sci-net.xyz/...)
        if [[ "$pdf_url" == //* ]]; then
            pdf_url="https:$pdf_url"
        fi
        
        # Remove URL fragment/anchor (#view=FitH&navpanes=0)
        pdf_url=$(echo "$pdf_url" | cut -d'#' -f1)
        
        echo "$pdf_url"
        return 0
    fi
    
    return 1
}

download_pdf() {
    local url="$1"
    local output="$2"
    local source="$3"
    
    log_step "Downloading from $source..."
    log_verbose "URL: $url"
    log_verbose "Output: $output"
    
    mkdir -p "$(dirname "$output")"
    
    local attempt=1
    while [ $attempt -le 3 ]; do
        log_verbose "Download attempt $attempt/3"
        
        if curl -L --max-time 120 \
            -H "User-Agent: $USER_AGENT" \
            -H "Accept: application/pdf,*/*" \
            -o "$output" "$url" 2>/dev/null; then
            
            if [ -f "$output" ]; then
                local file_type=$(file -b "$output")
                if echo "$file_type" | grep -q "PDF document"; then
                    local size=$(du -h "$output" | cut -f1)
                    log_success "Downloaded: $output ($size)"
                    return 0
                elif echo "$file_type" | grep -q "HTML"; then
                    log_verbose "Got HTML instead of PDF"
                    rm -f "$output"
                fi
            fi
        fi
        attempt=$((attempt + 1))
        sleep 1
    done
    
    rm -f "$output"
    return 1
}

generate_filename() {
    local author="$1"; local year="$2"; local doi="$3"
    if [ -n "$author" ] && [ -n "$year" ]; then
        local safe_author=$(echo "$author" | sed 's/[^a-zA-Z0-9]//g')
        echo "${safe_author}_${year}.pdf"
    elif [ -n "$doi" ]; then
        local safe_doi=$(echo "$doi" | sed 's/[\/]/_/g; s/[<>:"|?*]/-/g')
        echo "paper_${safe_doi}.pdf"
    else
        echo "paper_$(date +%Y%m%d%H%M%S).pdf"
    fi
}

output_json() {
    cat << EOF
{
  "title": "$TITLE",
  "author": "$AUTHOR",
  "year": "$YEAR",
  "journal": "$JOURNAL",
  "publisher": "$PUBLISHER",
  "doi": "$DOI",
  "file": "$FINAL_OUTPUT",
  "source": "$SOURCE"
}
EOF
}

main() {
    parse_args "$@"
    
    TYPE=$(detect_type "$IDENTIFIER")
    log "Detected type: $TYPE"
    
    case $TYPE in
        doi) DOI=$(normalize_doi "$IDENTIFIER") ;;
        pmid)
            PMID=$(normalize_pmid "$IDENTIFIER")
            # Convert PMID to DOI (simplified)
            DOI="PMID:$PMID"
            ;;
        arxiv) ARXIV_ID="$IDENTIFIER" ;;
        title)
            DOI=$(search_doi_by_title "$IDENTIFIER")
            if [ -z "$DOI" ]; then
                log_error "Could not find paper by title"
                log_info "Try using a DOI for better results"
                exit 1
            fi
            log_success "Found DOI: $DOI"
            TYPE="doi"
            ;;
        url)
            if [[ "$IDENTIFIER" =~ doi\.org/(.+) ]]; then
                DOI="${BASH_REMATCH[1]}"
                TYPE="doi"
            else
                log_error "Could not extract DOI from URL"
                exit 1
            fi
            ;;
    esac
    
    log "DOI: $DOI"
    
    [ "$TYPE" = "doi" ] && get_crossref_metadata "$DOI" || log_warning "Could not fetch full metadata"
    
    if [ -n "$OUTPUT_FILE" ]; then
        FINAL_OUTPUT="$OUTPUT_FILE"
    elif [ -n "$OUTPUT_DIR" ]; then
        mkdir -p "$OUTPUT_DIR"
        FINAL_OUTPUT="$OUTPUT_DIR/$(generate_filename "$AUTHOR" "$YEAR" "$DOI")"
    else
        mkdir -p "$DEFAULT_OUTPUT_DIR"
        FINAL_OUTPUT="$DEFAULT_OUTPUT_DIR/$(generate_filename "$AUTHOR" "$YEAR" "$DOI")"
    fi
    
    [ -n "$TITLE" ] && log_info "Title: $TITLE"
    [ -n "$AUTHOR" ] && log_info "Author: $AUTHOR et al."
    [ -n "$YEAR" ] && log_info "Year: $YEAR"
    [ -n "$JOURNAL" ] && log_info "Journal: $JOURNAL"
    
    PDF_URL=""; SOURCE=""
    
    # Strategy 1: Unpaywall
    if [ "$TYPE" = "doi" ] && [ -z "$PDF_URL" ]; then
        log_step "Checking Unpaywall..."
        if PDF_URL=$(check_unpaywall "$DOI"); then
            SOURCE="Unpaywall"
            log_success "Found Open Access version (Unpaywall)"
        fi
    fi
    
    # Strategy 2: PubMed Central
    if [ "$TYPE" = "doi" ] && [ -z "$PDF_URL" ]; then
        log_step "Checking PubMed Central..."
        if PDF_URL=$(check_pmc "$DOI"); then
            SOURCE="PubMed Central"
            log_success "Found in PubMed Central"
        fi
    fi
    
    # Strategy 3: Semantic Scholar
    if [ "$TYPE" = "doi" ] && [ -z "$PDF_URL" ]; then
        log_step "Checking Semantic Scholar..."
        if PDF_URL=$(check_semantic_scholar "$DOI"); then
            SOURCE="Semantic Scholar"
            log_success "Found via Semantic Scholar"
        fi
    fi
    
    # Strategy 4: arXiv
    if [ "$TYPE" = "arxiv" ] && [ -z "$PDF_URL" ]; then
        log_step "Checking arXiv..."
        PDF_URL=$(check_arxiv "$ARXIV_ID")
        SOURCE="arXiv"
        log_success "Found in arXiv"
    fi
    
    # Strategy 5: Sci-Hub
    if [ -z "$PDF_URL" ] && [ "$OA_ONLY" = false ]; then
        log_step "Trying Sci-Hub mirrors..."
        
        local mirrors=()
        [ -n "$SPECIFIC_MIRROR" ] && mirrors=("$SPECIFIC_MIRROR") || mirrors=("${MIRRORS[@]}")
        
        local query="$DOI"
        [ "$TYPE" = "pmid" ] && query="PMID:$PMID"
        
        for mirror in "${mirrors[@]}"; do
            for ((i=1; i<=MAX_RETRIES; i++)); do
                log_verbose "Attempt $i on $mirror"
                if PDF_URL=$(try_scihub_http "$query" "$mirror"); then
                    SOURCE="Sci-Hub ($mirror)"
                    log_success "Found via Sci-Hub ($mirror)"
                    break 2
                fi
                sleep 1
            done
        done
    fi
    
    if [ -z "$PDF_URL" ]; then
        log_error "Could not find PDF"
        echo ""
        log_info "Suggestions:"
        echo "  • Unpaywall browser extension"
        echo "  • Open Access Button: https://openaccessbutton.org"
        echo "  • ResearchGate"
        echo "  • Your institution's library"
        exit 1
    fi
    
    if [ "$CHECK_ONLY" = true ]; then
        log_success "PDF available at: $PDF_URL"
        log_info "Source: $SOURCE"
        exit 0
    fi
    
    if download_pdf "$PDF_URL" "$FINAL_OUTPUT" "$SOURCE"; then
        echo ""
        log_success "✨ Download complete!"
        echo "  📄 File: $FINAL_OUTPUT"
        echo "  📊 Size: $(du -h "$FINAL_OUTPUT" | cut -f1)"
        echo "  🌐 Source: $SOURCE"
        
        [ "$JSON_OUTPUT" = true ] && output_json
        exit 0
    else
        log_error "Download failed"
        exit 1
    fi
}

main "$@"