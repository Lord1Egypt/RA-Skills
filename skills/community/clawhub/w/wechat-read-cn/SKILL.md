---
name: wechat-read
version: 2.0.0
description: Read chat history from a WeChat contact or group via macOS desktop client screenshot + agent OCR. Use when the user asks to read, view, check, or retrieve WeChat chat messages, conversation history, or recent messages from a contact or group. v2.0 auto mode tries fast locate + verify first; falls back to Agent-assisted mode only when verification fails. Requires macOS, WeChat desktop logged in, Accessibility permission, and cliclick. NOT for sending messages (use wechat-send).
metadata:
  {
    "openclaw":
      {
        "emoji": "📖",
        "os": ["darwin"],
        "requires": { "bins": ["cliclick"], "apps": ["WeChat"] },
        "install":
          [
            {
              "id": "cliclick",
              "kind": "brew",
              "formula": "cliclick",
              "bins": ["cliclick"],
              "label": "安装 cliclick（brew）",
            },
          ],
      },
  }
---

# 微信读取聊天记录（wechat-read）

在 macOS 上通过截图 + Agent 视觉识别的方式，读取微信联系人或群组的聊天记录。

## 前置条件

- macOS 微信桌面客户端已安装并登录
- 已向终端 / osascript 授予**辅助功能（Accessibility）**权限
- 已向终端授予**屏幕录制（Screen Recording）**权限（`screencapture` 需要）
- 已安装 **cliclick**（`brew install cliclick`）

## v2.0 自动模式（推荐）

一条命令完成联系人定位 + 聊天截图：

```bash
bash scripts/wechat_read.sh "<联系人>" [--pages N]
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
  ├─ 验证通过 (≈99.5%) → 截图聊天记录 ✅
  └─ 验证失败 (≈0.5%)  → 精确定位降级 ↓
      ↓
降级路径 (≈3.5s)
  ESC → 重新搜索 → 截图下拉框 → 退出（exit 2）
  ⚠️ 脚本以 exit code 2 退出，Agent 需要接管：
     1. 读取 /tmp/wechat_read_search.png
     2. 找到目标联系人行的屏幕坐标
     3. 调用 --capture 模式截图
```

### 验证逻辑（步骤 2）

截图保存至 `/tmp/wechat_read_verify_title.png`，OCR 识别标题栏文字后按优先级判断：

**⚠️ 排除法必须优先执行**（搜索框内本身含联系人名）：

1. **排除法（优先）**：标题含 `"网络查找"` / `"查找微信号"` / `"搜索网络结果"` → ❌ 失败（确认在搜索结果页）
2. **精确匹配**：排除通过后，标题包含联系人名字 → ✅ 通过
3. **相似度**：逐字符匹配率 ≥ 60% → ✅ 通过
4. 以上均不满足 → ❌ 失败

### Exit Code 约定

| Code | 含义 | Agent 动作 |
|------|------|-----------|
| 0 | 截图成功 | 分析截图 |
| 1 | 致命错误 | 报告错误 |
| 2 | 降级退出 | 读取截图 → 识别坐标 → 调用 `--capture` |
| 3 | 已到顶（--next-page） | 停止，报告未找到 |

### 处理 exit code 2（降级路径）

当脚本以 exit 2 退出时，Agent 应：

```bash
# 1. 读取截图（脚本已输出路径）
#    /tmp/wechat_read_search.png

# 2. 分析截图，找到目标联系人行的屏幕坐标 (x, y)
#    坐标换算：截图区域起始于 (50, 50)
#    屏幕坐标 = (50 + 截图像素x, 50 + 截图像素y)

# 3. 调用 --capture 完成截图
bash scripts/wechat_read.sh "<联系人>" --capture <x>,<y> [--pages N]
```

## v1.0 兼容模式（两阶段手动）

仍保留原始两阶段流程，适用于需要完全手动控制的场景：

### 第一阶段：搜索联系人

```bash
bash scripts/wechat_read.sh "<联系人>" --enter
```

执行：激活微信 → 设窗口 → Cmd+F 搜索 → 截图保存至 `/tmp/wechat_read_search.png`

**Agent 操作**：读取截图，找到正确联系人行的屏幕坐标 `{x, y}`。

坐标换算：截图区域起始于 `(50, 50)`，屏幕坐标 = `(50 + 截图像素x, 50 + 截图像素y)`。

### 第二阶段：点击进入并截图捕获

```bash
bash scripts/wechat_read.sh "<联系人>" --capture <x>,<y> [--pages N]
```

点击联系人进入会话，等待聊天加载，然后逐页截图聊天记录。通过 `cliclick` 点击目标坐标进入聊天窗口。

- 截取**聊天内容区域**（右侧面板，不含侧边栏和输入框）
- 使用 AppleScript `key code 116`（PgUp）向上滚动
- 每次滚动执行 **1 次 PgUp**（恰好 1 屏），相邻页面可能有少量重叠
- 截图保存至 `/tmp/wechat_read_p1.png`、`/tmp/wechat_read_p2.png`……
- 默认截取 3 页；使用 `--pages N` 指定页数

**滚动终止检测**：对每张截图计算 MD5 校验值。若连续两张截图完全相同（页面未变化），则判定已到达聊天顶部，自动停止，并输出 `[REACHED_TOP]` 标记。

### 第三阶段：Agent OCR 与内容整合

**Agent 操作**：读取所有截图（`/tmp/wechat_read_p1.png` 至 `pN.png`），然后：

1. **识别消息**：从每张截图中提取发送人、时间戳、消息内容
2. **去除重叠**：相邻页面约有 30% 内容重叠，匹配重复消息并去重
3. **处理相对时间**：微信显示"昨天 14:30"、"星期三"、"3月28日"等格式，根据当前日期转换为绝对时间
4. **按时间顺序组装**：截图顺序为从新到旧（p1 最新），需反向排列为正序
5. **输出结果**：整理为清晰的对话记录格式

