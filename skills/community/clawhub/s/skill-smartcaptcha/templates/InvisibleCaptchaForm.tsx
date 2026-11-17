// InvisibleCaptchaForm.tsx — React-форма с невидимой SmartCaptcha (InvisibleSmartCaptcha):
// проверка запускается по submit, задание видят только подозрительные пользователи.
// Подробности — в docs/react.md (props, события) и docs/invisible-captcha.md (концепция).
import { FormEvent, useCallback, useRef, useState } from 'react';
import { InvisibleSmartCaptcha } from '@yandex/smart-captcha';

export interface InvisibleCaptchaFormProps {
  /** Ключ клиента из консоли Yandex Cloud: <ключ_клиента> (см. docs/keys.md). */
  sitekey: string;
  /**
   * Родитель получает данные формы вместе с токеном и отправляет их на бэкенд,
   * где токен проверяется через POST /validate (см. docs/server-validation.md).
   */
  onSubmit: (data: { email: string; token: string }) => Promise<void> | void;
}

/**
 * Сценарий работы:
 * 1. Пользователь жмёт submit → preventDefault, visible=true — запуск проверки
 *    (реактивный аналог window.smartCaptcha.execute()).
 * 2. SmartCaptcha оценивает пользователя; подозрительному показывает задание.
 * 3. Успех → onSuccess(token) → вызываем родительский onSubmit с токеном.
 * 4. После отправки перемонтируем капчу сменой key: токен одноразовый,
 *    без сброса повторная отправка уйдёт с тем же токеном и провалит /validate.
 */
export function InvisibleCaptchaForm({ sitekey, onSubmit }: InvisibleCaptchaFormProps) {
  const [email, setEmail] = useState('');
  // visible=true запускает проверку InvisibleSmartCaptcha.
  const [visible, setVisible] = useState(false);
  // Блокируем кнопку на время проверки и отправки, чтобы исключить повторные клики.
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  // Смена key перемонтирует капчу — штатный паттерн сброса состояния.
  const [resetCaptcha, setResetCaptcha] = useState(0);
  // Флаг «токен получен»: onChallengeHidden срабатывает при любом закрытии
  // окна с заданием (включая успешное решение), и без флага он разблокировал бы
  // кнопку, пока onSubmit ещё выполняется.
  const tokenReceivedRef = useRef(false);

  const handleFormSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault(); // не отправлять форму, пока нет токена
    setError(null);
    tokenReceivedRef.current = false;
    setSubmitting(true);
    setVisible(true); // запустить проверку
  };

  // Окно с заданием закрылось. Если токена нет (пользователь закрыл задание,
  // не решив его) — разблокируем кнопку, чтобы можно было попробовать снова;
  // если токен получен, отправкой и разблокировкой занимается handleSuccess.
  const handleChallengeHidden = useCallback(() => {
    setVisible(false);
    if (!tokenReceivedRef.current) {
      setSubmitting(false);
    }
  }, []);

  const handleSuccess = useCallback(
    async (token: string) => {
      tokenReceivedRef.current = true;
      setVisible(false);
      try {
        await onSubmit({ email, token });
      } catch {
        setError('Не удалось отправить форму. Попробуйте ещё раз.');
      } finally {
        setSubmitting(false);
        // Токен одноразовый — сбрасываем капчу для следующей отправки.
        setResetCaptcha((prev) => prev + 1);
      }
    },
    [email, onSubmit],
  );

  const handleNetworkError = useCallback(() => {
    setVisible(false);
    setSubmitting(false);
    setError('Ошибка сети. Проверьте соединение и попробуйте ещё раз.');
  }, []);

  const handleJavascriptError = useCallback(
    (jsError: { filename: string; message: string; col: number; line: number }) => {
      // Критическая ошибка JS: сообщите пользователю и НЕ засчитывайте
      // успешную проверку — это потенциальная уязвимость приложения.
      console.error('SmartCaptcha javascript-error:', jsError);
      setVisible(false);
      setSubmitting(false);
      setError('Не удалось выполнить проверку. Обновите страницу и попробуйте снова.');
    },
    [],
  );

  return (
    <form onSubmit={handleFormSubmit}>
      <label>
        Email
        <input
          type="email"
          name="email"
          required
          value={email}
          onChange={(event) => setEmail(event.target.value)}
          disabled={submitting}
        />
      </label>

      <button type="submit" disabled={submitting}>
        {submitting ? 'Проверяем…' : 'Отправить'}
      </button>

      {/* Предупреждайте, что может появиться задание: время загрузки виджета
          у проверяемых пользователей варьируется, ожидание не должно удивлять. */}
      {submitting && <p>Идёт проверка. Возможно, появится задание капчи.</p>}
      {error && <p role="alert">{error}</p>}

      <InvisibleSmartCaptcha
        key={resetCaptcha}
        sitekey={sitekey}
        visible={visible}
        onSuccess={handleSuccess}
        onChallengeHidden={handleChallengeHidden}
        onNetworkError={handleNetworkError}
        onJavascriptError={handleJavascriptError}
        // shieldPosition="bottom-right" — позиция блока об обработке данных.
        // hideShield скрывает блок, но тогда вы ОБЯЗАНЫ уведомить пользователей
        // об обработке данных SmartCaptcha другим способом (юридическое требование).
      />
    </form>
  );
}

// Пример подключения:
// <InvisibleCaptchaForm
//   sitekey="<ключ_клиента>"
//   onSubmit={(data) =>
//     fetch('/api/submit', {
//       method: 'POST',
//       headers: { 'Content-Type': 'application/json' },
//       body: JSON.stringify(data), // бэкенд проверяет data.token через /validate
//     }).then((res) => {
//       if (!res.ok) throw new Error('submit failed');
//     })
//   }
// />
