#!/usr/bin/env node

const SinopecOilPriceSkill = require('./index.js');
const fs = require('fs');
const path = require('path');

// 历史数据文件路径
const HISTORY_FILE = path.join(__dirname, 'oil-price-history.json');

/**
 * 读取历史油价数据
 */
function readHistory() {
  try {
    if (fs.existsSync(HISTORY_FILE)) {
      const data = fs.readFileSync(HISTORY_FILE, 'utf8');
      return JSON.parse(data);
    }
  } catch (e) {
    console.error('读取历史数据失败:', e.message);
  }
  return { date: '', prices: {} };
}

/**
 * 保存历史油价数据
 */
function saveHistory(data) {
  try {
    fs.writeFileSync(HISTORY_FILE, JSON.stringify(data, null, 2));
    console.log('历史数据已保存');
  } catch (e) {
    console.error('保存历史数据失败:', e.message);
  }
}

/**
 * 格式化价格显示
 */
function formatPrice(priceObj) {
  if (!priceObj) return '暂无数据';
  return `${priceObj.price}元/升 (${priceObj.change >= 0 ? '+' : ''}${priceObj.change})`;
}

/**
 * 比较价格变化
 */
function comparePrices(oldPrice, newPrice) {
  if (!oldPrice || !newPrice) return null;
  const priceChanged = oldPrice.price !== newPrice.price;
  const change = newPrice.price - oldPrice.price;
  return {
    changed: priceChanged,
    old: oldPrice.price,
    new: newPrice.price,
    diff: change
  };
}

/**
 * 主监控函数
 */
async function monitorOilPrice() {
  console.log('=== 开始监控广西油价 ===');
  
  const skill = new SinopecOilPriceSkill();
  
  // 1. 查询当前油价
  const current = await skill.getOilPrice({ province_name: '广西' });
  if (!current.success) {
    console.error('查询油价失败:', current.message);
    process.exit(1);
  }
  
  console.log(`查询时间: ${current.date}`);
  console.log(`省份: ${current.province}`);
  
  // 2. 读取历史数据
  const history = readHistory();
  console.log(`上次记录: ${history.date || '无记录'}`);
  
  // 3. 提取当前价格（取第一个区域，广西只有一个价区）
  const currentPrice = current.prices[0];
  if (!currentPrice) {
    console.error('未获取到油价数据');
    process.exit(1);
  }
  
  // 4. 定义要监控的油品类型
  const oilTypes = [
    { key: 'gas_92', name: '92号汽油' },
    { key: 'gas_95', name: '95号汽油' },
    { key: 'gas_98', name: '98号汽油' },
    { key: 'diesel_0', name: '0号柴油' },
    { key: 'aipao_98', name: '爱跑98' }
  ];
  
  // 5. 比较价格变化
  const changes = [];
  oilTypes.forEach(({ key, name }) => {
    const oldPrice = history.prices[key];
    const newPrice = currentPrice[key];
    
    if (newPrice) {
      const comparison = comparePrices(oldPrice, newPrice);
      if (comparison && comparison.changed) {
        changes.push({
          name,
          old: comparison.old,
          new: comparison.new,
          diff: comparison.diff
        });
      }
    }
  });
  
  // 6. 如果有变化，生成消息内容
  let message = '';
  if (changes.length > 0) {
    message = `⛽ 广西油价变动通知（${current.date}）\n\n`;
    changes.forEach(change => {
      const arrow = change.diff > 0 ? '↑' : '↓';
      message += `${change.name}: ${change.old} → ${change.new}元/升 (${arrow} ${Math.abs(change.diff)})\n`;
    });
    message += `\n数据来源：中石化官方API\n仅供参考，以加油站实际价格为准`;
  } else {
    console.log('油价无变化');
    message = `⛽ 广西油价日报（${current.date}）\n\n`;
    oilTypes.forEach(({ key, name }) => {
      const price = currentPrice[key];
      if (price) {
        message += `${name}: ${price.price}元/升 (${price.change >= 0 ? '+' : ''}${price.change})\n`;
      }
    });
    message += `\n（今日油价无变化）`;
  }
  
  console.log('\n消息内容:\n', message);
  
  // 7. 保存当前数据为历史
  const historyData = {
    date: current.date,
    province: current.province,
    prices: {}
  };
  
  oilTypes.forEach(({ key }) => {
    if (currentPrice[key]) {
      historyData.prices[key] = currentPrice[key];
    }
  });
  
  saveHistory(historyData);
  
  // 8. 输出结果（实际发送消息需要配合OpenClaw消息系统）
  console.log('\n=== 监控完成 ===');
  console.log('注意：此脚本需要集成到OpenClaw的cron或消息系统中才能自动发送通知');
  
  return {
    success: true,
    message: message,
    hasChanges: changes.length > 0,
    changes: changes
  };
}

// 执行监控
monitorOilPrice().then(result => {
  console.log('\n结果:', JSON.stringify(result, null, 2));
  process.exit(0);
}).catch(e => {
  console.error('监控失败:', e);
  process.exit(1);
});
