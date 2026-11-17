// Señales de "memoria inflada" que cuestan tokens en cada turno: líneas repetidas y volcados pegados.
// Todo es determinista y local. Devuelve solo conteos y caracteres recuperables, nunca el texto.

import { estimateTokens } from '../util.mjs';

const MIN_DUP_LEN = 25; // ignora líneas cortas (títulos, separadores, "- ok")
const BLOB_LINE_LEN = 1500; // una sola línea de más de 1,500 caracteres suele ser un volcado (base64, JSON, logs)
const BIG_FENCE_LINES = 60; // bloque de código de más de 60 líneas

function normalize(line) {
  return line.trim().replace(/\s+/g, ' ').toLowerCase();
}

function isStructural(line) {
  return /^(?:#{1,6}\s|[-*_=]{3,}\s*$|```|~~~|\|[-: |]+\|\s*$)/.test(line.trim());
}

/**
 * @param {string} text
 * @returns {{ dupLines: number, dupChars: number, blobLines: number, blobChars: number, bigFences: number, fenceChars: number, reclaimableChars: number, reclaimableTokens: number }}
 */
export function analyzeBloat(text) {
  const res = { dupLines: 0, dupChars: 0, blobLines: 0, blobChars: 0, bigFences: 0, fenceChars: 0, reclaimableChars: 0, reclaimableTokens: 0 };
  if (!text) return res;
  const lines = text.split(/\r?\n/);
  const seen = new Set();
  let inFence = false;
  let fenceStart = 0;
  let fenceLen = 0;

  for (let i = 0; i < lines.length; i++) {
    const raw = lines[i];
    const trimmed = raw.trim();

    if (/^(?:```|~~~)/.test(trimmed)) {
      if (!inFence) {
        inFence = true;
        fenceStart = i;
        fenceLen = 0;
      } else {
        inFence = false;
        const bodyLines = i - fenceStart - 1;
        if (bodyLines > BIG_FENCE_LINES) {
          res.bigFences++;
          res.fenceChars += fenceLen;
        }
      }
      continue;
    }
    if (inFence) {
      fenceLen += raw.length + 1;
      continue;
    }

    if (raw.length > BLOB_LINE_LEN) {
      res.blobLines++;
      res.blobChars += raw.length;
      continue; // no cuenta además como duplicado
    }
    if (trimmed.length < MIN_DUP_LEN || isStructural(raw)) continue;
    const key = normalize(raw);
    if (seen.has(key)) {
      res.dupLines++;
      res.dupChars += raw.length + 1;
    } else seen.add(key);
  }
  res.reclaimableChars = res.dupChars + res.blobChars + res.fenceChars;
  res.reclaimableTokens = estimateTokens(res.reclaimableChars);
  return res;
}
