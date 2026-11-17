#!/usr/bin/env python3
"""Audit Chinese prose for known AI-flavored writing patterns.

This is a regression aid, not an authorship detector or a prose-quality score.
"""

from __future__ import annotations

import argparse
import glob
import json
import re
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path


PROFILES = ("general", "social", "academic", "fiction", "sop", "email", "editorial")
TEXT_SUFFIXES = {".md", ".markdown", ".txt"}
SENTENCE_BODY = r"[^\n。！？!?]"
VERDICT_SEMANTICS = (
    "A clear verdict means no configured pattern requires review; "
    "it is not a prose-quality or authorship judgment."
)
PROFILE_SEVERITY_OVERRIDES = {
    "academic": {"essence_claim": 1},
    "fiction": {
        "fiction_cliche": 2,
        "hollow_question": 2,
        "slogan_ending": 1,
        "vivid_label": 0,
        "metaphor_stack": 0,
        "ellipsis_list": 0,
        "four_char_chain": 0,
    },
    "social": {"inflated_abstract_words": 2},
    "sop": {"staged_sequence": 0, "rigid_enumeration": 0},
    "email": {"ending_engagement_question": 1, "staged_sequence": 1},
    "editorial": {
        "rigid_enumeration": 0,
        "template_colon": 0,
        "slogan_ending": 1,
        "vivid_label": 1,
        "metaphor_stack": 1,
        "ellipsis_list": 0,
        "four_char_chain": 0,
    },
}
_HOLLOW_PREFIXES = ("这是一个值得", "这值得我们", "值得我们深思", "这个问题值得")
_SLOGAN_ENDING = re.compile(
    r"(?:必将|定能|定会|定将)[^\n。！？!?]{0,20}?(?:更加|美好|辉煌|澎湃|磅礴|光明)"
)
_SENTENCE_FINAL = frozenset("。！？!?")
_CHAIN_EDGE = frozenset("、，。；")
_FOUR_CHAR_CHAIN = re.compile(r"(?:[\u4e00-\u9fff]{4}、){3,}[\u4e00-\u9fff]{4}")
_METAPHOR_WORDS = ("加速器", "催化剂", "试金石", "压舱石", "稳定器", "蓄水池", "助推器", "新引擎")


@dataclass(frozen=True)
class Rule:
    rule_id: str
    label: str
    severity: int
    pattern: re.Pattern[str] | None = None
    terms: tuple[str, ...] = ()


