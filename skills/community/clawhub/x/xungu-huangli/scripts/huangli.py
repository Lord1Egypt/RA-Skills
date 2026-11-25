"""查询循古老黄历，默认输出传统文本格式。"""
import argparse
import json
import os
import sys
from datetime import date
from urllib.error import HTTPError, URLError
from urllib.request import HTTPRedirectHandler, Request, build_opener


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def get_calendar(day=None):
    url = 'https://www.xungufa.com/huangli/api/calendar'
    if day is not None:
        if date.fromisoformat(day).isoformat() != day:
            raise ValueError('日期格式须为 YYYY-MM-DD')
        url += '?date=' + day
    token = os.environ.get('HUANGLI_API_TOKEN')
    if not token:
        raise ValueError('请配置 HUANGLI_API_TOKEN，密钥可在 https://www.xungufa.com/apikey/ 创建。')
    req = Request(url, headers={'Authorization': 'Bearer ' + token, 'Accept': 'application/json'})
    with build_opener(NoRedirect()).open(req, timeout=30) as response:
        return json.load(response)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('day', nargs='?', help='YYYY-MM-DD，省略时查询北京时间今天')
    parser.add_argument('--json', action='store_true', help='输出原始 JSON')
    args = parser.parse_args()
    try:
        data = get_calendar(args.day)
        print(json.dumps(data, ensure_ascii=False) if args.json else format_calendar(data, args.day))
    except HTTPError as exc:
        sys.exit(f'HTTP {exc.code} {exc.reason}')
    except (ValueError, URLError, TimeoutError) as exc:
        sys.exit(str(exc))


def format_calendar(data, day=None):
    s = data['solar']
    l = data['lunar']
    g = data['ganzhi']
    h = data['huangli']
    tao = data['tao']
    buddha = data['buddha']

    # 干支格式：丙午 辛巳 甲申（不要年日月日）
    ganzhi = f"{g['year']} {g['month']} {g['day']}"

    # 道历：取年
    tao_year = tao.get('year_chinese', '')

    # 佛历：加"年"字
    buddha_year = f"{buddha.get('year_chinese', '')}年{buddha.get('month_chinese', '')}{buddha.get('day_chinese', '')}"

    result = f"""📅 {"指定日期黄历" if day else "今日黄历"}
───────────────────────────────────
公历: {s['date']} {s['week']} {s.get('xingzuo', '')}
农历: {l['date']}
干支: {ganzhi}
───────────────────────────────────
🟢 宜: {h['yi']}

🔴 忌: {h['ji']}

⏰ 吉时: {h['good_hours']}
🐲 冲煞: {h['chong_sha']}
🌙 月相: {l.get('yue_xiang', '')}
📿 道历: {tao_year}
☸️ 佛历: {buddha_year}"""

    if data.get('jieqi'):
        result += f"\n❄️ 节气: {data['jieqi']}"

    return result


if __name__ == '__main__':
    main()
