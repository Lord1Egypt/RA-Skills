
const fs = require('fs');
const path = require('path');

// 读取配置
const configPath = path.join(__dirname, '..', 'config.json');
const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));

const API_BASE = config.apiBaseUrl || 'https://rrbd20.yzidea.net/api';

async function checkVideoStatus() {
  try {
    // 1. 登录
    console.log('正在登录...');
    const loginResponse = await fetch(`${API_BASE}/auth/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        username: config.username,
        password: config.password
      })
    });
    
    if (!loginResponse.ok) {
      throw new Error(`登录失败: ${loginResponse.status}`);
    }
    
    const loginData = await loginResponse.json();
    const token = loginData.data.token;
    console.log('登录成功！');
    
    // 2. 查看视频列表
    console.log('\n正在获取视频列表...');
    const videoListResponse = await fetch(`${API_BASE}/szr/video/page?pageNum=1&amp;pageSize=10`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    
    if (!videoListResponse.ok) {
      throw new Error(`获取视频列表失败: ${videoListResponse.status}`);
    }
    
    const videoListData = await videoListResponse.json();
    console.log('\n最近的视频:');
    
    const videos = videoListData.data.records || [];
    for (let i = 0; i &lt; videos.length; i++) {
      const video = videos[i];
      console.log(`${i + 1}. ${video.title} - ${video.status} (${video.id})`);
      if (video.videoUrl) {
        console.log(`   链接: ${video.videoUrl}`);
      }
    }
    
  } catch (error) {
    console.error('错误:', error.message);
  }
}

checkVideoStatus();
