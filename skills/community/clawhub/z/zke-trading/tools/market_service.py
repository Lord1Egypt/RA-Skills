from typing import Any

def get_registry(public_api):
    from tools.symbol_utils import SpotSymbolRegistry
    symbols_data = public_api.symbols()
    return SpotSymbolRegistry(symbols_data)


def _resolve_symbols(registry, symbol: Any):
    """
    核心解析层：拦截空参数，确保传给 registry 的一定是合法字符串
    """
    safe_symbol = str(symbol).strip() if symbol is not None else ""
    if not safe_symbol:
        raise ValueError("交易对 symbol 不能为空")
        
    api_symbol = registry.get_api_symbol(safe_symbol)
    display_symbol = registry.get_display_symbol(safe_symbol)
    return api_symbol, display_symbol


def get_ticker(public_api, registry, symbol: Any):
    api_symbol, _ = _resolve_symbols(registry, symbol)
    return public_api.ticker(api_symbol)


def get_ticker_pretty_data(public_api, registry, symbol: Any):
    api_symbol, display_symbol = _resolve_symbols(registry, symbol)
    ticker_data = public_api.ticker(api_symbol)
    return display_symbol, ticker_data


def get_depth(public_api, registry, symbol: Any, limit: Any = 20):
    api_symbol, _ = _resolve_symbols(registry, symbol)
    # 【AI 加固】防止 limit 传入空字符串或 None，确保转为安全整数
    safe_limit = int(limit) if limit is not None and str(limit).strip() != "" else 20
    return public_api.depth(api_symbol, safe_limit)


def get_depth_pretty_data(public_api, registry, symbol: Any, limit: Any = 10):
    api_symbol, display_symbol = _resolve_symbols(registry, symbol)
    safe_limit = int(limit) if limit is not None and str(limit).strip() != "" else 10
    depth_data = public_api.depth(api_symbol, safe_limit)
    return display_symbol, depth_data


def get_trades(public_api, registry, symbol: Any, limit: Any = 20):
    api_symbol, _ = _resolve_symbols(registry, symbol)
    safe_limit = int(limit) if limit is not None and str(limit).strip() != "" else 20
    return public_api.trades(api_symbol, safe_limit)


def get_trades_pretty_data(public_api, registry, symbol: Any, limit: Any = 20):
    api_symbol, display_symbol = _resolve_symbols(registry, symbol)
    safe_limit = int(limit) if limit is not None and str(limit).strip() != "" else 20
    trades = public_api.trades(api_symbol, safe_limit)
    return display_symbol, trades


def get_my_trades_pretty_data(private_api, registry, symbol: Any, limit: Any = 10):
    api_symbol, display_symbol = _resolve_symbols(registry, symbol)
    safe_limit = int(limit) if limit is not None and str(limit).strip() != "" else 10
    trades = private_api.my_trades(api_symbol, safe_limit)
    return display_symbol, trades


def get_klines(public_api, registry, symbol: Any, interval: Any):
    api_symbol, _ = _resolve_symbols(registry, symbol)
    safe_interval = str(interval).strip() if interval is not None else ""
    return public_api.klines(api_symbol, safe_interval)


def get_klines_pretty_data(public_api, registry, symbol: Any, interval: Any):
    api_symbol, display_symbol = _resolve_symbols(registry, symbol)
    safe_interval = str(interval).strip() if interval is not None else ""
    klines = public_api.klines(api_symbol, safe_interval)
    return display_symbol, klines
