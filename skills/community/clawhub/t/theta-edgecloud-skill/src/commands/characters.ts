// Data flow: sends the game-scoped Characters key and character/session/story payloads to
// https://ai-chars-api.thetaedgecloud.com only. Every non-GET route (create/update/delete, session
// create/delete/context/message, Story mode groupings, library messages, story lines, dialogs and
// generation) requires confirm:true here, before any request. Dry-run makes zero write requests.
import { ThetaConfig } from '../config.js';
import { getJson, postJson, putJson, deleteEmpty } from '../clients/http.js';
import { redactObject } from '../redaction.js';
import { pathSegment } from '../security.js';
import { assertApproved, snapshotBody } from '../approval.js';

const HOST = 'https://ai-chars-api.thetaedgecloud.com';

type Validator = (payload: Record<string, unknown>) => void;
type CharacterRoute = {
  method: 'GET' | 'POST' | 'PUT' | 'DELETE';
  path: string;
  fields: string[];
  // Fixed request body for action routes (recreate, generate): caller payloads are not sent.
  fixedBody?: Record<string, unknown>;
  validate?: Validator;
  paginated?: boolean;
  billable?: boolean;
};

function oneOf(path: string, value: unknown, allowed: readonly string[]): void {
  if (value !== undefined && !(typeof value === 'string' && allowed.includes(value))) {
    throw new Error(`${path} must be one of: ${allowed.join(', ')}`);
  }
}

function idString(value: unknown, label: string): void {
  if (typeof value !== 'string' || !value.trim() || value.length > 200 || /[\x00-\x1f\x7f]/.test(value)) {
    throw new Error(`${label} must be a non-empty identifier string`);
  }
}

function idList(value: unknown, label: string, max: number, required: boolean): void {
  if (value === undefined && !required) return;
  if (!Array.isArray(value) || value.length < 1 || value.length > max) throw new Error(`${label} must be an array of 1 to ${max} IDs`);
  value.forEach((entry, i) => idString(entry, `${label}[${i}]`));
}

// Speaking-style values accepted by Theta's dashboard (in-app API reference, 2026-11).
const validateCharacter: Validator = (p) => {
  const style = p.speaking_style;
  if (style === undefined) return;
  if (!style || typeof style !== 'object' || Array.isArray(style)) throw new Error('speaking_style must be an object');
  const s = style as Record<string, unknown>;
  oneOf('speaking_style.formality', s.formality, ['casual', 'formal', 'neutral']);
  oneOf('speaking_style.gesture_frequency', s.gesture_frequency, ['low', 'medium', 'high']);
  oneOf('speaking_style.verbosity', s.verbosity, ['concise', 'normal', 'verbose']);
};

const MESSAGE_TYPES = ['chat', 'action', 'event', 'add_participant', 'remove_participant'] as const;
const validateSessionMessage: Validator = (p) => {
  if (!MESSAGE_TYPES.includes(p.type as typeof MESSAGE_TYPES[number])) throw new Error(`type must be one of: ${MESSAGE_TYPES.join(', ')}`);
  if (p.type === 'chat' || p.type === 'action') {
    idString(p.from_id, 'from_id');
    if (typeof p.content !== 'string' || !p.content.trim()) throw new Error('content must be a non-empty string');
  }
  if (p.type === 'event' && (typeof p.content !== 'string' || !p.content.trim())) throw new Error('content must be a non-empty string');
  if (p.type === 'add_participant' || p.type === 'remove_participant') {
    oneOf('participant_type', p.participant_type, ['npc', 'user']);
    if (p.participant_type === undefined) throw new Error('participant_type is required');
    idString(p.participant_id, 'participant_id');
  }
};

const validateGrouping: Validator = (p) => {
  if (p.name !== undefined && (typeof p.name !== 'string' || !p.name.trim())) throw new Error('name must be a non-empty string');
  if (p.order_index !== undefined && (!Number.isInteger(p.order_index) || (p.order_index as number) < 0)) throw new Error('order_index must be a non-negative integer');
};

