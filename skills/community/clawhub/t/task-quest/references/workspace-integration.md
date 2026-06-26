# Workspace Integration Guide — task-quest

task-quest는 smart-tasks의 companion skill.
**이 스킬은 워크스페이스 파일을 직접 수정하지 않는다.**
아래 변경사항을 사용자 승인 후 적용.

---

## 통합 개요

```
[smart-tasks] 태스크 완료
      ↓ 에이전트가 자동 연계
[task-quest] quest-state.md 업데이트 (XP, 스트릭)
      ↓
[task-quest] 업적 조건 체크
      ↓
[에이전트] 응답에 게임 요소 포함
```

- task-quest는 `tasks/` 데이터를 **읽기만** 함 (쓰기 없음)
- 별도 크론 불필요 — 기존 smart-tasks 크론 프롬프트 수정으로 통합
- 태스크 완료 시 에이전트가 자동으로 XP 계산 + quest-state.md 업데이트

---

## 1. smart-tasks 크론 프롬프트 수정

### Daily Morning Briefing 수정

```diff
 openclaw cron add \
   --name "daily-task-briefing" \
   --schedule "0 8 * * *" \
   --channel telegram \
   --model sonnet \
   --prompt "Perform a daily task briefing.

 1. Read tasks/INDEX.md for current status.
 2. If overdue tasks exist, warn at the top.
 3. List today's and this week's deadlines by priority.
 4. Read relevant task files from tasks/active/ for context (estimated hours, notes).
 5. Suggest a recommended work order with brief reasoning.
 6. Check recent memory/ entries for additional context.
+7. If task-quest/quest-state.md exists and active: true, read it and append one line:
+   streak status + current level + XP progress. Use theme-appropriate tone.
+   Example: '🔥 7일 연속 스트릭 중! Level 7 (340/500 XP)'

 Format: Concise message under 500 chars. Use emoji. Include a morning greeting.
 If no active tasks, send a brief 'all clear' message."
```

### Weekly Review 수정

```diff
 openclaw cron add \
   --name "weekly-task-review" \
   --schedule "0 20 * * 0" \
   --channel telegram \
   --model sonnet \
   --prompt "Perform a weekly task review.

 1. Read tasks/INDEX.md and ALL files in tasks/active/.
 2. Summarize tasks completed this week (scan tasks/done/).
 3. Preview next week's upcoming deadlines.
 4. Detect stale tasks: active for 2+ weeks with no progress updates.
    Suggest: close, defer, or break down.
 5. Archive cleanup: move tasks in tasks/done/ older than 30 days
    to tasks/archive/YYYY-QN/ (quarter based on completion date).
    Update file status to 'archived'.
 6. Refresh INDEX.md: recalculate counters, re-sort sections, update date.
 7. Send structured report to chat.
+8. If task-quest/quest-state.md exists and active: true, append Quest Report section:
+   - Level changes this week
+   - Streak status
+   - Total completed + XP earned this week
+   - New achievements unlocked
+   Format as the report card block shown in SKILL.md.

 Format: Structured report with sections (Completed, Upcoming, Stale, Archived).
 Keep actionable — user should be able to make quick decisions."
```

---

## 2. AGENTS.md 변경

### Session Startup에 quest-state 추가

```diff
 ## Session Startup

 Before doing anything else:

 1. Read `SOUL.md` — this is who you are
 2. Read `USER.md` — this is who you're helping
 3. Read `memory/YYYY-MM-DD.md` (today + yesterday) for recent context
 4. Read `tasks/INDEX.md` — current task status at a glance
+5. If `task-quest/quest-state.md` exists: read it for gamification state.
+   If active: false, skip all game elements during this session.
 6. **If in MAIN SESSION** (direct chat with your human): Also read `MEMORY.md`

 Don't ask permission. Just do it.
```

### Task Quest 섹션 추가

```diff
 ## Tasks

 `tasks/` is the task management system.

+## Task Quest
+
+`task-quest/` is the gamification layer for tasks.
+
+- **quest-state.md**: XP, level, streak. Read at session startup if present.
+- **achievements.md**: Achievement progress. Read only when checking/reporting.
+- **active: false**: Skip all game elements entirely.
+
+### Quest Operating Rules
+
+- On task complete: calculate XP → update quest-state.md → check achievements.
+- Always append game elements to existing response (never send separately).
+- Max 2 highlight messages per day (level up, achievement, streak milestone).
+- Regular completions: one-line XP note only.
+- Streak reset: positive framing only — "새로운 모험의 시작!"
+
```

---

## 3. HEARTBEAT.md 변경

```diff
 ## Task Check

 - Read `tasks/INDEX.md` for current overview
 - Check for overdue tasks (due < today)
 - Check for tasks due within 24 hours
 - If urgent task found AND not already alerted today:
   - Send brief, actionable reminder
   - Read task detail file if helpful context exists
 - If nothing urgent → skip silently (no noise)
 - Log alert to `memory/YYYY-MM-DD.md` to avoid duplicate alerts
+
+## Quest Check (optional, if task-quest installed)
+
+- If task-quest/quest-state.md exists and active: true:
+  - Check if streak may be at risk (last_completed == yesterday, no task today yet)
+  - If streak >= 7 and at risk: mention briefly alongside task check
+  - Do NOT send standalone quest heartbeat messages
```

---

## 적용 방법

1. 위 diff들을 사용자에게 보여주고 승인 받기
2. 크론 수정: 기존 크론 삭제 후 수정된 프롬프트로 재등록
   ```bash
   openclaw cron delete --name daily-task-briefing
   openclaw cron delete --name weekly-task-review
   # 수정된 프롬프트로 재등록 (cron-templates.md 참고)
   ```
3. AGENTS.md, HEARTBEAT.md 파일 수동 편집
4. 각 파일 편집 후 파싱 정상 여부 확인

---

## 데이터 흐름 다이어그램

```
tasks/active/T-001.md     task-quest/quest-state.md
    priority: high    →   xp: 340 → 400
    estimated_hours: 2    streak: 5 → 6
    due: 2026-04-05       total_completed: 47 → 48
    completed: today

                          task-quest/achievements.md
                              (조건 체크 → 필요 시 업데이트)
```

## 주의사항

- task-quest는 `tasks/` 디렉토리에 절대 쓰지 않는다
- `task-quest/` 데이터만 읽고 씀
- smart-tasks가 없으면 task-quest도 동작하지 않음 (의존성)
- 크론은 smart-tasks 크론을 수정하는 방식 (별도 크론 추가 불필요)
