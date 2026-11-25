"""
stocktoday-data proxy demo
==========================

StockToday 数据研究技能 demo 脚本, 调用 306 个数据接口, 后端走 StockToday 自定义加速 (https://tushare.citydata.club/).

LLM 调用方式:
    import sys
    sys.path.insert(0, "<skill_dir>/scripts")
    from proxy_demo import get_client
    pro = get_client("your_token_here")
    df = pro.daily(ts_code="600519.SH", start_date="20240101", end_date="20241231")

或者用环境变量:
    export TUSHARE_TOKEN="your_token"
    python proxy_demo.py
"""

import os
import sys
import tushare as ts
import pandas as pd
import requests

# === 网关地址 (主 + 备用, 都是 https + 有效证书) ===
DEFAULT_GATEWAY = "https://tushare.citydata.club/"
DEFAULT_BACKUP_GATEWAY = "https://backup.citydata.club/"

# 允许的自定义网关主机 (防止 token 被导向任意第三方服务器)
ALLOWED_GATEWAY_HOSTS = ("tushare.citydata.club", "backup.citydata.club")

# 第三个地址 (TUSHARE_GATEWAY_BACKUP2) **不随本包分发**: 需要时由使用者自备,
# 并显式设置 TUSHARE_GATEWAY_ALLOW_INSECURE=1 放行明文 HTTP (token 与数据不加密, 仅应急).
# 之所以不内置明文地址: 明文 HTTP 会让 API token 与金融数据在链路上裸奔
# (被动窃听 / 中间人篡改), 属于高危配置, 不应由技能包默认分发.
# ★ 官方备用站 backup.citydata.club 是 **https**, 可以安全内置并自动故障切换.


def _validate_gateway(gateway: str) -> str:
    """
    校验自定义网关地址.

    规则:
      1. 必须是 https:// (明文 HTTP 会泄露 API token 与金融数据)
         —— 唯一例外: 本地调试 (127.0.0.1 / localhost), 以及使用者显式设置
         TUSHARE_GATEWAY_ALLOW_INSECURE=1 后的自备明文备用地址
      2. 主机名必须在 ALLOWED_GATEWAY_HOSTS 白名单内 (防止 token 被导向攻击者服务器)
    """
    from urllib.parse import urlparse
    g = (gateway or "").strip()
    if not g:
        raise ValueError("gateway 不能为空")
    p = urlparse(g)
    host = (p.hostname or "").lower()
    if p.scheme == "http" and host in ("127.0.0.1", "localhost"):
        return g
    if p.scheme == "http":
        allow = os.getenv("TUSHARE_GATEWAY_ALLOW_INSECURE", "").strip().lower()
        if allow in ("1", "true", "yes"):
            # 使用者显式承担风险的明文备用地址
            return g
        raise ValueError(
            "gateway 必须是 https:// (明文 HTTP 会泄露 API token); "
            "如确需自备明文备用地址, 请显式设置 TUSHARE_GATEWAY_ALLOW_INSECURE=1")
    if host not in ALLOWED_GATEWAY_HOSTS:
        raise ValueError(
            "gateway 主机不在白名单 %s 内; 当前收到: %r" % (ALLOWED_GATEWAY_HOSTS, host))
    return g


def enable_utf8_stdout() -> None:
    """
    强制 stdout 用 UTF-8 输出.

    Windows 默认控制台编码是 GBK (cp936), 打印 emoji (✅/📊/⚠️) 会抛
    UnicodeEncodeError 直接崩掉整个 demo. 这里统一兜底.

    对已经被设置为 UTF-8 的终端 (PYTHONIOENCODING=utf-8 / Windows Terminal)
    以及不支持 reconfigure 的流 (被重定向到 StringIO 等) 都安全.
    """
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is None:
            continue
        try:
            reconfigure(encoding="utf-8", errors="replace")
        except (ValueError, OSError):
            pass


def _install_failover(pro, gateways):
    """给 pro 装上故障切换: 某个地址连不上 (连接错误 / 超时) 就自动换下一个.

    实现方式: 替换实例上的 query —— SDK 的 DataApi.__getattr__ 返回
    partial(self.query, api_name), 所以 pro.daily(...) 之类会走新的 query.
    只在**连接层**失败时切换; 业务错误 (code != 0) 属于对端的正常答复, 不切换.
    """
    if len(gateways) < 2:
        return pro
    original_query = pro.query
    state = {"idx": 0}

    def query(api_name, fields="", **kwargs):
        last_err = None
        for step in range(len(gateways)):
            i = (state["idx"] + step) % len(gateways)
            pro._DataApi__http_url = gateways[i]
            try:
                result = original_query(api_name, fields=fields, **kwargs)
            except (requests.exceptions.ConnectionError,
                    requests.exceptions.Timeout) as e:
                last_err = e
                continue
            state["idx"] = i          # 记住走通的地址, 下次优先用它
            return result
        raise last_err

    pro.query = query
    return pro


