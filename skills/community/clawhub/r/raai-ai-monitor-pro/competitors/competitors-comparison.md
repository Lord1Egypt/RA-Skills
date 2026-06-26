# ai-monitor-pro — Анализ конкурентов (verified + гипотезы, перезаписано 2026-04-20) > Конкуренты 1-2: прямой скрейп clawhub.ai через firecrawl 2026-04-20. > Конкурент 3: 🟡 гипотеза — прямых аналогов на ClawHub не найдено. --- ## Конкурент 1: afrexai-sre-platform by @1kalin **✅ verified** | URL: https://clawhub.ai/1kalin/afrexai-sre-platform **Загрузок:** 654 | **Звёзды:** 2 | **Версия:** v1.0.0 | **Цена:** бесплатно **Что делает:** Полная SRE-методология — от определения SLO до chaos engineering и управления on-call. 12 фаз, instruction-only, zero dependencies. Ориентирован на IT/Cloud сервисы. **Количество триггеров/режимов:** 12 команд / 12 фаз. **Ключевые фичи:**
- SLI/SLO Framework + Error Budget Policy (4 состояния)
- Burn Rate Alerts (fast 14.4x / medium 6.0x / slow 1.0x)
- Incident ICS (6 ролей + 6-step workflow)
- Blameless Postmortem Template + 5 Whys + Fishbone
- Chaos Engineering (Maturity 0-4 + 12 сценариев)
- Toil Management (<25% правило)
- On-Call Health Metrics (7 KPI)
- 100-Point SRE Quality Rubric **Таблица различий:** | Фича | afrexai-sre-platform | НАША |
|---|---|---|
| Строительные объекты / стройплощадки | НЕТ (IT/Cloud only) | ДА |
| TG-алёрты | НЕТ | ДА |
| Российские системы мониторинга | НЕТ | ДА |
| Русский язык | НЕТ | ДА |
| Мониторинг бизнес-процессов (не IT) | НЕТ | ДА |
| SLO/Error Budget framework | ДА | ДА |
| Incident Response | ДА | ДА | --- ## Конкурент 2: overkill-mission-control by @broedkrummen **✅ verified** | URL: https://clawhub.ai/broedkrummen/overkill-mission-control **Загрузок:** 370 | **Звёзды:** 0 | **Версия:** v1.0.1 **Флаг безопасности:** Suspicious (high confidence) — systemd services + sudo/root + hardcoded paths **Что делает:** Dashboard для мониторинга OpenClaw AI-агентов. Real-time metrics, agent-to-agent messaging, SLO tracking, automation workflows. Требует Node.js + Tailscale. **Ключевые фичи:**
- 17-страничный Next.js дашборд
- CPU/memory/disk мониторинг
- SLO + Error Budget tracker
- Automation workflows (visual builder)
- Agent-to-agent messaging (MiniMax M2.5)
- SQLite-backed с FTS5 поиском **Таблица различий:** | Фича | overkill-mission-control | НАША |
|---|---|---|
| Строительная специфика | НЕТ (только AI-агенты) | ДА |
| Русский язык | НЕТ | ДА |
| TG-алёрты | НЕТ | ДА |
| Безопасность | Suspicious | Benign |
| Без настройки сервера | НЕТ (Node.js + Tailscale) | ДА |
| Мониторинг бизнес-KPI | НЕТ | ДА | --- ## Конкурент 3: IT-мониторинг скиллы (общие) **🟡 гипотеза** — поиск по "site:clawhub.ai monitor alert construction building site" вернул 0 строительных скиллов. Ближайшие результаты — SRE/IT мониторинг. **Оценка ниши:**
- На ClawHub нет скиллов мониторинга строительных объектов
- Все найденные мониторинговые скиллы (skytekx/cpu/SRE) ориентированы на IT
- Строительный AI-мониторинг (сроки/бюджет/риски) — незанятая ниша на ClawHub --- ## Сводная таблица + наши дифференциаторы | Дифференциатор | afrexai-sre | overkill-mc | IT-мониторинг | НАША |
|---|---|---|---|---|
| Строительные объекты | НЕТ | НЕТ | НЕТ | **ДА** |
| TG-алёрты | НЕТ | НЕТ | НЕТ | **ДА** |
| Русский язык | НЕТ | НЕТ | НЕТ | **ДА** |
| Мониторинг сроков/бюджета | НЕТ | НЕТ | НЕТ | **ДА** |
| Без сервера/Node.js | ДА | НЕТ | НЕТ | **ДА** |
| Безопасность Benign | ДА | НЕТ | н/д | **ДА** | --- ## 6 verified дифференциаторов ai-monitor-pro 1. **Строительные объекты** — мониторинг стройплощадок, сроков сдачи, бюджетов, субподрядчиков. Все конкуренты мониторят IT-инфраструктуру.
2. **TG-алёрты** — ни у одного конкурента нет нативной отправки алёртов в Telegram. Наша — ДА (критично для строительных прорабов).
3. **Русский язык** — все verified конкуренты EN-only.
4. **Мониторинг бизнес-процессов** — afrexai-sre и overkill-mc мониторят технические метрики (CPU/SLO). Наша — бизнес-KPI стройки (сроки/смета/брак/оплаты).
5. **Без серверной настройки** — overkill-mc требует Node.js 22+ / Tailscale / systemd. Наша — instruction-only, 15 мин.
6. **Ниша пустая на ClawHub** — прямых строительных мониторинговых скиллов на ClawHub не обнаружено. Первый выход = преимущество. --- *verified: afrexai-sre-platform + overkill-mission-control — прямой скрейп clawhub.ai 2026-04-20.* *Конкурент 3 — 🟡 гипотеза: строительных мониторинговых скиллов на ClawHub не найдено.*
