/**
 * useSmartCaptcha — Vue 3 composable для Yandex SmartCaptcha. Подробности: ../docs/vue.md.
 * Типы window.smartCaptcha — в ../templates/smartcaptcha.d.ts (импорт ниже из './smartcaptcha').
 *
 * У Яндекса нет официального Vue-пакета, поэтому интеграция строится на расширенном
 * методе виджета (captcha.js?render=onload + window.smartCaptcha.render()).
 *
 * Composable закрывает все SPA-грабли, которые иначе приходится решать вручную:
 *  - скрипт captcha.js грузится ОДИН раз на всё приложение (синглтон-Promise;
 *    при ошибке загрузки синглтон сбрасывается — следующая попытка загрузит заново);
 *  - onMounted → render() с защитой от гонки «скрипт догрузился, а компонент уже размонтирован»;
 *  - onBeforeUnmount → отписки + destroy(widgetId) — обязательно при роутинге SPA;
 *  - token-expired → обнуление токена + reset() (токен живёт 5 минут);
 *  - javascript-error → успех НЕ засчитывается (потенциальная уязвимость);
 *  - executeAndWait() — невидимая капча как Promise<token> прямо в обработчике submit.
 */
import { onBeforeUnmount, onMounted, readonly, ref, type Ref } from 'vue';
import type {
  ShieldPosition,
  SmartCaptchaApi,
  SmartCaptchaLang,
  UnsubscribeFn,
  WidgetId,
} from './smartcaptcha';

declare global {
  interface Window {
    /** Глобальный onload-колбэк для captcha.js (имя передаётся в параметре onload URL). */
    __vueSmartCaptchaOnload?: () => void;
  }
}

/* -------------------------------------------------------------------------- */
/* Загрузка captcha.js: один раз на всё SPA                                    */
/* -------------------------------------------------------------------------- */

const ONLOAD_CALLBACK_NAME = '__vueSmartCaptchaOnload';
const SCRIPT_SRC = `https://smartcaptcha.yandexcloud.net/captcha.js?render=onload&onload=${ONLOAD_CALLBACK_NAME}`;

let scriptPromise: Promise<SmartCaptchaApi> | null = null;

/** Загружает captcha.js (расширенный метод) и возвращает window.smartCaptcha. */
export function loadSmartCaptchaScript(): Promise<SmartCaptchaApi> {
  if (window.smartCaptcha) {
    return Promise.resolve(window.smartCaptcha);
  }
  if (scriptPromise) {
    return scriptPromise;
  }

  scriptPromise = new Promise<SmartCaptchaApi>((resolve, reject) => {
    // Функция из параметра onload обязана быть глобальной и объявленной
    // ДО добавления тега <script> на страницу.
    window[ONLOAD_CALLBACK_NAME] = () => {
      if (window.smartCaptcha) {
        resolve(window.smartCaptcha);
      } else {
        reject(new Error('captcha.js загрузился, но window.smartCaptcha недоступен'));
      }
    };

    const script = document.createElement('script');
    script.src = SCRIPT_SRC;
    script.onerror = () => {
      // Сбрасываем синглтон: следующее монтирование сможет повторить загрузку.
      scriptPromise = null;
      reject(new Error('Не удалось загрузить скрипт SmartCaptcha'));
    };
    document.head.appendChild(script);
  });

  return scriptPromise;
}

/* -------------------------------------------------------------------------- */
/* Composable                                                                  */
/* -------------------------------------------------------------------------- */

export interface UseSmartCaptchaOptions {
  /** Ключ клиента (публичный, `ysc1_…`). */
  sitekey: string;
  /** Язык виджета. */
  hl?: SmartCaptchaLang;
  /** Режим тестирования (задание показывается всегда). Только для отладки. */
  test?: boolean;
  /** Невидимая капча — проверка запускается методами execute()/executeAndWait(). */
  invisible?: boolean;
  /** Позиция блока с уведомлением об обработке данных (для невидимой капчи). */
  shieldPosition?: ShieldPosition;
  /** Скрыть блок уведомления — тогда уведомите об обработке данных иным способом. */
  hideShield?: boolean;
}

/** Ошибка невидимой проверки с машиночитаемым кодом причины. */
export class SmartCaptchaError extends Error {
  constructor(
    public readonly code:
      | 'not-ready'
      | 'already-running'
      | 'challenge-closed'
      | 'network-error'
      | 'javascript-error'
      | 'reset',
    message: string,
  ) {
    super(message);
    this.name = 'SmartCaptchaError';
  }
}

/**
 * Монтирует виджет SmartCaptcha в контейнер и управляет его жизненным циклом.
 *
 * @param container - ref на DOM-контейнер (задайте ему height: 100px заранее — обычная капча).
 * @param options   - параметры render(); фиксируются в момент монтирования.
 */
