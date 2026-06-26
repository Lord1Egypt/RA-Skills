# Toonany — AI 漫剧创作助手

**Any story, any style, anyone.**

[![ClawHub](https://img.shields.io/badge/ClawHub-Install-blue)](https://clawhub.ai/casperkwok/toonany)

Toonany 是一个 [Claude Code Skill](https://clawhub.ai/casperkwok/toonany)，帮助任何人将小说或故事转化为 AI 生成的漫剧（短剧/动画）。无论你是新手还是专业创作者，都能快速产出高质量的视觉叙事内容。

> **核心理念**: 任何故事 × 任何风格 × 任何人 = 一部漫剧。
>
> 从一段文字到一段带配音、字幕、背景音乐的成片，最快 30 分钟。

---

## 适用场景

- **网文作者**: 将热门章节转化为短视频内容，引流涨粉
- **自媒体运营**: 批量生产小说推文视频，多平台分发
- **独立创作者**: 低成本实现个人动画/短剧创作
- **教育/培训**: 将教案、案例转化为生动的视频教材
- **品牌营销**: 用故事化视频传递品牌理念

## 完整工作流

```
小说原文
    ↓
故事线 (storyline) —— 核心情节脉络
    ↓
分集大纲 (outline) —— 每集场景拆分
    ↓
资产提取 (assets) —— 角色、场景、道具定义
    ↓
风格样张 (style-sample) —— 视觉锚点确认
    ↓
剧本 (script) —— 对白、旁白、镜头描述
    ↓
分镜 (storyboard) —— 镜头序列 + 画面描述
    ↓
分镜图 (storyboard-image) —— AI 生成每帧画面
    ↓
视频 (video) —— 图片转动态视频
    ↓
音频/字幕 (audio) —— AI 配音 + 自动字幕
    ↓
后期合成 (finalize) —— 拼接 + 混音 + 字幕烧录
    ↓
成片输出 🎬
```

## 核心设计原则

| 原则 | 说明 |
|------|------|
| **风格锚定** | 批量生成前先确认风格样张，杜绝风格漂移 |
| **角色一致** | 四视图参考图 + seed 锁定，跨集不变脸 |
| **变更传播** | 修改上游自动提示下游重算，避免版本错乱 |
| **质量校验** | 自动检查角色名一致性、场景一致性、风格一致性 |
| **新手友好** | 缺什么补什么，不会卡住，全程引导 |

## 特点

- **新手友好**: 引导式交互，缺什么补什么，不会卡住
- **快速出片**: `/toonany quick` 单命令走完完整流程
- **风格锚定**: 先确认风格样张，再批量生成，确保风格统一
- **角色一致**: 四视图参考图 + seed 锁定，跨集不变脸
- **完整管线**: 从小说到成片（含配音、字幕、混音）一站式完成
- **跨平台**: 纯 Python 脚本，Windows/macOS/Linux 通用

## 5 分钟快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 创建项目

在 Claude Code 中执行：

```
/toonany new 我的漫剧项目
```

系统会交互式询问项目信息，并自动检查 API Key 配置。

### 3. 快速出片（推荐新手）

```
/toonany quick
```

跟随引导：
1. 提供小说内容（直接粘贴或上传文件）
2. 选择风格（从 20+ 种预设风格中选择）
3. 等待生成...
4. **确认风格样张**（关键步骤！确保风格符合预期）
5. 继续生成，最终输出成片

### 4. 专业模式（推荐有经验的用户）

分阶段精细控制：

```
/toonany story           # 生成故事线
/toonany outline 1       # 生成第1集大纲
/toonany assets          # 提取资产
/toonany style-sample    # 生成风格样张
/toonany script 1        # 生成剧本
/toonany storyboard 1    # 生成分镜
/toonany storyboard-image 1  # 生成分镜图
/toonany video 1         # 生成视频
/toonany audio 1         # 生成配音和字幕
/toonany finalize 1      # 后期合成成片
```

## 项目结构

```
output/{project-name}/
├── project.json          # 项目配置
├── storyline.md          # 故事线
├── outline/              # 分集大纲
├── assets/               # 角色/场景/道具
│   ├── images/           # 资产图片
│   └── style-sample.jpg  # 风格样张
├── script/               # 剧本
├── storyboard/           # 分镜
├── video/                # 视频片段
├── audio/                # 配音
├── subtitle/             # 字幕
└── final/                # 最终成片
```

## 核心命令速查

| 命令 | 用途 |
|------|------|
| `/toonany new <name>` | 创建项目 |
| `/toonany config` | 配置 API Key |
| `/toonany quick` | 快速模式（一键出片） |
| `/toonany validate` | 校验项目 |
| `/toonany export` | 导出项目 |

## 常见问题

### Q: 没有 API Key 怎么办？
A: 执行 `/toonany config`，系统会自动检测缺失的 Key 并给出申请链接和配置指引。

### Q: 生成的角色在多集中不一致怎么办？
A: Toonany 使用四视图参考图 + seed 锁定机制。在 `project.json` 中检查角色的 `seed` 字段是否一致。如需调整，修改后重新运行 `/toonany assets`。

### Q: 风格不满意怎么办？
A: 在批量生成前，Toonany 会生成风格样张供你确认。如果不满意，可以修改 `project.json` 中的 `artStyle` 字段，然后重新运行 `/toonany style-sample`。

### Q: 修改了大纲，后续文件会联动更新吗？
A: Toonany 有依赖追踪机制。修改上游文件后，执行 `/toonany validate` 会提示哪些下游文件需要重新生成。

## 模型支持

| 类型 | 推荐 Provider | 说明 |
|------|--------------|------|
| 文本 | DeepSeek | 性价比高，适合大纲和剧本 |
| 图像 | 火山引擎 (豆包) | 支持宫格图，适合分镜 |
| 视频 | 可灵 / 豆包 | 支持多种生成模式 |
| 音频 | 豆包 TTS | 音色丰富，支持情感 |

## 安装方式

### 通过 ClawHub 安装（推荐）

在 Claude Code 中执行：

```bash
clawhub install toonany
```

或直接访问 👉 **[clawhub.ai/casperkwok/toonany](https://clawhub.ai/casperkwok/toonany)** 安装。

### 手动安装

将本仓库克隆到 `~/.claude/skills/toonany/` 目录：

```bash
git clone https://github.com/casperkwok/toonany.git ~/.claude/skills/toonany
```

## 了解更多

- [详细教程](TUTORIAL.md) — 完整使用指南
- [数据模型](references/data-model.md)
- [生产流程](references/workflow.md)
- [模型配置](references/model-config.md)
- [命令参考](references/commands.md)

---

**ClawHub**: [clawhub.ai/casperkwok/toonany](https://clawhub.ai/casperkwok/toonany)  
**GitHub**: [github.com/casperkwok/toonany](https://github.com/casperkwok/toonany)
