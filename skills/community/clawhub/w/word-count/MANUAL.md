# Word Count — User Manual

## English

### What does this skill do?
This skill counts the number of **lines**, **words**, and **bytes** (characters) in a text file. It's useful when you want to know how long a document is.

### How to use it
Run this command, replacing `<FILE>` with the path to your file:

```bash
bash run.sh <FILE>
```

**Example:**
```bash
bash run.sh /home/user/my-essay.txt
```

**What you'll see:**
```
FILE: /home/user/my-essay.txt
LINES: 42
WORDS: 350
BYTES: 2100
STATUS: OK
```

### Arguments
| Argument | Required? | What it means |
|----------|-----------|---------------|
| FILE | Yes | The file you want to count |

### How to tell if it worked
- **Success**: You see `STATUS: OK` with the counts
- **Failure**: You see `ERROR:` followed by what went wrong

### Requirements
- Linux with `wc` command (available on virtually all systems)

---

## 한국어 (Korean)

### 이 스킬은 무엇을 하나요?
텍스트 파일의 **줄 수**, **단어 수**, **바이트 수**(문자 수)를 셉니다. 문서의 길이를 알고 싶을 때 유용합니다.

### 사용 방법
아래 명령어에서 `<파일>`을 파일 경로로 바꿔서 실행하세요:

```bash
bash run.sh <파일>
```

**예시:**
```bash
bash run.sh /home/user/my-essay.txt
```

**출력 결과:**
```
FILE: /home/user/my-essay.txt
LINES: 42
WORDS: 350
BYTES: 2100
STATUS: OK
```

### 인수 설명
| 인수 | 필수 여부 | 설명 |
|------|-----------|------|
| 파일 | 예 | 셀 파일의 경로 |

### 성공/실패 확인 방법
- **성공**: `STATUS: OK`와 함께 숫자가 표시됩니다
- **실패**: `ERROR:`와 함께 오류 내용이 표시됩니다

### 요구 사항
- `wc` 명령어가 있는 Linux 시스템 (거의 모든 시스템에 기본 설치됨)
