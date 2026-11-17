// Сервер Express: форма с SmartCaptcha + проверка токена через /validate. Подробности: ../../docs/server-validation.md
'use strict';

const express = require('express');
const fs = require('fs');
const path = require('path');

const SMARTCAPTCHA_SERVER_KEY = process.env.SMARTCAPTCHA_SERVER_KEY;
const SMARTCAPTCHA_CLIENT_KEY = process.env.SMARTCAPTCHA_CLIENT_KEY;
const PORT = process.env.PORT || 3000;

if (!SMARTCAPTCHA_SERVER_KEY || !SMARTCAPTCHA_CLIENT_KEY) {
  console.error('Задайте переменные окружения SMARTCAPTCHA_SERVER_KEY и SMARTCAPTCHA_CLIENT_KEY.');
  process.exit(1);
}

const app = express();
app.use(express.urlencoded({ extended: false }));

// Страница отдается с подстановкой ключа клиента (sitekey) вместо плейсхолдера __SITEKEY__.
// Ключ клиента публичен, но хранить его удобнее рядом с ключом сервера — в переменных окружения.
const pageTemplate = fs.readFileSync(path.join(__dirname, 'public', 'index.html'), 'utf8');

app.get('/', (req, res) => {
  res.type('html').send(pageTemplate.replaceAll('__SITEKEY__', SMARTCAPTCHA_CLIENT_KEY));
});

/**
 * Проверка токена: POST https://smartcaptcha.yandexcloud.net/validate,
 * параметры secret, token, ip в формате x-www-form-urlencoded.
 *
 * Семантика из документации:
 * - HTTP-код != 200, таймаут или сетевая ошибка -> fail-open (пропускаем пользователя),
 *   чтобы сбой сервиса капчи не блокировал ваших пользователей и не задерживал ответ;
 * - иначе пользователь прошел проверку, только если поле status === "ok".
 *   Поле message — только для диагностики, не сравнивайте его в коде.
 */
async function checkCaptcha(token, ip) {
  const body = new URLSearchParams({
    secret: SMARTCAPTCHA_SERVER_KEY,
    token: token,
    ip: ip, // Параметр необязателен, но передавайте его: это улучшает качество работы SmartCaptcha.
  });

  try {
    const resp = await fetch('https://smartcaptcha.yandexcloud.net/validate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body,
      // Таймаут, чтобы при недоступности сервиса не задерживать обработку запроса пользователя.
      signal: AbortSignal.timeout(1000),
    });

    const content = await resp.text();

    if (resp.status !== 200) {
      console.error(`Allow access due to an error: code=${resp.status}; message=${content}`);
      return true; // fail-open
    }

    return JSON.parse(content).status === 'ok';
  } catch (err) {
    console.error(`Allow access due to an error: ${err.message}`);
    return true; // fail-open: таймаут или сетевая ошибка
  }
}

app.post('/submit', async (req, res) => {
  // Виджет добавляет токен в форму как скрытое поле <input name="smart-token">.
  const token = req.body['smart-token'];

  // Токена нет — пользователь не прошел капчу. В /validate не ходим: без токена ответ будет
  // "status": "failed" с сообщением "Invalid or expired Token".
  if (!token) {
    res.status(400).send('Отклонено: пройдите проверку капчи.');
    return;
  }

  // req.ip: если приложение стоит за обратным прокси, настройте app.set('trust proxy', ...),
  // иначе вместо IP пользователя сюда попадет IP прокси.
  const passed = await checkCaptcha(token, req.ip);

  if (passed) {
    res.send(`Принято: проверка пройдена. Сообщение: ${req.body.message || '(пусто)'}`);
  } else {
    res.status(403).send('Отклонено: проверка капчи не пройдена.');
  }
});

app.listen(PORT, () => {
  console.log(`Пример запущен: http://localhost:${PORT}`);
});
