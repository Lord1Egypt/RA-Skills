> ⚠️ Миссии изменяют локальные файлы и могут сохранять уроки/прогресс в локальную память ViBo. Запуская пример — вы соглашаетесь с этим (детали: SKILL.md, «Privacy, consent, retention & deletion»).

# vibo-selfdeed — примеры применения

Три типовых кейса. Каждый — это «задание», которое хозяин даёт агенту.
Агент действует по SKILL.md (START → SCAN → PROPOSE → FIX → ITERATE → LEARN → REPORT).

---

## Пример 1 — код: «Найди и исправь баги в src/»

**Задача:** в проекте `src/` падают тесты и есть дублирование кода.

```
./run_mission.sh init --task "исправить падающие тесты в src/" --target 90
python3 lib_vibo.py find "src тесты архитектура"      # START: контекст
./run_mission.sh checkpoint START ok "проект — Flask API, падают 3 теста"
# SCAN: pytest, grep дублей → 3 бага
./run_mission.sh checkpoint SCAN ok "3 бага: NPE в routes, таймаут, дубль helper"
./run_mission.sh progress 0/3
# PROPOSE: диффы → подтверждение (или --auto)
# FIX: safety.backup("src/routes.py") → правки → pytest
./run_mission.sh progress 2/3
# ITERATE: путь A не помог на 3-м баге → switch B
./run_mission.sh switch B
./run_mission.sh progress 3/3
# LEARN: vibo add lesson "таймаут-баг лечится asyncio.timeout, не sleep"
./run_mission.sh checkpoint LEARN ok "урок сохранён"
./run_mission.sh finish
```

---

## Пример 2 — документы: «Вычитай и приведи к единому стилю docs/»

**Задача:** в `docs/` 12 файлов, разный стиль (заголовки, термины).

```
./run_mission.sh init --task "единый стиль docs/ (заголовки+термины)" --target 100
python3 lib_vibo.py find "docs стиль термины"
# SCAN: grep заголовков (# vs ##), терминов (ViBo vs VIBO) → 8 расхождений
# PROPOSE → FIX (бэкап каждого файла)
# LEARN: vibo add lesson "стандарт: H2 для разделов, термин 'ViBo' один"
./run_mission.sh finish
```

---

## Пример 3 — конфиги: «Проверь согласованность конфигов»

**Задача:** `config/` — prod/staging/dev должны совпадать по ключам.

```
./run_mission.sh init --task "сверка config/ prod vs dev" --target 100
# SCAN: сравнить ключи (python yaml/json) → 2 пропущенных ключа
# PROPOSE → FIX (добавить ключи, бэкап)
# LEARN: vibo add lesson "ключ X обязателен во всех окружениях"
./run_mission.sh finish
```

---

## Советы агенту

- **SCAN исполняет сам агент** (линт, тесты, grep, чтение файлов) — скилл даёт структуру и память, а не «магический сканер». Это по ТЗ: агент — исполнитель, скилл — каркас.
- **Память — сила:** перед каждым кругом `vibo find` — не наступай на грабли.
- **Пути А/Б/В:** если способ не дал роста 2 круга — переключись, не долби.
- **Безопасность:** бэкап до правки, 3 попытки, 10 минут, L3 не трогать.
- **Честность:** не выдумывай «магию» — отчёт только по фактам.
