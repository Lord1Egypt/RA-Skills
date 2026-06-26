
const fs = require('fs');
const path = require('path');

const configPath = path.join(__dirname, 'config.json');
const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
const API_BASE = config.apiBaseUrl || 'https://rrbd20.yzidea.net/api';

async function main() {
  try {
    console.log('登录中...');
    const loginRes = await fetch(`${API_BASE}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username: config.username, password: config.password })
    });
    const loginData = await loginRes.json();
    const token = loginData.data.token;
    
    console.log('获取视频列表...');
    const videoRes = await fetch(`${API_BASE}/szr/video/page?pageNum=1&amp;pageSize=10`, {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    const videoData = await videoRes.json();
    
    console.log('\n=== 最近视频 ===');
    const videos = videoData.data.records || [];
    videos.forEach((v, i) =&gt; {
      console.log(`${i+1}. ${v.title} - ${v.status}`);
      if (v.videoUrl) console.log(`   ${v.videoUrl}`);
    });
  } catch (e) {
    console.error('错误:', e.message);
  }
}

main();
