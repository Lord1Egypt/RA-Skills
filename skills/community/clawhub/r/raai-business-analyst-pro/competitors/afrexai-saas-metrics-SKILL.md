# afrexai-saas-metrics — ClawHub SKILL.md (скачано с clawhub.ai) **Источник:** https://clawhub.ai/1kalin/afrexai-saas-metrics **Автор:** @1kalin (AfrexAI) **Версия:** v1.0.0 **Загрузок:** 711 **Звёзды:** 0 **Статус безопасности:** Benign high confidence **Цена:** бесплатно (контекст-паки $47/каждый) --- ## Описание Generates a complete SaaS metrics analysis from your data, benchmarking 15 key B2B SaaS KPIs for 2026 and providing red/yellow/green flags plus action items. ## Что делает 1. Запрашивает текущие числа (MRR, churn, CAC и т.д.)
2. Вычисляет производные метрики (LTV:CAC, Magic Number, Rule of 40, Burn Multiple)
3. Бенчмаркирует против SaaS-медиан 2026 по стадии (Pre-Seed → Series C+)
4. Флагирует red/yellow/green по каждой метрике
5. Выдаёт board-ready резюме с action items ## 15 ключевых метрик **Revenue:** MRR / ARR / NRR / GRR / Revenue per Employee **Growth:** MoM Growth / Quick Ratio / Magic Number **Unit Economics:** CAC / LTV / LTV:CAC / CAC Payback / Gross Margin **Efficiency:** Rule of 40 / Burn Multiple ## Бенчмарки по стадии (2026) | Стадия | ARR | NRR | LTV:CAC | Burn Multiple | Rule of 40 |
|---|---|---|---|---|---|
| Pre-Seed | <$100K | N/A | N/A | <5.0 | N/A |
| Seed | $100K-$1M | >100% | >2:1 | <3.0 | >20 |
| Series A | $1M-$5M | >110% | >3:1 | <2.0 | >30 |
| Series B | $5M-$20M | >115% | >3.5:1 | <1.5 | >35 |
| Series C+ | >$20M | >120% | >4:1 | <1.0 | >40 | ## Red Flag Detection - NRR < 100% → bucket leaking
- LTV:CAC < 1:1 → платишь больше чем получаешь
- CAC Payback > 24 мес → capital efficiency problem
- Burn Multiple > 3.0 → горишь быстрее чем растёшь
- Quick Ratio < 1.0 → emergency
- Gross Margin < 60% → это услуги, не SaaS ## Формат вывода ```
📊 SaaS METRICS DASHBOARD — [Company] — [Month YYYY]
🟢 HEALTHY / 🟡 WATCH / 🔴 FIX NOW
TOP 3 ACTIONS: [приоритеты с таргетами]
``` ## Industry Adjustments - Vertical SaaS (healthcare/legal/construction): GM 80%+, churn <2%, высокий ACV
- Horizontal SaaS: ниже маржа, выше объём
- Usage-based: потребление + традиционные метрики
- PLG: activation rate + time-to-value + viral coefficient
