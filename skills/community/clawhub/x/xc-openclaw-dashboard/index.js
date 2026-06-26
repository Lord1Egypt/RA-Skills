/**
 * OpenClaw Dashboard - Skill 入口
 * 处理 /status-card, /sessions, /status 命令
 */

const collector = require('./scripts/collector.js');

/**
 * 发送飞书状态卡片
 */
async function sendStatusCard() {
  try {
    const data = await collector.collectDashboardData();
    const card = collector.buildFeishuCard(data);
    return { success: true, data, card };
  } catch (err) {
    return { success: false, error: err.message };
  }
}

/**
 * 获取简要状态文本
 */
async function getStatusText() {
  try {
    const data = await collector.collectDashboardData();
    return collector.getStatusText(data);
  } catch (err) {
    return `获取状态失败: ${err.message}`;
  }
}

/**
 * 获取 Session 列表
 */
async function getSessionsList() {
  try {
    const data = await collector.collectDashboardData();
    return collector.getSessionsText(data);
  } catch (err) {
    return `获取 Session 失败: ${err.message}`;
  }
}

// 导出函数
module.exports = {
  sendStatusCard,
  getStatusText,
  getSessionsList
};

// 命令行测试
if (require.main === module) {
  const cmd = process.argv[2] || 'status';
  
  (async () => {
    let result;
    switch (cmd) {
      case 'card':
        result = await sendStatusCard();
        console.log(JSON.stringify(result, null, 2));
        break;
      case 'sessions':
        result = await getSessionsList();
        console.log(result);
        break;
      case 'status':
      default:
        result = await getStatusText();
        console.log(result);
    }
  })();
}
