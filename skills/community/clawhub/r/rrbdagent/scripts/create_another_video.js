const RRBDAgent = require('../index');

async function main() {
    console.log('='.repeat(60));
    console.log('创建另一个视频');
    console.log('='.repeat(60));
    
    const agent = new RRBDAgent();
    
    // 登录
    console.log('\n1. 登录中...');
    const username = '18098901246';
    const password = '123456';
    
    const loginSuccess = await agent.login(username, password);
    if (!loginSuccess) {
        console.log('❌ 登录失败！');
        return;
    }
    console.log('✅ 登录成功！');
    
    // 创建视频
    const title = '一物一码让信任更简单_第二版';
    const script = '一物一码让信任更简单！未来随着技术的不断发展，"一物一码" 将会在更多领域发挥更大的作用，为消费者创造更安全、更便捷、更美好的生活体验。赶快行动起来，体验 "一物一码" 带来的便捷与安心！';
    
    console.log('\n2. 创建视频...');
    console.log(`   标题: ${title}`);
    console.log(`   文案: ${script}`);
    
    const result = await agent.createVideo(title, script);
    
    if (result.success) {
        console.log('\n🎉' + '='.repeat(50) + '🎉');
        console.log('视频创建成功！');
        console.log(`视频URL: ${result.videoUrl}`);
        console.log('🎉' + '='.repeat(50) + '🎉');
    } else {
        console.log('\n❌ 视频创建失败！');
        console.log(`失败原因: ${result.message}`);
    }
}

main().catch(console.error);
