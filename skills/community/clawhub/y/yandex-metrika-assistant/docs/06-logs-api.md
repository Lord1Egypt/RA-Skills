# Logs API (неагрегированные данные)

Введение: https://yandex.ru/dev/metrika/ru/logs/  
Сценарий (quick start): https://yandex.ru/dev/metrika/ru/logs/practice/quick-start  
Авторизация (раздел logs): https://yandex.ru/dev/metrika/ru/logs/ (ссылка на intro/authorization)  
Квоты logs: https://yandex.ru/dev/metrika/ru/intro/quotas + общий раздел «Ограничения» на странице logs

## Назначение

Выгрузка **неагрегированных** данных, собираемых Метрикой; для самостоятельной обработки и нестандартной аналитики.

## Авторизация и квоты

- В каждом запросе — **OAuth-токен** (как для остального API).
- Отдельные **квоты Logs API**: с одного IP **10 запросов в секунду** (см. `04-quotas.md`).
- Общие суточные и параллельные лимиты пользователя также применяются.

## Хранение и актуальность

- Данные визитов **дозаполняются**; ~**99% визитов** завершаются в течение **3 дней** после начала.
- Статистика за **текущий день** может быть неполной — рекомендуют запрашивать **со вчера и раньше**.
- **Общий объём** данных логов на **один счётчик** (включая не удалённые логи): **10 ГБ**.

## Ограничения запросов (из введения logs)

| Ограничение | Значение |
|-------------|----------|
| Период в одном запросе | **Не более 1 года** |
| Длина параметра `fields` (список полей) | **Не более 3000 символов** |
| Квота хранилища логов на счётчик | **10 ГБ** суммарно (подготовленные + не удалённые) |

Освобождение места: регулярно удалять подготовленные и скачанные логи — метод **clean** (ниже).

Текущее занятое место: **GET** список log requests и суммировать поле **`size`** в ответах.  
Список: https://yandex.ru/dev/metrika/ru/logs/openapi/getLogRequests  
Clean: https://yandex.ru/dev/metrika/ru/logs/openapi/clean

## Увеличение квоты

Подключить **Метрику Про**: https://yandex.ru/support/metrica/pro/intro.html?lang=ru

## Сценарий работы (management + logs)

База URL: `https://api-metrika.yandex.net/management/v1/...`

1. **Оценка** (опционально):  
   `GET /counter/{counterId}/logrequests/evaluate`  
   https://yandex.ru/dev/metrika/ru/logs/openapi/evaluate

2. **Создать задание на выгрузку**:  
   `POST /counter/{counterId}/logrequests`  
   https://yandex.ru/dev/metrika/ru/logs/openapi/createLogRequest  
   Сохранить **`request_id`**.

3. **Статус**:  
   `GET /counter/{counterId}/logrequest/{requestId}`  
   https://yandex.ru/dev/metrika/ru/logs/openapi/getLogRequest  
   Когда статус **`processed`** — файл готов.

4. **Скачать часть**:  
   `GET /counter/{counterId}/logrequest/{requestId}/part/{partNumber}/download`  
   https://yandex.ru/dev/metrika/ru/logs/openapi/download

5. **Очистить** после выгрузки:  
   `POST /counter/{counterId}/logrequest/{requestId}/clean`  
   https://yandex.ru/dev/metrika/ru/logs/openapi/clean

Запросы обрабатываются **в очереди**; новый запрос в конец. Если статус **`created`**, ждать. При неудаче — повторить в другое время.

## ClickHouse / облако

Страница в доке Метрики: https://yandex.ru/dev/metrika/ru/logs/clickhouse-integration  

Практическая инструкция выгрузки (Yandex Cloud / DataLens):  
https://cloud.yandex.ru/docs/datalens/tutorials/data-from-metrica-yc-visualization#uploading-data-logs-api

## Расхождения с интерфейсом и числа с плавающей точкой

В интерфейсе — дополнительные алгоритмы обработки. В логах числа по **IEEE 754**; для ряда полей используются **коэффициенты** (см. FAQ на странице logs), например:

| Поле | Коэффициент |
|------|-------------|
| `ym:s:purchaseRevenue` | 1 (также в API отчётов) |
| `ym:s:goalsPrice` | 1000 |
| `ym:s:productsPrice`, `ym:s:impressionsProductPrice`, `ym:s:purchaseTax`, `ym:s:eventsProductPrice` | 1 000 000 |

## Переименования полей (changelog 15.10.2025)

В **визитах**:

- `ym:s:eventsProduct` → **`ym:s:product`**
- `ym:s:products` → **`ym:s:purchasedProduct`**

Старые имена пока выгружаются, поддержка будет прекращена.

В **событиях**: добавлены поля с массивами по e-commerce и звонкам; офлайн-конверсии — поле **`ym:pv:goalsID`**.

Для Метрики Про в визитах: поле **`ym:s:isRobotPro`** (и в Data Streaming — см. changelog).
