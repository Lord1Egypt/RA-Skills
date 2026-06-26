const https = require('https');
const fs = require('fs');
const path = require('path');

const configPath = path.join(__dirname, '../config.json');
const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));

const baseUrl = config.api.base_url;
const tenantId = config.api.tenant_id;
const username = config.login.default_username;
const password = config.login.default_password;

// Step 1: Login
console.log('1. 登录中...');
const loginUrl = new URL(baseUrl + config.endpoints.login);
const loginData = JSON.stringify({ mobile: username, password: password });

const loginOptions = {
    hostname: loginUrl.hostname,
    path: loginUrl.pathname,
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'X-Tenant-ID': tenantId,
        'Content-Length': Buffer.byteLength(loginData)
    }
};

const loginReq = https.request(loginOptions, (loginRes) => {
    let loginBody = '';
    loginRes.on('data', (chunk) => loginBody += chunk);
    loginRes.on('end', () => {
        const loginResult = JSON.parse(loginBody);
        console.log('登录响应:', loginBody);
        
        if (loginResult.data && loginResult.data.token) {
            const token = loginResult.data.token;
            console.log('Token 获取成功！');
            
            // Step 2: Get video list
            console.log('\n2. 获取视频列表...');
            const videoUrl = new URL(baseUrl + config.endpoints.video_list + '?pageNum=1&pageSize=15');
            
            const videoOptions = {
                hostname: videoUrl.hostname,
                path: videoUrl.pathname + videoUrl.search,
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': token,
                    'X-Tenant-ID': tenantId
                }
            };
            
            const videoReq = https.request(videoOptions, (videoRes) => {
                let videoBody = '';
                videoRes.on('data', (chunk) => videoBody += chunk);
                videoRes.on('end', () => {
                    console.log('视频列表响应:', videoBody);
                    
                    const videoResult = JSON.parse(videoBody);
                    if (videoResult.data && videoResult.data.records) {
                        console.log('\n找到', videoResult.data.records.length, '个视频:');
                        videoResult.data.records.slice(0, 5).forEach((video, i) => {
                            console.log(`\n${i+1}. 标题: ${video.title}`);
                            console.log(`   状态: ${video.status}`);
                            if (video.videoFileUrl) {
                                console.log(`   URL: ${video.videoFileUrl}`);
                            }
                        });
                    }
                });
            });
            
            videoReq.on('error', (e) => console.error('视频列表请求错误:', e));
            videoReq.end();
        }
    });
});

loginReq.on('error', (e) => console.error('登录请求错误:', e));
loginReq.write(loginData);
loginReq.end();
