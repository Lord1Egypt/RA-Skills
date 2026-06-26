#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
B站视频评论与弹幕深度分析报告生成器
基于专业分析报告格式
"""

import re
import argparse
import xml.etree.ElementTree as ET
from datetime import datetime
from collections import Counter

import requests
import jieba
from snownlp import SnowNLP

DEFAULT_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Referer': 'https://www.bilibili.com/',
    'Origin': 'https://www.bilibili.com'
}


def extract_bvid(url_or_bvid: str) -> str:
    if url_or_bvid.startswith("BV"):
        return url_or_bvid
    match = re.search(r'BV[\w]+', url_or_bvid)
    if match:
        return match.group()
    raise ValueError(f"无法从 '{url_or_bvid}' 中提取BV号")


def get_video_info(bvid: str) -> dict:
    url = f"https://api.bilibili.com/x/web-interface/view?bvid={bvid}"
    resp = requests.get(url, headers=DEFAULT_HEADERS, timeout=10)
    data = resp.json()
    if data['code'] == 0:
        info = data['data']
        return {
            'title': info.get('title', '未知标题'),
            'desc': info.get('desc', ''),
            'stat': info.get('stat', {}),
            'duration': info.get('duration', 0),
            'cid': info.get('cid', 0)
        }
    raise ValueError(f"获取视频信息失败: {data.get('message', 'Unknown error')}")


def get_danmakus(cid: str) -> list:
    url = f"https://api.bilibili.com/x/v1/dm/list.so?oid={cid}"
    resp = requests.get(url, headers=DEFAULT_HEADERS, timeout=15)
    resp.encoding = 'utf-8'
    danmakus = []
    try:
        root = ET.fromstring(resp.text)
        for d in root.findall('d'):
            p = d.get('p', '').split(',')
            if len(p) >= 5:
                danmakus.append({
                    'text': d.text or '',
                    'time': float(p[0]),
                    'type': int(p[1]),
                    'color': p[3],
                    'timestamp': int(p[4])
                })
    except ET.ParseError:
        import zlib
        try:
            decompressed = zlib.decompress(resp.content)
            root = ET.fromstring(decompressed.decode('utf-8'))
            for d in root.findall('d'):
                p = d.get('p', '').split(',')
                if len(p) >= 5:
                    danmakus.append({
                        'text': d.text or '',
                        'time': float(p[0]),
                        'type': int(p[1]),
                        'color': p[3],
                        'timestamp': int(p[4])
                    })
        except:
            pass
    return danmakus


def get_comments(bvid: str, max_pages: int = 50) -> list:
    all_comments = []
    page = 1
    while page <= max_pages:
        url = f"https://api.bilibili.com/x/v2/reply/main?next={page}&type=1&oid={bvid}&mode=3"
        resp = requests.get(url, headers=DEFAULT_HEADERS, timeout=10)
        data = resp.json()
        if data['code'] != 0:
            break
        replies = data['data'].get('replies', [])
        if not replies:
            break
        for r in replies:
            all_comments.append({
                'rpid': r.get('rpid', 0),
                'uname': r.get('member', {}).get('uname', '未知用户'),
                'content': r.get('content', {}).get('message', ''),
                'like': r.get('like', 0),
                'ctime': r.get('ctime', 0),
                'replies': r.get('replies', []) or []
            })
        if not data['data'].get('cursor', {}).get('has_more'):
            break
        page += 1
    return all_comments


def analyze_sentiment(texts: list) -> dict:
    positive = negative = neutral = 0
    sentiments = []
    for text in texts:
        if not text or len(text.strip()) < 2:
            continue
        try:
            s = SnowNLP(text)
            score = s.sentiments
            sentiments.append(score)
            if score > 0.6:
                positive += 1
            elif score < 0.4:
                negative += 1
            else:
                neutral += 1
        except:
            neutral += 1
    total = positive + negative + neutral
    return {
        'positive': positive,
        'negative': negative,
        'neutral': neutral,
        'total': total,
        'avg_score': sum(sentiments) / len(sentiments) if sentiments else 0.5,
        'positive_rate': positive / total * 100 if total > 0 else 0,
        'negative_rate': negative / total * 100 if total > 0 else 0,
        'neutral_rate': neutral / total * 100 if total > 0 else 0
    }


def extract_keywords(texts: list, top_n: int = 20) -> list:
    stopwords = set([
        '的', '了', '是', '在', '我', '有', '和', '就', '不', '人', '都', '一', '一个',
        '上', '也', '很', '到', '说', '要', '去', '你', '会', '着', '没有', '看', '好',
        '自己', '这', '这个', '那个', '什么', '怎么', '为什么', '哪', '哪个', '吗', '呢',
        '吧', '啊', '哦', '嗯', '哈', '哈哈', '哈哈哈', '哈哈哈哈哈', '呃', '唉',
        '噢', '诶', '嘿', '呀', '哟', '哇', '么', '得', '地', '被', '把',
        '给', '跟', '从', '向', '往', '比', '让', '能', '可以', '应该', '必须',
        '需要', '想要', '知道', '觉得', '感觉', '希望', '相信', '看到', '听到',
        '进行', '成为', '变成', '开始', '继续', '停止', '完成', '使用', '做',
        '等等', '这样', '那样', '怎样', '这么', '那么', '多少', '几次', '一下', '一点',
        '一些', '还有', '但是', '可是', '然而', '虽然', '因为', '所以', '如果',
        '不管', '无论', '既然', '为了', '目的', '结果', '最后', '首先', '然后',
        '终于', '总算', '原来', '其实', '当然', '果然', '竟然', '居然', '简直',
        '特别', '非常', '十分', '极其', '最', '更', '越', '太', '真', '实在',
        'bv', 'av', '视频', '弹幕', '评论', 'up', 'up主', 'b站', 'bilibili',
        'loading', '展开', '已评分', '...', '..'
    ])
    all_text = ' '.join([t for t in texts if t])
    words = jieba.cut(all_text)
    words = [w.strip() for w in words if len(w.strip()) >= 2 and w not in stopwords]
    return Counter(words).most_common(top_n)


def categorize_danmakus(danmakus: list) -> dict:
    """将弹幕分类"""
    categories = {
        '技术讨论型': [],
        '情感表达型': [],
        '玩梗调侃型': [],
        '疑问咨询型': [],
        '其他': []
    }
    tech_terms = ['怎么', '为什么', '什么', '如何', '原理', '方法', '教程', '配置', '设置', 'VPN', '代理', '协议', 'ip', 'dns', '端口', '教程']
    emotion_words = ['哈哈哈', '哈哈', '笑死', '牛逼', '厉害', '太强', '绝了', '好耶', 'awsl', '泪目', '感动', '难受', '绷不住', '难崩']
    meme_words = ['？？？', '???', '？？', '啊?', '这', '呃', '啊这', '6', '999', '233', '芜湖']

    for d in danmakus:
        text = d.get('text', '')
        if not text:
            continue
        if any(term in text for term in tech_terms):
            categories['技术讨论型'].append(text)
        elif any(term in text for term in emotion_words):
            categories['情感表达型'].append(text)
        elif any(term in text for term in meme_words) or '？' in text or '?' in text:
            categories['玩梗调侃型'].append(text)
        elif '？' in text or '?' in text or '怎么' in text or '为什么' in text:
            categories['疑问咨询型'].append(text)
        else:
            categories['其他'].append(text)

    return categories


def time_distribution(danmakus: list, duration: int) -> dict:
    """分析弹幕时间分布"""
    if duration <= 0 or not danmakus:
        return {}
    segments = 5
    segment_duration = duration / segments
    distribution = {}
    for i in range(segments):
        start = i * segment_duration
        end = (i + 1) * segment_duration
        count = sum(1 for d in danmakus if start <= d.get('time', 0) < end)
        minutes = int(start // 60)
        distribution[f"{minutes}-{minutes+3}分钟"] = count
    return distribution


def generate_professional_report(
    video_title: str,
    bvid: str,
    video_info: dict,
    danmakus: list,
    comments: list,
    output_path: str = None
) -> str:
    """生成专业分析报告"""

    danmaku_texts = [d['text'] for d in danmakus if d.get('text')]
    comment_texts = [c['content'] for c in comments if c.get('content')]

    # 情感分析
    danmaku_sentiment = analyze_sentiment(danmaku_texts)
    comment_sentiment = analyze_sentiment(comment_texts)

    # 关键词
    all_texts = danmaku_texts + comment_texts
    keywords = extract_keywords(all_texts)

    # 弹幕分类
    categorized = categorize_danmakus(danmakus)

    # 时间分布
    duration = video_info.get('duration', 0)
    time_dist = time_distribution(danmakus, duration)

    # 高赞评论
    top_comments = sorted(comments, key=lambda x: x.get('like', 0), reverse=True)[:10]
    hot_danmakus = sorted(danmakus, key=lambda x: len(x.get('text', '')), reverse=True)[:10]

    stats = video_info.get('stat', {})
    type_map = {1: '滚动', 4: '底端', 5: '顶端', 6: '逆向', 7: '高级', 8: '代码'}
    danmaku_types = Counter([d.get('type', 0) for d in danmakus])

    # 生成报告
    r = f"""# {video_title}

