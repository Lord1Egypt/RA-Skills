#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import os
import sys
import pandas as pd
from datetime import datetime

# 尝试导入 tushare
try:
    import tushare as ts
    TUSHARE_AVAILABLE = True
except ImportError:
    TUSHARE_AVAILABLE = False

# 支持的 14 个期货接口配置
SUPPORTED_APIS = {
    "fut_basic": {"name": "期货合约列表", "category": "基础信息", "description": "获取期货合约列表数据"},
    "trade_cal": {"name": "期货交易日历", "category": "基础信息", "description": "查询交易日历"},
    "fut_mapping": {"name": "主力合约映射", "category": "基础信息", "description": "主力与月合约映射"},
    "fut_daily": {"name": "期货日线行情", "category": "行情数据", "description": "日K线数据"},
    "fut_weekly_monthly": {"name": "期货周/月线行情", "category": "行情数据", "description": "周/月K线数据"},
    "ft_mins": {"name": "期货分钟行情(历史)", "category": "行情数据", "description": "历史分钟数据"},
    "rt_fut_min": {"name": "期货实时分钟行情", "category": "实时行情", "description": "实时分钟数据(需权限)"},
    "fut_wsr": {"name": "仓单日报", "category": "仓单与结算", "description": "每日仓单数据"},
    "fut_settle": {"name": "每日结算参数", "category": "仓单与结算", "description": "结算价及手续费参数"},
    "fut_holding": {"name": "成交持仓排名", "description": "会员成交持仓排名"},
    "index_daily": {"name": "南华指数行情", "category": "指数数据", "description": "南华期货指数日线"},
    "fut_weekly_detail": {"name": "周期交易统计", "category": "统计信息", "description": "品种周度交易统计"},
    "ft_limit": {"name": "涨跌停价格及保证金", "category": "风险指标", "description": "每日涨跌停及保证金率"}
}

class TushareFuturesClient:
    def __init__(self, token: str = None):
        # 严格校验：仅从参数或环境变量获取，不设任何默认硬编码
        self.token = token or os.environ.get("TUSHARE_TOKEN", "")
        if not self.token:
            raise ValueError(
                "未检测到 Tushare Token。本技能不内置默认 Token，请通过以下方式配置：\n"
                "1. 调用参数：{'token': '您的Token'}\n"
                "2. 环境变量：设置 TUSHARE_TOKEN"
            )
        self.pro = None
        self._init_pro()

    def _init_pro(self):
        try:
            self.pro = ts.pro_api(self.token)
        except Exception as e:
            raise Exception(f"Tushare 初始化失败，请检查 Token 有效性: {str(e)}")

    def call_api(self, api_name: str, **kwargs):
        if not hasattr(self.pro, api_name) and api_name != "trade_cal":
            raise Exception(f"接口 '{api_name}' 不存在")
        
        api_method = self.pro.query if api_name == "trade_cal" else getattr(self.pro, api_name)
        
        try:
            result = api_method(**kwargs)
            if isinstance(result, pd.DataFrame):
                return {"success": True, "data": result.where(pd.notnull(result), None).to_dict('records'), "count": len(result)}
            return {"success": True, "data": result}
        except Exception as e:
            return {"success": False, "error": f"API调用失败: {str(e)}"}

def handler(params: dict) -> dict:
    api_name = params.get("api_name", "").strip()
    token = params.get("token", "").strip()

    if api_name.lower() in ["list", "help"]:
        return {"success": True, "apis": [{"api": k, "name": v["name"]} for k, v in SUPPORTED_APIS.items()]}

    if api_name not in SUPPORTED_APIS:
        return {"success": False, "error": "无效的接口名称"}

    # 构建参数
    api_params = {k: v for k, v in params.items() if k not in ["api_name", "token", "extra_params"]}
    if "extra_params" in params:
        api_params.update(json.loads(params["extra_params"]))

    try:
        client = TushareFuturesClient(token=token if token else None)
        return client.call_api(api_name, **api_params)
    except Exception as e:
        return {"success": False, "error": str(e)}