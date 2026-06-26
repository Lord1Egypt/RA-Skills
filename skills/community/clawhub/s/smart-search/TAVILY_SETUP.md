# Tavily API Key 配置指南

## 🎯 为什么需要 Tavily？

虽然 **SearX 1.1.0** 可以处理 90% 的搜索需求，但 **Tavily** 在以下场景有独特优势：

| 场景 | SearX | Tavily |
|------|-------|--------|
| 日常搜索 | ✅ 完美 | ✅ 完美 |
| 新闻资讯 | ✅ 完美 | ✅ 完美 |
| **小红书文案** | ⚠️ 仅有链接 | ✅ AI 摘要 + 内容建议 |
| **内容总结** | ⚠️ 需手动阅读 | ✅ 自动提炼要点 |
| **AI 创作** | ⚠️ 无辅助 | ✅ AI 摘要辅助 |

---

## 🆓 免费额度

| 套餐 | 价格 | 月度额度 | 适用场景 |
|------|------|---------|---------|
| **Free** | $0 | 1000 次/月 | 个人使用 ✅ |
| Starter | $29 | 10000 次/月 | 小团队 |
| Pro | $99 | 50000 次/月 | 企业使用 |

**推荐：Free 套餐完全够用！**

---

## 📝 配置步骤（2 分钟）

### 1️⃣ 访问官网
```
https://tavily.com
```

### 2️⃣ 注册账号
- 点击 "Sign Up" 或 "Get Started"
- 使用邮箱或 GitHub 账号注册
- 验证邮箱

### 3️⃣ 获取 API Key
- 登录 Dashboard
- 找到 "API Keys" 或 "Settings"
- 复制你的 API Key（格式：`tvly-xxx-xxx-xxx`）

### 4️⃣ 配置到环境变量
```bash
# 编辑配置文件
nano ~/.openclaw/.env

# 添加（或替换）以下行
TAVILY_API_KEY=tvly-your-actual-key-here

# 保存退出（Ctrl+X, Y, Enter）
```

### 5️⃣ 验证配置
```bash
# 测试搜索（会用到 Tavily）
cd /home/admin/.openclaw/workspace/skills/smart-search
./search.sh "帮我总结 AI 最新进展" 5
```

**成功输出示例：**
```
🔍 Smart Search: 使用 tavily

📝 AI 摘要：
AI is transforming industries...

1. 第一条结果...
2. 第二条结果...

✅ 搜索成功（Tavily）
```

---

## 🧪 测试场景

配置完成后，测试以下场景：

### ✅ 日常搜索（用 SearX）
```bash
./search.sh "AI 新闻"
```
**预期：** 使用 SearX，免费无限

### ✅ AI 内容生成（用 Tavily）
```bash
./search.sh "小红书 AI 工具文案"
```
**预期：** 使用 Tavily，显示 AI 摘要

### ✅ 降级测试
```bash
# 临时注释 Tavily API Key
# TAVILY_API_KEY=tvly-xxx

./search.sh "小红书文案"
```
**预期：** 提示未配置 → 降级 SearX → 正常返回结果

---

## 💡 使用建议

### 推荐配置 Tavily 的场景
- ✅ 经常写小红书/公众号文案
- ✅ 需要快速总结长文章
- ✅ 做市场调研/竞品分析
- ✅ 需要 AI 辅助创作

### 可以不配置的场景
- ✅ 只用晨间简报（SearX 够用）
- ✅ 只做简单事实查询
- ✅ 预算有限（100% 免费优先）

---

## 🔧 常见问题

### Q1: API Key 无效？
**检查：**
```bash
# 查看配置的 Key
cat ~/.openclaw/.env | grep TAVILY

# 测试 API
curl -X POST https://api.tavily.com/search \
  -H "Authorization: Bearer tvly-your-key" \
  -d '{"query": "test"}'
```

**解决：** 重新从 Dashboard 复制，确保无空格

---

### Q2: 额度用完了？
**方案 A：多账号轮换**
```bash
# ~/.openclaw/.env
TAVILY_API_KEY=tvly-key1
TAVILY_API_KEY_2=tvly-key2  # 第二个账号
TAVILY_API_KEY_3=tvly-key3  # 第三个账号
```

**方案 B：等待下月重置**
- 免费额度每月 1 号重置
- 降级使用 SearX（无 AI 摘要）

**方案 C：升级付费**
- Starter: $29/月 = 10000 次
- 约 ¥0.02/次

---

### Q3: 孩子误操作删除了配置？
**恢复方法：**
```bash
# 重新编辑
nano ~/.openclaw/.env

# 添加 API Key
TAVILY_API_KEY=tvly-your-key

# 保存重启
```

---

## 📊 成本分析

### 个人使用（推荐 Free）
```
晨间简报：30 次/月
AI 内容：  30 次/月
────────────────────
总计：    60 次/月
免费额度：1000 次/月
剩余额度：940 次/月 ✅
月度成本：¥0
```

### 高频使用（考虑 Starter）
```
晨间简报：30 次/月
AI 内容： 200 次/月
调研分析：100 次/月
────────────────────
总计：   330 次/月
免费额度：1000 次/月
月度成本：¥0（仍在免费内）✅
```

---

## 🎁 总结

**必配理由：**
1. 🆓 免费 1000 次/月（个人完全够用）
2. 🤖 AI 摘要功能（SearX 没有）
3. ⚡ 响应速度快（1-1.5 秒）
4. 🛡️ 稳定可靠（云服务）

**配置难度：** ⭐⭐⭐⭐⭐（5 星最简单）  
**配置时间：** 2 分钟  
**月度成本：** ¥0

---

**立即获取：** https://tavily.com
