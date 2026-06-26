/**
 * Standard Memory Format - Unified format for memory interchange
 */

export function validateMemory(memory) {
  const errors = [];
  if (!memory.id) errors.push('Missing required field: id');
  if (!memory.text) errors.push('Missing required field: text');
  if (memory.importance !== undefined && (memory.importance < 0 || memory.importance > 1)) errors.push('importance must be 0-1');
  if (memory.confidence !== undefined && (memory.confidence < 0 || memory.confidence > 1)) errors.push('confidence must be 0-1');
  const validCategories = ['preference', 'entity', 'fact', 'decision', 'learning', 'task', 'general'];
  if (memory.category && !validCategories.includes(memory.category)) errors.push(`Invalid category`);
  return { valid: errors.length === 0, errors };
}

export function normalizeMemory(memory) {
  const now = new Date().toISOString();
  return {
    id: memory.id || `mem_${Date.now()}`,
    text: memory.text || memory.content || '',
    category: memory.category || 'general',
    importance: normalizeNumber(memory.importance, 0.5, 0, 1),
    confidence: normalizeNumber(memory.confidence, 0.8, 0, 1),
    tags: Array.isArray(memory.tags) ? memory.tags : (memory.tags ? [memory.tags] : []),
    project: memory.project || 'default',
    created_at: normalizeDate(memory.created_at || memory.timestamp || now),
    updated_at: normalizeDate(memory.updated_at || now),
    access_count: memory.access_count || 0,
    metadata: memory.metadata || {},
  };
}

function normalizeNumber(value, defaultVal, min = 0, max = 1) {
  if (value === undefined || value === null) return defaultVal;
  const num = Number(value);
  if (isNaN(num)) return defaultVal;
  return Math.max(min, Math.min(max, num));
}

function normalizeDate(value) {
  if (!value) return undefined;
  try { return new Date(value).toISOString(); }
  catch { return undefined; }
}

export function serializeMemory(memory, options = {}) {
  const m = { ...memory };
  if (!options.includeMetadata) delete m.metadata;
  return JSON.stringify(m);
}

export function deserializeMemory(str) {
  try { return normalizeMemory(JSON.parse(str)); }
  catch { return null; }
}

if (require.main === module) {
  console.log('\n📦 Standard Format\n');
  console.log('  validateMemory(memory) - Validate memory object');
  console.log('  normalizeMemory(memory) - Normalize to standard format');
  console.log('  serializeMemory(memory) - Serialize to JSON');
  console.log('  deserializeMemory(str) - Deserialize from JSON');
  console.log('');
}
