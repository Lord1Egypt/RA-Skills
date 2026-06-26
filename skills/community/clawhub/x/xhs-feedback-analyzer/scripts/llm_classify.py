#!/usr/bin/env python3
"""
用 LLM 对小红书帖子进行情感 + 反馈类型分类
调用 OpenAI 兼容接口 (kubeplex-maas)
"""
import json, os, sys, time, re
from pathlib import Path
from urllib import request, error

BASE_URL = "https://mmc.sankuai.com/openclaw/v1"
MODEL = "catclaw-proxy-model"
HEADERS = {
    "Content-Type": "application/json",
    "Authorization": "Bearer catpaw",
    "X-Conversation-Id": "qlojc6j4vnqa35nznvl6",
    "X-User-Id": "jibowen04",
    "X-Scene": "CATCLAW",
}

SYSTEM_PROMPT = """你是一个小红书内容分析助手，专门分析美团跑腿/众包相关帖子。

请对每篇帖子进行以下分析，严格以JSON格式返回：

1. **sentiment**（情感）：
   - "positive"：用户对美团跑腿/众包持正面态度，分享好体验、表示感谢、推荐使用
   - "negative"：用户对美团跑腿/众包持负面态度，投诉、避雷、差评、吐槽
   - "neutral"：中性内容，如骑手/众包员工的日常分享（接单流水账）、客观测评、无明显情感倾向、与服务评价无关

2. **feedback_type**（反馈类型，从以下选项中选1-2个最符合的）：
   - "好评/正面体验"：用户好评、满意表达
   - "骑手/众包分享"：骑手或众包员工的接单经历分享（第一人称，关注收入、工作感受）
   - "配送速度/超时"：关注配送时效问题
   - "骑手服务态度"：关注骑手服务行为、态度（从用户视角）
   - "客服/投诉处理"：涉及投诉、客服响应、申诉
   - "价格/费用问题"：涉及跑腿费、罚款、扣款
   - "丢失/损坏"：物品丢失或损坏
   - "App体验/功能"：APP操作、定位、功能问题
   - "使用攻略/教程"：教人如何使用美团跑腿的教程
   - "竞品比较/测评"：与其他平台对比
   - "其他"：不符合以上任何类型

3. **confidence**（置信度）："high" / "medium" / "low"

返回格式（只返回JSON，不要任何解释）：
{"sentiment": "...", "feedback_type": ["...", "..."], "confidence": "..."}"""


def classify_post(post):
    title = post.get('title', '')
    body = post.get('body', '')[:300]  # 限制长度
    text = f"标题：{title}\n正文：{body}"
    
    payload = json.dumps({
        "model": MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": text}
        ],
        "temperature": 0.1,
        "max_tokens": 200,
    }).encode('utf-8')
    
    req = request.Request(
        f"{BASE_URL}/chat/completions",
        data=payload,
        headers=HEADERS,
        method="POST"
    )
    
    try:
        with request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read())
            content = result['choices'][0]['message']['content'].strip()
            # 提取JSON
            match = re.search(r'\{.*\}', content, re.DOTALL)
            if match:
                return json.loads(match.group())
            return None
    except Exception as e:
        print(f"  Error: {e}", file=sys.stderr)
        return None


def main():
    data_file = Path(__file__).parent.parent / 'output' / 'xhs_paotui_2026-03-17.json'
    output_file = Path(__file__).parent.parent / 'output' / 'llm_classified_2026-03-18.json'
    
    with open(data_file) as f:
        raw = json.load(f)
    
    posts = []
    for date, items in raw.get('by_date', {}).items():
        for item in items:
            posts.append(item)
    
    RELEVANCE_KEYWORDS = ['跑腿', '帮送', '帮买', '帮忙', '美团', '代买', '代送', '取件', '送件', '配送',
                           '同城', '上门', '急送', '帮我买', '帮我送', '帮拿', '帮取', '代跑', '众包', '骑手', '快递员', '小哥']
    OFFICIAL_ACCOUNTS = ['美团跑腿', '美团外卖', '美团官方']
    
    def is_relevant(p):
        text = (p.get('title','') + ' ' + p.get('body','')).lower()
        return any(k in text for k in RELEVANCE_KEYWORDS)
    
    def is_official(p):
        text = p.get('title','') + ' ' + p.get('body','')
        likes = int(p.get('likes', 0)) if str(p.get('likes','0')).isdigit() else 0
        return any(text.startswith(o) for o in OFFICIAL_ACCOUNTS) and likes > 200
    
    valid = [p for p in posts if is_relevant(p) and not is_official(p)]
    print(f"共 {len(valid)} 篇帖子需要分析")
    
    # 加载已有结果（断点续跑）
    results = {}
    if output_file.exists():
        with open(output_file) as f:
            results = json.load(f)
        print(f"已有 {len(results)} 篇缓存结果")
    
    for i, post in enumerate(valid):
        url = post.get('url', '')
        if url in results:
            print(f"[{i+1}/{len(valid)}] 跳过（已缓存）: {post.get('title','')[:20]}")
            continue
        
        print(f"[{i+1}/{len(valid)}] 分析: {post.get('title','')[:30]}")
        result = classify_post(post)
        
        if result:
            results[url] = result
            print(f"  → {result}")
        else:
            print(f"  → 失败，标记为neutral/其他")
            results[url] = {"sentiment": "neutral", "feedback_type": ["其他"], "confidence": "low"}
        
        # 保存进度
        with open(output_file, 'w') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        time.sleep(0.3)  # 避免限流
    
    print(f"\n完成！结果保存到 {output_file}")
    
    # 统计
    from collections import Counter
    sentiments = Counter(v['sentiment'] for v in results.values())
    print(f"正面: {sentiments['positive']}  中立: {sentiments['neutral']}  负面: {sentiments['negative']}")


if __name__ == '__main__':
    main()
