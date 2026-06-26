#!/usr/bin/env node

const { createClient } = require('./create_client');

/**
 * 获取邮件详情
 * 
 * 参数：
 * --email: 用户邮箱地址（必填）
 * --message-id: 邮件唯一标识（必填）
 * --select: 要返回的字段，逗号分隔（可选）
 * --unwrap: 是否仅返回message字段（默认true，设为false返回完整响应）
 * 
 * 示例：
 * node scripts/get_message.js --email "zhangsan@example.com" --message-id "AAMkAGI2T..."
 * node scripts/get_message.js --email "zhangsan@example.com" --message-id "AAMkAGI2T..." --select "body,toRecipients,sender"
 */
async function main() {
    const args = process.argv.slice(2);
    const params = {};

    // 解析命令行参数
    for (let i = 0; i < args.length; i++) {
        if (args[i] === '--email' && args[i + 1]) {
            params.email = args[i + 1];
            i++;
        } else if (args[i] === '--message-id' && args[i + 1]) {
            params.messageId = args[i + 1];
            i++;
        } else if (args[i] === '--select' && args[i + 1]) {
            params.select = args[i + 1].split(',').map(s => s.trim());
            i++;
        } else if (args[i] === '--unwrap' && args[i + 1]) {
            params.unwrapMessage = args[i + 1].toLowerCase() === 'true';
            i++;
        }
    }

    // 验证必填参数
    if (!params.email) {
        console.error('错误：缺少必填参数 --email');
        console.error('用法：node scripts/get_message.js --email <邮箱地址> --message-id <邮件ID> [--select <字段列表>] [--unwrap <true|false>]');
        process.exit(1);
    }

    if (!params.messageId) {
        console.error('错误：缺少必填参数 --message-id');
        console.error('用法：node scripts/get_message.js --email <邮箱地址> --message-id <邮件ID> [--select <字段列表>] [--unwrap <true|false>]');
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
        if (params.unwrapMessage !== undefined) {
            options.unwrapMessage = params.unwrapMessage;
        } else {
            options.unwrapMessage = true; // 默认值
        }

        // 获取邮件详情
        console.log(`正在获取邮件详情: ${params.messageId}`);
        const message = await client.getMessage(params.email, params.messageId, options);

        // 输出结果
        console.log('\n=== 邮件详情 ===');
        console.log(JSON.stringify(message, null, 2));

    } catch (error) {
        console.error('获取邮件详情失败:');
        
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
