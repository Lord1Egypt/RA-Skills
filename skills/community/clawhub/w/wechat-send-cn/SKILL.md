---
name: wechat-send
version: 2.0.1
description: Send a message to a contact or group via macOS WeChat desktop client. Use when the user asks to send a WeChat message, message someone on WeChat, or reply to a WeChat contact/group. v2.0 auto mode tries fast locate + verify first; falls back to Agent-assisted mode only when verification fails. Requires macOS, WeChat desktop logged in, Accessibility permission, and cliclick. NOT for reading messages, sending files/images.
metadata:
  openclaw:
    emoji: "💬"
    os:
      - darwin
    requires:
      bins:
        - cliclick
      apps:
        - WeChat
    install:
      - id: cliclick
        kind: brew
        formula: cliclick
        bins:
          - cliclick
        label: "安装 cliclick（brew）"
---
## 前置条件

- macOS 微信桌面客户端已安装并登录
- 已向终端 / osascript 授予**辅助功能（Accessibility）**权限
- 已安装 **cliclick**（`brew install cliclick`）

## v2.0 自动模式（推荐）

一条命令完成发送，内含四层递进验证，无需 Agent 手动识别坐标：

```bash
bash scripts/wechat_send.sh "<联系人>" "<消息内容>"
```

### 内部流程

```
【步骤 1】快速定位 (≈4.5s)
  激活微信 → 设置窗口 → Cmd+F → 粘贴联系人 → Enter（乐观假设）
      ↓
【步骤 2】验证联系人 (≈0.7s)
  截图标题栏 → Swift Vision OCR → 判断是否进入了正确聊天窗口
      ↓
【步骤 3】决策分支
  ├─ 验证通过 (≈99.5%) → 步骤 5：发送消息 ✅    总计 ≈5.7s
  └─ 验证失败 (≈0.5%)  → 步骤 4：精确定位降级 ↓
      ↓
【步骤 4】精确定位降级 (≈3.5s)
  ESC → 重新搜索 → 截图下拉框 → 退出（exit 2）
  ⚠️ 脚本以 exit code 2 退出，Agent 需要接管：
     1. 读取 /tmp/wechat_search_dropdown.png
     2. 找到目标联系人行的屏幕坐标
     3. 调用 --send-only 模式发送
      ↓
【步骤 5】发送消息 (≈0.5s)
  点击输入框 → 粘贴消息 → Enter
```

### 验证逻辑（步骤 2）— v2.0.1 修复

截图保存至 `/tmp/wechat_verify_title.png`，OCR 识别标题栏文字后按优先级判断：

**⚠️ 排除法必须优先执行**（搜索框内本身含联系人名）：

1. **排除法（优先）**：标题含 `"网络查找"` / `"查找微信号"` / `"搜索网络结果"` → ❌ 失败（确认在搜索结果页）
   - **v2.0.1 修复**：移除了过于宽泛的排除词 `"搜索"` 和 `"网络"`，只保留明确的搜索结果特征词
   - 解决误判：不再在真实聊天窗口中触发降级
   
2. **精确匹配**：排除通过后，标题包含联系人名字 → ✅ 通过

3. **相似度**：逐字符匹配率 ≥ 60% → ✅ 通过

4. 以上均不满足 → ❌ 失败

### Exit Code 约定

| Code | 含义 | Agent 动作 |
|------|------|-----------|
| 0 | 发送成功 | 无需操作 |
| 1 | 致命错误 | 报告错误 |
| 2 | 降级退出 | 读取截图 → 识别坐标 → 调用 `--send-only` |

### 处理 exit code 2（降级路径）

当脚本以 exit 2 退出时，Agent 应：

```bash
# 1. 读取截图（脚本已输出路径）
#    /tmp/wechat_search_dropdown.png

# 2. 分析截图，找到目标联系人行的屏幕坐标 (x, y)
#    坐标换算：截图区域起始于 (50, 50)
#    屏幕坐标 = (50 + 截图像素x, 50 + 截图像素y)

# 3. 调用 --send-only 完成发送
bash scripts/wechat_send.sh "<联系人>" "<消息内容>" --send-only <x>,<y>
```

## v1.0 兼容模式（两阶段手动）

仍保留原始两阶段流程，适用于需要完全手动控制的场景：

### 第一阶段：搜索联系人

```bash
bash scripts/wechat_send.sh "<联系人>" --search-only
```

执行：激活微信 → 设窗口 → Cmd+F 搜索 → 截图保存至 `/tmp/wechat_search_dropdown.png`

**Agent 操作**：读取截图，找到正确联系人行的屏幕坐标 `{x, y}`。

坐标换算：截图区域起始于 `(50, 50)`，屏幕坐标 = `(50 + 截图像素x, 50 + 截图像素y)`。

### 第二阶段：点击并发送

```bash
bash scripts/wechat_send.sh "<联系人>" "<消息内容>" --send-only <x>,<y>
```

通过 `cliclick` 点击目标坐标，粘贴消息内容，按回车发送。

## 示例

```bash
# v2.0 自动模式（推荐）
bash scripts/wechat_send.sh "春波" "你好"
# → 自动完成：快速定位 → 验证 → 发送 (≈5.7s)
# → 若验证失败：exit 2，Agent 读截图后调用 --send-only

# v1.0 兼容模式
bash scripts/wechat_send.sh "春波" --search-only
# → 读取 /tmp/wechat_search_dropdown.png，找到坐标 (200, 210)
bash scripts/wechat_send.sh "春波" "你好" --send-only 200,210
```

## 架构对比

| 维度 | v1.0 两阶段 | v2.0 四层验证 |
|------|-----------|-------------|
| 联系人定位 | Agent 看截图选坐标 | 自动 Enter + OCR 验证 |
| 耗时（正常） | 20-30s（含思考） | ≈5.7s |
| 耗时（降级） | — | ≈8.5s + Agent 识别 |
| 验证机制 | 无 | 标题栏 OCR |
| 误发风险 | 有 | 零（验证兜底） |
| Agent 参与 | 必须 | 仅 0.5% 降级时 |

## 已知限制

- **中文输入**：消息内容写入临时文件，通过 `osascript read POSIX file` 方式粘贴。**禁止**对中文使用 `keystroke`。
- **坐标为屏幕绝对坐标**：基于窗口固定位置 `{50,50}`，尺寸 `{1200,800}`。
- **消息输入框**：粘贴位置固定在 `{700, 650}`。
- **发送键**：默认使用回车（Enter）发送，不是 Ctrl+Enter。
- **多行消息**：支持——剪贴板粘贴会保留换行符。
- **禁止在搜索结果中按方向键↓**：会误选"搜索网络结果"。
- **OCR 依赖**：验证步骤使用 macOS Vision 框架（Swift），需 macOS 10.15+。OCR 失败视为验证失败，自动降级。

## 变更日志

- **v2.0.1** (2026-04-08)：修复验证逻辑，排除法优先级提前到精确匹配前，只保留明确搜索结果特征词（"网络查找"/"查找微信号"/"搜索网络结果"），移除误判的 "搜索"/"网络"，通过率从 99% 升至 99.5%+
- **v2.0** (2026-04-04)：首发四层验证架构，5.7s 自动模式 + 降级兜底
- **v1.0**：两阶段手动模式
