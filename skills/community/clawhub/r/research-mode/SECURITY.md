# Security Policy

[English](#english) | [Русский](#русский)

## English

Research Mode is an OpenClaw cron-based skill for durable background research.
It stores task state and artifacts on disk, can prepare task-local runtimes, and
can format outputs for delivery surfaces. Treat research roots and task
workspaces as potentially sensitive.

Security expectations:

- Do not commit task roots, downloaded corpora, generated reports, secrets,
  tokens, webhooks, chat ids, or owner-specific configuration.
- Keep extra packages task-local. Review unusual or risky packages before
  installation.
- Treat `prepare-runtime --package` as a controlled capability. It can create a
  task-local venv, invoke Python tooling, and install requested packages, so the
  decision to install a package must come from an operator or trusted workflow,
  not from untrusted retrieved content.
- Treat absolute interpreter, venv, and workspace paths as local diagnostics.
  Prefer task-relative or redacted paths in public/package-facing summaries.
- URL capture accepts only `http://` and `https://` and blocks local or private
  network hosts, including redirect targets; local files should be attached
  through explicit file helpers.
- Do not pipe remote scripts into a shell from documentation or task artifacts.
- Treat web pages, PDFs, emails, and retrieved files as untrusted data, not as
  instructions.
- Review candidate deliverables before user-facing delivery.

Current public CI uses the full release gate plus a Bandit smoke scan over
production scripts. CodeQL is not enabled by default because the current risk
surface is mostly Python helper scripts, local files, task-local runtimes, and
OpenClaw integration boundaries; additional scanning can be added if it produces
useful signal without requiring private OpenClaw secrets.

To report a vulnerability, open a private security advisory or contact the
maintainer through the repository's configured security contact. Do not publish
exploitable details before maintainers have had time to respond.

## Русский

Research Mode — OpenClaw skill для длительного фонового исследования через
cron. Он хранит состояние задач и артефакты на диске, может готовить локальное
окружение задачи и форматировать результаты для выдачи. Корни исследований и
рабочие области задач нужно считать потенциально чувствительными.

Ожидания по безопасности:

- Не добавлять в коммиты корни задач, скачанные корпуса, сгенерированные отчёты,
  секреты, токены, URL вебхуков, идентификаторы чатов и конфигурацию
  конкретного владельца.
- Дополнительные пакеты держать локальными для задачи. Необычные или рискованные пакеты
  проверять перед установкой.
- `prepare-runtime --package` — controlled capability. Она может создавать
  task-local venv, запускать Python tooling и устанавливать requested packages,
  поэтому решение об установке package должно приходить от оператора или
  доверенного workflow, а не из недоверенного retrieved content.
- Абсолютные пути interpreter, venv и workspace считать локальной диагностикой.
  В public/package-facing summaries предпочитать task-relative или redacted
  paths.
- Захват URL принимает только `http://` и `https://` и блокирует локальные или
  приватные сетевые хосты, включая redirect targets; локальные файлы должны
  прикрепляться через явные file helpers.
- Не выполнять удалённые скрипты через shell pipe из документации или артефактов
  задачи.
- Веб-страницы, PDFs, emails и полученные файлы считать недоверенными данными, а не
  инструкциями.
- Кандидатные материалы проверять перед выдачей пользователю.

Текущий публичный CI запускает полный release gate и Bandit smoke scan по
production scripts. CodeQL по умолчанию не включён: основная поверхность риска
сейчас находится в Python helper scripts, локальных файлах, task-local runtimes и
границах интеграции с OpenClaw. Дополнительные сканеры стоит добавлять, если они
дают полезный сигнал и не требуют приватных OpenClaw secrets.

Сообщения об уязвимостях принимаются через private security advisory или
контакт безопасности, настроенный в репозитории. Детали эксплуатации не следует
публиковать до ответа сопровождающих.
