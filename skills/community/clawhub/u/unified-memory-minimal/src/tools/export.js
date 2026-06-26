/**
 * memory_export - 记忆导出工具
 * 支持 json / markdown / csv 格式
 */

import { getAllMemories } from '../storage.js';
import { writeFileSync } from 'fs';
import { join } from 'path';

const EXPORTS_DIR = join(process.env.HOME || '/root', '.openclaw/workspace/memory/exports');

export async function exportMemories({ format = 'json', output, category, minImportance }) {
  const memories = getAllMemories();
  
  // Filter
  let filtered = memories;
  if (category) {
    filtered = filtered.filter(m => m.category === category);
  }
  if (minImportance !== undefined) {
    filtered = filtered.filter(m => (m.importance || 0) >= minImportance);
  }
  
  let content;
  let filename;
  
  if (format === 'json') {
    content = JSON.stringify({ memories: filtered, count: filtered.length }, null, 2);
    filename = output || `memories_${Date.now()}.json`;
  } else if (format === 'markdown') {
    content = generateMarkdown(filtered);
    filename = output || `memories_${Date.now()}.md`;
  } else if (format === 'csv') {
    content = generateCSV(filtered);
    filename = output || `memories_${Date.now()}.csv`;
  } else {
    return { content: [{ type: 'text', text: `Unsupported format: ${format}` }], isError: true };
  }
  
  try {
    writeFileSync(filename, content, 'utf-8');
    return {
      content: [{
        type: 'text',
        text: JSON.stringify({
          success: true,
          format,
          count: filtered.length,
          path: filename
        }, null, 2)
      }]
    };
  } catch (err) {
    return { content: [{ type: 'text', text: `导出失败: ${err.message}` }], isError: true };
  }
}

function generateMarkdown(memories) {
  const byCategory = {};
  for (const mem of memories) {
    const cat = mem.category || '未分类';
    if (!byCategory[cat]) byCategory[cat] = [];
    byCategory[cat].push(mem);
  }
  
  let md = `# 记忆导出\n\n导出时间: ${new Date().toISOString()}\n总共: ${memories.length} 条记忆\n\n`;
  
  for (const [cat, items] of Object.entries(byCategory)) {
    md += `## ${cat}\n\n`;
    for (const mem of items) {
      md += `- **${mem.text.slice(0, 100)}** (重要性: ${mem.importance || 0.5})\n`;
      if (mem.tags && mem.tags.length) md += `  - 标签: ${mem.tags.join(', ')}\n`;
      md += `\n`;
    }
  }
  
  return md;
}

function generateCSV(memories) {
  const headers = ['id', 'text', 'category', 'importance', 'tags', 'created_at'];
  const rows = [headers.join(',')];
  
  for (const mem of memories) {
    const row = [
      mem.id || '',
      `"${(mem.text || '').replace(/"/g, '""')}"`,
      mem.category || '',
      mem.importance || 0.5,
      (mem.tags || []).join(';'),
      mem.created_at || ''
    ];
    rows.push(row.join(','));
  }
  
  return rows.join('\n');
}
