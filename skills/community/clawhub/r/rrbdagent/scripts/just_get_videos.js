
const APIClient = require('../api_client');

async function main() {
    console.log('开始获取视频！');
    
    const client = new APIClient();
    
    console.log('1. 登录中...');
    const username = client.config.login.default_username;
    const password = client.config.login.default_password;
    
    const loginResult = await client.login(username, password);
    if (!loginResult) {
        console.log('登录失败！');
        return;
    }
    console.log('2. 登录成功！');
    
    console.log('3. 获取视频列表...');
    const videoList = await client.get_video_list(1, 10);
    console.log('4. 收到响应！');
    console.log('完整视频列表:', JSON.stringify(videoList, null, 2));
    
    console.log('\n========== 视频列表 ==========');
    if (videoList &amp;&amp; videoList.data) {
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

main().catch(function(err) {
    console.error('出错了:', err);
});
