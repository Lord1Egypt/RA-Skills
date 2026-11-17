// SmartCaptchaField.tsx — React-компонент обычной SmartCaptcha (кнопка «Я не робот») для встраивания в форму.
// Подробности по установке @yandex/smart-captcha, props и паттернам — в docs/react.md.
import {
  FormEvent,
  forwardRef,
  useCallback,
  useImperativeHandle,
  useRef,
  useState,
} from 'react';
import { SmartCaptcha } from '@yandex/smart-captcha';

/**
 * Статус виджета, вычисленный по событиям компонента SmartCaptcha.
 * Используйте его, чтобы показывать пользователю, что происходит с проверкой.
 */
export type CaptchaStatus =
  | 'idle' // виджет отрисован, проверка ещё не пройдена
  | 'challenge-visible' // показано всплывающее окно с заданием
  | 'success' // проверка пройдена, токен получен
  | 'token-expired' // токен стал невалидным — нужна повторная проверка
  | 'network-error' // ошибка сети — предложите повторить
  | 'javascript-error'; // критическая ошибка JS — засчитывать успех НЕЛЬЗЯ

export interface SmartCaptchaFieldHandle {
  /**
   * Полный сброс капчи (перемонтирование виджета через смену key).
   * Вызывайте после КАЖДОЙ отправки формы: токен одноразовый, и без сброса
   * повторный запрос уйдёт с тем же токеном — сервер его отклонит.
   */
  reset: () => void;
}

export interface SmartCaptchaFieldProps {
  /** Ключ клиента из консоли Yandex Cloud (см. docs/keys.md). */
  sitekey: string;
  /** Получает токен после успешной проверки и null, когда токен протух или сброшен. */
  onTokenChange: (token: string | null) => void;
  /** Необязательный колбэк для отображения статуса проверки в UI. */
  onStatusChange?: (status: CaptchaStatus) => void;
  /** Язык виджета. */
  language?: 'ru' | 'en' | 'be' | 'kk' | 'tt' | 'uk' | 'uz' | 'tr';
  /** Тестовый режим: задание показывается всегда. Только для отладки. */
  test?: boolean;
}

/**
 * Поле «капча» для формы: оборачивает SmartCaptcha, поднимает токен и статус
 * в родителя и умеет сбрасываться через ref.
 */
export const SmartCaptchaField = forwardRef<SmartCaptchaFieldHandle, SmartCaptchaFieldProps>(
  function SmartCaptchaField({ sitekey, onTokenChange, onStatusChange, language, test }, ref) {
    // Смена key перемонтирует компонент — штатный паттерн сброса состояния капчи.
    const [resetCaptcha, setResetCaptcha] = useState(0);

    const setStatus = useCallback(
      (status: CaptchaStatus) => onStatusChange?.(status),
      [onStatusChange],
    );

    useImperativeHandle(
      ref,
      () => ({
        reset: () => {
          onTokenChange(null);
          setResetCaptcha((prev) => prev + 1);
        },
      }),
      [onTokenChange],
    );

    return (
      <SmartCaptcha
        key={resetCaptcha}
        sitekey={sitekey}
        language={language}
        test={test}
        onSuccess={(token) => {
          onTokenChange(token);
          setStatus('success');
        }}
        onTokenExpired={() => {
          // Протухший токен не пройдёт /validate — очищаем его у родителя.
          onTokenChange(null);
          setStatus('token-expired');
        }}
        onChallengeVisible={() => setStatus('challenge-visible')}
        onChallengeHidden={() => setStatus('idle')}
        onNetworkError={() => setStatus('network-error')}
        onJavascriptError={(error) => {
          // Критический сбой JS: сообщите пользователю и НЕ засчитывайте успех —
          // иначе создадите уязвимость в приложении.
          console.error('SmartCaptcha javascript-error:', error);
          onTokenChange(null);
          setStatus('javascript-error');
        }}
      />
    );
  },
);

// ---------------------------------------------------------------------------
// Пример использования: форма, которая отдаёт токен в родительский onSubmit.
// ---------------------------------------------------------------------------

export interface FormWithCaptchaProps {
  /** Ключ клиента: <ключ_клиента>. */
  sitekey: string;
  /**
   * Родитель получает данные формы вместе с токеном и отправляет их на бэкенд,
   * где токен проверяется через POST /validate (см. docs/server-validation.md).
   */
  onSubmit: (data: { email: string; token: string }) => Promise<void> | void;
}

export function FormWithCaptcha({ sitekey, onSubmit }: FormWithCaptchaProps) {
  const [email, setEmail] = useState('');
  const [token, setToken] = useState<string | null>(null);
  const [status, setStatus] = useState<CaptchaStatus>('idle');
  const captchaRef = useRef<SmartCaptchaFieldHandle>(null);

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (!token) {
      return; // без токена форму не отправляем
    }

    try {
      await onSubmit({ email, token });
    } finally {
      // Токен одноразовый: сбрасываем капчу после любой отправки (успешной
      // или отклонённой), чтобы следующая попытка получила новый токен.
      captchaRef.current?.reset();
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <label>
        Email
        <input
          type="email"
          name="email"
          required
          value={email}
          onChange={(event) => setEmail(event.target.value)}
        />
      </label>

      <SmartCaptchaField
        ref={captchaRef}
        sitekey={sitekey}
        onTokenChange={setToken}
        onStatusChange={setStatus}
      />

      {status === 'network-error' && <p role="alert">Ошибка сети. Попробуйте ещё раз.</p>}
      {status === 'javascript-error' && (
        <p role="alert">Не удалось выполнить проверку. Обновите страницу.</p>
      )}
      {status === 'token-expired' && (
        <p role="alert">Проверка устарела. Пройдите её заново.</p>
      )}

      {/* Кнопка активна только когда токен получен. */}
      <button type="submit" disabled={!token}>
        Отправить
      </button>
    </form>
  );
}

// Пример подключения:
// <FormWithCaptcha
//   sitekey="<ключ_клиента>"
//   onSubmit={(data) =>
//     fetch('/api/submit', {
//       method: 'POST',
//       headers: { 'Content-Type': 'application/json' },
//       body: JSON.stringify(data), // бэкенд проверяет data.token через /validate
//     }).then(() => undefined)
//   }
// />
