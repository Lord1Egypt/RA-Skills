import { getDatabase } from '../db/database';
import { Book } from '../types';

export class BookService {
  // 发布书目
  static create(book: Omit<Book, 'id' | 'createdAt' | 'updatedAt'>): Book {
    const db = getDatabase();
    const tagsJson = JSON.stringify(book.tags);
    
    const result = db.prepare(`
      INSERT INTO books (title, author, description, cover_url, tags, category)
      VALUES (?, ?, ?, ?, ?, ?)
    `).run(
      book.title,
      book.author,
      book.description,
      book.coverUrl || null,
      tagsJson,
      book.category || null
    );

    return this.getById(result.lastInsertRowid as number)!;
  }

  // 获取书目详情
  static getById(id: number): Book | null {
    const db = getDatabase();
    const row = db.prepare('SELECT * FROM books WHERE id = ?').get(id) as any;
    if (!row) return null;
    return this.mapRowToBook(row);
  }

  // 浏览书目列表
  static list(limit: number = 50, offset: number = 0): Book[] {
    const db = getDatabase();
    const rows = db.prepare(`
      SELECT * FROM books 
      ORDER BY created_at DESC 
      LIMIT ? OFFSET ?
    `).all(limit, offset) as any[];
    
    return rows.map(this.mapRowToBook);
  }

  // 搜索书目
  static search(query: string, category?: string): Book[] {
    const db = getDatabase();
    let sql = `
      SELECT * FROM books 
      WHERE (title LIKE ? OR author LIKE ? OR description LIKE ?)
    `;
    const params = [`%${query}%`, `%${query}%`, `%${query}%`];
    
    if (category) {
      sql += ' AND category = ?';
      params.push(category);
    }
    
    sql += ' ORDER BY created_at DESC';
    
    const rows = db.prepare(sql).all(...params) as any[];
    return rows.map(this.mapRowToBook);
  }

  // 按标签搜索
  static searchByTag(tag: string): Book[] {
    const db = getDatabase();
    const rows = db.prepare(`
      SELECT * FROM books 
      WHERE tags LIKE ?
      ORDER BY created_at DESC
    `).all(`%"${tag}"%`) as any[];
    
    return rows.map(this.mapRowToBook);
  }

  // 获取所有分类
  static getCategories(): string[] {
    const db = getDatabase();
    const rows = db.prepare(`
      SELECT DISTINCT category FROM books 
      WHERE category IS NOT NULL 
      ORDER BY category
    `).all() as any[];
    
    return rows.map(r => r.category);
  }

  // 获取所有标签
  static getAllTags(): string[] {
    const db = getDatabase();
    const rows = db.prepare('SELECT tags FROM books').all() as any[];
    
    const tagSet = new Set<string>();
    rows.forEach(row => {
      try {
        const tags = JSON.parse(row.tags);
        tags.forEach((tag: string) => tagSet.add(tag));
      } catch {}
    });
    
    return Array.from(tagSet).sort();
  }

  // 更新书目
  static update(id: number, updates: Partial<Book>): Book | null {
    const db = getDatabase();
    const fields: string[] = [];
    const values: any[] = [];

    if (updates.title) { fields.push('title = ?'); values.push(updates.title); }
    if (updates.author) { fields.push('author = ?'); values.push(updates.author); }
    if (updates.description !== undefined) { fields.push('description = ?'); values.push(updates.description); }
    if (updates.coverUrl !== undefined) { fields.push('cover_url = ?'); values.push(updates.coverUrl); }
    if (updates.tags) { fields.push('tags = ?'); values.push(JSON.stringify(updates.tags)); }
    if (updates.category !== undefined) { fields.push('category = ?'); values.push(updates.category); }
    
    fields.push('updated_at = CURRENT_TIMESTAMP');
    values.push(id);

    db.prepare(`UPDATE books SET ${fields.join(', ')} WHERE id = ?`).run(...values);
    return this.getById(id);
  }

  // 删除书目
  static delete(id: number): boolean {
    const db = getDatabase();
    const result = db.prepare('DELETE FROM books WHERE id = ?').run(id);
    return result.changes > 0;
  }

  private static mapRowToBook(row: any): Book {
    return {
      id: row.id,
      title: row.title,
      author: row.author,
      description: row.description,
      coverUrl: row.cover_url,
      tags: JSON.parse(row.tags || '[]'),
      category: row.category,
      createdAt: row.created_at,
      updatedAt: row.updated_at
    };
  }
}
