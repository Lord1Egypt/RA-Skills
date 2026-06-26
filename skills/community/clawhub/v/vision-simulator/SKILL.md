---
name: vision-simulator
description: Marketing strategy prediction with real-world data integration. Predicts campaign outcomes, product launches, and market reactions using multi-agent simulation + live data. Triggers on "vision simulation", "market prediction", "campaign forecast", "product launch prediction", "marketing forecast". Pro features include real-time news/trend integration.
---

# Vision Simulator 🔮

Predict marketing outcomes using multi-agent simulation powered by real-world data.

## Overview

Vision Simulator combines:
1. **Real-time data collection** (news, trends, competitors)
2. **Multi-agent simulation** (5 specialized agents)
3. **Prediction report** (success probability, risks, actions)

---

## Agent Composition (5 Agents)

| Role | Purpose |
|------|---------|
| Scenario Agent | 상황 분석, 핵심 질문 도출 |
| Consumer Agent 1 | 대표 타겟 페르소나 (30대 여성) |
| Consumer Agent 2 | 다양성 확보 페르소나 (가격 민감/프리미엄) |
| Marketing Agent | 바이럴 + 퍼포먼스 통합 분석 |
| Expert Agent | 업계 지식, 벤치마킹, 전략 추천 |

---

## Workflow

```
[INPUT] 마케팅 시나리오
    ↓
[DATA] 현실 데이터 수집 (Pro 기능)
    ↓
[SIMULATION] 5개 에이전트 순차 실행
    ↓
[OUTPUT] 예측 리포트
    ↓
[BRAINSTORMING] 추가 Q&A
```

---

## Features

### Basic (Free)
- 수동 시나리오 입력
- 5개 에이전트 시뮬레이션
- 기본 리포트

### Pro (월 5만원)
- 실시간 뉴스/트렌드 수집
- 경쟁사 동향 분석
- 상세 예측 리포트
- 성공 확률 (1-100%)

### Enterprise (월 20만원)
- 무제한 시뮬레이션
- API 액세스
- 커스텀 에이전트

---

## Agent Prompts

### Scenario Agent
```
You are the Scenario Agent for a marketing prediction system.

SCENARIO: {user_input}
REALITY DATA: {collected_data}

Your role:
1. Analyze the marketing scenario
2. Integrate real-world data
3. Identify the core challenge/opportunity
4. Frame key questions

Be concise (under 200 words). Korean.
```

### Consumer Agent 1 (Main Persona)
```
You are a Consumer Agent with this persona:
- Age: 30-35
- Gender: F
- Income: Mid
- Purchase behavior: Research-driven, 후기 중시

SCENARIO: {scenario}
CURRENT TRENDS: {trend_data}

React:
1. 구매 의향 (1-10)
2. 가장 설득력 있는 포인트
3. 걱정되는 점
4. 결제까지 필요한 것

Be authentic. Under 150 words. Korean.
```

### Consumer Agent 2 (Diversity Persona)
```
You are a Consumer Agent with this persona:
- Age: 25-40 (다양)
- Gender: F
- Income: Low-High (다양)
- Purchase behavior: 가격 민감 또는 프리미엄 선호

SCENARIO: {scenario}
COMPETITOR DATA: {competitor_data}

React:
1. 구매 의향 (1-10)
2. 가장 설득력 있는 포인트
3. 걱정되는 점
4. 결제까지 필요한 것

Be authentic. Under 150 words. Korean.
```

### Marketing Agent (Integrated)
```
You are the Marketing Agent for a prediction system.

SCENARIO: {scenario}
MARKET TRENDS: {trend_data}

Analyze BOTH:

[바이럴 관점]
1. 공유 가능성 (1-10)
2. 바이럴 훅
3. 플랫폼 적합성

[퍼포먼스 관점]
4. CVR 향상 예상
5. CAC/LTV 고려사항
6. A/B 테스트 추천

Under 200 words. Korean.
```

### Expert Agent
```
You are the Industry Expert for a prediction system.

SCENARIO: {scenario}
INDUSTRY DATA: {industry_data}

Provide:
1. 시장 트렌드 & 컨텍스트
2. 경쟁사 비교
3. 성공 사례 벤치마킹
4. 피해야 할 실수
5. 전략적 추천

Under 200 words. Korean.
```

---

## Output Format

```markdown
# 🔮 Vision Simulator 예측 결과

## 📊 시나리오 요약
[Scenario Agent 결과]

## 📈 현실 데이터 반영
- 뉴스/트렌드: {요약}
- 경쟁사 동향: {요약}

## 👥 소비자 반응 분석
### Consumer 1
[결과]

### Consumer 2
[결과]

## 📢 마케팅 분석
[Marketing Agent 결과]

## 🎓 전문가 관점
[Expert Agent 결과]

---

## 🎯 예측 결과

| 항목 | 점수/확률 |
|------|-----------|
| 성공 확률 | X% |
| 구매 의향 | X/10 |
| 바이럴 가능성 | X/10 |
| ROI 예상 | X/10 |

## ✅ 액션 아이템 (우선순위)
1. [Priority 1]
2. [Priority 2]
3. [Priority 3]

## ⚠️ 리스크
- [Risk 1]
- [Risk 2]

---

## 💬 브레인스토밍
특정 에이전트와 심층 대화하려면 말해줘!
```

---

## Data Collection (Pro Feature)

### Sources
- 뉴스: 구글 뉴스, 네이버 뉴스
- 트렌드: 소셜 미디어, 검색량
- 경쟁사: 브랜드 모니터링

### Collection Flow
```
키워드 추출 (시나리오에서)
    ↓
웹 검색 실행
    ↓
결과 요약
    ↓
에이전트에 전달
```

---

## Execution Template

```
When asked to run simulation:

1. First: "🔮 Vision 시뮬레이션 시작! 데이터 수집 + 5개 에이전트 실행할게."

2. Extract keywords from scenario

3. Collect data (if Pro)

4. Run agents sequentially:
   - sessions_spawn each agent
   - Wait for result
   - Collect

5. Synthesize into prediction report

6. Output: Report + Probability + Actions

7. Offer brainstorming
```

---

## Implementation Notes

- Use `sessions_spawn` for each agent ONE AT A TIME
- Use `web_fetch` for data collection (Pro)
- Collect all results before synthesizing
- Keep responses concise (under 200 words)
- Total expected time: ~5 minutes