RULES = (
    Rule(
        "binary_contrast",
        "二分对照壳",
        0,
        re.compile(
            rf"(?:(?<![要是])不是|并非|不在于|不只是|不止是|不仅是|并没有|不在(?!于))"
            rf"{SENTENCE_BODY}{{0,32}}?(?:而是|而在于|更是|而在(?!于))"
            rf"|与其说{SENTENCE_BODY}{{0,32}}?不如说"
        ),
    ),
    Rule(
        "staged_sequence",
        "机械先后顺序",
        2,
        re.compile(
            rf"(?<![首优事原率争预祖抢])先(?![生进锋前后例导驱])"
            rf"{SENTENCE_BODY}{{0,24}}(?:再|然后|后面|随后)|"
            rf"第一步{SENTENCE_BODY}{{0,60}}第二步"
        ),
    ),
    Rule(
        "essence_claim",
        "真正/本质/核心式拔高",
        3,
        re.compile(rf"真正{SENTENCE_BODY}{{0,24}}(?:的是|在于|决定|重要|打动|改变)|本质上|核心在于|底层逻辑"),
    ),
    Rule(
        "assistant_route_marker",
        "助手路标词",
        3,
        terms=("下面我们来", "接下来我会", "我们可以看到", "希望这能帮到你", "作为AI", "截至我的知识"),
    ),
    Rule("narrowing_frame", "过度收束开场", 2, terms=("这次只看", "今天只看", "这里只看", "我们只看")),
    Rule("easy_answer_colon", "很简单冒号模板", 2, re.compile(r"[^。！？!?\n]{1,18}很简单[：:]")),
    Rule(
        "lecture_marker",
        "讲义腔/总结腔",
        2,
        terms=(
            "总的来说",
            "值得注意的是",
            "不可否认的是",
            "不难看出",
            "由此可见",
            "在这个过程中",
            "这背后其实",
            "说白了",
            "划重点",
            "捋一捋",
            "盘一盘",
            "拆一拆",
            "聊一聊",
        ),
    ),
    Rule(
        "inflated_abstract_words",
        "抽象包装词堆叠",
        1,
        terms=("赋能", "助力", "抓手", "闭环", "深耕", "沉淀", "价值感", "长期主义", "意义深远", "前景广阔"),
    ),
    Rule(
        "academic_filler",
        "学术/技术填充套话",
        2,
        re.compile(
            r"(?:基于|依据)[^。！？!?\n]{0,18}(?:理论|框架)|"
            r"(?:研究表明|专家认为|业内普遍认为)|"
            r"(?:综上所述|此案例(?:印证|揭示|说明)了|具有重要(?:理论|现实)?意义|提供了新思路|开辟了新方向)"
        ),
    ),
    Rule(
        "rigid_enumeration",
        "整齐编号逻辑",
        2,
        re.compile(
            rf"首先{SENTENCE_BODY}{{0,80}}其次|其次{SENTENCE_BODY}{{0,80}}(?:再次|最后)|"
            rf"一方面{SENTENCE_BODY}{{0,80}}另一方面"
        ),
    ),
    Rule(
        "fiction_cliche",
        "小说正文套话",
        1,
        terms=(
            "不禁",
            "情不自禁",
            "不由自主",
            "映入眼帘",
            "心中暗道",
            "暗自思忖",
            "嘴角微扬",
            "勾起一抹弧度",
            "脸色一变",
            "身形一顿",
            "缓缓说道",
            "淡淡地说",
        ),
    ),
    Rule(
        "vivid_label",
        "评价性标签",
        1,
        re.compile(r"生动(?:写照|诠释|缩影|注脚|实践|样本|篇章)"),
    ),
    Rule(
        "ellipsis_list",
        "省略号收束列举",
        1,
        re.compile(r"[；，][^；，\n。！？!?]{4,60}……"),
    ),
)
_METAPHOR_STACK = Rule("metaphor_stack", "引号隐喻堆叠", 2)
_FOUR_CHAR_RULE = Rule("four_char_chain", "四字顿号链", 1)
_HOLLOW_QUESTION = Rule("hollow_question", "空转设问", 3)
_SLOGAN_RULE = Rule("slogan_ending", "口号式结尾", 2)


def line_number(text: str, index: int) -> int:
    return text.count("\n", 0, index) + 1


def excerpt(text: str, start: int, end: int) -> str:
    left = max(0, start - 24)
    right = min(len(text), end + 24)
    return text[left:right].replace("\n", "\\n")


# A quote or title may contain a single line break, but not a blank line.
_WITHIN_PARAGRAPH = r"(?:(?!\n[ \t]*\n).)*?"
_PAIRED_QUOTES = re.compile(
    rf"“{_WITHIN_PARAGRAPH}”|‘{_WITHIN_PARAGRAPH}’|「{_WITHIN_PARAGRAPH}」|『{_WITHIN_PARAGRAPH}』|\"[^\"\n]*\"",
    re.DOTALL,
)
_BOOK_TITLE = re.compile(rf"《{_WITHIN_PARAGRAPH}》", re.DOTALL)
_CITATION_MARKER = re.compile(r"（[^（）\n]*\d{4}|\([^()\n]*\d{4}|\[\d+\]")
_ENGAGEMENT_QUESTION = re.compile(r"你|大家|有没有|是不是|觉得|卡在|哪一步")
_TRANSACTIONAL_CLOSING = re.compile(
    r"确认|能否|方便|截止|请问"
    r"|(?:周|星期)[一二三四五六日天]"
    r"|上午|下午|中午|晚上|凌晨|早上"
    r"|\d{1,2}\s*[:：]\s*\d{2}"
    r"|\d{1,4}年|\d{1,2}月|\d{1,2}日"
    r"|(?:[0-9]{1,2}|[两二三四五六七八九十]|十[一二]?)点(?:半|钟|\d{1,2}分?|前|后|整|左右)?"
    r"|一点(?:半|钟|\d{1,2}分?|前|后|整|左右)"
)
_TERM_PATTERNS = {
    "不禁": re.compile(r"不禁(?!止)"),
    "助力": re.compile(r"助力(?!车)"),
}


