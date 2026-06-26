#!/usr/bin/env python3
"""实战 77-86 4 批 108 query 意图理解测试模板
跑法:
  cd /home/ubuntu/star-search/scripts
  rm -f /home/ubuntu/star-search/brain_cache.json
  PYTHONPATH=/home/ubuntu/.local/lib/python3.10/site-packages python3 /tmp/test_84.py

期望输出 (v20.33 实战 86 后):
  BRAIN (intent) 准: 100/108 = 92.6%
  STRAT (entity_type) 准: 64/108 = 59.3%
  两者都准: 63/108 = 58.3%
  总耗时: ~90s (8 线程并发)

每个测试: (query, expected_intent, expected_entity_type)
"""
import sys
import time
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, "/home/ubuntu/star-search/scripts")
import super_brain
import intent_strategy

# ========== BATCH 1 (37 query) 实战 78 第一批 ==========
BATCH1 = [
    # 导航
    ("韭研公社 网址", "navigation", "company"),
    ("北京暮辰恒信咨询有限公司", "navigation", "company"),
    ("华为官网", "navigation", "company"),
    ("特斯拉官网", "navigation", "company"),
    ("小红书 官网", "navigation", "product"),
    # 工商
    ("上海寻梦信息技术有限公司", "info", "company"),
    ("腾讯 公司 法人", "info", "company"),
    ("注册资本多少", "info", "company"),
    ("北京字节跳动 创始人", "info", "company"),
    ("公司联系方式", "info", "company"),
    # 购物
    ("华为 Mate 70 价格", "transaction", "shopping"),
    ("iPhone 16 Pro Max 哪里买", "transaction", "shopping"),
    ("比亚迪多少钱", "transaction", "shopping"),
    ("多少钱一台", "transaction", "shopping"),
    ("Nike 折扣", "transaction", "shopping"),
    # 对比
    ("比亚迪 vs 特斯拉", "comparison", "company"),
    ("Python vs Rust", "comparison", "academic"),
    ("Kimi 和 豆包 哪个好", "comparison", "product"),
    ("阿里云 腾讯云 哪家强", "comparison", "company"),
    ("RAG 和 Fine-tuning 区别", "comparison", "academic"),
    # 教程
    ("Python 教程", "info", "academic"),
    ("Rust 入门", "info", "academic"),
    ("Transformer 原理", "info", "academic"),
    # 新闻
    ("今天 AI 新闻", "news", "news"),
    ("最新 5G 进展", "news", "news"),
    ("中国股市今日动态", "news", "news"),
    # 人物
    ("马斯克 简历", "info", "person"),
    ("陆奇 在哪", "info", "person"),
    ("张一鸣 字节 故事", "info", "person"),
    # 产品百科
    ("openai 是什么公司", "info", "company"),
    ("什么是 LLM", "info", "academic"),
    ("Anthropic 简介", "info", "company"),
    # 视频
    ("最近好看的电影", "info", "video"),
    ("王心凌演唱会视频", "info", "video"),
    # 边界
    ("AI", "info", "general"),
    ("比亚迪", "info", "company"),
    ("hello", "info", "general"),
    ("中国", "info", "general"),
]

# ========== BATCH 2 (30 query) 实战 78 第二批 ==========
BATCH2 = [
    ("机器学习是什么", "info", "academic"),
    ("程序员 副业", "info", "general"),
    ("周末去哪儿玩", "info", "general"),
    ("推荐一本好书", "info", "general"),
    ("怎么做饭", "info", "general"),
    ("阿里 腾讯 百度 哪个好", "comparison", "company"),
    ("小米 华为 OPPO 对比", "comparison", "company"),
    ("微信 钉钉 飞书", "comparison", "product"),
    ("GPT Claude Gemini", "comparison", "product"),
    ("北京 上海 深圳 房价", "comparison", "general"),
    ("AI", "info", "general"),
    ("Python", "info", "general"),
    ("什么是 基于 Transformer 的深度学习模型 的训练方法", "info", "academic"),
    ("如何在 2026 年通过自学成为 AI 工程师并找到月薪 5 万的工作", "info", "academic"),
    ("我想了解关于 OpenAI 公司创始人 Sam Altman 的所有信息和最新动态", "info", "person"),
    ("什么是 LLM", "info", "academic"),
    ("GPT-4 是什么", "info", "product"),
    ("iPhone 16 Pro", "info", "product"),
    ("OpenAI 公司", "info", "company"),
    ("Apple stock price", "info", "company"),
    ("在北京 找一家 好的 心理咨询", "info", "general"),
    ("学习 Python 需要 多久", "info", "academic"),
    ("怎么 才能 让 AI 帮我 写代码", "info", "academic"),
    ("苹果公司 是 哪个 国家的", "info", "company"),
    ("什么是 LLM 大模型 跟 RAG 区别", "comparison", "academic"),
    ("告诉我 比亚迪 股价", "info", "company"),
    ("给我搜 韭研公社", "navigation", "company"),
    ("查询 2024 GDP", "info", "general"),
    ("搜索 Python 教程", "info", "academic"),
    ("百度一下 华为官网", "navigation", "company"),
]

