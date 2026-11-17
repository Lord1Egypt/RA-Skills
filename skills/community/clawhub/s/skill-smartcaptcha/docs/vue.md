# SmartCaptcha во Vue 3

Читай этот файл при интеграции SmartCaptcha в приложение на Vue 3 / Nuxt. Официального Vue-пакета у Яндекса нет (официальный пакет `@yandex/smart-captcha` — только React), поэтому Vue-интеграция строится на [расширенном методе виджета](widget-advanced.md): `captcha.js?render=onload` + `window.smartCaptcha.render()` в lifecycle-хуках.

## Готовые шаблоны скилла

Не пиши интеграцию с нуля — возьми шаблоны:

* [../templates/useSmartCaptcha.ts](../templates/useSmartCaptcha.ts) — composable: синглтон-загрузка скрипта, render/destroy по жизненному циклу, события, обычная и невидимая капча (`executeAndWait(): Promise<token>`).
* [../templates/smartcaptcha.d.ts](../templates/smartcaptcha.d.ts) — TypeScript-типы `window.smartCaptcha` (параметры `render()`, перегрузки `subscribe`), выверены по официальному справочнику.

## Что обязан делать Vue-компонент с капчей

Это грабли, на которые наступают все самописные интеграции; composable из шаблона закрывает их из коробки:

1. **Скрипт — один на всё SPA.** Загружай `captcha.js?render=onload&onload=<глобальный_колбэк>` через синглтон-Promise: глобальный onload-колбэк объявляй **до** вставки тега `<script>`; при `script.onerror` сбрасывай синглтон, чтобы следующее монтирование могло повторить загрузку.
2. **`render()` — в `onMounted`, с защитой от гонки.** Пока скрипт грузится, пользователь может уйти с маршрута: проверяй флаг «размонтирован» и наличие контейнера перед `render()`. Проверяй существование `window.smartCaptcha`.
3. **`destroy(widgetId)` — в `onBeforeUnmount`, всегда.** Без этого при каждом переходе по роутам обработчики виджета копятся в памяти. Перед `destroy` снимай подписки (`subscribe` возвращает функции отписки).
4. **`widgetId` сравнивай с `null`, а не по truthy** — `0` это валидный идентификатор первого виджета.
5. **`reset()` после каждой отправки формы** — токен одноразовый (и живёт 5 минут; по `token-expired` — сброс и повторная проверка).
6. **`javascript-error` — не успех.** При критической ошибке JS токен обнуляй и успех не засчитывай — это потенциальная уязвимость.
7. **Контейнеру задай `height: 100px` заранее** — иначе вёрстка «прыгнет» при загрузке виджета.

## Обычная капча: использование composable

```vue
<script setup lang="ts">
import { ref } from 'vue';
import { useSmartCaptcha } from '@/composables/useSmartCaptcha';

const container = ref<HTMLElement | null>(null);
const { token, ready, error, reset } = useSmartCaptcha(container, {
  sitekey: import.meta.env.VITE_SMARTCAPTCHA_SITEKEY,
});

async function onSubmit() {
  if (!token.value) return;
  try {
    await fetch('/api/register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ 'smart-token': token.value /* + поля формы */ }),
    });
  } finally {
    reset(); // токен одноразовый — сбрасываем после КАЖДОЙ попытки
  }
}
</script>

<template>
  <form @submit.prevent="onSubmit">
    <!-- поля формы -->
    <div ref="container" style="height: 100px"></div>
    <p v-if="error">{{ error }}</p>
    <button type="submit" :disabled="!token">Отправить</button>
  </form>
</template>
```

Ключ клиента храни в `VITE_SMARTCAPTCHA_SITEKEY` (публичный, `ysc1_…`); ключ сервера (`ysc2_…`) в переменные с префиксом `VITE_` не клади никогда — они попадают в бандл ([keys.md](keys.md)).

## Невидимая капча: executeAndWait в submit

Передай `invisible: true` и запускай проверку в обработчике отправки. `executeAndWait()` возвращает `Promise<token>` — это удобнее, чем следить за `token` через `watch`:

