#!/usr/bin/env python3
"""
多源数据智能路由器 - A股交易数据获取
=========================================
版本: v3.0 (2026-05-22)
Skill: wolfjkd-trader-data
作者: wolfjkd (MIT License)

数据源自动检测、评分、择优，支持并行探测和结果对比。
无需额外安装任何依赖，仅使用Python标准库。

使用方式:
  # 检测所有数据源健康状态
  python data_router.py health

  # 获取实时行情（自动选最优源）
  python data_router.py quote --codes sh000001,sz399001

  # 获取自选股行情
  python data_router.py watchlist

  # 对比多个数据源的同一条数据
  python data_router.py compare --code 600519.SH --type quote

  # 仅输出JSON（供其他脚本调用）
  python data_router.py quote --codes sh000001 --json
"""

import json
import sys
import time
import urllib.request
import urllib.error
import subprocess
from datetime import datetime
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed, TimeoutError

# ============================================================
# 配置区 —— 根据你的需求修改
# ============================================================

# 自选股列表（格式：("腾讯代码", "名称")）
# 腾讯代码规则：上海=sh+6位代码，深圳=sz+6位代码
WATCHLIST = [
    ("sh600519", "贵州茅台"),   # 示例：请修改为你的持仓/关注标的
    ("sz000001", "平安银行"),
    ("sh600036", "招商银行"),
    ("sz002594", "比亚迪"),
    ("sh601318", "中国平安"),
    ("sz300750", "宁德时代"),
]

# A股主要指数
INDEXES = ["sh000001", "sz399001", "sz399006"]

# 美股指数
US_INDEXES = ["usINDU", "usIXIC", "usINX"]

# 大宗商品
COMMODITIES = ["hf_GC", "hf_SI", "hf_CL"]

# 数据源超时阈值（秒）
TIMEOUTS = {
    "tencent": 5,      # 腾讯接口快，5秒足够
    "wind": 10,        # Wind MCP需要CLI调用+网络
    "ftshare": 15,     # ftshare Python脚本较慢
    "websearch": 20,   # WebSearch最慢（需AI处理）
}

# ============================================================
# 数据源适配器
# ============================================================

class DataSourceResult:
    """单次数据源探测结果"""
    def __init__(self, source: str, data_type: str):
        self.source = source
        self.data_type = data_type
        self.success = False
        self.response_time_ms = 0
        self.data = None           # 原始数据
        self.parsed = None         # 解析后的结构化数据
        self.error = None
        self.score = 0             # 综合评分 0-100
        self.availability_score = 0   # 可用性 0-100
        self.timeliness_score = 0     # 及时性 0-100
        self.quality_score = 0        # 质量 0-100
        self.timestamp = datetime.now().isoformat()

    def to_dict(self) -> dict:
        return {
            "source": self.source,
            "data_type": self.data_type,
            "success": self.success,
            "response_time_ms": self.response_time_ms,
            "score": round(self.score, 1),
            "availability_score": round(self.availability_score, 1),
            "timeliness_score": round(self.timeliness_score, 1),
            "quality_score": round(self.quality_score, 1),
            "error": self.error,
            "has_data": self.data is not None,
        }


