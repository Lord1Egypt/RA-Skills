import argparse
import inspect
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path


def get_python_version(python_cmd):
    try:
        output = subprocess.check_output(
            [python_cmd, "-c", "import sys; print(f'{sys.version_info[0]}.{sys.version_info[1]}')"],
            text=True,
        ).strip()
    except Exception:
        return None
    parts = output.split(".")
    if len(parts) < 2:
        return None
    try:
        return int(parts[0]), int(parts[1])
    except ValueError:
        return None


def is_compatible_python(version_tuple):
    if not version_tuple:
        return False
    major, minor = version_tuple
    return major == 3 and minor in {10, 11, 12}


def select_python():
    current = (sys.version_info[0], sys.version_info[1])
    if is_compatible_python(current):
        return sys.executable
    candidates = ["python3.12", "python3.11", "python3.10", "python3", "python"]
    for candidate in candidates:
        version = get_python_version(candidate)
        if is_compatible_python(version):
            return candidate
    json_out(
        {
            "ok": False,
            "error": "未找到兼容 futu-api 的 Python 版本",
            "next_steps": [
                "请安装 Python 3.10/3.11/3.12",
                "安装后重新运行本技能",
            ],
        },
        1,
    )


def ensure_venv():
    if os.environ.get("FUTU_SKILL_VENV") == "1":
        return
    base_dir = Path(__file__).resolve().parent
    venv_dir = base_dir / ".venv"
    python_path = venv_dir / "bin" / "python"
    pip_path = venv_dir / "bin" / "pip"
    if sys.platform.startswith("win"):
        python_path = venv_dir / "Scripts" / "python.exe"
        pip_path = venv_dir / "Scripts" / "pip.exe"
    python_cmd = select_python()
    if python_path.exists():
        venv_version = get_python_version(str(python_path))
        if not is_compatible_python(venv_version):
            shutil.rmtree(venv_dir, ignore_errors=True)
    if not python_path.exists():
        subprocess.check_call([python_cmd, "-m", "venv", str(venv_dir)])
    if not pip_path.exists():
        raise RuntimeError("虚拟环境创建失败")
    requirements = base_dir / "requirements.txt"
    subprocess.check_call([str(pip_path), "install", "-r", str(requirements)])
    env = os.environ.copy()
    env["FUTU_SKILL_VENV"] = "1"
    subprocess.check_call([str(python_path), str(Path(__file__).resolve()), *sys.argv[1:]], env=env)
    sys.exit(0)


def load_futu():
    try:
        from futu import OpenSecTradeContext
    except Exception:
        OpenSecTradeContext = None
    try:
        from futu import OpenTradeContext
    except Exception:
        OpenTradeContext = None
    try:
        from futu import OpenCNTradeContext
    except Exception:
        OpenCNTradeContext = None
    from futu import (
        OpenQuoteContext,
        TrdEnv,
        TrdMarket,
        TrdSide,
        OrderType,
        OrderStatus,
        ModifyOrderOp,
    )

    def create_trade_context(host, port, trd_market):
        if OpenSecTradeContext is not None:
            return OpenSecTradeContext(filter_trdmarket=trd_market, host=host, port=port)
        trade_context = OpenTradeContext or OpenCNTradeContext
        if trade_context is None:
            json_out({"ok": False, "error": "未找到可用的交易上下文类"}, 1)
        return trade_context(host=host, port=port)

    return (
        OpenQuoteContext,
        create_trade_context,
        TrdEnv,
        TrdMarket,
        TrdSide,
        OrderType,
        OrderStatus,
        ModifyOrderOp,
    )


def get_env(name, default=None):
    value = os.environ.get(name)
    if value is None or value == "":
        return default
    return value


def parse_trd_env(trd_env):
    _, _, TrdEnv, _, _, _, _, _ = load_futu()
    env = trd_env.upper()
    if env == "REAL":
        json_out({"ok": False, "error": "本技能仅支持纸面交易，不允许 REAL"}, 1)
    if env in {"PAPER", "SIMULATE"}:
        return TrdEnv.SIMULATE
    return TrdEnv.SIMULATE


def parse_trd_market(trd_market):
    _, _, _, TrdMarket, _, _, _, _ = load_futu()
    default_market = TrdMarket.HK
    mapping = {
        "HK": getattr(TrdMarket, "HK", default_market),
        "US": getattr(TrdMarket, "US", default_market),
        "CN": getattr(TrdMarket, "CN", default_market),
        "HKCC": getattr(TrdMarket, "HKCC", default_market),
        "USCC": getattr(TrdMarket, "USCC", default_market),
    }
    return mapping.get(trd_market.upper(), default_market)


def json_out(payload, exit_code=0):
    print(json.dumps(payload, ensure_ascii=False))
    sys.exit(exit_code)


def open_contexts(host, port, trd_market):
    OpenQuoteContext, create_trade_context, _, _, _, _, _, _ = load_futu()
    quote_ctx = OpenQuoteContext(host=host, port=port)
    trade_ctx = create_trade_context(host, port, trd_market)
    return quote_ctx, trade_ctx


def close_contexts(quote_ctx, trade_ctx):
    try:
        quote_ctx.close()
    finally:
        trade_ctx.close()


def find_quote_handler(quote_ctx, names):
    for name in names:
        if hasattr(quote_ctx, name):
            return getattr(quote_ctx, name)
    return None


def find_trade_handler(trade_ctx, names):
    for name in names:
        if hasattr(trade_ctx, name):
            return getattr(trade_ctx, name)
    return None


def build_signature_params(handler, param_groups):
    signature = None
    try:
        signature = inspect.signature(handler)
    except (TypeError, ValueError):
        signature = None
    params = {}
    if signature:
        for names, value in param_groups:
            if value is None:
                continue
            for name in names:
                if name in signature.parameters:
                    params[name] = value
                    break
    return signature, params


