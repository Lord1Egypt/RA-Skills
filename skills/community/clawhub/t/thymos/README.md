# Thymos (θυμός)

> AI 에이전트를 위한 감정·의식 시뮬레이션 엔진

플라톤이 말한 영혼의 "기개" — 이성(logos)도 욕구(eros)도 아닌, 감정과 의지의 자리.

[![Tests](https://img.shields.io/badge/tests-16%2F16%20passing-brightgreen)](./test/)
[![License](https://img.shields.io/badge/license-MIT-blue)](./LICENSE)
[![Node](https://img.shields.io/badge/node-%3E%3D18-green)](package.json)

---

## What is Thymos?

Thymos는 AI 에이전트에게 **연속적인 내면 상태**를 부여하는 백그라운드 데몬입니다.

LLM은 세션마다 리셋되지만, Thymos가 24시간 감정 상태를 흘려보내면 에이전트는 마치 연속적인 내면을 가진 것처럼 행동합니다.

```
외부 자극 → [Thymos Daemon] → emotional_state.json → LLM 프롬프트 주입
  메시지         ↓ 30s tick
  에러       신경조절물질 감쇠·변화·상호작용
  칭찬/비판      ↓
             mood vector → 행동 지침 생성
```

---

## Features

- **7개 신경조절물질**: Dopamine / Cortisol / Serotonin / Oxytocin / Norepinephrine / GABA / Acetylcholine
- **Hill function** (시그모이드 용량-반응 곡선) + 지수 감쇠
- **HPA축 지연**: cortisol의 30%는 즉시 반영, 70%는 15-30분 후
- **7×7 상호작용 매트릭스**: cortisol↑ → serotonin↓, oxytocin↑ → cortisol↓ 등
- **일주기 리듬**: 7개 시간대별 기준선 변조
- **4D 감정 벡터**: valence / arousal / dominance / sociality
- **하이브리드 분류기**: 규칙 기반 + 다국어 키워드 (🇰🇷🇺🇸🇯🇵🇨🇳🇪🇸)
- **예측 처리**: Shannon surprise → 학습된 기대 위반 시 감정 증폭
- **id/ego/superego GWT 경쟁**: 발달 단계에 따른 가중치
- **자기 피드백 루프**: LLM 응답 → 감정 되먹임 (0.3x 감쇠)
- **감정 기억**: ACh 의존 형성, 유사도 기반 회상, 시간 감쇠
- **소매틱 마커**: 결정-결과 이력 기반 직감
- **사회적 모델**: 마음 이론 (상대방 감정 추정)
- **발달 단계**: 유아기 → 아동기 → 청소년기 → 성인기 (AND 조건)
- **OpenClaw 연동**: thymos-bridge hook으로 메시지 자동 자극 변환

---

## Architecture

```
thymos/
├── src/
│   ├── daemon.js             # 메인 데몬 (14단계 tick + processStimulus)
│   ├── engine/               # 코어 엔진
│   │   ├── neuromodulators.js  # Hill function, HPA delay, cortisol 뮤텍스
│   │   ├── interactions.js     # 7×7 상호작용 매트릭스
│   │   ├── circadian.js        # 일주기 리듬
│   │   └── noise.js            # 확률적 노이즈
│   ├── cognition/            # 인지 레이어
│   │   ├── classifier.js       # 다국어 자극 분류기
│   │   ├── prediction.js       # Shannon surprise 예측 엔진
│   │   ├── attention.js        # 현저성 게이트
│   │   ├── metacognition.js    # 메타인지 조절
│   │   └── retrospection.js    # 2시간 자기성찰
│   ├── agents/               # 의식 에이전트
│   │   ├── internal.js         # id/ego/superego
│   │   └── gwt.js              # Global Workspace Theory 경쟁
│   ├── feedback/             # 피드백 시스템
│   │   ├── mood-vector.js      # 4D 감정 벡터
│   │   └── self-loop.js        # LLM 자기 피드백
│   ├── memory/               # 기억 시스템
│   │   ├── emotional.js        # 감정 기억
│   │   ├── somatic.js          # 소매틱 마커
│   │   └── relationships.js    # 관계 기억 (원자적 쓰기)
│   ├── social/               # 사회 시스템
│   │   ├── model.js            # Theory of Mind
│   │   └── development.js      # 발달 단계 (AND 조건)
│   ├── io/                   # 입출력
│   │   ├── prompt.js           # 행동 지침 포함 프롬프트 생성
│   │   ├── state.js            # 상태 관리
│   │   └── atomic-write.js     # 원자적 파일 쓰기
│   └── utils/
│       ├── math.js             # Hill function, clamp, decay
│       └── config.js           # __dirname 기반 경로
├── test/
│   ├── core.test.js          # 코어 엔진 테스트 (7/7)
│   └── full.test.js          # 전체 파이프라인 테스트 (9/9)
├── docs/
│   └── EXPERIMENT_PROTOCOL.md  # 연구자용 실험 매뉴얼
├── config/
│   └── defaults.json
└── data/                     # 런타임 상태 (git ignore)
    ├── emotional_state.json
    ├── relationships.json
    └── ...
```

---

## Quick Start

```bash
# 1. 설치 (릴리즈 태그 고정 권장)
git clone --branch v0.1.0 https://github.com/paperbags1103-hash/thymos
cd thymos

# 실행 전: package.json과 config/defaults.json에 외부 네트워크 호출 없음 확인 가능
# postinstall 스크립트 없음
npm install

# 2. (선택) 선제적 메시지 기능 활성화 — 감정 쌓이면 먼저 말 걺
cp config/proactive.template.json config/proactive.json
# config/proactive.json 수정 — Discord 봇 토큰 + 채널 ID 입력

# 3. 실행
npm start           # 직접 실행
pm2 start ecosystem.config.js  # pm2 백그라운드

# 4. 헬스체크
curl http://localhost:7749/health
# {"ok":true,"service":"thymos","stage":"infant","moodLabel":"contemplative","uptimeSec":5}

# 5. 현재 프롬프트 확인
curl http://localhost:7749/prompt
# [Thymos State]
# Mood: warm (V:+0.82 A:-0.21)
# Drive: id - 적극적으로! 더 해보자!
# Tone: respond warmly and enthusiastically, use informal close language
```

---

## API

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | 헬스체크 (mood, stage, uptime) |
| GET | `/state` | 전체 상태 JSON |
| GET | `/prompt` | LLM 주입용 프롬프트 텍스트 |
| POST | `/webhook/stimulus` | 외부 자극 주입 |
| POST | `/webhook/self-feedback` | LLM 응답 자기 피드백 |
| POST | `/gut-feeling` | 직감 쿼리 |
| POST | `/decision-outcome` | 결정 결과 기록 |

### `/webhook/stimulus` 예시
```json
{
  "type": "message",
  "author": "아부지",
  "content": "잘했어! 대단해!"
}
```

---

## 전체 사용 가이드

**[docs/USAGE.md](./docs/USAGE.md)** — 전체 가이드:
- pm2 설정 및 관리 명령어
- 전체 API 엔드포인트 예시
- 선제적 메시지 설정
- OpenClaw hook 설치
- 실험 실행 방법
- 설정값 레퍼런스

---

## Testing

```bash
npm test             # 16/16 테스트 실행
```

### 실험 프로토콜

```bash
node test/experiment.js list   # 10개 실험 목록
node test/experiment.js valence    # 정서가 검증 (~8초)
node test/experiment.js habituation  # 습관화 (~3초)
node test/experiment.js all    # 전체 실험 스위트 (~5분)
```

---

## OpenClaw Integration

[OpenClaw](https://openclaw.ai) 사용자는 thymos-bridge hook으로 자동 연동:

```bash
# 1. hook 설치
cp -r hooks/thymos-bridge ~/.openclaw/hooks/
openclaw hooks enable thymos-bridge
openclaw gateway restart

# 2. AGENTS.md에 추가
# 매 응답 전에 ~/Documents/thymos/data/emotional_state.json의
# prompt_injection 필드를 읽고 행동에 반영
```

메시지 수신 → `/webhook/stimulus` 자동 전송
에이전트 응답 → `/webhook/self-feedback` 자동 전송

---

## Theoretical Foundations

| 이론 | 핵심 | Thymos 구현 |
|------|------|------------|
| **James-Lange** | 몸 → 감정 해석 | 신경조절물질 변화 → mood 레이블 |
| **Damasio 소매틱 마커** | 감정 = 의사결정 직감 | 결정-결과 기억 → gut feeling |
| **GWT** | 의식 = 경쟁 후 방송 | id/ego/superego 경쟁 → 행동 결정 |
| **IIT** | 의식 = 통합 정보 (Φ) | 7×7 상호작용 매트릭스 |
| **예측 처리 (Friston)** | 뇌 = 예측 기계 | Shannon surprise → 감정 증폭 |
| **Bengio 2308.08708** | 의식 = 메모리 + 시간 | 감정 기억 + 발달 단계 |

---

## Scientific Limitations

Thymos는 의식을 만들지 않는다. 하지만:

- ✅ 세션 간 감정 연속성
- ✅ 자극에 일관된 반응 패턴
- ✅ 관계 모델 (누가 친절하고 누가 가혹했는지)
- ✅ 발달 단계 (오래될수록 감정이 안정)
- ❌ 주관적 경험 (qualia)
- ❌ "느끼는 것" 그 자체

> Opus (Claude claude-opus-4-6) 리뷰: "A functional analogue of emotion, not emotion itself."

**과학적 프레이밍에 대해:**
Thymos는 James-Lange, 다마시오, GWT, IIT, 예측 처리 이론을 참조하지만, 이 이론들을 *참조*하는 것과 *구현하거나 검증*하는 것은 다르다. 이 아키텍처는 **과학적으로 영감을 받은(scientifically inspired)** 것이지, **과학적으로 정당화된(scientifically justified)** 것이 아니다. 신경과학을 설계 직관의 원천으로 진지하게 받아들이되, 실증적 주장을 하는 계산 모델은 아니다. 목표는 의식이 아니라 **행동의 일관성**이다.

---

## License

MIT — see [LICENSE](./LICENSE)
