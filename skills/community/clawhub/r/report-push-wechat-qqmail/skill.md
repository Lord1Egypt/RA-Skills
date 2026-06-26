---
name: report-push-wechat-qqmail
description: "将分析报告智能摘要推送到微信(≤100字任务清单)+全文推送到QQ邮箱,说'推送报告'时触发"
user-invocable: true
metadata:
  openclaw:
    emoji: "📨"
    skillKey: "report-push-wechat-qqmail"
    requires:
      bins:
        - python3
      env:
        - QQ_MAIL_ACCOUNT
        - QQ_MAIL_AUTH_CODE
        - TARGET_QQ_MAIL
        - WECHAT_PUSH_KEY
      os:
        - macos
        - linux
        - windows
    install:
      - id: "requests"
        kind: "command"
        command: "pip3 install requests"
        bins: ["python3"]
        label: "Install requests library"
---

# 报告双通道智能推送 — 微信摘要 & 邮件全文

将分析报告（股票、科技、研究等）**差异化推送**到两个通道：
- **微信** → 由 Agent 提炼的 ≤100字 结构化任务清单/重要提示
- **QQ邮箱** → 完整原文（Markdown/纯文本）

内置合规过滤、频率限流、推送去重机制，确保安全高效。

## Use When
- 用户要求将分析报告推送/发送到微信或QQ邮箱
- 用户说"发送报告""推送结果""通知我""把报告发给我"
- 上游 Skill 生成报告后需要分发通知
- 用户明确要求"推送到微信""发到邮箱"

## Do NOT Use When
- 用户只是要求**生成**报告，但未要求推送
- 用户要求发送到钉钉、飞书、Telegram 等非微信/QQ邮箱渠道
- 推送内容包含明显违规信息（色情、暴力、赌博、政治敏感等）
- 同一报告在 5 分钟内已推送过（防重复）

## Prerequisites
1. **QQ邮箱 SMTP 配置**
   - `QQ_MAIL_ACCOUNT`：发件人QQ邮箱地址（如 `123456@qq.com`）
   - `QQ_MAIL_AUTH_CODE`：QQ邮箱 SMTP 授权码
     > ⚠️ 非QQ登录密码！获取路径：QQ邮箱 → 设置 → 账户 → POP3/SMTP服务 → 生成授权码
   - `TARGET_QQ_MAIL`：收件人QQ邮箱地址

2. **微信推送配置**
   - `WECHAT_PUSH_KEY`：推送服务 Token
     > 支持 Server酱（`SCT` 开头）或 PushPlus（32位字符串）

3. **运行环境**
   - Python 3.7+
   - `requests` 库：`pip3 install requests`

## Instructions

### 第一步：接收报告内容
获取用户提供的报告全文及标题。如用户未提供标题，从报告首行或内容摘要生成标题。

### 第二步：合规预检（你必须执行）
在推送前检查报告内容，如果包含以下内容则**拒绝推送并告知用户**：
- 色情、暴力、恐怖、赌博相关内容
- 明确的政治敏感信息
- 欺诈、虚假、不实或引人误解的信息
- 他人隐私数据（身份证号、手机号、银行卡号等）

如果内容合规，继续下一步。

### 第三步：生成微信摘要（你必须执行，不交给脚本）
你需要将报告全文提炼为**不超过100字**的结构化摘要，严格遵循以下模板：

📊 {报告标题}
▸ 结论：{一句话核心结论}
▸ 待办：{1-3条关键行动项}
▸ ⚠️ {一条风险/重要提示}

示例：
📊 贵州茅台Q3分析
▸ 结论：营收同比+15%，净利润超预期
▸ 待办：①关注Q4产能释放 ②12月股东大会
▸ ⚠️ 注意海外市场汇率波动风险

**硬性要求**：摘要总字符数（含标点符号和emoji）≤ 100 字。超过则精简。

### 第四步：调用推送脚本
```bash
python3 {baseDir}/scripts/push_report.py \
  --title "报告标题" \
  --summary "第三步生成的微信摘要(≤100字)" \
  --content "完整报告原文" \
  --channel both

参数说明：
--title：报告标题
--summary：微信端推送内容（≤100字结构化摘要）
--content：邮件端推送内容（完整原文）
--channel：both|wechat|email（默认 both）

第五步：解析并反馈
脚本返回 JSON 结果，据此向用户清晰报告：
✅ 各通道推送状态
⚠️ 如有合规过滤，说明过滤原因

basic

#### 2. 创建 `requirements.txt`
在 `report-pusher` 根目录下新建此文件，填入：
```text
requests==2.31.0