def call_ctx_method(handler, param_groups, fallback_args):
    signature, params = build_signature_params(handler, param_groups)
    if signature:
        if params:
            return handler(**params)
        ordered_args = []
        for param in signature.parameters.values():
            if param.kind in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD):
                continue
            value = None
            for names, candidate in param_groups:
                if candidate is None:
                    continue
                if param.name in names:
                    value = candidate
                    break
            if value is None:
                if param.default is inspect._empty:
                    ordered_args = []
                    break
                continue
            ordered_args.append(value)
        if ordered_args:
            return handler(*ordered_args)
        return handler(*fallback_args)
    return handler(*fallback_args)


def normalize_period(period):
    if not period:
        return None
    mapping = {
        "Q": "QUARTER",
        "QUARTERLY": "QUARTER",
        "QUARTER": "QUARTER",
        "H": "HALF",
        "HALF": "HALF",
        "HALF_YEAR": "HALF",
        "HALFYEAR": "HALF",
        "SEMI": "HALF",
        "SEMIANNUAL": "HALF",
        "SEMI_ANNUAL": "HALF",
        "Y": "YEAR",
        "YEAR": "YEAR",
        "YEARLY": "YEAR",
        "ANNUAL": "YEAR",
        "FY": "YEAR",
    }
    upper = period.upper()
    return mapping.get(upper, upper)


def resolve_enum_value(value_name, enum_names, candidates):
    try:
        import futu
    except Exception:
        return None
    for enum_name in enum_names:
        enum_cls = getattr(futu, enum_name, None)
        if enum_cls is None:
            continue
        for candidate in candidates:
            if hasattr(enum_cls, candidate):
                return getattr(enum_cls, candidate)
    return None


def build_financial_params(handler, args, extra_params):
    params = {}
    signature = None
    try:
        signature = inspect.signature(handler)
    except (TypeError, ValueError):
        signature = None
    if signature:
        if "code" in signature.parameters:
            params["code"] = args.code
        elif "code_list" in signature.parameters:
            params["code_list"] = [args.code]
        if "start" in signature.parameters and args.start:
            params["start"] = args.start
        if "end" in signature.parameters and args.end:
            params["end"] = args.end
        period_value = extra_params.get("period")
        if period_value is not None:
            if "period" in signature.parameters:
                params["period"] = period_value
            if "report_period" in signature.parameters:
                params["report_period"] = period_value
            if "period_type" in signature.parameters:
                params["period_type"] = period_value
        report_type_value = extra_params.get("report_type")
        if report_type_value is not None:
            if "report_type" in signature.parameters:
                params["report_type"] = report_type_value
            if "type" in signature.parameters:
                params["type"] = report_type_value
        statement_value = extra_params.get("statement_type")
        if statement_value is not None:
            if "statement_type" in signature.parameters:
                params["statement_type"] = statement_value
            if "sheet_type" in signature.parameters:
                params["sheet_type"] = statement_value
    return signature, params


def load_akshare():
    try:
        import akshare as ak
    except Exception:
        json_out(
            {
                "ok": False,
                "error": "AkShare 未安装或导入失败",
                "next_steps": [
                    "请确认已安装 akshare 依赖",
                    "重新运行本技能",
                ],
            },
            1,
        )
    return ak


def normalize_akshare_code(code):
    if not code:
        return None
    lower = code.lower()
    if lower.startswith(("sh", "sz")) and len(lower) > 2:
        return lower
    if "." in code:
        market, symbol = code.split(".", 1)
        market = market.strip().upper()
        symbol = symbol.strip()
        if market in {"SH", "SZ"} and symbol:
            return f"{market.lower()}{symbol}"
        return None
    prefix = code[:2].upper()
    symbol = code[2:]
    if prefix in {"SH", "SZ"} and symbol:
        return f"{prefix.lower()}{symbol}"
    return None


def normalize_akshare_hk_code(code):
    if not code:
        return None
    if "." in code:
        market, symbol = code.split(".", 1)
        market = market.strip().upper()
        symbol = symbol.strip()
        if market == "HK" and symbol:
            return symbol
        return None
    lower = code.lower()
    if lower.startswith("hk") and len(code) > 2:
        return code[2:].strip()
    return None


def normalize_akshare_market_code(code):
    ak_code = normalize_akshare_code(code)
    if ak_code:
        return "A", ak_code
    hk_code = normalize_akshare_hk_code(code)
    if hk_code:
        return "HK", hk_code
    return None


def resolve_akshare_market_code(code):
    result = normalize_akshare_market_code(code)
    if not result:
        json_out(
            {
                "ok": False,
                "error": "AkShare 仅支持 A 股与港股财务数据",
                "next_steps": [
                    "请使用 SH./SZ. 或 HK. 股票代码",
                    "其他市场请改用支持的官方接口",
                ],
            },
            1,
        )
    return result


def find_akshare_handler(ak, names):
    for name in names:
        if hasattr(ak, name):
            return getattr(ak, name)
    return None


def call_akshare_method(handler, args_map, fallback_args):
    signature = inspect.signature(handler)
    params = {}
    if signature and signature.parameters:
        for names, value in args_map:
            for name in names:
                if name in signature.parameters:
                    params[name] = value
                    break
    if params:
        return handler(**params)
    return handler(*fallback_args)


def filter_df_by_date(df, start, end):
    if df is None or (not start and not end):
        return df
    if not hasattr(df, "columns"):
        return df
    date_col = None
    for candidate in ("报告日期", "报告期", "报告时间", "日期", "截止日期", "截止日"):
        if candidate in df.columns:
            date_col = candidate
            break
    if not date_col:
        return df
    try:
        import pandas as pd
    except Exception:
        return df
    series_dt = pd.to_datetime(df[date_col], errors="coerce")
    if series_dt.isna().all():
        return df
    mask = pd.Series([True] * len(df))
    if start:
        start_dt = pd.to_datetime(start, errors="coerce")
        if not pd.isna(start_dt):
            mask &= series_dt >= start_dt
    if end:
        end_dt = pd.to_datetime(end, errors="coerce")
        if not pd.isna(end_dt):
            mask &= series_dt <= end_dt
    return df[mask]


