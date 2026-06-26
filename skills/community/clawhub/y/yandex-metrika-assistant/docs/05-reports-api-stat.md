# API отчётов (stat)

Введение: https://yandex.ru/dev/metrika/ru/stat/  
Справочник таблицы: https://yandex.ru/dev/metrika/ru/stat/openapi/data  
Примеры: https://yandex.ru/dev/metrika/ru/stat/examples  
Сегментация: https://yandex.ru/dev/metrika/ru/stat/segmentation  
Семплирование: https://yandex.ru/dev/metrika/ru/stat/sampling  
Шаблоны отчётов (preset): https://yandex.ru/dev/metrika/ru/stat/presets

## Концепции

- **Группировка (dimension)** — атрибут визита/хита, по которому агрегируют данные. В запросе: параметр **`dimensions`** (несколько через запятую).
- **Метрика (metric)** — числовая величина по визитам/хитам. В запросе: **`metrics`** (несколько через запятую).
- Отчёт **без группировок** — суммарный результат по метрикам.

### Префиксы (совместимость в одном запросе)

- **`ym:s:`** — визиты  
- **`ym:pv:`** — хиты  

В **одном** запросе нельзя смешивать разные префиксы в основном наборе dimensions/metrics и указывать больше одного «множества» (см. доку по сегментации).

В параметре **`filters`** допускаются другие префиксы — в доке приведён пример с `ym:s:` в dimensions/metrics и `ym:pv:` в фильтре.

## Эндпоинты

| Вид | Метод |
|-----|--------|
| Таблица | `GET https://api-metrika.yandex.net/stat/v1/data` |
| Drill down | `GET .../stat/v1/data/drilldown` |
| По времени | `GET .../stat/v1/data/bytime` |
| Сравнение (таблица) | `GET .../stat/v1/data/comparison` |
| Сравнение (drilldown) | `GET .../stat/v1/data/comparison/drilldown` |

Документация по каждому — в разделе stat на сайте (openapi-страницы).

## Формат ответа

- Кодировка: **UTF-8**
- Формат: **JSON** (по умолчанию) или **CSV** — задаётся суффиксом в пути, например:

```
GET https://api-metrika.yandex.net/stat/v1/data.csv?id=...&metrics=...&dimensions=...
```

Пример из документации:

```
https://api-metrika.yandex.net/stat/v1/data.csv?id=44147844&metrics=ym:s:avgPageViews&dimensions=ym:s:operatingSystem&limit=5
```

## GET /stat/v1/data — основные query-параметры

Источник: openapi «Таблица».

| Параметр | Описание / лимиты |
|----------|-------------------|
| `ids` | ID счётчиков через запятую (integer[]) |
| `metrics` | Список метрик через запятую. **Лимит: 20 метрик** |
| `dimensions` | Группировки через запятую. **Лимит: 10 группировок** |
| `date1`, `date2` | `YYYY-MM-DD` или `today`, `yesterday`, `ndaysAgo`. Defaults в доке: часто `6daysAgo` и `today` |
| `filters` | Сегментация. До **10** уникальных измерений/метрик в фильтре, до **20** отдельных фильтров, длина строки условия до **10 000** символов, до **100** значений в одном условии |
| `limit` | Строк на страницу. **Макс. 100 000**, default `100` |
| `offset` | Индекс первой строки, **начиная с 1**, default `1` |
| `accuracy` | Размер выборки (семплирование) |
| `proposed_accuracy` | Если `true`, API может повысить accuracy до рекомендуемого |
| `preset` | Шаблон отчёта |
| `sort` | Сортировка по метрикам/группировкам; `-` перед именем — по убыванию |
| `timezone` | `±hh:mm` в диапазоне [-23:59; +23:59]; `+` в URL как `%2B`. По умолчанию — часовой пояс счётчика |
| `include_undefined` | boolean — строки с неопределённой первой группировкой |
| `direct_client_logins` | Логины клиентов Директа через запятую (отчёты по Директ-расходам) |
| `lang`, `pretty`, `callback` | Язык, форматирование JSON, JSONP |

Также доступны `id` в виде `id=44147844` в примерах (идентификатор счётчика) — в справочнике основной параметр списка счётчиков: **`ids`**.

## Раскрытие данных и приватность

- Часть данных (например соцдем) выдаётся **только если в выборке больше 10 посетителей**.
- В ответе API смотреть **`contains_sensitive_data`**: если **`true`**, данные с ограничениями.

Справка: https://yandex.ru/support/metrica/reports/report-general.html?lang=ru#privacy

## Версии stat

Поддерживаются `v1`, `v2` и др.; новым интеграциям — актуальная версия (см. `02-base-url-and-structure.md`).
