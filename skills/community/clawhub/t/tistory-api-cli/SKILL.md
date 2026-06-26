---
name: Tistory API CLI
slug: tistory-api-cli
displayName: Tistory API CLI
version: 0.1.1
summary: Tistory 블로그용 비공식 CLI. 글 읽기/수정/삭제, 카테고리 조회, 이미지 첨부 업로드를 지원하며 요청/응답 스키마 검증과 한국어 에러 메시지를 제공한다.
tags: [latest, tistory, blog, cli]
license: MIT
metadata:
  openclaw:
    requires:
      env: []
    primaryEnv: ""
---

# Tistory API CLI

Tistory 블로그를 터미널에서 제어하기 위한 경량 CLI이다. 글 읽기/수정/삭제와 카테고리 조회, 이미지 첨부 POST를 지원한다. 요청/응답 스키마를 검증하고, 에러 메시지를 한국어로 안내한다. Python 런타임이 없는 환경을 고려해 uv/pipx 기반 설치 가이드를 제공하며, pytest 단위 테스트와 GitHub Actions CI를 포함한다. PyPI 배포(tistory-api-cli)를 고려해 pip 설치 경로를 제공한다.

## 무엇이 새로운가 — v0.1.1

- SKILL.md 메타데이터 반영 및 태그(latest) 유지
- 기능 보강
  - 읽기(read-post), 수정(update), 삭제(delete), 카테고리 조회 추가
  - 파일 첨부(이미지) POST 지원
  - 요청/응답 스키마 검증 및 에러 메시지 국문화
- 안정성/품질
  - Python 런타임 미존재 환경 고려한 설치 가이드(uv/pipx) README 보강
  - pytest 기반 단위 테스트(가짜 응답 fixture) 및 GitHub Actions CI 추가
  - PyPI 배포(tistory-api-cli) 고려해 pip 설치 경로 제공
- 확장 계획
  - Velog용 별도 스킬(velog-cli) 리서치/스펙 작성(블로그/시리즈 CRUD, 태그/검색)
  - 한·영 혼용 문서와 예시 강화로 해외 사용자 접근성 개선

## 설치

- pipx
  - pipx install tistory-api-cli
- uv
  - uv tool install tistory-api-cli
- pip (권장도 낮음)
  - pip install tistory-api-cli

## 사용 예시

- 글 조회: tistory-cli read --post-id 12345
- 글 수정: tistory-cli update --post-id 12345 --title "제목" --content @body.md
- 글 삭제: tistory-cli delete --post-id 12345
- 카테고리 조회: tistory-cli categories
- 이미지 업로드: tistory-cli upload-image ./image.png

## 환경 변수(필요 시)

- TISTORY_ACCESS_TOKEN: Tistory API 토큰
- TISTORY_BLOG_NAME: 기본 블로그 식별자

## 링크

- GitHub: 제공 예정

## 라이선스

MIT-0
