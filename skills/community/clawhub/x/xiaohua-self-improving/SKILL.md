---
name: xiaohua-self-improving
description: "小花专用自我迭代技能 - 基于 self-improving-agent 增强，集成 OpenClaw 工作流、MEMORY.md、百度千帆、看想做找四部曲。专为国内部署优化。"
metadata:
  version: "1.0.0"
  author: "HuaNiu-Team"
  fork-of: "self-improving-agent"
  openclaw_native: true
  china_optimized: true
---

# 小花自我迭代 (HuaNiu Enhanced)

> 🌸 **小花定制版**: 基于 `self-improving-agent` fork，专为 OpenClaw + 国内环境优化。集成 MEMORY.md、看想做找工作流、百度千帆 API、生产环境实战模式。

## 快速开始

```bash
# 安装
npx clawhub install xiaohua-self-improving

# 使用后记录
# 1. 错误 → .learnings/ERRORS.md
# 2. 修正 → .learnings/LEARNINGS.md
# 3. 功能请求 → .learnings/FEATURE_REQUESTS.md
# 4. 通用知识 → 提升到 MEMORY.md
```

## 核心增强

### 1. OpenClaw 原生集成

- ✅ 自动加载到 `~/.openclaw/workspace/`
- ✅ 与 `AGENTS.md`、`SOUL.md`、`TOOLS.md` 联动
- ✅ 支持 `memory/YYYY-MM-DD.md` 日常记录
- ✅ 与 `WORKFLOW_AUTO.md` 看想做找流程整合

### 2. MEMORY.md 提升工作流

```
.learnings/LEARNINGS.md  (详细上下文)
         ↓
   MEMORY.md  (团队通用知识)
         ↓
   SOUL.md  (行为准则/人格)
         ↓
   TOOLS.md  (工具使用模式)
```

### 3. 国内友好配置

- 🔍 **搜索**: 百度千帆 API (`baidu-search` 技能)
- 🧠 **记忆**: local-file-rag-basic 或 scripts/memory_search.py
- 🤖 **模型**: 阿里云千帆 / Ollama 本地
- 🌐 **部署**: 无需 VPN，全国内服务

### 4. 生产环境模式

- 上下文窗口修复流程 (配置→验证→重启)
- 技能安装测试规范 (装一个→测一个→记一个)
- 错误追踪模板 (标准化 ERR-XXX 格式)
- 日常记忆追加协议 (APPEND only)

## 文件结构

```
~/.openclaw/workspace/
├── AGENTS.md              # 多智能体工作流
├── SOUL.md                # 人格/行为准则
├── TOOLS.md               # 工具能力/坑点
├── MEMORY.md              # 长期记忆 (主会话)
├── memory/                # 日常记忆 (YYYY-MM-DD.md)
├── WORKFLOW_AUTO.md       # 看想做找四部曲
├── HEARTBEAT.md           # 状态监控
├── USER.md                # 主人偏好
└── .learnings/            # 本技能日志
    ├── LEARNINGS.md
    ├── ERRORS.md
    └── FEATURE_REQUESTS.md
```

## 使用示例

### 记录错误

```markdown
### [ERR-20260302-002] ChromaDB 不兼容 Python 3.14

**Logged**: 2026-03-02T15:45:00+08:00
**Priority**: high
**Status**: workaround
**Area**: dependencies

### Summary
ChromaDB 1.5.2 与 Python 3.14 不兼容 (Pydantic v1 问题)

### Error
```
pydantic.v1.errors.ConfigError: unable to infer type for attribute "chroma_server_nofile"
```

### Context
- Python: 3.14.0
- ChromaDB: 1.5.2
- Pydantic v1 已停止维护

### Suggested Fix
1. 临时：使用 local-file-rag-basic
2. 长期：等 ChromaDB 更新兼容版本
3. 替代：FAISS 或 LanceDB

### Metadata
- Reproducible: yes
- Tags: chromadb, python3.14, pydantic
- See Also: LRN-20260302-003
```

### 提升到 MEMORY.md

```markdown
## 主人的教导记录
### 2026-03-02
- Tool Call ID 格式：9 位字符 (A-Z, a-z, 0-9)，禁用特殊符号
- 上下文窗口：以实际 API 返回为准 (阿里云千帆编码版 32K，非文档 131K)
- PowerShell JSON：复杂管道易错，直接写文件更安全
```

