#!/usr/bin/env python3
"""wttr.in 天气查询工具 v2 — 覆盖 wttr.in 全部免费能力（2026-10 实测核对）。

使用方法:
    python weather.py                       # 当前位置（IP 判定）
    python weather.py Beijing               # 全量卡片（纯文本默认；--ansi 出彩色）
    python weather.py Beijing -f view0      # 只看当前天气
    python weather.py Beijing -V 0q         # 任意视图组合（?0q）
    python weather.py Beijing -f json       # 完整 JSON（含逐小时）
    python weather.py Beijing -f oneline --custom-format '%l:+%c+%t'
    python weather.py Paris -f png -o weather.png
    python weather.py -f moon                 # 月相
    python weather.py -f batch Beijing Shanghai Guangzhou
能力面以 live :help + README 探针为准；%e %H %L 服务端不支持，勿用。
"""

import argparse
import json
import subprocess
import sys
from typing import Any, Dict, Optional

VERIFIED_PCT = "%l %c %C %x %t %f %h %w %p %P %u %m %M %D %S %z %s %d %T %Z".split()
DEAD_PCT = ["%e", "%H", "%L"]  # 服务端原样回显 = 未实现（2026-10 实测）


def curl(url: str, headers: Optional[Dict[str, str]] = None,
         binary: bool = False, timeout: int = 30):
    cmd = ["curl", "-s", "--max-time", str(timeout), "--compressed"]
    for k, v in (headers or {}).items():
        cmd += ["-H", f"{k}: {v}"]
    cmd.append(url)
    r = subprocess.run(cmd, capture_output=True)
    if r.returncode != 0 and not r.stdout:
        raise RuntimeError(f"请求失败: {url} (curl exit {r.returncode})")
    return r.stdout if binary else r.stdout.decode("utf-8", "replace")


