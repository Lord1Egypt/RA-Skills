---
name: zhipin-phone-extractor
description: Automatically extract phone numbers from BOSS直聘 (zhipin.com) chat messages. Use when: (1) User needs to collect phone numbers from recruiter messages, (2) User wants to batch extract contact info from BOSS直聘, (3) User mentions "BOSS直聘", "zhipin", "提取手机号", "招聘消息", "猎聘" (job hunting context).
---

# BOSS直聘手机号提取器

从 BOSS直聘 (zhipin.com) 的聊天消息中自动提取手机号，帮助求职者快速收集 HR 联系方式。

## 快速开始

### 前置条件
- 已登录 BOSS直聘网页版（需要先手动登录一次）
- 浏览器自动化工具（Playwright）

### 基本使用

```bash
# 提取所有新消息中的手机号
python scripts/extract_phones.py

# 提取并保存到指定文件
python scripts/extract_phones.py --output ~/Desktop/phones.txt
```

## 工作流程

### 1. 检测新消息
- 打开浏览器访问 zhipin.com
- 导航到消息页面
- 识别未读消息（红点标记）

### 2. 提取手机号
- 遍历每条新消息
- 使用正则表达式匹配手机号：`1[3-9]\d{9}`
- 去重并验证格式

### 3. 保存结果
- 默认保存到 `~/Desktop/猎聘手机号记录.txt`
- 追加模式，不覆盖已有数据
- 格式：`姓名 - 手机号 - 提取时间`

## 使用场景

### 场景 1: 批量收集 HR 联系方式
```
用户: 帮我提取 BOSS直聘上所有新消息里的手机号
→ 执行脚本，自动打开浏览器，提取所有手机号
```

### 场景 2: 定期检查新消息
```
用户: 检查一下猎聘有没有新的手机号
→ 执行脚本，只提取新增的手机号
```

### 场景 3: 导出到指定位置
```
用户: 把 BOSS直聘的手机号导出到我的工作目录
→ python scripts/extract_phones.py --output ~/workspace/contacts.txt
```

## 注意事项

1. **登录状态**：首次使用需要手动登录 BOSS直聘，之后会保持登录状态
2. **频率限制**：避免频繁请求，建议间隔 5-10 分钟
3. **隐私保护**：提取的手机号仅保存在本地，不会上传到任何服务器
4. **反爬机制**：如遇验证码，需要手动处理

## 脚本说明

### scripts/extract_phones.py
主脚本，负责：
- 启动浏览器（使用 Playwright）
- 导航到消息页面
- 提取手机号
- 保存到文件

### 参数说明
- `--output`: 指定输出文件路径（默认：`~/Desktop/猎聘手机号记录.txt`）
- `--headless`: 无头模式运行（不显示浏览器窗口）
- `--limit`: 限制提取的消息数量

## 故障排查

### 问题 1: 浏览器无法启动
```bash
# 安装 Playwright 浏览器
playwright install chromium
```

### 问题 2: 登录失效
- 手动打开浏览器访问 zhipin.com
- 重新登录
- 再次运行脚本

### 问题 3: 提取不到手机号
- 检查消息中是否真的包含手机号
- 部分手机号可能以图片形式发送（需要 OCR 支持）

## 输出示例

```
=== BOSS直聘手机号提取报告 ===
时间: 2026-03-11 14:44:00
新消息数: 5
提取手机号: 3

1. 张经理 - 13800138000 - 腾讯科技
2. 李HR - 13900139000 - 字节跳动
3. 王总 - 13700137000 - 阿里巴巴

已保存到: ~/Desktop/猎聘手机号记录.txt
```

## 扩展功能

### 配合心跳自动检查
可以将此脚本集成到 HEARTBEAT.md 中，定期自动检查新消息：

```json
{
  "lastChecks": {
    "zhipin": "2026-03-11T14:44:00+08:00"
  }
}
```

### 与其他平台集成
参考此脚本，可以扩展支持：
- 猎聘 (liepin.com)
- 智联招聘 (zhaopin.com)
- 拉勾 (lagou.com)
