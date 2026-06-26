# 📚 SJTU Canvas 课程助手

> 一个 [OpenClaw](https://github.com/openclaw/openclaw) 技能，让 AI 帮你管理 Canvas LMS 上的课程、作业、成绩和课件。

默认适配 **上海交通大学** Canvas (oc.sjtu.edu.cn)，修改一行配置即可兼容任何 Canvas LMS 实例。

## 💡 灵感来源

本项目受 [SJTU-Canvas-Helper](https://github.com/Okabe-Rintarou-0/SJTU-Canvas-Helper) 启发，在其课程管理的基础上，结合 OpenClaw AI Agent 能力，实现了 **AI 驱动的课件总结、作业辅导和知识点关联** —— 不只是下载课件，更能帮你理解课件、定位作业对应的知识点、给出解题思路。

## ✨ 功能一览

| 功能 | 说明 |
|---|---|
| 📂 **课件管理** | 查看、下载、批量下载课程文件（PPT/PDF/DOCX） |
| 🧠 **AI 课件总结** | 提取课件内容为 Markdown，配合 AI 生成学习笔记 |
| 🎯 **作业辅导** | 自动提取作业要求，匹配相关课件，定位对应知识点，给出解题思路 |
| 📝 **DDL 追踪** | 一键查看所有课程的未来截止时间 |
| ⏰ **日历同步** | 将 DDL 同步到 Apple 日历，iCloud 自动推送到 iPhone |
| 📊 **成绩查询** | 查看各科已出成绩，计算均分 |
| 💬 **讨论区** | 获取课程讨论区内容和摘要 |
| 🚀 **提交作业** | 直接从命令行提交作业文件 |
| 📦 **复习包** | 批量导出所有课件为 Markdown，导入 NotebookLM 复习 |

### 🎯 AI 作业辅导 — 核心亮点

传统工具只能帮你下载课件，而本技能可以：

1. **提取作业要求** — 自动获取作业描述，识别题目图片
2. **关联课件知识点** — 在课程文件中检索与作业相关的课件内容
3. **定位核心知识点** — 告诉你这道题考的是哪个章节、哪个公式
4. **给出解题思路** — 结合课件内容，提供结构化的解题引导

> 对话示例：
> - "这次传热学作业考的是哪些知识点？"
> - "帮我看看这道题该用什么公式"
> - "把作业要求和对应的课件内容整理成文档"

## 🚀 安装

### 通过 ClawHub（推荐）

```bash
clawhub install sjtu-canvas
```

### 手动安装

```bash
cd ~/.openclaw/workspace/skills
git clone https://github.com/xhh678876/sjtu-canvas.git sjtu-canvas
```

## ⚙️ 配置

### 1. 创建配置文件

```bash
cd ~/.openclaw/workspace/skills/sjtu-canvas
cp config.example.json config.json
```

### 2. 获取 Canvas API Token

1. 登录你的 Canvas → **设置** → **新建访问令牌**
2. 复制 Token，填入 `config.json`：

```json
{
  "canvas_token": "你的Token",
  "base_url": "https://oc.sjtu.edu.cn",
  "save_dir": "~/Downloads/Canvas课件",
  "calendar_name": "Canvas作业"
}
```

> 💡 非 SJTU 用户只需修改 `base_url` 为你学校的 Canvas 地址。

### 3. 安装 Python 依赖

```bash
pip3 install python-pptx pdfplumber requests
```

## 💬 使用方式

配置完成后，在 OpenClaw 对话中自然语言交互即可：

```
"看一下最近有哪些 DDL"
"下载传热学的课件"
"帮我总结这个 PPT 的重点"
"这次作业考的是哪些知识点？"
"帮我看看这道题该怎么做"
"查看成绩"
"把 DDL 同步到日历"
```

### 命令行直接使用

```bash
cd ~/.openclaw/workspace/skills/sjtu-canvas

# 查看课程列表
python3 scripts/canvas_api.py courses

# 查看所有未来 DDL
python3 scripts/canvas_api.py ddls

# 查看已出成绩
python3 scripts/canvas_api.py grades

# 提取课件内容
python3 scripts/file_extractor.py path/to/lecture.pptx

# 同步 DDL 到 Apple 日历
python3 scripts/calendar_sync.py
```

## 🏗️ 项目结构

```
sjtu-canvas/
├── SKILL.md              # OpenClaw 技能定义
├── config.example.json   # 配置模板
├── README.md
├── LICENSE
└── scripts/
    ├── canvas_api.py       # Canvas API 核心（课程/文件/作业/成绩/讨论）
    ├── file_extractor.py   # 课件提取器（PPT/PDF/DOCX → Markdown）
    └── calendar_sync.py    # DDL → Apple Calendar 同步（macOS）
```

## 🎓 兼容性

- ✅ **Canvas LMS** — 适配任何 Canvas 实例，不限于 SJTU
- ✅ **macOS** — Apple 日历同步（iCloud → iPhone）
- ✅ **OpenClaw** — 作为 AgentSkill 自动触发
- ⚠️ 日历同步功能仅限 macOS

## 🙏 致谢

- [SJTU-Canvas-Helper](https://github.com/Okabe-Rintarou-0/SJTU-Canvas-Helper) — 本项目的灵感来源
- [OpenClaw](https://github.com/openclaw/openclaw) — AI Agent 运行时

## 📄 License

[MIT](LICENSE)

---

Made with 🐺 by [小灰灰大人](https://github.com/xhh678876)
