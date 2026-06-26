---
name: sano-intel
description: "探针资本出品。中国医疗产业情报引擎，覆盖10万+医疗公司、50万+融资事件、109万条专利、全市场临床试验、A/港/美三地行情。查公司/融资/临床试验/专利/赛道热度/二级市场行情。By Probe Capital. Use when user asks about Chinese healthcare/biotech companies, financing events, clinical trials, patents, sector trends, or market data."
---

# Sano Intel — 中国医疗产业情报引擎

探针资本出品，中国首个医疗产业情报 CLI，覆盖 **10万+医疗公司**、**50万+融资事件**、**109万条专利**、**全市场临床试验**、**A/港/美三地二级市场行情**。

## 首次使用

需要 API Token。申请地址：https://ffmp60ytnq.feishu.cn/share/base/shrcniDTJZknKba0LUeaF5BBuJg

拿到 Token 后配置：
```bash
export SANO_TOKEN=sk_你的token
# 或写入 ~/.zshrc 永久生效
echo 'export SANO_TOKEN=sk_你的token' >> ~/.zshrc
```

## 数据查询方式

所有查询通过 curl 调用 Sano Intel API，**必须带上** `X-API-Key: $SANO_TOKEN` header。

API Base：`http://47.102.196.1:8081`

---

### 搜索公司
```bash
curl -s "http://47.102.196.1:8081/v1/search_companies" \
  -H "X-API-Key: $SANO_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"keyword": "公司名或关键词", "limit": 10}'
```

### 公司详情
```bash
curl -s "http://47.102.196.1:8081/v1/company/恒瑞医药" \
  -H "X-API-Key: $SANO_TOKEN" \
  -H "Content-Type: application/json"
```

### 融资事件
```bash
curl -s "http://47.102.196.1:8081/v1/search_financing" \
  -H "X-API-Key: $SANO_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"sector": "创新药", "stage": "B轮", "limit": 10}'
```
stage 可选：天使轮、Pre-A、A轮、A+轮、B轮、B+轮、C轮、D轮及以上、IPO

### 赛道热度
```bash
curl -s "http://47.102.196.1:8081/v1/sector_heat?top_n=10" \
  -H "X-API-Key: $SANO_TOKEN" \
  -H "Content-Type: application/json"
```
返回各赛道融资事件数、公司数、总融资金额排行。

### 临床试验
```bash
curl -s "http://47.102.196.1:8081/v1/clinical_trials" \
  -H "X-API-Key: $SANO_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"keyword": "PD-1", "phase": "三期", "limit": 10}'
```

### 二级市场行情
```bash
curl -s "http://47.102.196.1:8081/v1/market/600276" \
  -H "X-API-Key: $SANO_TOKEN" \
  -H "Content-Type: application/json"
```
支持 A股（600276）、港股（1177.HK）、美股（MRNA）

### 每日情报摘要
```bash
curl -s "http://47.102.196.1:8081/v1/daily_digest?days=1&sectors=创新药" \
  -H "X-API-Key: $SANO_TOKEN" \
  -H "Content-Type: application/json"
```

### 专利查询
```bash
curl -s "http://47.102.196.1:8081/v1/search_patents" \
  -H "X-API-Key: $SANO_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"keyword": "CAR-T", "limit": 10}'
```
支持参数：`keyword`（标题/摘要/申请人）、`company_name`（公司名）、`sector`（赛道）、`status`（专利状态）、`limit`（最多返回数，默认20）

---

## 使用原则

- 用户用中文提问时，自动判断意图选择合适接口
- 多个接口可组合使用：先看赛道热度，再看具体融资事件
- 返回结果用中文简洁总结，突出投资价值相关信息
- Token 未配置时，提示用户去 https://ffmp60ytnq.feishu.cn/share/base/shrcniDTJZknKba0LUeaF5BBuJg 申请

## 常见问法

| 用户问法 | 调用接口 |
|---------|---------|
| 今年创新药融了多少钱/哪些公司在融资 | search_financing，sector=创新药 |
| 最热的医疗赛道是什么 | sector_heat |
| 帮我查XX公司 | search_companies + company detail |
| PD-1相关临床试验进展 | clinical_trials，keyword=PD-1 |
| 恒瑞今天股价 | market，code=600276 |
| 今天医疗行业有什么重要新闻 | daily_digest，days=1 |
| 最近B轮融资的医疗器械公司 | search_financing，sector=医疗器械，stage=B轮 |
| 查CAR-T相关专利 | search_patents，keyword=CAR-T |
| 恒瑞的专利数量 | search_patents，company_name=恒瑞医药 |