class TencentAdapter:
    """腾讯行情接口适配器"""

    NAME = "tencent"
    DESCRIPTION = "腾讯实时行情接口（毫秒级，基础字段）"

    @staticmethod
    def fetch(codes: list[str], timeout: int = 5) -> DataSourceResult:
        result = DataSourceResult("tencent", "quote")
        start = time.time()

        try:
            url = f"https://qt.gtimg.cn/q={','.join(codes)}"
            req = urllib.request.Request(url, headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
            })
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                raw = resp.read().decode("gbk", errors="ignore")

            result.response_time_ms = round((time.time() - start) * 1000)
            result.data = raw
            result.success = True

            # 解析并评分
            parsed = TencentAdapter._parse(raw, codes)
            result.parsed = parsed
            result = TencentAdapter._score(result, codes)

        except urllib.error.URLError as e:
            result.response_time_ms = round((time.time() - start) * 1000)
            result.error = f"网络错误: {e.reason}"
            result.score = 0
        except Exception as e:
            result.response_time_ms = round((time.time() - start) * 1000)
            result.error = str(e)
            result.score = 0

        return result

    @staticmethod
    def _parse(raw: str, expected_codes: list) -> list[dict]:
        """解析腾讯接口返回数据为结构化列表"""
        records = []
        for line in raw.strip().split(";"):
            line = line.strip()
            if not line:
                continue
            # 格式: v_sh600170="1~上海建工~..."
            if "~" in line and "=" in line:
                try:
                    data_str = line.split("=", 1)[1].strip('"')
                    fields = data_str.split("~")
                    if len(fields) >= 45:  # 腾讯返回约50个字段
                        records.append({
                            "code": fields[2],       # 股票代码
                            "name": fields[1],        # 名称
                            "price": float(fields[3]) if fields[3] else None,       # 最新价
                            "prev_close": float(fields[4]) if fields[4] else None,   # 收盘价
                            "open": float(fields[5]) if fields[5] else None,         # 今开
                            "volume": int(float(fields[36])) if fields[36] else None, # 成交量(手)
                            "amount": float(fields[37]) if fields[37] else None,      # 成交额
                            "change_pct": float(fields[32]) if fields[32] else None, # 涨跌幅
                            "change_amt": float(fields[31]) if fields[31] else None, # 涨跌额
                            "high": float(fields[33]) if fields[33] else None,       # 最高
                            "low": float(fields[34]) if fields[34] else None,        # 最低
                            "turnover": float(fields[38]) if fields[38] else None,   # 换手率
                            "pe": fields[39],              # 市盈率
                            "market_cap": fields[44],      # 总市值
                            "timestamp": fields[30],       # 更新时间
                            "_source": "tencent",
                        })
                except (ValueError, IndexError):
                    continue
        return records

    @staticmethod
    def _score(result: DataSourceResult, expected_codes: list) -> DataSourceResult:
        """腾讯接口评分"""
        n_expected = len(expected_codes)
        n_got = len(result.parsed) if result.parsed else 0

        # 可用性 (40%): 连通且返回数据=满分
        result.availability_score = 100 if result.success and n_got > 0 else 0

        # 及时性 (30%): <500ms=100, <1s=90, <2s=70, <3s=50, <5s=30, >5s=10
        rt = result.response_time_ms
        if rt <= 500: result.timeliness_score = 100
        elif rt <= 1000: result.timeliness_score = 90
        elif rt <= 2000: result.timeliness_score = 70
        elif rt <= 3000: result.timeliness_score = 50
        elif rt <= 5000: result.timeliness_score = 30
        else: result.timeliness_score = 10

        # 质量 (30%): 数据完整度 + 数值合理性
        if n_got == 0:
            result.quality_score = 0
        elif n_got >= n_expected:
            valid_count = sum(
                1 for r in result.parsed
                if r.get("price") is not None and r.get("price") > 0
            )
            ratio = valid_count / max(n_got, 1)
            result.quality_score = min(100, int(ratio * 100))
        else:
            result.quality_score = int((n_got / n_expected) * 70)

        # 加权总分
        result.score = (
            result.availability_score * 0.40 +
            result.timeliness_score * 0.30 +
            result.quality_score * 0.30
        )
        return result