const validateLibraryMessage: Validator = (p) => {
  if (p.content !== undefined && (typeof p.content !== 'string' || !p.content.trim())) throw new Error('content must be a non-empty string');
  if (p.type !== undefined && typeof p.type !== 'string') throw new Error('type must be a string');
};

const MAX_GROUPINGS = 20;
const validateStoryline = (required: boolean): Validator => (p) => {
  if (required) idString(p.npc_id, 'npc_id');
  else if (p.npc_id !== undefined) idString(p.npc_id, 'npc_id');
  idList(p.grouping_ids, 'grouping_ids', MAX_GROUPINGS, required);
};

const validateDialog: Validator = (p) => {
  idString(p.npc_id, 'npc_id');
  const refs = p.message_refs;
  if (!Array.isArray(refs) || refs.length < 1 || refs.length > MAX_GROUPINGS) throw new Error(`message_refs must be an array of 1 to ${MAX_GROUPINGS} references`);
  refs.forEach((ref, i) => {
    if (!ref || typeof ref !== 'object' || Array.isArray(ref)) throw new Error(`message_refs[${i}] must be an object`);
    idString((ref as Record<string, unknown>).grouping_id, `message_refs[${i}].grouping_id`);
    idString((ref as Record<string, unknown>).message_id, `message_refs[${i}].message_id`);
  });
};

// Theta AI Characters: public OpenAPI 1.0.0 (characters, sessions) plus Story mode routes documented in
// Theta's in-dashboard API reference (2026-11). Game create/update/delete/list and key rotation use
// dashboard session headers, not a game key, and are deliberately not implemented.
export const characterRoutes: Record<string, CharacterRoute> = {
  list: { method: 'GET', path: '/game/{gameId}/character/list', fields: ['gameId'] },
  get: { method: 'GET', path: '/game/{gameId}/character/{characterId}', fields: ['gameId', 'characterId'] },
  create: { method: 'POST', path: '/game/{gameId}/character', fields: ['gameId'], validate: validateCharacter },
  update: { method: 'PUT', path: '/game/{gameId}/character/{characterId}', fields: ['gameId', 'characterId'], validate: validateCharacter },
  delete: { method: 'DELETE', path: '/game/{gameId}/character/{characterId}', fields: ['gameId', 'characterId'] },
  'session.create': { method: 'POST', path: '/session', fields: [] },
  'session.get': { method: 'GET', path: '/session/{sessionId}', fields: ['sessionId'] },
  'session.delete': { method: 'DELETE', path: '/session/{sessionId}', fields: ['sessionId'] },
  'session.list': { method: 'GET', path: '/session/{gameId}/list', fields: ['gameId'] },
  'session.context': { method: 'PUT', path: '/session/{sessionId}/context', fields: ['sessionId'] },
  'session.message': { method: 'POST', path: '/session/{sessionId}/message', fields: ['sessionId'], validate: validateSessionMessage, billable: true },
  'session.messages': { method: 'GET', path: '/session/{sessionId}/message/list', fields: ['sessionId'], paginated: true },
  // Story mode: groupings (in-fiction events) hold library messages (authored player outcomes).
  'grouping.create': { method: 'POST', path: '/game/{gameId}/grouping', fields: ['gameId'], validate: validateGrouping },
  'grouping.list': { method: 'GET', path: '/game/{gameId}/grouping/list', fields: ['gameId'] },
  'grouping.get': { method: 'GET', path: '/game/{gameId}/grouping/{groupingId}', fields: ['gameId', 'groupingId'] },
  'grouping.update': { method: 'PUT', path: '/game/{gameId}/grouping/{groupingId}', fields: ['gameId', 'groupingId'], validate: validateGrouping },
  'grouping.delete': { method: 'DELETE', path: '/game/{gameId}/grouping/{groupingId}', fields: ['gameId', 'groupingId'] },
  'library.create': { method: 'POST', path: '/grouping/{groupingId}/message', fields: ['groupingId'], validate: validateLibraryMessage },
  'library.list': { method: 'GET', path: '/grouping/{groupingId}/message/list', fields: ['groupingId'] },
  'library.update': { method: 'PUT', path: '/grouping/{groupingId}/message/{messageId}', fields: ['groupingId', 'messageId'], validate: validateLibraryMessage },
  'library.delete': { method: 'DELETE', path: '/grouping/{groupingId}/message/{messageId}', fields: ['groupingId', 'messageId'] },
  // Story lines: ordered groupings + one NPC. Generation is handled by storylineGenerateAll below.
  'storyline.create': { method: 'POST', path: '/game/{gameId}/storyline', fields: ['gameId'], validate: validateStoryline(true) },
  'storyline.list': { method: 'GET', path: '/game/{gameId}/storyline/list', fields: ['gameId'] },
  'storyline.get': { method: 'GET', path: '/storyline/{storylineId}', fields: ['storylineId'] },
  'storyline.update': { method: 'PUT', path: '/storyline/{storylineId}', fields: ['storylineId'], validate: validateStoryline(false) },
  'storyline.delete': { method: 'DELETE', path: '/storyline/{storylineId}', fields: ['storylineId'] },
  'storyline.queue': { method: 'GET', path: '/storyline/{storylineId}/queue', fields: ['storylineId'] },
  'storyline.dialogs': { method: 'GET', path: '/storyline/{storylineId}/dialog/list', fields: ['storylineId'] },
  // Dialogs: one generated conversation for an explicit path of library messages.
  'dialog.create': { method: 'POST', path: '/game/{gameId}/dialog', fields: ['gameId'], validate: validateDialog, billable: true },
  'dialog.list': { method: 'GET', path: '/game/{gameId}/dialog/list', fields: ['gameId'] },
  'dialog.get': { method: 'GET', path: '/dialog/{dialogId}', fields: ['dialogId'] },
  'dialog.recreate': { method: 'POST', path: '/dialog/{dialogId}/recreate', fields: ['dialogId'], fixedBody: {}, billable: true },
  'dialog.delete': { method: 'DELETE', path: '/dialog/{dialogId}', fields: ['dialogId'] }
};

