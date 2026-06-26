
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
    
    console.log('\n========== 视频列表 ==========');
    let hasData = false;
    if (videoList) {
        if (videoList.data) {
            hasData = true;
        }
    }
    
    if (hasData) {
        let records = [];
        if (Array.isArray(videoList.data)) {
            records = videoList.data;
        } else if (videoList.data.records) {
            records = videoList.data.records;
        }
        
        console.log('找到 ' + records.length + ' 个视频:\n');
        for (let j = 0; j &lt; records.length; j++) {
            const video = records[j];
            console.log((j+1) + '. ' + video.title + ' - ' + video.status);
            if (video.videoFileUrl) {
                console.log('   链接: ' + video.videoFileUrl);
            }
            if (video.videoUrl) {
                console.log('   链接: ' + video.videoUrl);
            }
            console.log('');
        }
    }
}

main().catch(console.error);
