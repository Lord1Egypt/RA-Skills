# afrexai-lead-hunter — ClawHub SKILL.md (скачано с clawhub.ai) **Источник:** https://clawhub.ai/1kalin/afrexai-lead-hunter **Автор:** @1kalin (AfrexAI) **Версия:** v1.0.0 **Загрузок:** 674 | **Звёзды:** 0 **Статус безопасности:** Benign high confidence **Цена:** бесплатно --- ## Описание Complete lead generation system — from ICP definition to CRM-ready qualified leads with multi-channel outreach sequences and scoring automation. ## Архитектура (8 фаз) 1. ICP Definition — ICP YAML template + Anti-signals + Account Tiering (Tier 1/2/3)
2. Lead Discovery — Multi-source discovery: LinkedIn / Apollo / Hunter.io / Google Maps / Industry directories
3. Lead Enrichment — Contact data enrichment: email verification, company firmographics, tech stack
4. Lead Scoring — BANT scoring matrix (Budget / Authority / Need / Timeline) + custom weights
5. Lead Segmentation — Hot/Warm/Cold segmentation + Tier classification
6. Outreach Sequences — 14-day Multi-Channel Sequence: Email + LinkedIn + Phone
7. CRM Integration — HubSpot / Salesforce / Pipedrive data export templates
8. Automation Triggers — n8n / Zapier automation blueprints for lead routing ## Ключевые фичи **ICP YAML template:**
```yaml
ideal_customer_profile: firmographics: {industry, size, revenue, location} technographics: {tech_stack, tools_used} buying_signals: [hiring, funding, expansion] anti_signals: [too_small, wrong_industry, competitor]
``` **Lead Scoring Matrix (BANT):**
- Budget: 0-25 points
- Authority: 0-25 points
- Need: 0-25 points
- Timeline: 0-25 points
- Total: 0-100 → Hot (75+) / Warm (50-74) / Cold (<50) **Multi-Channel Sequence (14 days):**
Email D1 → LinkedIn D1 → Email D3 (value) → LinkedIn D5 → Phone D7 → Email D10 → LinkedIn D12 → Breakup D14 **Lead Sources Coverage:**
LinkedIn Sales Navigator / Apollo.io / Hunter.io / Google Maps / Clutch.co / Crunchbase / Industry associations ## Триггерные команды (10 штук) "Build my ICP" / "Find leads for [company type]" / "Score this lead" / "Write outreach for [lead]" / "Enrich this contact" / "Segment my lead list" / "Build outreach sequence for [ICP]" / "Export to CRM format" / "Review my lead sources" / "Automate lead routing" ## Ограничения - Нет нативной интеграции — только шаблоны и экспортные форматы
- Данные из внешних источников (Apollo/Hunter.io) требуют отдельных подписок
- Бенчмарки и примеры заточены под западные рынки (US/EU SaaS)
- Нет поддержки русскоязычных источников (hh.ru, 2ГИС, РБК, Контур.Фокус)
