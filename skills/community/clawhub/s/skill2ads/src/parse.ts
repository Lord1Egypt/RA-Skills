/**
 * LLM output parser for ad JSON. Handles NDJSON, arrays, code fences, and
 * concatenated `}{` blobs. Adapted from coachbot/src/lib/generate-parser.ts.
 */

import { normalizeTargeting, normalizeSchedule } from "./targeting.js";
import type { GeneratedAd } from "./types.js";

const MAX_AD_COUNT = 5;

function coerceString(v: unknown): string | null {
  if (typeof v === "string") {
    const t = v.trim();
    return t.length > 0 ? t : null;
  }
  if (v === null || v === undefined) return null;
  const t = String(v).trim();
  return t.length > 0 ? t : null;
}

function stripCodeFences(raw: string) {
  let s = raw.trim();
  if (/^```(?:json)?\s*/i.test(s) && !/\n```\s*$/m.test(s)) {
    s = s.replace(/^```(?:json)?\s*/i, "");
  }
  return s.replace(/^```(?:json)?\s*/i, "").replace(/\s*```$/, "").trim();
}

function stripLeadingNonJson(s: string): string {
  const idx = s.search(/[\[{]/);
  return idx > 0 ? s.slice(idx) : s;
}

function tryRepair(s: string): string {
  return s.replace(/,\s*([}\]])/g, "$1");
}

function buildAd(ad: Record<string, unknown>): GeneratedAd {
  const hook = coerceString(ad.hook);
  const body = coerceString(ad.body);
  const cta = coerceString(ad.cta);
  if (!hook || !body || !cta) throw new Error("Ad missing hook, body, or cta.");
  return {
    intent: typeof ad.intent === "string" && ad.intent.trim() ? ad.intent.trim() : "Unspecified",
    hook,
    body,
    cta,
    visual_direction: typeof ad.visual_direction === "string" ? ad.visual_direction : "",
    why_it_works: typeof ad.why_it_works === "string" ? ad.why_it_works : "",
    targeting: normalizeTargeting(ad.targeting),
    adset_schedule: normalizeSchedule(ad.adset_schedule),
  };
}

function extractFirstObjectSlice(text: string): string | null {
  const start = text.indexOf("{");
  if (start === -1) return null;
  let depth = 0;
  let inString = false;
  let escaped = false;
  for (let i = start; i < text.length; i++) {
    const ch = text[i];
    if (escaped) { escaped = false; continue; }
    if (inString) {
      if (ch === "\\") escaped = true;
      else if (ch === '"') inString = false;
      continue;
    }
    if (ch === '"') { inString = true; continue; }
    if (ch === "{") depth++;
    else if (ch === "}") {
      depth--;
      if (depth === 0) return text.slice(start, i + 1);
    }
  }
  return null;
}

function extractFirstArraySlice(text: string): string | null {
  const start = text.indexOf("[");
  if (start === -1) return null;
  let depth = 0;
  let inString = false;
  let escaped = false;
  for (let i = start; i < text.length; i++) {
    const ch = text[i];
    if (escaped) { escaped = false; continue; }
    if (inString) {
      if (ch === "\\") escaped = true;
      else if (ch === '"') inString = false;
      continue;
    }
    if (ch === '"') { inString = true; continue; }
    if (ch === "[") depth++;
    else if (ch === "]") {
      depth--;
      if (depth === 0) return text.slice(start, i + 1);
    }
  }
  return null;
}

function extractAllObjects(text: string): GeneratedAd[] {
  const ads: GeneratedAd[] = [];
  let i = 0;
  while (i < text.length) {
    const start = text.indexOf("{", i);
    if (start === -1) break;
    const slice = extractFirstObjectSlice(text.slice(start));
    if (!slice) { i = start + 1; continue; }
    const absEnd = start + slice.length;
    let raw: unknown;
    try { raw = JSON.parse(slice); } catch {
      try { raw = JSON.parse(tryRepair(slice)); } catch { i = start + 1; continue; }
    }
    if (raw && typeof raw === "object" && !Array.isArray(raw)) {
      const rec = raw as Record<string, unknown>;
      if (coerceString(rec.hook) && coerceString(rec.body) && coerceString(rec.cta)) {
        try { ads.push(buildAd(rec)); } catch { /* skip invalid */ }
      }
    }
    i = absEnd;
  }
  return ads;
}

function normalizeArray(parsed: unknown): GeneratedAd[] {
  const candidates = Array.isArray(parsed) ? parsed : parsed && typeof parsed === "object" ? [parsed] : [];
  if (candidates.length === 0) throw new Error("No ads in model output.");
  const out: GeneratedAd[] = [];
  for (const ad of candidates.slice(0, MAX_AD_COUNT)) {
    if (!ad || typeof ad !== "object" || Array.isArray(ad)) continue;
    const rec = ad as Record<string, unknown>;
    if (!coerceString(rec.hook) || !coerceString(rec.body) || !coerceString(rec.cta)) continue;
    try { out.push(buildAd(rec)); } catch { continue; }
  }
  if (out.length === 0) throw new Error("No ads in model output.");
  return out;
}

export function parseAds(raw: string): GeneratedAd[] {
  const cleaned = stripLeadingNonJson(stripCodeFences(raw.trim()));

  // Try direct JSON parse
  try { return normalizeArray(JSON.parse(cleaned)); } catch { /* continue */ }
  try { return normalizeArray(JSON.parse(tryRepair(cleaned))); } catch { /* continue */ }

  // Try extracting top-level array
  const arraySlice = extractFirstArraySlice(cleaned);
  if (arraySlice) {
    try { return normalizeArray(JSON.parse(arraySlice)); } catch { /* continue */ }
    try { return normalizeArray(JSON.parse(tryRepair(arraySlice))); } catch { /* continue */ }
  }

  // Walk all top-level `{...}` objects (handles NDJSON and `}{` blobs)
  const fromObjects = extractAllObjects(raw);
  if (fromObjects.length >= 1) return fromObjects.slice(0, MAX_AD_COUNT);

  // Try line-by-line NDJSON
  const lines = cleaned.split(/\r?\n/);
  const fromLines: GeneratedAd[] = [];
  for (const line of lines) {
    const t = stripLeadingNonJson(line.trim());
    if (!t) continue;
    let p: unknown;
    try { p = JSON.parse(t); } catch {
      try { p = JSON.parse(tryRepair(t)); } catch { continue; }
    }
    if (p && typeof p === "object" && !Array.isArray(p)) {
      const rec = p as Record<string, unknown>;
      if (coerceString(rec.hook) && coerceString(rec.body) && coerceString(rec.cta)) {
        try { fromLines.push(buildAd(rec)); } catch { /* skip */ }
      }
    }
  }
  if (fromLines.length >= 1) return fromLines.slice(0, MAX_AD_COUNT);

  throw new Error("No valid ads could be parsed from model output.");
}
