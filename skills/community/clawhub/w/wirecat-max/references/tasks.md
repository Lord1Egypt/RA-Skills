# Задачи владельца

Задачи открывает и закрывает `max personal review` ([обзор](reading.md#обзор-кто-кому-должен)). Id выдуманные.

```sh
max personal tasks list state:open --json              # что ждёт ответа владельца; задачи открывает и закрывает review
max personal tasks add <ссылка> --type request --category documents --json
# выход 2 task.duplicate-candidates: возможно, это та же открытая задача; повторите с --into <задача> или --new. Похожая только на закрытую — новая задача со связью follow-up-of
max personal tasks duplicates list --json               # пары, которые могут быть одной задачей; tasks merge <дубль> --into <задача>
max personal tasks duplicates reject <дубль> <задача>   # не одна задача; defer — решит владелец (decision:unsure); tasks unmerge <дубль> отменяет merge
max personal tasks related <задача> --json         # похожие задачи с полосой likely|maybe|different; ничего не меняет
max personal tasks agenda category:money tag:urgent --json   # план на сегодня; claimed:any — и занятые другими
max personal tasks claim <задача> --json           # занять, пока работаешь (30m, --lease); tasks release <задача> — отдать
max personal tasks categories --json             # категории; список один на хранилище (tg, max, memo), меняет его только владелец: max config set task_categories.<имя>
max personal tasks close <задача> --as dismissed --reason no-reply-needed --certainty 0.9 --json   # только когда владелец так решил; --certainty 0..1 обязателен, ниже порога задача остаётся открытой с предложением закрыть
max personal tasks list close:suggested --json      # предложения закрыть, которые ждут владельца: он подтверждает tasks close или отклоняет tasks reject
```
