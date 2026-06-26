# Smart Search 发布指南

## 📦 发布到 ClawHub

### 前置准备

1. **登录 ClawHub**
```bash
cd /home/admin/.openclaw/workspace/skills/smart-search
clawhub login
```
浏览器会自动打开，完成认证后返回终端。

2. **验证登录**
```bash
clawhub whoami
```

---

### 发布步骤

#### 方式 A：使用发布脚本（推荐）

```bash
cd /home/admin/.openclaw/workspace/skills/smart-search
chmod +x publish.sh
./publish.sh
```

#### 方式 B：手动发布

```bash
cd /home/admin/.openclaw/workspace/skills/smart-search

# 发布新版本
clawhub publish . \
  --slug smart-search \
  --name "Smart Search" \
  --version 2.0.0 \
  --changelog "v2.0.0: SearX 1.1.0 + Tavily 双引擎架构，智能场景识别，一键部署"
```

---

### 📝 更新现有版本

```bash
# 更新技能
clawhub update smart-search --force

# 或者重新发布
clawhub publish . --slug smart-search --version 2.0.0 --force
```

---

## 🎯 版本说明

### v2.0.0 新特性

**核心功能：**
- 🧠 智能场景识别（基于关键词自动选择引擎）
- 🔄 多层降级保障（SearX → Tavily → 错误处理）
- 💰 90% 搜索 0 成本（SearX 免费无限）
- 📚 完整文档（5 个文档文件）
- 🚀 一键部署（deploy-searx.sh）

**引擎对比：**
| 引擎 | 用途 | 成本 |
|------|------|------|
| SearX 1.1.0 | 日常搜索、新闻资讯 | 免费无限 |
| Tavily | AI 内容生成、备用 | 1000 次/月免费 |

**决策逻辑：**
- AI 内容生成（小红书、文案）→ Tavily
- 日常查询、新闻资讯 → SearX
- 用户指定 → 尊重选择

---

## 📋 文件清单

发布前检查以下文件：

```
smart-search/
├── SKILL.md              ✅ 技能说明
├── README.md             ✅ 决策参考
├── README.searx.md       ✅ SearX 部署指南
├── COMPARISON.md         ✅ 引擎对比
├── TAVILY_SETUP.md       ✅ Tavily 配置
├── search.sh             ✅ 主脚本（可执行）
├── deploy-searx.sh       ✅ 部署脚本（可执行）
├── _meta.json            ✅ 元数据
└── publish.sh            ✅ 发布脚本
```

---

## 🔧 故障排查

### 发布失败

**错误：Rate limit exceeded**
```bash
# 等待几分钟后重试
sleep 60
clawhub publish . --slug smart-search --version 2.0.0
```

**错误：Not logged in**
```bash
clawhub login
clawhub whoami  # 验证登录
```

**错误：Version already exists**
```bash
# 修改版本号
# 编辑 _meta.json，增加版本号
clawhub publish . --slug smart-search --version 2.0.1
```

---

## 📊 发布后验证

### 1. 检查发布状态
```bash
clawhub list | grep smart-search
```

### 2. 搜索技能
```bash
clawhub search "smart search"
```

### 3. 查看详情
```bash
clawhub info smart-search
```

---

## 🎉 发布成功后的事

### 推广建议

1. **更新文档**
   - 在 README 中添加 ClawHub 链接
   - 更新使用示例

2. **收集反馈**
   - 关注用户 issue
   - 及时修复 bug

3. **持续迭代**
   - 根据反馈优化
   - 定期更新版本

---

## 📚 相关资源

- **ClawHub 文档**: https://docs.clawhub.com
- **技能市场**: https://clawhub.com/skills
- **发布指南**: https://docs.clawhub.com/skills/publish

---

**准备就绪！** 执行以下命令开始发布：

```bash
cd /home/admin/.openclaw/workspace/skills/smart-search
clawhub login
./publish.sh
```
