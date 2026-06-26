# ClawHub upload bundle — Yandex Metrika Assistant

Эта папка собрана **без** каталога `.git`, чтобы загрузка на [ClawHub](https://clawhub.ai) не ломалась из‑за известной проблемы «SKILL.md required» при наличии `.git` в архиве.

## Поля формы ClawHub

| Поле | Рекомендуемое значение |
|------|-------------------------|
| **Slug** | `yandex-metrika-assistant` |
| **Display name** | `Yandex Metrika Assistant` |

- Включите согласие с **MIT-0** на форме публикации (текст лицензии: https://spdx.org/licenses/MIT-0.html).
- Обязателен **`SKILL.md`** — он уже в корне.

## Содержимое архива

- `SKILL.md` — навык для OpenClaw
- `openclaw.plugin.json` — контракт плагина OpenClaw
- `docs/` — справка и инструкции (пути `{baseDir}/docs/...` в SKILL)

Скрипт обмена OAuth и полный `LICENSE` — в репозитории на GitHub (см. ссылку ниже).

## Как упаковать (Windows PowerShell)

Из каталога **родителя** этой папки (обязательно `\*`, не саму папку — иначе `SKILL.md` не окажется в корне zip):

```powershell
Compress-Archive -Path ".\clawhub-yandex-metrika-assistant\*" -DestinationPath ".\yandex-metrika-assistant-clawhub.zip" -Force
```

### Если валидация пишет «SKILL.md is required»

1. **В корне zip должен быть именно `SKILL.md`**, а не `какая-то-папка/SKILL.md`. Неправильно: архивировать папку целиком (`Compress-Archive -Path .\clawhub-yandex-metrika-assistant` без `\*`) — внутри получится одна вложенная папка, ClawHub файл не находит.
2. В архиве **не должно быть** каталога `.git` (см. [issue OpenClaw #32169](https://github.com/openclaw/openclaw/issues/32169)).
3. **Не используйте для упаковки** `tar -c -f ... .` из папки навыка без проверки: в zip может оказаться путь вида `./SKILL.md`; часть проверок ожидает ровно `SKILL.md`. После сборки откройте zip и убедитесь, что в корне есть `SKILL.md`.
4. Загружайте архив, собранный из **`clawhub-yandex-metrika-assistant`**, а не из всего репозитория `yandex-metrika-assistant` с вложенной структурой.

Исходный репозиторий с историей: https://github.com/Horosheff/yandex-metrika-assistant
