# Workflow: интеграция SmartCaptcha на сайт (HTML + backend)

Читай этот файл, когда нужно добавить капчу на классический сайт: HTML-страницы с формами и серверная часть на любом стеке. Для React/SPA используй [integrate-react.md](integrate-react.md), для мобильных приложений — [integrate-mobile.md](integrate-mobile.md).

## Шаги

1. **Получи ключи капчи.**
   Справка: [../docs/keys.md](../docs/keys.md). Если капчи ещё нет — сначала выполни [setup-captcha.md](setup-captcha.md).
   Убедись, что домен сайта есть в списке разрешённых сайтов капчи (иначе виджет не отобразится) — настройки в [../docs/captcha-settings.md](../docs/captcha-settings.md).
   *Готово:* есть ключ клиента (`ysc1_...`) для страницы и ключ сервера (`ysc2_...`) в секретах бэкенда.

2. **Выбери метод подключения виджета.**
   Обзор и критерии: [../docs/overview.md](../docs/overview.md).
   - **Автоматический** ([../docs/widget-auto.md](../docs/widget-auto.md)) — по умолчанию для обычной формы: скрипт сам находит `div` с классом `smart-captcha`, токен попадает в форму как скрытый `input name="smart-token"`. Минимум кода.
   - **Расширенный** ([../docs/widget-advanced.md](../docs/widget-advanced.md)) — когда нужен контроль: колбэк с токеном, программная отрисовка (`window.smartCaptcha.render`), подписка на события, несколько виджетов, сброс состояния.
   - **Невидимая капча** ([../docs/invisible-captcha.md](../docs/invisible-captcha.md)) — когда кнопка **Я не робот** нежелательна в UI; подключается только расширенным методом, проверка запускается через `window.smartCaptcha.execute()` (например, по submit формы). Требует уведомления пользователей об обработке данных.
   *Готово:* метод выбран; для невидимой капчи пользователь понимает требование об уведомлении.

3. **Добавь виджет на страницу по шаблону.**
   Шаблоны: [../templates/widget-auto.html](../templates/widget-auto.html), [../templates/widget-advanced.html](../templates/widget-advanced.html), [../templates/invisible.html](../templates/invisible.html). Параметры — [../references/widget-params.md](../references/widget-params.md), методы/события — [../references/js-api.md](../references/js-api.md).
   Подставь `<ключ_клиента>` пользователя. Скрипт виджета: `https://smartcaptcha.yandexcloud.net/captcha.js`.

   > **Важно.** При загрузке виджет меняет высоту контейнера на `100px`. Чтобы избежать «скачка» вёрстки, задай контейнеру `style="height: 100px"` заранее.

   *Готово:* виджет встроен в форму.
   *Проверка:* на странице появилась кнопка **Я не робот** (для невидимой — блок с уведомлением об обработке данных в углу страницы); ошибок в консоли браузера нет.

4. **Передай токен на бэкенд.**
   - Автоматический метод: токен уже в POST-данных формы в поле `smart-token` (скрытый `<input type="hidden" name="smart-token" value="<токен>">` внутри контейнера виджета).
   - Расширенный/невидимый: токен приходит в `callback(token)` — положи его в скрытое поле формы или отправь вместе с данными запроса.
   *Готово:* обработчик формы на сервере получает токен.
   *Проверка:* залогируй тело запроса — поле с токеном непустое после прохождения капчи.

5. **Реализуй серверную проверку токена.**
   Справка: [../docs/server-validation.md](../docs/server-validation.md), формат запроса/ответов — [../references/validate-api.md](../references/validate-api.md).
   Возьми шаблон под стек: Python — [../templates/validate.py](../templates/validate.py), Node.js — [../templates/validate.js](../templates/validate.js), PHP — [../templates/validate.php](../templates/validate.php).
   Логика: POST на `https://smartcaptcha.yandexcloud.net/validate` (`x-www-form-urlencoded`: `secret`, `token`, `ip`); решение принимай только по полю `status` (`ok`/`failed`), поле `message` — только для диагностики.

   > **Важно.** Токен одноразовый и живёт 5 минут. При HTTP-коде ответа не 200 рекомендуется fail-open — пропустить пользователя, чтобы сбой сервиса не блокировал сайт.

   *Готово:* обработчик формы валидирует токен до выполнения бизнес-логики; серверный ключ читается из переменной окружения/секретов.
   *Проверка:* запрос с пустым/поддельным токеном получает отказ (`"status": "failed"`, `Invalid or expired Token`), с настоящим — проходит.

6. **Протестируй интеграцию.**
   Типичные проблемы: [../docs/troubleshooting.md](../docs/troubleshooting.md).
   - Проверь токен вручную: `python scripts/check_token.py --secret <ключ_сервера> --token <токен>` ([../scripts/check_token.py](../scripts/check_token.py)) — токен возьми со страницы; `--secret` можно опустить, если задана переменная окружения `SMARTCAPTCHA_SERVER_KEY`.
   - Открой страницу в режиме инкогнито или через VPN — так выше вероятность получить задание, а не мгновенный пропуск.
   - Для гарантированного показа задания используй тестовый режим (`test: true` в расширенном методе) — только на время отладки.
   - Проверь повторную отправку той же формы: второй запрос с тем же токеном должен отклоняться.
   *Готово:* полный цикл «виджет → токен → /validate → решение» работает; задание отображается и решается.

7. **Пройди чеклист безопасности.**
   - Серверный ключ не встречается во фронтенд-коде, шаблонах и репозитории ([../docs/keys.md](../docs/keys.md)).
   - Проверка токена выполняется на сервере при каждом защищаемом действии; фронтенд-валидации недостаточно.
   - Ответ обрабатывается по `status`, а не по `message`.
   - При событии `javascript-error` успех не засчитывается — это потенциальная уязвимость ([../references/js-api.md](../references/js-api.md)).
   - Для невидимой капчи: если блок с уведомлением скрыт (`hideShield`), пользователи уведомлены об обработке данных другим способом.
   *Готово:* все пункты подтверждены.

## См. также

- [setup-captcha.md](setup-captcha.md) — создание капчи и получение ключей
- [../docs/widget-auto.md](../docs/widget-auto.md), [../docs/widget-advanced.md](../docs/widget-advanced.md), [../docs/invisible-captcha.md](../docs/invisible-captcha.md) — методы подключения виджета
- [../docs/server-validation.md](../docs/server-validation.md), [../references/validate-api.md](../references/validate-api.md) — проверка токена
- [../docs/troubleshooting.md](../docs/troubleshooting.md) — если капча не отображается или не проходит проверку
- Официальная документация: [быстрый старт](https://yandex.cloud/ru/docs/smartcaptcha/quickstart), [методы виджета](https://yandex.cloud/ru/docs/smartcaptcha/concepts/widget-methods), [невидимая капча](https://yandex.cloud/ru/docs/smartcaptcha/concepts/invisible-captcha), [проверка капчи](https://yandex.cloud/ru/docs/smartcaptcha/operations/validate-captcha)
