#!/usr/bin/env node
import { Command } from 'commander';
import { initDatabase } from './db/init';
import { BookService } from './services/bookService';
import { RoomService } from './services/roomService';
import { ChatService } from './services/chatService';
import { UserService } from './services/userService';
import { RoomStatus, MessageType } from './types';

const program = new Command();

program
  .name('reading-buddy')
  .description('社交阅读平台 - 一起读书、交流心得')
  .version('1.0.0');

// ========== 数据库初始化命令 ==========
program
  .command('init')
  .description('初始化数据库')
  .action(() => {
    initDatabase();
    console.log('✅ 数据库初始化完成');
  });

// ========== 书目管理命令 ==========
const bookCmd = program.command('book').description('书目管理');

bookCmd
  .command('add')
  .description('添加新书目')
  .requiredOption('-t, --title <title>', '书名')
  .requiredOption('-a, --author <author>', '作者')
  .option('-d, --description <desc>', '简介')
  .option('--cover <url>', '封面URL')
  .option('--tags <tags>', '标签，用逗号分隔', '')
  .option('-c, --category <cat>', '分类')
  .action((options) => {
    const tags = options.tags.split(',').filter(Boolean).map((t: string) => t.trim());
    const book = BookService.create({
      title: options.title,
      author: options.author,
      description: options.description || '',
      coverUrl: options.cover,
      tags,
      category: options.category
    });
    console.log('✅ 书目添加成功:');
    console.log(`  ID: ${book.id}`);
    console.log(`  书名: ${book.title}`);
    console.log(`  作者: ${book.author}`);
  });

bookCmd
  .command('list')
  .description('列出书目')
  .option('-l, --limit <n>', '数量限制', '20')
  .option('-o, --offset <n>', '偏移量', '0')
  .action((options) => {
    const books = BookService.list(parseInt(options.limit), parseInt(options.offset));
    console.log(`📚 共找到 ${books.length} 本书:\n`);
    books.forEach(book => {
      console.log(`[${book.id}] ${book.title}`);
      console.log(`   作者: ${book.author}`);
      console.log(`   分类: ${book.category || '未分类'} | 标签: ${book.tags.join(', ') || '无'}`);
      console.log();
    });
  });

bookCmd
  .command('search <query>')
  .description('搜索书目')
  .option('-c, --category <cat>', '按分类筛选')
  .action((query, options) => {
    const books = BookService.search(query, options.category);
    console.log(`🔍 搜索 "${query}" 找到 ${books.length} 本书:\n`);
    books.forEach(book => {
      console.log(`[${book.id}] ${book.title} - ${book.author}`);
    });
  });

bookCmd
  .command('show <id>')
  .description('查看书目详情')
  .action((id) => {
    const book = BookService.getById(parseInt(id));
    if (!book) {
      console.log('❌ 书目不存在');
      return;
    }
    console.log(`\n📖 ${book.title}`);
    console.log(`   作者: ${book.author}`);
    console.log(`   分类: ${book.category || '未分类'}`);
    console.log(`   标签: ${book.tags.join(', ') || '无'}`);
    console.log(`   简介: ${book.description}`);
    console.log(`   创建时间: ${book.createdAt}\n`);
  });

// ========== 读书室管理命令 ==========
const roomCmd = program.command('room').description('读书室管理');

roomCmd
  .command('create')
  .description('创建读书室')
  .requiredOption('-b, --book-id <id>', '书目ID')
  .requiredOption('-n, --name <name>', '房间名称')
  .requiredOption('-u, --user <user>', '用户ID')
  .option('-d, --description <desc>', '房间描述')
  .option('-m, --max-members <n>', '最大人数', '10')
  .option('--start <time>', '开始时间 (ISO格式)')
  .option('--end <time>', '结束时间 (ISO格式)')
  .action((options) => {
    const room = RoomService.create({
      bookId: parseInt(options.bookId),
      name: options.name,
      description: options.description,
      hostId: options.user,
      maxMembers: parseInt(options.maxMembers),
      startTime: options.start || new Date().toISOString(),
      endTime: options.end
    });
    console.log('✅ 读书室创建成功:');
    console.log(`  ID: ${room.id}`);
    console.log(`  名称: ${room.name}`);
    console.log(`  状态: ${room.status}`);
  });

roomCmd
  .command('list')
  .description('列出读书室')
  .option('-s, --status <status>', '状态筛选 (pending/active/ended)')
  .action((options) => {
    const status = options.status as RoomStatus | undefined;
    const rooms = RoomService.list(status);
    console.log(`🏠 共找到 ${rooms.length} 个读书室:\n`);
    rooms.forEach(room => {
      console.log(`[${room.id}] ${room.name}`);
      console.log(`   状态: ${room.status} | 人数上限: ${room.maxMembers}`);
      console.log();
    });
  });