function buildPath(route: CharacterRoute, args: Record<string, unknown>): string {
  let path = route.path;
  for (const field of route.fields) {
    if (typeof args[field] !== 'string' || !(args[field] as string).trim()) throw new Error(`${field} must be a non-empty string`);
    path = path.replace(`{${field}}`, pathSegment(args[field] as string, field));
  }
  if (route.paginated && (args.page !== undefined || args.number !== undefined)) {
    const page = args.page ?? 1;
    const number = args.number ?? 100;
    if (!Number.isInteger(page) || (page as number) < 1 || (page as number) > 10000) throw new Error('page must be an integer from 1 to 10000');
    if (!Number.isInteger(number) || (number as number) < 1 || (number as number) > 100) throw new Error('number must be an integer from 1 to 100');
    path += `?${new URLSearchParams({ page: String(page), number: String(number) })}`;
  }
  return path;
}

function netOpts(cfg: ThetaConfig, method: string) {
  if (!cfg.charactersApiKey) throw new Error('THETA_CHARACTERS_API_KEY missing; use a game-scoped key, not an on-demand key');
  return {
    headers: { Authorization: `Bearer ${cfg.charactersApiKey}` },
    service: 'theta-characters',
    timeoutMs: cfg.httpTimeoutMs,
    maxRetries: method === 'GET' ? cfg.httpMaxRetries : 0,
    retryBackoffMs: cfg.httpRetryBackoffMs
  };
}

