# XHS Viral Factory 详细安装与使用说明

本技能旨在帮助你将任何形式的“死知识”转化为小红书上的“活流量”。

## 1. 安装前的准备 (Prerequisites)
- **Python 3.8+**: 核心运行环境。
- **pip 库**: 脚本依赖 `requests` 库。
  ```bash
  pip3 install requests
  ```
- **API 账号**: 你需要一个支持 OpenAI 协议的大模型密钥（推荐 DeepSeek）。

## 2. 三分钟上手指南 (Quick Start)

### 第一步：设置密钥
在终端执行（或放入 `~/.zshrc`）：
```bash
export LLM_API_KEY="你的 API Key"
export LLM_BASE_URL="https://api.deepseek.com" # 如果用 DeepSeek
export LLM_MODEL="deepseek-chat"               # 如果用 DeepSeek
```

### 第二步：运行脚本
```bash
python3 scripts/generate_xhs.py --source "/path/to/data" --output "./drafts"
```

## 3. 给 AI 代理的指令 (For AI Agents)
你可以直接对 AI 说：
> “使用 xhs-viral-factory 技能，分析 [文件夹路径] 并生成小红书笔记。”

## 4. 安全声明 (Security)
- **数据流向**：本 Skill 会读取本地资料，并通过加密 HTTPS 发送至你配置的模型供应商（如 OpenAI）。
- **隐私保护**：本 Skill 不会收集或上传你的 API Key。所有处理逻辑均在本地触发。
