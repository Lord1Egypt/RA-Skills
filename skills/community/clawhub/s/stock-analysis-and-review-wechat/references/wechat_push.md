# 微信推送集成指南

## 概述

股市复盘结果可以通过微信推送给用户。本指南说明如何正确配置微信推送，避免常见错误。

## 前置检查

### 1. 微信插件版本检查

在执行微信推送前，**必须**先检查微信插件版本：

```bash
# 检查OpenClaw和插件版本
openclaw status

# 检查微信插件配置
openclaw config get openclaw-weixin
```

**最低版本要求**:
- OpenClaw: >= 2026.3.x
- 微信插件: >= 1.0.x

**如果版本过低，提醒用户更新**:
```
⚠️ 检测到微信插件版本较低，建议更新以获得更好的推送体验。
更新命令: pnpm update -g openclaw
```

### 2. 微信账号配置检查

确保以下配置正确：

```yaml
# ~/.openclaw/config.yaml
openclaw-weixin:
  enabled: true
  # 其他配置...
```

## 推送方式选择

### 方式一：Delivery推送（推荐）

适用于定时任务自动推送，简洁可靠。

**配置示例**:
```yaml
# cron任务配置
delivery:
  mode: announce
  channel: openclaw-weixin
  to: "{user_id}@im.wechat"
  accountId: "{account_id}"
```

**优点**:
- 配置简单
- 自动触发
- 稳定可靠

**注意事项**:
- `to` 必须填写用户的微信ID（格式：`xxx@im.wechat`）
- `accountId` 必须填写当前机器人账号ID
- 缺少任一参数都会导致推送失败

### 方式二：Message工具推送

适用于临时推送或需要复杂格式的场景。

**使用示例**:
```json
{
  "action": "send",
  "channel": "openclaw-weixin",
  "to": "user_id@im.wechat",
  "message": "📊 收盘复盘报告..."
}
```

**优点**:
- 格式灵活
- 支持富文本
- 可随时调用

**注意事项**:
- 调用前确认用户已授权
- 长消息可能被截断，建议分页发送

## 复盘报告推送最佳实践

### 标准推送流程

```python
def push_review_report(report_content, user_config):
    """
    推送复盘报告
    
    Args:
        report_content: 报告内容（Markdown格式）
        user_config: 用户配置 {user_id, account_id}
    """
    
    # 1. 检查微信插件版本
    version_ok = check_wechat_plugin_version()
    if not version_ok:
        print("⚠️ 微信插件版本较低，建议更新")
    
    # 2. 检查必要参数
    if not user_config.get('user_id') or not user_config.get('account_id'):
        raise ValueError("缺少必要的用户ID或账号ID")
    
    # 3. 格式化报告（适配微信）
    formatted_report = format_for_wechat(report_content)
    
    # 4. 发送报告
    # 方式A: 通过message工具
    message.send(
        action="send",
        channel="openclaw-weixin",
        to=f"{user_config['user_id']}@im.wechat",
        accountId=user_config['account_id'],
        message=formatted_report
    )
```

### 报告格式化

**适配微信的格式调整**:

1. **表格转换**: 微信中Markdown表格会被截断，转换为竖排文本列表
   
   **❌ 不推荐（表格会被截断）**:
   ```markdown
   | 标的 | 数量 | 成本 | 现价 | 盈亏 | 收益率 |
   |------|------|------|------|------|--------|
   | 电池ETF | 15,200 | ¥0.95 | ¥1.05 | +¥1,594 | +11.1% |
   | 江苏银行 | 700 | ¥8.99 | ¥10.82 | +¥1,278 | +20.2% |
   ```
   
   **✅ 推荐（竖排展示，无需滑动）**:
   ```markdown
   **💼 持仓概览**
   
   🔋 **电池ETF** | 15,200份 | **+11.1%** (+¥1,594)
   ├─ 成本¥0.946 → 现价¥1.051
   └─ 今日+2.54% 📈
   
   🏦 **江苏银行** | 700股 | **+20.2%** (+¥1,278)
   ├─ 成本¥8.99 → 现价¥10.82
   └─ 距止盈¥11.50还差6.3%
   
   📊 **汇总**: 市值¥64,213 | 总盈亏+¥4,685 (+7.87%)
   ```

2. **格式优化技巧**:
   - **使用树形符号**：├─ └─ 让层次清晰
   - **一行一个关键数据**：避免一行超过20个汉字
   - **emoji前置**：用图标区分不同标的
   - **汇总信息独立成行**：方便快速查看整体盈亏

