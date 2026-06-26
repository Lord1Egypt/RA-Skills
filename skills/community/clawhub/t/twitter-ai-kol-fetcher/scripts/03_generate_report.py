#!/usr/bin/env python3
"""
Twitter KOL Fetcher - Report Generator
内参生成脚本

[优化]
- 机会判定使用便宜的 Lightning 模型
- 报告生成使用贵的 M2.1 模型（强推理+文笔）
- 优化 prompt 提升战略分析深度
"""

import json
import requests
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

# 配置
OPENROUTER_API_KEY = None  # 需要配置

# 读取配置
def load_config():
    """从配置文件加载 API Key"""
    import os
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "config.json")
    if os.path.exists(config_path):
        try:
            with open(config_path, "r") as f:
                return json.load(f)
        except:
            pass
    return {}

CONFIG = load_config()

# 从配置文件读取，否则用环境变量兜底
if not OPENROUTER_API_KEY:
    OPENROUTER_API_KEY = CONFIG.get("openrouter_api_key") or os.environ.get("OPENROUTER_API_KEY")

# [优化] 模型分离
# 机会判定：MiniMax M2.5（逻辑判断 + 排序）
MODEL_OPPORTUNITY = "minimax/minimax-m2.5"

# 报告生成：Gemini 3.1 Pro（强推理 + 文笔）
MODEL_REPORT = "google/gemini-3.1-pro-preview"

