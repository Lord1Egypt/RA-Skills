#!/bin/bash
# clean-xcode-global.sh — Scan and clean global Xcode caches (~/Library/Developer)
# Usage: clean-xcode-global.sh [--dry-run] [--yes] [--keep-ios <pattern>]...
#
# Covers:
#   • ~/Library/Developer/Xcode/DerivedData/*
#   • ~/Library/Developer/Xcode/iOS DeviceSupport/*   (with --keep-ios filters)
#   • ~/Library/Developer/Xcode/watchOS DeviceSupport/*
#   • ~/Library/Developer/Xcode/tvOS DeviceSupport/*
#   • ~/Library/Developer/Xcode/macOS DeviceSupport/*
#   • ~/Library/Developer/Xcode/Archives/*   (DRY-RUN ONLY by default — see --include-archives)
#   • ~/Library/Caches/com.apple.dt.Xcode
#   • CoreSimulator unavailable devices (xcrun simctl delete unavailable)
#
# --keep-ios PATTERN may be passed multiple times. Substring match against folder name.
#   Example: --keep-ios "26.4.2" --keep-ios "18.5"
# If no --keep-ios given, by default keeps the SINGLE highest-version folder per platform.
#
# --include-archives    Also delete Archives/* (off by default — these are your signed .ipa archives!)
# --dry-run             Scan and report only, no deletions
# --yes / -y            Skip confirmation prompt

set -euo pipefail

DRY_RUN=false
AUTO_YES=false
INCLUDE_ARCHIVES=false
KEEP_PATTERNS=()