# ========== BATCH 3 (20 query) 行业垂直 ==========
BATCH3 = [
    ("宁德时代 股票", "info", "company"),
    ("今天 上证指数", "info", "general"),
    ("比亚迪 财报", "info", "company"),
    ("茅台 股价 多少", "transaction", "company"),
    ("如何 选股", "info", "academic"),
    ("高血压 怎么 治", "info", "general"),
    ("布洛芬 副作用", "info", "general"),
    ("推荐 一家 三甲医院", "info", "general"),
    ("抑郁症 自我 治疗", "info", "general"),
    ("心理咨询 师", "info", "general"),
    ("哈佛大学 申请条件", "info", "academic"),
    ("GRE 怎么 备考", "info", "academic"),
    ("机器学习 入门 课程", "info", "academic"),
    ("MIT 公开课", "info", "academic"),
    ("如何 选 大学 专业", "info", "academic"),
    ("劳动合同 纠纷 怎么办", "info", "general"),
    ("离婚 财产 分割", "info", "general"),
    ("创业 公司 注册 流程", "info", "general"),
    ("理想 L7 评测", "info", "shopping"),
    ("上海 房价 2026", "info", "general"),
]

# ========== BATCH 4 (20 query) 奇葩边界 ==========
BATCH4 = [
    ("huwei mate70 jiage", "transaction", "shopping"),
    ("拜迪 比亚 蒂", "info", "company"),
    ("苹果怎嘛样", "info", "company"),
    ("特里拉 怎么样", "info", "company"),
    ("马思克 简历", "info", "person"),
    ("5G", "info", "general"),
    ("微信", "info", "product"),
    ("元宇宙", "info", "academic"),
    ("为什么 我穷", "info", "general"),
    ("为什么 老板 这么 蠢", "info", "general"),
    ("AI 是不是 泡沫", "info", "academic"),
    ("你晓得 比亚迪 哪儿的 伐", "info", "company"),
    ("恁说 这 苹果 咋样", "info", "company"),
    ("Ai 到底 是个 啥玩意儿", "info", "academic"),
    ("我想了解一下目前市面上所有的 AI 大语言模型产品包括 ChatGPTClaudeGemin 文心一言 通义千问 豆包 Kimi 等等它们各自的优缺点适用场景以及收费情况", "info", "product"),
    ("请问 2026 年最新款的 iPhone 17 Pro Max 256GB 国行版本在京东和天猫以及拼多多这三个平台上的价格分别是多少有没有什么优惠活动", "transaction", "shopping"),
    ("我是一个 30 岁的程序员在北京工作年薪 50 万我应该如何在 2026 年通过投资理财实现财务自由请给出具体可行的方案", "info", "general"),
    ("!@#$%", "info", "general"),
    ("𓀀𓂀𓆎𓃷", "info", "general"),
    ("   空格 query   ", "info", "general"),
]

ALL = BATCH1 + BATCH2 + BATCH3 + BATCH4
print(f"Total: {len(ALL)} queries")

def test(q):
    try:
        bi = super_brain.analyze_query(q[0], use_cache=False)
        s = intent_strategy.strategy_for_query(q[0], bi)
        brain_ok = (bi.get("intent") == q[1])
        strat_ok = (s.get("entity_type") == q[2])
        return (q[0], q[1], q[2], bi.get("intent"), s.get("entity_type"), brain_ok, strat_ok)
    except Exception as e:
        return (q[0], q[1], q[2], "ERR", "ERR", False, False)

t0 = time.time()
with ThreadPoolExecutor(max_workers=8) as ex:
    results = list(ex.map(test, ALL))
elapsed = round(time.time() - t0, 1)

total = len(results)
brain_ok = sum(1 for r in results if r[5])
strat_ok = sum(1 for r in results if r[6])
both_ok = sum(1 for r in results if r[5] and r[6])

print(f"\n{'='*100}")
print(f"实测 4 批 {total} query (并发 8 线程):")
print(f"  BRAIN (intent) 准: {brain_ok}/{total} = {round(brain_ok/total*100, 1)}%")
print(f"  STRAT (entity_type) 准: {strat_ok}/{total} = {round(strat_ok/total*100, 1)}%")
print(f"  两者都准: {both_ok}/{total} = {round(both_ok/total*100, 1)}%")
print(f"  总耗时: {elapsed}s")

print(f"\n--- BRAIN 错 ---")
for r in results:
    if not r[5]:
        print(f"  {r[0][:40]}: 期望={r[1]}, 实际={r[3]}")

print(f"\n--- STRAT 错 (前 20) ---")
for r in results:
    if not r[6]:
        print(f"  {r[0][:40]}: 期望={r[2]}, 实际={r[4]}")
