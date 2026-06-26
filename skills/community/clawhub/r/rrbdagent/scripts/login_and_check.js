const https = require('https');
const fs = require('fs');
const path = require('path');

const configPath = path.join(__dirname, '../config.json');
const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));

const baseUrl = config.api.base_url;
const tenantId = config.api.tenant_id;
const username = config.login.default_username;
const password = config.login.default_password;

let token = null;

function makeRequest(url, method = 'GET', data = null, authToken = null) {
    return new Promise((resolve, reject) => {
        const urlObj = new URL(url);
        const headers = {
            'Content-Type': 'application/json',
            'X-Tenant-ID': tenantId
        };
        
        if (authToken) {
            headers['Authorization'] = authToken;
        }
        
        const options = {
            hostname: urlObj.hostname,
            path: urlObj.pathname + urlObj.search,
            method: method,
            headers: headers
        };
        
        const req = https.request(options, (res) => {
            let body = '';
            res.on('data', (chunk) => body += chunk);
            res.on('end', () => {
                try {
                    resolve(JSON.parse(body));
                } catch (e) {
                    resolve(body);
                }
            });
        });
        
        req.on('error', reject);
        
        if (data) {
            req.write(JSON.stringify(data));
        }
        
        req.end();
    });
}

async function login() {
    console.log('正在登录...');
    const url = baseUrl + config.endpoints.login;
    const data = { mobile: username, password: password };
    const response = await makeRequest(url, 'POST', data);
    
    if (response && (response.code === 200 || response.code === 0)) {
        if (response.data && response.data.token) {
            token = response.data.token;
            console.log('登录成功！');
            return true;
        }
    }
    console.log('登录失败:', response);
    return false;
}

async function getVideoList() {
    console.log('正在获取视频列表...');
    const url = baseUrl + config.endpoints.video_list + '?pageNum=1&pageSize=15';
    return await makeRequest(url, 'GET', null, token);
}

async function main() {
    console.log('='.repeat(60));
    
    // 登录
    if (!await login()) {
        return;
    }
    
    console.log('='.repeat(60));
    
    // 获取视频列表
    const videoList = await getVideoList();
    
    if (videoList && videoList.data) {
        const data = videoList.data;
        if (data.records) {
            console.log(`\n找到 ${data.records.length} 个视频:`);
            console.log('='.repeat(60));
            
            for (let j = 0; j < Math.min(data.records.length, 10); j++) {
                const video = data.records[j];
                console.log(`\n${j+1}. 标题: ${video.title}`);
                console.log(`   状态: ${video.status}`);
                console.log(`   创建时间: ${video.createDate}`);
                if (video.videoFileUrl) {
                    console.log(`   视频URL: ${video.videoFileUrl}`);
                }
                console.log('-'.repeat(60));
                
                if (video.title === '一物一码让信任更简单') {
                    if (video.status === 'succeed' && video.videoFileUrl) {
                        console.log('\n🎉' + '='.repeat(50) + '🎉');
                        console.log('视频创建成功！');
                        console.log(`视频URL: ${video.videoFileUrl}`);
                        console.log('🎉' + '='.repeat(50) + '🎉');
                    }
                }
            }
        }
    }
}

main().catch(console.error);
