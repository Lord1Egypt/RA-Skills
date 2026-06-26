# dellight-cro-revenue-ops — ClawHub SKILL.md (скачано с clawhub.ai) **Источник:** https://clawhub.ai/arthurelgindell/dellight-cro-revenue-ops **Автор:** @arthurelgindell (DELLIGHT.AI) **Версия:** v1.0.0 **Загрузок:** 713 | **Звёзды:** 0 **Статус безопасности:** Suspicious (отсутствуют скрипты pipeline_tracker.py и revenue_forecast.py) **Цена:** бесплатно --- ## Описание CRO Revenue Operations system for DELLIGHT.AI — revenue strategy, pipeline management, pricing, BANT-AI qualification, and founder-led sales playbook. ## Архитектура **Revenue Operations Stack:**
1. Market Analysis — TAM/SAM/SOM, competitive positioning, pricing benchmarks
2. BANT-AI Qualification — Budget / Authority / Need / Timeline / AI-Readiness
3. Pipeline Management — LEAD → QUALIFIED → PROPOSAL → NEGOTIATION → CLOSED-WON
4. Pricing Strategy — Value-based pricing (не cost-plus), tiered packages
5. Founder-Led Sales — Personal brand, content marketing, thought leadership
6. ROI Calculator — scripts/roi_calculator.py (Benign, включён)
7. Revenue Forecasting — pipeline_tracker.py (MISSING — Suspicious flag)
8. Content Marketing — LinkedIn, thought leadership, case studies ## Ключевые фичи **BANT-AI Qualification Matrix:**
- Budget: confirmed / range / unknown
- Authority: DM / influencer / end-user
- Need: critical / important / nice-to-have
- Timeline: immediate / quarter / year
- AI-Readiness: champion / skeptic / no-context **Pipeline Stages:**
```
LEAD → QUALIFIED → PROPOSAL → NEGOTIATION → CLOSED-WON / CLOSED-LOST
``` **Value-Based Pricing Framework:**
- ROI calculation for client
- Value metrics definition
- Price anchoring against alternatives
- Discount guardrails **Founder-Led Sales Playbook:**
- Outbound: LinkedIn DMs + email
- Inbound: content funnel
- Referral: customer success → expansion
- Partnership: integrations ecosystem ## Флаги безопасности - **Suspicious** — скилл декларирует `pipeline_tracker.py` и `revenue_forecast.py` в descriptions, но файлы физически отсутствуют в архиве
- `roi_calculator.py` присутствует и Benign ## Ограничения - Жёсткая привязка к бренду DELLIGHT.AI — не white label
- Фокус на AI/SaaS продажах — нет адаптации под строительство / B2G
- Без русского языка
- Suspicious статус из-за missing scripts
- Методология founder-led = применима только при наличии сильного личного бренда основателя
