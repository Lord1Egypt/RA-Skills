#!/usr/bin/env python3
"""
wttr.in 天气查询工具
支持多种输出格式和自定义选项

使用方法:
    python weather.py                    # 当前位置
    python weather.py Beijing            # 指定城市
    python weather.py Beijing -f json    # JSON 格式
    python weather.py Beijing -f oneline # 一行输出
    python weather.py Beijing -f v2      # 详细格式 (v2)
    python weather.py Paris -f png -o weather.png  # 下载 PNG
"""

import subprocess
import sys
import json
import argparse
from typing import Optional, Dict, Any


class WeatherQuery:
    """wttr.in 天气查询类"""

    def __init__(self, location: str = ""):
        self.location = location
        self.base_url = "wttr.in"

    def _build_url(self, path: str = "", params: Optional[Dict[str, str]] = None) -> str:
        """构建查询 URL"""
        if path.startswith("http"):
            base = path
        else:
            base = f"{self.base_url}/{self.location}" if self.location else self.base_url
            if path:
                base = base.rstrip("/") + "/" + path.lstrip("/")

        if params:
            param_str = "&".join(f"{k}={v}" for k, v in params.items())
            base += f"?{param_str}"

        return base

    def _curl(self, url: str, headers: Optional[Dict[str, str]] = None) -> str:
        """执行 curl 请求"""
        cmd = ["curl", "-s", url]
        if headers:
            for key, value in headers.items():
                cmd.extend(["-H", f"{key}: {value}"])
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.stdout

    def query(self, params: Optional[Dict[str, str]] = None,
              headers: Optional[Dict[str, str]] = None,
              use_v2: bool = False,
              use_v3: bool = False) -> str:
        """执行天气查询"""
        if use_v3:
            base = f"v3.wttr.in/{self.location}" if self.location else "v3.wttr.in"
        elif use_v2:
            base = f"v2.wttr.in/{self.location}" if self.location else "v2.wttr.in"
        else:
            base = f"{self.base_url}/{self.location}" if self.location else self.base_url

        if params:
            param_str = "&".join(f"{k}={v}" for k, v in params.items())
            base += f"?{param_str}"

        return self._curl(base, headers)

    # === 标准查询 ===

    def current(self, lang: str = "zh", unit: str = "m") -> str:
        """获取当前天气（标准终端输出）"""
        params = {"lang": lang, unit: ""}
        return self.query(params)

    def current_plain(self, lang: str = "zh") -> str:
        """获取纯文本天气（无 ANSI 颜色）"""
        params = {"lang": lang, "T": ""}
        return self.query(params)

    def current_compact(self, lang: str = "zh") -> str:
        """获取紧凑格式（标准控制台字符）"""
        params = {"lang": lang, "d": ""}
        return self.query(params)

    # === JSON 格式 ===

    def json_full(self) -> Dict[str, Any]:
        """获取完整 JSON 格式天气数据（含小时数据）"""
        result = self.query({"format": "j1"})
        return json.loads(result)

    def json_lite(self) -> Dict[str, Any]:
        """获取精简 JSON 格式（不含小时数据）"""
        result = self.query({"format": "j2"})
        return json.loads(result)

    # === 一行输出格式 ===

    def oneline(self, format_str: str = "3") -> str:
        """获取一行天气信息

        Args:
            format_str: 预设格式 (1-4) 或自定义格式 (%-notation)
        """
        return self.query({"format": format_str})

    # === PNG 图片格式 ===

    def png(self, output_path: Optional[str] = None,
            transparent: bool = False,
            transparency_level: int = 255) -> str:
        """下载 PNG 天气图

        Args:
            output_path: 输出文件路径，默认为 weather_<location>.png
            transparent: 是否透明背景
            transparency_level: 透明度 0-255
        """
        if output_path is None:
            loc = self.location.replace("/", "_").replace("+", "_") or "current"
            output_path = f"weather_{loc}.png"

        if transparent:
            suffix = f"_tqp{transparency_level}" if transparency_level < 255 else "_tqp"
        else:
            suffix = ""

        url = f"{self.base_url}/{self.location}.png{suffix}" if self.location else f"{self.base_url}.png{suffix}"
        cmd = ["wget", "-q", url, "-O", output_path]
        subprocess.run(cmd, check=True)
        return output_path

    # === v2 详细格式 ===

    def v2(self, lang: str = "zh") -> str:
        """获取 v2 详细格式天气数据"""
        return self.query({"lang": lang}, use_v2=True)

    def v2_day(self, lang: str = "zh") -> str:
        """获取 v2 日间模式（使用 Nerd Fonts）"""
        return self._curl(f"v2d.wttr.in/{self.location}?lang={lang}")

    def v2_night(self, lang: str = "zh") -> str:
        """获取 v2 夜间模式（使用 Nerd Fonts）"""
        return self._curl(f"v2n.wttr.in/{self.location}?lang={lang}")

    # === v3 地图格式 ===

    def v3(self, output_format: str = "png") -> str:
        """获取 v3 地图格式天气

        Args:
            output_format: png, sxl, html
        """
        return self.query({output_format: ""}, use_v3=True)

    # === 月相查询 ===

    def moon(self, date: Optional[str] = None) -> str:
        """查询月相

        Args:
            date: 日期，格式 YYYY-MM-DD，默认为今天
        """
        if date:
            return self._curl(f"wttr.in/Moon@{date}")
        return self._curl("wttr.in/Moon")

    # === Prometheus 格式 ===

    def prometheus(self) -> str:
        """获取 Prometheus 监控指标格式"""
        return self.query({"format": "p1"})

    # === 自定义格式 ===

    def custom_format(self, format_str: str, lang: str = "zh") -> str:
        """使用自定义格式字符串

        Args:
            format_str: 自定义格式，如 "%l: %c %t %h %w"
            lang: 语言代码
        """
        return self.query({"format": format_str, "lang": lang})

    # === 多地点查询 ===

    def multi_location(self, locations: list, format_str: str = "3") -> str:
        """多地点天气查询

        Args:
            locations: 地点列表
            format_str: 输出格式
        """
        loc_str = ":".join(locations)
        return self._curl(f"wttr.in/{loc_str}?format={format_str}")

    # === 特殊地点查询 ===

    def at_location(self, name: str, lang: str = "zh") -> str:
        """查询特殊地点（景点、山脉等）

        Args:
            name: 地点名称，如 "Eiffel+Tower"
        """
        return self._curl(f"wttr.in/~{name}?lang={lang}")

    def airport(self, code: str, lang: str = "zh") -> str:
        """查询机场天气

        Args:
            code: 机场三字代码，如 "PEK"
        """
        return self._curl(f"wttr.in/{code}?lang={lang}")


