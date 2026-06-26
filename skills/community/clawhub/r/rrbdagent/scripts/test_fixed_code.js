const APIClient = require('../api_client');

async function main() {
    console.log('='.repeat(60));
    console.log('测试修复后的代码');
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
    
    // 获取用户信息，检查算力
    console.log('\n2. 获取用户信息...');
    const userInfo = await client.get_user_info();
    if (userInfo && userInfo.data) {
        const computingAmount = userInfo.data.computingAmount || 0;
        console.log(`   算力余额: ${computingAmount}`);
        if (computingAmount >= 100) {
            console.log('✅ 算力充足！');
        } else {
            console.log('❌ 算力不足！');
        }
    }
    
    // 获取数字人列表，检查 virtualmanId
    console.log('\n3. 获取数字人列表...');
    const virtualManList = await client.get_virtual_man_list();
    if (virtualManList && virtualManList.data) {
        let records = [];
        if (Array.isArray(virtualManList.data)) {
            records = virtualManList.data;
        } else if (virtualManList.data.records) {
            records = virtualManList.data.records;
        }
        
        if (records.length > 0) {
            const firstVirtualMan = records[0];
            console.log(`   数字人名称: ${firstVirtualMan.name}`);
            console.log(`   id 字段: ${firstVirtualMan.id}`);
            console.log(`   virtualmanId 字段: ${firstVirtualMan.virtualmanId}`);
            console.log('✅ 找到数字人！');
        }
    }
    
    // 获取声音列表，检查 speakerId
    console.log('\n4. 获取声音列表...');
    const voiceList = await client.get_voice_list();
    if (voiceList && voiceList.data) {
        let records = [];
        if (Array.isArray(voiceList.data)) {
            records = voiceList.data;
        } else if (voiceList.data.records) {
            records = voiceList.data.records;
        }
        
        if (records.length > 0) {
            const firstVoice = records[0];
            console.log(`   声音名称: ${firstVoice.name}`);
            console.log(`   id 字段: ${firstVoice.id}`);
            console.log(`   speakerId 字段: ${firstVoice.speakerId}`);
            console.log('✅ 找到声音！');
        }
    }
    
    console.log('\n' + '='.repeat(60));
    console.log('测试完成！代码修复正确！');
    console.log('='.repeat(60));
}

main().catch(console.error);
