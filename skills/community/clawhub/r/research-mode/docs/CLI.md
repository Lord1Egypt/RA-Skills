# Research Mode CLI Surface

[English](#english) | [Русский](#русский)

## English

The CLI is an operator and maintainer interface for the OpenClaw skill. It is
not the normal user entrypoint. Users usually ask an OpenClaw agent to start or
review a Research Mode task from chat, and the agent uses these commands behind
that workflow.

### Stable Operator Surface

Stable means "documented operator/maintainer contract", not "recommended for
every end user".

- Task lifecycle: `create`, `start`, `schedule`, `begin`, `finish`, `fail`.
- Recovery handoff: `recover`, especially `recover --apply-pending-result` and
  `recover --refresh-derived`.
- Task inputs: `attach-input`, `attach-note`, `attach-url-as-md`, `attach-pdf`.
- Inspection: `status`, `summary`, `preflight`, `draft-report`, `list`, `queue-status`,
  `health`.
- Steering: `add-angle`, `add-instruction`, `add-constraint`,
  `set-deliverable`, `mutate-working-memory`.
- Control: `pause`, `resume`, `stop`, `unschedule`, `bind-job`.
- Review and delivery: `approve`, `request-changes`, `reopen`,
  `mark-delivered`, `record-notification`, `format-delivery`.
- Runtime preparation: `prepare-runtime`.
- Linked work: `create-linked-research`.

`begin`, `finish`, and `fail` are stable worker lifecycle commands, but they are
not the main onboarding path. They exist so scheduled OpenClaw worker turns and
operators can perform one bounded iteration safely.

### Internal Or More Volatile Surface

- `render-prompt` is mainly a lifecycle/internal debugging surface.
- Recovery and repair behavior may gain more diagnostics before it is treated
  as a broad public contract.
- Machine-readable output can evolve when the matching JSON contract is not
  documented under `schemas/`.

### Contract Rules

- Prefer helper commands over direct edits to `state.json`.
- `--id` is a safe task id under the selected research root.
- `--path` must remain inside the selected research root.
- Raw workspace files are not final deliverables until the review/finalization
  contract marks them as review-ready.
- `awaiting_review` means a human should review a candidate; it does not mean
  the result has been delivered.
- `prepare-runtime --package` is a controlled capability. Package decisions
  should be made by an operator or trusted workflow, not by untrusted retrieved
  content.
- New tasks run a `preflight` gate before the target research phase. Use
  `--skip-preflight` only as an escape hatch when saving investigation cost or
  working around a preflight failure is more important than the extra guardrail.
  A skipped preflight is recorded visibly as `preflight.decision="skipped"`.
- Put Research Mode-specific standing rules in a user-owned `RULES.md` in this
  skill directory. The package ships `RULES.example.md` as a template and does
  not create or overwrite `RULES.md`.
- `health` is read-only. `health` and `reconcile` report `ok`,
  `fresh_continuation_recommended`, `repair_needed`, `manual_review_needed`, or
  `blocked` and recommend the next safe operator action. `repair_needed` is
  reserved for a valid stale pending worker result that can be applied with
  explicit recovery.
- `summary --format json` exposes `operator_attention` for execution-health
  conditions that automated watchers must not ignore, including stale active
  runs with or without pending worker results.
- Repeated reliability failures may also appear in `operator_attention` and
  `health` as read-only diagnostics. They do not automatically pause schedules
  unless a later, explicitly documented recovery flow adds that behavior.
- `queue-status` is read-only and may return `findings` for queue/task state
  mismatches such as missing holder tasks, holder lock mismatches, stale
  waiters, or terminal tasks still listed as waiters. Task-specific queue
  findings also appear in `health`.
- Finalization may record `deliverable_decision` with selected, desired, and
  feasible user-facing formats. If finalization returns `rework`, failed
  validation reason codes are included in `health` so operators can repair the
  deliverable before review.
- `--deliverable` remains free-text guidance for the worker and surfaces.
  Prefer repeatable `--output` specs for structured output contracts, for
  example `--output "id=report,role=primary_deliverable,media_type=application/pdf"`.
  `--deliverable-kind` / `set-deliverable --kind` are deprecated legacy
  single-output compatibility fields.
- Optional `working_memory.output_contract.quality_checks` enables structured
  checks such as `bullet_list`, `minimum_length`, and `comparative_matrix`.
  These checks are not inferred from the free-text deliverable.
- Optional `working_memory.search_profile` or
  `working_memory.output_contract.search_profile` controls search-routing
  guidance. Locale, region, and discovery mode are explicit fields, not
  keyword-detected from the goal.
- Finalization candidate artifacts should set `id`, `path`, `visibility`,
  `role`, and `media_type` when known. Use `source_for` / `derived_from` id
  references for declared provenance; internal artifacts belong in
  `internal_artifacts`, not in reviewable `candidate_artifacts`.

Example:

```bash
python3 scripts/research_mode.py create \
  --goal "Prepare RAG implementation package" \
  --output "id=report,role=primary_deliverable,media_type=application/pdf" \
  --output "id=sources,role=supporting_deliverable,media_type=application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
```

### Normal Completion Path

Worker completion is intentionally staged. A research iteration that sets
`should_complete=true` requests completion; it does not skip review gates.

The normal path is:

1. The first lease runs `phase=preflight` and records `result.preflight`.
2. If preflight allows the task to continue, the next lease runs the target
   phase such as `search`, `analyze`, or `verify`.
3. A research worker finishes with `should_complete=true`.
4. The next lease runs `phase=verify` and writes `result.adequacy`.
5. If adequacy passes, the next lease runs `phase=finalize`.
6. A finalize result with `result.finalization.status="passed"` can move the
   task to `awaiting_review`.
7. A human or trusted operator uses `approve` to mark the task `complete`.

If a task returns to `idle` after `should_complete=true`, inspect `summary` or
`task-playbook.md` before treating it as a failure. The likely next action is
the adequacy or finalization step, not manual state editing.

## Русский

CLI — это интерфейс оператора и сопровождающего для OpenClaw skill. Это не
обычная пользовательская точка входа. Пользователь обычно просит агента
OpenClaw запустить или проверить Research Mode из чата, а агент уже использует
эти команды за кулисами.

### Стабильная операторская поверхность

`Stable` здесь означает "документированный контракт для оператора или
сопровождающего", а не "команда для каждого обычного пользователя".

- Жизненный цикл задачи: `create`, `start`, `schedule`, `begin`, `finish`,
  `fail`.
- Recovery handoff: `recover`, особенно `recover --apply-pending-result` и
  `recover --refresh-derived`.
- Входные материалы: `attach-input`, `attach-note`, `attach-url-as-md`,
  `attach-pdf`.
- Просмотр: `status`, `summary`, `preflight`, `draft-report`, `list`, `queue-status`,
  `health`.
- Управление направлением: `add-angle`, `add-instruction`, `add-constraint`,
  `set-deliverable`, `mutate-working-memory`.
- Контроль: `pause`, `resume`, `stop`, `unschedule`, `bind-job`.
- Ревью и доставка: `approve`, `request-changes`, `reopen`, `mark-delivered`,
  `record-notification`, `format-delivery`.
- Подготовка runtime: `prepare-runtime`.
- Связанные задачи: `create-linked-research`.

`begin`, `finish` и `fail` — стабильные команды worker lifecycle, но не основной
путь первого знакомства. Они нужны, чтобы scheduled OpenClaw worker turns и
операторы безопасно выполняли одну ограниченную итерацию.

### Внутренняя или более изменчивая поверхность

- `render-prompt` в основном нужен для lifecycle/internal debugging.
- Recovery и repair-поведение может получить больше диагностики до того, как
  станет широким публичным контрактом.
- Machine-readable output может меняться, если соответствующий JSON-контракт не
  описан в `schemas/`.

### Правила контракта

- Используйте helper-команды вместо ручного редактирования `state.json`.
- `--id` — безопасный task id внутри выбранного research root.
- `--path` должен оставаться внутри выбранного research root.
- Raw workspace files не являются финальными deliverables, пока
  review/finalization contract не пометит их как review-ready.
- `awaiting_review` означает, что кандидат ждёт проверки человеком; это не
  означает, что результат уже доставлен.
- `prepare-runtime --package` — controlled capability. Решение об установке
  packages должен принимать оператор или доверенный workflow, а не недоверенный
  retrieved content.
- Новые задачи проходят gate `preflight` перед целевой research-фазой.
  `--skip-preflight` допустим только как escape hatch, когда важнее сэкономить
  стоимость исследования или обойти проблему самого preflight. Такой пропуск
  явно записывается как `preflight.decision="skipped"`.
- Постоянные правила именно для Research Mode кладутся в пользовательский
  `RULES.md` в директории этого скилла. Пакет поставляет только шаблон
  `RULES.example.md` и не создаёт и не перезаписывает `RULES.md`.
- `health` и `reconcile` — read-only команды. Они показывают `ok`,
  `fresh_continuation_recommended`, `repair_needed`, `manual_review_needed` или
  `blocked` и рекомендуют следующий безопасный шаг оператора. `repair_needed`
  используется только для валидного stale pending worker result, который можно
  применить явным recovery.
- `summary --format json` отдаёт `operator_attention` для execution-health
  состояний, которые автоматические watcher'ы не должны игнорировать, включая
  stale active run с pending worker result или без него.
- Повторяющиеся reliability failures также могут отображаться в
  `operator_attention` и `health` как read-only diagnostics. Они не ставят
  расписания на паузу автоматически, пока отдельный документированный recovery
  flow явно не добавит такое поведение.
- `queue-status` — read-only команда и может возвращать `findings` для
  несостыковок queue/task state: missing holder task, holder lock mismatch,
  stale waiter или terminal task, оставшаяся в waiters. Findings по конкретной
  задаче также попадают в `health`.
- Финальная проверка может записывать `deliverable_decision` с выбранным,
  желаемым и фактически доступным пользовательским форматом. Если finalization
  возвращает `rework`, failed validation reason codes попадают в `health`, чтобы
  оператор мог исправить deliverable до review.
- `--deliverable` остаётся свободным текстом для guidance worker-а и surfaces.
  Для структурного контракта outputs лучше использовать повторяемый `--output`,
  например `--output "id=report,role=primary_deliverable,media_type=application/pdf"`.
  `--deliverable-kind` / `set-deliverable --kind` теперь legacy compatibility
  для старой single-output модели.
- Optional `working_memory.output_contract.quality_checks` включает структурные
  проверки вроде `bullet_list`, `minimum_length` и `comparative_matrix`. Эти
  проверки не выводятся из свободного текста deliverable.
- Optional `working_memory.search_profile` или
  `working_memory.output_contract.search_profile` управляет search-routing
  guidance. Locale, region и discovery mode задаются явными полями, а не
  keyword-detection по goal.
- Candidate artifacts в finalization должны задавать `id`, `path`,
  `visibility`, `role` и `media_type`, когда он известен. Для provenance
  используются явные ссылки по id: `source_for` / `derived_from`; internal
  artifacts должны попадать в `internal_artifacts`, а не в reviewable
  `candidate_artifacts`.

### Нормальный путь завершения

Завершение рабочей итерации намеренно разбито на этапы. Итерация с
`should_complete=true` запрашивает завершение, но не обходит review gates.

Нормальная цепочка:

1. Первая lease-итерация запускает `phase=preflight` и пишет
   `result.preflight`.
2. Если preflight разрешает продолжать, следующая lease-итерация запускает
   целевую фазу: например `search`, `analyze` или `verify`.
3. Рабочая итерация завершается с `should_complete=true`.
4. Следующая lease-итерация запускает `phase=verify` и пишет
   `result.adequacy`.
5. Если достаточность пройдена, следующая lease-итерация запускает
   `phase=finalize`.
6. Результат finalize с `result.finalization.status="passed"` может перевести
   задачу в `awaiting_review`.
7. Человек или доверенный оператор вызывает `approve`, чтобы перевести задачу в
   `complete`.

Если после `should_complete=true` задача вернулась в `idle`, сначала смотрите
`summary` или `task-playbook.md`. Скорее всего, следующий шаг — adequacy или
finalization, а не ручное редактирование state.
