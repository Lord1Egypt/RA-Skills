---
name: Self-Check
slug: self-check
version: 2.0.0
description: "系统自检工具。全面检查环境配置、文件完整性、权限、依赖、API token 等，并汇报问题给出修复建议（但不主动修复）。"
metadata: {"clawdbot":{"emoji":"🔍","requires":{"bins":["node","npm","nvm"],"os":["linux","darwin"]},"configPaths":[".openclaw/"]}}
---

## When to Use

- 用户要求进行系统自检
- 环境更新后验证配置
- 排查问题前的基础检查
- 定期健康检查

## 核心原则 ⚠️

**只检查、汇报、建议，绝不主动修复**

- ❌ 不自动安装任何包
- ❌ 不自动修改任何配置文件
- ❌ 不自动重启任何服务
- ✅ 只汇报发现的问题
- ✅ 只给出修复建议命令
- ✅ 等待用户确认后再执行修复

## 自检项目

### 1. Node.js 环境
- [ ] Node.js 版本（需 >= 22.12.0）
- [ ] nvm 是否可用
- [ ] npm 版本

### 2. OpenClaw 核心
- [ ] Gateway 状态
- [ ] Gateway 进程 node 版本
- [ ] 插件加载状态（acpx, qqbot, discord 等）

### 3. 配置文件
- [ ] openclaw.json 语法正确
- [ ] 必要的 channel 配置存在

### 4. Agent 文件
- [ ] SOUL.md 存在（必需）
- [ ] USER.md 存在（必需）
- [ ] AGENTS.md 存在（必需）
- [ ] MEMORY.md 存在（可选，用于长期记忆）
- [ ] memory/ 目录（每日记录）
- [ ] self-improving/ 目录（学习记忆）

### 5. Skills 详细检查
- [ ] skill 目录结构完整（SKILL.md, scripts/, config.json）
- [ ] Python 模块依赖是否安装
- [ ] 外部工具是否可用

### 6. MCP 检查
- [ ] acpx 插件版本
- [ ] acpx 二进制文件
- [ ] acpx 运行时后端状态

### 7. API Token
- [ ] 环境变量中的 API key
- [ ] 配置文件中的 API key（不显示值）

### 8. 权限
- [ ] workspace 目录权限
- [ ] .openclaw 目录权限
- [ ] skills 目录可写性

## 输出格式

```
# 🔍 自检报告

## ✅ 通过项
- Node.js (nvm): v22.22.1 ✅
- Gateway: 运行中 ✅

## ⚠️ 警告项
- telegram: 未启用（可选）

## ❌ 问题项
### 1. 🔴 Skill aliyun-stt: 缺少 Python 模块 'dashscope'
   修复建议: pip3 install dashscope --break-system-packages
   ⚠️ 请手动执行上述命令，不要自动修复
```

## 执行方式

```bash
python3 ~/.openclaw/workspace-ptilopsis/skills/self-check/scripts/self_check.py
```

## 注意事项

- **绝不主动修复** - 只汇报问题和建议
- 所有修复命令需用户手动执行
- 敏感信息（如 token）只显示是否配置，不显示值
- 检查结果按严重程度排序（错误 > 警告 > 通过）
