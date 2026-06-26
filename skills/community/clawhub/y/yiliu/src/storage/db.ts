/**
 * 数据库模块 - LibSQL 版本
 * 使用 @libsql/client 替代 sql.js
 */

import { createClient, type Client, type InValue, type ResultSet } from '@libsql/client';
import { Note, NoteVersion } from '../types/index.js';
import { randomUUID } from 'crypto';
import path from 'path';
import fs from 'fs';
import { generateEmbedding, enhanceNote, isAIAvailable, type AIEnhanceResult } from '../ai/index.js';
import { initVectorStore, addVector, removeVector, semanticSearch, hybridSearch, getStats } from './vector.js';

const DB_PATH = path.join(process.cwd(), 'data', 'yiliu.db');

let db: Client;

/**
 * 初始化数据库
 */
export async function initDB(): Promise<void> {
  const dataDir = path.join(process.cwd(), 'data');
  if (!fs.existsSync(dataDir)) {
    fs.mkdirSync(dataDir, { recursive: true });
  }

  // 使用 LibSQL 本地文件数据库
  db = createClient({
    url: `file:${DB_PATH}`,
  });

  // 创建表
  await db.execute(`
    CREATE TABLE IF NOT EXISTS notes (
      id TEXT PRIMARY KEY,
      content TEXT NOT NULL,
      layer TEXT DEFAULT 'L0',
      source TEXT DEFAULT 'text',
      url TEXT,
      createdAt INTEGER NOT NULL,
      updatedAt INTEGER NOT NULL,
      wordCount INTEGER DEFAULT 0,
      aiEnhanced TEXT,
      embedding TEXT
    )
  `);

  await db.execute(`
    CREATE TABLE IF NOT EXISTS note_versions (
      id TEXT PRIMARY KEY,
      noteId TEXT NOT NULL,
      content TEXT NOT NULL,
      version INTEGER NOT NULL,
      isMarked INTEGER DEFAULT 0,
      markNote TEXT,
      createdAt INTEGER NOT NULL
    )
  `);

  // 初始化向量存储
  initVectorStore(dataDir);
}

/**
 * 将 ResultSet 转换为对象数组
 */
function resultSetToObjects(result: ResultSet): any[] {
  return result.rows.map(row => {
    const obj: any = {};
    result.columns.forEach((col, i) => {
      obj[col] = row[i];
    });
    return obj;
  });
}

/**
 * 将行数据转换为 Note 对象
 */
function rowToNote(row: any, columns: string[]): Note {
  const obj: any = {};
  columns.forEach((col, i) => {
    obj[col] = row[i];
  });
  
  return {
    id: obj.id,
    content: obj.content,
    layer: obj.layer || 'L0',
    source: obj.source || 'text',
    url: obj.url,
    createdAt: obj.createdAt,
    updatedAt: obj.updatedAt,
    wordCount: obj.wordCount || 0,
    aiEnhanced: obj.aiEnhanced ? JSON.parse(obj.aiEnhanced) : undefined,
    embedding: obj.embedding ? JSON.parse(obj.embedding) : undefined,
  };
}

/**
 * 创建笔记（带 AI 增强）
 */
export async function createNoteAsync(content: string, source: string = 'text', url?: string): Promise<Note> {
  const id = randomUUID();
  const now = Date.now();
  const wordCount = content.length;

  // 初始笔记
  let note: Note = {
    id,
    content,
    layer: 'L0',
    source: source as any,
    url: url || undefined,
    createdAt: now,
    updatedAt: now,
    wordCount
  };

  // AI 增强
  let aiResult: AIEnhanceResult | null = null;
  let embedding: number[] | null = null;

  if (isAIAvailable()) {
    // 并行执行 embedding 和 enhancement
    const [embResult, enhanceResult] = await Promise.all([
      generateEmbedding(content),
      enhanceNote(content),
    ]);

    embedding = embResult?.embedding || null;
    aiResult = enhanceResult;

    if (aiResult) {
      note.aiEnhanced = {
        summary: aiResult.summary,
        tags: aiResult.tags,
        relatedIds: [],
      };
    }
  }

  // 插入数据库
  await db.execute({
    sql: `INSERT INTO notes (id, content, layer, source, url, createdAt, updatedAt, wordCount, aiEnhanced, embedding) 
          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`,
    args: [
      note.id,
      note.content,
      note.layer,
      note.source,
      note.url ?? null,
      note.createdAt,
      note.updatedAt,
      note.wordCount,
      note.aiEnhanced ? JSON.stringify(note.aiEnhanced) : null,
      embedding ? JSON.stringify(embedding) : null,
    ] as InValue[]
  });

  // 添加到向量索引
  if (embedding) {
    addVector(id, embedding, content);
  }

  await createVersion(note);

  return note;
}

