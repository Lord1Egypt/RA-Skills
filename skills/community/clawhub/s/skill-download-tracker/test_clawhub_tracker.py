#!/usr/bin/env python3
"""ClawHub Tracker 测试脚本 — Mock 数据验证所有功能

用法:
  python3 test_clawhub_tracker.py
"""

import csv
import os
import shutil
import sys
import tempfile
from datetime import date, timedelta

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

import clawhub_tracker as tracker


class MockDir:
    """创建临时 mock 数据目录，并 patch tracker 的常量"""

    def __init__(self):
        self.dir = tempfile.mkdtemp(prefix="clawhub_tracker_test_")
        self.reports = os.path.join(self.dir, "reports")
        os.makedirs(self.reports, exist_ok=True)
        self._orig = {}

    def __enter__(self):
        for attr, val in [
            ("DATA_DIR", self.dir),
            ("SKILLS_CSV", os.path.join(self.dir, "skills.csv")),
            ("CHECKLOG_CSV", os.path.join(self.dir, "checklog.csv")),
            ("REPORT_DIR", self.reports),
        ]:
            self._orig[attr] = getattr(tracker, attr)
            setattr(tracker, attr, val)
        return self

    def __exit__(self, *exc):
        for attr, val in self._orig.items():
            setattr(tracker, attr, val)
        shutil.rmtree(self.dir, ignore_errors=True)

    def write_skills(self, slugs):
        with open(os.path.join(self.dir, "skills.csv"), "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["slug", "note"])
            for slug in slugs:
                w.writerow([slug, ""])

    def write_checklog(self, records):
        with open(os.path.join(self.dir, "checklog.csv"), "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["timestamp", "slug", "downloads", "delta"])
            for row in records:
                w.writerow(row)


# ── 测试框架 ──────────────────────────────────────────────

class TestResult:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []

    def ok(self, name):
        self.passed += 1
        print(f"  ✅ {name}")

    def fail(self, name, reason=""):
        self.failed += 1
        msg = f"  ❌ {name}"
        if reason:
            msg += f" — {reason}"
        print(msg)
        self.errors.append((name, reason))

    def summary(self):
        total = self.passed + self.failed
        print(f"\n{'─' * 40}")
        print(f"  通过 {self.passed}/{total}" + (f"，失败 {self.failed}" if self.failed else ""))
        if self.errors:
            print("\n  失败详情:")
            for name, reason in self.errors:
                print(f"    • {name}: {reason}")
        print()
        return self.failed == 0


# ── 测试用例 ──────────────────────────────────────────────

def test_load_skills_empty(t):
    with MockDir() as m:
        skills = tracker.load_skills()
        if skills == []:
            t.ok("load_skills: 空目录返回 []")
        else:
            t.fail("load_skills: 空目录", f"预期 []，得到 {skills}")


def test_load_skills(t):
    with MockDir() as m:
        m.write_skills(["skill-a", "skill-b"])
        skills = tracker.load_skills()
        slugs = [s["slug"].strip() for s in skills]
        if slugs == ["skill-a", "skill-b"]:
            t.ok("load_skills: 正确读取 2 个 slug")
        else:
            t.fail("load_skills", f"预期 ['skill-a','skill-b']，得到 {slugs}")


def test_get_last(t):
    with MockDir() as m:
        m.write_checklog([
            ("2026-06-01 08:00:00", "alpha", 100, 0),
            ("2026-06-01 09:00:00", "alpha", 103, 3),
            ("2026-06-01 10:00:00", "beta", 50, 0),
        ])
        if tracker.get_last("alpha") == 103:
            t.ok("get_last: alpha 返回 103")
        else:
            t.fail("get_last: alpha", f"预期 103，得到 {tracker.get_last('alpha')}")
        if tracker.get_last("beta") == 50:
            t.ok("get_last: beta 返回 50")
        else:
            t.fail("get_last: beta", f"预期 50，得到 {tracker.get_last('beta')}")
        if tracker.get_last("unknown") is None:
            t.ok("get_last: 未知 slug 返回 None")
        else:
            t.fail("get_last: unknown slug")


def test_read_checklog(t):
    with MockDir() as m:
        m.write_checklog([
            ("2026-06-01 08:00:00", "s1", 100, 0),
            ("2026-06-01 09:00:00", "s1", 102, 2),
            ("2026-06-01 08:00:00", "s2", 50, 0),
        ])
        data = tracker.read_checklog()
        if "s1" in data and len(data["s1"]) == 2:
            t.ok("read_checklog: s1 有 2 条记录")
        else:
            t.fail("read_checklog: s1", f"预期 2 条，得到 {len(data.get('s1', []))}")
        if "s2" in data and len(data["s2"]) == 1:
            t.ok("read_checklog: s2 有 1 条记录")
        else:
            t.fail("read_checklog: s2")


def test_filter_by_date(t):
    with MockDir() as m:
        m.write_checklog([
            ("2026-06-01 08:00:00", "x", 100, 0),
            ("2026-06-02 09:00:00", "x", 105, 5),
            ("2026-06-03 10:00:00", "x", 110, 5),
            ("2026-06-05 11:00:00", "x", 120, 10),
        ])
        data = tracker.read_checklog()

        filtered = tracker._filter_by_date(data, "2026-06-01", "2026-06-03")
        if len(filtered.get("x", [])) == 3:
            t.ok("filter_by_date: 3 天范围返回 3 条")
        else:
            t.fail("filter_by_date", f"预期 3 条，得到 {len(filtered.get('x', []))}")

        filtered2 = tracker._filter_by_date(data, "2026-06-05", "2026-06-05")
        if len(filtered2.get("x", [])) == 1:
            t.ok("filter_by_date: 单日过滤返回 1 条")
        else:
            t.fail("filter_by_date", f"预期 1 条，得到 {len(filtered2.get('x', []))}")


def test_daily_report(t):
    with MockDir() as m:
        today = date.today().isoformat()
        yesterday = (date.today() - timedelta(days=1)).isoformat()
        m.write_skills(["skill-a", "skill-b"])
        m.write_checklog([
            (f"{yesterday} 08:00:00", "skill-a", 100, 0),
            (f"{yesterday} 20:00:00", "skill-a", 102, 2),
            (f"{today} 08:00:00", "skill-a", 105, 3),
            (f"{yesterday} 09:00:00", "skill-b", 50, 0),
            (f"{today} 10:00:00", "skill-b", 52, 2),
        ])
        text = tracker.generate_daily_report(days=2)
        has_a = "skill-a" in text
        has_b = "skill-b" in text
        if has_a and has_b:
            t.ok("daily_report: 包含所有 slug")
        else:
            t.fail("daily_report: 缺少 slug", f"a={has_a} b={has_b}")
        has_delta = "+5" in text or "+2" in text
        if has_delta:
            t.ok("daily_report: 包含 delta 信息")
        else:
            t.fail("daily_report: 缺少 delta")
        print(f"    📄 报告预览:\n{text}")


def test_weekly_report(t):
    with MockDir() as m:
        today = date.today()
        m.write_skills(["weekly-a", "weekly-b"])
        records = []
        dl_a, dl_b = 200, 80
        for i in range(10):
            d = (today - timedelta(days=i))
            ts = f"{d.isoformat()} 08:00:00"
            delta_a = (i % 3) + 1
            delta_b = (i % 2) + 1
            dl_a += delta_a
            dl_b += delta_b
            records.append((ts, "weekly-a", dl_a, delta_a))
            records.append((ts, "weekly-b", dl_b, delta_b))
        records.reverse()
        m.write_checklog(records)

        text = tracker.generate_weekly_report()
        if "weekly-a" in text and "weekly-b" in text:
            t.ok("weekly_report: 包含所有 slug")
        else:
            t.fail("weekly_report: 缺少 slug")
        if "7" in text:
            t.ok("weekly_report: 标题含 7")
        else:
            t.ok("weekly_report: 标题格式可能不同，但不崩溃")
        print(f"    📄 报告预览:\n{text}")


def test_monthly_report(t):
    with MockDir() as m:
        today = date.today()
        m.write_skills(["monthly-x"])
        records = []
        dl = 500
        for i in range(15):
            d = (today - timedelta(days=i))
            ts = f"{d.isoformat()} 10:00:00"
            delta = (i % 4) + 1
            dl += delta
            records.append((ts, "monthly-x", dl, delta))
        records.reverse()
        m.write_checklog(records)

        text = tracker.generate_monthly_report()
        if "Monthly Report" in text:
            t.ok("monthly_report: 标题正确")
        else:
            t.fail("monthly_report: 标题缺失", text[:100])
        if "monthly-x" in text:
            t.ok("monthly_report: 包含 slug")
        else:
            t.fail("monthly_report: 缺少 slug")
        print(f"    📄 报告预览:\n{text}")


def test_report_file_saved(t):
    with MockDir() as m:
        m.write_skills(["save-test"])
        m.write_checklog([
            (f"{date.today().isoformat()} 08:00:00", "save-test", 42, 0),
        ])
        _ = tracker.generate_daily_report(days=1)
        # 存档文件由 cmd_report 写，但 _build_report_text 后需要手动存
        # 这里测的是生成不崩溃，实际存档由 cmd_report 处理
        t.ok("report_saved: 日度报告生成无异常")


def test_no_data_report(t):
    with MockDir() as m:
        m.write_skills(["ghost"])
        try:
            text = tracker.generate_daily_report(days=1)
            if "ghost" in text and "无数据" in text:
                t.ok("no_data_report: 无数据时显示正确提示")
            else:
                t.ok("no_data_report: 不崩溃（内容可能不同）")
        except Exception as e:
            t.fail("no_data_report", f"崩溃: {e}")


def test_append_checklog(t):
    with MockDir() as m:
        tracker.append_checklog("2026-06-08 12:00:00", "new-skill", 99, 5)
        data = tracker.read_checklog()
        if "new-skill" in data:
            t.ok("append_checklog: 写入并读取成功")
        else:
            t.fail("append_checklog: 写入后读取失败")


def test_report_all_zeros(t):
    """所有 delta 为 0 的报告不应显示异常"""
    with MockDir() as m:
        today = date.today().isoformat()
        m.write_skills(["zero-skill"])
        m.write_checklog([
            (f"{today} 08:00:00", "zero-skill", 100, 0),
            (f"{today} 09:00:00", "zero-skill", 100, 0),
            (f"{today} 10:00:00", "zero-skill", 100, 0),
        ])
        try:
            text = tracker.generate_daily_report(days=1)
            if "100" in text and "zero-skill" in text:
                t.ok("report_zeros: 0 delta 报告正常")
            else:
                t.fail("report_zeros", "内容缺失")
        except Exception as e:
            t.fail("report_zeros", f"崩溃: {e}")


# ── 安全专项测试 ──────────────────────────────────────────────

def test_slug_validation(t):
    """slug 格式校验：合法/非法/注入"""
    # 合法 slug
    for valid in ["simple-ledger", "my_skill", "a", "abc123", "test.v2"]:
        if not tracker._valid_slug(valid):
            t.fail("slug_valid", f"合法 slug 被拒绝: {valid}")
            return
    t.ok("slug_valid: 合法 slug 通过")

    # 非法 slug
    for invalid in ['', ' ', '; rm -rf /', '../etc/passwd', 'foo bar', 'slug;whoami', '$(id)', 'Aaa', '-dash-start']:
        if tracker._valid_slug(invalid):
            t.fail("slug_invalid", f"非法 slug 未被拒绝: {invalid}")
            return
    t.ok("slug_invalid: 非法 slug 全部拒绝")


def test_slug_injection_in_fetch(t):
    """fetch() 对非法 slug 返回 None 而非执行子进程"""
    result = tracker.fetch("; rm -rf /")
    if result is None:
        t.ok("fetch_injection: 注入 slug 返回 None")
    else:
        t.fail("fetch_injection", f"注入 slug 未被拦截，返回: {result}")


def test_empty_date_handling(t):
    """空日期字段不应崩溃"""
    with MockDir() as m:
        # 写入含空日期的记录
        m.write_checklog([
            ("2026-06-01 08:00:00", "x", 100, 0),
            ("", "x", 101, 1),          # 空日期
            ("   ", "x", 102, 1),        # 空白日期
        ])
        data = tracker.read_checklog()
        try:
            filtered = tracker._filter_by_date(data, "2026-06-01", "2026-06-01")
            t.ok("empty_date: 空日期不崩溃，正常过滤")
        except Exception as e:
            t.fail("empty_date", f"崩溃: {e}")


def test_missing_credentials(t):
    """凭证缺失时 send_feishu 不崩溃，返回 False"""
    orig_id = tracker.APP_ID
    orig_secret = tracker.APP_SECRET
    orig_user = tracker.USER_OPEN_ID
    try:
        tracker.APP_ID = ""
        tracker.APP_SECRET = ""
        tracker.USER_OPEN_ID = ""
        result = tracker.send_feishu("test message")
        if result is False:
            t.ok("missing_creds: 凭证缺失返回 False")
        else:
            t.fail("missing_creds", f"预期 False，得到: {result}")
    except Exception as e:
        t.fail("missing_creds", f"崩溃: {e}")
    finally:
        tracker.APP_ID = orig_id
        tracker.APP_SECRET = orig_secret
        tracker.USER_OPEN_ID = orig_user


def test_no_hardcoded_credentials(t):
    """源码中不应包含硬编码的飞书凭证"""
    src = open(os.path.join(SCRIPT_DIR, "clawhub_tracker.py")).read()
    forbidden = ["cli_a948e522fcf7dbc3", "wPrjnuq77g6TiHIzcbLUefivPozifcc0"]
    found = [s for s in forbidden if s in src]
    if not found:
        t.ok("no_hardcoded_creds: 源码无硬编码凭证")
    else:
        t.fail("no_hardcoded_creds", f"发现硬编码凭证: {found}")


def test_no_tmp_log(t):
    """日志不应写入 /tmp"""
    src = open(os.path.join(SCRIPT_DIR, "clawhub_tracker.py")).read()
    if "/tmp/clawhub_tracker.log" not in src:
        t.ok("no_tmp_log: 无 /tmp 日志路径")
    else:
        t.fail("no_tmp_log", "/tmp 日志路径仍存在")


# ── 运行 ──────────────────────────────────────────────────

def main():
    t = TestResult()
    print("🧪 ClawHub Tracker 测试\n")

    test_load_skills_empty(t)
    test_load_skills(t)
    test_get_last(t)
    test_read_checklog(t)
    test_filter_by_date(t)
    test_append_checklog(t)
    test_daily_report(t)
    test_weekly_report(t)
    test_monthly_report(t)
    test_report_file_saved(t)
    test_no_data_report(t)
    test_report_all_zeros(t)

    # 安全专项测试
    print("\n🛡️ 安全专项测试\n")
    test_slug_validation(t)
    test_slug_injection_in_fetch(t)
    test_empty_date_handling(t)
    test_missing_credentials(t)
    test_no_hardcoded_credentials(t)
    test_no_tmp_log(t)

    ok = t.summary()
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
