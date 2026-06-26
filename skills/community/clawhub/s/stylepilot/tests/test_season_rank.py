#!/usr/bin/env python3
"""季节与天气排序逻辑回归（不依赖数据库）。"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))

from wardrobe import (
    _season_hot_score,
    _sort_category_buckets_for_weather,
    _weather_tag,
)


def main():
    assert _weather_tag("海南露营") == "hot"
    assert _weather_tag("三亚海边") == "hot"
    assert _weather_tag("阴天18度") == "mild"

    assert _season_hot_score("秋冬") < _season_hot_score("夏")
    assert _season_hot_score("春秋") < _season_hot_score("夏")
    assert _season_hot_score("夏") == _season_hot_score("春夏")

    # 同品类内：炎热天优先夏款，其次才是偏好顺序
    summer_top = {"id": "t1", "category": "上衣", "season": "夏"}
    fall_top = {"id": "t2", "category": "上衣", "season": "秋冬"}
    ordered = [fall_top, summer_top]  # 偏好上先选了秋冬款
    by_cat = {"上衣": [fall_top, summer_top]}
    out = _sort_category_buckets_for_weather(by_cat, ordered, "高温暴晒")
    assert out["上衣"][0]["id"] == "t1"

    # 同季则保持偏好顺序（先出现的优先）
    a = {"id": "a", "category": "上衣", "season": "夏"}
    b = {"id": "b", "category": "上衣", "season": "夏"}
    out2 = _sort_category_buckets_for_weather({"上衣": [b, a]}, [a, b], "高温")
    assert out2["上衣"][0]["id"] == "a"

    print("OK")


if __name__ == "__main__":
    main()
