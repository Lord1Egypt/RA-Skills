# File Tree / 파일 트리

## What it does / 기능

Shows the directory structure of a folder as an indented list, so you can see what files and subdirectories are inside.

폴더의 디렉토리 구조를 들여쓰기 목록으로 보여주어, 내부의 파일과 하위 디렉토리를 확인할 수 있습니다.

## How to use / 사용법

```bash
bash run.sh [DIRECTORY] [DEPTH]
```

| Argument | Required | Description |
|----------|----------|-------------|
| DIRECTORY | No / 선택 | Folder to display (default: current dir) / 표시할 폴더 (기본: 현재 디렉토리) |
| DEPTH | No / 선택 | How many levels deep (default: 3) / 표시할 깊이 (기본: 3) |

## Example / 예시

```bash
bash run.sh /home/user/project 2
```

Output / 출력:
```
  project
    src
      main.py
      utils.py
    README.md
```

## Troubleshooting / 문제 해결

- **"Directory not found"** — Check the path / 경로를 확인하세요
- **"DEPTH must be a positive integer"** — Use a number like 1, 2, 3 / 1, 2, 3 같은 숫자를 사용하세요
- For large directories, use a smaller depth / 큰 디렉토리는 작은 깊이를 사용하세요
