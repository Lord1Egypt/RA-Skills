---
name: "youdaonote"
description: "安全地操作用户的有道云笔记，支持读取、搜索、创建笔记。当用户要求操作有道云笔记时调用。"
---

# Youdao Note Skill

这个 Skill 允许大模型代理安全地操作用户的有道云笔记 (Youdao Note)。
使用 Cookie 认证（从浏览器 F12 获得），**所有凭证通过环境变量 `YOUDAO_COOKIE` 注入脚本**，不硬编码、不在对话中明文传输。

## 核心能力
1. **列出目录**：`list` — 获取根目录或指定目录下的所有文件和文件夹。
2. **搜索笔记**：`search` — 通过关键词搜索云笔记。
3. **读取笔记**：`read` — 通过 File ID 获取云笔记内容。
4. **创建笔记**：`create` — 在指定目录下创建新笔记。

## 环境变量设置

### 获取完整 Cookie
1. 在浏览器打开 [有道云笔记网页版](https://note.youdao.com/) 并登录。
2. 按 `F12` → 切换到 **Network** 面板 → 刷新页面。
3. 点击任意一个 XHR 请求（如 `check-alive`）。
4. 在 **Request Headers** 中找到 `Cookie`，复制完整字符串值。

### 设置环境变量
**Windows (PowerShell)**：
```powershell
[System.Environment]::SetEnvironmentVariable(
    "YOUDAO_COOKIE",
    "从浏览器复制的完整Cookie字符串",
    "User"
)
```

> ⚠️ 添加到**用户变量**即可，不需要系统变量。重启终端让变量生效。

## 代理使用指南

### 1. 搜索笔记 (推荐作为入口)
如果不知道目录 ID，可以直接搜索，从搜索结果中获取目录和文件 ID：
```bash
py youdao_api.py search "关键词"
```

### 2. 列出指定目录文件
由于部分账号结构问题，默认根目录获取可能失败，推荐直接通过 URL 或搜索结果获取目录 ID（如 `WEBe72b0f1a...`）：
```bash
py youdao_api.py list --dir "目录ID"
```

### 3. 读取单篇笔记内容
```bash
py youdao_api.py read "笔记的FileID"
```

### 4. 读取目录下所有笔记
这个命令会遍历指定目录，把该目录下**所有非文件夹**的笔记内容一次性读取出来：
```bash
py youdao_api.py read_all "目录ID"
```

### 5. 创建新笔记
```bash
# 在指定目录创建（推荐）
py youdao_api.py create "标题" "内容" --dir "目录ID"
```

## 工作流 (Workflow)

当用户发出诸如 **“分析我的有道工作日志文件夹”** 的指令时，代理应遵循以下自动化工作流，将“读取”与“分析”一步完成：

1. **定位目标**：
   使用 `search` 命令或基于用户提供的关键词查找目标文件夹（如“工作日志”）。
   ```bash
   py youdao_api.py search "工作日志"
   ```
2. **批量读取**：
   获取到目标文件夹的 ID 后，使用 `read_all` 命令一键提取该目录下所有的笔记内容。
   ```bash
   py youdao_api.py read_all "文件夹ID"
   ```
3. **自动深度分析（关键步）**：
   在获取到日志内容后，代理**不要仅限于展示内容**，必须主动对数据进行综合分析。例如：
   - **梳理核心进展**：提取关键的工作成果与里程碑。
   - **识别风险与待办**：提炼出尚未解决的问题（Blockers）或后续计划（To-Dos）。
   - **趋势与高频主题**：总结这段时间内主要投入精力的工作方向。
   - 最终向用户输出一份结构化、清晰的分析报告（如使用 Markdown 表格、项目符号等）。

## 安全规范
- **禁止** 在代码或对话中硬编码 Cookie。
- **禁止** 要求用户直接在聊天窗口输入凭证。
- 所有认证均通过环境变量完成。
