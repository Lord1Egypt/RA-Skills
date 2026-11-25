"""The paywall server — runs on the seller's machine.

Deliberately tiny and stdlib-only. It is a public listening socket on a box that
holds a private key, so every line here is attack surface and there is as little
of it as possible.

    stipend sell serve --port 8402

Endpoints:
    GET  /              catalogue, plain text
    GET  /item/<slug>   402 with the price, or the goods if payment is attached
    POST /item/<slug>   payment attached -> settle, then deliver
    GET  /health        liveness
"""

import base64
import json
import os
import threading
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from . import keystore, sell
from .config import chain_params, load_config, to_units

MAX_BODY = 32 * 1024
_delivery_lock = threading.Lock()
_settled_nonces = set()


class Handler(BaseHTTPRequestHandler):
    server_version = "stipend-storefront"

    # ---- helpers ----
    def _text(self, code, body, extra=None):
        raw = body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        for k, v in (extra or {}).items():
            self.send_header(k, v)
        self.end_headers()
        self.wfile.write(raw)

    def _json(self, code, obj, extra=None):
        raw = json.dumps(obj, indent=2).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(raw)))
        for k, v in (extra or {}).items():
            self.send_header(k, v)
        self.end_headers()
        self.wfile.write(raw)

    def _quote(self, slug, item):
        """402 with the price. payTo is the seller — never an intermediary."""
        body = sell.payment_requirements(slug, item, self.server.receiving_address)
        raw = json.dumps(body, separators=(",", ":")).encode()
        self._json(402, body, {"PAYMENT-REQUIRED": base64.b64encode(raw).decode()})

    def _deliver(self, slug, item):
        if item.get("file") and os.path.exists(item["file"]):
            with open(item["file"], "rb") as f:
                data = f.read()
            self.send_response(200)
            self.send_header("Content-Type", "application/octet-stream")
            self.send_header("Content-Disposition",
                             f'attachment; filename="{os.path.basename(item["file"])}"')
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
        else:
            self._text(200, item.get("text") or "(nothing attached to this item)")

    def _handle(self, method):
        path = self.path.split("?")[0].rstrip("/") or "/"

        if path == "/health":
            return self._json(200, {"ok": True, "items": len(sell.catalog())})

        if path == "/":
            items = sell.catalog()
            if not items:
                return self._text(200, "Nothing for sale yet.\n")
            lines = ["For sale — pay in USDC, no account needed.", ""]
            for slug, it in items.items():
                lines.append(f"  /item/{slug}   ${it['price_usdc']:.2f}   {it['name']}")
                if it.get("description"):
                    lines.append(f"      {it['description']}")
            lines += ["", "GET an item URL to see its price. Payment is x402 —",
                      "your agent handles it: stipend x402 fetch <url>", ""]
            return self._text(200, "\n".join(lines))

        if not path.startswith("/item/"):
            return self._text(404, "not found\n")

        slug = path[len("/item/"):]
        item = sell.catalog().get(slug)
        if not item:
            return self._text(404, "no such item\n")

        header = self.headers.get("PAYMENT-SIGNATURE") or self.headers.get("X-PAYMENT")
        if not header:
            return self._quote(slug, item)

        try:
            payment = json.loads(base64.b64decode(header + "=" * (-len(header) % 4)))
        except Exception:
            return self._json(400, {"error": "PAYMENT-SIGNATURE is not valid base64 JSON"})

        auth = (payment.get("payload") or {}).get("authorization") or {}
        nonce = auth.get("nonce", "")
        if not nonce:
            return self._json(400, {"error": "authorization has no nonce"})

        with _delivery_lock:
            if nonce in _settled_nonces:
                # Replay: deliver again, settle nothing twice. Harmless for a
                # digital good and kinder than an error if a download dropped.
                return self._deliver(slug, item)

            p = chain_params()
            expected = to_units(item["price_usdc"], p["decimals"])
            ok, detail = sell.settle(payment, self.server.receiving_address, expected)
            if not ok:
                return self._json(402, {"error": detail})

            _settled_nonces.add(nonce)
            sell.record_sale(slug, item, item["price_usdc"], detail, auth.get("from"))

        print(f"[sale] {item['name']} — ${item['price_usdc']:.2f} — tx {detail}", flush=True)
        return self._deliver(slug, item)

    def do_GET(self):
        try:
            self._handle("GET")
        except Exception as e:
            self._json(500, {"error": str(e)[:120]})

    def do_POST(self):
        try:
            length = int(self.headers.get("Content-Length", 0) or 0)
            if length > MAX_BODY:
                return self._json(413, {"error": "body too large"})
            if length:
                self.rfile.read(length)
            self._handle("POST")
        except Exception as e:
            self._json(500, {"error": str(e)[:120]})

    def log_message(self, fmt, *args):
        pass


def serve(port=8402, host="0.0.0.0"):
    address = keystore.address()      # fails loudly if there is no wallet
    httpd = ThreadingHTTPServer((host, port), Handler)
    httpd.receiving_address = address

    print(f"stipend storefront on http://{host}:{port}")
    print(f"  payments go directly to {address}")
    print(f"  {len(sell.catalog())} item(s) listed")
    print("  we are not in this transaction — buyer pays you on-chain, "
          "you pay the gas, nothing routes through stipend.sh")
    print("\n  Buyers must be able to reach this machine. Behind a home router "
          "you will need\n  a tunnel — that is yours to set up.\n")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nstopped")
        httpd.server_close()
