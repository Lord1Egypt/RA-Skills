# Reading Buddy - 社交阅读平台

一个让用户一起读书、交流心得的社交阅读平台。

## 功能特性

### 1. 书目注册中心
- 发布书目（书名、作者、简介、封面、标签、分类）
- 浏览书目列表
- 搜索书目（按标题、作者、简介）
- 按标签/分类筛选

### 2. 虚拟读书室
- 创建读书室（选择书目、设置开放时间、人数上限）
- 加入/退出读书室
- 读书室列表/搜索
- 房间状态管理（未开始、进行中、已结束）

### 3. 读书交流
- 实时聊天（文字消息）
- 心得分享（特殊消息类型）
- 聊天记录保存与导出

## 安装

```bash
cd ~/.openclaw/workspace/skills/reading-buddy
npm install
npm run build
```

## 初始化数据库

```bash
npm run init-db
# 或
reading-buddy init
```

## CLI 命令

### 书目管理
```bash
# 添加书目
reading-buddy book add -t "书名" -a "作者" -d "简介" --tags "标签1,标签2" -c "分类"

# 列出书目
reading-buddy book list

# 搜索书目
reading-buddy book search "关键词"

# 查看书目详情
reading-buddy book show <id>
```

### 读书室管理
```bash
# 创建读书室
reading-buddy room create -b <bookId> -n "房间名" -u <userId>

# 列出读书室
reading-buddy room list
reading-buddy room list -s active

# 加入读书室
reading-buddy room join <roomId> -u <userId> -n "用户名"

# 退出读书室
reading-buddy room leave <roomId> -u <userId>

# 查看成员
reading-buddy room members <roomId>

# 开始/结束读书室（仅房主）
reading-buddy room start <roomId> -u <userId>
reading-buddy room end <roomId> -u <userId>
```

### 聊天功能
```bash
# 发送消息
reading-buddy chat send <roomId> -u <userId> -n "用户名" -m "消息内容"

# 查看聊天记录
reading-buddy chat history <roomId>

# 分享心得
reading-buddy chat insight <roomId> -u <userId> -n "用户名" -c "心得内容"

# 导出聊天记录
reading-buddy chat export <roomId>
```

### 用户管理
```bash
# 注册用户
reading-buddy user register -i <userId> -n "用户名"

# 查看用户信息
reading-buddy user show <userId>
```

## 技术栈

- **运行时**: Node.js + TypeScript
- **数据库**: SQLite (better-sqlite3)
- **CLI**: Commander.js
- **实时通信**: EventEmitter (可扩展为 WebSocket)

## 数据存储

数据库文件位于: `~/.reading-buddy/reading-buddy.db`

## API 使用

```typescript
import { BookService, RoomService, ChatService, UserService } from 'reading-buddy';

// 书目操作
const book = BookService.create({ title: '...', author: '...', ... });
const books = BookService.list();

// 读书室操作
const room = RoomService.create({ bookId: 1, name: '...', ... });
RoomService.joinRoom(roomId, userId, userName);

// 聊天操作
ChatService.sendMessage(roomId, userId, userName, 'Hello!');
ChatService.shareInsight(roomId, userId, userName, '我的读书心得...');
```

## 项目结构

```
reading-buddy/
├── src/
│   ├── cli.ts              # CLI 入口
│   ├── index.ts            # 库入口
│   ├── types.ts            # 类型定义
│   ├── db/
│   │   ├── database.ts     # 数据库连接
│   │   └── init.ts         # 初始化脚本
│   └── services/
│       ├── bookService.ts  # 书目服务
│       ├── roomService.ts  # 读书室服务
│       ├── chatService.ts  # 聊天服务
│       └── userService.ts  # 用户服务
├── package.json
├── tsconfig.json
└── SKILL.md
```
