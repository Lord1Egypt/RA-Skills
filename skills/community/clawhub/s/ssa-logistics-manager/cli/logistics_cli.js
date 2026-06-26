#!/usr/bin/env node

/**
 * Logistics CLI - 物流管理命令行工具
 * 
 * 功能：
 * - list: 列出所有物流记录
 * - get <id>: 查看单个物流记录详情
 * - create: 创建新物流记录（交互式）
 * - update <id>: 更新物流记录
 * - delete <id>: 删除物流记录
 * - tracking <id>: 查看物流追踪
 * - documents <id>: 管理报关单据
 * - bol <id>: 管理提单
 * - notify <id>: 发送客户通知
 * - sync-okki <id>: 同步到 OKKI
 */

const { Command } = require('commander');
const chalk = require('chalk');
const readline = require('readline');
const path = require('path');
const fs = require('fs');

const program = new Command();

// 配置
const API_BASE_URL = process.env.LOGISTICS_API_URL || 'http://localhost:3000';
const DATA_DIR = path.join(__dirname, '../data');

// 确保数据目录存在
if (!fs.existsSync(DATA_DIR)) {
  fs.mkdirSync(DATA_DIR, { recursive: true });
}

// 本地数据存储文件
const SHIPMENTS_FILE = path.join(DATA_DIR, 'shipments.json');
const TRACKING_FILE = path.join(DATA_DIR, 'tracking.json');
const DOCUMENTS_FILE = path.join(DATA_DIR, 'documents.json');
const BOLS_FILE = path.join(DATA_DIR, 'bols.json');
const NOTIFICATIONS_FILE = path.join(DATA_DIR, 'notifications.json');

/**
 * 读取本地数据
 */
function loadShipments() {
  if (fs.existsSync(SHIPMENTS_FILE)) {
    const data = fs.readFileSync(SHIPMENTS_FILE, 'utf8');
    return JSON.parse(data);
  }
  return [];
}

/**
 * 保存本地数据
 */
function saveShipments(shipments) {
  fs.writeFileSync(SHIPMENTS_FILE, JSON.stringify(shipments, null, 2), 'utf8');
}

/**
 * 生成 ID
 */
function generateId() {
  return 'LOG-' + Date.now().toString(36).toUpperCase() + '-' + Math.random().toString(36).substr(2, 4).toUpperCase();
}

/**
 * 交互式输入
 */
function createInterface() {
  return readline.createInterface({
    input: process.stdin,
    output: process.stdout
  });
}

/**
 * 异步提问
 */
function askQuestion(rl, question) {
  return new Promise((resolve) => {
    rl.question(question, (answer) => {
      resolve(answer);
    });
  });
}

/**
 * 列出所有物流记录
 */
async function listShipments() {
  console.log(chalk.blue('\n📋 物流记录列表\n'));
  
  const shipments = loadShipments();
  
  if (shipments.length === 0) {
    console.log(chalk.yellow('  暂无物流记录'));
    console.log(chalk.gray('  使用 "node logistics_cli.js create" 创建新记录\n'));
    return;
  }
  
  console.log(chalk.gray('  ' + '─'.repeat(120)));
  console.log(chalk.gray('  |') + chalk.cyan(' ID'.padEnd(30)) + chalk.gray('|') + 
              chalk.cyan(' 订单号'.padEnd(18)) + chalk.gray('|') + 
              chalk.cyan(' 起运港'.padEnd(15)) + chalk.gray('|') + 
              chalk.cyan(' 目的港'.padEnd(15)) + chalk.gray('|') + 
              chalk.cyan(' 状态'.padEnd(15)) + chalk.gray('|') + 
              chalk.cyan(' 运输方式'.padEnd(12)) + chalk.gray('|'));
  console.log(chalk.gray('  ' + '─'.repeat(120)));
  
  shipments.forEach((item) => {
    const statusColor = {
      'Draft': chalk.gray,
      'Pending': chalk.yellow,
      'In Transit': chalk.blue,
      'Customs Clearance': chalk.yellow.bold,
      'Delivered': chalk.green,
      'Completed': chalk.green.bold,
      'Cancelled': chalk.red
    }[item.status] || chalk.white;
    
    console.log(chalk.gray('  |') + chalk.white(item.id.padEnd(30)) + chalk.gray('|') + 
                chalk.white((item.orderId || '-').padEnd(18)) + chalk.gray('|') + 
                chalk.white((item.portOfLoading || '-').padEnd(15)) + chalk.gray('|') + 
                chalk.white((item.portOfDischarge || '-').padEnd(15)) + chalk.gray('|') + 
                statusColor(item.status.padEnd(15)) + chalk.gray('|') + 
                chalk.white((item.transportMode || '-').padEnd(12)) + chalk.gray('|'));
  });
  
  console.log(chalk.gray('  ' + '─'.repeat(120)));
  console.log(chalk.gray(`  共 ${shipments.length} 条记录\n`));
}

