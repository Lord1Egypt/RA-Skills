from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = SKILL_ROOT / "scripts" / "audit_ai_flavor.py"


def load_audit_module():
    spec = importlib.util.spec_from_file_location("tone_audit", SCRIPT_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("Unable to load audit module")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


audit = load_audit_module()


class AuditBehaviorTests(unittest.TestCase):
    def test_general_profile_lists_binary_shell_without_scoring(self):
        result = audit.audit_text("这不是效率问题，而是系统问题。", profile="general")
        contrasts = [item for item in result["findings"] if item["rule"] == "binary_contrast"]
        self.assertEqual([0], [item["severity"] for item in contrasts])
        self.assertEqual(0, result["score"])
        self.assertEqual(1, result["finding_count"])
        self.assertEqual("clear", result["verdict"])

    def test_general_profile_reviews_when_other_rules_still_cluster(self):
        text = (
            "这不是效率问题，而是系统问题。"
            "总的来说，这套方法论是赋能团队的抓手。"
            "值得注意的是，它能助力增长。"
        )
        result = audit.audit_text(text, profile="general")
        contrasts = [item for item in result["findings"] if item["rule"] == "binary_contrast"]
        self.assertEqual([0], [item["severity"] for item in contrasts])
        self.assertEqual(7, result["score"])
        self.assertEqual("review", result["verdict"])

    def test_fiction_profile_preserves_required_dialogue(self):
        text = "沈弦说：“这不是参数波动，而是有人改了供电优先级。”"
        result = audit.audit_text(text, profile="fiction")
        self.assertEqual("clear", result["verdict"])
        self.assertNotIn("binary_contrast", {item["rule"] for item in result["findings"]})

    def test_direct_quote_is_not_treated_as_editable_prose(self):
        text = "报告原文写道：“这不是效率问题，而是系统问题。”"
        result = audit.audit_text(text, profile="general")
        self.assertEqual("clear", result["verdict"])
        self.assertNotIn("binary_contrast", {item["rule"] for item in result["findings"]})

    def test_academic_profile_does_not_block_defined_core_phrase(self):
        text = "该方法的核心在于保持边界条件一致。"
        result = audit.audit_text(text, profile="academic")
        self.assertEqual("clear", result["verdict"])
        essence = [item for item in result["findings"] if item["rule"] == "essence_claim"]
        self.assertEqual([1], [item["severity"] for item in essence])

    def test_academic_profile_reviews_core_phrase_when_other_filler_clusters(self):
        text = "本研究的核心在于赋能行业发展，具有重要现实意义。"
        result = audit.audit_text(text, profile="academic")
        self.assertEqual("review", result["verdict"])

    def test_sop_profile_allows_operational_order(self):
        text = "先关闭总闸，再拆下外壳。先确认电容放电，再接触主板。"
        result = audit.audit_text(text, profile="sop")
        self.assertEqual("clear", result["verdict"])
        sequences = [item for item in result["findings"] if item["rule"] == "staged_sequence"]
        self.assertEqual([0, 0], [item["severity"] for item in sequences])

    def test_sop_profile_reviews_ceremonial_sequence_with_jargon(self):
        text = "先统一思想，再形成共识。总的来说，这将赋能团队。值得注意的是，这套闭环会助力长期主义。"
        result = audit.audit_text(text, profile="sop")
        self.assertEqual("review", result["verdict"])
        self.assertEqual(8, result["score"])
        sequences = [item for item in result["findings"] if item["rule"] == "staged_sequence"]
        self.assertEqual([0], [item["severity"] for item in sequences])

    def test_fiction_profile_reviews_clustered_narrator_cliches(self):
        text = "他不禁停下脚步，随后缓缓说道：夜已经深了。"
        result = audit.audit_text(text, profile="fiction")
        self.assertEqual("review", result["verdict"])

    def test_social_profile_reviews_clustered_marketing_jargon(self):
        text = "这套长期主义内容闭环会留下来。"
        result = audit.audit_text(text, profile="social")
        self.assertEqual("review", result["verdict"])

    def test_all_before_fixtures_require_review(self):
        # Novel narration only reaches review under fiction, where the two
        # stock modifiers are severity 2 and the same rule repeats.
        fixture_dir = SKILL_ROOT / "tests" / "fixtures"
        profiles = {"novel_opening_before.md": "fiction"}
        verdicts = {
            path.name: audit.audit_text(
                path.read_text(encoding="utf-8"),
                profile=profiles.get(path.name, "general"),
            )["verdict"]
            for path in fixture_dir.glob("*_before.md")
        }
        self.assertTrue(verdicts)
        self.assertEqual([], [name for name, verdict in verdicts.items() if verdict != "review"])

    def test_sequence_pattern_does_not_cross_sentence_boundary(self):
        text = "先关闭总闸。随后核对电压。"
        result = audit.audit_text(text, profile="general")
        self.assertNotIn("staged_sequence", {item["rule"] for item in result["findings"]})

    def test_fenced_code_is_not_audited_as_prose(self):
        text = "示例命令如下：\n```text\n先备份，再部署。\n```"
        result = audit.audit_text(text, profile="general")
        self.assertEqual("clear", result["verdict"])
        self.assertEqual([], result["findings"])

    def test_chinese_corner_quotes_are_not_treated_as_editable_prose(self):
        for text in (
            "报告写道：『这不是效率问题，而是系统问题。』",
            "报告写道：「这不是效率问题，\n而是系统问题。」",
        ):
            with self.subTest(text=text):
                result = audit.audit_text(text, profile="general")
                self.assertEqual("clear", result["verdict"])


class AuditCliTests(unittest.TestCase):
    def test_cli_expands_windows_style_glob(self):
        # Glob expansion only. Fidelity tests check after-fixture verdicts.
        pattern = str(SKILL_ROOT / "tests" / "fixtures" / "*_after.md")
        completed = subprocess.run(
            [sys.executable, str(SCRIPT_PATH), pattern],
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        self.assertEqual(0, completed.returncode, completed.stderr)
        self.assertIn("academic_technical_after.md", completed.stdout)
        self.assertNotIn("Traceback", completed.stderr)

    def test_cli_accepts_stdin_and_emits_versioned_json(self):
        completed = subprocess.run(
            [sys.executable, str(SCRIPT_PATH), "--stdin", "--json", "--profile", "general"],
            input="普通句子。",
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        self.assertEqual(0, completed.returncode, completed.stderr)
        payload = json.loads(completed.stdout)
        self.assertEqual(1, payload["schema_version"])
        self.assertEqual("clear", payload["results"]["<stdin>"]["verdict"])
        self.assertIn("not", payload["verdict_semantics"].lower())
        self.assertIn("authorship", payload["verdict_semantics"].lower())

    def test_cli_plain_output_explains_clear_verdict(self):
        completed = subprocess.run(
            [sys.executable, str(SCRIPT_PATH), "--stdin"],
            input="普通句子。",
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        self.assertEqual(0, completed.returncode, completed.stderr)
        self.assertIn("not a prose-quality or authorship judgment", completed.stdout)

    def test_cli_reports_missing_path_without_traceback(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            missing = str(Path(temp_dir) / "missing.md")
            completed = subprocess.run(
                [sys.executable, str(SCRIPT_PATH), missing],
                check=False,
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
        self.assertEqual(2, completed.returncode)
        self.assertIn("not found", completed.stderr.lower())
        self.assertNotIn("Traceback", completed.stderr)

    def test_cli_fail_on_review_exits_1_when_document_needs_review(self):
        completed = subprocess.run(
            [sys.executable, str(SCRIPT_PATH), "--stdin", "--fail-on-review"],
            input="总的来说，范围已经收束。值得注意的是，步骤没有变。",
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        self.assertEqual(1, completed.returncode, completed.stdout + completed.stderr)
        self.assertIn("review score=", completed.stdout)
        self.assertNotIn("Traceback", completed.stderr)

    def test_cli_fail_on_review_exits_0_for_zero_severity_contrast(self):
        completed = subprocess.run(
            [sys.executable, str(SCRIPT_PATH), "--stdin", "--fail-on-review"],
            input="这不是效率问题，而是系统问题。",
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        self.assertEqual(0, completed.returncode, completed.stdout + completed.stderr)
        self.assertIn("clear score=0", completed.stdout)
        self.assertIn("二分对照壳", completed.stdout)
        self.assertNotIn("Traceback", completed.stderr)


def rules_of(result):
    return {item["rule"] for item in result["findings"]}


class AuditBoundaryRegressionTests(unittest.TestCase):
    def test_xian_inside_common_words_is_not_staged_sequence(self):
        for text in (
            "王先生再次来电确认了时间。",
            "系统会优先处理队列，再写日志。",
            "事先通知相关人，再开始变更。",
            "首先核对名单，再发放材料。",
            "他率先到达现场，再组织分工。",
            "预先准备材料，再进场。",
            "抢先发布通知，再补说明。",
        ):
            with self.subTest(text=text):
                result = audit.audit_text(text, profile="general")
                self.assertNotIn("staged_sequence", rules_of(result))

    def test_real_staged_sequence_still_matches(self):
        for text in (
            "先关闭总闸，再拆下外壳。",
            "我会先整理资料，再输出方案。",
            "先生先到，再登记。",
            "第一步备份配置，第二步开放流量。",
        ):
            with self.subTest(text=text):
                result = audit.audit_text(text, profile="general")
                sequences = [item for item in result["findings"] if item["rule"] == "staged_sequence"]
                self.assertEqual([2], [item["severity"] for item in sequences])

    def test_false_contrast_shells_do_not_match(self):
        for text in (
            "要不是下雨，而是晴天，比赛也会照常。",
            "你是不是把附件发错了，而是发到了旧邮箱。",
        ):
            with self.subTest(text=text):
                result = audit.audit_text(text, profile="general")
                self.assertNotIn("binary_contrast", rules_of(result))

    def test_real_binary_contrast_still_matches_at_severity_0(self):
        text = "你是不是觉得这不是效率问题，而是系统问题。"
        result = audit.audit_text(text, profile="general")
        contrasts = [item for item in result["findings"] if item["rule"] == "binary_contrast"]
        self.assertEqual(1, len(contrasts))
        self.assertEqual(0, contrasts[0]["severity"])
        self.assertIn("不是效率问题，而是", contrasts[0]["match"])

    def test_adjacent_contrasts_are_counted_separately(self):
        text = "不是记录问题，而是交接问题；不是个人疏忽，而是名单过期。"
        result = audit.audit_text(text, profile="general")
        contrasts = [item for item in result["findings"] if item["rule"] == "binary_contrast"]
        self.assertEqual(2, len(contrasts))
        self.assertEqual([0, 0], [item["severity"] for item in contrasts])

    def test_missing_contrast_forms_are_detected(self):
        samples = (
            "问题不在这段脚本里，而在昨天改过的配置。",
            "预算并没有增加，而是改了支出科目。",
        )
        for text in samples:
            with self.subTest(text=text):
                result = audit.audit_text(text, profile="general")
                contrasts = [item for item in result["findings"] if item["rule"] == "binary_contrast"]
                self.assertEqual([0], [item["severity"] for item in contrasts])

    def test_existing_contrast_forms_still_match_once(self):
        for text in (
            "不在于形式，而在于结果。",
            "不只是记录，更是复盘。",
            "并非临时起意，而是长期安排。",
            "与其说是效率问题，不如说是系统问题。",
        ):
            with self.subTest(text=text):
                result = audit.audit_text(text, profile="general")
                contrasts = [item for item in result["findings"] if item["rule"] == "binary_contrast"]
                self.assertEqual(1, len(contrasts))
                self.assertEqual(0, contrasts[0]["severity"])

    def test_partial_quote_does_not_exempt_surrounding_contrast(self):
        text = "他说的不是“效率”，而是“系统”。"
        result = audit.audit_text(text, profile="general")
        self.assertIn("binary_contrast", rules_of(result))

    def test_jin_and_zhuli_do_not_match_longer_words(self):
        banned = audit.audit_text("本场所不禁止拍照。", profile="general")
        self.assertNotIn("fiction_cliche", rules_of(banned))
        vehicle = audit.audit_text("电动助力车停在门口。", profile="general")
        self.assertNotIn("inflated_abstract_words", rules_of(vehicle))

    def test_jin_and_zhuli_still_match_as_terms(self):
        cliche = audit.audit_text("他不禁停下脚步。", profile="fiction")
        hits = [item for item in cliche["findings"] if item["rule"] == "fiction_cliche"]
        self.assertEqual([("不禁", 2)], [(item["match"], item["severity"]) for item in hits])

        mixed = audit.audit_text("规定不禁止旁听，他不禁笑出声。", profile="general")
        hits = [item for item in mixed["findings"] if item["rule"] == "fiction_cliche"]
        self.assertEqual(["不禁"], [item["match"] for item in hits])

        help_word = audit.audit_text("这项安排会助力后续复盘。", profile="general")
        hits = [item for item in help_word["findings"] if item["rule"] == "inflated_abstract_words"]
        self.assertEqual([("助力", 1)], [(item["match"], item["severity"]) for item in hits])

        both = audit.audit_text("购买助力车之后，再谈如何助力复盘。", profile="general")
        hits = [item for item in both["findings"] if item["rule"] == "inflated_abstract_words"]
        self.assertEqual(["助力"], [item["match"] for item in hits])

    def test_qingbuzijin_is_not_also_counted_as_bujin(self):
        result = audit.audit_text("她情不自禁地笑了。", profile="general")
        hits = [item for item in result["findings"] if item["rule"] == "fiction_cliche"]
        self.assertEqual(["情不自禁"], [item["match"] for item in hits])


class AuditQuoteAndTitleRegressionTests(unittest.TestCase):
    def test_unclosed_quote_does_not_exempt_later_paragraphs(self):
        text = (
            "草稿开头落下一个“。\n"
            "\n"
            "总的来说，这不是效率问题，而是系统问题。真正重要的是把边界写清楚。\n"
            "\n"
            "写到这里才补上收尾的”。\n"
        )
        result = audit.audit_text(text, profile="general")
        self.assertIn("lecture_marker", rules_of(result))
        self.assertIn("binary_contrast", rules_of(result))
        self.assertIn("essence_claim", rules_of(result))

    def test_blank_line_of_spaces_also_ends_quote_span(self):
        text = "句首有一个“。\n \n总的来说，这不是效率问题，而是系统问题。\n \n结束的”。"
        result = audit.audit_text(text, profile="general")
        self.assertIn("lecture_marker", rules_of(result))
        self.assertIn("binary_contrast", rules_of(result))

    def test_quote_may_still_cross_a_single_line_break(self):
        text = "报告写道：「这不是效率问题，\n而是系统问题。」"
        result = audit.audit_text(text, profile="general")
        self.assertNotIn("binary_contrast", rules_of(result))
        self.assertEqual("clear", result["verdict"])

    def test_ascii_apostrophes_do_not_exempt_prose(self):
        text = "It's fine. 这不是效率问题，而是系统问题。 Don't worry."
        result = audit.audit_text(text, profile="general")
        contrasts = [item for item in result["findings"] if item["rule"] == "binary_contrast"]
        self.assertEqual(1, len(contrasts))
        self.assertEqual(0, contrasts[0]["severity"])

    def test_ascii_single_quotes_around_chinese_still_exempt(self):
        text = "他说：'这不是效率问题，而是系统问题。'"
        result = audit.audit_text(text, profile="general")
        self.assertNotIn("binary_contrast", rules_of(result))

    def test_book_title_marks_are_not_audited(self):
        titled = audit.audit_text("详见《先备份，再部署》里的说明。", profile="general")
        self.assertNotIn("staged_sequence", rules_of(titled))
        titled_term = audit.audit_text("请阅读《赋能团队的方法》。", profile="general")
        self.assertNotIn("inflated_abstract_words", rules_of(titled_term))

    def test_text_outside_book_title_marks_is_still_audited(self):
        result = audit.audit_text("先备份配置，再阅读《部署手册》。", profile="general")
        sequences = [item for item in result["findings"] if item["rule"] == "staged_sequence"]
        self.assertEqual(1, len(sequences))
        outside = audit.audit_text("这套做法会赋能团队，详见《手册》。", profile="general")
        words = [item for item in outside["findings"] if item["rule"] == "inflated_abstract_words"]
        self.assertEqual(["赋能"], [item["match"] for item in words])


class AuditCitationAndQuestionRegressionTests(unittest.TestCase):
    def test_research_claim_with_nearby_citation_is_skipped(self):
        for text in (
            "研究表明，注意力会回升（Chen, 2020）。",
            "研究表明，注意力会回升（林某，2019）。",
            "研究表明该方法有效[12]。",
            "研究表明该方法有效(Chen, 2020)。",
            "研究表明" + ("补" * 29) + "（Ada, 2020）。",
        ):
            with self.subTest(text=text):
                result = audit.audit_text(text, profile="academic")
                self.assertNotIn("academic_filler", rules_of(result))

    def test_research_claim_without_nearby_citation_still_matches(self):
        for text in (
            "研究表明，注意力会回升。",
            "研究表明[待补]。",
            "研究表明" + ("补" * 30) + "（Ada, 2020）。",
            "专家认为这种方法可行（Chen, 2020）。",
        ):
            with self.subTest(text=text):
                result = audit.audit_text(text, profile="academic")
                fillers = [item for item in result["findings"] if item["rule"] == "academic_filler"]
                self.assertEqual([2], [item["severity"] for item in fillers])

    def test_transactional_closing_questions_are_skipped(self):
        for text in (
            "请问你周四下午三点前能确认参会人数吗？",
            "你能否参加这次讨论吗？",
            "你方便看一下附件吗？",
            "你知道截止日期改了吗？",
            "你收到后确认一下参会人数吗？",
            "请问你还有补充吗？",
            "你周四有空吗？",
            "你三点前有空吗？",
        ):
            with self.subTest(text=text):
                result = audit.audit_text(text, profile="general")
                self.assertNotIn("ending_engagement_question", rules_of(result))

    def test_generic_closing_questions_still_match(self):
        for text in (
            "你觉得这个方案怎么样？",
            "大家还有没有想补充的？",
            "你有一点想法吗？",
        ):
            with self.subTest(text=text):
                result = audit.audit_text(text, profile="general")
                questions = [item for item in result["findings"] if item["rule"] == "ending_engagement_question"]
                self.assertEqual([3], [item["severity"] for item in questions])


class AuditShapeLineAndRecursiveTests(unittest.TestCase):
    def test_shape_rules_report_real_line_numbers(self):
        hen = audit.audit_text("前言一句。\n\n房间很暗。风很大。路很滑。", profile="general")
        hen_hits = [item for item in hen["findings"] if item["rule"] == "dense_hen_judgments"]
        self.assertEqual([3], [item["line"] for item in hen_hits])

        paragraphs = "标题\n\n" + "\n\n".join(["段" * 30] * 5)
        even = audit.audit_text(paragraphs, profile="general")
        even_hits = [item for item in even["findings"] if item["rule"] == "over_even_paragraph_distribution"]
        self.assertEqual([3], [item["line"] for item in even_hits])

        people = audit.audit_text(
            "这里没有称呼。\n\n你看看甲，你看看乙，你看看丙，大家看看丁，你看看戊，大家看看己。",
            profile="general",
        )
        people_hits = [item for item in people["findings"] if item["rule"] == "second_person_overuse"]
        self.assertEqual([3], [item["line"] for item in people_hits])

    def test_cli_directory_scan_is_not_recursive_by_default(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            nested = root / "nested"
            nested.mkdir()
            (nested / "note.md").write_text("普通句子。", encoding="utf-8")
            completed = subprocess.run(
                [sys.executable, str(SCRIPT_PATH), str(root)],
                check=False,
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
        self.assertEqual(2, completed.returncode)
        self.assertIn("no readable text files", completed.stderr.lower())
        self.assertNotIn("Traceback", completed.stderr)

    def test_cli_recursive_flag_scans_subdirectories(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            nested = root / "nested"
            nested.mkdir()
            (root / "top.txt").write_text("普通句子。", encoding="utf-8")
            (nested / "note.md").write_text("这也是普通句子。", encoding="utf-8")
            (nested / "skip.py").write_text("print('先备份，再部署')", encoding="utf-8")
            without = subprocess.run(
                [sys.executable, str(SCRIPT_PATH), str(root), "--json"],
                check=False,
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
            with_flag = subprocess.run(
                [sys.executable, str(SCRIPT_PATH), str(root), "--recursive", "--json"],
                check=False,
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
        self.assertEqual(0, without.returncode, without.stderr)
        without_payload = json.loads(without.stdout)
        self.assertEqual(["top.txt"], [Path(name).name for name in without_payload["results"]])
        self.assertEqual(0, with_flag.returncode, with_flag.stderr)
        with_payload = json.loads(with_flag.stdout)
        self.assertEqual(
            ["note.md", "top.txt"],
            sorted(Path(name).name for name in with_payload["results"]),
        )
        self.assertEqual(1, with_payload["schema_version"])
        self.assertNotIn("skip.py", with_flag.stdout)


class AuditVerdictThresholdTests(unittest.TestCase):
    def test_binary_contrast_is_zero_in_every_profile(self):
        text = "这不是效率问题，而是系统问题。"
        for profile in audit.PROFILES:
            with self.subTest(profile=profile):
                result = audit.audit_text(text, profile=profile)
                contrasts = [item for item in result["findings"] if item["rule"] == "binary_contrast"]
                self.assertEqual([0], [item["severity"] for item in contrasts])
                self.assertEqual(0, result["score"])
                self.assertEqual(0, result["blocker_count"])
                self.assertEqual(1, result["finding_count"])
                self.assertEqual("clear", result["verdict"])

    def test_score_3_is_clear_and_score_4_is_review(self):
        score_3 = audit.audit_text("这套做法会赋能团队，也能助力复盘，并且留下一个抓手。", profile="general")
        self.assertEqual([1, 1, 1], sorted(item["severity"] for item in score_3["findings"]))
        self.assertEqual(3, score_3["score"])
        self.assertEqual(0, score_3["blocker_count"])
        self.assertEqual("clear", score_3["verdict"])

        score_4 = audit.audit_text(
            "这套做法会赋能团队，也能助力复盘，并且留下一个抓手，最后收成闭环。",
            profile="general",
        )
        self.assertEqual([1, 1, 1, 1], sorted(item["severity"] for item in score_4["findings"]))
        self.assertEqual(4, score_4["score"])
        self.assertEqual(0, score_4["blocker_count"])
        self.assertEqual("review", score_4["verdict"])

    def test_one_severity_3_finding_is_clear(self):
        result = audit.audit_text("下面我们来核对今晚的名单。", profile="general")
        self.assertEqual([3], [item["severity"] for item in result["findings"]])
        self.assertEqual(1, result["blocker_count"])
        self.assertEqual(3, result["score"])
        self.assertEqual("clear", result["verdict"])

    def test_two_severity_3_findings_review(self):
        result = audit.audit_text("下面我们来核对名单。你觉得这个方案怎么样？", profile="general")
        self.assertEqual([3, 3], sorted(item["severity"] for item in result["findings"]))
        self.assertEqual(2, result["blocker_count"])
        self.assertEqual("review", result["verdict"])

    def test_same_rule_severity_2_twice_reviews(self):
        result = audit.audit_text("总的来说，范围已经收束。值得注意的是，步骤没有变。", profile="general")
        lectures = [item for item in result["findings"] if item["rule"] == "lecture_marker"]
        self.assertEqual([2, 2], sorted(item["severity"] for item in lectures))
        self.assertEqual(2, len(result["findings"]))
        self.assertEqual(4, result["score"])
        self.assertEqual("review", result["verdict"])

    def test_severity_1_repeat_does_not_force_review(self):
        result = audit.audit_text("这套做法会赋能团队，也能助力复盘。", profile="general")
        self.assertEqual([1, 1], sorted(item["severity"] for item in result["findings"]))
        self.assertEqual(2, result["score"])
        self.assertEqual("clear", result["verdict"])

    def test_zero_severity_repeat_does_not_force_review(self):
        text = "不是记录问题，而是交接问题；不是个人疏忽，而是名单过期。"
        result = audit.audit_text(text, profile="general")
        contrasts = [item for item in result["findings"] if item["rule"] == "binary_contrast"]
        self.assertEqual([0, 0], [item["severity"] for item in contrasts])
        self.assertEqual(2, result["finding_count"])
        self.assertEqual(0, result["score"])
        self.assertEqual(0, result["blocker_count"])
        self.assertEqual("clear", result["verdict"])

    def test_skill_example_after_is_clear_under_academic_profile(self):
        text = "该缓存策略的核心在于保持版本戳单调递增。故障源于服务重启后把版本戳恢复成了 0。修复时先恢复持久化版本戳，再重新开放流量。"
        result = audit.audit_text(text, profile="academic")
        self.assertEqual(3, result["score"])
        self.assertEqual("clear", result["verdict"])
        self.assertEqual(
            [("essence_claim", 1), ("staged_sequence", 2)],
            sorted((item["rule"], item["severity"]) for item in result["findings"]),
        )


# Severities from P2-11. general / social / academic / sop share one column.
PATTERN_SEVERITY = {
    "hollow_question": {
        "general": 3,
        "social": 3,
        "academic": 3,
        "sop": 3,
        "fiction": 2,
        "email": 3,
        "editorial": 3,
    },
    "slogan_ending": {
        "general": 2,
        "social": 2,
        "academic": 2,
        "sop": 2,
        "fiction": 1,
        "email": 2,
        "editorial": 1,
    },
    "vivid_label": {
        "general": 1,
        "social": 1,
        "academic": 1,
        "sop": 1,
        "fiction": 0,
        "email": 1,
        "editorial": 1,
    },
    "metaphor_stack": {
        "general": 2,
        "social": 2,
        "academic": 2,
        "sop": 2,
        "fiction": 0,
        "email": 2,
        "editorial": 1,
    },
    "ellipsis_list": {
        "general": 1,
        "social": 1,
        "academic": 1,
        "sop": 1,
        "fiction": 0,
        "email": 1,
        "editorial": 0,
    },
    "four_char_chain": {
        "general": 1,
        "social": 1,
        "academic": 1,
        "sop": 1,
        "fiction": 0,
        "email": 1,
        "editorial": 0,
    },
}

PATTERN_SAMPLES = {
    "hollow_question": "加装电梯为什么难？这是一个值得深思的问题。",
    "slogan_ending": "城市更新必将更加美好。",
    "vivid_label": "这是民生工程的生动写照。",
    "metaphor_stack": "他把工期说成“加速器”，把预算说成“催化剂”。",
    "ellipsis_list": "已完成加装 1260 部，惠及居民 3.8 万户……",
    "four_char_chain": "甲乙丙丁、戊己庚辛、壬癸子丑、寅卯辰巳。",
}

JSON_TOP_KEYS = {"schema_version", "profile", "verdict_semantics", "results"}
JSON_RESULT_KEYS = {"profile", "score", "finding_count", "blocker_count", "verdict", "findings"}
JSON_FINDING_KEYS = {"rule", "label", "severity", "line", "match", "excerpt"}


def severities_for(result, rule_id):
    return [item["severity"] for item in result["findings"] if item["rule"] == rule_id]


class AuditEmailEditorialProfileTests(unittest.TestCase):
    def test_profiles_include_email_and_editorial(self):
        self.assertEqual(
            ("general", "social", "academic", "fiction", "sop", "email", "editorial"),
            audit.PROFILES,
        )

    def test_new_pattern_severities_follow_the_profile_table(self):
        self.assertEqual(set(PATTERN_SEVERITY), set(PATTERN_SAMPLES))
        for rule_id, by_profile in PATTERN_SEVERITY.items():
            self.assertEqual(set(audit.PROFILES), set(by_profile))
            for profile, expected in by_profile.items():
                with self.subTest(rule=rule_id, profile=profile):
                    result = audit.audit_text(PATTERN_SAMPLES[rule_id], profile=profile)
                    self.assertEqual([expected], severities_for(result, rule_id))
                    self.assertEqual(expected, result["score"])
                    self.assertEqual("clear", result["verdict"])

    def test_hollow_question_prefixes_and_exemptions(self):
        prefixes = ("这是一个值得", "这值得我们", "值得我们深思", "这个问题值得")
        for prefix in prefixes:
            text = f"费用为什么分不开？{prefix}再议。"
            with self.subTest(prefix=prefix):
                result = audit.audit_text(text, profile="general")
                self.assertEqual([3], severities_for(result, "hollow_question"))
                self.assertIn(prefix, result["findings"][0]["match"])

        not_next = audit.audit_text(
            "费用为什么分不开？有人说这是一个值得深思的问题。",
            profile="general",
        )
        self.assertEqual([], severities_for(not_next, "hollow_question"))

        quoted = audit.audit_text(
            "笔记里写着：“费用为什么分不开？这是一个值得深思的问题。”旁边没有别的句子。",
            profile="general",
        )
        self.assertEqual([], severities_for(quoted, "hollow_question"))

        across_blank = audit.audit_text(
            "费用为什么分不开？\n\n这是一个值得再看的分歧。",
            profile="editorial",
        )
        hits = [item for item in across_blank["findings"] if item["rule"] == "hollow_question"]
        self.assertEqual([(3, 3)], [(item["severity"], item["line"]) for item in hits])

    def test_slogan_ending_only_checks_the_last_paragraph(self):
        earlier = audit.audit_text(
            "城市更新必将更加美好。\n\n接下来核对名单。",
            profile="general",
        )
        self.assertEqual([], severities_for(earlier, "slogan_ending"))

        call = audit.audit_text(
            "前面还有一句。\n\n让我们把名单再对一遍。",
            profile="editorial",
        )
        hits = [item for item in call["findings"] if item["rule"] == "slogan_ending"]
        self.assertEqual([(1, 3)], [(item["severity"], item["line"]) for item in hits])
        self.assertEqual("让我们", hits[0]["match"])

        not_at_start = audit.audit_text("请让我们出发。", profile="general")
        self.assertEqual([], severities_for(not_at_start, "slogan_ending"))

        both = audit.audit_text(
            "只要我们久久为功，城市更新必将更加美好，人民群众的幸福感定会更加充盈！",
            profile="editorial",
        )
        hits = [item for item in both["findings"] if item["rule"] == "slogan_ending"]
        self.assertEqual(1, len(hits))
        self.assertEqual(1, hits[0]["severity"])
        self.assertEqual(1, both["score"])
        self.assertEqual("clear", both["verdict"])

    def test_slogan_ending_treats_single_newline_sentence_lines_as_paragraphs(self):
        not_at_end = audit.audit_text(
            "城市更新必将更加美好。\n接下来核对名单，周五前回复。",
            profile="general",
        )
        self.assertEqual([], severities_for(not_at_end, "slogan_ending"))
        self.assertEqual("clear", not_at_end["verdict"])

        call = audit.audit_text(
            "前面还有一句。\n让我们把名单再对一遍。",
            profile="editorial",
        )
        hits = [item for item in call["findings"] if item["rule"] == "slogan_ending"]
        self.assertEqual([(1, 2)], [(item["severity"], item["line"]) for item in hits])
        self.assertEqual("让我们", hits[0]["match"])
        self.assertEqual("clear", call["verdict"])

    def test_slogan_gap_stays_inside_one_sentence_and_at_most_20_characters(self):
        within = audit.audit_text("必将" + ("再" * 20) + "更加光明。", profile="general")
        self.assertEqual([2], severities_for(within, "slogan_ending"))
        self.assertEqual("clear", within["verdict"])
        beyond = audit.audit_text("必将" + ("再" * 21) + "更加光明。", profile="general")
        self.assertEqual([], severities_for(beyond, "slogan_ending"))
        crossed = audit.audit_text("必将。更加美好。", profile="general")
        self.assertEqual([], severities_for(crossed, "slogan_ending"))

    def test_vivid_label_matches_the_listed_words_only(self):
        for word in ("写照", "诠释", "缩影", "注脚", "实践", "样本", "篇章"):
            text = f"这是一次生动{word}。"
            with self.subTest(word=word):
                result = audit.audit_text(text, profile="email")
                self.assertEqual([1], severities_for(result, "vivid_label"))
        unrelated = audit.audit_text("这是一次生动的说明。", profile="general")
        self.assertEqual([], severities_for(unrelated, "vivid_label"))
        quoted = audit.audit_text("他引用了“生动写照”四个字。", profile="general")
        self.assertEqual([], severities_for(quoted, "vivid_label"))

    def test_metaphor_stack_needs_two_quoted_words_in_one_sentence(self):
        one = audit.audit_text("他把工期说成“加速器”。", profile="general")
        self.assertEqual([], severities_for(one, "metaphor_stack"))
        bare = audit.audit_text("加速器和催化剂都写进了纪要。", profile="general")
        self.assertEqual([], severities_for(bare, "metaphor_stack"))
        split = audit.audit_text("他把工期说成“加速器”。预算则是“催化剂”。", profile="general")
        self.assertEqual([], severities_for(split, "metaphor_stack"))
        three = audit.audit_text(
            "工期是“加速器”，预算是“催化剂”，考核是“试金石”。",
            profile="editorial",
        )
        hits = [item for item in three["findings"] if item["rule"] == "metaphor_stack"]
        self.assertEqual([1], [item["severity"] for item in hits])
        self.assertEqual(1, three["score"])
        for word in ("加速器", "催化剂", "试金石"):
            self.assertIn(word, hits[0]["match"])
        words = ("加速器", "催化剂", "试金石", "压舱石", "稳定器", "蓄水池", "助推器", "新引擎")
        for left, right in zip(words, words[1:]):
            paired = audit.audit_text(f"甲是“{left}”，乙是“{right}”。", profile="sop")
            self.assertEqual([2], severities_for(paired, "metaphor_stack"), f"{left}+{right}")
        corners = audit.audit_text("工期是「加速器」，预算是「催化剂」。", profile="general")
        self.assertEqual([2], severities_for(corners, "metaphor_stack"))

    def test_ellipsis_list_boundaries(self):
        short = audit.audit_text("已完成，一二……", profile="general")
        self.assertEqual([], severities_for(short, "ellipsis_list"))
        exact = audit.audit_text("已完成，一二三四……", profile="email")
        self.assertEqual([1], severities_for(exact, "ellipsis_list"))
        nearest = audit.audit_text(
            "今年先做甲，再做乙，已完成加装 1260 部，惠及居民 3.8 万户……",
            profile="general",
        )
        ellipses = [item for item in nearest["findings"] if item["rule"] == "ellipsis_list"]
        self.assertEqual(["，惠及居民 3.8 万户……"], [item["match"] for item in ellipses])
        quoted = audit.audit_text("他说：“已完成，惠及居民很多户……”", profile="general")
        self.assertEqual([], severities_for(quoted, "ellipsis_list"))
        editorial = audit.audit_text("已完成加装 1260 部，惠及居民 3.8 万户……", profile="editorial")
        self.assertEqual([0], severities_for(editorial, "ellipsis_list"))
        self.assertEqual(0, editorial["score"])
        self.assertEqual("clear", editorial["verdict"])

    def test_four_char_chain_counts_four_or_more_and_keeps_listed_terms(self):
        three = audit.audit_text("甲乙丙丁、戊己庚辛、壬癸子丑。", profile="general")
        self.assertEqual([], severities_for(three, "four_char_chain"))
        five = audit.audit_text(
            "甲乙丙丁、戊己庚辛、壬癸子丑、寅卯辰巳、子丑寅卯。",
            profile="general",
        )
        self.assertEqual([1], severities_for(five, "four_char_chain"))
        lead_in = audit.audit_text("要统筹规划、科学布局、精准施策、久久为功。", profile="general")
        lead_hits = [item for item in lead_in["findings"] if item["rule"] == "four_char_chain"]
        self.assertEqual(
            ["统筹规划、科学布局、精准施策、久久为功"],
            [item["match"] for item in lead_hits],
        )
        trimmed = audit.audit_text(
            "资料收集、分类整理、限时审核、结果公示、跟踪回访机制。",
            profile="general",
        )
        trimmed_hits = [item for item in trimmed["findings"] if item["rule"] == "four_char_chain"]
        self.assertEqual(
            ["资料收集、分类整理、限时审核、结果公示"],
            [item["match"] for item in trimmed_hits],
        )
        for fragment in (
            "到车间去、到仓库去、到码头去、到田间地头去",
            "到车间去、到仓库去、到码头去、到田间地头去。",
        ):
            with self.subTest(fragment=fragment):
                result = audit.audit_text(fragment, profile="general")
                self.assertEqual([], severities_for(result, "four_char_chain"))
        quoted = audit.audit_text(
            "他说：“甲乙丙丁、戊己庚辛、壬癸子丑、寅卯辰巳”。",
            profile="general",
        )
        self.assertEqual([], severities_for(quoted, "four_char_chain"))
        titled = audit.audit_text(
            "详见《甲乙丙丁、戊己庚辛、壬癸子丑、寅卯辰巳》。",
            profile="general",
        )
        self.assertEqual([], severities_for(titled, "four_char_chain"))

        chain = "甲乙丙丁、戊己庚辛、壬癸子丑、寅卯辰巳。"
        broken = audit.audit_text(chain, profile="general", keep_terms=("戊己庚辛",))
        self.assertEqual([], severities_for(broken, "four_char_chain"))
        whole = audit.audit_text(chain, profile="editorial", keep_terms=("甲乙丙丁、戊己庚辛、壬癸子丑、寅卯辰巳",))
        self.assertEqual([], severities_for(whole, "four_char_chain"))
        untouched = audit.audit_text(chain, profile="fiction", keep_terms=("并不在句中",))
        self.assertEqual([0], severities_for(untouched, "four_char_chain"))

    def test_keep_terms_exempt_contained_findings_and_leave_json_fields_unchanged(self):
        text = "这是民生工程的生动写照。总的来说，步骤没变。"
        without = audit.audit_text(text, profile="general")
        self.assertEqual([1], severities_for(without, "vivid_label"))
        self.assertEqual([2], severities_for(without, "lecture_marker"))
        exempted = audit.audit_text(text, profile="general", keep_terms=("  生动写照  ",))
        self.assertEqual([], severities_for(exempted, "vivid_label"))
        self.assertEqual([2], severities_for(exempted, "lecture_marker"))

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            terms = root / "terms.txt"
            terms.write_text("# 甲乙丙丁\n\n  戊己庚辛  \n", encoding="utf-8")
            draft = root / "draft.md"
            draft.write_text(
                "甲乙丙丁、戊己庚辛、壬癸子丑、寅卯辰巳。这是生动写照。\n",
                encoding="utf-8",
            )
            missing = root / "missing.txt"
            kept = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT_PATH),
                    str(draft),
                    "--json",
                    "--profile",
                    "general",
                    "--keep-terms",
                    str(terms),
                ],
                check=False,
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
            plain = subprocess.run(
                [sys.executable, str(SCRIPT_PATH), str(draft), "--json", "--profile", "general"],
                check=False,
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
            absent = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT_PATH),
                    "--stdin",
                    "--keep-terms",
                    str(missing),
                ],
                input="普通句子。",
                check=False,
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
        self.assertEqual(0, kept.returncode, kept.stderr)
        self.assertEqual(0, plain.returncode, plain.stderr)
        kept_payload = json.loads(kept.stdout)
        plain_payload = json.loads(plain.stdout)
        self.assertEqual(1, kept_payload["schema_version"])
        self.assertEqual(JSON_TOP_KEYS, set(kept_payload))
        self.assertEqual(JSON_TOP_KEYS, set(plain_payload))
        kept_result = next(iter(kept_payload["results"].values()))
        plain_result = next(iter(plain_payload["results"].values()))
        self.assertEqual(JSON_RESULT_KEYS, set(kept_result))
        self.assertEqual(JSON_RESULT_KEYS, set(plain_result))
        self.assertEqual("clear", kept_result["verdict"])
        self.assertEqual(1, kept_result["score"])
        self.assertEqual("clear", plain_result["verdict"])
        self.assertEqual(2, plain_result["score"])
        self.assertNotIn("four_char_chain", rules_of(kept_result))
        self.assertIn("four_char_chain", rules_of(plain_result))
        self.assertIn("vivid_label", rules_of(kept_result))
        self.assertEqual(JSON_FINDING_KEYS, set(kept_result["findings"][0]))
        self.assertEqual(2, absent.returncode)
        self.assertIn("not found", absent.stderr.lower())
        self.assertNotIn("Traceback", absent.stderr)

    def test_email_profile_lowers_sequence_and_closing_question_only(self):
        sequence = "先关闭总闸，再拆下外壳。"
        question = "你觉得这个方案怎么样？"
        for profile, sequence_severity, question_severity in (
            ("general", 2, 3),
            ("email", 1, 1),
            ("editorial", 2, 3),
        ):
            with self.subTest(profile=profile):
                sequenced = audit.audit_text(sequence, profile=profile)
                asked = audit.audit_text(question, profile=profile)
                self.assertEqual([sequence_severity], severities_for(sequenced, "staged_sequence"))
                self.assertEqual([question_severity], severities_for(asked, "ending_engagement_question"))

        fixture_dir = SKILL_ROOT / "tests" / "fixtures"
        before = audit.audit_text(
            (fixture_dir / "email_comment_before.md").read_text(encoding="utf-8"),
            profile="email",
        )
        after = audit.audit_text(
            (fixture_dir / "email_comment_after.md").read_text(encoding="utf-8"),
            profile="email",
        )
        self.assertEqual("review", before["verdict"])
        self.assertEqual("clear", after["verdict"])
        self.assertEqual([1], severities_for(after, "staged_sequence"))

    def test_editorial_profile_lowers_enumeration_and_template_colon(self):
        # Two non-overlapping hits: one match consumes 首先…其次, so a second
        # pair has to sit in its own sentence to be counted again.
        enumeration = "首先说明背景，其次公布结果。一方面保留记录，另一方面核对名单。"
        single = "首先要凝聚共识，其次要完善机制，最后要强化保障。"
        template = "概念：甲\n原因：乙\n结论：丙\n"
        general_enum = audit.audit_text(enumeration, profile="general")
        editorial_enum = audit.audit_text(enumeration, profile="editorial")
        self.assertEqual([2, 2], severities_for(general_enum, "rigid_enumeration"))
        self.assertEqual("review", general_enum["verdict"])
        self.assertEqual([0, 0], severities_for(editorial_enum, "rigid_enumeration"))
        self.assertEqual(0, editorial_enum["score"])
        self.assertEqual("clear", editorial_enum["verdict"])
        general_single = audit.audit_text(single, profile="general")
        editorial_single = audit.audit_text(single, profile="editorial")
        self.assertEqual([2], severities_for(general_single, "rigid_enumeration"))
        self.assertEqual([0], severities_for(editorial_single, "rigid_enumeration"))

        general_template = audit.audit_text(template, profile="general")
        editorial_template = audit.audit_text(template, profile="editorial")
        self.assertEqual([2], severities_for(general_template, "template_colon"))
        self.assertEqual([0], severities_for(editorial_template, "template_colon"))

    def test_binary_contrast_stays_listed_at_zero_for_owner_decisions(self):
        additive = "这不只是记录，更是复盘。"
        definitional = "何谓好用？不是功能多，而是三步之内能完成报销。"
        for profile in audit.PROFILES:
            with self.subTest(profile=profile):
                added = audit.audit_text(additive, profile=profile)
                defined = audit.audit_text(definitional, profile=profile)
                self.assertEqual(["binary_contrast"], [item["rule"] for item in added["findings"]])
                self.assertEqual([0], severities_for(added, "binary_contrast"))
                self.assertNotIn("additive_contrast", rules_of(added))
                self.assertEqual([0], severities_for(defined, "binary_contrast"))
                self.assertEqual([], severities_for(defined, "hollow_question"))
                self.assertEqual(0, defined["score"])
                self.assertEqual("clear", defined["verdict"])

    def test_editorial_fixture_reviews_before_and_clears_after(self):
        fixture_dir = SKILL_ROOT / "tests" / "fixtures"
        before = audit.audit_text(
            (fixture_dir / "editorial_commentary_before.md").read_text(encoding="utf-8"),
            profile="editorial",
        )
        after = audit.audit_text(
            (fixture_dir / "editorial_commentary_after.md").read_text(encoding="utf-8"),
            profile="editorial",
        )
        scored = sorted(
            (item["rule"], item["severity"]) for item in before["findings"] if item["severity"] > 0
        )
        self.assertEqual(
            [("hollow_question", 3), ("slogan_ending", 1), ("vivid_label", 1)],
            scored,
        )
        self.assertEqual(5, before["score"])
        self.assertEqual("review", before["verdict"])
        for rule_id in ("binary_contrast", "rigid_enumeration", "ellipsis_list"):
            self.assertTrue(severities_for(before, rule_id))
            self.assertTrue(all(item == 0 for item in severities_for(before, rule_id)))
        hollow = [item for item in before["findings"] if item["rule"] == "hollow_question"]
        slogan = [item for item in before["findings"] if item["rule"] == "slogan_ending"]
        self.assertEqual([7], [item["line"] for item in hollow])
        self.assertEqual([13], [item["line"] for item in slogan])

        self.assertEqual([], [item for item in after["findings"] if item["severity"] > 0])
        self.assertEqual(0, after["score"])
        self.assertEqual("clear", after["verdict"])
        self.assertEqual([0], severities_for(after, "ellipsis_list"))
        self.assertEqual(1, after["finding_count"])
        general_after = audit.audit_text(
            (fixture_dir / "editorial_commentary_after.md").read_text(encoding="utf-8"),
            profile="general",
        )
        self.assertEqual([1], severities_for(general_after, "ellipsis_list"))
        self.assertEqual(1, general_after["score"])
        self.assertEqual("clear", general_after["verdict"])
        self.assertEqual(1, general_after["finding_count"])


if __name__ == "__main__":
    unittest.main()