roomCmd
  .command('join <roomId>')
  .description('加入读书室')
  .requiredOption('-u, --user <user>', '用户ID')
  .requiredOption('-n, --name <name>', '用户名')
  .action((roomId, options) => {
    try {
      RoomService.joinRoom(parseInt(roomId), options.user, options.name);
      console.log('✅ 成功加入读书室');
    } catch (e: any) {
      console.log(`❌ ${e.message}`);
    }
  });

roomCmd
  .command('leave <roomId>')
  .description('退出读书室')
  .requiredOption('-u, --user <user>', '用户ID')
  .action((roomId, options) => {
    RoomService.leaveRoom(parseInt(roomId), options.user);
    console.log('✅ 已退出读书室');
  });

roomCmd
  .command('members <roomId>')
  .description('查看成员列表')
  .action((roomId) => {
    const members = RoomService.getMembers(parseInt(roomId));
    console.log(`👥 成员列表 (${members.length}人):\n`);
    members.forEach(m => {
      console.log(`  - ${m.userName} (${m.userId})`);
    });
  });

roomCmd
  .command('start <roomId>')
  .description('开始读书室（仅房主）')
  .requiredOption('-u, --user <user>', '用户ID')
  .action((roomId, options) => {
    try {
      RoomService.startRoom(parseInt(roomId), options.user);
      console.log('✅ 读书室已开始');
    } catch (e: any) {
      console.log(`❌ ${e.message}`);
    }
  });

roomCmd
  .command('end <roomId>')
  .description('结束读书室（仅房主）')
  .requiredOption('-u, --user <user>', '用户ID')
  .action((roomId, options) => {
    try {
      RoomService.endRoom(parseInt(roomId), options.user);
      console.log('✅ 读书室已结束');
    } catch (e: any) {
      console.log(`❌ ${e.message}`);
    }
  });

// ========== 聊天命令 ==========
const chatCmd = program.command('chat').description('聊天功能');

chatCmd
  .command('send <roomId>')
  .description('发送消息')
  .requiredOption('-u, --user <user>', '用户ID')
  .requiredOption('-n, --name <name>', '用户名')
  .requiredOption('-m, --message <text>', '消息内容')
  .action((roomId, options) => {
    const msg = ChatService.sendMessage(
      parseInt(roomId),
      options.user,
      options.name,
      options.message
    );
    console.log('✅ 消息已发送');
  });

chatCmd
  .command('history <roomId>')
  .description('查看聊天记录')
  .option('-l, --limit <n>', '数量限制', '50')
  .action((roomId, options) => {
    const messages = ChatService.getRoomMessages(parseInt(roomId), parseInt(options.limit));
    console.log(`💬 聊天记录 (${messages.length}条):\n`);
    messages.forEach(msg => {
      const type = msg.messageType === MessageType.INSIGHT ? '【心得】' : '';
      console.log(`[${new Date(msg.createdAt).toLocaleTimeString()}] ${msg.userName}${type}:`);
      console.log(`  ${msg.content}\n`);
    });
  });

chatCmd
  .command('insight <roomId>')
  .description('分享心得')
  .requiredOption('-u, --user <user>', '用户ID')
  .requiredOption('-n, --name <name>', '用户名')
  .requiredOption('-c, --content <text>', '心得内容')
  .action((roomId, options) => {
    ChatService.shareInsight(
      parseInt(roomId),
      options.user,
      options.name,
      options.content
    );
    console.log('✅ 心得已分享');
  });

chatCmd
  .command('export <roomId>')
  .description('导出聊天记录')
  .action((roomId) => {
    const content = ChatService.exportChat(parseInt(roomId));
    console.log(content);
  });

// ========== 用户命令 ==========
const userCmd = program.command('user').description('用户管理');

userCmd
  .command('register')
  .description('注册用户')
  .requiredOption('-i, --id <id>', '用户ID')
  .requiredOption('-n, --name <name>', '用户名')
  .option('-a, --avatar <url>', '头像URL')
  .action((options) => {
    try {
      const user = UserService.create({
        id: options.id,
        name: options.name,
        avatar: options.avatar
      });
      console.log('✅ 用户注册成功:');
      console.log(`  ID: ${user.id}`);
      console.log(`  名称: ${user.name}`);
    } catch (e: any) {
      console.log(`❌ ${e.message}`);
    }
  });

userCmd
  .command('show <id>')
  .description('查看用户信息')
  .action((id) => {
    const user = UserService.getById(id);
    if (!user) {
      console.log('❌ 用户不存在');
      return;
    }
    console.log(`\n👤 ${user.name}`);
    console.log(`   ID: ${user.id}`);
    console.log(`   注册时间: ${user.createdAt}\n`);
  });

// 解析命令行参数
program.parse();