class WeatherQuery:
    """wttr.in 查询封装。base 可为 wttr.in 或等价备用域 wttr.is。"""

    def __init__(self, location: str = "", base: str = "wttr.in", timeout: int = 30):
        self.location = location
        self.base = base
        self.timeout = timeout

    # ---------- URL 组装 ----------
    def loc_path(self, location: Optional[str] = None) -> str:
        loc = self.location if location is None else location
        return f"{loc}" if loc else ""

    def url(self, params: Optional[Dict[str, str]] = None,
            base: Optional[str] = None, path: Optional[str] = None) -> str:
        host = base or self.base
        p = path if path is not None else self.loc_path()
        u = f"{host}/{p}" if p else host
        if params:
            qs = "&".join(k if v == "" else f"{k}={v}" for k, v in params.items())
            u += f"?{qs}"
        return u

    def get(self, params=None, base=None, path=None, headers=None,
            binary=False, use_scheme=True) -> Any:
        u = self.url(params, base, path)
        if use_scheme and not u.startswith("http"):
            u = "https://" + u
        return curl(u, headers, binary, timeout=self.timeout)

    # ---------- 视图选项 0/1/2/n/q/Q/F/A/d/T ----------
    def view(self, view: str = "full", lang: str = "zh", unit: Optional[str] = "m",
             plain: bool = True, noemoji: bool = False, follow: bool = False,
             flags: str = "") -> str:
        """视图组合。flags 为任意视图字母串（012nqQFTdA），如 "0q" → ?0q。
        默认去 Follow 行（follow=True 保留）；plain=False 保留 ANSI 颜色。"""
        p: Dict[str, str] = {}
        for c in (flags or ("" if view == "full" else view)):
            if c in "012nqQFTdA":
                p[c] = ""
        if not follow and "F" not in p:
            p["F"] = ""
        if plain and "T" not in p:
            p["T"] = ""
        if noemoji and "d" not in p:
            p["d"] = ""
        if unit:
            p[unit] = ""
        if lang:
            p["lang"] = lang
        return self.get(p)

    # ---------- JSON ----------
    def json_full(self) -> Dict[str, Any]:
        """format=j1：3 天预报，每天 8 组逐小时。"""
        return json.loads(self.get({"format": "j1"}))

    def json_lite(self) -> Dict[str, Any]:
        """format=j2：同 j1 但 weather[] 无 hourly（更轻，别盲猜字段！）。"""
        return json.loads(self.get({"format": "j2"}))

    # ---------- 一行 / 自定义 ----------
    def oneline(self, fmt: str = "3", lang: str = "", unit: Optional[str] = None,
                period: Optional[str] = None) -> str:
        p: Dict[str, str] = {"format": fmt}
        if lang:
            p["lang"] = lang
        if unit:
            p[unit] = ""
        if period:
            p["period"] = period
        return self.get(p)

    def batch(self, locations, fmt: str = "3") -> str:
        """{a,b,c} 花括号一次查多家（冒号形式只会重复查询取最后一家）。"""
        locs = locations if isinstance(locations, str) else ",".join(locations)
        return curl(f"https://{self.base}/{{{locs}}}?format={fmt}", timeout=self.timeout)

    # ---------- PNG ----------
    def png(self, output_path: Optional[str] = None, view: str = "",
            frame: bool = False, background: Optional[str] = None,
            transparency: Optional[int] = None, lang: str = "",
            notitle: bool = True, extra_flags: str = "") -> str:
        """PNG 选项写在文件名里：_0pq / background=RRGGBB / transparency=0..255。
        注意：裸 `_tqp` 后缀服务端拒绝（返回 "fail"）——用 transparency= 或 t+完整组合。"""
        if output_path is None:
            loc = self.location.replace("/", "_").replace("+", "_") or "current"
            output_path = f"weather_{loc}.png"
        chars = ""
        for c in view + extra_flags:
            if c in "012npq" and c not in chars:
                chars += c
        if frame and "p" not in chars:
            chars += "p"
        if notitle and "q" not in chars:
            chars += "q"
        named = []
        if background:
            named.append(f"background={background}")
        if transparency is not None:
            named.append(f"transparency={transparency}")
        if lang:
            named.append(f"lang={lang}")
        suffix = "_" + chars if chars else ""
        if transparency is not None and not (0 <= transparency <= 255):
            raise RuntimeError("transparency 必须在 0-255")
        if named:
            suffix += "_" + "_".join(named)
        url = f"https://{self.base}/{self.location}{suffix}.png"
        data = curl(url, binary=True, timeout=self.timeout)
        if data[:4] != b"\x89PNG":
            raise RuntimeError(f"PNG 获取失败: {url} -> {data[:32]!r}")
        with open(output_path, "wb") as f:
            f.write(data)
        return output_path

    # ---------- 月相 ----------
    def moon(self, date: Optional[str] = None, region: Optional[str] = None) -> str:
        """/Moon、/Moon@YYYY-MM-DD、/moon,+国家（地区与日期二选一）。"""
        if date:
            return self.get({}, path=f"Moon@{date}")
        if region:
            return self.get({}, path=f"Moon,+{region}")
        return self.get({}, path="Moon")

    # ---------- Prometheus ----------
    def prometheus(self) -> str:
        return self.get({"format": "p1"})

    # ---------- v2 / v3 ----------
    def v2(self, lang: str = "", nerd: Optional[str] = None) -> str:
        """v2.wttr.in 富数据版；nerd='day'|'night' 走 v2d/v2n 字体集。"""
        host = "v2.wttr.in"
        if nerd == "day":
            host = "v2d.wttr.in"
        elif nerd == "night":
            host = "v2n.wttr.in"
        params = {"lang": lang} if lang else {}
        return self.get(params, base=host)

    def v3(self, out: str = "png") -> Any:
        """v3 地图视图：png 字节 或 sixel 文本（v3.wttr.in/Region.sxl）。"""
        host = "v3.wttr.in"
        loc = self.location or ""
        if out == "sxl":
            return curl(f"https://{host}/{loc}.sxl" if loc else f"https://{host}/?sxl",
                        timeout=self.timeout)
        return curl(f"https://{host}/{loc}.png" if loc else f"https://{host}/.png",
                    binary=True, timeout=self.timeout)

    # ---------- 特殊 URL ----------
    def special(self, kind: str = "help") -> str:
        return self.get({}, path=f":{kind}")

    # ---------- HTML ----------
    def html(self) -> str:
        return self.get({}, headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) HTML_ UA"})

    # ---------- 地点形态直通（城市/POI+/Unicode/机场码/@域名/邮编/GPS） ----------
    def raw(self, params: Dict[str, str], headers=None, base=None) -> str:
        return self.get(params, base=base, headers=headers)


FORMATS = ["terminal", "view0", "view1", "view2", "narrow", "quiet", "superquiet",
           "nofollow", "plain", "compact", "json", "json-lite", "oneline", "batch",
           "png", "moon", "prometheus", "v2", "v2-day", "v2-night", "v3", "v3-sixel",
           "html", "help", "special"]

VIEWMAP = {"terminal": "full", "view0": "0", "view1": "1", "view2": "2",
           "narrow": "n", "quiet": "q", "superquiet": "Q", "nofollow": "full",
           "plain": "full", "compact": "full"}


