# File Backup / 파일 백업

## What it does / 기능

Creates a timestamped backup copy of a file, so you can safely make changes to the original.

파일의 타임스탬프 백업 복사본을 만들어, 원본을 안전하게 수정할 수 있게 합니다.

## How to use / 사용법

```bash
bash run.sh <FILE_PATH> [BACKUP_DIR]
```

| Argument | Required | Description |
|----------|----------|-------------|
| FILE_PATH | Yes / 필수 | File to back up / 백업할 파일 |
| BACKUP_DIR | No / 선택 | Where to save backup (default: same directory) / 백업 저장 위치 (기본: 같은 디렉토리) |

## Example / 예시

```bash
bash run.sh /home/user/config.yaml
```

Output / 출력:
```
OK: Backup created at /home/user/config.yaml.backup_20260328_143022
```

The backup filename format is: `ORIGINAL.backup_YYYYMMDD_HHMMSS`

백업 파일명 형식: `원본파일명.backup_년월일_시분초`

## Troubleshooting / 문제 해결

- **"File not found"** — Check the file path / 파일 경로를 확인하세요
- **"Backup directory not found"** — The target directory must exist / 대상 디렉토리가 존재해야 합니다
