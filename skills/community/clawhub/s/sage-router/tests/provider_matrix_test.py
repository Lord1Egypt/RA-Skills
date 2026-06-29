#!/usr/bin/env python3
"""Provider matrix integration test for Sage Router."""
import contextlib, http.server, json, os, socket, subprocess, sys, tempfile, threading, time, urllib.error, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROVIDER_PROFILES = json.loads((ROOT / 'provider-profiles.json').read_text())
PROVIDERS = [k for k in PROVIDER_PROFILES if not k.startswith('_')]
PROVIDERS.append('ollama')
MODEL_BY_PROVIDER = {
    'openai': 'gpt-4o-mini', 'anthropic': 'claude-sonnet-4', 'google': 'gemini-2.5-flash',
    'xai': 'grok-3-mini', 'perplexity': 'sonar',
    'groq': 'llama-3.3-70b-versatile', 'together': 'meta-llama/Llama-3.3-70B-Instruct-Turbo',
    'fireworks': 'accounts/fireworks/models/llama-v3p1-8b-instruct', 'mistral': 'mistral-small-latest',
    'cohere': 'command-r', 'azure-openai': 'gpt-4o', 'github-copilot': 'gpt-4o-copilot',
    'deepseek': 'deepseek-chat', 'darkbloom': 'darkbloom-chat', 'openrouter': 'openai/gpt-4o-mini',
    'ollama': 'qwen3.5:cloud',
}
REQUEST_MODES = {
    'fast': {'route': 'fast', 'thinking': 'low'},
    'balanced': {'route': 'balanced', 'thinking': 'medium'},
    'deep': {'route': 'deep', 'thinking': 'high'},
}

def free_port():
    with contextlib.closing(socket.socket()) as s:
        s.bind(('127.0.0.1', 0)); return s.getsockname()[1]

class MockProvider(http.server.BaseHTTPRequestHandler):
    calls = []
    def log_message(self, *_): return
    def _json(self, status, body):
        data = json.dumps(body).encode(); self.send_response(status); self.send_header('Content-Type','application/json'); self.send_header('Content-Length',str(len(data))); self.end_headers(); self.wfile.write(data)
    def do_GET(self):
        if self.path.endswith('/v1/models') or self.path == '/v1/models':
            self._json(200, {'data': [{'id': m, 'object': 'model'} for m in sorted(set(MODEL_BY_PROVIDER.values()))]})
        elif self.path == '/api/tags':
            self._json(200, {'models': [{'name': 'qwen3.5:cloud'}]})
        else:
            self._json(200, {'ok': True})
    def do_POST(self):
        payload = json.loads(self.rfile.read(int(self.headers.get('Content-Length','0') or '0')) or b'{}')
        MockProvider.calls.append({'path': self.path, 'payload': payload, 'headers': dict(self.headers)})
        if self.path.endswith('/api/chat'):
            model = payload.get('model','unknown'); self._json(200, {'model': model, 'message': {'role':'assistant','content': f'mock ollama ok {model}'}, 'done': True})
        elif '/v1/messages' in self.path:
            model = payload.get('model','unknown'); self._json(200, {'id':'msg_mock','type':'message','role':'assistant','model':model,'content':[{'type':'text','text':f'mock anthropic ok {model}'}], 'stop_reason':'end_turn', 'usage': {'input_tokens':1,'output_tokens':1}})
        elif ':generateContent' in self.path:
            model = self.path.split('/models/',1)[-1].split(':',1)[0]; self._json(200, {'candidates':[{'content':{'parts':[{'text':f'mock google ok {model}'}], 'role':'model'}, 'finishReason':'STOP'}]})
        else:
            model = payload.get('model','unknown'); self._json(200, {'id':'chatcmpl_mock','object':'chat.completion','model':model,'choices':[{'index':0,'message':{'role':'assistant','content':f'mock openai ok {model}'},'finish_reason':'stop'}], 'usage': {'prompt_tokens':1,'completion_tokens':1,'total_tokens':2}})

def post_json(url, payload, timeout=20):
    req = urllib.request.Request(url, data=json.dumps(payload).encode(), headers={'Content-Type':'application/json','Authorization':'Bearer test'})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode(); return resp.status, dict(resp.headers), json.loads(raw) if raw else None
    except urllib.error.HTTPError as e:
        raw = e.read().decode(errors='replace')
        try: body = json.loads(raw)
        except Exception: body = raw
        return e.code, dict(e.headers), body

