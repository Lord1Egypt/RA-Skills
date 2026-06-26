/**
 * 笔记命令处理模块
 * 处理所有笔记相关的用户命令
 */

import { 
  createNote, 
  createNoteAsync, 
  getNote, 
  getNoteSync,
  getAllNotes, 
  getAllNotesSync,
  updateNote, 
  searchNotes, 
  searchNotesSync,
  semanticSearchNotes,
  searchByTag,
  getVersions, 
  getVersionsSync,
  markVersion, 
  revertToVersion, 
  deleteNote, 
  exportToMarkdown,
  getDBStats 
} from '../storage/db.js';
import { isAIAvailable, expandSearchQuery, isLocalEmbeddingAvailable, getEmbeddingModelInfo } from '../ai/index.js';
import { Note } from '../types/index.js';
import path from 'path';
import fs from 'fs';

const DATA_PATH = process.env.YILIU_DATA_PATH || path.join(process.cwd(), 'data');

/**
 * 同步创建笔记（向后兼容）
 */
export function handleNote(input: string): { message: string; note?: Note } {
  const note = createNote(input.trim());
  return { message: formatNoteResponse(note), note };
}

/**
 * 异步创建笔记（带 AI 增强）
 */
export async function handleNoteAsync(input: string): Promise<{ message: string; note?: Note }> {
  const note = await createNoteAsync(input.trim());
  return { message: formatNoteResponseEnhanced(note), note };
}

export async function handleList(limit: number = 10): Promise<string> {
  const notes = await getAllNotes(limit);
  
  if (notes.length === 0) {
    return '暂无笔记，来记一条吧！';
  }

  const list = notes.map((n, i) => {
    const preview = n.content.slice(0, 30);
    const time = new Date(n.updatedAt).toLocaleString('zh-CN');
    const tags = n.aiEnhanced?.tags?.slice(0, 2).map(t => `#${t}`).join(' ') || '';
    return `${i + 1}. ${preview}... ${tags}\n   📅 ${time}`;
  }).join('\n\n');

  return `共有 ${notes.length} 条笔记：\n\n${list}`;
}

/**
 * 关键词搜索（同步版本）
 */
export function handleSearch(query: string): string {
  const notes = searchNotesSync(query.trim());
  
  if (notes.length === 0) {
    return `未找到关于「${query}」的笔记`;
  }

  const list = notes.map((n, i) => {
    const preview = n.content.slice(0, 50);
    const shortId = n.id.slice(0, 8);
    const tags = n.aiEnhanced?.tags?.slice(0, 2).map(t => `#${t}`).join(' ') || '';
    return `${shortId}: ${preview}... ${tags}`;
  }).join('\n');

  return `找到 ${notes.length} 条相关笔记：\n\n${list}`;
}

/**
 * 语义搜索（异步版本，带向量相似度）
 */
export async function handleSemanticSearch(query: string): Promise<string> {
  // 检查是否有 AI 能力（云端或本地）
  const hasAI = isAIAvailable() || await isLocalEmbeddingAvailable();
  
  if (!hasAI) {
    // 没有 AI 能力，回退到关键词搜索（使用异步版本）
    const notes = await searchNotes(query);
    
    if (notes.length === 0) {
      return `未找到关于「${query}」的笔记`;
    }

    const list = notes.map((n, i) => {
      const preview = n.content.slice(0, 50);
      const shortId = n.id.slice(0, 8);
      const tags = n.aiEnhanced?.tags?.slice(0, 2).map(t => `#${t}`).join(' ') || '';
      return `${shortId}: ${preview}... ${tags}`;
    }).join('\n');

    return `找到 ${notes.length} 条相关笔记：\n\n${list}`;
  }

  const results = await semanticSearchNotes(query, 10);
  
  if (results.length === 0) {
    // 语义搜索无结果，回退到关键词搜索
    const notes = await searchNotes(query);
    if (notes.length === 0) {
      return `未找到关于「${query}」的笔记`;
    }
    
    const list = notes.map((n) => {
      const preview = n.content.slice(0, 50);
      const shortId = n.id.slice(0, 8);
      return `${shortId}: ${preview}...`;
    }).join('\n');
    
    return `找到 ${notes.length} 条相关笔记（关键词匹配）：\n\n${list}`;
  }

  const list = results.map((r, i) => {
    const preview = r.note.content.slice(0, 50);
    const shortId = r.note.id.slice(0, 8);
    const score = Math.round(r.score * 100);
    const tags = r.note.aiEnhanced?.tags?.slice(0, 2).map(t => `#${t}`).join(' ') || '';
    return `${shortId}: ${preview}... ${tags} (${score}%)`;
  }).join('\n');

  return `找到 ${results.length} 条相关笔记：\n\n${list}`;
}