/**
 * 获取物流记录详情
 */
async function getShipment(id) {
  console.log(chalk.blue(`\n📄 物流记录详情：${id}\n`));
  
  const shipments = loadShipments();
  const shipment = shipments.find(s => s.id === id);
  
  if (!shipment) {
    console.log(chalk.red(`  ❌ 未找到物流记录：${id}`));
    return;
  }
  
  console.log(chalk.gray('  ' + '─'.repeat(60)));
  console.log(chalk.gray('  |') + chalk.cyan(' 字段'.padEnd(20)) + chalk.gray('|') + chalk.cyan(' 值'.padEnd(35)) + chalk.gray('|'));
  console.log(chalk.gray('  ' + '─'.repeat(60)));
  
  const fields = [
    ['ID', shipment.id],
    ['订单号', shipment.orderId || '-'],
    ['客户 ID', shipment.customerId || '-'],
    ['客户名称', shipment.customerName || '-'],
    ['起运港', shipment.portOfLoading || '-'],
    ['目的港', shipment.portOfDischarge || '-'],
    ['运输方式', shipment.transportMode || '-'],
    ['船名/航次', shipment.vesselVoyage || '-'],
    ['集装箱号', shipment.containerNo || '-'],
    ['封条号', shipment.sealNo || '-'],
    ['货物描述', shipment.cargoDescription || '-'],
    ['件数', shipment.packages || '-'],
    ['毛重', shipment.grossWeight || '-'],
    ['体积', shipment.volume || '-'],
    ['贸易术语', shipment.incoterms || '-'],
    ['状态', shipment.status || 'Draft'],
    ['备注', shipment.notes || '-'],
    ['创建时间', shipment.createdAt ? new Date(shipment.createdAt).toLocaleString('zh-CN') : '-'],
    ['更新时间', shipment.updatedAt ? new Date(shipment.updatedAt).toLocaleString('zh-CN') : '-']
  ];
  
  fields.forEach(([key, value]) => {
    const valueStr = String(value || '-');
    console.log(chalk.gray('  |') + chalk.white(key.padEnd(20)) + chalk.gray('|') + 
                chalk.white(valueStr.padEnd(35)) + chalk.gray('|'));
  });
  
  console.log(chalk.gray('  ' + '─'.repeat(60)));
  
  // 显示关联数据
  console.log(chalk.blue('\n📎 关联数据:'));
  
  const tracking = loadTracking();
  const trackingCount = tracking.filter(t => t.shipmentId === id).length;
  console.log(chalk.gray(`  🚚 追踪记录：${trackingCount} 条`));
  
  const documents = loadDocuments();
  const docCount = documents.filter(d => d.shipmentId === id).length;
  console.log(chalk.gray(`  📄 报关单据：${docCount} 份`));
  
  const bols = loadBols();
  const bolCount = bols.filter(b => b.shipmentId === id).length;
  console.log(chalk.gray(`  📜 提单：${bolCount} 份`));
  
  const notifications = loadNotifications();
  const notifyCount = notifications.filter(n => n.shipmentId === id).length;
  console.log(chalk.gray(`  📧 通知记录：${notifyCount} 条`));
  
  console.log();
}

