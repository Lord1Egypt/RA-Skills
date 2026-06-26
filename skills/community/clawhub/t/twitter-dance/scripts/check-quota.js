#!/usr/bin/env node

/**
 * Twitter Dance - API 配额检查工具
 * 
 * 用法：
 * node scripts/check-quota.js                # 检查一次
 * node scripts/check-quota.js --watch        # 监控模式（每 5 秒刷新一次）
 * node scripts/check-quota.js --json         # JSON 输出
 */

const TwitterDanceAPIClient = require('../src/twitter-api-client');
const fs = require('fs');
const path = require('path');

require('dotenv').config({ path: path.join(__dirname, '../.env') });

const args = process.argv.slice(2);
const isWatch = args.includes('--watch');
const isJson = args.includes('--json');

// 颜色定义
const colors = {
  reset: '\x1b[0m',
  bright: '\x1b[1m',
  dim: '\x1b[2m',
  red: '\x1b[31m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  cyan: '\x1b[36m'
};

/**
 * 格式化百分比条
 */
function formatProgressBar(used, total, width = 30) {
  const percentage = Math.round((used / total) * 100);
  const filledWidth = Math.round((percentage / 100) * width);
  
  let color = colors.green;
  if (percentage > 80) color = colors.red;
  else if (percentage > 60) color = colors.yellow;
  
  const bar = '█'.repeat(filledWidth) + '░'.repeat(width - filledWidth);
  return `${color}${bar}${colors.reset} ${percentage}%`;
}

/**
 * 格式化数字（千位分隔）
 */
function formatNumber(num) {
  return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
}

/**
 * 显示配额信息（美化格式）
 */
function displayQuota(quota) {
  console.clear();
  console.log(`\n${colors.bright}${colors.cyan}╔════════════════════════════════════════════╗${colors.reset}`);
  console.log(`${colors.bright}${colors.cyan}║   🎭 Twitter Dance - API 配额监控        ║${colors.reset}`);
  console.log(`${colors.bright}${colors.cyan}╚════════════════════════════════════════════╝${colors.reset}\n`);

  console.log(`${colors.bright}API Key Status${colors.reset}`);
  console.log(`  Key: ${quota.apiKey?.substring(0, 10)}...${quota.apiKey?.substring(-5)}`);
  console.log(`  时间: ${quota.timestamp || new Date().toLocaleString('zh-CN')}\n`);

  console.log(`${colors.bright}配额使用情况${colors.reset}`);
  console.log(`  剩余: ${colors.bright}${formatNumber(quota.remaining)}${colors.reset} 次\n`);

  if (quota.remaining > 0) {
    console.log(`${colors.bright}状态${colors.reset}`);
    if (quota.remaining > 5000) {
      console.log(`  ${colors.green}✅ 配额充足，可正常使用${colors.reset}`);
    } else if (quota.remaining > 1000) {
      console.log(`  ${colors.yellow}⚠️  配额开始不足，请准备购买${colors.reset}`);
    } else if (quota.remaining > 0) {
      console.log(`  ${colors.red}⚠️  配额即将用尽，请立即购买！${colors.reset}`);
    }
  } else {
    console.log(`  ${colors.red}❌ 配额已用尽！${colors.reset}`);
  }

  console.log(`\n${colors.dim}apidance.pro: https://t.me/shingle${colors.reset}`);
  if (isWatch) {
    console.log(`${colors.dim}监控模式中... (按 Ctrl+C 退出)${colors.reset}`);
  }
  console.log('');
}

/**
 * 显示 JSON 格式
 */
function displayJson(quota) {
  const output = {
    success: true,
    data: {
      remaining: quota.remaining,
      timestamp: quota.timestamp,
      apiKey: quota.apiKey
    }
  };
  
  console.log(JSON.stringify(output, null, 2));
}

/**
 * 主函数
 */
async function main() {
  try {
    const client = new TwitterDanceAPIClient({
      verbose: false
    });

    if (isWatch) {
      // 监控模式
      console.log(`${colors.cyan}🔍 API 配额监控模式已启动...${colors.reset}\n`);
      
      const checkQuota = async () => {
        try {
          const quota = await client.checkQuota();
          quota.apiKey = client.apiKey;
          
          if (isJson) {
            displayJson(quota);
          } else {
            displayQuota(quota);
          }
        } catch (err) {
          console.error(`${colors.red}[❌] 配额检查失败: ${err.message}${colors.reset}`);
        }
      };

      // 首次立即检查
      await checkQuota();

      // 然后每 5 秒检查一次
      setInterval(checkQuota, 5000);
    } else {
      // 单次检查
      const quota = await client.checkQuota();
      quota.apiKey = client.apiKey;
      
      if (isJson) {
        displayJson(quota);
      } else {
        displayQuota(quota);
      }
    }
  } catch (err) {
    console.error(`${colors.red}[❌] 错误: ${err.message}${colors.reset}`);
    process.exit(1);
  }
}

main();