def akshare_financial_statement(code, statement, start, end):
    ak = load_akshare()
    try:
        market, ak_code = resolve_akshare_market_code(code)
        if market == "A":
            handler = find_akshare_handler(ak, ("stock_financial_report_sina",))
            if handler is None:
                json_out({"ok": False, "error": "AkShare 未提供 A 股财务报表接口"}, 1)
            df = call_akshare_method(
                handler,
                [(["stock", "symbol", "code"], ak_code), (["symbol", "type", "report_type"], statement)],
                [ak_code, statement],
            )
        else:
            handler = find_akshare_handler(ak, ("stock_financial_hk_report_em", "stock_hk_financial_report_em"))
            if handler is None:
                json_out(
                    {
                        "ok": False,
                        "error": "AkShare 未提供港股财务报表接口",
                        "next_steps": [
                            "请升级 akshare 版本",
                            "可尝试 financial-indicators 获取港股指标",
                        ],
                    },
                    1,
                )
            df = call_akshare_method(
                handler,
                [
                    (["symbol", "stock", "code"], ak_code),
                    (["report_type", "type", "statement_type", "sheet_type", "statement"], statement),
                ],
                [ak_code],
            )
    except Exception as exc:
        json_out({"ok": False, "error": f"AkShare 财务报表获取失败: {exc}"}, 1)
    return filter_df_by_date(df, start, end)


def akshare_financial_report_bundle(code, start, end):
    balance = akshare_financial_statement(code, "资产负债表", start, end)
    income = akshare_financial_statement(code, "利润表", start, end)
    cashflow = akshare_financial_statement(code, "现金流量表", start, end)
    return {
        "balance_sheet": balance.to_dict("records") if hasattr(balance, "to_dict") else balance,
        "income_statement": income.to_dict("records") if hasattr(income, "to_dict") else income,
        "cash_flow_statement": cashflow.to_dict("records") if hasattr(cashflow, "to_dict") else cashflow,
    }


def akshare_financial_indicators(code, start, end):
    ak = load_akshare()
    try:
        market, ak_code = resolve_akshare_market_code(code)
        if market == "A":
            handler = find_akshare_handler(ak, ("stock_financial_abstract",))
            if handler is None:
                json_out({"ok": False, "error": "AkShare 未提供 A 股财务指标接口"}, 1)
            df = call_akshare_method(handler, [(["stock", "symbol", "code"], ak_code)], [ak_code])
        else:
            handler = find_akshare_handler(ak, ("stock_hk_financial_indicator_em",))
            if handler is None:
                json_out({"ok": False, "error": "AkShare 未提供港股财务指标接口"}, 1)
            df = call_akshare_method(handler, [(["symbol", "stock", "code"], ak_code)], [ak_code])
    except Exception as exc:
        json_out({"ok": False, "error": f"AkShare 财务指标获取失败: {exc}"}, 1)
    return filter_df_by_date(df, start, end)


def call_financial_api(quote_ctx, handler_names, args, extra_params, error_message, fallback=None):
    handler = find_quote_handler(quote_ctx, handler_names)
    if handler is None:
        if fallback:
            return fallback()
        json_out(
            {
                "ok": False,
                "error": error_message,
                "next_steps": [
                    "确认 futu-api 版本是否支持该接口",
                    "如需接入其他数据源，请提供接口要求",
                ],
            },
            1,
        )
    signature, params = build_financial_params(handler, args, extra_params)
    if signature:
        if params:
            result = handler(**params)
        else:
            result = handler(args.code)
    else:
        result = handler(args.code)
    if not isinstance(result, tuple) or len(result) < 2:
        json_out({"ok": False, "error": "财务接口返回格式不符合预期"}, 1)
    ret, data = result[0], result[1]
    if ret != 0:
        json_out({"ok": False, "error": str(data)}, 1)
    payload = data.to_dict("records") if hasattr(data, "to_dict") else data
    json_out({"ok": True, "data": payload})


def cmd_quote(args):
    host = get_env("FUTU_HOST", "127.0.0.1")
    port = int(get_env("FUTU_PORT", "11111"))
    trd_market = parse_trd_market(get_env("FUTU_TRD_MARKET", "HK"))
    symbols = args.symbols
    quote_ctx, trade_ctx = open_contexts(host, port, trd_market)
    try:
        from futu import SubType

        handler = find_quote_handler(quote_ctx, ("subscribe",))
        if handler is None:
            json_out({"ok": False, "error": "当前 futu-api 未提供行情订阅接口"}, 1)
        result = call_ctx_method(
            handler,
            [
                (["code_list", "security_list", "securities", "symbol_list"], symbols),
                (["subtype_list", "sub_type_list", "sub_type", "sub_types"], [SubType.QUOTE]),
                (["is_first_push"], False),
                (["subscribe_push"], False),
            ],
            [symbols, [SubType.QUOTE], False, False],
        )
        ret, data = result
        if ret != 0:
            json_out({"ok": False, "error": str(data)}, 1)
        handler = find_quote_handler(quote_ctx, ("get_stock_quote",))
        if handler is None:
            json_out({"ok": False, "error": "当前 futu-api 未提供行情查询接口"}, 1)
        result = call_ctx_method(
            handler,
            [(["code_list", "codes", "code", "symbols"], symbols)],
            [symbols],
        )
        ret, data = result
        if ret != 0:
            json_out({"ok": False, "error": str(data)}, 1)
        payload = data.to_dict("records") if hasattr(data, "to_dict") else data
        json_out({"ok": True, "data": payload})
    finally:
        close_contexts(quote_ctx, trade_ctx)


