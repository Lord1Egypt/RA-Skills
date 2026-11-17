# Расширенный метод подключения виджета SmartCaptcha

Читайте этот файл, когда автоматической вставки `div.smart-captcha` недостаточно: нужно самому управлять моментом загрузки и отрисовки виджета, получать токен в JavaScript-коде, отрисовывать несколько виджетов или отправлять токен на бэкенд без HTML-формы. Про автоматический метод — [widget-auto.md](./widget-auto.md).

## Когда нужен расширенный метод

Выбирайте расширенный метод, если хотя бы одно верно:

* Нужно контролировать момент загрузки скрипта и отрисовки виджета (модальные окна, SPA, отложенная загрузка).
* Нужен токен в JS-коде — например, чтобы отправить его `fetch`-запросом без классической формы.
* На странице несколько виджетов (несколько форм).
* Нужно управлять жизненным циклом виджета: сбрасывать (`reset`) или удалять (`destroy`).
* Используется [невидимая капча](./invisible-captcha.md) — она подключается только расширенным методом с параметром `invisible` и запуском проверки через `execute`.

Если у вас одна статичная форма и токен достаточно передать в POST формы — быстрее использовать [автоматический метод](./widget-auto.md).

## Шаг 1. Подключите скрипт с параметром render=onload

Разместите в любом месте страницы (например, в `<head>`):

```html
<script
    src="https://smartcaptcha.yandexcloud.net/captcha.js?render=onload&onload=onloadFunction"
    defer
></script>
```

В параметре `onload` передаётся имя глобальной callback-функции: скрипт вызовет её после своей загрузки. Именно в этой функции вы отрисовываете виджет. После загрузки скрипта появляется доступ к объекту `window.smartCaptcha` с методами для работы с виджетом.

## Шаг 2. Добавьте пустой контейнер

```html
<div id="<идентификатор_контейнера>" style="height: 100px"></div>
```

Где `id` — произвольный идентификатор.

> **Важно.** При загрузке виджет меняет высоту контейнера на `100px`. Чтобы избежать «скачка» вёрстки, задайте контейнеру высоту `100px` заранее (как в примере выше).

## Шаг 3. Отрисуйте виджет: window.smartCaptcha.render

```html
<script>
    let widgetId; // объявите во внешней области видимости, чтобы идентификатор был доступен другим функциям (reset, getResponse и т. д.)

    function onloadFunction() {
        if (window.smartCaptcha) {
            const container = document.getElementById('<идентификатор_контейнера>');

            widgetId = window.smartCaptcha.render(container, {
                sitekey: '<ключ_клиента>',
                hl: 'ru',
            });
        }
    }
</script>
```

Обязательно проверяйте существование `window.smartCaptcha`: это защищает от ошибки, если функция будет вызвана до завершения загрузки JS-скрипта.

Сигнатура метода:

```ts
(container: HTMLElement | string, params) => WidgetId;
```

* `container` — DOM-элемент или строка с идентификатором контейнера.
* `params` — объект параметров. Ключевые: `sitekey` (ключ клиентской части, см. [keys.md](./keys.md)), `callback` (обработчик токена), `hl` (язык: `'ru' | 'en' | 'be' | 'kk' | 'tt' | 'uk' | 'uz' | 'tr'`), `test` (режим тестирования — задание показывается всегда; только для отладки), `webview` (для мобильных приложений), `invisible` (невидимая капча), `shieldPosition` / `hideShield` (блок с уведомлением об обработке данных), `metadata` (собственные данные для [правил показа](./captcha-settings.md) вариантов заданий, до 512 символов). Полная таблица параметров — в [../references/widget-params.md](../references/widget-params.md).
* Возвращает `widgetId` — уникальный идентификатор виджета. Сохраните его: он нужен для `getResponse`, `reset`, `destroy` и `subscribe`.

> **Важно.** Вы обязаны уведомлять пользователей о том, что их данные обрабатывает SmartCaptcha. Если скрываете блок с уведомлением (`hideShield`), сообщите об обработке данных иным способом.

## Получение токена: параметр callback

Передайте в `render` функцию `callback: (token: string) => void` — она вызывается при успешной проверке пользователя и получает токен. Типовой паттерн: сохранить токен и разблокировать кнопку отправки.

```js
function onCaptchaSuccess(token) {
    capchaToken = token; // сохраните для отправки на бэкенд
    document.getElementById('submit-btn').disabled = !token;
}
```

Альтернатива — метод `window.smartCaptcha.getResponse(widgetId)`: возвращает текущее значение токена пользователя. За событиями виджета (`success`, `token-expired`, `javascript-error` и др.) можно следить через `subscribe` — см. [../references/js-api.md](../references/js-api.md).

