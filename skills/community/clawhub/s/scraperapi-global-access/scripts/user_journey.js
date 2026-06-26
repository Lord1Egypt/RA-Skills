const axios = require('axios');

const SCRAPER_API_KEY = 'fd18228b13dd001b794a8c74e9a35667';
const BASE_URL = 'https://faceswap.cool';

// 7个国家访问不同页面
const tasks = [
    { country: '美国', code: 'us', page: '/', name: '首页' },
    { country: '英国', code: 'uk', page: '/pricing', name: '价格页' },
    { country: '德国', code: 'de', page: '/tools/face-swap', name: '换脸工具页' },
    { country: '日本', code: 'jp', page: '/', name: '首页' },
    { country: '新加坡', code: 'sg', page: '/pricing', name: '价格页' },
    { country: '加拿大', code: 'ca', page: '/tools/face-swap', name: '换脸工具页' },
    { country: '澳大利亚', code: 'au', page: '/', name: '首页' },
];

async function visitPageWithGA(task) {
    const fullUrl = BASE_URL + task.page;
    console.log(`\n🌍 ${task.country} - 访问 ${task.name}`);
    console.log(`   URL: ${fullUrl}`);
    
    try {
        const response = await axios.get('http://api.scraperapi.com', {
            params: {
                api_key: SCRAPER_API_KEY,
                url: fullUrl,
                country_code: task.code,
                render: true,              // ✅ 开启 JS 渲染
                wait_for_selector: 'body', // 等待页面加载
                session_number: Math.floor(Math.random() * 10000) // 模拟不同会话
            },
            timeout: 60000 // 渲染需要更长时间
        });
        
        const title = response.data.match(/<title>(.*?)<\/title>/)?.[1] || '未找到标题';
        
        console.log(`✅ 成功访问（已执行 JS，GA 应该能看到）`);
        console.log(`   状态码: ${response.status}`);
        console.log(`   响应大小: ${(response.data.length / 1024).toFixed(2)} KB`);
        console.log(`   页面标题: ${title.substring(0, 60)}...`);
        
        return {
            success: true,
            country: task.country,
            page: task.name,
            url: fullUrl,
            status: response.status,
            size: response.data.length
        };
        
    } catch (error) {
        const status = error.response?.status || 'N/A';
        console.log(`❌ 失败 (${status}): ${error.message}`);
        return {
            success: false,
            country: task.country,
            page: task.name,
            url: fullUrl,
            error: error.message
        };
    }
}

async function main() {
    console.log('🚀 7个国家访问 faceswap.cool（开启 JS 渲染，触发 GA）\n');
    console.log('目标网站:', BASE_URL);
    console.log('代理服务: ScraperAPI');
    console.log('JS 渲染: ✅ 开启（会触发 Google Analytics）');
    console.log('='.repeat(70));
    
    const results = [];
    
    for (const task of tasks) {
        const result = await visitPageWithGA(task);
        results.push(result);
        await new Promise(resolve => setTimeout(resolve, 3000)); // 渲染需要更长间隔
    }
    
    console.log('\n' + '='.repeat(70));
    console.log('\n📊 最终结果:\n');
    
    const successful = results.filter(r => r.success);
    const failed = results.filter(r => !r.success);
    
    console.log(`✅ 成功: ${successful.length}/7`);
    console.log(`❌ 失败: ${failed.length}/7\n`);
    
    if (successful.length > 0) {
        console.log('成功访问的页面（应该会出现在 GA 后台）:');
        successful.forEach((r, i) => {
            console.log(`${i + 1}. ${r.country.padEnd(6)} | ${r.page.padEnd(12)} | ${(r.size / 1024).toFixed(2)} KB`);
        });
    }
    
    console.log('\n💡 提示：');
    console.log('- 访问记录可能需要 24-48 小时才会出现在 GA 后台');
    console.log('- 如果 GA 开启了 Bot Filtering，可能仍然会被过滤');
    console.log('- 建议在 GA 后台查看"实时"报告，看是否有新访问');
    
    console.log('\n✨ 任务完成！');
}

main();
