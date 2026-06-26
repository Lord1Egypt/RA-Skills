---
name: social-auto-tool-builder
description: 复用“小红书自动回复项目”实战经验，快速构建新的本地AI自动化工具（含多平台选择器映射模板）
---

# 社媒自动化工具构建 Skill v1.1.0

## 目标
把“新自动化工具”的制作过程标准化，并在 v1.0.0 基础上新增多平台适配能力：
- Python + Playwright（persistent_context）
- 本地 Ollama（意图识别 + 回复生成）
- 规则过滤 + AI 生成混合策略
- 先 dry-run 再真实发送
- 参数化运行 + Windows EXE 打包
- 小红书 / 抖音 / 快手选择器映射模板

---

## 先决输入（必须确认）
1. 目标平台（xiaohongshu / douyin / kuaishou）
2. 入口 URL（通知页/消息页）
3. 已回复判定规则（例如“作者”）
4. 发送成功信号（toast 或状态文本）
5. 时间窗口与轮询间隔
6. 单轮最多处理条数

默认值（信息不全时）：
- `interval-minutes=5`
- `recent-hours=1`
- `max-replies=0`
- 先 `--once` dry-run

---

## 多平台选择器映射模板（核心）

在主程序中维护一个映射表（先填模板，后按真实 DOM 覆盖）：

```python
SELECTOR_MAP = {
    "xiaohongshu": {
        "url": "https://www.xiaohongshu.com/notification",
        "comment_item": ".interaction-item, .comment-item",
        "comment_text": ".interaction-content, .comment-text, .content",
        "reply_trigger": "button:has(svg.reply-icon), svg.reply-icon, .reply-btn",
        "input": "p#content-textarea.content-input, [contenteditable='true'].content-input, textarea.comment-input",
        "submit": "button.submit, button:has-text('发送')",
        "success": "text=评论成功",
        "replied_marker": "作者"
    },
    "douyin": {
        "url": "<TO_FILL_DOUYIN_URL>",
        "comment_item": "<TO_FILL>",
        "comment_text": "<TO_FILL>",
        "reply_trigger": "<TO_FILL>",
        "input": "<TO_FILL>",
        "submit": "<TO_FILL>",
        "success": "<TO_FILL_SUCCESS_TEXT>",
        "replied_marker": "<TO_FILL_MARKER>"
    },
    "kuaishou": {
        "url": "<TO_FILL_KUAISHOU_URL>",
        "comment_item": "<TO_FILL>",
        "comment_text": "<TO_FILL>",
        "reply_trigger": "<TO_FILL>",
        "input": "<TO_FILL>",
        "submit": "<TO_FILL>",
        "success": "<TO_FILL_SUCCESS_TEXT>",
        "replied_marker": "<TO_FILL_MARKER>"
    }
}
```

适配规则：
- 先读平台映射，再执行统一流程。
- 每个关键 selector 至少保留 1 个 fallback。
- 任何平台都先跑 dry-run 列候选，再启用真实发送。

---

## 标准流程（6 Phase）

### Phase 1：骨架搭建
- 主程序拆分：AI 客户端、自动化模块、参数解析。
- 支持参数：
  - `--platform`
  - `--interval-minutes`
  - `--recent-hours`
  - `--max-replies`
  - `--once`
  - `--interactive`

### Phase 2：平台映射接入
- 将平台 selector 映射注入 `Automation`。
- URL、评论列表、输入框、发送按钮、成功信号全部来自映射。

### Phase 3：真实 DOM 校准
- 让用户提供截图/DOM 片段，增量修正映射。
- 每次只改一个动作链路（打开弹窗、输入、发送）。

### Phase 4：安全与准确
- 已回复过滤（marker）
- 时间窗口过滤（recent-hours）
- 去重（`(text, age)`）
- 2-5 秒随机延迟

### Phase 5：验证
- dry-run：列出候选不发送
- 用户确认后真实发送
- 必须等待成功信号

### Phase 6：交付
- EXE 打包（含 Playwright 浏览器路径兼容）
- QUICK_START + FAQ
- Git 提交与推送

---

## 质量闸门（必须通过）
1. `python -m py_compile auto_responder_production.py`
2. `--once` 模式可运行
3. dry-run 候选与人工预期一致
4. 至少 1 条真实发送成功信号
5. EXE 参数模式可运行
6. EXE 交互模式可运行

---

## Windows 命令模板

```powershell
# 安装依赖
pip install -r requirements.txt
python -m playwright install chromium

# 本地模型检查
python -c "import requests;print(requests.get('http://127.0.0.1:11434/api/tags',timeout=5).status_code)"

# 单轮 dry-run
python auto_responder_production.py --platform xiaohongshu --once --recent-hours 1 --max-replies 3

# 构建 EXE
powershell -ExecutionPolicy Bypass -File .\build_exe.ps1

# EXE 参数模式
.\dist\auto_responder.exe --platform xiaohongshu --interval-minutes 5 --recent-hours 2 --max-replies 3

# EXE 交互模式
.\dist\auto_responder.exe --interactive
```

---

## 可复用 Prompt（新项目直接用）

```text
按 social-auto-tool-builder v1.1.0 的流程，帮我做一个【平台名】自动化工具。
要求：
1) Python + Playwright + 本地 Ollama
2) 用 persistent_context 保存登录状态
3) 先 dry-run 列候选，再真实发送
4) 支持 --platform --interval-minutes --recent-hours --max-replies --once --interactive
5) 用多平台选择器映射模板实现，允许按我提供的DOM增量修正
6) 最后打包EXE并给 QUICK_START
```

---

## 输出物检查清单
- [ ] `skill.yaml` 与 `SKILL.md` 完整
- [ ] 选择器映射模板已建立
- [ ] 平台参数化设计明确
- [ ] 验证与交付步骤可执行