Токен одноразовый и живёт ограниченное время, поэтому получайте его непосредственно перед отправкой и всегда проверяйте на бэкенде — см. [server-validation.md](./server-validation.md).

## Управление жизненным циклом виджета

Все методы принимают `widgetId`; если аргумент не передан, метод применяется к первому отрисованному виджету.

* `reset(widgetId)` — сбрасывает состояние виджета до начального. Вызывайте после каждой отправки токена на бэкенд (токен одноразовый) и при событии `token-expired`, чтобы пользователь мог пройти проверку заново.
* `destroy(widgetId)` — удаляет виджет и созданные им обработчики. Обязателен в SPA при размонтировании компонента, иначе обработчики останутся в памяти.
* `getResponse(widgetId)` — возвращает текущее значение токена пользователя.
* `execute(widgetId)` — запускает проверку пользователя; используется для [невидимой капчи](./invisible-captcha.md).

Полное описание методов и событий — в [../references/js-api.md](../references/js-api.md).

## Несколько виджетов на странице

Каждый вызов `render` возвращает свой `widgetId`. Сохраняйте идентификаторы и передавайте их в `getResponse` / `reset` / `destroy` явно — без аргумента методы работают только с первым отрисованным виджетом, что при нескольких виджетах даст не тот результат.

```js
let loginWidgetId, feedbackWidgetId;

function onloadFunction() {
    if (!window.smartCaptcha) {
        return;
    }
    loginWidgetId = window.smartCaptcha.render('login-captcha', {
        sitekey: '<ключ_клиента>',
        callback: (token) => sendLogin(token),
    });
    feedbackWidgetId = window.smartCaptcha.render('feedback-captcha', {
        sitekey: '<ключ_клиента>',
        callback: (token) => sendFeedback(token),
    });
}

// Сбросить конкретный виджет после использования его токена:
window.smartCaptcha.reset(loginWidgetId);
```

## Отправка токена на бэкенд без формы (fetch)

Токен, полученный в `callback`, отправьте на свой бэкенд любым способом — например, в JSON-теле `fetch`-запроса. Бэкенд обязан проверить токен запросом к `/validate` (см. [server-validation.md](./server-validation.md)); проверка на клиенте ничего не гарантирует.

```js
async function submitForm() {
    const response = await fetch('/api/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            user: document.getElementById('username').value,
            'smart-token': capchaToken,
        }),
    });

    // Токен одноразовый: после отправки сбросьте виджет,
    // чтобы при повторной попытке пользователь получил новый токен.
    window.smartCaptcha.reset(widgetId);
    capchaToken = null;

    return response.json();
}
```

## Отложенная загрузка скрипта

Чтобы не загружать капчу до нужного момента (например, до открытия модального окна с формой), создавайте тег `<script>` динамически и обрабатывайте ошибку загрузки:

```js
window.onloadFunction = () => {
    if (window.smartCaptcha) {
        // Создание капчи: window.smartCaptcha.render(...)
    }
};

function handleScriptLoadingError() {
    // Обработка ошибок загрузки скрипта
}

const scriptElement = document.createElement('script');
scriptElement.src = 'https://smartcaptcha.yandexcloud.net/captcha.js?render=onload&onload=onloadFunction';
scriptElement.onerror = handleScriptLoadingError;
document.body.appendChild(scriptElement);
```

Функция из параметра `onload` должна быть глобальной (`window.onloadFunction`) и объявленной до загрузки скрипта.

Готовая страница со всеми элементами (отложенная загрузка, `render` с `callback`, отправка `fetch`) — [../templates/widget-advanced.html](../templates/widget-advanced.html).

## См. также

* [../references/widget-params.md](../references/widget-params.md) — полная таблица параметров `render()` и data-атрибутов.
* [../references/js-api.md](../references/js-api.md) — все методы и события `window.smartCaptcha` (включая `subscribe`).
* [./widget-auto.md](./widget-auto.md) — автоматический метод подключения.
* [./invisible-captcha.md](./invisible-captcha.md) — невидимая капча (`invisible` + `execute`).
* [./server-validation.md](./server-validation.md) — обязательная проверка токена на бэкенде.
* [../templates/widget-advanced.html](../templates/widget-advanced.html) — готовый шаблон страницы.
* [../workflows/integrate-website.md](../workflows/integrate-website.md) — пошаговая интеграция на сайт.
* Официальная документация: [Добавить виджет расширенным методом](https://yandex.cloud/ru/docs/smartcaptcha/operations/advanced-method), [Методы установки виджета](https://yandex.cloud/ru/docs/smartcaptcha/concepts/widget-methods).