3. **表情符号**: 使用微信支持的emoji
   - ✅ 支持：📈 📉 🎯 🚨 💡 🔋 🏦 📊
   - ❌ 避免：复杂Unicode字符、特殊边框符号

4. **消息长度**: 单条消息不超过2000字
   - 超过则分页发送
   - 重要内容放前面

### 定时任务配置示例

```bash
# 1. 创建收盘复盘任务
openclaw cron add \
  --name stock-daily-review \
  --cron "5 15 * * 1-5" \
  --agent main \
  --message "执行收盘复盘并微信推送：
    1. 获取大盘数据
    2. 计算持仓盈亏
    3. 评估建仓标的
    4. 生成报告
    5. 微信推送报告给用户" \
  --description "工作日收盘后复盘并推送"

# 2. 任务中配置delivery（在代码中实现）
```

**代码中的delivery配置**:
```python
# 在复盘脚本中添加
delivery_config = {
    "mode": "announce",
    "channel": "openclaw-weixin",
    "to": f"{user_id}@im.wechat",
    "accountId": account_id
}

# 生成报告后自动触发推送
```

## 常见问题

### Q1: 微信推送失败

**可能原因**:
1. 用户未授权微信插件
2. user_id 或 account_id 错误
3. 微信插件版本过低
4. 网络问题

**排查步骤**:
```bash
# 1. 检查授权状态
openclaw weixin status

# 2. 检查配置
openclaw config get openclaw-weixin

# 3. 测试发送
openclaw weixin send --to "user_id" --message "测试消息"
```

### Q2: 消息格式错乱

**解决**: 
- 使用微信支持的简单Markdown
- 避免复杂表格，改用列表
- 测试发送前先在本地预览

### Q3: 定时任务没有推送

**检查**:
1. cron表达式是否正确
2. delivery配置是否完整
3. 任务是否启用

```bash
# 查看定时任务列表
openclaw cron list

# 查看任务日志
openclaw cron logs stock-daily-review
```

## 完整推送示例代码

```python
#!/usr/bin/env python3
"""
股市复盘报告微信推送模块
"""

import json
from datetime import datetime

def check_wechat_version():
    """检查微信插件版本"""
    # 实际实现中调用 openclaw status
    return {"ok": True, "version": "1.2.3"}

def format_report_for_wechat(report_md):
    """将Markdown报告格式化为微信友好格式"""
    
    # 简化表格
    lines = report_md.split('\n')
    formatted = []
    
    for line in lines:
        # 跳过Markdown表格分隔线
        if line.startswith('|') and '---' in line:
            continue
        # 转换表格行为列表
        if line.startswith('|') and not '标的' in line:
            parts = [p.strip() for p in line.split('|')[1:-1]]
            if len(parts) >= 3:
                formatted.append(f"• {parts[0]}: {parts[2]} {parts[3] if len(parts) > 3 else ''}")
        else:
            formatted.append(line)
    
    return '\n'.join(formatted)

def push_to_wechat(report, user_id, account_id):
    """
    推送报告到微信
    
    Args:
        report: 报告内容
        user_id: 用户微信ID
        account_id: 机器人账号ID
    """
    
    # 检查版本
    version_info = check_wechat_version()
    if not version_info.get('ok'):
        print(f"⚠️ 微信插件检查失败: {version_info}")
        return False
    
    # 格式化
    formatted = format_report_for_wechat(report)
    
    # 添加推送配置到输出（供OpenClaw解析）
    delivery = {
        "mode": "announce",
        "channel": "openclaw-weixin",
        "to": f"{user_id}@im.wechat",
        "accountId": account_id
    }
    
    # 输出报告和delivery配置
    print("=== REPORT START ===")
    print(formatted)
    print("=== REPORT END ===")
    print(f"DELIVERY: {json.dumps(delivery)}")
    
    return True

if __name__ == "__main__":
    # 示例
    sample_report = """
# 2026-04-11 收盘复盘

| 标的 | 价格 | 涨跌 |
|------|------|------|
| 江苏银行 | ¥10.78 | +1% |
| 电池ETF | ¥1.00 | +2% |

今日盈利: +¥500
"""
    
    push_to_wechat(sample_report, "user_xxx", "account_xxx")
```

## 更新记录

- 2026-04-11: 初始版本，总结微信推送最佳实践
