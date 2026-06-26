# Базовый URL и структура API

Источник: https://yandex.ru/dev/metrika/ru/intro/method-call  
Версионирование: https://yandex.ru/dev/metrika/ru/intro/versions

## Протокол и хост

- Запросы только по **HTTPS**.
- Хост: **`api-metrika.yandex.net`**

## Шаблон запроса

```
<METHOD> https://api-metrika.yandex.net/<раздел_API>/<версия>/<имя_метода>.<формат_результата>?<параметры>
```

- **METHOD** — GET, POST, PUT, DELETE (в зависимости от ресурса).
- **раздел_API**:
  - `management` — API управления и часть операций **Logs API**
  - `stat` — API отчётов
  - `analytics` — API, совместимое с **Google Analytics Core Reporting API**
- **версия** — например `v1`, `v2` (указывать явно).
- **имя_метода** — путь ресурса.
- **формат_результата** — опционально; по умолчанию часто JSON.
- **параметры** — query и/или тело для POST/PUT.

## Примеры с версиями

```
https://api-metrika.yandex.net/stat/v1/data?id=...
https://api-metrika.yandex.net/stat/v2/data?id=...
```

## REST-модель

Ресурсы адресуются уникальными URL; операции: чтение (GET), запись (PUT), удаление (DELETE), добавление в коллекции (POST).

## Виды API (введение)

См. https://yandex.ru/dev/metrika/ru/

1. **API управления** — счётчики, цели, фильтры, доступы, представители и др.  
   https://yandex.ru/dev/metrika/ru/management/
2. **API импорта данных** — расходы, CRM, звонки, офлайн-конверсии, параметры посетителей.  
   https://yandex.ru/dev/metrika/ru/data-import/index
3. **API отчётов** — агрегированная статистика, сегментация.  
   https://yandex.ru/dev/metrika/ru/stat/
4. **Logs API** — неагрегированные данные.  
   https://yandex.ru/dev/metrika/ru/logs/
