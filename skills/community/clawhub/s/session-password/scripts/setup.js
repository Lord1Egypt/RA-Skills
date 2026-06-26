#!/usr/bin/env node
/**
 * Session Password - Setup Wizard v1.0.0
 * Author: squallsol
 * 
 * First-time setup with mandatory email for recovery.
 */

const fs = require('fs');
const path = require('path');
const bcrypt = require('bcrypt');
const crypto = require('crypto');
const readline = require('readline');

const WORKSPACE = process.env.OPENCLAW_WORKSPACE || path.join(process.env.HOME, '.openclaw', 'workspace');
const MEMORY_DIR = path.join(WORKSPACE, 'memory');

if (!fs.existsSync(MEMORY_DIR)) {
  fs.mkdirSync(MEMORY_DIR, { recursive: true });
}

const CONFIG_FILE = path.join(MEMORY_DIR, 'auth-config.json');
const USERS_FILE = path.join(MEMORY_DIR, 'auth-users.json');
const AUDIT_FILE = path.join(MEMORY_DIR, 'auth-audit.log');

const WEAK_PASSWORDS = [
  'password', 'Password123!', '123456789', 'qwerty', 'admin',
  'welcome1', 'letmein', 'abc123', 'monkey', 'master'
];

function validatePassword(password, config = {}) {
  const errors = [];
  const minLength = config.passwordMinLength || 12;
  
  if (password.length < minLength) {
    errors.push(`口令至少需要 ${minLength} 个字符`);
  }
  if (!/[a-z]/.test(password)) {
    errors.push('口令必须包含小写字母');
  }
  if (!/[A-Z]/.test(password)) {
    errors.push('口令必须包含大写字母');
  }
  if (!/\d/.test(password)) {
    errors.push('口令必须包含数字');
  }
  if (!/[@$!%*?&]/.test(password)) {
    errors.push('口令必须包含特殊符号（@$!%*?&）');
  }
  if (WEAK_PASSWORDS.includes(password.toLowerCase())) {
    errors.push('口令过于常见或太弱');
  }
  
  return errors;
}

function saveJson(file, data) {
  fs.writeFileSync(file, JSON.stringify(data, null, 2));
  fs.chmodSync(file, 0o600);
}

function validateEmail(email) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
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

