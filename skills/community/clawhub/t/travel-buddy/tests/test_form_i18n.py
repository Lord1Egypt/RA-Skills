#!/usr/bin/env python3
"""The intake forms speak the traveller's language -- all of them, not most of them.

Both forms were Chinese-only while SKILL.md makes the form the mandatory first step, so an
English-speaking traveller's first screen was a page they could not read (2026-09-24). Each form
now keeps one HTML file with a zh/en dictionary; this test is what makes "every string" checkable,
because a translation that covers 95% of a form ships the other 5% to someone who cannot read it.

What it holds, for every form in FORMS:
  1. every visible text node containing CJK is under an element carrying data-i18n / data-i18n-html;
  2. every CJK placeholder / title / aria-label carries its data-i18n-* twin;
  3. every <option> has an explicit value, so translating its label never changes what is stored;
  4. the dictionary parses, zh and en have the same keys, every key the markup and the script use
     exists, every key in it is used, and no en value contains CJK;
  5. each zh value is the element's own original content (or attribute), so the default page is
     unchanged -- and a data-i18n element has no child elements, because setting its textContent
     would delete them (a checkbox inside a translated label is the case that bites);
  6. a CJK string literal left in the script is a STORED value, listed below with its reason.

Run:  python tests/test_form_i18n.py
      python -m pytest tests/test_form_i18n.py
"""

from __future__ import annotations

import html as html_module
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FORMS = [ROOT / "assets" / "trip-intake-form.html", ROOT / "assets" / "traveler-profile-intake.html"]

CJK = re.compile(r"[　-〿㐀-鿿＀-￯]")

# CJK literals a form's script may keep, because they are VALUES the intake stores and downstream
# reads, not text a traveller reads. Translating one would change what the pipeline receives, and
# the design keeps every stored value identical in both languages.
STORED_VALUE_LITERALS = {
    # travel_window.date_flexibility for an exact-date trip; the option values are the same words.
    "固定",
    # origin.connection_tolerance -- stored words the planner reads.
    "优先直飞，可接受转机", "仅接受直飞", "可接受转机", "未使用航班",
    # The climate checkbox VALUE that excludes all the others.
    "无特别气候限制",
    # destination_scope.commitment.
    "必须去", "强偏好",
    # Saved-profile spellings mapped onto the form's option values (old spelling -> current value).
    "交通枢纽", "机场/交通枢纽便利", "景点步行范围", "景点步行可达", "安静安全", "安静、安全",
    "海岸/海岛", "海岛/海岸", "山地徒步", "山地/徒步", "历史建筑", "历史建筑/古城", "当地美食",
    "美食/市场",
    # The example fill selects option VALUES, which are stored words in either language.
    "± 1–2 天", "情侣/两人", "舒适中档", "不超过 10 小时", "适中", "短距离步行", "邻近地铁/车站",
    "最好含早", "优先可取消", "高铁/动车优先", "仅短途接驳（约 3 小时内）",
    # feasibility.residence_status: the words the Chinese hint offers are what the intake has
    # always stored, so an English "EU citizen" is stored as the same word, not as a new value.
    "欧盟公民", "成员国居留卡", "欧盟长期居留", "短期签证", "其他", "不确定",
    # The profile's self-drive option VALUES: its example selects one, and the trip form maps each to
    # a label when it quotes the saved profile.
    "优先公共交通", "可接受自驾", "偏好自驾", "不自驾",
}
# Words a traveller may TYPE into the profile's list columns (scope, would-you-go-back, strength).
# The form recognises them and stores a code; it never displays them except as a suggestion, and a
# suggestion is taken from the table in the page's own language. Translating them would stop the
# form understanding a Chinese answer.
ACCEPTED_SPELLINGS = {
    "城市", "区域", "地区", "国家",
    "想", "想再去", "是", "不想", "不再去", "否", "说不好", "看情况", "也许",
    "永不推荐", "永远不去", "绝对不去", "暂时避开", "暂时不去", "这次不去",
}
# The language switch names the OTHER language in that language, so a reader who cannot read the
# page they are on can still find their own. It is a name, not a translation. ("中文" is also the
# profile's response-language option VALUE, which the example selects.)
LANGUAGE_ENDONYMS = {"中文"}