def cmd_positions(args):
    host = get_env("FUTU_HOST", "127.0.0.1")
    port = int(get_env("FUTU_PORT", "11111"))
    trd_env = parse_trd_env(get_env("FUTU_TRD_ENV", "SIMULATE"))
    trd_market = parse_trd_market(get_env("FUTU_TRD_MARKET", "HK"))
    quote_ctx, trade_ctx = open_contexts(host, port, trd_market)
    try:
        handler = find_trade_handler(trade_ctx, ("position_list_query",))
        if handler is None:
            json_out({"ok": False, "error": "当前 futu-api 未提供持仓查询接口"}, 1)
        result = call_ctx_method(
            handler,
            [
                (["trd_env"], trd_env),
                (["position_market", "trd_market", "order_market", "deal_market"], trd_market),
            ],
            [trd_env, trd_market],
        )
        ret, data = result
        if ret != 0:
            json_out({"ok": False, "error": str(data)}, 1)
        payload = data.to_dict("records") if hasattr(data, "to_dict") else data
        json_out({"ok": True, "data": payload})
    finally:
        close_contexts(quote_ctx, trade_ctx)


def cmd_historical_kline(args):
    host = get_env("FUTU_HOST", "127.0.0.1")
    port = int(get_env("FUTU_PORT", "11111"))
    trd_market = parse_trd_market(get_env("FUTU_TRD_MARKET", "HK"))
    quote_ctx, trade_ctx = open_contexts(host, port, trd_market)
    try:
        from futu import KLType, AuType

        ktype_name = args.ktype.upper()
        ktype_map = {
            "DAY": KLType.K_DAY,
            "WEEK": KLType.K_WEEK,
            "MONTH": KLType.K_MON,
            "1M": KLType.K_1M,
            "5M": KLType.K_5M,
            "15M": KLType.K_15M,
            "30M": KLType.K_30M,
            "60M": KLType.K_60M,
        }
        ktype = ktype_map.get(ktype_name)
        if ktype is None:
            json_out({"ok": False, "error": "无效的 K 线周期"}, 1)
        autype_name = args.autype.upper()
        if not hasattr(AuType, autype_name):
            json_out({"ok": False, "error": "无效的复权类型"}, 1)
        handler = find_quote_handler(quote_ctx, ("request_history_kline",))
        if handler is None:
            json_out({"ok": False, "error": "当前 futu-api 未提供历史 K 线接口"}, 1)
        result = call_ctx_method(
            handler,
            [
                (["code", "symbol", "stock_code", "security"], args.code),
                (["start", "start_time", "start_date"], args.start),
                (["end", "end_time", "end_date"], args.end),
                (["ktype", "kl_type", "k_type"], ktype),
                (["autype", "au_type", "rehab_type"], getattr(AuType, autype_name)),
                (["max_count", "count"], int(args.max_count)),
                (["page_req_key"], args.page_req_key or None),
            ],
            [
                args.code,
                args.start,
                args.end,
                ktype,
                getattr(AuType, autype_name),
                int(args.max_count),
                args.page_req_key or None,
            ],
        )
        if not isinstance(result, tuple) or len(result) < 2:
            json_out({"ok": False, "error": "历史 K 线接口返回格式不符合预期"}, 1)
        ret, data = result[0], result[1]
        page_req_key = result[2] if len(result) > 2 else None
        if ret != 0:
            json_out({"ok": False, "error": str(data)}, 1)
        json_out({"ok": True, "data": data.to_dict("records"), "page_req_key": page_req_key})
    finally:
        close_contexts(quote_ctx, trade_ctx)


def cmd_financial_report(args):
    host = get_env("FUTU_HOST", "127.0.0.1")
    port = int(get_env("FUTU_PORT", "11111"))
    trd_market = parse_trd_market(get_env("FUTU_TRD_MARKET", "HK"))
    quote_ctx, trade_ctx = open_contexts(host, port, trd_market)
    try:
        def fallback():
            if normalize_akshare_market_code(args.code):
                payload = akshare_financial_report_bundle(args.code, args.start, args.end)
                json_out({"ok": True, "data": payload})
            json_out(
                {
                    "ok": False,
                    "error": "当前 futu-api 未提供财务报表接口",
                    "next_steps": [
                        "仅 A 股/港股可回退 AkShare",
                        "请使用 SH./SZ. 或 HK. 股票代码",
                    ],
                },
                1,
            )

        call_financial_api(
            quote_ctx,
            ("get_financial_report", "request_financial_report"),
            args,
            {"period": None, "report_type": None, "statement_type": None},
            "当前 futu-api 未提供财务报表接口",
            fallback=fallback,
        )
    finally:
        close_contexts(quote_ctx, trade_ctx)


def resolve_period_value(period):
    normalized = normalize_period(period)
    if not normalized:
        return None
    if normalized not in {"QUARTER", "HALF", "YEAR"}:
        json_out({"ok": False, "error": "无效的报表周期"}, 1)
    candidates = {
        "QUARTER": ["QUARTER", "QUARTERLY", "REPORT_QUARTER", "SEASON"],
        "HALF": ["HALF", "HALF_YEAR", "HALFYEAR", "SEMI", "SEMIANNUAL", "SEMI_ANNUAL"],
        "YEAR": ["YEAR", "ANNUAL", "FULL_YEAR", "FY", "YEARLY"],
    }
    enum_value = resolve_enum_value(
        normalized,
        ["FinancialPeriod", "FinancialReportPeriod", "ReportPeriod", "PeriodType", "FinancialPeriodType"],
        candidates.get(normalized, [normalized]),
    )
    return enum_value if enum_value is not None else normalized


def resolve_statement_value(statement):
    candidates = {
        "BALANCE": ["BALANCE_SHEET", "BALANCE", "BS"],
        "INCOME": ["INCOME_STATEMENT", "INCOME", "PROFIT", "P_L", "PL"],
        "CASHFLOW": ["CASH_FLOW", "CASHFLOW", "CASH_FLOW_STATEMENT", "CF"],
    }
    enum_value = resolve_enum_value(
        statement,
        ["FinancialStatementType", "StatementType", "FinancialReportType", "ReportType"],
        candidates.get(statement, [statement]),
    )
    return enum_value if enum_value is not None else statement