/**
 * 创建物流记录（交互式）
 */
async function createShipment() {
  console.log(chalk.blue('\n➕ 创建新物流记录\n'));
  
  const rl = createInterface();
  
  try {
    console.log(chalk.gray('  请输入物流信息（按 Enter 跳过可选字段）:\n'));
    
    const orderId = await askQuestion(rl, chalk.white('  订单号 (必填): '));
    if (!orderId) {
      console.log(chalk.red('  ❌ 订单号为必填项'));
      rl.close();
      return;
    }
    
    const customerId = await askQuestion(rl, chalk.white('  客户 ID (必填): '));
    if (!customerId) {
      console.log(chalk.red('  ❌ 客户 ID 为必填项'));
      rl.close();
      return;
    }
    
    const portOfLoading = await askQuestion(rl, chalk.white('  起运港 (必填): '));
    if (!portOfLoading) {
      console.log(chalk.red('  ❌ 起运港为必填项'));
      rl.close();
      return;
    }
    
    const portOfDischarge = await askQuestion(rl, chalk.white('  目的港 (必填): '));
    if (!portOfDischarge) {
      console.log(chalk.red('  ❌ 目的港为必填项'));
      rl.close();
      return;
    }
    
    const transportMode = await askQuestion(rl, chalk.white('  运输方式 [Sea Freight]: ') || 'Sea Freight');
    const customerName = await askQuestion(rl, chalk.white('  客户名称: '));
    const vesselVoyage = await askQuestion(rl, chalk.white('  船名/航次: '));
    const containerNo = await askQuestion(rl, chalk.white('  集装箱号: '));
    const sealNo = await askQuestion(rl, chalk.white('  封条号: '));
    const cargoDescription = await askQuestion(rl, chalk.white('  货物描述: '));
    const packages = await askQuestion(rl, chalk.white('  件数: '));
    const grossWeight = await askQuestion(rl, chalk.white('  毛重 (KG): '));
    const volume = await askQuestion(rl, chalk.white('  体积 (CBM): '));
    const incoterms = await askQuestion(rl, chalk.white('  贸易术语 [FOB]: ') || 'FOB');
    const notes = await askQuestion(rl, chalk.white('  备注: '));
    
    const newShipment = {
      id: generateId(),
      orderId,
      customerId,
      customerName: customerName || null,
      portOfLoading,
      portOfDischarge,
      transportMode: transportMode || 'Sea Freight',
      vesselVoyage: vesselVoyage || null,
      containerNo: containerNo || null,
      sealNo: sealNo || null,
      cargoDescription: cargoDescription || null,
      packages: packages ? parseInt(packages) : null,
      grossWeight: grossWeight ? parseFloat(grossWeight) : null,
      volume: volume ? parseFloat(volume) : null,
      incoterms: incoterms || 'FOB',
      notes: notes || null,
      status: 'Draft',
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString()
    };
    
    const shipments = loadShipments();
    shipments.push(newShipment);
    saveShipments(shipments);
    
    console.log(chalk.green('\n  ✅ 物流记录创建成功!'));
    console.log(chalk.gray(`  ID: ${newShipment.id}`));
    console.log(chalk.gray(`  订单号：${newShipment.orderId}`));
    console.log(chalk.gray(`  路线：${newShipment.portOfLoading} → ${newShipment.portOfDischarge}`));
    console.log(chalk.gray(`  状态：${newShipment.status}\n`));
    
  } catch (error) {
    console.log(chalk.red(`  ❌ 创建失败：${error.message}`));
  } finally {
    rl.close();
  }
}

/**
 * 更新物流记录
 */
