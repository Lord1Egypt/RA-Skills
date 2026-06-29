# Research Mode Architecture

[English](#english) | [Русский](#русский)

`research-mode` is a durable research control plane for OpenClaw. It turns a
large research goal into bounded worker iterations, keeps task state and
artifacts on disk, and blocks user-facing delivery until a reviewable final
candidate exists.

It is better than simpler alternatives for long-running, evidence-heavy work
because it combines scheduled continuation, local auditability, explicit review
gates, and finalization checks. It is distributed as an OpenClaw skill package,
not as a standalone Python daemon. It is not meant to replace one-shot chat,
interactive notebooks, or custom domain pipelines when those are enough.

## English

## System Overview

Research Mode has three layers:

- **OpenClaw execution layer** schedules isolated worker turns through cron.
- **Research Mode control plane** owns task state transitions and validation.
- **Task workspace** stores sources, findings, iteration notes, runtime outputs,
  candidate deliverables, and final reports.

```mermaid
flowchart LR
    User[User or operator] --> CLI[Research Mode CLI]
    CLI --> State[state.json]
    CLI --> Artifacts[Task artifacts]
    CLI --> Cron[OpenClaw cron]
    Cron --> Worker[Isolated worker turn]
    Worker --> CLI
    Worker --> Corpus[Sources and findings]
    Worker --> Workspace[Task-local workspace]
    CLI --> Review[Review gate]
    Review --> Delivery[Approved delivery]
```

The helper scripts are deterministic state-management tools. The autonomous
research behavior comes from OpenClaw workers using those tools repeatedly on a
schedule.

## Core Components

```mermaid
flowchart TB
    RM[research_mode.py] --> Lifecycle[Lifecycle commands]
    RM --> Control[Operator control commands]
    RM --> Surfaces[Operator surfaces]
    RM --> Runtime[Task-local runtime]
    RM --> Corpus[Corpus helpers]

    Lifecycle --> Create[create / start / schedule]
    Lifecycle --> Iterate[begin / finish / fail]
    Lifecycle --> Finalize[finalization validation]

    Control --> Pause[pause / resume / stop]
    Control --> Review[approve / request-changes / reopen]
    Control --> Delivery[format-delivery / mark-delivered]

    Surfaces --> Summary[summary / status]
    Surfaces --> Reports[draft-report / task-playbook.md / runs.tsv]

    Runtime --> Workspace[workspace/]
    Runtime --> SQLite[optional SQLite]
    Runtime --> Packages[task-local packages]

    Corpus --> Inputs[attached files, notes, URLs, PDFs]
```

Main files:

- `research_mode.py` — CLI entrypoint and command routing.
- `research_mode_lifecycle_commands.py` — `begin`, `finish`, `fail`, and
  lifecycle state transitions.
- `research_mode_payloads.py` — task and worker result payload contracts.
- `research_mode_finalization.py` — finalization surface and operator next
  action calculation.
- `research_mode_reliability.py` — bounded reliability counters, failure
  fingerprints, and operator-attention merge helpers.
- `research_mode_queue.py` / `research_mode_health.py` — root-global queue
  state and read-only health diagnostics.
- `research_mode_surfaces.py` / `research_mode_reporting.py` — human-readable
  and JSON operator views.
- `research_mode_runtime.py` — OpenClaw cron integration and task-local runtime
  preparation.
- `research_mode_task.py` — task paths, state files, append-only run artifacts.

## Data Model

Each task is a directory under a selected research root.

```text
research/
  demo-task/
    state.json
    sources.jsonl
    findings.jsonl
    runs.tsv
    final-report.md
    task-playbook.md
    iterations/
    workspace/
      analysis/
      tools/
      data/
      outputs/
```

`state.json` is the control plane. It records task status, working memory,
current lock, cron binding, research adequacy state, finalization state, review
state, delivery state, and transition history.

Append-only files such as `sources.jsonl`, `findings.jsonl`, and iteration
notes preserve a reviewable trail. The task-local `workspace/` is available for
scripts, SQLite, temporary analysis, screenshots, exports, and derived outputs.

## Lifecycle

```mermaid
stateDiagram-v2
    [*] --> idle: create
    idle --> running: begin lease
    running --> idle: finish, continue
    running --> idle: finish, verify needs more work
    running --> idle: finish, adequacy passed and phase=finalize
    running --> finalize: finish, completion requested but finalization failed
    finalize --> running: begin rework
    running --> awaiting_review: finish with passed finalization
    awaiting_review --> idle: request-changes or reopen
    awaiting_review --> complete: approve or mark-delivered
    idle --> paused: pause
    paused --> idle: resume
    idle --> cancelled: stop
    running --> failed: fail or error threshold
    complete --> [*]
    cancelled --> [*]
    failed --> [*]
```

A worker iteration is intentionally bounded:

1. `begin` acquires a lease and returns a work order.
2. The worker performs one focused research step.
3. The worker writes a result JSON file.
4. `finish` validates and commits the state transition.
5. `fail` records errors when a leased iteration breaks.

`begin` also participates in a root-global iteration queue. The queue serializes
worker execution across tasks under the same research root, while still allowing
multiple background tasks to be scheduled. If another task is already running,
`begin` returns a deferred/skipped result and records waiter diagnostics instead
of treating the cron tick as a failure.

This prevents one long assistant session from becoming the only source of truth.

## Research Adequacy Gate

```mermaid
flowchart TD
    WorkerResult[Worker result JSON] --> WantsComplete{completion requested?}
    WantsComplete -- no --> Continue[idle / continue research]
    WantsComplete -- yes --> Adequacy[result.adequacy]
    Adequacy --> Check[research adequacy validation]
    Check --> Passed{adequacy passed?}
    Passed -- no, needs sources --> Search[search]
    Passed -- no, needs analysis --> Analyze[analyze]
    Passed -- no, needs synthesis --> Synthesize[synthesize]
    Passed -- needs user/operator --> Blocked[idle with operator_next_action]
    Passed -- yes --> Finalize[finalize]
```

The adequacy gate answers whether the research itself is sufficient before the
system spends effort packaging a final deliverable. It evaluates goal alignment,
explicit constraints, requested deliverable shape, open questions, source
diversity, evidence gaps, and contradictions.

Worker-provided `result.adequacy` is treated as a candidate assessment. Control
code owns attempt counters, routing, and `operator_next_action`. This keeps the
trust boundary clear: workers can report gaps, but lifecycle code decides
whether the task returns to `search`, `analyze`, `synthesize`, or moves to
`finalize`.

## Finalization and Review Gate

```mermaid
flowchart TD
    WorkerResult[Worker result JSON] --> WantsComplete{should_complete?}
    WantsComplete -- no --> Continue[idle / continue research]
    WantsComplete -- yes --> Adequacy{adequacy passed?}
    Adequacy -- no --> Verify[verify / research rework]
    Adequacy -- yes --> Trace[result.finalization]
    Trace --> Validate[Finalization validation]
    Validate --> Passed{passed?}
    Passed -- no --> Rework[finalize / worker rework]
    Passed -- repeated failures --> Intervention[operator intervention]
    Passed -- yes --> Review[awaiting_review]
    Review --> Approve[approve]
    Review --> Changes[request-changes]
    Approve --> Complete[complete / delivery-ready]
    Changes --> Continue
```

Worker-initiated completion requires a passed research adequacy assessment,
`result.finalization.status="passed"`, non-empty validation evidence, no
blocking defects, and inspectable candidate artifacts. `awaiting_review` means a
candidate is ready for human review. It does not mean the result was already
delivered.

The operator-facing finalization surface exposes `operator_next_action`:

- `review_candidate`
- `worker_rework`
- `operator_intervention`
- `verify_review_state`
- `continue_research`

This makes the next action explicit instead of requiring the operator to infer
intent from raw JSON.

Structured outputs live in `working_memory.output_contract.outputs[]`. Each
output uses an open `id`, a small system `role`, optional open `media_type`, and
optional `source_for` / `derived_from` id references. Produced files appear in
`finalization.candidate_artifacts` and `delivery.outputs` with explicit paths.
Validation matches declared contract to declared artifacts and checks task-local
path/readability/non-empty shape; it does not infer file type, role, or
provenance from filename, extension, MIME string, title, note, or list order.

Finalization records `output_decision` for structured output contracts.
`deliverable_decision`, `working_memory.output_contract.kind`, and
`finalization.primary_deliverable_kind` are legacy single-output compatibility
fields. Free-text `--deliverable`, channel context, titles, summaries, and notes
do not choose output format or provenance.

## Reliability Diagnostics

```mermaid
flowchart TD
    Lifecycle[Lifecycle validation] --> Reliability[state.reliability]
    Delivery[Delivery and queue checks] --> Health[health]
    Finalization[Finalization findings] --> Health
    Queue[queue-status findings] --> Health
    Reliability --> Summary[summary operator_attention]
    Reliability --> Health
    Health --> Operator[Operator action]
```

Reliability diagnostics are deliberately read-only unless an existing lifecycle
command applies an explicit recovery. They normalize observed failure classes
such as repeated completion-validation rejections, delivery artifact handoff
mismatches, delivery channel addressing failures, queue holder/waiter
mismatches, and finalization rework reasons. The goal is to make the next safe
operator action visible without silently pausing schedules or editing state.

## OpenClaw Cron Integration

```mermaid
sequenceDiagram
    participant Operator
    participant CLI as Research Mode CLI
    participant Cron as OpenClaw cron
    participant Worker
    participant State as state.json

    Operator->>CLI: start or schedule
    CLI->>State: create task and cron binding
    CLI->>Cron: register recurring isolated turn
    Cron->>Worker: launch bounded worker turn
    Worker->>CLI: begin
    CLI->>State: acquire lease
    Worker->>State: write artifacts and result file
    Worker->>CLI: finish
    CLI->>State: validate and commit transition
    CLI->>Cron: suspend when awaiting_review
    Operator->>CLI: approve / request-changes / reopen
```

The project deliberately depends on OpenClaw cron for scheduling, isolation,
owner-channel updates, pause/resume/stop behavior, and review handoff. The
Python scripts can be run manually, but they are not a standalone scheduler.

## Why This Architecture Is Better For Durable Research

The important comparison is not "better at everything". Research Mode is better
for a specific class of tasks: long-running, evidence-heavy, revisable research
where losing state or delivering an unchecked draft is costly.

| Alternative category | Typical weakness | Research Mode advantage |
| --- | --- | --- |
| One-shot chat answer | Loses continuity and evidence trail after one response. | Persistent state, sources, findings, iteration notes, and resumable work. |
| Manual notebook workflow | Accurate but operator-heavy and easy to leave undocumented. | Structured task lifecycle plus task-local code/data workspace. |
| Generic scheduled prompt | Can repeat work without strong state contracts. | Lease-based `begin`/`finish`, normalized statuses, and committed transitions. |
| Autonomous agent loop | May run too long, drift, or deliver raw artifacts as final. | Bounded iterations, review gates, finalization trace, and artifact inspection. |
| Standalone scraper/RAG pipeline | Strong ingestion, weaker human review and delivery workflow. | Operator surfaces, review/rework loop, delivery formatting, and follow-up tasks. |

Research Mode is not always the right tool. Use simpler tools when the task is a
quick lookup, a one-turn summary, an ordinary coding change, or a tightly scoped
data pipeline that already has its own scheduler and review process.

## Design Principles

- **Durability over prompt length.** State lives on disk, not only inside a chat.
- **Bounded work over endless autonomy.** Each cron turn does one manageable
  iteration.
- **Explicit transitions over hand-edited JSON.** Helpers own state mutation.
- **Review before delivery.** `awaiting_review` is a gate, not a final state.
- **Inspectable artifacts.** Candidate deliverables must be task-local and
  structurally readable.
- **Operator clarity.** `summary`, `status`, `task-playbook.md`, and
  `operator_next_action` make the current situation visible.
- **OpenClaw-native scheduling.** Cron and isolated turns are part of the
  product model, not incidental implementation detail.

## Русский

## Обзор системы

Research Mode состоит из трёх слоёв:

- **Слой выполнения OpenClaw** запускает изолированные рабочие итерации через cron.
- **Управляющий слой Research Mode** управляет состоянием, переходами и проверками.
- **Рабочая область задачи** хранит источники, выводы, заметки итераций,
  выводы локального окружения, кандидатные материалы и финальные отчёты.

```mermaid
flowchart LR
    User[Пользователь или оператор] --> CLI[Research Mode CLI]
    CLI --> State[state.json]
    CLI --> Artifacts[Артефакты задачи]
    CLI --> Cron[OpenClaw cron]
    Cron --> Worker[Изолированная рабочая итерация]
    Worker --> CLI
    Worker --> Corpus[Источники и выводы]
    Worker --> Workspace[Рабочая область задачи]
    CLI --> Review[Проверка результата]
    Review --> Delivery[Утверждённая выдача]
```

Вспомогательные скрипты — это детерминированные инструменты управления
состоянием. Автономное исследовательское поведение появляется за счёт рабочих
итераций OpenClaw, которые используют эти инструменты по расписанию.

## Основные компоненты

```mermaid
flowchart TB
    RM[research_mode.py] --> Lifecycle[Команды жизненного цикла]
    RM --> Control[Команды управления]
    RM --> Surfaces[Поверхности оператора]
    RM --> Runtime[Локальное окружение задачи]
    RM --> Corpus[Помощники корпуса]

    Lifecycle --> Create[create / start / schedule]
    Lifecycle --> Iterate[begin / finish / fail]
    Lifecycle --> Finalize[Финальная проверка]

    Control --> Pause[pause / resume / stop]
    Control --> Review[approve / request-changes / reopen]
    Control --> Delivery[format-delivery / mark-delivered]

    Surfaces --> Summary[summary / status]
    Surfaces --> Reports[draft-report / task-playbook.md / runs.tsv]

    Runtime --> Workspace[workspace/]
    Runtime --> SQLite[Опциональный SQLite]
    Runtime --> Packages[Пакеты задачи]

    Corpus --> Inputs[attached files, notes, URLs, PDFs]
```

Главные файлы:

- `research_mode.py` — CLI-точка входа и маршрутизация команд.
- `research_mode_lifecycle_commands.py` — `begin`, `finish`, `fail` и переходы
  жизненного цикла.
- `research_mode_payloads.py` — контракты задачи и JSON-результата рабочей итерации.
- `research_mode_finalization.py` — поверхность финальной проверки и расчёт следующего
  действия оператора.
- `research_mode_reliability.py` — ограниченные counters, fingerprints сбоев и
  helpers для объединения operator attention.
- `research_mode_queue.py` / `research_mode_health.py` — состояние общей
  очереди на уровне root и read-only диагностика health.
- `research_mode_surfaces.py` / `research_mode_reporting.py` — представления для оператора в
  JSON и человекочитаемом виде.
- `research_mode_runtime.py` — интеграция с OpenClaw cron и локальное окружение задачи.
- `research_mode_task.py` — пути задач, файлы состояния и append-only артефакты запусков.

## Модель данных

Каждая задача — директория внутри выбранного корня исследований.

```text
research/
  demo-task/
    state.json
    sources.jsonl
    findings.jsonl
    runs.tsv
    final-report.md
    task-playbook.md
    iterations/
    workspace/
      analysis/
      tools/
      data/
      outputs/
```

`state.json` — управляющий файл задачи. Там хранятся статус задачи, рабочая
память, активная блокировка, привязка к cron, состояние проверки достаточности
исследования, состояние финальной проверки, состояние ревью, состояние выдачи и
история переходов.

Файлы с дозаписью вроде `sources.jsonl`, `findings.jsonl` и заметок итераций
оставляют проверяемый след. Локальный `workspace/` задачи нужен для скриптов,
SQLite, временного анализа, скриншотов, экспортов и производных результатов.

## Жизненный цикл

```mermaid
stateDiagram-v2
    [*] --> idle: create
    idle --> running: begin lease
    running --> idle: finish, continue
    running --> idle: finish, verify needs more work
    running --> idle: finish, adequacy passed and phase=finalize
    running --> finalize: finish, completion requested but finalization failed
    finalize --> running: begin rework
    running --> awaiting_review: finish with passed finalization
    awaiting_review --> idle: request-changes or reopen
    awaiting_review --> complete: approve or mark-delivered
    idle --> paused: pause
    paused --> idle: resume
    idle --> cancelled: stop
    running --> failed: fail or error threshold
    complete --> [*]
    cancelled --> [*]
    failed --> [*]
```

Рабочая итерация намеренно ограничена:

1. `begin` берёт блокировку и возвращает задание на работу.
2. Исполнитель делает один сфокусированный шаг исследования.
3. Исполнитель пишет JSON-результат.
4. `finish` проверяет результат и фиксирует переход состояния.
5. `fail` фиксирует ошибку, если итерация с блокировкой сломалась.

`begin` также участвует в общей очереди итераций на уровне research root. Очередь
сериализует выполнение worker-итераций между задачами одного root, но не мешает
планировать несколько фоновых задач. Если другая задача уже выполняется, `begin`
возвращает deferred/skipped результат и записывает диагностические поля ожидания,
а тик cron не считается ошибкой.

Так одна длинная сессия ассистента не становится единственным источником
правды.

## Проверка достаточности исследования

```mermaid
flowchart TD
    WorkerResult[Worker result JSON] --> WantsComplete{completion requested?}
    WantsComplete -- no --> Continue[idle / continue research]
    WantsComplete -- yes --> Adequacy[result.adequacy]
    Adequacy --> Check[research adequacy validation]
    Check --> Passed{adequacy passed?}
    Passed -- no, needs sources --> Search[search]
    Passed -- no, needs analysis --> Analyze[analyze]
    Passed -- no, needs synthesis --> Synthesize[synthesize]
    Passed -- needs user/operator --> Blocked[idle with operator_next_action]
    Passed -- yes --> Finalize[finalize]
```

Проверка достаточности отвечает на вопрос, достаточно ли само исследование до
того, как система начнёт упаковывать финальный результат. Она оценивает
соответствие цели, явные ограничения, требуемую форму результата, открытые
вопросы, разнообразие источников, пробелы доказательств и противоречия.

`result.adequacy`, который предоставляет worker, считается кандидатной оценкой.
Control-код сам ведёт счётчик попыток, выбирает маршрут и рассчитывает
`operator_next_action`. Граница доверия остаётся явной: worker сообщает о
пробелах, а lifecycle-код решает, вернуть задачу в `search`, `analyze`,
`synthesize` или перейти к `finalize`.

## Финальная проверка и ревью

```mermaid
flowchart TD
    WorkerResult[Worker result JSON] --> WantsComplete{should_complete?}
    WantsComplete -- no --> Continue[idle / continue research]
    WantsComplete -- yes --> Adequacy{adequacy passed?}
    Adequacy -- no --> Verify[verify / research rework]
    Adequacy -- yes --> Trace[result.finalization]
    Trace --> Validate[Finalization validation]
    Validate --> Passed{passed?}
    Passed -- no --> Rework[finalize / worker rework]
    Passed -- repeated failures --> Intervention[operator intervention]
    Passed -- yes --> Review[awaiting_review]
    Review --> Approve[approve]
    Review --> Changes[request-changes]
    Approve --> Complete[complete / delivery-ready]
    Changes --> Continue
```

Завершение, инициированное рабочей итерацией, требует пройденной проверки
достаточности исследования, `result.finalization.status="passed"`, непустых
доказательств проверки, отсутствия блокирующих дефектов и кандидатных
артефактов, которые можно посмотреть. `awaiting_review` означает, что кандидат
готов к проверке человеком. Это ещё не означает, что результат доставлен
пользователю.

Поверхность финальной проверки показывает `operator_next_action`:

- `review_candidate`
- `worker_rework`
- `operator_intervention`
- `verify_review_state`
- `continue_research`

Оператор видит следующий шаг явно, а не реконструирует намерение по сырому JSON.

Структурные outputs задаются в `working_memory.output_contract.outputs[]`.
Каждый output использует открытый `id`, небольшую системную `role`, optional
open `media_type` и optional ссылки `source_for` / `derived_from` по artifact
id. Фактические файлы появляются в `finalization.candidate_artifacts` и
`delivery.outputs` с явными путями. Validation сверяет объявленный контракт с
объявленными artifacts и проверяет task-local path/readability/non-empty shape;
тип файла, роль и provenance не выводятся из имени, расширения, MIME-строки,
заголовка, заметки или порядка в списке.

Финальная проверка записывает `output_decision` для structured output
contracts. `deliverable_decision`, `working_memory.output_contract.kind` и
`finalization.primary_deliverable_kind` остаются legacy compatibility для старой
single-output модели. Свободный `--deliverable`, channel context, title,
summary и notes не выбирают формат output или provenance.

## Reliability diagnostics

```mermaid
flowchart TD
    Lifecycle[Проверки жизненного цикла] --> Reliability[state.reliability]
    Delivery[Проверки доставки и очереди] --> Health[health]
    Finalization[Причины финальной проверки] --> Health
    Queue[queue-status findings] --> Health
    Reliability --> Summary[summary operator_attention]
    Reliability --> Health
    Health --> Operator[Действие оператора]
```

Reliability diagnostics остаётся read-only, если существующая команда жизненного
цикла явно не выполняет восстановление. Слой нормализует наблюдаемые классы
сбоев: повторные отказы completion validation, несостыковки delivery artifact
handoff, ошибки формы delivery channel, queue holder/waiter mismatches и причины
finalization rework. Цель — показать следующий безопасный шаг оператора без
тихой паузы расписаний или скрытого редактирования state.

## Интеграция с OpenClaw cron

```mermaid
sequenceDiagram
    participant Operator
    participant CLI as Research Mode CLI
    participant Cron as OpenClaw cron
    participant Worker
    participant State as state.json

    Operator->>CLI: start or schedule
    CLI->>State: create task and cron binding
    CLI->>Cron: register recurring isolated turn
    Cron->>Worker: launch bounded worker turn
    Worker->>CLI: begin
    CLI->>State: acquire lease
    Worker->>State: write artifacts and result file
    Worker->>CLI: finish
    CLI->>State: validate and commit transition
    CLI->>Cron: suspend when awaiting_review
    Operator->>CLI: approve / request-changes / reopen
```

Проект осознанно зависит от OpenClaw cron: расписание, изоляция, обновления в
канале владельца, поведение `pause` / `resume` / `stop` и передача на ревью
находятся на этом слое. Python-скрипты можно запускать вручную, но это не
самостоятельный планировщик.

## Почему эта архитектура лучше для длительных исследований

Правильное сравнение не "лучше во всём". Research Mode лучше для класса задач,
где исследование длится несколько итераций, важны проверяемый след, ревью,
повторяемость и аккуратная доставка.

| Категория альтернатив | Типичная слабость | Преимущество Research Mode |
| --- | --- | --- |
| Одноразовый ответ в чате | Теряет контекст и проверяемый след после одного ответа. | Состояние на диске, источники, выводы, заметки итераций и возможность продолжить работу. |
| Ручной процесс в notebook | Точный, но требует много ручной дисциплины и легко остаётся недокументированным. | Структурированный жизненный цикл плюс локальная рабочая область для кода и данных. |
| Обычная инструкция по расписанию | Может повторять работу без строгого контракта состояния. | `begin`/`finish` с блокировкой, нормализованные статусы и фиксируемые переходы. |
| Автономный цикл агента | Может дрейфовать, работать слишком долго или выдать сырые артефакты как финал. | Ограниченные итерации, ревью, след финальной проверки и проверка артефактов. |
| Отдельный scraper/RAG pipeline | Силен в сборе данных, но слабее в ревью человеком и выдаче результата. | Поверхности оператора, цикл ревью/доработки, форматирование выдачи и связанные задачи. |

Research Mode не нужен для быстрых поисков, одноразовых сводок, обычных задач
по коду или узких конвейеров данных, у которых уже есть собственные планировщик и
процесс ревью.

## Принципы дизайна

- **Долговечность вместо длинной инструкции.** Состояние живёт на диске, а не только в
  чате.
- **Ограниченная работа вместо бесконечной автономности.** Один запуск cron делает одну
  управляемую итерацию.
- **Явные переходы вместо ручного JSON.** Изменение состояния проходит через
  вспомогательные команды.
- **Ревью перед выдачей.** `awaiting_review` — контрольная точка, а не финальная доставка.
- **Проверяемые артефакты.** Кандидатные материалы должны лежать внутри задачи и
  быть структурно читаемыми.
- **Ясность для оператора.** `summary`, `status`, `task-playbook.md` и
  `operator_next_action` показывают текущую ситуацию.
- **Планирование через OpenClaw.** Cron и изолированные итерации — часть модели
  продукта, а не случайная деталь реализации.