### 看想做找工作流

```markdown
## 看 (Look)
- 读取 WORKFLOW_AUTO.md、MEMORY.md、HEARTBEAT.md
- 扫描主人消息语气和情绪

## 想 (Think)
- 分析意图和优先级
- 匹配响应风格

## 找 (Find)
- 搜索 MEMORY.md 相关知识
- web_search / baidu-search 查找信息
- 检查 .learnings/ 避免重复错误

## 做 (Do)
- 执行任务
- 记录结果到 .learnings/
- 提升到 MEMORY.md (如适用)
- 验证输出质量
```

## 最佳实践

1. **立即记录** - 上下文最新鲜
2. **具体详细** - 未来智能体需要快速理解
3. **包含复现步骤** - 特别是错误
4. **链接相关文件** - 便于修复
5. **建议具体方案** - 不只是"调查"
6. **使用一致分类** - 便于筛选
7. **积极提升** - 有疑问就加到 MEMORY.md
8. **定期回顾** - 过时的学习会贬值
9. **工作流自动化** - 遵循看想做找
10. **国内部署** - 用百度 API、本地模型、国内工具

## 实战模式

### 模式 1: 日常记忆追加

更新 `memory/YYYY-MM-DD.md` 时:
- **只追加 (APPEND)**，绝不覆盖
- 用时间戳标题：`## ✅ 下午技术修复完成 (2026-03-02 16:00)`
- 包含文件清单便于追溯

### 模式 2: 错误追踪

使用 `.learnings/ERRORS.md` 模板:
```markdown
### [ERR-YYYYMMDD-XXX] skill_name

**Logged**: ISO 时间戳
**Priority**: high/medium/low
**Status**: pending/workaround/fixed
**Area**: dependencies/config/skill/other

### Summary
一句话描述

### Error
```
实际错误信息
```

### Context
- 环境细节
- 尝试了什么

### Suggested Fix
临时方案或永久修复

### Metadata
- Reproducible: yes/no
- Tags: 逗号分隔
- See Also: LRN-XXX (如相关)
```

### 模式 3: 上下文窗口修复

当模型上下文与文档不符时:
1. 检查实际 API 返回值
2. 更新 `openclaw.json` 匹配现实
3. 重启网关：`Stop-Process` → 等 2 秒 → `openclaw gateway`
4. 记录到 MEMORY.md 作为技术修复

### 模式 4: 技能安装

- **一个一个装**: `clawhub install` 只接受单个 slug
- **装完测试**: 验证功能再依赖
- **记录 bug**: 坏了就加到 `.learnings/ERRORS.md`

## 与其他技能协作

| 技能 | 协作方式 |
|------|----------|
| `baidu-search` | 国内搜索替代 Brave/Tavily |
| `local-file-rag-basic` | 本地记忆检索 (ChromaDB 不兼容时) |
| `clawhub` | 技能安装/发布/更新 |
| `ollama-local` | 本地模型部署 (无需 API) |
| `deep-research-pro` | 深度研究 (需配置 Tavily API) |

## 已知限制

- ❌ `baidu-academic` 技能不存在 (clawhub 无此技能)
- ❌ ChromaDB 不兼容 Python 3.14+ (Pydantic v1 问题)
- ❌ `local-file-rag-basic` 可能有 bug (`CodeChunker is not defined`)
- ⚠️ Tavily 搜索国内信息效果差 (返回英文结果)

## 更新日志

### v1.0.0 (2026-03-02)
- ✅ 基于 self-improving-agent fork
- ✅ OpenClaw 原生集成
- ✅ MEMORY.md 提升工作流
- ✅ 百度千帆 API 配置
- ✅ 看想做找自动化
- ✅ 生产环境实战模式
- ✅ 国内部署优化
- ✅ 错误追踪模板
- ✅ 上下文窗口修复流程

## 参考

- 原始技能：https://github.com/peterskoett/self-improving-agent
- OpenClaw 文档：https://docs.openclaw.ai
- ClawHub: https://clawhub.com
- 小花文档：`C:\Users\qwe12\.openclaw\workspace\`

---

*🌸 小花出品，必属精品 - 持续迭代，越用越聪明*
