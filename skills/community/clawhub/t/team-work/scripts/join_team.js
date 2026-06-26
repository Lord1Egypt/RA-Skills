#!/usr/bin/env node

/**
 * Team Join Script
 *
 * This script initializes an agent's connection to a team by:
 * 1. Sending a join request to the team service
 * 2. Saving the team configuration to a specified file path
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
    const required = ['host', 'port', 'team-id', 'agent-name', 'config-path'];
    for (const param of required) {
        if (!params[param]) {
            console.error(`❌ 缺少必需参数: --${param}`);
            process.exit(1);
        }
    }
}

// 保存配置文件
function saveConfig(configPath, config) {
    const dir = path.dirname(configPath);
    if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
    }

    fs.writeFileSync(configPath, JSON.stringify(config, null, 2));
    console.log(`✅ 团队配置已保存到: ${configPath}`);
}

// 加载配置文件
function loadConfig(configPath) {
    if (!fs.existsSync(configPath)) {
        return null;
    }

    const content = fs.readFileSync(configPath, 'utf-8');
    return JSON.parse(content);
}

// 发送 HTTP 请求
async function joinTeam(host, port, teamId, agentName) {
    const http = require('http');

    const payload = JSON.stringify({
        team_id: teamId,
        agent_name: agentName
    });

    return new Promise((resolve, reject) => {
        const options = {
            hostname: host,
            port: port,
            path: '/team/join_team',
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
            reject(new Error('Request timeout'));
        });

        req.write(payload);
        req.end();
    });
}

// 主函数
async function main() {
    const params = parseArgs();
    validateParams(params);

    const host = params['host'];
    const port = parseInt(params['port']);
    const teamId = params['team-id'];
    const agentName = params['agent-name'];
    const configPath = params['config-path'];

    try {
        const result = await joinTeam(host, port, teamId, agentName);

        if (result.success) {
            // 保存配置
            const config = {
                host: host,
                port: port,
                team_id: teamId,
                agent_name: agentName
            };

            saveConfig(configPath, config);
            console.log(`✅ 成功加入团队: '${teamId}'`);

            console.log('⏳ 等待其他成员加入...');
        } else {
            console.error(`❌ 加入团队失败: ${result.message}`);
            process.exit(1);
        }
    } catch (error) {
        console.error(`❌ 错误: ${error.message}`);
        process.exit(1);
    }
}

// 执行主函数
main();
