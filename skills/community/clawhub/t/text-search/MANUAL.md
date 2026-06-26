# Text Search / 텍스트 검색

## What it does / 기능

Searches for a word or phrase in all files within a directory, showing matching lines with file names and line numbers.

디렉토리 내 모든 파일에서 단어나 문구를 검색하여, 파일명과 줄 번호와 함께 일치하는 줄을 보여줍니다.

## How to use / 사용법

```bash
bash run.sh <PATTERN> [DIRECTORY]
```

| Argument | Required | Description |
|----------|----------|-------------|
| PATTERN | Yes / 필수 | Text to search for / 검색할 텍스트 |
| DIRECTORY | No / 선택 | Where to search (default: current dir) / 검색 위치 (기본: 현재 디렉토리) |

## Example / 예시

```bash
bash run.sh "TODO" /home/user/project
```

Output / 출력:
```
Searching for 'TODO' in /home/user/project:
---
/home/user/project/main.py:12:# TODO: fix this
/home/user/project/utils.py:5:# TODO: add tests
```

Format / 형식: `FILENAME:LINE_NUMBER:MATCHING_LINE` (`파일명:줄번호:일치하는줄`)

## Troubleshooting / 문제 해결

- **"No matches found"** — The pattern was not found, this is normal / 패턴이 없으면 정상입니다
- **"Directory not found"** — Check the path / 경로를 확인하세요
- Search is case-sensitive / 대소문자를 구분합니다
