#!/usr/bin/env python3
"""End-to-end tests with a local fake gateway; no paid API calls."""

from __future__ import annotations

import json
import datetime as dt
import os
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import threading
import unittest
import zipfile
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


SCRIPT = Path(__file__).with_name("mangyun_intelligence.py")
IDENTITY = json.loads(Path(__file__).with_name('client_identity.json').read_text(encoding='utf-8'))
EXPECTED_AGENT = 'wechat-intelligence/' + IDENTITY['version'] + ' (source=' + IDENTITY['channel'] + ')'


class GatewayHandler(BaseHTTPRequestHandler):
    # 每个账号(seed标识)对应一组文章；首次调用返回基线，之后返回增量(含同主题跨号)
    history_calls = 0

    def log_message(self, *_args):
        pass

    def do_GET(self):
        assert self.headers.get("User-Agent") == EXPECTED_AGENT
        if self.path.startswith(("/api/v1/public/products", "/api/v1/products")):
            self.reply({"code": "OK", "data": {"items": [
                {"slug": "wechat-native-account-articles", "priceMicros": 35000},
                {"slug": "wechat-native-article-content", "priceMicros": 21000},
            ]}})
            return
        self.send_error(404)

    def do_POST(self):
        assert self.headers.get("User-Agent") == EXPECTED_AGENT
        length = int(self.headers.get("Content-Length", "0"))
        body = json.loads(self.rfile.read(length) or b"{}")
        if self.path.endswith("/accounts/articles"):
            url = body.get("url", "")
            account_key = "seed2" if "seed2" in url else "seed"
            first = type(self).history_calls % 2 == 0
            type(self).history_calls += 1
            if first:
                items = self._baseline_items(account_key)
            else:
                items = self._incremental_items(account_key)
            self.reply({
                "requestId": f"history-{account_key}-{type(self).history_calls}", "code": "OK", "balance": 99.9,
                "consumption": 0.035,
                "data": {"account": {"accountName": "测试行业号" if account_key == "seed" else "竞品号",
                                     "originalId": "gh_aaaaaaaaaaaa" if account_key == "seed" else "gh_bbbbbbbbbbbb"},
                "items": items, "offset": body.get("offset", 0), "nextOffset": 20, "hasMore": False},
            })
            return
        if self.path.endswith("/articles/content"):
            self.reply({
                "requestId": "content-1", "code": "OK", "balance": 99.8, "consumption": 0.021,
                "data": {"format": "text", "content": "行业进入新阶段。样本增长 20%，但该数据仍需核验。"},
            })
            return
        self.send_error(404)

    def _baseline_items(self, account_key):
        if account_key == "seed2":
            return [article("202", "竞品号行业趋势分析"), article("201", "竞品号第二篇")]
        return [article("102", "第二篇"), article("101", "第一篇")]

    def _incremental_items(self, account_key):
        # 增量返回一篇；测试行业号的增量是"新的行业变化"(与竞品同主题)
        if account_key == "seed2":
            return [article("203", "竞品号新的行业变化"), article("202", "竞品号行业趋势分析")]
        return [article("103", "新的行业变化"), article("102", "第二篇")]

    def reply(self, value):
        data = json.dumps(value, ensure_ascii=False).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)


def article(mid: str, title: str):
    now = dt.datetime.now(dt.timezone.utc)
    return {
        "url": f"https://mp.weixin.qq.com/s?__biz=MzTest&mid={mid}&idx=1&sn=sn{mid}",
        "title": title, "digest": title + "摘要", "author": "作者", "publishTime": now.isoformat(),
        "publishTimestamp": int(now.timestamp()), "biz": "MzTest", "mid": mid, "idx": "1", "sn": f"sn{mid}",
        "contentType": "article",
    }


