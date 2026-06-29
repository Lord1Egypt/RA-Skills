# Research Mode Roadmap

[English](#english) | [Русский](#русский)

## English

Research Mode is an OpenClaw-first skill for durable, review-gated background
research. It is not a standalone Python package yet. The roadmap below describes
the public direction of the GitHub repository and avoids private workspace,
operator, or task-specific context.

### Completed in v0.3.0

- Added public repository onboarding: `ROADMAP.md`, `CONTRIBUTING.md`, issue
  templates, support/security docs, and release-boundary checks.
- Documented public contracts: stable/internal CLI surface, JSON schemas,
  `state_version`, migration policy, and architecture decision context.
- Hardened public/package-facing path surfaces so generated summaries avoid
  leaking unnecessary host layout details while local diagnostics stay useful.
- Added read-only `health` diagnostics and `reconcile` as a read-only alias for
  state, artifacts, runtime, delivery, and recovery status.
- Improved partial-failure recovery so operators can distinguish `ok`,
  `repair_needed`, `manual_review_needed`, `blocked`, and
  `fresh_continuation_recommended`.

### Completed in v0.4.0

- Added the default preflight gate for new tasks, including
  `research-preflight.md`, `--skip-preflight`, visible preflight state in
  operator surfaces, and skill-local `RULES.md` support through
  `RULES.example.md`.
- Added `operator_attention` to `summary --format json` so monitors can
  identify stale active runs and follow a clear recovery action.

### Completed in v0.5.0

- Added the initial stability diagnostics line: reliability counters,
  repeated completion-validation loop detection, structural comparative
  validation, delivery handoff/channel diagnostics, default deliverable format
  decisions, queue mismatch findings, and deterministic reliability soak
  coverage.
- Added structured output artifact contracts with explicit
  `output_contract.outputs[]`, candidate artifact ids, `delivery.outputs`, and
  provenance relations instead of relying on a single primary deliverable kind.
- Deprecated legacy single-output fields for new tasks while preserving
  compatibility for older states.
- Updated public status messaging to make research stability, observability,
  and recovery the current project priority.

### Now

- Continue hardening research stability as the primary release gate. The first
  diagnostics line is in place; remaining work should focus on phase
  progression, repeated low-yield turns, and recovery flows that are safe enough
  to automate.
- Improve lifecycle phase progression so tasks do not keep searching after they
  have repeatedly signaled that synthesis or finalization is the right next
  step. Surface stalled transitions in `summary`, `status`, and `health`, and
  add bounded auto-advance where it is safe.
- Make task-local package installation more governed without making ordinary
  research tasks painful: audit trails, optional strict policy, and reproducible
  package snapshots where useful.
- Add a refine/pivot ladder for repeated low-yield iterations so long-running
  tasks change strategy instead of repeating weak searches.
- Persist reusable research lessons across similar tasks when that can be done
  transparently and safely.

### Next

- Add versioned deliverable profiles for repeated output shapes such as briefs,
  source matrices, reports, and implementation plans.

### Later

- Improve portability beyond the current Linux/OpenClaw-first baseline,
  especially Windows compatibility: isolate POSIX-specific locking such as
  `fcntl`, evaluate Windows-friendly file locking, and define a cross-platform
  state strategy.
- Revisit larger-scale storage if traces become too large for simple task-local
  files, with a migration path toward SQLite or PostgreSQL-backed views.
- Consider a `pyproject.toml` and CLI entrypoint only if it improves maintainer
  ergonomics without implying that Research Mode is a standalone product.

### Not planned

- A hosted research service.
- A generic agent framework.
- A replacement for OpenClaw cron, skill loading, or messaging adapters.
- Publishing private task roots, corpora, generated reports, chat identifiers,
  webhooks, owner-specific configuration, or local workspace paths.

## Русский

Research Mode — OpenClaw-first skill для длительных фоновых исследований с
ревью перед выдачей результата. Это пока не самостоятельный Python package.
Roadmap ниже описывает публичное направление GitHub-репозитория и не включает
приватный workspace-контекст, операторские заметки или детали конкретных задач.

### Выполнено в v0.3.0

- Добавлен публичный onboarding репозитория: `ROADMAP.md`, `CONTRIBUTING.md`,
  issue templates, support/security docs и проверки release boundary.
- Описаны публичные контракты: stable/internal CLI surface, JSON schemas,
  `state_version`, migration policy и архитектурные решения.
- Усилены public/package-facing path surfaces: generated summaries не должны
  раскрывать лишние детали host layout, но локальная диагностика остается
  полезной.
- Добавлена read-only диагностика `health` и read-only alias `reconcile` для
  state, artifacts, runtime, delivery и recovery status.
- Улучшено восстановление после частичных сбоев: оператор видит `ok`,
  `repair_needed`, `manual_review_needed`, `blocked` и
  `fresh_continuation_recommended`.

### Выполнено в v0.4.0

- Добавлен preflight gate по умолчанию для новых задач: `research-preflight.md`,
  `--skip-preflight`, видимое состояние preflight в операторских представлениях
  и skill-local `RULES.md` через публичный шаблон `RULES.example.md`.
- В `summary --format json` добавлен `operator_attention`, чтобы наблюдатели
  могли видеть stale active run и понятное действие для восстановления.

### Выполнено в v0.5.0

- Добавлена начальная линия stability diagnostics: reliability counters,
  detection повторяющихся completion-validation loops, структурная проверка
  сравнительных результатов, delivery handoff/channel diagnostics,
  contract-driven deliverable format decisions, queue mismatch findings и deterministic
  reliability soak coverage.
- Добавлены structured output artifact contracts с явными
  `output_contract.outputs[]`, id candidate artifacts, `delivery.outputs` и
  provenance-связями вместо зависимости от одного primary deliverable kind.
- Legacy single-output поля помечены как deprecated для новых задач, но
  совместимость со старыми states сохранена.
- Публичный статус проекта уточнён: текущий приоритет — стабильность,
  наблюдаемость и восстановимость исследований.

### Сейчас

- Продолжать делать стабильность исследований главным release gate. Первая
  линия диагностики уже есть; следующий фокус — progression между фазами,
  повторяющиеся low-yield итерации и recovery flows, которые достаточно
  безопасны для автоматизации.
- Улучшить progression между фазами, чтобы задачи не продолжали поиск после
  повторяющихся сигналов, что следующий правильный шаг — synthesis или
  finalization. Stalled transitions должны быть видны в `summary`, `status` и
  `health`; для безопасных случаев нужен bounded auto-advance.
- Сделать установку task-local packages управляемее без лишней бюрократии для
  обычных исследований: audit trail, optional strict policy и воспроизводимые
  package snapshots там, где это полезно.
- Добавить refine/pivot ladder для серий слабых итераций, чтобы долгие задачи
  меняли стратегию, а не повторяли неудачный поиск.
- Переиспользовать уроки между похожими исследованиями, если это можно сделать
  прозрачно и безопасно.

### Дальше

- Добавить версионированные deliverable profiles для повторяемых форматов:
  briefs, source matrices, reports и implementation plans.

### Позже

- Улучшить portability за пределами текущего Linux/OpenClaw-first baseline,
  особенно Windows compatibility: изолировать POSIX-specific locking вроде
  `fcntl`, изучить Windows-friendly file locking и определить cross-platform
  strategy для состояния.
- Вернуться к storage scaling, если traces станут слишком большими для простых
  task-local files, с возможным migration path к SQLite или PostgreSQL-backed
  представлениям.
- Подумать о `pyproject.toml` и CLI entrypoint только если это реально улучшит
  сопровождение и не создаст впечатление standalone-продукта.

### Не планируется

- Hosted research service.
- Универсальный agent framework.
- Замена OpenClaw cron, skill loading или messaging adapters.
- Публикация приватных task roots, corpora, generated reports, chat identifiers,
  webhooks, owner-specific configuration или локальных workspace paths.