class Tree(HTMLParser):
    """Enough of the document to answer the checks: text nodes with their ancestors' attributes."""

    VOID = {"input", "br", "img", "meta", "link", "hr", "source", "area", "col", "wbr"}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.stack: list[tuple[str, dict]] = []
        self.texts: list[tuple[str, list[tuple[str, dict]]]] = []
        self.options: list[dict] = []
        self.attr_misses: list[str] = []
        self.attr_keys: list[tuple[str, str, str]] = []   # (attribute, key, original value)
        self.i18n_keys: set[str] = set()
        self.text_keyed_with_children: list[str] = []
        self.scripts: list[tuple[dict, str]] = []
        self._in_script: dict | None = None
        self._script_text: list[str] = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        for name in ("placeholder", "title", "aria-label"):
            twin = f"data-i18n-{name}"
            if attrs.get(name) and CJK.search(attrs[name]) and twin not in attrs:
                self.attr_misses.append(f"<{tag} {name}={attrs[name]!r}>")
            if attrs.get(twin):
                self.attr_keys.append((name, attrs[twin], attrs.get(name) or ""))
        for key, value in attrs.items():
            if key.startswith("data-i18n") and value:
                self.i18n_keys.add(value)
        if self.stack and "data-i18n" in self.stack[-1][1]:
            self.text_keyed_with_children.append(f"{self.stack[-1][1]['data-i18n']} > <{tag}>")
        if tag == "option":
            self.options.append(attrs)
        if tag == "script":
            self._in_script, self._script_text = attrs, []
        if tag not in self.VOID:
            self.stack.append((tag, attrs))

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in self.VOID:
            self.stack.pop()

    def handle_endtag(self, tag):
        if tag == "script" and self._in_script is not None:
            self.scripts.append((self._in_script, "".join(self._script_text)))
            self._in_script = None
        while self.stack:
            if self.stack.pop()[0] == tag:
                break

    def handle_data(self, data):
        if self._in_script is not None:
            self._script_text.append(data)
            return
        if any(tag == "style" for tag, _ in self.stack):
            return
        if CJK.search(data):
            self.texts.append((data, list(self.stack)))