export function characterRequest(cfg: ThetaConfig, name: string, args: Record<string, unknown>) {
  const route = Object.hasOwn(characterRoutes, name) ? characterRoutes[name] : undefined;
  if (!route) throw new Error('Unknown AI Characters operation');
  const path = buildPath(route, args);
  // Take one plain JSON copy of the caller payload before payload validation; only that copy is validated and sent.
  let body: Record<string, unknown> | undefined;
  if (route.method === 'POST' || route.method === 'PUT') {
    if (route.fixedBody) body = { ...route.fixedBody };
    else {
      if (!args.payload || typeof args.payload !== 'object' || Array.isArray(args.payload)) throw new Error('payload must be an object');
      body = snapshotBody(args.payload);
      route.validate?.(body);
    }
  }
  if (cfg.dryRun && route.method !== 'GET') {
    return { dryRun: true, method: route.method, path, billable: route.billable === true, payload: redactObject(body ?? {}) };
  }
  if (route.method !== 'GET') assertApproved(cfg, args.confirm, `theta.characters.${name}`);
  const url = `${HOST}${path}`;
  const opts = netOpts(cfg, route.method);
  if (route.method === 'GET') return getJson(url, opts);
  if (route.method === 'POST') return postJson(url, body, opts);
  if (route.method === 'PUT') return putJson(url, body, opts);
  return deleteEmpty(url, opts);
}

// ---- Story line bulk generation with a code-enforced path cap ----

export const STORYLINE_PATH_CAP = 5000;

// Response envelopes are {status, body:{...}}; field names come from Theta's dashboard reference.
function pick(obj: unknown, keys: string[]): unknown {
  if (!obj || typeof obj !== 'object') return undefined;
  const o = obj as Record<string, unknown>;
  for (const key of keys) if (o[key] !== undefined) return o[key];
  return undefined;
}

function storylineGroupingIds(response: unknown): string[] {
  const body = pick(response, ['body']) ?? response;
  const storyline = pick(body, ['storyline']) ?? body;
  // Every place a grouping_ids list may appear must agree; conflicting copies refuse.
  const copies = [response, body, storyline]
    .filter((c, i, all) => all.indexOf(c) === i)
    .map((c) => pick(c, ['grouping_ids']))
    .filter((v) => v !== undefined);
  if (new Set(copies.map((v) => JSON.stringify(v))).size > 1) {
    throw new Error('Story line response has conflicting grouping_ids; refusing to generate without a path count');
  }
  const ids = pick(storyline, ['grouping_ids']);
  if (!Array.isArray(ids) || ids.length < 1 || ids.length > MAX_GROUPINGS || !ids.every((id) => typeof id === 'string' && id.trim())) {
    throw new Error('Could not read the story line grouping_ids; refusing to generate without a path count');
  }
  return ids as string[];
}

// Supported library-list contract (fail closed on anything else):
// - the response is an object (optionally a {status, body} envelope) or a bare array;
// - the list is a bare array body, or exactly ONE of `messages` / `library_messages` / `items`;
// - `pagination`, when present, is a plain object whose keys are all in PAGINATION_FIELDS;
// - completeness/total fields, wherever present (envelope, body or pagination), must be
//   well-typed and must show a complete first page.
// - envelope and body fields are an exact allowlist: the envelope may hold `body`,
//   `pagination`, the recognised paging fields and plain informational values; the body may hold
//   the one list field, `pagination`, the recognised paging fields and plain identity/info values.
//   Any other field refuses, so unrecognised paging metadata is never silently ignored;
// - `offset`, when present, must be 0 (the first page).
// A list with no pagination metadata at all is treated as the complete list.
const LIST_ALIASES = ['messages', 'library_messages', 'items'];
const TOTAL_FIELDS = ['total_count', 'totalCount', 'total', 'count'];
const MORE_FIELDS = ['has_more', 'hasMore', 'has_next', 'hasNext'];
const NEXT_FIELDS = ['next', 'next_page', 'nextPage', 'next_cursor', 'nextCursor', 'next_page_token', 'nextPageToken'];
const PAGES_FIELDS = ['total_pages', 'totalPages', 'page_count', 'pageCount', 'pages'];
const PAGE_FIELDS = ['page', 'page_number', 'pageNumber', 'current_page', 'currentPage'];
const PAGE_SIZE_FIELDS = ['number', 'per_page', 'perPage', 'page_size', 'pageSize', 'limit', 'size', 'offset'];
const PAGINATION_FIELDS = new Set([...TOTAL_FIELDS, ...MORE_FIELDS, ...NEXT_FIELDS, ...PAGES_FIELDS, ...PAGE_FIELDS, ...PAGE_SIZE_FIELDS]);

