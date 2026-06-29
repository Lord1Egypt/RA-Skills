# Contributing to Research Mode

[English](#english) | [Русский](#русский)

## English

Thanks for helping improve Research Mode. This repository is public, but the
tool was built for OpenClaw-first research workflows. Keep contributions
reviewable, privacy-aware, and honest about the current support boundary.

### Development Environment

Use a Unix-like environment with Python 3.11 or newer. The release gate uses
only repository scripts plus `uvx` for lightweight tooling in CI.

```bash
python3 --version
python3 scripts/check_research_mode_docs.py
scripts/check_research_mode.sh
uvx --from bandit bandit -q -r scripts -x scripts/selftest
```

If your checkout does not preserve executable bits, run the full gate through
`bash scripts/check_research_mode.sh`.

### Contribution Flow

1. Fork or branch from the current `main`.
2. Keep one pull request focused on one coherent change.
3. Update docs and tests together when behavior, contracts, or support
   boundaries change.
4. Run the release gate before opening a pull request.
5. Explain security or privacy implications in the pull request when the change
   touches task state, artifacts, package installs, delivery, cron, paths, or
   external inputs.

### Public Contracts

These surfaces should be changed carefully and documented:

- user and operator documentation in `README.md`, `TROUBLESHOOTING.md`,
  `ARCHITECTURE.md`, `SECURITY.md`, `RELEASING.md`, and `ROADMAP.md`;
- helper commands exposed by `scripts/research_mode.py`;
- task-local files such as `state.json`, `sources.jsonl`, `findings.jsonl`,
  `runs.tsv`, `task-playbook.md`, result payloads, and delivery intents;
- public examples under `examples/`, including sanitized `research-trace/`
  directories.

The helper scripts are an operator and maintainer interface for an OpenClaw
skill. Do not present them as a standalone Python product unless the repository
actually gains that support.

### Security-Sensitive Areas

Be especially careful with:

- `prepare-runtime --package` and task-local Python package installation;
- filesystem path handling, path containment, symlinks, and artifact selection;
- URL capture and redirect handling;
- cron scheduling, worker leases, recovery, and queue state;
- delivery intents, owner binding, chat/thread/topic identifiers, and
  platform-specific adapters.

Do not commit task roots, downloaded corpora, generated reports, local runtime
folders, secrets, tokens, webhooks, chat ids, owner-specific configuration, or
private workspace paths. Public examples may include sanitized traces, but live
task roots should stay out of the repository.

### Issue Reports

Use the issue templates where possible. Sanitize logs and state before sharing:
remove secrets, tokens, webhooks, private paths, chat identifiers, owner
identifiers, internal hostnames, and any sensitive source material.

For vulnerabilities, use the repository security contact or a private security
advisory instead of a public issue.

## Русский

Спасибо за помощь с Research Mode. Репозиторий публичный, но инструмент создан
как OpenClaw-first workflow для длительных исследований. Изменения должны быть
удобны для ревью, аккуратны к приватности и честны про текущие границы
поддержки.

### Среда разработки

Нужна Unix-like среда и Python 3.11 или новее. Release gate использует скрипты
репозитория и `uvx` для лёгких проверок в CI.

```bash
python3 --version
python3 scripts/check_research_mode_docs.py
scripts/check_research_mode.sh
uvx --from bandit bandit -q -r scripts -x scripts/selftest
```

Если checkout не сохранил executable bit, полный gate можно запустить через
`bash scripts/check_research_mode.sh`.

### Как предлагать изменения

1. Делайте fork или ветку от актуального `main`.
2. Держите один pull request вокруг одного связного изменения.
3. Обновляйте документацию и тесты вместе, если меняется поведение, контракт или
   граница поддержки.
4. Перед pull request запускайте release gate.
5. Отдельно описывайте security/privacy implications, если изменение касается
   task state, artifacts, package installs, delivery, cron, paths или external
   inputs.

### Публичные контракты

Эти поверхности нужно менять аккуратно и документировать:

- пользовательская и операторская документация: `README.md`,
  `TROUBLESHOOTING.md`, `ARCHITECTURE.md`, `SECURITY.md`, `RELEASING.md`,
  `ROADMAP.md`;
- helper-команды из `scripts/research_mode.py`;
- task-local файлы: `state.json`, `sources.jsonl`, `findings.jsonl`,
  `runs.tsv`, `task-playbook.md`, result payloads и delivery intents;
- публичные примеры в `examples/`, включая очищенные `research-trace/`
  директории.

Helper-скрипты — это интерфейс оператора и сопровождающего для OpenClaw skill.
Не описывайте их как standalone Python product, пока такая поддержка реально не
появилась.

### Зоны повышенного внимания

Будьте особенно аккуратны с:

- `prepare-runtime --package` и установкой task-local Python packages;
- filesystem paths, path containment, symlinks и выбором artifacts;
- URL capture и redirect handling;
- cron scheduling, worker leases, recovery и queue state;
- delivery intents, owner binding, chat/thread/topic identifiers и
  platform-specific adapters.

Не коммитьте task roots, downloaded corpora, generated reports, local runtime
folders, secrets, tokens, webhooks, chat ids, owner-specific configuration или
private workspace paths. Публичные примеры могут включать sanitized traces, но
живые task roots не должны попадать в репозиторий.

### Issues

По возможности используйте issue templates. Перед публикацией логов и state
удаляйте secrets, tokens, webhooks, private paths, chat identifiers,
owner identifiers, internal hostnames и чувствительные исходные материалы.

Об уязвимостях лучше сообщать через security contact репозитория или private
security advisory, а не через публичный issue.
