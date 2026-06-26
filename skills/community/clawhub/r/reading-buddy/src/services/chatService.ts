import { getDatabase } from '../db/database';
import { ChatMessage, MessageType } from '../types';
import EventEmitter from 'events';

// 聊天事件发射器，用于实时消息通知
export const chatEvents = new EventEmitter();

export class ChatService {
  // 发送消息
  static sendMessage(
    roomId: number,
    userId: string,
    userName: string,
    content: string,
    messageType: MessageType = MessageType.TEXT
  ): ChatMessage {
    const db = getDatabase();
    
    const result = db.prepare(`
      INSERT INTO chat_messages (room_id, user_id, user_name, content, message_type)
      VALUES (?, ?, ?, ?, ?)
    `).run(roomId, userId, userName, content, messageType);

    const message = this.getById(result.lastInsertRowid as number)!;
    
    // 触发消息事件，用于实时通知
    chatEvents.emit('message', { roomId, message });
    
    return message;
  }

  // 获取消息详情
  static getById(id: number): ChatMessage | null {
    const db = getDatabase();
    const row = db.prepare('SELECT * FROM chat_messages WHERE id = ?').get(id) as any;
    if (!row) return null;
    return this.mapRowToMessage(row);
  }

  // 获取房间消息历史
  static getRoomMessages(
    roomId: number,
    limit: number = 100,
    beforeId?: number
  ): ChatMessage[] {
    const db = getDatabase();
    let sql = 'SELECT * FROM chat_messages WHERE room_id = ?';
    const params: any[] = [roomId];
    
    if (beforeId) {
      sql += ' AND id < ?';
      params.push(beforeId);
    }
    
    sql += ' ORDER BY created_at DESC LIMIT ?';
    params.push(limit);
    
    const rows = db.prepare(sql).all(...params) as any[];
    return rows.map(this.mapRowToMessage).reverse(); // 按时间正序返回
  }

  // 获取最新消息
  static getLatestMessages(roomId: number, limit: number = 50): ChatMessage[] {
    const db = getDatabase();
    const rows = db.prepare(`
      SELECT * FROM chat_messages 
      WHERE room_id = ? 
      ORDER BY created_at DESC 
      LIMIT ?
    `).all(roomId, limit) as any[];
    
    return rows.map(this.mapRowToMessage).reverse();
  }

  // 分享心得
  static shareInsight(
    roomId: number,
    userId: string,
    userName: string,
    content: string
  ): ChatMessage {
    return this.sendMessage(roomId, userId, userName, content, MessageType.INSIGHT);
  }

  // 获取房间的心得分享
  static getRoomInsights(roomId: number, limit: number = 50): ChatMessage[] {
    const db = getDatabase();
    const rows = db.prepare(`
      SELECT * FROM chat_messages 
      WHERE room_id = ? AND message_type = ?
      ORDER BY created_at DESC 
      LIMIT ?
    `).all(roomId, MessageType.INSIGHT, limit) as any[];
    
    return rows.map(this.mapRowToMessage);
  }

  // 搜索消息
  static searchMessages(roomId: number, query: string): ChatMessage[] {
    const db = getDatabase();
    const rows = db.prepare(`
      SELECT * FROM chat_messages 
      WHERE room_id = ? AND content LIKE ?
      ORDER BY created_at DESC
    `).all(roomId, `%${query}%`) as any[];
    
    return rows.map(this.mapRowToMessage);
  }

  // 删除消息
  static deleteMessage(messageId: number, userId: string): boolean {
    const db = getDatabase();
    const message = this.getById(messageId);
    if (!message) throw new Error('消息不存在');
    if (message.userId !== userId) throw new Error('只能删除自己的消息');
    
    const result = db.prepare('DELETE FROM chat_messages WHERE id = ?').run(messageId);
    return result.changes > 0;
  }

  // 获取用户发送的消息统计
  static getUserStats(roomId: number, userId: string): {
    totalMessages: number;
    insights: number;
  } {
    const db = getDatabase();
    
    const totalResult = db.prepare(`
      SELECT COUNT(*) as count FROM chat_messages 
      WHERE room_id = ? AND user_id = ?
    `).get(roomId, userId) as any;
    
    const insightResult = db.prepare(`
      SELECT COUNT(*) as count FROM chat_messages 
      WHERE room_id = ? AND user_id = ? AND message_type = ?
    `).get(roomId, userId, MessageType.INSIGHT) as any;
    
    return {
      totalMessages: totalResult.count,
      insights: insightResult.count
    };
  }

  // 导出聊天记录
  static exportChat(roomId: number): string {
    const messages = this.getRoomMessages(roomId, 10000);
    
    let markdown = `# 读书室聊天记录\n\n`;
    markdown += `导出时间: ${new Date().toLocaleString()}\n\n`;
    markdown += `---\n\n`;
    
    for (const msg of messages) {
      const typeLabel = msg.messageType === MessageType.INSIGHT ? '【心得】' : '';
      markdown += `**${msg.userName}** ${typeLabel} (${new Date(msg.createdAt).toLocaleString()})\n\n`;
      markdown += `${msg.content}\n\n`;
      markdown += `---\n\n`;
    }
    
    return markdown;
  }

  private static mapRowToMessage(row: any): ChatMessage {
    return {
      id: row.id,
      roomId: row.room_id,
      userId: row.user_id,
      userName: row.user_name,
      content: row.content,
      messageType: row.message_type as MessageType,
      createdAt: row.created_at
    };
  }
}
