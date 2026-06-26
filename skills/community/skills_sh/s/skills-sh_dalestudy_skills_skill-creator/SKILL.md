---
name: skill-creator
description: "DaleStudy/skills 저장소의 스킬 생성, 수정, 검증 시 사용. 다음 상황에서 활성화: (1) 새 스킬 생성 요청 시, (2) skills/ 디렉토리 내 SKILL.md 파일 수정 시, (3) SKILL.md 변경 검토 또는 리뷰 시, (4) 스킬 frontmatter 또는 메타데이터 작업 시, (5) 'skill', 'SKILL.md', 'frontmatter', 'version', 'metadata', 'review', 'skills/' 키워드가 포함된 작업 시"
license: MIT
compatibility: Git repository with skills/ directory
metadata:
  author: DaleStudy
  version: "1.1.0"
---

# Skill Creator for DaleStudy

DaleStudy/skills 저장소에 새로운 스킬을 추가하기 위한 가이드.

## 스킬 구조

```
skills/{skill-name}/
└── SKILL.md          # YAML frontmatter + Markdown 지시사항 (필수)
```

## SKILL.md 형식

```yaml
---
name: skill-name # 필수: 디렉토리명과 일치 (최대 64자, 소문자/숫자/하이픈)
description: "스킬 설명" # 필수: 트리거 조건 포함 (최대 1024자)
license: MIT # 선택
compatibility: Required CLI tools # 선택: 필요한 도구
metadata: # 선택
  author: DaleStudy
  version: "1.0.0"
allowed-tools: Bash(command:*) # 선택: 허용할 도구 패턴
---
# 스킬 제목

스킬 지시사항 (Markdown)
```

## 스킬 생성 절차

### 1. 디렉토리 생성

```bash
mkdir -p skills/{skill-name}
```

### 2. SKILL.md 작성

#### Frontmatter 작성 규칙

**name 필드:**

- 디렉토리명과 동일해야 함
- 소문자, 숫자, 하이픈만 사용
- 연속된 하이픈 불가 (`my--skill` ❌)
- 최대 64자

**description 필드 (가장 중요):**

- 스킬의 목적과 **트리거 조건**을 명확히 기술
- Body는 트리거 후에만 로드되므로, "언제 사용"은 반드시 description에 포함
- 패턴: `"{스킬 설명}. 다음 상황에서 사용: (1) ..., (2) ..., (3) ..."`

```yaml
# ✅ 좋은 예
description: "Node.js 대신 Bun 런타임 사용을 위한 스킬. 다음 상황에서 사용: (1) 새 JavaScript/TypeScript 프로젝트 생성 시, (2) package.json 또는 의존성 관련 작업 시"

# ❌ 나쁜 예
description: "Bun 관련 스킬"  # 트리거 조건 없음
```

#### Body 작성 규칙

- 간결하게 유지 (500줄 이하 권장)
- Claude가 이미 아는 내용은 생략
- 예제 코드 > 장황한 설명
- 명령형/부정사 형태 사용

### 3. README.md 업데이트

저장소 루트의 README.md에 새 스킬 추가:

```markdown
## Current Skills

- **bun**: Node.js 대신 Bun 런타임 사용
- **github-actions**: GitHub Actions 워크플로우 작성 및 보안
- **{new-skill}**: {간단한 설명} <!-- 추가 -->
```

### 4. 워크플로우 매트릭스 업데이트

`.github/workflows/ci.yml`의 matrix에 새 스킬 추가:

```yaml
matrix:
  skill:
    - bun
    - github-actions
    - { new-skill } # 추가
```

## 기존 스킬 참고

| 스킬             | 특징                                          |
| ---------------- | --------------------------------------------- |
| `bun`            | 명령어 매핑 테이블, 코드 예제 중심            |
| `github-actions` | 보안 모범 사례, YAML 예제 중심                |
| `skill-creator`  | 메타 스킬, 구조화된 절차, frontmatter 가이드  |
| `storybook`      | CSF 3.0 베스트 프랙티스, TypeScript 타입 예제 |

