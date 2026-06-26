---
name: wechat-auto-reply
description: 微信消息自动发送/半自动回复。主动发送时，按“搜索联系人→单聊直接 Enter 进入聊天；群聊先识别群聊分组再定位目标项→粘贴消息→发送”的逻辑执行。适用于 macOS + 微信桌面版环境，需本机完成权限和依赖配置。使用方式：wechat-auto-reply "联系人名称" 或 wechat-auto-reply "联系人名称" "消息内容"
---

# WeChat Auto Reply Skill

微信自动发送 / 半自动回复技能。

## 当前已验证能力

### 主动发送模式
```bash
wechat-auto-reply "联系人名称" "消息内容"
```

已验证链路：
- 单聊：搜索联系人 → Enter 进入聊天 → 粘贴 → 发送
- 群聊：先 OCR 判断是否存在“群聊”分组；若存在，则在群聊分组下定位目标项并点击，再粘贴发送；若未识别到群聊分组，则自动 fallback 到搜索后直接 Enter 逻辑

### 半自动回复模式
```bash
wechat-auto-reply "联系人名称"
```

会尝试读取当前聊天截图并基于 OCR 生成建议回复。

## 🚀 安装

### 当前状态说明

这版 skill **已在作者环境中实测可用**，但目前更适合描述为：

- 在 **macOS + 微信桌面版** 的相似环境下可复用
- 需要本机完成依赖安装、权限授权和一次基础测试
- 单聊与群聊走不同路径，群聊更依赖 OCR 对搜索结果结构的判断
- 并不承诺“任何机器装上后零配置即用”

### 使用 Homebrew（推荐）

```bash
# 一行安装
brew install bjdzliu/openclaw/wechat-auto-reply

# 或者两步安装
brew tap bjdzliu/openclaw
brew install wechat-auto-reply
```

> 说明：Homebrew 方案用于安装命令入口与可安装依赖，但**不代表系统权限、微信登录状态、界面差异、OCR 路径差异都能自动处理完成**。

### 安装后仍需用户自己确认的事项

- 微信桌面版已安装并已登录
- 终端/相关执行程序具备 **辅助功能（Accessibility）** 权限
- 当前机器上的 `cliclick` 可正常调用
- Python / Vision Framework 相关桥接在本机可用
- 首次使用时，建议先用“文件传输助手”做发送测试
- 如果界面布局或微信版本差异较大，可能需要重新校准入口逻辑或点击区域

## 💡 使用方式

```bash
# OCR 半自动回复（查看聊天记录，智能判断回复内容）
# 置信度 > 85% 自动发送，否则弹窗确认
wechat-auto-reply "联系人名称"

# 主动发送（直接发送指定消息，不走 OCR）
wechat-auto-reply "联系人名称" "消息内容"
```

**示例：**
```bash
# 半自动回复模式
wechat-auto-reply "小李"      # 如果是"在吗"等高置信场景，自动发送
wechat-auto-reply "小王"      # 如果是问题类，会弹窗让你确认或修改

# 主动发送模式
wechat-auto-reply "小李" "什么时候下班"
wechat-auto-reply "小王" "今天行情怎么样"
```

## 功能描述

**两种模式：**
1. **半自动回复模式**：搜索联系人 → OCR 识别聊天内容 → AI 判断回复
   - 置信度 > 85% → 自动发送
   - 置信度 ≤ 85% → 弹窗确认（可修改回复内容）
2. **主动发送模式**：搜索联系人 → 直接发送指定消息

## 📂 文件位置

### Homebrew 安装后
- **Skill 目录**: `$(brew --prefix)/share/openclaw/skills/wechat-auto-reply`
- **用户链接**: `~/.openclaw/workspace/skills/wechat-auto-reply`
- **全局命令**: `$(brew --prefix)/bin/wechat-auto-reply`
- **配置文件**: `~/.openclaw/workspace/skills/wechat-auto-reply/wechat-dm.applescript`

### 查看安装路径
```bash
which wechat-auto-reply
ls -la ~/.openclaw/workspace/skills/wechat-auto-reply
```

## 环境准备

### 通过 Homebrew 安装（推荐）

Homebrew 版本会尽量处理可安装依赖，但**不应假设所有环境都能一次性自动完成**。

实际还需要用户确认：
- 微信桌面版已安装并登录
- macOS 已为终端/脚本授予 **辅助功能（Accessibility）** 权限
- Python / Vision Framework 相关桥接在本机可用

### 手动安装依赖（兜底）

#### 依赖工具

| 工具 | 安装方式 | 用途 |
|------|----------|------|
| `cliclick` | `brew install cliclick` | 稳定的鼠标点击 |
| `screencapture` | macOS 内置 | 截图（可通过 `/usr/sbin/screencapture` 调用） |
| Vision Framework | macOS 10.15+ | OCR 文本识别 |

#### Python 依赖

推荐使用虚拟环境，而不是直接往系统 Python 里装： 

