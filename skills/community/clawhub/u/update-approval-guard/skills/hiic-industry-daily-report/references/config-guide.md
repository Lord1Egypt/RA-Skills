# HIIC日报配置指南

## 📖 配置系统说明

HIIC日报支持自定义配置，你可以：

- ✅ 添加自己的RSS数据源
- ✅ 修改产业关键词
- ✅ 添加自定义产业
- ✅ 调整主题映射

---

## 🚀 快速开始

### 1. 查看默认配置

```bash
# 查看产业配置
cat config/defaults/industries.json

# 查看数据源配置
cat config/defaults/sources.json

# 查看主题配置
cat config/defaults/topics.json
```

### 2. 创建自定义配置

```bash
# 1. 创建工作区配置目录
mkdir -p workspace/config

# 2. 复制默认配置
cp config/defaults/*.json workspace/config/

# 3. 编辑配置
vim workspace/config/sources.json
```

### 3. 使用自定义配置

```bash
# 方式1：使用默认配置
node scripts/generate-report.mjs --industry "人工智能"

# 方式2：使用自定义配置
node scripts/generate-report.mjs \
  --industry "人工智能" \
  --config workspace/config
```

---

## 📋 配置文件详解

### industries.json（产业配置）

```json
{
  "industries": [
    {
      "id": "artificial-intelligence",        // 产业唯一标识
      "name": "人工智能",                      // 产业名称
      "keywords": ["人工智能", "AI", "大模型"], // 搜索关键词
      "topics": ["llm", "ai-agent"],          // 映射到 tech-news-digest 主题
      "enabled": true,                         // 是否启用
      "priority": true,                        // 是否高优先级
      "category": "战略性新兴产业"             // 产业分类
    }
  ]
}
```

**字段说明**：

- `id`: 唯一标识，用于命令行参数
- `name`: 显示名称，用于日报标题
- `keywords`: 搜索关键词数组，用于搜索引擎
- `topics`: tech-news-digest 主题数组，用于数据源映射
- `enabled`: 是否启用（false 则跳过）
- `priority`: 高优先级产业会优先处理
- `category`: 产业分类（战略性新兴产业/先进制造业/未来产业）

**支持的 topics**：

- `llm`: 大语言模型（GPT、Claude、Gemini等）
- `ai-agent`: AI代理（机器人、自动驾驶等）
- `frontier-tech`: 前沿科技（新材料、生物医药等）
- `crypto`: 加密货币（区块链、Web3等）

---

### sources.json（数据源配置）

```json
{
  "sources": [
    {
      "id": "my-custom-rss",                  // 数据源唯一标识
      "type": "rss",                           // 数据源类型
      "name": "我的博客",                      // 数据源名称
      "url": "https://blog.example.com/feed",  // RSS地址
      "enabled": true,                         // 是否启用
      "priority": false,                       // 是否高优先级
      "topics": ["llm"],                       // 关联的主题
      "note": "个人技术博客"                   // 备注
    }
  ]
}
```

**支持的数据源类型**：

- `rss`: RSS/Atom 订阅源
- `twitter`: Twitter/X 账号（需要API密钥）
- `github`: GitHub 仓库
- `reddit`: Reddit 子版块
- `web`: 网页搜索

---

### topics.json（主题配置）

```json
{
  "topics": [
    {
      "id": "llm",                             // 主题ID
      "label": "大语言模型",                   // 显示名称
      "description": "LLM、GPT相关",           // 描述
      "emoji": "🤖"                            // Emoji图标
    }
  ]
}
```

---

## 💡 使用示例

### 示例1：添加自定义RSS源

**步骤**：

1. 创建自定义配置：

```bash
mkdir -p workspace/config
cat > workspace/config/sources.json << 'EOF'
{
  "sources": [
    {
      "id": "my-tech-blog",
      "type": "rss",
      "name": "我的技术博客",
      "url": "https://blog.example.com/feed.xml",
      "enabled": true,
      "priority": true,
      "topics": ["llm", "ai-agent"]
    }
  ]
}
EOF
```

2. 使用自定义配置生成日报：

```bash
node scripts/generate-report.mjs \
  --industry "人工智能" \
  --config workspace/config
```

**效果**：

- ✅ 日报会包含你的博客文章
- ✅ 自动去重和排序
- ✅ 与其他数据源合并

---

### 示例2：修改产业关键词

**场景**：你想让人工智能日报也包含 "大语言模型" 和 "LLM" 关键词

**步骤**：

1. 复制默认配置：

```bash
mkdir -p workspace/config
cp config/defaults/industries.json workspace/config/
```