def main():
    parser = argparse.ArgumentParser(
        description="wttr.in 天气查询工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
    python weather.py                    # 当前位置
    python weather.py Beijing            # 北京天气
    python weather.py Beijing -f json    # JSON 格式
    python weather.py Beijing -f oneline # 一行输出
    python weather.py Beijing -f v2      # 详细格式
    python weather.py Paris -f png -o weather.png
    python weather.py --moon             # 月相
    python weather.py --v3               # 地图视图
        """
    )

    parser.add_argument("location", nargs="?", default="", help="地点名称")
    parser.add_argument("-f", "--format", default="terminal",
                        choices=["terminal", "json", "json-lite", "oneline", "png",
                                 "v2", "v2-day", "v2-night", "v3", "plain", "compact",
                                 "prometheus", "moon"],
                        help="输出格式")
    parser.add_argument("-l", "--lang", default="zh", help="语言代码")
    parser.add_argument("-u", "--unit", default="m", choices=["m", "u", "M"],
                        help="单位：m=公制，u=英制，M=公制+m/s")
    parser.add_argument("-o", "--output", help="输出文件路径（PNG 格式用）")
    parser.add_argument("--custom-format", help="自定义 format 参数（%%-notation）")
    parser.add_argument("--moon-date", help="月相查询日期 (YYYY-MM-DD)")
    parser.add_argument("--transparent", action="store_true", help="PNG 透明背景")
    parser.add_argument("--transparency", type=int, default=255, help="PNG 透明度 (0-255)")

    args = parser.parse_args()

    weather = WeatherQuery(args.location)

    try:
        if args.format == "json":
            data = weather.json_full()
            print(json.dumps(data, indent=2, ensure_ascii=False))
        elif args.format == "json-lite":
            data = weather.json_lite()
            print(json.dumps(data, indent=2, ensure_ascii=False))
        elif args.format == "png":
            output = args.output
            path = weather.png(output, transparent=args.transparent,
                              transparency_level=args.transparency)
            print(f"Saved to {path}")
        elif args.format == "oneline":
            fmt = args.custom_format or "3"
            print(weather.oneline(fmt))
        elif args.format == "v2":
            print(weather.v2(lang=args.lang))
        elif args.format == "v2-day":
            print(weather.v2_day(lang=args.lang))
        elif args.format == "v2-night":
            print(weather.v2_night(lang=args.lang))
        elif args.format == "v3":
            print(weather.v3())
        elif args.format == "plain":
            print(weather.current_plain(lang=args.lang))
        elif args.format == "compact":
            print(weather.current_compact(lang=args.lang))
        elif args.format == "prometheus":
            print(weather.prometheus())
        elif args.format == "moon":
            print(weather.moon(args.moon_date))
        else:
            # terminal - 标准输出
            params = {"lang": args.lang, args.unit: ""}
            print(weather.query(params))

    except subprocess.CalledProcessError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