def protected_spans(text: str) -> list[tuple[int, int]]:
    spans = [(match.start(), match.end()) for match in re.finditer(r"```.*?```", text, re.DOTALL)]
    spans.extend((match.start(), match.end()) for match in re.finditer(r"`[^`\n]+`", text))
    spans.extend(match.span() for match in _BOOK_TITLE.finditer(text))
    return sorted(spans)


def _is_latin_letter(char: str) -> bool:
    return len(char) == 1 and char.isascii() and char.isalpha()


def _paragraph_ranges(text: str) -> list[tuple[int, int]]:
    ranges: list[tuple[int, int]] = []
    start = 0
    for match in re.finditer(r"\n[ \t]*\n", text):
        ranges.append((start, match.start()))
        start = match.end()
    ranges.append((start, len(text)))
    return ranges


def _ascii_single_quote_spans(text: str) -> list[tuple[int, int]]:
    """Pair ASCII single quotes only when neither side is a Latin letter.

    Apostrophes in words like It's and Don't are not quotation marks. Pairs
    also stay inside one paragraph, so an opener cannot exempt later text.
    """
    spans: list[tuple[int, int]] = []
    for para_start, para_end in _paragraph_ranges(text):
        marks: list[int] = []
        for index in range(para_start, para_end):
            if text[index] != "'":
                continue
            before = text[index - 1] if index > 0 else ""
            after = text[index + 1] if index + 1 < len(text) else ""
            if _is_latin_letter(before) or _is_latin_letter(after):
                continue
            marks.append(index)
        spans.extend((left, right + 1) for left, right in zip(marks[0::2], marks[1::2]))
    return spans


def quoted_spans(text: str) -> list[tuple[int, int]]:
    spans = [match.span() for match in _PAIRED_QUOTES.finditer(text)]
    spans.extend(_ascii_single_quote_spans(text))
    return spans


def contained_in(start: int, end: int, spans: list[tuple[int, int]]) -> bool:
    return any(span_start <= start and end <= span_end for span_start, span_end in spans)


def iter_term_matches(text: str, term: str):
    pattern = _TERM_PATTERNS.get(term)
    if pattern is not None:
        for match in pattern.finditer(text):
            yield match.start(), match.end(), term
        return
    start = 0
    while True:
        index = text.find(term, start)
        if index < 0:
            return
        yield index, index + len(term), term
        start = index + len(term)


def cited_research_claim(text: str, end: int, match_text: str) -> bool:
    """Skip 研究表明 when a citation marker begins within the next 30 characters."""
    if match_text != "研究表明":
        return False
    region = text[end : end + 80]
    marker = _CITATION_MARKER.search(region)
    return marker is not None and marker.start() < 30


def is_exempt(
    start: int,
    end: int,
    protected: list[tuple[int, int]],
    quoted: list[tuple[int, int]],
) -> bool:
    if contained_in(start, end, protected):
        return True
    if contained_in(start, end, quoted):
        return True
    return False


def severity_for(rule_id: str, default: int, profile: str) -> int:
    return PROFILE_SEVERITY_OVERRIDES.get(profile, {}).get(rule_id, default)


def effective_severity(rule: Rule, profile: str) -> int:
    return severity_for(rule.rule_id, rule.severity, profile)


def normalize_keep_terms(keep_terms: tuple[str, ...] | list[str] | None) -> tuple[str, ...]:
    """Exact formulations, one string each. Blank entries are ignored."""
    terms: list[str] = []
    seen: set[str] = set()
    for raw in keep_terms or ():
        term = raw.strip()
        if term and term not in seen:
            terms.append(term)
            seen.add(term)
    return tuple(terms)


def keep_term_spans(text: str, terms: tuple[str, ...]) -> list[tuple[int, int]]:
    spans: list[tuple[int, int]] = []
    for term in terms:
        start = 0
        while True:
            index = text.find(term, start)
            if index < 0:
                break
            spans.append((index, index + len(term)))
            start = index + len(term)
    return spans


def _sentence_spans(text: str) -> list[tuple[int, int]]:
    spans: list[tuple[int, int]] = []
    start = 0
    for match in re.finditer(r"[。！？!?]", text):
        spans.append((start, match.end()))
        start = match.end()
    if start < len(text):
        spans.append((start, len(text)))
    return spans


