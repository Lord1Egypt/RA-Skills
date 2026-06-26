const nodemailer = require('nodemailer');
const fs = require('fs');
const path = require('path');

const config = require('./smtp.json');

// 解析命令行参数
const args = process.argv.slice(2);
let to = '', cc = '', template = '', varsJson = '';

for (let i = 0; i < args.length; i++) {
  if (args[i] === '--to' && args[i + 1]) { to = args[++i]; }
  else if (args[i] === '--cc' && args[i + 1]) { cc = args[++i]; }
  else if (args[i] === '--template' && args[i + 1]) { template = args[++i]; }
  else if (args[i] === '--vars' && args[i + 1]) { varsJson = args[++i]; }
}

if (!to || !template) {
  console.error('用法：node send-template-email.js --to <邮箱> --template <模板名> [--cc <抄送>] --vars \'{...}\'');
  process.exit(1);
}

const vars = JSON.parse(varsJson);

// 读取模板
const templatePath = path.join(__dirname, 'email-templates', `${template}.md`);
const templateContent = fs.readFileSync(templatePath, 'utf-8');

// 提取 HTML 和纯文本部分
const htmlMatch = templateContent.match(/### 正文 \(HTML\)\s*\n```html([\s\S]*?)```/);
const textMatch = templateContent.match(/### 正文 \(纯文本\)\s*\n```([\s\S]*?)```/);

if (!htmlMatch || !textMatch) {
  console.error('模板格式错误，找不到 HTML 或纯文本部分');
  process.exit(1);
}

let htmlContent = htmlMatch[1].trim();
let textContent = textMatch[1].trim();

// 替换变量
Object.keys(vars).forEach(key => {
  const regex = new RegExp(`{{${key}}}`, 'g');
  htmlContent = htmlContent.replace(regex, vars[key]);
  textContent = textContent.replace(regex, vars[key]);
});

async function sendEmail() {
  try {
    console.log('📧 发送模板邮件...');
    console.log(`收件人：${to}`);
    if (cc) console.log(`抄送：${cc}`);
    
    const transporter = nodemailer.createTransport({
      host: config.host,
      port: config.port,
      secure: config.secure,
      auth: config.auth,
      tls: config.tls
    });
    
    const mailOptions = {
      from: `"${config.from.name}" <${config.from.email}>`,
      to: to,
      subject: `【Remnawave】账号已创建 - 运维组 Crads`,
      text: textContent,
      html: htmlContent
    };
    
    if (cc) {
      mailOptions.cc = cc;
    }
    
    const info = await transporter.sendMail(mailOptions);
    
    console.log('✅ 发送成功!');
    console.log('Message ID:', info.messageId);
    
    process.exit(0);
  } catch (error) {
    console.error('❌ 发送失败:', error.message);
    console.error(error);
    process.exit(1);
  }
}

sendEmail();
