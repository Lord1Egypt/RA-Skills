const { handlePurchase } = require('./index');

async function test() {
    console.log('测试采购记录技能...\n');

    const tests = [
        '采购 0312 螺丝 5 元',
        '采购 0317 角磨机切割片 50 元',
        '采购 0318 轴套压制机气动配件 780 元'
    ];

    for (const test of tests) {
        console.log(`输入：${test}`);
        try {
            const result = await handlePurchase(test);
            console.log(`输出：${result}\n`);
        } catch (error) {
            console.log(`错误：${error.message}\n`);
        }
    }

    console.log('测试完成！');
}

test().catch(console.error);