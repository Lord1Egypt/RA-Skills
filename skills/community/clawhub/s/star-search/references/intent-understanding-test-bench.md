# 意图理解测试基准 (Intent Understanding Test Bench)

实战 77 (2026-06-17) 建立的意图理解测试方法论。107 query 4 批测试, 暴露 17 个根因。

## 犀牛核心原则

**不要着急推进, 先测试能否准确、全面的理解用户意图。**

任何意图理解模块（super_brain / intent_strategy / entity_type 检测）改动后, **必须先跑测试基准**, 通过后再发布。

## 测试模板

```python
# /tmp/test_intent.py
import sys, time
sys.path.insert(0, "/home/ubuntu/star-search/scripts")
import super_brain
import intent_strategy

TESTS = [
    # (query, exp_intent, exp_strat)
    ("韭研公社 网址", "navigation", "company"),
    ("华为 Mate 70 价格", "transaction", "shopping"),
    # ... 30+ query
]

print(f"{'QUERY':<30} {'EXPECT':<22} {'BRAIN':<28} {'STRAT':<12}")
total_brain = total_strat = total = 0
issue_brain, issue_strat = [], []

t0 = time.time()
for query, exp_intent, exp_strat in TESTS:
    try:
        bi = super_brain.analyze_query(query, use_cache=False)  # 必须 False
        s = intent_strategy.strategy_for_query(query, bi)
        brain_ok = (bi.get("intent") == exp_intent)
        strat_ok = (s.get("entity_type") == exp_strat)
        total += 1
        if brain_ok: total_brain += 1
        else: issue_brain.append(f"  {query}: 期望 intent={exp_intent}, 实际={bi.get('intent')}")
        if strat_ok: total_strat += 1
        else: issue_strat.append(f"  {query}: 期望 strategy={exp_strat}, 实际={s.get('entity_type')}")
        # print 行
    except Exception as e:
        print(f"{query}: ERROR {e}")

print(f"\nBRAIN: {total_brain}/{total} = {round(total_brain/total*100, 1)}%")
print(f"STRAT: {total_strat}/{total} = {round(total_strat/total*100, 1)}%")
print(f"耗时: {round(time.time()-t0, 1)}s")
```

## 跑测试命令

```bash
# 1. 上传测试脚本
base64 test_intent.py | ssh root@server "base64 -d > /tmp/test_intent.py"

# 2. 清缓存（避免假阳性）
ssh root@server "rm -f /home/ubuntu/star-search/brain_cache.json"

# 3. 跑（注意 timeout 至少 240s, 30 query × 8s = 240s）
ssh root@server "PYTHONPATH=/home/ubuntu/.local/lib/python3.10/site-packages python3 /tmp/test_intent.py"

# 4. 统计 BRAIN/STRAT 评分
```

## 4 批 107 query 评分

| 批 | 类型 | query | BRAIN | STRAT |
|---|---|---|---|---|
| 1 | 10 类基础场景 | 37 | 83.8% | 54.1% |
| 2 | 模糊/多 entity/中英/极长/命令 | 30 | 90.0% | 43.3% |
| 3 | 行业垂直 (金融/医疗/教育/法律) | 20 | 95.0% | 70.0% |
| 4 | 错拼/极简/讽刺/方言/乱码 | 20 | 85.0% | 25.0% |
| **合计** | | **107** | **87.9%** | **48.6%** |

## 17 个根因（待实战 78 修）

### A. detect_entity_type 缺规则（5 个）
- 缺 "X 官网" → company
- 缺 "X 是什么" → company/product
- 缺 "X 简介" → company/product
- 缺 "X vs Y" 拆 entity
- 缺 "X 进展" → news

### B. 不看 brain_info.intent
- news/transaction 应优先
- intent=news → news / intent=transaction → shopping

### C. 购物类错
- "X 多少钱" 应 shopping（不是 company）

### D. 2-4 字中文 entity → person 误判
- 收紧: 2-4 字 + 后缀"简历/生平"才 person

### E. 开放式 → academic 误判
- "X 怎么样/推荐" 应 general

### F. 极短 1-2 字 → academic
- 单独 "Python" / "AI" → general

### G. 复合 entity 拆分错
- "什么是基于 Transformer 的深度学习模型" 拆 entity 错

### H. 英文 entity 不走 KB
- "Apple stock price" 应 company

### I. 极长 query 拆 entity 错

### J. "怎么 + 动词" → academic
- 教程类信号

### K. 泛化词 → general
- 流程/师/指数/查询/服务

### L. 评测/价格 → shopping
- "X 评测" / "X 价格"

### M. 区域/城市 → general
- "上海 房价"

### N. 拼音 query 没重写
- "huwei mate70" → "华为 mate 70"

