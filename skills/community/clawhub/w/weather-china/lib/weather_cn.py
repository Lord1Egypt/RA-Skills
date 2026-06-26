#!/usr/bin/env python3
"""
中国天气网天气预报查询工具 (weather.com.cn)
查询7天天气预报和生活指数数据，输出结构化数据供AI模型使用。
"""
import re
import sys
import json
import urllib.parse
import urllib.request
from html.parser import HTMLParser
from datetime import datetime


class WeatherHTMLParser(HTMLParser):
    """解析天气页面HTML，提取7天预报和生活指数数据。"""

    def __init__(self):
        super().__init__()
        self._capture = False
        self._target_id = None
        self._depth = 0
        self._data_parts = []
        self._result = ""

    def extract(self, html, target_id):
        """提取指定id的div内容。"""
        self._capture = False
        self._target_id = target_id
        self._depth = 0
        self._data_parts = []
        self._result = ""
        self.feed(html)
        return self._result

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag == "div" and attrs_dict.get("id") == self._target_id:
            self._capture = True
            self._depth = 1
            return
        if self._capture and tag == "div":
            self._depth += 1
        if self._capture:
            attr_str = " ".join(f'{k}="{v}"' for k, v in attrs)
            self._data_parts.append(f"<{tag} {attr_str}>" if attr_str else f"<{tag}>")

    def handle_endtag(self, tag):
        if self._capture:
            self._data_parts.append(f"</{tag}>")
            if tag == "div":
                self._depth -= 1
                if self._depth <= 0:
                    self._capture = False
                    self._result = "".join(self._data_parts)

    def handle_data(self, data):
        if self._capture:
            self._data_parts.append(data)