// Plain informational / identity fields (status/success/error are separately checked for failure
// by assertNotFailure). Allowed only with
// primitive (string, number, boolean or null) values.
const INFO_FIELDS = new Set([
  'status', 'message', 'code', 'success', 'error', 'request_id', 'requestId',
  'id', 'grouping_id', 'groupingId', 'storyline_id', 'storylineId', 'npc_id', 'npcId', 'name', 'title',
  'created_at', 'createdAt', 'updated_at', 'updatedAt'
]);

function assertOnlyKnownFields(container: Record<string, unknown>, allowed: Set<string>) {
  for (const key of Object.keys(container)) {
    if (allowed.has(key) || PAGINATION_FIELDS.has(key)) continue;
    const value = container[key];
    if (INFO_FIELDS.has(key) && (value === null || typeof value !== 'object')) continue;
    refuseCount(`response has an unrecognised field (${key.slice(0, 40)})`);
  }
}

// A container reports failure when `success` is present and not exactly true, `status` is an
// error word or an HTTP-style code of 400 or more, or `error` holds anything other than
// null/false/empty string.
function assertNotFailure(container: Record<string, unknown>) {
  const success = own(container, 'success');
  const status = own(container, 'status');
  const error = own(container, 'error');
  const statusText = typeof status === 'string' ? status.trim() : '';
  const statusCode = typeof status === 'number' ? status : /^\d{3}$/.test(statusText) ? Number(statusText) : undefined;
  if (
    (success !== undefined && success !== true) ||
    /^(err|error|errors|fail|failed|failure)$/i.test(statusText) ||
    (statusCode !== undefined && statusCode >= 400) ||
    (error !== undefined && error !== null && error !== false && error !== '')
  ) {
    refuseCount('list response reports a failure');
  }
}

function isPlainObject(value: unknown): value is Record<string, unknown> {
  return !!value && typeof value === 'object' && !Array.isArray(value);
}

function refuseCount(reason: string): never {
  throw new Error(`Library message ${reason}; refusing to generate without a reliable path count`);
}

function own(obj: Record<string, unknown>, key: string): unknown {
  return Object.prototype.hasOwnProperty.call(obj, key) ? obj[key] : undefined;
}

