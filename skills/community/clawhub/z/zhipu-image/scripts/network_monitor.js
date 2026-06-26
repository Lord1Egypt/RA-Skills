#!/usr/bin/env node
/**
 * 网络请求抓包工具
 * 用于分析智谱AI的API请求
 */

const CDP = require('chrome-remote-interface');

async function monitorNetwork() {
    console.log('Connecting to browser via CDP...');
    
    const client = await CDP({ port: 18800 });
    const { Network, Page } = client;
    
    await Network.enable();
    await Page.enable();
    
    console.log('Monitoring network requests...');
    console.log('Press Ctrl+C to stop');
    console.log();
    
    let requestCount = 0;
    
    // 监听请求
    Network.requestWillBeSent(params => {
        const url = params.request.url;
        
        // 只显示API相关请求
        if (url.includes('api') || url.includes('z.ai') || url.includes('generation')) {
            requestCount++;
            console.log(`\n[${requestCount}] ${params.request.method} ${url}`);
            
            // 显示请求体
            if (params.request.postData) {
                try {
                    const postData = JSON.parse(params.request.postData);
                    console.log('  POST data:', JSON.stringify(postData).substring(0, 200));
                } catch (e) {
                    console.log('  POST data:', params.request.postData.substring(0, 200));
                }
            }
        }
    });
    
    // 监听响应
    Network.responseReceived(params => {
        const url = params.response.url;
        
        if (url.includes('api') || url.includes('generation')) {
            console.log(`  <- Status: ${params.response.status} ${params.response.statusText}`);
        }
    });
    
    // 保持运行
    process.on('SIGINT', async () => {
        console.log('\n\nStopping...');
        await client.close();
        process.exit(0);
    });
}

monitorNetwork().catch(err => {
    console.error('Error:', err.message);
    process.exit(1);
});