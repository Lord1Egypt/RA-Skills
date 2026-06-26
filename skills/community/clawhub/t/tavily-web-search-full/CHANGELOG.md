# Tavily Web Search Skill - 更新总结

## 📦 版本 2.0.0 更新内容（重大更新）

### 新增 API（默认禁用）

#### 1. Crawl API（网站爬取）⚠️
- **脚本**: `scripts/crawl.py`
- **成本**: 3-5 信用/10 页
- **安全控制**: 必须使用 `--enable` 标志
- **特性**:
  - ✅ 智能网站遍历
  - ✅ 自然语言指令
  - ✅ 深度/广度控制
  - ✅ 路径/域名过滤
  - ✅ 自动缓存（2 小时）

**使用示例**:
```bash
# 必须使用 --enable
python3 scripts/crawl.py --url "https://example.com" --enable

# 带指令
python3 scripts/crawl.py --url "https://example.com" --enable --instructions "find all pricing pages"
```

#### 2. Map API（网站地图）⚠️
- **脚本**: `scripts/map.py`
- **成本**: 1-2 信用/10 页
- **安全控制**: 必须使用 `--enable` 标志
- **特性**:
  - ✅ 快速生成网站地图
  - ✅ 自然语言指令
  - ✅ 多种输出格式（包括 URL 列表）
  - ✅ 自动缓存

**使用示例**:
```bash
# 必须使用 --enable
python3 scripts/map.py --url "https://example.com" --enable

# 输出 URL 列表
python3 scripts/map.py --url "https://example.com" --enable --output urls
```

#### 3. Research API（深度研究）⚠️⚠️
- **脚本**: `scripts/research.py`
- **成本**: 4-250 信用/次（非常贵！）
- **安全控制**: 必须使用 `--enable --confirm` 双重确认
- **特性**:
  - ✅ 深度研究报告
  - ✅ 两种模型（mini/pro）
  - ✅ 多源分析
  - ✅ 自动缓存（24 小时）

**使用示例**:
```bash
# 必须使用 --enable AND --confirm
python3 scripts/research.py --query "AI impact on healthcare" --enable --confirm

# Pro 模型
python3 scripts/research.py --query "market analysis" --model pro --enable --confirm
```

### 安全控制策略

| API | 默认状态 | 启用要求 | 原因 |
|-----|---------|---------|------|
| Search | ✅ 启用 | 无 | 便宜（1-2 信用） |
| Extract | ✅ 启用 | 无 | 便宜（1-2 信用/5 URL） |
| Usage | ✅ 启用 | 无 | 免费 |
| Crawl | ❌ 禁用 | `--enable` | 较贵（3-5 信用/10 页） |
| Map | ❌ 禁用 | `--enable` | 中等（1-2 信用/10 页） |
| Research | ❌ 禁用 | `--enable --confirm` | 极贵（4-250 信用） |

### 设计理念

1. **日常 API 默认启用** - Search/Extract/Usage 足够满足 90% 场景
2. **高级 API 需要确认** - 防止误用导致信用快速消耗
3. **研究 API 双重确认** - 极端成本，必须明确意图

---

## 📦 版本 1.1.0 更新内容

### 新增功能

#### 1. Extract API（URL 内容提取）
- **脚本**: `scripts/extract.py`
- **功能**: 从指定 URL 提取完整内容
- **成本**: 1 信用/5 个 URL（basic）或 2 信用/5 个 URL（advanced）
- **特性**:
  - ✅ 支持单个或多个 URL
  - ✅ 查询重排（按相关性排序内容块）
  - ✅ 两种提取深度（basic/advanced）
  - ✅ 支持图片提取
  - ✅ 支持 favicon
  - ✅ 多种输出格式（markdown/text/JSON）
  - ✅ 自动缓存

**使用示例**:
```bash
# 提取单个 URL
python3 scripts/extract.py --urls "https://example.com/article"

# 提取多个 URL
python3 scripts/extract.py --urls "https://a.com,https://b.com"

# 带查询提取（重排内容）
python3 scripts/extract.py --urls "https://example.com" --query "find pricing info"
```

#### 2. Usage API（使用量查询）
- **脚本**: `scripts/usage.py`
- **功能**: 查询 API 使用量和信用余额
- **成本**: 免费
- **特性**:
  - ✅ 显示已用/剩余/总信用
  - ✅ 可视化使用进度条
  - ✅ 按端点分类统计
  - ✅ 支持项目过滤
  - ✅ 多种输出格式（compact/md/JSON）