def squash(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def keyed_contents(html: str, attr: str, key: str) -> list[str]:
    """The original inner content of EVERY element carrying attr="key" (shared keys included)."""
    pattern = rf'<(\w+)\b[^>]*\s{attr}="{re.escape(key)}"[^>]*>(.*?)</\1>'
    return [squash(m.group(2)) for m in re.finditer(pattern, html, re.S)]


def tag_sequence(fragment: str) -> list[str]:
    return re.findall(r"</?\s*([a-zA-Z0-9]+)", fragment)


def strip_comments(code: str) -> str:
    """Drop /* */ blocks and whole-line // comments, which carry CJK quotations as history."""
    code = re.sub(r"/\*.*?\*/", "", code, flags=re.S)
    return "\n".join(line for line in code.splitlines() if not line.lstrip().startswith("//"))


def string_literals(code: str) -> list[str]:
    """Every '...', "..." and `...` literal, read the way a tokenizer reads them.

    A regex over backticks pairs the END of one template literal with the START of the next and
    reports the code between them as a string; this walks the code instead. A template's ${...}
    stays part of its text, which is what the CJK check wants to see anyway.
    """
    found, i, n = [], 0, len(code)
    while i < n:
        quote = code[i]
        if quote not in "\"'`":
            i += 1
            continue
        j, text = i + 1, []
        while j < n and code[j] != quote:
            if code[j] == "\\":
                text.append(code[j:j + 2])
                j += 2
                continue
            if code[j] == "\n" and quote != "`":
                break
            text.append(code[j])
            j += 1
        found.append("".join(text))
        i = j + 1
    return found


def main() -> int:
    failures: list[str] = []

    def check(label: str, condition: object, detail: object = "") -> None:
        if not condition:
            failures.append(f"{label}\n    {str(detail)[:600]}")

    for form in FORMS:
        name = form.name
        html = form.read_text(encoding="utf-8")
        tree = Tree()
        tree.feed(html)

        # 1. Visible CJK text is always under a translated element.
        bare = [data.strip()[:40] for data, ancestors in tree.texts
                if not any("data-i18n" in attrs or "data-i18n-html" in attrs
                           for _, attrs in ancestors)]
        check(f"{name}: every CJK text node is translatable", not bare, bare[:8])
        # 2. Attributes.
        check(f"{name}: every CJK attribute is translatable", not tree.attr_misses,
              tree.attr_misses[:6])
        # 3. Stored values never depend on the display language.
        implicit = [o for o in tree.options if "value" not in o]
        check(f"{name}: every option states its stored value", not implicit, implicit[:4])
        # 5b. textContent replaces children, so a keyed element must not have any.
        check(f"{name}: no data-i18n element has child elements", not tree.text_keyed_with_children,
              tree.text_keyed_with_children[:6])

        # 4. The dictionary.
        blocks = [text for attrs, text in tree.scripts if attrs.get("id") == "tb-i18n"]
        check(f"{name}: the form carries its dictionary", len(blocks) == 1, len(blocks))
        if len(blocks) != 1:
            continue
        try:
            table = json.loads(blocks[0])
        except ValueError as exc:
            check(f"{name}: the dictionary parses", False, exc)
            continue
        zh, en = table.get("zh") or {}, table.get("en") or {}
        check(f"{name}: zh and en carry the same keys", set(zh) == set(en),
              sorted(set(zh) ^ set(en))[:8])
        code = strip_comments("\n".join(text for attrs, text in tree.scripts
                                        if attrs.get("id") != "tb-i18n"))
        namespaces = {key.split(".", 1)[0] for key in zh}
        script_keys = {lit for lit in re.findall(r'"([a-z][a-z0-9_-]*(?:\.[a-z0-9_-]+)+)"', code)
                       if lit.split(".", 1)[0] in namespaces}
        used = tree.i18n_keys | script_keys
        check(f"{name}: every key used exists in the dictionary", used <= set(zh),
              sorted(used - set(zh))[:8])
        check(f"{name}: every dictionary key is used", set(zh) <= used, sorted(set(zh) - used)[:8])
        cjk_en = [k for k, v in en.items() if CJK.search(str(v))]
        check(f"{name}: no English value contains CJK", not cjk_en, cjk_en[:8])
        blank = [k for k, v in {**zh, **en}.items() if not str(v).strip()]
        check(f"{name}: no dictionary value is blank", not blank, blank[:8])
        # Missing required fields are named in one joined list, so a field name that contains the
        # list separator ("Nature, culture or a balance") splits into what reads as two fields.
        for lang, table_ in (("zh", zh), ("en", en)):
            sep = str(table_.get("sep.list", "")).strip()
            split = [k for k, v in table_.items() if k.startswith("req.") and sep and sep in str(v)]
            check(f"{name}: no {lang} required-field name contains the list separator", not split, split)
        # The forms are shared by every assistant that runs the skill. The profile page told
        # everyone to "go back to Codex" in both languages, including a traveller on Claude Code,
        # Cursor or opencode, who has no Codex to go back to.
        branded = [k for k, v in {**zh, **en}.items()
                   if re.search(r"\b(?:codex|claude|chatgpt|cursor|opencode)\b", str(v), re.I)]
        check(f"{name}: no page text names one assistant", not branded, branded[:6])
        for key in sorted(k for k in tree.i18n_keys if k in zh and k in en):
            if f'data-i18n-html="{key}"' in html:
                check(f"{name}: {key} keeps its markup in English",
                      tag_sequence(zh[key]) == tag_sequence(en[key]),
                      f"{tag_sequence(zh[key])} vs {tag_sequence(en[key])}")

        # 5. The default (zh) rendering is the original page.
        drift = []
        for key in sorted(tree.i18n_keys):
            for content in keyed_contents(html, "data-i18n", key):
                if squash(str(zh.get(key, ""))) != squash(html_module.unescape(content)):
                    drift.append(f"{key}: {content[:40]!r}")
            for content in keyed_contents(html, "data-i18n-html", key):
                if squash(str(zh.get(key, ""))) != content:
                    drift.append(f"{key}: {content[:40]!r}")
        for attr, key, original in tree.attr_keys:
            if str(zh.get(key, "")) != original:
                drift.append(f"{key} ({attr}): {original[:40]!r}")
        check(f"{name}: each zh value is the element's own content", not drift, drift[:8])

        # 6. The only CJK left in the script is a stored value.
        literals = {lit for lit in string_literals(code) if CJK.search(lit)}
        allowed = STORED_VALUE_LITERALS | ACCEPTED_SPELLINGS | LANGUAGE_ENDONYMS
        stray = sorted(lit for lit in literals if lit not in allowed
                       and not re.fullmatch(r'input\[name="[\w-]+"\]\[value="[^"]+"\]', lit))
        check(f"{name}: CJK in the script is only stored values", not stray, stray[:10])

    if failures:
        print(f"FAILED {len(failures)} case(s):\n", file=sys.stderr)
        for failure in failures:
            print(f"--- {failure}\n", file=sys.stderr)
        return 1
    print(f"form i18n cases passed for {len(FORMS)} form(s)")
    return 0


def test_form_i18n() -> None:
    assert main() == 0


if __name__ == "__main__":
    raise SystemExit(main())