class WindAdapter:
    """Wind MCP Skill适配器"""

    NAME = "wind"
    DESCRIPTION = "Wind万得金融（全维度数据，有日额度）"

    # Wind skill目录（自动检测：从data_router.py位置向上查找 .agents/skills/wind-mcp-skill）
    WIND_SKILL_DIR = Path(__file__).parent.parent.parent.parent / ".agents" / "skills" / "wind-mcp-skill"

    @classmethod
    def _is_available(cls) -> bool:
        """检查Wind CLI是否可用"""
        cli = cls.WIND_SKILL_DIR / "scripts" / "cli.mjs"
        return cli.exists()

    @classmethod
    def fetch(cls, code: str, indexes: str = "中文简称,最新成交价,涨跌幅,成交量",
              timeout: int = 10) -> DataSourceResult:
        """获取单个标的Wind行情快照"""
        result = DataSourceResult("wind", "quote")
        start = time.time()

        if not cls._is_available():
            result.error = "Wind CLI不存在，请先安装wind-mcp-skill"
            result.response_time_ms = round((time.time() - start) * 1000)
            result.score = 0
            return result

        try:
            cli = cls.WIND_SKILL_DIR / "scripts" / "cli.mjs"
            params_json = json.dumps({"windcode": code, "indexes": indexes}, ensure_ascii=False)
            cmd = ["node", str(cli), "call", "stock_data", "get_stock_price_indicators", params_json]

            proc = subprocess.run(
                cmd, capture_output=True, text=True, timeout=timeout,
                cwd=str(cls.WIND_SKILL_DIR)
            )

            result.response_time_ms = round((time.time() - start) * 1000)
            stdout = proc.stdout.strip()
            stderr = proc.stderr.strip()

            if proc.returncode == 0 and stdout:
                result.data = stdout
                result.success = True
                try:
                    result.parsed = json.loads(stdout) if stdout.startswith("{") or stdout.startswith("[") else {"raw": stdout}
                except json.JSONDecodeError:
                    result.parsed = {"raw": stdout}
            else:
                result.error = stdout or stderr or f"退出码 {proc.returncode}"
                result.data = stdout

            result = cls._score(result)

        except subprocess.TimeoutExpired:
            result.response_time_ms = round((time.time() - start) * 1000)
            result.error = f"超时({timeout}s)"
            result.score = 0
        except Exception as e:
            result.response_time_ms = round((time.time() - start) * 1000)
            result.error = str(e)
            result.score = 0

        return result

    @classmethod
    def _score(cls, result: DataSourceResult) -> DataSourceResult:
        """Wind评分"""
        result.availability_score = 100 if result.success else 0

        rt = result.response_time_ms
        if rt <= 1500: result.timeliness_score = 100
        elif rt <= 3000: result.timeliness_score = 85
        elif rt <= 5000: result.timeliness_score = 70
        elif rt <= 8000: result.timeliness_score = 50
        elif rt <= 10000: result.timeliness_score = 30
        else: result.timeliness_score = 10

        if result.success and result.data:
            data_str = str(result.data)
            if len(data_str) > 20 and "error" not in data_str.lower()[:200]:
                result.quality_score = 95
            elif len(data_str) > 5:
                result.quality_score = 70
            else:
                result.quality_score = 30
        else:
            result.quality_score = 0

        result.score = (
            result.availability_score * 0.40 +
            result.timeliness_score * 0.25 +
            result.quality_score * 0.35
        )
        return result


