#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const {
  insertWineEntry,
  listWineEntries,
  queryWineEntries,
  recallWineEntries,
  DB_PATH,
  openDb,
  summarizeWine,
  deleteWineEntry,
} = require('../lib/wine-store');
const { extractFromText, parseLabelText } = require('../lib/wine-extractor');

function parseArgs(argv) {
  const args = { _: [] };
  for (let i = 0; i < argv.length; i += 1) {
    const token = argv[i];
    if (token.startsWith('--')) {
      const key = token.slice(2);
      const next = argv[i + 1];
      if (!next || next.startsWith('--')) {
        args[key] = true;
      } else {
        args[key] = next;
        i += 1;
      }
    } else {
      args._.push(token);
    }
  }
  return args;
}

function print(obj) {
  process.stdout.write(`${JSON.stringify(obj, null, 2)}\n`);
}

function today() {
  return new Date().toISOString().slice(0, 10);
}

function shiftDate(baseIso, days) {
  const date = new Date(`${baseIso}T12:00:00Z`);
  date.setUTCDate(date.getUTCDate() + days);
  return date.toISOString().slice(0, 10);
}

function monthWindow(baseIso, deltaMonths = 0) {
  const date = new Date(`${baseIso}T12:00:00Z`);
  date.setUTCMonth(date.getUTCMonth() + deltaMonths, 1);
  const start = date.toISOString().slice(0, 10);
  const next = new Date(`${start}T12:00:00Z`);
  next.setUTCMonth(next.getUTCMonth() + 1, 1);
  next.setUTCDate(next.getUTCDate() - 1);
  return { start, end: next.toISOString().slice(0, 10) };
}

