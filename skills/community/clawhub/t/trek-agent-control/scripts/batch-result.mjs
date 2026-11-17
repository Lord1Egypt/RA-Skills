const RESOURCE_KEYS = [
  'trip',
  'place',
  'assignment',
  'reservation',
  'accommodation',
  'item',
  'bag',
  'file',
  'note',
  'proposal',
  'todo',
  'member',
];

export function isHighRiskBatchTool(name) {
  return typeof name === 'string'
    && (/(^|_)(delete|remove|decide|schedule|settle|restore|rotate)(_|$)/i.test(name)
      || name === 'unassign_place');
}

export function normalizeBatchResult(value) {
  const payload = value && typeof value === 'object' && !Array.isArray(value) ? value : {};
  const resourceType = RESOURCE_KEYS.find((key) => payload[key] && typeof payload[key] === 'object') || null;
  const failed = payload.ok === false || Boolean(payload.error);
  return {
    ok: !failed,
    resourceType,
    resource: resourceType ? payload[resourceType] : null,
    warnings: Array.isArray(payload.warnings) ? payload.warnings : [],
    result: value,
  };
}

export function normalizeBatchError(error) {
  return {
    ok: false,
    resourceType: null,
    resource: null,
    warnings: [],
    result: null,
    error: {
      message: error instanceof Error ? error.message : String(error),
    },
  };
}
