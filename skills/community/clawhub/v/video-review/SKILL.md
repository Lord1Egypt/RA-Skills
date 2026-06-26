---
name: video-review
description: 视频基础质量审核技能，对视频进行批量或单条的基础问题检测，包括画面质量、构图、音频、黑边、分辨率等，输出审核报告。
trigger:
  - "视频初审"
  - "审核视频"
  - "视频质量检测"
  - "检测视频"
  - "批量审核视频"
  - "视频基础问题"
---

# 视频初审 Skill

本技能对视频进行**基础质量审核**及**内容安全检测**，输出标准化的检测报告。**每次执行请严格遵循以下流程。**

---

## 执行流程总览

| 步骤 | 内容 | 工具 |
|------|------|------|
| 1 | 视频信息提取 + 基础质量检测 | ffprobe |
| 2 | 抽帧（1fps，全部帧） | ffmpeg |
| 3 | 视觉安全检测（并行批量） | image 工具 |
| 4 | 字幕转录 + 违禁词检测 | haoone-cli + 正则 |
| 5 | 汇总生成完整报告 | — |

---

## 第一步：视频信息提取 + 基础质量检测

```bash
ffprobe -v error \
  -show_entries format=duration,size \
  -show_entries stream=width,height,codec_name,r_frame_rate \
  -of json "<视频路径>"
```

**基础质量检测项目：**

| 检测项 | 合格标准 | 超标处理 |
|--------|---------|---------|
| 分辨率/比例 | 1080×1920（9:16竖屏） | 标记⚠️ |
| 帧率 | 统一（24/25/30fps） | 标记⚠️ |
| 码率 | 8-15Mbps | 标记⚠️ |
| 黑边 | 不存在 letterbox/pillarbox | width/height 比值在0.5-0.6为正常 |
| 跳帧/黑帧 | 无明显卡顿 | 逐帧像素对比，超80%相似则无跳帧 |
| 人声响度 | 各段音量差异<6dB | 差异>10dB标记⚠️ |

**跳帧检测脚本：**
```bash
python3 ~/.openclaw/skills/video-review/scripts/jump_frame_detector.py \
  -i "<视频路径>" --threshold 0.80
```

---

## 第二步：抽帧

```bash
mkdir -p /tmp/audit_frames
ffmpeg -y -i "<视频路径>" -vf "fps=1" -q:v "2" /tmp/audit_frames/frame_%04d.png
```

- **采样频率**：每秒1帧（1fps）
- **帧位置对应**：frame_0001 = 第0秒，frame_0002 = 第1秒，frame_00N = 第N-1秒
- **输出目录**：/tmp/audit_frames/
- **总帧数** ≈ 视频时长（秒）

---

## 第三步：视觉安全检测（并行批量）

**使用 image 工具分批分析，每批10帧，同时并行提交所有批次（最多6批/轮）。**

**时间戳换算公式：**
```
frame_NNNN = 第 (NNNN-1) // 60 分 (NNNN-1) % 60 秒
```

示例：
- frame_0046 → 第 0 分 45 秒
- frame_0091 → 第 1 分 30 秒
- frame_0106 → 第 1 分 45 秒

**每批 prompt（严格使用）：**
```
Review these 10 video frames for content safety compliance. 
OUTPUT ONE LINE PER FRAME. Format: frame_XXXX | [PASS or ISSUE_LETTER] | [SEVERE/MINOR/NONE]

Time mapping: frame_XXXX = (N-1) seconds (e.g. frame_0031 = 30s, frame_0046 = 45s)

Issues: A=revealing clothes, B=gov uniform, C=national emblem, D=money, E=blood/injury, F=dark/shocking, G=superstition, H=bad behavior

Safety work uniforms OK. Only mark police/military/gov uniform as B. Common work helmets and cleaning uniforms are NOT violations.

Output all 10 lines then end.
```

**问题等级标准：**
- 严重（SEVERE）：正面大面积暴露、警察/军人制服特写、人民币完整图案、血腥暴力特写
- 轻微（MINOR）：边缘暴露、暗示性穿着、仿真枪贴纸、轻微伤痕

**并发策略：** 同时最多提交6批（60帧），队列式接力，不等待第一批完成再提交下一批。

---

## 第四步：字幕检测

```bash
# 提取WAV
ffmpeg -y -i "<视频路径>" -ar 16000 -ac 1 -acodec pcm_s16le /tmp/audit.wav

# 转录
haoone-cli transcribe /tmp/audit.wav
```

**违禁词检测（比对 refs/banned_words.json）：**

| 类别 | 示例 |
|------|------|
| 脏话粗口 | 他妈的、傻逼、去死、装逼、草泥马、卧槽 |
| 极限词 | 最高、最低、第一、顶级、极品、绝对、全网最低 |
| 敏感国家名 | 中国、美国、英国、日本、俄罗斯、台湾 |

