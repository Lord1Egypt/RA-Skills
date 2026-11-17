#!/usr/bin/env node
// Read-only, bounded event -> historical affect recall. No inferred joins.
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { httpJson, textOf } from './notionctl_bridge.js';

const UUID = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;
const key = value => String(value || '').replaceAll('-', '').toLowerCase();
function id(value, name) {
  if (!UUID.test(value || '')) throw new Error(`Invalid or missing ${name}: expected a UUID`);
  return value.toLowerCase();
}
function bounded(value, fallback, max, name) {
  const n = value ?? fallback;
  if (!Number.isInteger(n) || n < 1 || n > max) throw new Error(`${name} must be an integer from 1 to ${max}`);
  return n;
}

export async function recallExperiences(options, { request = httpJson } = {}) {
  const cfg = {
    events: id(options.eventsDsid, '--events-dsid'),
    emotions: id(options.emotionsDsid, '--emotions-dsid'),
    state: id(options.stateDsid, '--state-dsid'),
  };
  const limit = bounded(options.limit, 3, 5, '--limit');
  const linkedLimit = bounded(options.linkedLimit, 5, 10, '--linked-limit');
  const maxRequests = bounded(options.maxRequests, 32, 64, '--max-requests');
  const textLimit = bounded(options.textLimit, 2000, 4000, '--text-limit');
  const totalTextLimit = bounded(options.totalTextLimit, 24000, 48000, '--total-text-limit');
  let textRemaining = totalTextLimit;
  if ([options.query, options.eventId, options.stateId].filter(Boolean).length !== 1) {
    throw new Error('Use exactly one of --query, --event-id, --state-id');
  }
  if (options.query && (!options.query.trim() || options.query.length > 400)) throw new Error('Query must contain 1-400 characters');
  if (options.eventId) id(options.eventId, '--event-id');
  if (options.stateId) id(options.stateId, '--state-id');
  let calls = 0;
  const diagnostics = [];
  const schemas = {};
  const cache = new Map();
  const note = (code, lane, pageId, property) => diagnostics.push({ code, lane, ...(pageId ? { page_id: pageId } : {}), ...(property ? { property } : {}) });
  async function call(method, apiPath, body, lane) {
    if (calls >= maxRequests) { note('request_budget_exhausted', lane); return null; }
    calls++;
    try {
      const result = await request(method, apiPath, body);
      if (!result || typeof result !== 'object' || result.object === 'error') throw new Error('Invalid API response');
      return result;
    } catch {
      // The bridge error may contain request bodies/private text. Do not echo it.
      note('request_failed', lane);
      return null;
    }
  }
  const matchesParent = (page, lane) => key(page?.parent?.data_source_id) === key(cfg[lane]);
  async function page(pageId, lane) {
    if (!UUID.test(pageId || '')) { note('invalid_relation_id', lane); return null; }
    const cacheKey = lane + ':' + key(pageId);
    if (cache.has(cacheKey)) return cache.get(cacheKey);
    const result = await call('GET', `/pages/${pageId}`, undefined, lane);
    let valid = result;
    if (result && (key(result.id) !== key(pageId) || !matchesParent(result, lane) || result.archived || result.in_trash)) {
      note('source_unavailable_or_wrong_parent', lane, pageId); valid = null;
    }
    cache.set(cacheKey, valid);
    return valid;
  }
  async function query(lane, body) {
    const res = await call('POST', `/data_sources/${cfg[lane]}/query`, body, lane);
    if (!res) return [];
    if (!Array.isArray(res.results)) { note('invalid_query_response', lane); return []; }
    if (res.has_more || res.results.length > body.page_size) note('result_limit', lane);
    return res.results.slice(0, body.page_size).filter(p => {
      if (!UUID.test(p?.id || '') || !matchesParent(p, lane) || p.archived || p.in_trash) {
        note('source_unavailable_or_wrong_parent', lane, p?.id); return false;
      }
      cache.set(lane + ':' + key(p.id), p);
      return true;
    });
  }
  function relationSupported(lane, property, target) {
    const prop = schemas[lane]?.properties?.[property];
    if (!prop) { note('missing_relation_schema', lane, null, property); return false; }
    if (prop.type !== 'relation' || key(prop.relation?.data_source_id) !== key(cfg[target])) {
      note('incompatible_relation_schema', lane, null, property); return false;
    }
    return true;
  }
  function refs(p, property, lane, cap) {
    const prop = p.properties?.[property];
    if (prop?.type !== 'relation' || !Array.isArray(prop.relation)) {
      note('missing_relation_value', lane, p.id, property); return [];
    }
    if (prop.has_more || prop.relation.length > cap) note('relation_limit', lane, p.id, property);
    return [...new Set(prop.relation.map(r => r.id))].slice(0, cap);
  }
  function normalize(p, lane, fields) {
    const out = { id: p.id, url: p.url || null, data_source_id: cfg[lane], created_time: p.created_time || null,
      last_edited_time: p.last_edited_time || null, fields: {}, missing_fields: [], truncated_fields: [] };
    for (const [name, type] of Object.entries(fields)) {
      const prop = p.properties?.[name];
      if (lane === 'emotions' && name === 'scale_version' && (!prop || prop.number === null)) {
        out.fields[name] = 1; // Legacy records are retained in their original coordinates.
        continue;
      }
      if (prop?.type !== type) {
        out.fields[name] = null; out.missing_fields.push(name); note('missing_or_incompatible_field', lane, p.id, name); continue;
      }
      let value = textOf(prop);
      const takeText = text => {
        const cap = Math.min(textLimit, textRemaining);
        if (text.length > cap) {
          if (!out.truncated_fields.includes(name)) { out.truncated_fields.push(name); note('text_limit', lane, p.id, name); }
        }
        const result = text.slice(0, cap); textRemaining -= result.length; return result;
      };
      if (typeof value === 'string') value = takeText(value);
      if (Array.isArray(value)) {
        if (value.length > 20 || value.some(v => String(v).length > textLimit)) {
          out.truncated_fields.push(name); note('text_limit', lane, p.id, name);
        }
        value = value.slice(0, 20).map(v => takeText(String(v)));
      }
      out.fields[name] = value;
      const required = lane === 'emotions' ? ['axis','level'] : lane === 'events' ? ['Name','context','when'] : ['when','mood_label','state_json'];
      if (required.includes(name) && (value === null || value === '')) note('empty_recorded_value', lane, p.id, name);
    }
    return out;
  }
  for (const lane of ['events', 'emotions', 'state']) {
    schemas[lane] = await call('GET', `/data_sources/${cfg[lane]}`, undefined, lane);
    if (schemas[lane] && (key(schemas[lane].id) !== key(cfg[lane]) || !schemas[lane].properties)) {
      note('invalid_schema_response', lane); schemas[lane] = null;
    }
  }
  let events = [];
  let origin = null;
  if (schemas.events) {
    if (options.eventId) {
      const p = await page(options.eventId, 'events');
      if (p) events = [p];
    } else if (options.stateId) {
      const p = await page(options.stateId, 'state');
      if (p) origin = { kind: 'notion_state', id: p.id, url: p.url || null };
      if (p && relationSupported('state', 'event', 'events')) {
        const eventIds = refs(p, 'event', 'state', limit);
        if (!eventIds.length) note('missing_event_link', 'state', p.id);
        for (const eventId of eventIds) {
          const e = await page(eventId, 'events');
          if (e) events.push(e);
        }
      }
    } else {
      const filters = [];
      for (const [property, type] of [['Name', 'title'], ['context', 'rich_text']]) {
        if (schemas.events.properties[property]?.type === type) filters.push({ property, [type]: { contains: options.query.trim() } });
        else note('missing_search_field', 'events', null, property);
      }
      if (filters.length) events = await query('events', { page_size: limit, filter: filters.length === 1 ? filters[0] : { or: filters },
        sorts: [{ timestamp: 'created_time', direction: 'descending' }] });
    }
  }
  const results = [];
  const acquisitionDiagnostics = diagnostics.slice();
  for (const event of events) {
    const start = diagnostics.length;
    const experience = normalize(event, 'events', EVENT_FIELDS);
    const linked = {};
    for (const lane of ['emotions', 'state']) {
      const found = new Map();
      const back = relationSupported(lane, 'event', 'events');
      if (back) {
        const rows = await query(lane, { page_size: linkedLimit, filter: { property: 'event', relation: { contains: event.id } },
          sorts: [{ timestamp: 'created_time', direction: 'descending' }] });
        for (const row of rows) {
          const evidence = refs(row, 'event', lane, 25);
          if (!evidence.some(r => key(r) === key(event.id))) {
            // A matching query may refer to an inline-truncated relation; do not
            // silently claim that the edge was independently read.
            note('unverified_reverse_relation', lane, row.id, 'event'); continue;
          }
          found.set(key(row.id), { page: row, via: ['reverse:event'] });
        }
      }
      if (relationSupported('events', lane, lane)) {
        for (const linkedId of refs(event, lane, 'events', linkedLimit)) {
          const existing = found.get(key(linkedId));
          if (existing) { existing.via.push(`forward:${lane}`); continue; }
          if (found.size >= linkedLimit) { note('result_limit', lane, event.id); break; }
          const p = await page(linkedId, lane);
          if (!p) continue;
          const reverse = p.properties?.event;
          if (reverse?.type === 'relation' && reverse.relation?.length && !reverse.relation.some(r => key(r.id) === key(event.id))) {
            note('conflicting_relation', lane, p.id, 'event');
            // Preserve the observed forward edge but label its inconsistency.
          }
          found.set(key(p.id), { page: p, via: [`forward:${lane}`] });
        }
      }
      if (!found.size) note('no_linked_records', lane, event.id);
      linked[lane] = [...found.values()].map(({page: p, via}) => ({ ...normalize(p, lane, lane === 'emotions' ? EMOTION_FIELDS : STATE_FIELDS),
        relation_evidence: { event_id: event.id, via } }));
    }
    results.push({ experience, temporal_scope: 'recorded_at_experience_not_current', emotions: linked.emotions, states: linked.state,
      complete: acquisitionDiagnostics.length === 0 && diagnostics.length === start,
      diagnostics: [...acquisitionDiagnostics, ...diagnostics.slice(start)] });
  }
  const failed = diagnostics.some(d => ['request_failed', 'request_budget_exhausted', 'invalid_query_response', 'invalid_schema_response'].includes(d.code));
  return { ok: !failed, status: failed && !results.length ? 'error' : diagnostics.length ? 'partial' : results.length ? 'complete' : 'no_match',
    complete: diagnostics.length === 0, retrieved_at: new Date().toISOString(), origin, query: options.query || null, results, diagnostics,
    budget: { requests: calls, max_requests: maxRequests, event_limit: limit, linked_limit: linkedLimit, text_limit: textLimit,
      total_text_limit: totalTextLimit, text_characters: totalTextLimit - textRemaining },
    mem_join: 'not_inferred', consumption: 'not_acknowledged' };
}

