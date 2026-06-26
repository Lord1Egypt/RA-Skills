---
name: github-actions
description: "GitHub Actions 워크플로우 생성, 보안 및 버전 관리 스킬. 다음 상황에서 사용: (1) 새 워크플로우 파일(.yml) 작성 시, (2) 기존 워크플로우 수정 시, (3) 액션 버전 검토 또는 업데이트 시, (4) CI/CD 보안 감사 시, (5) 'actions/', 'uses:', 'workflow', '.github/workflows' 키워드가 포함된 작업 시"
license: MIT
metadata:
  author: DaleStudy
  version: "2.0.0"
allowed-tools: Bash(gh release:*)
---

# GitHub Actions

> **참고:** GitHub Actions 워크플로우 실행 및 결과 조회, 이슈/PR 관리 등 `gh` CLI 관련 작업은 `github` 스킬을 함께 로드하여 참조한다.

## 주의 사항 (Anti-patterns)

### 1. 오래된 버전 사용

```yaml
# ❌ 오래된 버전 - 가장 흔한 실수
uses: actions/checkout@v4 # v6가 최신인 경우

# ✅ 최신 메이저 버전 (gh release view로 확인 후 사용)
uses: actions/checkout@v6
```

최신 버전에서 제공하는 성능 개선과 보안 패치를 놓치지 않도록 합니다.

**버전 확인 명령어:**

```bash
gh release view --repo {owner}/{repo} --json tagName --jq '.tagName'

# 예시
gh release view --repo actions/checkout --json tagName --jq '.tagName'
gh release view --repo oven-sh/setup-bun --json tagName --jq '.tagName'
```

> 참고: 보안 민감 환경이나 신뢰도 낮은 서드파티 액션은 [SHA 피닝](https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions#using-third-party-actions)(`@a1b2c3...`)을 고려.

### 2. 민감정보 하드코딩

```yaml
# ❌ 하드코딩 - 보안 위험
env:
  API_KEY: "sk-1234567890"
  DATABASE_PASSWORD: "mypassword123"
# ✅ secrets 사용
env:
  API_KEY: ${{ secrets.API_KEY }}
  DATABASE_PASSWORD: ${{ secrets.DATABASE_PASSWORD }}
```

비밀번호나 API Key와 같은 민감 정보가 그대로 노출되어 보안 사고로 이어질 수 있습니다.
보안 상 중요한 정보는 반드시 저장소나 조직의 시크릿으로 저장해놓고 읽어 와야합니다.

> 참고: [Using secrets](https://docs.github.com/en/actions/security-guides/using-secrets-in-github-actions)

### 3. 입력값 인젝션 취약점

```yaml
# ❌ 인젝션 취약 - github.event 직접 사용
run: echo "${{ github.event.issue.title }}"
run: gh issue comment ${{ github.event.issue.number }} --body "${{ github.event.comment.body }}"
# ✅ 환경변수로 전달하여 인젝션 방지
env:
  ISSUE_TITLE: ${{ github.event.issue.title }}
  COMMENT_BODY: ${{ github.event.comment.body }}
run: |
  echo "$ISSUE_TITLE"
  gh issue comment ${{ github.event.issue.number }} --body "$COMMENT_BODY"
```

악의적인 사용자가 이슈 제목이나 코멘트에 셸 명령어를 주입할 수 있습니다.

> 참고: [Script injections](https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions#understanding-the-risk-of-script-injections)

### 4. pull_request_target 이벤트 오용

```yaml
# ⚠️ 위험 - 포크의 코드를 신뢰된 컨텍스트에서 실행
on: pull_request_target
steps:
  - uses: actions/checkout@v{N}
    with:
      ref: ${{ github.event.pull_request.head.sha }} # 위험!
```

`pull_request_target` 이벤트는 포크의 PR에서도 시크릿에 접근 가능합니다. 포크 코드를 체크아웃하면 악성 코드가 실행될 수 있습니다.

> 참고: [pull_request_target](https://docs.github.com/en/actions/writing-workflows/choosing-when-your-workflow-runs/events-that-trigger-workflows#pull_request_target)

### 5. 사전 설치된 도구에 중복 설정

```yaml
# ❌ 불필요한 setup - node, npm, npx는 이미 설치됨
steps:
  - uses: actions/setup-node@v{N}
  - run: npx some-command
# ✅ 바로 사용
steps:
  - run: npx some-command
  - run: python script.py
  - run: docker build .
```

중복 설치는 워크플로우 실행 시간을 늘리고 불필요한 네트워크 요청을 발생시킵니다.

**주요 사전 설치 도구:** Node.js, npm, npx, Python, pip, Ruby, gem, Go, Docker, git, gh, curl, wget, jq, yq

**주요 미설치 도구:** Bun, Deno, Rust, Zig, pnpm, Poetry, Ruff

**사전 설치된 도구 확인:**

- Ubuntu: https://github.com/actions/runner-images/blob/main/images/ubuntu/Ubuntu2404-Readme.md
- macOS: https://github.com/actions/runner-images/blob/main/images/macos/macos-15-Readme.md
- Windows: https://github.com/actions/runner-images/blob/main/images/windows/Windows2022-Readme.md

## 모범 사례 (Best Practices)

### 최소 권한 원칙

권한은 가능한 하위 레벨에 선언. 범위를 좁게 유지:

```yaml
# ✅ 권한 범위: workflow > job > step (좁을수록 좋음)
jobs:
  build:
    permissions:
      contents: read # job 레벨에서 필요한 권한만
```

> 참고: [Modifying the permissions for the GITHUB_TOKEN](https://docs.github.com/en/actions/security-guides/automatic-token-authentication#modifying-the-permissions-for-the-github_token)

## 권장 워크플로우 구조

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      contents: read

    steps:
      # 버전은 gh release view로 확인 후 사용
      - uses: actions/checkout@v{N}

      - name: Setup Bun
        uses: oven-sh/setup-bun@v{N}
```

## 자주 사용되는 이벤트

```yaml
on:
  push: # 푸시 시
    branches: [main]
  pull_request: # PR 생성/업데이트 시
    branches: [main]
  workflow_dispatch: # 수동 실행
  schedule: # 스케줄 실행
    - cron: "0 0 * * 1" # 매주 월요일 00:00 UTC
  release: # 릴리스 생성 시
    types: [published]
  workflow_call: # 다른 워크플로우에서 호출
```

## 자주 사용되는 권한

```yaml
permissions:
  contents: read        # CI (빌드/테스트), 코드 체크아웃
  contents: write       # 커밋/푸시
  pull-requests: write  # PR 코멘트 봇
  issues: write         # 이슈 코멘트
  packages: write       # 패키지 배포 (contents: write와 함께)
  id-token: write       # OIDC 클라우드 인증 (contents: read와 함께)
```

## 자주 사용되는 액션

```yaml
# 버전은 gh release view --repo {owner}/{repo} --json tagName --jq '.tagName'으로 확인
steps:
  - uses: actions/cache@v{N} # 의존성 캐싱
  - uses: actions/checkout@v{N} # 코드 체크아웃
  - uses: actions/download-artifact@v{N} # 아티팩트 다운로드
  - uses: actions/upload-artifact@v{N} # 아티팩트 업로드
  - uses: oven-sh/setup-bun@v{N} # Bun 설정
```
