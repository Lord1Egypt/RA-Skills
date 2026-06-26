#!/usr/bin/env python3
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _encoding_compat

"""
🧬 用户分身·风格克隆引擎 (Style Clone Engine)
输入：你的文章、笔记、聊天记录
输出：20+ 维语言指纹 + 风格化文本生成
理念：不只是分析"写了什么"，而是捕捉"怎么写"——让你的 AI 分身真正像你。
"""

import os
import re
import json
import math
import random
from collections import Counter
from pathlib import Path

class StyleFingerprint:
    def __init__(self):
        self.dimensions = {}
        self.corpus = ""
        self.sentences = []
        self.words = []

    def analyze(self, text):
        if not text or len(text.strip()) < 50:
            raise ValueError("文本太短，至少需要 50 个字符才能分析风格")

        self.corpus = text
        self.sentences = self._split_sentences(text)
        self.words = self._tokenize(text)

        self.dimensions = {
            "sentence_length": self._sentence_length_stats(),
            "punctuation": self._punctuation_style(),
            "emoji": self._emoji_style(),
            "vocabulary": self._vocabulary_profile(),
            "formality": self._formality_score(),
            "expressiveness": self._expressiveness_profile(),
            "paragraphing": self._paragraphing_style(),
            "person_ratio": self._person_pronoun_ratio(),
            "formatting": self._formatting_habits(),
            "rhythm": self._rhythm_score(),
            "sentiment_words": self._sentiment_profile(),
            "quote_style": self._quote_habit(),
        }

        self.dimensions["overall_label"] = self._generate_label()
        self.dimensions["vivid_description"] = self._vivid_description()
        return self.dimensions

    def analyze_files(self, paths):
        all_text = ""
        for p in paths:
            path = Path(p)
            if not path.exists():
                print(f"⚠️ 跳过不存在的文件：{p}")
                continue
            if path.is_dir():
                for f in path.rglob("*"):
                    if f.suffix in (".md", ".txt", ".py"):
                        all_text += f.read_text(encoding="utf-8", errors="ignore") + "\n\n"
            else:
                all_text += path.read_text(encoding="utf-8", errors="ignore") + "\n\n"
        return self.analyze(all_text)

    def _split_sentences(self, text):
        raw = re.split(r'[。！？!?\n]+', text)
        return [s.strip() for s in raw if len(s.strip()) > 1]

    def _tokenize(self, text):
        tokens = []
        for ch in text:
            if '\u4e00' <= ch <= '\u9fff':
                tokens.append(ch)
            elif ch.isalpha():
                if tokens and tokens[-1] and tokens[-1][-1].isalpha() if tokens[-1] else True:
                    tokens[-1] = (tokens[-1] if tokens[-1] else "") + ch
                else:
                    tokens.append(ch)
        return [t for t in tokens if len(t) > 0]

    def _sentence_length_stats(self):
        lengths = [len(s) for s in self.sentences]
        if not lengths:
            return {"avg": 0, "median": 0, "min": 0, "max": 0, "style": "未知"}
        lengths.sort()
        n = len(lengths)
        return {
            "avg": round(sum(lengths) / n, 1),
            "median": lengths[n // 2],
            "min": lengths[0],
            "max": lengths[-1],
            "short_ratio": round(sum(1 for l in lengths if l < 15) / n, 2),
            "long_ratio": round(sum(1 for l in lengths if l > 80) / n, 2),
            "style": "短句控" if lengths[n // 2] < 25 else ("长句控" if lengths[n // 2] > 50 else "长短兼备"),
        }

    def _punctuation_style(self):
        text = self.corpus
        stats = {
            "句号": text.count("。"),
            "逗号": text.count("，"),
            "感叹号": text.count("！") + text.count("!"),
            "问号": text.count("？") + text.count("?"),
            "冒号": text.count("：") + text.count(":"),
            "分号": text.count("；") + text.count(";"),
            "省略号": text.count("…") + text.count("..."),
            "破折号": text.count("——") + text.count("--"),
            "括号": text.count("（") + text.count("("),
            "引号": text.count("「") + text.count("」") + text.count('"'),
        }
        total = sum(stats.values()) or 1
        top = Counter(stats).most_common(3)

        comma_period_ratio = (stats["逗号"] + 1) / (stats["句号"] + 1)
        exclaim_ratio = (stats["感叹号"] + 1) / (stats["句号"] + 1)

        habit = []
        if exclaim_ratio > 0.3:
            habit.append("感叹号爱好者")
        if comma_period_ratio > 4:
            habit.append("长句流水")
        if stats["省略号"] > total * 0.05:
            habit.append("欲言又止型")
        if stats["问号"] > total * 0.1:
            habit.append("爱提问")
        if stats["破折号"] > total * 0.03:
            habit.append("破折号控")

        return {
            "counts": stats,
            "top3": top,
            "comma_period_ratio": round(comma_period_ratio, 2),
            "exclaim_ratio": round(exclaim_ratio, 2),
            "habits": habit or ["标点规范型"],
        }

    def _emoji_style(self):
        emoji_pattern = re.compile(
            "[\U0001F300-\U0001F9FF\U0001FA00-\U0001FA6F"
            "\U0001FA70-\U0001FAFF\U00002702-\U000027B0"
            "\U000024C2-\U0001F251\u2600-\u26FF\u2700-\u27BF"
            "\u2B50\u2764\u2705\u274C\u2753\u2757\u2795-\u2797"
            "\u3030\u303D\u3297\u3299\u25AA\u25AB\u25B6\u25C0"
            "\u25FB-\u25FE\u2615\u231A\u231B\u2328\u23CF"
            "\u23E9-\u23F3\u23F8-\u23FA\u200D\uFE0F"
            "\U0001F000-\U0001FFFF\u00A9\u00AE]",
            re.UNICODE,
        )
        emojis = emoji_pattern.findall(self.corpus)
        counter = Counter(emojis)

        chinese_emoji = re.findall(r'[😂❤️🔥😭😊👍🥰😅🤔💪🙏😢🎉😍🤣💕]', self.corpus)
        all_emoji = emojis + chinese_emoji
        counter_all = Counter(all_emoji)

        return {
            "count": len(all_emoji),
            "density": round(len(all_emoji) / max(len(self.sentences), 1), 2),
            "top5": counter_all.most_common(5),
            "style": "表情包大户" if len(all_emoji) > len(self.sentences) * 0.3
                     else ("适度表情" if len(all_emoji) > 0 else "纯文字派"),
        }

    def _vocabulary_profile(self):
        char_counter = Counter(self.words)
        total_chars = len(self.words)
        unique_chars = len(char_counter)

        common_starts = Counter()
        common_ends = Counter()
        for w in self.words:
            if len(w) >= 2:
                common_starts[w[:2]] += 1
                common_ends[w[-2:]] += 1

        freq_words = Counter()
        for i in range(len(self.words) - 1):
            bigram = self.words[i] + self.words[i + 1] if i + 1 < len(self.words) else ""
            if len(bigram) >= 2:
                freq_words[bigram] += 1

        return {
            "total_chars": total_chars,
            "unique_chars": unique_chars,
            "diversity": round(unique_chars / max(total_chars, 1), 3),
            "top_bigrams": freq_words.most_common(15),
            "common_starts": common_starts.most_common(8),
            "common_ends": common_ends.most_common(8),
            "label": "词汇丰富" if unique_chars / max(total_chars, 1) > 0.7
                     else ("适中" if unique_chars / max(total_chars, 1) > 0.4 else "口语化"),
        }

    def _formality_score(self):
        text = self.corpus
        formal_markers = [
            "综上所述", "因此", "然而", "此外", "值得注意的是",
            "笔者认为", "研究表明", "由此可见", "换言之", "从某种意义",
            "基于", "本文", "论证", "结论", "推导",
        ]
        casual_markers = [
            "嘛", "啦", "呀", "哦", "呗", "哈",
            "真的", "超", "太", "好", "吧",
            "我觉得", "感觉", "应该", "可能", "大概",
            "嘿嘿", "哈哈", "嗯嗯", "啊啊", "嘻嘻",
        ]
        formal_count = sum(text.count(m) for m in formal_markers)
        casual_count = sum(text.count(m) for m in casual_markers)
        total = max(formal_count + casual_count, 1)
        formal_ratio = formal_count / total

        return {
            "formal_count": formal_count,
            "casual_count": casual_count,
            "ratio": round(formal_ratio, 2),
            "level": "学术严谨型" if formal_ratio > 0.6
                     else ("朋友聊天型" if formal_ratio < 0.3 else "半正式型"),
            "top_formal": [m for m in formal_markers if m in text][:5],
            "top_casual": [m for m in casual_markers if m in text][:5],
        }

    def _expressiveness_profile(self):
        text = self.corpus
        intensifiers = ["非常", "极其", "特别", "十分", "超级", "太", "真的", "绝了"]
        hedges = ["可能", "也许", "大概", "好像", "似乎", "感觉", "应该"]

        adj_pattern = re.compile(r'(很|非常|极其|特别|十分|超级|太)\S{1,3}')
        adverbs = adj_pattern.findall(text)

        return {
            "intensifier_count": sum(text.count(w) for w in intensifiers),
            "hedge_count": sum(text.count(w) for w in hedges),
            "intensifier_density": round(sum(text.count(w) for w in intensifiers) / max(len(self.sentences), 1), 2),
            "hedge_density": round(sum(text.count(w) for w in hedges) / max(len(self.sentences), 1), 2),
            "style": "果断直接型" if sum(text.count(w) for w in hedges) < len(self.sentences) * 0.1
                     else ("谨慎留白型" if sum(text.count(w) for w in hedges) > len(self.sentences) * 0.3
                           else "平衡型"),
        }

    def _paragraphing_style(self):
        paragraphs = [p.strip() for p in self.corpus.split("\n\n") if p.strip()]
        lengths = [len(p) for p in paragraphs]
        if not lengths:
            return {"avg": 0, "style": "未知"}
        return {
            "count": len(paragraphs),
            "avg_length": round(sum(lengths) / len(lengths), 1),
            "style": "短段落风" if sum(lengths) / len(lengths) < 150
                     else ("长段落风" if sum(lengths) / len(lengths) > 400 else "适中"),
        }

    def _person_pronoun_ratio(self):
        text = self.corpus
        first = sum(text.count(w) for w in ["我", "我们", "我的", "我们的"])
        second = sum(text.count(w) for w in ["你", "你们", "你的", "你们的", "您"])
        third = sum(text.count(w) for w in ["他", "她", "它", "他们", "她们", "它们"])
        total = max(first + second + third, 1)
        return {
            "first_person_ratio": round(first / total, 2),
            "second_person_ratio": round(second / total, 2),
            "third_person_ratio": round(third / total, 2),
            "style": "自我表达型" if first / total > 0.5
                     else ("对话型" if second / total > 0.4 else "客观叙述型"),
        }

    def _formatting_habits(self):
        text = self.corpus
        return {
            "uses_bullet_list": "✅" if ("- " in text or "* " in text) else "❌",
            "uses_numbered_list": "✅" if re.search(r'\d+[\.\、]', text) else "❌",
            "uses_table": "✅" if "| " in text else "❌",
            "uses_code_block": "✅" if "```" in text else "❌",
            "uses_bold": "✅" if "**" in text else "❌",
            "uses_heading": "✅" if re.search(r'^#{1,6}\s', text, re.MULTILINE) else "❌",
            "uses_blockquote": "✅" if "> " in text else "❌",
            "uses_horizontal_rule": "✅" if "---" in text else "❌",
        }

    def _rhythm_score(self):
        lengths = [len(s) for s in self.sentences]
        if len(lengths) < 3:
            return {"variance": 0, "style": "无法判断"}
        variance = round(sum((l - sum(lengths) / len(lengths)) ** 2 for l in lengths) / len(lengths), 1)
        return {
            "variance": variance,
            "style": "节奏多变" if variance > 800 else ("节奏平稳" if variance > 300 else "节奏统一"),
        }

    def _sentiment_profile(self):
        positive = ["好", "棒", "赞", "优秀", "厉害", "成功", "完美", "开心", "喜欢", "爱",
                     "高效", "实用", "简洁", "优雅", "惊艳", "卓越", "强大", "优秀"]
        negative = ["差", "烂", "失败", "糟糕", "难", "复杂", "麻烦", "错误", "问题", "坑",
                     "慢", "卡", "崩溃", "没用", "不行", "失望", "困惑"]
        pos_count = sum(self.corpus.count(w) for w in positive)
        neg_count = sum(self.corpus.count(w) for w in negative)
        total = max(pos_count + neg_count, 1)
        return {
            "positive_ratio": round(pos_count / total, 2),
            "negative_ratio": round(neg_count / total, 2),
            "tone": "积极乐观型" if pos_count > neg_count * 2
                    else ("批判反思型" if neg_count > pos_count * 2 else "中性"),
        }

    def _quote_habit(self):
        text = self.corpus
        cn_quotes = text.count("「") + text.count("」")
        en_quotes = text.count('"')
        return {
            "chinese_quotes": cn_quotes,
            "english_quotes": en_quotes,
            "style": "爱引用" if cn_quotes + en_quotes > 5 else "少引用",
        }

    def _generate_label(self):
        parts = []
        d = self.dimensions
        if d.get("formality", {}).get("level") == "朋友聊天型":
            parts.append("随和")
        elif d.get("formality", {}).get("level") == "学术严谨型":
            parts.append("严谨")
        else:
            parts.append("半正式")

        if d.get("sentence_length", {}).get("style") == "短句控":
            parts.append("利落")
        elif d.get("sentence_length", {}).get("style") == "长句控":
            parts.append("绵长")

        if d.get("emoji", {}).get("style") == "表情包大户":
            parts.append("活泼")
        elif d.get("emoji", {}).get("style") == "纯文字派":
            parts.append("严肃")

        persona_types = {
            ("随和", "利落", "活泼"): "邻家高手",
            ("随和", "利落", "严肃"): "直率实干家",
            ("随和", "绵长", "活泼"): "温暖絮叨者",
            ("随和", "绵长", "严肃"): "深度思考者",
            ("严谨", "利落", "严肃"): "冷面专家",
            ("严谨", "绵长", "严肃"): "学院派学者",
            ("严谨", "利落", "活泼"): "幽默大师",
            ("严谨", "绵长", "活泼"): "儒雅风趣者",
            ("半正式", "利落", "严肃"): "务实派",
            ("半正式", "绵长", "严肃"): "娓娓道来者",
            ("半正式", "利落", "活泼"): "轻松达人",
            ("半正式", "绵长", "活泼"): "故事大王",
        }
        key = tuple(parts) if len(parts) >= 2 else ("半正式", "利落", "严肃")
        for k, v in persona_types.items():
            if all(p in key for p in k):
                return v
        return "独特灵魂"

    def _vivid_description(self):
        d = self.dimensions
        lines = []

        sl = d.get("sentence_length", {})
        lines.append(f"每句话平均 {sl.get('avg', '?')} 个字，{sl.get('style', '')}。")

        pct = d.get("punctuation", {})
        habits = pct.get("habits", [])
        if habits:
            lines.append(f"标点习惯：{'、'.join(habits)}。")

        emoji = d.get("emoji", {})
        lines.append(f"Emoji 密度 {emoji.get('density', 0)}/句，{emoji.get('style', '')}。"
                     if emoji.get('style') != '纯文字派' else "不爱用表情，靠文字说话。")

        form = d.get("formality", {})
        lines.append(f"语气 {form.get('level', '')}，{form.get('ratio', 0.5) * 100:.0f}% 偏正式。")

        expr = d.get("expressiveness", {})
        lines.append(f"表达风格：{expr.get('style', '')}。")

        rhythm = d.get("rhythm", {})
        lines.append(f"节奏：{rhythm.get('style', '')}。")

        vocab = d.get("vocabulary", {})
        lines.append(f"词汇 {vocab.get('label', '')}，{vocab.get('diversity', 0) * 100:.1f}% 不重复。")

        return "\n".join(lines)

    def save(self, path):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.dimensions, f, ensure_ascii=False, indent=2, default=str)
        print(f"💾 风格指纹已保存：{path}")

    def load(self, path):
        with open(path, "r", encoding="utf-8") as f:
            self.dimensions = json.load(f)
        return self.dimensions


class StyleMimic:
    def __init__(self, fingerprint):
        self.fp = fingerprint

    def rewrite(self, text):
        fp = self.fp
        style = fp.get("sentence_length", {}).get("style", "")
        avg_len = fp.get("sentence_length", {}).get("avg", 30)

        sentences = re.split(r'[。！？!?\n]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]

        result = []
        for s in sentences:
            if style == "短句控":
                parts = re.split(r'[，,;；]', s)
                parts = [p.strip() for p in parts if p.strip()]
                for p in parts:
                    if len(p) > avg_len * 1.5:
                        mid = len(p) // 2
                        idx = p.rfind("，", 0, mid + 10)
                        if idx < 0:
                            idx = p.find("，", mid - 10)
                        if idx > 0:
                            result.append(p[:idx] + "。")
                            result.append(p[idx + 1:])
                        else:
                            result.append(p)
                    else:
                        result.append(p)
            elif style == "长句控":
                merged = "，".join(sentences[:3])
                result.append(merged)
            else:
                result.append(s)

        habits = fp.get("punctuation", {}).get("habits", [])
        final_text = "。".join(result)

        if "感叹号爱好者" in habits:
            final_text = final_text.replace("。", "！", final_text.count("。") // 4)
        if "欲言又止型" in habits:
            final_text += "…" + "…"

        formality = fp.get("formality", {}).get("level", "")
        casual_list = fp.get("formality", {}).get("top_casual", [])
        if formality == "朋友聊天型" and casual_list and random.random() > 0.7:
            final_text = random.choice(casual_list) + "，" + final_text

        emoji_style = fp.get("emoji", {})
        top_emojis = emoji_style.get("top5", [])
        if emoji_style.get("style") != "纯文字派" and top_emojis and len(final_text) > 30:
            final_text += " " + random.choice(top_emojis)[0]

        return final_text


def main():
    import argparse
    parser = argparse.ArgumentParser(description="🧬 用户分身·风格克隆引擎")
    sub = parser.add_subparsers(dest="command")

    analyze = sub.add_parser("analyze", help="分析你的写作风格")
    analyze.add_argument("input", nargs="+", help="输入文件或目录（.md/.txt）")
    analyze.add_argument("--save", default="style_fingerprint.json", help="保存指纹到文件")

    profile = sub.add_parser("profile", help="查看已有指纹的可读报告")
    profile.add_argument("fingerprint", help="风格指纹 JSON 文件")
    profile.add_argument("--html", action="store_true", help="输出 HTML 报告")

    mimic = sub.add_parser("mimic", help="将文本改写成你的风格")
    mimic.add_argument("text", help="要改写的文本")
    mimic.add_argument("--fingerprint", default="style_fingerprint.json", help="风格指纹文件")

    args = parser.parse_args()

    if args.command == "analyze":
        sf = StyleFingerprint()
        sf.analyze_files(args.input)
        sf.save(args.save)
        print("\n" + "=" * 60)
        print(f"🧬 风格标签：{sf.dimensions.get('overall_label', '未知')}")
        print("=" * 60)
        print(sf.dimensions.get("vivid_description", ""))
        print("=" * 60)

    elif args.command == "profile":
        sf = StyleFingerprint()
        fp = sf.load(args.fingerprint)
        if args.html:
            html = _render_html_report(fp)
            out = args.fingerprint.replace(".json", ".html")
            with open(out, "w", encoding="utf-8") as f:
                f.write(html)
            print(f"📄 HTML 报告已生成：{out}")
        else:
            print(f"\n🧬 风格标签：{fp.get('overall_label', '未知')}\n")
            print(fp.get("vivid_description", ""))
            print("\n--- 完整指纹 ---")
            print(json.dumps(fp, ensure_ascii=False, indent=2))

    elif args.command == "mimic":
        sf = StyleFingerprint()
        fp = sf.load(args.fingerprint)
        sm = StyleMimic(fp)
        result = sm.rewrite(args.text)
        print(result)

    else:
        parser.print_help()


def _render_html_report(fp):
    sl = fp.get("sentence_length", {})
    pct = fp.get("punctuation", {})
    emoji = fp.get("emoji", {})
    form = fp.get("formality", {})
    expr = fp.get("expressiveness", {})
    person = fp.get("person_ratio", {})
    fmt = fp.get("formatting", {})
    vocab = fp.get("vocabulary", {})
    para = fp.get("paragraphing", {})
    rhythm = fp.get("rhythm", {})
    sentiment = fp.get("sentiment_words", {})

    emoji_top = "".join(e[0] for e in emoji.get("top5", [])[:5]) or "—"

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>🧬 风格指纹报告 - {fp.get('overall_label', '')}</title>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ font-family: 'PingFang SC', 'Microsoft YaHei', sans-serif; background: linear-gradient(135deg, #0f0c29, #302b63, #24243e); color: #e0e0e0; min-height: 100vh; padding: 40px 20px; }}
.container {{ max-width: 800px; margin: 0 auto; }}
.header {{ text-align: center; margin-bottom: 40px; }}
.header h1 {{ font-size: 2.5em; background: linear-gradient(90deg, #f7971e, #ffd200); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 10px; }}
.header .label {{ font-size: 1.4em; color: #ffd200; }}
.description {{ background: rgba(255,255,255,0.05); border-radius: 16px; padding: 24px; margin-bottom: 20px; line-height: 1.8; border: 1px solid rgba(255,255,255,0.1); }}
.card {{ background: rgba(255,255,255,0.05); border-radius: 16px; padding: 20px; margin-bottom: 16px; border: 1px solid rgba(255,255,255,0.08); }}
.card h2 {{ font-size: 1.1em; color: #ffd200; margin-bottom: 12px; display: flex; align-items: center; gap: 8px; }}
.row {{ display: flex; justify-content: space-between; padding: 6px 0; border-bottom: 1px solid rgba(255,255,255,0.05); }}
.row:last-child {{ border: none; }}
.row .key {{ color: #aaa; }}
.row .val {{ color: #fff; font-weight: 500; }}
.bar {{ background: rgba(255,255,255,0.1); border-radius: 8px; height: 8px; margin-top: 8px; overflow: hidden; }}
.bar-fill {{ height: 100%; border-radius: 8px; background: linear-gradient(90deg, #f7971e, #ffd200); transition: width 0.8s; }}
.tags {{ display: flex; gap: 8px; flex-wrap: wrap; }}
.tag {{ background: rgba(255,210,0,0.15); color: #ffd200; padding: 4px 12px; border-radius: 20px; font-size: 0.85em; }}
.footer {{ text-align: center; margin-top: 40px; color: #666; font-size: 0.85em; }}
</style>
</head>
<body>
<div class="container">
<div class="header">
<h1>🧬 风格指纹报告</h1>
<div class="label">{fp.get('overall_label', '')}</div>
</div>
<div class="description">{fp.get('vivid_description', '').replace(chr(10), '<br>')}</div>

<div class="card">
<h2>📏 句子长度</h2>
<div class="row"><span class="key">平均长度</span><span class="val">{sl.get('avg', '?')} 字</span></div>
<div class="row"><span class="key">中位数</span><span class="val">{sl.get('median', '?')} 字</span></div>
<div class="row"><span class="key">最短 / 最长</span><span class="val">{sl.get('min', '?')} / {sl.get('max', '?')} 字</span></div>
<div class="row"><span class="key">短句占比</span><span class="val">{sl.get('short_ratio', 0) * 100:.0f}%</span></div>
<div class="row"><span class="key">长句占比</span><span class="val">{sl.get('long_ratio', 0) * 100:.0f}%</span></div>
<div class="tags"><span class="tag">{sl.get('style', '')}</span></div>
</div>

<div class="card">
<h2>✏️ 标点习惯</h2>
<div class="tags">{''.join(f'<span class="tag">{h}</span>' for h in pct.get('habits', []))}</div>
<div class="row"><span class="key">逗号/句号比</span><span class="val">{pct.get('comma_period_ratio', '?')}</span></div>
<div class="row"><span class="key">感叹号/句号比</span><span class="val">{pct.get('exclaim_ratio', '?')}</span></div>
</div>

<div class="card">
<h2>😊 表情使用</h2>
<div class="row"><span class="key">总表情数</span><span class="val">{emoji.get('count', 0)}</span></div>
<div class="row"><span class="key">密度（/句）</span><span class="val">{emoji.get('density', 0)}</span></div>
<div class="row"><span class="key">最爱 Top5</span><span class="val">{emoji_top}</span></div>
<div class="tags"><span class="tag">{emoji.get('style', '')}</span></div>
</div>

<div class="card">
<h2>🎙️ 语气与表达</h2>
<div class="row"><span class="key">正式度</span><span class="val">{form.get('level', '')} ({form.get('ratio', 0) * 100:.0f}% 正式)</span></div>
<div class="row"><span class="key">表达风格</span><span class="val">{expr.get('style', '')}</span></div>
<div class="row"><span class="key">人称偏好</span><span class="val">{person.get('style', '')}</span></div>
<div class="row"><span class="key">情感基调</span><span class="val">{sentiment.get('tone', '')}</span></div>
</div>

<div class="card">
<h2>📐 排版习惯</h2>
<div class="tags">{''.join(f'<span class="tag">{k}: {v}</span>' for k, v in fmt.items())}</div>
<div class="row"><span class="key">段落风格</span><span class="val">{para.get('style', '')}（均 {para.get('avg_length', '?')} 字/段）</span></div>
<div class="row"><span class="key">节奏</span><span class="val">{rhythm.get('style', '')}</span></div>
</div>

<div class="card">
<h2>📚 词汇特征</h2>
<div class="row"><span class="key">词汇多样性</span><span class="val">{vocab.get('diversity', 0) * 100:.1f}%</span></div>
<div class="row"><span class="key">评价</span><span class="val">{vocab.get('label', '')}</span></div>
<div class="tags">{''.join(f'<span class="tag">{w[0]}</span>' for w in vocab.get('top_bigrams', [])[:8])}</div>
</div>

<div class="footer">🧬 0+1+2≠3 风格克隆引擎 · 你的数字分身</div>
</div>
</body>
</html>"""


if __name__ == "__main__":
    main()