**使用示例**:
```bash
# 查看使用量
python3 scripts/usage.py

# 详细输出
python3 scripts/usage.py --md

# JSON 输出
python3 scripts/usage.py --json
```

### 改进功能

#### 1. 更新脚本增强
- **脚本**: `scripts/update.py`
- **改进**:
  - ✅ 支持 Extract API 参数追踪
  - ✅ 更详细的更新日志
  - ✅ 自动版本号递增

#### 2. 测试套件
- **脚本**: `scripts/test_all.py`
- **功能**: 自动化测试所有 API
- **使用**:
  ```bash
  # 快速测试（仅 Search）
  python3 scripts/test_all.py --quick
  
  # 完整测试
  python3 scripts/test_all.py
  ```

### 文档更新

- ✅ SKILL.md - 添加 Extract 和 Usage 完整文档
- ✅ README.md - 更新使用示例
- ✅ _meta.json - 版本更新到 1.1.0

---

## 📊 完整 API 支持

| API | 端点 | 状态 | 脚本 | 成本 |
|-----|------|------|------|------|
| **Search** | `/search` | ✅ 100% | `search.py` | 1-2 信用/次 |
| **Extract** | `/extract` | ✅ 100% | `extract.py` | 1-2 信用/5 URL |
| **Usage** | `/usage` | ✅ 100% | `usage.py` | 免费 |
| Crawl | `/crawl` | ❌ | - | 3-5 信用/10 页 |
| Map | `/map` | ❌ | - | 1-2 信用/10 页 |
| Research | `/research` | ❌ | - | 4-250 信用/次 |

---

## 💰 成本对比

### 免费额度（1000 信用/月）能做：

| 操作 | 次数 |
|------|------|
| Search (basic) | 1,000 次 |
| Search (advanced) | 500 次 |
| Extract (basic) | 5,000 个 URL |
| Extract (advanced) | 2,500 个 URL |
| Usage | 无限次 |

---

## 📁 文件结构

```
tavily-web-search/
├── SKILL.md                  # 完整文档
├── README.md                 # 快速开始
├── _meta.json                # 版本信息 (v1.1.0)
├── CHANGELOG.md              # 本文件
├── update.log                # 更新日志
├── .last_check               # 最后检查记录
└── scripts/
    ├── search.py             # Search API (592 行)
    ├── extract.py            # Extract API (464 行)
    ├── usage.py              # Usage API (307 行)
    ├── update.py             # 自动更新 (315 行)
    └── test_all.py           # 测试套件 (120 行)
```

**总代码量**: ~1,800 行

---

## 🧪 测试结果

```bash
$ python3 scripts/test_all.py --quick

📍 Testing Search API...
✅ PASS - search.py --query "Python tutorial"
✅ PASS - search.py --query "AI news" --topic news
✅ PASS - search.py --query "Python" --include-domains python.org
✅ PASS - search.py --query "test" --format raw

📊 TEST SUMMARY
Passed: 4/4
Success Rate: 100.0%
✅ All tests passed!
```

---

## 🚀 发布到 ClawHub

```bash
# 发布 v1.1.0
clawhub publish skills/tavily-web-search --slug tavily-web-search-full --version 1.1.0

# 输出
✔ OK. Published tavily-web-search-full@1.1.0
```

---

## 📈 使用统计

### 典型工作流

```bash
# 1. 先查看使用量
python3 scripts/usage.py
# 输出：Used: 150 | Remaining: 850 | Total: 1,000

# 2. 搜索相关信息
python3 scripts/search.py --query "AI trends 2026" --max-results 5

# 3. 提取感兴趣的文章
python3 scripts/extract.py --urls "https://example.com/article1,https://example.com/article2"

# 4. 再次检查使用量
python3 scripts/usage.py
# 输出：Used: 151 | Remaining: 849 | Total: 1,000
```

---

## 🎯 下一步计划

### 可选扩展
- [ ] Crawl API（网站爬取）
- [ ] Map API（网站地图）
- [ ] Project ID 支持（项目追踪）
- [ ] 异步并发搜索
- [ ] 结果评分过滤

### 优化建议
- [x] ✅ 添加 Extract API
- [x] ✅ 添加 Usage API
- [x] ✅ 完整测试套件
- [ ] 性能基准测试
- [ ] 更多输出格式模板

---

## 📚 相关链接

- **ClawHub**: https://clawhub.com/skills/tavily-web-search-full
- **Tavily 官方**: https://tavily.com
- **API 文档**: https://docs.tavily.com
- **定价**: https://docs.tavily.com/documentation/api-credits.md

---

**版本**: 1.1.0  
**发布日期**: 2026-03-22  
**作者**: System  
**许可**: MIT
