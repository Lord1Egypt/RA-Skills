# Example mcporter wiring

## English

Example `mcporter.json` entry for `yacli`:

```json
{
  "name": "yacli",
  "transport": "stdio",
  "command": "/path/to/yacli-mcp-server",
  "env": {
    "YACLI_CONFIG_DIR": "/path/to/yacli-config",
    "YACLI_SECRET_BACKEND": "file"
  }
}
```

### Notes
- Replace all example paths with real host paths
- `YACLI_CONFIG_DIR` should point to a persistent directory
- Do not publish real tokens, cookies, or account snapshots with this skill
- If your host uses another secret backend, adjust `YACLI_SECRET_BACKEND` accordingly

## Русский

- Ниже пример того, как может выглядеть подключение `yacli` через `mcporter`
- Это не готовый production config, а шаблон
- Все пути нужно заменить на реальные

### Примечания
- Замените все примерные пути на реальные пути вашего хоста
- `YACLI_CONFIG_DIR` должен указывать на персистентный каталог
- Не публикуйте вместе со skill реальные токены, cookies и account snapshots
- Если на вашем хосте используется другой secret backend, скорректируйте `YACLI_SECRET_BACKEND`