class ChinaWeather:
    """中国天气网天气查询。"""

    # 城市搜索API
    SEARCH_URL = "https://toy1.weather.com.cn/search?cityname={query}&callback=success_jsonpCallback&_={ts}"

    # 天气预报页面
    WEATHER_URL = "https://www.weather.com.cn/weather/{code}.shtml"

    # 请求超时（秒）
    REQUEST_TIMEOUT = 15

    # 请求头
    REQUEST_HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36",
        "Accept": "*/*",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Referer": "https://www.weather.com.cn/",
    }

    # 预置常用城市代码
    PRESET_CITIES = {
        "北京": "101010100", "上海": "101020100", "广州": "101280101",
        "深圳": "101280601", "成都": "101270101", "杭州": "101210101",
        "南京": "101190101", "武汉": "101200101", "西安": "101110101",
        "重庆": "101040100", "天津": "101030100", "沈阳": "101070101",
        "哈尔滨": "101050101", "长春": "101060101", "济南": "101120101",
        "青岛": "101120201", "郑州": "101180101", "长沙": "101250101",
        "南昌": "101240101", "福州": "101230101", "厦门": "101230201",
        "南宁": "101300101", "海口": "101310101", "三亚": "101310201",
        "贵阳": "101260101", "昆明": "101290101", "兰州": "101160101",
        "银川": "101170101", "西宁": "101150101", "拉萨": "101140101",
        "乌鲁木齐": "101130101", "石家庄": "101090101", "太原": "101100101",
        "呼和浩特": "101080101", "大连": "101070201", "苏州": "101190401",
        "无锡": "101190201", "宁波": "101210401", "温州": "101210701",
        "绍兴": "101210601", "金华": "101210901", "台州": "101211101",
        "嘉兴": "101210301", "湖州": "101210201", "衢州": "101211001",
        "丽水": "101211201", "舟山": "101211301", "东莞": "101281901",
        "佛山": "101281701", "珠海": "101280701", "中山": "101281801",
        "惠州": "101280301", "江门": "101280603", "肇庆": "101280901",
        "湛江": "101281001", "茂名": "101281101", "汕头": "101280401",
        "合肥": "101220101", "常州": "101191101", "徐州": "101190801",
        "烟台": "101120501", "潍坊": "101120601", "临沂": "101120901",
        "洛阳": "101180901", "襄阳": "101200201", "宜昌": "101200901",
        "芜湖": "101220301", "泉州": "101230501", "漳州": "101230601",
        "桂林": "101300501", "柳州": "101300301", "遵义": "101260201",
        "大理": "101290601", "丽江": "101291401", "西双版纳": "101291601",
        "延安": "101110600", "宝鸡": "101110901", "咸阳": "101110200",
        "香港": "101320101", "澳门": "101330101",
    }

    # 生活指数名称映射
    LIFE_INDEX_NAMES = {
        "感冒": "cold",
        "运动": "exercise",
        "过敏": "allergy",
        "穿衣": "clothing",
        "洗车": "carwash",
        "紫外线": "uv",
        "钓鱼": "fishing",
        "旅游": "travel",
        "晾晒": "drying",
        "交通": "traffic",
        "防晒": "sunscreen",
    }

    def __init__(self):
        self._parser = WeatherHTMLParser()

    def _http_get(self, url, encoding="utf-8"):
        """发送HTTP GET请求。"""
        req = urllib.request.Request(url, headers=self.REQUEST_HEADERS)
        try:
            with urllib.request.urlopen(req, timeout=self.REQUEST_TIMEOUT) as resp:
                return resp.read().decode(encoding, errors="replace")
        except Exception as e:
            raise ConnectionError(f"HTTP请求失败: {url} - {e}")

    def search_city(self, city_name):
        """通过搜索API查询城市代码。

        Returns:
            tuple: (城市代码, 城市显示名) 或 None
        """
        encoded = urllib.parse.quote(city_name)
        ts = int(datetime.now().timestamp() * 1000)
        url = self.SEARCH_URL.format(query=encoded, ts=ts)

        try:
            text = self._http_get(url)
        except ConnectionError:
            return None

        # 解析JSONP: success_jsonpCallback([...])
        match = re.search(r"success_jsonpCallback\((\[.*\])\)", text, re.DOTALL)
        if not match:
            return None

        try:
            results = json.loads(match.group(1))
        except json.JSONDecodeError:
            return None

        if not results:
            return None

        # 取第一个结果，解析格式: "代码~省份~城市名~英文名~..."
        ref = results[0].get("ref", "")
        parts = ref.split("~")
        if len(parts) >= 3:
            code = parts[0]
            display_name = parts[2]
            # 确保是有效的城市代码（以101开头的9位数字）
            if re.match(r"^101\d{6}$", code):
                return (code, display_name)

        return None

    def get_city_code(self, city_name):
        """获取城市代码，优先使用预置数据。

        Returns:
            tuple: (城市代码, 城市显示名)
        """
        city_name = city_name.strip()

        # 优先查预置城市
        if city_name in self.PRESET_CITIES:
            return (self.PRESET_CITIES[city_name], city_name)

        # 实时搜索
        result = self.search_city(city_name)
        if result:
            return result

        raise ValueError(f"未找到城市: {city_name}")

    def fetch_weather_html(self, city_code):
        """获取天气预报页面HTML。"""
        url = self.WEATHER_URL.format(code=city_code)
        return self._http_get(url)

    def parse_7day_forecast(self, html):
        """解析7天天气预报数据。

        从 <div id="7d"> 区域提取每天的天气信息。
        实际HTML结构 (per <li>):
          <h1>日期</h1>
          <p title="天气" class="wea">天气</p>
          <p class="tem"><span>高温</span>/<i>低温℃</i></p>
          <p class="win">
            <em><span title="风向"></span>...</em>
            <i>风力等级</i>
          </p>
        """
        block = self._parser.extract(html, "7d")
        if not block:
            return []

        forecasts = []

        # 按 <li> 拆分，逐个解析
        li_blocks = re.findall(r'<li[^>]*>(.*?)</li>', block, re.DOTALL)

        for li in li_blocks:
            # 跳过没有 <h1> 的空 li 元素
            m_date = re.search(r'<h1>([^<]+)</h1>', li)
            if not m_date:
                continue

            day = {
                "date": m_date.group(1).strip(),
                "weather": "",
                "temp_high": "",
                "temp_low": "",
                "wind": "",
                "wind_level": "",
            }

            # 天气状况 - 优先取title属性
            m = re.search(r'<p\s+title="([^"]*)"[^>]*class="wea"', li)
            if m:
                day["weather"] = m.group(1).strip()
            else:
                m = re.search(r'class="wea"[^>]*>([^<]+)<', li)
                if m:
                    day["weather"] = m.group(1).strip()

            # 温度 - <p class="tem"><span>高温℃</span>/<i>低温℃</i></p>
            # 注意：晚间"今天"可能无<span>高温，仅有<i>低温℃</i>
            m = re.search(r'<span>(\d+)℃?</span>', li)
            if m:
                day["temp_high"] = m.group(1) + "℃"
            m = re.search(r'<i>(\d+)℃</i>', li)
            if m:
                day["temp_low"] = m.group(1) + "℃"

            # 风向 - <em> 内第一个 <span title="风向">
            m = re.search(r'<span\s+title="([^"]*)"[^>]*class="[A-Z]', li)
            if m:
                day["wind"] = m.group(1).strip()

            # 风力等级 - <p class="win"> 内紧跟 </em> 后的 <i>等级</i>
            m = re.search(r'</em>\s*<i>([^<]+)</i>', li)
            if m:
                day["wind_level"] = m.group(1).strip()

            forecasts.append(day)

        return forecasts

    def parse_life_indices(self, html):
        """解析生活指数数据。

        从 <div id="livezs"> 区域提取生活指数。
        实际HTML结构 (per <li>):
          <li>
            <i class="gmi"></i>
            <span>级别</span>
            <em>类型指数</em>
            <p>描述</p>
          </li>
        """
        block = self._parser.extract(html, "livezs")
        if not block:
            return []

        indices = []

        # 按 <li> 拆分解析
        li_blocks = re.findall(r'<li[^>]*>(.*?)</li>', block, re.DOTALL)

        for li in li_blocks:
            # 级别 - <span>易发</span>
            m_level = re.search(r'<span>([^<]+)</span>', li)
            # 指数名 - <em>感冒指数</em>
            m_name = re.search(r'<em>([^<]+)</em>', li)
            # 描述 - <p>描述内容</p>
            m_desc = re.search(r'<p>([^<]+)</p>', li)

            if not (m_level and m_name):
                continue

            level = m_level.group(1).strip()
            name = m_name.group(1).strip()
            desc = m_desc.group(1).strip() if m_desc else ""

            # 提取指数类型关键词（去掉"指数"后缀）
            index_type = name.replace("指数", "").strip()
            key = self.LIFE_INDEX_NAMES.get(index_type, index_type)

            indices.append({
                "name": name,
                "key": key,
                "level": level,
                "description": desc,
            })

        return indices

    def query(self, city_name):
        """查询指定城市的天气预报。

        Args:
            city_name: 城市名称，如"南京"、"北京"

        Returns:
            dict: 包含城市信息、7天预报（含每日生活指数）的结构化数据
        """
        code, display_name = self.get_city_code(city_name)
        html = self.fetch_weather_html(code)

        forecast = self.parse_7day_forecast(html)
        life_indices = self.parse_life_indices(html)

        # 将生活指数按天分组后合并到对应天的forecast中
        # livezs中的指数是连续排列的，每天的指数类型数量相同
        if forecast and life_indices:
            num_days = len(forecast)
            indices_per_day = len(life_indices) // num_days if num_days > 0 else 0
            if indices_per_day > 0:
                for i, day in enumerate(forecast):
                    start = i * indices_per_day
                    end = start + indices_per_day
                    day["life_indices"] = life_indices[start:end]
            else:
                # 无法均分时，全部放到第一天
                forecast[0]["life_indices"] = life_indices
        
        return {
            "city": display_name,
            "city_code": code,
            "query_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "source": "weather.com.cn",
            "forecast": forecast,
        }

    def format_output(self, data):
        """格式化天气数据为文本输出（供AI模型读取）。"""
        if "error" in data:
            return f"错误: {data['error']}"

        lines = [
            f"城市: {data['city']} (代码: {data['city_code']})",
            f"数据来源: {data['source']}",
            f"查询时间: {data['query_time']}",
        ]

        for day in data.get("forecast", []):
            lines.append("")
            temp = f"{day['temp_high']}/{day['temp_low']}" if day.get("temp_high") else day.get("temp_low", "")
            wind_info = f"{day['wind']} {day['wind_level']}" if day.get("wind") else ""
            lines.append(f"[{day['date']}] {day['weather']}, {temp}, {wind_info}".rstrip(", "))

            # 每天的生活指数
            for idx in day.get("life_indices", []):
                lines.append(f"  {idx['name']}: {idx['level']} - {idx['description']}")

        return "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        print("Usage: weather_cn.py <command> <city>")
        print("Commands:")
        print("  query <city>  - 查询天气（格式化文本输出）")
        print("  json <city>   - 查询天气（JSON输出）")
        print()
        print("Examples:")
        print("  weather_cn.py query 南京")
        print("  weather_cn.py json 北京")
        sys.exit(1)

    weather = ChinaWeather()
    command = sys.argv[1].lower()
    city = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else ""

    if not city:
        print("错误: 请指定城市名称", file=sys.stderr)
        sys.exit(1)

    try:
        if command == "query":
            data = weather.query(city)
            print(weather.format_output(data))
        elif command == "json":
            data = weather.query(city)
            print(json.dumps(data, ensure_ascii=False, indent=2))
        else:
            print(f"未知命令: {command}", file=sys.stderr)
            sys.exit(1)
    except ValueError as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)
    except ConnectionError as e:
        print(f"网络错误: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"未知错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