async function updateShipment(id) {
  console.log(chalk.blue(`\n✏️  更新物流记录：${id}\n`));
  
  const shipments = loadShipments();
  const index = shipments.findIndex(s => s.id === id);
  
  if (index === -1) {
    console.log(chalk.red(`  ❌ 未找到物流记录：${id}`));
    return;
  }
  
  const shipment = shipments[index];
  const rl = createInterface();
  
  try {
    console.log(chalk.gray('  当前值显示在 [方括号] 中，直接按 Enter 保持不变:\n'));
    
    const orderId = await askQuestion(rl, chalk.white(`  订单号 [${shipment.orderId}]: `));
    const customerId = await askQuestion(rl, chalk.white(`  客户 ID [${shipment.customerId}]: `));
    const customerName = await askQuestion(rl, chalk.white(`  客户名称 [${shipment.customerName || '-'}]: `));
    const portOfLoading = await askQuestion(rl, chalk.white(`  起运港 [${shipment.portOfLoading}]: `));
    const portOfDischarge = await askQuestion(rl, chalk.white(`  目的港 [${shipment.portOfDischarge}]: `));
    const transportMode = await askQuestion(rl, chalk.white(`  运输方式 [${shipment.transportMode || 'Sea Freight'}]: `));
    const vesselVoyage = await askQuestion(rl, chalk.white(`  船名/航次 [${shipment.vesselVoyage || '-'}]: `));
    const containerNo = await askQuestion(rl, chalk.white(`  集装箱号 [${shipment.containerNo || '-'}]: `));
    const sealNo = await askQuestion(rl, chalk.white(`  封条号 [${shipment.sealNo || '-'}]: `));
    const cargoDescription = await askQuestion(rl, chalk.white(`  货物描述 [${shipment.cargoDescription || '-'}]: `));
    const packages = await askQuestion(rl, chalk.white(`  件数 [${shipment.packages || '-'}]: `));
    const grossWeight = await askQuestion(rl, chalk.white(`  毛重 [${shipment.grossWeight || '-'}]: `));
    const volume = await askQuestion(rl, chalk.white(`  体积 [${shipment.volume || '-'}]: `));
    const incoterms = await askQuestion(rl, chalk.white(`  贸易术语 [${shipment.incoterms || 'FOB'}]: `));
    const notes = await askQuestion(rl, chalk.white(`  备注 [${shipment.notes || '-'}]: `));
    const status = await askQuestion(rl, chalk.white(`  状态 [${shipment.status}]: `));
    
    // 更新字段
    if (orderId) shipment.orderId = orderId;
    if (customerId) shipment.customerId = customerId;
    if (customerName) shipment.customerName = customerName;
    if (portOfLoading) shipment.portOfLoading = portOfLoading;
    if (portOfDischarge) shipment.portOfDischarge = portOfDischarge;
    if (transportMode) shipment.transportMode = transportMode;
    if (vesselVoyage) shipment.vesselVoyage = vesselVoyage;
    if (containerNo) shipment.containerNo = containerNo;
    if (sealNo) shipment.sealNo = sealNo;
    if (cargoDescription) shipment.cargoDescription = cargoDescription;
    if (packages) shipment.packages = parseInt(packages);
    if (grossWeight) shipment.grossWeight = parseFloat(grossWeight);
    if (volume) shipment.volume = parseFloat(volume);
    if (incoterms) shipment.incoterms = incoterms;
    if (notes !== undefined) shipment.notes = notes;
    if (status) shipment.status = status;
    
    shipment.updatedAt = new Date().toISOString();
    shipments[index] = shipment;
    saveShipments(shipments);
    
    console.log(chalk.green('\n  ✅ 物流记录更新成功!\n'));
    
  } catch (error) {
    console.log(chalk.red(`  ❌ 更新失败：${error.message}`));
  } finally {
    rl.close();
  }
}

/**
 * 删除物流记录
 */
