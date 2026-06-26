/**
 * OpenClaw Waiting Tips - Feishu/Lark Adapter
 *
 * Usage:
 *   const { createFeishuTips } = require('./feishu');
 *   const tips = createFeishuTips(feishuClient);
 *
 *   // In message handler:
 *   const tipHandle = await tips.showTip(chatId);
 *   const aiResponse = await getAIResponse(userMessage);
 *   await tips.updateTip(tipHandle, aiResponse);
 */
const { getRandomTip, formatTip } = require('./tips');

function createFeishuTips(client, options = {}) {
  const {
    style = 'card',
    prefix = 'AI is thinking...',
  } = options;

  return {
    /**
     * Send an interactive card with a tip while AI processes
     */
    async showTip(chatId) {
      const tip = getRandomTip();
      const [zh, en] = tip.split(' | ');

      const card = {
        config: { wide_screen_mode: true },
        header: {
          title: { tag: 'plain_text', content: `⏳ ${prefix}` },
          template: 'blue',
        },
        elements: [
          {
            tag: 'div',
            text: {
              tag: 'lark_md',
              content: `💡 **Tips while you wait**\n\n${zh || tip}${en ? `\n${en}` : ''}`,
            },
          },
          {
            tag: 'note',
            elements: [
              { tag: 'plain_text', content: 'OpenClaw is processing your request...' },
            ],
          },
        ],
      };

      const res = await client.im.message.create({
        receive_id_type: 'chat_id',
        data: {
          receive_id: chatId,
          msg_type: 'interactive',
          content: JSON.stringify(card),
        },
      });

      return {
        chatId,
        messageId: res.data.message_id,
        tip,
      };
    },

    /**
     * Update the card with AI response (Feishu cards support in-place update)
     */
    async updateTip(handle, aiResponse) {
      if (!handle) return;

      const card = {
        config: { wide_screen_mode: true },
        header: {
          title: { tag: 'plain_text', content: '🦞 OpenClaw' },
          template: 'green',
        },
        elements: [
          {
            tag: 'div',
            text: {
              tag: 'lark_md',
              content: aiResponse,
            },
          },
        ],
      };

      try {
        await client.im.message.patch({
          path: { message_id: handle.messageId },
          data: { content: JSON.stringify(card) },
        });
      } catch (e) {
        // fallback: send new message
        await client.im.message.create({
          receive_id_type: 'chat_id',
          data: {
            receive_id: handle.chatId,
            msg_type: 'interactive',
            content: JSON.stringify(card),
          },
        });
      }
    },
  };
}

module.exports = { createFeishuTips };
