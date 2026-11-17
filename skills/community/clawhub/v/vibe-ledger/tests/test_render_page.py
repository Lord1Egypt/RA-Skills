import re

import pytest

import render
from helpers.verified import OPENAI, PROBES, RUN, sample
from ledger_report import bits, i18n


def test_i18n_key_sets_match_and_t_formats():
    assert set(i18n.STR["zh"]) == set(i18n.STR["en"])
    assert i18n.t("zh", "ok_rows", n=3) == "其余 3 类数据（没发现问题）"
    assert i18n.t("fr", "today") == i18n.STR["en"]["today"]


def test_every_literal_key_used_in_the_report_code_exists():
    import pathlib
    scripts = pathlib.Path(__file__).resolve().parents[1] / "scripts"
    src = "".join(p.read_text(encoding="utf-8") for p in scripts.glob("**/*.py"))
    keys = set(re.findall(r"""\bt\(\s*lang\s*,\s*["']([a-z_]+)["']\s*[,)]""", src))
    assert keys and keys <= set(i18n.STR["en"]), keys - set(i18n.STR["en"])


def test_h_masks_then_escapes_and_ht_masks_before_truncating():
    assert bits.h(f"<b>{OPENAI}</b>") == f"&lt;b&gt;sk-proj-…{OPENAI[-4:]}&lt;/b&gt;"
    short = bits.ht(f"key: {OPENAI}", 20)
    assert "Ab3dE5fG7h" not in short and len(short) <= 20


def test_counts_and_summaries():
    led = sample()
    assert render.counts(led) == {"broken": 1, "partial": 0, "pending": 1, "unknown": 1, "kept": 1}
    s = render.summaries(led, "zh")
    assert s["where_data"] == "数据存放在：Supabase。数据还会发给：OpenAI。"
    assert s["what_costs"] == "会花钱的服务：OpenAI。"
    assert s["who_can_see"] == "2 类数据里，有 1 类陌生人能读到；0 处说法冲突。"
    assert s["what_breaks"] == "1 处“报错后的妥协”仍在代码里；1 条承诺没做到。"
    assert s["open_debts"] == "还欠着 1 件说过“以后再说”的事。"


def test_page_structure(monkeypatch):
    html = render.render_html(sample(), RUN, PROBES, "zh")
    assert html.startswith("<!doctype html>") and '<html lang="zh-CN">' in html
    assert "「notes」对账单" in html and "依据 2 段对话" in html
    assert html.index("没做到") < html.index("做到了")
    assert html.count('class="copy"') == 2  # broken + pending; not unknown, not kept
    assert 'class="verdict-dev dev-only"' in html
    assert "原结论“做到了”缺少能通过校验的证据" in html
    assert "没有覆盖的技术栈：flask" in html and "lib/legacy.ts" in html
    assert "file not found" in html and "made up" in html and "format may have changed" in html
    assert 'data-status="broken"' in html and 'data-filter="pending"' in html


def test_report_never_contains_a_raw_secret():
    html = render.render_html(sample(), RUN, PROBES, "zh")
    assert OPENAI not in html and f"sk-proj-…{OPENAI[-4:]}" in html
    assert render.find_secrets(html) == []


def test_assert_no_secrets_refuses():
    with pytest.raises(RuntimeError) as exc:
        render.assert_no_secrets(f"<p>{OPENAI}</p>")
    assert OPENAI not in str(exc.value)


def test_english_report_and_empty_ledger():
    led = sample()
    led["promises"], led["compromises"] = [], []
    led["map"] = {"nodes": [], "edges": [], "unverified_nodes": [], "unverified_edges": []}
    led["access"] = {"resources": []}
    led["paths"] = []
    run = {**RUN, "sessions": {**RUN["sessions"], "records": 0, "threads": 0}}
    html = render.render_html(led, run, PROBES, "en")
    assert '<html lang="en">' in html and "No conversations were found" in html
    assert "The ledger is empty" in html


