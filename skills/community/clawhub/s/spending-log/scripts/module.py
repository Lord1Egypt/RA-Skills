"""共享配置和工具函数，供 crud.py / query.py / report.py 统一引用"""

import json
import os
from collections import defaultdict

# ── 分类配置（统一 emoji / 颜色） ──────────────────────────────
CATEGORIES = ['餐饮', '交通', '购物', '娱乐', '医疗', '房租', '日用', '社交', '其他']

CAT_CONFIG = {
    '餐饮': {'emoji': '🍜', 'color': '#d4845a', 'bg': '#fdf5ee'},
    '交通': {'emoji': '🚗', 'color': '#7ba699', 'bg': '#eef5f2'},
    '购物': {'emoji': '🛒', 'color': '#c4899e', 'bg': '#faf0f3'},
    '娱乐': {'emoji': '🎮', 'color': '#d4a04a', 'bg': '#fdf8ed'},
    '医疗': {'emoji': '💊', 'color': '#8aaa7b', 'bg': '#f0f5ee'},
    '房租': {'emoji': '🏠', 'color': '#9b8ec4', 'bg': '#f3f1f8'},
    '日用': {'emoji': '🧴', 'color': '#6ba3a8', 'bg': '#edf5f5'},
    '社交': {'emoji': '🤝', 'color': '#c97070', 'bg': '#faf0f0'},
    '其他': {'emoji': '📌', 'color': '#a0978e', 'bg': '#f5f3f1'},
}

# ── Schema 校验字段 ──────────────────────────────────────────
REQUIRED_FIELDS = ('id', 'amount', 'category', 'description', 'date', 'timestamp')

# ── 数据加载 ──────────────────────────────────────────────────

def load_data(filepath):
    """加载 JSON 数据，带 schema 校验"""
    if not os.path.exists(filepath):
        return []
    with open(filepath, 'r') as f:
        data = json.load(f)
    if not isinstance(data, list):
        data = [data]
    # 校验每条记录
    for i, rec in enumerate(data):
        if not isinstance(rec, dict):
            raise ValueError(f"第 {i+1} 条记录不是对象: {rec!r}")
        for field in REQUIRED_FIELDS:
            if field not in rec:
                raise ValueError(f"第 {i+1} 条记录缺少字段 '{field}': {rec!r}")
    return data


# （统计工具已内联到 query.py / report.py 中，此处不再单独导出）
