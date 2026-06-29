#!/usr/bin/env node
const relayUrl = process.env.SAGE_TUNNEL_URL;
const token = process.env.SAGE_TUNNEL_TOKEN;
const localBase = (process.env.SAGE_TUNNEL_LOCAL_BASE_URL || 'http://127.0.0.1:8790').replace(/\/$/, '');
const localAuth = process.env.SAGE_TUNNEL_LOCAL_AUTH || '';

if (!relayUrl || !token) {
  console.error('Usage: SAGE_TUNNEL_URL=wss://your-worker/tunnel/connect SAGE_TUNNEL_TOKEN=... node scripts/sage_tunnel_connector.mjs');
  process.exit(2);
}

function connect() {
  const sep = relayUrl.includes('?') ? '&' : '?';
  const url = `${relayUrl}${sep}token=${encodeURIComponent(token)}`;
  const ws = new WebSocket(url);

  ws.addEventListener('open', () => {
    console.log(`[sage-tunnel] connected to ${relayUrl}; local=${localBase}`);
  });

  ws.addEventListener('message', async (event) => {
    let job;
    try { job = JSON.parse(event.data); } catch (err) { return; }
    if (!job || job.type !== 'chat.completions' || !job.id) return;

    try {
      const headers = { 'Content-Type': 'application/json' };
      if (localAuth) headers.Authorization = localAuth.startsWith('Bearer ') ? localAuth : `Bearer ${localAuth}`;
      const resp = await fetch(`${localBase}/v1/chat/completions`, {
        method: 'POST',
        headers,
        body: JSON.stringify(job.payload || {}),
      });
      const text = await resp.text();
      let body;
      try { body = JSON.parse(text); } catch (_) { body = { error: text || `HTTP ${resp.status}` }; }
      ws.send(JSON.stringify({ type: 'result', id: job.id, status: resp.status, body }));
    } catch (err) {
      ws.send(JSON.stringify({ type: 'result', id: job.id, status: 502, body: { error: String(err?.message || err) } }));
    }
  });

  ws.addEventListener('close', () => {
    console.error('[sage-tunnel] disconnected; reconnecting in 2s');
    setTimeout(connect, 2000);
  });

  ws.addEventListener('error', (err) => {
    console.error('[sage-tunnel] websocket error', err?.message || err);
    try { ws.close(); } catch (_) {}
  });
}

connect();
