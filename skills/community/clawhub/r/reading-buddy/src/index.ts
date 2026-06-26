// Reading Buddy - 社交阅读平台
// 主入口文件，导出核心服务

export { BookService } from './services/bookService';
export { RoomService } from './services/roomService';
export { ChatService, chatEvents } from './services/chatService';
export { UserService } from './services/userService';
export { getDatabase, closeDatabase } from './db/database';
export { initDatabase } from './db/init';
export * from './types';

// 版本信息
export const VERSION = '1.0.0';
