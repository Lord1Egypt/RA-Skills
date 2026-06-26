# project-management-guru-adhd — ClawHub SKILL.md (скачано с clawhub.ai) **Источник:** https://clawhub.ai/mikecourt/project-management-guru-adhd **Автор:** @mikecourt (оригинал: @erichowens, конвертация в MoltBot формат: Mike Court) **Версия:** v1.0.0 **Загрузок:** 2 800 | **Звёзды:** 3 **Статус безопасности:** Suspicious (medium confidence) — заявлены интеграции (Slack/Calendar/GitHub webhooks) без деклараций credentials; unicode control chars в SKILL.md **Цена:** бесплатно --- ## Описание Expert project manager for ADHD engineers managing multiple concurrent projects. Specializes in hyperfocus management, context-switching minimization, and parakeet-style gentle reminders. NOT for neurotypical PM. ## Архитектура **4 Core Principles:** 1. **Hyperfocus Management** — никогда не прерывать <6ч; gentle check-in в 6ч; firm interrupt в 10ч; 2-3ч recovery после
2. **Context Switching Minimization** — ADHD tax: 30-45 мин потеря на переключение. Batch meetings Tue/Thu only. Max 2 переключения/день
3. **Parakeet Reminders** — progressive urgency (1wk FYI → 3-7d Upcoming → 1-3d Soon → 24h Urgent → 4h CRITICAL)
4. **Task Chunking** — задачи <1ч с видимым прогрессом; group in 3-hour hyperfocus sessions max **Urgency Levels:**
| Time Left | Tone |
|---|---|
| 1+ week | "Just keeping it on your radar" |
| 1-3 days | "Would you like to time-box this?" |
| Under 4 hours | "Dropping everything to help you" | ## Ключевые фичи **Anti-patterns описаны явно:**
- Just-Focus-Harder Management = запрещено
- Meeting Sprawl = запрещено (каждая встреча = 30-45 мин потеря)
- Deadline Dump = запрещено
- Shame-Based Accountability = запрещено **Интеграции (Suspicious — не реализованы в пакете):**
- send_slack_dm, schedule_task, GitHub webhooks, calendar API — заявлены но credentials не декларированы ## Флаги безопасности (SUSPICIOUS) - Unicode control characters в SKILL.md — потенциальный prompt-injection вектор
- Функции (send_slack_dm/schedule_task/prompt_user) заявлены без credentials declaration
- Suspicious medium confidence — инспекция raw файла рекомендована до установки ## Ограничения - Только для ADHD-инженеров — не для строительных прорабов
- Нет строительной специфики (наряды, субподрядчики, стройплощадка)
- Нет русского языка
- Suspicious статус — рекомендовано тестирование в sandbox
- Интеграции (Slack/GitHub) требуют отдельной настройки и credentials
- Методология не адаптирована под физические работы (земляные/монолит/отделка)
