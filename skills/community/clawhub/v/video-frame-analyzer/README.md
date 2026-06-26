# video-frame-analyzer

AI漫剧/短剧视频智能帧分析工具，自动提取关键帧 → 多模态逐帧解读 → 输出完整分析报告。

## ✨ 功能简介

把任意短剧/AI漫剧视频丢进来，自动完成：

- **智能帧提取**：基于场景变化检测，非固定间隔截图（避免冗余）
- **逐帧解读**：画面内容、字幕/台词、镜头类型、叙事功能、情绪基调
- **完整报告**：剧情大纲、镜头语言分析、角色设定、字幕整理、商业改编建议

---

## 📋 分析报告包含

1. 视频基本信息（时长、帧数、AI生成标识）
2. 逐帧详细分析（表格形式）
3. 剧情大纲（分幕整理故事线）
4. 镜头语言分析（镜头类型分布、叙事节奏）
5. 角色设定（角色表，自动标注一致性问题⚠️）
6. 字幕/台词整理（时间轴表格）
7. 商业分析与改编建议（亮点、问题、改编方案）
8. 技术备注

---

## 🚀 快速开始

### 第一步：安装 Skill

**方式一：ClawHub（推荐）**
1. 访问 [https://clawhub.ai/import](https://clawhub.ai/import)
2. 搜索 `video-frame-analyzer`
3. 一键安装

**方式二：本地安装**
1. 下载 `video-frame-analyzer.skill.zip`
2. 在 WorkBuddy 左侧技能栏 → 上传技能 → 选择 zip 文件
3. 启用该技能

---

### 第二步：切换多模态模型

⚠️ **必须！** 先切换到支持图片输入的模型：
```
/model GLM-5v-Turbo
```
或
```
/model GPT-4o
```

纯文本模型（如 MiMo）无法分析图片。

---

### 第三步：开始分析

直接对 WorkBuddy 说：
> "分析这个视频"（然后上传或给出视频路径）

AI 会自动跑完全流程，最终输出完整分析报告。

---

## 📂 文件结构

```
video-frame-analyzer/
├── SKILL.md                      # Skill 定义文件
└── references/
    ├── smart_extract.py         # 智能帧提取（场景变化检测）
    └── extract_frames.py       # 保底帧提取（固定间隔）
```

---

## 🔧 依赖环境

```bash
pip install opencv-python          # 智能帧提取（推荐）
pip install moviepy Pillow       # 保底帧提取（备选）
```

Python 3.8+

---

## ⚠️ 常见问题

| 错误 | 原因 | 解决方案 |
|------|------|----------|
| `ImportError: No module named 'cv2'` | OpenCV 未安装 | `pip install opencv-python` |
| `400 input length too long` | 一次性发图太多 | 改为每批 3-4 帧 |
| 模型无法识别图片 | 当前为纯文本模型 | 先切换多模态模型 |
| 视频路径含中文 | 路径解析失败 | 用绝对路径或加引号 |

---

## 📌 适用场景

- 拆解竞品短剧/AI漫剧的叙事结构和镜头语言
- 分析视频剧情、角色、台词，输出改编建议
- 批量处理多个视频，建立素材库分析报告
- AI生成视频质量巡检（角色一致性、AI水印、表情自然度）

---

## 📄 开源协议

[MIT-0](LICENSE)

---

## ⭐ 支持作者

如果这个工具对你有帮助，欢迎：

- ⭐ 给本项目点一个 Star
- 📢 在小红书/朋友圈分享给你的朋友
- ☕ [请作者喝一杯咖啡](https://github.com/sponsors/shijin-ai)

---

## 👤 作者

**AI漫剧花大叔**

- GitHub: [https://github.com/shijin-ai](https://github.com/shijin-ai)
- 小红书: （在此填入你的小红书主页链接）

---

© 2026 AI漫剧花大叔。保留所有权利。
转载或使用请注明出处。
