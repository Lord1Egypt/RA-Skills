const https = require('https');

async function getChatList() {
  const token = await new Promise((resolve, reject) => {
    const data = JSON.stringify({
      app_id: process.env.FEISHU_APP_ID,
      app_secret: process.env.FEISHU_APP_SECRET
    });
    
    const req = https.request({
      hostname: 'open.feishu.cn',
      port: 443,
      path: '/open-apis/auth/v3/tenant_access_token/internal',
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Content-Length': data.length }
    }, res => {
      let body = '';
      res.on('data', chunk => body += chunk);
      res.on('end', () => resolve(JSON.parse(body).tenant_access_token));
    });
    req.on('error', reject);
    req.write(data);
    req.end();
  });
  
  console.log('✅ Token 获取成功');
  
  // 获取群列表
  const req = https.request({
    hostname: 'open.feishu.cn',
    port: 443,
    path: '/open-apis/im/v1/chats?page_size=10',
    method: 'GET',
    headers: {
      'Authorization': 'Bearer ' + token,
      'Content-Type': 'application/json'
    }
  }, res => {
    let body = '';
    res.on('data', chunk => body += chunk);
    res.on('end', () => {
      const result = JSON.parse(body);
      if (result.code === 0) {
        console.log('\n📋 可用群组列表：');
        result.data.items.forEach((chat, i) => {
          console.log(`${i + 1}. ${chat.name} (ID: ${chat.chat_id})`);
        });
        console.log('\n👉 选择一个群 ID，告诉我配置 FEISHU_CHAT_ID');
      } else {
        console.log('❌ 获取群列表失败:', result.msg);
        console.log('💡 请手动提供群 ID，或在飞书群设置中查看');
      }
    });
  });
  req.on('error', console.error);
  req.end();
}

getChatList();
