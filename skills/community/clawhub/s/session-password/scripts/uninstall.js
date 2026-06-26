#!/usr/bin/env node
/**
 * Session Password - Uninstall Tool v1.0.0
 * Author: squallsol
 * 
 * Removes all authentication configuration and cleans up the system.
 * Requires passphrase confirmation before executing.
 */

const fs = require('fs');
const path = require('path');
const bcrypt = require('bcrypt');
const readline = require('readline');

const WORKSPACE = process.env.OPENCLAW_WORKSPACE || path.join(process.env.HOME, '.openclaw', 'workspace');
const MEMORY_DIR = path.join(WORKSPACE, 'memory');
const SKILL_DIR = path.join(WORKSPACE, 'skills', 'session-password');

const CONFIG_FILE = path.join(MEMORY_DIR, 'auth-config.json');
const USERS_FILE = path.join(MEMORY_DIR, 'auth-users.json');
const STATE_FILE = path.join(MEMORY_DIR, 'auth-state.json');
const AUDIT_FILE = path.join(MEMORY_DIR, 'auth-audit.log');
const PASSPHRASE_FILE = path.join(MEMORY_DIR, 'passphrase.json');

function loadJson(file, defaultValue = {}) {
  try {
    return JSON.parse(fs.readFileSync(file, 'utf8'));
  } catch {
    return defaultValue;
  }
}

async function prompt(rl, question, hidden = false) {
  return new Promise((resolve) => {
    if (hidden) {
      process.stdout.write(question);
      process.stdin.setRawMode(true);
      process.stdin.resume();
      process.stdin.setEncoding('utf8');
      let password = '';
      process.stdin.on('data', (char) => {
        if (char === '\n' || char === '\r') {
          process.stdin.setRawMode(false);
          process.stdin.pause();
          console.log();
          resolve(password);
        } else if (char === '\u0003') {
          process.exit();
        } else {
          password += char;
        }
      });
    } else {
      rl.question(question, (answer) => {
        resolve(answer.trim());
      });
    }
  });
}

async function uninstall() {
  // Detect language from config
  let language = 'zh-CN';
  try {
    const config = loadJson(CONFIG_FILE, {});
    language = config.language || 'zh-CN';
  } catch {}
  
  const isEnglish = language === 'en';
  
  console.log(isEnglish 
    ? '\n🗑️  Session Password - Uninstall Tool v1.0.0\n'
    : '\n🗑️  会话口令守护 - 卸载工具 v1.0.0\n');
  console.log('Author: squallsol\n');
  
  // Check if installed
  if (!fs.existsSync(USERS_FILE)) {
    console.log(isEnglish 
      ? '❌ Session Password is not installed. Nothing to uninstall.\n'
      : '❌ 会话口令守护未安装，无需卸载。\n');
    return;
  }
  
  const users = loadJson(USERS_FILE, { users: {} });
  const usernames = Object.keys(users.users);
  
  if (usernames.length === 0) {
    console.log(isEnglish 
      ? '❌ No user data found.\n'
      : '❌ 未找到用户数据。\n');
    return;
  }
  
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
  });
  
  try {
    // Step 1: Confirm passphrase
    const username = usernames[0]; // Primary user
    const user = users.users[username];
    
    console.log(isEnglish 
      ? `Please enter passphrase to confirm uninstall:\n`
      : `请输入口令以确认卸载：\n`);
    const passphrase = await prompt(rl, isEnglish ? 'Passphrase: ' : '口令: ', true);
    
    // Verify passphrase
    let valid = false;
    if (user.hashAlgorithm === 'bcrypt' || user.passphraseHash.startsWith('$2')) {
      valid = await bcrypt.compare(passphrase, user.passphraseHash);
    } else {
      // Legacy SHA256
      const crypto = require('crypto');
      const hash = crypto.createHash('sha256').update(passphrase).digest('hex');
      valid = hash === user.passphraseHash;
    }
    
    if (!valid) {
      console.log(isEnglish 
        ? '\n❌ Incorrect passphrase. Uninstall cancelled.\n'
        : '\n❌ 口令不正确，卸载已取消。\n');
      rl.close();
      return;
    }
    
    // Step 2: Final confirmation
    console.log(isEnglish 
      ? '\n⚠️  The following files and directories will be deleted:\n'
      : '\n⚠️  即将删除以下文件和目录：\n');
    console.log(isEnglish ? 'Configuration files:' : '配置文件：');
    if (fs.existsSync(CONFIG_FILE)) console.log(`  - ${CONFIG_FILE}`);
    if (fs.existsSync(USERS_FILE)) console.log(`  - ${USERS_FILE}`);
    if (fs.existsSync(STATE_FILE)) console.log(`  - ${STATE_FILE}`);
    if (fs.existsSync(AUDIT_FILE)) console.log(`  - ${AUDIT_FILE}`);
    if (fs.existsSync(PASSPHRASE_FILE)) console.log(`  - ${PASSPHRASE_FILE}`);
    
    console.log(isEnglish ? '\nSkill directory:' : '\nSkill 目录：');
    if (fs.existsSync(SKILL_DIR)) console.log(`  - ${SKILL_DIR}`);
    
    console.log(isEnglish 
      ? '\nThis action cannot be undone!\n'
      : '\n此操作不可恢复！\n');
    
    const confirm = await prompt(rl, isEnglish 
      ? 'Confirm uninstall? Type "yes" to continue: '
      : '确认卸载？输入 "yes" 继续: ');
    
    if (confirm.toLowerCase() !== 'yes') {
      console.log(isEnglish 
        ? '\n❌ Uninstall cancelled.\n'
        : '\n❌ 卸载已取消。\n');
      rl.close();
      return;
    }
    
    // Step 3: Execute uninstall
    console.log(isEnglish ? '\nUninstalling...\n' : '\n正在卸载...\n');
    
    // Remove config files
    const filesToRemove = [CONFIG_FILE, USERS_FILE, STATE_FILE, AUDIT_FILE, PASSPHRASE_FILE];
    let removedCount = 0;
    
    for (const file of filesToRemove) {
      if (fs.existsSync(file)) {
        fs.unlinkSync(file);
        console.log(isEnglish 
          ? `  ✓ Deleted: ${path.basename(file)}`
          : `  ✓ 已删除: ${path.basename(file)}`);
        removedCount++;
      }
    }
    
    // Remove skill directory
    if (fs.existsSync(SKILL_DIR)) {
      fs.rmSync(SKILL_DIR, { recursive: true, force: true });
      console.log(isEnglish 
        ? `  ✓ Deleted: session-password/`
        : `  ✓ 已删除: session-password/`);
      removedCount++;
    }
    
    console.log(isEnglish 
      ? `\n✅ Uninstall complete! ${removedCount} items removed.\n`
      : `\n✅ 卸载完成！已删除 ${removedCount} 项。\n`);
    console.log(isEnglish 
      ? 'Session Password has been completely removed. No passphrase required.\n'
      : '会话口令守护已完全移除。系统不再需要口令认证。\n');
    
  } finally {
    rl.close();
  }
}

// Run
uninstall().catch(console.error);