새 스킬 작성 시 기존 스킬의 스타일을 참고하여 일관성 유지.

## 버전 관리

Semantic Versioning (MAJOR.MINOR.PATCH)을 따라 스킬 수정 시 버전 업데이트:

### MAJOR 버전 (x.0.0)

**호환성이 깨지는 변경** - 기존 사용자에게 영향:

- Frontmatter 필수 필드 추가/변경
- `allowed-tools` 권한 축소
- 스킬 트리거 조건 대폭 변경 (description 수정)
- 기존 지시사항과 상충되는 새 규칙 도입

```yaml
# 예: 1.2.3 → 2.0.0
metadata:
  version: "2.0.0"
```

### MINOR 버전 (0.x.0)

**새 기능 추가** - 하위 호환 유지:

- 새로운 예제 코드 추가
- 지시사항 섹션 추가 (기존과 충돌 없음)
- `allowed-tools` 권한 확대
- 트리거 조건 확장 (기존 조건 유지)

```yaml
# 예: 1.2.3 → 1.3.0
metadata:
  version: "1.3.0"
```

### PATCH 버전 (0.0.x)

**버그 수정 및 사소한 개선**:

- 오타 수정
- 설명 명확화 (의미 변경 없음)
- 코드 예제 포맷 정리
- 링크 업데이트

```yaml
# 예: 1.2.3 → 1.2.4
metadata:
  version: "1.2.4"
```

### 버전 업데이트 체크리스트

**CRITICAL: 스킬 SKILL.md 파일을 수정할 때마다 반드시 버전을 업데이트하세요.**

스킬 수정 후:

1. [ ] 변경 내용이 MAJOR/MINOR/PATCH 중 어디에 해당하는지 판단
2. [ ] `metadata.version` 필드 업데이트 (필수)
3. [ ] (선택) CHANGELOG.md 작성 (주요 변경 시)

**버전 미업데이트는 스킬 검증 실패로 간주됩니다.**

## 스킬 변경 시 자동 검증

**IMPORTANT: SKILL.md 파일을 수정할 때, 반드시 다음을 확인하세요:**

### 1. 버전 업데이트 검증

SKILL.md 파일이 수정되었다면 `metadata.version`도 함께 업데이트되어야 합니다:

```bash
# 변경된 SKILL.md 확인
git diff --name-only HEAD | grep "skills/.*/SKILL.md"

# 또는 커밋 전 staged 파일 확인
git diff --cached --name-only | grep "skills/.*/SKILL.md"

# metadata.version 필드가 변경되었는지 확인
git diff HEAD -- skills/{skill-name}/SKILL.md | grep "^\+.*version:"
git diff --cached -- skills/{skill-name}/SKILL.md | grep "^\+.*version:"

# 변경되지 않았다면:
# ❌ ERROR: skills/{skill-name}/SKILL.md was modified but metadata.version was not updated
# Required: Update version according to Semantic Versioning (see 버전 관리 section above)
```

### 2. 버전 증가 방향 검증

변경된 내용이 올바른 버전 증가를 따르는지 확인:

- **MAJOR 변경인데 MINOR/PATCH 증가**: ❌ 에러
- **MINOR 변경인데 PATCH 증가**: ⚠️ 경고
- **PATCH 변경인데 MINOR/MAJOR 증가**: ✅ 허용 (보수적 증가는 안전)

### 3. Frontmatter 유효성 검증

- `name` 필드가 디렉토리명과 일치하는가?
- `description` 필드가 트리거 조건을 포함하는가? ("다음 상황에서 사용:" 패턴)
- `metadata.version` 형식이 "X.Y.Z" (Semantic Versioning)인가?

## 수동 검증

스킬 설치 테스트:

```bash
npx skills add DaleStudy/skills --skill {skill-name} --agent claude-code --global --yes
```