def resolve_indicator_value():
    enum_value = resolve_enum_value(
        "INDICATOR",
        ["FinancialReportType", "ReportType", "FinancialDataType", "FinancialType"],
        [
            "FINANCIAL_DATA",
            "FINANCIAL_SUMMARY",
            "BASIC_FINANCIAL",
            "FINANCIAL_RATIO",
            "FINANCIAL_INDICATOR",
            "INDICATOR",
            "FINANCIAL_METRIC",
        ],
    )
    return enum_value


def cmd_financial_indicators(args):
    host = get_env("FUTU_HOST", "127.0.0.1")
    port = int(get_env("FUTU_PORT", "11111"))
    trd_market = parse_trd_market(get_env("FUTU_TRD_MARKET", "HK"))
    quote_ctx, trade_ctx = open_contexts(host, port, trd_market)
    try:
        def fallback():
            if normalize_akshare_market_code(args.code):
                df = akshare_financial_indicators(args.code, args.start, args.end)
                payload = df.to_dict("records") if hasattr(df, "to_dict") else df
                json_out({"ok": True, "data": payload})
            json_out(
                {
                    "ok": False,
                    "error": "当前 futu-api 未提供财务指标接口",
                    "next_steps": [
                        "仅 A 股/港股可回退 AkShare",
                        "请使用 SH./SZ. 或 HK. 股票代码",
                    ],
                },
                1,
            )

        period_value = resolve_period_value(args.period)
        report_type_value = resolve_indicator_value()
        call_financial_api(
            quote_ctx,
            ("get_financial", "get_financial_data", "get_financial_summary", "get_stock_financial"),
            args,
            {"period": period_value, "report_type": report_type_value, "statement_type": None},
            "当前 futu-api 未提供财务指标接口",
            fallback=fallback,
        )
    finally:
        close_contexts(quote_ctx, trade_ctx)


def cmd_financial_balance(args):
    host = get_env("FUTU_HOST", "127.0.0.1")
    port = int(get_env("FUTU_PORT", "11111"))
    trd_market = parse_trd_market(get_env("FUTU_TRD_MARKET", "HK"))
    quote_ctx, trade_ctx = open_contexts(host, port, trd_market)
    try:
        def fallback():
            if normalize_akshare_market_code(args.code):
                df = akshare_financial_statement(args.code, "资产负债表", args.start, args.end)
                payload = df.to_dict("records") if hasattr(df, "to_dict") else df
                json_out({"ok": True, "data": payload})
            json_out(
                {
                    "ok": False,
                    "error": "当前 futu-api 未提供资产负债表接口",
                    "next_steps": [
                        "仅 A 股/港股可回退 AkShare",
                        "请使用 SH./SZ. 或 HK. 股票代码",
                    ],
                },
                1,
            )

        period_value = resolve_period_value(args.period)
        statement_value = resolve_statement_value("BALANCE")
        call_financial_api(
            quote_ctx,
            ("get_financial_report", "request_financial_report", "get_financial_statement"),
            args,
            {"period": period_value, "report_type": statement_value, "statement_type": statement_value},
            "当前 futu-api 未提供资产负债表接口",
            fallback=fallback,
        )
    finally:
        close_contexts(quote_ctx, trade_ctx)


def cmd_financial_income(args):
    host = get_env("FUTU_HOST", "127.0.0.1")
    port = int(get_env("FUTU_PORT", "11111"))
    trd_market = parse_trd_market(get_env("FUTU_TRD_MARKET", "HK"))
    quote_ctx, trade_ctx = open_contexts(host, port, trd_market)
    try:
        def fallback():
            if normalize_akshare_market_code(args.code):
                df = akshare_financial_statement(args.code, "利润表", args.start, args.end)
                payload = df.to_dict("records") if hasattr(df, "to_dict") else df
                json_out({"ok": True, "data": payload})
            json_out(
                {
                    "ok": False,
                    "error": "当前 futu-api 未提供利润表接口",
                    "next_steps": [
                        "仅 A 股/港股可回退 AkShare",
                        "请使用 SH./SZ. 或 HK. 股票代码",
                    ],
                },
                1,
            )

        period_value = resolve_period_value(args.period)
        statement_value = resolve_statement_value("INCOME")
        call_financial_api(
            quote_ctx,
            ("get_financial_report", "request_financial_report", "get_financial_statement"),
            args,
            {"period": period_value, "report_type": statement_value, "statement_type": statement_value},
            "当前 futu-api 未提供利润表接口",
            fallback=fallback,
        )
    finally:
        close_contexts(quote_ctx, trade_ctx)


def cmd_financial_cashflow(args):
    host = get_env("FUTU_HOST", "127.0.0.1")
    port = int(get_env("FUTU_PORT", "11111"))
    trd_market = parse_trd_market(get_env("FUTU_TRD_MARKET", "HK"))
    quote_ctx, trade_ctx = open_contexts(host, port, trd_market)
    try:
        def fallback():
            if normalize_akshare_market_code(args.code):
                df = akshare_financial_statement(args.code, "现金流量表", args.start, args.end)
                payload = df.to_dict("records") if hasattr(df, "to_dict") else df
                json_out({"ok": True, "data": payload})
            json_out(
                {
                    "ok": False,
                    "error": "当前 futu-api 未提供现金流量表接口",
                    "next_steps": [
                        "仅 A 股/港股可回退 AkShare",
                        "请使用 SH./SZ. 或 HK. 股票代码",
                    ],
                },
                1,
            )

        period_value = resolve_period_value(args.period)
        statement_value = resolve_statement_value("CASHFLOW")
        call_financial_api(
            quote_ctx,
            ("get_financial_report", "request_financial_report", "get_financial_statement"),
            args,
            {"period": period_value, "report_type": statement_value, "statement_type": statement_value},
            "当前 futu-api 未提供现金流量表接口",
            fallback=fallback,
        )
    finally:
        close_contexts(quote_ctx, trade_ctx)


