// Dependency-free, allowlisted projections from normalized API snapshots.

const error = (code, message) => ({ ok: false, error: { code, message } });
const MAX_METRIC_STRING = 4096;
const MAX_TABLE_STRING = 1024;
const BLOCK_OPERATIONS = Object.freeze({
  'price-chart': new Set(['stock_chart']),
  sentiment: new Set(['score_series', 'sentiment_series']),
  'news-feed': new Set(['ticker_stories', 'stories']),
  watchlist: new Set(['index_prices', 'screener_execute']),
  'market-mood': new Set(['market_mood']),
});

const scalar = (value, maxString) => value === null || typeof value === 'boolean' ||
  (typeof value === 'number' && Number.isFinite(value)) ||
  (typeof value === 'string' && value.length <= maxString);

const operationFor = (manifest, operationId) =>
  manifest?.operations?.find((operation) => operation.kind === 'api' && operation.id === operationId);

const readPath = (value, path) => {
  let current = value;
  for (const key of path.split('.').filter(Boolean)) {
    if (current === null || typeof current !== 'object' || !Object.hasOwn(current, key)) return undefined;
    current = current[key];
  }
  return current;
};

const collectionPath = (path) => {
  const marker = path.indexOf('[]');
  if (marker < 0) return null;
  const root = path.slice(0, marker).replace(/\.$/, '');
  const item = path.slice(marker + 2).replace(/^\./, '');
  if (!item || item.includes('[]')) return null;
  return { root, item };
};

const validDate = (value) => {
  if (typeof value !== 'string' || !/^\d{4}-\d{2}-\d{2}$/.test(value)) return false;
  const parsed = new Date(`${value}T00:00:00Z`);
  return Number.isFinite(parsed.valueOf()) && parsed.toISOString().slice(0, 10) === value;
};

const validInstant = (value) => typeof value === 'string' &&
  /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})$/.test(value) &&
  validDate(value.slice(0, 10)) &&
  Number.isFinite(Date.parse(value));

export function validateLiveBlockBinding(manifest, snapshot, block, options = {}) {
  if (!block?.props?.dataRef) return error('MISSING_DATA_REF', 'Live block requires props.dataRef.');
  const expectedSnapshotId = options.effectiveSnapshotId ?? block.props.dataRef;
  if (typeof expectedSnapshotId !== 'string' || snapshot?.id !== expectedSnapshotId) {
    return error('SNAPSHOT_BINDING_MISMATCH', 'Snapshot does not match the trusted effective binding.');
  }
  const operation = operationFor(manifest, snapshot.operationId);
  if (!operation) return error('UNSUPPORTED_OPERATION', 'Snapshot operation is not registered for presentation.');
  if (!Array.isArray(operation.displayFields) || operation.displayFields.length === 0) {
    return error('UNSUPPORTED_OPERATION', 'Snapshot operation has no display field contract.');
  }
  if (!Object.hasOwn(snapshot, 'data')) return error('INVALID_SNAPSHOT', 'Snapshot has no normalized data payload.');
  const allowedOperations = BLOCK_OPERATIONS[block.type];
  if (allowedOperations && !allowedOperations.has(operation.id)) {
    return error('BLOCK_OPERATION_MISMATCH', 'Snapshot operation is not allowed for this block type.');
  }
  if (block.props.ticker) {
    if (!snapshot.inputs || typeof snapshot.inputs.ticker !== 'string') {
      return error('INVALID_SNAPSHOT', 'Ticker block requires normalized snapshot inputs for binding verification.');
    }
    if (snapshot.inputs.ticker.toUpperCase() !== block.props.ticker.toUpperCase()) {
      return error('INPUT_MISMATCH', 'Block ticker does not match the normalized snapshot input.');
    }
  }
  if (block.type === 'price-chart' && block.props.range) {
    const requestedRange = snapshot.inputs?.timeframe ?? snapshot.inputs?.range;
    if (typeof requestedRange !== 'string') {
      return error('INVALID_SNAPSHOT', 'Price chart requires its normalized timeframe input for binding verification.');
    }
    if (requestedRange.toUpperCase() !== block.props.range.toUpperCase()) {
      return error('INPUT_MISMATCH', 'Block range does not match the normalized snapshot timeframe.');
    }
  }
  if (block.type === 'metric-card') {
    const selected = getDisplayField(manifest, snapshot, block.props.field);
    if (!selected.ok) return selected;
  }
  if (block.type === 'table') {
    const projected = projectSnapshotTable(manifest, snapshot);
    if (!projected.ok) return projected;
  }
  return { ok: true, operation, snapshot };
}

// A flat preview contract (operation.preview.shape === 'flat') moves the fields it keeps from
// nested objects such as `latest` or `context` directly under data. Returns the path to read,
// or null when the preview withholds the field entirely.
const previewPath = (operation, snapshot, path) => {
  const contract = operation.preview;
  if (snapshot?.isPreview !== true || contract?.shape !== 'flat') return path;
  const keys = path.split('.');
  const flattened = keys.length === 2 && contract.flattens?.includes(keys[0]);
  const leaf = flattened ? keys[1] : path;
  return contract.fields?.includes(leaf) ? leaf : null;
};

