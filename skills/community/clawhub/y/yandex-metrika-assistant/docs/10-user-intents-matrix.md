# Типовые вопросы пользователей → API Метрики (матрица для агента)

Собрано по структуре [примеров API отчётов](https://yandex.ru/dev/metrika/ru/stat/examples), [шаблонов (preset)](https://yandex.ru/dev/metrika/ru/stat/presets) и разделам **management / logs / import**. Имена **`metrics`/`dimensions`/`filters`** агент подбирает только из **актуального справочника** Метрики, не «с головы».

**Общий порядок:** токен → `ids` счётчика → `date1`/`date2` → `GET /stat/v1/data` (или `bytime` / `comparison` / `drilldown`) → интерпретация `contains_sensitive_data`.

Для фильтров с **русскими названиями** городов и т.п. в запросе указывать **`lang=ru`** (см. примеры в доке).

---

## A. Трафик и динамика

| Как могут спросить | Что делать | Примечание |
|--------------------|------------|------------|
| Сколько визитов/посетителей за период | `stat/v1/data`, `metrics=ym:s:visits`, `ym:s:users` (или пресет посещаемости) | Период явно; по умолчанию в примерах часто 7 дней |
| Динамика по дням / «график за месяц» | `stat/v1/data/bytime` или `dimensions=ym:s:date` + метрики | См. [пример «просмотры по дням»](https://yandex.ru/dev/metrika/ru/stat/examples#query4) |
| Сравни два периода / вчера и позавчера | `stat/v1/data/comparison` | [Сравнение сегментов](https://yandex.ru/dev/metrika/ru/stat/examples#comparison) |
| Падение/рост трафика — почему | Несколько запросов: источники + география + устройства за два окна | Косвенный анализ, API даёт числа |
| Исключить роботов | `filters=... AND ym:s:isRobot=='No'` | [Пример](https://yandex.ru/dev/metrika/ru/stat/examples#robots) |

---

## B. Источники, UTM, реклама

| Как могут спросить | Что делать | Примечание |
|--------------------|------------|------------|
| Откуда приходят / источники сводка | `preset=sources_summary` | [Пример](https://yandex.ru/dev/metrika/ru/stat/examples#ex1) |
| Органика / поисковики / прямой / рефералы | `dimensions` по типу источника + `filters` | [Типы источников](https://yandex.ru/dev/metrika/ru/stat/examples#ex0) |
| Какие поисковые системы / фразы | `preset=sources_search_phrases` или группировки по поиску | [Поисковые фразы](https://yandex.ru/dev/metrika/ru/stat/examples#ex3) |
| UTM-метки, кампании, объявления | Пресеты раздела **Источники** или явные dimensions UTM | [Источники (presets)](https://yandex.ru/dev/metrika/ru/stat/presets/preset_sources) |
| Яндекс Директ, сводка по рекламе | Пресеты **Директ** | [preset_direct](https://yandex.ru/dev/metrika/ru/stat/presets/preset_direct) |
| Рекламные расходы (загруженные в Метрику) | Пресет **Рекламные расходы** + при необходимости импорт | [preset_expenses](https://yandex.ru/dev/metrika/ru/stat/presets/preset_expenses), `docs/07-data-import.md` |
| Эксперименты Директа | Пример «сегменты эксперимента» | [dim-metrics2](https://yandex.ru/dev/metrika/ru/stat/examples#dim-metrics2) |

---

## C. Аудитория: география, демография, устройства

| Как могут спросить | Что делать | Примечание |
|--------------------|------------|------------|
| Страны, города, регионы | Пресеты **Посетители → География** или `dimensions` региона | Фильтр по городу: [пример СПб](https://yandex.ru/dev/metrika/ru/stat/examples#ex2); `lang=ru` для русских названий |
| Мобильные vs десктоп / планшеты | `comparison` мобильный / не мобильный | [Пример](https://yandex.ru/dev/metrika/ru/stat/examples#comparison2) |
| ОС, браузеры | `preset=tech_platforms`, `dimensions=ym:s:browser` и т.д. | [Браузеры](https://yandex.ru/dev/metrika/ru/stat/examples#ex4) |
| Язык браузера | Группировки уровня визита из справочника | Сверять имя в доке |
| Новые vs вернувшиеся | Метрики/сегментация «новый посетитель» (справочник) | См. разделы preset **Посетители** |

Соцдем (пол, возраст) в API может быть **ограничен** из-за порога выборки — смотреть **`contains_sensitive_data`**.

---

## D. Контент и поведение на сайте

| Как могут спросить | Что делать | Примечание |
|--------------------|------------|------------|
| Топ страниц по просмотрам | `ym:pv:URL` + `ym:pv:pageviews`, сортировка | Сценарий в `SKILL.md` |
| Входные страницы / лендинги | Группировки уровня **визита** (вход), не путать с хитами | Справочник **Содержание** |
| Глубина просмотра, время, отказы | Метрики визита из справочника | Фильтр «глубина > N»: [пример](https://yandex.ru/dev/metrika/ru/stat/examples#page-view) |
| Поиск по сайту | Пресеты **Содержание** | [preset_content](https://yandex.ru/dev/metrika/ru/stat/presets/preset_content) |
| Загрузки файлов | Метрики/группировки «Загрузки» (обновления API 2025) | `docs/09-changelog-highlights.md` |
| Контентная аналитика (статьи, авторы, рубрики) | `preset=publishers_*` | [Примеры](https://yandex.ru/dev/metrika/ru/stat/examples#ex5) |

---

## E. Цели, конверсии, деньги

| Как могут спросить | Что делать | Примечание |
|--------------------|------------|------------|
| Конверсия по цели / сколько достигли цели | Метрики целей в `stat/v1/data` + `filters` по цели | [Пример конверсии](https://yandex.ru/dev/metrika/ru/stat/examples#conv), несколько целей: [conv-mult](https://yandex.ru/dev/metrika/ru/stat/examples#conv-mult) |
| Список целей счётчика, id цели | `GET .../management/v1/counter/{id}/goals` | `docs/08-management-quickstart.md` |
| Создать / изменить цель | `POST`/`PUT` goals в management | OpenAPI в доке management |
| E-commerce: заказы, товары, выручка | Если данные передаются в Метрику — метрики ecommerce из справочника | [Справка ecommerce](https://yandex.ru/support/metrica/ru/ecommerce/data.html); пресеты монетизации при необходимости |

---

## F. Сегментация и «дрельдаун»

| Как могут спросить | Что делать | Примечание |
|--------------------|------------|------------|
| Только органика из Москвы | `filters` на источник + регион | Комбинировать условия, `lang=ru` |
| Сложные условия | Параметр `filters`, лимиты длины и числа условий | `docs/05-reports-api-stat.md`, [сегментация](https://yandex.ru/dev/metrika/ru/stat/segmentation) |
| Дерево отчёта (как в интерфейсе) | `stat/v1/data/drilldown` | [Пример ОС](https://yandex.ru/dev/metrika/ru/stat/examples#drilldown1) |

---

## G. Выгрузка, точность, лимиты

| Как могут спросить | Что делать | Примечание |
|--------------------|------------|------------|
| В Excel / CSV | Суффикс `.csv` в пути `.../data.csv?...` | `docs/05-reports-api-stat.md` |
| Данные «как в интерфейсе» не сходятся | Объяснить семплирование (`accuracy`), таймзону (`timezone`), задержку обработки | Logs vs отчёты — см. FAQ в `docs/06-logs-api.md` |
| Слишком долго / 429 | Квоты, реже дергать `/stat/v1/data/` | `docs/04-quotas.md` |

---

## H. Сырые данные и импорт (продвинутые)

| Как могут спросить | Что делать | Примечание |
|--------------------|------------|------------|
| Выгрузить сырые визиты/хиты | Logs API: create → poll → download → **clean** | `docs/06-logs-api.md` |
| Связать с ClickHouse | Интеграция из доки | `docs/06-logs-api.md` |
| Загрузить расходы на рекламу | Импорт расходов (multipart) | `docs/07-data-import.md` |
| Офлайн-конверсии, CRM, звонки | Импорт офлайн / CRM / calls | `docs/07-data-import.md` |

---

## I. Управление счётчиком и доступы

| Как могут спросить | Что делать | Примечание |
|--------------------|------------|------------|
| Какие счётчики есть / id сайта | `GET .../management/v1/counters` | `search_string`, `docs/08-management-quickstart.md` |
| Выдать доступ коллеге | Grants / представители в management | Справка по доступам + OpenAPI |
| Счётчик не собирает данные | `GET` параметры счётчика, `code_status`, проверка кода на сайте | Частично [справка Метрики](https://yandex.ru/support/metrica/), не всё через API |

---

## J. Что пользователи спрашивают, но API отчётов не заменяет полностью

| Тема | Как отвечать агенту |
|------|---------------------|
| **Вебвизор** (записи сессий, карты кликов) | В основном интерфейс Метрики; в API — ограниченно, не обещать полный паритет |
| **Онлайн в реальном времени** | Уточнить: в UI есть «сейчас»; в отчётном API — задержки и агрегация по правилам Метрики |
| **SEO-аудит «сделай за меня»** | API даёт метрики; интерпретация и рекомендации — зона аналитика, не самого API |
| **Юридическая интерпретация GDPR** | Отсылка к политике Яндекса и настройкам счётчика |
| **Почему упали продажи вне сайта** | Метрика не видит всё; только связанные данные и импорты |

---

## Ключевые URL

- Примеры запросов: https://yandex.ru/dev/metrika/ru/stat/examples  
- Шаблоны отчётов: https://yandex.ru/dev/metrika/ru/stat/presets  
- Сегментация: https://yandex.ru/dev/metrika/ru/stat/segmentation  
- Хаб API: https://yandex.ru/dev/metrika  
