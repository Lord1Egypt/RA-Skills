#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
股票数据工具函数 - stock_utils.py

核心规则（resolve_ths_code）：
  ┌─────────────────────────────────────────────────────────────┐
  │ 只有以下两种格式可以直接使用，无需查询：                      │
  │   USHA + 6位数字  →  如 USHA600519（上交所A股）              │
  │   USZA + 6位数字  →  如 USZA000001（深交所A股）              │
  │                                                             │
  │ 其余所有输入（短代码/中文/缩写/其他前缀/混合格式等）          │
  │ 一律先调用 search_symbols() 查询候选列表，                   │
  │ 获取完整的 ths_code 后再进行后续操作。                       │
  └─────────────────────────────────────────────────────────────┘

多条A股结果时返回候选列表，由 AI 助手展示给用户选择。
"""

import re
import sys
import subprocess
import time
import pandas as pd
from typing import Dict, List, Optional, Union

# ─────────────────────────────────────────────
# thsdk 版本要求
# ─────────────────────────────────────────────
THSDK_MIN_VERSION = "1.7.14"

def check_thsdk_installed() -> bool:
    """检查 thsdk 是否已安装"""
    try:
        import thsdk
        return True
    except ImportError:
        return False

def get_thsdk_version() -> str:
    """获取当前 thsdk 版本"""
    try:
        import thsdk
        return getattr(thsdk, '__version__', 'unknown')
    except ImportError:
        return 'not installed'

def install_thsdk(version: str = None) -> bool:
    """
    安装或升级 thsdk 库
    
    Args:
        version: 指定版本号，如 "1.7.14"。如果为 None，则安装最新版
        
    Returns:
        bool: 安装是否成功
    """
    try:
        pkg = f"thsdk=={version}" if version else "thsdk"
        print(f"[stock_utils] 正在安装 {pkg}...")
        
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "--upgrade", pkg],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print(f"[stock_utils] ✅ thsdk 安装成功")
            return True
        else:
            print(f"[stock_utils] ❌ thsdk 安装失败: {result.stderr}")
            return False
    except Exception as e:
        print(f"[stock_utils] ❌ thsdk 安装异常: {e}")
        return False

def ensure_thsdk() -> bool:
    """
    确保 thsdk 已安装且版本满足要求
    如果未安装或版本过低，自动安装最新版本
    
    Returns:
        bool: 是否满足要求
    """
    try:
        import thsdk
        # 检查版本
        version = getattr(thsdk, '__version__', '0.0.0')
        
        # 简单版本比较（假设版本号格式为 x.y.z）
        try:
            v_parts = [int(x) for x in version.split('.')]
            min_parts = [int(x) for x in THSDK_MIN_VERSION.split('.')]
            
            if v_parts < min_parts:
                print(f"[stock_utils] thsdk 版本过低 ({version} < {THSDK_MIN_VERSION})，正在升级...")
                return install_thsdk()
        except:
            pass  # 版本比较失败，假设满足要求
        
        return True
    except ImportError:
        print(f"[stock_utils] thsdk 未安装，正在安装...")
        return install_thsdk()

def get_ths_instance():
    """
    获取 THS 实例，自动处理 thsdk 安装
    
    Returns:
        THS 实例或 None
    """
    if not ensure_thsdk():
        return None
    
    try:
        from thsdk import THS
        return THS()
    except ImportError as e:
        print(f"[stock_utils] ❌ 导入 thsdk 失败: {e}")
        return None


# ─────────────────────────────────────────────
# 限频常量
# ─────────────────────────────────────────────
_SLEEP_SEARCH = 0.1  # search_symbols 查询间隔

# 合法 ths_code 直通白名单（只有这两种格式跳过查询）
_DIRECT_PATTERN = re.compile(r'^(USHA|USZA)\d{6}$', re.IGNORECASE)

# 特殊返回值：表示需要用户选择
NEED_USER_SELECTION = "NEED_USER_SELECTION"


def _is_direct_code(code: str) -> bool:
    """
    判断是否满足"直通"条件：
      USHA + 6位数字  或  USZA + 6位数字
    满足则无需查询，直接返回大写形式。
    """
    return bool(_DIRECT_PATTERN.match(code))


def _search_symbols(ths, query: str, retries: int = 3) -> List[Dict]:
    """
    调用 search_symbols 搜索股票，返回候选列表。
    每项格式：{'ths_code': 'USZA300750', 'name': '宁德时代', 'code': '300750', 'market': '深A'}
    
    search_symbols 返回数据格式：
    {
        'MarketStr': 'USZA',
        'Code': '300750',
        'Name': '宁德时代',
        'CodeDisplay': '300750',
        'MarketDisplay': '深A',
        'THSCODE': 'USZA300750'
    }
    """
    candidates = []
    for attempt in range(retries):
        time.sleep(_SLEEP_SEARCH)
        try:
            resp = ths.search_symbols(query)
            if not resp.success or not resp.data:
                continue
            for item in resp.data:
                ths_code = item.get('THSCODE', '')
                name = item.get('Name', '')
                code = item.get('Code', '')
                market = item.get('MarketDisplay', '')
                
                if not ths_code:
                    continue
                    
                candidates.append({
                    'ths_code': ths_code,
                    'name': name,
                    'code': code,
                    'market': market,
                })
            break  # 成功则不重试
        except Exception as e:
            print(f'[stock_utils] search_symbols 异常 (尝试 {attempt + 1}/{retries}): {e}')
            continue
    return candidates


def _format_candidates_for_display(candidates: List[Dict], title: str = "匹配结果") -> str:
    """
    将候选列表格式化为易读的字符串，供 AI 展示给用户。
    """
    lines = [f"\n**{title}**：\n"]
    for i, c in enumerate(candidates):
        lines.append(f"  {i + 1}. **{c['name']}** `{c['ths_code']}` ({c['market']})")
    lines.append(f"\n请输入序号选择（1-{len(candidates)}），或输入 0 取消。")
    return "\n".join(lines)


# ─────────────────────────────────────────────
# 核心公开函数
# ─────────────────────────────────────────────

def search_stock_candidates(ths, user_input: str) -> Dict:
    """
    搜索股票并返回候选结果（供 AI 调用，不自动选择）。
    
    返回格式：
    {
        'status': 'found' | 'not_found' | 'need_selection',
        'ths_code': 'USZA300750' | None,  # 唯一匹配时返回
        'candidates': [...],  # 多条结果时返回候选列表
        'message': '...',     # 给用户的提示信息
        'display': '...'      # 格式化的展示文本
    }
    """
    code = user_input.strip()
    
    # ── 直通：USHA/USZA + 6位数字 ──────────
    if _is_direct_code(code):
        return {
            'status': 'found',
            'ths_code': code.upper(),
            'candidates': [],
            'message': f'直通模式，无需查询',
            'display': f'股票代码：`{code.upper()}`'
        }
    
    # ── 搜索 ─────────────────────────────
    candidates = _search_symbols(ths, code)
    
    if not candidates:
        return {
            'status': 'not_found',
            'ths_code': None,
            'candidates': [],
            'message': f'未找到与 "{code}" 匹配的证券',
            'display': f'❌ 未找到与 "{code}" 匹配的证券，请检查输入。'
        }
    
    # 单条结果，自动匹配
    if len(candidates) == 1:
        c = candidates[0]
        return {
            'status': 'found',
            'ths_code': c['ths_code'],
            'candidates': [],
            'message': f'已自动匹配：{c["name"]}',
            'display': f'✅ 已自动匹配：**{c["name"]}** `{c["ths_code"]}` ({c["market"]})'
        }
    
    # 多条结果，筛选A股
    a_stock_candidates = [c for c in candidates if c['market'] in ('深A', '沪A')]
    
    # 只有一只A股，自动选择
    if len(a_stock_candidates) == 1:
        c = a_stock_candidates[0]
        return {
            'status': 'found',
            'ths_code': c['ths_code'],
            'candidates': [],
            'message': f'自动选择唯一A股：{c["name"]}',
            'display': f'✅ 找到唯一A股，自动选择：**{c["name"]}** `{c["ths_code"]}` ({c["market"]})'
        }
    
    # 多只A股，需要用户选择
    if len(a_stock_candidates) > 1:
        display = _format_candidates_for_display(a_stock_candidates, f'找到 {len(a_stock_candidates)} 只A股')
        return {
            'status': 'need_selection',
            'ths_code': None,
            'candidates': a_stock_candidates,
            'message': f'找到 {len(a_stock_candidates)} 只A股，请选择',
            'display': display
        }
    
    # 无A股，展示所有结果
    display = _format_candidates_for_display(candidates, f'找到 {len(candidates)} 个匹配结果')
    return {
        'status': 'need_selection',
        'ths_code': None,
        'candidates': candidates,
        'message': f'找到 {len(candidates)} 个匹配结果，请选择',
        'display': display
    }


def get_candidate_by_index(candidates: List[Dict], index: int) -> Optional[Dict]:
    """
    根据用户输入的序号获取候选股票。
    index: 1-based 索引
    
    返回：
        {'ths_code': '...', 'name': '...', 'code': '...', 'market': '...'} 或 None
    """
    if 1 <= index <= len(candidates):
        return candidates[index - 1]
    return None


def resolve_ths_code(ths, user_input: str) -> Union[str, Dict, None]:
    """
    将任意格式的股票标识符解析为合法的 ths_code。
    
    返回值：
      - 字符串：ths_code（唯一匹配或直通）
      - Dict：{'need_selection': True, 'candidates': [...], 'display': '...'}
      - None：未找到
    
    此函数保持向后兼容，但推荐使用 search_stock_candidates() 获取更详细的结果。
    """
    result = search_stock_candidates(ths, user_input)
    
    if result['status'] == 'found':
        return result['ths_code']
    elif result['status'] == 'need_selection':
        return {
            'need_selection': True,
            'candidates': result['candidates'],
            'display': result['display']
        }
    else:
        return None


# ─────────────────────────────────────────────
# 数据获取封装
# ─────────────────────────────────────────────

def get_kline_data(ths, stock_code: str, interval: str = "day",
                   count: int = 100, adjust: str = "") -> Union[pd.DataFrame, Dict, None]:
    """
    获取K线数据。stock_code 支持任意格式，内部自动解析。
    
    返回值：
      - pd.DataFrame：成功获取数据
      - Dict：{'need_selection': True, 'candidates': [...], 'display': '...'} 需要用户选择
      - None：未找到或失败
    
    Args:
        interval: 1m/5m/15m/30m/60m/120m/day/week/month/quarter/year
        count:    数据条数
        adjust:   "" 不复权 | "forward" 前复权 | "backward" 后复权
    """
    ths_code = resolve_ths_code(ths, stock_code)
    
    # 需要用户选择
    if isinstance(ths_code, dict) and ths_code.get('need_selection'):
        return ths_code
    
    if not ths_code:
        return None
    
    resp = ths.klines(ths_code, interval=interval, count=count, adjust=adjust)
    if resp.success:
        return resp.df
    print(f'[stock_utils] klines 失败: {resp.error}')
    return None


def get_realtime_data(ths, stock_code: str) -> Union[Dict, None]:
    """
    获取股票实时行情（最新价/涨跌幅/成交量等）。
    
    返回值：
      - Dict：成功获取数据
      - Dict：{'need_selection': True, 'candidates': [...], 'display': '...'} 需要用户选择
      - None：未找到或失败
    """
    ths_code = resolve_ths_code(ths, stock_code)
    
    if isinstance(ths_code, dict) and ths_code.get('need_selection'):
        return ths_code
    
    if not ths_code:
        return None
    
    resp = ths.market_data_cn(ths_code, "基础数据")
    if resp.success and not resp.df.empty:
        row = resp.df.iloc[0]
        return {
            'ths_code': ths_code,
            'name': row.get('股票名称', '未知'),
            'price': row.get('最新价', 0),
            'change_pct': row.get('涨跌幅', 0),
            'change_amt': row.get('涨跌额', 0),
            'open': row.get('开盘价', 0),
            'high': row.get('最高价', 0),
            'low': row.get('最低价', 0),
            'pre_close': row.get('昨收', 0),
            'volume': row.get('成交量', 0),
            'turnover': row.get('成交额', 0),
            'turnover_rate': row.get('换手率', 0),
        }
    print(f'[stock_utils] 实时数据获取失败: {resp.error}')
    return None


def get_stock_basic_info(ths, stock_code: str) -> Union[Dict, None]:
    """获取股票基础行情。支持任意格式输入。"""
    return get_realtime_data(ths, stock_code)


def get_fund_flow(ths, stock_code: str) -> Union[Dict, None]:
    """
    获取资金流向数据。
    
    返回值：
      - Dict：成功获取数据
      - Dict：{'need_selection': True, 'candidates': [...], 'display': '...'} 需要用户选择
      - None：未找到或失败
    """
    ths_code = resolve_ths_code(ths, stock_code)
    
    if isinstance(ths_code, dict) and ths_code.get('need_selection'):
        return ths_code
    
    if not ths_code:
        return None
    
    resp = ths.market_data_cn(ths_code, "资金流向")
    if resp.success and not resp.df.empty:
        row = resp.df.iloc[0]
        return {
            'ths_code': ths_code,
            'main_net_inflow': row.get('主力净流入', 0),
            'super_net_inflow': row.get('超大单净流入', 0),
            'big_net_inflow': row.get('大单净流入', 0),
            'medium_net_inflow': row.get('中单净流入', 0),
            'small_net_inflow': row.get('小单净流入', 0),
            'retail_net_inflow': row.get('散户净流入', 0),
            'total_net_inflow': row.get('资金净流入', 0),
        }
    print(f'[stock_utils] 资金流向获取失败: {resp.error}')
    return None


def get_intraday_data(ths, stock_code: str, date: str = None) -> Union[pd.DataFrame, Dict, None]:
    """
    获取分时数据。
    
    返回值：
      - pd.DataFrame：成功获取数据
      - Dict：{'need_selection': True, 'candidates': [...], 'display': '...'} 需要用户选择
      - None：未找到或失败
    """
    ths_code = resolve_ths_code(ths, stock_code)
    
    if isinstance(ths_code, dict) and ths_code.get('need_selection'):
        return ths_code
    
    if not ths_code:
        return None
    
    resp = ths.min_snapshot(ths_code, date=date) if date else ths.intraday_data(ths_code)
    if resp.success:
        return resp.df
    print(f'[stock_utils] 分时数据获取失败: {resp.error}')
    return None


def get_depth_data(ths, stock_code: str) -> Union[Dict, None]:
    """
    获取5档深度数据。
    
    返回值：
      - Dict：成功获取数据
      - Dict：{'need_selection': True, 'candidates': [...], 'display': '...'} 需要用户选择
      - None：未找到或失败
    """
    ths_code = resolve_ths_code(ths, stock_code)
    
    if isinstance(ths_code, dict) and ths_code.get('need_selection'):
        return ths_code
    
    if not ths_code:
        return None
    
    resp = ths.depth(ths_code)
    if resp.success and not resp.df.empty:
        df = resp.df
        return {
            'ths_code': ths_code,
            'bid_prices': df['bid_price'].tolist() if 'bid_price' in df.columns else [],
            'bid_volumes': df['bid_volume'].tolist() if 'bid_volume' in df.columns else [],
            'askPrices': df['ask_price'].tolist() if 'ask_price' in df.columns else [],
            'ask_volumes': df['ask_volume'].tolist() if 'ask_volume' in df.columns else [],
        }
    print(f'[stock_utils] 深度数据获取失败: {resp.error}')
    return None


def calculate_technical_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """计算 MA / RSI / MACD，原地修改并返回。"""
    if df.empty or 'close' not in df.columns:
        return df

    df['MA5'] = df['close'].rolling(5).mean()
    df['MA10'] = df['close'].rolling(10).mean()
    df['MA20'] = df['close'].rolling(20).mean()

    delta = df['close'].diff()
    gain = delta.where(delta > 0, 0).rolling(14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
    df['RSI'] = 100 - 100 / (1 + gain / loss)

    ema12 = df['close'].ewm(span=12, adjust=False).mean()
    ema26 = df['close'].ewm(span=26, adjust=False).mean()
    df['MACD'] = ema12 - ema26
    df['MACD_Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
    df['MACD_Histogram'] = df['MACD'] - df['MACD_Signal']
    return df


def batch_query_stocks(ths, stock_codes: List[str], data_type: str = "basic") -> Dict:
    """
    批量查询，每个代码都经过 resolve_ths_code 自动解析。
    data_type: "basic" | "kline" | "flow"
    """
    results = {}
    for code in stock_codes:
        if data_type == "basic":
            results[code] = get_stock_basic_info(ths, code)
        elif data_type == "kline":
            results[code] = get_kline_data(ths, code)
        elif data_type == "flow":
            results[code] = get_fund_flow(ths, code)
    return results


# ─────────────────────────────────────────────
# 便捷函数：直接获取 ths_code
# ─────────────────────────────────────────────

def query_stock_code(ths, user_input: str) -> Union[str, Dict, None]:
    """
    将用户输入转换为完整的 ths_code 并返回。
    这是 resolve_ths_code 的别名，便于理解。
    
    示例：
        query_stock_code(ths, "平安银行")  → "USZA000001"
        query_stock_code(ths, "ndsd")      → "USZA300750"
        query_stock_code(ths, "USHA600519") → "USHA600519" (直通)
    """
    return resolve_ths_code(ths, user_input)


# ─────────────────────────────────────────────
# 问财查询
# ─────────────────────────────────────────────

def wencai_query(ths, query: str) -> Union[pd.DataFrame, None]:
    """
    使用问财自然语言查询
    
    Args:
        query: 自然语言查询语句，如 "最近热度前50的行业"
        
    Returns:
        pd.DataFrame 或 None
    """
    resp = ths.wencai_nlp(query)
    if resp.success and resp.data:
        if isinstance(resp.data, list):
            return pd.DataFrame(resp.data)
        return pd.DataFrame([resp.data])
    print(f'[stock_utils] 问财查询失败: {resp.error}')
    return None


# ─────────────────────────────────────────────
# 测试入口
# ─────────────────────────────────────────────
if __name__ == "__main__":
    import logging
    logging.disable(logging.CRITICAL)
    
    # 首先检查 thsdk 安装状态
    print("=" * 60)
    print("thsdk 检查")
    print("=" * 60)
    print(f"已安装: {check_thsdk_installed()}")
    print(f"版本: {get_thsdk_version()}")
    print(f"最低要求: {THSDK_MIN_VERSION}")
    print()
    
    # 确保 thsdk 可用
    if not ensure_thsdk():
        print("❌ thsdk 安装失败，无法继续")
        sys.exit(1)
    
    from thsdk import THS

    with THS() as ths:
        print("=" * 60)
        print("search_stock_candidates 测试")
        print("=" * 60)
        
        # 测试唯一匹配
        print("\n[测试1] ndsd（预期唯一匹配）")
        result = search_stock_candidates(ths, "ndsd")
        print(f"  status: {result['status']}")
        print(f"  display: {result['display']}")
        
        # 测试多只A股
        print("\n[测试2] sjkj（预期多只A股）")
        result = search_stock_candidates(ths, "sjkj")
        print(f"  status: {result['status']}")
        print(f"  display: {result['display']}")
        
        # 测试直通
        print("\n[测试3] USHA600519（预期直通）")
        result = search_stock_candidates(ths, "USHA600519")
        print(f"  status: {result['status']}")
        print(f"  display: {result['display']}")
