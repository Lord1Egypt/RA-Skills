const APIClient = require('../api_client');

async function main() {
    console.log('='.repeat(60));
    console.log('测试 SZR 前缀 API');
    console.log('='.repeat(60));
    
    // 初始化 API 客户端
    const client = new APIClient();
    
    // 登录
    console.log('\n1. 登录中...');
    const username = client.config.login.default_username;
    const password = client.config.login.default_password;
    console.log(`   账号: ${username}`);
    
    const loginResult = await client.login(username, password);
    if (!loginResult) {
        console.log('❌ 登录失败！');
        return;
    }
    console.log('✅ 登录成功！');
    
    // 获取用户信息
    console.log('\n2. 获取用户信息...');
    const userInfo = await client.get_user_info();
    console.log('用户信息响应:', JSON.stringify(userInfo, null, 2));
    
    // 用 SZR 前缀的 API 手动获取数字人列表
    console.log('\n3. 手动获取数字人列表 (szr 前缀)...');
    const https = require('https');
    const url = new URL(client.base_url + '/digital/szrVirtualMan/page');
    const headers = {
        'Content-Type': 'application/json',
        'Authorization': client.token,
        'X-Tenant-ID': client.tenant_id
    };
    
    const params = {
        'pageNum': 1,
        'pageSize': 100
    };
    url.search = new URLSearchParams(params).toString();
    
    const options = {
        hostname: url.hostname,
        path: url.pathname + url.search,
        method: 'GET',
        headers: headers
    };
    
    const virtualManResult = await new Promise((resolve, reject) => {
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
        req.end();
    });
    
    console.log('数字人列表 (szr 前缀):', JSON.stringify(virtualManResult, null, 2));
    
    // 获取声音列表 (szr 前缀)
    console.log('\n4. 手动获取声音列表 (szr 前缀)...');
    const voiceUrl = new URL(client.base_url + '/digital/szrVoice/page');
    voiceUrl.search = new URLSearchParams(params).toString();
    const voiceOptions = {
        hostname: voiceUrl.hostname,
        path: voiceUrl.pathname + voiceUrl.search,
        method: 'GET',
        headers: headers
    };
    
    const voiceResult = await new Promise((resolve, reject) => {
        const req = https.request(voiceOptions, (res) => {
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
        req.end();
    });
    
    console.log('声音列表 (szr 前缀):', JSON.stringify(voiceResult, null, 2));
    
    // 获取模板列表 (szr 前缀)
    console.log('\n5. 手动获取模板列表 (szr 前缀)...');
    const templateUrl = new URL(client.base_url + '/digital/szrVideo/clipTemplate');
    const templateParams = {
        'pageNum': 1,
        'pageSize': 100,
        'scene': 'virtualman'
    };
    templateUrl.search = new URLSearchParams(templateParams).toString();
    const templateOptions = {
        hostname: templateUrl.hostname,
        path: templateUrl.pathname + templateUrl.search,
        method: 'GET',
        headers: headers
    };
    
    const templateResult = await new Promise((resolve, reject) => {
        const req = https.request(templateOptions, (res) => {
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
        req.end();
    });
    
    console.log('模板列表 (szr 前缀):', JSON.stringify(templateResult, null, 2));
}

main().catch(console.error);