function libraryMessageCount(response: unknown): number {
  if (!isPlainObject(response) && !Array.isArray(response)) refuseCount('list response is malformed');
  const containers: Array<Record<string, unknown>> = [];
  let body: unknown = response;
  if (isPlainObject(response) && Object.prototype.hasOwnProperty.call(response, 'body')) {
    body = response.body;
    if (!isPlainObject(body) && !Array.isArray(body)) refuseCount('list response body is malformed');
    assertOnlyKnownFields(response, new Set(['body', 'pagination']));
    containers.push(response); // envelope-level totals/completeness fields are checked too
  }
  let list: unknown[];
  if (Array.isArray(body)) list = body;
  else {
    const b = body as Record<string, unknown>;
    containers.push(b);
    const present = LIST_ALIASES.filter((key) => own(b, key) !== undefined);
    if (present.length === 0) refuseCount('list is missing');
    if (present.length > 1) refuseCount(`response has conflicting list fields (${present.join(', ')})`);
    const value = b[present[0]];
    if (!Array.isArray(value)) refuseCount('list is malformed');
    assertOnlyKnownFields(b, new Set([present[0], 'pagination']));
    list = value;
  }
  // Failure flags refuse wherever they appear: on the envelope or on the body.
  for (const c of containers) assertNotFailure(c);
  // Any present `pagination` container must be a plain object with only supported fields.
  for (const container of [...containers]) {
    const pagination = own(container, 'pagination');
    if (pagination === undefined) continue;
    if (!isPlainObject(pagination)) refuseCount('pagination metadata is malformed');
    for (const key of Object.keys(pagination)) {
      if (!PAGINATION_FIELDS.has(key)) refuseCount(`pagination metadata has an unsupported field (${key.slice(0, 40)})`);
    }
    containers.push(pagination);
  }
  const totals: number[] = [];
  const pageSizes: number[] = [];
  let reportedComplete = false;
  const safeInt = (value: unknown) => typeof value === 'number' && Number.isSafeInteger(value) && value >= 0;
  for (const container of containers) {
    for (const key of TOTAL_FIELDS) {
      const value = own(container, key);
      if (value === undefined) continue;
      if (!safeInt(value)) refuseCount('pagination total is malformed');
      totals.push(value as number);
    }
    for (const key of MORE_FIELDS) {
      const value = own(container, key);
      if (value === undefined) continue;
      if (typeof value !== 'boolean') refuseCount('pagination completeness flag is malformed');
      if (value) refuseCount('list page is incomplete (more pages reported)');
    }
    for (const key of NEXT_FIELDS) {
      const value = own(container, key);
      if (value === undefined || value === null || value === '' || value === false) continue;
      refuseCount('list page is incomplete (a next page is reported)');
    }
    for (const key of PAGES_FIELDS) {
      const value = own(container, key);
      if (value === undefined) continue;
      if (!safeInt(value)) refuseCount('pagination page count is malformed');
      if ((value as number) > 1) refuseCount('list page is incomplete (more than one page reported)');
    }
    for (const key of PAGE_FIELDS) {
      const value = own(container, key);
      if (value === undefined) continue;
      if (!safeInt(value) || (value as number) > 1) refuseCount('pagination page is malformed or not the first page');
    }
    for (const key of PAGE_SIZE_FIELDS) {
      const value = own(container, key);
      if (value === undefined) continue;
      if (!safeInt(value)) refuseCount('pagination page size or offset is malformed');
      if (key === 'offset' && value !== 0) refuseCount('list page is not the first page (offset is not 0)');
      if (key !== 'offset') pageSizes.push(value as number);
    }
    for (const key of MORE_FIELDS) if (own(container, key) === false) reportedComplete = true;
  }
  if (totals.length > 1 && new Set(totals).size > 1) refuseCount('pagination totals conflict');
  const total = totals[0];
  // A full page (as many items as the reported page size) may have more pages behind it; accept
  // it only when a total or an explicit has_more:false says the list is complete.
  if (total === undefined && !reportedComplete && pageSizes.some((size) => list.length >= size)) {
    refuseCount('list page is full and may be incomplete (no total or has_more:false reported)');
  }
  if (total !== undefined && total < list.length) refuseCount('pagination total is smaller than the returned page');
  // When the service reports a larger total than the page returned, use the larger number (fail toward refusing).
  return total !== undefined ? Math.max(total, list.length) : list.length;
}

