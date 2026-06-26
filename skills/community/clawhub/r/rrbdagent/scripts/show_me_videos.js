
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
    return new Promise((resolve, reject) =&gt; {
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
        
        const req = https.request(options, (res) =&gt; {
            let body = '';
            res.on('data', (chunk) =&gt; body += chunk);
            res.on('end', () =&gt; {
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
    console.log('步骤1: 正在登录...');
    const url = baseUrl + config.endpoints.login;
    const data = { mobile: username, password: password };
    const response = await makeRequest(url, 'POST', data);
    
    if (response &amp;&amp; (response.code === 200 || response.code === 0)) {
        if (response.data &amp;&amp; response.data.token) {
            token = response.data.token;
            console.log('步骤2: 登录成功！');
            return true;
        }
    }
    console.log('登录失败:', response);
    return false;
}

async function getVideoList() {
    console.log('步骤3: 正在获取视频列表...');
    const url = baseUrl + config.endpoints.video_list + '?pageNum=1&amp;pageSize=15';
    return await makeRequest(url, 'GET', null, token);
}

async function main() {
    console.log('开始检查视频状态！\n');
    
    if (!await login()) {
        return;
    }
    
    const videoList = await getVideoList();
    console.log('\n步骤4: 收到视频列表响应！');
    console.log('完整响应:', JSON.stringify(videoList, null, 2));
    
    console.log('\n========== 视频列表 ==========');
    if (videoList &amp;&amp; videoList.data) {
        const data = videoList.data;
        if (data.records) {
            console.log(`找到 ${data.records.length} 个视频！\n`);
            for (let j = 0; j &lt; data.records.length; j++) {
                const video = data.records[j];
                console.log(`${j+1}. 【${video.title}】`);
                console.log(`   状态: ${video.status}`);
                if (video.videoFileUrl) {
                    console.log(`   链接: ${video.videoFileUrl}`);
                }
                if (video.videoUrl) {
                    console.log(`   链接2: ${video.videoUrl}`);
                }
                console.log('');
            }
        }
    }
}

main().catch(err =&gt; {
    console.error('出错了:', err);
});
