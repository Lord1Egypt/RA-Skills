#!/usr/bin/env node

/**
 * manage_draft.js - 微信公众号草稿与已发布文章管理
 *
 * 用法:
 *   node manage_draft.js get <media-id>
 *   node manage_draft.js list [--offset 0] [--count 20] [--no-content]
 *   node manage_draft.js count
 *   node manage_draft.js delete <media-id>
 *   node manage_draft.js publish <media-id> [--wait] [--timeout 120] [--interval 5]
 *   node manage_draft.js status <publish-id> [--wait] [--timeout 120] [--interval 5]
 *   node manage_draft.js published-list [--offset 0] [--count 20] [--no-content]
 *   node manage_draft.js published-get <article-id>
 *   node manage_draft.js published-delete <article-id> [--index 0]
 */

const { execFileSync } = require('child_process');
const fs = require('fs');
const path = require('path');
const os = require('os');
const { ensureWenyanReady } = require('./wenyan_runner');

const TOOLS_MD_PATHS = [
    path.join(os.homedir(), '.openclaw', 'workspace-writer-test', 'TOOLS.md'),
    path.join(os.homedir(), '.openclaw', 'workspace-xina-gongzhonghao', 'TOOLS.md'),
    path.join(os.homedir(), '.openclaw', 'workspace', 'TOOLS.md'),
];

const supportsColor = process.stdout.isTTY;
const color = {
    red: (s) => supportsColor ? `\x1b[31m${s}\x1b[0m` : s,
    green: (s) => supportsColor ? `\x1b[32m${s}\x1b[0m` : s,
    yellow: (s) => supportsColor ? `\x1b[33m${s}\x1b[0m` : s,
};

function showHelp() {
    console.log(`Usage:
  node manage_draft.js get <media-id>
  node manage_draft.js list [--offset 0] [--count 20] [--no-content]
  node manage_draft.js count
  node manage_draft.js delete <media-id>
  node manage_draft.js publish <media-id> [--wait] [--timeout 120] [--interval 5]
  node manage_draft.js status <publish-id> [--wait] [--timeout 120] [--interval 5]
  node manage_draft.js published-list [--offset 0] [--count 20] [--no-content]
  node manage_draft.js published-get <article-id>
  node manage_draft.js published-delete <article-id> [--index 0]

Examples:
  node manage_draft.js get xxxxx
  node manage_draft.js list --count 5
  node manage_draft.js delete xxxxx
  node manage_draft.js publish xxxxx --wait
  node manage_draft.js status 100000001 --wait
  node manage_draft.js published-list --no-content
  node manage_draft.js published-get 1234567890
  node manage_draft.js published-delete 1234567890 --index 2`);
}

function checkWenyan() {
    return ensureWenyanReady();
}

function loadCredentials() {
    let appId = process.env.WECHAT_APP_ID || '';
    let secret = process.env.WECHAT_APP_SECRET || '';

    if (appId && secret) return { appId, secret };

    for (const toolsPath of TOOLS_MD_PATHS) {
        if (!fs.existsSync(toolsPath)) continue;
        const content = fs.readFileSync(toolsPath, 'utf-8');
        for (const line of content.split('\n')) {
            const idMatch = line.match(/export\s+WECHAT_APP_ID=(\S+)/);
            if (idMatch) appId = idMatch[1];
            const secretMatch = line.match(/export\s+WECHAT_APP_SECRET=(\S+)/);
            if (secretMatch) secret = secretMatch[1];
        }
        if (appId && secret) {
            console.log(color.yellow(`📖 凭证从 ${toolsPath} 读取`));
            return { appId, secret };
        }
    }

    return { appId, secret };
}

function checkEnv() {
    const { appId, secret } = loadCredentials();
    if (!appId || !secret) {
        console.error(color.red('❌ 环境变量未设置！'));
        console.log('  export WECHAT_APP_ID=your_app_id');
        console.log('  export WECHAT_APP_SECRET=your_app_secret');
        process.exit(1);
    }
    return { appId, secret };
}

function runWenyan(args, env) {
    const runner = ensureWenyanReady();
    console.log(color.yellow(`🔧 Wenyan: ${runner.label}`));
    execFileSync(runner.command, [...runner.prefixArgs, ...args], {
        env,
        stdio: 'inherit',
    });
}

function requireId(id, label) {
    if (!id || id.startsWith('--')) {
        console.error(color.red(`❌ 缺少必要参数: ${label}`));
        showHelp();
        process.exit(1);
    }
    return id;
}

function buildCommand(action, rest) {
    switch (action) {
        case 'get': {
            const mediaId = requireId(rest[0], 'media-id');
            return { label: `📄 获取草稿: ${mediaId}`, args: ['draft', 'get', mediaId, ...rest.slice(1)] };
        }
        case 'list':
            return { label: '📚 获取草稿列表', args: ['draft', 'list', ...rest] };
        case 'count':
            return { label: '🔢 获取草稿总数', args: ['draft', 'count', ...rest] };
        case 'delete': {
            const mediaId = requireId(rest[0], 'media-id');
            return { label: `🗑️  删除草稿: ${mediaId}`, args: ['draft', 'delete', mediaId, ...rest.slice(1)] };
        }
        case 'publish': {
            const mediaId = requireId(rest[0], 'media-id');
            return { label: `🚀 正式发布草稿: ${mediaId}`, args: ['draft', 'publish', mediaId, ...rest.slice(1)] };
        }
        case 'status': {
            const publishId = requireId(rest[0], 'publish-id');
            return { label: `📡 查询发布状态: ${publishId}`, args: ['publish-status', publishId, ...rest.slice(1)] };
        }
        case 'published-list':
            return { label: '📰 获取已发布文章列表', args: ['published', 'list', ...rest] };
        case 'published-get': {
            const articleId = requireId(rest[0], 'article-id');
            return { label: `🔍 获取已发布文章: ${articleId}`, args: ['published', 'get', articleId, ...rest.slice(1)] };
        }
        case 'published-delete': {
            const articleId = requireId(rest[0], 'article-id');
            return { label: `🧹 删除已发布文章: ${articleId}`, args: ['published', 'delete', articleId, ...rest.slice(1)] };
        }
        default:
            return null;
    }
}

function main() {
    const args = process.argv.slice(2);
    if (args.length === 0 || args[0] === '-h' || args[0] === '--help') {
        showHelp();
        process.exit(0);
    }

    const [action, ...rest] = args;
    const task = buildCommand(action, rest);
    if (!task) {
        showHelp();
        process.exit(1);
    }

    checkWenyan();
    const { appId, secret } = checkEnv();
    const env = { ...process.env, WECHAT_APP_ID: appId, WECHAT_APP_SECRET: secret };

    try {
        console.log(color.green(task.label));
        runWenyan(task.args, env);
    } catch {
        console.error(color.red('❌ 操作失败！'));
        process.exit(1);
    }
}

main();
