# Task Quest — 업적 카탈로그

업적은 `task-quest/achievements.md`에 달성 여부와 날짜를 기록.
조건 체크는 태스크 완료 시마다 자동 수행.

---

## 업적 카탈로그

### 시작 계열 — 첫 걸음

| ID | 업적 | 조건 | XP 보너스 |
|----|------|------|----------|
| `first_blood` | 🏅 First Blood | 첫 태스크 완료 (total_completed == 1) | +50 XP |
| `getting_started` | 📝 Getting Started | 태스크 5개 완료 | +30 XP |
| `centurion` | 🎊 Centurion | 태스크 100개 완료 | +200 XP |
| `five_hundred` | 🏆 Five Hundred | 태스크 500개 완료 | +500 XP |

### 속도 계열 — 빠른 실행

| ID | 업적 | 조건 | XP 보너스 |
|----|------|------|----------|
| `speed_demon` | ⚡ Speed Demon | 예상 시간의 50% 이내에 완료 (actual_hours <= estimated_hours × 0.5) | +40 XP |
| `ahead_of_schedule` | 🚀 Ahead of Schedule | 마감 1주일 이상 전에 완료 | +60 XP |
| `blitz` | 💨 Blitz | critical 태스크를 조기 완료 (마감 3일+ 전) | +80 XP |

### 연속 계열 — 꾸준함

| ID | 업적 | 조건 | XP 보너스 |
|----|------|------|----------|
| `on_fire` | 🔥 On Fire | 10일 연속 스트릭 | +100 XP |
| `unstoppable` | 💎 Unstoppable | 30일 연속 스트릭 | +300 XP |
| `legendary` | 👑 Legendary | 100일 연속 스트릭 | +1000 XP |

### 카테고리 계열 — 전문성 (동적 생성)

카테고리별로 완료 수가 기준에 도달하면 자동 생성.
`task-quest/achievements.md`의 미달성 목록에서 현황 추적.

| ID | 업적 | 조건 | XP 보너스 |
|----|------|------|----------|
| `{cat}_apprentice` | 📚 {Category} Apprentice | 해당 카테고리 태스크 10개 완료 | +50 XP |
| `{cat}_master` | 🎓 {Category} Master | 해당 카테고리 태스크 20개 완료 | +100 XP |
| `{cat}_expert` | 🎯 {Category} Expert | 해당 카테고리 태스크 50개 완료 | +200 XP |

예시: "research" 카테고리 → Research Apprentice / Research Master / Research Expert

### 특별 계열 — 독특한 도전

| ID | 업적 | 조건 | XP 보너스 |
|----|------|------|----------|
| `early_bird` | 🌅 Early Bird | 하루 오전(~12시) 중 태스크 3개 이상 완료 | +60 XP |
| `zero_inbox` | 🧹 Zero Inbox | 활성 태스크 0개 달성 (INDEX.md 활성 태스크 수 == 0) | +80 XP |
| `weekly_champion` | 📋 Weekly Champion | 주간 리뷰 기준 완료율 100% (주 시작 기준 예정 태스크 모두 완료) | +120 XP |
| `mountain_climber` | 🏔️ Mountain Climber | critical 태스크 10개 완료 | +150 XP |
| `night_owl` | 🦉 Night Owl | 자정~새벽 3시 사이에 태스크 완료 3회 | +50 XP |
| `multitasker` | 🔀 Multitasker | 하루에 서로 다른 카테고리 태스크 3개 완료 | +60 XP |
| `comeback` | 🔄 Comeback | 스트릭 리셋 후 7일 이내에 다시 7일 연속 달성 | +80 XP |

---

## 업적 조건 체크 로직

에이전트는 태스크 완료 후 다음 순서로 조건을 확인:

```
1. total_completed 업데이트
2. 시작 계열: total_completed in [1, 5, 100, 500] → 해당 업적 체크
3. 속도 계열: actual_hours, due 필드 있으면 → speed_demon, ahead_of_schedule 체크
4. 연속 계열: streak가 [10, 30, 100] 도달 → on_fire, unstoppable, legendary 체크
5. 카테고리 계열: 완료 태스크의 category 카운트 → {cat}_apprentice/master/expert 체크
6. 특별 계열: 해당 조건 충족 여부 체크
```

이미 달성한 업적은 task-quest/achievements.md에서 확인 후 스킵.

---

## achievements.md 파일 포맷

```markdown
# Achievements

## 달성 업적

| 업적 | 날짜 | 비고 |
|------|------|------|
| 🏅 First Blood | 2026-04-02 | 첫 태스크: AAAI 심사 |
| ⚡ Speed Demon | 2026-04-05 | 메일 정리 (예상 2시간 → 45분) |
| 🔥 On Fire | 2026-04-12 | 10일 연속 스트릭 |

## 미달성 업적 (다음 목표)

| 업적 | 현황 | 목표 |
|------|------|------|
| 💎 Unstoppable | 10일 스트릭 | 30일 |
| 🎊 Centurion | 완료 47개 | 100개 |
| 🎓 Research Master | 연구 태스크 12개 | 20개 |
```

### 업데이트 규칙

- 새 업적 달성 시 "달성 업적" 테이블에 행 추가
- "미달성 업적"에서 해당 항목 제거
- 카테고리 계열은 태스크 완료 시 현황 숫자 업데이트

---

## 업적 XP 보너스 처리

업적 달성 시 XP 보너스는 **태스크 XP와 별도**로 지급:

```
태스크 완료: "+80 XP (조기완료 보너스)"
업적 달성:  "+ 100 XP (🔥 On Fire 보너스)"
합산 표시:  "총 +180 XP"
```

quest-state.md의 `xp`, `total_xp` 모두 합산 반영.
