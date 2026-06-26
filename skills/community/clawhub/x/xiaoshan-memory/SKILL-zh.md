# 小山记忆引擎

AI 的持久记忆 — 语义向量搜索、知识图谱、记忆蒸馏和分析。

## 快速开始

1. 安装：`npx clawhub@latest install xiaoshan-memory`
2. 配置 AI 提供商（编辑 `~/.xiaoshan/config.yaml`）
3. 启动：`python scripts/start_server.py`

支持的提供商：OpenAI、智谱AI、DeepSeek、Ollama（本地）

## 核心 API

| 端点 | 方法 | 说明 |
|------|------|------|
| /save | POST | 保存新记忆 |
| /search | POST | 语义搜索记忆 |
| /ask | POST | 基于记忆问答 |
| /stats | GET | 获取统计信息 |
| /list | GET | 列出最近记忆 |
| /kg/stats | GET | 知识图谱统计 |
| /forget | POST | 删除记忆 |

服务默认运行在 `127.0.0.1:18790`

## 配置

通过环境变量设置提供商凭证：

| 变量 | 说明 |
|------|------|
| `OPENAI_API_KEY` | OpenAI 密钥 |
| `ZHIPU_API_KEY` | 智谱AI 密钥 |
| `DEEPSEEK_API_KEY` | DeepSeek 密钥 |

或直接编辑 `~/.xiaoshan/config.yaml`

## 决策指南

| 用户说 | 操作 |
|--------|------|
| "记住" | POST /save |
| "搜索记忆" | POST /search |
| "知识图谱" | GET /kg/stats |
| "删除记忆" | POST /forget |
