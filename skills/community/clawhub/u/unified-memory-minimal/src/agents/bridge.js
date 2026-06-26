/**
 * Memory Bridge - Bridge between different memory systems
 */

export function toExternalFormat(memory, target) {
  switch (target) {
    case 'anthropic':
      return { id: memory.id, content: memory.text, category: memory.category, priority: memory.importance };
    case 'openai':
      return { id: memory.id, text: memory.text, metadata: { category: memory.category, importance: memory.importance } };
    case 'langchain':
      return { page_content: memory.text, metadata: { id: memory.id, category: memory.category, importance: memory.importance } };
    default:
      return memory;
  }
}

export function fromExternalFormat(data, source) {
  switch (source) {
    case 'anthropic':
      return { id: data.id, text: data.content || data.text, category: data.category || 'general', importance: data.priority || 0.5 };
    case 'openai':
      return { id: data.id, text: data.text, category: data.metadata?.category || 'general', importance: data.metadata?.importance || 0.5 };
    case 'langchain':
      return { id: data.metadata?.id, text: data.page_content || data.text, category: data.metadata?.category || 'general', importance: data.metadata?.importance || 0.5 };
    default:
      return data;
  }
}

export function batchExport(memories, target) {
  return memories.map(mem => toExternalFormat(mem, target));
}

export function batchImport(data, source) {
  return data.map(item => fromExternalFormat(item, source));
}

if (require.main === module) {
  console.log('\n🌉 Memory Bridge\n');
  console.log('  Supported: anthropic, openai, langchain');
  console.log('  Usage: bridge.export(memory, target)');
  console.log('');
}
