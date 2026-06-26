/**
 * 小红书竞品监控系统 - 主程序 V5
 * 整合所有模块 + 飞书卡片推送
 */

const fs = require('fs');
const path = require('path');
const puppeteerCore = require('puppeteer-core');
const { loadHistory, saveToHistory, deduplicate } = require('./dedupe');
const { parseNotes } = require('./parser');
const { getAccountUrl, ACCOUNTS: CONFIG_ACCOUNTS } = require('./config');

// 使用config中的账号，如未配置则报错
const ACCOUNTS = CONFIG_ACCOUNTS || [];

if (ACCOUNTS.length === 0) {
  console.error('❌ 请先配置账号！复制 config.example.js 为 config.js 并填入账号');
  process.exit(1);
}

const DEBUG_PORT = 9223;