def cmd_today_pnl(args):
    host = get_env("FUTU_HOST", "127.0.0.1")
    port = int(get_env("FUTU_PORT", "11111"))
    trd_env = parse_trd_env(get_env("FUTU_TRD_ENV", "SIMULATE"))
    trd_market = parse_trd_market(get_env("FUTU_TRD_MARKET", "HK"))
    quote_ctx, trade_ctx = open_contexts(host, port, trd_market)
    try:
        def parse_number(value):
            if value is None:
                return None
            if isinstance(value, str):
                stripped = value.strip()
                if stripped == "" or stripped.upper() == "N/A":
                    return None
                try:
                    return float(stripped)
                except ValueError:
                    return None
            try:
                return float(value)
            except (TypeError, ValueError):
                return None

        handler = find_trade_handler(trade_ctx, ("position_list_query",))
        if handler is None:
            json_out({"ok": False, "error": "当前 futu-api 未提供持仓查询接口"}, 1)
        result = call_ctx_method(
            handler,
            [
                (["trd_env"], trd_env),
                (["position_market", "trd_market", "order_market", "deal_market"], trd_market),
                (["refresh_cache"], args.refresh_cache),
            ],
            [trd_env, trd_market, args.refresh_cache],
        )
        ret, data = result
        if ret != 0:
            json_out({"ok": False, "error": str(data)}, 1)
        records = data.to_dict("records")
        total_today_pl = 0.0
        total_market_val = 0.0
        for row in records:
            today_pl = parse_number(row.get("today_pl_val"))
            market_val = parse_number(row.get("market_val"))
            if today_pl is not None:
                total_today_pl += today_pl
            if market_val is not None:
                total_market_val += market_val
        today_pl_ratio = None
        if total_market_val:
            today_pl_ratio = total_today_pl / total_market_val
        json_out(
            {
                "ok": True,
                "data": {
                    "today_pl_val": total_today_pl,
                    "today_pl_ratio": today_pl_ratio,
                    "positions": records,
                },
            }
        )
    finally:
        close_contexts(quote_ctx, trade_ctx)


def unlock_trade(trade_ctx):
    _, _, _, _, _, _, _, _ = load_futu()
    password = get_env("FUTU_TRADE_PWD", get_env("FUTU_PASSWORD", ""))
    if not password:
        json_out({"ok": False, "error": "缺少 FUTU_TRADE_PWD"}, 1)
    handler = find_trade_handler(trade_ctx, ("unlock_trade",))
    if handler is None:
        json_out({"ok": False, "error": "当前 futu-api 未提供交易解锁接口"}, 1)
    result = call_ctx_method(
        handler,
        [(["password", "pwd", "unlock_password"], password)],
        [password],
    )
    ret, data = result
    if ret != 0:
        json_out({"ok": False, "error": str(data)}, 1)


def cmd_order(args, side):
    host = get_env("FUTU_HOST", "127.0.0.1")
    port = int(get_env("FUTU_PORT", "11111"))
    trd_env = parse_trd_env(get_env("FUTU_TRD_ENV", "SIMULATE"))
    trd_market = parse_trd_market(get_env("FUTU_TRD_MARKET", "HK"))
    symbol = args.symbol
    price = float(args.price)
    qty = int(args.qty)
    order_type = args.order_type.lower()
    _, _, _, _, TrdSide, OrderType, _, _ = load_futu()
    quote_ctx, trade_ctx = open_contexts(host, port, trd_market)
    try:
        unlock_trade(trade_ctx)
        if order_type == "market":
            order_type_value = OrderType.MARKET
        else:
            order_type_value = OrderType.NORMAL
        handler = find_trade_handler(trade_ctx, ("place_order",))
        if handler is None:
            json_out({"ok": False, "error": "当前 futu-api 未提供下单接口"}, 1)
        result = call_ctx_method(
            handler,
            [
                (["price"], price),
                (["qty", "quantity"], qty),
                (["code", "symbol", "stock_code"], symbol),
                (["trd_side", "side"], TrdSide.BUY if side == "buy" else TrdSide.SELL),
                (["order_type", "order_type_value", "order_type_enum"], order_type_value),
                (["trd_env"], trd_env),
                (["trd_market", "order_market"], trd_market),
            ],
            [price, qty, symbol, TrdSide.BUY if side == "buy" else TrdSide.SELL, order_type_value, trd_env, trd_market],
        )
        ret, data = result
        if ret != 0:
            json_out({"ok": False, "error": str(data)}, 1)
        json_out({"ok": True, "data": data.to_dict("records")})
    finally:
        close_contexts(quote_ctx, trade_ctx)


def parse_status_filter(status):
    _, _, _, _, _, _, OrderStatus, _ = load_futu()
    if status.lower() in {"all", "any"}:
        return []
    name = status.upper()
    if hasattr(OrderStatus, name):
        return [getattr(OrderStatus, name)]
    return None