def test_deliver_prefers_explicit_dir_then_falls_back(tmp_path, monkeypatch):
    run_dir = tmp_path / "run"
    run_dir.mkdir()
    out = render.deliver("<p>x</p>", run_dir, "我的 应用", out_dir=tmp_path / "out")
    assert out.parent == tmp_path / "out" and out.name.startswith("vibe-ledger-我的-应用-")
    assert (run_dir / "report.html").exists()
    blocker = tmp_path / "not-a-dir"
    blocker.write_text("x")
    monkeypatch.setenv("HOME", str(tmp_path / "nohome"))
    fallback = render.deliver("<p>x</p>", run_dir, "app", out_dir=blocker)
    assert fallback == run_dir / "report.html"


def test_deliver_uses_env_dir(tmp_path, monkeypatch):
    monkeypatch.setenv("VIBE_LEDGER_OUT_DIR", str(tmp_path / "env-out"))
    run_dir = tmp_path / "run"
    run_dir.mkdir()
    assert render.deliver("<p>x</p>", run_dir, "app").parent == tmp_path / "env-out"


def test_deliver_never_overwrites_another_report(tmp_path):
    run_a, run_b = tmp_path / "a", tmp_path / "b"
    run_a.mkdir()
    run_b.mkdir()
    first = render.deliver("<p>A</p>", run_a, "project", out_dir=tmp_path / "out")
    second = render.deliver("<p>B</p>", run_b, "project", out_dir=tmp_path / "out")
    assert first != second
    assert first.read_text() == "<p>A</p>" and second.read_text() == "<p>B</p>"


def test_fit_counts_wide_characters_as_two():
    assert bits.width("ab中文") == 6
    s = bits.fit("不要让陌生人随便调用 AI 花我的钱", 20)
    assert bits.width(s) <= 20 and s.endswith("…")
    assert bits.fit("short", 20) == "short"
    assert "Ab3dE5fG7h" not in bits.hf(f"key: {OPENAI}", 12)


def test_skipped_checks_are_explained_in_the_report_language():
    zh = render.render_html(sample(), RUN, PROBES, "zh")
    assert "firebase_rules（项目没用到 firebase）" in zh and "routes (crashed: ValueError(&#x27;x&#x27;))" in zh
    en = render.render_html(sample(), RUN, PROBES, "en")
    assert "firebase_rules (this project does not use firebase)" in en


def test_downgraded_verdicts_are_labelled_unverified():
    html = render.render_html(sample(), RUN, PROBES, "zh")
    card = html[html.index('id="P3"'):]
    card = card[:card.index("</article>")]
    assert "未经核实的原结论" in card
    assert card.index("未经核实的原结论") < card.index("没找到能证明这一点的代码")
    row = html[html.index('data-status="unknown"'):]
    row = row[:row.index("</tr>")]
    assert "未经核实的原结论" in row


def test_without_conversations_the_report_does_not_claim_zero_problems():
    led = sample()
    led["promises"], led["compromises"] = [], []
    run = {**RUN, "sessions": {**RUN["sessions"], "records": 0, "threads": 0}}
    html = render.render_html(led, run, PROBES, "zh")
    assert "没做到 <b>0</b>" not in html and 'class="counts"' not in html
    assert "0 条承诺没做到" not in html and "没有对话记录，这一问无法回答" in html


def test_english_counts_take_the_singular_for_one():
    from pathlib import Path
    from ledger_report.i18n import STR, t
    assert t("en", "g_area_row", n=1) == "1 file" and t("en", "g_area_row", n=2) == "2 files"
    assert t("en", "g_badge_warn", n=1) == "1 hint" and t("en", "g_badge_warn", n=0) == "0 hints"
    one = t("en", "r_summary", n=1, messages=1, skipped=1)
    assert one.startswith("1 requirement from your 1 message; 1 more was a confirmation"), one
    assert t("zh", "g_area_row", n=1) == "1 个文件"
    assert not any("|" in v and "{" in v for v in STR["zh"].values() if isinstance(v, str))
    js = (Path(__file__).resolve().parents[1] / "scripts/ledger_report/assets/graph.js").read_text(encoding="utf-8")
    assert "one : many" in js  # graph.js formats the same "{n|one|many}" token
