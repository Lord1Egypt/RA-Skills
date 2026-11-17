# Параметры виджета SmartCaptcha

Полный справочник параметров виджета: объект `params` метода `window.smartCaptcha.render()` (расширенный метод) и data-атрибуты контейнера `div.smart-captcha` (автоматический метод). Читай, когда нужно узнать точное имя, тип или значение по умолчанию любого параметра.

## Как передаются параметры

- **Автоматический метод** — параметры задаются data-атрибутами контейнера `<div class="smart-captcha" ...>`; скрипт `https://smartcaptcha.yandexcloud.net/captcha.js` сам находит такие контейнеры и отрисовывает виджеты. Подробности: [../docs/widget-auto.md](../docs/widget-auto.md).
- **Расширенный метод** — параметры передаются вторым аргументом в `window.smartCaptcha.render(container, params)`; скрипт подключается с `?render=onload&onload=onloadFunction`. Подробности: [../docs/widget-advanced.md](../docs/widget-advanced.md).

## Таблица параметров

| Параметр `render()` | Data-атрибут (авто) | Тип | По умолчанию | Что делает |
| --- | --- | --- | --- | --- |
| `sitekey` | `data-sitekey` | `string` | — (обязательный) | Ключ клиентской части. Без него виджет не работает. См. [../docs/keys.md](../docs/keys.md). |
| `callback` | `data-callback` | `(token: string) => void`; в data-атрибуте — имя глобальной функции (`string`) | — | Функция-обработчик: вызывается с токеном после успешной проверки пользователя. Токен затем отправляют на бэкенд для проверки через `/validate`. |
| `hl` | `data-hl` | `'ru' \| 'en' \| 'be' \| 'kk' \| 'tt' \| 'uk' \| 'uz' \| 'tr'` | `window.navigator.language` | Язык виджета и задания. |
| `test` | — | `boolean` | — | Режим тестирования: пользователь **всегда** получает задание. Используй только для отладки и тестирования — в проде включённый `test` покажет капчу всем. |
| `webview` | — | `boolean` | — | Запуск капчи в **WebView**. Включай при встраивании капчи в мобильные приложения через WebView — повышает точность оценки пользователей. См. [../docs/mobile-webview.md](../docs/mobile-webview.md). |
| `invisible` | — | `boolean` | — | Невидимая капча: кнопка «Я не робот» не отрисовывается, задание видят только подозрительные пользователи; проверка запускается методом `execute()`. См. [../docs/invisible-captcha.md](../docs/invisible-captcha.md). |
| `shieldPosition` | — | `'top-left' \| 'center-left' \| 'bottom-left' \| 'top-right' \| 'center-right' \| 'bottom-right'` | нижний правый угол (`bottom-right`) | Расположение блока с уведомлением об обработке данных (ссылка на [условия обработки данных](https://yandex.ru/legal/smartcaptcha_notice/)), который появляется на странице с невидимой капчей. |
| `hideShield` | — | `boolean` | — | Скрыть блок с уведомлением об обработке данных. См. предупреждение ниже. |
| `metadata` | — | `object` (`ключ: значение`) | — | Собственные дополнительные данные с фронтенда (например, категория пользователя от антифрода) для [правил показа](../docs/captcha-settings.md) разных вариантов заданий. Общая длина всех ключей и значений — не более 512 символов. Сохраняйте выданные значения на бэкенде и сверяйте их при валидации токена, чтобы защититься от подделки. |

В документации для автоматического метода описаны только `data-sitekey`, `data-hl` и `data-callback`. Остальные параметры (`test`, `webview`, `invisible`, `shieldPosition`, `hideShield`, `metadata`) передавай через `render()` расширенным методом.

> **Важно.** Вы обязаны уведомлять пользователей о том, что их данные обрабатывает SmartCaptcha. Если вы скрываете блок с уведомлением (`hideShield: true`), сообщите пользователям иным способом о том, что SmartCaptcha обрабатывает их данные.

## Практические заметки

- При загрузке виджет меняет высоту контейнера на `100px`. Чтобы избежать «скачка» вёрстки, заранее задай контейнеру `style="height: 100px"`.
- `render()` возвращает `widgetId` — сохрани его, если на странице несколько виджетов: он нужен методам `execute`, `getResponse`, `reset`, `destroy`, `subscribe` (см. [js-api.md](js-api.md)).

## См. также

- [js-api.md](js-api.md) — методы и события `window.smartCaptcha`.
- [../docs/widget-auto.md](../docs/widget-auto.md) — автоматическое подключение виджета.
- [../docs/widget-advanced.md](../docs/widget-advanced.md) — расширенный метод подключения.
- [../docs/invisible-captcha.md](../docs/invisible-captcha.md) — невидимая капча.
- Официальная документация: [Методы установки виджета](https://yandex.cloud/ru/docs/smartcaptcha/concepts/widget-methods), [Невидимая капча](https://yandex.cloud/ru/docs/smartcaptcha/concepts/invisible-captcha).
