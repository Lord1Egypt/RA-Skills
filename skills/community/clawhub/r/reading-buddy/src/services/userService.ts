import { getDatabase } from '../db/database';
import { User } from '../types';

export class UserService {
  // 创建用户
  static create(user: Omit<User, 'createdAt'>): User {
    const db = getDatabase();
    
    try {
      db.prepare(`
        INSERT INTO users (id, name, avatar)
        VALUES (?, ?, ?)
      `).run(user.id, user.name, user.avatar || null);
    } catch (e: any) {
      if (e.message.includes('UNIQUE constraint failed')) {
        throw new Error('用户ID已存在');
      }
      throw e;
    }

    return this.getById(user.id)!;
  }

  // 获取用户详情
  static getById(id: string): User | null {
    const db = getDatabase();
    const row = db.prepare('SELECT * FROM users WHERE id = ?').get(id) as any;
    if (!row) return null;
    return this.mapRowToUser(row);
  }

  // 获取或创建用户（如果不存在则创建）
  static getOrCreate(id: string, name: string, avatar?: string): User {
    const existing = this.getById(id);
    if (existing) {
      // 如果名称有变化，更新用户信息
      if (existing.name !== name) {
        return this.update(id, { name, avatar })!;
      }
      return existing;
    }
    return this.create({ id, name, avatar });
  }

  // 更新用户信息
  static update(id: string, updates: Partial<Omit<User, 'id' | 'createdAt'>>): User | null {
    const db = getDatabase();
    const fields: string[] = [];
    const values: any[] = [];

    if (updates.name) { fields.push('name = ?'); values.push(updates.name); }
    if (updates.avatar !== undefined) { fields.push('avatar = ?'); values.push(updates.avatar); }
    
    if (fields.length === 0) return this.getById(id);
    
    values.push(id);
    db.prepare(`UPDATE users SET ${fields.join(', ')} WHERE id = ?`).run(...values);
    return this.getById(id);
  }

  // 列出所有用户
  static list(limit: number = 100): User[] {
    const db = getDatabase();
    const rows = db.prepare(`
      SELECT * FROM users ORDER BY created_at DESC LIMIT ?
    `).all(limit) as any[];
    
    return rows.map(this.mapRowToUser);
  }

  // 搜索用户
  static search(query: string): User[] {
    const db = getDatabase();
    const rows = db.prepare(`
      SELECT * FROM users WHERE id LIKE ? OR name LIKE ? ORDER BY created_at DESC
    `).all(`%${query}%`, `%${query}%`) as any[];
    
    return rows.map(this.mapRowToUser);
  }

  // 删除用户
  static delete(id: string): boolean {
    const db = getDatabase();
    const result = db.prepare('DELETE FROM users WHERE id = ?').run(id);
    return result.changes > 0;
  }

  private static mapRowToUser(row: any): User {
    return {
      id: row.id,
      name: row.name,
      avatar: row.avatar,
      createdAt: row.created_at
    };
  }
}
