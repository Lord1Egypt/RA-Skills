export class SageTunnel {
  constructor(state, env) {
    this.state = state;
    this.env = env;
    this.connector = null;
    this.pending = new Map();
  }

  async fetch(request) {
    const url = new URL(request.url);

    if (url.pathname === "/tunnel/connect") {
      if (!this.authorized(request)) return new Response("unauthorized", { status: 401 });
      const upgrade = request.headers.get("Upgrade") || "";
      if (upgrade.toLowerCase() !== "websocket") return new Response("expected websocket", { status: 426 });

      const pair = new WebSocketPair();
      const [client, server] = Object.values(pair);
      server.accept();
      this.attachConnector(server);
      return new Response(null, { status: 101, webSocket: client });
    }

    if (url.pathname === "/health") {
      return Response.json({ ok: true, connector: Boolean(this.connector) });
    }

    if (url.pathname === "/v1/chat/completions" && request.method === "POST") {
      if (!this.authorized(request)) return Response.json({ error: "unauthorized" }, { status: 401 });
      if (!this.connector) return Response.json({ error: "no connector online" }, { status: 503 });

      const payload = await request.json();
      const id = crypto.randomUUID();
      const timeoutMs = Number(this.env.SAGE_TUNNEL_REQUEST_TIMEOUT_MS || 180000);
      const job = { type: "chat.completions", id, payload };

      const resultPromise = new Promise((resolve, reject) => {
        const timer = setTimeout(() => {
          this.pending.delete(id);
          reject(new Error("connector timeout"));
        }, timeoutMs);
        this.pending.set(id, { resolve, reject, timer });
      });

      try {
        this.connector.send(JSON.stringify(job));
        const result = await resultPromise;
        return new Response(JSON.stringify(result.body), {
          status: result.status || 200,
          headers: {
            "Content-Type": "application/json",
            "Cache-Control": "no-store",
          },
        });
      } catch (err) {
        return Response.json({ error: String(err?.message || err) }, { status: 504 });
      }
    }

    return new Response("not found", { status: 404 });
  }

  authorized(request) {
    const expected = this.env.SAGE_TUNNEL_TOKEN;
    if (!expected) return false;
    const auth = request.headers.get("Authorization") || "";
    const token = auth.startsWith("Bearer ") ? auth.slice(7) : new URL(request.url).searchParams.get("token") || "";
    return token && token === expected;
  }

  attachConnector(ws) {
    if (this.connector) {
      try { this.connector.close(1012, "replaced by newer connector"); } catch (_) {}
    }
    this.connector = ws;

    ws.addEventListener("message", (event) => {
      let msg;
      try { msg = JSON.parse(event.data); } catch (_) { return; }
      if (!msg || msg.type !== "result" || !msg.id) return;
      const pending = this.pending.get(msg.id);
      if (!pending) return;
      clearTimeout(pending.timer);
      this.pending.delete(msg.id);
      pending.resolve({ status: msg.status || 200, body: msg.body || {} });
    });

    ws.addEventListener("close", () => {
      if (this.connector === ws) this.connector = null;
      for (const [id, pending] of this.pending.entries()) {
        clearTimeout(pending.timer);
        pending.reject(new Error("connector disconnected"));
        this.pending.delete(id);
      }
    });

    ws.addEventListener("error", () => {
      try { ws.close(); } catch (_) {}
    });
  }
}

export default {
  async fetch(request, env) {
    const id = env.SAGE_TUNNEL.idFromName("default");
    const stub = env.SAGE_TUNNEL.get(id);
    return stub.fetch(request);
  },
};