> **链接**: https://www.bilibili.com/video/{bvid}  
> **分析时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}

---

## 一、视频基本信息

| 指标 | 数值 |
|:-----|-----:|
| 播放量 | {stats.get('view', 0):,} |
| 点赞数 | {stats.get('like', 0):,} |
| 投币数 | {stats.get('coin', 0):,} |
| 收藏数 | {stats.get('favorite', 0):,} |
| 分享数 | {stats.get('share', 0):,} |
| 评论数 | {stats.get('reply', 0):,} |
| 弹幕数 | {len(danmakus):,} |

**视频简介**:  
{danmakus[0].get('text', '') if danmakus else video_info.get('desc', 'N/A')[:300]}{'...' if len(video_info.get('desc', '')) > 300 else ''}

---

## 二、弹幕深度分析

### 2.1 弹幕概况

- **弹幕总数**: {len(danmakus):,} 条
- **弹幕类型分布**: {', '.join([f'{type_map.get(t, str(t))}={c}' for t, c in danmaku_types.most_common(3)]) if danmaku_types else 'N/A'}

### 2.2 弹幕情感分析

| 情感类型 | 数量 | 占比 |
|:---------|-----:|-----:|
| 正面情绪 | {danmaku_sentiment['positive']:,} | {danmaku_sentiment['positive_rate']:.1f}% |
| 中性情绪 | {danmaku_sentiment['neutral']:,} | {danmaku_sentiment['neutral_rate']:.1f}% |
| 负面情绪 | {danmaku_sentiment['negative']:,} | {danmaku_sentiment['negative_rate']:.1f}% |