2. 修改配置：

```bash
vim workspace/config/industries.json
```

找到人工智能产业，修改 keywords：

```json
{
  "id": "artificial-intelligence",
  "name": "人工智能",
  "keywords": [
    "人工智能",
    "AI",
    "大模型",
    "GPT",
    "机器学习",
    "深度学习",
    "大语言模型",  // 新增
    "LLM",         // 新增
    "AGI"          // 新增
  ],
  "topics": ["llm", "ai-agent"],
  "enabled": true,
  "priority": true,
  "category": "战略性新兴产业"
}
```

3. 使用自定义配置：

```bash
node scripts/generate-report.mjs \
  --industry "人工智能" \
  --config workspace/config
```

---

### 示例3：添加自定义产业

**场景**：你想跟踪 "Web3" 产业，但这不在默认的28个产业中

**步骤**：

1. 创建自定义产业配置：

```bash
mkdir -p workspace/config
cat > workspace/config/industries.json << 'EOF'
{
  "industries": [
    {
      "id": "web3",
      "name": "Web3",
      "keywords": ["Web3", "区块链", "DeFi", "NFT", "DAO"],
      "topics": ["crypto"],
      "enabled": true,
      "priority": true,
      "category": "自定义产业"
    }
  ]
}
EOF
```

2. 生成自定义产业日报：

```bash
node scripts/generate-report.mjs \
  --industry "Web3" \
  --config workspace/config
```

---

## 🔧 高级用法

### 1. 验证配置

```bash
# 验证配置文件格式
python3 scripts/validate-config.py

# 输出
=== HIIC日报配置验证 ===

📄 验证 industries.json...
✅ 验证通过 (28 个产业)

📄 验证 sources.json...
✅ 验证通过 (0/1 个数据源启用)

📄 验证 topics.json...
✅ 验证通过 (4 个主题)

🎉 所有配置验证通过！
```

### 2. 查看配置

```bash
# 查看合并后的配置
node scripts/config-loader.mjs

# 查看自定义配置
node scripts/config-loader.mjs workspace/config
```

### 3. 配置优先级

**合并规则**：

1. 默认配置（`config/defaults/`）
2. 自定义配置（`--config` 指定的目录）
3. 自定义配置会**覆盖**同名的默认配置

**示例**：

- 默认 `industries.json` 中有 "人工智能" 产业
- 自定义 `industries.json` 中也有 "人工智能" 产业
- **结果**：使用自定义的 "人工智能" 配置

---

## 📊 配置最佳实践

### 1. 关键词优化

**✅ 好的关键词**：

- 具体：`"GPT-4"` 而不是 `"AI"`
- 多样：`["人工智能", "AI", "大模型"]`
- 时效：包含最新术语

**❌ 避免的关键词**：

- 太宽泛：`"技术"`、`"创新"`
- 太狭窄：`"GPT-4-turbo-0125"`
- 过时：`"AlphaGo"`

### 2. 数据源选择

**推荐的数据源**：

- ✅ 官方博客（OpenAI、DeepMind等）
- ✅ 技术媒体（机器之心、量子位等）
- ✅ 学术博客（arXiv、Papers with Code等）
- ✅ 社区讨论（Reddit、Hacker News等）

**避免的数据源**：

- ❌ 内容农场
- ❌ 营销号
- ❌ 低质量转载

### 3. 配置管理

**推荐结构**：

```
workspace/
├── config/           # 自定义配置
│   ├── industries.json
│   ├── sources.json
│   └── topics.json
└── reports/          # 生成的日报
```

**版本控制**：

```bash
# 将配置加入 Git
cd workspace
git init
git add config/
git commit -m "初始配置"
```

---

## 🐛 故障排查

### 问题1：配置不生效

**检查**：

```bash
# 1. 验证配置格式
python3 scripts/validate-config.py

# 2. 查看合并后的配置
node scripts/config-loader.mjs workspace/config

# 3. 确认配置路径正确
ls -la workspace/config/
```

### 问题2：数据源未抓取

**检查**：

1. 数据源的 `enabled` 是否为 `true`
2. RSS URL 是否可访问
3. 查看运行日志（`--verbose`）

### 问题3：产业匹配不到

**检查**：

1. 产业的 `enabled` 是否为 `true`
2. 关键词是否正确
3. topics 是否与数据源匹配

---

## 📚 相关文档

- [配置模板](../references/config-template.json)
- [快速参考](../references/quick-reference.md)
- [定时任务配置](../references/cron-guide.md)

---

**🎯 配置系统让日报更灵活，满足个性化需求！**
