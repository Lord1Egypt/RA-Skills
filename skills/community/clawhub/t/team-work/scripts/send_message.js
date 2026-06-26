#!/usr/bin/env node

/**
 * Send Message Script
 *
 * This script sends messages to team members via the team service.
 * It automatically loads the team configuration from the specified file path.
 */

const fs = require('fs');
const path = require('path');

// 解析命令行参数
function parseArgs() {
    const args = process.argv.slice(2);
    const params = {};

    for (let i = 0; i < args.length; i++) {
        if (args[i].startsWith('--')) {
            const key = args[i].substring(2);
            const value = args[i + 1];
            params[key] = value;
            i++;
        }
    }

    return params;
}

// 验证必需参数
function validateParams(params) {
    if (!params['config-path']) {
        console.error('❌ 缺少必需参数: --config-path');
        process.exit(1);
    }
    if (!params['content']) {
        console.error('❌ 缺少必需参数: --content');
        process.exit(1);
    }
}

// 加载配置文件
function loadConfig(configPath) {
    if (!fs.existsSync(configPath)) {
        throw new Error(`配置文件不存在: ${configPath}\n请先运行 join_team.js 初始化团队连接。`);
    }

    const content = fs.readFileSync(configPath, 'utf-8');
    return JSON.parse(content);
}

// 发送 HTTP 请求
async function sendMessage(host, port, teamId, fromAgent, toAgent, content) {
    const http = require('http');

    const payload = JSON.stringify({
        team_id: teamId,
        from_agent: fromAgent,
        to_agent: toAgent,
        content: content
    });

    return new Promise((resolve, reject) => {
        const options = {
            hostname: host,
            port: port,
            path: '/team/send_message',
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Content-Length': Buffer.byteLength(payload)
            },
            timeout: 10000
        };

        const req = http.request(options, (res) => {
            let data = '';

            res.on('data', (chunk) => {
                data += chunk;
            });

            res.on('end', () => {
                if (res.statusCode !== 200) {
                    reject(new Error(`HTTP ${res.statusCode}: ${data}`));
                } else {
                    resolve(JSON.parse(data));
                }
            });
        });

        req.on('error', (e) => {
            reject(e);
        });

        req.on('timeout', () => {
            req.destroy();
            reject(new Error('请求超时'));
        });

        req.write(payload);
        req.end();
    });
}

// 主函数
async function main() {
    const params = parseArgs();
    validateParams(params);

    const configPath = params['config-path'];
    const recipient = params['recipient'] || '__all__';
    const content = params['content'];

    try {
        // 加载配置
        const config = loadConfig(configPath);
        const host = config.host;
        const port = config.port;
        const teamId = config.team_id;
        const agentName = config.agent_name;

        // 发送消息
        console.log(`📤 正在发送消息给 ${recipient}...`);
        const result = await sendMessage(host, port, teamId, agentName, recipient, content);

        if (result.success) {
            if (recipient === '__all__') {
                console.log('✅ 消息已广播给所有团队成员');
            } else {
                console.log(`✅ 消息已发送给 ${recipient}`);
            }
            console.log(`💬 内容: ${content}`);
        } else {
            console.error(`❌ 发送消息失败: ${result.message}`);
            process.exit(1);
        }
    } catch (error) {
        console.error(`❌ 错误: ${error.message}`);
        process.exit(1);
    }
}

// 执行主函数
main();