**综合情感评分**: {danmaku_sentiment['avg_score']:.2f} / 1.0

"""

    # 弹幕时间分布
    if time_dist:
        r += """### 2.3 弹幕时间分布特征

| 时间段 | 弹幕数量 |
|:-------|-----:|
"""
        for period, count in time_dist.items():
            bar = '█' * (count // 5 + 1)
            r += f"| {period} | {count:,} {bar} |\n"

    # 弹幕内容分类
    r += """
### 2.4 弹幕内容分类

| 类型 | 数量 | 占比 | 典型弹幕 |
|:-----|-----:|-----:|:---------|
"""
    for cat, texts in categorized.items():
        if texts:
            pct = len(texts) / len(danmaku_texts) * 100 if danmaku_texts else 0
            sample = texts[0][:30] if texts else ''
            r += f"| {cat} | {len(texts):,} | {pct:.1f}% | `{sample}` |\n"

    # 热门弹幕
    r += """
### 2.5 热门弹幕内容

"""
    for i, d in enumerate(hot_danmakus[:15], 1):
        if d.get('text'):
            time_min = int(d['time'] // 60)
            time_sec = int(d['time'] % 60)
            r += f"- `[{time_min:02d}:{time_sec:02d}]` {d['text']}\n"

    # 评论分析
    r += f"""

