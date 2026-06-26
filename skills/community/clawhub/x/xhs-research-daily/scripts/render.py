from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any


def build_markdown_digest(topic_name: str, date_label: str, ranked_posts: list[dict[str, Any]]) -> str:
    lines = [f"# {topic_name} 日报 - {date_label}", ""]
    if not ranked_posts:
        lines.append("今天没有抓到足够高质量的新内容。")
        return "\n".join(lines)
    lines.append("## 今日重点")
    lines.append("")
    for index, item in enumerate(ranked_posts, start=1):
        post = item["post"]
        title = post.get("noteCard", {}).get("displayTitle") or "无标题"
        author = post.get("noteCard", {}).get("user", {}).get("nickname") or "未知作者"
        lines.append(f"{index}. {title} ｜ {author} ｜ score={item['score']}")
        lines.append(f"   - note_id: {post.get('id', '')}")
        lines.append(f"   - summary: {item['summary']}")
        lines.append("")
    return "\n".join(lines)


def build_xhs_post(topic_name: str, topic_config: dict[str, Any], date_label: str, ranked_posts: list[dict[str, Any]]) -> dict[str, str]:
    hashtags = " ".join(f"#{tag}" for tag in topic_config.get("post_hashtags", []))
    compact_date = date_label.replace('.', '')
    title = f"{topic_config.get('post_title_prefix', topic_name)}{compact_date}"
    if not ranked_posts:
        content = (
            f"今天又刷了一轮 {topic_name} 👀\n\n"
            f"老实说，真正让我停下来看的内容不多。\n"
            f"但这也说明一个问题：这个方向热度在涨，真正有信息量的讨论还在慢慢冒出来。\n\n"
            f"我先继续蹲。\n"
            f"后面刷到值得细聊的，再整理给大家。\n\n"
            f"{hashtags}"
        ).strip()
        return {"title": title[:20], "content": content}

    problem_lines: list[str] = []
    paper_lines: list[str] = []
    thought_lines: list[str] = []
    for item in ranked_posts[: topic_config.get('max_digest_items', 5)]:
        post = item['post']
        summary = item['summary']
        title_text = post.get('noteCard', {}).get('displayTitle') or '无标题'
        lower = summary.lower()
        problem = _infer_problem(summary)
        if problem and problem not in problem_lines:
            problem_lines.append(problem)
        paper_hint = _infer_paper_or_work(title_text, summary)
        if paper_hint and paper_hint not in paper_lines:
            paper_lines.append(paper_hint)
        thought = _infer_thought(summary, lower)
        if thought and thought not in thought_lines:
            thought_lines.append(thought)

    hook = _build_hook(problem_lines, thought_lines)
    sections = [
        hook,
        "",
        f"今天又刷了一轮 {topic_name} 相关内容。",
        "有几条确实让我停下来多想了一会儿。",
        "",
        "比起单篇帖子写得多热闹，",
        "我更在意大家反复在争什么。",
        "因为那个东西，往往更接近一个方向真正的 tension。",
        "",
        "1️⃣ 大家到底在争什么",
    ]
    if problem_lines:
        sections.extend([f"- {line}" for line in problem_lines])
    else:
        sections.append("- 大家在反复讨论 diffusion 路线到底能不能真正带来更好的推理与更快的生成。")
    sections.extend(["", "2️⃣ 我觉得值得继续跟的线索"])
    if paper_lines:
        sections.extend([f"- {line}" for line in paper_lines])
    else:
        sections.append("- 一部分帖子在讨论 diffusion-style decoding 与 reasoning 的关系，这条线值得继续往论文里挖。")
    sections.extend(["", "3️⃣ 我自己的一点判断"])
    if thought_lines:
        sections.extend([f"- {line}" for line in thought_lines])
    else:
        sections.append("- 我更想盯的不是速度宣传，而是它到底有没有带来新的 reasoning bias 和后训练空间。")
    sections.extend([
        "",
        "我现在越来越觉得，",
        f"{topic_name} 值不值得长期追，关键不在于它新不新。",
        "而在于它能不能真的改写 test-time computation 这件事。",
        "",
        "如果后面继续刷到更硬的内容，",
        "我会继续整理成这种日报。",
        "一边看热度，一边尽量把问题看清楚。",
        "",
        hashtags,
    ])
    return {"title": title[:20], "content": "\n".join(sections).strip()}


