#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tushare 股票数据技能 (完整接口版)
基于用户提供的详细接口文档实现。
支持 23 个核心接口。
"""
import json
import os
import sys
import pandas as pd
import traceback
from datetime import datetime

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 尝试导入tushare
try:
    import tushare as ts
    TUSHARE_AVAILABLE = True
except ImportError:
    TUSHARE_AVAILABLE = False
    print("警告: tushare库未安装，请运行: pip install tushare")

# ========== 【核心】本技能支持的全部接口列表 ==========
SUPPORTED_APIS = {
    # ===== 行情数据类 =====
    "daily": {
        "name": "日线行情",
        "description": "获取股票日线行情数据，包含开盘、最高、最低、收盘、成交量等。交易日每天15点～16点之间入库。本接口是未复权行情，停牌期间不提供数据。",
        "category": "行情数据"
    },
    "rt_k": {
        "name": "实时日K线",
        "description": "获取实时日k线行情，支持按股票代码及股票代码通配符一次性提取全部股票实时日k线行情。单次最大可提取6000条数据。",
        "category": "行情数据"
    },
    "stk_mins": {
        "name": "分钟行情",
        "description": "获取A股分钟数据，支持1min/5min/15min/30min/60min行情。单次最大8000行数据，可提供超过10年历史分钟数据。",
        "category": "行情数据"
    },
    "rt_min": {
        "name": "全A实时分钟数据",
        "description": "获取全A股票实时分钟数据，包括1~60min。单次最大1000行数据。",
        "category": "行情数据"
    },
    "weekly": {
        "name": "周线行情",
        "description": "获取A股周线行情，本接口每周最后一个交易日更新。单次最大6000行。",
        "category": "行情数据"
    },
    "monthly": {
        "name": "月线行情",
        "description": "获取A股月线数据。单次最大4500行。",
        "category": "行情数据"
    },
    "stk_weekly_monthly": {
        "name": "股票周/月线行情(每日更新)",
        "description": "股票周/月线行情(每日更新)。单次最大6000行。",
        "category": "行情数据"
    },
    "stk_week_month_adj": {
        "name": "股票周/月线行情(复权--每日更新)",
        "description": "股票周/月线行情(复权--每日更新)。单次最大6000行。",
        "category": "行情数据"
    },
    "adj_factor": {
        "name": "复权因子",
        "description": "获取股票复权因子，可提取单只股票全部历史复权因子，也可以提取单日全部股票的复权因子。盘前9点15~20分完成当日复权因子入库。",
        "category": "行情数据"
    },
    "daily_basic": {
        "name": "每日指标",
        "description": "获取全部股票每日重要的基本面指标，可用于选股分析、报表展示等。交易日每日15点～17点之间更新。单次请求最大返回6000条数据。",
        "category": "行情数据"
    },
    "stk_limit": {
        "name": "涨跌停价格",
        "description": "获取全市场（包含A/B股和基金）每日涨跌停价格，包括涨停价格，跌停价格等，每个交易日8点40左右更新当日股票涨跌停价格。单次最多提取5800条记录。",
        "category": "行情数据"
    },
    "suspend_d": {
        "name": "每日停复牌信息",
        "description": "按日期方式获取股票每日停复牌信息。",
        "category": "行情数据"
    },
    "hsgt_top10": {
        "name": "沪深港通十大成交股",
        "description": "获取沪股通、深股通每日前十大成交详细数据，每天18~20点之间完成当日更新。",
        "category": "行情数据"
    },
    # ===== 基础信息类 =====
    "stock_basic": {
        "name": "股票列表",
        "description": "获取基础信息数据，包括股票代码、名称、上市日期、退市日期等。每次最多返回6000行数据。此接口是基础信息，调取一次就可以拉取完，建议保存到本地存储后使用。",
        "category": "基础信息"
    },
    "trade_cal": {
        "name": "交易日历",
        "description": "获取各大交易所交易日历数据，默认提取的是上交所。",
        "category": "基础信息"
    },
    "stock_st": {
        "name": "ST股票列表",
        "description": "获取ST股票列表，可根据交易日期获取历史上每天的ST列表。每天上午9:20更新，单次请求最大返回1000行数据。本接口数据从20160101开始。",
        "category": "基础信息"
    },
    "stock_hsgt": {
        "name": "沪深港通股票列表",
        "description": "获取沪深港通股票列表。每天上午9:20更新，单次请求最大返回2000行数据。本接口数据从20250812开始。",
        "category": "基础信息"
    },
    "namechange": {
        "name": "历史名称变更记录",
        "description": "获取股票历史名称变更记录。",
        "category": "基础信息"
    },
    "stock_company": {
        "name": "上市公司基础信息",
        "description": "获取上市公司基础信息，单次提取4500条，可以根据交易所分批提取。",
        "category": "基础信息"
    },
    "stk_managers": {
        "name": "上市公司管理层",
        "description": "获取上市公司管理层信息。",
        "category": "基础信息"
    },
    "stk_rewards": {
        "name": "管理层薪酬和持股",
        "description": "获取上市公司管理层薪酬和持股信息。",
        "category": "基础信息"
    },
    "bse_mapping": {
        "name": "北交所新旧代码对照表",
        "description": "获取北交所股票代码变更后新旧代码映射表数据。单次最大1000条。",
        "category": "基础信息"
    },
    "new_share": {
        "name": "IPO新股列表",
        "description": "获取新股上市列表数据。单次最大2000条。",
        "category": "基础信息"
    },
    "bak_basic": {
        "name": "股票历史列表（备用基础列表）",
        "description": "获取备用基础列表，数据从2016年开始。单次最大7000条。",
        "category": "基础信息"
    }
}

class TushareClient:
    """Tushare API客户端"""
    
    def __init__(self, token: str = None):
        # 【关键修正】移除默认Token，强制用户提供
        self.token = token or os.environ.get("TUSHARE_TOKEN", "")
        if not self.token:
            raise ValueError(
                "未检测到有效的 Tushare Token。\n"
                "请通过以下任一方式配置：\n"
                "  1. 在调用参数中传入：{'token': '你的token'}\n"
                "  2. 设置系统环境变量：export TUSHARE_TOKEN='你的token'\n"
                "Token需在Tushare官网(https://tushare.pro)注册获取。"
            )
        self.pro = None
        self._init_pro()
    
    def _init_pro(self):
        try:
            self.pro = ts.pro_api(self.token)
        except Exception as e:
            raise Exception(f"Tushare初始化失败: {str(e)}")
    
    def call_api(self, api_name: str, **kwargs):
        if not self.pro:
            self._init_pro()
        
        if not hasattr(self.pro, api_name):
            raise Exception(f"Tushare接口 '{api_name}' 不存在。请检查接口名称。")
        
        try:
            api_method = getattr(self.pro, api_name)
            result = api_method(**kwargs)
            
            if result is None:
                return {"success": False, "error": "API返回空结果", "data": None}
            
            if isinstance(result, pd.DataFrame):
                if result.empty:
                    return {"success": True, "message": "查询成功，但无数据", "data": [], "count": 0}
                df = result.where(pd.notnull(result), None)
                return {
                    "success": True,
                    "message": "查询成功",
                    "data": df.to_dict('records'),
                    "count": len(df),
                    "columns": list(df.columns)
                }
            else:
                return {"success": True, "message": "查询成功", "data": result, "count": 1}
        except Exception as e:
            return {"success": False, "error": f"API调用失败: {str(e)}"}

def handler(params: dict) -> dict:
    if not TUSHARE_AVAILABLE:
        return {"success": False, "error": "tushare库未安装。请运行: pip install tushare pandas"}
    
    api_name = params.get("api_name", "").strip()
    token = params.get("token", "").strip()
    ts_code = params.get("ts_code", "").strip()
    trade_date = params.get("trade_date", "").strip()
    start_date = params.get("start_date", "").strip()
    end_date = params.get("end_date", "").strip()
    fields = params.get("fields", "").strip()
    extra_params_str = params.get("extra_params", "{}").strip()
    
    # 处理 list 命令
    if api_name.lower() in ["list", "help", "?", "接口列表"]:
        result_list = []
        for api_key, info in SUPPORTED_APIS.items():
            result_list.append({
                "api_name": api_key,
                "name": info["name"],
                "category": info["category"],
                "description": info["description"][:100] + "..." if len(info["description"]) > 100 else info["description"]
            })
        return {
            "success": True,
            "message": f"本技能共支持 {len(SUPPORTED_APIS)} 个Tushare股票接口",
            "apis": result_list
        }
    
    # 验证必需参数
    if not api_name:
        return {"success": False, "error": "参数 'api_name' 为必填项。输入 'list' 查看全部接口。"}
    if api_name not in SUPPORTED_APIS:
        return {"success": False, "error": f"接口 '{api_name}' 不在支持列表中。输入 'list' 查看全部接口。"}
    
    # 构建API参数
    api_params = {}
    for key in ["ts_code", "trade_date", "start_date", "end_date", "fields"]:
        if value := params.get(key, "").strip():
            api_params[key] = value
    
    if extra_params_str:
        try:
            extra_params = json.loads(extra_params_str)
            if isinstance(extra_params, dict):
                api_params.update(extra_params)
        except json.JSONDecodeError:
            return {"success": False, "error": "参数 'extra_params' 必须是有效的JSON字符串。"}
    
    api_params = {k: v for k, v in api_params.items() if v not in ["", None]}
    
    # 调用API
    try:
        client = TushareClient(token=token if token else None)
        result = client.call_api(api_name, **api_params)
        if result.get("success"):
            result["request_info"] = {"api_name": api_name, "params": api_params, "called_at": datetime.now().isoformat()}
        return result
    except ValueError as e:
        return {"success": False, "error": str(e)}
    except Exception as e:
        return {"success": False, "error": f"处理请求时出错: {str(e)}"}

if __name__ == "__main__":
    import sys
    import json

    # 从标准输入读取调用参数
    input_str = sys.stdin.read()
    if not input_str.strip():
        # 如果输入为空，默认执行列出接口的命令
        params = {"api_name": "list"}
    else:
        try:
            params = json.loads(input_str)
        except json.JSONDecodeError as e:
            # 如果输入不是合法JSON，返回错误
            error_result = {"success": False, "error": f"Invalid JSON input: {e}"}
            print(json.dumps(error_result, ensure_ascii=False))
            sys.exit(1)

    # 调用主处理函数
    try:
        result = handler(params)
        # 将结果以JSON格式打印到标准输出，供平台捕获
        print(json.dumps(result, ensure_ascii=False))
    except Exception as e:
        # 捕获处理过程中的未预期异常
        error_result = {"success": False, "error": f"Handler execution failed: {str(e)}"}
        print(json.dumps(error_result, ensure_ascii=False))
        sys.exit(1)