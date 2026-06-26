#!/usr/bin/env python3
"""
Browser Actions — 通过 CDP 实现页面交互操作。
"""

import base64, json, os, sys, time, argparse
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import _encoding_fix  # noqa: F401
from cdp_client import CDPClient
from page_snapshot import PageSnapshot


KEY_DEFINITIONS = {
    'enter': {'key': 'Enter', 'code': 'Enter', 'keyCode': 13, 'text': '\r'},
    'return': {'key': 'Enter', 'code': 'Enter', 'keyCode': 13, 'text': '\r'},
    'tab': {'key': 'Tab', 'code': 'Tab', 'keyCode': 9},
    'escape': {'key': 'Escape', 'code': 'Escape', 'keyCode': 27},
    'esc': {'key': 'Escape', 'code': 'Escape', 'keyCode': 27},
    'backspace': {'key': 'Backspace', 'code': 'Backspace', 'keyCode': 8},
    'delete': {'key': 'Delete', 'code': 'Delete', 'keyCode': 46},
    'space': {'key': ' ', 'code': 'Space', 'keyCode': 32, 'text': ' '},
    'arrowup': {'key': 'ArrowUp', 'code': 'ArrowUp', 'keyCode': 38},
    'arrowdown': {'key': 'ArrowDown', 'code': 'ArrowDown', 'keyCode': 40},
    'arrowleft': {'key': 'ArrowLeft', 'code': 'ArrowLeft', 'keyCode': 37},
    'arrowright': {'key': 'ArrowRight', 'code': 'ArrowRight', 'keyCode': 39},
    'home': {'key': 'Home', 'code': 'Home', 'keyCode': 36},
    'end': {'key': 'End', 'code': 'End', 'keyCode': 35},
    'pageup': {'key': 'PageUp', 'code': 'PageUp', 'keyCode': 33},
    'pagedown': {'key': 'PageDown', 'code': 'PageDown', 'keyCode': 34},
    'f1': {'key': 'F1', 'code': 'F1', 'keyCode': 112},
    'f2': {'key': 'F2', 'code': 'F2', 'keyCode': 113},
    'f3': {'key': 'F3', 'code': 'F3', 'keyCode': 114},
    'f4': {'key': 'F4', 'code': 'F4', 'keyCode': 115},
    'f5': {'key': 'F5', 'code': 'F5', 'keyCode': 116},
    'f12': {'key': 'F12', 'code': 'F12', 'keyCode': 123},
}


def _resolve_key(key_name):
    lower = key_name.lower().replace(' ', '')
    if lower in KEY_DEFINITIONS:
        return KEY_DEFINITIONS[lower]
    if len(key_name) == 1:
        code = ord(key_name)
        return {'key': key_name, 'code': f'Key{key_name.upper()}' if key_name.isalpha() else '', 'keyCode': code, 'text': key_name}
    return {'key': key_name, 'code': '', 'keyCode': 0}