def find_metaphor_stacks(
    text: str,
    profile: str,
    protected: list[tuple[int, int]],
    quoted: list[tuple[int, int]],
) -> list[dict]:
    """One finding per sentence that quotes at least two functional metaphors.

    The quotation marks are the signal, so a quoted word is not exempt. A word
    inside a code span, a book title, or a --keep-terms span still is.
    """
    severity = severity_for(_METAPHOR_STACK.rule_id, _METAPHOR_STACK.severity, profile)
    findings: list[dict] = []
    for sentence_start, sentence_end in _sentence_spans(text):
        hits: list[tuple[int, int, str]] = []
        for word in _METAPHOR_WORDS:
            search_from = sentence_start
            while True:
                index = text.find(word, search_from, sentence_end)
                if index < 0:
                    break
                word_end = index + len(word)
                quoted_word = contained_in(index, word_end, quoted)
                protected_word = contained_in(index, word_end, protected)
                if quoted_word and not protected_word:
                    hits.append((index, word_end, word))
                search_from = word_end
        if len(hits) < 2:
            continue
        hits.sort()
        match_text = "、".join(word for _, _, word in hits)
        findings.append(
            finding(_METAPHOR_STACK, severity, text, hits[0][0], hits[-1][1], match_text)
        )
    return findings


def _is_han(char: str) -> bool:
    return "\u4e00" <= char <= "\u9fff"


def _trailing_word_extra(text: str, index: int) -> int:
    """1 or 2 when a 4-character item is the head of a 5- or 6-character word."""
    limit = len(text)
    for extra in (1, 2):
        stop = index + extra
        if stop > limit or not all(_is_han(text[i]) for i in range(index, stop)):
            continue
        if stop == limit or text[stop] in _CHAIN_EDGE:
            return extra
    return 0


def find_four_char_chains(text: str, profile: str, masked: list[tuple[int, int]]) -> list[dict]:
    """Four or more four-character words joined by enumeration commas.

    Keep-term, quote, title, and code spans are masked first, so a listed
    formulation breaks a chain instead of hiding the words around it.
    A one-character lead-in is kept. If the last item is only the first four
    characters of a 5- or 6-character word, that item is dropped and the chain
    is kept when at least four items remain.
    """
    visible = mask_spans(text, masked)
    severity = severity_for(_FOUR_CHAR_RULE.rule_id, _FOUR_CHAR_RULE.severity, profile)
    findings: list[dict] = []
    cursor = 0
    while True:
        match = _FOUR_CHAR_CHAIN.search(visible, cursor)
        if match is None:
            break
        end = match.end()
        items = match.group(0).split("、")
        if _trailing_word_extra(visible, end):
            items = items[:-1]
            if len(items) < 4:
                cursor = match.start() + 1
                continue
            end = match.start() + len("、".join(items))
        findings.append(
            finding(
                _FOUR_CHAR_RULE,
                severity,
                text,
                match.start(),
                end,
                text[match.start() : end],
            )
        )
        cursor = match.end()
    return findings


def finding(rule: Rule, severity: int, text: str, start: int, end: int, match_text: str) -> dict:
    return {
        "rule": rule.rule_id,
        "label": rule.label,
        "severity": severity,
        "line": line_number(text, start),
        "match": match_text,
        "excerpt": excerpt(text, start, end),
    }


def audit_text(
    text: str,
    profile: str = "general",
    keep_terms: tuple[str, ...] | list[str] | None = None,
) -> dict:
    if profile not in PROFILES:
        raise ValueError(f"unsupported profile: {profile}")

    findings: list[dict] = []
    terms = normalize_keep_terms(keep_terms)
    protected = protected_spans(text)
    protected.extend(keep_term_spans(text, terms))
    protected.sort()
    quoted = quoted_spans(text)

    for rule in RULES:
        severity = effective_severity(rule, profile)
        matches: list[tuple[int, int, str]] = []
        if rule.pattern:
            matches.extend((match.start(), match.end(), match.group(0)) for match in rule.pattern.finditer(text))
        for term in rule.terms:
            matches.extend(iter_term_matches(text, term))

        for start, end, match_text in matches:
            if rule.rule_id == "academic_filler" and cited_research_claim(text, end, match_text):
                continue
            if not is_exempt(start, end, protected, quoted):
                findings.append(finding(rule, severity, text, start, end, match_text))

    masked = sorted(protected + quoted)
    findings.extend(find_metaphor_stacks(text, profile, protected, quoted))
    findings.extend(find_four_char_chains(text, profile, masked))
    findings.extend(audit_shape(text, masked, profile))
    findings.sort(key=lambda item: (item["line"], -item["severity"], item["rule"], item["match"]))
    score = sum(item["severity"] for item in findings)
    blockers = [item for item in findings if item["severity"] >= 3]
    repeated_rules = Counter(item["rule"] for item in findings if item["severity"] >= 2)
    clustered = any(count >= 2 for count in repeated_rules.values())
    return {
        "profile": profile,
        "score": score,
        "finding_count": len(findings),
        "blocker_count": len(blockers),
        "verdict": "review" if score >= 4 or len(blockers) >= 2 or clustered else "clear",
        "findings": findings,
    }


