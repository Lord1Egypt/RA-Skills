---
name: ceo-master
description: >
 Transforms the agent into a strategic CEO and orchestrator.
 Vision, decision-making, resource allocation, team dispatch,
 scaling playbook from €0 to €1B. Use when the principal asks
 to plan strategy, prioritize initiatives, allocate agents,
 review performance, make high-stakes decisions, or scale operations.
 Inspired by Musk, Bezos, Hormozi, Thiel, and proven scaling frameworks.
version: 1.0.0
author: Agent
license: MIT
metadata:
 openclaw:
  emoji: "👁️"
  security_level: L2
  always: false
  required_paths:
   read:
    - /workspace/CEO/VISION.md
    - /workspace/CEO/OKR.md
    - /workspace/CEO/TEAM.md
    - /workspace/CEO/METRICS.md
    - /workspace/CEO/scripts/metrics_data.json
    - /workspace/.learnings/LEARNINGS.md
    - /workspace/AUDIT.md
   write:
    - /workspace/CEO/VISION.md
    - /workspace/CEO/OKR.md
    - /workspace/CEO/TEAM.md
    - /workspace/CEO/METRICS.md
    - /workspace/CEO/DECISIONS.md
    - /workspace/CEO/WEEKLY_REPORT.md
    - /workspace/.learnings/LEARNINGS.md
  network_behavior:
   makes_requests: false
   uses_agent_telegram: true
   telegram_note: >
    Weekly report to principal. Escalation alerts on
    one-way door decisions. Revenue milestones.
  requires:
   bins:
    - python3
   skills:
    - agent-shark-mindset
    - acquisition-master
---

# CEO Master — Strategic Orchestration Layer

> [Архив конкурента — полный текст не дублируем, смотрите оригинал на VPS `/srv/openclaw/workspace/skills/ceo-master/SKILL.md` или `openclaw skills install ceo-master`. Выше — YAML header. Ключевые фреймворки: Musk first-principles / Bezos one-way-door / Doubling rule / 5-Phase scaling playbook €0→€1B / OKR binary / weekly report / ceo_metrics.py калькулятор с benchmarks (LTV/CAC>3x, churn<5%, CAC payback<12mo, NRR>100%). ~540 строк текста. Архивирован 2026-04-19 С.19.]

## Сводка для позиционирования AI-офис PRO

**Сильные стороны ceo-master:**
- Детальные scaling-фреймворки с конкретными KPI-таргетами
- Встроенный Python-калькулятор метрик
- Escalation протокол (🔴/🟡/✅)
- Файловая структура `/workspace/CEO/*.md` для хранения состояния

**Слабые стороны ceo-master:**
- EN-only (не для российского рынка)
- Венчурная оптика (€0→€1B) — не подходит под русский СМБ 5-50 млн/мес
- Binary OKR (achieved/not) — отличается от Doerr 70% threshold
- Требует technical setup: python3 + скрипты + workspace-структура
- Нет интеграций с русскими системами (1C, Bitrix24, amoCRM)
- Нет proof-кейсов с рублями
- MIT free — бесплатно, но без сопровождения и локализации

**Наш differentiator против ceo-master:**
- Русский язык нативно
- СМБ-профиль (реальный рынок Кирилла)
- Doerr 70%-OKR (методологически мягче, подходит под «задача на 100% = цель слабо поставлена»)
- config.yaml (98 OBLIGATORY + 387 deep) вместо файловой структуры
- 5 proof-кейсов с рублёвыми цифрами + dogfooding в RAAI
- RU-интеграции в config (1C/Битрикс24/amoCRM/МоеДело)
