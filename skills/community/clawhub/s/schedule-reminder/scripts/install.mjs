#!/usr/bin/env node
/**
 * 安装脚本 - 自动配置双保险提醒系统
 */

import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { execSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const HOME_DIR = process.env.HOME || os.homedir();
const SKILL_DIR = path.resolve(__dirname, '..');
const DATA_DIR = path.join(HOME_DIR, '.openclaw', 'data');
const CONFIG_SOURCE = path.join(SKILL_DIR, 'config', 'default.json');
const CONFIG_TARGET = path.join(DATA_DIR, 'schedule-reminder-config.json');
const REMINDERS_FILE = path.join(DATA_DIR, 'reminders.json');
const RUNTIME_FILE = path.join(DATA_DIR, 'schedule-reminder-runtime.json');
const BACKUP_SCRIPT = path.join(SKILL_DIR, 'scripts', 'reminder-backup.mjs');
const DAILY_BRIEF_SCRIPT = path.join(SKILL_DIR, 'scripts', 'daily-brief.mjs');
const LOG_FILE = path.join(DATA_DIR, 'reminder-backup.log');
const SERVICE_LABEL = 'ai.openclaw.schedule-reminder.backup';
const DAILY_SERVICE_LABEL = 'ai.openclaw.schedule-reminder.daily-brief';

console.log('🚀 安装双保险提醒系统...\n');

function resolveBin(name) {
  try {
    const value = execSync(`command -v ${name}`, { encoding: 'utf-8', stdio: ['ignore', 'pipe', 'ignore'] }).trim();
    return value || null;
  } catch {
    return null;
  }
}

function shellQuote(value) {
  return `'${String(value).replace(/'/g, `'\\''`)}'`;
}

function escapeXml(value) {
  return String(value)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&apos;');
}

function writeJson(filePath, data) {
  fs.writeFileSync(filePath, JSON.stringify(data, null, 2));
}

function installLinuxCron({ nodeBin, openclawBin }) {
  const crontabBin = resolveBin('crontab');
  if (!crontabBin) {
    console.warn('⚠️  未找到 crontab，已跳过 Linux 定时安装');
    return;
  }

  const shellCommand = [
    `HOME=${shellQuote(HOME_DIR)}`,
    `PATH=${shellQuote(process.env.PATH || '/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin')}`,
    openclawBin ? `OPENCLAW_BIN=${shellQuote(openclawBin)}` : '',
    `${shellQuote(nodeBin)} ${shellQuote(BACKUP_SCRIPT)} >> ${shellQuote(LOG_FILE)} 2>&1`,
  ]
    .filter(Boolean)
    .join(' ');
  
  const dailyShellCommand = [
    `HOME=${shellQuote(HOME_DIR)}`,
    `PATH=${shellQuote(process.env.PATH || '/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin')}`,
    openclawBin ? `OPENCLAW_BIN=${shellQuote(openclawBin)}` : '',
    `${shellQuote(nodeBin)} ${shellQuote(DAILY_BRIEF_SCRIPT)} >> ${shellQuote(LOG_FILE)} 2>&1`,
  ].filter(Boolean).join(' ');

  const backupCronLine = `* * * * * /bin/sh -lc ${shellQuote(shellCommand)}`;
  const dailyCronLine = `0 8 * * * /bin/sh -lc ${shellQuote(dailyShellCommand)}`;

  try {
    const currentCrontab = execSync(`${crontabBin} -l 2>/dev/null || echo ""`, {
      encoding: 'utf-8',
    });

    let nextCrontab = currentCrontab.trim();
    let modified = false;
    
    if (!nextCrontab.includes(BACKUP_SCRIPT)) {
      nextCrontab += `\n# 双保险提醒系统 - 备用检查\n${backupCronLine}\n`;
      modified = true;
    }
    
    if (!nextCrontab.includes(DAILY_BRIEF_SCRIPT)) {
      nextCrontab += `\n# 双保险提醒系统 - 每日早报\n${dailyCronLine}\n`;
      modified = true;
    }

    if (!modified) {
      console.log('ℹ️  Linux crontab 已配置');
      return;
    }

    execSync(`printf %s ${shellQuote(nextCrontab)} | ${crontabBin} -`, { stdio: 'ignore' });
    console.log('✅ Linux crontab 已更新');
  } catch (err) {
    console.warn('⚠️  Linux crontab 安装失败:', err.message);
    console.log('   请手动添加以下行到 crontab:');
    console.log('   ', backupCronLine);
    console.log('   ', dailyCronLine);
  }
}

