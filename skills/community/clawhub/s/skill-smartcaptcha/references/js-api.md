# JS API: window.smartCaptcha

Справочник методов объекта `window.smartCaptcha` и событий `subscribe` с сигнатурами. Читай, когда пишешь код расширенного метода, невидимой капчи или подписки на события виджета.

## Доступ к объекту

`window.smartCaptcha` появляется после загрузки скрипта, подключённого с параметрами `render=onload&onload=<имя_функции>`:

```html
<script src="https://smartcaptcha.yandexcloud.net/captcha.js?render=onload&onload=onloadFunction" defer></script>
```

В `onload`-функции всегда проверяй существование объекта (`if (window.smartCaptcha) { ... }`) — иначе вызов до завершения загрузки скрипта приведёт к ошибке.

## Методы

| Метод | Сигнатура | Что делает |
| --- | --- | --- |
| `render` | `(container: HTMLElement \| string, params) => WidgetId` | Отрисовывает виджет в контейнере (DOM-элемент или его идентификатор) и возвращает `widgetId` — уникальный идентификатор виджета. Состав `params` — в [widget-params.md](widget-params.md). |
| `getResponse` | `(widgetId: WidgetId \| undefined) => string` | Возвращает текущее значение токена пользователя. Без аргумента — токен первого отрисованного виджета. |
| `execute` | `(widgetId: WidgetId \| undefined) => void` | Запускает проверку пользователя. Используй для невидимой капчи, чтобы начать проверку по событию (например, по нажатию submit формы). Без аргумента — первый отрисованный виджет; при нескольких виджетах на странице передавай `widgetId` обязательно. |
| `reset` | `(widgetId: WidgetId \| undefined) => void` | Сбрасывает состояние виджета до начального. Без аргумента — первый отрисованный виджет. Полезно после серверной проверки токена: токен одноразовый, для повторной отправки формы нужна новая проверка. |
| `destroy` | `(widgetId: WidgetId \| undefined) => void` | Удаляет виджет и созданные им обработчики. Без аргумента — первый отрисованный виджет. Вызывай при размонтировании страницы/компонента в SPA. |
| `subscribe` | `(widgetId: WidgetId, event: SubscribeEvent, callback: Function) => UnsubscribeFunction` | Подписывает обработчик на событие виджета (например, чтобы отследить открытие/закрытие окна с заданием — полезно для управления клавиатурой на мобильных устройствах). |

Отдельного метода `unsubscribe` нет: `subscribe` возвращает функцию отписки `UnsubscribeFunction = () => void` — сохрани и вызови её, чтобы снять обработчик.

## События subscribe

```ts
type SubscribeEvent =
  | 'challenge-visible'
  | 'challenge-hidden'
  | 'network-error'
  | 'javascript-error'
  | 'success'
  | 'token-expired';
```

| Событие | Когда происходит | Сигнатура обработчика (полезная нагрузка) |
| --- | --- | --- |
| `challenge-visible` | Открытие всплывающего окна с заданием | `() => void` |
| `challenge-hidden` | Закрытие всплывающего окна с заданием | `() => void` |
| `network-error` | Возникла сетевая ошибка | `() => void` |
| `javascript-error` | Возникла критическая ошибка JS | `(error: { filename: string, message: string, col: number, line: number }) => void` |
| `success` | Успешная валидация пользователя | `(token: string) => void` |
| `token-expired` | Токен прохождения проверки стал невалидным | `() => void` |

> **Важно.** Ошибка `javascript-error` указывает на критический сбой в работе JavaScript. Сообщите об этой проблеме пользователю в интерфейсе приложения. При возникновении такой ошибки засчитывать успешное выполнение задания нельзя — это может создать потенциальную уязвимость вашего приложения.

## Пример подписки

```html
<!-- Подписка на событие виджета; подробности — в ../docs/widget-advanced.md -->
<div id="container"></div>

<script src="https://smartcaptcha.yandexcloud.net/captcha.js?render=onload&onload=onloadFunction" async defer></script>

<script>
  function onloadFunction() {
    if (window.smartCaptcha) {
      const container = document.getElementById('container');
      const widgetId = window.smartCaptcha.render(container, {
        sitekey: '<ключ_клиента>',
      });

      const unsubscribe = window.smartCaptcha.subscribe(
        widgetId,
        'challenge-visible',
        () => console.log('challenge is visible')
      );
      // Позже: unsubscribe(); — снять обработчик
    }
  }
</script>
```

## См. также

- [widget-params.md](widget-params.md) — все параметры `render()` и data-атрибуты.
- [../docs/widget-advanced.md](../docs/widget-advanced.md) — подключение расширенным методом, колбэки.
- [../docs/invisible-captcha.md](../docs/invisible-captcha.md) — невидимая капча и `execute()`.
- [../docs/server-validation.md](../docs/server-validation.md) — что делать с токеном на бэкенде.
- Официальная документация: [Методы установки виджета](https://yandex.cloud/ru/docs/smartcaptcha/concepts/widget-methods), [Добавить виджет расширенным методом](https://yandex.cloud/ru/docs/smartcaptcha/operations/advanced-method).
