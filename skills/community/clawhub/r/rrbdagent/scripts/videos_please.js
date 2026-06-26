
const APIClient = require('../api_client');

async function main() {
    console.log('='.repeat(60));
    console.log('获取视频列表');
    console.log('='.repeat(60));
    
    const client = new APIClient();
    
    console.log('\n1. 登录中...');
    const username = client.config.login.default_username;
    const password = client.config.login.default_password;
    
    const loginResult = await client.login(username, password);
    if (!loginResult) {
        console.log('登录失败！');
        return;
    }
    console.log('登录成功！');
    
    console.log('\n2. 获取视频列表...');
    const videoList = await client.get_video_list(1, 10);
    console.log('视频列表响应:', JSON.stringify(videoList, null, 2));
}

main().catch(console.error);
