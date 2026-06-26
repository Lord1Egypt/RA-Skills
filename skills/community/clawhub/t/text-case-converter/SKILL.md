---
name: text-case-converter
version: 1.0.0
description: >-
  Convert text in a file to upper, lower, or title case. Use when the user
  wants to change the capitalization of text in a file.
allowed-tools: Bash(bash:*)
metadata: >-
  {"openclaw":{"emoji":"🔠","requires":{"bins":["tr","awk"],"env":[]},"install":[]}}
---

# Text Case Converter / 텍스트 대소문자 변환기

Convert text in a file to UPPER, lower, or Title case with a single command.
파일의 텍스트를 대문자, 소문자 또는 제목 형식으로 한 번의 명령으로 변환합니다.

## Usage / 사용법

```bash
bash run.sh <FILE_PATH> [CASE]
```

**Arguments / 인수:**
| # | Name | Description | 설명 |
|---|------|-------------|------|
| 1 | FILE_PATH | Path to the text file | 텍스트 파일의 경로 |
| 2 | CASE | `upper`, `lower`, or `title` (default: upper) | `upper`, `lower`, `title` (기본값: upper) |

## Example / 예시

```bash
bash run.sh /home/user/notes.txt lower
```

**Output / 출력:**
```
FILE: /home/user/notes.txt
CASE: lower
---
hello world this is a test
---
STATUS: OK
```

## Success / Failure — 성공 / 실패

- **Success / 성공**: Converted text followed by `STATUS: OK` (exit code 0) — 변환된 텍스트와 `STATUS: OK` 출력 (종료 코드 0)
- **Failure / 실패**: Error message starting with `ERROR:` (exit code non-zero) — `ERROR:`로 시작하는 오류 메시지 (종료 코드 0이 아님)
