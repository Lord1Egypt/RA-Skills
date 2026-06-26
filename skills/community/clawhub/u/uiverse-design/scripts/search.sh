#!/bin/bash
# Search Uiverse Galaxy components
# Usage: search.sh <category> [keyword] [--tailwind|--css|--all]
# Examples:
#   search.sh Buttons                    # List all buttons
#   search.sh Buttons hover              # Search buttons with "hover" tag
#   search.sh Cards gradient --tailwind  # Search tailwind gradient cards
#   search.sh --all glow                 # Search all categories for "glow"
#   search.sh --tags                     # List all available tags
#   search.sh --stats                    # Show category statistics

# Auto-detect skill directory
SCRIPT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
GALAXY_DIR="$SCRIPT_DIR/assets/galaxy"

if [ ! -d "$GALAXY_DIR" ]; then
    echo "Error: Galaxy assets not found at $GALAXY_DIR"
    exit 1
fi

cd "$GALAXY_DIR"

# Show stats
if [ "$1" = "--stats" ]; then
    echo "=== Uiverse Galaxy Component Stats ==="
    for dir in */; do
        [ "$dir" = ".git/" ] && continue
        count=$(find "$dir" -name "*.html" 2>/dev/null | wc -l)
        echo "  ${dir%/}: $count"
    done
    total=$(find . -maxdepth 2 -name "*.html" | wc -l)
    echo "  ---"
    echo "  TOTAL: $total"
    exit 0
fi

# Show all tags
if [ "$1" = "--tags" ]; then
    echo "=== Available Tags ==="
    grep -roh 'Tags: [^*]*' --include="*.html" 2>/dev/null | \
        sed 's/Tags: //' | tr ',' '\n' | sed 's/^ *//;s/ *$//' | \
        tr '[:upper:]' '[:lower:]' | sort | uniq -c | sort -rn | head -50
    exit 0
fi

# Show a random sample for inspiration
if [ "$1" = "--sample" ]; then
    category="${2:-Buttons}"
    count="${3:-3}"
    if [ ! -d "$category" ]; then
        echo "Category '$category' not found."
        exit 1
    fi
    echo "=== Random $category Samples ==="
    ls "$category"/*.html 2>/dev/null | shuf | head -n "$count" | while read -r f; do
        fname=$(basename "$f")
        tags=$(grep -oP 'Tags:\s*\K[^*/\n]+' "$f" 2>/dev/null | tr '[:upper:]' '[:lower:]')
        style="css"
        has_style=$(grep -c '<style' "$f")
        has_tw=$(grep -cP 'class="[^"]*(?:bg-|text-|flex |rounded-|p-\d|m-\d)' "$f")
        if [ "$has_style" -eq 0 ] && [ "$has_tw" -gt 0 ]; then style="tailwind"; fi
        echo "  [$style] $fname"
        echo "    tags: $tags"
        echo "    path: $f"
        echo ""
    done
    exit 0
fi

# Parse arguments
STYLE_FILTER="all"
SEARCH_ALL=false
CATEGORY=""
KEYWORD=""

while [[ $# -gt 0 ]]; do
    case "$1" in
        --tailwind) STYLE_FILTER="tailwind"; shift ;;
        --css) STYLE_FILTER="css"; shift ;;
        --mixed) STYLE_FILTER="mixed"; shift ;;
        --all) SEARCH_ALL=true; shift ;;
        *)
            if [ -z "$CATEGORY" ] && [ "$SEARCH_ALL" = false ]; then
                CATEGORY="$1"
            elif [ -z "$KEYWORD" ]; then
                KEYWORD="$1"
            fi
            shift
            ;;
    esac
done

# Search function
search_dir() {
    local dir="$1"
    local keyword="$2"
    local style="$3"
    local count=0

    for f in "$dir"/*.html; do
        [ -f "$f" ] || continue
        fname=$(basename "$f")

        content=$(cat "$f" 2>/dev/null)
        tags=$(echo "$content" | grep -oP 'Tags:\s*\K[^*/\n]+' | tr '[:upper:]' '[:lower:]')

        has_style=$(echo "$content" | grep -c '<style')
        has_tw=$(echo "$content" | grep -cP 'class="[^"]*(?:bg-|text-|flex |rounded-|p-\d|m-\d)')

        if [ "$has_style" -eq 0 ] && [ "$has_tw" -gt 0 ]; then
            file_style="tailwind"
        elif [ "$has_style" -gt 0 ] && [ "$has_tw" -gt 0 ]; then
            file_style="mixed"
        else
            file_style="css"
        fi

        if [ "$style" != "all" ] && [ "$file_style" != "$style" ]; then
            continue
        fi

        if [ -n "$keyword" ]; then
            echo "$tags" | grep -qi "$keyword" || \
            echo "$fname" | grep -qi "$keyword" || \
            echo "$content" | grep -qi "$keyword" || continue
        fi

        echo "  [$file_style] $fname  (tags: $tags)"
        count=$((count + 1))

        if [ $count -ge 20 ]; then
            echo "  ... (showing first 20, use more specific keyword to narrow)"
            break
        fi
    done

    echo "  Found: $count components"
}

if [ "$SEARCH_ALL" = true ]; then
    echo "=== Searching all categories for: ${KEYWORD:-<all>} ==="
    for dir in */; do
        [ "$dir" = ".git/" ] && continue
        results=$(search_dir "${dir%/}" "$KEYWORD" "$STYLE_FILTER" 2>/dev/null)
        if echo "$results" | grep -q "Found: [^0]"; then
            echo ""
            echo "📁 ${dir%/}"
            echo "$results"
        fi
    done
elif [ -n "$CATEGORY" ]; then
    if [ ! -d "$CATEGORY" ]; then
        echo "Category '$CATEGORY' not found. Available:"
        ls -d */ 2>/dev/null | grep -v '.git' | sed 's/\//  /'
        exit 1
    fi
    echo "=== $CATEGORY === (keyword: ${KEYWORD:-<all>}, style: $STYLE_FILTER)"
    search_dir "$CATEGORY" "$KEYWORD" "$STYLE_FILTER"
else
    echo "Usage: search.sh <category> [keyword] [--tailwind|--css|--all]"
    echo "       search.sh --all [keyword]"
    echo "       search.sh --stats"
    echo "       search.sh --tags"
    echo "       search.sh --sample [category] [count]"
    echo ""
    echo "Categories:"
    ls -d */ 2>/dev/null | grep -v '.git' | sed 's/\//  /'
fi