def main():
    mock_port, router_port = free_port(), free_port()
    mock = http.server.ThreadingHTTPServer(('127.0.0.1', mock_port), MockProvider)
    threading.Thread(target=mock.serve_forever, daemon=True).start()
    base = f'http://127.0.0.1:{mock_port}'
    providers_cfg = {}
    for name in PROVIDERS:
        api = 'ollama' if name == 'ollama' else PROVIDER_PROFILES[name].get('api','openai-completions')
        if name == 'google': api = 'google-generative-ai'
        if name == 'anthropic': api = 'anthropic-messages'
        providers_cfg[name] = {'baseUrl': base, 'apiKey': 'test-key', 'api': api, 'models': [{'id': MODEL_BY_PROVIDER[name], 'name': MODEL_BY_PROVIDER[name]}]}
    with tempfile.TemporaryDirectory(prefix='sage-router-provider-matrix-') as td:
        cfg_path = Path(td) / 'openclaw.json'; cfg_path.write_text(json.dumps({'models': {'providers': providers_cfg}}))
        env = os.environ.copy(); env.update({'SAGE_ROUTER_OPENCLAW_CONFIG': str(cfg_path), 'SAGE_ROUTER_DARIO_BASE_URL': base, 'SAGE_ROUTER_DARIO_AUTOSTART': '0', 'SAGE_ROUTER_OLLAMA_AUTO_PULL_PATTERNS': '', 'SAGE_ROUTER_BUNDLED_OLLAMA_AUTOSTART': '0', 'SAGE_ROUTER_MAX_PROVIDER_ATTEMPTS': '1'})
        proc = subprocess.Popen([sys.executable, str(ROOT/'router.py'), '--port', str(router_port)], env=env, cwd=str(ROOT), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, text=True)
        try:
            health = None; deadline = time.time()+20
            while time.time() < deadline:
                try:
                    with urllib.request.urlopen(f'http://127.0.0.1:{router_port}/health', timeout=2) as resp: health=json.loads(resp.read()); break
                except Exception: time.sleep(0.25)
            if not health: raise RuntimeError('router did not become healthy')
            configured, reachable = set(health.get('configured',[])), set(health.get('providers',[]))
            expected = set(PROVIDERS); expected.remove('anthropic'); expected.add('dario')
            missing_configured = (set(PROVIDERS)-configured)-{'anthropic'}; missing_reachable = expected-reachable
            results=[]; failures=[]
            for provider in PROVIDERS:
                runtime_provider = 'dario' if provider == 'anthropic' else provider; model = MODEL_BY_PROVIDER[provider]
                for mode, flags in REQUEST_MODES.items():
                    st,h,b = post_json(f'http://127.0.0.1:{router_port}/v1/chat/completions', {'model': f'{runtime_provider}/{model}', 'route': flags['route'], 'thinking': flags['thinking'], 'messages': [{'role':'user','content':f'{mode} smoke test for {provider}'}], 'max_tokens':64})
                    content = ((b or {}).get('choices') or [{}])[0].get('message',{}).get('content','') if isinstance(b,dict) else ''
                    ok = st==200 and h.get('X-Sage-Router-Provider')==runtime_provider and content and (mode!='deep' or h.get('X-Sage-Router-Route-Mode')=='best')
                    row={'provider':provider,'runtimeProvider':runtime_provider,'mode':mode,'status':st,'selectedProvider':h.get('X-Sage-Router-Provider'),'routeMode':h.get('X-Sage-Router-Route-Mode'),'ok':bool(ok)}; results.append(row)
                    if not ok: failures.append({'row':row,'body':b})
            adapters=[]
            st,h,b=post_json(f'http://127.0.0.1:{router_port}/v1/messages', {'model':'claude-test','route':'deep','thinking':'high','max_tokens':64,'messages':[{'role':'user','content':'adapter smoke'}]}); adapters.append({'adapter':'anthropic-messages','status':st,'routeMode':h.get('X-Sage-Router-Route-Mode'),'ok':st==200 and h.get('X-Sage-Router-Route-Mode')=='best'})
            st,h,b=post_json(f'http://127.0.0.1:{router_port}/v1beta/models/gemini-test:generateContent', {'route':'fast','contents':[{'role':'user','parts':[{'text':'adapter smoke'}]}]}); adapters.append({'adapter':'google-generateContent','status':st,'routeMode':h.get('X-Sage-Router-Route-Mode'),'ok':st==200 and h.get('X-Sage-Router-Route-Mode')=='fast'})
            summary={'providersTested':PROVIDERS,'requestModes':list(REQUEST_MODES),'configuredCount':len(configured),'reachableCount':len(reachable),'missingConfigured':sorted(missing_configured),'missingReachable':sorted(missing_reachable),'matrixTotal':len(results),'matrixPassed':sum(1 for r in results if r['ok']),'matrixFailed':len(failures),'adapterTests':adapters,'failures':failures[:10],'results':results}
            print(json.dumps(summary, indent=2))
            return 1 if missing_configured or missing_reachable or failures or not all(t['ok'] for t in adapters) else 0
        finally:
            proc.terminate()
            try: proc.wait(timeout=5)
            except subprocess.TimeoutExpired: proc.kill()
            mock.shutdown()
if __name__ == '__main__': raise SystemExit(main())
