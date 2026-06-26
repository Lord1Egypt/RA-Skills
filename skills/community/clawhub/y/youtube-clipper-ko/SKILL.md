---
name: youtube-clipper-ko
description: >
  한국어 YouTube 영상을 바이럴 클립으로 자동 분할하는 스킬.
  Whisper로 음성 분석 → Claude로 바이럴 구간 선정 → ffmpeg으로 클립 추출.
  무음/숨소리 구간 제거, 3색 한국어 자막(SUIT 폰트), 바이럴 점수 + 리즌 텍스트 포함.
  YouTube URL 또는 로컬 파일 입력 지원. Clawitzer 파이프라인 연결 가능.
triggers:
  - youtube 클립
  - 영상 클리핑
  - 바이럴 구간 추출
  - 쇼츠 변환
  - 롱폼 쇼츠
---

# YouTube Clipper KO

한국어 YouTube 영상 → 바이럴 숏폼 클립 자동 분할기.

## 개요

1. YouTube URL 또는 로컬 영상 파일 입력
2. yt-dlp로 영상 다운로드
3. Whisper API로 전체 자막 + word-level 타임스탬프 추출
4. Claude Haiku로 바이럴 구간 8~12개 선정 + 점수 + 한국어 리즌
5. ffmpeg으로 각 구간 9:16 클립 추출
6. 무음/숨소리 압축 (max_gap_sec=0.06)
7. 3색 한국어 자막 burn-in (SUIT ExtraBold)
8. 결과 폴더에 클립 + 메타데이터 JSON 저장

## 필수 도구 확인

에이전트는 작업 시작 전 반드시 환경을 확인해야 한다:

```bash
# yt-dlp
yt-dlp --version

# ffmpeg (libass 포함 여부 확인)
ffmpeg -filters 2>&1 | grep subtitles

# python 의존성
python3 -c "import openai, anthropic; print('OK')"

# SUIT 폰트
ls /usr/share/fonts/truetype/SUIT-ExtraBold.ttf 2>/dev/null || echo "MISSING"
```

없으면:
- yt-dlp: `pip install yt-dlp`
- ffmpeg: `apt install ffmpeg` 또는 `brew install ffmpeg`
- 의존성: `pip install openai anthropic`
- SUIT 폰트 없으면 NotoSansCJK-Bold.ttc fallback 자동 적용

## 사용법

에이전트는 사용자에게 다음을 물어야 한다:

1. YouTube URL 또는 로컬 영상 경로
2. 구간 설정 (선택, 기본: 전체)
3. 클립 길이 (선택: 15~30초 / 30~60초 / 60~90초 / 90~120초, 기본: 30~60초)
4. 자막 언어 (선택: 한국어 / 영어, 기본: 한국어)

받은 후 scripts/clip.py 실행:

```bash
python3 skills/youtube-clipper-ko/scripts/clip.py \
  --url "https://youtu.be/VIDEO_ID" \
  --clip-length 60 \
  --lang ko
```

또는 로컬 파일:

```bash
python3 skills/youtube-clipper-ko/scripts/clip.py \
  --file "/path/to/video.mp4" \
  --clip-length 60
```

## 출력 구조

```
outputs/YYYYMMDD_HHMMSS/
├── source.mp4           # 원본 (URL 입력 시 다운로드)
├── transcript.json      # Whisper 전체 자막 + 타임스탬프
├── viral_segments.json  # 바이럴 구간 분석 결과
├── clips/
│   ├── clip_01_[제목].mp4
│   ├── clip_02_[제목].mp4
│   └── ...
└── result.json          # 전체 메타데이터
```

## viral_segments.json 구조

```json
[
  {
    "rank": 1,
    "score": 87,
    "start": "03:14",
    "end": "04:02",
    "title": "월 200만원 자동화하는 방법",
    "reason": "구체적인 금액과 방법이 동시에 나옴. 첫 3초 안에 결론 제시.",
    "hook": "근데 진짜 이게 되거든요",
    "clip_file": "clips/clip_01_월200만원자동화.mp4"
  }
]
```

## Clawitzer 연결

클립 추출 후 Clawitzer 파이프라인으로 넘기려면:

```bash
# 추출된 클립을 Clawitzer 소스로 사용
python3 projects/clawitzer/main.py \
  --video "skills/youtube-clipper-ko/outputs/TIMESTAMP/clips/clip_01.mp4" \
  --script-file "skills/youtube-clipper-ko/outputs/TIMESTAMP/clip_01_script.json"
```

단, Clawitzer의 TTS는 사용하지 않음 (원본 음성 유지).
editor.py의 자막/편집 로직만 활용 가능.

## API 키

- OpenAI Whisper: TOOLS.md의 Gemini 키 대신 OpenAI API 필요 (없으면 달비님께 요청)
- Anthropic Claude: 기존 설정 사용 (환경변수 ANTHROPIC_API_KEY)

## 바이럴 구간 선정 기준 (Claude 프롬프트 기반)

1. **감정 강도**: 놀람, 공감, 궁금증, 웃음 유발 구간
2. **정보 밀도**: 구체적 숫자/금액/방법이 나오는 구간
3. **완결성**: 클립 단독으로 이해 가능한 구간
4. **훅 가능성**: 첫 3초 안에 시청자를 잡을 수 있는 문장 포함 여부
5. **한국어 최적화**: 한국 시청자 반응 패턴 반영

## 무음/숨소리 처리

Clawitzer editor.py 로직 차용:
- silenceremove 필터 (max_gap_sec=0.06)
- 완전 제거가 아닌 압축 (자연스러운 흐름 유지)
- 숨소리 구간: 50ms로 압축

## 자막 스타일 (Clawitzer 3색 룰)

- 기본: 흰색(#FFFFFF), 52px
- 빨강 앞뒤: 노란색(#FFFF00), 52px
- 강조 키워드: 빨강(#FF0000), 62px (연속 불가)
- 폰트: SUIT ExtraBold (없으면 NotoSansCJK fallback)
- 자간: -1 (좁힘)
- 위치: 화면 중앙 (an5, Y=900/1920)
