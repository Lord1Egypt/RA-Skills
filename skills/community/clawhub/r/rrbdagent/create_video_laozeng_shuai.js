const APIClient = require('./api_client');

async function main() {
    console.log('='.repeat(60));
    console.log('RRBD 视频生成 - 老曾你真帅');
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
        console.log('登录失败！');
        return;
    }
    
    console.log('\n2. 获取模板列表...');
    const templateList = await client.get_template_list();
    if (!templateList || !templateList.data || !templateList.data.results) {
        console.log('获取模板列表失败！');
        return;
    }
    
    // 打印所有可用模板
    console.log('   可用模板列表:');
    templateList.data.results.forEach((template, index) => {
        console.log(`   ${index + 1}. ${template.name} (ID: ${template.id})`);
    });
    
    // 随机选择一个模板
    const templateIndex = Math.floor(Math.random() * templateList.data.results.length);
    const templateId = templateList.data.results[templateIndex].id;
    const templateName = templateList.data.results[templateIndex].name;
    console.log(`\n   选择模板: ${templateName} (ID: ${templateId})`);
    
    console.log('\n3. 获取数字人形象列表...');
    const virtualManList = await client.get_virtual_man_list();
    if (!virtualManList) {
        console.log('获取数字人形象列表失败！');
        return;
    }
    
    let figureId = null;
    if (virtualManList.data) {
        if (Array.isArray(virtualManList.data) && virtualManList.data.length > 0) {
            figureId = virtualManList.data[0].virtualmanId || virtualManList.data[0].id;
        } else if (virtualManList.data.records && virtualManList.data.records.length > 0) {
            figureId = virtualManList.data.records[0].virtualmanId || virtualManList.data.records[0].id;
        }
    }
    
    if (!figureId) {
        console.log('未找到数字人形象！');
        return;
    }
    console.log(`   选择数字人ID: ${figureId}`);
    
    console.log('\n4. 获取声音列表...');
    const voiceList = await client.get_voice_list();
    if (!voiceList) {
        console.log('获取声音列表失败！');
        return;
    }
    
    let speakerId = null;
    if (voiceList.data) {
        if (Array.isArray(voiceList.data) && voiceList.data.length > 0) {
            speakerId = voiceList.data[0].speakerId || voiceList.data[0].id;
        } else if (voiceList.data.records && voiceList.data.records.length > 0) {
            speakerId = voiceList.data.records[0].speakerId || voiceList.data.records[0].id;
        }
    }
    
    if (!speakerId) {
        console.log('未找到声音！');
        return;
    }
    console.log(`   选择声音ID: ${speakerId}`);
    
    // 视频信息
    const title = '老曾你真帅';
    const script = '一物一码让信任更简单！未来随着技术的不断发展，"一物一码" 将会在更多领域发挥更大的作用，为消费者创造更安全、更便捷、更美好的生活体验。赶快行动起来，体验 "一物一码" 带来的便捷与安心！';
    
    console.log('\n5. 创建视频...');
    console.log(`   标题: ${title}`);
    console.log(`   文案: ${script}`);
    console.log(`   使用模板: ${templateName}`);
    
    const createResult = await client.create_video(figureId, speakerId, script, templateId, title);
    if (!createResult) {
        console.log('视频创建失败！');
        return;
    }
    
    console.log('\n✅ 视频创建任务已提交！');
    console.log('='.repeat(60));
    
    // 获取视频ID
    let videoId = null;
    if (createResult.data) {
        if (typeof createResult.data === 'object') {
            videoId = createResult.data.id || createResult.data.videoId;
        } else {
            videoId = createResult.data;
        }
    }
    console.log(`视频任务ID: ${videoId}`);
    
    // 等待视频生成
    console.log('\n⏳ 等待视频生成中... (通常需要1-3分钟)');
    
    const maxRetries = 30;
    const retryInterval = 6000; // 6秒
    
    for (let i = 0; i < maxRetries; i++) {
        console.log(`\n第 ${i+1}/${maxRetries} 次检查...`);
        
        const videoList = await client.get_video_list();
        if (videoList && videoList.data) {
            const records = videoList.data.records || videoList.data;
            if (Array.isArray(records)) {
                for (const video of records) {
                    if (video.title === title) {
                        console.log(`   状态: ${video.status}`);
                        
                        if (video.status === 'succeed' && video.videoUrl) {
                            console.log('\n🎉' + '='.repeat(50) + '🎉');
                            console.log('视频创建成功！');
                            console.log(`标题: ${title}`);
                            console.log(`使用模板: ${templateName}`);
                            console.log(`视频URL: ${video.videoUrl}`);
                            console.log('🎉' + '='.repeat(50) + '🎉');
                            return;
                        } else if (video.status === 'failed') {
                            console.log('❌ 视频创建失败！');
                            return;
                        }
                    }
                }
            }
        }
        
        if (i < maxRetries - 1) {
            console.log('   等待6秒后继续检查...');
            await new Promise(resolve => setTimeout(resolve, retryInterval));
        }
    }
    
    console.log('\n⏰ 检查超时，请稍后手动查看视频状态');
}

main().catch(console.error);