---

## 三、评论深度分析

### 3.1 评论概况

- **评论总数**: {len(comments):,} 条
- **采样分析数**: {len(comment_texts):,} 条

### 3.2 评论情感分析

| 情感类型 | 数量 | 占比 |
|:---------|-----:|-----:|
| 正面情绪 | {comment_sentiment['positive']:,} | {comment_sentiment['positive_rate']:.1f}% |
| 中性情绪 | {comment_sentiment['neutral']:,} | {comment_sentiment['neutral_rate']:.1f}% |
| 负面情绪 | {comment_sentiment['negative']:,} | {comment_sentiment['negative_rate']:.1f}% |

**综合情感评分**: {comment_sentiment['avg_score']:.2f} / 1.0

### 3.3 高赞评论TOP10

| 排名 | 用户 | 评论内容 | 点赞 |
|:----:|:-----|:---------|-----:|
"""

    for i, c in enumerate(top_comments, 1):
        if c.get('content'):
            content = c.get('content', '')[:40].replace('|', '\\|')
            r += f"| {i} | {c.get('uname', '未知')} | {content} | {c.get('like', 0):,} |\n"

    # 关键词
    r += """

---

## 四、关键词与话题提取

### 4.1 高频词TOP20

| 排名 | 关键词 | 频次 |
|:----:|:-------|-----:|
"""

    for i, (word, count) in enumerate(keywords, 1):
        r += f"| {i} | {word} | {count:,} |\n"

    # 综合洞察
    r += """

---

## 五、综合洞察

### 5.1 用户情感倾向

"""
    if danmaku_sentiment['avg_score'] > 0.6:
        danmaku_judge = "整体偏正面，用户反馈积极，情绪乐观"
    elif danmaku_sentiment['avg_score'] < 0.4:
        danmaku_judge = "整体偏负面，可能存在争议性内容或用户不满"
    else:
        danmaku_judge = "整体偏中性，用户讨论相对客观理性"

    if comment_sentiment['avg_score'] > 0.6:
        comment_judge = "评论正向居多，视频内容获得用户认可"
    elif comment_sentiment['avg_score'] < 0.4:
        comment_judge = "评论负向居多，视频可能存在争议或批评"
    else:
        comment_judge = "评论中性偏多，用户讨论较为理性"

    r += f"""- **弹幕情感 ({danmaku_sentiment['avg_score']:.2f}/1.0)**: {danmaku_judge}
- **评论情感 ({comment_sentiment['avg_score']:.2f}/1.0)**: {comment_judge}

### 5.2 互动热度分析

"""

    if stats.get('view', 0) > 0:
        like_rate = stats.get('like', 0) / stats.get('view', 1) * 100
        comment_rate = stats.get('reply', 0) / stats.get('view', 1) * 100
        danmaku_rate = len(danmakus) / stats.get('view', 1) * 100

        if like_rate > 5:
            like_judge = "点赞率高，内容非常受欢迎"
        elif like_rate > 2:
            like_judge = "点赞率中等，内容有一定吸引力"
        else:
            like_judge = "点赞率偏低，内容吸引力有待提升"

        r += f"""- **点赞率**: {like_rate:.2f}% → {like_judge}
- **评论率**: {comment_rate:.2f}% → {'互动性好' if comment_rate > 0.5 else '互动性中等'}
- **弹幕密度**: {danmaku_rate:.2f}% → {'弹幕氛围活跃' if danmaku_rate > 0.5 else '弹幕氛围一般'}

### 5.3 内容质量观察