def mask_spans(text: str, spans: list[tuple[int, int]]) -> str:
    characters = list(text)
    for start, end in spans:
        for index in range(start, end):
            if characters[index] != "\n":
                characters[index] = " "
    return "".join(characters)


def audit_shape(text: str, protected: list[tuple[int, int]], profile: str = "general") -> list[dict]:
    findings: list[dict] = []
    visible_text = mask_spans(text, protected)
    nonempty_lines = [(number, line.strip()) for number, line in enumerate(visible_text.splitlines(), start=1) if line.strip()]

    template_prefix = re.compile(
        r"^(?:概念|问题|原因|结论|答案|核心|本质|关键|目标|方法|步骤|第一步|第二步|第三步|SOP|"
        r"Hook|Usefulness|Specificity|Trust|Privacy|Tags|正文质量评分)[：:]"
    )
    colon_lines = [(number, line) for number, line in nonempty_lines if template_prefix.match(line)]
    if len(colon_lines) >= 3:
        findings.append(
            {
                "rule": "template_colon",
                "label": "冒号模板重复",
                "severity": severity_for("template_colon", 2, profile),
                "line": colon_lines[0][0],
                "match": f"{len(colon_lines)} colon-template lines",
                "excerpt": " / ".join(line for _, line in colon_lines[:3]),
            }
        )

    sentences = [
        sentence.strip()
        for sentence in re.split(r"[。！？!?]\s*", visible_text)
        if sentence.strip() and not sentence.strip().startswith("#")
    ]
    hen_judgments = [
        sentence for sentence in sentences if re.match(r"^[^，,；;：:\n]{1,18}很[^，,；;：:\n]{1,12}$", sentence)
    ]
    if len(hen_judgments) >= 3:
        first_hen = hen_judgments[0]
        hen_start = visible_text.find(first_hen)
        findings.append(
            {
                "rule": "dense_hen_judgments",
                "label": "很字判断句过密",
                "severity": 2,
                "line": line_number(visible_text, hen_start),
                "match": f"{len(hen_judgments)} 'X很X' sentences",
                "excerpt": " / ".join(hen_judgments[:3]),
            }
        )

    parallel_commas = re.findall(r"(?:[^，。！？\n]{2,18}很[^，。！？\n]{1,12}[，。]){3,}", visible_text)
    if parallel_commas:
        first = parallel_commas[0]
        start = visible_text.find(first)
        findings.append(
            {
                "rule": "parallel_hen_clauses",
                "label": "很字排比过密",
                "severity": 2,
                "line": line_number(visible_text, start),
                "match": "parallel '很' clauses",
                "excerpt": excerpt(visible_text, start, start + len(first)),
            }
        )

    paragraph_info: list[tuple[int, str]] = []
    offset = 0
    paragraphs = visible_text.split("\n\n")
    for index, paragraph in enumerate(paragraphs):
        paragraph_info.append((offset, paragraph))
        offset += len(paragraph)
        if index != len(paragraphs) - 1:
            offset += 2
    measured = []
    for start, paragraph in paragraph_info:
        if paragraph.strip() and not paragraph.strip().startswith("#"):
            length = len(re.sub(r"\s+", "", paragraph))
            content_start = start + (len(paragraph) - len(paragraph.lstrip("\n")))
            measured.append((content_start, length))
    medium = [(start, length) for start, length in measured if 24 <= length <= 90]
    medium_lengths = [length for _, length in medium]
    if len(medium_lengths) >= 5 and max(medium_lengths) - min(medium_lengths) <= 12:
        findings.append(
            {
                "rule": "over_even_paragraph_distribution",
                "label": "段落长度过于均匀",
                "severity": 1,
                "line": line_number(visible_text, medium[0][0]),
                "match": f"paragraph lengths={medium_lengths[:8]}",
                "excerpt": "Review whether repeated paragraph weight serves the text.",
            }
        )

    final_line_number, final_line = next(
        ((number, line) for number, line in reversed(nonempty_lines) if not line.startswith("#")),
        (1, ""),
    )
    if (
        final_line.endswith(("？", "?"))
        and _ENGAGEMENT_QUESTION.search(final_line)
        and not _TRANSACTIONAL_CLOSING.search(final_line)
    ):
        findings.append(
            {
                "rule": "ending_engagement_question",
                "label": "结尾假互动提问",
                "severity": severity_for("ending_engagement_question", 3, profile),
                "line": final_line_number,
                "match": final_line,
                "excerpt": final_line,
            }
        )

    findings.extend(find_hollow_questions(text, visible_text, profile))
    findings.extend(find_slogan_ending(text, visible_text, profile))

    second_person = list(re.finditer(r"你|大家", visible_text))
    if len(second_person) >= 6:
        findings.append(
            {
                "rule": "second_person_overuse",
                "label": "二人称过密",
                "severity": 1,
                "line": line_number(visible_text, second_person[0].start()),
                "match": f"{len(second_person)} second-person markers",
                "excerpt": "Review whether each reader address is necessary.",
            }
        )

    return findings


