/**
 * LLM Memory Extraction - Extract structured memory from text
 */

export async function extractMemory(text, config) {
  const result = {
    text: text.trim(),
    category: 'general',
    importance: 0.5,
    confidence: 0.7,
    tags: [],
    entities: [],
  };
  
  const textLower = text.toLowerCase();
  
  if (textLower.includes('喜欢') || textLower.includes('prefer')) {
    result.category = 'preference'; result.importance = 0.7; result.tags.push('preference');
  } else if (textLower.includes('决定') || textLower.includes('decided')) {
    result.category = 'decision'; result.importance = 0.8; result.tags.push('decision');
  } else if (textLower.includes('项目') || textLower.includes('project')) {
    result.category = 'entity'; result.importance = 0.6; result.tags.push('project');
  }
  
  const knownEntities = ['python', 'javascript', 'typescript', 'java', 'rust', 'go', 'openai', 'claude', 'ollama', 'lancedb'];
  for (const entity of knownEntities) {
    if (textLower.includes(entity)) { result.entities.push(entity); result.tags.push(entity); }
  }
  
  if (text.length > 100) result.summary = text.substring(0, 100).trim() + '...';
  
  result.confidence = 0.5;
  if (result.category !== 'general') result.confidence += 0.2;
  if (result.entities.length > 0) result.confidence += 0.1;
  
  return result;
}

export async function extractBatch(texts, config) {
  const results = [];
  for (const text of texts) {
    results.push(await extractMemory(text, config));
    await new Promise(resolve => setTimeout(resolve, 10));
  }
  return results;
}

if (require.main === module) {
  console.log('\n🧠 LLM Memory Extraction\n');
  console.log('  extractMemory(text) - Extract structured memory');
  console.log('  extractBatch(texts) - Batch extract');
  console.log('');
}