class FtShareAdapter:
    """ftshare公告数据适配器"""

    NAME = "ftshare"
    DESCRIPTION = "FTShare公告数据（A股公告结构化）"

    # ftshare目录（自动检测：从data_router.py位置向上查找 .workbuddy/skills/ftshare-announcement-data）
    FTSHARE_DIR = Path(__file__).parent.parent.parent / ".workbuddy" / "skills" / "ftshare-announcement-data"

    @classmethod
    def _is_available(cls) -> bool:
        run_py = cls.FTSHARE_DIR / "run.py"
        return run_py.exists()

    @classmethod
    def fetch(cls, stock_code: str, page: int = 1, page_size: int = 10,
              timeout: int = 15) -> DataSourceResult:
        """获取个股公告"""
        result = DataSourceResult("ftshare", "announcement")
        start = time.time()

        if not cls._is_available():
            result.error = "ftshare run.py不存在"
            result.response_time_ms = round((time.time() - start) * 1000)
            result.score = 0
            return result

        try:
            cmd = [
                sys.executable, str(cls.FTSHARE_DIR / "run.py"),
                "stock-announcements-single-stock-all-periods",
                "--stock-code", stock_code,
                "--page", str(page),
                "--page-size", str(page_size)
            ]
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)

            result.response_time_ms = round((time.time() - start) * 1000)
            stdout = proc.stdout.strip()

            if proc.returncode == 0 and stdout:
                result.data = stdout
                result.success = True
                try:
                    result.parsed = json.loads(stdout)
                except json.JSONDecodeError:
                    result.parsed = {"raw": stdout}
            else:
                result.error = stdout or proc.stderr or f"退出码 {proc.returncode}"

            result = cls._score(result)

        except subprocess.TimeoutExpired:
            result.response_time_ms = round((time.time() - start) * 1000)
            result.error = f"超时({timeout}s)"
            result.score = 0
        except Exception as e:
            result.response_time_ms = round((time.time() - start) * 1000)
            result.error = str(e)
            result.score = 0

        return result

    @classmethod
    def _score(cls, result: DataSourceResult) -> DataSourceResult:
        result.availability_score = 100 if result.success else 0

        rt = result.response_time_ms
        if rt <= 2000: result.timeliness_score = 100
        elif rt <= 5000: result.timeliness_score = 80
        elif rt <= 10000: result.timeliness_score = 60
        elif rt <= 15000: result.timeliness_score = 40
        else: result.timeliness_score = 20

        if result.success and result.parsed:
            if isinstance(result.parsed, dict) and "data" in result.parsed:
                count = len(result.parsed["data"]) if isinstance(result.parsed["data"], list) else 0
            elif isinstance(result.parsed, list):
                count = len(result.parsed)
            else:
                count = 1 if len(str(result.parsed)) > 50 else 0

            if count >= 5: result.quality_score = 95
            elif count >= 1: result.quality_score = 75
            else: result.quality_score = 40
        else:
            result.quality_score = 0

        result.score = (
            result.availability_score * 0.40 +
            result.timeliness_score * 0.25 +
            result.quality_score * 0.35
        )
        return result


# ============================================================
# 路由核心逻辑
# ============================================================

def probe_sources(data_type: str, **kwargs) -> list[DataSourceResult]:
    """
    并行探测所有候选数据源，返回按得分排序的结果列表。
    
    data_type: 'quote' | 'announcement' | 'index' | 'commodity'
    """
    results = []
    futures_map = {}

    with ThreadPoolExecutor(max_workers=4) as executor:
        if data_type in ("quote", "index", "commodity"):
            codes = kwargs.get("codes", INDEXES)
            fut = executor.submit(TencentAdapter.fetch, codes, TIMEOUTS["tencent"])
            futures_map[fut] = ("tencent", "primary")

            single_code = kwargs.get("single_code")
            if single_code and WindAdapter._is_available():
                fut_w = executor.submit(WindAdapter.fetch, single_code)
                futures_map[fut_w] = ("wind", "secondary")

        elif data_type == "announcement":
            stock_code = kwargs.get("stock_code", "600519.SH")
            if FtShareAdapter._is_available():
                fut_f = executor.submit(FtShareAdapter.fetch, stock_code)
                futures_map[fut_f] = ("ftshare", "primary")

        for future in as_completed(futures_map, timeout=max(TIMEOUTS.values()) + 5):
            src_name, role = futures_map[future]
            try:
                res = future.result(timeout=5)
                results.append(res)
            except TimeoutError:
                fallback = DataSourceResult(src_name, data_type)
                fallback.error = "探测超时"
                fallback.score = 0
                results.append(fallback)
            except Exception as e:
                fallback = DataSourceResult(src_name, data_type)
                fallback.error = str(e)
                fallback.score = 0
                results.append(fallback)

    results.sort(key=lambda x: x.score, reverse=True)
    return results