export async function handleView(idOrKeyword: string): Promise<string> {
  // 先尝试作为 ID 查询
  let note = await getNote(idOrKeyword);
  if (!note) {
    // 回退到关键词搜索
    const notes = await searchNotes(idOrKeyword);
    if (notes.length > 0) {
      note = notes[0];
    }
  }
  
  if (!note) {
    return '笔记不存在';
  }
  return formatNoteDetail(note);
}

export async function handleUpdate(id: string, content: string): Promise<string> {
  const note = await updateNote(id, content.trim());
  if (!note) {
    return '更新失败，笔记不存在';
  }
  const versions = await getVersions(id);
  return `已更新为v${versions.length}：\n\n${note.content}`;
}

export async function handleHistory(idOrKeyword: string): Promise<string> {
  let note = await getNote(idOrKeyword);
  if (!note) {
    const notes = await searchNotes(idOrKeyword);
    if (notes.length > 0) {
      note = notes[0];
    }
  }
  
  if (!note) {
    return '笔记不存在';
  }

  const versions = await getVersions(note.id);
  
  const list = versions.map(v => {
    const time = new Date(v.createdAt).toLocaleString('zh-CN');
    const marked = v.isMarked ? ' ⭐' : '';
    const markNote = v.markNote ? ` - ${v.markNote}` : '';
    return `v${v.version} ${time}${marked}${markNote}`;
  }).join('\n');

  return `「${note.content.slice(0, 20)}...」\nID: ${note.id.slice(0, 8)}\n\n版本历史：\n\n${list}`;
}

export async function handleMark(id: string, version: number, markNote: string): Promise<string> {
  const success = await markVersion(id, version, markNote);
  if (!success) {
    return '标记失败';
  }
  return `已标记为「${markNote}」`;
}

export async function handleRevert(id: string, version: number): Promise<string> {
  const note = await revertToVersion(id, version);
  if (!note) {
    return '回溯失败';
  }
  return `已恢复到v${version}：\n\n${note.content}`;
}

export async function handleDelete(id: string): Promise<string> {
  const success = await deleteNote(id);
  if (!success) {
    return '删除失败';
  }
  return '已删除';
}

export function handleExport(format: string = 'md'): string {
  try {
    const filePath = exportToMarkdown(format);
    return `已导出到：${filePath}`;
  } catch (e) {
    return `导出失败：${e}`;
  }
}

export async function handleLinkCapture(url: string): Promise<string> {
  // Basic URL capture - in V2 would fetch and extract content
  const note = await createNoteAsync(`链接：${url}`, 'link', url);
  return `已保存链接：${url}`;
}

/**
 * 显示统计信息
 */
export async function handleStats(): Promise<string> {
  const stats = await getDBStats();
  const aiStatus = isAIAvailable() ? '✅ 已配置' : '❌ 未配置';
  const modelInfo = getEmbeddingModelInfo();
  
  let embedderInfo = '';
  if (modelInfo.isLocal) {
    embedderInfo = `\n🧠 嵌入模型：${modelInfo.model} (本地)`;
  } else if (isAIAvailable()) {
    embedderInfo = `\n🧠 嵌入模型：${modelInfo.model} (云端)`;
  }
  
  return `📊 忆流统计

📝 笔记总数：${stats.notes}
🧮 已向量化：${stats.vectorized}
📏 平均长度：${stats.avgLength} 字

🤖 AI 状态：${aiStatus}${embedderInfo}
`;
}

function formatNoteResponse(note: Note): string {
  const time = new Date(note.createdAt).toLocaleString('zh-CN');
  return `已保存 (v1)\n\n${note.content}\n\n📅 ${time}`;
}

function formatNoteResponseEnhanced(note: Note): string {
  const time = new Date(note.createdAt).toLocaleString('zh-CN');
  let msg = `已保存 (v1)\n\n${note.content}\n\n📅 ${time}`;
  
  if (note.aiEnhanced) {
    if (note.aiEnhanced.summary) {
      msg += `\n\n📝 摘要：${note.aiEnhanced.summary}`;
    }
    if (note.aiEnhanced.tags?.length) {
      msg += `\n🏷️ 标签：${note.aiEnhanced.tags.map(t => `#${t}`).join(' ')}`;
    }
  }
  
  return msg;
}

function formatNoteDetail(note: Note): string {
  const time = new Date(note.updatedAt).toLocaleString('zh-CN');
  let info = `📝 ${note.content}\n\n`;
  info += `📅 更新时间：${time}\n`;
  info += `📊 字数：${note.wordCount}\n`;
  info += `🏷️ 来源：${note.source}`;
  
  if (note.aiEnhanced?.tags?.length) {
    info += `\n🏷️ 标签：${note.aiEnhanced.tags.map(t => `#${t}`).join(' ')}`;
  }
  
  if (note.aiEnhanced?.summary) {
    info += `\n📝 摘要：${note.aiEnhanced.summary}`;
  }
  
  return info;
}
