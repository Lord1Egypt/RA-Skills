# 合规处置工具 (Sensitive Disposal) — 免费版

> 敏感内容扫描后的合规处置解决方案 —— **免费使用**

---

## 🎯 功能特点

| 处置方式 | 说明 | 支持格式 |
:|----------|------|----------|
| 🔒 **脱敏处理** | 部分替换/关键字替换/正则替换 | txt, md, json, xml, docx, xlsx, pptx, **pdf** |
| 🔐 **文件加密** | 密码保护 + 飞书/微信通知 | 所有格式 |

---

## 🚀 快速开始

### 安装依赖

```bash
pip install python-docx openpyxl python-pptx PyMuPDF requests
```

### 基本用法

```bash
# 脱敏处理（部分替换）
python disposal.py document.txt --action redact --strategy partial

# 脱敏处理（关键字替换）
python disposal.py document.txt --action redact --strategy keyword -k "密码,密钥"

# 文件加密
python disposal.py document.txt --action encrypt --password "YourPassword"
```

---

## 📋 三种脱敏粒度

### 1. 部分替换（默认）
```
原始: 13812345678 → 脱敏: 1*********8
原始: 身份证110101199001011234 → 脱敏: 110101********1234
```

### 2. 关键字替换
```
原始: 密码: admin123 → 脱敏: 密码: [REDACTED]
原始: 密钥: sk-xxx → 脱敏: 密钥: [REDACTED]
```

### 3. 正则替换
```
自定义正则规则，替换匹配的中间部分
```

---

## 💾 保存方式

| 参数 | 说明 |
|------|------|
| `--output path` | 指定输出文件路径 |
| `--overwrite` | 覆盖原文件（谨慎使用） |
| （默认） | 自动生成 `原文件名_脱敏版.xxx` 或 `原文件名_加密版.xxx` |

---

## 📢 通知功能

### 配置 Webhook

```bash
# 飞书通知
python disposal.py document.txt --action encrypt --password "xxx" \
  --feishu-webhook "https://open.feishu.cn/open-apis/bot/v2/hook/xxx"

# 企业微信通知
python disposal.py document.txt --action encrypt --password "xxx" \
  --wecom-webhook "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxx"
```

### 配置文件

创建 `config.json`：

```json
{
  "feishu_webhook": "https://...",
  "wecom_webhook": "https://..."
}
```

然后使用：
```bash
python disposal.py document.txt --config config.json
```

---

## 📁 支持格式

| 类型 | 格式 | 脱敏 | 加密 |
:|------|------|:----:|:----:|
| 文本 | txt, md, json, xml, csv | ✅ | ✅ |
| Word | docx | ✅ | ✅ |
| Excel | xlsx | ✅ | ✅ |
| PPT | pptx | ✅ | ✅ |
| PDF | pdf | ✅ | ✅ |

---

## ⚙️ 完整参数

```
positional arguments:
  file                  要处理的文件路径

options:
  --action, -a          处置动作 (redact=脱敏 / encrypt=加密)
  --output, -o          输出文件路径
  --overwrite           覆盖原文件
  --strategy, -s        脱敏策略 (partial / keyword / regex)
  --keywords, -k         自定义关键词（逗号分隔）
  --password, -p        加密密码
  --notify, -n          通知渠道（feishu, wecom, email）
  --feishu-webhook      飞书Webhook地址
  --wecom-webhook       企业微信Webhook地址
  --config, -c          配置文件路径（JSON格式）
  --verbose, -v         详细输出
```

---

## 📚 相关项目

- 敏感内容扫描器 - 扫描发现敏感内容（配套使用）

---

**版本**: 1.2.0
**更新日期**: 2026-04-21
**定价**: 免费版