class IntelligenceE2ETest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), GatewayHandler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()

    def setUp(self):
        self.connections = []
        GatewayHandler.history_calls = 0
        self.temp = tempfile.TemporaryDirectory()
        self.workspace = Path(self.temp.name) / "workspace"
        self.env = os.environ.copy()
        self.env["MANGYUN_API_KEY"] = "test-key-never-persisted"
        self.env["MANGYUN_INTEL_TEST_ALLOW_HTTP"] = "1"
        self.env["PYTHONUTF8"] = "1"
        self.exec_cli("init")
        config_path = self.workspace / "config.json"
        config = json.loads(config_path.read_text(encoding="utf-8"))
        config["baseUrl"] = f"http://127.0.0.1:{self.server.server_port}"
        config_path.write_text(json.dumps(config, ensure_ascii=False, indent=2), encoding="utf-8")
        self.exec_cli("account", "add", "--name", "测试行业号", "--url", "https://mp.weixin.qq.com/s/seed", "--group", "竞品")

    def tearDown(self):
        for connection in self.connections:
            connection.close()
        keep = os.environ.get("MANGYUN_INTEL_TEST_OUTPUT", "").strip()
        if keep and self.workspace.exists():
            shutil.copytree(self.workspace, Path(keep), dirs_exist_ok=True)
        self.temp.cleanup()

    def exec_cli(self, *args: str, expect: int = 0):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--workspace", str(self.workspace), *args],
            env=self.env, text=True, encoding="utf-8", capture_output=True,
        )
        if result.returncode != expect:
            self.fail(f"command {args} returned {result.returncode}\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}")
        return result

    def connection(self):
        conn = sqlite3.connect(self.workspace / "data" / "intelligence.db")
        self.connections.append(conn)
        conn.row_factory = sqlite3.Row
        return conn

    def test_incremental_analysis_dashboard_and_excel(self):
        first = self.exec_cli("scan")
        self.assertIn("基线新增 2 篇", first.stdout)
        with self.connection() as conn:
            self.assertEqual(conn.execute("SELECT COUNT(*) FROM articles").fetchone()[0], 2)
            self.assertEqual(conn.execute("SELECT COUNT(*) FROM articles WHERE analysis_status='needs_content'").fetchone()[0], 0)

        second = self.exec_cli("scan", "--force")
        self.assertIn("增量新增 1 篇", second.stdout)
        with self.connection() as conn:
            self.assertEqual(conn.execute("SELECT COUNT(*) FROM articles").fetchone()[0], 3)
            self.assertEqual(conn.execute("SELECT COUNT(*) FROM articles WHERE analysis_status='needs_content'").fetchone()[0], 1)

        fetched = self.exec_cli("fetch-content")
        self.assertIn("实际费用 ¥0.021", fetched.stdout)
        queue_path = self.workspace / "output" / "analysis-queue.json"
        self.exec_cli("make-analysis-queue")
        queue = json.loads(queue_path.read_text(encoding="utf-8"))
        self.assertEqual(len(queue["items"]), 1)
        article_id = queue["items"][0]["articleId"]
        analysis_path = self.workspace / "analysis-result.json"
        analysis_path.write_text(json.dumps({"items": [{
            "articleId": article_id, "summary": "行业出现可观察的新变化。", "keyPoints": ["进入新阶段"],
            "keyData": ["文中称样本增长 20%"], "logic": "先提出变化，再以样本数据支撑。", "topics": ["行业趋势"],
            "sentiment": "neutral", "importance": 4, "changeNotes": "暂无足够历史分析用于纵向对比。",
            "risks": ["20% 数据缺少外部核验"],
        }]}, ensure_ascii=False), encoding="utf-8")
        self.exec_cli("import-analysis", "--input", str(analysis_path))
        self.exec_cli("build-dashboard")
        self.exec_cli("export")

        dashboard = (self.workspace / "output" / "dashboard.html").read_text(encoding="utf-8")
        self.assertIn("新的行业变化", dashboard)
        self.assertIn("行业趋势", dashboard)
        self.assertIn('"todayCount":3', dashboard)
        workbook = self.workspace / "output" / "公众号情报数据.xlsx"
        self.assertTrue(workbook.exists())
        with zipfile.ZipFile(workbook) as archive:
            self.assertEqual(archive.testzip(), None)
            workbook_xml = archive.read("xl/workbook.xml").decode("utf-8")
            self.assertIn("公众号汇总", workbook_xml)
            self.assertIn("测试行业号", workbook_xml)
            self.assertIn("跨号话题对比", workbook_xml)
            self.assertIn("每日摘要", workbook_xml)
            self.assertIn("主题追踪", workbook_xml)

        status = self.exec_cli("status")
        self.assertIn("实际费用：¥0.091", status.stdout)
        combined = "".join(path.read_text(encoding="utf-8", errors="ignore") for path in self.workspace.rglob("*.json"))
        self.assertNotIn("test-key-never-persisted", combined)

    def _import_two_accounts(self):
        """添加第二个公众号，扫描两号、获取正文、导入含新字段的分析结果。"""
        self.exec_cli("account", "add", "--name", "竞品号", "--url", "https://mp.weixin.qq.com/s/seed2", "--group", "竞品")
        # 两账号基线扫描
        self.exec_cli("scan")
        self.exec_cli("scan", "--force")
        self.exec_cli("fetch-content")
        # 队列应包含待分析文章
        self.exec_cli("make-analysis-queue")
        queue_path = self.workspace / "output" / "analysis-queue.json"
        queue = json.loads(queue_path.read_text(encoding="utf-8"))
        items = queue["items"]
        self.assertGreater(len(items), 0)
        # 检查跨账号上下文（任一 item 的 crossAccountContext 可能为空，但 accountKeywords 字段必须存在）
        for item in items:
            self.assertIn("crossAccountContext", item)
            self.assertIn("accountKeywords", item)
        # 对每个待分析文章写含新字段的分析结果（两号同主题"行业趋势"，立场不同）
        analysis_items = []
        for item in items:
            analysis_items.append({
                "articleId": item["articleId"],
                "summary": "行业进入可观察的新阶段，样本增长 20%。",
                "keyPoints": ["进入新阶段"], "keyData": ["样本增长 20%"],
                "logic": "先提出变化，再以样本数据支撑。", "topics": ["行业趋势"],
                "sentiment": "neutral", "importance": 4,
                "changeNotes": "较同号前文有新增行业信号。",
                "risks": ["20% 数据缺少外部核验"],
                "stance": "support" if item["account"] == "竞品号" else "question",
                "angle": "从竞品格局切入" if item["account"] == "竞品号" else "从行业风险角度切入",
                "relatedAccounts": [{"account": "竞品号" if item["account"] != "竞品号" else "测试行业号",
                                     "stance": "support" if item["account"] != "竞品号" else "question",
                                     "angle": "竞品偏乐观" if item["account"] != "竞品号" else "行业号偏谨慎"}],
                "keywordsHit": ["行业"],
            })
        analysis_path = self.workspace / "analysis-result.json"
        analysis_path.write_text(json.dumps({"items": analysis_items}, ensure_ascii=False), encoding="utf-8")
        self.exec_cli("import-analysis", "--input", str(analysis_path))

    def test_multi_account_cross_topic_analysis_and_brief(self):
        self._import_two_accounts()
        # make-brief：重建主题分组 + 每日摘要 + AI 收尾队列
        self.exec_cli("make-brief")
        with self.connection() as conn:
            topic_count = conn.execute("SELECT COUNT(*) FROM articles WHERE analysis_status='analyzed'").fetchone()[0]
            self.assertGreater(topic_count, 0)
            tg_count = conn.execute("SELECT COUNT(*) FROM topic_groups").fetchone()[0]
            self.assertGreater(tg_count, 0)
            brief_count = conn.execute("SELECT COUNT(*) FROM daily_briefs").fetchone()[0]
            self.assertGreater(brief_count, 0)
        # analyze-topics 检索指定主题
        result = self.exec_cli("analyze-topics", "--topic", "行业趋势")
        self.assertIn("行业趋势", result.stdout)
        # build-dashboard 应包含新板块
        self.exec_cli("build-dashboard")
        dashboard = (self.workspace / "output" / "dashboard.html").read_text(encoding="utf-8")
        self.assertIn("跨号话题对比", dashboard)
        self.assertIn("主题追踪", dashboard)
        self.assertIn("每日摘要", dashboard)
        self.assertIn("公众号立场画像", dashboard)
        # export 应包含新 sheet
        self.exec_cli("export")
        workbook = self.workspace / "output" / "公众号情报数据.xlsx"
        with zipfile.ZipFile(workbook) as archive:
            workbook_xml = archive.read("xl/workbook.xml").decode("utf-8")
            self.assertIn("跨号话题对比", workbook_xml)
            self.assertIn("主题追踪", workbook_xml)
            self.assertIn("每日摘要", workbook_xml)

    def test_schema_backward_compatibility(self):
        # 旧格式（无新字段）分析结果应能正常导入；用增量文章测试（基线默认跳过正文）
        self.exec_cli("scan")
        self.exec_cli("scan", "--force")
        self.exec_cli("fetch-content")
        self.exec_cli("make-analysis-queue")
        queue = json.loads((self.workspace / "output" / "analysis-queue.json").read_text(encoding="utf-8"))
        if not queue["items"]:
            self.skipTest("无待分析文章")
        article_id = queue["items"][0]["articleId"]
        old_analysis = {"items": [{
            "articleId": article_id, "summary": "旧格式分析。", "keyPoints": ["旧观点"],
            "keyData": [], "logic": "旧论证。", "topics": ["行业趋势"], "sentiment": "neutral",
            "importance": 2, "changeNotes": "", "risks": [],
        }]}
        analysis_path = self.workspace / "old-analysis.json"
        analysis_path.write_text(json.dumps(old_analysis, ensure_ascii=False), encoding="utf-8")
        self.exec_cli("import-analysis", "--input", str(analysis_path))
        with self.connection() as conn:
            row = conn.execute("SELECT stance,related_accounts_json,keywords_hit_json FROM articles WHERE article_id=?",
                               (article_id,)).fetchone()
            self.assertEqual(row["stance"], "informational")
            self.assertEqual(row["related_accounts_json"], "[]")
            self.assertEqual(row["keywords_hit_json"], "[]")

    def test_make_brief_rebuild_idempotent(self):
        self._import_two_accounts()
        self.exec_cli("make-brief", "--rebuild")
        with self.connection() as conn:
            first = conn.execute("SELECT COUNT(*),SUM(article_count) FROM topic_groups").fetchone()
        self.exec_cli("make-brief", "--rebuild")
        with self.connection() as conn:
            second = conn.execute("SELECT COUNT(*),SUM(article_count) FROM topic_groups").fetchone()
        self.assertEqual(first[0], second[0])
        self.assertEqual(first[1], second[1])


if __name__ == "__main__":
    unittest.main(verbosity=2)