export function getDisplayField(manifest, snapshot, key) {
  const operation = operationFor(manifest, snapshot?.operationId);
  if (!operation) return error('UNSUPPORTED_OPERATION', 'Snapshot operation is not registered for presentation.');
  const field = operation.displayFields?.find((candidate) => candidate.key === key);
  if (!field) return error('UNSUPPORTED_FIELD', 'Field is not allowlisted for this operation.');
  if (collectionPath(field.path)) {
    return error('COLLECTION_FIELD', 'A collection field cannot be selected as a metric scalar.');
  }
  const path = previewPath(operation, snapshot, field.path);
  if (path === null) return { ok: true, field, value: null, missing: true, withheldByPreview: true };
  const value = readPath(snapshot.data, path);
  if (value === undefined || value === null) return { ok: true, field, value: null, missing: true };
  if (!scalar(value, MAX_METRIC_STRING)) return error('NON_SCALAR_FIELD', 'Display field did not resolve to a bounded scalar value.');
  return { ok: true, field, value, missing: false };
}

export function projectSnapshotTable(manifest, snapshot, options = {}) {
  const operation = operationFor(manifest, snapshot?.operationId);
  if (!operation) return error('UNSUPPORTED_OPERATION', 'Snapshot operation is not registered for presentation.');
  const defaults = operation.displayFields?.filter((field) => collectionPath(field.path)).map((field) => field.key) ?? [];
  const requested = options.fields ?? defaults;
  if (!Array.isArray(requested) || requested.length === 0) return error('NO_TABLE_FIELDS', 'Table needs at least one allowlisted field.');
  if (new Set(requested).size !== requested.length) return error('DUPLICATE_FIELD', 'Table fields must be unique.');
  const fields = [];
  for (const key of requested) {
    const field = operation.displayFields?.find((candidate) => candidate.key === key);
    if (!field) return error('UNSUPPORTED_FIELD', 'Table field is not allowlisted for this operation.');
    const parsed = collectionPath(field.path);
    if (!parsed) return error('NOT_A_TABLE_FIELD', 'Table fields must select rows from a documented collection.');
    fields.push({ ...field, ...parsed });
  }
  if (new Set(fields.map((field) => field.root)).size !== 1) {
    return error('MIXED_COLLECTIONS', 'Table fields must come from one documented collection.');
  }
  const rowsValue = fields[0].root ? readPath(snapshot.data, fields[0].root) : snapshot.data;
  if (!Array.isArray(rowsValue)) return error('INVALID_TABLE_DATA', 'Documented table collection is not an array.');
  const limit = options.limit ?? 25;
  if (!Number.isInteger(limit) || limit < 1 || limit > 100) return error('INVALID_LIMIT', 'Table limit must be an integer from 1 to 100.');
  const rows = [];
  for (const source of rowsValue.slice(0, limit)) {
    if (source === null || typeof source !== 'object' || Array.isArray(source)) {
      return error('INVALID_TABLE_ROW', 'Table collection contains a non-object row.');
    }
    const row = {};
    for (const field of fields) {
      const value = readPath(source, field.item);
      if (value !== undefined && !scalar(value, MAX_TABLE_STRING)) return error('NON_SCALAR_FIELD', 'Table field resolved to a non-scalar or oversized value.');
      row[field.key] = value === undefined ? null : value;
    }
    rows.push(row);
  }
  return {
    ok: true,
    columns: fields.map(({ key, label }) => ({ key, label })),
    rows,
    truncated: rowsValue.length > rows.length,
  };
}

export function getSnapshotAsOf(manifest, snapshot) {
  const operation = operationFor(manifest, snapshot?.operationId);
  if (!operation) return error('UNSUPPORTED_OPERATION', 'Snapshot operation is not registered for presentation.');
  const contract = operation.asOf;
  if (!contract || contract.kind === 'none') return { ok: true, contract, value: null, missing: true };
  if (collectionPath(contract.path ?? '')) {
    return { ok: true, contract, value: null, missing: true, rowLevel: true };
  }
  const value = readPath(snapshot.data, contract.path);
  if (value === undefined || value === null) return { ok: true, contract, value: null, missing: true };
  const valid = contract.unit === 'epoch-ms' || contract.unit === 'epoch-sec'
    ? typeof value === 'number' && Number.isSafeInteger(value) && value >= 0
    : contract.unit === 'date'
      ? validDate(value)
      : contract.unit === 'iso-8601'
        ? validInstant(value)
        : false;
  if (!valid) return error('INVALID_AS_OF', 'As-of value does not match the operation contract.');
  return { ok: true, contract, value, missing: false };
}
