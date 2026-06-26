import 'dotenv/config';
import express from 'express';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

// --- OpenClaw config auto-discovery ---
function loadOpenClawConfig() {
  // Search paths: ~/.openclaw/openclaw.json (Linux/macOS)
  const candidates = [
    path.join(os.homedir(), '.openclaw', 'openclaw.json'),
  ];

  for (const p of candidates) {
    try {
      const raw = fs.readFileSync(p, 'utf-8');
      const cfg = JSON.parse(raw);
      const port = cfg?.gateway?.port;
      const token = cfg?.gateway?.auth?.token;
      if (port && token) {
        console.log(`[voiceclaw] OpenClaw config loaded from ${p}`);
        return { url: `http://127.0.0.1:${port}`, token };
      }
    } catch {
      // file not found or parse error — try next
    }
  }
  return null;
}

const openclawAuto = loadOpenClawConfig();

const app = express();
app.use(express.json({ limit: '1mb' }));

const HOST = process.env.HOST || '127.0.0.1';
const PORT = process.env.PORT ? Number(process.env.PORT) : 8788;
const OPENCLAW_GATEWAY_URL = process.env.OPENCLAW_GATEWAY_URL || openclawAuto?.url || 'http://127.0.0.1:18789';
const OPENCLAW_GATEWAY_TOKEN = process.env.OPENCLAW_GATEWAY_TOKEN || openclawAuto?.token || '';
const VOICEVOX_URL = process.env.VOICEVOX_URL || 'http://127.0.0.1:50021';
const VOICEVOX_SPEAKER = process.env.VOICEVOX_SPEAKER ? Number(process.env.VOICEVOX_SPEAKER) : 1;
const OPENCLAW_MODEL = process.env.OPENCLAW_MODEL || 'openclaw';
const WAKE_WORDS = (process.env.WAKE_WORDS || 'アリスちゃん,ありすちゃん,アリスチャン,アリス,ありす').split(',').map(w => w.trim()).filter(Boolean);
const STT_LANG = process.env.STT_LANG || 'ja-JP';

if (!OPENCLAW_GATEWAY_TOKEN) {
  console.warn('[voiceclaw] ⚠ No OpenClaw gateway token found (env or ~/.openclaw/openclaw.json)');
} else if (openclawAuto && !process.env.OPENCLAW_GATEWAY_TOKEN) {
  console.log(`[voiceclaw] Using OpenClaw gateway at ${OPENCLAW_GATEWAY_URL} (auto-detected)`);
}

// Serve web UI
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const publicDir = path.join(__dirname, '..', 'public');

// Serve index explicitly (avoids environment-specific static quirks)
app.get('/', (req, res) => {
  res.sendFile(path.join(publicDir, 'index.html'));
});

// Static assets (if we add any later)
app.use(express.static(publicDir));

app.get('/health', (req, res) => {
  res.json({ ok: true });
});

// GET /api/config → client-safe settings
app.get('/api/config', (req, res) => {
  res.json({
    wakeWords: WAKE_WORDS,
    sttLang: STT_LANG,
    voicevoxSpeaker: VOICEVOX_SPEAKER,
  });
});

// POST /api/tts { text } → VOICEVOX → WAV audio
app.post('/api/tts', async (req, res) => {
  try {
    const text = String(req.body?.text || '').trim();
    if (!text) return res.status(400).json({ ok: false, error: 'text required' });

    const speakerId = req.body?.speaker ?? VOICEVOX_SPEAKER;

    // Step 1: audio_query
    const queryRes = await fetch(
      `${VOICEVOX_URL}/audio_query?text=${encodeURIComponent(text)}&speaker=${speakerId}`,
      { method: 'POST' }
    );
    if (!queryRes.ok) throw new Error(`VOICEVOX audio_query failed: ${queryRes.status}`);
    const query = await queryRes.json();

    // Step 2: synthesis
    const synthRes = await fetch(
      `${VOICEVOX_URL}/synthesis?speaker=${speakerId}`,
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(query),
      }
    );
    if (!synthRes.ok) throw new Error(`VOICEVOX synthesis failed: ${synthRes.status}`);

    const wav = await synthRes.arrayBuffer();
    res.set('Content-Type', 'audio/wav');
    res.send(Buffer.from(wav));
  } catch (e) {
    res.status(500).json({ ok: false, error: e?.message || String(e) });
  }
});

