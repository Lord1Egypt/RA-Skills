# -*- coding: utf-8 -*-
"""truetime-cn 单元测试。运行:  python3 -m pytest tests/ -v"""
import sys
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import truetime_cn as tt


# ─── 单位解析 ───
class TestParseDuration:
    def test_simple_minute(self):
        assert tt.parse_duration("1m") == [(1.0, 60_000, 0)]

    def test_decimal(self):
        assert tt.parse_duration("1.5m") == [(1.5, 60_000, 0)]

    def test_compound(self):
        r = tt.parse_duration("1h30m")
        assert r == [(1.0, 3_600_000, 0), (30.0, 60_000, 0)]

    def test_calendar_month(self):
        r = tt.parse_duration("1.5month")
        assert r == [(1.5, 0, 1)]

    def test_year_decade_century(self):
        assert tt.parse_duration("1y")[0][2] == 12
        assert tt.parse_duration("1decade")[0][2] == 120
        assert tt.parse_duration("1century")[0][2] == 1200

    def test_invalid_unit_raises(self):
        with pytest.raises(ValueError, match="未识别"):
            tt.parse_duration("10sigma")

    def test_empty_raises(self):
        with pytest.raises(ValueError):
            tt.parse_duration("")

    def test_mixed_calendar_fixed(self):
        r = tt.parse_duration("1month2weeks")
        assert r == [(1.0, 0, 1), (2.0, 604_800_000, 0)]

    def test_comma_decimal(self):
        # 中文/欧洲小数点逗号
        assert tt.parse_duration("1,5m") == [(1.5, 60_000, 0)]


# ─── 日历月运算 ───
class TestCalendarMonths:
    def test_simple_add(self):
        d = datetime(2026, 5, 8, 12, 0)
        assert tt.add_calendar_months(d, 1) == datetime(2026, 6, 8, 12, 0)

    def test_end_of_month_clamp(self):
        d = datetime(2026, 1, 31, 10, 0)
        # 2 月没有 31，钳到 2/28
        assert tt.add_calendar_months(d, 1) == datetime(2026, 2, 28, 10, 0)

    def test_leap_year_clamp(self):
        d = datetime(2028, 1, 31, 10, 0)
        # 2028 是闰年
        assert tt.add_calendar_months(d, 1) == datetime(2028, 2, 29, 10, 0)

    def test_year_overflow(self):
        d = datetime(2026, 12, 15, 0, 0)
        assert tt.add_calendar_months(d, 1) == datetime(2027, 1, 15, 0, 0)

    def test_fractional_uses_target_month_length(self):
        d = datetime(2026, 1, 1, 0, 0)
        # 1 + 0.5 mo -> 整数 1mo 到 2/1，再加 28*0.5 天 (2026 二月 28 天)
        result = tt.add_calendar_months(d, 1.5)
        # 2/1 + 14 天 = 2/15
        assert result == datetime(2026, 2, 15, 0, 0)


# ─── DST 检测 ───
class TestDST:
    LA = ZoneInfo("America/Los_Angeles")

    def test_normal_time_ok(self):
        assert tt.check_dst_validity(datetime(2026, 5, 8, 12, 0), self.LA) is None

    def test_spring_forward_gap(self):
        msg = tt.check_dst_validity(datetime(2026, 3, 8, 2, 30), self.LA)
        assert msg and "不存在" in msg

    def test_fall_back_overlap(self):
        msg = tt.check_dst_validity(datetime(2026, 11, 1, 1, 30), self.LA)
        assert msg and "模糊" in msg

    def test_shanghai_no_dst(self):
        # 中国不实行 DST
        sh = ZoneInfo("Asia/Shanghai")
        assert tt.check_dst_validity(datetime(2026, 3, 8, 2, 30), sh) is None


# ─── 农历 ───
class TestLunar:
    def test_today_lunar(self):
        info = tt.lunar_info(datetime(2026, 5, 8))
        # 2026-05-08 应该是丙午年三月廿二
        assert "丙午年" in info["display"]
        assert info["zodiac"] == "马"

    def test_chinese_new_year(self):
        info = tt.lunar_info(datetime(2026, 2, 17))
        assert "正月初一" in info["display"]

    def test_mid_autumn(self):
        info = tt.lunar_info(datetime(2026, 9, 25))
        assert "八月十五" in info["display"]


