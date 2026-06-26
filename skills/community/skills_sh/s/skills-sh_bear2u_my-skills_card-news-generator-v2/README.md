# Card News Generator Skill

한국어 텍스트를 지원하는 소셜 미디어용 카드 뉴스 이미지 생성 스킬입니다.

## 특징

- ✅ **인터랙티브 모드**: 단계별 안내로 쉽게 카드 생성
- ✅ **RGB 색상 입력**: 사용자가 직접 RGB 값으로 색상 선택
- ✅ 한글 텍스트 완벽 지원
- ✅ 자동 중앙 정렬 및 레이아웃
- ✅ 숫자 배지 지원
- ✅ 다양한 이미지 크기

## 설치 방법

### 필요한 패키지 설치

```bash
pip install Pillow --break-system-packages
```

### 한글 폰트 설치 (Ubuntu/Debian)

```bash
sudo apt-get update
sudo apt-get install -y fonts-noto-cjk fonts-noto-cjk-extra
```

## 파일 구조

```
card-news-generator/
├── SKILL.md              # 스킬 메타데이터 및 사용 가이드
├── generate_card.py      # 카드 생성 스크립트
└── README.md            # 이 파일
```

## 사용 예시

### 방법 1: 인터랙티브 모드 (권장)

사용자가 단계별로 입력하는 방식:

```bash
python interactive_generator.py
```

프롬프트에 따라 다음을 입력:
1. 제목 (여러 줄 가능, 빈 줄로 종료)
2. 내용 (여러 줄 가능, 빈 줄로 종료)
3. 배경색 RGB (예: `245,243,238`)
4. 텍스트색 RGB (예: `26,26,26`)
5. 카드 번호 (선택사항)
6. 파일명

### 방법 2: 직접 명령어

모든 정보를 한 번에 제공:

```bash
python generate_card.py \
  --title "선생님·부모보다\n유튜브 등을 더 신뢰함" \
  --content "정보 접근이 빠르고,\n권위보다 '속도'를 더 신뢰함." \
  --number 1 \
  --bg-color "#f5f3ee" \
  --text-color "#1a1a1a" \
  --output /mnt/user-data/outputs/card_01.png
```

## 파라미터 설명

### 필수 파라미터
- `--title`: 카드의 메인 제목 (줄바꿈은 `\n` 사용)
- `--content`: 본문 내용 (줄바꿈은 `\n` 사용)
- `--output`: 저장할 파일 경로

### 선택 파라미터
- `--bg-color`: 배경색 (기본값: `#F5F3EE`)
- `--text-color`: 텍스트 색상 (기본값: `#1A1A1A`)
- `--width`: 이미지 너비 (기본값: 1080)
- `--height`: 이미지 높이 (기본값: 1920)
- `--title-size`: 제목 폰트 크기 (기본값: 120)
- `--content-size`: 본문 폰트 크기 (기본값: 60)
- `--number`: 숫자 배지 (선택사항)

## 추천 배경색 (RGB 형식)

| 색상 이름 | RGB 값 | Hex 코드 | 용도 |
|---------|---------|---------|-----|
| 따뜻한 베이지 | `245,243,238` | `#f5f3ee` | 기본, 모든 주제 |
| 소프트 핑크 | `255,229,229` | `#ffe5e5` | 부드러운 주제 |
| 민트 그린 | `224,244,241` | `#e0f4f1` | 자연, 건강 |
| 라벤더 | `232,224,245` | `#e8e0f5` | 감성, 힐링 |
| 피치 | `255,232,214` | `#ffe8d6` | 따뜻함, 활력 |
| 스카이 블루 | `227,242,253` | `#e3f2fd` | 전문성, 신뢰 |

**색상 입력 방법:**
- 인터랙티브 모드: RGB 값 직접 입력 (예: `245,243,238`)
- 직접 명령어: Hex 코드 사용 (예: `#f5f3ee`)

## 해결 방법

### 한글이 깨질 때
```bash
# 폰트 재설치
sudo apt-get install --reinstall fonts-noto-cjk
fc-cache -fv
```

### PIL 모듈 에러
```bash
pip install --upgrade Pillow --break-system-packages
```

### 파일 저장 실패
- 출력 경로가 존재하는지 확인
- 쓰기 권한이 있는지 확인
- 절대 경로 사용 권장

## 스킬 로드 방법

Claude Code에서 이 스킬을 사용하려면:

1. 스킬 디렉토리를 skills 폴더에 복사
2. Claude에게 요청: "card-news-generator 스킬을 사용해서 카드를 만들어줘"

## 라이선스

MIT License
