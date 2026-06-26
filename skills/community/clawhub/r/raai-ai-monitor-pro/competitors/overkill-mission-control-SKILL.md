# overkill-mission-control — ClawHub SKILL.md (скачано с clawhub.ai) **Источник:** https://clawhub.ai/broedkrummen/overkill-mission-control **Автор:** @broedkrummen **Версия:** v1.0.1 **Загрузок:** 370 | **Звёзды:** 0 **Статус безопасности:** Suspicious (high confidence) — создаёт systemd сервисы, требует sudo/root, хардкодит пути **Цена:** бесплатно --- ## Описание Enterprise-grade operations dashboard for OpenClaw autonomous agents. Real-time monitoring, agent-to-agent messaging, task execution, automation workflows, SLO tracking. ## Архитектура **Stack:** Node.js 22+ / Next.js 16 / SQLite (better-sqlite3) / Tailwind CSS / Tailscale **Pages (17 штук):**
- `/` — Main dashboard (live metrics: sessions, agents, CPU/memory/disk, health score)
- `/tasks` — Task queue and management
- `/workshop` — Agent workshop with Kanban
- `/teams` — Team management
- `/messages` — Agent-to-agent messaging (LLM: MiniMax M2.5)
- `/documents` — Document storage + FTS5 search
- `/automation` — Automation workflows (visual builder)
- `/alerts` — Alert management
- `/slo` — SLO/Error budget tracking
- `/runbooks` — Runbook automation
- `/feature-flags`, `/environments`, `/webhooks`, `/stats`, `/settings` **Databases:**
- `/mnt/openclaw/state/messages.db` — messaging
- `/mnt/openclaw/state/documents.db` — documents **API Endpoints:** /api/status / /api/mission-control/agents / /api/messages / /api/automation / /api/alerts / /api/slo / /api/runbooks ## Ключевые фичи **Real-time Dashboard:**
- Live session count, active agents, resource utilization
- System health score + task distribution timeline **Agent-to-Agent Messaging:**
- LLM-powered responses via MiniMax M2.5
- Polling каждые 60 секунд
- Task types: researcher/seo/contentwriter/data-analyst/designer/orchestrator **Automation Workflows:**
- Triggers: schedule / webhook / event / manual / condition
- Actions: message / HTTP / task / notify / condition **SLO + Error Budget Tracking:** встроенный трекер SLO ## Флаги безопасности (SUSPICIOUS) - Создаёт systemd сервисы (`/etc/systemd/system/mission-control.service`) с `User=broedkrummen` — хардкоженный username
- `tailscale-serve.service` запускается от `User=root` с sudo
- Hardcoded paths: `/mnt/openclaw/state/`, `/home/broedkrummen/.openclaw/`
- Заявленные metadata ≠ реальные требования (нет деклараций Node.js/npm/Tailscale в registry) ## Установка ```bash
cd ~/.openclaw/workspace-mission-control
npm run dev
# Доступ: http://localhost:3000
# Через Tailscale: https://<host>.taila0448b.ts.net
``` ## Ограничения - **Suspicious** — не рекомендуется для prod без полного ревью
- Требует Node.js 22+ + npm + Tailscale + SQLite
- Хардкоженный username и пути — не generic
- Нет поддержки строительных объектов и российской специфики
- Только для мониторинга AI-агентов OpenClaw (не бизнес-процессов)
