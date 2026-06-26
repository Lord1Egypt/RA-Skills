#!/bin/bash
# Remotion Anti-Template Quality Checker
# Usage: bash check-quality.sh <file-or-directory>
# Exit code: 0 = pass, 1 = warnings found

set -uo pipefail

TARGET="${1:-.}"
WARNINGS=0
WARN_MSGS=""

warn() {
  WARNINGS=$((WARNINGS + 1))
  WARN_MSGS="${WARN_MSGS}\n⚠ $1"
}

# Collect all .tsx files
if [ -f "$TARGET" ]; then
  FILES="$TARGET"
else
  FILES=$(find "$TARGET" -name '*.tsx' -not -path '*/node_modules/*' -not -name 'Root.tsx' -not -name 'index.ts' 2>/dev/null || true)
fi

[ -z "$FILES" ] && echo "No .tsx files found" && exit 0

# ─── 1. Uniform stagger pattern (i * N) ───
if echo "$FILES" | xargs grep -lE 'delay[=:}]\s*\{?\s*i\s*\*\s*[0-9]+' >/dev/null 2>&1; then
  MATCHED=$(echo "$FILES" | xargs grep -lE 'delay[=:}]\s*\{?\s*i\s*\*\s*[0-9]+' 2>/dev/null | xargs -I{} basename {})
  warn "UNIFORM_STAGGER: 'delay={i * N}' in ${MATCHED}. Use organic delays like [0, 5, 13, 21]."
fi

# ─── 2. Same spring config reused across file ───
for f in $FILES; do
  SPRING_CONFIGS=$(grep -oE 'damping:\s*[0-9]+' "$f" 2>/dev/null | sort | uniq -c | sort -rn | head -1)
  if [ -n "$SPRING_CONFIGS" ]; then
    COUNT=$(echo "$SPRING_CONFIGS" | awk '{print $1}')
    if [ "$COUNT" -gt 3 ]; then
      warn "UNIFORM_SPRING: $(basename $f) uses the same damping value ${COUNT}x. Vary spring configs by element weight (heavy: damping 18-25, light: 6-10)."
    fi
  fi
done

# ─── 3. Only WipeTransition used (no transition variety) ───
for f in $FILES; do
  WIPE_COUNT=$(grep -c 'WipeTransition' "$f" 2>/dev/null || true)
  if [ "$WIPE_COUNT" -gt 2 ]; then
    OTHER_TRANSITIONS=$(grep -cE '(FadeTransition|ScaleTransition|ClipReveal|clipPath.*inset)' "$f" 2>/dev/null || true)
    if [ "$OTHER_TRANSITIONS" -eq 0 ]; then
      warn "SINGLE_TRANSITION: $(basename $f) uses WipeTransition ${WIPE_COUNT}x with no alternatives. Mix transition types."
    fi
  fi
done

# ─── 4. All-centered layout (every scene centered) ───
for f in $FILES; do
  CENTER_COUNT=$(grep -c "justifyContent: 'center'" "$f" 2>/dev/null || true)
  TOTAL_FILLS=$(grep -c 'AbsoluteFill\|<Sequence' "$f" 2>/dev/null || true)
  if [ "$CENTER_COUNT" -gt 4 ] && [ "$TOTAL_FILLS" -gt 0 ]; then
    OFF_CENTER=$(grep -cE "(justifyContent: '(flex-start|flex-end|space-between)'|textAlign: '(left|right)')" "$f" 2>/dev/null || true)
    if [ "$OFF_CENTER" -eq 0 ]; then
      warn "ALL_CENTERED: $(basename $f) has ${CENTER_COUNT} centered layouts with no off-center variation. Add asymmetry to at least one scene."
    fi
  fi
done

# ─── 5. Generic translateY + opacity reveal (template #1 pattern) ───
for f in $FILES; do
  GENERIC_REVEAL=$(grep -cE 'translateY.*spring|translateY.*interpolate.*\[100.*0\]' "$f" 2>/dev/null || true)
  MASK_REVEAL=$(grep -cE 'clipPath|clip-path|maskImage|mask-image' "$f" 2>/dev/null || true)
  CHAR_STAGGER=$(grep -cE 'split.*map|\.charAt|charIndex|wordIndex' "$f" 2>/dev/null || true)
  if [ "$GENERIC_REVEAL" -gt 2 ] && [ "$MASK_REVEAL" -eq 0 ] && [ "$CHAR_STAGGER" -eq 0 ]; then
    warn "GENERIC_REVEAL: $(basename $f) uses translateY+opacity reveal ${GENERIC_REVEAL}x. Add at least one mask-reveal (clipPath) or per-word/per-char stagger."
  fi
done

# ─── 6. No SFX audio (music only) ───
COMPOSITION_FILES=$(echo "$FILES" | xargs grep -lE '<Audio.*src.*bgm|<Audio.*src.*music' 2>/dev/null || true)
for f in $COMPOSITION_FILES; do
  SFX_COUNT=$(grep -cE '<Audio.*src.*(sfx|impact|whoosh|hit|click)' "$f" 2>/dev/null || true)
  if [ "$SFX_COUNT" -eq 0 ]; then
    warn "NO_SFX: $(basename $f) has BGM but no SFX. Add impact/whoosh sounds synced to transitions and text reveals."
  fi
done

# ─── 7. Long static scene (Sequence > 8s at 30fps = 240 frames) ───
for f in $FILES; do
  LONG_SCENES=$(grep -oE 'durationInFrames=\{?[0-9]+' "$f" 2>/dev/null | grep -oE '[0-9]+' | while read dur; do
    if [ "$dur" -gt 240 ]; then
      echo "$dur"
    fi
  done)
  if [ -n "$LONG_SCENES" ]; then
    for dur in $LONG_SCENES; do
      SECS=$((dur / 30))
      warn "LONG_SCENE: $(basename $f) has a ${SECS}s scene (${dur} frames). Break into sub-scenes or vary the visual composition within."
    done
  fi
done

# ─── 8. No social proof beat in 30s promo ───
for f in $FILES; do
  IS_30S=$(grep -c 'durationInFrames.*900\|Promo30\|30秒' "$f" 2>/dev/null || true)
  if [ "$IS_30S" -gt 0 ]; then
    HAS_SOCIAL_PROOF=$(grep -ciE 'social.proof|stars|rating|users|downloads|free.*no.*account|レビュー|評価|ユーザー' "$f" 2>/dev/null || true)
    if [ "$HAS_SOCIAL_PROOF" -eq 0 ]; then
      warn "NO_SOCIAL_PROOF: $(basename $f) is a 30s promo with no social proof beat. Add a 'Free. 4.8 stars.' or download count frame."
    fi
  fi
done

# ─── Output ───
if [ "$WARNINGS" -gt 0 ]; then
  echo ""
  echo "━━━ Remotion Quality Check: ${WARNINGS} warning(s) ━━━"
  echo -e "$WARN_MSGS"
  echo ""
  echo "📖 Details: .claude/skills/remotion/references/anti-template-checklist.md"
  exit 1
else
  echo "✓ Remotion quality check passed"
  exit 0
fi