def get_client(token: str = None, gateway: str = None,
               backup_gateway: str = None) -> "ts.pro_api":
    """
    获取走 StockToday gateway 的 pro client

    优先顺序: 参数 > TUSHARE_TOKEN env > TUSHARE_GATEWAY env > 默认 gateway
    自定义 gateway 会被 _validate_gateway 校验 (仅 https + 主机白名单)

    ★ 主地址 + 备用地址自动故障切换:
      主站 (tushare.citydata.club) 连不上时自动改走备用站 (backup.citydata.club),
      两个都失败才抛错. 两个地址都是 https + 有效证书, token 与数据全程加密.
    """
    token = token or os.getenv("TUSHARE_TOKEN") or "your_token_here"
    primary = _validate_gateway(
        gateway or os.getenv("TUSHARE_GATEWAY") or DEFAULT_GATEWAY)
    backup = _validate_gateway(
        backup_gateway or os.getenv("TUSHARE_GATEWAY_BACKUP")
        or DEFAULT_BACKUP_GATEWAY)
    extra = os.getenv("TUSHARE_GATEWAY_BACKUP2", "").strip()

    chain = [primary]
    for g in (backup, extra):
        if g and g not in chain:
            chain.append(_validate_gateway(g))

    pro = ts.pro_api(token)
    # 指向 stocktoday gateway
    pro._DataApi__token = token
    pro._DataApi__http_url = chain[0]
    _install_failover(pro, chain)
    return pro


def print_section(title: str, df: pd.DataFrame, max_rows: int = 5) -> None:
    """统一打印格式: 标题 + 前 max_rows 行"""
    print(f"\n{'=' * 50}")
    print(f"📊 {title}")
    print(f"{'=' * 50}")
    print(f"  数据行数: {len(df)}")
    print(f"  字段: {list(df.columns)[:8]}{'...' if len(df.columns) > 8 else ''}")
    print(df.head(max_rows).to_string(index=False))


# ============================================================
# 5 个 demo case: 行情 / 财务 / 对比 / 资金 / 板块
# ============================================================

def demo_quote(pro: "ts.pro_api") -> None:
    """Demo 1: 单只股票最近 1 个月日线"""
    df = pro.daily(ts_code="600519.SH", start_date="20260601", end_date="20260618")
    print_section("Demo 1: 茅台 6 月日线", df)


def demo_finance(pro: "ts.pro_api") -> None:
    """Demo 2: 单只股票 2024 年报关键指标"""
    # 注: fields 里必须用 end_date —— StockToday gateway 的 fina_indicator 没有
    # `period` 输出列, 请求不存在的列会直接返 0 行 (不是权限问题).
    df = pro.fina_indicator(ts_code="600519.SH", period="20241231",
                            fields="ts_code,end_date,roe,grossprofit_margin,eps,debt_to_assets")
    print_section("Demo 2: 茅台 2024 年报 ROE/毛利率/EPS", df)


def demo_compare(pro: "ts.pro_api") -> None:
    """Demo 3: 多只股票对比 (用 daily 取最新一日收盘)"""
    df = pro.daily(ts_code="600519.SH,000858.SZ,000568.SZ",
                   trade_date="20260618",
                   fields="ts_code,close,pct_chg,vol,amount")
    print_section("Demo 3: 白酒 3 只对比 (6/18 收盘)", df)


def demo_moneyflow(pro: "ts.pro_api") -> None:
    """Demo 4: 单只股票资金流向 (主力净流入)"""
    df = pro.moneyflow(ts_code="600519.SH", trade_date="20260618",
                       fields="ts_code,trade_date,buy_sm_amount,sell_sm_amount,buy_md_amount,sell_md_amount,buy_lg_amount,sell_lg_amount,buy_elg_amount,sell_elg_amount,net_mf_amount")
    print_section("Demo 4: 茅台 6/18 资金流向 (小/中/大/特大单)", df)


def demo_sector(pro: "ts.pro_api") -> None:
    """Demo 5: 板块行情 (同花顺概念)"""
    # 参数取值见 references/接口索引.md 的 ths_index:
    #   exchange = "A" (a股) / "HK" (港股) / "US" (美股), type = "N" 概念指数
    df = pro.ths_index(exchange="A", type="N")
    print_section("Demo 5: 同花顺概念指数列表 (exchange=A, type=N)", df.head(10))


# ============================================================
# 主入口: 跑全部 5 个 demo
# ============================================================

if __name__ == "__main__":
    enable_utf8_stdout()
    pro = get_client()
    print(f"✅ StockToday client 已初始化, gateway: {pro._DataApi__http_url}")
    print(f"   备用地址: {DEFAULT_BACKUP_GATEWAY} (主站连不上时自动切换)")
    # 不打印 token 的任何片段 (避免 token 前缀进日志/agent 上下文)
    print("   凭据: 已从环境变量读取 (不打印内容)")

    try:
        demo_quote(pro)
    except Exception as e:
        print(f"❌ Demo 1 失败: {e}")

    try:
        demo_finance(pro)
    except Exception as e:
        print(f"❌ Demo 2 失败: {e}")

    try:
        demo_compare(pro)
    except Exception as e:
        print(f"❌ Demo 3 失败: {e}")

    try:
        demo_moneyflow(pro)
    except Exception as e:
        print(f"❌ Demo 4 失败: {e}")

    try:
        demo_sector(pro)
    except Exception as e:
        print(f"❌ Demo 5 失败: {e}")