def select_best(results: list[DataSourceResult], min_score: float = 50.0) -> tuple[DataSourceResult | None, str]:
    """
    从探测结果中选择最优源。
    
    返回: (最佳结果, 决策理由)
    """
    if not results:
        return None, "无可用数据源"

    best = results[0]
    runner_up = results[1] if len(results) > 1 else None

    if best.score < min_score:
        return None, f"所有数据源评分均低于{min_score}分阈值（最佳: {best.source}={best.score:.1f}）"

    if runner_up and abs(best.score - runner_up.score) <= 10:
        if best.response_time_ms > runner_up.response_time_ms:
            decision = f"{runner_up.source}胜出（与{best.source}分数接近但更快：{runner_up.response_time_ms}ms vs {best.response_time_ms}ms）"
            return runner_up, decision

    grade = _score_to_grade(best.score)
    decision = f"{best.source}胜出（评分:{best.score:.1f}/100, 等级:{grade}, 响应:{best.response_time_ms}ms）"
    return best, decision


def _score_to_grade(score: float) -> str:
    """数值评分转为等级"""
    if score >= 85: return "A"
    if score >= 70: return "B"
    if score >= 50: return "C"
    return "D"


# ============================================================
# CLI命令
# ============================================================

def cmd_health():
    """检测所有数据源健康状态"""
    print("=" * 65)
    print(f"  数据源健康检测  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 65)

    all_results = {}

    # 1. 检测腾讯接口
    print("\n[1/3] 检测腾讯行情接口...")
    tencent_result = TencentAdapter.fetch(INDEXES, TIMEOUTS["tencent"])
    all_results["tencent"] = tencent_result
    _print_source_result(tencent_result)

    # 2. 检测Wind
    print("\n[2/3] 检测Wind万得...")
    if WindAdapter._is_available():
        wind_result = WindAdapter.fetch("600519.SH", timeout=TIMEOUTS["wind"])
        all_results["wind"] = wind_result
        _print_source_result(wind_result)
    else:
        print(f"  [!] Wind未安装（路径不存在: {WindAdapter.WIND_SKILL_DIR}）")
        dummy = DataSourceResult("wind", "quote")
        dummy.error = "未安装"
        dummy.score = 0
        all_results["wind"] = dummy

    # 3. 检测ftshare
    print("\n[3/3] 检测FTShare公告...")
    if FtShareAdapter._is_available():
        ft_result = FtShareAdapter.fetch("600519.SH", timeout=TIMEOUTS["ftshare"])
        all_results["ftshare"] = ft_result
        _print_source_result(ft_result)
    else:
        print(f"  [!] FTShare未安装（路径不存在: {FtShareAdapter.FTSHARE_DIR}）")
        dummy = DataSourceResult("ftshare", "announcement")
        dummy.error = "未安装"
        dummy.score = 0
        all_results["ftshare"] = dummy

    # 汇总
    print("\n" + "=" * 65)
    print("  汇总")
    print("=" * 65)
    print(f"{'数据源':<12} {'状态':^6} {'评分':^8} {'响应':^10} {'等级':^6}")
    print("-" * 65)
    for name, res in all_results.items():
        status = "OK" if res.success and res.score >= 50 else "WARN" if res.score >= 20 else "FAIL"
        grade = _score_to_grade(res.score)
        rt_str = f"{res.response_time_ms}ms" if res.response_time_ms > 0 else "N/A"
        print(f"{name:<12} {status:^6} {res.score:^8.1f} {rt_str:^10} {grade:^6}")

    best_name = max(all_results.keys(), key=lambda k: all_results[k].score)
    best = all_results[best_name]
    print(f"\n[*] 最佳数据源: {best_name}（评分 {best.score:.1f}, 等级 {_score_to_grade(best.score)}）")


def cmd_quote(codes: list[str] | None = None, output_json: bool = False):
    """获取实时行情（自动选最优源）"""
    target_codes = codes or INDEXES

    results = probe_sources("quote", codes=target_codes)
    best, reason = select_best(results)

    if output_json:
        output = {
            "timestamp": datetime.now().isoformat(),
            "best_source": best.source if best else None,
            "reason": reason,
            "all_probes": [r.to_dict() for r in results],
            "data": best.parsed if best and best.parsed else None,
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))
        return

    if not best:
        print(f"[ERR] {reason}")
        return

    print(f"[OK] 选择: {reason}\n")
    if best.source == "tencent" and best.parsed:
        _print_quote_table(best.parsed)
    elif best.source == "wind":
        print(best.data)


