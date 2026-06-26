// imap-smtp-email/scripts/smtp-wrapper.js
/**
 * SMTP 发送邮件包装器
 * 封装 smtp.js 的功能，供其他模块调用
 */

const { execSync } = require('child_process');
const path = require('path');

const SMTP_SCRIPT = path.join(__dirname, 'smtp.js');

/**
 * 发送邮件
 * @param {object} options - 邮件选项
 * @param {string} options.to - 收件人
 * @param {string} options.subject - 主题
 * @param {string} options.body - 纯文本正文
 * @param {string} options.html - HTML 正文
 * @param {string} options.attach - 附件路径（逗号分隔）
 * @returns {object} 发送结果
 */
function sendEmail(options) {
  const args = ['node', SMTP_SCRIPT, 'send'];
  
  if (options.to) {
    args.push('--to', options.to);
  }
  if (options.subject) {
    args.push('--subject', options.subject);
  }
  if (options.html) {
    args.push('--html');
    args.push('--body', options.html);
  } else if (options.body) {
    args.push('--body', options.body);
  }
  if (options.attach) {
    args.push('--attach', options.attach);
  }
  if (options.cc) {
    args.push('--cc', options.cc);
  }

  try {
    const output = execSync(args.join(' '), { encoding: 'utf-8' });
    return {
      success: true,
      output: output
    };
  } catch (error) {
    return {
      success: false,
      error: error.message
    };
  }
}

module.exports = {
  sendEmail
};