function parseNaturalDateQuery(text) {
  const raw = (text || '').trim();
  const lower = raw.toLowerCase();
  const criteria = {};
  const now = today();

  if (/\b(last week)\b/.test(lower)) {
    criteria.consumed_after = shiftDate(now, -7);
    criteria.consumed_before = now;
  }
  if (/\b(this week)\b/.test(lower)) {
    criteria.consumed_after = shiftDate(now, -6);
    criteria.consumed_before = now;
  }
  if (/\b(yesterday)\b/.test(lower)) {
    const day = shiftDate(now, -1);
    criteria.consumed_after = day;
    criteria.consumed_before = day;
  }
  if (/\b(today)\b/.test(lower)) {
    criteria.consumed_after = now;
    criteria.consumed_before = now;
  }
  if (/\b(last month)\b/.test(lower)) {
    const window = monthWindow(now, -1);
    criteria.consumed_after = window.start;
    criteria.consumed_before = window.end;
  }
  if (/\b(this month)\b/.test(lower)) {
    const window = monthWindow(now, 0);
    criteria.consumed_after = window.start;
    criteria.consumed_before = window.end;
  }

  const afterMatch = raw.match(/\bafter\s+(\d{4}-\d{2}-\d{2})\b/i);
  const beforeMatch = raw.match(/\bbefore\s+(\d{4}-\d{2}-\d{2})\b/i);
  if (afterMatch) criteria.consumed_after = afterMatch[1];
  if (beforeMatch) criteria.consumed_before = beforeMatch[1];

  const ratingMatch = raw.match(/\b(?:rated|rating)\s*(?:at least|>=|above)?\s*(\d(?:\.\d+)?)\b/i);
  if (ratingMatch) criteria.min_subjective_rating = Number(ratingMatch[1]);

  const matchedTerms = [];
  const fieldPatterns = {
    varietal: /\b(pinot noir|cabernet sauvignon|merlot|syrah|shiraz|zinfandel|tempranillo|grenache|garnacha|malbec|sauvignon blanc|chardonnay|riesling|chenin blanc|albariño|albarino|loureiro|arinto|trajadura)\b/i,
    style: /\b(vino verde|sparkling|dessert|fortified|still)\b/i,
    color: /\b(red|white|rose|rosé|orange)\b/i,
    region: /\b(minho|douro|rioja|burgundy|bourgogne|napa valley|sonoma coast|willamette valley|marlborough|mosel|tuscany|piemonte|barossa valley)\b/i,
    place_of_purchase: /\b(nugget|costco|trader joe'?s|bevmo|total wine|whole foods)\b/i,
  };

  for (const [field, pattern] of Object.entries(fieldPatterns)) {
    const m = raw.match(pattern);
    if (m) {
      criteria[field] = m[1];
      matchedTerms.push(m[1].toLowerCase());
    }
  }

  let sanitizedText = lower
    .replace(/\b(show|find|recall|what|which|wines|wine|did|do|i|have|had|drank|drink|bought|buy|from|that|were|was|the|a|an|me|my|entries|at)\b/g, ' ')
    .replace(/\b(last week|this week|yesterday|today|last month|this month)\b/g, ' ')
    .replace(/\bafter\s+\d{4}-\d{2}-\d{2}\b/gi, ' ')
    .replace(/\bbefore\s+\d{4}-\d{2}-\d{2}\b/gi, ' ')
    .replace(/\b(rated|rating)\s*(?:at least|>=|above)?\s*\d(?:\.\d+)?\b/gi, ' ');

  for (const term of matchedTerms) {
    const escaped = term.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    sanitizedText = sanitizedText.replace(new RegExp(`\\b${escaped}\\b`, 'gi'), ' ');
  }

  sanitizedText = sanitizedText.replace(/\s+/g, ' ').trim();

  if (sanitizedText) criteria.text = sanitizedText;
  return criteria;
}

function init() {
  openDb().close();
  print({ status: 'ok', db: DB_PATH, note: 'init only creates the DB if missing; it does not reset entries.' });
}

function add(args) {
  let entry = {};

  if (args.text) {
    entry = extractFromText(args.text);
  }

  if (args['label-text']) {
    entry = { ...entry, ...parseLabelText(args['label-text']) };
  }

  if (args.json) {
    entry = { ...entry, ...JSON.parse(fs.readFileSync(path.resolve(args.json), 'utf8')) };
  }

  if (!args.purchased_on && !args.consumed_on && /\blast week\b/i.test(args.text || '')) {
    entry.consumed_on = shiftDate(today(), -7);
  }
  if (!args.purchased_on && !args.consumed_on && /\byesterday\b/i.test(args.text || '')) {
    entry.consumed_on = shiftDate(today(), -1);
  }
  if (!args.purchased_on && !args.consumed_on && /\btoday\b/i.test(args.text || '')) {
    entry.consumed_on = today();
  }

  for (const field of ['wine_name', 'producer', 'varietal', 'region', 'country', 'style', 'color', 'vintage', 'currency', 'place_of_purchase', 'purchased_on', 'consumed_on', 'official_rating_source', 'notes']) {
    if (args[field]) entry[field] = args[field];
  }
  for (const field of ['price', 'subjective_rating', 'official_rating']) {
    if (args[field] != null) entry[field] = Number(args[field]);
  }
  if (args.image) {
    entry.source_image_path = path.resolve(args.image);
    entry.source_type = entry.source_type || 'image';
  }
  if (args.text) {
    entry.source_text = args.text;
    entry.source_type = entry.source_type || 'chat';
  }
  if (!entry.source_type) entry.source_type = 'manual';

  const created = insertWineEntry(entry);
  print({ status: 'ok', entry: created, summary: summarizeWine(created) });
}

function list(args) {
  const limit = Number(args.limit || 25);
  const entries = listWineEntries(limit);
  print({
    status: 'ok',
    entries,
    summary: entries.map((entry) => ({ id: entry.id, summary: summarizeWine(entry) })),
  });
}

function query(args) {
  const criteria = {
    text: args.text,
    wine_name: args.wine_name,
    producer: args.producer,
    varietal: args.varietal,
    region: args.region,
    country: args.country,
    style: args.style,
    color: args.color,
    place_of_purchase: args.place_of_purchase,
    purchased_after: args.purchased_after,
    purchased_before: args.purchased_before,
    consumed_after: args.consumed_after,
    consumed_before: args.consumed_before,
    min_subjective_rating: args.min_subjective_rating,
    limit: args.limit,
  };
  print({ status: 'ok', entries: queryWineEntries(criteria) });
}

function recall(args) {
  const criteria = args.text ? parseNaturalDateQuery(args.text) : {};
  if (args.limit) criteria.limit = args.limit;
  const result = recallWineEntries(criteria);
  print({ status: 'ok', ...result });
}

function parseLabel(args) {
  let text = args['label-text'] || '';
  if (!text && args.file) {
    text = fs.readFileSync(path.resolve(args.file), 'utf8');
  }
  const parsed = parseLabelText(text);
  print({ status: 'ok', parsed });
}

function remove(args) {
  if (!args.id) {
    print({ status: 'error', message: 'remove requires --id' });
    process.exitCode = 1;
    return;
  }
  const removed = deleteWineEntry(Number(args.id));
  if (!removed) {
    print({ status: 'error', message: `entry not found: ${args.id}` });
    process.exitCode = 1;
    return;
  }
  print({ status: 'ok', removed });
}

function main() {
  const [command, ...rest] = process.argv.slice(2);
  const args = parseArgs(rest);

  if (command === 'init') return init();
  if (command === 'add') return add(args);
  if (command === 'list') return list(args);
  if (command === 'query') return query(args);
  if (command === 'recall') return recall(args);
  if (command === 'parse-label') return parseLabel(args);
  if (command === 'remove') return remove(args);

  print({
    status: 'error',
    message: 'usage: wine-service.js <init|add|list|query|recall|parse-label|remove> [--flags]',
  });
  process.exitCode = 1;
}

main();