def main():
    ap = argparse.ArgumentParser(
        description="wttr.in 天气查询工具（全免费能力覆盖版）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python weather.py Beijing                          全量卡片(纯文本+中文)
  python weather.py Beijing -f view0                 只看当前天气
  python weather.py Beijing -f oneline --custom-format '%l:+%c+%t+%h+%w'
  python weather.py -f batch Beijing Shanghai        花括号批量一次出
  python weather.py Paris -f png --background 00aaaa --transparency 150
  python weather.py -f moon --moon-date 2026-12-25     月相
  python weather.py Beijing -f moon --region China
  python weather.py Beijing -f v2                    v2 富数据
  python weather.py California -f v3 -o map.png      v3 地图
  python weather.py -f special --special translation 译者名单
  python weather.py Beijing -f json | jq .current_condition[0].temp_C
""")
    ap.add_argument("location", nargs="?", default="",
                    help="地点：城市/POI(+代空格)/机场三字码/@域名/邮编/GPS，留空=IP 定位")
    ap.add_argument("extra_locations", nargs="*",
                    help="batch 模式的其余地点（跟在首个地点后）")
    ap.add_argument("-f", "--format", default="terminal", choices=FORMATS,
                    help="输出格式")
    ap.add_argument("-l", "--lang", default="zh",
                    help="语言（zh/zh-tw/ja/en/fr/de/ru/...；lang=zh-hans 等会 ERR008）")
    ap.add_argument("-u", "--unit", default="m", choices=["m", "u", "M", ""],
                    help="m=公制 u=英制 M=公制风m/s 空=自动")
    ap.add_argument("--base-url", default="wttr.in",
                    help="wttr.in 或等价备用域 wttr.is")
    ap.add_argument("-o", "--output", help="PNG 输出路径")
    ap.add_argument("--custom-format", metavar="FMT",
                    help="一行格式 %%-notation（可用集见文档；%%e %%H %%L 服务端不支持）")
    ap.add_argument("--locations", nargs="*", help="batch 模式的多个地点")
    ap.add_argument("--period", help="批量查询节流秒数（配合 format）")
    ap.add_argument("-V", "--view-flags", default="", metavar="FLAGS",
                    help="任意视图字母组合直通，如 0q / nQ / FT（覆盖 -f 视图语义）")
    ap.add_argument("--ansi", action="store_true", help="保留彩色（不发 T）")
    ap.add_argument("--follow", action="store_true", help="保留 Follow 行")
    ap.add_argument("--frame", action="store_true", help="PNG 加边框 (p)")
    ap.add_argument("--background", metavar="RRGGBB", help="PNG 背景色")
    ap.add_argument("--transparency", type=int, metavar="0-255",
                    help="PNG 透明度 0-255（255=不透明）")
    ap.add_argument("--keep-title", action="store_true", help="PNG 保留标题(不加q)")
    ap.add_argument("--view", default="", choices=["", "0", "1", "2"],
                    help="PNG 内容详略")
    ap.add_argument("--moon-date", help="月相日期 YYYY-MM-DD")
    ap.add_argument("--region", help="月相地区，如 China/France")
    ap.add_argument("--special", default="help",
                    choices=["help", "bash.function", "translation"],
                    help="特殊 URL 类型")
    ap.add_argument("--timeout", type=int, default=30, help="curl 超时秒")
    args = ap.parse_args()

    w = WeatherQuery(args.location, base=args.base_url, timeout=args.timeout)
    f = args.format
    try:
        if f in VIEWMAP:
            noemoji = f == "compact"
            print(w.view(VIEWMAP.get(f, "full"), lang=args.lang, unit=args.unit or None,
                         plain=not args.ansi, noemoji=noemoji,
                         follow=args.follow, flags=args.view_flags))
        elif f == "json":
            print(json.dumps(w.json_full(), indent=2, ensure_ascii=False))
        elif f == "json-lite":
            print(json.dumps(w.json_lite(), indent=2, ensure_ascii=False))
        elif f == "prometheus":
            print(w.prometheus())
        elif f == "oneline":
            fmt = args.custom_format or "3"
            print(w.oneline(fmt, lang=args.lang,
                            unit=args.unit or None, period=args.period))
        elif f == "batch":
            locs = list(args.locations or [])
            if args.location:
                locs = [args.location] + [l for l in locs if l != args.location]
            if not args.locations and args.extra_locations:
                locs = [args.location] + list(args.extra_locations)
            if not args.locations and args.extra_locations is not None and not args.location:
                locs = []
            if not locs and args.location and "," in args.location:
                locs = args.location.split(",")
            if not locs:
                raise RuntimeError("batch 需要至少一个地点：weather.py -f batch Beijing Shanghai 或 --locations a b c")
            fmt = args.custom_format or "3"
            print(w.batch(locs, fmt))
        elif f == "png":
            path = w.png(args.output, view=args.view, frame=args.frame,
                         background=args.background, transparency=args.transparency,
                         lang=args.lang, notitle=not args.keep_title,
                         extra_flags=args.view_flags)
            print(f"Saved to {path}")
        elif f == "v3":
            data = w.v3("png")
            if isinstance(data, bytes):
                out = args.output or f"weather_{args.location or 'map'}.png"
                open(out, "wb").write(data)
                print(f"Saved to {out}")
            else:
                sys.stdout.write(data)
        elif f == "v3-sixel":
            sys.stdout.write(w.v3("sxl"))
        elif f in ("v2", "v2-day", "v2-night"):
            nerd = {"v2": None, "v2-day": "day", "v2-night": "night"}[f]
            print(w.v2(lang=args.lang, nerd=nerd))
        elif f == "moon":
            print(w.moon(args.moon_date, args.region))
        elif f == "html":
            print(w.html())
        elif f == "special":
            print(w.special(args.special))
        elif f == "help":
            print(w.special("help"))
    except (RuntimeError, json.JSONDecodeError, subprocess.SubprocessError) as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
