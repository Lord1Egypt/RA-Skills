# Text Case Converter — User Manual

## English

### What does this skill do?
This skill changes the capitalization of all text in a file. You can convert text to:
- **UPPER CASE** — all capital letters
- **lower case** — all small letters
- **Title Case** — first letter of each word capitalized

It's useful when you need to standardize text formatting or change how text appears.

### How to use it
Run this command with the file path and the desired case:

```bash
bash run.sh <FILE> [CASE]
```

If you don't specify a case, it defaults to `upper`.

**Example:**
```bash
bash run.sh /home/user/notes.txt lower
```

**What you'll see:**
```
FILE: /home/user/notes.txt
CASE: lower
---
hello world this is a test
---
STATUS: OK
```

### Arguments
| Argument | Required? | What it means |
|----------|-----------|---------------|
| FILE | Yes | The text file to convert |
| CASE | No | `upper`, `lower`, or `title` (default: `upper`) |

### Case options explained
| Option | Input | Output |
|--------|-------|--------|
| `upper` | hello world | HELLO WORLD |
| `lower` | Hello World | hello world |
| `title` | hello world | Hello World |

### How to tell if it worked
- **Success**: Converted text followed by `STATUS: OK`
- **Failure**: You see `ERROR:` followed by what went wrong

### Important note
This skill displays the converted text but does **not** modify the original file. Your original file stays unchanged.

### Requirements
- Linux with `tr` and `awk` commands (standard on all systems)

---

## 한국어 (Korean)

### 이 스킬은 무엇을 하나요?
파일의 모든 텍스트의 대소문자를 변환합니다. 다음과 같이 변환할 수 있습니다:
- **UPPER CASE (대문자)** — 모든 글자를 대문자로
- **lower case (소문자)** — 모든 글자를 소문자로
- **Title Case (제목 형식)** — 각 단어의 첫 글자를 대문자로

텍스트 서식을 통일하거나 표시 방식을 바꿀 때 유용합니다.

### 사용 방법
파일 경로와 원하는 형식으로 아래 명령어를 실행하세요:

```bash
bash run.sh <파일> [형식]
```

형식을 지정하지 않으면 기본값은 `upper`(대문자)입니다.

**예시:**
```bash
bash run.sh /home/user/notes.txt lower
```

**출력 결과:**
```
FILE: /home/user/notes.txt
CASE: lower
---
hello world this is a test
---
STATUS: OK
```

### 인수 설명
| 인수 | 필수 여부 | 설명 |
|------|-----------|------|
| 파일 | 예 | 변환할 텍스트 파일 |
| 형식 | 아니오 | `upper`, `lower`, `title` 중 하나 (기본값: `upper`) |

### 형식 옵션 설명
| 옵션 | 입력 | 출력 |
|------|------|------|
| `upper` | hello world | HELLO WORLD |
| `lower` | Hello World | hello world |
| `title` | hello world | Hello World |

### 성공/실패 확인 방법
- **성공**: 변환된 텍스트와 `STATUS: OK`가 표시됩니다
- **실패**: `ERROR:`와 함께 오류 내용이 표시됩니다

### 중요 사항
이 스킬은 변환된 텍스트를 화면에 표시할 뿐 원본 파일을 **수정하지 않습니다**. 원본 파일은 그대로 유지됩니다.

### 요구 사항
- `tr`와 `awk` 명령어가 있는 Linux 시스템 (모든 시스템에 기본 설치됨)
