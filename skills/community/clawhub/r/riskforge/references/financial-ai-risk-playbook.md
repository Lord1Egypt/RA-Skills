# Financial AI Risk Playbook

Use this reference when the target system involves finance, banking, payments, credit, wealth management, insurance, trading, anti-fraud, AML/KYC, risk control, customer service agents, or AI-generated financial decisions.

## Analysis Lens

### 1. Model and Agent Risk
- Identify LLM, agentic workflow, RAG, tool-calling, model-routing, prompt-template, feature-store, and scoring-model dependencies.
- Check hallucination paths, tool misuse, prompt injection, data leakage, unsafe fallback, non-deterministic approvals, and missing human-in-the-loop controls.
- Verify model output constraints for financial advice, credit decisions, risk scores, pricing, fraud flags, and compliance explanations.

### 2. Financial Data Controls
- Trace PII, account data, transaction data, credit data, device fingerprint, behavioral data, risk labels, and third-party bureau data.
- Check masking, minimization, retention, audit logging, encryption boundaries, and cross-border or cross-tenant leakage.
- Flag any test data that can reconstruct real customers, merchants, transactions, or trading positions.

### 3. Compliance and Auditability
- Require explainability for material decisions: eligibility, rejection, risk blocking, transaction review, KYC/AML flags, limit changes, and pricing.
- Check evidence trails: input snapshot, model version, prompt version, tool outputs, policy version, reviewer identity, and final decision.
- Ensure reports separate factual evidence, inferred risk, business impact, and recommended verification.

### 4. Scenario Testing
- Add adversarial tests for prompt injection, jailbreaks, document poisoning, tool-call replay, stale retrieval, conflicting policy, and manipulated transaction narratives.
- Add fairness and edge-case tests across customer segment, channel, device, geography, merchant type, transaction amount, and risk tier.
- Add resilience tests for model timeout, low-confidence output, RAG retrieval failure, upstream risk engine degradation, and partial settlement states.

## Risk Categories to Add

| Category | What to inspect | Typical evidence |
| --- | --- | --- |
| AI decision integrity | Model output drives financial outcome | prompt, model version, decision branch |
| Explainability gap | User or auditor cannot understand decision | missing reason codes or trace |
| Data leakage | Sensitive finance data enters logs/prompts | raw payload, log sink, RAG chunk |
| Prompt/tool injection | Untrusted content controls tools | tool call path, retrieved document |
| Regulatory control gap | No approval/audit trail for material decisions | missing reviewer/policy/version |
| Fairness risk | Segment-level adverse outcome | test matrix by customer/risk segment |
| Operational resilience | Model or risk service outage changes behavior | timeout/fallback branch |

## Required Output Additions

When finance or AI is in scope, add a dedicated section:

```markdown
## 金融AI专项风险

| 风险 | 代码位置 | 金融影响 | AI/模型链路 | 合规证据 | 验证建议 | 优先级 |
| --- | --- | --- | --- | --- | --- | --- |
```

Each finding must include:
- exact code location or configuration path;
- business/financial impact;
- model, prompt, RAG, or tool-calling link if applicable;
- audit/compliance evidence needed;
- concrete test or monitoring recommendation.