# ─── 节假日 ───
class TestHolidays:
    def test_chinese_new_year_day1(self):
        d = datetime(2026, 2, 17, 10, 0, tzinfo=ZoneInfo("Asia/Shanghai"))
        info = tt.cn_holiday_info(d)
        assert info["holiday_name"] == "春节"
        assert info["is_workday"] is False
        assert info["source"] == "statutory_holiday"

    def test_compensatory_workday(self):
        # 2026-02-14 是周六但调休上班
        d = datetime(2026, 2, 14, 10, 0, tzinfo=ZoneInfo("Asia/Shanghai"))
        info = tt.cn_holiday_info(d)
        assert info["holiday_name"] is None
        assert info["is_workday"] is True
        assert info["source"] == "compensatory_workday"

    def test_normal_weekend(self):
        # 2026-05-09 是周六（非调休）
        d = datetime(2026, 5, 9, 10, 0, tzinfo=ZoneInfo("Asia/Shanghai"))
        info = tt.cn_holiday_info(d)
        # 注意：5/9 是劳动节调休补班日
        assert info["source"] == "compensatory_workday"
        assert info["is_workday"] is True

    def test_pure_weekend(self):
        # 2026-05-16 周六，不在任何调休
        d = datetime(2026, 5, 16, 10, 0, tzinfo=ZoneInfo("Asia/Shanghai"))
        info = tt.cn_holiday_info(d)
        assert info["holiday_name"] is None
        assert info["is_workday"] is False
        assert info["source"] == "weekend_rule"

    def test_normal_weekday(self):
        d = datetime(2026, 5, 8, 10, 0, tzinfo=ZoneInfo("Asia/Shanghai"))  # 周五
        info = tt.cn_holiday_info(d)
        assert info["holiday_name"] is None
        assert info["is_workday"] is True

    def test_unknown_year_fallback(self):
        # 2099 必然没数据
        d = datetime(2099, 6, 1, 10, 0, tzinfo=ZoneInfo("Asia/Shanghai"))
        info = tt.cn_holiday_info(d)
        assert info["source"] == "fallback_weekend_only"
        assert info["year_data_available"] is False


# ─── 全部 7 个 2026 节日识别 ───
class TestAllHolidays2026:
    sh = ZoneInfo("Asia/Shanghai")

    @pytest.mark.parametrize("date_str,expected", [
        ("2026-01-01", "元旦"),
        ("2026-02-15", "春节"),
        ("2026-02-23", "春节"),
        ("2026-04-04", "清明节"),
        ("2026-05-01", "劳动节"),
        ("2026-05-05", "劳动节"),
        ("2026-06-19", "端午节"),
        ("2026-09-25", "中秋节"),
        ("2026-10-01", "国庆节"),
        ("2026-10-07", "国庆节"),
    ])
    def test_holiday(self, date_str, expected):
        d = datetime.strptime(date_str, "%Y-%m-%d").replace(tzinfo=self.sh)
        assert tt.cn_holiday_info(d)["holiday_name"] == expected

    @pytest.mark.parametrize("date_str", [
        "2026-01-04", "2026-02-14", "2026-02-28",
        "2026-05-09", "2026-09-20", "2026-10-10",
    ])
    def test_compensatory(self, date_str):
        d = datetime.strptime(date_str, "%Y-%m-%d").replace(tzinfo=self.sh)
        info = tt.cn_holiday_info(d)
        assert info["is_workday"] is True
        assert info["source"] == "compensatory_workday"


# ─── humanize ───
class TestHumanize:
    def test_seconds(self):
        assert "秒" in tt.humanize_delta_zh(45)

    def test_minutes(self):
        assert "分" in tt.humanize_delta_zh(120)

    def test_months(self):
        s = tt.humanize_delta_zh(86400 * 45)
        assert "个月" in s

    def test_negative(self):
        assert tt.humanize_delta_zh(-100).startswith("-")
