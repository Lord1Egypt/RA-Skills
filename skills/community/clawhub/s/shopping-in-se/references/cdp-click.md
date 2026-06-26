# CDP Coordinate Click — Bypassing Cross-Origin Iframes

## Background

The browser's same-origin policy prevents JavaScript from accessing the DOM of cross-origin iframes, which means the browser tool's ref/selector clicks do not work on Klarna/Stripe/Adyen payment iframes.

**Solution:** Use Chrome DevTools Protocol (CDP) to connect directly to the iframe's independent target, execute JS inside it, and dispatch mouse events. Physical mouse events are not subject to same-origin policy.

## CDP Connection

OpenClaw exposes the CDP interface at `ws://127.0.0.1:18800`.

```bash
# List all targets (pages and iframes)
curl -s http://127.0.0.1:18800/json
```

## Python Utility Functions

```python
import socket, struct, json, time, base64 as b64

def ws_connect(target_id):
    s = socket.socket()
    s.connect(('127.0.0.1', 18800))
    key = b64.b64encode(b'openclaw-cdp-key').decode()
    h = (f"GET /devtools/page/{target_id} HTTP/1.1\r\n"
         f"Host: 127.0.0.1:18800\r\n"
         f"Upgrade: websocket\r\nConnection: Upgrade\r\n"
         f"Sec-WebSocket-Key: {key}\r\nSec-WebSocket-Version: 13\r\n\r\n")
    s.send(h.encode())
    s.recv(2048)
    return s

def ws_send(s, mid, method, params={}):
    d = json.dumps({'id': mid, 'method': method, 'params': params}).encode()
    n = len(d)
    mask = b'\x01\x02\x03\x04'
    masked = bytes(b ^ mask[i%4] for i,b in enumerate(d))
    hdr = bytes([0x81, 0x80|n]) + mask if n<=125 else bytes([0x81,0xFE])+struct.pack('>H',n)+mask
    s.send(hdr+masked)

def ws_recv(s, timeout=4):
    results = []
    s.settimeout(timeout)
    while True:
        try:
            h = s.recv(2)
            n = h[1]&0x7F
            if n==126: n=struct.unpack('>H',s.recv(2))[0]
            elif n==127: n=struct.unpack('>Q',s.recv(8))[0]
            d=b''
            while len(d)<n: d+=s.recv(min(8192,n-len(d)))
            results.append(json.loads(d))
        except: break
    return results

def cdp_click(s, x, y, mid_base=1):
    """Dispatch a mouse click event at the given coordinates."""
    for mid, typ in [(mid_base,'mouseMoved'),(mid_base+1,'mousePressed'),(mid_base+2,'mouseReleased')]:
        ws_send(s, mid, 'Input.dispatchMouseEvent', {
            'type': typ, 'x': x, 'y': y,
            'button': 'left' if typ != 'mouseMoved' else 'none',
            'clickCount': 1 if typ == 'mousePressed' else 0
        })
        time.sleep(0.2)

def find_button_coords(s, text_contains):
    """Find the coordinates of a button containing the given text."""
    ws_send(s, 99, 'Runtime.evaluate', {'expression': f'''
    (function() {{
        const btn = Array.from(document.querySelectorAll("button")).find(b => b.innerText.includes("{text_contains}"));
        if (!btn) return JSON.stringify({{notfound: true, all: Array.from(document.querySelectorAll("button")).map(b=>b.innerText.trim().slice(0,20))}});
        const r = btn.getBoundingClientRect();
        return JSON.stringify({{x: r.left+r.width/2, y: r.top+r.height/2, text: btn.innerText.trim().slice(0,30)}});
    }})()
    '''})
    time.sleep(0.5)
    msgs = ws_recv(s)
    for m in msgs:
        if 'result' in m:
            try:
                return json.loads(m['result']['result']['value'])
            except: pass
    return None

def type_into_input(s, name, value, mid_base=10):
    """Fill an input field (e.g. Stripe card number)."""
    ws_send(s, mid_base, 'Runtime.evaluate', {'expression': f'''
    (function() {{
        const inp = document.querySelector('input[name="{name}"]');
        if (!inp) return "not found";
        inp.focus(); inp.click();
        return "ok";
    }})()
    '''})
    time.sleep(0.3)
    ws_recv(s)
    ws_send(s, mid_base+1, 'Input.insertText', {'text': value})
    time.sleep(0.3)
    ws_send(s, mid_base+2, 'Runtime.evaluate', {'expression': f'''
    (function() {{
        const inp = document.querySelector('input[name="{name}"]');
        if (!inp) return "not found";
        inp.dispatchEvent(new Event("input", {{bubbles: true}}));
        inp.dispatchEvent(new Event("change", {{bubbles: true}}));
        return inp.value;
    }})()
    '''})
    time.sleep(0.3)
    msgs = ws_recv(s)
    for m in msgs:
        if 'result' in m:
            print(f"  {name}: {m['result']['result'].get('value','')}")
```

## Klarna Payment Flow

```python
import urllib.request

# 1. Click "Betala köp" inside the Klarna iframe
tabs = json.loads(urllib.request.urlopen('http://127.0.0.1:18800/json').read())
kustom = next(t for t in tabs if 'kustom' in t.get('url','') and 'template' in t.get('url',''))

s = ws_connect(kustom['id'])
btn = find_button_coords(s, "Betala")
if btn and 'x' in btn:
    cdp_click(s, int(btn['x']), int(btn['y']))
s.close()

time.sleep(3)

# 2. Wait for Klarna login/confirmation page to appear
tabs = json.loads(urllib.request.urlopen('http://127.0.0.1:18800/json').read())
klarna_tab = next((t for t in tabs if 'klarna' in t.get('url','') and t.get('type')=='page'), None)
# → May show a BankID QR code or a direct confirmation page
```

## Stripe Card Entry

Stripe's card input fields live in an independent iframe target but can be accessed directly:

```python
# Find the Stripe elements-inner target
tabs = json.loads(urllib.request.urlopen('http://127.0.0.1:18800/json').read())
stripe = next(t for t in tabs if 'stripe.com/v3/elements-inner-accessory' in t.get('url',''))

s = ws_connect(stripe['id'])

# Verify input fields are present
ws_send(s, 1, 'Runtime.evaluate', {'expression': 'JSON.stringify(Array.from(document.querySelectorAll("input[name]")).map(i=>({name:i.name,placeholder:i.placeholder})))'})
# Should return: number, expiry, cvc

# Fill in card details (read from ~/Private/)
type_into_input(s, "number", "4273 1800 0443 8968", 10)
type_into_input(s, "expiry", "03/31", 20)
type_into_input(s, "cvc", "991", 30)

s.close()
```

## Common Target Identification

| Provider | URL Pattern | Purpose |
|----------|-------------|---------|
| Klarna Checkout | `kustom.co/kcoc/.../checkout-template` | Main payment iframe with "Betala köp" button |
| Klarna Login | `login.klarna.com` | BankID verification page |
| Klarna Confirm | `payments.klarna.com/app/main` | Final payment confirmation page |
| Stripe Card | `js.stripe.com/v3/elements-inner-accessory` | Card number / expiry / CVC input |
| Adyen Card | `checkoutshopper-live.adyen.com` | Card input (same approach as Stripe) |

## Confirming Success

Signs of a successful payment:
- **Apotea**: URL changes to `/kassa/KlarnaConfirmationV3?...`
- **Apoteket**: URL changes to `/orderbekraftelse/...`
- Page shows a thank-you or order confirmation message
