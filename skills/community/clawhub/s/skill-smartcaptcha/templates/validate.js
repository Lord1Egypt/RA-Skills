// Серверная проверка токена Yandex SmartCaptcha (Node.js 18+, глобальный fetch). Подробности: ../docs/server-validation.md
//
// Переиспользуемый ESM-модуль:
//   import { check_captcha } from './validate.js';
//   const passed = await check_captcha(token, req.ip);
//
// Ключ сервера берется из переменной окружения SMARTCAPTCHA_SERVER_KEY.
// Отсутствие ключа — громкая ошибка конфигурации (throw), а не тихий фолбэк:
// с плейсхолдером /validate отвечал бы failed всем пользователям.
//
// Семантика (по официальной документации):
// - POST https://smartcaptcha.yandexcloud.net/validate, формат x-www-form-urlencoded;
// - таймаут 1 секунда, чтобы не задерживать обработку запроса пользователя;
// - fail-open: при HTTP-коде != 200, сетевой ошибке или неразборчивом JSON
//   пользователь пропускается (рекомендация сервиса — обрабатывать ошибки
//   HTTP-протокола как ответ "status": "ok");
// - решение принимается только по полю status ("ok" / "failed");
//   поле message — только для диагностики, не сравнивайте его в коде.
//
// Важно: токен одноразовый и живет 5 минут. Повторная валидация того же токена
// вернет "status": "failed" с сообщением "Invalid or expired Token".

const VALIDATE_URL = 'https://smartcaptcha.yandexcloud.net/validate';
const SMARTCAPTCHA_SERVER_KEY = process.env.SMARTCAPTCHA_SERVER_KEY || '';

/**
 * Проверяет токен SmartCaptcha. Возвращает true — пропустить пользователя.
 *
 * @param {string} token - Одноразовый токен из формы (поле smart-token).
 * @param {string} [ip] - IP-адрес пользователя. Необязателен, но передавайте его —
 *   это улучшает качество работы SmartCaptcha. Способ получения зависит
 *   от фреймворка и прокси (например, в Express — req.ip).
 * @param {object} [options]
 * @param {string} [options.secret] - Ключ сервера (по умолчанию — из SMARTCAPTCHA_SERVER_KEY).
 * @param {number} [options.timeoutMs] - Таймаут запроса в миллисекундах.
 * @returns {Promise<boolean>} true — проверка пройдена (status === "ok") или сервис
 *   недоступен (fail-open); false — это робот (status === "failed").
 */
export async function check_captcha(token, ip, { secret = SMARTCAPTCHA_SERVER_KEY, timeoutMs = 1000 } = {}) {
    if (!secret) {
        // Ошибка конфигурации должна падать громко: пустой/неверный secret приводит
        // к "status": "failed" для всех пользователей — тихий отказ всем живым людям.
        throw new Error('SMARTCAPTCHA_SERVER_KEY не задан: укажите ключ сервера (ysc2_...)');
    }
    const body = new URLSearchParams({ secret, token });
    if (ip) {
        body.set('ip', ip);
    }

    let res;
    let content;
    try {
        res = await fetch(VALIDATE_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: body.toString(),
            signal: AbortSignal.timeout(timeoutMs),
        });
        content = await res.text();
    } catch (error) {
        // Сетевая ошибка или таймаут — пропускаем пользователя (fail-open),
        // чтобы сбой сервиса не блокировал реальных людей.
        console.error('Allow access due to an error:', error);
        return true;
    }

    if (res.status !== 200) {
        console.error(`Allow access due to an error: code=${res.status}; message=${content}`);
        return true;
    }

    try {
        const parsedContent = JSON.parse(content);
        return parsedContent.status === 'ok';
    } catch (err) {
        console.error('Error parsing response: ', err);
        return true;
    }
}

export default check_captcha;