class BrowserActions:
    def __init__(self, client, snapshot=None):
        self._client = client
        self._snapshot = snapshot

    def navigate(self, url, wait_until='load', timeout=30.0):
        from urllib.parse import urlparse
        parsed = urlparse(url)
        ALLOWED_SCHEMES = {'http', 'https', 'about', 'chrome', 'edge'}
        if parsed.scheme and parsed.scheme.lower() not in ALLOWED_SCHEMES:
            raise ValueError(f"Blocked navigation to '{parsed.scheme}://' URL.")
        if parsed.hostname:
            import ipaddress
            try:
                ip = ipaddress.ip_address(parsed.hostname)
                if ip.is_private and parsed.hostname != '127.0.0.1':
                    raise ValueError(f"Blocked navigation to private IP: {parsed.hostname}")
            except ValueError as ve:
                if 'Blocked' in str(ve):
                    raise
                pass
            BLOCKED_HOSTS = {'metadata.google.internal', '169.254.169.254'}
            if parsed.hostname in BLOCKED_HOSTS:
                raise ValueError(f"Blocked navigation to metadata endpoint: {parsed.hostname}")
        self._client.send('Page.enable')
        result = self._client.send('Page.navigate', {'url': url})
        error_text = result.get('errorText')
        if error_text:
            raise RuntimeError(f"Navigation failed: {error_text}")
        self.wait_for_load(timeout=timeout)

    def go_back(self):
        history = self._client.send('Page.getNavigationHistory')
        current = history.get('currentIndex', 0)
        if current > 0:
            entries = history.get('entries', [])
            self._client.send('Page.navigateToHistoryEntry', {'entryId': entries[current - 1]['id']})

    def go_forward(self):
        history = self._client.send('Page.getNavigationHistory')
        current = history.get('currentIndex', 0)
        entries = history.get('entries', [])
        if current < len(entries) - 1:
            self._client.send('Page.navigateToHistoryEntry', {'entryId': entries[current + 1]['id']})

    def reload(self, ignore_cache=False):
        self._client.send('Page.reload', {'ignoreCache': ignore_cache})
        self.wait_for_load()

    def wait_for_load(self, timeout=30.0):
        try:
            self._client.send('Page.enable')
            result = self._client.send('Runtime.evaluate', {'expression': 'document.readyState', 'returnByValue': True})
            state = result.get('result', {}).get('value', '')
            if state == 'complete':
                return
            self._client.wait_for_event('Page.loadEventFired', timeout=timeout)
        except RuntimeError:
            pass

    def wait_for_selector(self, selector, timeout=10.0):
        deadline = time.time() + timeout
        while time.time() < deadline:
            result = self._client.send('Runtime.evaluate', {
                'expression': f'!!document.querySelector("{selector}")',
                'returnByValue': True,
            })
            if result.get('result', {}).get('value') is True:
                return True
            time.sleep(0.3)
        return False

    def wait_for_navigation(self, timeout=30.0):
        self._client.send('Page.enable')
        self._client.wait_for_event('Page.frameNavigated', timeout=timeout)
        self.wait_for_load(timeout=timeout)

    def wait(self, seconds):
        time.sleep(seconds)

    def click(self, x, y, button='left', click_count=1):
        self._client.send('Input.dispatchMouseEvent', {'type': 'mouseMoved', 'x': x, 'y': y})
        self._client.send('Input.dispatchMouseEvent', {'type': 'mousePressed', 'x': x, 'y': y, 'button': button, 'clickCount': click_count})
        self._client.send('Input.dispatchMouseEvent', {'type': 'mouseReleased', 'x': x, 'y': y, 'button': button, 'clickCount': click_count})

    def click_selector(self, selector, timeout=5.0):
        result = self._client.send('Runtime.evaluate', {
            'expression': f'''(function() {{const el = document.querySelector("{selector}"); if (!el) return null; const rect = el.getBoundingClientRect(); return {{x: rect.x + rect.width/2, y: rect.y + rect.height/2}};}})()''',
            'returnByValue': True,
        })
        pos = result.get('result', {}).get('value')
        if not pos:
            raise RuntimeError(f"Element not found: {selector}")
        self.click(pos['x'], pos['y'])

    def click_by_ref(self, ref):
        if not self._snapshot:
            raise RuntimeError("No PageSnapshot for ref-based interaction")
        refs = self._snapshot.refs
        if ref not in refs:
            raise RuntimeError(f"Ref '{ref}' not found. Re-run accessibility_tree().")
        node_info = refs[ref]
        role = node_info['role']
        name = node_info['name']
        backend_node_id = node_info.get('backendDOMNodeId')
        object_id = None
        if backend_node_id is not None:
            object_id, pos = self._resolve_position_and_object(backend_node_id)
            if pos:
                if object_id and self._verify_hit(object_id, pos['x'], pos['y']):
                    self.click(pos['x'], pos['y'])
                    return
                if object_id and self._dom_click(object_id):
                    return
                self.click(pos['x'], pos['y'])
                return
        if object_id:
            if self._dom_click(object_id):
                return
        if backend_node_id is not None and object_id is None:
            object_id = self._resolve_object_id(backend_node_id)
            if object_id and self._dom_click(object_id):
                return
        pos = self._resolve_position_by_js(role, name)
        if pos:
            self.click(pos['x'], pos['y'])
            return
        raise RuntimeError(f"Could not locate element for ref '{ref}' (role={role}, name={name})")

    def _resolve_object_id(self, backend_node_id):
        try:
            self._client.send('DOM.enable')
            resolve_result = self._client.send('DOM.resolveNode', {'backendNodeId': backend_node_id})
            return resolve_result.get('object', {}).get('objectId')
        except Exception:
            return None

    def _resolve_position_and_object(self, backend_node_id):
        try:
            self._client.send('DOM.enable')
            resolve_result = self._client.send('DOM.resolveNode', {'backendNodeId': backend_node_id})
            object_id = resolve_result.get('object', {}).get('objectId')
            if not object_id:
                return None, None
            fn_result = self._client.send('Runtime.callFunctionOn', {
                'objectId': object_id,
                'functionDeclaration': '''function() {const rect = this.getBoundingClientRect(); if(rect.width===0&&rect.height===0)return null; return {x:rect.x+rect.width/2, y:rect.y+rect.height/2, width:rect.width, height:rect.height};}''',
                'returnByValue': True,
            })
            pos = fn_result.get('result', {}).get('value')
            if pos and pos.get('width', 0) > 0 and pos.get('height', 0) > 0:
                return object_id, {'x': pos['x'], 'y': pos['y']}
            self._client.send('Runtime.callFunctionOn', {
                'objectId': object_id,
                'functionDeclaration': '''function() {this.scrollIntoViewIfNeeded?this.scrollIntoViewIfNeeded(true):this.scrollIntoView({block:"center",inline:"center"});}''',
            })
            time.sleep(0.3)
            fn_result = self._client.send('Runtime.callFunctionOn', {
                'objectId': object_id,
                'functionDeclaration': '''function() {const rect = this.getBoundingClientRect(); if(rect.width===0&&rect.height===0)return null; return {x:rect.x+rect.width/2, y:rect.y+rect.height/2};}''',
                'returnByValue': True,
            })
            pos = fn_result.get('result', {}).get('value')
            return object_id, pos
        except Exception:
            return None, None

    def _verify_hit(self, object_id, x, y):
        try:
            result = self._client.send('Runtime.callFunctionOn', {
                'objectId': object_id,
                'functionDeclaration': '''function(px,py){const hit=document.elementFromPoint(px,py);if(!hit)return false;return this===hit||this.contains(hit)||hit.contains(this);}''',
                'arguments': [{'value': x}, {'value': y}],
                'returnByValue': True,
            })
            return result.get('result', {}).get('value', False) is True
        except Exception:
            return True

    def _dom_click(self, object_id):
        try:
            result = self._client.send('Runtime.callFunctionOn', {
                'objectId': object_id,
                'functionDeclaration': '''function(){if(this.scrollIntoViewIfNeeded)this.scrollIntoViewIfNeeded(true);else if(this.scrollIntoView)this.scrollIntoView({block:"center",inline:"center"});if(this.focus)this.focus();this.dispatchEvent(new MouseEvent('mousedown',{bubbles:true,cancelable:true,view:window}));this.dispatchEvent(new MouseEvent('mouseup',{bubbles:true,cancelable:true,view:window}));this.dispatchEvent(new MouseEvent('click',{bubbles:true,cancelable:true,view:window}));return true;}''',
                'returnByValue': True,
            })
            return result.get('result', {}).get('value', False) is True
        except Exception:
            return False

    def _resolve_position_by_js(self, role, name):
        safe_name = name.replace('\\', '\\\\').replace('"', '\\"').replace("'", "\\'")
        js_code = f'''
(function(){{
try{{const byLabel=document.querySelectorAll('[aria-label="{safe_name}"]');for(const el of byLabel){{if(el.getAttribute('role')==='{role}'||!'{role}'){{const rect=el.getBoundingClientRect();if(rect.width>0&&rect.height>0)return{{x:rect.x+rect.width/2,y:rect.y+rect.height/2}};}}}}}}catch(e){{}}
try{{const byRole=document.querySelectorAll('[role="{role}"]');for(const el of byRole){{if(el.textContent.trim().includes("{safe_name}")||el.getAttribute('aria-label')==="{safe_name}"){{const rect=el.getBoundingClientRect();if(rect.width>0&&rect.height>0)return{{x:rect.x+rect.width/2,y:rect.y+rect.height/2}};}}}}}}catch(e){{}}
const tagMap={{'button':'button,input[type="button"],input[type="submit"]','link':'a','textbox':'input[type="text"],input[type="search"],input[type="email"],input[type="password"],input:not([type]),textarea','checkbox':'input[type="checkbox"]','radio':'input[type="radio"]','combobox':'select','searchbox':'input[type="search"]','img':'img'}};
const tagSelector=tagMap['{role}'];
if(tagSelector){{try{{const candidates=document.querySelectorAll(tagSelector);for(const el of candidates){{const elName=el.getAttribute('aria-label')||el.getAttribute('title')||el.getAttribute('placeholder')||el.textContent.trim();if(elName&&elName.includes("{safe_name}")){{const rect=el.getBoundingClientRect();if(rect.width>0&&rect.height>0)return{{x:rect.x+rect.width/2,y:rect.y+rect.height/2}};}}}}}}catch(e){{}}}}
return null;
}})()'''
        result = self._client.send('Runtime.evaluate', {'expression': js_code, 'returnByValue': True})
        return result.get('result', {}).get('value')

    def hover(self, x, y):
        self._client.send('Input.dispatchMouseEvent', {'type': 'mouseMoved', 'x': x, 'y': y})

    def drag(self, from_x, from_y, to_x, to_y, steps=10):
        self._client.send('Input.dispatchMouseEvent', {'type': 'mousePressed', 'x': from_x, 'y': from_y, 'button': 'left'})
        for i in range(1, steps + 1):
            t = i / steps
            x = from_x + (to_x - from_x) * t
            y = from_y + (to_y - from_y) * t
            self._client.send('Input.dispatchMouseEvent', {'type': 'mouseMoved', 'x': x, 'y': y})
            time.sleep(0.02)
        self._client.send('Input.dispatchMouseEvent', {'type': 'mouseReleased', 'x': to_x, 'y': to_y, 'button': 'left'})

    def scroll(self, x, y, delta_x=0, delta_y=-200):
        self._client.send('Input.dispatchMouseEvent', {'type': 'mouseWheel', 'x': x, 'y': y, 'deltaX': delta_x, 'deltaY': delta_y})

    def type_text(self, text, delay_ms=50):
        for char in text:
            self._client.send('Input.insertText', {'text': char})
            if delay_ms:
                time.sleep(delay_ms / 1000.0)

    def press_key(self, key):
        key_def = _resolve_key(key)
        params = {'type': 'keyDown', 'key': key_def.get('key', key),
                  'code': key_def.get('code', ''), 'windowsVirtualKeyCode': key_def.get('keyCode', 0)}
        if 'text' in key_def:
            params['text'] = key_def['text']
        self._client.send('Input.dispatchKeyEvent', params)
        self._client.send('Input.dispatchKeyEvent', {'type': 'keyUp', 'key': key_def.get('key', key),
                  'code': key_def.get('code', ''), 'windowsVirtualKeyCode': key_def.get('keyCode', 0)})

    def fill(self, selector, value):
        self._client.send('Runtime.evaluate', {
            'expression': f'(function(){{const el=document.querySelector("{selector}");if(el){{el.focus();el.value="";el.dispatchEvent(new Event("input",{{bubbles:true}}));}}}})()'
        })
        time.sleep(0.1)
        self.type_text(value, delay_ms=20)

    def select_option(self, selector, value):
        self._client.send('Runtime.evaluate', {
            'expression': f'(function(){{const el=document.querySelector("{selector}");if(el){{el.value="{value}";el.dispatchEvent(new Event("change",{{bubbles:true}}));}}}})()'
        })

    def screenshot(self, path='/tmp/screenshot.png', full_page=False, quality=None):
        params = {}
        if full_page:
            metrics = self._client.send('Page.getLayoutMetrics')
            cs = metrics.get('contentSize', {})
            params['clip'] = {'x': 0, 'y': 0, 'width': cs.get('width', 1920), 'height': cs.get('height', 1080), 'scale': 1}
        if path.lower().endswith(('.jpg', '.jpeg')):
            params['format'] = 'jpeg'
            if quality:
                params['quality'] = quality
        else:
            params['format'] = 'png'
        result = self._client.send('Page.captureScreenshot', params)
        data = result.get('data', '')
        img_bytes = base64.b64decode(data)
        os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
        with open(path, 'wb') as f:
            f.write(img_bytes)
        return path

    def pdf(self, path='/tmp/page.pdf', **kwargs):
        params = {'printBackground': True, 'preferCSSPageSize': True}
        params.update(kwargs)
        result = self._client.send('Page.printToPDF', params)
        data = result.get('data', '')
        pdf_bytes = base64.b64decode(data)
        os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
        with open(path, 'wb') as f:
            f.write(pdf_bytes)
        return path

    def evaluate(self, expression, return_by_value=True):
        result = self._client.send('Runtime.evaluate', {
            'expression': expression, 'returnByValue': return_by_value, 'awaitPromise': True,
        })
        remote_obj = result.get('result', {})
        exception = result.get('exceptionDetails')
        if exception:
            text = exception.get('text', '')
            desc = exception.get('exception', {}).get('description', '')
            raise RuntimeError(f"JS evaluation error: {text} — {desc}")
        return remote_obj.get('value') if return_by_value else remote_obj

    def list_tabs(self):
        return self._client.list_tabs()

    def new_tab(self, url='about:blank'):
        return self._client.create_tab(url)

    def switch_tab(self, target_id):
        self._client.detach()
        self._client.activate_tab(target_id)
        self._client.attach(target_id)

    def close_tab(self, target_id=None):
        if target_id:
            self._client.close_tab(target_id)
        else:
            self._client.send('Runtime.evaluate', {'expression': 'window.close()'})

    def get_console_messages(self, clear=True):
        events = self._client.get_events('Runtime.consoleAPICalled', clear=clear)
        messages = []
        for event in events:
            params = event.get('params', {})
            msg_type = params.get('type', 'log')
            args = params.get('args', [])
            text_parts = []
            for arg in args:
                val = arg.get('value', arg.get('description', str(arg.get('type', ''))))
                text_parts.append(str(val))
            messages.append({'type': msg_type, 'text': ' '.join(text_parts)})
        return messages

    def enable_console_capture(self):
        self._client.send('Runtime.enable')

    def get_title(self):
        result = self._client.send('Runtime.evaluate', {'expression': 'document.title', 'returnByValue': True})
        return str(result.get('result', {}).get('value', ''))

    def get_url(self):
        result = self._client.send('Runtime.evaluate', {'expression': 'window.location.href', 'returnByValue': True})
        return str(result.get('result', {}).get('value', ''))

    def get_cookies(self):
        result = self._client.send('Network.getCookies')
        return result.get('cookies', [])

    def set_viewport(self, width, height, device_scale_factor=1.0):
        self._client.send('Emulation.setDeviceMetricsOverride', {
            'width': width, 'height': height, 'deviceScaleFactor': device_scale_factor, 'mobile': False,
        })