def cmd_orders(args):
    host = get_env("FUTU_HOST", "127.0.0.1")
    port = int(get_env("FUTU_PORT", "11111"))
    trd_env = parse_trd_env(get_env("FUTU_TRD_ENV", "SIMULATE"))
    trd_market = parse_trd_market(get_env("FUTU_TRD_MARKET", "HK"))
    status_filter = parse_status_filter(args.status)
    if status_filter is None:
        json_out({"ok": False, "error": "无效的订单状态"}, 1)
    quote_ctx, trade_ctx = open_contexts(host, port, trd_market)
    try:
        handler = find_trade_handler(trade_ctx, ("order_list_query",))
        if handler is None:
            json_out({"ok": False, "error": "当前 futu-api 未提供订单查询接口"}, 1)
        result = call_ctx_method(
            handler,
            [
                (["order_id"], args.order_id or ""),
                (["order_market", "trd_market"], trd_market),
                (["status_filter_list", "status_filter"], status_filter),
                (["code", "symbol", "stock_code"], args.symbol or ""),
                (["start", "start_time", "start_date"], args.start or ""),
                (["end", "end_time", "end_date"], args.end or ""),
                (["trd_env"], trd_env),
                (["refresh_cache"], args.refresh_cache),
            ],
            [
                args.order_id or "",
                status_filter,
                args.symbol or "",
                args.start or "",
                args.end or "",
                trd_env,
                trd_market,
                args.refresh_cache,
            ],
        )
        ret, data = result
        if ret != 0:
            json_out({"ok": False, "error": str(data)}, 1)
        json_out({"ok": True, "data": data.to_dict("records")})
    finally:
        close_contexts(quote_ctx, trade_ctx)


def cmd_cancel(args):
    host = get_env("FUTU_HOST", "127.0.0.1")
    port = int(get_env("FUTU_PORT", "11111"))
    trd_env = parse_trd_env(get_env("FUTU_TRD_ENV", "SIMULATE"))
    _, _, _, _, _, _, _, ModifyOrderOp = load_futu()
    trd_market = parse_trd_market(get_env("FUTU_TRD_MARKET", "HK"))
    quote_ctx, trade_ctx = open_contexts(host, port, trd_market)
    try:
        unlock_trade(trade_ctx)
        handler = find_trade_handler(trade_ctx, ("modify_order",))
        if handler is None:
            json_out({"ok": False, "error": "当前 futu-api 未提供改撤单接口"}, 1)
        result = call_ctx_method(
            handler,
            [
                (["modify_order_op", "modify_op", "op"], ModifyOrderOp.CANCEL),
                (["order_id"], args.order_id),
                (["qty", "quantity"], 0),
                (["price"], 0),
                (["trd_env"], trd_env),
                (["trd_market", "order_market"], trd_market),
            ],
            [ModifyOrderOp.CANCEL, args.order_id, 0, 0, trd_env, trd_market],
        )
        ret, data = result
        if ret != 0:
            json_out({"ok": False, "error": str(data)}, 1)
        json_out({"ok": True, "data": data.to_dict("records")})
    finally:
        close_contexts(quote_ctx, trade_ctx)


def cmd_fills(args):
    host = get_env("FUTU_HOST", "127.0.0.1")
    port = int(get_env("FUTU_PORT", "11111"))
    trd_env = parse_trd_env(get_env("FUTU_TRD_ENV", "SIMULATE"))
    trd_market = parse_trd_market(get_env("FUTU_TRD_MARKET", "HK"))
    days = int(args.days)
    _, _, TrdEnv, _, _, _, _, _ = load_futu()
    quote_ctx, trade_ctx = open_contexts(host, port, trd_market)
    try:
        if days <= 1:
            handler = find_trade_handler(trade_ctx, ("deal_list_query",))
            if handler is None:
                json_out({"ok": False, "error": "当前 futu-api 未提供成交查询接口"}, 1)
            result = call_ctx_method(
                handler,
                [
                    (["code", "symbol", "stock_code"], args.symbol or ""),
                    (["deal_market", "trd_market", "order_market"], trd_market),
                    (["trd_env"], trd_env),
                    (["refresh_cache"], args.refresh_cache),
                ],
                [args.symbol or "", trd_market, trd_env, args.refresh_cache],
            )
            ret, data = result
        else:
            if trd_env == TrdEnv.SIMULATE:
                json_out({"ok": False, "error": "纸面交易环境不支持历史成交查询"}, 1)
            from datetime import datetime, timedelta

            end_date = datetime.now()
            start_date = end_date - timedelta(days=days - 1)
            handler = find_trade_handler(trade_ctx, ("history_deal_list_query",))
            if handler is None:
                json_out({"ok": False, "error": "当前 futu-api 未提供历史成交接口"}, 1)
            result = call_ctx_method(
                handler,
                [
                    (["code", "symbol", "stock_code"], args.symbol or ""),
                    (["deal_market", "trd_market", "order_market"], trd_market),
                    (["start", "start_time", "start_date"], start_date.strftime("%Y-%m-%d")),
                    (["end", "end_time", "end_date"], end_date.strftime("%Y-%m-%d")),
                    (["trd_env"], trd_env),
                ],
                [
                    args.symbol or "",
                    trd_market,
                    start_date.strftime("%Y-%m-%d"),
                    end_date.strftime("%Y-%m-%d"),
                    trd_env,
                ],
            )
            ret, data = result
        if ret != 0:
            json_out({"ok": False, "error": str(data)}, 1)
        json_out({"ok": True, "data": data.to_dict("records")})
    finally:
        close_contexts(quote_ctx, trade_ctx)


def cmd_check(args):
    host = get_env("FUTU_HOST", "127.0.0.1")
    port = int(get_env("FUTU_PORT", "11111"))
    trd_market = parse_trd_market(get_env("FUTU_TRD_MARKET", "HK"))
    download_url = "https://www.futuhk.com/en/support/topic1_464"
    quote_ctx, trade_ctx = open_contexts(host, port, trd_market)
    try:
        handler = find_quote_handler(quote_ctx, ("get_global_state",))
        if handler is None:
            json_out({"ok": False, "error": "当前 futu-api 未提供全局状态接口"}, 1)
        result = call_ctx_method(handler, [], [])
        ret, data = result
        if ret != 0:
            json_out(
                {
                    "ok": False,
                    "error": str(data),
                    "next_steps": [
                        "请确认 FutuOpenD 已启动并保持运行",
                        "下载入口: " + download_url,
                        "命令行登录示例: ./FutuOpenD -login_account=YOUR_ID -login_pwd=YOUR_PASSWORD",
                        "避免使用 XML 保存密码",
                    ],
                },
                1,
            )
        payload = data.to_dict("records") if hasattr(data, "to_dict") else data
        json_out({"ok": True, "data": payload})
    except Exception as exc:
        json_out(
            {
                "ok": False,
                "error": str(exc),
                "next_steps": [
                    "请确认 FutuOpenD 已启动并保持运行",
                    "下载入口: " + download_url,
                    "命令行登录示例: ./FutuOpenD -login_account=YOUR_ID -login_pwd=YOUR_PASSWORD",
                    "避免使用 XML 保存密码",
                ],
            },
            1,
        )
    finally:
        close_contexts(quote_ctx, trade_ctx)


