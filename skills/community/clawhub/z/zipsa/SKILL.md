---
name: zipsa
description: Local-first privacy gateway for LLM applications. Use when the user needs to process sensitive, private, or proprietary information (PII, health records, internal business strategy, SSNs, credentials) while still utilizing cloud models (Claude, Gemini, GPT). Zipsa reformulates queries locally to remove identity and secrets before routing to the cloud, then synthesizes the answer back to the local context.
---

# Zipsa

Zipsa is a local-first privacy gateway that sits between OpenClaw and cloud LLMs. It ensures that raw private context never leaves the local environment while still allowing the use of powerful frontier models for reasoning.

## When to Use

Trigger this skill whenever the user provides or asks to process:
- **PII**: Names, SSNs, DOBs, contact info.
- **Healthcare Data**: Patient records, clinical notes, symptoms.
- **Internal Business Context**: Pricing floors, negotiation terms, churn warnings, project codenames.
- **Secrets**: API keys, credentials, internal system details.

## Core Workflow

Zipsa operates as an OpenAI-compatible gateway (default: `http://localhost:8000/v1`). 

### 1. Identify Sensitive Context
When the user's request contains sensitive data, explain that Zipsa will be used to protect their privacy.

### 2. Route Through Zipsa
Instead of calling the standard cloud providers directly, use the Zipsa endpoint. Zipsa will:
- **Scan locally** for high-risk markers.
- **Classify** the query (Private, Hybrid, or Knowledge).
- **Reformulate** (rewrite) the query to abstract identity and proprietary details.
- **Route** the safe version to the cloud.
- **Synthesize** the final answer back with the local details.

## Integration Examples

### Using with OpenClaw
OpenClaw can be configured to use Zipsa as its backend:
- `OPENAI_BASE_URL=http://localhost:8000/v1`
- `OPENAI_API_KEY=zipsa-key`
- `OPENAI_MODEL=zipsa`

### Multi-turn Sessions
For conversation continuity, always pass a `session_id`.
```json
{
  "model": "zipsa",
  "messages": [...],
  "extra_body": { "session_id": "unique-session-id" }
}
```

## Admin Console

Zipsa includes an enterprise Admin Console for security teams and CISOs.

Key capabilities:
- **실시간 대시보드**: 차단/알람/마스킹 건수, 활성 에이전트 모니터링
- **개인정보 유형 설정**: 개인정보보호법 제2조 기준 (고유식별정보, 민감정보, 일반 개인정보, 금융정보, 인증정보)
- **탐지·처리 정책 매트릭스**: AI 서비스별 (ChatGPT/Claude/Gemini/Copilot) 처리 방식 설정
- **조합 탐지 규칙**: 단일 항목이 아닌 복합 식별자 조합 탐지
- **민감정보 사전**: 회사별 기밀 키워드 직접 등록 (CSV/XLSX 업로드 지원)
- **알람 채널**: Slack, 이메일, Teams, Webhook(SIEM/SOAR)
- **인시던트 자동 대응**: 임계값 기반 자동 차단 및 에스컬레이션
- **ISMS-P 컴플라이언스 매핑**: 인증기준 2.0 (2024년 개정) 기준
- **감사 로그**: 3년 보존, 해시 체인 무결성 검증, SIEM 실시간 전송
- **통계 리포트**: 일/주/월간 보고서 자동 발송

For full Admin Console spec, see [references/admin-dashboard.md](references/admin-dashboard.md).

## Reference
For detailed configuration and advanced examples, see [references/README.md](references/README.md).
