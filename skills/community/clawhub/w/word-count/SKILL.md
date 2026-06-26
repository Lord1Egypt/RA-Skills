---
name: word-count
version: 1.0.0
description: >-
  Count words, lines, and characters in a file. Outputs a single summary line.
  Use when the user wants to know how long a file is or count words in a document.
allowed-tools: Bash(wc:*)
metadata: >-
  {"openclaw":{"emoji":"🔢","requires":{"bins":["wc"],"env":[]},"install":[]}}
---

# Word Count / 단어 수 세기

Count words, lines, and characters in any text file with a single command.
텍스트 파일의 단어, 줄, 문자 수를 한 번의 명령으로 셉니다.

## Usage / 사용법

```bash
wc <FILE_PATH>
```

**Arguments / 인수:**
| # | Name | Description | 설명 |
|---|------|-------------|------|
| 1 | FILE_PATH | Path to the file to count | 셀 파일의 경로 |

## Example / 예시

```bash
wc /home/user/document.txt
```

**Output / 출력:**
```
  42  350 2100 /home/user/document.txt
```

Format / 형식: `LINES  WORDS  CHARACTERS  FILENAME`
(`줄 수  단어 수  문자 수  파일명`)

## Success / Failure — 성공 / 실패

- **Success / 성공**: Output line with 3 numbers and filename (exit code 0) — 숫자 3개와 파일명이 포함된 출력 (종료 코드 0)
- **Failure / 실패**: Error message from `wc` (exit code non-zero) — `wc` 오류 메시지 (종료 코드 0이 아님)
