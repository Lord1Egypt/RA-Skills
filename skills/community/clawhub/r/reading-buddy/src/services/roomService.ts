import { getDatabase } from '../db/database';
import { ReadingRoom, RoomMember, RoomStatus } from '../types';

export class RoomService {
  // 创建读书室
  static create(room: Omit<ReadingRoom, 'id' | 'createdAt' | 'status'>): ReadingRoom {
    const db = getDatabase();
    
    const result = db.prepare(`
      INSERT INTO reading_rooms (book_id, name, description, host_id, max_members, start_time, end_time, status)
      VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    `).run(
      room.bookId,
      room.name,
      room.description || null,
      room.hostId,
      room.maxMembers,
      room.startTime,
      room.endTime || null,
      RoomStatus.PENDING
    );

    // 自动将创建者加入房间
    db.prepare(`
      INSERT INTO room_members (room_id, user_id, user_name)
      VALUES (?, ?, ?)
    `).run(result.lastInsertRowid, room.hostId, room.hostId); // 临时用id作为name

    return this.getById(result.lastInsertRowid as number)!;
  }

  // 获取读书室详情
  static getById(id: number): ReadingRoom | null {
    const db = getDatabase();
    const row = db.prepare('SELECT * FROM reading_rooms WHERE id = ?').get(id) as any;
    if (!row) return null;
    return this.mapRowToRoom(row);
  }

  // 获取读书室列表
  static list(status?: RoomStatus, limit: number = 50, offset: number = 0): ReadingRoom[] {
    const db = getDatabase();
    let sql = 'SELECT * FROM reading_rooms';
    const params: any[] = [];
    
    if (status) {
      sql += ' WHERE status = ?';
      params.push(status);
    }
    
    sql += ' ORDER BY created_at DESC LIMIT ? OFFSET ?';
    params.push(limit, offset);
    
    const rows = db.prepare(sql).all(...params) as any[];
    return rows.map(this.mapRowToRoom);
  }

  // 搜索读书室
  static search(query: string): ReadingRoom[] {
    const db = getDatabase();
    const rows = db.prepare(`
      SELECT r.* FROM reading_rooms r
      JOIN books b ON r.book_id = b.id
      WHERE r.name LIKE ? OR b.title LIKE ? OR b.author LIKE ?
      ORDER BY r.created_at DESC
    `).all(`%${query}%`, `%${query}%`, `%${query}%`) as any[];
    
    return rows.map(this.mapRowToRoom);
  }

  // 加入读书室
  static joinRoom(roomId: number, userId: string, userName: string): boolean {
    const db = getDatabase();
    
    // 检查房间是否存在且未满
    const room = this.getById(roomId);
    if (!room) throw new Error('读书室不存在');
    if (room.status === RoomStatus.ENDED) throw new Error('读书室已结束');
    
    const memberCount = this.getMemberCount(roomId);
    if (memberCount >= room.maxMembers) throw new Error('读书室已满员');

    try {
      db.prepare(`
        INSERT INTO room_members (room_id, user_id, user_name)
        VALUES (?, ?, ?)
      `).run(roomId, userId, userName);
      return true;
    } catch (e: any) {
      if (e.message.includes('UNIQUE constraint failed')) {
        throw new Error('您已在该读书室中');
      }
      throw e;
    }
  }

  // 退出读书室
  static leaveRoom(roomId: number, userId: string): boolean {
    const db = getDatabase();
    const result = db.prepare(`
      DELETE FROM room_members WHERE room_id = ? AND user_id = ?
    `).run(roomId, userId);
    return result.changes > 0;
  }

  // 获取成员列表
  static getMembers(roomId: number): RoomMember[] {
    const db = getDatabase();
    const rows = db.prepare(`
      SELECT * FROM room_members WHERE room_id = ? ORDER BY joined_at
    `).all(roomId) as any[];
    
    return rows.map(row => ({
      id: row.id,
      roomId: row.room_id,
      userId: row.user_id,
      userName: row.user_name,
      joinedAt: row.joined_at
    }));
  }

  // 获取成员数量
  static getMemberCount(roomId: number): number {
    const db = getDatabase();
    const result = db.prepare(`
      SELECT COUNT(*) as count FROM room_members WHERE room_id = ?
    `).get(roomId) as any;
    return result.count;
  }

  // 更新房间状态
  static updateStatus(roomId: number, status: RoomStatus): boolean {
    const db = getDatabase();
    const result = db.prepare(`
      UPDATE reading_rooms SET status = ? WHERE id = ?
    `).run(status, roomId);
    return result.changes > 0;
  }

  // 开始读书室
  static startRoom(roomId: number, hostId: string): boolean {
    const db = getDatabase();
    const room = this.getById(roomId);
    if (!room) throw new Error('读书室不存在');
    if (room.hostId !== hostId) throw new Error('只有房主可以开始读书室');
    if (room.status !== RoomStatus.PENDING) throw new Error('读书室已开始或已结束');
    
    return this.updateStatus(roomId, RoomStatus.ACTIVE);
  }

  // 结束读书室
  static endRoom(roomId: number, hostId: string): boolean {
    const db = getDatabase();
    const room = this.getById(roomId);
    if (!room) throw new Error('读书室不存在');
    if (room.hostId !== hostId) throw new Error('只有房主可以结束读书室');
    if (room.status === RoomStatus.ENDED) throw new Error('读书室已结束');
    
    return this.updateStatus(roomId, RoomStatus.ENDED);
  }

  // 获取用户的读书室
  static getUserRooms(userId: string): ReadingRoom[] {
    const db = getDatabase();
    const rows = db.prepare(`
      SELECT r.* FROM reading_rooms r
      JOIN room_members m ON r.id = m.room_id
      WHERE m.user_id = ?
      ORDER BY r.created_at DESC
    `).all(userId) as any[];
    
    return rows.map(this.mapRowToRoom);
  }

  // 删除读书室
  static delete(roomId: number, hostId: string): boolean {
    const db = getDatabase();
    const room = this.getById(roomId);
    if (!room) throw new Error('读书室不存在');
    if (room.hostId !== hostId) throw new Error('只有房主可以删除读书室');
    
    const result = db.prepare('DELETE FROM reading_rooms WHERE id = ?').run(roomId);
    return result.changes > 0;
  }

  private static mapRowToRoom(row: any): ReadingRoom {
    return {
      id: row.id,
      bookId: row.book_id,
      name: row.name,
      description: row.description,
      hostId: row.host_id,
      maxMembers: row.max_members,
      startTime: row.start_time,
      endTime: row.end_time,
      status: row.status as RoomStatus,
      createdAt: row.created_at
    };
  }
}
