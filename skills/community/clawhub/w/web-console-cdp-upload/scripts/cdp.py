"""通过 CDP 驱动「本机已安装的 Chrome/Edge」做网页后台自动化（零安装，只依赖 websocket-client）。

子命令：
    chrome-path                        打印探测到的浏览器可执行文件（供启动命令使用）
    eval "<js 表达式>"                   在页面上下文求值
    shot <out.png>                     截图
    file <css选择器> <本地路径>            给 <input type=file> 塞文件

环境变量：
    CDP_PORT   调试端口，默认 9222
    CDP_MATCH  页面 URL 需包含的串；留空则取第一个 page 标签
"""
import json
import os
import platform
import sys
import urllib.request

import websocket

PORT = os.environ.get('CDP_PORT', '9222')
MATCH = os.environ.get('CDP_MATCH', '')


# ---------------- 浏览器探测 ----------------
def chrome_candidates():
    sysname = platform.system()
    if sysname == 'Windows':
        return [
            r'C:\Program Files\Google\Chrome\Application\chrome.exe',
            r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe',
            os.path.expandvars(r'%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe'),
            r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
            r'C:\Program Files\Microsoft\Edge\Application\msedge.exe',
        ]
    if sysname == 'Darwin':
        return [
            '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
            '/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge',
            os.path.expanduser('~/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'),
        ]
    return [
        '/usr/bin/google-chrome', '/usr/bin/google-chrome-stable',
        '/usr/bin/chromium', '/usr/bin/chromium-browser',
        '/snap/bin/chromium', '/usr/bin/microsoft-edge',
    ]


def detect_browser():
    for p in chrome_candidates():
        if os.path.exists(p):
            return p
    return ''


# ---------------- CDP ----------------
def targets():
    req = urllib.request.Request('http://127.0.0.1:%s/json/list' % PORT)
    return json.load(urllib.request.urlopen(req, timeout=10))


def pick():
    pages = [t for t in targets() if t.get('type') == 'page']
    if MATCH:
        pages = [t for t in pages if MATCH in (t.get('url') or '')]
    if not pages:
        raise SystemExit('未找到可用页面标签（CDP_MATCH=%r）。当前标签：\n%s'
                         % (MATCH, '\n'.join('%s %s' % (t.get('type'), t.get('url'))
                                             for t in targets())))
    return pages[0]


class CDP(object):
    def __init__(self, ws_url):
        # Chrome 新版会校验 WS 握手的 Origin，未加 --remote-allow-origins 时必须抑制
        self.ws = websocket.create_connection(ws_url, timeout=60, suppress_origin=True)
        self.i = 0

    def call(self, method, **params):
        self.i += 1
        self.ws.send(json.dumps({'id': self.i, 'method': method, 'params': params}))
        while True:
            msg = json.loads(self.ws.recv())
            if msg.get('id') == self.i:
                if 'error' in msg:
                    raise RuntimeError('%s -> %s' % (method, msg['error']))
                return msg.get('result', {})

    def eval(self, expr):
        r = self.call('Runtime.evaluate', expression=expr,
                      returnByValue=True, awaitPromise=True)
        if r.get('exceptionDetails'):
            return json.dumps(r['exceptionDetails'], ensure_ascii=False)
        v = r.get('result', {}).get('value')
        return v if isinstance(v, str) else json.dumps(v, ensure_ascii=False)

    def close(self):
        try:
            self.ws.close()
        except Exception:
            pass


def main():
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    cmd = sys.argv[1]
    if cmd == 'chrome-path':
        p = detect_browser()
        print(p if p else 'NOT_FOUND')
        return
    c = CDP(pick()['webSocketDebuggerUrl'])
    try:
        if cmd == 'eval':
            print(c.eval(sys.argv[2]))
        elif cmd == 'shot':
            import base64
            data = c.call('Page.captureScreenshot', format='png')['data']
            open(sys.argv[2], 'wb').write(base64.b64decode(data))
            print('saved', sys.argv[2])
        elif cmd == 'file':
            sel, path = sys.argv[2], sys.argv[3]
            doc = c.call('DOM.getDocument', depth=-1)
            node = c.call('DOM.querySelector', nodeId=doc['root']['nodeId'], selector=sel)
            if not node.get('nodeId'):
                raise SystemExit('选择器没匹配到节点: %s' % sel)
            c.call('DOM.setFileInputFiles', files=[os.path.abspath(path)],
                   nodeId=node['nodeId'])
            print('file set ->', sel, path)
        else:
            raise SystemExit('未知命令 %s' % cmd)
    finally:
        c.close()


if __name__ == '__main__':
    main()