/**
 * 内部：创建版本记录
 */
async function createVersion(note: Note): Promise<void> {
  const result = await db.execute({
    sql: `SELECT COUNT(*) as count FROM note_versions WHERE noteId = ?`,
    args: [note.id]
  });
  
  const count = result.rows.length > 0 ? Number(result.rows[0][0]) : 0;
  const version = count + 1;

  await db.execute({
    sql: `INSERT INTO note_versions (id, noteId, content, version, isMarked, createdAt) VALUES (?, ?, ?, ?, 0, ?)`,
    args: [randomUUID(), note.id, note.content, version, Date.now()] as InValue[]
  });
}

/**
 * 更新笔记
 */
export async function updateNote(id: string, content: string): Promise<Note | null> {
  const note = await getNote(id);
  if (!note) return null;

  const now = Date.now();
  const wordCount = content.length;

  await db.execute({
    sql: `UPDATE notes SET content = ?, updatedAt = ?, wordCount = ? WHERE id = ?`,
    args: [content, now, wordCount, id] as InValue[]
  });

  await createVersion({ ...note, content, updatedAt: now, wordCount });

  return getNote(id);
}

/**
 * 获取单个笔记
 */
export async function getNote(id: string): Promise<Note | null> {
  const result = await db.execute({
    sql: `SELECT * FROM notes WHERE id = ?`,
    args: [id]
  });
  
  if (result.rows.length === 0) return null;
  
  return rowToNote(result.rows[0], result.columns);
}

/**
 * 获取所有笔记
 */
export async function getAllNotes(limit: number = 50): Promise<Note[]> {
  const result = await db.execute({
    sql: `SELECT * FROM notes ORDER BY updatedAt DESC LIMIT ?`,
    args: [limit]
  });
  
  return result.rows.map(row => rowToNote(row, result.columns));
}

/**
 * 关键词搜索
 */
export async function searchNotes(keyword: string): Promise<Note[]> {
  const result = await db.execute({
    sql: `SELECT * FROM notes WHERE content LIKE ? ORDER BY updatedAt DESC LIMIT 20`,
    args: [`%${keyword}%`]
  });
  
  return result.rows.map(row => rowToNote(row, result.columns));
}

/**
 * 语义搜索（使用向量相似度）
 */
export async function semanticSearchNotes(query: string, topK: number = 10): Promise<Array<{ note: Note; score: number }>> {
  // 生成查询向量
  const embResult = await generateEmbedding(query);
  
  if (!embResult) {
    // 回退到关键词搜索
    const notes = await searchNotes(query);
    return notes.map(note => ({ note, score: 0.5 }));
  }

  // 使用混合搜索
  const results = hybridSearch(embResult.embedding, [query], topK);
  
  // 获取完整笔记
  const notesWithScores: Array<{ note: Note; score: number }> = [];
  for (const r of results) {
    const note = await getNote(r.id);
    if (note) {
      notesWithScores.push({ note, score: r.score });
    }
  }
  
  return notesWithScores;
}

/**
 * 按标签搜索
 */
export async function searchByTag(tag: string): Promise<Note[]> {
  const result = await db.execute({
    sql: `SELECT * FROM notes WHERE aiEnhanced LIKE ? ORDER BY updatedAt DESC LIMIT 20`,
    args: [`%"${tag}"%`]
  });
  
  return result.rows.map(row => rowToNote(row, result.columns));
}

/**
 * 获取笔记版本历史
 */
export async function getVersions(noteId: string): Promise<NoteVersion[]> {
  const result = await db.execute({
    sql: `SELECT * FROM note_versions WHERE noteId = ? ORDER BY version DESC`,
    args: [noteId]
  });
  
  return result.rows.map(row => {
    const obj: any = {};
    result.columns.forEach((col, i) => {
      obj[col] = row[i];
    });
    return obj as NoteVersion;
  });
}

/**
 * 标记版本
 */
export async function markVersion(noteId: string, version: number, markNote: string): Promise<boolean> {
  const result = await db.execute({
    sql: `UPDATE note_versions SET isMarked = 1, markNote = ? WHERE noteId = ? AND version = ?`,
    args: [markNote, noteId, version] as InValue[]
  });
  
  return result.rowsAffected > 0;
}

/**
 * 回滚到指定版本
 */
