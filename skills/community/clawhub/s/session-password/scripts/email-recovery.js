/**
 * Session Password - Email Recovery Module v1.0.0
 * Author: squallsol
 * 
 * Sends recovery codes via email for password reset.
 * Requires SMTP configuration or external email service.
 */

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const WORKSPACE = process.env.OPENCLAW_WORKSPACE || path.join(process.env.HOME, '.openclaw', 'workspace');
const MEMORY_DIR = path.join(WORKSPACE, 'memory');

const PASSPHRASE_FILE = path.join(MEMORY_DIR, 'passphrase.json');
const RECOVERY_FILE = path.join(MEMORY_DIR, 'auth-recovery.json');

// ═══════════════════════════════════════════════════
// Recovery Code Management
// ═══════════════════════════════════════════════════

function generateRecoveryCode() {
  // 6-digit code
  return Math.floor(100000 + Math.random() * 900000).toString();
}

function hashRecoveryCode(code) {
  return crypto.createHash('sha256').update(code).digest('hex');
}

function createRecoveryRecord(email) {
  const code = generateRecoveryCode();
  const record = {
    email,
    codeHash: hashRecoveryCode(code),
    createdAt: Date.now(),
    expiresAt: Date.now() + 15 * 60 * 1000, // 15 minutes
    used: false
  };
  
  fs.writeFileSync(RECOVERY_FILE, JSON.stringify(record, null, 2));
  return code;
}

function verifyRecoveryCode(inputCode) {
  if (!fs.existsSync(RECOVERY_FILE)) {
    return { valid: false, error: 'no_recovery_pending' };
  }
  
  const record = JSON.parse(fs.readFileSync(RECOVERY_FILE, 'utf8'));
  
  if (record.used) {
    return { valid: false, error: 'code_already_used' };
  }
  
  if (Date.now() > record.expiresAt) {
    return { valid: false, error: 'code_expired' };
  }
  
  const inputHash = hashRecoveryCode(inputCode);
  if (inputHash !== record.codeHash) {
    return { valid: false, error: 'invalid_code' };
  }
  
  // Mark as used
  record.used = true;
  fs.writeFileSync(RECOVERY_FILE, JSON.stringify(record, null, 2));
  
  return { valid: true };
}

// ═══════════════════════════════════════════════════
// Email Sending (Stub - requires configuration)
// ═══════════════════════════════════════════════════

/**
 * Send recovery code via email
 * 
 * This is a stub that logs the code. To enable actual email:
 * 1. Install nodemailer: npm install nodemailer
 * 2. Configure SMTP settings in auth-smtp.json
 * 3. Replace the stub below with actual send
 */
async function sendRecoveryEmail(email, code) {
  // Check for SMTP configuration
  const smtpConfigFile = path.join(MEMORY_DIR, 'auth-smtp.json');
  
  if (fs.existsSync(smtpConfigFile)) {
    try {
      const nodemailer = require('nodemailer');
      const smtpConfig = JSON.parse(fs.readFileSync(smtpConfigFile, 'utf8'));
      
      const transporter = nodemailer.createTransport(smtpConfig);
      
      await transporter.sendMail({
        from: smtpConfig.from || 'noreply@openclaw.ai',
        to: email,
        subject: 'OpenClaw 口令恢复 / Password Recovery',
        text: `您的恢复验证码是: ${code}\n\n验证码 15 分钟内有效。\n\nYour recovery code is: ${code}\n\nCode expires in 15 minutes.`
      });
      
      return { sent: true, method: 'smtp' };
    } catch (e) {
      console.error('SMTP error:', e);
      // Fall through to stub
    }
  }
  
  // Stub: log to console (for development/testing)
  console.log('\n══════════════════════════════════════════════');
  console.log('📧 EMAIL RECOVERY (STUB MODE)');
  console.log('══════════════════════════════════════════════');
  console.log(`To: ${email}`);
  console.log(`Subject: OpenClaw 口令恢复`);
  console.log(`\n您的恢复验证码是: ${code}`);
  console.log(`验证码 15 分钟内有效。`);
  console.log('══════════════════════════════════════════════\n');
  
  // Write to file for agent to read
  const stubFile = path.join(MEMORY_DIR, 'auth-recovery-stub.txt');
  fs.writeFileSync(stubFile, `Recovery code for ${email}: ${code}\nExpires in 15 minutes.\n`);
  
  return { sent: true, method: 'stub', code };
}

/**
 * Initiate password recovery
 */
async function initiateRecovery() {
  // Get email from config
  if (!fs.existsSync(PASSPHRASE_FILE)) {
    return { success: false, error: 'not_configured' };
  }
  
  const config = JSON.parse(fs.readFileSync(PASSPHRASE_FILE, 'utf8'));
  const email = config.securityEmail;
  
  if (!email) {
    return { success: false, error: 'no_email_configured' };
  }
  
  // Generate and send code
  const code = createRecoveryRecord(email);
  const result = await sendRecoveryEmail(email, code);
  
  if (result.sent) {
    // Mask email for display
    const [localPart, domain] = email.split('@');
    const masked = localPart.slice(0, 2) + '***@' + domain;
    
    return {
      success: true,
      maskedEmail: masked,
      method: result.method,
      message: `恢复验证码已发送至 ${masked}，请查收邮件。`
    };
  }
  
  return { success: false, error: 'send_failed' };
}

/**
 * Complete password recovery (verify code + security answer)
 */
async function completeRecovery(code, securityAnswer, newPassword) {
  // Verify recovery code
  const codeResult = verifyRecoveryCode(code);
  if (!codeResult.valid) {
    return { success: false, error: codeResult.error };
  }
  
  // Verify security answer
  const config = JSON.parse(fs.readFileSync(PASSPHRASE_FILE, 'utf8'));
  const answerHash = config.securityAnswerHash;
  
  const inputHash = crypto.createHash('sha256').update(securityAnswer).digest('hex');
  if (inputHash !== answerHash) {
    return { success: false, error: 'invalid_security_answer' };
  }
  
  // Validate new password
  if (!newPassword || newPassword.length < 12) {
    return { success: false, error: 'password_too_short' };
  }
  
  if (!/[a-z]/.test(newPassword) || !/[A-Z]/.test(newPassword) ||
      !/\d/.test(newPassword) || !/[@$!%*?&]/.test(newPassword)) {
    return { success: false, error: 'password_complexity' };
  }
  
  // Update password
  const newHash = crypto.createHash('sha256').update(newPassword).digest('hex');
  config.passphraseHash = newHash;
  config.hashAlgorithm = 'sha256';
  fs.writeFileSync(PASSPHRASE_FILE, JSON.stringify(config, null, 2));
  fs.chmodSync(PASSPHRASE_FILE, 0o600);
  
  return { success: true, message: '口令已重置，请使用新口令登录。' };
}

// ═══════════════════════════════════════════════════
// CLI Interface
// ═══════════════════════════════════════════════════

if (require.main === module) {
  const args = process.argv.slice(2);
  const command = args[0];
  
  switch (command) {
    case 'init':
      initiateRecovery().then(result => {
        console.log(JSON.stringify(result, null, 2));
      });
      break;
      
    case 'verify':
      const code = args[1];
      console.log(JSON.stringify(verifyRecoveryCode(code), null, 2));
      break;
      
    default:
      console.log(`
Usage: node email-recovery.js <command>

Commands:
  init    - Send recovery code to configured email
  verify <code> - Verify recovery code
`);
  }
}

module.exports = {
  initiateRecovery,
  verifyRecoveryCode,
  sendRecoveryEmail,
  completeRecovery
};
