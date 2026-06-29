# Research Mode Releasing

[English](#english) | [Русский](#русский)

Audience: maintainers.

This is the maintainer-facing release procedure for `research-mode` as an
OpenClaw cron-based skill package.

Это процедура релиза для сопровождающих `research-mode` как OpenClaw skill,
работающего через cron.

## English

## Release scope

`research-mode` is distributed as an OpenClaw skill package. It is not a generic
standalone Python package, daemon, hosted service, or platform-independent
library.

Release bundle:

- this repository as an OpenClaw skill package;
- helper scripts runnable for smoke tests and manual inspection;
- OpenClaw cron documented as the expected execution layer;
- no claim that the helper scripts are a platform-independent scheduler.

Use `RELEASE_NOTES.md` as the version handoff.

## Package boundary

Include in the public package:

- `SKILL.md`
- `README.md`
- `TROUBLESHOOTING.md`
- `ARCHITECTURE.md`
- `RELEASING.md`
- `RELEASE_NOTES.md`
- `LICENSE`
- `SECURITY.md`
- `AGENTS.md`
- `ROADMAP.md`
- `CONTRIBUTING.md`
- `RULES.example.md`
- `.gitignore`
- `pyrightconfig.json`
- `assets/`
- `docs/`
- `schemas/`
- `examples/`
- `scripts/*.py`
- `scripts/check_research_mode.sh`
- `scripts/selftest/`

ClawHub skill publishing currently uploads text-like files only. Binary
repository assets such as `assets/social-preview.png` and example `.xlsx`
workbooks remain available through the GitHub repository and GitHub releases,
but are not present in `clawhub install` outputs. ClawHub also applies its
platform skill license to the registry package; the GitHub source repository is
licensed under Apache License, Version 2.0.

Exclude from the public package:

- `research/` task roots and runtime task directories;
- task-local `workspace/` outputs unless deliberately anonymized;
- private notes and personal memory files;
- owner-specific chat ids, cron ids, tokens, webhooks, local helper paths, or
  service configuration;
- generated caches such as `__pycache__/`, `.pytest_cache/`, and temporary smoke
  roots.

The repository may keep optional internal documentation elsewhere, but the
public skill package must pass `scripts/check_research_mode_docs.py` without
requiring private workspace files.

## Release gate

Before tagging a release:

- [ ] Run `scripts/check_research_mode.sh` from the package root.
- [ ] Confirm the gate finishes with `ruff`, docs smoke, release smoke, `pyright`, selftest, and pytest all passing.
- [ ] Confirm GitHub Actions CI is green on the release commit.
- [ ] Confirm `uvx --from bandit bandit -q -r scripts -x scripts/selftest` has no findings.
- [ ] For a focused lifecycle check, run `python3 scripts/release_smoke.py` from the package root.
- [ ] Review `git diff --stat` and the full diff for unrelated workspace or memory changes.
- [ ] Confirm release docs are covered by `scripts/check_research_mode_docs.py`.
- [ ] Confirm any new CLI command is documented with argparse-valid examples.
- [ ] Confirm `RELEASING.md` and `RELEASE_NOTES.md` are covered by docs smoke.
- [ ] Confirm Apache License, Version 2.0 is present as `LICENSE`.

## Release safety review

Before building a release bundle:

- [ ] Remove or rewrite private workspace paths that are not necessary for OpenClaw usage.
- [ ] Remove private chat, owner, task, cron, token, webhook, and service identifiers from examples.
- [ ] Do not include task artifacts from `research/`, runtime workspaces, downloaded corpora, or generated reports unless deliberately anonymized.
- [ ] Keep sample data synthetic or clearly redistributable.
- [ ] Audit dependency instructions for `curl|sh`, unpinned remote scripts, or blind package installs.
- [ ] Make local-package installation behavior explicit: task-local runtimes are allowed; unusual or risky packages require review.

## Finalization contract

Released behavior must preserve these invariants:

- [ ] Worker-initiated completion requires `result.finalization.status="passed"`.
- [ ] Finalization evidence must distinguish internal artifacts from candidate user-facing artifacts.
- [ ] Candidate artifacts must be inspectable and task-local.
- [ ] Raw workspace artifacts must not be exposed as the final user deliverable.
- [ ] `awaiting_review` means review-ready, not delivery-ready.
- [ ] `summary`, `status`, and `task-playbook.md` expose `operator_next_action`.
- [ ] Failed finalization routes to worker rework or operator intervention instead of silently marking the task complete.

## Documentation handoff

Before asking someone else to try the package:

- [ ] README is bilingual: English and Russian.
- [ ] README clearly says this is an OpenClaw cron-based skill.
- [ ] README explains installation through a repository clone inside the OpenClaw skills directory.
- [ ] README links to Apache License, Version 2.0 via `LICENSE`.
- [ ] README explains chat-first usage, launch parameters, review, common work patterns, launch modes, CLI command families, task states, scheduling, delivery, and quality gates.
- [ ] README mentions that GitHub Actions runs the release gate and Bandit security smoke scan.
- [ ] `TROUBLESHOOTING.md` explains diagnosis order, common failure modes, and safe repair paths.
- [ ] `TROUBLESHOOTING.md` covers preflight `needs_setup` / `blocked` states.
- [ ] `ARCHITECTURE.md` explains the system with diagrams and calibrated comparisons.
- [ ] `RELEASING.md` explains the OpenClaw skill package boundary.
- [ ] `SECURITY.md` explains task artifact, package, and untrusted-input safety.
- [ ] `AGENTS.md` keeps coding-agent maintenance notes separate from human-facing docs.
- [ ] `RELEASE_NOTES.md` states current status and known limitations.
- [ ] `SKILL.md` is still agent-facing and concise enough to load as operational instruction.
- [ ] Human docs explain create/start, begin/finish, pause/resume/stop, review, approval, delivery, and linked research.
- [ ] Troubleshooting covers stale locks, review-gated tasks, failed finalization, missing artifacts, and dangerous package decisions.
- [ ] Examples avoid assuming a specific chat system, note app, private cron ids, or local helper setup.

## Smoke scenario

Run a clean task in a temporary root:

1. Create a task.
2. Confirm the first lease runs `phase=preflight`.
3. Finish preflight with `result.preflight.decision="go"` and confirm the task
   returns to the target phase.
4. Begin a research iteration.
5. Finish with a human-ready Markdown report and passing finalization evidence.
6. Confirm the task reaches `awaiting_review`.
7. Confirm `summary --format text` shows `operator_next_action: review_candidate`.
8. Approve the task.
9. Confirm delivery state is consistent and no worker lease remains active.

## Русский

## Контур релиза

`research-mode` распространяется как OpenClaw skill. Это не универсальный
Python-пакет, не самостоятельный демон, не размещённый сервис и не независимая
от платформы библиотека.

Состав релиза:

- этот репозиторий как OpenClaw skill;
- вспомогательные скрипты запускаются для smoke-тестов и ручной диагностики;
- OpenClaw cron описан как ожидаемый слой выполнения;
- вспомогательные скрипты не позиционируются как независимый планировщик.

`RELEASE_NOTES.md` описывает текущий релиз.

## Граница пакета

Включать в публичный пакет:

- `SKILL.md`
- `README.md`
- `TROUBLESHOOTING.md`
- `ARCHITECTURE.md`
- `RELEASING.md`
- `RELEASE_NOTES.md`
- `LICENSE`
- `SECURITY.md`
- `AGENTS.md`
- `ROADMAP.md`
- `CONTRIBUTING.md`
- `RULES.example.md`
- `.gitignore`
- `pyrightconfig.json`
- `assets/`
- `docs/`
- `schemas/`
- `examples/`
- `scripts/*.py`
- `scripts/check_research_mode.sh`
- `scripts/selftest/`

ClawHub сейчас публикует skill-пакеты только как набор text-like файлов.
Бинарные файлы репозитория, например `assets/social-preview.png` и example
`.xlsx` workbooks, остаются доступными через GitHub repository и GitHub
releases, но не попадают в результат `clawhub install`. ClawHub также применяет
к registry package свою платформенную лицензию для skills; исходный GitHub
repository лицензирован под Apache License, Version 2.0.

Исключать из публичного пакета:

- корни задач `research/` и директории выполнения задач;
- выводы из локального для задачи `workspace/`, если они не были специально
  анонимизированы;
- приватные заметки и файлы личной памяти;
- идентификаторы чатов, cron-заданий, токены, webhooks, локальные пути
  вспомогательных инструментов и конфигурацию сервисов конкретного владельца;
- сгенерированные кэши: `__pycache__/`, `.pytest_cache/`, временные корни
  smoke-тестов.

В репозитории могут оставаться внутренние документы, но публичный пакет skill
должен проходить `scripts/check_research_mode_docs.py` без приватных файлов
рабочей области.

## Проверка релиза

Перед тегом релиза:

- [ ] Запустить `scripts/check_research_mode.sh` из корня репозитория.
- [ ] Проверить, что проходят `ruff`, проверка документации, релизный smoke-тест, `pyright`, selftest и pytest.
- [ ] Для отдельной проверки жизненного цикла запустить `python3 scripts/release_smoke.py` из корня репозитория.
- [ ] Просмотреть `git diff --stat` и полный diff на случайные изменения рабочей области или файлов памяти.
- [ ] Убедиться, что релизные документы покрыты `scripts/check_research_mode_docs.py`.
- [ ] Убедиться, что новые CLI-команды документированы примерами, валидными относительно `argparse`.
- [ ] Убедиться, что `RELEASING.md` и `RELEASE_NOTES.md` покрыты проверкой документации.
- [ ] Убедиться, что Apache License, Version 2.0 добавлена как `LICENSE`.

## Проверка безопасности релиза

Перед сборкой релизного пакета:

- [ ] Убрать или переписать приватные пути рабочей области, которые не нужны для использования с OpenClaw.
- [ ] Убрать приватные идентификаторы чатов, владельца, задач, cron-заданий, токенов, webhook URLs и сервисов из примеров.
- [ ] Не включать артефакты задач из `research/`, runtime-директории, скачанные корпуса или сгенерированные отчёты без явной анонимизации.
- [ ] Использовать только синтетические примеры или данные, которые явно можно распространять.
- [ ] Проверить инструкции по зависимостям на `curl|sh`, удалённые скрипты без закреплённой версии и слепую установку пакетов.
- [ ] Явно описать политику установки пакетов: окружения, локальные для задачи, разрешены, необычные или рискованные пакеты требуют ревью.

## Контракт финализации

Поведение релиза должно сохранять инварианты:

- [ ] Завершение, инициированное рабочей итерацией, требует `result.finalization.status="passed"`.
- [ ] Доказательства финальной проверки различают внутренние артефакты и кандидатные пользовательские материалы.
- [ ] Кандидатные артефакты должны быть доступны для проверки и лежать внутри задачи.
- [ ] Сырые артефакты рабочей области не должны выдаваться как финальный пользовательский результат.
- [ ] `awaiting_review` означает готовность к ревью, а не готовность к выдаче.
- [ ] `summary`, `status` и `task-playbook.md` показывают `operator_next_action`.
- [ ] Неудачная финальная проверка ведёт к доработке или вмешательству оператора, а не к тихому завершению.

## Передача документации

Перед тем как отдавать пакет кому-то на пробу:

- [ ] README двуязычный: English и Russian.
- [ ] README прямо говорит, что это OpenClaw skill, работающий через cron.
- [ ] README объясняет установку через clone репозитория прямо внутри директории skills OpenClaw.
- [ ] README ссылается на Apache License, Version 2.0 через `LICENSE`.
- [ ] README объясняет использование из чата, параметры запуска, ревью, частые рабочие сценарии, варианты запуска, семейства CLI-команд, состояния задач, расписание, доставку и проверки качества.
- [ ] `TROUBLESHOOTING.md` объясняет порядок диагностики, частые сбои и безопасные способы исправления.
- [ ] `TROUBLESHOOTING.md` покрывает состояния preflight `needs_setup` / `blocked`.
- [ ] `ARCHITECTURE.md` объясняет систему через схемы и аккуратные сравнения.
- [ ] `RELEASING.md` объясняет состав пакета OpenClaw skill.
- [ ] `SECURITY.md` объясняет безопасность артефактов задач, пакетов и недоверенных входных данных.
- [ ] `AGENTS.md` держит заметки для агентов-разработчиков отдельно от пользовательской документации.
- [ ] `RELEASE_NOTES.md` фиксирует текущий статус и известные ограничения.
- [ ] `SKILL.md` остаётся инструкцией для агентов и достаточно компактен для загрузки.
- [ ] Пользовательская документация объясняет create/start, begin/finish, pause/resume/stop, ревью, утверждение, выдачу и связанные исследования.
- [ ] Раздел troubleshooting покрывает stale locks, задачи на ревью, неудачную финальную проверку, отсутствующие артефакты и решения по рискованным пакетам.
- [ ] Примеры не предполагают конкретную систему чатов, приложение для заметок, приватные cron ids или локальные вспомогательные инструменты.

## Smoke-сценарий

Прогнать чистую задачу во временной директории:

1. Создать задачу.
2. Проверить, что первая блокировка запускает `phase=preflight`.
3. Завершить preflight с `result.preflight.decision="go"` и проверить, что
   задача вернулась к целевой фазе.
4. Начать рабочую итерацию.
5. Завершить её с Markdown-отчётом для человека и успешными доказательствами финальной проверки.
6. Проверить, что задача перешла в `awaiting_review`.
7. Проверить, что `summary --format text` показывает `operator_next_action: review_candidate`.
8. Утвердить задачу.
9. Проверить, что состояние выдачи согласовано и активной рабочей блокировки больше нет.
