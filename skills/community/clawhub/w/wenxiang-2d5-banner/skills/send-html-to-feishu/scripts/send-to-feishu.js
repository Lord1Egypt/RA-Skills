// 发送文件到飞书脚本
// 使用飞书 Webhook 发送文件

const axios = require('axios');
const fs = require('fs');
const FormData = require('form-data');
const path = require('path');

async function sendToFeishu(filePath, message) {
  // 获取 Webhook URL
  const webhookUrl = process.env.FEISHU_WEBHOOK;
  
  if (!webhookUrl) {
    console.error('❌ 错误：FEISHU_WEBHOOK 环境变量未设置');
    console.error('   请设置：export FEISHU_WEBHOOK="https://open.feishu.cn/open-apis/bot/v2/hook/xxx"');
    process.exit(1);
  }

  // 验证文件
  if (!fs.existsSync(filePath)) {
    console.error(`❌ 文件不存在：${filePath}`);
    process.exit(1);
  }

  console.log(`📤 发送文件到飞书`);
  console.log(`   文件：${filePath}`);
  console.log(`   消息：${message || '(自动生成)'}`);

  try {
    // 读取文件
    const fileData = fs.readFileSync(filePath);
    const fileName = path.basename(filePath);
    
    // 创建 FormData
    const formData = new FormData();
    formData.append('file', fileData, {
      filename: fileName,
      contentType: 'application/pdf'
    });

    // 上传文件到飞书
    console.log(`⬆️ 上传文件...`);
    const uploadResponse = await axios.post(
      'https://open.feishu.cn/open-apis/im/v1/files',
      formData,
      {
        headers: {
          ...formData.getHeaders(),
          'Authorization': `Bearer ${getAccessToken()}`
        }
      }
    );

    const fileKey = uploadResponse.data.data.id;
    console.log(`✅ 文件上传成功：${fileKey}`);

    // 发送消息
    console.log(`💬 发送消息...`);
    const messagePayload = {
      receive_id: getReceiveId(),
      msg_type: 'file',
      content: JSON.stringify({
        file_key: fileKey,
        file_type: 'pdf'
      })
    };

    const messageResponse = await axios.post(
      `https://open.feishu.cn/open-apis/im/v1/messages`,
      messagePayload,
      {
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${getAccessToken()}`
        },
        params: {
          receive_id_type: 'open_id'
        }
      }
    );

    console.log(`✅ 消息发送成功：${messageResponse.data.data.message_id}`);
    console.log(`MEDIA: ${filePath}`);
    
  } catch (error) {
    console.error(`❌ 错误：${error.message}`);
    if (error.response) {
      console.error(`   状态码：${error.response.status}`);
      console.error(`   响应：${JSON.stringify(error.response.data)}`);
    }
    process.exit(1);
  }
}

// 获取 Access Token（简化版，实际应该缓存）
function getAccessToken() {
  const appAccessToken = process.env.FEISHU_APP_ACCESS_TOKEN;
  if (!appAccessToken) {
    console.warn('⚠️ 警告：FEISHU_APP_ACCESS_TOKEN 未设置，使用 Webhook 模式');
    return '';
  }
  return appAccessToken;
}

// 获取 Receive ID（简化版）
function getReceiveId() {
  return process.env.FEISHU_RECEIVE_ID || 'ou_e3a0d4a64a9e0932ee919b97f17ec210';
}

// 命令行参数
const args = process.argv.slice(2);
const filePath = args[0];
const message = args.slice(1).join(' ');

if (!filePath) {
  console.error('用法：node send-to-feishu.js <file.pdf> [message]');
  process.exit(1);
}

sendToFeishu(filePath, message);
