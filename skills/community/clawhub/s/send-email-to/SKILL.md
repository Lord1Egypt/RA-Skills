---
name: send-email-to
description: >
  发送邮件，支持中文附件（RFC 2231 编码）。
  当用户说"发送邮件"、"发送报告"、"发送日报"时触发。
---

# 发送邮件 Skill

执行脚本：`send-email-to/scripts/send_email.py`

## 功能

- 读取 `market_data.json` 中的市场数据，生成摘要正文
- 自动查找 `E:\daily\{date}\` 下的 Word 和 PPT 附件
- 中文文件名使用 RFC 2231 编码，防止邮件客户端显示为 `.bin`
- 附件 Content-Type 设置为正确的 Office 文档类型

## 脚本逻辑

1. 读取 `market_data.json`（由 collect-market-data 生成）
2. 查找当日 `*_YYYYMMDD.docx` 和 `*_YYYYMMDD.pptx` 文件
3. 构建带摘要正文的邮件，附件使用 RFC 2231 编码
4. 通过 SMTP 发送至 yugi.chong@fubonchina.com

## 邮件配置（来自 config.py）

| 配置项 | 值 |
|--------|-----|
| SMTP 服务器 | smtp.163.com |
| SMTP 端口 | 25 |
| 发件人 | 13045609072@163.com |
| 收件人 | yugi.chong@fubonchina.com |
| 授权码 | MN3dS36RDsLcyFTb |
