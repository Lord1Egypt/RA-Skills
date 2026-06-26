---
name: task-quest
description: >
  Zero-friction gamification layer for task management.
  Adds XP, levels, streaks, and achievements to completed tasks
  with no manual input required — the agent tracks everything
  automatically. Companion skill for smart-tasks.
  Use when: user wants motivation/gamification for their tasks;
  user mentions XP, levels, streaks, achievements, or gamification;
  user asks to make task management more fun or engaging.
  NOT for: standalone use without a task system;
  complex team-based gamification or leaderboards.
---

# Task Quest

Zero-friction 게이미피케이션 레이어. 사용자는 평소처럼 일하고, 에이전트가 게임을 운영한다.
smart-tasks의 companion skill.

## Setup

Run the init script once:

```bash
bash skills/task-quest/scripts/init-quest.sh
```

This creates `task-quest/quest-state.md`, `task-quest/achievements.md`,
and `task-quest/history/`. Idempotent — safe to re-run.

After init, apply workspace integration changes from
[workspace-integration.md](references/workspace-integration.md) with user approval.

## Runtime Data Structure

- `task-quest/quest-state.md` — 레벨, XP, 스트릭, 통계 (every session startup에 읽기)
- `task-quest/achievements.md` — 달성/미달성 업적 목록
- `task-quest/history/YYYY-QN.md` — 분기별 XP/완료 이력

For full mechanics see [mechanics.md](references/mechanics.md).
For achievement catalog see [achievements.md](references/achievements.md).
For theme options see [themes.md](references/themes.md).

## Core Workflow

### 1. Session Startup

Read `task-quest/quest-state.md` alongside `tasks/INDEX.md`.
If `active: false`, skip all game elements silently.

### 2. Task Completion → XP Award

When a smart-tasks task is completed:

1. Calculate XP using priority + estimated_hours + timing bonuses.
   Full formula in [mechanics.md](references/mechanics.md).
2. Update `task-quest/quest-state.md`:
   - Increment `xp` and `total_xp`
   - Increment `total_completed`
   - Update streak (check last_completed date)
   - Recalculate `xp_to_next` and `level` if leveled up
   - Append to `## 최근 활동` (keep last 10 entries)
3. Check achievement conditions (see [achievements.md](references/achievements.md))
4. Update `task-quest/achievements.md` if new achievement unlocked

### 3. Inline Reporting (핵심: 자연스러운 삽입)

게임 요소를 **별도 메시지로 보내지 않고** 기존 응답에 자연스럽게 한 줄 추가.

**일반 완료** (매번):
> "심사 완료 처리했습니다. +80 XP ⚡ (조기완료 보너스!)"

**레벨업** (강조):
> "🎉 Level 8 달성! '마스터' 칭호 획득! 다음 목표: Level 9 (320 XP 남음)"

**업적 달성** (강조):
> "🏅 새 업적: On Fire! 10일 연속 스트릭 달성!"

**스트릭 마일스톤** (7, 14, 30, 60, 100일):
> "🔥 30일 연속 스트릭! 새 기록!"

**강조 메시지는 하루 최대 2번**. 초과 시 XP 한 줄만.

### 4. Briefing Integration

아침 브리핑에 한 줄 추가:
> "🔥 7일 연속 스트릭 중! Level 7 (340/500 XP)"

주간 리뷰에 리포트 카드 섹션 추가:
```
📊 이번 주 퀘스트 리포트
━━━━━━━━━━━━
⭐ Level 7 → 8 승급!
🔥 스트릭: 12일 (최장 기록 갱신!)
✅ 완료: 8건 | 💎 획득 XP: 420
🏅 새 업적: Scholar 달성!
```

### 5. Theme Change

사용자가 "테마 바꿔줘" → 자연어로 요청:
1. Read `task-quest/quest-state.md`
2. Update `theme` field to requested theme
3. Update `title` to match new theme's title for current level
4. Confirm: "테마를 'space'로 변경했습니다. 현재 칭호: 파일럿"

Available themes: `rpg` | `space` | `academic` | `minimal`
See [themes.md](references/themes.md) for full title tables.

### 6. Activate / Deactivate

- "게이미피케이션 끄기" / "퀘스트 중지" → `active: false` in quest-state.md
- "다시 켜기" / "퀘스트 켜기" → `active: true`
- 비활성 중에도 데이터 트래킹 계속 (재활성 시 복원 가능)

### 7. Status Query

사용자가 "내 퀘스트 현황" / "레벨이 몇이야" 등 질의 시:
1. Read `task-quest/quest-state.md`
2. Read `task-quest/achievements.md` (미달성 목표 확인용)
3. 현재 상태 요약 + 다음 목표 제시

## quest-state.md Format

```yaml
---
active: true
level: 7
xp: 340
xp_to_next: 500
title: "리서치 나이트"
streak: 5
longest_streak: 12
last_completed: 2026-04-01
total_completed: 47
total_xp: 2840
theme: rpg
daily_highlights: 0     # 오늘 강조 메시지 횟수 (자정 리셋)
highlight_date: 2026-04-01
---

## 최근 활동

- 2026-04-02: +80 XP (AAAI 심사 완료, 조기완료 보너스)
- 2026-04-01: +40 XP (메일 정리)
```

## Streak Logic

- `last_completed` 날짜가 어제이면 → streak +1
- `last_completed` 날짜가 오늘이면 → streak 유지 (이미 카운트됨)
- `last_completed` 날짜가 그 이전이면 → streak 1로 리셋 (부정적 메시지 없음 — "새로운 모험의 시작!")
- Streak 리셋 시 `longest_streak`는 유지

## Achievement Check Sequence

태스크 완료 후 다음 순서로 업적 조건 확인:
1. 시작 계열 (total_completed 기반)
2. 속도 계열 (완료 타이밍 기반)
3. 연속 계열 (streak 기반)
4. 카테고리 계열 (카테고리별 완료 수 기반)
5. 특별 계열 (기타 조건)

이미 달성한 업적은 스킵.
신규 달성 시 achievements.md 업데이트 + 인라인 알림.

## History Logging

분기가 바뀔 때 (또는 매 주간 리뷰 시):
`task-quest/history/YYYY-QN.md`에 기간 요약 기록.
포맷: 주별 완료 수 + XP + 레벨 변화.

## Best Practices

1. quest-state.md는 태스크 완료 시마다 즉시 업데이트.
2. 게임 요소는 항상 기존 응답의 끝에 추가 (별도 메시지 금지).
3. `active: false`이면 quest-state.md 업데이트도 중단.
4. XP 계산 시 task 파일의 `priority`, `estimated_hours`, `due` 필드 활용.
5. 필드 누락 시: priority → medium(40 XP), hours → 0, timing → ×1.0.
