# 同花顺数据获取实现细节

## 页面结构分析

### 1. 个股详情页 - 题材/概念

**URL**: `https://stockpage.10jqka.com.cn/[股票代码]/`

**示例**: `https://stockpage.10jqka.com.cn/000001/`

#### 关键元素定位

```
heading "平安银行 000001" [level=1] [ref=e31]
  └─ link "平安银行 000001" [ref=e32]
      └─ strong [ref=e33]
          ├─ text: 平安银行
          └─ text: "000001"

term [ref=e456]: 所属地域：
definition [ref=e455]: 广东省

term [ref=e456]: 涉及概念：
definition [ref=e457]: 高股息精选，跨境支付 (CIPS)...

term [ref=e458]: 主营业务：
definition [ref=e459]: 经营分析 [link]
definition [ref=e461]: 办理人民币存、贷、结算、汇兑业务...
```

#### 提取逻辑

1. **股票名称和代码**：
   - 查找 `heading [level=1]`
   - 提取 `strong` 内的文本

2. **涉及概念**：
   - 查找 `term` 文本包含"涉及概念"
   - 获取相邻的 `definition` 元素文本
   - 按逗号分隔得到概念列表

3. **所属地域**：
   - 查找 `term` 文本包含"所属地域"
   - 获取相邻的 `definition` 元素文本

4. **主营业务**：
   - 查找 `term` 文本包含"主营业务"
   - 获取相邻的 `definition` 元素文本

### 2. 问财人气排名页

**URL**: `https://www.iwencai.com/unifiedwap/result?w=个股人气排名`

#### 关键元素定位

```
table [ref=e208]:
  └─ rowgroup [ref=e209]:
      └─ row "1 600396 华电辽能 6.26 10.02 1 16.79 万" [ref=e210]:
          ├─ cell "1" [ref=e211]         → 排名
          ├─ cell [ref=e213]             → (空)
          ├─ cell "600396" [ref=e216]    → 股票代码
          ├─ cell "华电辽能" [ref=e218]  → 股票简称
          ├─ cell "6.26" [ref=e221]      → 现价
          ├─ cell "10.02" [ref=e223]     → 涨跌幅
          ├─ cell "1" [ref=e225]         → 热度排名
          └─ cell "16.79 万" [ref=e227]  → 热度值
```

#### 表头结构

```
list [ref=e191]:
  ├─ listitem [ref=e192]: 现价 (元)
  ├─ listitem [ref=e195]: 涨跌幅 (%)
  ├─ listitem [ref=e198]: 个股热度排名 2026.03.21
  └─ listitem [ref=e202]: 个股热度 2026.03.21
```

#### 提取逻辑

1. **定位表格**：
   - 查找包含"个股热度排名"的 `table` 元素
   - 或使用第一个主要数据表格

2. **遍历行**：
   - 查找 `rowgroup` > `row`
   - 跳过表头行

3. **提取单元格**：
   - cell 0: 排名（序号）
   - cell 1: (空，忽略)
   - cell 2: 股票代码
   - cell 3: 股票简称（可能有 link）
   - cell 4: 现价
   - cell 5: 涨跌幅
   - cell 6: 热度排名
   - cell 7: 热度值

4. **数据清洗**：
   - 涨跌幅：添加正负号（>0 添加"+"）
   - 热度值：保留原始格式（如"16.79 万"）

## Browser 工具调用流程

### 获取个股题材

```python
# 1. 打开个股页面
browser(action="open", targetUrl="https://stockpage.10jqka.com.cn/000001/")

# 2. 等待加载（可通过 snapshot 检查）
browser(action="snapshot", refs="aria", timeoutMs=5000)

# 3. 解析 snapshot 提取数据
# 查找 heading[level=1] 获取股票名称
# 查找 term"涉及概念"获取概念列表
```

### 获取人气排名

```python
# 1. 打开问财页面
browser(action="open", targetUrl="https://www.iwencai.com/unifiedwap/result?w=个股人气排名")

# 2. 等待加载
browser(action="snapshot", refs="aria", timeoutMs=5000)

# 3. 解析 snapshot 提取表格数据
# 查找 table 包含"个股热度排名"
# 遍历 row 提取每行数据
```

## 数据格式

### 个股题材 JSON

```json
{
  "stock_code": "000001",
  "stock_name": "平安银行",
  "themes": ["高股息精选", "跨境支付 (CIPS)", "..."],
  "region": "广东省",
  "business": "办理人民币存、贷、结算、汇兑业务...",
  "fetch_time": "2026-03-21 14:18:00",
  "source": "同花顺 stockpage.10jqka.com.cn"
}
```

### 人气排名 JSON

```json
{
  "rank_type": "个股人气排名",
  "limit": 20,
  "fetch_time": "2026-03-21 14:18:00",
  "source": "同花顺问财 iwencai.com",
  "stocks": [
    {
      "rank": 1,
      "code": "600396",
      "name": "华电辽能",
      "price": "6.26",
      "change": "10.02",
      "hot_rank": "1",
      "hot_value": "16.79 万"
    }
  ]
}
```

## 错误处理

### 常见问题

1. **页面返回 404**：
   - 检查股票代码是否正确
   - 检查 URL 格式

2. **snapshot 为空**：
   - 增加等待时间
   - 检查页面是否完全加载

3. **数据解析失败**：
   - 检查页面结构是否变化
   - 更新 selector 定位逻辑

### 重试策略

```python
MAX_RETRIES = 3
RETRY_DELAY = 2  # 秒

for attempt in range(MAX_RETRIES):
    try:
        # 执行操作
        break
    except Exception as e:
        if attempt == MAX_RETRIES - 1:
            raise
        time.sleep(RETRY_DELAY)
```

## 性能优化

1. **减少请求频率**：
   - 同一股票 5 分钟内不重复请求
   - 批量获取时使用延迟

2. **缓存机制**：
   - 缓存已获取的题材数据
   - 设置合理的过期时间

3. **并行处理**：
   - 多个股票题材获取可并行
   - 注意浏览器标签页数量限制

## 更新日志

- 2026-03-21: 初始版本，基于同花顺页面结构分析
