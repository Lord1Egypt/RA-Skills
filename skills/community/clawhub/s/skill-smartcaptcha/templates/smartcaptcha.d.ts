/**
 * Типы JS API Yandex SmartCaptcha (window.smartCaptcha). Подробности: ../docs/vue.md,
 * справочники: ../references/js-api.md и ../references/widget-params.md.
 *
 * Положите файл в src/types/smartcaptcha.d.ts (или .ts) вашего проекта.
 * Используется шаблоном ../templates/useSmartCaptcha.ts (импорт из './smartcaptcha').
 *
 * Основано на официальном справочнике (расширенный метод подключения):
 * методы render/getResponse/execute/reset/destroy/subscribe и параметры render().
 */

/**
 * Идентификатор виджета. Возвращается методом render();
 * используйте его только для передачи обратно в методы API
 * (getResponse, execute, reset, destroy, subscribe).
 */
export type WidgetId = number;

/** Поддерживаемые языки виджета и задания. */
export type SmartCaptchaLang = 'ru' | 'en' | 'be' | 'kk' | 'tt' | 'uk' | 'uz' | 'tr';

/** Расположение блока с уведомлением об обработке данных. */
export type ShieldPosition =
  | 'top-left'
  | 'center-left'
  | 'bottom-left'
  | 'top-right'
  | 'center-right'
  | 'bottom-right';

/** Параметры window.smartCaptcha.render(container, params). */
export interface SmartCaptchaRenderParams {
  /** Ключ клиентской части (публичный, `ysc1_…`). Обязательный. */
  sitekey: string;
  /** Вызывается с одноразовым токеном после успешной проверки пользователя. */
  callback?: (token: string) => void;
  /** Язык виджета и задания. По умолчанию — window.navigator.language. */
  hl?: SmartCaptchaLang;
  /**
   * Режим тестирования: пользователь ВСЕГДА получает задание.
   * Только для отладки — в проде включённый test покажет капчу всем.
   */
  test?: boolean;
  /** Запуск капчи в WebView мобильного приложения. */
  webview?: boolean;
  /** Невидимая капча: проверка запускается методом execute(). */
  invisible?: boolean;
  /** Позиция блока с уведомлением об обработке данных (невидимая капча). По умолчанию bottom-right. */
  shieldPosition?: ShieldPosition;
  /**
   * Скрыть блок с уведомлением об обработке данных.
   * Внимание: тогда вы обязаны уведомить пользователей об обработке данных иным способом.
   */
  hideShield?: boolean;
  /** Собственные данные для правил показа вариантов заданий (все ключи и значения — суммарно до 512 символов). */
  metadata?: Record<string, string>;
}

/** Полезная нагрузка события javascript-error. */
export interface SmartCaptchaJsError {
  filename: string;
  message: string;
  col: number;
  line: number;
}

/** События, доступные через subscribe. */
export type SmartCaptchaSubscribeEvent =
  | 'challenge-visible'
  | 'challenge-hidden'
  | 'network-error'
  | 'javascript-error'
  | 'success'
  | 'token-expired';

/** subscribe возвращает функцию отписки — отдельного метода unsubscribe нет. */
export type UnsubscribeFn = () => void;

export interface SmartCaptchaApi {
  /** Отрисовывает виджет в контейнере (DOM-элемент или id) и возвращает widgetId. */
  render(container: HTMLElement | string, params: SmartCaptchaRenderParams): WidgetId;
  /** Возвращает текущее значение токена пользователя. */
  getResponse(widgetId?: WidgetId): string;
  /** Запускает проверку пользователя (нужен для невидимой капчи). */
  execute(widgetId?: WidgetId): void;
  /** Сбрасывает состояние виджета до начального (токен одноразовый — сбрасывайте после каждой отправки). */
  reset(widgetId?: WidgetId): void;
  /** Удаляет виджет и его обработчики. Обязателен в SPA при размонтировании компонента. */
  destroy(widgetId?: WidgetId): void;
  /** Подписка на события виджета; возвращает функцию отписки. */
  subscribe(widgetId: WidgetId, event: 'success', callback: (token: string) => void): UnsubscribeFn;
  subscribe(
    widgetId: WidgetId,
    event: 'javascript-error',
    callback: (error: SmartCaptchaJsError) => void
  ): UnsubscribeFn;
  subscribe(
    widgetId: WidgetId,
    event: 'challenge-visible' | 'challenge-hidden' | 'network-error' | 'token-expired',
    callback: () => void
  ): UnsubscribeFn;
}

declare global {
  interface Window {
    /** Появляется после загрузки captcha.js, подключённого с ?render=onload. */
    smartCaptcha?: SmartCaptchaApi;
  }
}
