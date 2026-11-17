# React: интеграция через @yandex/smart-captcha

Читай этот файл, когда подключаешь SmartCaptcha в React-приложение (SPA, Next.js и т.п.): установка npm-пакета, компоненты `SmartCaptcha` и `InvisibleSmartCaptcha`, обработка событий, сброс состояния и передача токена на бэкенд.

## Установка пакета

Выполни внутри проекта одну из команд:

### npm

```bash
npm i -PE @yandex/smart-captcha
```

### yarn

```bash
yarn add @yandex/smart-captcha
```

### pnpm

```bash
pnpm add @yandex/smart-captcha
```

## Состав пакета

| Компонент | Назначение |
|---|---|
| `SmartCaptcha` | Валидация пользователя на сайтах с кнопкой **Я не робот** (обычная капча). |
| `InvisibleSmartCaptcha` | Валидация без кнопки **Я не робот** (невидимая капча, концепция — в [invisible-captcha.md](invisible-captcha.md)). |

При работе через пакет подключение виджета берут на себя компоненты — отдельный тег `<script src="https://smartcaptcha.yandexcloud.net/captcha.js">` в примерах официальной документации для React не используется.

## Свойства компонентов

Оба компонента принимают одинаковый набор свойств:

| Свойство | Тип | Описание |
|---|---|---|
| `sitekey` | `string` | Ключ клиента (см. [keys.md](keys.md)). |
| `visible` | `boolean` \| `undefined` | Показывать задание пользователю. |
| `language` | `ru` \| `en` \| `be` \| `kk` \| `tt` \| `uk` \| `uz` \| `tr` \| `undefined` | Язык виджета. |
| `test` | `boolean` \| `undefined` | Тестовый режим: пользователь всегда получает задание. Только для отладки и тестирования. |
| `webview` | `boolean` \| `undefined` | Запуск капчи в WebView — повышает точность оценки пользователей в мобильных приложениях (см. [mobile-webview.md](mobile-webview.md)). |
| `shieldPosition` | `top-left` \| `center-left` \| `bottom-left` \| `top-right` \| `center-right` \| `bottom-right` \| `undefined` | Расположение блока с уведомлением об обработке данных. |
| `hideShield` | `boolean` \| `undefined` | Скрыть блок с уведомлением об обработке данных. |
| `onChallengeVisible` | `() => void` \| `undefined` | Вызывается, когда появляется всплывающее окно с заданием. |
| `onChallengeHidden` | `() => void` \| `undefined` | Вызывается, когда закрывается всплывающее окно с заданием. |
| `onNetworkError` | `() => void` \| `undefined` | Вызывается при ошибке сети. |
| `onJavascriptError` | `(error: { filename: string, message: string, col: number, line: number }) => void` \| `undefined` | Вызывается при критической ошибке в работе JavaScript. |
| `onSuccess` | `(token: string) => void` \| `undefined` | Вызывается, когда пользователь успешно прошёл проверку; аргумент — уникальный токен пользователя. |
| `onTokenExpired` | `() => void` \| `undefined` | Вызывается, когда полученный токен становится невалидным. |

> **Важно.** Вы обязаны уведомлять пользователей о том, что их данные обрабатывает SmartCaptcha. Если скрываете блок с уведомлением через `hideShield`, сообщите пользователям об обработке данных иным способом.

## Обычная капча: SmartCaptcha

Виджет с кнопкой **Я не робот**; проверка запускается кликом пользователя. Токен приходит в `onSuccess` — сохрани его в состоянии и отправь на бэкенд вместе с формой:

```tsx
import { useState } from 'react';
import { SmartCaptcha } from '@yandex/smart-captcha';

export const ComponentWithCaptcha = () => {
  const [token, setToken] = useState('');

  return <SmartCaptcha sitekey="<ключ_клиента>" onSuccess={setToken} />;
};
```

Готовый типизированный компонент для формы — [../templates/SmartCaptchaField.tsx](../templates/SmartCaptchaField.tsx).

## Невидимая капча: InvisibleSmartCaptcha

Кнопки **Я не робот** нет; задание увидят только подозрительные пользователи. Проверка запускается из кода — переключением `visible` в `true` (реактивный аналог `execute()` из JS API, см. [invisible-captcha.md](invisible-captcha.md)):

```tsx
import { useCallback, useState } from 'react';
import { InvisibleSmartCaptcha } from '@yandex/smart-captcha';

export const InvisibleCaptcha = () => {
  const [token, setToken] = useState('');
  const [visible, setVisible] = useState(false);

  const handleChallengeHidden = useCallback(() => setVisible(false), []);

  const handleButtonClick = () => setVisible(true);

  return (
    <>
      <button onClick={handleButtonClick}>Validate</button>
      <InvisibleSmartCaptcha
        sitekey="<ключ_клиента>"
        onSuccess={setToken}
        onChallengeHidden={handleChallengeHidden}
        visible={visible}
      />
    </>
  );
};
```

Сбрасывай `visible` в `false` в `onChallengeHidden` — иначе после закрытия задания без решения повторный сабмит не запустит проверку (состояние не изменится). Готовая форма с запуском по submit — [../templates/InvisibleCaptchaForm.tsx](../templates/InvisibleCaptchaForm.tsx).

