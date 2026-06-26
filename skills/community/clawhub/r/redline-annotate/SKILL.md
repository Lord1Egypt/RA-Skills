---
name: redline
description: 在 AI 生成的 HTML 网页上做可视化标注，把"点元素 + 写评论"的反馈通过本地 server + UserPromptSubmit hook 自动喂回模型，无需复制粘贴。当用户说"标注网页"、"给这个 HTML 加批注"、"/annotate"、或希望对生成的网页提具体元素修改意见时触发。
---

# Redline

把 AI 生成的网页变成"可批注文档"，让用户像在 Google Docs 上 comment 一样直接在网页元素上提反馈。

**核心架构**：浏览器 ←(HTTP)→ 本地 server → 写 inbox 文件 → UserPromptSubmit hook 自动注入 → 模型 apply。用户**只需点一次"提交反馈"**，没有复制粘贴动作。

## 触发场景

- 用户已经让你生成了一个 HTML 文件，想对其中某些元素提具体修改意见
- 用户明确说"标注 xxx.html"、"给这个网页加批注"、"/annotate"
- **注意**：apply 阶段是 hook 自动触发的，模型不需要等用户说"应用反馈"

## 主要流程：注入（Inject）

**何时执行**：用户要求"标注 <文件名>"或"给 <文件> 加批注"。

**步骤**：
1. 确认目标 HTML 文件路径（默认就是最近生成的那个）
2. 调用 `injector.sh <html-file>`，它会：
   - 启动本地 server（127.0.0.1:7893，复用已有进程）
   - 把 `inject.css` / `inject.js` / `__RL_CONFIG__` 注入到 `</body>` 前
   - 输出到 `<原文件名>.annotated.html`（不动原文件）
   - 用 `open` 在默认浏览器打开
3. 告诉用户：「已打开标注页面。点右上角"✏️ 标注模式"开始，标完点"📤 提交反馈"，回来随便说一句话即可应用」

**绝对不要**：
- 改写原 HTML 文件
- 主动模拟 apply 阶段——它由 hook 自动触发

## 阶段 2：应用（Apply）

**何时执行**：**hook 自动触发**——当 cwd 下存在 `.redline-inbox.json` 时，UserPromptSubmit hook 会把它的内容塞进 additionalContext，并附带 apply 指令。模型不需要等用户显式说"应用"。

**步骤**：
1. 读取 hook 注入的 inbox JSON 内容
2. 读取 `feedback-template.md` 的渲染规则
3. 用 Edit 修改 inbox.file 对应的**源 HTML**（不是 .annotated.html）
4. **必须**用 `rm <inbox_path>` 删掉 inbox 文件，否则下一次 prompt 会重复触发
5. 简明汇报：每条标注 ✓/✗/⚠ + 一行说明

**冲突处理**：
- 如果用户当前 prompt 和反馈无关，先问「检测到 N 条挂起反馈，先处理还是继续当前话题？」
- 多条反馈对同一元素冲突 → 以最后一条为准，但在汇报里指出

## 文件清单

- `injector.sh` — 注入脚本，启 server + 注入资源 + 开浏览器
- `inject.js` — 标注层逻辑（toolbar/popover/sidebar/fetch 提交）
- `inject.css` — 标注层样式
- `server.py` — 本地 HTTP 接收端（POST /feedback → 写 inbox 文件）
- `hook.sh` — UserPromptSubmit hook（检测 inbox → 注入 additionalContext）
- `feedback-template.md` — JSON → 模型 prompt 的转换规则

## 安装 / 卸载

```bash
# 安装（自动配置软链接 + hook）
cd <skill-dir>/redline
./install.sh

# 卸载（移除软链接 + hook + 停 server）
./uninstall.sh
```

`install.sh` 会自动完成：
1. 创建 `~/.claude/skills/redline` 软链接
2. 向 `~/.claude/settings.json` 添加 UserPromptSubmit hook
3. 设置脚本可执行权限

首次使用时 server 自动启动，无需手动运行。

## 标注 JSON 形态（inbox 内容）

```json
{
  "file": "output.html",
  "timestamp": "2026-05-21T10:30:00Z",
  "annotations": [
    {
      "id": 1,
      "selector": "main > .hero > button.cta",
      "elementHTML": "<button class=\"cta\">立即购买</button>",
      "elementText": "立即购买",
      "boundingBox": {"x": 480, "y": 320, "w": 120, "h": 40},
      "comment": "颜色改成红的，再大 1.5 倍"
    }
  ]
}
```

## 调试

- 看 server 日志：`tail -f ~/.claude/redline/server.log`
- 手动起 server：`python3 server.py 7893`
- 手动测 hook：`CLAUDE_PROJECT_DIR=/path/to/project ./hook.sh`（需先在该目录放一份 inbox）
- 杀 server：`kill $(cat ~/.claude/redline/server.pid)`