def cmd_watchlist(output_json: bool = False):
    """获取自选股行情"""
    codes = [item[0] for item in WATCHLIST]
    results = probe_sources("quote", codes=codes)
    best, reason = select_best(results)

    if output_json:
        output = {
            "timestamp": datetime.now().isoformat(),
            "best_source": best.source if best else None,
            "reason": reason,
            "watchlist_data": best.parsed if best and best.parsed else None,
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))
        return

    if not best:
        print(f"[ERR] {reason}")
        return

    print(f"  自选股行情 ({datetime.now().strftime('%H:%M:%S')}) | 来源: {best.source.upper()} ({_score_to_grade(best.score)}级)\n")
    print(f"{'名称':<8} {'代码':<10} {'最新价':>8} {'涨跌幅':>8} {'成交量':>12} {'响应':>8}")
    print("-" * 62)

    if best.source == "tencent" and best.parsed:
        watch_codes = set(item[0].replace("sh", "").replace("sz", "") for item in WATCHLIST)
        for rec in best.parsed:
            code_raw = rec.get("code", "")
            if any(code_raw.endswith(c) for c in watch_codes):
                price = f"{rec.get('price', '-'):.2f}" if rec.get("price") else "-"
                chg_pct = f"{rec.get('change_pct', '-')}%" if rec.get("change_pct") is not None else "-"
                vol = rec.get("volume")
                vol_str = f"{vol:,}" if vol else "-"
                name = rec.get("name", "-")[:6]
                print(f"{name:<8} {code_raw:<10} {price:>8} {chg_pct:>8} {vol_str:>12} {best.response_time_ms:>7}ms")
    else:
        print(best.data)


def cmd_compare(code: str, data_type: str = "quote"):
    """对比多个数据源的同一条数据"""
    print(f"  数据源对比: {code} ({data_type})\n")

    all_results = []

    # 腾讯
    print("探测腾讯接口...")
    tencent_code = code.replace(".SH", "").replace(".SZ", "")
    if not tencent_code.startswith(("sh", "sz", "us", "hk")):
        if tencent_code.startswith("6") or tencent_code.startswith("5"):
            tencent_code = "sh" + tencent_code
        elif tencent_code.startswith("0") or tencent_code.startswith("3"):
            tencent_code = "sz" + tencent_code
        else:
            tencent_code = "sh" + tencent_code
    t_res = TencentAdapter.fetch([tencent_code], TIMEOUTS["tencent"])
    all_results.append(t_res)
    _print_source_result(t_res)

    # Wind
    if data_type == "quote" and WindAdapter._is_available():
        print("探测Wind...")
        w_res = WindAdapter.fetch(code, timeout=TIMEOUTS["wind"])
        all_results.append(w_res)
        _print_source_result(w_res)

    # 对比表
    print(f"\n{'='*55}")
    print(f"{'数据源':<10} {'评分':>6} {'可用性':>6} {'及时性':>6} {'质量':>6} {'响应ms':>8}")
    print("-" * 55)
    for r in sorted(all_results, key=lambda x: x.score, reverse=True):
        grade = _score_to_grade(r.score)
        print(f"{r.source:<10} {r.score:>5.1f}{grade:<1} {r.availability_score:>6.0f} "
              f"{r.timeliness_score:>6.0f} {r.quality_score:>6.0f} {r.response_time_ms:>8}")

    # 一致性检查
    successes = [r for r in all_results if r.success]
    if len(successes) >= 2:
        print(f"\n  一致性检查:")
        prices = {}
        for r in successes:
            if r.source == "tencent" and r.parsed:
                for item in r.parsed:
                    if item.get("price"):
                        prices[r.source] = item["price"]
            elif r.source == "wind" and r.data:
                try:
                    d = json.loads(r.data) if isinstance(r.data, str) else r.data
                    if isinstance(d, dict):
                        for k, v in d.items():
                            if "价" in k and isinstance(v, (int, float)):
                                prices[r.source] = v
                                break
                except:
                    pass

        if len(prices) >= 2:
            sources_list = list(prices.keys())
            p1, p2 = prices[sources_list[0]], prices[sources_list[1]]
            diff_abs = abs(p1 - p2)
            diff_pct = (diff_abs / max(p1, p2)) * 100 if max(p1, p2) > 0 else 0
            status = "高度一致" if diff_pct < 0.5 else "有偏差" if diff_pct < 2 else "差异较大"
            print(f"  {sources_list[0]}: {p1} vs {sources_list[1]}: {p2} -> 差异 {diff_abs:.2f} ({diff_pct:.2f}%) {status}")


