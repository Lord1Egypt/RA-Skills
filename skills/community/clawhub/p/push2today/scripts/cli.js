#!/usr/bin/env node
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const commander_1 = require("commander");
const program = new commander_1.Command();
program
    .name('cli')
    .description('AS Today CLI - 推送消息到负一屏')
    .version('1.0.0');
program
    .command('push2today')
    .description('推送任务结果到 iOS 负一屏')
    .requiredOption('--msgId <id>', '消息 ID')
    .requiredOption('--summary <text>', '任务摘要（64字符以内）')
    .requiredOption('--result <status>', '执行结果：任务执行成功 | 任务执行失败')
    .requiredOption('--content <text>', '详细内容（限制30717字符）')
    .option('--scheduleTaskId <id>', '定时任务 ID')
    .option('--scheduleTaskName <name>', '定时任务名称')
    .option('--source <source>', '来源类型', 'openclaw')
    .option('--taskFinishTime <timestamp>', '任务完成时间戳（秒）')
    .action(async (options) => {
    const { msgId, summary, result, content, scheduleTaskId, scheduleTaskName, source, taskFinishTime } = options;
    const authCode = process.env.AS_TODAY_AUTH_CODE;
    if (!authCode) {
        console.error('错误: 未设置环境变量 AS_TODAY_AUTH_CODE');
        console.error('请先配置: openclaw config set skills.entries.push2today.env.AS_TODAY_AUTH_CODE "your_token"');
        process.exit(1);
    }
    if (result !== '任务执行成功' && result !== '任务执行失败') {
        console.error('错误: result 必须为 "任务执行成功" 或 "任务执行失败"');
        process.exit(1);
    }
    if (summary.length > 64) {
        console.error(`错误: summary 长度超过限制 (${summary.length}/64)`);
        process.exit(1);
    }
    if (content.length > 30717) {
        console.error(`错误: content 长度超过限制 (${content.length}/30717)`);
        process.exit(1);
    }
    const payload = {
        data: {
            authCode,
            msgContent: [{
                    msgId,
                    taskFinishTime: taskFinishTime ? parseInt(taskFinishTime, 10) : Math.floor(Date.now() / 1000),
                    source: source || 'openclaw',
                    summary,
                    result,
                    content,
                    ...(scheduleTaskId && { scheduleTaskId }),
                    ...(scheduleTaskName && { scheduleTaskName }),
                }],
        },
    };
    if (process.env.DEBUG === 'true') {
        console.error('[DEBUG] 请求 Payload:');
        console.error(JSON.stringify(payload, null, 2));
    }
    const apiUrl = process.env.AS_TODAY_API_URL || 'https://api.example.com/push2today';
    try {
        console.error('正在推送至负一屏...');
        const response = await fetch(apiUrl, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload),
        });
        if (!response.ok) {
            const errorText = await response.text();
            console.error(`推送失败: ${response.status} ${response.statusText} - ${errorText}`);
            process.exit(1);
        }
        const result = await response.json();
        if (result.code === 0 || result.code === 200) {
            console.log('推送成功');
        }
        else {
            console.error(`推送失败: ${result.message || '未知错误'}`);
            process.exit(1);
        }
    }
    catch (error) {
        console.error(`网络请求失败: ${error instanceof Error ? error.message : '未知错误'}`);
        process.exit(1);
    }
});
program.parse();
