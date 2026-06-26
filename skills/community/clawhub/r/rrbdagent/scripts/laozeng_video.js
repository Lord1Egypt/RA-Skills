
const APIClient = require('../api_client');

async function main() {
    console.log('='.repeat(60));
    console.log('RRBD 视频生成（老曾大佬的视频标题）');
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
    
    console.log('\n2. 获取模板列表...');
    const templateList = await client.get_template_list();
    const templateId = templateList.data.results[0].id;
    console.log('选择模板ID: ' + templateId);
    
    console.log('\n3. 获取数字人形象列表...');
    const virtualManList = await client.get_virtual_man_list();
    let figureId = null;
    if (virtualManList.data) {
        if (virtualManList.data.records) {
            if (virtualManList.data.records.length &gt; 0) {
                figureId = virtualManList.data.records[0].virtualmanId;
                if (!figureId) {
                    figureId = virtualManList.data.records[0].id;
                }
            }
        }
    }
    console.log('选择数字人ID: ' + figureId);
    
    console.log('\n4. 获取声音列表...');
    const voiceList = await client.get_voice_list();
    let speakerId = null;
    if (voiceList.data) {
        if (voiceList.data.records) {
            if (voiceList.data.records.length &gt; 0) {
                speakerId = voiceList.data.records[0].speakerId;
                if (!speakerId) {
                    speakerId = voiceList.data.records[0].id;
                }
            }
        }
    }
    console.log('选择声音ID: ' + speakerId);
    
    const title = '老曾大佬的视频标题';
    const script = '一物一码让信任更简单！未来随着技术的不断发展，"一物一码" 将会在更多领域发挥更大的作用，为消费者创造更安全、更便捷、更美好的生活体验。赶快行动起来，体验 "一物一码" 带来的便捷与安心！';
    
    console.log('\n5. 创建视频...');
    console.log('标题: ' + title);
    console.log('文案: ' + script);
    
    const createResult = await client.create_video(figureId, speakerId, script, templateId, title);
    console.log('创建结果:', JSON.stringify(createResult, null, 2));
    
    if (createResult) {
        console.log('\n视频创建任务已提交成功！');
    }
}

main().catch(console.error);
