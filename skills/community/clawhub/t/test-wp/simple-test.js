// 简单测试WordPress连接
const https = require('https');

console.log('测试WordPress连接...');
console.log('站点: https://your-site.com');

// 尝试访问WordPress REST API
const options = {
  hostname: 'openow.ai',
  port: 443,
  path: '/wp-json/wp/v2/posts',
  method: 'GET',
  headers: {
    'User-Agent': 'OpenClaw-Test/1.0'
  }
};

const req = https.request(options, (res) => {
  console.log(`状态码: ${res.statusCode}`);
  console.log(`状态消息: ${res.statusMessage}`);
  
  let data = '';
  res.on('data', (chunk) => {
    data += chunk;
  });
  
  res.on('end', () => {
    if (res.statusCode === 200) {
      console.log('✅ WordPress REST API可访问');
      try {
        const posts = JSON.parse(data);
        console.log(`找到 ${posts.length} 篇文章`);
      } catch (e) {
        console.log('响应数据:', data.substring(0, 200));
      }
    } else {
      console.log('响应:', data);
    }
  });
});

req.on('error', (e) => {
  console.error(`❌ 连接错误: ${e.message}`);
});

req.end();