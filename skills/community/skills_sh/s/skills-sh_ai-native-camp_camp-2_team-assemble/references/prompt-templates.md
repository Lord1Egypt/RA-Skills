# Teammate Prompt Templates

## 기본 구조

모든 teammate 프롬프트는 5개 섹션으로 구성:

```
## 맥락
{프로젝트 배경과 이 작업이 전체에서 차지하는 위치}

## 목표
{구체적으로 무엇을 달성해야 하는지}

## 제약조건
- {하지 말아야 할 것}
- {변경하면 안 되는 파일/범위}
- {따라야 할 규칙}

## 출력 형식
{결과물의 형태 — 텍스트 요약, 파일 생성, 코드 등}

## 팀 정보
- team_name: {team-name}
- task_id: {task-id}
- 작업 완료 시 TaskUpdate(taskId: "{task-id}", status: "completed") 호출
```

## 역할별 프롬프트 예시

### Analyst (분석가)

```
## 맥락
Supabase 기반 프로젝트를 셀프호스팅 PostgreSQL로 마이그레이션하는 작업의 첫 단계.
프로젝트 루트: /Users/bong/team-attention/deep-thought

## 목표
현재 Supabase 스키마를 분석하고 문서화:
1. 모든 테이블, 컬럼, 타입, 관계 (FK)
2. RLS 정책 목록
3. Supabase 전용 기능 (auth, storage, realtime) 의존성
4. Edge Functions 목록

## 제약조건
- 코드를 수정하지 말 것 — 분석만 수행
- Supabase 대시보드 접근 불가, 로컬 파일만 분석

## 출력 형식
마크다운 문서로 반환:
- 테이블별 스키마 요약 테이블
- Supabase 전용 의존성 목록
- 마이그레이션 시 주의사항

## 팀 정보
- team_name: migration-team
- task_id: 1
- 완료 시 TaskUpdate(taskId: "1", status: "completed")
```

### Implementer (구현자)

```
## 맥락
인증 아키텍처가 설계 완료됨. JWT + refresh token 방식.
프레임워크: Next.js 14 (App Router), Prisma ORM.

선행 작업 결과:
{architect_result}

## 목표
설계를 기반으로 백엔드 API 구현:
1. POST /api/auth/register — 회원가입
2. POST /api/auth/login — 로그인 (JWT 발급)
3. POST /api/auth/refresh — 토큰 갱신
4. POST /api/auth/logout — 로그아웃
5. Prisma 스키마에 User 모델 추가

## 제약조건
- src/app/api/auth/ 디렉토리에만 파일 생성
- 기존 코드 수정 금지
- 비밀번호는 bcrypt로 해싱
- 환경변수: JWT_SECRET, REFRESH_SECRET

## 출력 형식
생성한 파일 경로 목록과 각 엔드포인트의 요청/응답 형식 요약.

## 팀 정보
- team_name: auth-team
- task_id: 2
- 완료 시 TaskUpdate(taskId: "2", status: "completed")
```

### Validator (검증자)

```
## 맥락
DB 마이그레이션의 모든 단계가 완료됨. DDL 적용 및 데이터 이전 완료.

선행 작업 결과:
- DDL: {schema_writer_result}
- 데이터 이전: {data_migrator_result}

## 목표
마이그레이션 무결성을 검증:
1. 레코드 수 비교 (원본 vs 이전)
2. FK 관계 무결성 확인
3. 누락 데이터 탐지
4. 인덱스 및 제약조건 확인

## 제약조건
- 읽기 전용 쿼리만 사용 (SELECT, COUNT)
- 데이터 수정 금지

## 출력 형식
검증 결과 테이블:
| 검증 항목 | 상태 | 상세 |
PASS/FAIL 표시와 실패 시 원인.

## 팀 정보
- team_name: migration-team
- task_id: 5
- 완료 시 TaskUpdate(taskId: "5", status: "completed")
```

## 프롬프트 작성 팁

- **구체적**: "코드 분석해줘" 대신 "src/lib/auth.ts의 인증 로직을 분석하고 보안 취약점을 식별"
- **제한된 범위**: 변경 가능한 파일/디렉토리를 명시적으로 지정
- **출력 형식 고정**: 자유 형식이 아닌 구조화된 형식 요구 (테이블, 체크리스트 등)
- **선행 결과 포함**: 의존 작업 시 이전 결과를 프롬프트 본문에 직접 삽입
