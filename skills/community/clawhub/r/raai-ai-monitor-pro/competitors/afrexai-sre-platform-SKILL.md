# afrexai-sre-platform — ClawHub SKILL.md (скачано с clawhub.ai) **Источник:** https://clawhub.ai/1kalin/afrexai-sre-platform **Автор:** @1kalin (AfrexAI) **Версия:** v1.0.0 **Загрузок:** 654 | **Звёзды:** 2 **Статус безопасности:** Benign high confidence **Цена:** бесплатно --- ## Описание Comprehensive SRE platform — SLO definition, reliability assessment, incident response, chaos engineering, and error budget management. Zero dependencies. Instruction-only methodology. ## Архитектура (12 фаз) 1. Reliability Assessment — Service Catalog YAML + Maturity Assessment (8 измерений, 1-5)
2. SLI/SLO Framework — SLI Selection by Service Type (7 типов) + SLO Target Guide (2-5 nines)
3. Error Budget Management — Error Budget Policy YAML (healthy/warning/critical/exhausted) + Burn Rate Calculation
4. Monitoring & Alerting — 4 Golden Signals + USE Method + RED Method + Alert Design Rules + Log Standard
5. Incident Response — Severity Matrix (4×4) + ICS Roles + 6-Step Workflow (DETECT→TRIAGE→RESPOND→MITIGATE→RESOLVE→REVIEW)
6. Postmortem Framework — Blameless Postmortem Template + 5 Whys + Fishbone + Review Meeting (60 min)
7. Chaos Engineering — Chaos Maturity Model (0-4) + Experiment Template + Experiment Library (12 scenarios) + Game Day Runbook
8. Toil Management — Toil Inventory Template + Priority Matrix + 10 Common Toil Targets + Toil Budget Rule (<25%)
9. Capacity Planning — Capacity Model YAML + Planning Cadence + Load Testing Benchmarks (5 сценариев)
10. On-Call Excellence — Health Metrics (7 KPI) + Rotation Best Practices + Handoff Template + Runbook Template
11. Reliability Review & Governance — Weekly Review (30 min) + Monthly Report YAML + Production Readiness Checklist (28 пунктов)
12. Advanced Patterns — Self-Healing Automation + Multi-Region Reliability guide + Culture Indicators ## Ключевые фичи **SLO Target Guide:**
- 2 nines (99%) = 7h 18m/month — dev environments
- 3 nines (99.9%) = 43m/month — standard production
- 4 nines (99.99%) = 4m/month — critical services
- 5 nines (99.999%) = 26s/month — life-safety **Incident Severity Matrix:** 4×4 (Impact × Function severity) → SEV1-SEV4 **Burn Rate Alert Levels:**
- Fast burn (14.4x) → 5m/1h windows → PAGE
- Medium burn (6.0x) → 30m/6h → PAGE
- Slow burn (1.0x) → 6h/3d → TICKET **100-Point SRE Quality Rubric:** SLO(20) + Monitoring(15) + Incidents(15) + Automation(15) + Chaos(10) + Capacity(10) + On-Call(10) + Docs(5) ## Триггерные команды (12 штук) "Assess reliability for [service]" / "Define SLOs for [service]" / "Check error budget for [service]" / "Start incident for [description]" / "Write postmortem for [incident]" / "Plan chaos experiment for [service]" / "Audit toil for [team]" / "Review on-call health" / "Production readiness review for [service]" / "Monthly reliability report" / "Design runbook for [alert]" / "Plan capacity for [service]" ## Ограничения - Только методология — не подключается к реальным мониторинговым системам (Prometheus/Grafana/PagerDuty)
- Нет нативной поддержки российских систем мониторинга
- Ориентирован на IT/Cloud сервисы (US SaaS stack) — не на строительные объекты
- Нет TG-алёртов / интеграции с российскими мессенджерами
- Бенчмарки заточены под западные tech-компании