## Обработка статусов: подписка на события

Оба компонента дают шесть колбэков-подписок на события виджета: `onChallengeVisible`, `onChallengeHidden`, `onNetworkError`, `onJavascriptError`, `onSuccess`, `onTokenExpired`. Используй их, чтобы показывать статус проверки в UI (индикатор «идёт проверка», сообщение об ошибке сети и т.д.):

```tsx
import { useCallback, useState } from 'react';
import { SmartCaptcha, SmartCaptchaProps } from '@yandex/smart-captcha';

export const SubscriptionToCaptcha = () => {
  const [token, setToken] = useState('');
  const [status, setStatus] = useState('hidden');

  const handleChallengeVisible = useCallback(() => setStatus('visible'), []);
  const handleChallengeHidden = useCallback(() => setStatus('hidden'), []);

  const handleSuccess = useCallback((token: string) => {
    setStatus('success');
    setToken(token);
  }, []);
  const handleTokenExpired = useCallback(() => {
    setStatus('token-expired');
    setToken('');
  }, []);

  const handleNetworkError: SmartCaptchaProps['onNetworkError'] =
    useCallback(() => setStatus('network-error'), []);

  const handleJavaScriptError: SmartCaptchaProps['onJavascriptError'] =
    useCallback((error) => {
      setStatus('javascript-error');
      console.error(error); // залогируйте { filename, message, col, line }
    }, []);

  return (
    <>
      Status: {status}
      <SmartCaptcha
        sitekey="<ключ_клиента>"
        onChallengeVisible={handleChallengeVisible}
        onChallengeHidden={handleChallengeHidden}
        onNetworkError={handleNetworkError}
        onJavascriptError={handleJavaScriptError}
        onSuccess={handleSuccess}
        onTokenExpired={handleTokenExpired}
      />
    </>
  );
};
```

> **Важно.** Ошибка `javascript-error` указывает на критический сбой в работе JavaScript. Сообщи о проблеме пользователю в интерфейсе приложения. Засчитывать успешное выполнение задания при такой ошибке нельзя — это потенциальная уязвимость приложения.

В `onTokenExpired` очищай сохранённый токен (`setToken('')`) — протухший токен всё равно не пройдёт серверную проверку.

## Сброс состояния капчи

Капча сохраняет состояние после прохождения валидации. Если пользователь отправляет форму повторно (например, сервер отклонил данные), запрос уйдёт **с тем же одноразовым токеном** — и `/validate` его отклонит. Поэтому после каждой отправки сбрасывай капчу.

Паттерн сброса — перемонтирование компонента через смену `key`:

```tsx
import { useState } from 'react';
import { SmartCaptcha } from '@yandex/smart-captcha';

export default function App() {
  const [resetCaptcha, setResetCaptcha] = useState(0);

  /* Смена key перемонтирует компонент и сбрасывает состояние капчи */
  const handleReset = () => setResetCaptcha((prev) => prev + 1);

  return (
    <div className="App">
      <SmartCaptcha key={resetCaptcha} sitekey="<ключ_клиента>" />
      <button onClick={handleReset}>Сбросить капчу</button>
    </div>
  );
}
```

Вызывай `handleReset` после каждого запроса на бэкенд (и успешного, и отклонённого) — токен одноразовый в любом случае.

## Отправка токена на бэкенд

Токен из `onSuccess` — это ещё не подтверждение, что пользователь не робот. Отправь его на свой сервер вместе с данными формы и проверь через `/validate` (см. [server-validation.md](server-validation.md)):

```tsx
const handleSubmit = async (event: React.FormEvent) => {
  event.preventDefault();
  if (!token) return; // не отправлять форму без токена

  await fetch('/api/submit', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, 'smart-token': token }),
  });

  handleReset(); // токен одноразовый — сбросить капчу для следующей отправки
};
```

Помни про жизненный цикл токена (детали — [overview.md](overview.md)): он одноразовый и живёт 5 минут. Блокируй кнопку отправки, пока токена нет (`disabled={!token}`), и очищай токен в `onTokenExpired`.

## См. также

* [../templates/SmartCaptchaField.tsx](../templates/SmartCaptchaField.tsx) — готовый компонент обычной капчи для формы (статусы, сброс, токен в родительский `onSubmit`).
* [../templates/InvisibleCaptchaForm.tsx](../templates/InvisibleCaptchaForm.tsx) — готовая форма с невидимой капчей и запуском проверки по submit.
* [../workflows/integrate-react.md](../workflows/integrate-react.md) — пошаговый сценарий интеграции в React/SPA.
* [invisible-captcha.md](invisible-captcha.md) — как работает невидимая капча (концепция, уведомление об обработке данных).
* [vue.md](vue.md) — если проект на Vue 3: официального пакета нет, интеграция через composable.
* [server-validation.md](server-validation.md) — проверка токена на сервере через `/validate`.
* [keys.md](keys.md) — где взять ключ клиента и как хранить ключ сервера.
* [../references/js-api.md](../references/js-api.md) — события виджета, на которые опираются колбэки компонентов.
* Официальная документация: https://yandex.cloud/ru/docs/smartcaptcha/concepts/react