```ts
const { executeAndWait, reset, challengeVisible } = useSmartCaptcha(container, {
  sitekey: import.meta.env.VITE_SMARTCAPTCHA_SITEKEY,
  invisible: true,
  shieldPosition: 'bottom-right',
});

async function onSubmit() {
  try {
    const token = await executeAndWait(); // подозрительному пользователю покажется задание
    await sendLead(token);
  } catch (e) {
    // e.code: 'challenge-closed' (пользователь закрыл окно), 'network-error',
    // 'javascript-error', 'not-ready' — покажи понятный статус и дай повторить
  } finally {
    reset();
  }
}
```

Два важных нюанса невидимого сценария:

* **Закрытие окна задания.** Документированного события «пользователь отменил проверку» нет. Паттерн шаблона: по `challenge-hidden` ждать ~400 мс — если за это время не пришёл `callback` с токеном (при успехе события идут почти одновременно, callback обычно первым), значит пользователь закрыл окно — отклоняй ожидание с кодом `challenge-closed`. Без этого паттерна submit может «зависнуть» навсегда.
* **Уведомление об обработке данных** (блок-«щит») обязательно: настраивай позицию через `shieldPosition`; про `hideShield` см. предупреждение в [invisible-captcha.md](invisible-captcha.md).

## Nuxt / SSR

`window` и `captcha.js` существуют только в браузере. В composable вся работа начинается в `onMounted` (выполняется только на клиенте), поэтому он SSR-безопасен; не вызывай `loadSmartCaptchaScript()` вне lifecycle-хуков на сервере. В Nuxt при сомнениях оборачивай виджет в `<ClientOnly>`. Существует community-модуль `nuxt-yandex-smartcaptcha` (Nuxt 3/4).

## Community-пакеты (неофициальные)

Если не хочешь свой composable — есть сторонние обёртки. Они не поддерживаются Яндексом: проверяй актуальность и исходники перед использованием (состояние на июль 2026):

| Пакет | Что даёт |
|---|---|
| `vue3-smart-captcha` (czernika, MIT, v1.2.2) | Компонент `SmartCaptcha` + composable `useSmartCaptcha` (execute/reset/destroy/getResponse/subscribeTo); props повторяют параметры `render()`; события `@success`, `@token-expired` и др. |
| `@gladesinger/vue3-yandex-smartcaptcha` (v1.0.1) | Компонент `YandexSmartCaptcha` на TypeScript: props `siteKey`/`language`/`invisible`/…, emits `onSuccess`/`onTokenExpired`/…, методы через ref |
| `nuxt-yandex-smartcaptcha` | Модуль Nuxt 3/4, конфигурация через `nuxt.config` |

Имена props/событий у пакетов различаются — сверяй с их README; семантика виджета та же, что в [../references/widget-params.md](../references/widget-params.md) и [../references/js-api.md](../references/js-api.md).

## Локальная разработка

Валидация домена по умолчанию **строгая**: добавь `localhost` (и dev-домены) в список хостов капчи, иначе виджет не отобразится ([captcha-settings.md](captcha-settings.md), [troubleshooting.md](troubleshooting.md)). Токен всё равно проверяется на бэкенде — см. [server-validation.md](server-validation.md).

## См. также

* [../templates/useSmartCaptcha.ts](../templates/useSmartCaptcha.ts), [../templates/smartcaptcha.d.ts](../templates/smartcaptcha.d.ts) — готовый код.
* [widget-advanced.md](widget-advanced.md) — расширенный метод, на котором всё построено.
* [invisible-captcha.md](invisible-captcha.md) — концепция невидимой капчи и уведомление об обработке данных.
* [server-validation.md](server-validation.md) — обязательная серверная проверка токена.
* [react.md](react.md) — если проект на React: там есть официальный пакет.
* Официальная документация: [Методы установки виджета](https://yandex.cloud/ru/docs/smartcaptcha/concepts/widget-methods), [Невидимая капча](https://yandex.cloud/ru/docs/smartcaptcha/concepts/invisible-captcha).
