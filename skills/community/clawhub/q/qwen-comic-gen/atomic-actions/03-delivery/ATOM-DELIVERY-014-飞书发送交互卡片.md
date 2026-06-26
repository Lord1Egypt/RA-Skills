# ATOM-DELIVERY-014 - 飞书发送交互卡片

> 版本：V1.0  
> 状态：🟡 待规范  
> 最后更新：2026-03-07

---

## 📋 动作定义

**名称：** 飞书发送交互卡片  
**分类：** 交付层（Delivery Layer）  
**编号：** ATOM-DELIVERY-014

**一句话描述：** 发送带按钮的交互式卡片消息到飞书

---

## 🎯 输入输出

### 输入
- **类型：** 卡片 JSON + 按钮配置
- **内容：** 交互卡片结构

### 输出
- **类型：** 飞书消息（interactive 类型）
- **返回：** messageId

---

## ⚙️ 偏好设置

### 卡片类型
- **msg_type：** interactive
- **wide_screen_mode：** true（宽屏模式）

### 按钮配置
| 字段 | 说明 | 示例 |
|------|------|------|
| tag | 按钮类型 | button |
| text | 按钮文字 | "点击查看" |
| type | 动作类型 | url/default |
| url | 跳转链接 | https://... |

### 卡片布局
- **标题：** 简洁明了
- **内容：** 结构化（列表/表格）
- **按钮：** 1-3 个（不要过多）

---

## 📝 操作步骤

```powershell
# 1. 设计卡片 JSON
$card = @{
    config = @{
        wide_screen_mode = $true
    }
    header = @{
        title = @{
            tag = "plain_text"
            content = "🎯 优先级提醒"
        }
    }
    elements = @(
        @{
            tag = "div"
            text = @{
                tag = "lark_md"
                content = "当前最优先任务：**飞书 OAuth 配置**"
            }
        },
        @{
            tag = "action"
            actions = @(
                @{
                    tag = "button"
                    text = @{
                        tag = "plain_text"
                        content = "查看详情"
                    }
                    type = "primary"
                }
            )
        }
    )
} | ConvertTo-Json -Depth 10

# 2. 发送飞书
Invoke-MessageSend `
    -Action "send" `
    -MessageType "interactive" `
    -Card $card `
    -Target "ou_e3a0d4a64a9e0932ee919b97f17ec210"

# 3. 确认
Write-Host "✅ 交互卡片已发送"
```

---

## 🔄 使用场景

### 场景 1：优先级提醒（交互式）
```
触发：每小时 Cron 任务
  ↓
调用：ATOM-DELIVERY-014
  ↓
输出：带按钮的优先级卡片
```

### 场景 2：任务确认
```
触发：任务完成需要确认
  ↓
调用：ATOM-DELIVERY-014
  ↓
输出：带"确认"按钮的卡片
```

---

## 🔗 关联动作

### 前置动作
- 无（可独立执行）

### 后置动作
- 无（终端动作）

---

## ✅ 检查清单

执行前确认：
- [ ] 卡片 JSON 格式正确
- [ ] 按钮配置完整
- [ ] wide_screen_mode: true
- [ ] target 用户 ID 正确

---

_模块化定义 | 可独立调用 | 2026-03-07_
