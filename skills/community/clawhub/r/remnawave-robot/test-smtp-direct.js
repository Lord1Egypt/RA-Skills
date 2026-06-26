const nodemailer = require('nodemailer');
const config = require('./config/smtp.json');

async function testSmtp() {
  try {
    console.log('📧 测试邮件发送（直接复制旧脚本方式）...\n');
    console.log('SMTP 配置:');
    console.log(`  Host: ${config.host}:${config.port}`);
    console.log(`  User: ${config.auth.user}`);
    console.log(`  From: "${config.from.name}" <${config.from.email}>\n`);
    
    const transporter = nodemailer.createTransport({
      host: config.host,
      port: config.port,
      secure: config.secure,
      auth: config.auth,
      tls: config.tls
    });
    
    const mailOptions = {
      from: `"${config.from.name}" <${config.from.email}>`,
      to: 'jung@bydfi.com',
      cc: 'crads@codeforce.tech',
      subject: `【VPN】账号已创建 - 运维组 Crads`,
      text: '测试邮件',
      html: '<h1>测试邮件</h1><p>账号：jung_pc</p>'
    };
    
    console.log('📧 发送邮件...');
    const info = await transporter.sendMail(mailOptions);
    
    console.log('✅ 邮件发送成功!');
    console.log('Message ID:', info.messageId);
    
    process.exit(0);
  } catch (error) {
    console.error('❌ 邮件发送失败:', error.message);
    console.error('错误代码:', error.code);
    console.error('响应:', error.response);
    process.exit(1);
  }
}

testSmtp();
