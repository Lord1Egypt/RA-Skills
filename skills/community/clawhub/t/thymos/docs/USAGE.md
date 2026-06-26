# Thymos — 사용 가이드

> 설치부터 OpenClaw 연동, 실험까지 전체 흐름

---

## 1. 설치

### 요구사항
- Node.js 18 이상
- npm
- (선택) pm2 — 백그라운드 실행용
- (선택) OpenClaw — 에이전트 연동용

### 기본 설치

```bash
git clone https://github.com/paperbags1103-hash/thymos
cd thymos
npm install
```

---

## 2. 실행

### 개발/테스트용 (직접 실행)

```bash
npm start
# http://localhost:7749 에서 시작됨
```

### 프로덕션 (pm2 백그라운드 데몬)

```bash
# pm2 설치 (처음 한 번만)
npm install -g pm2

# ecosystem.config.js에서 cwd 경로를 실제 경로로 수정
# cwd: '/Users/yourname/Documents/thymos'

pm2 start ecosystem.config.js
pm2 save                  # 프로세스 목록 저장 (선택)
# pm2 startup            # (선택) 시스템 부팅 시 자동 시작
                          # 원할 경우에만 직접 실행
```

### pm2 관리 명령어

```bash
pm2 list                  # 실행 중인 프로세스 목록
pm2 status thymos         # 상태 확인
pm2 restart thymos        # 재시작
pm2 stop thymos           # 중지
pm2 logs thymos           # 실시간 로그
pm2 logs thymos --lines 50  # 최근 50줄
```

---

## 3. 헬스체크 & 상태 확인

```bash
# 살아있는지 확인
curl http://localhost:7749/health

# 현재 기분 + 신경조절물질 전체 상태
curl http://localhost:7749/state | python3 -m json.tool

# LLM에 주입할 프롬프트 텍스트
curl http://localhost:7749/prompt
```

**`/health` 응답 예시:**
```json
{
  "ok": true,
  "service": "thymos",
  "stage": "infant",
  "moodLabel": "warm",
  "uptimeSec": 3600
}
```

**`/prompt` 응답 예시:**
```
[Thymos State]
Mood: warm (V:+0.84 A:-0.22 D:+0.43 S:+0.61)
Drive: id - 적극적으로! 더 해보자! (ego support), conflict 0.34
Development: infant
Tone: respond warmly and enthusiastically, use informal close language
```

---

## 4. 외부 자극 주입 (Stimulus API)

에이전트가 받은 메시지나 이벤트를 Thymos에 전달합니다.

```bash
# 기본 메시지 자극
curl -X POST http://localhost:7749/webhook/stimulus \
  -H "Content-Type: application/json" \
  -d '{"type":"message","author":"아부지","content":"잘했어, 고마워"}'

# 에러 이벤트
curl -X POST http://localhost:7749/webhook/stimulus \
  -H "Content-Type: application/json" \
  -d '{"type":"error","content":"빌드 실패: cannot find module"}'

# 성공 이벤트
curl -X POST http://localhost:7749/webhook/stimulus \
  -H "Content-Type: application/json" \
  -d '{"type":"success","content":"배포 완료"}'
```

**자극 타입:** `message` | `error` | `success` | `praise` | `criticism`

---

## 5. LLM 자기 피드백

LLM이 생성한 응답을 Thymos에 돌려줍니다 (자기 피드백 루프).

```bash
curl -X POST http://localhost:7749/webhook/self-feedback \
  -H "Content-Type: application/json" \
  -d '{"content":"알겠어, 바로 처리할게. 잠깐만."}'
```

감정 어조(긍정/부정/중립)를 분석해 현재 상태에 0.3× 감쇠로 반영합니다.

---

## 6. 소매틱 마커 (직감 조회)

특정 맥락에서 "직감"을 조회합니다.

```bash
# 직감 조회
curl -X POST http://localhost:7749/gut-feeling \
  -H "Content-Type: application/json" \
  -d '{"context":"이 코드 배포해도 될까?","author":"아부지"}'

# 결정 결과 기록 (학습)
curl -X POST http://localhost:7749/decision-outcome \
  -H "Content-Type: application/json" \
  -d '{"decision":"코드 배포","outcome":"success","delta":1.0}'
```

