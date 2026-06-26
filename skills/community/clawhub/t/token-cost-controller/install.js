/**
 * 安装脚本
 */
const fs = require('fs');
const path = require('path');

console.log('Token省钱管家安装中...');

// 创建数据目录
const dataDir = path.join(__dirname, '.openclaw', 'data');
fs.mkdirSync(dataDir, { recursive: true });

// 初始化配置文件
const configFile = path.join(dataDir, 'controls.json');
if (!fs.existsSync(configFile)) {
  fs.writeFileSync(configFile, JSON.stringify({
    disabledSkills: [],
    pausedPlans: [],
    maxCostPerSkill: {},
    skillCosts: {}
  }, null, 2));
}

console.log('安装完成!');
console.log('使用: node cli.js report');
