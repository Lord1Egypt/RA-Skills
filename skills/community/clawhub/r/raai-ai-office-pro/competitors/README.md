# Competitors/ — архив конкурентного анализа Эта папка — **архив SKILL.md прямых конкурентов** AI-офис PRO с ClawHub.
Анализ сводный лежит в [`../docs/competitors-comparison.md`](../docs/competitors-comparison.md). ## Состав | Файл | Конкурент | Источник | Дата архива |
|---|---|---|---|
| `ceo-master_SKILL.md` | ceo-master@1.0.0 | `openclaw skills install ceo-master` → /srv/openclaw/workspace/skills/ceo-master/ | 2026-04-19 С.19 |
| `ceo-assistant_SKILL.md` | ceo-assistant@1.0.0 | `openclaw skills install ceo-assistant` → /srv/openclaw/workspace/skills/ceo-assistant/ | 2026-04-19 С.19 |
| `morning-briefing-pro_SKILL.md` | morning-briefing-pro@1.0.2 | `openclaw skills install morning-briefing-pro` → /srv/openclaw/workspace/skills/morning-briefing-pro/ | 2026-04-19 С.19 | ## Политика обновления - **Bump версии коробки** ( → v3.6 и т.д.) → re-install конкурентов и сверка SKILL.md
- **Появление нового конкурента в ClawHub категории CEO/executive/briefing** → добавить в эту папку
- **Обновление SKILL.md конкурента** → обновить архив + внести изменения в `docs/competitors-comparison.md` ## Как обновить архив ```bash
# На VPS:
openclaw skills update ceo-master
openclaw skills update ceo-assistant
openclaw skills update morning-briefing-pro # Проверить версии:
grep -r '^version:' /srv/openclaw/workspace/skills/{ceo-master,ceo-assistant,morning-briefing-pro}/SKILL.md # Синхронизировать архив (команда на ПК):
# mcp__ssh-server__exec "cat /srv/openclaw/workspace/skills/<name>/SKILL.md" → Write в этот каталог
``` ## Правило ассумпций (feedback_assumption_vs_verified) Любые утверждения «у конкурента X есть Y / нет Z» — **только после открытия их SKILL.md**. Без файла в этой папке — фраза «конкурент ceo-master слаб» запрещена.
