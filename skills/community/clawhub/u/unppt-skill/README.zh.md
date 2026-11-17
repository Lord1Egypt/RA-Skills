[English](README.md) | **简体中文**

# unppt-skill

给 AI 编程助手（WorkBuddy / Claude Code / Cursor 等）用的 [unppt](https://github.com/spitmaster/unppt) 技能：让 AI 学会**把 PowerPoint 课件（.pptx）转换成网页**——命令行或代码调用、批量转换、检查字体、iframe 嵌入、用 JS 控制翻页。

装上这个技能后，直接对 AI 说：

- "把这个 PPT 转成网页"
- "把 demo.pptx 转成一个单文件 HTML 发给别人"
- "帮我把这批课件批量转出来放到网站上"
- "检查一下这个 PPT 的字体有没有问题"
- "把这个课件嵌到我的网页里，做一个上一页/下一页按钮"

AI 会按照 `SKILL.md` 里的流程选择合适的产物形式、执行转换、处理字体问题；需要进阶能力（嵌入控制、云函数部署）时，会自动加载 `references/` 下的详细参考。

> **输入格式**：直接输入支持 `.pptx`（OOXML）。老的二进制格式 `.ppt` 转码器本身不支持——需先在 PowerPoint 里另存为 `.pptx`（文件 → 另存为）；技能会教 AI 引导用户完成这一步，包括 Windows 下用 PowerPoint COM 自动化批量另存。

## 目录结构

```
unppt-skill/
├── SKILL.md                    # 技能入口：环境准备、产物形式选择、常见任务、关键规则
├── references/
│   ├── cli.md                  # 命令行全部选项、unppt check、字体机制
│   ├── api.md                  # convert()/checkFonts() JS API、write 回调、大文件、四类可运行示例
│   └── embedding.md            # iframe、postMessage 协议、UnpptFrame、原生 App、直播课同步
└── scripts/
    └── batch-convert.mjs       # 批量转换脚本，可直接运行
```

技能内容基于 **unppt 0.3.2**，随上游版本更新维护。

## 安装

前提：转码的机器上装有 [Node.js](https://nodejs.org/) ≥ 20.12（转码时还需 `npm install -g @unppt/unppt`，AI 会在技能流程中自动处理）。

### WorkBuddy

用户级（所有项目可用）：

```bash
git clone https://github.com/spitmaster/unppt-skill.git "%USERPROFILE%\.workbuddy\skills\unppt"
```

或项目级（随仓库共享给团队）：

```bash
git clone https://github.com/spitmaster/unppt-skill.git .workbuddy/skills/unppt
```

### Claude Code

```bash
# 用户级
git clone https://github.com/spitmaster/unppt-skill.git ~/.claude/skills/unppt
# 或项目级
git clone https://github.com/spitmaster/unppt-skill.git .claude/skills/unppt
```

### Cursor

```bash
git clone https://github.com/spitmaster/unppt-skill.git .cursor/skills/unppt
```

### 其他支持 SKILL.md 约定的 AI 工具

把本仓库克隆进该工具的 skills 目录即可（目录名 `unppt` 就是技能名）。技能只有文本和一个脚本，无需构建。

> 手动安装（不用 git）：下载 [ZIP](../../archive/refs/heads/main.zip) 解压，把解压出的文件夹改名为 `unppt`，放进对应工具的 skills 目录。

## 验证

安装后对 AI 说"把这个 PPT 转成网页"（或提到 unppt），确认它触发 unppt 技能并按流程执行。也可以直接跑批量脚本：

```bash
npm install @unppt/unppt
node scripts/batch-convert.mjs <pptx目录> <输出目录>
```

## 相关链接

- unppt 主仓库：<https://github.com/spitmaster/unppt>
- npm：<https://www.npmjs.com/package/@unppt/unppt>
- unppt 文档（本技能内容的来源）：[docs/zh](https://github.com/spitmaster/unppt/tree/main/docs/zh)

## 许可

[Apache-2.0](LICENSE)。技能内容整理自 unppt 项目文档（Apache-2.0）。
