#!/bin/sh
# init-quest.sh — Initialize the task-quest/ directory structure.
# Idempotent: skips existing files/directories.
# Usage: bash skills/task-quest/scripts/init-quest.sh [workspace_root]

set -e

WORKSPACE="${1:-.}"
QUEST_DIR="$WORKSPACE/task-quest"

echo "Initializing task-quest system in $QUEST_DIR ..."

# Create directories
for dir in "$QUEST_DIR" "$QUEST_DIR/history"; do
  if [ ! -d "$dir" ]; then
    mkdir -p "$dir"
    echo "  Created: $dir"
  else
    echo "  Exists:  $dir (skipped)"
  fi
done

# Create quest-state.md
STATE_FILE="$QUEST_DIR/quest-state.md"
if [ ! -f "$STATE_FILE" ]; then
  TODAY=$(date +%Y-%m-%d)
  cat > "$STATE_FILE" << EOF
---
active: true
level: 1
xp: 0
xp_to_next: 100
title: "견습생"
streak: 0
longest_streak: 0
last_completed: ""
total_completed: 0
total_xp: 0
theme: rpg
daily_highlights: 0
highlight_date: $TODAY
---

## 최근 활동

_아직 완료한 태스크가 없습니다. 첫 태스크를 완료해보세요!_
EOF
  echo "  Created: $STATE_FILE"
else
  echo "  Exists:  $STATE_FILE (skipped)"
fi

# Create achievements.md
ACH_FILE="$QUEST_DIR/achievements.md"
if [ ! -f "$ACH_FILE" ]; then
  TODAY=$(date +%Y-%m-%d)
  cat > "$ACH_FILE" << EOF
# Achievements

> Initialized: $TODAY

## 달성 업적

_아직 달성한 업적이 없습니다._

| 업적 | 날짜 | 비고 |
|------|------|------|

## 미달성 업적 (다음 목표)

| 업적 | 현황 | 목표 |
|------|------|------|
| 🏅 First Blood | 완료 0개 | 1개 |
| 📝 Getting Started | 완료 0개 | 5개 |
| ⚡ Speed Demon | — | 예상 시간 50% 내 완료 |
| 🚀 Ahead of Schedule | — | 마감 1주 전 완료 |
| 🔥 On Fire | 스트릭 0일 | 10일 |
| 💎 Unstoppable | 스트릭 0일 | 30일 |
| 👑 Legendary | 스트릭 0일 | 100일 |
| 🌅 Early Bird | — | 오전 중 3개 완료 |
| 🧹 Zero Inbox | — | 활성 태스크 0개 |
| 📋 Weekly Champion | — | 주간 완료율 100% |
| 🏔️ Mountain Climber | critical 0개 | 10개 |
| 🎊 Centurion | 완료 0개 | 100개 |
EOF
  echo "  Created: $ACH_FILE"
else
  echo "  Exists:  $ACH_FILE (skipped)"
fi

# Detect current quarter for history
YEAR=$(date +%Y)
MONTH=$(date +%m)
if [ "$MONTH" -le 3 ]; then
  QUARTER="Q1"
elif [ "$MONTH" -le 6 ]; then
  QUARTER="Q2"
elif [ "$MONTH" -le 9 ]; then
  QUARTER="Q3"
else
  QUARTER="Q4"
fi

HISTORY_FILE="$QUEST_DIR/history/${YEAR}-${QUARTER}.md"
if [ ! -f "$HISTORY_FILE" ]; then
  TODAY=$(date +%Y-%m-%d)
  cat > "$HISTORY_FILE" << EOF
# Quest History — ${YEAR} ${QUARTER}

> Started: $TODAY

## 주별 요약

| 주 | 완료 | XP | 레벨 변화 | 비고 |
|----|------|----|----------|------|

## 분기 목표

_분기 목표를 설정해보세요! (예: 레벨 5 달성, 스트릭 30일 등)_
EOF
  echo "  Created: $HISTORY_FILE"
else
  echo "  Exists:  $HISTORY_FILE (skipped)"
fi

echo ""
echo "Done. Task Quest system ready!"
echo ""
echo "Next steps:"
echo "  1. Apply workspace integration changes from:"
echo "     skills/task-quest/references/workspace-integration.md"
echo "  2. Complete your first task to earn XP and unlock First Blood!"
echo "  3. To change theme: tell the agent '테마 바꿔줘 → space/academic/minimal'"
