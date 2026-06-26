# Brave 搜索配置指南

## 快速配置

### 步骤 1：获取 API Key

1. 访问 [Brave Search API](https://api.search.brave.com/app/dashboard)
2. 注册账号
3. 在 Dashboard 创建 API Key

### 步骤 2：配置到 OpenClaw

**方式 A：环境变量（推荐）**
```bash
# 添加到 ~/.bashrc 或 ~/.zshrc
export BRAVE_API_KEY="your_api_key_here"

# 生效
source ~/.bashrc
```

**方式 B：Gateway 配置**
```bash
openclaw configure --section web
# 按提示输入 API Key
```

**方式 C：直接修改 Gateway 配置**
```bash
# 编辑 Gateway 配置文件
vim ~/.openclaw/gateway/config.yaml

# 添加
web:
  brave_api_key: "your_api_key_here"
```

### 步骤 3：验证配置

```python
# 测试搜索
web_search(query="test", count=1)
```

---

## 使用示例

### 示例 1：市场规模调研

```python
# 搜索住房租赁市场规模
results = web_search(
    query="中国住房租赁市场规模 2024 万亿",
    count=10,
    freshness="py"  # 过去一年
)

# 输出到报告
write_market_report(results, "住房租赁")
```

### 示例 2：竞品分析

```python
# 搜索竞品动态
results = web_search(
    query="自如 相寓 蛋壳 融资 估值 2024",
    count=10,
    freshness="pm"  # 过去一个月
)

# 分析竞品对比
analyze_competitors(results, ["自如", "相寓", "蛋壳"])
```

### 示例 3：专家背景调研

```python
# 搜索专家观点
results = web_search(
    query="左晖 贝壳 房产科技 观点 访谈",
    count=10,
    freshness="py"
)

# 整理专家观点
extract_expert_opinions(results, "左晖")
```

### 示例 4：行业趋势

```python
# 搜索政策动态
results = web_search(
    query="保障性租赁住房 政策 2024 住建部",
    count=10,
    freshness="pm"
)

# 整理政策摘要
summarize_policy_updates(results)
```

---

## 与战略顾问工作流整合

### 外部访谈前

```python
# 1. 调研访谈对象背景
expert_bg = web_search(f"{expert_name} 背景 经历 观点")

# 2. 调研相关话题最新动态
topic_trends = web_search(f"{topic} 最新动态 2024")

# 3. 生成访谈准备文档
generate_interview_prep(expert_bg, topic_trends)
```

### 研讨会准备

```python
# 1. 市场规模数据
market_size = web_search(f"{industry} 市场规模 TAM SAM SOM")

# 2. 竞品对标数据
competitor_data = web_search(f"{competitors} 融资 估值 收入")

# 3. 专家观点汇总
expert_opinions = web_search(f"{industry} 专家 观点 趋势")

# 4. 生成研讨会输入
generate_workshop_input(market_size, competitor_data, expert_opinions)
```

### 商业模式验证

```python
# 1. 搜索对标案例
similar_cases = web_search(f"{business_model} 成功案例 商业模式")

# 2. 搜索失败教训
failure_lessons = web_search(f"{business_model} 失败 教训 倒闭")

# 3. 搜索融资参考
funding_ref = web_search(f"{industry} 融资 估值倍数 2024")

# 4. 生成验证报告
generate_validation_report(similar_cases, failure_lessons, funding_ref)
```

---

## 搜索技巧

### 关键词优化

| 搜索目的 | 推荐关键词组合 |
|----------|---------------|
| 市场规模 | `{行业} 市场规模 TAM SAM SOM 报告 2024` |
| 竞品分析 | `{公司名} 融资 估值 收入 商业模式` |
| 专家观点 | `{专家名} 观点 访谈 演讲 最新` |
| 行业趋势 | `{话题} 趋势 2024 预测 报告` |
| 政策法规 | `{话题} 政策 法规 住建部 最新` |
| 投资动态 | `{行业} 投资 融资 估值 IPO` |

### 时间筛选

- `freshness="pd"` - 过去24小时（新闻追踪）
- `freshness="pw"` - 过去一周（动态监控）
- `freshness="pm"` - 过去一月（趋势分析）
- `freshness="py"` - 过去一年（基准数据）

---

## 定价参考

Brave Search API 免费层级：
- 每月 2,000 次查询
- 适合战略顾问日常使用

付费层级：
- Pro: $3/月，5,000 次查询
- Pro+: $5/月，10,000 次查询

---

## 故障排除

### 错误：`missing_brave_api_key`
- 原因：未配置 API Key
- 解决：按上述步骤配置 BRAVE_API_KEY

### 错误：搜索结果为空
- 原因：关键词过于具体或生僻
- 解决：使用更通用的关键词，或减少筛选条件

### 错误：超出查询限制
- 原因：免费层级每月 2,000 次用完
- 解决：升级付费计划，或优化搜索策略减少调用次数
