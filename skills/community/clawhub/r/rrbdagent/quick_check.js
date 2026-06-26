
const fs = require('fs');
const path = require('path');
const config = JSON.parse(fs.readFileSync(path.join(__dirname, 'config.json'), 'utf8'));
const API_BASE = config.apiBaseUrl || 'https://rrbd20.yzidea.net/api';

async function go() {
  const login = await fetch(API_BASE + '/auth/login', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({username: config.username, password: config.password})
  });
  const data = await login.json();
  const token = data.data.token;
  
  const videos = await fetch(API_BASE + '/szr/video/page?pageNum=1&amp;pageSize=10', {
    headers: {'Authorization': 'Bearer ' + token}
  });
  const vdata = await videos.json();
  const list = vdata.data.records || [];
  
  console.log('=== 视频列表 ===');
  for (let k = 0; k &lt; list.length; k++) {
    const v = list[k];
    console.log((k+1) + '. ' + v.title + ' - ' + v.status);
    if (v.videoUrl) console.log('   ' + v.videoUrl);
  }
}

go().catch(console.error);