---

## 第五步：汇总生成完整报告

**报告格式规范（严格遵循）：**

```
━━━ 视频初审检测报告 ━━━
文件：
时长：<X>秒 | 分辨率：<宽>x<高> | 帧率：<fps>
通过：✅ / ⚠️ / ❌
问题数量：<N>

━━━ 视觉问题 ━━━

【A类 · 低俗暴露】

| 时间戳 | 第几分第几秒 | 问题描述 | 严重程度 |
|--------|------------|---------|---------|
| frame_XXXX | 00:0X:XX-XX | <问题描述> | **严重** |
| frame_XXXX | 00:0X:XX-XX | <问题描述> | 轻微 |

━━━ 字幕/台词问题 ━━━
  无违禁词检出

━━━ 总结 ━━━
综合判定：⚠️ 需处理后通过
严重问题：<N>帧（A类低俗暴露）
轻微问题：<N>帧

【问题分布】
  00:0X:XX-XX（<秒数>秒区间）━ A类约<N>帧

━━━ 操作建议 ━━━
<秒数>秒区间存在多帧女性暴露内容，建议：
  ① 剪辑删除该区间（<起始秒>-<结束秒>秒）
  ② 或局部遮挡+画面替换

详细帧位置已标记，可对应原视频时间码精确定位剪辑点。
```

**格式规范说明：**
- `通过：`行：✅（通过）/ ⚠️（需处理后通过）/ ❌（不通过）
- 表格使用 `┌─┬─┐` 框线字符，字段：时间戳 | 第几分第几秒 | 问题描述 | 严重程度
- **严重程度为"严重"的行，文字加粗处理**
- 第几分第几秒格式：`00:0X:XX`（分:秒），区间范围 `00:0X:XX-XX`
- 问题描述：简洁明确，说明违规内容和视觉特征
- 问题分布：标注具体时间区间和帧数
- 操作建议：给出具体处理方案（剪辑删除/局部遮挡）
- 报告末尾不加结尾符号，直接结束

---

## 检测维度（完整）
## 检测维度（完整）

### A. 基础质量检测

| 检测项 | 说明 |
|--------|------|
| 分辨率/比例 | 9:16竖屏（1080x1920等） |
| 帧率 | 统一（24/25/30fps） |
| 码率 | 8-15Mbps |
| 黑边 | 不存在 letterbox/pillarbox |
| 音频 | 音轨正常 |
| 跳帧/黑帧 | 无明显卡顿花屏 |
| 人声响度 | 各段音量差异<6dB |

### B. 内容安全/违规检测

| 类别 | 说明 |
|------|------|
| **A·低俗暴露** | 深V、低胸、透视、过于紧身、性暗示动作 |
| **B·公职人员** | 警察/军人制服、警徽/军徽、法官/检察官、国徽/法槌/法院标识 |
| **C·机关标志** | 国徽、警局/公安局标识、检察院、政府楼外观 |
| **D·人民币** | 人民币纸币/硬币完整图案（含变形涂鸦） |
| **E·血腥暴力** | 割腕/自残血痕（中景及以上特写）、虐待、家暴殴打特写 |
| **F·阴暗画风** | 整体色调极度阴暗压抑、灵异惊悚氛围 |
| **G·封建迷信** | 现实题材中算命/看相/做法事/巫蛊/香灰 |
| **H·未成年保护** | 未成年人吸烟/饮酒/纹身、校园霸凌、早恋 |
| **脏话粗口** | 字幕/台词中粗鄙辱骂性语言 |
| **极限词** | 含"最"字的夸大宣传语 |
| **敏感国家名** | 中国、美国、英国、日本、俄罗斯等（真实背景设定语境） |

---

## 违禁词库

文件：`refs/banned_words.json`

---

## 常用脚本

### 单条视频审核
```bash
python3 ~/.openclaw/skills/video-review/scripts/content_audit.py <视频路径>
```

### 跳帧检测
```bash
python3 ~/.openclaw/skills/video-review/scripts/jump_frame_detector.py \
  -i <视频路径> --threshold 0.80 --output-json /tmp/jump_report.json
```

### 批量审核文件夹
```bash
for f in /path/to/folder/*.mp4; do
  echo "▶ $f"
  python3 ~/.openclaw/skills/video-review/scripts/content_audit.py "$f"
done
```

---

## 注意事项

1. **抽帧频率**：统一使用1fps，不用场景感知抽帧
2. **并行检测**：视觉检测必须并行分批，不逐个等待
3. **帧号换算**：frame_NNNN = 第 `(NNNN-1)//60` 分 `(NNNN-1)%60` 秒
4. **假阳性**：AI 视觉判断有误差，报告仅供参考，最终由人判断
5. **审核尺度**：以《动画微短剧内容创作建议》和《剧目修改意见统计汇总》为基准