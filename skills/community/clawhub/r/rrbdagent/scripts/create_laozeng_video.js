
const APIClient = require('../api_client');

async function main() {
    console.log('步骤1: 开始创建视频');
    const client = new APIClient();
    
    console.log('步骤2: 登录中...');
    const username = client.config.login.default_username;
    const password = client.config.login.default_password;
    
    const loginResult = await client.login(username, password);
    if (!loginResult) {
        console.log('登录失败！');
        return;
    }
    console.log('步骤3: 登录成功！');
    
    console.log('步骤4: 检查算力余额...');
    const userInfo = await client.get_user_info();
    const computingAmount = userInfo.data.computingAmount || 0;
    console.log('当前算力余额: ' + computingAmount);
    
    if (computingAmount &lt; 100) {
        console.log('算力不足！');
        return;
    }
    console.log('步骤5: 算力检查通过！');
    
    console.log('步骤6: 获取数字人列表...');
    const virtualManList = await client.get_virtual_man_list();
    let figureId = null;
    if (virtualManList.data) {
        if (Array.isArray(virtualManList.data) &amp;&amp; virtualManList.data.length &gt; 0) {
            figureId = virtualManList.data[0].virtualmanId || virtualManList.data[0].id;
        } else if (virtualManList.data.records &amp;&amp; virtualManList.data.records.length &gt; 0) {
            figureId = virtualManList.data.records[0].virtualmanId || virtualManList.data.records[0].id;
        }
    }
    console.log('选择数字人ID: ' + figureId);
    
    console.log('步骤7: 获取声音列表...');
    const voiceList = await client.get_voice_list();
    let speakerId = null;
    if (voiceList.data) {
        if (Array.isArray(voiceList.data) &amp;&amp; voiceList.data.length &gt; 0) {
            speakerId = voiceList.data[0].speakerId || voiceList.data[0].id;
        } else if (voiceList.data.records &amp;&amp; voiceList.data.records.length &gt; 0) {
            speakerId = voiceList.data.records[0].speakerId || voiceList.data.records[0].id;
        }
    }
    console.log('选择声音ID: ' + speakerId);
    
    console.log('步骤8: 获取模板列表...');
    const templateList = await client.get_template_list();
    let templateId = null;
    if (templateList.data &amp;&amp; templateList.data.results &amp;&amp; templateList.data.results.length &gt; 0) {
        templateId = templateList.data.results[0].id;
    }
    console.log('选择模板ID: ' + templateId);
    
    console.log('步骤9: 创建视频...');
    const title = '老曾大佬的视频标题';
    const script = '一物一码让信任更简单！未来随着技术的不断发展，"一物一码" 将会在更多领域发挥更大的作用，为消费者创造更安全、更便捷、更美好的生活体验。赶快行动起来，体验 "一物一码" 带来的便捷与安心！';
    
    const result = await client.create_video(figureId, speakerId, script, templateId, title);
    if (!result) {
        console.log('视频创建失败！');
        return;
    }
    console.log('步骤10: 视频创建任务已提交！');
    
    let videoId = null;
    if (result.data) {
        if (typeof result.data === 'object') {
            videoId = result.data.id || result.data.videoId;
        } else {
            videoId = result.data;
        }
    }
    console.log('视频任务ID: ' + videoId);
    
    console.log('\n视频创建任务已提交！请等待视频生成完成...');
}

main().catch(console.error);
