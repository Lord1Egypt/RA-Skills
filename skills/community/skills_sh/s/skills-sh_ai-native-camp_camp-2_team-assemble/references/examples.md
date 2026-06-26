# Team Assemble - Worked Examples

## Example 1: DB 마이그레이션

**사용자 입력**: "팀 구성해서 Supabase에서 PostgreSQL로 마이그레이션 해줘"

### Phase 1 제안

```
팀 구성 제안: migration-team

| # | 역할 | 모델 | 담당 작업 | 의존성 |
|---|------|------|----------|--------|
| 1 | schema-analyst | opus | Supabase 현재 스키마, RLS 정책, 함수 분석 | - |
| 2 | migration-planner | opus | 마이그레이션 전략 수립 (순서, 위험요소, 롤백) | #1 |
| 3 | schema-writer | sonnet | PostgreSQL DDL 스크립트 작성 | #2 |
| 4 | data-migrator | sonnet | 데이터 이전 스크립트 (pg_dump/restore) | #2 |
| 5 | validator | sonnet | 데이터 무결성 검증 쿼리 작성 | #3, #4 |
```

### Phase 2 도구 호출

```
TeamCreate(team_name: "migration-team", description: "Supabase → PostgreSQL 마이그레이션")

TaskCreate(subject: "#1 schema-analyst: Supabase 스키마 분석", ...)
TaskCreate(subject: "#2 migration-planner: 마이그레이션 전략 수립", ...)
TaskCreate(subject: "#3 schema-writer: DDL 스크립트 작성", ...)
TaskCreate(subject: "#4 data-migrator: 데이터 이전 스크립트", ...)
TaskCreate(subject: "#5 validator: 무결성 검증", ...)

TaskUpdate(taskId: "2", addBlockedBy: ["1"])
TaskUpdate(taskId: "3", addBlockedBy: ["2"])
TaskUpdate(taskId: "4", addBlockedBy: ["2"])
TaskUpdate(taskId: "5", addBlockedBy: ["3", "4"])
```

### Phase 3 실행 순서

1. **Round 1** (병렬 없음 — #1만 독립): Task(schema-analyst, opus)
2. **Round 2** (#2는 #1 결과 필요): Task(migration-planner, opus, 선행결과 포함)
3. **Round 3** (병렬 — #3, #4 독립): Task(schema-writer, sonnet) + Task(data-migrator, sonnet) 동시
4. **Round 4** (#5는 #3+#4 필요): Task(validator, sonnet, 선행결과 포함)

---

## Example 2: 경쟁사 분석 리포트

**사용자 입력**: "전문가 팀으로 AI 코딩 도구 경쟁사 분석 리포트 만들어줘"

### Phase 1 제안

```
팀 구성 제안: competitor-analysis-team

| # | 역할 | 모델 | 담당 작업 | 의존성 |
|---|------|------|----------|--------|
| 1 | market-researcher | opus | 주요 경쟁사 식별 및 시장 동향 조사 | - |
| 2 | product-analyst | opus | 각 제품 기능/가격/차별점 비교 분석 | - |
| 3 | tech-reviewer | sonnet | 기술 스택, 아키텍처 비교 | - |
| 4 | report-writer | sonnet | 조사 결과 종합 리포트 작성 | #1, #2, #3 |
```

### Phase 3 실행 순서

1. **Round 1** (병렬 — #1, #2, #3 모두 독립): 3개 Task 동시 호출
2. **Round 2** (#4는 모든 결과 필요): Task(report-writer, sonnet, 3개 결과 포함)

---

## Example 3: 풀스택 기능 구현

**사용자 입력**: "팀으로 해줘 — 사용자 인증 시스템 구현"

### Phase 1 제안

```
팀 구성 제안: auth-team

| # | 역할 | 모델 | 담당 작업 | 의존성 |
|---|------|------|----------|--------|
| 1 | architect | opus | 인증 아키텍처 설계 (JWT/세션, OAuth) | - |
| 2 | backend-dev | sonnet | API 엔드포인트 구현 (login, register, refresh) | #1 |
| 3 | frontend-dev | sonnet | 로그인/회원가입 UI 구현 | #1 |
| 4 | test-writer | sonnet | E2E 테스트 작성 | #2, #3 |
```

### Phase 3 실행 순서

1. **Round 1**: Task(architect, opus)
2. **Round 2** (병렬 — #2, #3 독립): Task(backend-dev, sonnet) + Task(frontend-dev, sonnet) 동시
3. **Round 3**: Task(test-writer, sonnet, 선행결과 포함)
