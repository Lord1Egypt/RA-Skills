#!/usr/bin/env node
/**
 * share-file.js — aggiunge un file alla cartella shared/ e genera il link
 * Uso: node share-file.js <percorso-file> [durata-minuti]
 */

const fs = require('fs');
const path = require('path');
const http = require('http');

const filePath = process.argv[2];
const ttl = parseInt(process.argv[3]) || 60;

if (!filePath) {
  console.error('Uso: node share-file.js <percorso-file> [durata-minuti]');
  process.exit(1);
}

const absPath = path.resolve(filePath);
if (!fs.existsSync(absPath)) {
  console.error(`File non trovato: ${absPath}`);
  process.exit(1);
}

const SHARED_DIR = process.env.SHARED_DIR ||
  path.join(__dirname, '../../../shared');

if (!fs.existsSync(SHARED_DIR)) fs.mkdirSync(SHARED_DIR, { recursive: true });

// Copia file in shared/
const dest = path.join(SHARED_DIR, path.basename(absPath));
fs.copyFileSync(absPath, dest);
console.log(`File copiato in shared/: ${path.basename(dest)}`);

// Chiedi al server di generare il link
const body = JSON.stringify({ filename: path.basename(dest), ttl });
const headers = {
  'Content-Type': 'application/json',
  'Content-Length': Buffer.byteLength(body),
};
if (process.env.SHARE_SECRET) {
  headers['x-share-secret'] = process.env.SHARE_SECRET;
}

const req = http.request({
  hostname: '127.0.0.1',
  port: process.env.SHARE_PORT || 5050,
  path: '/generate',
  method: 'POST',
  headers
}, (res) => {
  let data = '';
  res.on('data', chunk => data += chunk);
  res.on('end', () => {
    try {
      const json = JSON.parse(data);
      if (json.link) {
        console.log(`\n✅ Link pronto (valido ${json.expiresIn} min):`);
        console.log(json.link);
        console.log(`Scade alle: ${json.expiresAt}`);
      } else {
        console.error('Errore dal server:', data);
      }
    } catch {
      console.error('Risposta non valida dal server:', data);
    }
  });
});

req.on('error', (e) => {
  console.error('Impossibile contattare il server share. È avviato? Errore:', e.message);
  process.exit(1);
});

req.write(body);
req.end();
