#!/usr/bin/env node
/**
 * ⚡ SharkFlow - 模板系统
 * 保存和复用常用任务模板
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const TEMPLATES_DIR = path.join(__dirname, '..', 'templates');

// 确保模板目录存在
if (!fs.existsSync(TEMPLATES_DIR)) {
    fs.mkdirSync(TEMPLATES_DIR, { recursive: true });
}

// 预定义模板
const DEFAULT_TEMPLATES = {
    'dca-weekly': {
        name: '每周定投',
        description: '每周一定投 USDC 到 Aave',
        action: 'deposit',
        token: 'USDC',
        amount: 100,
        platform: 'aave',
        schedule: 'weekly',
        scheduleDay: 'monday'
    },
    'auto-compound': {
        name: '自动复投',
        description: '每周自动复投收益',
        action: 'compound',
        amount: 'all',
        schedule: 'weekly',
        scheduleDay: 'sunday'
    },
    'yield-hunt': {
        name: '收益狩猎',
        description: '监控 USDT 收益 > 10% 的平台',
        action: 'monitor',
        token: 'USDT',
        minApy: 10,
        notify: true
    },
    'multi-deposit': {
        name: '多平台存款',
        description: '分散存款到多个平台',
        actions: [
            { action: 'deposit', token: 'USDC', amount: 1000, platform: 'aave' },
            { action: 'deposit', token: 'USDC', amount: 1000, platform: 'compound' },
            { action: 'deposit', token: 'USDC', amount: 1000, platform: 'spark' }
        ]
    }
};

// 加载模板
function loadTemplates() {
    const templates = { ...DEFAULT_TEMPLATES };
    
    try {
        const files = fs.readdirSync(TEMPLATES_DIR);
        files.forEach(file => {
            if (file.endsWith('.json')) {
                const content = fs.readFileSync(path.join(TEMPLATES_DIR, file), 'utf8');
                const template = JSON.parse(content);
                templates[file.replace('.json', '')] = template;
            }
        });
    } catch (e) {
        console.error('⚠️  加载自定义模板失败:', e.message);
    }
    
    return templates;
}

// 保存模板
function saveTemplate(id, template) {
    const file = path.join(TEMPLATES_DIR, `${id}.json`);
    fs.writeFileSync(file, JSON.stringify(template, null, 2));
    console.log(`✅ 模板 "${template.name}" 已保存: ${file}`);
}

// 删除模板
function deleteTemplate(id) {
    const file = path.join(TEMPLATES_DIR, `${id}.json`);
    if (fs.existsSync(file)) {
        fs.unlinkSync(file);
        console.log(`✅ 模板 "${id}" 已删除`);
    } else {
        console.log(`❌ 模板 "${id}" 不存在`);
    }
}

// 列出模板
function listTemplates() {
    const templates = loadTemplates();
    
    console.log('\n⚡ SharkFlow - 任务模板库\n');
    console.log(`ID              名称            描述`);
    console.log(`────────────────────────────────────────────────────────────`);
    
    Object.entries(templates).forEach(([id, t]) => {
        const idStr = id.padEnd(14);
        const name = (t.name || 'Unknown').padEnd(14);
        const desc = (t.description || '').substring(0, 35);
        console.log(`${idStr} ${name} ${desc}`);
    });
    
    console.log(`\n💡 提示:`);
    console.log(`   node scripts/template.mjs --use dca-weekly  # 使用模板`);
    console.log(`   node scripts/template.mjs --show dca-weekly # 查看模板详情`);
    console.log(`   node scripts/template.mjs --create my-template # 创建新模板`);
}

// 显示模板详情
function showTemplate(id) {
    const templates = loadTemplates();
    const template = templates[id];
    
    if (!template) {
        console.log(`❌ 模板 "${id}" 不存在`);
        return;
    }
    
    console.log(`\n📋 模板详情: ${template.name}\n`);
    console.log(`ID: ${id}`);
    console.log(`描述：${template.description}`);
    console.log(`\n配置:`);
    console.log(JSON.stringify(template, null, 2));
    console.log(`\n💡 使用：node scripts/template.mjs --use ${id}`);
}

// 使用模板
function useTemplate(id) {
    const templates = loadTemplates();
    const template = templates[id];
    
    if (!template) {
        console.log(`❌ 模板 "${id}" 不存在`);
        return;
    }
    
    console.log(`\n⚡ 使用模板：${template.name}\n`);
    console.log(`准备执行:`);
    
    if (template.actions) {
        template.actions.forEach((action, i) => {
            console.log(`  ${i + 1}. ${action.action} ${action.token || ''} ${action.amount || ''} ${action.platform || ''}`);
        });
    } else {
        console.log(`  ${template.action} ${template.token || ''} ${template.amount || ''} ${template.platform || ''}`);
    }
    
    console.log(`\n🚀 执行命令:`);
    if (template.schedule) {
        console.log(`   node scripts/flow.mjs schedule --action ${template.action} --amount ${template.amount} --recur ${template.schedule}`);
    } else {
        console.log(`   node scripts/flow.mjs add --action ${template.action} --amount ${template.amount}`);
    }
    
    console.log(`\n💡 以上为模拟输出，实际执行请复制命令运行`);
}

// 创建模板向导
function createTemplate(id) {
    console.log(`\n📝 创建新模板：${id}\n`);
    
    console.log(`请按以下格式保存模板到: ${TEMPLATES_DIR}/${id}.json`);
    console.log(`
{
  "name": "你的模板名称",
  "description": "模板描述",
  "action": "deposit",
  "token": "USDC",
  "amount": 100,
  "platform": "aave",
  "schedule": "weekly",
  "scheduleDay": "monday"
}

字段说明:
- name: 模板名称（必填）
- description: 描述（必填）
- action: 操作类型 (deposit/withdraw/swap/stake/claim)
- token: 代币符号
- amount: 金额
- platform: 平台名称
- schedule: 定时 (daily/weekly/monthly)
- scheduleDay: 星期几 (monday/tuesday/...)

💡 提示：可以直接复制上面的 JSON 修改后保存
`);
}

// 主函数
const args = process.argv.slice(2);

if (args.includes('--help') || args.includes('-h')) {
    console.log(`
⚡ SharkFlow - 模板系统

用法:
  node scripts/template.mjs              # 列出所有模板
  node scripts/template.mjs --use ID     # 使用模板
  node scripts/template.mjs --show ID    # 查看模板详情
  node scripts/template.mjs --create ID  # 创建新模板向导
  node scripts/template.mjs --delete ID  # 删除模板

预定义模板:
  dca-weekly     每周定投
  auto-compound  自动复投
  yield-hunt     收益狩猎
  multi-deposit  多平台分散存款

示例:
  node scripts/template.mjs --use dca-weekly
  node scripts/template.mjs --show auto-compound
`);
    process.exit(0);
}

const useIndex = args.indexOf('--use');
const showIndex = args.indexOf('--show');
const createIndex = args.indexOf('--create');
const deleteIndex = args.indexOf('--delete');

if (useIndex > -1) {
    useTemplate(args[useIndex + 1]);
} else if (showIndex > -1) {
    showTemplate(args[showIndex + 1]);
} else if (createIndex > -1) {
    createTemplate(args[createIndex + 1]);
} else if (deleteIndex > -1) {
    deleteTemplate(args[deleteIndex + 1]);
} else {
    listTemplates();
}