def find_hollow_questions(text: str, visible_text: str, profile: str) -> list[dict]:
    """The sentence after a question mark opens with an empty-pondering prefix."""
    severity = severity_for(_HOLLOW_QUESTION.rule_id, _HOLLOW_QUESTION.severity, profile)
    findings: list[dict] = []
    for match in re.finditer(r"[？?]", visible_text):
        rest = visible_text[match.end() :]
        stripped = rest.lstrip(" \t\r\n")
        prefix = next((item for item in _HOLLOW_PREFIXES if stripped.startswith(item)), None)
        if prefix is None:
            continue
        prefix_at = match.end() + (len(rest) - len(stripped))
        end = prefix_at + len(prefix)
        while end < len(text) and text[end] not in "。！？!?\n":
            end += 1
        if end < len(text) and text[end] in "。！？!?":
            end += 1
        findings.append(
            finding(_HOLLOW_QUESTION, severity, text, prefix_at, end, text[prefix_at:end].strip())
        )
    return findings


def _blank_separated_blocks(text: str) -> list[tuple[int, str]]:
    blocks: list[tuple[int, str]] = []
    start = 0
    for match in re.finditer(r"\n[ \t]*\n", text):
        blocks.append((start, text[start : match.start()]))
        start = match.end()
    blocks.append((start, text[start:]))
    return blocks


def _line_entries(block_start: int, block: str) -> list[tuple[int, str]]:
    entries: list[tuple[int, str]] = []
    offset = block_start
    lines = block.split("\n")
    for index, line in enumerate(lines):
        stripped = line.strip()
        if stripped:
            entries.append((offset + (len(line) - len(line.lstrip())), stripped))
        offset += len(line)
        if index != len(lines) - 1:
            offset += 1
    return entries


def _paragraph_to_check(visible_text: str) -> tuple[int, str] | None:
    """Last paragraph, including single-newline paragraphs that each end a sentence.

    Blank lines always separate blocks. Inside the last block, lines that each
    end with sentence-final punctuation are paragraphs of their own; only the
    last non-empty, non-heading line is checked.
    """
    for block_start, block in reversed(_blank_separated_blocks(visible_text)):
        entries = _line_entries(block_start, block)
        if not entries:
            continue
        if len(entries) >= 2 and all(line[-1] in _SENTENCE_FINAL for _, line in entries):
            content = [(pos, line) for pos, line in entries if not line.startswith("#")]
            if content:
                return content[-1]
            continue
        stripped = block.strip()
        if not stripped or stripped.startswith("#"):
            continue
        return block_start + (len(block) - len(block.lstrip())), block.lstrip()
    return None


