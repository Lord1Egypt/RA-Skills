# Task Quest — 게임 메커닉스

## XP 계산

### 기본 XP (priority 기준)

| priority | base_xp |
|----------|---------|
| critical | 100 |
| high     | 60  |
| medium   | 40  |
| low      | 20  |

필드 누락 시 → `medium` (40 XP)

### estimated_hours 보정

```
adjusted_xp = base_xp × (1 + estimated_hours × 0.1)
```

예시:
- critical, 5시간 → 100 × 1.5 = 150 XP
- high, 2시간 → 60 × 1.2 = 72 XP
- medium, 0시간 → 40 × 1.0 = 40 XP

### 타이밍 보너스/패널티

| 조건 | 배율 | 설명 |
|------|------|------|
| 마감 3일+ 전 완료 | ×1.5 | 조기완료 보너스 |
| 마감 1~2일 전 완료 | ×1.2 | 여유있는 완료 |
| 마감일 당일 완료 | ×1.0 | 정시 완료 |
| 마감 초과 | ×0.7 | "놓친 보너스" 프레이밍 (벌이 아님) |
| due 필드 없음 | ×1.0 | 타이밍 보정 없음 |

### 연속 보너스 (streak multiplier)

streak 배율은 타이밍 배율과 **별도** 적용 (곱산):

| streak | 배율 |
|--------|------|
| 1~4일  | ×1.0 |
| 5~9일  | ×1.2 |
| 10~29일 | ×1.5 |
| 30일+  | ×2.0 |

### 최종 계산식

```
final_xp = round(base_xp × hours_mult × timing_mult × streak_mult)
```

### 예시

| 태스크 | priority | hours | timing | streak | 결과 |
|--------|----------|-------|--------|--------|------|
| AAAI 심사 | critical | 3h | 조기 | 5일 | 100×1.3×1.5×1.2 = 234 XP |
| 메일 정리 | low | 0.5h | 정시 | 5일 | 20×1.05×1.0×1.2 = 25 XP |
| 논문 리뷰 | high | 4h | 지각 | 10일 | 60×1.4×0.7×1.5 = 88 XP |

---

## 레벨 테이블

### 누적 XP → 레벨

| Level | 레벨 도달 필요 누적 XP | 해당 레벨 구간 XP |
|-------|----------------------|-----------------|
| 1  | 0      | 0 ~ 99    |
| 2  | 100    | 100 ~ 299 |
| 3  | 300    | 300 ~ 599 |
| 4  | 600    | 600 ~ 999 |
| 5  | 1,000  | 1000 ~ 1499 |
| 6  | 1,500  | 1500 ~ 2199 |
| 7  | 2,200  | 2200 ~ 2999 |
| 8  | 3,000  | 3000 ~ 3999 |
| 9  | 4,000  | 4000 ~ 5499 |
| 10 | 5,500  | 5500 ~ 7499 |
| 11 | 7,500  | 7500 ~ 9999 |
| 12 | 10,000 | 10000 ~ 12999 |
| 13 | 13,000 | 13000 ~ 16999 |
| 14 | 17,000 | 17000 ~ 21999 |
| 15 | 22,000 | 22000 ~ 27999 |
| 16 | 28,000 | 28000 ~ 34999 |
| 17 | 35,000 | 35000 ~ 42999 |
| 18 | 43,000 | 43000 ~ 52999 |
| 19 | 53,000 | 53000 ~ 63999 |
| 20 | 64,000 | 64000+       |

### xp_to_next 계산

```
xp_to_next = next_level_threshold - total_xp
```

레벨 20 도달 시: `xp_to_next: 0` (최대 레벨)

### 레벨업 처리

1. `total_xp` 업데이트 후 레벨 재계산
2. 새 level에 해당하는 칭호(title) 업데이트 (현재 theme 기준)
3. 레벨업 메시지는 항상 강조 (daily_highlights 소모)

---

## 스트릭 로직

### 업데이트 규칙

```
today = 오늘 날짜
last = last_completed 날짜

if last == today:
    # 이미 오늘 카운트됨, streak 변화 없음
elif last == today - 1:
    # 어제 완료 → 연속
    streak += 1
    if streak > longest_streak:
        longest_streak = streak
else:
    # 하루 이상 공백 → 리셋
    streak = 1
    # 메시지: "새로운 모험의 시작!" (부정적 프레이밍 금지)

last_completed = today
```

### 스트릭 마일스톤 알림

스트릭이 다음 값에 도달하면 강조 메시지:
- 7일: "🔥 일주일 연속 달성!"
- 14일: "💪 2주 연속 달성!"
- 30일: "💎 한 달 연속 달성!"
- 60일: "🚀 두 달 연속 달성!"
- 100일: "👑 100일 연속 달성! 전설이 되었습니다!"

---

## daily_highlights 관리

강조 메시지 빈도 제한 (하루 최대 2번):

```
if highlight_date != today:
    daily_highlights = 0
    highlight_date = today

if is_highlight_worthy (레벨업, 업적, 스트릭 마일스톤):
    if daily_highlights < 2:
        daily_highlights += 1
        # 강조 메시지 표시
    else:
        # XP 한 줄만 (강조 없음)
```

강조 우선순위: 레벨업 > 업적 > 스트릭 마일스톤

---

## quest-state.md 전체 필드 정의

| 필드 | 타입 | 설명 |
|------|------|------|
| active | bool | false이면 모든 게임 요소 중단 |
| level | int | 현재 레벨 (1~20) |
| xp | int | 현재 레벨 내 XP |
| xp_to_next | int | 다음 레벨까지 남은 XP |
| title | str | 현재 테마 기준 칭호 |
| streak | int | 현재 연속 완료 일수 |
| longest_streak | int | 역대 최장 스트릭 |
| last_completed | date | 마지막 태스크 완료 날짜 |
| total_completed | int | 누적 완료 태스크 수 |
| total_xp | int | 누적 획득 XP |
| theme | str | rpg \| space \| academic \| minimal |
| daily_highlights | int | 오늘 강조 메시지 횟수 |
| highlight_date | date | daily_highlights 기준 날짜 |
