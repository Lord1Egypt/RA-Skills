#!/usr/bin/env node

const { createClient } = require('./create_client');

/**
 * 获取用户信息
 * 
 * 参数：
 * --email: 用户邮箱地址（必填）
 * --select: 要返回的可选字段，逗号分隔（可选）
 * 
 * 示例：
 * node scripts/get_user.js --email "zhangsan@example.com"
 * node scripts/get_user.js --email "zhangsan@example.com" --select "phone,managerInfo,customFields"
 */
async function main() {
    const args = process.argv.slice(2);
    const params = {};

    // 解析命令行参数
    for (let i = 0; i < args.length; i++) {
        if (args[i] === '--email' && args[i + 1]) {
            params.email = args[i + 1];
            i++;
        } else if (args[i] === '--select' && args[i + 1]) {
            params.select = args[i + 1].split(',').map(s => s.trim());
            i++;
        }
    }

    // 验证必填参数
    if (!params.email) {
        console.error('错误：缺少必填参数 --email');
        console.error('用法：node scripts/get_user.js --email <邮箱地址> [--select <字段列表>]');
        process.exit(1);
    }

    try {
        // 创建客户端
        const client = createClient();

        // 构造选项
        const options = {};
        if (params.select && params.select.length > 0) {
            options.select = params.select;
        }

        // 获取用户信息
        console.log(`正在获取用户信息: ${params.email}`);
        const user = await client.getUser(params.email, options);

        // 输出结果
        console.log('\n=== 用户信息 ===');
        console.log(JSON.stringify(user, null, 2));

    } catch (error) {
        console.error('获取用户信息失败:');
        
        if (error.name === 'AliMailSdkError') {
            console.error(`  错误信息: ${error.message}`);
            console.error(`  HTTP状态码: ${error.status}`);
            console.error(`  错误代码: ${error.code}`);
            console.error(`  请求ID: ${error.requestId}`);
            console.error(`  请求URL: ${error.url}`);
            if (error.details) {
                console.error(`  详细信息: ${JSON.stringify(error.details)}`);
            }
        } else {
            console.error(`  ${error.message}`);
        }
        
        process.exit(1);
    }
}

main();
