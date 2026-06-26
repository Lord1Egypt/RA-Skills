#!/bin/bash
# clean-cache.sh — Scan and clean build caches in a project directory
# Usage: clean-cache.sh <target-dir> [--dry-run] [--yes]

set -euo pipefail

# ── Args ──
TARGET_DIR=""
DRY_RUN=false
AUTO_YES=false

for arg in "$@"; do
    case "$arg" in
        --dry-run) DRY_RUN=true ;;
        --yes|-y) AUTO_YES=true ;;
        -*) echo "Unknown option: $arg"; exit 1 ;;
        *) TARGET_DIR="$arg" ;;
    esac
done

if [[ -z "$TARGET_DIR" ]]; then
    echo "Usage: clean-cache.sh <target-dir> [--dry-run] [--yes]"
    exit 1
fi

TARGET_DIR="$(cd "$TARGET_DIR" && pwd)"

if $DRY_RUN; then
    echo "🔍 Dry run — scan only, no deletions"
    echo ""
fi

echo "📁 Target: $TARGET_DIR"
echo ""

# ── Cache patterns ──
# Each entry: "label|find-args"
PATTERNS=(
    "SPM .build|-name .build -type d -not -path */.git/*"
    "DerivedData|-name DerivedData -type d"
    "xcresult bundles|-name *.xcresult -type d"
    "Pods|-name Pods -type d -not -path */node_modules/*"
    "Carthage/Build|-path */Carthage/Build -type d"
    "node_modules|-name node_modules -type d -prune"
    "Gradle .gradle|-name .gradle -type d"
    "Gradle build|-name build -type d -path */.gradle/../build"
    "Rust target|-name target -type d -path */Cargo.toml/../target"
    "Python __pycache__|-name __pycache__ -type d"
    ".pytest_cache|-name .pytest_cache -type d"
    ".mypy_cache|-name .mypy_cache -type d"
    "Go build cache|-name go-build -type d -path *cache*"
)

declare -a FOUND_LABELS=()
declare -a FOUND_PATHS=()
declare -a FOUND_SIZES=()
GRAND_TOTAL=0

for pattern in "${PATTERNS[@]}"; do
    IFS='|' read -r label find_args <<< "$pattern"
    
    # Collect matching dirs
    matches=()
    while IFS= read -r -d '' dir; do
        matches+=("$dir")
    done < <(eval "find \"$TARGET_DIR\" $find_args -print0 2>/dev/null" || true)
    
    if [[ ${#matches[@]} -eq 0 ]]; then
        continue
    fi

    subtotal=0
    echo "━━━ $label ━━━"
    for dir in "${matches[@]}"; do
        size_mb=$(du -sm "$dir" 2>/dev/null | awk '{print $1}')
        subtotal=$((subtotal + size_mb))
        rel="${dir#$TARGET_DIR/}"
        if [[ $size_mb -ge 1024 ]]; then
            printf "  %6.1f GB  %s\n" "$(echo "$size_mb / 1024" | bc -l)" "$rel"
        else
            printf "  %6d MB  %s\n" "$size_mb" "$rel"
        fi
    done

    if [[ $subtotal -ge 1024 ]]; then
        printf "  小计: %.1f GB\n" "$(echo "$subtotal / 1024" | bc -l)"
    else
        echo "  小计: ${subtotal} MB"
    fi
    echo ""

    FOUND_LABELS+=("$label")
    FOUND_PATHS+=("$(IFS=$'\n'; echo "${matches[*]}")")
    FOUND_SIZES+=("$subtotal")
    GRAND_TOTAL=$((GRAND_TOTAL + subtotal))
done

# ── Git info ──
if [[ -d "$TARGET_DIR/.git" ]]; then
    git_mb=$(du -sm "$TARGET_DIR/.git" 2>/dev/null | awk '{print $1}')
    echo "━━━ Git 仓库 (不会删除) ━━━"
    if [[ $git_mb -ge 1024 ]]; then
        printf "  .git: %.1f GB — 可用 'git gc --aggressive' 压缩\n" "$(echo "$git_mb / 1024" | bc -l)"
    else
        echo "  .git: ${git_mb} MB — 可用 'git gc --aggressive' 压缩"
    fi
    echo ""
fi

# ── Summary ──
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if [[ $GRAND_TOTAL -ge 1024 ]]; then
    printf "🗑  可清理总计: %.1f GB (%d MB)\n" "$(echo "$GRAND_TOTAL / 1024" | bc -l)" "$GRAND_TOTAL"
else
    echo "🗑  可清理总计: ${GRAND_TOTAL} MB"
fi
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

if [[ $GRAND_TOTAL -eq 0 ]]; then
    echo "✅ 没有需要清理的缓存"
    exit 0
fi

if $DRY_RUN; then
    echo "💡 去掉 --dry-run 执行实际清理"
    exit 0
fi

# ── Confirm ──
if ! $AUTO_YES; then
    read -p "⚠️  确认删除以上内容？(y/N) " confirm
    if [[ "$confirm" != "y" && "$confirm" != "Y" ]]; then
        echo "❌ 已取消"
        exit 1
    fi
fi

echo ""
echo "🧹 清理中..."

for i in "${!FOUND_LABELS[@]}"; do
    label="${FOUND_LABELS[$i]}"
    IFS=$'\n' read -ra paths <<< "${FOUND_PATHS[$i]}"
    for p in "${paths[@]}"; do
        rm -rf "$p" 2>/dev/null || true
    done
    echo "  ✅ $label 已清理"
done

echo ""
if [[ $GRAND_TOTAL -ge 1024 ]]; then
    printf "🎉 已释放约 %.1f GB\n" "$(echo "$GRAND_TOTAL / 1024" | bc -l)"
else
    echo "🎉 已释放约 ${GRAND_TOTAL} MB"
fi
