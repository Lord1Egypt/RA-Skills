"""Fidelity checks for before/after fixture pairs.

Each pair is `tests/fixtures/<stem>_before.md`, `<stem>_after.md`, and
`<stem>_keep.txt`. Keep lines are non-negotiable source spans: each one must
be a substring of both the before and the after. A line `# drop: <quoted
inner text>` declares a quotation the revision may remove. A line
`# allow-rule: <rule_id>` names an audit rule the score check may ignore.
Current fixtures leave this list empty: `binary_contrast` is severity 0 and
does not change the verdict. Other `#` lines are comments.

The person-name screen is warning-level. It is a coarse surname regex, not
named-entity recognition, so ordinary words that merely start with a surname
(高价值, 段落都, 连续出) are excluded rather than treated as people.
"""

from __future__ import annotations

import importlib.util
import re
import sys
import unittest
import warnings
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = SKILL_ROOT / "scripts" / "audit_ai_flavor.py"
FIXTURES = Path(__file__).resolve().parent / "fixtures"
# Register used in addition to general. Fixtures without a dedicated profile stay on general.
REGISTER_PROFILES = {
    "academic_technical": "academic",
    "editorial_commentary": "editorial",
    "email_comment": "email",
    "novel_opening": "fiction",
    "xhs_ai_flavor": "social",
}

QUOTE_RE = re.compile(
    r"“(.*?)”|‘(.*?)’|「(.*?)」|『(.*?)』|\"([^\"\n]*)\"|'([^'\n]*)'",
    re.DOTALL,
)
DIGIT_RE = re.compile(r"\d+(?:\.\d+)?")
# Chinese numeral plus a measure word, so revisions cannot add counts such as
# 三件事 or 三类材料.
MEASURE_RE = re.compile(r"[一二两三四五六七八九十百千万]+(?:个|件|类|条|步|种|次|天|位|人|项)")
_CLOCK = r"\d{1,2}[:：]\d{2}(?:[:：]\d{2})?"
_NUMERAL = r"[零〇一二三四五六七八九十两\d]{1,3}"
_TIME_OF_DAY = r"凌晨|清晨|早上|上午|中午|下午|傍晚|晚上|深夜|夜里"
# Bare "X点" matches only with 分/钟 after it, or with a time-of-day word
# before it. 少一点 and 两点意见 are not times.
TIME_RE = re.compile(
    rf"{_CLOCK}"
    rf"|(?:{_TIME_OF_DAY})(?:{_NUMERAL}点(?:{_NUMERAL}分|钟)?)?"
    rf"|{_NUMERAL}点(?:{_NUMERAL}分|钟)"
)

