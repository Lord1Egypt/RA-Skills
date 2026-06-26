#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
各城市社保公积金费率配置
数据参考：2024 年各地人社局公布标准
"""

CITY_RATES = {
    "北京": {
        "social_security": {
            "pension": {"personal": 0.08, "company": 0.16},
            "medical": {"personal": 0.02, "company": 0.10},
            "unemployment": {"personal": 0.005, "company": 0.005},
            "work_injury": {"personal": 0, "company": 0.004},
            "maternity": {"personal": 0, "company": 0.008},
        },
        "fund": {"personal_min": 0.05, "personal_max": 0.12, "default": 0.12},
        "base": {
            "min": 6326,
            "max": 33891,
        }
    },
    "上海": {
        "social_security": {
            "pension": {"personal": 0.08, "company": 0.16},
            "medical": {"personal": 0.02, "company": 0.10},
            "unemployment": {"personal": 0.005, "company": 0.005},
            "work_injury": {"personal": 0, "company": 0.0025},
            "maternity": {"personal": 0, "company": 0.01},
        },
        "fund": {"personal_min": 0.05, "personal_max": 0.07, "default": 0.07},
        "base": {
            "min": 7310,
            "max": 36921,
        }
    },
    "广州": {
        "social_security": {
            "pension": {"personal": 0.08, "company": 0.14},
            "medical": {"personal": 0.02, "company": 0.055},
            "unemployment": {"personal": 0.002, "company": 0.008},
            "work_injury": {"personal": 0, "company": 0.004},
            "maternity": {"personal": 0, "company": 0.005},
        },
        "fund": {"personal_min": 0.05, "personal_max": 0.12, "default": 0.12},
        "base": {
            "min": 5284,
            "max": 26421,
        }
    },
    "深圳": {
        "social_security": {
            "pension": {"personal": 0.08, "company": 0.15},
            "medical": {"personal": 0.02, "company": 0.06},
            "unemployment": {"personal": 0.003, "company": 0.007},
            "work_injury": {"personal": 0, "company": 0.005},
            "maternity": {"personal": 0, "company": 0.005},
        },
        "fund": {"personal_min": 0.05, "personal_max": 0.12, "default": 0.12},
        "base": {
            "min": 3523,
            "max": 26421,
        }
    },
    "杭州": {
        "social_security": {
            "pension": {"personal": 0.08, "company": 0.14},
            "medical": {"personal": 0.02, "company": 0.095},
            "unemployment": {"personal": 0.005, "company": 0.005},
            "work_injury": {"personal": 0, "company": 0.004},
            "maternity": {"personal": 0, "company": 0.005},
        },
        "fund": {"personal_min": 0.05, "personal_max": 0.12, "default": 0.12},
        "base": {
            "min": 4462,
            "max": 24060,
        }
    },
    "成都": {
        "social_security": {
            "pension": {"personal": 0.08, "company": 0.16},
            "medical": {"personal": 0.02, "company": 0.065},
            "unemployment": {"personal": 0.004, "company": 0.016},
            "work_injury": {"personal": 0, "company": 0.005},
            "maternity": {"personal": 0, "company": 0.008},
        },
        "fund": {"personal_min": 0.05, "personal_max": 0.12, "default": 0.12},
        "base": {
            "min": 4071,
            "max": 20355,
        }
    },
}

# 退休金计算参数
PENSION_PARAMS = {
    "personal_account_divisor": 139,  # 60 岁退休计发月数
    "base_pension_rate": 0.01,  # 基础养老金计发比例
    "years_threshold": 15,  # 最低缴费年限
}
