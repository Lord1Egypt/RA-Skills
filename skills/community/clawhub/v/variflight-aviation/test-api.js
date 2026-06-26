const { VariflightClient } = require('./src/lib/variflight-client');

async function test() {
    console.log('🧪 测试 Variflight API\n');

    const client = new VariflightClient();

    try {
        // 测试连接
        console.log('1️⃣  测试连接...');
        await client.connect();
        console.log('✅ 连接成功\n');

        // 测试工具列表
        console.log('2️⃣  获取工具列表...');
        const tools = await client.listTools();
        console.log(`✅ 发现 ${tools.tools?.length || 0} 个工具\n`);

        // 测试查询（使用今天的日期）
        const today = new Date().toISOString().split('T')[0];
        console.log(`3️⃣  测试查询 PEK → SHA (${today})...`);

        try {
            const result = await client.searchFlightsByDepArr('PEK', 'SHA', today);
            console.log('✅ 查询成功');
            console.log('结果预览:', JSON.stringify(result).substring(0, 200) + '...\n');
        } catch (e) {
            console.log('⚠️  查询返回错误（可能是日期无航班或 API 限制）');
            console.log('错误:', e.message, '\n');
        }

        // 测试天气查询
        console.log('4️⃣  测试天气查询 (PEK)...');
        try {
            const weather = await client.getAirportWeather('PEK');
            console.log('✅ 天气查询成功');
            console.log('结果预览:', JSON.stringify(weather).substring(0, 200) + '...\n');
        } catch (e) {
            console.log('⚠️  天气查询错误:', e.message, '\n');
        }

        console.log('✅ 所有测试完成');

    } catch (error) {
        console.error('❌ 测试失败:', error.message);
        if (error.message.includes('401')) {
            console.error('\n💡 提示：请检查 API Key 是否正确，以及邮箱是否已激活');
        }
        process.exit(1);
    } finally {
        await client.disconnect();
    }
}

test();