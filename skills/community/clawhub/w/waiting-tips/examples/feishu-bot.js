/**
 * Example: Feishu/Lark Bot with OpenClaw Waiting Tips
 *
 * npm install @larksuiteoapi/node-sdk
 * APP_ID=xxx APP_SECRET=xxx node examples/feishu-bot.js
 */
const lark = require('@larksuiteoapi/node-sdk');
const { createFeishuTips } = require('../src');

const client = new lark.Client({
  appId: process.env.APP_ID,
  appSecret: process.env.APP_SECRET,
});

const tips = createFeishuTips(client, {
  style: 'card',
  prefix: 'OpenClaw is thinking...',
});

// Simulate AI response delay
async function fakeAIResponse(text) {
  return new Promise(resolve => {
    setTimeout(() => resolve(`**AI Response**\n\nYou asked: "${text}"\n\nThis is a simulated response.`), 3000);
  });
}

// Message event handler (use with Feishu event subscription)
async function handleMessage(event) {
  const chatId = event.message.chat_id;
  const text = event.message.content;

  // 1. Show tip card while waiting
  const tipHandle = await tips.showTip(chatId);

  // 2. Get AI response
  const aiResponse = await fakeAIResponse(text);

  // 3. Update card in-place with response (Feishu's killer feature!)
  await tips.updateTip(tipHandle, aiResponse);
}

module.exports = { handleMessage };
console.log('Feishu handler ready. Wire up with your event subscription.');