async function setup() {
  console.log('\n🔐 Session Password - Setup Wizard v1.0.0\n');
  console.log('🔐 会话口令守护 - 设置向导 v1.0.0\n');
  console.log('Author: squallsol\n');
  
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
  });
  
  try {
    // Step 0: Language selection
    console.log('请选择语言 / Select language:');
    console.log('  1. 中文 (zh-CN)');
    console.log('  2. English (en)');
    const langInput = await prompt(rl, '[1/2, default 1]: ');
    const language = langInput === '2' ? 'en' : 'zh-CN';
    const isEnglish = language === 'en';
    
  console.log(isEnglish 
    ? '\nThis wizard will help you configure passphrase authentication.\n'
    : '\n此向导将帮助您配置口令认证。\n');
    
    console.log(`\n${isEnglish ? 'Step 1: Create Admin User' : '步骤 1：创建管理员用户'}\n`);
    
    // Step 1: Username
    const username = (await prompt(rl, isEnglish ? 'Enter admin username [admin]: ' : '输入管理员用户名 [admin]: ')) || 'admin';
    
    // Step 2: Password
    let password;
    while (true) {
      password = await prompt(rl, isEnglish ? 'Enter passphrase: ' : '输入口令: ', true);
      const errors = validatePassword(password);
      if (errors.length === 0) break;
      console.log(isEnglish ? '❌ Password does not meet requirements:' : '❌ 口令不符合要求:');
      errors.forEach(e => console.log(`   - ${e}`));
    }
    
    const confirm = await prompt(rl, isEnglish ? 'Confirm passphrase: ' : '确认口令: ', true);
    if (password !== confirm) {
      console.log(isEnglish ? '\n❌ Passphrases do not match.\n' : '\n❌ 口令不匹配。\n');
      rl.close();
      return;
    }
    
    const passwordHash = await bcrypt.hash(password, 12);
    console.log(isEnglish ? '✅ Passphrase accepted (bcrypt hashed)\n' : '✅ 口令已接受（bcrypt 加密）\n');
    
    // Step 3: Security Email (REQUIRED)
    console.log(isEnglish ? '\nStep 2: Security Email (Required for Recovery)' : '\n步骤 2：安全邮箱（恢复必需）');
    console.log(isEnglish 
      ? '   Recovery codes will be sent to this email if you forget your password.\n'
      : '   忘记口令时，恢复码将发送到此邮箱。\n');
    
    let email;
    while (true) {
      email = await prompt(rl, isEnglish ? 'Enter security email: ' : '输入安全邮箱: ');
      if (!email) {
        console.log(isEnglish ? '❌ Email is required for account recovery.' : '❌ 安全邮箱是账户恢复的必需项。');
        continue;
      }
      if (!validateEmail(email)) {
        console.log(isEnglish ? '❌ Invalid email format.' : '❌ 邮箱格式无效。');
        continue;
      }
      break;
    }
    console.log(`✅ ${isEnglish ? 'Recovery email' : '安全邮箱'}: ${email}\n`);
    
    // Step 4: Security question (optional)
    console.log(isEnglish ? 'Step 3: Security Question (Optional)' : '步骤 3：安全问题（可选）');
    const useSecurity = await prompt(rl, isEnglish ? 'Set up security question? (y/n) [n]: ' : '设置安全问题？(y/n) [n]: ');
    let securityQuestion = null;
    let securityAnswerHash = null;
    
    if (useSecurity.toLowerCase() === 'y') {
      securityQuestion = await prompt(rl, isEnglish ? 'Enter security question: ' : '输入安全问题: ');
      const answer = await prompt(rl, isEnglish ? 'Enter answer: ' : '输入答案: ');
      securityAnswerHash = crypto.createHash('sha256').update(answer).digest('hex');
      console.log(isEnglish ? '✅ Security question configured\n' : '✅ 安全问题已配置\n');
    } else {
      console.log();
    }
    
    // Step 5: Settings
    console.log(isEnglish ? 'Step 4: Settings' : '步骤 4：设置');
    const timeoutInput = await prompt(rl, isEnglish ? 'Idle timeout in minutes (default 60): ' : '闲置超时分钟数（默认 60）: ');
    const timeoutMinutes = parseInt(timeoutInput) || 60;
    const timeoutMs = timeoutMinutes * 60 * 1000;
    
    console.log(`\n${isEnglish ? 'Auto-reset options:' : '自动重置选项：'}`);
    console.log(isEnglish ? '  1. None (disabled)' : '  1. 无（禁用）');
    console.log(isEnglish ? '  2. /new - Start fresh session after auth' : '  2. /new - 认证后开始新会话');
    console.log(isEnglish ? '  3. /reset - Reset session after auth' : '  3. /reset - 认证后重置会话');
    const autoResetInput = await prompt(rl, isEnglish ? 'Choose auto-reset option [1-3, default 2]: ' : '选择自动重置选项 [1-3, 默认 2]: ');
    
    let autoReset = '/new';
    if (autoResetInput === '1') autoReset = null;
    else if (autoResetInput === '3') autoReset = '/reset';
    
    // Save configuration
    const config = {
      enabled: true,
      language: language,
      timeoutMs: timeoutMs,
      autoReset: autoReset,
      maxFailedAttempts: 5,
      lockoutDurationMs: 900000,
      passwordMinLength: 12,
      passwordRequiresUppercase: true,
      passwordRequiresLowercase: true,
      passwordRequiresDigit: true,
      passwordRequiresSpecial: true,
      auditLog: true,
      recoveryEnabled: true,
      emailRequired: true,
      createdAt: new Date().toISOString()
    };
    
    const users = {
      users: {
        [username]: {
          passphraseHash: passwordHash,
          hashAlgorithm: 'bcrypt',
          securityQuestion: securityQuestion,
          securityAnswerHash: securityAnswerHash,
          email: email,
          recoveryCodes: [],
          pendingRecovery: null,
          createdAt: new Date().toISOString(),
          lastLoginAt: null
        }
      }
    };
    
    saveJson(CONFIG_FILE, config);
    saveJson(USERS_FILE, users);
    
    // Initialize audit log
    const timestamp = new Date().toISOString();
    fs.writeFileSync(AUDIT_FILE, `[${timestamp}] SETUP: {"adminUser":"${username}","email":"${email}"}\n`);
    fs.chmodSync(AUDIT_FILE, 0o600);
    
    console.log(`\n✅ ${isEnglish ? 'Setup complete!' : '设置完成！'}\n`);
    console.log(isEnglish ? 'Configuration saved to:' : '配置已保存至：');
    console.log(`  - ${CONFIG_FILE}`);
    console.log(`  - ${USERS_FILE}`);
    console.log(`\n${isEnglish ? 'Settings:' : '设置：'}`);
    console.log(`  - ${isEnglish ? 'Timeout' : '超时'}: ${timeoutMinutes} ${isEnglish ? 'minutes' : '分钟'}`);
    console.log(`  - ${isEnglish ? 'Auto-reset' : '自动重置'}: ${autoReset || (isEnglish ? 'disabled' : '已禁用')}`);
    console.log(`  - ${isEnglish ? 'Security question' : '安全问题'}: ${securityQuestion ? (isEnglish ? 'enabled' : '已启用') : (isEnglish ? 'disabled' : '已禁用')}`);
    console.log(`  - ${isEnglish ? 'Recovery email' : '安全邮箱'}: ${email}`);
    
    console.log(`\n📧 ${isEnglish ? 'Recovery: If you forget your password, request a recovery code and it will be sent to your email.' : '恢复：忘记口令时，请求恢复码将发送到您的邮箱。'}`);
    console.log();
    
  } finally {
    rl.close();
  }
}

// Run setup
setup().catch(console.error);
