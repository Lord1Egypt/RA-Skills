/**
 * Example: WhatsApp Bot with OpenClaw Waiting Tips (Baileys)
 *
 * npm install @whiskeysockets/baileys
 * node examples/whatsapp-bot.js
 */
const { default: makeWASocket, useMultiFileAuthState } = require('@whiskeysockets/baileys');
const { createWhatsAppTips } = require('../src');

async function start() {
  const { state, saveCreds } = await useMultiFileAuthState('./auth');
  const sock = makeWASocket({ auth: state });
  sock.ev.on('creds.update', saveCreds);

  const tips = createWhatsAppTips(sock, {
    style: 'emoji',
    library: 'baileys',
  });

  // Simulate AI response delay
  async function fakeAIResponse(text) {
    return new Promise(resolve => {
      setTimeout(() => resolve(`AI Response to: "${text}"\n\nThis is a simulated response.`), 3000);
    });
  }

  sock.ev.on('messages.upsert', async ({ messages }) => {
    const msg = messages[0];
    if (!msg.message || msg.key.fromMe) return;

    const jid = msg.key.remoteJid;
    const text = msg.message.conversation || msg.message.extendedTextMessage?.text || '';

    // 1. Show typing + tip
    const tipHandle = await tips.showTip(jid);

    // 2. Get AI response
    const aiResponse = await fakeAIResponse(text);

    // 3. Send actual response
    await tips.replaceTip(tipHandle, aiResponse);
  });

  console.log('WhatsApp bot started. Scan QR code to connect.');
}

start();
