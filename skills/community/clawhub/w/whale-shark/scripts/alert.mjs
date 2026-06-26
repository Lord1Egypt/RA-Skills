#!/usr/bin/env node
/**
 * 🐋 WhaleWatch - 转账提醒
 * 设置和管理巨鲸转账提醒
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const DATA_DIR = path.join(__dirname, '..', 'data');
const ALERTS_FILE = path.join(DATA_DIR, 'whale-alerts.json');

// 确保数据目录存在
if (!fs.existsSync(DATA_DIR)) {
    fs.mkdirSync(DATA_DIR, { recursive: true });
}

// 加载提醒
function loadAlerts() {
    try {
        if (fs.existsSync(ALERTS_FILE)) {
            return JSON.parse(fs.readFileSync(ALERTS_FILE, 'utf8'));
        }
    } catch (e) {
        console.error('⚠️  加载提醒失败:', e.message);
    }
    return { alerts: [] };
}

// 保存提醒
function saveAlerts(data) {
    fs.writeFileSync(ALERTS_FILE, JSON.stringify(data, null, 2));
}

// 添加提醒
function addAlert(whale, minAmount) {
    const data = loadAlerts();
    
    const alert = {
        id: Date.now(),
        whale,
        minAmount,
        createdAt: new Date().toISOString(),
        triggered: false
    };
    
    data.alerts.push(alert);
    saveAlerts(data);
    
    console.log(`\n✅ 提醒已设置\n`);
    console.log(`巨鲸：${whale}`);
    console.log(`监控条件：转账金额 > $${(minAmount / 1000).toFixed(0)}K`);
    console.log(`\n💡 查看提醒：node scripts/alert.mjs --list`);
    console.log(`\n🐋 WhaleWatch v0.1.0 - Follow The Whales`);
}

// 查看所有提醒
function listAlerts() {
    const data = loadAlerts();
    
    if (data.alerts.length === 0) {
        console.log('ℹ️  暂无提醒');
        console.log('\n💡 添加提醒：node scripts/alert.mjs add --whale 0x8f3B --min 50000');
        return;
    }
    
    console.log('\n🐋 WhaleWatch - 转账提醒\n');
    console.log(`ID     巨鲸              最小金额     状态`);
    console.log(`─────────────────────────────────────────────────────────`);
    
    data.alerts.forEach(a => {
        const id = a.id.toString().padEnd(6);
        const whale = a.whale.padEnd(16);
        const amount = `$${(a.minAmount / 1000).toFixed(0)}K`.padEnd(10);
        const status = a.triggered ? '✅ 已触发' : '⏳ 监控中';
        
        console.log(`${id} ${whale} ${amount} ${status}`);
    });
    
    console.log(`\n💡 删除提醒：node scripts/alert.mjs remove <ID>`);
}

// 删除提醒
function removeAlert(id) {
    const data = loadAlerts();
    const initialLength = data.alerts.length;
    
    data.alerts = data.alerts.filter(a => a.id.toString() !== id);
    
    if (data.alerts.length === initialLength) {
        console.log(`❌ 未找到提醒 ID: ${id}`);
        return;
    }
    
    saveAlerts(data);
    console.log(`✅ 提醒已删除`);
    console.log(`\n🐋 WhaleWatch v0.1.0 - Follow The Whales`);
}

// 主函数
const args = process.argv.slice(2);

if (args.includes('--help') || args.includes('-h')) {
    console.log(`
🐋 WhaleWatch - 转账提醒

用法:
  node scripts/alert.mjs add --whale <addr> --min <amount>  # 添加提醒
  node scripts/alert.mjs --list         # 查看所有提醒
  node scripts/alert.mjs remove <ID>    # 删除提醒

示例:
  node scripts/alert.mjs add --whale 0x8f3B...2Ae1 --min 50000
  node scripts/alert.mjs --list
  node scripts/alert.mjs remove 1234567890

选项:
  --help, -h        显示帮助
  --list            查看提醒列表
  --whale <addr>    巨鲸地址
  --min <amount>    最小金额 (美元)
`);
    process.exit(0);
}

const action = args[0];

if (action === 'add') {
    const whaleIndex = args.indexOf('--whale');
    const minIndex = args.indexOf('--min');
    
    const whale = whaleIndex > -1 ? args[whaleIndex + 1] : null;
    const minAmount = minIndex > -1 ? parseInt(args[minIndex + 1]) : null;
    
    if (!whale || !minAmount) {
        console.log('❌ 请提供巨鲸地址和最小金额');
        console.log('用法：node scripts/alert.mjs add --whale 0x8f3B --min 50000');
        process.exit(1);
    }
    
    addAlert(whale, minAmount);
} else if (action === '--list' || args.includes('--list')) {
    listAlerts();
} else if (action === 'remove') {
    const id = args[1];
    if (!id) {
        console.log('❌ 请提供提醒 ID');
        process.exit(1);
    }
    removeAlert(id);
} else {
    console.log('❌ 未知操作');
    console.log('用法：node scripts/alert.mjs --help');
    process.exit(1);
}
