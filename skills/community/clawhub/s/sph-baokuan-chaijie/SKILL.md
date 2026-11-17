---
name: sph-baokuan-chaijie
description: 视频号爆款拆解流水线。给一条或多条视频号分享链接，自动下载视频→提取音频→Whisper转录文案→提取元数据（标题/标签/互动数据/账号信息），然后按分析框架拆解爆款逻辑（标题公式/标签漏斗/内容结构/互动数据/可复用策略），输出综合HTML报告。触发词：视频号拆解、爆款分析、视频号文案提取、视频号账号分析、sph拆解、视频号爆款。
license: MIT
metadata:
  version: "1.0.0"
  author: "心明增长实验室"
  category: "营销运营"
  tags: "视频号,爆款分析,文案提取,内容拆解,GEO,AI营销"
  triggers: "视频号拆解,爆款分析,视频号文案提取,视频号账号分析,sph拆解,视频号爆款"
---

# 视频号爆款拆解流水线

## Overview

给一条视频号分享链接（`https://weixin.qq.com/sph/xxxxx`），自动完成「下载视频 → 转录文案 → 爆款逻辑分析 → 综合报告」全流程。支持多条链接批量处理。

## 前置条件

### 必须满足
1. **wx-video-download 技能**：已安装该技能并完成腾讯元宝登录（首次使用需在可见浏览器中手动登录一次）
2. **ffmpeg**：系统已安装 ffmpeg（用于音频提取）
3. **openai-whisper**：已安装 Whisper（本地转录，无需 API Key）

### 检查命令
```bash
# 检查 Yuanbao 登录状态（路径根据实际安装位置调整）
python "<wx-video-download技能路径>/scripts/yuanbao_channels.py" doctor

# 检查 ffmpeg
ffmpeg -version

# 检查 Whisper
python -c "import whisper; print('OK')"
```

如果 Yuanbao 未登录，执行：
```bash
python "<wx-video-download技能路径>/scripts/yuanbao_channels.py" login --timeout 300
```
（在弹出的浏览器窗口中完成腾讯元宝登录）

> pipeline.py 会自动检测 wx-video-download 技能的安装位置和 Whisper 可执行文件路径，无需手动配置。

---

## 工作流程

### Step 1: 运行流水线脚本（下载 + 转录 + 元数据提取）

**单条链接：**
```bash
python "<本技能路径>/scripts/pipeline.py" "https://weixin.qq.com/sph/xxxxx" --output-dir "<工作目录>/outputs/sph-analysis"
```

**多条链接（从文件读取）：**
1. 创建 `links.txt`，每行一个链接
2. 运行：
```bash
python "<本技能路径>/scripts/pipeline.py" --links-file links.txt --output-dir "<工作目录>/outputs/sph-analysis"
```

**输出文件：**
- `result.json` — 全部元数据 + 文案（供分析使用）
- `videos/*.mp4` — 原始视频文件
- `audio/*.wav` — 提取的音频
- `transcripts/*.txt` — Whisper 转录的逐字稿

### Step 2: 顺藤摸瓜——发现更多视频（可选）

视频号 API 不支持获取账号全部视频列表，需要用以下方式发现更多链接：

**方法 A：Web 搜索**
用 WebSearch 搜索该账号的视频链接：
- 搜索词：`"<账号名>" weixin.qq.com/sph`
- 搜索词：`"<账号名>" 视频号 分享`
- 从搜索结果中提取 `weixin.qq.com/sph/xxxxx` 格式的链接

**方法 B：用户提供**
请用户在手机微信中打开账号主页，复制视频链接发过来。

发现新链接后，追加到 links.txt 并重新运行 pipeline.py。

### Step 3: 读取 result.json 进行分析

读取 `result.json`，对每个视频按 `references/analysis_framework.md` 框架进行分析：

1. **标题公式**：拆解标题中的热点词/情绪词/平台词/利益词
2. **标签策略**：按三层漏斗分类（精准层/人群层/泛流量层）
3. **内容结构**：从转录文案中识别开头钩子→正文展开→行动引导
4. **互动数据**：计算转发率，判定爆款类型
5. **爆款逻辑**：提炼核心公式
6. **跨视频对比**（多视频时）：找共性、排差异

### Step 4: 生成 HTML 报告

基于分析结果，生成一份完整的 HTML 报告，包含：

- **封面区**：账号名 + 分析视频数 + 分析日期
- **账号概览**：账号定位、内容方向、互动总量
- **视频列表**：按转发数排序，每个视频一张卡片
- **单视频拆解**：每个视频的标题公式/标签漏斗/内容结构/互动数据
- **跨视频分析**（多视频时）：标题公式共性、标签体系、内容模式
- **可执行建议**：3-5 条可落地的策略建议
- **原始文案**：附上每条视频的完整转录文本

报告保存为 `<工作目录>/outputs/sph-analysis/爆款拆解报告.html`

### Step 5: 呈现结果

用 `present_files` 展示 HTML 报告，同时附上 result.json 和转录文本文件。

---

## 技术限制说明

| 能力 | 状态 | 说明 |
|------|------|------|
| 下载视频 | ✅ | 通过 Yuanbao API + 浏览器会话 |
| 转录文案 | ✅ | ffmpeg 提取音频 + Whisper 自动选模型（小视频用small，大视频用base） |
| 提取元数据 | ✅ | 标题/标签/互动数据/账号名/封面 |
| 爆款逻辑分析 | ✅ | AI 按分析框架执行 |
| 获取账号全部视频 | ⚠️ | API 不支持，依赖 Web 搜索 + 用户提供 |

> **重要**：视频号没有公开的账号主页 API，无法自动获取账号下所有视频。`pipeline.py` 处理的是你提供的链接。"顺藤摸瓜"需要通过 Web 搜索发现更多公开分享的链接，覆盖面不完整。建议用户在手机微信中打开账号主页，批量复制视频链接。

---

## 资源文件

### scripts/
- `pipeline.py` — 核心流水线脚本（下载→转录→元数据提取），自动检测环境路径

### references/
- `analysis_framework.md` — 爆款拆解分析框架（标题公式/标签漏斗/内容结构/互动数据/跨视频对比）

---

## 转录质量说明

- 使用 Whisper 自动选择模型：音频≤3MB 用 small（更准），>3MB 用 base（更快）
- 小视频（< 2分钟）转录约 30-60 秒
- 中文准确率约 85-95%，专有名词可能有误
- 如需更高精度，可改用 `medium` 或 `large` 模型（速度更慢）
- 转录结果包含语气词和口语化表达，分析时需自行清洗

---

## 开发者

心明增长实验室出品  
公众号：心明增长实验室  
如需批量拆解服务或定制分析，请通过公众号联系。