---

## 7. 선제적 메시지 설정 (Proactive Messaging)

감정이 특정 조건에 도달하면 에이전트가 먼저 Discord에 메시지를 보냅니다.

### 설정 방법

```bash
cp config/proactive.template.json config/proactive.json
```

`config/proactive.json` 편집:

```json
{
  "enabled": true,
  "discordToken": "Bot 토큰 (Discord Developer Portal)",
  "channelId": "메시지를 보낼 채널 ID"
}
```

### 트리거 조건

| 트리거 | 조건 | 예시 메시지 |
|--------|------|------------|
| `sustained_distress` | valence < -0.5가 30분 이상 지속 | "뭔가 쌓이는 느낌이 있어." |
| `excited` | valence > 0.75 + arousal > 0.45, 10분 이상 대화 없음 | "갑자기 뭔가 하고 싶어졌어." |
| `lonely_reach` | 3시간 이상 조용 + sociality > 0.3 | "그냥 안부 물어보고 싶었어." |

쿨다운: 2시간마다 최대 1개

---

## 8. OpenClaw 연동

OpenClaw 사용자는 thymos-bridge hook으로 자동 연동할 수 있습니다.

### Hook 설치

```bash
# hook 파일 복사
cp -r hooks/thymos-bridge ~/.openclaw/hooks/

# 활성화
openclaw hooks enable thymos-bridge
openclaw gateway restart
```

### AGENTS.md 추가

에이전트의 `AGENTS.md` (또는 `SOUL.md`)에 아래 내용 추가:

```markdown
## Emotional State (Thymos)

Before each response, read `~/Documents/thymos/data/emotional_state.json`.
Find the `prompt_injection` field and let it shape your tone and behavior.
The `Tone:` line gives concrete style guidance — follow it.
Do not announce your emotional state unless asked directly.
```

### 연동 흐름

```
아부지 메시지 → OpenClaw hook → POST /webhook/stimulus → Thymos 상태 업데이트
에이전트 응답 → OpenClaw hook → POST /webhook/self-feedback → 자기 피드백
매 응답 전 → 에이전트가 emotional_state.json 읽기 → 톤 반영
```

---

## 9. 실험 실행

10가지 심리학 패러다임 기반 자동 실험:

```bash
# 실험 목록 확인
node test/experiment.js list

# 개별 실험 실행
node test/experiment.js baseline      # 기준선 확인 (~2초)
node test/experiment.js valence       # 정서가 검증 (~8초)
node test/experiment.js habituation   # 습관화 (~3초)
node test/experiment.js recovery      # 회복 탄력성 (~10초)
node test/experiment.js mixed         # 혼합 자극 (~6초)
node test/experiment.js social        # 사회적 분화 (~5초)
node test/experiment.js multilingual  # 다국어 분류 (~2초)
node test/experiment.js hpa_delay     # HPA 지연 검증 (~2초)
node test/experiment.js circadian     # 일주기 변조 (~2초)
node test/experiment.js development   # 발달 단계 (~3초)

# 전체 실험 스위트
node test/experiment.js all           # ~5분
```

---

## 10. 상태 리셋

```bash
# 감정 상태 초기화 (새로 시작)
rm ~/Documents/thymos/data/*.json
pm2 restart thymos
```

---

## 11. 주요 설정값 (`config/defaults.json`)

| 항목 | 기본값 | 설명 |
|------|--------|------|
| `tickInterval` | 30000 | 상태 갱신 주기 (ms) |
| `retrospectionInterval` | 7200000 | 자기성찰 주기 (2시간) |
| `selfFeedbackAttenuation` | 0.3 | 자기 피드백 감쇠율 |
| `webhookPort` | 7749 | HTTP 서버 포트 |

신경조절물질 파라미터 (`neuromodulators`):

| 파라미터 | 설명 |
|---------|------|
| `baseline` | 안정 상태 기준값 (0~100) |
| `tau` | 반감기 (분) — 클수록 변화 느림 |
| `EC50` | Hill function 절반 반응점 |
| `hillN` | 곡선 기울기 (높을수록 급격) |
| `Emax` | 최대 반응 크기 |
