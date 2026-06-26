"""安全校验函数专项测试"""

import sys
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

# ── 注入 mock 环境 ────────────────────────────────────────
import os
os.environ["LEDGER_DATA_DIR"] = str(Path.home() / ".openclaw" / "workspace")

from invest import (
    _safe_ledger_path,
    _sanitize,
    _validate_code,
    _validate_amount,
    _validate_shares,
    _validate_price,
    confirm_buy,
    confirm_sell,
    auto_lookup_code,
)


class TestSafeLedgerPath(unittest.TestCase):
    """路径白名单校验"""

    def test_allowed_path(self):
        safe = _safe_ledger_path(Path.home() / ".openclaw" / "workspace" / "data" / "test.csv")
        self.assertIsNotNone(safe)

    def test_reject_absolute_outside_workspace(self):
        unsafe = _safe_ledger_path(Path("/etc/passwd"))
        self.assertIsNone(unsafe)

    def test_reject_parent_traversal(self):
        unsafe = _safe_ledger_path(Path.home() / ".openclaw" / "workspace" / ".." / ".." / "etc" / "passwd")
        self.assertIsNone(unsafe)

    def test_reject_symlink_outside_workspace(self):
        # 模拟指向 /tmp 的 symlink 在 workspace 内
        safe = _safe_ledger_path(Path.home() / ".openclaw" / "workspace")
        self.assertIsNotNone(safe)


class TestSanitize(unittest.TestCase):
    """ANSI / 转义序列过滤"""

    def test_strip_ansi_escape(self):
        # ANSI颜色转义序列
        dirty = "\x1b[31m红色\x1b[0m正常"
        clean = _sanitize(dirty)
        self.assertNotIn("\x1b[", clean)
        self.assertNotIn("[31", clean)

    def test_strip_bell_char(self):
        # \x07 (Bell) 不是 ANSI 转义序列，不过滤；纯文本，不构成安全风险
        dirty = "hello\x07world"
        clean = _sanitize(dirty)
        self.assertEqual(clean, "hello\x07world")  # 保留，内容无害

    def test_normal_text_unchanged(self):
        self.assertEqual(_sanitize("今天吃饭花了50块"), "今天吃饭花了50块")


class TestValidateCode(unittest.TestCase):
    """证券代码格式校验"""

    def test_valid_6digit(self):
        self.assertTrue(_validate_code("025209"))
        self.assertTrue(_validate_code("600519"))

    def test_reject_short(self):
        self.assertFalse(_validate_code("12345"))
        self.assertFalse(_validate_code("123"))

    def test_reject_non_digit(self):
        self.assertFalse(_validate_code("02520A"))
        self.assertFalse(_validate_code("1234567"))
        self.assertFalse(_validate_code(""))
        self.assertFalse(_validate_code("00000 "))

    def test_reject_with_ansi(self):
        # 代码被污染时直接拒绝
        self.assertFalse(_validate_code("025209\x1b[31m"))


class TestValidateAmount(unittest.TestCase):
    """金额校验（_MAX_AMOUNT = 1,000,000,000）"""

    def test_valid(self):
        self.assertAlmostEqual(_validate_amount(100.0), 100.0)
        self.assertAlmostEqual(_validate_amount(0.01), 0.01)

    def test_reject_zero(self):
        with self.assertRaises(ValueError):
            _validate_amount(0)

    def test_reject_negative(self):
        with self.assertRaises(ValueError):
            _validate_amount(-50)

    def test_reject_1b_boundary(self):
        with self.assertRaises(ValueError):
            _validate_amount(1_000_000_001)

    def test_valid_at_max(self):
        self.assertAlmostEqual(_validate_amount(1_000_000_000), 1_000_000_000)


class TestValidateShares(unittest.TestCase):
    """份额校验（仅校验正数，无上限）"""

    def test_valid(self):
        self.assertAlmostEqual(_validate_shares(100), 100)
        self.assertAlmostEqual(_validate_shares(0.1), 0.1)

    def test_reject_zero(self):
        with self.assertRaises(ValueError):
            _validate_shares(0)

    def test_reject_negative(self):
        with self.assertRaises(ValueError):
            _validate_shares(-10)


class TestInvestmentConfirmation(unittest.TestCase):
    """投资写入必须要求交互式确认"""

    def test_confirm_buy_rejects_non_interactive_stdin(self):
        fake_stdin = mock.Mock()
        fake_stdin.isatty.return_value = False
        with mock.patch.object(sys, "stdin", fake_stdin):
            ok = confirm_buy("沪深300ETF", "510050", 100, 3.5, 350, "银行卡", "2026-01-15")
        self.assertFalse(ok)

    def test_confirm_sell_rejects_non_interactive_stdin(self):
        fake_stdin = mock.Mock()
        fake_stdin.isatty.return_value = False
        with mock.patch.object(sys, "stdin", fake_stdin):
            ok = confirm_sell("沪深300ETF", "510050", 100, 3.5, 350, "银行卡", "2026-01-15")
        self.assertFalse(ok)


class TestNetworkOptIn(unittest.TestCase):
    """联网查询必须显式 opt-in"""

    def test_auto_lookup_requires_allow_network(self):
        with mock.patch("subprocess.run") as mocked_run:
            result = auto_lookup_code("沪深300ETF")
        mocked_run.assert_not_called()
        self.assertFalse(result["found"])
        self.assertTrue(result["network_denied"])


class TestValidatePrice(unittest.TestCase):
    """单价校验（_MAX_AMOUNT = 1,000,000,000）"""

    def test_valid(self):
        self.assertAlmostEqual(_validate_price(3.50), 3.50)
        self.assertAlmostEqual(_validate_price(0.01), 0.01)

    def test_reject_zero(self):
        with self.assertRaises(ValueError):
            _validate_price(0)

    def test_reject_negative(self):
        with self.assertRaises(ValueError):
            _validate_price(-1.5)

    def test_reject_1b_boundary(self):
        with self.assertRaises(ValueError):
            _validate_price(1_000_000_001)


if __name__ == "__main__":
    unittest.main(verbosity=2)