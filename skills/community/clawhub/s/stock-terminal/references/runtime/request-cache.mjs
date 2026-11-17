// Deterministic request-window defaults and cache planning for stock-terminal hosts.

export const FIVE_MINUTES_MS = 5 * 60 * 1000;
export const UTC_DAY_MS = 24 * 60 * 60 * 1000;
export const DEFAULT_CACHE_TTL_MS = FIVE_MINUTES_MS;

const finiteEpoch = (value, label) => {
  if (!Number.isSafeInteger(value) || value < 0) throw new TypeError(`${label} must be a non-negative safe-integer epoch millisecond value`);
  return value;
};

export function defaultRelativeWindow(nowMs = Date.now()) {
  const now = finiteEpoch(nowMs, 'nowMs');
  const utcDayStart = Math.floor(now / UTC_DAY_MS) * UTC_DAY_MS;
  return {
    epochMs30dAgo: utcDayStart - (30 * UTC_DAY_MS),
    epochMsNow: Math.floor(now / FIVE_MINUTES_MS) * FIVE_MINUTES_MS,
  };
}

export function fillRelativeWindowDefaults(recipe, suppliedInputs = {}, nowMs = Date.now()) {
  if (!recipe || !Array.isArray(recipe.requiredInputs)) throw new TypeError('recipe with requiredInputs is required');
  const result = { ...suppliedInputs };
  const defaults = defaultRelativeWindow(nowMs);
  for (const name of ['epochMs30dAgo', 'epochMsNow']) {
    if (recipe.requiredInputs.includes(name) && !Object.hasOwn(result, name)) result[name] = defaults[name];
    if (Object.hasOwn(result, name)) finiteEpoch(result[name], name);
  }
  if (Object.hasOwn(result, 'epochMs30dAgo') && Object.hasOwn(result, 'epochMsNow') && result.epochMs30dAgo > result.epochMsNow) {
    throw new RangeError('epochMs30dAgo must not be later than epochMsNow');
  }
  return result;
}

/** A reusable cache wrapper has shape { status: 'success', fetchedAtMs, snapshot }. */
export function cacheEntryIsFresh(entry, nowMs = Date.now(), ttlMs = DEFAULT_CACHE_TTL_MS) {
  const now = finiteEpoch(nowMs, 'nowMs');
  if (!Number.isFinite(ttlMs) || ttlMs < 0 || ttlMs > DEFAULT_CACHE_TTL_MS) {
    throw new TypeError(`ttlMs must be between zero and ${DEFAULT_CACHE_TTL_MS}`);
  }
  if (!entry || entry.status !== 'success' || !entry.snapshot || !Number.isSafeInteger(entry.fetchedAtMs)) return false;
  const age = now - entry.fetchedAtMs;
  return age >= 0 && age < ttlMs;
}

export function planCachedRequests(requests, cacheEntries = new Map(), options = {}) {
  const nowMs = options.nowMs ?? Date.now();
  const ttlMs = options.ttlMs ?? DEFAULT_CACHE_TTL_MS;
  const refresh = options.refresh ?? false;
  const refreshSet = refresh instanceof Set ? refresh : null;
  const bypasses = (identity) => refresh === true || refreshSet?.has(identity);
  const hits = [];
  const misses = [];
  for (const request of requests) {
    const entry = cacheEntries instanceof Map ? cacheEntries.get(request.cacheIdentity) : undefined;
    if (!bypasses(request.cacheIdentity) && cacheEntryIsFresh(entry, nowMs, ttlMs)) hits.push(request);
    else misses.push(request);
  }
  return { requests, hits, misses };
}
