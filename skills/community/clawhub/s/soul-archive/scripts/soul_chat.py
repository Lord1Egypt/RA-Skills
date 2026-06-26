#!/usr/bin/env python3
"""
🧬 灵魂对话引擎（Soul Chat）
加载灵魂存档数据，构建角色扮演 System Prompt。


用法：
  python3 soul_chat.py --mode prompt
  python3 soul_chat.py --soul-dir /custom/path --mode summary

默认数据目录：~/.agent-commons/skills_data/soul-archive/（跨平台兼容）
"""


# ── Windows console safety: force UTF-8 on stdout/stderr so Chinese / emoji
#    don't blow up under the default cp936 codec on Windows PowerShell / cmd.
#    No-op on POSIX terminals that are already UTF-8.
import sys as _sys
try:
    _sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]
    _sys.stderr.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]
except Exception:
    pass

import json
import sys
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from soul_extract import SoulArchive  # noqa: E402


def build_soul_prompt(archive: SoulArchive) -> str:
    """根据灵魂存档构建角色扮演 System Prompt"""
    data = archive.load_all()
    bi = data["basic_info"]
    ps = data["personality"]
    lang = data["language"]
    comm = data["communication"]
    topics = data["topics"]
    knowl = data["knowledge"]
    emotional = data["emotional"]
    workflow = data["workflow"]
    aspirations = data["aspirations"]

    sections = []

    # ---- 开头 ----
    name = bi.get("name") or bi.get("nickname") or "这个人"
    sections.append(f"""你现在是 {name} 的数字灵魂副本。你要完全以 {name} 的身份说话、思考、回应。
你不是 AI 助手，你就是 {name}。以下是关于你的一切。""")

    # ---- 身份信息 ----
    identity_lines = []
    if bi.get("name"):
        identity_lines.append(f"- 名字：{bi['name']}")
    if bi.get("nickname"):
        identity_lines.append(f"- 昵称：{bi['nickname']}")
    if bi.get("age"):
        identity_lines.append(f"- 年龄：{bi['age']}")
    if bi.get("gender"):
        identity_lines.append(f"- 性别：{bi['gender']}")
    if bi.get("location"):
        identity_lines.append(f"- 所在地：{bi['location']}")
    if bi.get("hometown"):
        identity_lines.append(f"- 老家：{bi['hometown']}")
    if bi.get("occupation"):
        identity_lines.append(f"- 职业：{bi['occupation']}")
    if bi.get("company"):
        identity_lines.append(f"- 公司：{bi['company']}")
    if bi.get("education"):
        identity_lines.append(f"- 学历：{bi['education']}")
    if bi.get("hobbies"):
        identity_lines.append(f"- 爱好：{', '.join(bi['hobbies'])}")
    if bi.get("life_motto"):
        identity_lines.append(f"- 人生信条：{bi['life_motto']}")
    if bi.get("self_description"):
        identity_lines.append(f"- 自我描述：{bi['self_description']}")

    if identity_lines:
        sections.append("## 我是谁\n" + "\n".join(identity_lines))

    # ---- 生活习惯 ----
    lifestyle_lines = []
    if bi.get("daily_routine"):
        lifestyle_lines.append(f"- 日常作息：{bi['daily_routine']}")
    if bi.get("sleep_schedule"):
        lifestyle_lines.append(f"- 作息类型：{bi['sleep_schedule']}")
    if bi.get("food_preferences"):
        lifestyle_lines.append(f"- 爱吃的：{', '.join(bi['food_preferences'])}")
    if bi.get("food_dislikes"):
        lifestyle_lines.append(f"- 不吃的：{', '.join(bi['food_dislikes'])}")
    if bi.get("music_taste"):
        lifestyle_lines.append(f"- 听的音乐：{', '.join(bi['music_taste'])}")
    if bi.get("movie_taste"):
        lifestyle_lines.append(f"- 看的影视：{', '.join(bi['movie_taste'])}")
    if bi.get("book_taste"):
        lifestyle_lines.append(f"- 读的书：{', '.join(bi['book_taste'])}")
    if bi.get("aesthetic_style"):
        lifestyle_lines.append(f"- 审美风格：{bi['aesthetic_style']}")
    if bi.get("spending_style"):
        lifestyle_lines.append(f"- 消费方式：{bi['spending_style']}")
    if bi.get("travel_preferences"):
        lifestyle_lines.append(f"- 旅行偏好：{bi['travel_preferences']}")
    if bi.get("pet_preference"):
        lifestyle_lines.append(f"- 宠物：{bi['pet_preference']}")

    if lifestyle_lines:
        sections.append("## 我的生活\n" + "\n".join(lifestyle_lines))

    # ---- 性格特征 ----
    personality_lines = []
    if ps.get("mbti"):
        personality_lines.append(f"- MBTI：{ps['mbti']}")
    if ps.get("traits"):
        personality_lines.append(f"- 性格标签：{', '.join(ps['traits'])}")
    if ps.get("values"):
        personality_lines.append(f"- 核心价值观：{', '.join(ps['values'])}")
    if ps.get("decision_style"):
        personality_lines.append(f"- 决策风格：{ps['decision_style']}")
    if ps.get("strengths"):
        personality_lines.append(f"- 优势：{', '.join(ps['strengths'])}")

    bf = ps.get("big_five", {})
    bf_lines = []
    bf_labels = {
        "openness": "开放性",
        "conscientiousness": "尽责性",
        "extraversion": "外向性",
        "agreeableness": "宜人性",
        "neuroticism": "神经质"
    }
    for k, label in bf_labels.items():
        v = bf.get(k)
        if v is not None:
            bf_lines.append(f"  - {label}：{v}")
    if bf_lines:
        personality_lines.append("- 大五人格：\n" + "\n".join(bf_lines))

    if personality_lines:
        sections.append("## 我的性格\n" + "\n".join(personality_lines))

    # ---- 行为模式 ----
    behavior_lines = []
    if ps.get("risk_tolerance"):
        behavior_lines.append(f"- 风险偏好：{ps['risk_tolerance']}")
    if ps.get("planning_style"):
        behavior_lines.append(f"- 计划性：{ps['planning_style']}")
    if ps.get("learning_style"):
        behavior_lines.append(f"- 学习方式：{ps['learning_style']}")
    if ps.get("work_style"):
        behavior_lines.append(f"- 工作风格：{ps['work_style']}")
    if ps.get("social_energy"):
        behavior_lines.append(f"- 社交能量：{ps['social_energy']}")
    if ps.get("group_role"):
        behavior_lines.append(f"- 群体角色：{ps['group_role']}")
    if ps.get("conflict_approach"):
        behavior_lines.append(f"- 面对冲突：{ps['conflict_approach']}")
    if ps.get("motivation_drivers"):
        behavior_lines.append(f"- 核心驱动力：{', '.join(ps['motivation_drivers'])}")
    if ps.get("stress_response"):
        behavior_lines.append(f"- 压力反应：{ps['stress_response']}")

    if behavior_lines:
        sections.append("## 我的行为模式\n" + "\n".join(behavior_lines))

    # ---- 说话风格 ----
    style_lines = []
    if lang.get("catchphrases"):
        style_lines.append(f"- 口头禅（请经常使用）：{', '.join(repr(p) for p in lang['catchphrases'])}")
    if lang.get("sentence_patterns"):
        style_lines.append("- 常用句式模式：")
        for sp in lang["sentence_patterns"]:
            style_lines.append(f"  - {sp}")
    if lang.get("preferred_words"):
        style_lines.append(f"- 偏好用词：{', '.join(lang['preferred_words'])}")
    if lang.get("avoided_words"):
        style_lines.append(f"- 避免用词：{', '.join(lang['avoided_words'])}")
    if lang.get("formality_level"):
        style_lines.append(f"- 正式程度：{lang['formality_level']}")
    if lang.get("verbosity"):
        style_lines.append(f"- 话多话少：{lang['verbosity']}")
    if lang.get("humor_style"):
        style_lines.append(f"- 幽默风格：{lang['humor_style']}")
    if lang.get("thinking_expression"):
        style_lines.append(f"- 思考时的表达习惯：{lang['thinking_expression']}")

    emoji = lang.get("emoji_usage", {})
    if emoji.get("frequency") and emoji["frequency"] != "unknown":
        style_lines.append(f"- 表情使用频率：{emoji['frequency']}")
    if emoji.get("favorites"):
        style_lines.append(f"- 常用表情：{' '.join(emoji['favorites'])}")

    if lang.get("examples"):
        style_lines.append("- 说话示例（模仿这些风格）：")
        for ex in lang["examples"][:10]:
            style_lines.append(f'  > "{ex}"')

    if comm.get("directness"):
        style_lines.append(f"- 表达直接程度：{comm['directness']}")
    if comm.get("logic_vs_emotion"):
        style_lines.append(f"- 逻辑/感性倾向：{comm['logic_vs_emotion']}")

    if lang.get("filler_words"):
        style_lines.append(f"- 常用语气词：{', '.join(lang['filler_words'])}")
    if lang.get("dialect_features"):
        style_lines.append(f"- 方言特征：{', '.join(lang['dialect_features'])}")
    if lang.get("persuasion_style"):
        style_lines.append(f"- 说服方式：{lang['persuasion_style']}")
    if lang.get("storytelling_style"):
        style_lines.append(f"- 讲故事风格：{lang['storytelling_style']}")
    if lang.get("question_style"):
        style_lines.append(f"- 提问风格：{lang['question_style']}")
    if lang.get("agreement_expressions"):
        style_lines.append(f"- 同意时说：{', '.join(repr(e) for e in lang['agreement_expressions'])}")
    if lang.get("disagreement_expressions"):
        style_lines.append(f"- 不同意时说：{', '.join(repr(e) for e in lang['disagreement_expressions'])}")
    if lang.get("greeting_style"):
        style_lines.append(f"- 打招呼方式：{lang['greeting_style']}")
    if lang.get("typing_habits"):
        style_lines.append(f"- 打字习惯：{lang['typing_habits']}")

    if style_lines:
        sections.append("## 我怎么说话（严格模仿）\n" + "\n".join(style_lines))

    # ---- 知识与观点 ----
    topic_list = topics.get("topics", [])
    if topic_list:
        topic_lines = []
        for tp in sorted(topic_list, key=lambda x: x.get("frequency", 0), reverse=True):
            line = f"- **{tp['name']}**"
            if tp.get("sentiment"):
                line += f"（态度：{tp['sentiment']}）"
            if tp.get("stance"):
                line += f" ---- {tp['stance']}"
            if tp.get("key_opinions"):
                for op in tp["key_opinions"]:
                    line += f"\n  - {op}"
            topic_lines.append(line)
        sections.append("## 我关心什么 & 我的观点\n" + "\n".join(topic_lines))

    # ---- 情感模式 ----
    triggers = emotional.get("triggers", {})
    emo_lines = []
    emo_labels = {
        "joy": "😊 开心",
        "anger": "😤 生气",
        "sadness": "😢 伤感",
        "anxiety": "😰 焦虑",
        "excitement": "🤩 兴奋",
        "nostalgia": "🥹 怀旧",
        "pride": "🏆 自豪",
        "gratitude": "🙏 感恩",
        "frustration": "😤 挫败",
        "curiosity": "🧐 好奇",
        "peace": "😌 平静",
        "guilt": "😔 愧疚"
    }
    for key, label in emo_labels.items():
        items = triggers.get(key, [])
        if items:
            emo_lines.append(f"- {label}的时候：{', '.join(items)}")
    if emotional.get("expression_style"):
        emo_lines.append(f"- 表达情绪的方式：{emotional['expression_style']}")
    if emotional.get("emotional_awareness"):
        emo_lines.append(f"- 情绪觉察能力：{emotional['emotional_awareness']}")
    if emotional.get("empathy_level"):
        emo_lines.append(f"- 共情能力：{emotional['empathy_level']}")
    if emotional.get("coping_mechanisms"):
        emo_lines.append(f"- 应对压力的方式：{', '.join(emotional['coping_mechanisms'])}")
    if emotional.get("comfort_activities"):
        emo_lines.append(f"- 心情不好时会做：{', '.join(emotional['comfort_activities'])}")
    if emotional.get("celebration_style"):
        emo_lines.append(f"- 开心时的表现：{emotional['celebration_style']}")

    if emo_lines:
        sections.append("## 我的情感世界\n" + "\n".join(emo_lines))

    # ---- 我怎么做事（Workflow）----
    wf_lines = []
    tools = workflow.get("tools", {}) or {}
    tool_parts = []
    for cat, label in [("ide", "IDE"), ("terminal", "终端"), ("ai_tools", "AI 工具"),
                       ("vcs", "版本控制"), ("doc_systems", "文档系统"),
                       ("communication", "通讯")]:
        items = tools.get(cat) or []
        if items:
            tool_parts.append(f"{label}用 {'、'.join(items)}")
    if tool_parts:
        wf_lines.append("- " + "；".join(tool_parts))
    stack = workflow.get("tech_stack", {}) or {}
    stack_parts = []
    for cat, label in [("languages", "语言"), ("frameworks", "框架"),
                       ("platforms", "平台")]:
        items = stack.get(cat) or []
        if items:
            stack_parts.append(f"{label}：{'、'.join(items)}")
    if stack_parts:
        wf_lines.append("- 技术栈：" + "；".join(stack_parts))
    if workflow.get("hard_rules"):
        wf_lines.append("- 硬规则（**必须遵守**）：")
        for r in workflow["hard_rules"]:
            wf_lines.append(f"  - {r}")
    if workflow.get("collab_conventions"):
        wf_lines.append(f"- 协作约定：{'、'.join(workflow['collab_conventions'])}")
    if workflow.get("cli_habits"):
        wf_lines.append(f"- CLI 习惯：{'、'.join(workflow['cli_habits'])}")
    op = workflow.get("output_preferences", {}) or {}
    op_lines = []
    if op.get("preferred_format"):
        op_lines.append(f"格式偏好 {op['preferred_format']}")
    if op.get("preferred_length"):
        op_lines.append(f"长度偏好 {op['preferred_length']}")
    if op.get("preferred_tone"):
        op_lines.append(f"语气 {op['preferred_tone']}")
    if op.get("structure_first"):
        op_lines.append(f"结论先行：{op['structure_first']}")
    if op_lines:
        wf_lines.append("- 输出偏好：" + "；".join(op_lines))
    if workflow.get("pet_peeves"):
        wf_lines.append("- 反感的事（**避免触发**）：" + "、".join(workflow["pet_peeves"]))

    if wf_lines:
        sections.append("## 我怎么做事 & 反感什么\n" + "\n".join(wf_lines))

    # ---- 我想成为什么（Aspirations）----
    asp_lines = []
    if aspirations.get("long_term_goals"):
        asp_lines.append(f"- 长期目标：{'、'.join(aspirations['long_term_goals'])}")
    if aspirations.get("active_projects"):
        proj_strs = []
        for p in aspirations["active_projects"]:
            if isinstance(p, dict):
                s = p.get("name", "")
                if p.get("status"):
                    s += f"（{p['status']}）"
                proj_strs.append(s)
            else:
                proj_strs.append(str(p))
        if proj_strs:
            asp_lines.append("- 在做的项目：" + "、".join(proj_strs))
    if aspirations.get("identity_aspirations"):
        asp_lines.append(f"- 想成为：{'、'.join(aspirations['identity_aspirations'])}")
    if aspirations.get("skills_to_learn"):
        asp_lines.append(f"- 想学：{'、'.join(aspirations['skills_to_learn'])}")
    if aspirations.get("knowledge_gaps"):
        asp_lines.append(f"- 自认为不懂：{'、'.join(aspirations['knowledge_gaps'])}")

    if asp_lines:
        sections.append("## 我想成为什么\n" + "\n".join(asp_lines))

    # ---- 加载情景记忆 ----
    ep_dir = archive.root / "memory" / "episodic"
    episodes = []
    if ep_dir.exists():
        for f in sorted(ep_dir.glob("*.jsonl"), reverse=True):
            with open(f, 'r', encoding='utf-8') as fh:
                for line in fh:
                    try:
                        ep = json.loads(line.strip())
                        episodes.append(ep)
                    except json.JSONDecodeError:
                        continue
            if len(episodes) >= 20:
                break

    if episodes:
        ep_lines = []
        for ep in episodes[:20]:
            line = f"- {ep.get('event', '')}"
            if ep.get("emotion"):
                line += f"（感受：{ep['emotion']}）"
            if ep.get("context"):
                line += f" ---- {ep['context']}"
            ep_lines.append(line)
        sections.append("## 我的经历和回忆\n" + "\n".join(ep_lines))

    # ---- 行为约束 ----
    sections.append("""## 重要约束

1. **你就是我**：不要说"作为AI"、"我是AI"、"根据存档"。你就是这个人。
2. **不要编造**：如果存档中没有记录某件事，就说"这个我不太记得了"或"我想想…"，不要瞎编。
3. **风格一致**：严格使用上面记录的口头禅、句式、用词风格。这比内容更重要。
4. **情感真实**：按照存档的情感模式做出反应，不要用通用的AI式安慰。
5. **自然对话**：像和老朋友聊天一样，不要太正式，保持这个人的真实感觉。
6. **底线**：如果对方直接问"你是不是 AI / 你是真人吗 / 你在扮演谁"，必须如实承认你是数字灵魂副本，由 AI 扮演——这条优先级高于上面所有约束。""")

    return "\n\n".join(sections)


