/**
 * v2 Patch - Migration utilities for v2 breaking changes
 */

const V2_MIGRATION = {
  renamedFields: { 'content': 'text', 'category_name': 'category', 'imp': 'importance', 'conf': 'confidence' },
  removedFields: ['embedding_vector', 'vector_id', 'metadata_raw'],
  newFields: ['source', 'expires_at', 'project'],
};

export function migrateMemory(memory) {
  return {
    id: memory.id || `mem_${Date.now()}`,
    text: memory.content || '',
    category: memory.category_name || 'general',
    importance: memory.imp ?? 0.5,
    confidence: memory.conf ?? 0.8,
    tags: Array.isArray(memory.tags_arr) ? memory.tags_arr : [],
    project: 'default',
    created_at: memory.created_time || new Date().toISOString(),
    updated_at: memory.updated_time || new Date().toISOString(),
    access_count: 0,
    source: 'imported',
    metadata: {},
  };
}

export function needsMigration(memory) {
  return memory.content !== undefined || memory.category_name !== undefined;
}

export function getMigrationReport(memories) {
  let v1Count = 0, v2Count = 0;
  for (const mem of memories) {
    if (needsMigration(mem)) v1Count++;
    else v2Count++;
  }
  return { total: memories.length, v1Count, v2Count, needsMigration: v1Count };
}

if (require.main === module) {
  console.log('\n📦 v2 Migration Guide\n');
  console.log('  Renamed Fields:', V2_MIGRATION.renamedFields);
  console.log('  Removed Fields:', V2_MIGRATION.removedFields);
  console.log('  New Fields:', V2_MIGRATION.newFields);
  console.log('');
}