function installMacLaunchd({ nodeBin, openclawBin }) {
  const launchAgentsDir = path.join(HOME_DIR, 'Library', 'LaunchAgents');
  const plistPath = path.join(launchAgentsDir, `${SERVICE_LABEL}.plist`);
  const dailyPlistPath = path.join(launchAgentsDir, `${DAILY_SERVICE_LABEL}.plist`);
  const uid = execSync('id -u', { encoding: 'utf-8' }).trim();
  const envPath = process.env.PATH || '/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin';

  fs.mkdirSync(launchAgentsDir, { recursive: true });

  const plist = `<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>${escapeXml(SERVICE_LABEL)}</string>
  <key>ProgramArguments</key>
  <array>
    <string>${escapeXml(nodeBin)}</string>
    <string>${escapeXml(BACKUP_SCRIPT)}</string>
  </array>
  <key>WorkingDirectory</key>
  <string>${escapeXml(SKILL_DIR)}</string>
  <key>RunAtLoad</key>
  <true/>
  <key>StartInterval</key>
  <integer>60</integer>
  <key>EnvironmentVariables</key>
  <dict>
    <key>HOME</key>
    <string>${escapeXml(HOME_DIR)}</string>
    <key>PATH</key>
    <string>${escapeXml(envPath)}</string>
    ${openclawBin ? `<key>OPENCLAW_BIN</key>\n    <string>${escapeXml(openclawBin)}</string>` : ''}
  </dict>
  <key>StandardOutPath</key>
  <string>${escapeXml(LOG_FILE)}</string>
  <key>StandardErrorPath</key>
  <string>${escapeXml(LOG_FILE)}</string>
</dict>
</plist>
`;

  const dailyPlist = `<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>${escapeXml(DAILY_SERVICE_LABEL)}</string>
  <key>ProgramArguments</key>
  <array>
    <string>${escapeXml(nodeBin)}</string>
    <string>${escapeXml(DAILY_BRIEF_SCRIPT)}</string>
  </array>
  <key>WorkingDirectory</key>
  <string>${escapeXml(SKILL_DIR)}</string>
  <key>StartCalendarInterval</key>
  <dict>
    <key>Hour</key>
    <integer>8</integer>
    <key>Minute</key>
    <integer>0</integer>
  </dict>
  <key>EnvironmentVariables</key>
  <dict>
    <key>HOME</key>
    <string>${escapeXml(HOME_DIR)}</string>
    <key>PATH</key>
    <string>${escapeXml(envPath)}</string>
    ${openclawBin ? `<key>OPENCLAW_BIN</key>\n    <string>${escapeXml(openclawBin)}</string>` : ''}
  </dict>
  <key>StandardOutPath</key>
  <string>${escapeXml(LOG_FILE)}</string>
  <key>StandardErrorPath</key>
  <string>${escapeXml(LOG_FILE)}</string>
</dict>
</plist>
`;

  fs.writeFileSync(plistPath, plist);
  fs.writeFileSync(dailyPlistPath, dailyPlist);

  try {
    execSync(`launchctl bootout gui/${uid} ${shellQuote(plistPath)}`, { stdio: 'ignore' });
    execSync(`launchctl bootout gui/${uid} ${shellQuote(dailyPlistPath)}`, { stdio: 'ignore' });
  } catch {
    // ignore bootout failures for first install
  }

  try {
    execSync(`launchctl bootstrap gui/${uid} ${shellQuote(plistPath)}`, { stdio: 'ignore' });
    execSync(`launchctl enable gui/${uid}/${SERVICE_LABEL}`, { stdio: 'ignore' });
    
    execSync(`launchctl bootstrap gui/${uid} ${shellQuote(dailyPlistPath)}`, { stdio: 'ignore' });
    execSync(`launchctl enable gui/${uid}/${DAILY_SERVICE_LABEL}`, { stdio: 'ignore' });
    
    console.log('✅ macOS launchd 已安装 (备用检查 + 每日早报)');
  } catch (err) {
    console.warn('⚠️  macOS launchd 安装失败:', err.message);
    console.log('   请手动加载:');
    console.log(`   launchctl bootstrap gui/${uid} ${plistPath}`);
    console.log(`   launchctl bootstrap gui/${uid} ${dailyPlistPath}`);
  }
}

// 1. 检查并创建数据目录
fs.mkdirSync(DATA_DIR, { recursive: true });
console.log('✅ 数据目录:', DATA_DIR);

// 2. 复制配置文件（如果不存在）
if (!fs.existsSync(CONFIG_TARGET)) {
  fs.copyFileSync(CONFIG_SOURCE, CONFIG_TARGET);
  console.log('✅ 配置文件已创建:', CONFIG_TARGET);
  console.log('⚠️  请编辑配置文件，填写你的 userId 和 accountId');
} else {
  console.log('ℹ️  配置文件已存在:', CONFIG_TARGET);
}

// 3. 创建提醒数据文件
if (!fs.existsSync(REMINDERS_FILE)) {
  fs.writeFileSync(REMINDERS_FILE, JSON.stringify({ reminders: [], lastCheck: 0 }, null, 2));
  console.log('✅ 提醒数据文件已创建');
}

// 4. 记录运行时路径
const runtime = {
  installedAt: new Date().toISOString(),
  platform: process.platform,
  nodeBin: process.execPath,
  openclawBin: resolveBin('openclaw'),
  backupScript: BACKUP_SCRIPT,
  logFile: LOG_FILE,
};
writeJson(RUNTIME_FILE, runtime);
console.log('✅ 运行时配置已写入:', RUNTIME_FILE);

// 5. 安装平台调度器
if (process.platform === 'darwin') {
  installMacLaunchd({ nodeBin: runtime.nodeBin, openclawBin: runtime.openclawBin });
} else if (process.platform === 'linux') {
  installLinuxCron({ nodeBin: runtime.nodeBin, openclawBin: runtime.openclawBin });
} else {
  console.warn(`⚠️  当前平台 ${process.platform} 暂未自动安装调度器，请手动调度 ${BACKUP_SCRIPT}`);
}

console.log('\n📋 安装完成！');
console.log('\n使用说明:');
console.log('  1. 编辑配置:', CONFIG_TARGET);
console.log('  2. 创建提醒: node scripts/create-reminder.mjs "名称" "消息" "+5m"');
console.log('  3. 查看日志:', LOG_FILE);
