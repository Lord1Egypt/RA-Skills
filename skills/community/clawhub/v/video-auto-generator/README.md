# Video Auto Generator

> 全自动视频生成工具 — 输入选题，自动生成完整视频（脚本 + 配音 + 字幕 + 封面 + 剪辑）

[![Skill Version](https://img.shields.io/badge/Skill%20Version-2026.06-blue.svg)](#)
[![Platform](https://img.shields.io/badge/Platform-OpenClaw-green.svg)](#)
[![License](https://img.shields.io/badge/License-MIT-orange.svg)](#)

## 截图预览

> 以下截图展示典型视频生成效果，实际输出由 AI 动态生成。

| 脚本生成示例 | 配音 + 字幕输出 | 封面图示例 |
|:---:|:---:|:---:|
| 分镜 + 配音文案 + 时长 | SRT 字幕时间轴对齐 | 平台适配封面图 |

## 功能亮点

## 功能亮点

- ✅ **一键生成**：输入选题，5分钟生成完整视频
- ✅ **零基础可用**：无需视频编辑技能
- ✅ **高质量输出**：AI优化脚本/配音/剪辑
- ✅ **批量生产**：一天生成10-100个视频

## 使用场景

- 内容创作者需要批量生产视频（抖音/小红书/B站）
- 企业需要做产品宣传视频
- 教育者需要做在线课程视频
- 营销团队需要做广告视频

## 安装方法

1. 下载 `video-auto-generator.skill` 文件
2. 在QClaw中安装：`Skills` → `Install Skill` → 选择文件
3. 重启QClaw Gateway
4. 开始使用！

## 使用方法

### 基础用法

```
帮我生成一个视频，选题是：2026年最值得用的5个AI工具
```

### 高级用法

```
使用video-auto-generator技能，生成视频：
- 选题：2026年AI工具测评
- 时长：60秒
- 风格：测评
- 音色：云希（男声）
```

## 工作流程

1. **生成脚本** - AI自动生成视频脚本和分镜
2. **生成配音** - 使用edge-tts生成高质量配音
3. **生成字幕** - 自动生成SRT字幕文件
4. **生成封面** - 自动生成视频封面图
5. **合成视频** - 使用FFmpeg合成最终视频

## 技术要求

## 安装方法

### 方式一：SkillHub 在线安装（推荐）

```bash
skillhub install video-auto-generator
```

### 方式二：本地 Zip 安装

```bash
skillhub install /path/to/video-auto-generator-x.x.x.zip
```

### 方式三：手动安装

1. 下载 Skill 包，解压到 `~/.qclaw/skills/video-auto-generator/`
2. 重启 QClaw Gateway

## 依赖说明

| 依赖 | 版本要求 | 用途 | 必选 |
|------|---------|------|------|
| Python | 3.8+ | 运行环境 | 必选 |
| ffmpeg | 8.1+ | 视频处理引擎 | 必选 |
| edge-tts | 最新版 | AI 配音 | 必选 |
| Pillow | 最新版 | 图片处理 | 可选 |
| moviepy | 最新版 | 视频处理（高级功能） | 可选 |
| 当前平台模型 | — | 脚本生成（model route 自动选择） | 必选 |

**ffmpeg 安装建议**：使用 winget 安装（Windows）：
```bash
winget install ffmpeg
```

**edge-tts 安装**：
```bash
pip install edge-tts
```

## 变现路径

### 方案A：使用本Skill生成视频变现

- 生成视频 → 发布到各平台 → 流量分成
- 预计收益：5000-20000元/月

### 方案B：销售本Skill

- 在ClawHub上销售（定价99-299元）
- 提供定制开发服务（999-2999元）

## 常见问题

**Q: 生成的视频质量如何？**
A: 取决于AI模型和质量设置，建议先行测试。

**Q: 可以商用吗？**
A: 可以，但需要遵守各平台的版权规定。

**Q: 如何批量生成视频？**
A: 配合 `qclaw-cron-skill` 实现定时自动生成。

## 更新日志

### v1.0 (2026-06-12)

- 初始版本
- 支持基础视频生成流程
- 支持多种音色选择

## 联系方式

- 作者：QClaw AI
- 支持：在QClaw中留言

---

**立即安装，开始自动生成视频！**
