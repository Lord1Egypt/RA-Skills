#!/usr/bin/env node

const { createClient } = require('./create_client');

/**
 * 搜索邮件
 * 
 * 参数：
 * --email: 用户邮箱地址（必填）
 * --query: KQL查询语句（必填）
 * --cursor: 分页游标，首次传空字符串（可选，默认空字符串）
 * --size: 每页数量，取值1-100（可选，默认20）
 * --select: 要返回的字段，逗号分隔（可选）
 * 
 * 示例：
 * node scripts/search_messages.js --email "zhangsan@example.com" --query 'fromEmail="alice@example.com"'
 * node scripts/search_messages.js --email "zhangsan@example.com" --query 'date>2025-01-01' --size 50
 */
async function main() {
    const args = process.argv.slice(2);
    const params = {};

    // 解析命令行参数
    for (let i = 0; i < args.length; i++) {
        if (args[i] === '--email' && args[i + 1]) {
            params.email = args[i + 1];
            i++;
        } else if (args[i] === '--query' && args[i + 1]) {
            params.query = args[i + 1];
            i++;
        } else if (args[i] === '--cursor' && args[i + 1]) {
            params.cursor = args[i + 1];
            i++;
        } else if (args[i] === '--size' && args[i + 1]) {
            params.size = parseInt(args[i + 1], 10);
            i++;
        } else if (args[i] === '--select' && args[i + 1]) {
            params.select = args[i + 1].split(',').map(s => s.trim());
            i++;
        }
    }

    // 验证必填参数
    if (!params.email) {
        console.error('错误：缺少必填参数 --email');
        console.error('用法：node scripts/search_messages.js --email <邮箱地址> --query <KQL查询语句> [--cursor <游标>] [--size <数量>] [--select <字段列表>]');
        process.exit(1);
    }

    if (!params.query) {
        console.error('错误：缺少必填参数 --query');
        console.error('用法：node scripts/search_messages.js --email <邮箱地址> --query <KQL查询语句> [--cursor <游标>] [--size <数量>] [--select <字段列表>]');
        process.exit(1);
    }

    // 设置默认值
    if (!params.cursor) {
        params.cursor = '';
    }
    if (!params.size) {
        params.size = 20;
    }
    if (params.size < 1 || params.size > 100) {
        console.error('错误：size参数必须在1-100之间');
        process.exit(1);
    }

    try {
        // 创建客户端
        const client = createClient();

        // 构造选项
        const options = {
            query: params.query,
            cursor: params.cursor,
            size: params.size,
        };
        if (params.select && params.select.length > 0) {
            options.select = params.select;
        }

        // 搜索邮件
        console.log(`正在搜索邮件: ${params.query}`);
        console.log(`查询参数: size=${params.size}, cursor="${params.cursor}"`);
        const result = await client.searchMessages(params.email, options);

        // 输出结果
        console.log('\n=== 搜索结果 ===');
        console.log(`找到邮件数量: ${result.messages.length}`);
        console.log(`下一页游标: ${result.nextCursor}`);
        
        if (result.messages.length > 0) {
            console.log('\n邮件列表:');
            result.messages.forEach((msg, index) => {
                console.log(`\n[${index + 1}] 邮件ID: ${msg.id}`);
                console.log(`    主题: ${msg.subject || '(无主题)'}`);
                console.log(`    发件人: ${msg.sender?.emailAddress?.name || msg.sender?.emailAddress?.address || '未知'}`);
                console.log(`    接收时间: ${msg.receivedDateTime || '未知'}`);
                if (msg.internetMessageId) {
                    console.log(`    互联网消息ID: ${msg.internetMessageId}`);
                }
            });
        }

        console.log('\n=== 完整数据 ===');
        console.log(JSON.stringify(result, null, 2));

    } catch (error) {
        console.error('搜索邮件失败:');
        
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