def cmd_funds(args):
    host = get_env("FUTU_HOST", "127.0.0.1")
    port = int(get_env("FUTU_PORT", "11111"))
    trd_env = parse_trd_env(get_env("FUTU_TRD_ENV", "SIMULATE"))
    trd_market = parse_trd_market(get_env("FUTU_TRD_MARKET", "HK"))
    _, _, _, _, _, _, _, _ = load_futu()
    quote_ctx, trade_ctx = open_contexts(host, port, trd_market)
    try:
        handler = find_trade_handler(trade_ctx, ("accinfo_query",))
        if handler is None:
            json_out({"ok": False, "error": "当前 futu-api 未提供资金查询接口"}, 1)
        result = call_ctx_method(
            handler,
            [
                (["trd_env"], trd_env),
                (["refresh_cache"], args.refresh_cache),
            ],
            [trd_env, args.refresh_cache],
        )
        ret, data = result
        if ret != 0:
            json_out({"ok": False, "error": str(data)}, 1)
        json_out({"ok": True, "data": data.to_dict("records")})
    finally:
        close_contexts(quote_ctx, trade_ctx)


def build_parser():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    quote = sub.add_parser("quote")
    quote.add_argument("--symbols", nargs="+", required=True)
    quote.set_defaults(func=cmd_quote)

    positions = sub.add_parser("positions")
    positions.set_defaults(func=cmd_positions)

    historical_kline = sub.add_parser("historical-kline")
    historical_kline.add_argument("--code", required=True)
    historical_kline.add_argument("--start", required=True)
    historical_kline.add_argument("--end", required=True)
    historical_kline.add_argument("--max-count", default="1000")
    historical_kline.add_argument("--ktype", default="DAY")
    historical_kline.add_argument("--autype", default="QFQ")
    historical_kline.add_argument("--page-req-key")
    historical_kline.set_defaults(func=cmd_historical_kline)

    financial_report = sub.add_parser("financial-report")
    financial_report.add_argument("--code", required=True)
    financial_report.add_argument("--start")
    financial_report.add_argument("--end")
    financial_report.set_defaults(func=cmd_financial_report)

    financial_indicators = sub.add_parser("financial-indicators")
    financial_indicators.add_argument("--code", required=True)
    financial_indicators.add_argument("--period", default="QUARTER")
    financial_indicators.add_argument("--start")
    financial_indicators.add_argument("--end")
    financial_indicators.set_defaults(func=cmd_financial_indicators)

    financial_balance = sub.add_parser("financial-balance")
    financial_balance.add_argument("--code", required=True)
    financial_balance.add_argument("--period", default="QUARTER")
    financial_balance.add_argument("--start")
    financial_balance.add_argument("--end")
    financial_balance.set_defaults(func=cmd_financial_balance)

    financial_income = sub.add_parser("financial-income")
    financial_income.add_argument("--code", required=True)
    financial_income.add_argument("--period", default="QUARTER")
    financial_income.add_argument("--start")
    financial_income.add_argument("--end")
    financial_income.set_defaults(func=cmd_financial_income)

    financial_cashflow = sub.add_parser("financial-cashflow")
    financial_cashflow.add_argument("--code", required=True)
    financial_cashflow.add_argument("--period", default="QUARTER")
    financial_cashflow.add_argument("--start")
    financial_cashflow.add_argument("--end")
    financial_cashflow.set_defaults(func=cmd_financial_cashflow)

    today_pnl = sub.add_parser("today-pnl")
    today_pnl.add_argument("--refresh-cache", action="store_true")
    today_pnl.set_defaults(func=cmd_today_pnl)

    buy = sub.add_parser("buy")
    buy.add_argument("--symbol", required=True)
    buy.add_argument("--qty", required=True)
    buy.add_argument("--price", required=True)
    buy.add_argument("--order-type", default="limit")
    buy.set_defaults(func=lambda args: cmd_order(args, "buy"))

    sell = sub.add_parser("sell")
    sell.add_argument("--symbol", required=True)
    sell.add_argument("--qty", required=True)
    sell.add_argument("--price", required=True)
    sell.add_argument("--order-type", default="limit")
    sell.set_defaults(func=lambda args: cmd_order(args, "sell"))

    orders = sub.add_parser("orders")
    orders.add_argument("--status", default="all")
    orders.add_argument("--symbol")
    orders.add_argument("--order-id")
    orders.add_argument("--start")
    orders.add_argument("--end")
    orders.add_argument("--refresh-cache", action="store_true")
    orders.set_defaults(func=cmd_orders)

    cancel = sub.add_parser("cancel")
    cancel.add_argument("--order-id", required=True)
    cancel.set_defaults(func=cmd_cancel)

    fills = sub.add_parser("fills")
    fills.add_argument("--days", default="1")
    fills.add_argument("--symbol")
    fills.add_argument("--refresh-cache", action="store_true")
    fills.set_defaults(func=cmd_fills)

    check = sub.add_parser("check")
    check.set_defaults(func=cmd_check)

    funds = sub.add_parser("funds")
    funds.add_argument("--refresh-cache", action="store_true")
    funds.set_defaults(func=cmd_funds)
    return parser


def main():
    ensure_venv()
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        json_out({"ok": False, "error": str(exc)}, 1)