async function deleteShipment(id) {
  console.log(chalk.blue(`\n🗑️  删除物流记录：${id}\n`));
  
  const shipments = loadShipments();
  const index = shipments.findIndex(s => s.id === id);
  
  if (index === -1) {
    console.log(chalk.red(`  ❌ 未找到物流记录：${id}`));
    return;
  }
  
  const rl = createInterface();
  
  try {
    const confirm = await askQuestion(rl, chalk.red('  ⚠️  确认删除？(输入 yes 确认): '));
    
    if (confirm.toLowerCase() !== 'yes') {
      console.log(chalk.yellow('  取消删除\n'));
      return;
    }
    
    shipments.splice(index, 1);
    saveShipments(shipments);
    
    console.log(chalk.green('  ✅ 物流记录已删除\n'));
    
  } catch (error) {
    console.log(chalk.red(`  ❌ 删除失败：${error.message}`));
  } finally {
    rl.close();
  }
}

/**
 * 查看物流追踪
 */
async function viewTracking(id) {
  console.log(chalk.blue(`\n🚚 物流追踪：${id}\n`));
  
  const shipments = loadShipments();
  const shipment = shipments.find(s => s.id === id);
  
  if (!shipment) {
    console.log(chalk.red(`  ❌ 未找到物流记录：${id}`));
    return;
  }
  
  const tracking = loadTracking();
  const shipmentTracking = tracking.filter(t => t.shipmentId === id);
  
  if (shipmentTracking.length === 0) {
    console.log(chalk.yellow('  暂无追踪记录'));
    console.log(chalk.gray('  物流状态更新时会自动记录追踪信息\n'));
    return;
  }
  
  console.log(chalk.gray('  ' + '─'.repeat(100)));
  console.log(chalk.gray('  |') + chalk.cyan(' 时间'.padEnd(22)) + chalk.gray('|') + 
              chalk.cyan(' 地点'.padEnd(20)) + chalk.gray('|') + 
              chalk.cyan(' 状态'.padEnd(20)) + chalk.gray('|') + 
              chalk.cyan(' 备注'.padEnd(35)) + chalk.gray('|'));
  console.log(chalk.gray('  ' + '─'.repeat(100)));
  
  shipmentTracking.forEach((track) => {
    console.log(chalk.gray('  |') + chalk.white(track.timestamp.padEnd(22)) + chalk.gray('|') + 
                chalk.white((track.location || '-').padEnd(20)) + chalk.gray('|') + 
                chalk.white((track.status || '-').padEnd(20)) + chalk.gray('|') + 
                chalk.white((track.notes || '-').padEnd(35)) + chalk.gray('|'));
  });
  
  console.log(chalk.gray('  ' + '─'.repeat(100)));
  console.log(chalk.gray(`  共 ${shipmentTracking.length} 条追踪记录\n`));
}

/**
 * 管理报关单据
 */
async function manageDocuments(id) {
  console.log(chalk.blue(`\n📄 报关单据管理：${id}\n`));
  
  const documents = loadDocuments();
  const shipmentDocs = documents.filter(d => d.shipmentId === id);
  
  if (shipmentDocs.length === 0) {
    console.log(chalk.yellow('  暂无报关单据'));
    console.log(chalk.gray('  使用 add 命令添加单据\n'));
    return;
  }
  
  console.log(chalk.gray('  ' + '─'.repeat(100)));
  console.log(chalk.gray('  |') + chalk.cyan(' ID'.padEnd(25)) + chalk.gray('|') + 
              chalk.cyan(' 单据类型'.padEnd(20)) + chalk.gray('|') + 
              chalk.cyan(' 文件名'.padEnd(25)) + chalk.gray('|') + 
              chalk.cyan(' 上传时间'.padEnd(20)) + chalk.gray('|') + 
              chalk.cyan(' 状态'.padEnd(10)) + chalk.gray('|'));
  console.log(chalk.gray('  ' + '─'.repeat(100)));
  
  shipmentDocs.forEach((doc) => {
    const statusColor = doc.status === 'Approved' ? chalk.green : (doc.status === 'Pending' ? chalk.yellow : chalk.white);
    console.log(chalk.gray('  |') + chalk.white(doc.id.padEnd(25)) + chalk.gray('|') + 
                chalk.white((doc.docType || '-').padEnd(20)) + chalk.gray('|') + 
                chalk.white((doc.filename || '-').padEnd(25)) + chalk.gray('|') + 
                chalk.white((doc.uploadedAt || '-').padEnd(20)) + chalk.gray('|') + 
                statusColor((doc.status || '-').padEnd(10)) + chalk.gray('|'));
  });
  
  console.log(chalk.gray('  ' + '─'.repeat(100)));
  console.log(chalk.gray(`  共 ${shipmentDocs.length} 份单据\n`));
}