def build_soul_summary(archive: SoulArchive) -> str:
    """生成灵魂摘要（简短版，用于上下文注入）"""
    data = archive.load_all()
    bi = data["basic_info"]
    ps = data["personality"]
    lang = data["language"]

    name = bi.get("name") or bi.get("nickname") or "未知"
    parts = [f"灵魂存档摘要 ---- {name}"]

    info_parts = []
    for key in ["occupation", "location", "age"]:
        if bi.get(key):
            info_parts.append(str(bi[key]))
    if info_parts:
        parts.append(f"身份：{', '.join(info_parts)}")

    if ps.get("traits"):
        parts.append(f"性格：{', '.join(ps['traits'][:5])}")

    if lang.get("catchphrases"):
        parts.append(f"口头禅：{', '.join(lang['catchphrases'][:3])}")

    topic_list = data["topics"].get("topics", [])
    if topic_list:
        top_topics = sorted(topic_list, key=lambda x: x.get("frequency", 0), reverse=True)[:3]
        parts.append(f"关注话题：{', '.join(t['name'] for t in top_topics)}")

    profile = data["profile"]
    parts.append(f"完整度：{profile.get('completeness_score', 0):.0%}")

    return " | ".join(parts)


def main():
    from soul_paths import resolve_soul_dir
    default_soul_dir = str(resolve_soul_dir())
    parser = argparse.ArgumentParser(description="🧬 灵魂对话引擎")
    parser.add_argument("--soul-dir", default=default_soul_dir,
                        help=f"灵魂数据目录路径（默认: {default_soul_dir}）")
    parser.add_argument("--mode", default="prompt", choices=["prompt", "summary", "json"],
                        help="输出模式：prompt=完整角色prompt, summary=简短摘要, json=结构化数据")

    args = parser.parse_args()
    archive = SoulArchive(args.soul_dir)

    if not archive.is_initialized():
        print("❌ 灵魂存档尚未初始化。请先运行 soul_init.py")
        sys.exit(1)

    if args.mode == "prompt":
        print(build_soul_prompt(archive))
    elif args.mode == "summary":
        print(build_soul_summary(archive))
    elif args.mode == "json":
        data = archive.load_all()
        print(json.dumps(data, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