"""

        if categorized['技术讨论型']:
            r += f"- 技术讨论型弹幕占比 {(len(categorized['技术讨论型']) / len(danmaku_texts) * 100):.1f}%，说明视频有一定知识含量\n"
        if categorized['情感表达型']:
            r += f"- 情感表达型弹幕占比 {(len(categorized['情感表达型']) / len(danmaku_texts) * 100):.1f}%，观众参与度高\n"

        avg_comment_len = sum(len(c) for c in comment_texts) / len(comment_texts) if comment_texts else 0
        if avg_comment_len > 50:
            r += "- 用户评论内容丰富，视频引发了深度讨论\n"
        elif avg_comment_len > 20:
            r += "- 用户评论长度适中，讨论氛围良好\n"
        else:
            r += "- 用户评论较为简短，以轻松互动为主\n"

        if duration > 0:
            r += f"- 弹幕密度: 平均每分钟 {len(danmakus) / (duration / 60):.1f} 条\n"

    # 总结
    r += f"""

---

## 六、总结评价

### 核心发现

1. **情感倾向**: 弹幕{'(positive)' if danmaku_sentiment['avg_score'] > 0.5 else '(neutral)' if danmaku_sentiment['avg_score'] > 0.4 else '(negative)'}，评论{'(positive)' if comment_sentiment['avg_score'] > 0.5 else '(neutral)' if comment_sentiment['avg_score'] > 0.4 else '(negative)'}

2. **互动特点**: {'高互动' if stats.get('like', 0) / max(stats.get('view', 1), 1) > 0.03 else '中等互动'}视频，{'弹幕氛围活跃' if len(danmakus) / max(stats.get('view', 1), 1) > 0.005 else '弹幕氛围一般'}

3. **内容特征**: {categorized['技术讨论型'] and '技术讨论较多' or '娱乐互动为主'}

### 总体评价

本视频整体{'(positive)' if (danmaku_sentiment['avg_score'] + comment_sentiment['avg_score']) / 2 > 0.55 else '(neutral)' if (danmaku_sentiment['avg_score'] + comment_sentiment['avg_score']) / 2 > 0.45 else '(negative)' }，{'获得了用户的积极反馈和认可' if danmaku_sentiment['avg_score'] > 0.5 else '引发了用户的理性讨论' if danmaku_sentiment['avg_score'] > 0.4 else '存在一定的争议或负面反馈'}。

---

## 附录

- **数据来源**: Bilibili 公开API
- **弹幕接口**: `https://api.bilibili.com/x/v1/dm/list.so`
- **评论接口**: `https://api.bilibili.com/x/v2/reply/main`
- **分析工具**: SnowNLP (情感分析), jieba (关键词提取)
- **报告生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

*本报告由AI自动生成，数据仅供参考*
"""

    if output_path:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(r)
        print(f"报告已保存到: {output_path}")

    return r


def main():
    parser = argparse.ArgumentParser(description='B站视频深度分析报告生成器')
    parser.add_argument('url', help='B站视频链接或BV号')
    parser.add_argument('-o', '--output', help='输出报告路径', default=None)
    args = parser.parse_args()

    try:
        bvid = extract_bvid(args.url)
        print(f"正在分析视频: {bvid}")

        print("正在获取视频信息...")
        video_info = get_video_info(bvid)
        title = video_info.get('title', '未知标题')

        print(f"正在获取弹幕 (共 {video_info.get('stat', {}).get('danmu', 0)} 条)...")
        cid = video_info.get('cid', 0)
        danmakus = get_danmakus(str(cid)) if cid else []
        print(f"获取到 {len(danmakus)} 条弹幕")

        print("正在获取评论...")
        comments = get_comments(bvid)
        print(f"获取到 {len(comments)} 条评论")

        print("正在生成分析报告...")
        report = generate_professional_report(
            video_title=title,
            bvid=bvid,
            video_info=video_info,
            danmakus=danmakus,
            comments=comments,
            output_path=args.output
        )

        print("\n" + "="*60)
        print("分析完成!")
        print("="*60)
        print(report)

    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()
        return


if __name__ == "__main__":
    main()
