/**
 * server.js — Share One-Time Link server
 * Gestisce generazione token, download one-shot e cleanup automatico
 */

const express = require('express');
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const app = express();
app.use(express.json());

const PORT = process.env.SHARE_PORT || 5050;
const HOST = process.env.SHARE_HOST || '0.0.0.0';
const PUBLIC_URL = process.env.SHARE_PUBLIC_URL || `http://localhost:${PORT}`;
const SHARED_DIR = process.env.SHARED_DIR ||
  path.join(__dirname, '../../../shared');
const API_SECRET = process.env.SHARE_SECRET || null;

if (!API_SECRET) {
  console.error('[error] SHARE_SECRET env var is required but not set.');
  console.error('[error] Set SHARE_SECRET to a strong random string before starting the server.');
  console.error('[error] Example: SHARE_SECRET=$(openssl rand -hex 32) node server.js');
  process.exit(1);
}

// Auth middleware for protected endpoints (API_SECRET is always set)
function requireSecret(req, res, next) {
  const provided = req.headers['x-share-secret'] || req.query.secret;
  if (provided !== API_SECRET) {
    return res.status(401).json({ error: 'Unauthorized: missing or invalid secret' });
  }
  next();
}

if (!fs.existsSync(SHARED_DIR)) fs.mkdirSync(SHARED_DIR, { recursive: true });

// Map token -> { filename, expiresAt, downloaded }
const tokens = new Map();

// ─── POST /generate ──────────────────────────────────────────────────────────
// Body: { filename: string, ttl: number (minuti, default 60) }
app.post('/generate', requireSecret, (req, res) => {
  const { filename, ttl = 60 } = req.body || {};

  if (!filename) {
    return res.status(400).json({ error: 'filename richiesto' });
  }

  const filePath = path.join(SHARED_DIR, path.basename(filename));
  if (!fs.existsSync(filePath)) {
    return res.status(404).json({ error: `File non trovato: ${filename}` });
  }

  const token = crypto.randomBytes(32).toString('hex');
  const expiresAt = new Date(Date.now() + ttl * 60 * 1000);

  tokens.set(token, {
    filename: path.basename(filename),
    filePath,
    expiresAt,
    downloaded: false,
  });

  const link = `${PUBLIC_URL}/dl/${token}`;
  console.log(`[generate] token=${token.slice(0, 8)}... file=${filename} ttl=${ttl}min scade=${expiresAt.toISOString()}`);

  res.json({
    link,
    token,
    expiresIn: ttl,
    expiresAt: expiresAt.toLocaleString('it-IT', { timeZone: 'Europe/Rome' }),
  });
});

// ─── GET /dl/:token ───────────────────────────────────────────────────────────
app.get('/dl/:token', (req, res) => {
  const { token } = req.params;
  const entry = tokens.get(token);

  if (!entry) {
    return res.status(404).send('Link non valido o già utilizzato.');
  }

  if (new Date() > entry.expiresAt) {
    tokens.delete(token);
    cleanup(entry.filePath);
    return res.status(410).send('Link scaduto. Il file è stato eliminato.');
  }

  if (entry.downloaded) {
    return res.status(410).send('Link già utilizzato. Il file è stato eliminato.');
  }

  if (!fs.existsSync(entry.filePath)) {
    tokens.delete(token);
    return res.status(404).send('File non trovato.');
  }

  console.log(`[download] token=${token.slice(0, 8)}... file=${entry.filename}`);

  // Marca come scaricato PRIMA di inviare
  entry.downloaded = true;

  // Imposta headers per il download
  res.setHeader('Content-Disposition', `attachment; filename="${entry.filename}"`);
  res.setHeader('Content-Type', 'application/octet-stream');

  const fileStream = fs.createReadStream(entry.filePath);
  fileStream.pipe(res);

  fileStream.on('end', () => {
    tokens.delete(token);
    cleanup(entry.filePath);
  });

  fileStream.on('error', (err) => {
    console.error(`[download] errore stream: ${err.message}`);
    tokens.delete(token);
    cleanup(entry.filePath);
    if (!res.headersSent) res.status(500).send('Errore durante il download.');
  });
});

// ─── GET /status ─────────────────────────────────────────────────────────────
app.get('/status', requireSecret, (req, res) => {
  const active = [];
  for (const [token, entry] of tokens.entries()) {
    active.push({
      token: token.slice(0, 8) + '...',
      filename: entry.filename,
      expiresAt: entry.expiresAt.toISOString(),
      downloaded: entry.downloaded,
    });
  }
  res.json({ activeTokens: active.length, tokens: active });
});

// ─── Cleanup automatico ogni minuto ──────────────────────────────────────────
setInterval(() => {
  const now = new Date();
  for (const [token, entry] of tokens.entries()) {
    if (now > entry.expiresAt) {
      console.log(`[cleanup] token scaduto: ${token.slice(0, 8)}... file=${entry.filename}`);
      tokens.delete(token);
      cleanup(entry.filePath);
    }
  }
}, 60 * 1000);

function cleanup(filePath) {
  try {
    if (fs.existsSync(filePath)) {
      fs.unlinkSync(filePath);
      console.log(`[cleanup] file eliminato: ${filePath}`);
    }
  } catch (e) {
    console.error(`[cleanup] errore eliminazione ${filePath}: ${e.message}`);
  }
}

// ─── Start ────────────────────────────────────────────────────────────────────
app.listen(PORT, HOST, () => {
  console.log(`[share] Server avviato su http://${HOST}:${PORT}`);
  console.log(`[share] Cartella condivisione: ${SHARED_DIR}`);
  console.log(`[share] URL pubblico: ${PUBLIC_URL}`);
});
