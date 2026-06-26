---
name: wechat-talk
version: 2.0.0
description: Windows 电脑端微信消息自动发送技能，通过键盘模拟给指定联系人发送消息。快捷命令：wt
triggers:
  - wt
  - 微信发送
  - 发微信
---

# WeChat Talk

Windows 电脑端微信消息自动发送技能。

## 功能

- 👤 搜索并打开联系人聊天窗口
- ✉️ 给指定联系人发送消息
- 🔄 批量发送（智能优化执行步骤）
- ⌨️ 纯键盘模拟，无需 API
- ⚡ 快捷命令：`wt`

## 安装

需要先安装 Python 依赖：

```bash
pip install pyautogui pygetwindow pillow pyperclip
```

## 使用方法

### 1. 单人发送

```bash
python send_batch.py "[张三]" "消息内容"
```

### 2. 批量发送（轮询模式）

```bash
# 初始化并发送第一条
python send_batch.py "[张三，李四，王五]" "消息内容"

# 继续发送下一条
python send_batch.py --next

# 继续发送下一条
python send_batch.py --next
```

**注意**: 联系人格式必须为 `[A,B,C]` 格式

### 3. 快捷命令

```bash
wt [张三] 消息内容
wt [张三，李四] 消息内容
```

## 执行流程

### 标准步骤

| 步骤 | 操作 | 快捷键/方法 | 延迟 |
|------|------|-------------|------|
| 1 | 打开微信 | `Ctrl+Shift+X` | 1.0s |
| 2 | 打开搜索 | `Ctrl+F` | 0.3s |
| 3 | 输入联系人名称 | `Ctrl+A` → `Delete` → `Ctrl+V` | 0.5s |
| 4 | 打开聊天窗口 | `Enter` | 0.5s |
| 5 | 粘贴消息 | `Ctrl+V` | 0.3s |
| 6 | 发送消息 | `Enter` | 0.3s |

### 智能执行逻辑

| 场景 | 位置 | 执行步骤 | 说明 |
|------|------|----------|------|
| **单人发送** | 唯一 | Step 1-6 | 完整流程 |
| **多人发送** | 第一个人 | Step 1-6 | 完整流程 |
| **多人发送** | 后续人员 | Step 2-6 | 跳过打开微信 |

**效率优化**: 多人发送时，后续人员跳过打开微信步骤，提升发送效率。

## 输入格式

### 联系人格式

**必须为 `[A,B,C]` 格式**

✅ 正确示例:
```bash
python send_batch.py "[张三]" "消息"
python send_batch.py "[张三，李四]" "消息"
```

❌ 错误示例:
```bash
python send_batch.py "张三" "消息"      # 缺少括号
python send_batch.py "张三，李四" "消息"  # 缺少括号
```

错误时返回：`请输入正确的发送人格式`

## 注意事项

1. 微信 PC 客户端需要已安装并登录
2. 发送消息时会自动激活微信窗口
3. 中文输入需要确保系统中文输入法正常工作
4. 执行过程中不要干扰键盘操作
5. 批量发送时请保持窗口打开状态，不要手动关闭
6. 联系人格式必须为 `[A,B,C]` 格式

## 文件结构

```
wechat-talk/
├── server.py       # 核心实现
├── send_batch.py   # 批量发送脚本
├── requirements.txt
├── send_queue.json # 批量队列（临时）
└── SKILL.md
```