export function useSmartCaptcha(container: Ref<HTMLElement | null>, options: UseSmartCaptchaOptions) {
  /** Актуальный одноразовый токен (null — проверка не пройдена). Живёт 5 минут. */
  const token = ref<string | null>(null);
  /** Виджет отрисован и готов к работе. */
  const ready = ref(false);
  /** Человекочитаемое сообщение об ошибке для UI (или null). */
  const error = ref<string | null>(null);
  /** Открыто ли всплывающее окно с заданием (полезно для статуса в UI). */
  const challengeVisible = ref(false);

  let api: SmartCaptchaApi | null = null;
  let widgetId: WidgetId | null = null;
  let unsubscribers: UnsubscribeFn[] = [];
  let unmounted = false;

  // Ожидание executeAndWait(): resolve придёт из callback, reject — из событий ошибок.
  let pending: { resolve: (token: string) => void; reject: (e: SmartCaptchaError) => void } | null = null;
  let challengeHiddenTimer: ReturnType<typeof setTimeout> | undefined;

  function rejectPending(e: SmartCaptchaError): void {
    clearTimeout(challengeHiddenTimer);
    if (pending) {
      const p = pending;
      pending = null;
      p.reject(e);
    }
  }

  onMounted(async () => {
    try {
      const loaded = await loadSmartCaptchaScript();

      // Пока скрипт грузился, пользователь мог уйти с маршрута — виджет не рисуем.
      if (unmounted || !container.value) {
        return;
      }
      api = loaded;

      widgetId = api.render(container.value, {
        sitekey: options.sitekey,
        hl: options.hl,
        test: options.test,
        invisible: options.invisible,
        shieldPosition: options.shieldPosition,
        hideShield: options.hideShield,
        callback: (value) => {
          clearTimeout(challengeHiddenTimer);
          token.value = value;
          error.value = null;
          if (pending) {
            const p = pending;
            pending = null;
            p.resolve(value);
          }
        },
      });

      unsubscribers = [
        api.subscribe(widgetId, 'challenge-visible', () => {
          challengeVisible.value = true;
        }),
        api.subscribe(widgetId, 'challenge-hidden', () => {
          challengeVisible.value = false;
          // Окно задания закрылось. Если это успех — callback придёт следом,
          // события почти одновременны. Небольшая задержка даёт callback'у
          // сработать первым; если токена так и нет — пользователь закрыл окно.
          clearTimeout(challengeHiddenTimer);
          challengeHiddenTimer = setTimeout(() => {
            rejectPending(new SmartCaptchaError('challenge-closed', 'Проверка отменена: окно с заданием закрыто'));
          }, 400);
        }),
        api.subscribe(widgetId, 'token-expired', () => {
          // Токен живёт 5 минут: сбрасываем виджет, чтобы пройти проверку заново.
          token.value = null;
          error.value = 'Срок действия проверки истёк — пройдите её ещё раз.';
          if (api && widgetId !== null) {
            api.reset(widgetId);
          }
        }),
        api.subscribe(widgetId, 'network-error', () => {
          error.value = 'Сетевая ошибка при проверке. Проверьте соединение и попробуйте ещё раз.';
          rejectPending(new SmartCaptchaError('network-error', 'Сетевая ошибка SmartCaptcha'));
        }),
        api.subscribe(widgetId, 'javascript-error', (jsError) => {
          // Критический сбой JS: засчитывать успешное прохождение нельзя.
          token.value = null;
          error.value = 'Ошибка в работе проверки. Обновите страницу и попробуйте снова.';
          console.error('SmartCaptcha javascript-error:', jsError);
          rejectPending(new SmartCaptchaError('javascript-error', 'Критическая ошибка JS в виджете'));
        }),
      ];

      ready.value = true;
    } catch (loadError) {
      error.value = 'Не удалось загрузить проверку «Я не робот». Обновите страницу.';
      console.error(loadError);
    }
  });

  onBeforeUnmount(() => {
    unmounted = true;
    rejectPending(new SmartCaptchaError('reset', 'Компонент размонтирован'));

    for (const unsubscribe of unsubscribers) {
      unsubscribe();
    }
    unsubscribers = [];

    if (api && widgetId !== null) {
      // Обязательно в SPA: destroy удаляет виджет и созданные им обработчики.
      api.destroy(widgetId);
    }
    api = null;
    widgetId = null;
  });

  /**
   * Сбрасывает виджет и обнуляет токен. Токен одноразовый — вызывайте reset()
   * после КАЖДОЙ отправки формы (успешной или нет).
   */
  function reset(): void {
    rejectPending(new SmartCaptchaError('reset', 'Виджет сброшен'));
    token.value = null;
    if (api && widgetId !== null) {
      api.reset(widgetId);
    }
  }

  /** Запускает невидимую проверку без ожидания (токен придёт в token/callback). */
  function execute(): void {
    if (api && widgetId !== null) {
      api.execute(widgetId);
    }
  }

  /**
   * Невидимая капча как Promise: вызывайте в обработчике submit.
   * resolve — одноразовый токен; reject — SmartCaptchaError с кодом причины
   * (challenge-closed / network-error / javascript-error / not-ready / reset).
   */
  function executeAndWait(): Promise<string> {
    if (pending) {
      return Promise.reject(new SmartCaptchaError('already-running', 'Проверка уже выполняется'));
    }
    if (!ready.value || !api || widgetId === null) {
      return Promise.reject(new SmartCaptchaError('not-ready', error.value ?? 'Виджет SmartCaptcha не готов'));
    }
    return new Promise<string>((resolve, reject) => {
      pending = { resolve, reject };
      api!.execute(widgetId!);
    });
  }

  return {
    token: readonly(token),
    ready: readonly(ready),
    error: readonly(error),
    challengeVisible: readonly(challengeVisible),
    reset,
    execute,
    executeAndWait,
  };
}
