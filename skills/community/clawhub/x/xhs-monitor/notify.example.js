/**
 * 模块5: 飞书消息推送
 * 支持：飞书卡片消息 + 多维表格数据写入
 * 
 * 使用说明：
 * 1. 复制 notify.example.js 为 notify.js
 * 2. 填入自己的飞书配置
 */

const ACCOUNTS = {};  // 从 config.js 导入
const BITABLE_CONFIG = {
  app_token: '你的多维表格app_token',
  table_id: '你的表格ID'
};

const createFeishuCard = (accountName, notes) => {
  const valuableNotes = notes.filter(n => n.isValuable).slice(0, 3);
  
  if (valuableNotes.length === 0) return null;
  
  const productItems = [];
  valuableNotes.forEach(n => {
    if (n.productItems && n.productItems.length > 0) {
      productItems.push(...n.productItems);
    }
  });
  
  const liveTimes = [];
  valuableNotes.forEach(n => {
    if (n.liveTime) liveTimes.push(n.liveTime);
  });
  
  // 从config获取账号URL
  const { getAccountUrl } = require('./config');
  const profileUrl = getAccountUrl(accountName) || 'https://www.xiaohongshu.com/';
  
  return {
    msg_type: "interactive",
    card: {
      config: { wide_screen_mode: true, enable_forward: true },
      header: {
        template: "red",
        title: { content: `🚨 竞品情报：${accountName} 有新动作`, tag: "plain_text" }
      },
      elements: [
        {
          tag: "markdown",
          content: `**📝 笔记一句话总结：**\n${valuableNotes[0].title ? '📌 ' + valuableNotes[0].title + '\n' : ''}${valuableNotes[0].content || valuableNotes[0].rawTextSummary}`
        },
        {
          tag: "div",
          fields: [
            { is_short: true, text: { tag: "lark_md", content: `**🛒 提及商品：**\n${productItems.length > 0 ? productItems.join(', ') : '无'}` } },
            { is_short: true, text: { tag: "lark_md", content: `**⏰ 开播时间：**\n<font color='red'>${liveTimes.length > 0 ? liveTimes.join(', ') : '未提及'}</font>` } }
          ]
        },
        { tag: "hr" },
        { tag: "div", text: { tag: "lark_md", content: `**价值判断：** ✅ 有价值 (${valuableNotes.length}条)` } },
        {
          tag: "action",
          actions: [{
            tag: "button",
            text: { content: "📱 跳转小红书", tag: "plain_text" },
            type: "primary",
            value: { action_type: "open_url" },
            multi_url: { url: profileUrl, android_url: profileUrl, ios_url: profileUrl, pc_url: profileUrl }
          }]
        },
        { tag: "note", elements: [{ tag: "plain_text", content: `🤖 OpenClaw 自动抓取 | 仅供内部参考` }] }
      ]
    }
  };
};

module.exports = { createFeishuCard, BITABLE_CONFIG };