---

### ⚠️ 消息方向识别规则（必须严格遵守）

微信聊天界面布局规则：

| 位置 | 含义 | 气泡颜色 |
|------|------|----------|
| **右侧** | **我方发出的消息** | 绿色气泡 |
| **左侧** | **对方发来的消息** | 白色/灰色气泡 |
| **底部** | **最新消息** | — |
| **顶部** | **最旧消息** | — |

**关键逻辑**：
- 时间轴方向：从上到下 = 从旧到新，**底部永远是最新消息**
- 判断谁说的：看气泡在屏幕**左边（对方）还是右边（我方）**，不是看截图顺序
- 判断最新消息：看 p1 截图**最底部**，那里是整个对话最新内容
- 联系人最新回复 = p1 截图底部最后几条**左侧白色**气泡

**常见错误（禁止）**：
- 把右侧绿色（我方）气泡误读为对方的回复
- 把截图顶部的消息当作最新消息
- 把页面顺序（p1/p2/p3）和消息新旧方向搞反

## 查找对方最新回复（自动翻页）

当最新一屏全是我方（右侧绿色）消息，找不到对方回复时，使用 **--next-page** 模式逐页向上翻找：

```bash
# 第一页已截，分析后发现全是我方消息，继续向上翻
bash scripts/wechat_read.sh "大号" --next-page 2
# → 截取第2页，保存 /tmp/wechat_read_p2.png
# → Agent 分析：有左侧白色气泡？有 → 停止；没有 → 继续

bash scripts/wechat_read.sh "大号" --next-page 3
# → 截取第3页，保存 /tmp/wechat_read_p3.png
# → 如此循环直到找到对方消息或到达聊天顶部
```

### Exit Code 约定（--next-page）

| Code | 含义 | Agent 动作 |
|------|------|-----------|
| 0 | 截图成功 | 分析截图 |
| 3 | 已到顶（与上一页相同） | 停止，报告未找到 |

### Agent 决策逻辑



## 使用示例

### v2.0 自动模式（推荐）

```bash
# 自动模式：快速定位 → 验证 → 截图（默认 3 页）
bash scripts/wechat_read.sh "联系人"
# → 自动完成：快速定位 → 验证 → 截图 (≈6s)
# → 若验证失败：exit 2，Agent 读截图后调用 --capture

# 自动模式：指定页数
bash scripts/wechat_read.sh "联系人" --pages 10
```

### v1.0 兼容模式

```bash
# 第一阶段
bash scripts/wechat_read.sh "微信联系人" --enter
# → Agent 读取 /tmp/wechat_read_search.png，找到联系人坐标 (200, 210)

# 第二阶段：截取 3 页（默认）
bash scripts/wechat_read.sh "微信联系人" --capture 200,210
```

### 读取更多历史记录

```bash
# 截取 10 页
bash scripts/wechat_read.sh "微信联系人" --capture 200,210 --pages 10
```

### 读取全部已加载历史

```bash
# 最多截取 50 页，到顶自动停止
bash scripts/wechat_read.sh "微信联系人" --capture 200,210 --pages 50
```

## 已知限制

- **截图区域固定**：聊天内容区域固定为屏幕矩形 `(370, 90, 830, 620)`，基于窗口位置 `{50,50}`、尺寸 `{1200,800}`。若微信窗口布局变化，需重新校准。
- **滚动粒度**：每页 8 次方向键↑，调整为约 30% 重叠。若重叠过多或过少，可修改脚本中的 `SCROLL_STEPS`。
- **仅捕获文字消息**：图片、表情包、语音、文件以视觉元素形式出现——Agent 可描述但无法提取内容。
- **历史深度取决于微信客户端**：仅能读取客户端已加载的消息。极旧消息可能需要先手动向上滚动加载。
- **中文 OCR 准确率**：取决于 Agent 使用的视觉模型，高分辨率截图效果更佳。
- **坐标为屏幕绝对坐标**：基于窗口固定位置 `{50,50}`，尺寸 `{1200,800}`。
- **OCR 依赖**：验证步骤使用 macOS Vision 框架（Swift），需 macOS 10.15+。OCR 失败视为验证失败，自动降级。

## 架构对比

| 维度 | v1.0 两阶段 | v2.0 自动验证 |
|------|-----------|-------------|
| 联系人定位 | Agent 看截图选坐标 | 自动 Enter + OCR 验证 |
| 耗时（正常） | 20-30s（含思考） | ≈6s |
| 耗时（降级） | — | ≈9s + Agent 识别 |
| 验证机制 | 无 | 标题栏 OCR |
| 误读风险 | 有 | 零（验证兜底） |
| Agent 参与 | 必须 | 仅 0.5% 降级时 |

## 可校准参数

以下参数为基于标准微信 macOS 布局（窗口位置 `{50,50}`，尺寸 `{1200,800}`）的固定值。若截图区域偏移，请测试并调整：

| 参数 | 当前值 | 控制内容 |
|------|--------|----------|
| `CHAT_RECT` | `370,90,830,620` | 聊天内容区截图范围（x, y, 宽, 高） |
| `SCROLL_STEPS` | `1` | 每次翻页 PgUp/PgDown 次数（1次=1屏） |
| `SCROLL_DELAY` | `0.05` | 每次按键之间的等待时间（秒） |
| `POST_SCROLL_WAIT` | `0.6` | 滚动后截图前的等待时间（秒） |
| `CLICK_FOCUS_POS` | `750,400` | 截图前点击聚焦聊天区域的坐标 |