def _build_hook(problem_lines: list[str], thought_lines: list[str]) -> str:
    if problem_lines:
        first = problem_lines[0]
        if 'agent' in first.lower():
            return '最近越来越感觉，这条线不只是“快一点”这么简单。🤔'
        if '瓶颈' in first or '概率' in first:
            return '刷了一圈之后我最大的感受是：这个方向现在最缺的不是热度，是把问题讲明白。'
    if thought_lines:
        return '今天又认真刷了一轮相关内容，居然真有几条让我停下来多想了一会儿。'
    return '今天刷这个方向的时候，看到几条还挺值得记一下。'


def _infer_problem(summary: str) -> str:
    text = summary.lower()
    if 'agent' in text:
        return '一类讨论在问：它只是生成更快，还是已经开始具备做 agent planning / execution 的潜力？'
    if 'reason' in text or '推理' in summary:
        return '一类讨论聚焦在 reasoning：任意顺序生成到底是提升了推理自由度，还是反而削弱了稳定的推理路径？'
    if '概率' in summary or 'bottleneck' in text or '瓶颈' in summary:
        return '一类讨论在拆这个方向的瓶颈：问题究竟出在概率建模、采样过程，还是训练目标本身？'
    if '速度' in summary or 'faster' in text or '加速' in summary:
        return '还有一类帖子明显更关心 inference efficiency：这条路线能不能在不明显掉质量的前提下换来更高吞吐。'
    return '社区的关注点正在从“新不新”转向“到底解决了什么核心问题”。'


def _infer_paper_or_work(title_text: str, summary: str) -> str:
    combined = f'{title_text} {summary}'
    if 'LeapLab' in combined or 'Flexibility Trap' in combined:
        return '关于 arbitrary order 与 reasoning 上限的讨论，值得顺手把原论文找出来细看。'
    if 'Mercury' in combined or 'Inception Labs' in combined:
        return '速度叙事这条线还在升温，但更值得看的是速度提升背后的生成机制有没有带来新能力。'
    if 'agent' in combined.lower():
        return '已经有人在把这个方向和 agent 放在一起想了，这条线往 agentic RL 延展会很自然。'
    if '概率' in combined or 'bottleneck' in combined.lower():
        return '从概率视角拆瓶颈的内容，适合拿来对齐建模假设和训练目标。'
    return '有些讨论虽然不系统，但问题意识是对的，适合作为继续顺藤摸瓜的入口。'


def _infer_thought(summary: str, lower: str) -> str:
    if 'agent' in lower:
        return '如果这种生成方式真能带来更灵活的全局修正，那它对 long-horizon agent 可能不只是提速，而是连策略结构都会变。'
    if 'reason' in lower or '推理' in summary:
        return '我更关心的是 reasoning trace 会不会因此变得更可回退、可修正，这可能比表面 benchmark 涨点更重要。'
    if '概率' in summary or '瓶颈' in summary:
        return '这个方向不能只讲故事，最后还是得回到：训练目标、采样机制、后训练方法到底哪一块是真正的瓶颈。'
    if '速度' in summary or 'faster' in lower or '加速' in summary:
        return '单纯更快还不够，真正有意思的是：速度优势能不能转化成新的后训练空间和 test-time scaling 机制。'
    return '我现在的整体感觉是：最值得看的是它有没有带来新的 test-time computation 组织方式。'


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding='utf-8')


def now_labels() -> tuple[str, str]:
    now = datetime.now()
    return now.strftime('%Y-%m-%d'), now.strftime('%m.%d')