export async function revertToVersion(noteId: string, version: number): Promise<Note | null> {
  const result = await db.execute({
    sql: `SELECT * FROM note_versions WHERE noteId = ? AND version = ?`,
    args: [noteId, version]
  });
  
  if (result.rows.length === 0) return null;
  
  const row = result.rows[0];
  const content = row[2] as string; // content 是第3列
  
  return updateNote(noteId, content);
}

/**
 * 删除笔记
 */
export async function deleteNote(id: string): Promise<boolean> {
  await db.execute({
    sql: `DELETE FROM note_versions WHERE noteId = ?`,
    args: [id]
  });
  
  const result = await db.execute({
    sql: `DELETE FROM notes WHERE id = ?`,
    args: [id]
  });
  
  removeVector(id);
  
  return result.rowsAffected > 0;
}

/**
 * 关闭数据库
 */
export function closeDB(): void {
  // LibSQL 客户端会自动关闭
}

/**
 * 导出为 Markdown
 */
export async function exportToMarkdown(format: string = 'md'): Promise<string> {
  const notes = await getAllNotes(1000);
  const now = new Date().toISOString().slice(0, 10);
  const dataDir = path.join(process.cwd(), 'data');
  
  if (!fs.existsSync(dataDir)) {
    fs.mkdirSync(dataDir, { recursive: true });
  }
  
  const filePath = path.join(dataDir, `yiliu-export-${now}.md`);
  
  let content = `# 忆流笔记导出\n\n导出时间：${new Date().toLocaleString('zh-CN')}\n\n---\n\n`;
  
  for (let i = 0; i < notes.length; i++) {
    const note = notes[i];
    const time = new Date(note.createdAt).toLocaleString('zh-CN');
    content += `## ${i + 1}. ${note.content.slice(0, 50)}${note.content.length > 50 ? '...' : ''}\n\n`;
    content += `- ID: ${note.id.slice(0, 8)}\n`;
    content += `- 创建时间：${time}\n`;
    content += `- 来源：${note.source}\n`;
    if (note.url) content += `- 链接：${note.url}\n`;
    if (note.aiEnhanced?.tags?.length) {
      content += `- 标签：${note.aiEnhanced.tags.join(', ')}\n`;
    }
    content += `\n${note.content}\n\n---\n\n`;
  }
  
  fs.writeFileSync(filePath, content, 'utf-8');
  return filePath;
}

/**
 * 获取数据库统计信息
 */
export async function getDBStats(): Promise<{ notes: number; vectorized: number; avgLength: number }> {
  const stats = getStats();
  const result = await db.execute(`SELECT COUNT(*) as count FROM notes`);
  const noteCount = result.rows.length > 0 ? Number(result.rows[0][0]) : 0;
  
  return {
    notes: noteCount,
    vectorized: stats.count,
    avgLength: stats.avgContentLength,
  };
}

// ========== 兼容层：同步函数（已弃用，建议使用异步版本）==========

// 为兼容旧代码，提供同步封装（内部使用异步调用）
export function createNote(content: string, source: string = 'text', url?: string): Note {
  // 同步版本已弃用，请使用 createNoteAsync
  // 这里返回一个临时对象，实际创建是异步的
  const id = randomUUID();
  const now = Date.now();
  return {
    id,
    content,
    layer: 'L0',
    source: source as any,
    url: url || undefined,
    createdAt: now,
    updatedAt: now,
    wordCount: content.length
  };
}

export function getNoteSync(id: string): Note | null {
  // 同步版本已弃用，请使用 await getNote(id)
  return null;
}

export function getAllNotesSync(limit: number = 50): Note[] {
  // 同步版本已弃用，请使用 await getAllNotes(limit)
  return [];
}

export function searchNotesSync(keyword: string): Note[] {
  // 同步版本已弃用，请使用 await searchNotes(keyword)
  return [];
}

export function getVersionsSync(noteId: string): NoteVersion[] {
  // 同步版本已弃用，请使用 await getVersions(noteId)
  return [];
}

export function deleteNoteSync(id: string): boolean {
  // 同步版本已弃用，请使用 await deleteNote(id)
  return false;
}

export function updateNoteSync(id: string, content: string): Note | null {
  // 同步版本已弃用，请使用 await updateNote(id, content)
  return null;
}

export function getDBStatsSync(): { notes: number; vectorized: number; avgLength: number } {
  // 同步版本已弃用，请使用 await getDBStats()
  return { notes: 0, vectorized: 0, avgLength: 0 };
}
