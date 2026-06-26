const { loadTips, getRandomTip, getRandomTips, formatTip, reloadTips } = require('./tips');
const { createTelegramTips } = require('./telegram');
const { createFeishuTips } = require('./feishu');
const { createWhatsAppTips } = require('./whatsapp');

module.exports = {
  loadTips,
  getRandomTip,
  getRandomTips,
  formatTip,
  reloadTips,
  createTelegramTips,
  createFeishuTips,
  createWhatsAppTips,
};
