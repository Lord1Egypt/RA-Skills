/**
 * 飞书消息推送 - Webhook 机器人方式
 * 使用自定义机器人 Webhook URL
 */

const https = require('https');

/**
 * 发送文本消息到飞书
 */
async function sendToFeishu(content) {
  const webhookUrl = process.env.FEISHU_WEBHOOK_URL;
  
  if (!webhookUrl) {
    throw new Error('未配置 FEISHU_WEBHOOK_URL 环境变量');
  }
  
  const message = {
    msg_type: 'text',
    content: {
      text: content
    }
  };
  
  return new Promise((resolve, reject) => {
    const data = JSON.stringify(message);
    const url = new URL(webhookUrl);
    
    const options = {
      hostname: url.hostname,
      port: url.port || 443,
      path: url.pathname + url.search,
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(data)
      }
    };
    
    const req = https.request(options, (res) => {
      let body = '';
      res.on('data', (chunk) => body += chunk);
      res.on('end', () => {
        try {
          const response = JSON.parse(body);
          if (response.StatusCode === 0 || response.code === 0 || response.msg === 'success') {
            resolve({ success: true, response });
          } else {
            reject(new Error(`飞书返回错误：${JSON.stringify(response)}`));
          }
        } catch (e) {
          resolve({ success: true, raw: body });
        }
      });
    });
    
    req.on('error', reject);
    req.write(data);
    req.end();
  });
}

/**
 * 发送富文本卡片消息（可选升级）
 */
async function sendFeishuCard(reportData) {
  const webhookUrl = process.env.FEISHU_WEBHOOK_URL;
  if (!webhookUrl) throw new Error('未配置 FEISHU_WEBHOOK_URL');
  
  const message = {
    msg_type: 'interactive',
    card: {
      config: {
        wide_screen_mode: true
      },
      header: {
        template: 'blue',
        title: {
          tag: 'plain_text',
          content: '📡 Tech Radar Daily'
        }
      },
      elements: [
        {
          tag: 'markdown',
          content: formatCardContent(reportData)
        }
      ]
    }
  };
  
  return new Promise((resolve, reject) => {
    const data = JSON.stringify(message);
    const url = new URL(webhookUrl);
    
    const options = {
      hostname: url.hostname,
      port: url.port || 443,
      path: url.pathname + url.search,
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(data)
      }
    };
    
    const req = https.request(options, (res) => {
      let body = '';
      res.on('data', (chunk) => body += chunk);
      res.on('end', () => {
        try {
          const response = JSON.parse(body);
          if (response.StatusCode === 0 || response.code === 0) {
            resolve({ success: true });
          } else {
            reject(new Error(`发送失败：${response.msg}`));
          }
        } catch (e) {
          resolve({ success: true, raw: body });
        }
      });
    });
    
    req.on('error', reject);
    req.write(data);
    req.end();
  });
}

/**
 * 格式化卡片内容
 */
function formatCardContent(reportData) {
  let content = `**今日精选 ${reportData.items.length} 条技术情报**\n\n`;
  
  reportData.items.forEach((item, i) => {
    content += `${i + 1}. **${item.name || item.title}** ${item.confidenceEmoji || ''}\n`;
    content += `${item.summary || item.description}\n`;
    content += `[查看详情](${item.url || item.hnUrl})\n\n`;
  });
  
  return content;
}

/**
 * 测试推送
 */
async function testPush() {
  const testMessage = `📡 Tech Radar Daily 测试推送

这是一条测试消息，确认飞书 Webhook 配置正确。

测试时间：${new Date().toISOString()}
`;
  
  try {
    await sendToFeishu(testMessage);
    console.log('✅ 测试推送成功！');
    return true;
  } catch (error) {
    console.error('❌ 测试推送失败:', error.message);
    return false;
  }
}

// ============ 导出 ============

module.exports = {
  sendToFeishu,
  sendFeishuCard,
  testPush
};
