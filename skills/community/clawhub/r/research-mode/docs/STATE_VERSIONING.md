# Research Mode State Versioning

[English](#english) | [Русский](#русский)

## English

Current public task state uses `version: 2`. Some planning notes may refer to
`state_version`; do not treat that as a separate required public field until a
future migration introduces it compatibly. For the current contract, `version`
is the state format version.

### Compatibility Policy

Backward-compatible changes:

- adding optional fields;
- adding nullable fields with safe defaults;
- adding new status details that older readers can ignore;
- adding derived summaries that do not replace the source-of-truth fields.

Breaking changes:

- renaming or removing fields used by existing task states;
- changing the meaning of lifecycle status, review state, or delivery state;
- requiring new fields without lazy normalization for older tasks;
- changing path containment or artifact semantics in a way that could expose or
  accept files outside the task directory.

### Reading Older State

Readers should normalize older state lazily where possible. That means a command
can fill missing optional structures in memory or during a safe state update
without requiring an operator to run a manual migration first.

Use explicit migration only when a change cannot be represented through safe
defaults or when old state would otherwise be ambiguous.

Current optional compatibility defaults include owner routing fields, delivery
intent lists, queue state, delivery package markers, and the `reliability`
diagnostic block. Older tasks may omit these fields and should still render
through `status`, `summary`, `health`, and `begin` without a migration command.

### Testing

State compatibility belongs in automated tests. The current compatibility test
anchor is `scripts/selftest/test_state_compatibility.py`. When a new state field
is added, include at least one old-state fixture or construction path that proves
existing tasks do not fail with `KeyError` or silently lose review/delivery
meaning.

Schemas under `schemas/` describe the public contract slice. They are not a
license to invent new required fields without compatibility work.

## Русский

Текущее публичное состояние задачи использует `version: 2`. В некоторых
планировочных заметках может встречаться `state_version`; не нужно считать это
отдельным обязательным публичным полем, пока будущая миграция не введёт его
совместимо. В текущем контракте версию формата state задаёт поле `version`.

### Политика совместимости

Backward-compatible изменения:

- добавление optional fields;
- добавление nullable fields с безопасными defaults;
- добавление новых деталей статуса, которые старые readers могут игнорировать;
- добавление производных summaries, которые не заменяют source-of-truth поля.

Breaking changes:

- переименование или удаление полей, которые уже используются существующими
  task states;
- изменение смысла lifecycle status, review state или delivery state;
- требование новых полей без lazy normalization для старых задач;
- изменение path containment или artifact semantics так, что это может раскрыть
  или принять файлы вне директории задачи.

### Чтение старого state

Readers должны по возможности нормализовать старое состояние лениво. Команда
может добавить отсутствующие optional structures в памяти или при безопасном
обновлении state, не требуя от оператора сначала запускать ручную миграцию.

Явная миграция нужна только тогда, когда изменение нельзя выразить через
безопасные defaults или старое состояние иначе становится неоднозначным.

Текущие optional defaults включают поля owner routing, список delivery intents,
queue state, delivery package markers и диагностический блок `reliability`.
Старые задачи могут не иметь этих полей и всё равно должны отображаться через
`status`, `summary`, `health` и `begin` без ручной миграции.

### Тестирование

Совместимость state должна проверяться автоматически. Текущая точка для таких
проверок — `scripts/selftest/test_state_compatibility.py`. Если добавляется
новое поле state, нужен хотя бы один old-state fixture или construction path,
который доказывает, что существующие задачи не падают с `KeyError` и не теряют
смысл review/delivery.

Schemas в `schemas/` описывают публичный срез контракта. Они не дают права
придумывать новые обязательные поля без compatibility work.
