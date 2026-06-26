import { getDatabase, closeDatabase } from './database';

const CREATE_TABLES_SQL = `
-- 书目表
CREATE TABLE IF NOT EXISTS books (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  author TEXT NOT NULL,
  description TEXT,
  cover_url TEXT,
  tags TEXT DEFAULT '[]',
  category TEXT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 用户表
CREATE TABLE IF NOT EXISTS users (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  avatar TEXT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 读书室表
CREATE TABLE IF NOT EXISTS reading_rooms (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  book_id INTEGER NOT NULL,
  name TEXT NOT NULL,
  description TEXT,
  host_id TEXT NOT NULL,
  max_members INTEGER DEFAULT 10,
  start_time DATETIME,
  end_time DATETIME,
  status TEXT DEFAULT 'pending',
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (book_id) REFERENCES books(id),
  FOREIGN KEY (host_id) REFERENCES users(id)
);

-- 读书室成员表
CREATE TABLE IF NOT EXISTS room_members (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  room_id INTEGER NOT NULL,
  user_id TEXT NOT NULL,
  user_name TEXT NOT NULL,
  joined_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (room_id) REFERENCES reading_rooms(id) ON DELETE CASCADE,
  UNIQUE(room_id, user_id)
);

-- 聊天消息表
CREATE TABLE IF NOT EXISTS chat_messages (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  room_id INTEGER NOT NULL,
  user_id TEXT NOT NULL,
  user_name TEXT NOT NULL,
  content TEXT NOT NULL,
  message_type TEXT DEFAULT 'text',
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (room_id) REFERENCES reading_rooms(id) ON DELETE CASCADE
);

-- 创建索引
CREATE INDEX IF NOT EXISTS idx_books_tags ON books(tags);
CREATE INDEX IF NOT EXISTS idx_books_category ON books(category);
CREATE INDEX IF NOT EXISTS idx_rooms_status ON reading_rooms(status);
CREATE INDEX IF NOT EXISTS idx_rooms_book_id ON reading_rooms(book_id);
CREATE INDEX IF NOT EXISTS idx_messages_room_id ON chat_messages(room_id);
CREATE INDEX IF NOT EXISTS idx_messages_created_at ON chat_messages(created_at);
`;

export function initDatabase(): void {
  const db = getDatabase();
  db.exec(CREATE_TABLES_SQL);
  console.log('数据库初始化完成');
}

// 如果直接运行此文件
if (require.main === module) {
  initDatabase();
  closeDatabase();
}
