# API импорта данных

Введение: https://yandex.ru/dev/metrika/ru/data-import/index

Импорт дополняет данные счётчика: сквозная аналитика, расходы по каналам, связь офлайн-действий с визитами и т.д.

## Типы импорта и ссылки в документацию

### Офлайн-конверсии

Действия пользователя вне сайта (оплата после заявки и т.п.), связь с визитами.

- Подробнее: https://yandex.ru/dev/metrika/ru/data-import/management/offline-conv

### Чаты

Чаты в мессенджерах, связь с визитами; цели и отчёты.

- Подробнее: https://yandex.ru/dev/metrika/ru/data-import/management/chats-transfer-data

### CRM

Клиенты и заказы.

- Подробнее: https://yandex.ru/dev/metrika/ru/data-import/data-import/contacts

### Звонки

- Подробнее: https://yandex.ru/dev/metrika/ru/data-import/management/calls

### Расходы

- Multipart: https://yandex.ru/dev/metrika/ru/data-import/management/openapi/expense/uploadMultipart

### Параметры посетителей

- Upload: https://yandex.ru/dev/metrika/ru/data-import/management/openapi/user_params/upload

## Права

Для загрузок обычно нужен **`metrika:write`** (или узкие scopes из `03-auth-oauth.md`).

## Связанные темы в changelog

- **Measurement Protocol**: см. https://yandex.ru/dev/metrika/ru/data-import/measurement-about  
- Параметры счётчика **`measurement_tokens`**, **`measurement_enabled`** (обновление API управления, см. `09-changelog-highlights.md`).
