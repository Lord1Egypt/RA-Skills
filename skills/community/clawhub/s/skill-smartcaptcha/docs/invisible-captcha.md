# Невидимая капча

Читай этот файл, когда нужно подключить SmartCaptcha без кнопки «Я не робот»: проверка запускается кодом по событию (обычно по отправке формы), а окно с заданием видят только подозрительные пользователи.

## Что это и чем отличается от обычной капчи

Невидимая капча — способ подключения виджета SmartCaptcha, при котором кнопка **Я не робот** отсутствует на странице. Окно с заданием увидят только те пользователи, чьи запросы сервис SmartCaptcha посчитает подозрительными. Разработчик сам выбирает момент проверки — например, клик по **submit** формы.

Ключевые отличия от обычного виджета:

| | Обычный виджет | Невидимая капча |
|---|---|---|
| Кнопка «Я не робот» | Есть, пользователь кликает сам | Нет |
| Запуск проверки | Клик пользователя по кнопке | Вызов `window.smartCaptcha.execute()` из вашего кода |
| Метод подключения | Автоматический или расширенный | **Только расширенный** (см. [widget-advanced.md](widget-advanced.md)) |
| Потребление памяти | Больше | Меньше — не загружается код отрисовки кнопки |

Невидимая капча включается параметром `invisible: true` в методе `render`. Полученный токен всё равно нужно проверить на сервере через `/validate` — см. [server-validation.md](server-validation.md).

## Алгоритм подключения

### 1. Загрузите скрипт расширенным методом

```html
<script
  src="https://smartcaptcha.yandexcloud.net/captcha.js?render=onload&onload=onloadFunction"
  defer
></script>
```

В параметре `onload` передаётся имя вашей функции инициализации — она вызовется, когда скрипт загрузится и объект `window.smartCaptcha` станет доступен.

### 2. Отрисуйте виджет с `invisible: true`

```html
<form id="form" method="POST" action="/login">
  <div id="captcha-container"></div>
  <input type="submit" />
</form>

<script>
const form = document.getElementById('form');

function onloadFunction() {
  if (!window.smartCaptcha) {
    return; // защита от вызова до загрузки скрипта
  }

  window.smartCaptcha.render('captcha-container', {
    sitekey: '<ключ_клиента>',
    invisible: true, // сделать капчу невидимой
    callback: callback,
  });
}

function callback(token) {
  form.submit();
}
</script>
```

Токен приходит через `callback` (или событие `success` метода `subscribe`) — после успешной проверки; текущее значение токена также можно получить методом `window.smartCaptcha.getResponse()`. Внутри `callback` обычно передают токен на сервер и отправляют форму.

### 3. Вызовите `execute()` по событию

Метод `execute` запускает проверку пользователя. Вызывайте его в момент, когда проверка нужна, — обычно в обработчике отправки формы:

```js
function handleSubmit(event) {
  event.preventDefault(); // не отправлять форму, пока нет токена

  if (!window.smartCaptcha) {
    return;
  }

  window.smartCaptcha.execute();
}
```

Дальше сценарий такой: `execute()` → SmartCaptcha оценивает пользователя (подозрительному показывает задание) → при успехе вызывается `callback(token)` → вы кладёте токен в форму и отправляете её. Полный рабочий пример — [../templates/invisible.html](../templates/invisible.html).

### Несколько виджетов на странице

`render` возвращает `widgetId`. Если на странице больше одного виджета, передавайте его в `execute` явно — иначе проверка запустится на первом отрисованном виджете:

```js
let widgetId;

function onloadFunction() {
  if (!window.smartCaptcha) return;
  widgetId = window.smartCaptcha.render('captcha-container', {
    sitekey: '<ключ_клиента>',
    invisible: true,
    callback: callback,
  });
}

function handleSubmit() {
  if (!window.smartCaptcha) return;
  window.smartCaptcha.execute(widgetId);
}
```

## Уведомление об обработке данных

