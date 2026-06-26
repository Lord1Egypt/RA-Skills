/**
 * OpenClaw Waiting Tips - Telegram Adapter
 *
 * Usage:
 *   const { createTelegramTips } = require('./telegram');
 *   const tips = createTelegramTips(bot);
 *
 *   bot.on('message', async (msg) => {
 *     const tipHandle = await tips.showTip(msg.chat.id);
 *     const aiResponse = await getAIResponse(msg.text);
 *     await tips.replaceTip(tipHandle, aiResponse);
 *   });
 */
const { getRandomTip, formatTip } = require('./tips');

function createTelegramTips(bot, options = {}) {
  const {
    style = 'emoji',         // 'plain' | 'emoji' | 'zh-only' | 'en-only' | 'card'
    deleteTipAfter = true,   // delete tip message after AI responds
    showTyping = true,       // send "typing..." action
    prefix = '⏳ AI is thinking...\n\n',
  } = options;

  return {
    /**
     * Send a tip message while waiting for AI response
     * @returns {object} handle with chatId and messageId for later cleanup
     */
    async showTip(chatId) {
      if (showTyping) {
        await bot.sendChatAction(chatId, 'typing');
      }

      const tip = getRandomTip();
      const text = prefix + formatTip(tip, style);
      const sent = await bot.sendMessage(chatId, text, { parse_mode: 'Markdown' });

      return {
        chatId,
        messageId: sent.message_id,
        tip,
      };
    },

    /**
     * Replace the tip with the actual AI response
     */
    async replaceTip(handle, aiResponse) {
      if (!handle) return;

      if (deleteTipAfter) {
        try {
          await bot.deleteMessage(handle.chatId, handle.messageId);
        } catch (e) {
          // message may already be deleted
        }
      }

      await bot.sendMessage(handle.chatId, aiResponse, { parse_mode: 'Markdown' });
    },

    /**
     * Edit the tip message to show the AI response (instead of delete+resend)
     */
    async editTip(handle, aiResponse) {
      if (!handle) return;

      try {
        await bot.editMessageText(aiResponse, {
          chat_id: handle.chatId,
          message_id: handle.messageId,
          parse_mode: 'Markdown',
        });
      } catch (e) {
        // fallback: send new message
        await bot.sendMessage(handle.chatId, aiResponse, { parse_mode: 'Markdown' });
      }
    },
  };
}

module.exports = { createTelegramTips };