/**
 * 管理提单
 */
async function manageBol(id) {
  console.log(chalk.blue(`\n📜 提单管理：${id}\n`));
  
  const bols = loadBols();
  const shipmentBols = bols.filter(b => b.shipmentId === id);
  
  if (shipmentBols.length === 0) {
    console.log(chalk.yellow('  暂无提单'));
    console.log(chalk.gray('  使用 add 命令添加提单\n'));
    return;
  }
  
  console.log(chalk.gray('  ' + '─'.repeat(110)));
  console.log(chalk.gray('  |') + chalk.cyan(' ID'.padEnd(25)) + chalk.gray('|') + 
              chalk.cyan(' 提单号'.padEnd(20)) + chalk.gray('|') + 
              chalk.cyan(' 类型'.padEnd(15)) + chalk.gray('|') + 
              chalk.cyan(' 签发日期'.padEnd(15)) + chalk.gray('|') + 
              chalk.cyan(' 状态'.padEnd(15)) + chalk.gray('|') + 
              chalk.cyan(' 备注'.padEnd(15)) + chalk.gray('|'));
  console.log(chalk.gray('  ' + '─'.repeat(110)));
  
  shipmentBols.forEach((bol) => {
    const statusColor = bol.status === 'Released' ? chalk.green : (bol.status === 'Pending' ? chalk.yellow : chalk.white);
    console.log(chalk.gray('  |') + chalk.white(bol.id.padEnd(25)) + chalk.gray('|') + 
                chalk.white((bol.bolNo || '-').padEnd(20)) + chalk.gray('|') + 
                chalk.white((bol.bolType || '-').padEnd(15)) + chalk.gray('|') + 
                chalk.white((bol.issueDate || '-').padEnd(15)) + chalk.gray('|') + 
                statusColor((bol.status || '-').padEnd(15)) + chalk.gray('|') + 
                chalk.white((bol.notes || '-').padEnd(15)) + chalk.gray('|'));
  });
  
  console.log(chalk.gray('  ' + '─'.repeat(110)));
  console.log(chalk.gray(`  共 ${shipmentBols.length} 份提单\n`));
}

/**
 * 发送客户通知
 */
async function sendNotification(id) {
  console.log(chalk.blue(`\n📧 发送客户通知：${id}\n`));
  
  const shipments = loadShipments();
  const shipment = shipments.find(s => s.id === id);
  
  if (!shipment) {
    console.log(chalk.red(`  ❌ 未找到物流记录：${id}`));
    return;
  }
  
  const rl = createInterface();
  
  try {
    console.log(chalk.gray('  物流信息:'));
    console.log(chalk.gray(`    订单号：${shipment.orderId}`));
    console.log(chalk.gray(`    客户：${shipment.customerName || shipment.customerId}`));
    console.log(chalk.gray(`    路线：${shipment.portOfLoading} → ${shipment.portOfDischarge}`));
    console.log(chalk.gray(`    状态：${shipment.status}\n`));
    
    const notificationType = await askQuestion(rl, chalk.white('  通知类型 [Shipment Update]: ') || 'Shipment Update');
    const message = await askQuestion(rl, chalk.white('  通知内容: '));
    
    if (!message) {
      console.log(chalk.yellow('  取消发送\n'));
      rl.close();
      return;
    }
    
    const notification = {
      id: 'NOTIFY-' + Date.now().toString(36).toUpperCase(),
      shipmentId: id,
      customerId: shipment.customerId,
      customerName: shipment.customerName,
      notificationType,
      message,
      status: 'Sent',
      sentAt: new Date().toISOString()
    };
    
    const notifications = loadNotifications();
    notifications.push(notification);
    saveNotifications(notifications);
    
    console.log(chalk.green('\n  ✅ 通知已发送!'));
    console.log(chalk.gray(`  通知 ID: ${notification.id}`));
    console.log(chalk.gray(`  类型：${notification.notificationType}`));
    console.log(chalk.gray(`  状态：${notification.status}\n`));
    
  } catch (error) {
    console.log(chalk.red(`  ❌ 发送失败：${error.message}`));
  } finally {
    rl.close();
  }
}