// POST /api/chat-stream { messages } → sentence-level SSE
// Each SSE event: data: {"sentence":"...", "done":false} or {"done":true,"fullText":"..."}
app.post('/api/chat-stream', async (req, res) => {
  if (!OPENCLAW_GATEWAY_TOKEN) {
    return res.status(500).json({ ok: false, error: 'OPENCLAW_GATEWAY_TOKEN not set' });
  }

  let messages;
  if (req.body?.messages?.length) {
    messages = req.body.messages;
  } else {
    const text = String(req.body?.text || '').trim();
    if (!text) return res.status(400).json({ ok: false, error: 'text or messages required' });
    messages = [{ role: 'user', content: text }];
  }

  // SSE headers
  res.setHeader('Content-Type', 'text/event-stream');
  res.setHeader('Cache-Control', 'no-cache');
  res.setHeader('Connection', 'keep-alive');
  res.flushHeaders();

  const sendEvent = (obj) => res.write(`data: ${JSON.stringify(obj)}\n\n`);

  try {
    const upstream = await fetch(`${OPENCLAW_GATEWAY_URL}/v1/chat/completions`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${OPENCLAW_GATEWAY_TOKEN}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ model: OPENCLAW_MODEL, user: 'voiceclaw', messages, stream: true }),
    });

    if (!upstream.ok) {
      sendEvent({ error: `OpenClaw error: ${upstream.status}` });
      return res.end();
    }

    const reader = upstream.body.getReader();
    const decoder = new TextDecoder();
    let lineBuffer = '';
    let textBuf = '';   // accumulates current incomplete sentence
    let fullText = '';
    const SENT_RE = /[。！？!?]/;

    const flushSentence = (force = false) => {
      let idx;
      while ((idx = textBuf.search(SENT_RE)) !== -1) {
        const sentence = textBuf.slice(0, idx + 1).trim();
        textBuf = textBuf.slice(idx + 1).trimStart();
        if (sentence) sendEvent({ sentence, done: false });
      }
      // On force (stream end), flush remainder
      if (force && textBuf.trim()) {
        sendEvent({ sentence: textBuf.trim(), done: false });
        textBuf = '';
      }
    };

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      lineBuffer += decoder.decode(value, { stream: true });
      const lines = lineBuffer.split('\n');
      lineBuffer = lines.pop() ?? '';

      for (const line of lines) {
        if (!line.startsWith('data: ')) continue;
        const raw = line.slice(6).trim();
        if (raw === '[DONE]') {
          flushSentence(true);
          sendEvent({ done: true, fullText });
          return res.end();
        }
        try {
          const parsed = JSON.parse(raw);
          const delta = parsed.choices?.[0]?.delta?.content ?? '';
          if (delta) {
            textBuf += delta;
            fullText += delta;
            flushSentence();
          }
        } catch {}
      }
    }

    flushSentence(true);
    sendEvent({ done: true, fullText });
    res.end();
  } catch (e) {
    sendEvent({ error: e?.message || String(e) });
    res.end();
  }
});

// POST /api/chat { text } → OpenClaw Gateway → { reply }
app.post('/api/chat', async (req, res) => {
  try {
    if (!OPENCLAW_GATEWAY_TOKEN) {
      return res.status(500).json({ ok: false, error: 'OPENCLAW_GATEWAY_TOKEN not set' });
    }

    // Accept { messages } (full history) or { text } (single turn)
    let messages;
    if (req.body?.messages?.length) {
      messages = req.body.messages;
    } else {
      const text = String(req.body?.text || '').trim();
      if (!text) return res.status(400).json({ ok: false, error: 'text or messages required' });
      messages = [{ role: 'user', content: text }];
    }

    const response = await fetch(`${OPENCLAW_GATEWAY_URL}/v1/chat/completions`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${OPENCLAW_GATEWAY_TOKEN}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        model: OPENCLAW_MODEL,
        user: 'voiceclaw',  // stable session key
        messages,
      }),
    });

    if (!response.ok) {
      const errText = await response.text().catch(() => '');
      throw new Error(`OpenClaw API error: ${response.status} ${errText}`);
    }

    const data = await response.json();
    const reply = data?.choices?.[0]?.message?.content;
    if (!reply) throw new Error('No reply from OpenClaw');

    res.json({ ok: true, reply });
  } catch (e) {
    res.status(500).json({ ok: false, error: e?.message || String(e) });
  }
});

app.listen(PORT, HOST, () => {
  console.log(`[voiceclaw] listening on http://${HOST}:${PORT}`);
});