```bash
python3 -m venv ~/.venvs/pyobjc
source ~/.venvs/pyobjc/bin/activate
pip install pyobjc-core pyobjc-framework-Quartz pyobjc-framework-Vision pyobjc-framework-Cocoa
```

如果脚本默认依赖该 venv，请先确认对应路径存在；若你使用不同路径，请同步调整脚本中的 Python 调用入口。

## 实现原理

### 1. 激活微信

```applescript
tell application "WeChat" to activate
```

### 2. 确保前台

```applescript
tell app "System Events"
  tell process "WeChat"
    set frontmost to true
  end tell
end tell
```

### 3. 搜索联系人 / 群聊

- 使用 `Cmd+F` 打开微信搜索
- 通过剪贴板粘贴目标名称
- **单聊路径**：搜索后直接 `Enter` 更稳定
- **群聊路径**：先 OCR 判断是否存在 `群聊` 分组，再在该分组下定位目标项

> 注意：
> - 不要把“点击左侧搜索结果项”默认当成进入聊天的稳定入口
> - 在某些结果结构下，点击左侧结果项会把界面带到“搜索聊天记录”态，而不是正常聊天窗口

### 4. OCR 截图

使用 macOS Vision Framework 识别聊天内容：

```python
from Vision import VNRecognizeTextRequest, VNImageRequestHandler

theRequest.setRecognitionLanguages(["zh-Hans", "en-US"])
theRequest.setUsesLanguageCorrection(True)
```

### 5. 智能回复判断（带置信度）

根据聊天内容自动生成回复，每个回复都附带置信度评分：

| 场景 | 关键词 | 回复内容 | 置信度 |
|------|--------|----------|--------|
| 询问在线 | "在吗"、"忙吗" | "在的，什么事？" | 95% |
| 感谢回复 | "谢谢"、"感谢" | "不客气" | 95% |
| 确认信息 | "收到"+"好的" | "好的" | 90% |
| 投资讨论 | "投资"、"抄底"、"行情" | "不急，等稳一点" | 85% |
| 问题咨询 | "?"、"？" | "我看看，稍等" | 75% |
| 一般确认 | "好"、"OK" | "好的" | 80% |
| 时间相关 | "明天"、"几点" | "我确认一下，回头告诉你" | 70% |
| 默认回复 | 其他 | "收到" | 60% |

**置信度规则：**
- **≥ 85%**：直接自动发送（高置信度场景）
- **< 85%**：弹窗显示建议回复，需用户确认
  - 可选择"确认发送"直接发送
  - 可选择"修改回复"手动编辑内容
  - 可选择"取消"不发送

### 6. 发送消息

当前已验证的发送链路依赖：
- 先正确进入目标聊天
- 再粘贴消息
- 再按回车发送

其中：
- **单聊**：当前实测“搜索后直接 `Enter` 进入聊天，再粘贴发送”更稳
- **群聊**：必须先完成“群聊分组识别与命中项定位”，不能直接套用单聊逻辑

## 注意事项

- **系统要求**：仅适用于 macOS + 微信桌面版
- **权限要求**：必须为执行环境授予 **辅助功能（Accessibility）** 权限
- **OCR 路线**：当前更依赖 macOS 原生 Vision Framework，不建议再回退到本机异常的 tesseract 路线
- **单聊/群聊差异**：两者必须分支处理，不能再用一套逻辑硬套
- **搜索结果限制**：左侧搜索结果项并不总是“进入聊天”的稳定入口；某些情况下会把界面带到“搜索聊天记录”态
- **群聊稳定性**：群聊逻辑仍然比单聊更依赖 OCR 与结果结构，跨机器/跨版本时需要额外测试
- **首次验证建议**：先用“文件传输助手”做单聊发送测试，再测试群聊

## 自定义配置

### 修改输入框坐标 / 路径逻辑

找到配置文件位置：
```bash
# Homebrew 安装
vim ~/.openclaw/workspace/skills/wechat-auto-reply/wechat-dm.applescript

# 或使用 brew 路径
vim $(brew --prefix)/share/openclaw/skills/wechat-auto-reply/wechat-dm.applescript
```

需要注意：
- 输入框点位可能因屏幕分辨率、微信版本、窗口大小而变化
- 单聊与群聊路径不要混写成同一套固定动作
- 如果后续继续优化，建议把“单聊入口”“群聊入口”“发送动作”拆成独立函数/脚本


### 调整置信度阈值

编辑配置文件：
```applescript
if confidence > 85 then  # 修改为你需要的阈值（0-100）
  set autoSend to true
```

### 添加自定义回复规则

在智能回复判断部分添加：
```applescript
else if ocrResult contains "你的关键词" then
  set replyText to "你的回复内容"
  set confidence to 90  -- 设置置信度
```

## 更新与卸载

### 更新
```bash
brew upgrade wechat-auto-reply
```

### 卸载
```bash
brew uninstall wechat-auto-reply

# 可选：删除 tap
brew untap bjdzliu/openclaw
```

## 错误处理

- 微信未安装：提示安装微信
- 搜索无结果：提示联系人不存在
- OCR 失败：重试截图或使用备用方案
