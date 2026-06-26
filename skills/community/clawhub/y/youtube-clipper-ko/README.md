# YouTube Clipper KO

**한국어 YouTube 영상 → 바이럴 숏폼 클립 자동 분할**

알파컷 써보고 맘에 안 들어서 직접 만들었습니다.

---

## 왜 만들었나

알파컷/피카클립은 "몇 개 뽑아서 점수 붙여준다"는 건데, 정작 **왜 이 클립을 올려야 하는지**는 안 알려줘요. 점수 숫자만 보고 고르다 보면 결국 감에 의존하게 됨.

그래서 3단계 AI 검증으로 각 클립에 이런 걸 붙여줍니다:

- 왜 이 구간이 바이럴 가능성이 있는지 (구체적 이유)
- 첫 3초 훅 문장이 뭔지
- 어떤 감정을 유발하는지 (공감/놀람/궁금증/웃음/정보)
- 올릴 때 주의할 약점

유저가 직접 보고 고르는 구조예요. 알고리즘이 대신 결정하지 않습니다.

---

## 특징

- **Haiku 3중 검증** — 1차(후보 20개 넓게) → 2차(독립 재평가, 완결성 미달 탈락) → 3차(메타데이터 보강, 시간순 정렬)
- **Whisper word-level 타임스탬프** — 자막 싱크 정확도 최고
- **3색 한국어 자막** — SUIT ExtraBold, 강조 키워드 자동 빨강/노랑 처리
- **9:16 자동 크롭** — 쇼츠/릴스/틱톡 바로 올릴 수 있는 사이즈
- **원본 음성 유지** — 클리퍼니까 TTS 없음, 무음 압축 없음
- **로컬 실행** — 영상 외부 서버에 올라가지 않음

---

## 설치

```bash
npx skills add thedalbee/youtube-clipper-ko -g -y
```

또는 직접:

```bash
git clone https://github.com/thedalbee/youtube-clipper-ko
pip install yt-dlp openai anthropic
```

필요한 것:
- ffmpeg (`apt install ffmpeg` / `brew install ffmpeg`)
- SUIT ExtraBold 폰트 (없으면 NotoSansCJK로 자동 대체)

---

## 사용법

```bash
# YouTube URL
python3 scripts/clip.py --url "https://youtu.be/VIDEO_ID"

# 구간 지정 (긴 영상)
python3 scripts/clip.py --url "https://youtu.be/VIDEO_ID" --start "10:00" --end "40:00"

# 클립 길이 조정 (기본 60초)
python3 scripts/clip.py --url "https://youtu.be/VIDEO_ID" --clip-length 90

# 자막만 먼저 확인하고 싶을 때
python3 scripts/clip.py --url "https://youtu.be/VIDEO_ID" --dry

# 로컬 파일
python3 scripts/clip.py --file "/path/to/video.mp4"
```

환경변수:

```bash
export OPENAI_API_KEY="sk-..."       # Whisper 자막 추출
export ANTHROPIC_API_KEY="sk-..."    # Claude Haiku 구간 선정
```

---

## 출력 예시

```
outputs/20260315_225000/
├── source.mp4              # 원본
├── transcript.json         # Whisper 전체 자막 + 타임스탬프
├── viral_segments.json     # 구간 분석 결과 (시간순)
├── result.json             # 전체 메타데이터
└── clips/
    ├── clip_01_월200만원자동화.mp4
    ├── clip_02_AI로3일만에만든것.mp4
    └── ...
```

`viral_segments.json` 안에 이런 게 들어있어요:

```json
[
  {
    "start_sec": 194.5,
    "end_sec": 248.0,
    "score": 82,
    "title": "월 200만원 자동화하는 법",
    "hook": "근데 진짜 이게 되거든요",
    "emotion_type": "궁금증",
    "reason": "구체적인 금액과 방법이 동시에 나옵니다. 첫 3초 안에 결론을 먼저 던지는 구조라 이탈률이 낮을 것. '이게 되거든요'라는 훅이 다음 내용을 궁금하게 만듦.",
    "weakness": "앞 맥락 모르면 '뭘 자동화한다는 건지' 불분명할 수 있음."
  }
]
```

---

## Haiku 3중 검증이 뭔가요

일반 AI 클리퍼는 한 번 판단하고 끝이에요. 이건 다릅니다.

**1차 (후보 추출)** — 자막 전체 보고 가능성 있는 구간 20개 넓게 뽑음. 이 단계에선 엄격하게 안 자름.

**2차 (독립 재평가)** — 1차 결과를 모르는 척하고 다시 평가. 이 단계에서 탈락 기준 엄격하게 적용:
- 앞 맥락 없이는 이해 불가 → 탈락
- 너무 일반적이어서 차별점 없음 → 탈락
- 단순 나열에 불과 → 탈락

**3차 (메타데이터 보강)** — 살아남은 것들에 훅/리즌/감정타입/약점 붙여서 유저가 고를 수 있게 정리. 랭킹 매기지 않음. 시간순으로 나열.

---

## 비교

| | 알파컷 | 피카클립 | YouTube Clipper KO |
|---|---|---|---|
| 바이럴 이유 설명 | ✗ | 간단히 | 3~4문장 구체적 |
| 약점 명시 | ✗ | ✗ | ✅ |
| 훅 문장 추출 | ✗ | ✗ | ✅ |
| 감정 타입 분류 | ✗ | ✗ | ✅ |
| AI 검증 단계 | 1회 | 1회 | 3회 |
| 유저가 고르는 구조 | ✗ (알고리즘 순서) | ✗ | ✅ (시간순 나열) |
| 로컬 실행 | ✗ | ✗ | ✅ |
| 오픈소스 | ✗ | ✗ | ✅ |
| 비용 | 월 5,800원~ | 월 5,500원~ | Whisper ~7원/분 + Haiku 소액 |

---

## 비용

영상 30분 기준 대략:
- Whisper: ~210원 (30분 × 7원/분)
- Claude Haiku 3회: ~50원
- **합계: 약 260원**

알파컷 월 5,800원이면 22회 사용 가능한 금액이에요.

---

## Clawitzer 연결 (선택)

[Clawitzer](https://github.com/thedalbee/clawitzer)로 추출한 클립에 한국어 자막/배경음악/편집 효과를 추가할 수 있어요.

```bash
python3 projects/clawitzer/main.py \
  --video "skills/youtube-clipper-ko/outputs/TIMESTAMP/clips/clip_01.mp4"
```

---

## 만든 사람

달비 ([@thedalbee](https://x.com/thedalbee))

YouTube 채널 "기획자 달비"에서 이 툴 만드는 과정을 공개하고 있습니다.
→ [youtube.com/@기획자달비](https://youtube.com/@기획자달비)

---

## 라이선스

MIT