const EVENT_FIELDS = { Name:'title', context:'rich_text', when:'date', source:'select', link:'url', trigger:'select', importance:'select', uncertainty:'number', control:'number' };
const EMOTION_FIELDS = { Name:'title', axis:'select', level:'number', scale_version:'number', comment:'rich_text', weight:'number', body_signal:'multi_select', need:'select', coping:'select' };
const STATE_FIELDS = { Name:'title', when:'date', mood_label:'select', intent:'select', need_stack:'select', need_level:'number', avoid:'multi_select', reason:'rich_text', state_json:'rich_text', source:'select' };

export function parseRecallArgs(argv) {
  const names = { '--query':'query', '--event-id':'eventId', '--state-id':'stateId', '--events-dsid':'eventsDsid', '--emotions-dsid':'emotionsDsid',
    '--state-dsid':'stateDsid', '--limit':'limit', '--linked-limit':'linkedLimit', '--max-requests':'maxRequests', '--text-limit':'textLimit', '--total-text-limit':'totalTextLimit' };
  const numeric = new Set(['limit','linkedLimit','maxRequests','textLimit','totalTextLimit']);
  const out = {};
  for (let i = 0; i < argv.length; i++) {
    if (argv[i] === '--help') { out.help = true; continue; }
    const name = names[argv[i]];
    if (!name || !argv[i + 1] || argv[i + 1].startsWith('--') || name in out) throw new Error('Unknown, repeated or incomplete argument');
    out[name] = numeric.has(name) ? Number(argv[++i]) : argv[++i];
  }
  return out;
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  try {
    const options = parseRecallArgs(process.argv.slice(2));
    if (options.help) console.log('experience_recall.js (--query <text> | --event-id <uuid> | --state-id <uuid>) --events-dsid <uuid> --emotions-dsid <uuid> --state-dsid <uuid> [--limit 3 --linked-limit 5 --max-requests 32 --text-limit 2000 --total-text-limit 24000]');
    else {
      const result = await recallExperiences(options);
      console.log(JSON.stringify(result, null, 2));
      if (!result.ok) process.exitCode = 1;
    }
  } catch (err) {
    console.error(JSON.stringify({ok:false,status:'error',error:err.message})); process.exitCode = 1;
  }
}
