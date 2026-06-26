/**
 * Example: Telegram Bot with OpenClaw Waiting Tips
 *
 * npm install node-telegram-bot-api
 * BOT_TOKEN=xxx node examples/telegram-bot.js
 */
const TelegramBot = require('node-telegram-bot-api');
const { createTelegramTips } = require('../src');

const bot = new TelegramBot(process.env.BOT_TOKEN, { polling: true });
const tips = createTelegramTips(bot, {
  style: 'card',           // 'plain' | 'emoji' | 'zh-only' | 'en-only' | 'card'
  deleteTipAfter: true,    // delete tip after AI responds
  showTyping: true,
});

// Simulate AI response delay
async function fakeAIResponse(text) {
  return new Promise(resolve => {
    setTimeout(() => resolve(`AI Response to: "${text}"\n\nThis is a simulated response.`), 3000);
  });
}

bot.on('message', async (msg) => {
  const chatId = msg.chat.id;
  const text = msg.text;

  if (!text || text.startsWith('/start')) {
    await bot.sendMessage(chatId, 'Send me a message and I\'ll show a tip while "thinking"!');
    return;
  }

  // 1. Show tip while waiting
  const tipHandle = await tips.showTip(chatId);

  // 2. Get AI response (replace with your actual AI call)
  const aiResponse = await fakeAIResponse(text);

  // 3. Replace tip with actual response
  await tips.replaceTip(tipHandle, aiResponse);
});

console.log('Telegram bot started. Send a message to test tips!');