export async function storylineGenerateAll(cfg: ThetaConfig, args: Record<string, unknown>) {
  const storylineId = pathSegment(String(args.storylineId ?? ''), 'storylineId');
  const maxPaths = args.maxPaths;
  if (!Number.isInteger(maxPaths) || (maxPaths as number) < 1 || (maxPaths as number) > STORYLINE_PATH_CAP) {
    throw new Error(`maxPaths must be an integer from 1 to ${STORYLINE_PATH_CAP}: the most dialog paths you approve generating`);
  }
  // Refuse unapproved live generation before any request, including the counting reads.
  if (!cfg.dryRun) assertApproved(cfg, args.confirm, 'theta.characters.storyline.generateAll');
  if (cfg.dryRun && !cfg.charactersApiKey) {
    return { dryRun: true, requiresKeyForPathCount: true, method: 'POST', path: `/storyline/${storylineId}/generate_all`, maxPaths };
  }
  const read = netOpts(cfg, 'GET');
  const storyline = await getJson(`${HOST}/storyline/${storylineId}`, read);
  const groupingIds = storylineGroupingIds(storyline);
  const perGrouping: Array<{ grouping_id: string; library_messages: number }> = [];
  let pathCount = 1;
  const effectiveLimit = Math.min(maxPaths as number, STORYLINE_PATH_CAP);
  for (const groupingId of groupingIds) {
    const count = libraryMessageCount(await getJson(`${HOST}/grouping/${pathSegment(groupingId, 'grouping_id')}/message/list`, read));
    if (count < 1) throw new Error(`A grouping has no library messages, so there is nothing to generate: ${JSON.stringify(perGrouping)}`);
    perGrouping.push({ grouping_id: groupingId, library_messages: count });
    // Overflow-safe incremental cap: compare via division so the running product never exceeds
    // the effective limit, and stop reading as soon as refusal is proven.
    if (pathCount > Math.floor(effectiveLimit / count)) {
      throw new Error(`This story line exceeds ${effectiveLimit === STORYLINE_PATH_CAP ? `Theta's ${STORYLINE_PATH_CAP}-path cap` : `the approved maxPaths ${maxPaths}`} paths; nothing was generated. Counted so far: ${JSON.stringify(perGrouping)}`);
    }
    pathCount *= count;
  }
  const summary = { storylineId: args.storylineId, groupings: perGrouping, pathCount, maxPaths, serviceCap: STORYLINE_PATH_CAP };
  // Final invariant: the product stayed a finite safe integer at or below the approved limit.
  if (!Number.isSafeInteger(pathCount) || pathCount < 1 || pathCount > effectiveLimit) {
    throw new Error(`Path count failed the final safety check (${pathCount}); refusing to generate`);
  }
  if (cfg.dryRun) return { dryRun: true, method: 'POST', path: `/storyline/${storylineId}/generate_all`, billable: true, ...summary };
  // Theta skips already-generated paths (idempotent). The preflight count is a snapshot: messages
  // added between the reads and this single POST are not covered. Never retried.
  const result = await postJson(`${HOST}/storyline/${storylineId}/generate_all`, {}, netOpts(cfg, 'POST'));
  return { ...summary, result };
}

// ---- Cost estimate: pure arithmetic, no network ----

// Theta's published AI Characters prices (blog and product page, 2026-11-11), USD per 1M tokens.
export const CHARACTERS_PUBLISHED_PRICES = Object.freeze({ inputPer1M: 7.5, outputPer1M: 20, embeddingPer1M: 0.2, source: 'published-2026-11-11' });

export function estimateCharactersCost(args: Record<string, unknown>) {
  const tokens = (label: string): number => {
    const v = args[label];
    if (v === undefined) return 0;
    if (typeof v !== 'number' || !Number.isFinite(v) || v < 0 || v > 1e12) throw new Error(`${label} must be a number from 0 to 1e12`);
    return v;
  };
  const input = tokens('inputTokens');
  const output = tokens('outputTokens');
  const embedding = tokens('embeddingTokens');
  const p = CHARACTERS_PUBLISHED_PRICES;
  const round = (n: number) => Math.round(n * 1e6) / 1e6;
  const breakdown = {
    inputUsd: round((input / 1e6) * p.inputPer1M),
    outputUsd: round((output / 1e6) * p.outputPer1M),
    embeddingUsd: round((embedding / 1e6) * p.embeddingPer1M)
  };
  return {
    estimateUsd: round(breakdown.inputUsd + breakdown.outputUsd + breakdown.embeddingUsd),
    breakdown,
    usage: { inputTokens: input, outputTokens: output, embeddingTokens: embedding },
    prices: p,
    note: 'Estimate only, from Theta published prices; actual charges depend on usage. Verify current prices with theta.billing.pricing and spend with theta.billing.usage.'
  };
}
