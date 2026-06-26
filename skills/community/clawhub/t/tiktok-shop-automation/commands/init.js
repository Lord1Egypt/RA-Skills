/**
 * 初始化配置模块
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import inquirer from 'inquirer';
import chalk from 'chalk';
import { loadConfig as loadConfigFromSrc, saveConfig as saveConfigFromSrc, toggleMockMode } from '../src/config.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const CONFIG_DIR = path.join(process.env.HOME || process.env.USERPROFILE, '.clawhub', 'tiktok-shop');
const CONFIG_FILE = path.join(CONFIG_DIR, 'config.json');

/**
 * 初始化配置
 */
export async function initConfig() {
  // 创建配置目录
  if (!fs.existsSync(CONFIG_DIR)) {
    fs.mkdirSync(CONFIG_DIR, { recursive: true });
  }

  // 如果配置文件已存在，询问是否覆盖
  if (fs.existsSync(CONFIG_FILE)) {
    const { overwrite } = await inquirer.prompt([
      {
        type: 'confirm',
        name: 'overwrite',
        message: '配置文件已存在，是否覆盖？',
        default: false
      }
    ]);

    if (!overwrite) {
      console.log(chalk.yellow('⚠️  已取消初始化'));
      return;
    }
  }

  // 收集配置信息
  const answers = await inquirer.prompt([
    {
      type: 'confirm',
      name: 'useMock',
      message: '是否使用 Mock API 模式？（无需 TikTok API 权限，推荐开发测试使用）',
      default: true
    },
    {
      type: 'input',
      name: 'defaultRegion',
      message: '默认地区 (US/UK/SEA/ID):',
      default: 'US',
      when: (a) => !a.useMock
    },
    {
      type: 'confirm',
      name: 'enableFeishu',
      message: '是否启用飞书集成？',
      default: true
    }
  ]);

  const config = {
    tiktok: {
      apiKey: '',
      apiSecret: '',
      shopId: '',
      region: answers.defaultRegion || 'US',
      useMock: answers.useMock
    },
    feishu: {
      enabled: answers.enableFeishu,
      appToken: '',
      tableId: '',
      webhookUrl: ''
    },
    accounts: [],
    currentAccount: null,
    notifications: {
      feishuWebhook: '',
      email: ''
    },
    autoSync: {
      orders: {
        enabled: false,
        interval: 15
      },
      inventory: {
        enabled: false,
        interval: 60
      }
    }
  };

  if (answers.enableFeishu) {
    const feishuAnswers = await inquirer.prompt([
      {
        type: 'input',
        name: 'appToken',
        message: '飞书多维表格 App Token:'
      },
      {
        type: 'input',
        name: 'tableId',
        message: '飞书多维表格 Table ID:'
      },
      {
        type: 'input',
        name: 'webhookUrl',
        message: '飞书机器人 Webhook URL:'
      }
    ]);

    config.feishu.appToken = feishuAnswers.appToken;
    config.feishu.tableId = feishuAnswers.tableId;
    config.feishu.webhookUrl = feishuAnswers.webhookUrl;
  }

  if (!answers.useMock) {
    const apiAnswers = await inquirer.prompt([
      {
        type: 'input',
        name: 'apiKey',
        message: 'TikTok Shop API Key:',
        mask: true
      },
      {
        type: 'input',
        name: 'apiSecret',
        message: 'TikTok Shop API Secret:',
        mask: true
      },
      {
        type: 'input',
        name: 'shopId',
        message: 'TikTok Shop ID:'
      }
    ]);

    config.tiktok.apiKey = apiAnswers.apiKey;
    config.tiktok.apiSecret = apiAnswers.apiSecret;
    config.tiktok.shopId = apiAnswers.shopId;
  }

  // 保存配置
  saveConfigFromSrc(config);
  
  console.log(chalk.green('\n✓ 配置文件已保存到:', CONFIG_FILE));
  console.log(chalk.blue('\n提示:'));
  console.log('  - 使用 add-account 命令添加 TikTok 账号');
  console.log('  - 使用 toggle-mock 命令切换 Mock/真实 API 模式');
  
  if (answers.useMock) {
    console.log(chalk.yellow('\n⚠️  当前为 Mock 模式，适合开发和测试'));
    console.log('   生产使用请配置真实 TikTok API 并切换模式');
  }
}

/**
 * 加载配置（兼容旧版）
 */
export function loadConfig() {
  return loadConfigFromSrc();
}

/**
 * 保存配置（兼容旧版）
 */
export function saveConfig(config) {
  return saveConfigFromSrc(config);
}

/**
 * 切换 Mock 模式
 */
export async function toggleMockCommand() {
  const config = loadConfig();
  const newMode = !config.tiktok.useMock;
  
  console.log(`🔄 切换 API 模式...`);
  console.log(`  当前：${config.tiktok.useMock ? 'Mock' : '真实 API'}`);
  console.log(`  目标：${newMode ? 'Mock' : '真实 API'}`);
  
  toggleMockMode(newMode);
  
  console.log(`✓ 已切换到${newMode ? ' Mock' : ' 真实 API'}模式`);
  
  if (!newMode) {
    console.log(chalk.yellow('\n⚠️  请确保已配置 TikTok API 凭证'));
  }
}
