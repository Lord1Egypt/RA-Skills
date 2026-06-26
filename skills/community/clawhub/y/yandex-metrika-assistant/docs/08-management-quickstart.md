# API управления — быстрый старт и счётчики

Быстрый старт (общий): https://yandex.ru/dev/metrika/ru/intro/quick-start  
Введение management: https://yandex.ru/dev/metrika/ru/management/

## Список счётчиков

```
GET https://api-metrika.yandex.net/management/v1/counters
Authorization: OAuth <token>
```

Пример curl из документации:

```bash
curl -i -X GET 'https://api-metrika.yandex.net/management/v1/counters' \
  -H 'Authorization: OAuth 05dd3dd8...'
```

Ответ содержит массив **`counters`** с полями вроде `id`, `name`, `site`, `permission`, `status` и т.д.

### Полезные query-параметры (справочник counters)

Документация: https://yandex.ru/dev/metrika/ru/management/openapi/counter/counters

| Параметр | Назначение |
|----------|------------|
| `per_page` | Количество счётчиков (макс. **10 000** за запрос, default **1000**) |
| `offset` | С какого номера начать (1-based, макс. смещение связано с лимитом 100 000 счётчиков на пользователя) |
| `permission` | `own`, `view`, `edit` (можно несколько через запятую) |
| `counter_ids` | Явный список ID |
| `field` | Доп. поля объекта через запятую, без пробелов: например `goals,mirrors,grants,filters,operations,counter_flags,measurement_tokens` |
| `favorite`, `label_id`, `search_string`, `reverse`, `robots` | Фильтры и сортировка — см. openapi |

## Пример: создать цель

```
POST https://api-metrika.yandex.net/management/v1/counter/{counterId}/goals
Authorization: OAuth <token>
Content-Type: application/json
```

Документация метода: https://yandex.ru/dev/metrika/ru/management/openapi/goal/addGoal  

Пример из quick-start — цель типа **MessengerGoal** (`messenger`), условие с `url` (например `whatsapp`):

```bash
curl -i -X POST 'https://api-metrika.yandex.net/management/v1/counter/XXX/goals' \
  -H 'Authorization: OAuth 05dd3dd8...' \
  -H 'Content-Type: application/json' \
  -d '{
    "goal": {
      "id": 0,
      "name": "MyMessengerGoal",
      "type": "messenger ",
      "conditions": [{
        "type": "messenger",
        "url": "whatsapp"
      }]
    }
  }'
```

(В ответе `type` нормализуется к `"messenger"`.)

## Область API управления

Счётчики (CRUD), цели, операции, фильтры, доступы, представители и др. — см. дерево методов в разделе **management** на сайте разработчиков.

### Фильтры доступа (changelog 02.10.2024)

Методы access filter, например:

- create: https://yandex.ru/dev/metrika/ru/management/openapi/access_filter/createAccessFilter  
- delete, get, list, update — см. changelog в `09-changelog-highlights.md` или поиск по `access_filter` в доке.