# Common single-character surnames, plus frequent compound surnames.
# Rare 百家姓 entries that are ordinary words (后, 从, 党, …) are omitted
# so the screen stays a name check rather than a word check.
COMPOUND_SURNAMES = (
    "欧阳",
    "太史",
    "端木",
    "上官",
    "司马",
    "东方",
    "独孤",
    "南宫",
    "万俟",
    "闻人",
    "夏侯",
    "诸葛",
    "尉迟",
    "公羊",
    "赫连",
    "澹台",
    "皇甫",
    "宗政",
    "濮阳",
    "公冶",
    "太叔",
    "申屠",
    "公孙",
    "慕容",
    "仲孙",
    "钟离",
    "长孙",
    "宇文",
    "司徒",
    "鲜于",
    "司空",
    "闾丘",
    "子车",
    "亓官",
    "司寇",
    "巫马",
    "公西",
    "颛孙",
    "壤驷",
    "公良",
    "漆雕",
    "乐正",
    "宰父",
    "谷梁",
    "拓跋",
    "夹谷",
    "轩辕",
    "令狐",
    "段干",
    "百里",
    "呼延",
    "东郭",
    "南门",
    "羊舌",
    "微生",
    "左丘",
    "西门",
    "公祖",
    "第五",
    "公乘",
    "贯丘",
    "公皙",
    "南荣",
    "东里",
    "东宫",
    "仲长",
    "子书",
    "子桑",
    "即墨",
    "达奚",
    "褚师",
)
SINGLE_SURNAMES = frozenset(
    "赵钱孙李周吴郑王冯陈褚卫蒋沈韩杨朱秦尤许何吕施张孔曹严华金魏陶姜"
    "戚谢邹喻柏水窦章云苏潘葛奚范彭郎鲁韦昌马苗凤花方俞任袁柳鲍史唐"
    "费廉岑薛雷贺倪汤滕殷罗毕郝邬安常乐于时傅皮卞齐康伍余元卜顾孟平黄"
    "和穆萧尹姚邵汪祁毛禹狄米贝明臧计伏成戴谈宋茅庞熊纪舒屈项祝董梁杜"
    "阮蓝闵席季麻强贾路娄危江童颜郭梅盛林刁钟徐邱骆高夏蔡田樊胡凌霍虞"
    "万支柯管卢莫经房裘缪干解应宗丁宣邓郁单杭洪包诸左石崔吉钮龚程嵇邢"
    "裴陆荣翁荀羊惠甄曲家封芮羿储靳汲邴糜松井段富巫乌焦巴弓牧隗山谷车"
    "侯宓蓬全郗班仰秋仲伊宫宁仇栾暴甘厉戎祖武符刘景詹束龙叶幸司韶郜黎"
    "蓟薄印宿白怀蒲邰鄂索咸籍赖卓蔺屠蒙池乔阴胥能苍双闻莘翟谭贡劳"
    "逄姬申扶堵冉宰郦雍桑桂濮牛寿通边扈燕冀浦尚农温别庄晏柴瞿阎充慕连"
    "茹习宦艾鱼容向古易慎戈廖庾终暨居衡步都耿满弘匡国文寇广禄阙东殳沃"
    "利蔚越夔隆师巩聂晁勾敖融冷訾辛阚那简饶空曾沙养鞠须丰巢关蒯相查"
    "荆红游竺权逯盖益"
)
# Stop a given name before function characters or numerals, so 凌晨三点
# is not read as a three-character name.
GIVEN_NAME_STOP = frozenset(
    "的了是在不也和与或而及把被让从对到向给跟同并就还又再很最更这那"
    "你我他她它其个中上下里为以所会能可要着过呢吗吧啊呀嘛们后前"
    "零〇一二三四五六七八九十两"
)
# Ordinary phrases the surname screen would otherwise call names.
NOT_PERSON_NAMES = frozenset({"高价值", "段落都", "连续出", "支持"})


