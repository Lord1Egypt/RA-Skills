# 📧 VPN 账号开通通知

**模板 ID:** remnawave-account-created  
**用途:** Remnawave/VPN 账号创建成功后发送

---

## 📋 模板变量

| 变量 | 说明 | 示例 |
|------|------|------|
| `{{recipient_name}}` | 收件人姓名 | 张三 |
| `{{recipient_email}}` | 收件人邮箱 | zhangsan@company.com |
| `{{account_name}}` | VPN 账号名称 | user_001 |
| `{{subscription_url}}` | 订阅地址 | https://sub.example.com/xxx |
| `{{tutorial_url}}` | 安装教程 | https://... |
| `{{download_url}}` | VPN 客户端下载 (Windows) | https://v2raytun.com/ |
| `{{download_backup}}` | VPN 备用下载 (Windows) | https://...zip |
| `{{appstore_url}}` | VPN 客户端下载 (Mac/iOS) | https://apps.apple.com/... |
| `{{send_date}}` | 发送日期 | 2026-03-18 |

---

## 📧 邮件内容

### 主题
```
【VPN】账号已创建 - 运维组 Crads
```

### 正文 (HTML)
```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <style>
    body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
    .container { max-width: 600px; margin: 0 auto; padding: 20px; }
    .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 5px; margin-bottom: 20px; color: white; }
    .info-box { background: #f8f9fa; border-left: 4px solid #667eea; padding: 15px; margin: 15px 0; }
    .warning { background: #fff3cd; border-left: 4px solid #ffc107; padding: 15px; margin: 15px 0; }
    .success { background: #d4edda; border-left: 4px solid #28a745; padding: 15px; margin: 15px 0; }
    .footer { background: #f4f4f4; padding: 15px; border-radius: 5px; margin-top: 20px; font-size: 12px; color: #666; }
    a { color: #667eea; }
    .code { background: #f4f4f4; padding: 3px 8px; border-radius: 3px; font-family: 'Courier New', monospace; font-size: 12px; word-break: break-all; }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h2>🚀 VPN 账号已创建</h2>
      <p>您的 VPN 访问凭证已生成</p>
    </div>
    
    <p>尊敬的 {{recipient_name}}：</p>
    <p>您好！您的 VPN 账号已创建成功，以下是您的访问信息：</p>
    
    <div class="info-box">
      <h3>📚 VPN 账号信息</h3>
      <p><strong>安装教程：</strong><br>
      <a href="{{tutorial_url}}">{{tutorial_url}}</a></p>
      
      <p><strong>订阅地址：</strong><br>
      <span class="code">{{subscription_url}}</span></p>
      
      <p><strong>VPN 账号名称：</strong><br>
      <span class="code">{{account_name}}</span></p>
    </div>
    
    <div class="success">
      <h3>📥 VPN 客户端下载</h3>
      <p><strong>Windows 版（官方）：</strong><a href="{{download_url}}">{{download_url}}</a></p>
      <p><strong>Windows 版（备用）：</strong><a href="{{download_backup}}">{{download_backup}}</a></p>
      <p><strong>Mac/iOS 版：</strong><a href="{{appstore_url}}">{{appstore_url}}</a></p>
      <p><small>💡 如官方地址无法访问，请使用备用下载地址</small></p>
    </div>
    
    <div class="warning">
      <h3>⚠️ 重要提醒</h3>
      <p><strong>VPN 账号唯一，只允许单设备使用</strong></p>
    </div>
    
    <p>如遇问题，请联系运维组获取技术支持。</p>
    
    <div class="footer">
      <p><strong>运维组：</strong>Crads</p>
      <p><strong>发送时间：</strong>{{send_date}}</p>
      <p><em>此邮件由系统自动发送，请勿回复</em></p>
    </div>
  </div>
</body>
</html>
```

### 正文 (纯文本)
```
尊敬的 {{recipient_name}}：

您好！您的 VPN 账号已创建成功，以下是您的访问信息：

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📚 VPN 账号信息
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

安装教程：{{tutorial_url}}
订阅地址：{{subscription_url}}
VPN 账号名称：{{account_name}}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📥 VPN 客户端下载
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Windows 版（官方）：{{download_url}}
Windows 版（备用）：{{download_backup}}
Mac/iOS 版：{{appstore_url}}

💡 如官方地址无法访问，请使用备用下载地址

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ 重要提醒
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

VPN 账号唯一，只允许单设备使用

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

如遇问题，请联系运维组获取技术支持。

此致
运维组：Crads
发送时间：{{send_date}}

此邮件由系统自动发送，请勿回复
```

---

**标签:** #邮件模板 #VPN #账号开通