def call_llm(prompt, model=MODEL_REPORT):
    """调用 OpenRouter API"""
    if not OPENROUTER_API_KEY:
        return "API key not configured"

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7
            },
            timeout=120  # 报告生成可能需要更长时间
        )
        result = response.json()
        return result["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error: {e}"

def prepare_opportunity_detection_prompt(topics):
    """[优化] 机会判定 prompt - 针对聚类后的主题"""
    topics_text = ""

    for i, topic in enumerate(topics[:10]):  # 只取前 10 个
        topic_preview = topic.get("topic_preview", "")[:80]
        hotness = topic.get("hotness", 0)
        authors = topic.get("authors", [])
        keywords = topic.get("keywords", [])
        tweet_count = len(topic.get("tweets", []))

        topics_text += f"""
### 话题 {i+1}: {topic_preview}
- 热度: {hotness:.0f}
- 涉及KOL: {', '.join(set(authors))}
- 关键词: {', '.join(keywords)}
- 相关推文: {tweet_count} 条
"""

    prompt = f"""
## 任务
作为 AI 战略分析师，判断以下候选话题是否值得写内参。

## 核心原则
**宁可多写，不可漏写**：领导更关心"为什么写这个"而不是"为什么没写"。

## 候选话题（已聚类）
{topics_text}

## 判定标准（1-10分）
1. **影响力**: 是否影响大量用户/开发者/投资者？
2. **新颖性**: 是否是新发布/新突破/新趋势？
3. **争议性**: 是否有不同观点碰撞？是否有潜在风险？
4. **战略价值**: 是否与 AI 竞争格局、政策走向相关？

## 额外标记（直接建议写）
- 🔥 产品发布（GPT、Claude、Sora 等）
- 💰 融资事件（> $50M）
- ⚠️ 安全/伦理事件
- 📜 政策动向（监管、出口管制）
- 🏢 公司重大变化

## 筛选规则
- 总分 ≥ 24 分 → 值得写
- 或任一单项 ≥ 8 分 → 值得写
- 或符合上述额外标记 → 直接写

## 输出格式（JSON）
```json
[
  {{
    "topic": "话题名",
    "topic_preview": "话题摘要",
    "scores": {{"影响力": X, "新颖性": X, "争议性": X, "战略价值": X}},
    "total": XX,
    "should_write": true/false,
    "reason": "简短理由",
    "priority": "high/medium/low"
  }}
]
```
只输出 JSON，不要其他内容。
"""
    return prompt

def prepare_report_prompt(topic, tweets):
    """
    [优化] 报告生成 prompt - 提升战略分析深度
    
    核心改进：
    - 强调"为什么重要"的逻辑链条
    - 要求明确的战略判断（不是泛泛而谈）
    - 对齐中关村两院风格：问题-分析-对策
    """
    # 整理推文（包含原文链接）
    tweets_text = ""
    for i, t in enumerate(tweets[:8]):  # 增加到 8 条
        tweet_url = t.get("url", f"https://x.com/{t.get('username')}/status/{t.get('id', '')}")
        tweets_text += f"""
{i+1}. @{t.get('username', 'unknown')}: {t.get('text', '')[:250]}...
   ❤️ {t.get('likes', 0)} | 🔁 {t.get('retweets', 0)} | [原文]({tweet_url})
"""

    # 从聚类 topic 中提取更多信息
    topic_name = topic.get("topic", "")[:100]
    topic_preview = topic.get("topic_preview", "")[:150]
    keywords = topic.get("keywords", [])
    authors = list(set(topic.get("authors", [])))
    
    prompt = f"""
## 任务
作为 AI 战略分析师，根据以下素材生成一份专业内参。

## 核心要求
- **问题导向**：先说清楚"这是什么事件"，再说"为什么重要"
- **逻辑链条**：每个结论都要有论据支撑
- **战略判断**：不要泛泛而谈，要给出明确的趋势判断
- **对齐风格**：参考中关村两院内参，问题-分析-对策

## 话题
{topic_name}

## 话题摘要
{topic_preview}

## 关键词
{', '.join(keywords)}

## 背景
- 热度: {topic.get('hotness', 0):.0f}
- 涉及KOL: {', '.join(authors)}
- 相关推文: {len(tweets)} 条

## 相关推文（按热度排序）
{tweets_text}

## 内参结构要求

# AI 内参：{topic_name}

**日期**: {datetime.now().strftime('%Y-%m-%d')}
**来源**: Twitter AI 圈动态
**可信度**: ⭐⭐⭐⭐

---

## 核心要点（3条）

请用一句话概括本报告最核心的3个发现。
格式：- {要点}

---

## 一、事件还原

### （一）发生了什么
简明扼要描述事件本身

### （二）时间线
按时间顺序梳理关键节点

---

## 二、战略意义分析（重点！）

### （一）为什么此时发生
分析触发因素和背景

### （二）对行业格局的影响
- 对头部厂商的影响
- 对中小厂商的机会
- 对开发者的影响

### （三）潜在风险与挑战
- 技术风险
- 商业风险
- 政策风险

---

## 三、各方观点

### 支持方
| 观点 | 来源 |
|------|------|
| ... | [@username](链接) |

### 质疑/担忧方
| 观点 | 来源 |
|------|------|
| ... | [@username](链接) |

### 中立/分析
| 观点 | 来源 |
|------|------|
| ... | [@username](链接) |

---

## 四、趋势判断（明确！）

| 周期 | 判断 | 依据 |
|------|------|------|
| 短期（1-3个月） | | |
| 中期（6-12个月） | | |
| 长期（1年以上） | | |

---

## 五、对策建议（可操作）

### （一）跟踪关注
- 需要持续关注哪些动态？

### （二）行动建议
- 如果是从业者，应该怎么做？
- 如果是投资者，应该关注什么？

---

## 相关链接

1. [标题](URL)

---

## 🏷️ 标签

#AI #大模型 #{具体领域}
"""

    return prompt

def generate_single_report(topic_info, topics, model=MODEL_REPORT):
    """
    [新增] 生成单篇报告 - 用于并行调用
    """
    topic_name = topic_info.get("topic", "")
    
    # 找到对应的推文
    topic_tweets = []
    target_topic = None
    
    for t in topics:
        if topic_name in (t.get("topic_preview", "") or t.get("topic", "")):
            topic_tweets = t.get("tweets", [])
            target_topic = t
            break
    
    if not topic_tweets:
        topic_tweets = [target_topic.get("key_tweet", {})] if target_topic else []

    topic_dict = {
        "topic": topic_name,
        "topic_preview": topic_info.get("topic_preview", "") or topic_name,
        "hotness": target_topic.get("hotness", 0) if target_topic else 0,
        "authors": target_topic.get("authors", []) if target_topic else []
    }

    report_prompt = prepare_report_prompt(topic_dict, topic_tweets)
    report_content = call_llm(report_prompt, model=model)

    return {
        "topic": topic_name,
        "content": report_content
    }


def generate_reports(filtered_file, output_markdown=True):
    """
    主函数：生成内参
    
    [优化]
    - 机会判定使用 M2.5 模型
    - 报告生成使用 Gemini 3.1 Pro（强推理）
    - 处理聚类后的 topics
    - [新增] 并行生成报告 - 速度翻倍
    """
    # 读取过滤后的数据
    with open(filtered_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 优先使用聚类后的 topics，否则回退到 raw_topics
    topics = data.get("topics", []) or data.get("raw_topics", [])

    if not topics:
        print("没有找到热门话题")
        return []

    # Step 1: 机会判定（用 Lightning 模型 - 便宜）
    print(f"[Step 1] 调用 LLM 进行机会判定，共 {len(topics)} 个话题...")
    print(f"    模型: {MODEL_OPPORTUNITY}")

    detection_prompt = prepare_opportunity_detection_prompt(topics)
    detection_result = call_llm(detection_prompt, model=MODEL_OPPORTUNITY)

    # 解析结果
    try:
        import re
        json_match = re.search(r'\[.*\]', detection_result, re.DOTALL)
        if json_match:
            decisions = json.loads(json_match.group())
        else:
            decisions = []
            print("    [警告] 无法解析 LLM 返回的 JSON")
    except Exception as e:
        decisions = []
        print(f"    [警告] 解析错误: {e}")

    # 筛选要写内参的话题
    topics_to_report = []
    for d in decisions:
        if d.get("should_write", False):
            topics_to_report.append({
                "topic": d.get("topic", ""),
                "topic_preview": d.get("topic_preview", ""),
                "priority": d.get("priority", "medium")
            })

    # 按优先级排序
    topics_to_report.sort(key=lambda x: {"high": 0, "medium": 1, "low": 2}.get(x.get("priority", "medium"), 1))
    
    print(f"    决定写内参的话题: {len(topics_to_report)} 个")

    # Step 2: 生成报告（并行 - 速度翻倍）
    reports = []
    max_reports = 3  # 成本控制
    topics_subset = topics_to_report[:max_reports]

    print(f"[Step 2] 并行生成 {len(topics_subset)} 篇内参...")
    print(f"    模型: {MODEL_REPORT}")

    # 并行执行
    with ThreadPoolExecutor(max_workers=3) as executor:
        # 提交所有任务
        future_to_topic = {
            executor.submit(generate_single_report, topic_info, topics, MODEL_REPORT): topic_info
            for topic_info in topics_subset
        }

        # 收集结果（按完成顺序）
        for future in as_completed(future_to_topic):
            topic_info = future_to_topic[future]
            try:
                result = future.result()
                reports.append(result)
                print(f"    ✓ {result['topic'][:40]}... 完成")
            except Exception as e:
                print(f"    ✗ {topic_info.get('topic', '')[:40]}... 失败: {e}")

    # 按原始顺序排序（保持一致性）
    topic_order = {t.get("topic"): i for i, t in enumerate(topics_subset)}
    reports.sort(key=lambda x: topic_order.get(x["topic"], 999))

    print(f"\n完成！共生成 {len(reports)} 篇内参")

    # 直接输出到控制台（供发送）
    return reports

if __name__ == "__main__":
    import sys
    input_file = sys.argv[1] if len(sys.argv) > 1 else f"/tmp/kol_tweets_filtered.json"

    # 配置 API Key（需要从环境变量或配置文件读取）
    import os
    OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")

    reports = generate_reports(input_file)

    for i, report in enumerate(reports):
        print(f"\n{'='*50}")
        print(f"内参 {i+1}: {report['topic'][:50]}...")
        print(f"{'='*50}")
        print(report["content"])