while [[ $# -gt 0 ]]; do
    case "$1" in
        --dry-run) DRY_RUN=true; shift ;;
        --yes|-y) AUTO_YES=true; shift ;;
        --include-archives) INCLUDE_ARCHIVES=true; shift ;;
        --keep-ios)
            shift
            [[ $# -gt 0 ]] || { echo "--keep-ios needs a value"; exit 1; }
            KEEP_PATTERNS+=("$1")
            shift
            ;;
        *) echo "Unknown option: $1"; exit 1 ;;
    esac
done

XCODE_DIR="$HOME/Library/Developer/Xcode"
DERIVED="$XCODE_DIR/DerivedData"
XCODE_CACHE="$HOME/Library/Caches/com.apple.dt.Xcode"
ARCHIVES="$XCODE_DIR/Archives"

# Prefer `trash` if available, fall back to rm -rf
if command -v trash >/dev/null 2>&1; then
    DEL_CMD="trash"
else
    DEL_CMD="rm -rf"
fi

human_size() {
    # macOS du -sh prints already-human size; just echo
    du -sh "$1" 2>/dev/null | awk '{print $1}'
}

size_bytes() {
    # macOS BSD du supports -A but no -b; use 1024-block then convert? simpler: stat-style not available for dirs.
    # use `du -sk` (1024-byte blocks) for delta calc
    du -sk "$1" 2>/dev/null | awk '{print $1}'
}

if $DRY_RUN; then
    echo "🔍 Dry run — scan only, no deletions"
else
    echo "🧹 清理全局 Xcode 缓存"
fi
echo ""

TOTAL_KB=0
ACTIONS=()  # array of "delete:<path>" or "simctl:unavailable"

# ── DerivedData ──
if [[ -d "$DERIVED" ]]; then
    echo "━━━ DerivedData ━━━"
    if compgen -G "$DERIVED/*" > /dev/null; then
        for d in "$DERIVED"/*; do
            sz=$(human_size "$d")
            kb=$(size_bytes "$d")
            TOTAL_KB=$((TOTAL_KB + kb))
            echo "  $sz  $(basename "$d")"
            ACTIONS+=("delete:$d")
        done
    else
        echo "  (空)"
    fi
    echo ""
fi

# ── *OS DeviceSupport ──
clean_device_support() {
    local label="$1"; shift
    local dir="$1"; shift
    [[ -d "$dir" ]] || return 0

    echo "━━━ $label ━━━"
    if ! compgen -G "$dir/*" > /dev/null; then
        echo "  (空)"; echo ""; return 0
    fi

    # Default keep: highest version folder (lexicographic sort works for typical Apple version strings well enough; use `sort -V`)
    local auto_keep=""
    if [[ ${#KEEP_PATTERNS[@]} -eq 0 ]]; then
        auto_keep=$(ls "$dir" | sort -V | tail -1 || true)
    fi

    for entry in "$dir"/*; do
        local name; name=$(basename "$entry")
        local keep=false
        if [[ ${#KEEP_PATTERNS[@]} -gt 0 ]]; then
            for p in "${KEEP_PATTERNS[@]}"; do
                if [[ "$name" == *"$p"* ]]; then keep=true; break; fi
            done
        else
            [[ "$name" == "$auto_keep" ]] && keep=true
        fi
        local sz; sz=$(human_size "$entry")
        if $keep; then
            echo "  保留 $sz  $name"
        else
            local kb; kb=$(size_bytes "$entry")
            TOTAL_KB=$((TOTAL_KB + kb))
            echo "  删除 $sz  $name"
            ACTIONS+=("delete:$entry")
        fi
    done
    echo ""
}

clean_device_support "iOS DeviceSupport"     "$XCODE_DIR/iOS DeviceSupport"
clean_device_support "watchOS DeviceSupport" "$XCODE_DIR/watchOS DeviceSupport"
clean_device_support "tvOS DeviceSupport"    "$XCODE_DIR/tvOS DeviceSupport"
clean_device_support "macOS DeviceSupport"   "$XCODE_DIR/macOS DeviceSupport"

# ── Xcode Cache ──
if [[ -d "$XCODE_CACHE" ]]; then
    sz=$(human_size "$XCODE_CACHE")
    kb=$(size_bytes "$XCODE_CACHE")
    echo "━━━ Caches/com.apple.dt.Xcode ━━━"
    echo "  $sz  (会清理)"
    TOTAL_KB=$((TOTAL_KB + kb))
    ACTIONS+=("delete:$XCODE_CACHE")
    echo ""
fi

# ── Archives (off by default) ──
if [[ -d "$ARCHIVES" ]]; then
    echo "━━━ Archives (.xcarchive) ━━━"
    if compgen -G "$ARCHIVES/*" > /dev/null; then
        for d in "$ARCHIVES"/*; do
            sz=$(human_size "$d")
            echo "  $sz  $(basename "$d")"
            if $INCLUDE_ARCHIVES; then
                kb=$(size_bytes "$d")
                TOTAL_KB=$((TOTAL_KB + kb))
                ACTIONS+=("delete:$d")
            fi
        done
        if ! $INCLUDE_ARCHIVES; then
            echo "  ⚠️  默认保留（这些是签名 .xcarchive）。要删请加 --include-archives"
        fi
    else
        echo "  (空)"
    fi
    echo ""
fi

# ── CoreSimulator unavailable ──
echo "━━━ CoreSimulator (unavailable devices) ━━━"
if command -v xcrun >/dev/null 2>&1; then
    unavail_count=$(xcrun simctl list devices 2>/dev/null | grep -c "(unavailable" || true)
    if [[ "$unavail_count" -gt 0 ]]; then
        echo "  发现 $unavail_count 个 unavailable simulator(s) — 会跑 'xcrun simctl delete unavailable'"
        ACTIONS+=("simctl:unavailable")
    else
        echo "  无 unavailable simulator"
    fi
else
    echo "  (xcrun 不可用，跳过)"
fi
echo ""

# ── Summary ──
TOTAL_MB=$((TOTAL_KB / 1024))
TOTAL_GB_INT=$((TOTAL_MB / 1024))
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if [[ "$TOTAL_GB_INT" -ge 1 ]]; then
    printf "🗑  可清理总计: ~%.1f GB\n" "$(echo "scale=1; $TOTAL_MB/1024" | bc)"
else
    echo "🗑  可清理总计: ~${TOTAL_MB} MB"
fi
echo "    + simctl delete unavailable (大小未计)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if $DRY_RUN; then
    echo ""
    echo "💡 去掉 --dry-run 执行实际清理"
    exit 0
fi

if ! $AUTO_YES; then
    echo ""
    read -p "继续? [y/N] " ans
    [[ "$ans" =~ ^[Yy]$ ]] || { echo "已取消"; exit 0; }
fi

echo ""
echo "执行中..."
for a in "${ACTIONS[@]}"; do
    case "$a" in
        delete:*)
            p="${a#delete:}"
            echo "  → $DEL_CMD $(basename "$p")"
            $DEL_CMD "$p" || echo "    ⚠️  失败"
            ;;
        simctl:unavailable)
            echo "  → xcrun simctl delete unavailable"
            xcrun simctl delete unavailable || echo "    ⚠️  失败"
            ;;
    esac
done

echo ""
echo "✅ 完成"
