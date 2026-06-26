#!/usr/bin/env python3
"""
CDP WebSocket Client — Chrome DevTools Protocol 通信核心层。
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import _encoding_fix  # noqa: F401

import json, threading, time, argparse
from urllib.request import urlopen, Request
from urllib.error import URLError

import importlib.util
if importlib.util.find_spec('websockets') is None:
    print("❌ 缺少依赖: websockets")
    print("   请先安装: pip install websockets")
    sys.exit(1)
import websockets
from websockets.sync.client import connect as ws_connect
HAS_WEBSOCKETS = True

CDP_WS_HANDSHAKE_TIMEOUT_S = 5.0
CDP_SEND_TIMEOUT_S = 30.0
CDP_HTTP_TIMEOUT_S = 5.0
CDP_CONNECT_RETRY_COUNT = 3
CDP_CONNECT_RETRY_DELAY_S = 0.5


def _http_get_json(url, timeout=CDP_HTTP_TIMEOUT_S):
    req = Request(url, headers={'Accept': 'application/json'})
    with urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode('utf-8'))


def _http_put_json(url, timeout=CDP_HTTP_TIMEOUT_S):
    req = Request(url, method='PUT', headers={'Accept': 'application/json'})
    with urlopen(req, timeout=timeout) as resp:
        body = resp.read().decode('utf-8')
        return json.loads(body) if body.strip() else {}


class CDPClient:
    def __init__(self, cdp_url):
        self.cdp_url = cdp_url.rstrip('/')
        self._ws = None; self._msg_id = 0; self._pending = {}
        self._lock = threading.Lock(); self._recv_thread = None
        self._closed = False; self._events = []; self._event_lock = threading.Lock()
        self._session_id = None; self._ws_only = False

    def connect(self):
        if not HAS_WEBSOCKETS: raise RuntimeError("Missing 'websockets'. Install: pip install websockets")
        ws_url = None
        try:
            version_info = self._get_version()
            ws_url = version_info.get('webSocketDebuggerUrl')
            if version_info.get('_proxy'): self._ws_only = False
        except Exception: pass
        if not ws_url:
            self._ws_only = True
            ws_url = self._connect_via_proxy()
        last_err = None
        for attempt in range(CDP_CONNECT_RETRY_COUNT):
            try:
                self._ws = ws_connect(ws_url, open_timeout=CDP_WS_HANDSHAKE_TIMEOUT_S, max_size=64*1024*1024)
                break
            except Exception as e:
                last_err = e
                if attempt < CDP_CONNECT_RETRY_COUNT - 1: time.sleep(CDP_CONNECT_RETRY_DELAY_S * (attempt + 1))
        if self._ws is None:
            raise RuntimeError(f"Failed to connect to CDP WebSocket after {CDP_CONNECT_RETRY_COUNT} attempts: {last_err}")
        self._closed = False
        self._recv_thread = threading.Thread(target=self._recv_loop, daemon=True, name='cdp-recv')
        self._recv_thread.start()

    def _connect_via_proxy(self):
        from urllib.parse import urlparse
        parsed = urlparse(self.cdp_url)
        chrome_port = parsed.port or 9222
        try:
            from cdp_proxy import ensure_proxy_running, get_proxy_state
            proxy_url = ensure_proxy_running(chrome_port=chrome_port)
            self.cdp_url = proxy_url; self._ws_only = False
            proxy_parsed = urlparse(proxy_url)
            proxy_host = proxy_parsed.hostname or '127.0.0.1'
            proxy_port = proxy_parsed.port or 9223
            ws_url = f'ws://{proxy_host}:{proxy_port}/devtools/browser'
            state = get_proxy_state()
            if state and state.get('auth_token'): ws_url += f'?token={state["auth_token"]}'
            return ws_url
        except Exception:
            host = parsed.hostname or '127.0.0.1'; port = parsed.port or 9222
            return f'ws://{host}:{port}/devtools/browser'

    def close(self):
        self._closed = True
        if self._ws:
            try: self._ws.close()
            except Exception: pass
            self._ws = None

    @property
    def connected(self): return self._ws is not None and not self._closed

    def send(self, method, params=None, timeout=CDP_SEND_TIMEOUT_S):
        if not self.connected: raise RuntimeError("Not connected to CDP")
        with self._lock: self._msg_id += 1; msg_id = self._msg_id
        msg = {'id': msg_id, 'method': method}
        if params: msg['params'] = params
        if self._session_id: msg['sessionId'] = self._session_id
        event = threading.Event(); holder = {'result': None, 'error': None}
        self._pending[msg_id] = (event, holder)
        self._ws.send(json.dumps(msg))
        if not event.wait(timeout=timeout):
            self._pending.pop(msg_id, None)
            raise RuntimeError(f"CDP command '{method}' timed out after {timeout}s (id={msg_id})")
        self._pending.pop(msg_id, None)
        if holder['error']:
            err = holder['error']
            raise RuntimeError(f"CDP error for '{method}': [{err.get('code')}] {err.get('message')}")
        return holder['result'] or {}

    def list_tabs(self):
        if not self._ws_only:
            try:
                targets = _http_get_json(f"{self.cdp_url}/json/list")
                return [{'id': t.get('id',''), 'type': t.get('type',''), 'title': t.get('title',''),
                         'url': t.get('url',''), 'webSocketDebuggerUrl': t.get('webSocketDebuggerUrl','')}
                        for t in targets if t.get('type') == 'page']
            except Exception: pass
        if not self.connected: raise RuntimeError("Not connected — call connect() first")
        old = self._session_id; self._session_id = None
        try: result = self.send('Target.getTargets')
        finally: self._session_id = old
        return [{'id': t.get('targetId',''), 'type': t.get('type',''), 'title': t.get('title',''),
                 'url': t.get('url',''), 'webSocketDebuggerUrl': ''}
                for t in result.get('targetInfos',[]) if t.get('type') == 'page']

    def create_tab(self, url='about:blank'):
        if not self._ws_only:
            try:
                from urllib.parse import quote
                endpoint = f"{self.cdp_url}/json/new?{quote(url, safe='')}"
                try: target = _http_put_json(endpoint)
                except Exception: target = _http_get_json(endpoint)
                return {'id': target.get('id',''), 'type': target.get('type',''),
                        'title': target.get('title',''), 'url': target.get('url',''),
                        'webSocketDebuggerUrl': target.get('webSocketDebuggerUrl','')}
            except Exception: pass
        if not self.connected: raise RuntimeError("Not connected — call connect() first")
        old = self._session_id; self._session_id = None
        try: result = self.send('Target.createTarget', {'url': url})
        finally: self._session_id = old
        tid = result.get('targetId', '')
        return {'id': tid, 'type': 'page', 'title': '', 'url': url, 'webSocketDebuggerUrl': ''}

    def close_tab(self, target_id):
        if not self._ws_only:
            try:
                req = Request(f"{self.cdp_url}/json/close/{target_id}", headers={'Accept': 'application/json'})
                with urlopen(req, timeout=CDP_HTTP_TIMEOUT_S) as resp: resp.read()
                return
            except Exception: pass
        if not self.connected: raise RuntimeError("Not connected — call connect() first")
        old = self._session_id; self._session_id = None
        try: self.send('Target.closeTarget', {'targetId': target_id})
        finally: self._session_id = old

    def activate_tab(self, target_id):
        if not self._ws_only:
            try: _http_get_json(f"{self.cdp_url}/json/activate/{target_id}"); return
            except Exception: pass
        if not self.connected: raise RuntimeError("Not connected — call connect() first")
        old = self._session_id; self._session_id = None
        try: self.send('Target.activateTarget', {'targetId': target_id})
        finally: self._session_id = old

    def attach(self, target_id):
        result = self.send('Target.attachToTarget', {'targetId': target_id, 'flatten': True})
        self._session_id = result.get('sessionId')
        if not self._session_id: raise RuntimeError(f"Failed to attach to target {target_id}: no sessionId")

    def detach(self):
        if self._session_id:
            try:
                old = self._session_id; self._session_id = None
                self.send('Target.detachFromTarget', {'sessionId': old})
            except Exception: pass
            self._session_id = None

    def get_events(self, method=None, clear=True):
        with self._event_lock:
            if method:
                matched = [e for e in self._events if e.get('method') == method]
                if clear: self._events = [e for e in self._events if e.get('method') != method]
            else:
                matched = list(self._events)
                if clear: self._events.clear()
        return matched

    def wait_for_event(self, method, timeout=30.0):
        deadline = time.time() + timeout
        while time.time() < deadline:
            events = self.get_events(method, clear=True)
            if events: return events[0]
            time.sleep(0.1)
        raise RuntimeError(f"Timeout waiting for CDP event '{method}' after {timeout}s")

    def get_version(self): return self._get_version()
    def _get_version(self): return _http_get_json(f"{self.cdp_url}/json/version")

    def _recv_loop(self):
        while not self._closed and self._ws:
            try: raw = self._ws.recv(timeout=1.0)
            except TimeoutError: continue
            except Exception as e:
                if not self._closed:
                    cls_name = type(e).__name__
                    if 'ConnectionClosed' not in cls_name:
                        import traceback
                        print(f"[cdp-client] _recv_loop error: {cls_name}: {e}", file=__import__('sys').stderr, flush=True)
                self._closed = True
                break
            try: msg = json.loads(raw)
            except json.JSONDecodeError: continue
            if 'id' in msg:
                pending = self._pending.get(msg['id'])
                if pending:
                    event, holder = pending
                    if 'error' in msg: holder['error'] = msg['error']
                    else: holder['result'] = msg.get('result')
                    event.set()
            elif 'method' in msg:
                with self._event_lock:
                    self._events.append(msg)
                    if len(self._events) > 1000: self._events = self._events[-500:]


def main():
    parser = argparse.ArgumentParser(description='CDP Client')
    parser.add_argument('--cdp-url', default='http://localhost:9222')
    sub = parser.add_subparsers(dest='command')
    sub.add_parser('version', help='Show browser version')
    sub.add_parser('tabs', help='List open tabs')
    open_p = sub.add_parser('open', help='Open a new tab')
    open_p.add_argument('url')
    eval_p = sub.add_parser('eval', help='Evaluate JS')
    eval_p.add_argument('expression')
    args = parser.parse_args()
    if not args.command: parser.print_help(); sys.exit(0)
    client = CDPClient(args.cdp_url)
    if args.command == 'version': print(json.dumps(client.get_version(), indent=2, ensure_ascii=False))
    elif args.command == 'tabs':
        tabs = client.list_tabs()
        for i, t in enumerate(tabs): print(f"  [{i}] {t['title']} — {t['url']}")
        if not tabs: print("  (no tabs)")
    elif args.command == 'open':
        tab = client.create_tab(args.url); print(f"Opened: {tab['id']}")
    elif args.command == 'eval':
        client.connect(); tabs = client.list_tabs()
        if not tabs: print("No tabs"); sys.exit(1)
        client.attach(tabs[0]['id'])
        result = client.send('Runtime.evaluate', {'expression': args.expression, 'returnByValue': True})
        val = result.get('result', {}).get('value')
        print(json.dumps(val, indent=2, ensure_ascii=False) if val is not None else 'undefined')
        client.close()


if __name__ == '__main__': main()
