# Changelog

## v5.1.2 (2026-03-28)
- OpenClaw 보안 스캔 Suspicious 지적 수정 (메타데이터 불완전)
- frontmatter에 `runtime` 및 `credentials` 필드 선언 추가
- 전제 조건에 자격증명 파일 경로 및 용도 명시
- `publish.sh`는 자격증명을 읽지 않음을 문서에 명시

## v5.1.1 (2026-03-28)
- 보안 스캔(VirusTotal/OpenClaw) 지적 수정
- `publish.sh`에서 자격증명 처리 코드 제거 → 세션 만료 시 에러 메시지 + `scripts/login.sh` 안내로 대체
- 로그인 기능을 `scripts/login.sh` 전용 스크립트로 분리

## v5.1.0 (2026-03-28)
- 카카오 로그인 세션 만료 시 자동 재로그인 기능 추가 (deprecated by v5.1.1)

## v5.0.3 (2026-03-27)
- OpenClaw security scan 지적 수정
- `banner.js`: `child_process.execSync` 제거
- `deep-dive.js`: 미사용 `child_process` import 제거

## v5.0.2 (2026-03-27)
- VirusTotal security scan 지적 수정
- `publish.sh`: Canvas Drop fallback 제거 (base64/atob 패턴), `subprocess` → `datetime` 교체
- `tistory-publish.js`: 레거시 함수에 LEGACY 주석 추가

## v5.0.0 (2026-03-27)
- **agent-browser → OpenClaw Playwright CDP 전환** (networkidle hang 해결)
- 단일 Python 스크립트 내장 (bash → Python heredoc)
- `--template` preset 지원 (mk-review, simple-post)
- `--article-title` 자동 날짜 접두사 생성
- `--cdp-port` 옵션 추가
- 배너: Playwright `set_input_files`로 업로드
- 빈 본문 방지: 발행 직전 `save()` + textarea 길이 검증
- 비공개 저장: 다이얼로그 닫힘 확인
- 레거시 삭제: `agent-browser-mk-publish.sh`, `tistory_post.py`, `tistory_post_cdp.py`

## v4.1.0 (2026-03-23)
- 본문 삽입 후 길이 검증 추가
- 발행 후 공개 페이지 재검증 추가

## v4.0.0 (2026-03-07)
- 범용 스킬로 재설계: 매경 리뷰 전용 → 어떤 포맷이든 발행 가능
- 범용 `publish.sh` 스크립트 추가
- 매경 리뷰를 `templates/mk-review/` 예시로 이동
- 단순 발행 예시 `templates/simple-post/` 추가

## v3.0.0 (2026-03-07)
- OpenClaw Playwright → agent-browser 전환
- 카테고리: JS eval → Playwright native ARIA combobox click
- 배너: base64 chunk → agent-browser upload
