// Telegram Mini App Deep Link Helper
//
// OpenClaw agent inline_keyboard gönderemiyor. Bunun yerine t.me deep link'ini
// plain text olarak yolluyoruz — Telegram client onu otomatik "Open" butonuna
// çeviriyor. Tek tık ile Mini App açılır, üstelik link her grupta paylaşılınca
// aynı butonu gösterir (viral hook).
//
// Sidecar bot kullanmak istersen `bot.js` dosyası klasik inline_keyboard yolunu
// hâlâ destekliyor (web_app button via node-telegram-bot-api).

const BOT_USERNAME = process.env.BOT_USERNAME || 'OpenClawTamagotchi_bot';
const APP_SHORT_NAME = process.env.APP_SHORT_NAME || 'pet';

function petLink(startParam) {
  const base = `https://t.me/${BOT_USERNAME}/${APP_SHORT_NAME}`;
  return startParam ? `${base}?startapp=${startParam}` : base;
}

function petMessage() {
  return `🐣 OpenClaw Pet seni bekliyor!\n\n${petLink()}\n\n🥚 Yumurtaya dokun, hayvanını keşfet → 🐧🐱🐕🐠🐥`;
}

function visitLink(userId) {
  return petLink(`pet_${userId}`);
}

module.exports = { petLink, petMessage, visitLink };
