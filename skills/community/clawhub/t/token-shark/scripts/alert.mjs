#!/usr/bin/env node
/**
 * 🎯 TokenSniper - 价格提醒
 * 设置和管理价格提醒
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const DATA_DIR = path.join(__dirname, '..', 'data');
const ALERTS_FILE = path.join(DATA_DIR, 'alerts.json');

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
function addAlert(address, targetPrice, condition = 'above') {
    const data = loadAlerts();
    
    const alert = {
        id: Date.now(),
        address,
        targetPrice,
        condition, // 'above' or 'below'
        createdAt: new Date().toISOString(),
        triggered: false
    };
    
    data.alerts.push(alert);
    saveAlerts(data);
    
    const conditionText = condition === 'above' ? '上涨至' : '下跌至';
    console.log(`\n✅ 提醒已设置\n`);
    console.log(`代币：${address}`);
    console.log(`提醒条件：价格${conditionText} $${targetPrice}`);
    console.log(`\n💡 查看提醒：node scripts/alert.mjs --list`);
    console.log(`\n🎯 TokenSniper v0.1.0 - Snipe Before Moon`);
}

// 查看所有提醒
function listAlerts() {
    const data = loadAlerts();
    
    if (data.alerts.length === 0) {
        console.log('ℹ️  暂无提醒');
        console.log('\n💡 添加提醒：node scripts/alert.mjs add --token 0x1234 --price 0.01');
        return;
    }
    
    console.log('\n🎯 TokenSniper - 价格提醒\n');
    console.log(`ID     代币              条件        目标价格    状态`);
    console.log(`─────────────────────────────────────────────────────────`);
    
    data.alerts.forEach(a => {
        const id = a.id.toString().padEnd(6);
        const addr = a.address.slice(0, 10) + '...';
        const condition = a.condition === 'above' ? '🟢 上涨至' : '🔴 下跌至';
        const price = `$${a.targetPrice}`.padEnd(10);
        const status = a.triggered ? '✅ 已触发' : '⏳ 监控中';
        
        console.log(`${id} ${addr.padEnd(16)} ${condition.padEnd(12)} ${price} ${status}`);
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
    console.log(`\n🎯 TokenSniper v0.1.0 - Snipe Before Moon`);
}

// 主函数
const args = process.argv.slice(2);

if (args.includes('--help') || args.includes('-h')) {
    console.log(`
🎯 TokenSniper - 价格提醒

用法:
  node scripts/alert.mjs add --token <addr> --price <price>  # 添加提醒
  node scripts/alert.mjs --list         # 查看所有提醒
  node scripts/alert.mjs remove <ID>    # 删除提醒

示例:
  node scripts/alert.mjs add --token 0x1234...5678 --price 0.01
  node scripts/alert.mjs add --token 0x1234 --price 0.005 --condition below
  node scripts.alert.mjs --list
  node scripts/alert.mjs remove 1234567890

选项:
  --help, -h        显示帮助
  --list            查看提醒列表
  --token <addr>    代币地址
  --price <price>   目标价格
  --condition <c>   条件 (above/below, 默认 above)
`);
    process.exit(0);
}

const action = args[0];

if (action === 'add') {
    const tokenIndex = args.indexOf('--token');
    const priceIndex = args.indexOf('--price');
    const conditionIndex = args.indexOf('--condition');
    
    const token = tokenIndex > -1 ? args[tokenIndex + 1] : null;
    const price = priceIndex > -1 ? parseFloat(args[priceIndex + 1]) : null;
    const condition = conditionIndex > -1 ? args[conditionIndex + 1] : 'above';
    
    if (!token || !price) {
        console.log('❌ 请提供代币地址和目标价格');
        console.log('用法：node scripts/alert.mjs add --token 0x1234 --price 0.01');
        process.exit(1);
    }
    
    if (condition !== 'above' && condition !== 'below') {
        console.log('❌ condition 必须是 above 或 below');
        process.exit(1);
    }
    
    addAlert(token, price, condition);
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