По умолчанию на странице с невидимой капчей появляется блок со ссылкой на документ «Уведомление об условиях обработки данных сервисом» (https://yandex.ru/legal/smartcaptcha_notice/). Блок располагается в нижнем правом углу.

* Переместить блок — параметр `shieldPosition` метода `render`: `top-left` | `center-left` | `bottom-left` | `top-right` | `center-right` | `bottom-right`.
* Скрыть блок — параметр `hideShield: true`.

```js
window.smartCaptcha.render('captcha-container', {
  sitekey: '<ключ_клиента>',
  invisible: true,
  shieldPosition: 'top-left',
  callback: callback,
});
```

> **Важно.** Вы обязаны уведомлять пользователей о том, что их данные обрабатывает SmartCaptcha. Если скрываете блок через `hideShield`, разместите уведомление об обработке данных SmartCaptcha на странице самостоятельно иным способом. Это юридическое требование, а не опция оформления.

## UX-рекомендации

* **Предупреждайте о возможном показе задания.** У пользователей, которым SmartCaptcha покажет задание, время загрузки виджета может варьироваться. Сообщите пользователю, что после нажатия кнопки может появиться проверка, чтобы ожидание не приводило его в замешательство.
* **Блокируйте повторные клики на время проверки.** Между `execute()` и `callback` проходит время (особенно если показано задание) — дизейбльте кнопку отправки, чтобы пользователь не кликал повторно.
* **Реагируйте на события виджета** через `window.smartCaptcha.subscribe`: `challenge-visible`/`challenge-hidden` — показать/скрыть индикатор проверки, `network-error` — предложить повторить, `token-expired` — токен стал невалидным, нужно пройти проверку заново. Полный список — [../references/js-api.md](../references/js-api.md).
* **Не засчитывайте успех при `javascript-error`.** Это критический сбой JS: сообщите о проблеме пользователю в интерфейсе; засчитывать успешное прохождение при такой ошибке нельзя — это потенциальная уязвимость.

## Типичные ошибки

* **`execute()` вызван до `render()` или до загрузки скрипта.** Объекта `window.smartCaptcha` ещё нет или виджет не отрисован — проверка не запустится. Всегда проверяйте `if (!window.smartCaptcha) return;` и вызывайте `render` только из `onload`-функции скрипта.
* **Повторный `execute()` без сброса состояния.** Токен одноразовый и живёт 5 минут (см. [overview.md](overview.md)). Если пользователь отправляет форму повторно (например, сервер отклонил данные без перезагрузки страницы), сначала вызовите `window.smartCaptcha.reset()`, чтобы вернуть виджет в начальное состояние, и только затем запускайте `execute()` заново.
* **Отправка формы прямо из обработчика submit.** Без `event.preventDefault()` форма уйдёт на сервер без токена. Отправляйте форму только из `callback`, когда токен получен (нативный `form.submit()` не вызывает обработчик события `submit`, поэтому зацикливания не будет).
* **Не передан `widgetId` при нескольких виджетах.** `execute()` без аргумента работает с первым отрисованным виджетом — при нескольких виджетах сохраняйте и передавайте `widgetId`.
* **Токен не проверен на сервере.** Наличие токена в форме ничего не гарантирует — обязательно проверяйте его через `/validate` ([server-validation.md](server-validation.md)).

## React

В пакете `@yandex/smart-captcha` для невидимой капчи есть готовый компонент `InvisibleSmartCaptcha` — см. [react.md](react.md) и шаблон [../templates/InvisibleCaptchaForm.tsx](../templates/InvisibleCaptchaForm.tsx).

## См. также

* [widget-advanced.md](widget-advanced.md) — расширенный метод подключения (база для невидимой капчи).
* [server-validation.md](server-validation.md) — проверка токена на сервере.
* [react.md](react.md) — `InvisibleSmartCaptcha` из `@yandex/smart-captcha`.
* [mobile-webview.md](mobile-webview.md) — невидимая капча в мобильном WebView.
* [../references/widget-params.md](../references/widget-params.md) — все параметры `render()`.
* [../references/js-api.md](../references/js-api.md) — методы `execute`, `reset`, `subscribe` и события.
* [../templates/invisible.html](../templates/invisible.html) — готовая страница с невидимой капчей.
* Официальная документация: https://yandex.cloud/ru/docs/smartcaptcha/concepts/invisible-captcha
