# SprintX OpenClaw Handoff

SprintX의 첫 공개 ClawHub skill 저장소입니다.

이 스킬은 기존 OpenClaw 사용자가 SprintX와 연결할 때, 지금 기준으로 가장 안전하고 짧은 handoff proof packet만 안내합니다.

```text
sx auth
-> sx project use
-> sx event
-> sx artifact add
-> sx status
-> sx brief
```

의도적으로 범위를 좁게 유지합니다.

- custom MCP server 없음
- 숨겨진 SprintX 자동화 없음
- 범용 자연어 control plane 아님
- 프로젝트 생성 flow 내장 안 함

링크:
- ClawHub: https://clawhub.ai/terry3838/sprintx-openclaw-handoff
- GitHub: https://github.com/terry3838/SprintX-SKILL
- SprintX handoff quickstart: https://www.sprintx.co.kr/docs/getting-started/openclaw-handoff-quickstart
- SprintX CLI quickstart (ko): https://www.sprintx.co.kr/docs/getting-started/cli-quickstart.ko

## 왜 필요한가

OpenClaw 사용자는 이미 SprintX CLI로 연결할 수 있습니다.

문제는 첫 연결 마찰입니다.

- 어떤 명령부터 쳐야 하는지
- `projectId`를 어디서 가져와야 하는지
- 성공 신호가 뭔지
- 중간에 실패하면 무엇을 해야 하는지

이 스킬은 그걸 하나의 operator flow로 압축합니다.

마법을 늘리는 게 아니라, 혼란을 줄입니다.

## 이 스킬이 하는 일

1. SprintX 사전 조건 확인
2. `sx`가 이미 있는지 먼저 확인
3. handoff card / handoff URL을 기본 `projectId` source로 사용
4. 필요할 때만 `sx project list`로 복구
5. proof packet을 올바른 순서로 실행
6. `sx status`, `sx brief`로 성공 확인
7. 실패 시 명시적인 rescue guidance 제공

## 이런 사람에게 맞다

다음 조건이면 잘 맞습니다.

- 이미 OpenClaw를 쓴다
- 이미 SprintX 계정이 있다
- SprintX 프로젝트가 있다
- 넓은 통합 surface가 아니라 가장 안전한 현재 handoff 경로가 필요하다

다음 목적에는 맞지 않습니다.

- chat에서 SprintX 프로젝트 생성
- skill 자체에서 task CRUD
- review / approval workflow
- remote MCP server 기반 연동

## 빠른 시작

### 1. skill 설치

```bash
clawhub install sprintx-openclaw-handoff
```

비대화형 환경에서 이미 검토를 끝냈다면:

```bash
clawhub install sprintx-openclaw-handoff --force --no-input
```

### 2. skill 호출

예시 프롬프트:

```text
Use $sprintx-openclaw-handoff to connect my existing OpenClaw runtime to SprintX.
```

### 3. proof packet 실행

```bash
sx auth
sx project use <project-id>
sx event --type runtime.started --summary "OpenClaw handoff started"
sx artifact add --title "first-log" --reference-uri "file:///tmp/openclaw.log" --content-type "text/plain" --summary "Initial OpenClaw evidence"
sx status
sx brief
```

## 전제 조건

시작 전에 다음이 있어야 합니다.

- SprintX 웹 로그인 세션
- SprintX 프로젝트
- `/dashboard?handoff=1&projectId=<id>` 또는 handoff card 접근

`projectId`가 이미 보이면 그 값을 바로 씁니다.

`sx project list`는 기본 단계가 아니라 복구 경로입니다.

## 신뢰 경계

- SprintX는 executor가 아닙니다. OpenClaw가 실행하고, SprintX는 읽고 거버넌스를 제공합니다.
- 기본 auth 경로는 browser-approved `sx auth`입니다.
- access-token override는 advanced 또는 break-glass 용도입니다.
- 이 스킬은 토큰을 채팅에 붙여 넣지 말라고 명시합니다.
- provider API key는 이 flow 밖입니다.

## Advanced Operators

headless/CI 환경도 지원하지만 기본 경로는 아닙니다.

```bash
sx --headless auth
```

access-token override도 문서화하지만, 일부러 메인 onboarding path 밖에 둡니다.

## 저장소 구조

```text
SprintX-SKILL/
├── SKILL.md
├── README.md
├── README.ko.md
├── README.zh.md
├── CHANGELOG.md
├── LICENSE
├── LICENSE.md
├── package.json
├── references/
│   └── source-of-truth.md
├── scripts/
│   ├── check-skill.mjs
│   └── check-contract.mjs
└── .github/workflows/ci.yml
```

설계 원칙:

- `SKILL.md`만 operator truth
- `README*`는 사람이 읽는 문서
- `references/`는 upstream source-of-truth 링크
- CI는 검증만 하고 publish는 수동

## 검증

```bash
npm run check
```

이 검증은 다음을 확인합니다.

- frontmatter shape
- 실제 필요한 runtime requirement
- install metadata
- license 존재
- command order
- recovery-only `sx project list`
- advanced-only token guidance

## 배포

```bash
clawhub publish . \
  --slug sprintx-openclaw-handoff \
  --name "SprintX OpenClaw Handoff" \
  --version 0.1.3 \
  --tags latest \
  --changelog "Add localized READMEs and tighten metadata to match real requirements"
```

현재는 수동 publish를 유지합니다.

이유는 ClawHub에서 skill publish는 CLI 경로가 가장 분명하고, plugin/package auto-publish 쪽이 더 성숙했기 때문입니다.