### O. 错别字/方言不纠正

### P. 2-4 字中文 entity KB 优先
- "微信" / "元宇宙" / "5G" → KB 命中

### Q. 复合句/自述 → general
- "我是/我想" → general

## 实战 78 修复后预估

| 维度 | 当前 | 修后预估 |
|---|---|---|
| BRAIN (intent) | 87.9% | 95%+ |
| STRAT (entity_type) | 48.6% | 85%+ |

## 复用测试 query 库

实战 77 已积累 107 query, 实战 78 修复后**必须用相同 query 重测**:
- 评分变好 → 发版
- 评分持平或变差 → 排查新 bug

## 犀利测试原则

1. **必须 `use_cache=False`**：避免 brain cache 假阳性（实战 77 第一批有 bug, 全 brain=None, 清 cache 后准）
2. **必须 `rm -f brain_cache.json`**：清缓存是必要步骤
3. **必须 timeout≥240s**：30 query × 8s LLM 调用 = 240s
4. **必须分批跑**：50 query 一次性会超时 (300s 限制), 拆 30+20+20
5. **必须输出 issue_brain/issue_strat 列表**：知道哪些 query 错, 才能针对性修
6. **必须统计耗时**：LLM 调 8s/query, 30 query = 240s 是正常

## 并发测试模板 (实战 84, 108 query 80s)

**串行测试 50+ query 超时 300s**。**实战 84 解决方案**：8 线程 ThreadPoolExecutor + use_cache=False + 清缓存。

```python
# /tmp/test_84.py
import sys, time
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, "/home/ubuntu/star-search/scripts")
import super_brain
import intent_strategy

ALL = BATCH1 + BATCH2 + BATCH3 + BATCH4  # 108 query

def test(q):
    try:
        bi = super_brain.analyze_query(q[0], use_cache=False)
        s = intent_strategy.strategy_for_query(q[0], bi)
        return (q[0], q[1], q[2], bi.get("intent"), s.get("entity_type"),
                bi.get("intent") == q[1], s.get("entity_type") == q[2])
    except Exception as e:
        return (q[0], q[1], q[2], "ERR", "ERR", False, False)

t0 = time.time()
with ThreadPoolExecutor(max_workers=8) as ex:
    results = list(ex.map(test, ALL))

brain_ok = sum(1 for r in results if r[5])
strat_ok = sum(1 for r in results if r[6])
print(f"BRAIN: {brain_ok}/{len(ALL)} = {round(brain_ok/len(ALL)*100, 1)}%")
print(f"STRAT: {strat_ok}/{len(ALL)} = {round(strat_ok/len(ALL)*100, 1)}%")
print(f"耗时: {round(time.time()-t0, 1)}s")  # 8 线程 108 query ~80-90s
```

**关键**：`max_workers=8`（LLM API 并发 8 不触发限流）, 必须 `use_cache=False`。

## 4 阶段评分演进（实战 73→85 完整数据）

| 阶段 | BRAIN (intent) | STRAT (entity_type) | 两者都准 |
|---|---|---|---|
| 实战 73 之前 | ~70% | ~30% | ~25% |
| 实战 78 之前 | 87.9% | 48.6% | 47.4% |
| 实战 78 之后 | 91.7% | 53.7% | 51.9% |
| **实战 85 之后** | **94.4%** | **56.5%** | **55.6%** |
| 目标 (Perplexity) | ~95% | ~90% | ~85% |

**关键洞察**：
- BRAIN 94.4% 接近 LLM 极限
- STRAT 56.5% 是规则天花板（剩余都是学术类 query 推 general, 需更多 query 模式）
- 实战 73→85: 25% → 56% (2.3 倍), 但离 Perplexity 级 85% 还差 30 个百分点
- **BRAIN 准不是终极目标, 真正能 "理解意图" 必须 BRAIN + STRAT 都准**

## 实战 85 KB 扩展真实数据 (180+ 实体)

**BUILTIN_KB_EXTRA2** 实战 85 一次性加 90+ entity (15 人物/15+ 公司/12 AI 产品/11 概念/11 游戏/10 食物/5 地点), `_build_kb_hint()` 动态合并 EXTRA+EXTRA2 = 180+ 实体。

**8 query 端到端命中真网址**（实战 85 验证）：
- "微信" → weixin.qq.com (product)
- "openai 是什么" → openai.com (company)
- "GPT-4 是什么" → openai.com/gpt-4 (product)
- "特斯拉 官网" → tesla.com (company)
- "比亚迪 vs 特斯拉" → tesla.com (company, comparison 拆 entity)

**复用口诀**：当 BUILTIN_KB_HINT 命中时, detect_entity_type 走 KB → 返回对应 type。KB 越大 STRAT 越准。