def load_audit_module():
    spec = importlib.util.spec_from_file_location("tone_audit_fidelity", SCRIPT_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("Unable to load audit module")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def parse_keep_text(text: str) -> tuple[list[str], list[str], list[str]]:
    keeps: list[str] = []
    drops: list[str] = []
    allow_rules: list[str] = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith("# drop:"):
            value = _strip_wrapping_quotes(line[len("# drop:") :].strip())
            if value:
                drops.append(value)
            continue
        if line.startswith("# allow-rule:"):
            rule = line[len("# allow-rule:") :].strip()
            if rule:
                allow_rules.append(rule)
            continue
        if line.startswith("#"):
            continue
        keeps.append(line)
    return keeps, drops, allow_rules


def _strip_wrapping_quotes(value: str) -> str:
    pairs = (("“", "”"), ("‘", "’"), ("「", "」"), ("『", "』"), ('"', '"'), ("'", "'"))
    for left, right in pairs:
        if len(value) >= 2 and value.startswith(left) and value.endswith(right):
            return value[len(left) : -len(right)]
    return value


def quoted_inners(text: str) -> list[str]:
    inners: list[str] = []
    for match in QUOTE_RE.finditer(text):
        inner = next(group for group in match.groups() if group is not None)
        if inner:
            inners.append(inner)
    return inners


def strings_absent_from(needles: list[str], haystack: str) -> list[str]:
    return [needle for needle in needles if needle not in haystack]


def _is_cjk(char: str) -> bool:
    return "\u4e00" <= char <= "\u9fff"


def person_name_candidates(text: str) -> set[str]:
    """2–4 character name candidates: surname plus one or two given-name chars.

    A candidate must sit at a non-Chinese boundary (start, punctuation, or
    Latin). This is a coarse screen, not named-entity recognition.
    """
    found: set[str] = set()
    for index, char in enumerate(text):
        if not _is_cjk(char):
            continue
        if index and _is_cjk(text[index - 1]):
            continue
        surname = next((item for item in COMPOUND_SURNAMES if text.startswith(item, index)), None)
        surname_len = len(surname) if surname else 0
        if surname is None and char in SINGLE_SURNAMES:
            surname, surname_len = char, 1
        if surname is None:
            continue
        given = ""
        cursor = index + surname_len
        while (
            cursor < len(text)
            and len(given) < 2
            and _is_cjk(text[cursor])
            and text[cursor] not in GIVEN_NAME_STOP
        ):
            given += text[cursor]
            cursor += 1
        if not given or not (2 <= surname_len + len(given) <= 4):
            continue
        candidate = surname + given
        if candidate in NOT_PERSON_NAMES:
            continue
        found.add(candidate)
    return found


def new_person_names(before: str, after: str) -> set[str]:
    return {name for name in person_name_candidates(after) if name not in before}


def warn_on_new_names(stem: str, before: str, after: str) -> None:
    fresh = sorted(new_person_names(before, after))
    if fresh:
        warnings.warn(
            f"{stem}: new 2–4 character name candidates {fresh}",
            UserWarning,
            stacklevel=2,
        )


def load_pairs() -> list[tuple[str, str, str, list[str], list[str], list[str]]]:
    pairs: list[tuple[str, str, str, list[str], list[str], list[str]]] = []
    before_paths = sorted(FIXTURES.glob("*_before.md"))
    if not before_paths:
        raise AssertionError(f"no before fixtures in {FIXTURES}")
    for before_path in before_paths:
        stem = before_path.name[: -len("_before.md")]
        after_path = FIXTURES / f"{stem}_after.md"
        keep_path = FIXTURES / f"{stem}_keep.txt"
        if not after_path.is_file():
            raise AssertionError(f"missing after fixture for {stem}")
        if not keep_path.is_file():
            raise AssertionError(f"missing keep file for {stem}")
        keeps, drops, allow_rules = parse_keep_text(keep_path.read_text(encoding="utf-8"))
        pairs.append(
            (
                stem,
                before_path.read_text(encoding="utf-8"),
                after_path.read_text(encoding="utf-8"),
                keeps,
                drops,
                allow_rules,
            )
        )
    return pairs


def counted_findings(result: dict, allow_rules: list[str]) -> list[dict]:
    allowed = set(allow_rules)
    return [item for item in result["findings"] if item["rule"] not in allowed]


class FixtureFidelityTests(unittest.TestCase):
    def test_keep_lines_are_in_before_and_after(self):
        for stem, before, after, keeps, _drops, _allow in load_pairs():
            with self.subTest(stem=stem):
                self.assertTrue(keeps, f"{stem}_keep.txt has no required lines")
                missing_before = [line for line in keeps if line not in before]
                missing_after = [line for line in keeps if line not in after]
                self.assertEqual([], missing_before)
                self.assertEqual([], missing_after)

    def test_after_adds_no_digit_or_time_strings(self):
        for stem, before, after, _keeps, _drops, _allow in load_pairs():
            with self.subTest(stem=stem):
                new_digits = strings_absent_from(DIGIT_RE.findall(after), before)
                new_measures = strings_absent_from(MEASURE_RE.findall(after), before)
                new_times = strings_absent_from(TIME_RE.findall(after), before)
                self.assertEqual([], new_digits)
                self.assertEqual([], new_measures)
                self.assertEqual([], new_times)

    def test_quoted_spans_survive_unless_dropped(self):
        for stem, before, after, _keeps, drops, _allow in load_pairs():
            with self.subTest(stem=stem):
                missing = [
                    inner
                    for inner in quoted_inners(before)
                    if inner not in drops and inner not in after
                ]
                self.assertEqual([], missing)

    def test_after_differs_from_before(self):
        audit = load_audit_module()
        for stem, before, after, _keeps, _drops, _allow in load_pairs():
            with self.subTest(stem=stem):
                self.assertNotEqual(before, after)
                before_score = audit.audit_text(before, profile="general")["score"]
                after_score = audit.audit_text(after, profile="general")["score"]
                self.assertLess(after_score, before_score)

    def test_after_score_ignores_only_allow_listed_rules(self):
        audit = load_audit_module()
        for stem, _before, after, _keeps, _drops, allow_rules in load_pairs():
            with self.subTest(stem=stem):
                result = audit.audit_text(after, profile="general")
                counted = counted_findings(result, allow_rules)
                blockers = [item["rule"] for item in counted if item["severity"] >= 3]
                score = sum(item["severity"] for item in counted)
                self.assertEqual([], allow_rules)
                self.assertEqual("clear", result["verdict"])
                self.assertEqual([], blockers)
                self.assertLessEqual(score, 2)

    def test_register_profile_after_is_clear_and_lower_scoring(self):
        audit = load_audit_module()
        seen = []
        for stem, before, after, _keeps, _drops, allow_rules in load_pairs():
            profile = REGISTER_PROFILES.get(stem)
            if profile is None:
                continue
            seen.append(stem)
            with self.subTest(stem=stem, profile=profile):
                before_result = audit.audit_text(before, profile=profile)
                after_result = audit.audit_text(after, profile=profile)
                self.assertEqual([], allow_rules)
                self.assertEqual("review", before_result["verdict"])
                self.assertEqual("clear", after_result["verdict"])
                self.assertLess(after_result["score"], before_result["score"])
        self.assertIn("editorial_commentary", seen)

    def test_new_person_names_warn_only(self):
        # Coarse screen: warn, do not fail the pair.
        for stem, before, after, _keeps, _drops, _allow in load_pairs():
            with self.subTest(stem=stem):
                warn_on_new_names(stem, before, after)

    def test_name_screen_warns_on_invented_zhou_jingming(self):
        before = "凌晨三点三十六分，沈弦盯着会议室的大屏。"
        after = before + "三天前，周景明临时加了一条策略。"
        self.assertIn("周景明", new_person_names(before, after))
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            warn_on_new_names("novel_opening", before, after)
        self.assertTrue(any("周景明" in str(item.message) for item in caught))

    def test_name_screen_skips_ordinary_surname_words(self):
        before = "原文。"
        after = "高价值区域。段落都差不多。连续出现。"
        self.assertEqual(set(), new_person_names(before, after))

    def test_drop_declaration_exempts_quoted_span(self):
        before = "老板说：“这句要删”。旁边还有“留下”。"
        after = "留下"
        keeps, drops, allow_rules = parse_keep_text(
            "# comment\n留下\n# drop: 这句要删\n# allow-rule: binary_contrast\n"
        )
        self.assertEqual(["留下"], keeps)
        self.assertEqual(["这句要删"], drops)
        self.assertEqual(["binary_contrast"], allow_rules)
        missing = [inner for inner in quoted_inners(before) if inner not in drops and inner not in after]
        self.assertEqual([], missing)
        still_required = [inner for inner in quoted_inners(before) if inner not in after]
        self.assertEqual(["这句要删"], still_required)

    def test_drop_line_accepts_wrapping_quotes(self):
        _keeps, drops, _allow = parse_keep_text("# drop: “这句要删”\n")
        self.assertEqual(["这句要删"], drops)

    def test_new_digit_and_time_strings_are_detected(self):
        before = "凌晨三点三十六分到场。"
        after = "凌晨三点三十六分到场，一共 12 人，晚上七点再开会。"
        self.assertEqual(["12"], strings_absent_from(DIGIT_RE.findall(after), before))
        new_times = strings_absent_from(TIME_RE.findall(after), before)
        self.assertTrue(any("晚上七点" in item for item in new_times), new_times)
        self.assertNotIn("凌晨三点三十六分", new_times)

    def test_new_measure_phrases_are_detected(self):
        before = "先整理资料，再输出方案。"
        after = "先做三件事，再准备三类材料。"
        new_measures = strings_absent_from(MEASURE_RE.findall(after), before)
        self.assertIn("三件", new_measures)
        self.assertIn("三类", new_measures)

    def test_loose_point_phrases_are_not_times(self):
        for text in ("少一点", "两点意见", "但这一点还需要研究支撑。"):
            with self.subTest(text=text):
                self.assertEqual([], TIME_RE.findall(text))


if __name__ == "__main__":
    unittest.main()