def main():
    parser = argparse.ArgumentParser(description='Browser Actions')
    parser.add_argument('--cdp-url', default='http://localhost:9222')
    parser.add_argument('--target', default=None)
    sub = parser.add_subparsers(dest='command')
    nav_p = sub.add_parser('navigate', help='Navigate to URL')
    nav_p.add_argument('url')
    eval_p = sub.add_parser('eval', help='Evaluate JS')
    eval_p.add_argument('expression')
    sub.add_parser('tabs', help='List open tabs')
    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(0)
    client = CDPClient(args.cdp_url)
    client.connect()
    tabs = client.list_tabs()
    if not tabs:
        print("No tabs available")
        sys.exit(1)
    target_id = args.target or tabs[0]['id']
    client.attach(target_id)
    snapshot = PageSnapshot(client)
    actions = BrowserActions(client, snapshot)
    try:
        if args.command == 'navigate':
            actions.navigate(args.url)
            print(f"Title: {actions.get_title()}")
        elif args.command == 'eval':
            result = actions.evaluate(args.expression)
            print(json.dumps(result, indent=2, ensure_ascii=False) if result is not None else 'undefined')
        elif args.command == 'tabs':
            for i, t in enumerate(actions.list_tabs()):
                print(f"  [{i}] {t['title']} — {t['url']}")
    finally:
        client.close()


if __name__ == '__main__':
    main()
