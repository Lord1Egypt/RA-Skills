# Workflow: интеграция SmartCaptcha в React/SPA

Читай этот файл, когда капчу нужно встроить в React-приложение (SPA, Next.js и т.п.) через npm-пакет `@yandex/smart-captcha`. Для классического сайта без React используй [integrate-website.md](integrate-website.md), для мобильных приложений — [integrate-mobile.md](integrate-mobile.md).

## Шаги

1. **Получи ключи капчи.**
   Справка: [../docs/keys.md](../docs/keys.md). Если капчи ещё нет — сначала выполни [setup-captcha.md](setup-captcha.md).
   Убедись, что домен приложения есть в списке разрешённых сайтов капчи — иначе виджет не отобразится ([../docs/captcha-settings.md](../docs/captcha-settings.md)).
   *Готово:* ключ клиента (`ysc1_...`) доступен фронтенду, ключ сервера (`ysc2_...`) — только бэкенду (секреты/переменные окружения).

2. **Установи пакет `@yandex/smart-captcha`.**
   Справка: [../docs/react.md](../docs/react.md).
   Под менеджер пакетов проекта: `npm i -PE @yandex/smart-captcha`, `yarn add @yandex/smart-captcha` или `pnpm add @yandex/smart-captcha`. Отдельный тег `<script src="https://smartcaptcha.yandexcloud.net/captcha.js">` подключать не нужно — в официальных примерах для React он не используется, подключение виджета берут на себя компоненты пакета.
   *Готово:* пакет в `dependencies`.
   *Проверка:* `import { SmartCaptcha } from '@yandex/smart-captcha'` резолвится, сборка проходит.

3. **Выбери компонент.**
   Справка: [../docs/react.md](../docs/react.md), концепция невидимой капчи — [../docs/invisible-captcha.md](../docs/invisible-captcha.md).
   - **`SmartCaptcha`** — по умолчанию: виджет с кнопкой **Я не робот**, проверка запускается кликом пользователя.
   - **`InvisibleSmartCaptcha`** — когда кнопка нежелательна в UI: проверка запускается из кода переключением свойства `visible` в `true` (например, по submit формы). Требует уведомления пользователей об обработке данных, если блок-уведомление скрыт (`hideShield`).
   *Готово:* компонент выбран; для невидимой капчи пользователь понимает требование об уведомлении.

4. **Добавь компонент по шаблону.**
   Шаблоны: обычная капча — [../templates/SmartCaptchaField.tsx](../templates/SmartCaptchaField.tsx), невидимая — [../templates/InvisibleCaptchaForm.tsx](../templates/InvisibleCaptchaForm.tsx). Полная таблица свойств — в [../docs/react.md](../docs/react.md), соответствие параметрам виджета — [../references/widget-params.md](../references/widget-params.md).
   Подставь `sitekey="<ключ_клиента>"`.
   *Готово:* компонент встроен в форму.
   *Проверка:* для `SmartCaptcha` на странице появилась кнопка **Я не робот**; для `InvisibleSmartCaptcha` кнопки нет, но виден блок с уведомлением об обработке данных; ошибок в консоли браузера нет.

5. **Обработай события и жизненный цикл токена.**
   Справка: [../docs/react.md](../docs/react.md), события виджета — [../references/js-api.md](../references/js-api.md).
   - `onSuccess(token)` — сохрани токен в состоянии; блокируй отправку формы, пока токена нет (`disabled={!token}`).
   - `onTokenExpired` — очищай токен (`setToken('')`): протухший токен не пройдёт серверную проверку.
   - `onJavascriptError` — не засчитывай успех, сообщи пользователю об ошибке (иначе — потенциальная уязвимость).
   - Для `InvisibleSmartCaptcha` в `onChallengeHidden` сбрасывай `visible` в `false` — иначе повторный submit не запустит проверку.
   - Сброс после каждой отправки формы: перемонтируй компонент сменой `key` — токен одноразовый, повторный запрос с тем же токеном `/validate` отклонит.
   *Готово:* все колбэки подключены, сброс по `key` реализован.

6. **Отправь токен на бэкенд и реализуй проверку.**
   Справка: [../docs/server-validation.md](../docs/server-validation.md), формат запроса/ответов — [../references/validate-api.md](../references/validate-api.md).
   Отправляй токен вместе с данными формы (например, поле `smart-token` в JSON). На сервере возьми шаблон под стек: [../templates/validate.py](../templates/validate.py), [../templates/validate.js](../templates/validate.js), [../templates/validate.php](../templates/validate.php). Логика: POST `https://smartcaptcha.yandexcloud.net/validate` (`x-www-form-urlencoded`: `secret`, `token`, `ip`); решение — только по полю `status`.

   > **Важно.** Токен одноразовый и живёт 5 минут. При HTTP-коде ответа не 200 рекомендуется fail-open — пропустить пользователя.

   *Готово:* защищаемый API-эндпоинт валидирует токен до бизнес-логики.
   *Проверка:* запрос без токена или с поддельным токеном получает отказ (`"status": "failed"`), с настоящим — проходит.

7. **Протестируй интеграцию.**
   Типичные проблемы: [../docs/troubleshooting.md](../docs/troubleshooting.md).
   - Проверь токен вручную: `python scripts/check_token.py --token <токен>` ([../scripts/check_token.py](../scripts/check_token.py)).
   - Открой приложение в режиме инкогнито или через VPN — выше вероятность получить задание.
   - Для гарантированного показа задания включи свойство `test` — только на время отладки, убери перед продакшеном.
   - Отправь форму дважды: второй запрос должен уйти с новым токеном (сброс по `key` сработал), а повтор старого токена — отклоняться.
   *Готово:* полный цикл «компонент → `onSuccess` → API → `/validate` → решение» работает.

8. **Пройди чеклист безопасности.**
   - Серверный ключ не попал во фронтенд: поиск `ysc2_` по бандлу/репозиторию пуст ([../docs/keys.md](../docs/keys.md)).
   - Проверка токена — на сервере при каждом защищаемом действии; наличие токена на клиенте ничего не гарантирует.
   - Ответ `/validate` обрабатывается по `status`, `message` — только для диагностики.
   - При `onJavascriptError` успех не засчитывается.
   - Если используется `hideShield` — пользователи уведомлены об обработке данных другим способом.
   *Готово:* все пункты подтверждены.

## См. также

- [setup-captcha.md](setup-captcha.md) — создание капчи и получение ключей
- [integrate-website.md](integrate-website.md) — тот же сценарий без React (HTML + backend)
- [../docs/react.md](../docs/react.md) — свойства компонентов, события, сброс состояния
- [../docs/server-validation.md](../docs/server-validation.md), [../references/validate-api.md](../references/validate-api.md) — проверка токена
- [../docs/troubleshooting.md](../docs/troubleshooting.md) — если виджет не отображается или проверка не проходит
- Официальная документация: [React-компоненты](https://yandex.cloud/ru/docs/smartcaptcha/concepts/react), [проверка капчи](https://yandex.cloud/ru/docs/smartcaptcha/operations/validate-captcha)
