/**
 * OpenClaw Waiting Tips - WhatsApp Adapter (via whatsapp-web.js or Baileys)
 *
 * Usage:
 *   const { createWhatsAppTips } = require('./whatsapp');
 *   const tips = createWhatsAppTips(sock); // Baileys socket or whatsapp-web.js client
 *
 *   // In message handler:
 *   const tipHandle = await tips.showTip(remoteJid);
 *   const aiResponse = await getAIResponse(userMessage);
 *   await tips.replaceTip(tipHandle, aiResponse);
 */
const { getRandomTip, formatTip } = require('./tips');

function createWhatsAppTips(sock, options = {}) {
  const {
    style = 'emoji',
    library = 'baileys',  // 'baileys' | 'whatsapp-web.js'
    prefix = '⏳ AI is thinking...\n\n',
  } = options;

  // Baileys adapter
  const baileys = {
    async showTip(jid) {
      await sock.presenceSubscribe(jid);
      await sock.sendPresenceUpdate('composing', jid);

      const tip = getRandomTip();
      const text = prefix + formatTip(tip, style);
      const sent = await sock.sendMessage(jid, { text });

      await sock.sendPresenceUpdate('paused', jid);

      return { jid, messageKey: sent.key, tip };
    },

    async replaceTip(handle, aiResponse) {
      if (!handle) return;
      // WhatsApp doesn't support editing — send AI response as new message
      await sock.sendMessage(handle.jid, { text: aiResponse });
    },
  };

  // whatsapp-web.js adapter
  const webjs = {
    async showTip(chatId) {
      const chat = await sock.getChatById(chatId);
      await chat.sendStateTyping();

      const tip = getRandomTip();
      const text = prefix + formatTip(tip, style);
      const sent = await chat.sendMessage(text);

      await chat.clearState();

      return { chatId, messageId: sent.id._serialized, message: sent, tip };
    },

    async replaceTip(handle, aiResponse) {
      if (!handle) return;
      const chat = await sock.getChatById(handle.chatId);
      await chat.sendMessage(aiResponse);
    },
  };

  return library === 'baileys' ? baileys : webjs;
}

module.exports = { createWhatsAppTips };