# ============================================================
# 输出辅助
# ============================================================

def _print_source_result(res: DataSourceResult):
    """打印单个数据源检测结果"""
    grade = _score_to_grade(res.score)
    status_icon = "[+]" if res.success and res.score >= 50 else "[!]" if res.score >= 20 else "[x]"
    print(f"  {status_icon} [{res.source.upper()}] 评分: {res.score:.1f}/100 ({grade}级)")
    print(f"     响应时间: {res.response_time_ms}ms")
    print(f"     可用性: {res.availability_score:.0f} | 及时性: {res.timeliness_score:.0f} | 质量: {res.quality_score:.0f}")
    if res.error:
        print(f"     错误: {res.error}")
    if res.success:
        preview = str(res.data)[:120] if res.data else "(空)"
        print(f"     数据预览: {preview}...")


def _print_quote_table(records: list[dict]):
    """打印行情表格"""
    print(f"{'名称':<8} {'代码':<10} {'最新价':>8} {'涨跌额':>8} {'涨跌幅':>8} {'成交量(手)':>12} {'成交额':>14}")
    print("-" * 74)
    for r in records:
        price = f"{r.get('price', '-'):.2f}" if r.get("price") is not None else "-"
        chg = f"{r.get('change_amt', '-'):+.2f}" if r.get("change_amt") is not None else "-"
        chg_pct = f"{r.get('change_pct', '-')}%" if r.get("change_pct") is not None else "-"
        vol = f"{r.get('volume', '-'):,}" if r.get("volume") is not None else "-"
        amt = f"{r.get('amount', '-'):,}" if r.get("amount") is not None else "-"
        name = (r.get("name", "-") or "-")[:7]
        code = r.get("code", "-") or "-"
        print(f"{name:<8} {code:<10} {price:>8} {chg:>8} {chg_pct:>8} {vol:>12} {amt:>14}")


# ============================================================
# 入口
# ============================================================

def main():
    args = sys.argv[1:] if len(sys.argv) > 1 else ["health"]

    if not args or args[0] in ("health", "-h", "--help", "status"):
        if args[0] in ("-h", "--help"):
            print(__doc__)
            return
        cmd_health()

    elif args[0] == "quote":
        codes = None
        output_json = False
        i = 1
        while i < len(args):
            if args[i] in ("--codes", "-c") and i + 1 < len(args):
                codes = args[i + 1].split(",")
                i += 2
            elif args[i] == "--json":
                output_json = True
                i += 1
            else:
                i += 1
        cmd_quote(codes, output_json)

    elif args[0] in ("watchlist", "wl"):
        output_json = "--json" in args
        cmd_watchlist(output_json)

    elif args[0] == "compare":
        code = "600519.SH"
        dtype = "quote"
        i = 1
        while i < len(args):
            if args[i] in ("--code", "-c") and i + 1 < len(args):
                code = args[i + 1]
                i += 2
            elif args[i] in ("--type", "-t") and i + 1 < len(args):
                dtype = args[i + 1]
                i += 2
            else:
                i += 1
        cmd_compare(code, dtype)

    else:
        print(f"未知命令: {args[0]}")
        print("用法: python data_router.py [health|quote|watchlist|compare] [--json]")
        sys.exit(1)


if __name__ == "__main__":
    main()