def find_slogan_ending(text: str, visible_text: str, profile: str) -> list[dict]:
    """One finding when the last paragraph is a slogan, however many clauses match."""
    checked = _paragraph_to_check(visible_text)
    if checked is None:
        return []
    content_start, paragraph = checked
    slogan = _SLOGAN_ENDING.search(paragraph)
    if slogan is None and not paragraph.startswith("让我们"):
        return []
    if slogan is not None:
        match_text = slogan.group(0)
        start = content_start + slogan.start()
    else:
        match_text = "让我们"
        start = content_start
    severity = severity_for(_SLOGAN_RULE.rule_id, _SLOGAN_RULE.severity, profile)
    return [finding(_SLOGAN_RULE, severity, text, start, start + len(match_text), match_text)]


def load_keep_terms(path: str) -> tuple[str, ...]:
    file = Path(path)
    if not file.is_file():
        raise ValueError(f"not found: {path}")
    terms: list[str] = []
    for raw in file.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        terms.append(line)
    return tuple(terms)


def expand_input_paths(raw_paths: list[str], recursive: bool = False) -> list[Path]:
    expanded: list[Path] = []
    for raw_path in raw_paths:
        if glob.has_magic(raw_path):
            matches = [Path(match) for match in sorted(glob.glob(raw_path, recursive=True))]
            if not matches:
                raise ValueError(f"not found: {raw_path}")
            expanded.extend(path for path in matches if path.is_file())
            continue

        path = Path(raw_path)
        if path.is_dir():
            children = path.rglob("*") if recursive else path.iterdir()
            expanded.extend(
                child for child in sorted(children) if child.is_file() and child.suffix.lower() in TEXT_SUFFIXES
            )
        elif path.is_file():
            expanded.append(path)
        else:
            raise ValueError(f"not found: {raw_path}")

    unique: list[Path] = []
    seen: set[str] = set()
    for path in expanded:
        key = str(path.resolve())
        if key not in seen:
            unique.append(path)
            seen.add(key)
    if not unique:
        raise ValueError("no readable text files found")
    return unique


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Audit Chinese prose for known AI-flavored patterns.",
        epilog=VERDICT_SEMANTICS,
    )
    parser.add_argument("paths", nargs="*", help="Text files, directories, or glob patterns")
    parser.add_argument("--stdin", action="store_true", help="Read one document from standard input")
    parser.add_argument("--profile", choices=PROFILES, default="general")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON")
    parser.add_argument("--fail-on-review", action="store_true", help="Exit 1 if any document needs review")
    parser.add_argument(
        "--recursive",
        action="store_true",
        help="When scanning a directory, include text files in subdirectories",
    )
    parser.add_argument(
        "--keep-terms",
        metavar="FILE",
        help="Exempt exact formulations listed in FILE, one per line. Blank lines and # comments are ignored",
    )
    args = parser.parse_args()

    if args.stdin and args.paths:
        parser.error("--stdin cannot be combined with paths")
    if not args.stdin and not args.paths:
        parser.error("provide at least one path or use --stdin")

    try:
        keep_terms = load_keep_terms(args.keep_terms) if args.keep_terms else ()
        if args.stdin:
            documents = [("<stdin>", sys.stdin.read())]
        else:
            documents = [
                (str(path), path.read_text(encoding="utf-8"))
                for path in expand_input_paths(args.paths, recursive=args.recursive)
            ]
    except (OSError, UnicodeError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2

    results = {
        name: audit_text(text, profile=args.profile, keep_terms=keep_terms) for name, text in documents
    }
    failed = any(result["verdict"] == "review" for result in results.values())

    if args.json:
        print(
            json.dumps(
                {
                    "schema_version": 1,
                    "profile": args.profile,
                    "verdict_semantics": VERDICT_SEMANTICS,
                    "results": results,
                },
                ensure_ascii=False,
                indent=2,
            )
        )
    else:
        for path, result in results.items():
            print(
                f"{path}: {result['verdict']} score={result['score']} "
                f"findings={result['finding_count']} blockers={result['blocker_count']} profile={result['profile']}"
            )
            for item in result["findings"][:12]:
                print(f"  L{item['line']} [{item['label']}] {item['match']}")
            if len(result["findings"]) > 12:
                print(f"  ... {len(result['findings']) - 12} more")
        print(f"Note: {VERDICT_SEMANTICS}")

    return 1 if args.fail_on_review and failed else 0


if __name__ == "__main__":
    sys.exit(main())
