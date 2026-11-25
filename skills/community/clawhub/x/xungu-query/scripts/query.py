"""循古 OpenClaw 查询客户端。以标准输入接收 JSON，标准输出返回 JSON。"""
import argparse
import json
import os
import sys
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import HTTPRedirectHandler, Request, build_opener


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


ROUTES = {
    'bazi': '/api/agent/bazi',
    'liuyao': '/api/agent/liuyao',
    'daliuren': '/api/agent/daliuren',
    'ziwei': '/api/agent/ziwei',
    'qimen': '/api/agent/qimen',
    'locations': '/api/locations/search',
}


def query(action, params):
    if not isinstance(params, dict):
        raise ValueError('参数须为 JSON 对象')
    url = 'https://www.xungufa.com' + ROUTES[action]
    headers = {'Accept': 'application/json'}
    if action != 'locations':
        token = os.environ.get('XUNGU_API_TOKEN')
        if token:
            headers['Authorization'] = 'Bearer ' + token
        elif action != 'bazi':
            raise ValueError('请在 OpenClaw 中配置 XUNGU_API_TOKEN，密钥可在 https://www.xungufa.com/apikey/ 创建。')
    body = None
    if action == 'locations':
        if params:
            url += '?' + urlencode(params)
    else:
        headers['Content-Type'] = 'application/json'
        body = json.dumps(params).encode()
    req = Request(url, data=body, headers=headers)
    with build_opener(NoRedirect()).open(req, timeout=30) as resp:
        return json.load(resp)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=ROUTES)
    parser.add_argument('--chart', action='store_true', help='六爻或大六壬传统文本盘面')
    args = parser.parse_args()
    if args.chart and args.action not in ('liuyao', 'daliuren'):
        parser.error('--chart 适用于 liuyao 和 daliuren')
    try:
        data = query(args.action, json.load(sys.stdin))
        if args.chart:
            from format_courses import format_liuyao_result, format_daliuren_result
            formatter = format_liuyao_result if args.action == 'liuyao' else format_daliuren_result
            print(formatter(data))
        else:
            print(json.dumps(data, ensure_ascii=False))
    except HTTPError as exc:
        try:
            error = json.load(exc)
        except ValueError:
            error = {}
        sys.exit(f"HTTP {exc.code} {error.get('message') or error.get('error') or exc.reason}")
    except (ValueError, URLError, TimeoutError) as exc:
        sys.exit(str(exc))


if __name__ == '__main__':
    main()
