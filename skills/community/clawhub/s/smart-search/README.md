# Smart Search v4.0 - 免费无限搜索

**Exa MCP（主力·零配置·免费无限）+ SearX（隐私）+ Tavily（AI 摘要）**

---

## 🎉 核心特性

- ✅ **零配置** - 无需任何 API Key，开箱即用
- ✅ **免费无限** - Exa MCP 官方免费，无次数限制
- ✅ **三引擎** - Exa MCP + SearX + Tavily，智能切换
- ✅ **隐私保护** - 敏感查询自动使用 SearX
- ✅ **AI 摘要** - 可选 Tavily 支持内容创作

---

## 🚀 快速开始

### 1. 零配置！直接用

```bash
# 不需要配置任何 API Key
# 直接运行即可
./search.sh "AI 最新新闻"
```

### 2. 可选配置（增强功能）

```bash
# ~/.openclaw/.env

# SearX（隐私保护，可选）
SEARXNG_URL=http://localhost:8080

# Tavily（AI 摘要，可选）
TAVILY_API_KEY=your_tavily_key_here
```

### 3. 使用示例

```bash
# 日常搜索 → Exa MCP
./search.sh "AI 最新新闻"

# 技术查询 → Exa MCP
./search.sh "Python async 教程"

# 隐私查询 → SearX
./search.sh "本地隐私配置"

# AI 创作 → Tavily（需配置）
./search.sh "小红书文案怎么写"

# 指定引擎
./search.sh "用 searx 搜索 XXX"
```

---

## 📊 引擎对比

| 引擎 | 定位 | 使用场景 | 成本 |
|------|------|----------|------|
| **Exa MCP** | 主力 (70%) | 技术/商业/学术搜索、日常查询 | 免费无限 ✅ |
| **SearX** | 隐私 (20%) | 隐私敏感查询 | 免费无限 |
| **Tavily** | AI 摘要 (10%) | 内容创作 | 免费 1000 次/月 |

---

## 💰 成本优势

### v3.0 vs v4.0

**v3.0（Exa API）：**
```
免费额度：1000 次（一次性）
用完后：¥50/1000 次
月成本：¥50/月
年成本：¥600/年
```

**v4.0（Exa MCP）：**
```
免费额度：♾️ 无限
用完后：¥0（永远免费）
月成本：¥0/月 ✅
年成本：¥0/年 ✅
```

**年度节省：¥600/年！**

---

## 🎯 智能场景识别

| 场景 | 关键词 | 引擎 | 原因 |
|------|--------|------|------|
| 技术搜索 | API、GitHub、教程 | Exa MCP | 结构化数据，精准 |
| 深度研究 | 深度分析、行业调研 | Exa MCP | 专业数据源 |
| 隐私查询 | 密码、隐私、本地 | SearX | 无追踪保护 |
| AI 创作 | 文案、总结、生成 | Tavily | AI 摘要辅助 |
| 日常查询 | 新闻、资讯、是什么 | Exa MCP | 快速全面 |

---

## 🛠️ 部署指南

### Exa MCP（主力）
- ✅ **零配置** - 无需注册，无需 API Key
- ✅ **开箱即用** - 直接调用官方服务

### SearX（隐私保护，可选）
```bash
cd /home/admin/.openclaw/workspace/skills/smart-search
chmod +x deploy-searx.sh
./deploy-searx.sh
```

### Tavily（AI 摘要，可选）
1. 访问 https://tavily.com
2. 注册免费账号（1000 次/月）
3. 获取 API Key
4. 添加到 `~/.openclaw/.env`

---

## 📝 使用示例

**日常搜索**
```
问：AI 最新进展
→ Exa MCP（免费无限）
```

**技术文档**
```
问：Python async/await 教程
→ Exa MCP（精准技术结果）
```

**隐私查询**
```
问：本地隐私配置方法
→ SearX（隐私保护）
```

**AI 创作**
```
问：帮我写小红书文案
→ Tavily（带 AI 摘要）
```

**指定引擎**
```
问：用 tavily 搜索 XXX
→ Tavily（尊重用户选择）
```

---

## 🔧 故障排查

### Exa MCP 测试
```bash
curl -X POST https://mcp.exa.ai/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc": "2.0", "id": 1, "method": "tools/list"}'
```

### SearX 检查
```bash
docker ps | grep searx
docker logs searx --tail 20
docker restart searx
```

### 降级日志
```
🔍 Smart Search v4.0: 使用 exa
⚠️  Exa MCP 暂时不可用，降级到 SearX...
✅ 共找到 5 条结果（SearX 隐私保护）
```

---

## 💡 架构优势

### 为什么选择 Exa MCP？

| 特性 | Exa MCP | Exa API | SearX |
|------|---------|---------|-------|
| **费用** | 免费无限 | ¥50/1000 次 | 免费无限 |
| **配置** | 零配置 | 需要 API Key | 需要部署 |
| **响应速度** | ~1s | ~500ms | ~2s |
| **结果质量** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |

**Exa MCP 核心优势：**
- 🎯 **官方免费** - Exa 官方提供的免费服务
- 🔌 **零配置** - 无需注册，无需 API Key
- ♾️ **无限使用** - 没有次数限制
- 📊 **高质量** - 1B+ 页面索引，精准搜索
- 🚀 **快速响应** - 通常 1 秒内返回

---

## ❓ 常见问题

### Q: Exa MCP 真的完全免费吗？
**A:** 是的！Exa 官方免费提供的 MCP 服务，没有次数限制。

### Q: 为什么还要配置 SearX 和 Tavily？
**A:** 
- **SearX**：隐私保护场景（本地部署，无外部请求）
- **Tavily**：AI 内容生成（带 AI 摘要，辅助创作）

### Q: Exa MCP 和 Exa API 有什么区别？
**A:**
- **MCP**：免费无限，零配置，基础搜索功能
- **API**：付费（有免费赠额），完整功能，可自定义参数

### Q: 适合什么场景使用？
**A:** 
- ✅ 个人日常搜索
- ✅ 技术文档查询
- ✅ 新闻资讯获取
- ✅ 学术研究
- ✅ 商业调研

---

## 📚 文档

- [SKILL.md](SKILL.md) - 完整技能文档（v4.0.0）
- [SKILL.en.md](SKILL.en.md) - English documentation
- [CHANGELOG.md](CHANGELOG.md) - 变更日志
- [README.searx.md](README.searx.md) - SearX 部署指南
- [TAVILY_SETUP.md](TAVILY_SETUP.md) - Tavily 配置指南

---

**版本：** 4.0.0（Exa MCP 免费无限）  
**最后更新：** 2026-03-30  
**作者：** Li Yang (@Lee920311)

**变更日志：**
- v4.0 - 使用 Exa MCP，零配置，免费无限
- v3.0.4 - Exa API + SearX + Tavily 三引擎
- v2.0 - SearX + Tavily 双引擎