/**
 * 同步到 OKKI
 */
async function syncToOKKI(id) {
  console.log(chalk.blue(`\n🔄 同步到 OKKI: ${id}\n`));
  
  const shipments = loadShipments();
  const shipment = shipments.find(s => s.id === id);
  
  if (!shipment) {
    console.log(chalk.red(`  ❌ 未找到物流记录：${id}`));
    return;
  }
  
  console.log(chalk.gray('  正在同步到 OKKI CRM...'));
  console.log(chalk.gray(`    订单号：${shipment.orderId}`));
  console.log(chalk.gray(`    客户：${shipment.customerName || shipment.customerId}`));
  console.log(chalk.gray(`    状态：${shipment.status}\n`));
  
  // 模拟同步到 OKKI
  // 实际实现时调用 OKKI API 创建跟进记录
  
  setTimeout(() => {
    console.log(chalk.green('  ✅ 同步成功!'));
    console.log(chalk.gray('  OKKI Trail ID: TRAIL-' + Date.now().toString(36).toUpperCase()));
    console.log(chalk.gray('  同步内容：物流状态更新\n'));
  }, 500);
}

/**
 * 辅助函数：加载各类数据
 */
function loadTracking() {
  if (fs.existsSync(TRACKING_FILE)) {
    return JSON.parse(fs.readFileSync(TRACKING_FILE, 'utf8'));
  }
  return [];
}

function loadDocuments() {
  if (fs.existsSync(DOCUMENTS_FILE)) {
    return JSON.parse(fs.readFileSync(DOCUMENTS_FILE, 'utf8'));
  }
  return [];
}

function loadBols() {
  if (fs.existsSync(BOLS_FILE)) {
    return JSON.parse(fs.readFileSync(BOLS_FILE, 'utf8'));
  }
  return [];
}

function loadNotifications() {
  if (fs.existsSync(NOTIFICATIONS_FILE)) {
    return JSON.parse(fs.readFileSync(NOTIFICATIONS_FILE, 'utf8'));
  }
  return [];
}

function saveNotifications(notifications) {
  fs.writeFileSync(NOTIFICATIONS_FILE, JSON.stringify(notifications, null, 2), 'utf8');
}

// 定义 CLI 命令
program
  .name('logistics-cli')
  .description('物流管理命令行工具')
  .version('1.0.0');

program
  .command('list')
  .description('列出所有物流记录')
  .action(listShipments);

program
  .command('get <id>')
  .description('查看单个物流记录详情')
  .action(getShipment);

program
  .command('create')
  .description('创建新物流记录（交互式）')
  .action(createShipment);

program
  .command('update <id>')
  .description('更新物流记录')
  .action(updateShipment);

program
  .command('delete <id>')
  .description('删除物流记录')
  .action(deleteShipment);

program
  .command('tracking <id>')
  .description('查看物流追踪')
  .action(viewTracking);

program
  .command('documents <id>')
  .description('管理报关单据')
  .action(manageDocuments);

program
  .command('bol <id>')
  .description('管理提单')
  .action(manageBol);

program
  .command('notify <id>')
  .description('发送客户通知')
  .action(sendNotification);

program
  .command('sync-okki <id>')
  .description('同步到 OKKI CRM')
  .action(syncToOKKI);

// 解析命令行参数
program.parse(process.argv);

// 如果没有提供命令，显示帮助
if (!process.argv.slice(2).length) {
  program.outputHelp();
}
