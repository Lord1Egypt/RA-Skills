-- 企业微信存档服务数据库初始化脚本
-- 运行此脚本可手动初始化或修复数据库

-- 消息表 - 存储所有消息记录
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    msg_id TEXT UNIQUE NOT NULL,
    msg_type TEXT NOT NULL,
    from_user TEXT NOT NULL,
    to_users TEXT,
    room_id TEXT,
    content TEXT,
    timestamp INTEGER NOT NULL,
    received_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata TEXT,
    
    -- 索引优化查询性能
    INDEX idx_msg_id (msg_id),
    INDEX idx_from_user (from_user),
    INDEX idx_room_id (room_id),
    INDEX idx_timestamp (timestamp),
    INDEX idx_received_time (received_time)
);

-- 附件表 - 存储文件附件信息
CREATE TABLE IF NOT EXISTS attachments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    msg_id TEXT NOT NULL,
    attachment_id TEXT NOT NULL,
    file_name TEXT,
    file_type TEXT,
    file_size INTEGER,
    file_path TEXT,
    download_url TEXT,
    download_status TEXT DEFAULT 'pending',
    download_time TIMESTAMP,
    metadata TEXT,
    
    UNIQUE(msg_id, attachment_id),
    FOREIGN KEY (msg_id) REFERENCES messages(msg_id) ON DELETE CASCADE,
    
    INDEX idx_attachment_id (attachment_id),
    INDEX idx_download_status (download_status)
);

-- 用户表 - 存储用户信息
CREATE TABLE IF NOT EXISTS users (
    user_id TEXT PRIMARY KEY,
    name TEXT,
    avatar TEXT,
    department TEXT,
    position TEXT,
    mobile TEXT,
    email TEXT,
    status INTEGER DEFAULT 1,
    last_seen TIMESTAMP,
    metadata TEXT,
    
    INDEX idx_name (name),
    INDEX idx_department (department)
);

-- 群聊表 - 存储群聊信息
CREATE TABLE IF NOT EXISTS rooms (
    room_id TEXT PRIMARY KEY,
    room_name TEXT,
    creator TEXT,
    create_time INTEGER,
    member_count INTEGER,
    notice TEXT,
    status INTEGER DEFAULT 1,
    metadata TEXT,
    
    INDEX idx_room_name (room_name),
    INDEX idx_creator (creator)
);

-- 群聊成员表 - 存储群聊成员关系
CREATE TABLE IF NOT EXISTS room_members (
    room_id TEXT NOT NULL,
    user_id TEXT NOT NULL,
    join_time INTEGER,
    role INTEGER DEFAULT 0, -- 0:普通成员, 1:管理员, 2:群主
    metadata TEXT,
    
    PRIMARY KEY (room_id, user_id),
    FOREIGN KEY (room_id) REFERENCES rooms(room_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    
    INDEX idx_user_id (user_id),
    INDEX idx_role (role)
);

-- 消息统计表 - 用于分析
CREATE TABLE IF NOT EXISTS message_stats (
    date DATE PRIMARY KEY,
    total_messages INTEGER DEFAULT 0,
    text_messages INTEGER DEFAULT 0,
    image_messages INTEGER DEFAULT 0,
    file_messages INTEGER DEFAULT 0,
    voice_messages INTEGER DEFAULT 0,
    video_messages INTEGER DEFAULT 0,
    active_users INTEGER DEFAULT 0,
    active_rooms INTEGER DEFAULT 0
);

-- 系统日志表 - 记录服务操作
CREATE TABLE IF NOT EXISTS system_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    level TEXT NOT NULL,
    module TEXT NOT NULL,
    message TEXT NOT NULL,
    details TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_level (level),
    INDEX idx_module (module),
    INDEX idx_timestamp (timestamp)
);

-- 回调日志表 - 记录企业微信回调
CREATE TABLE IF NOT EXISTS callback_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    callback_type TEXT NOT NULL, -- 'normal' 或 'archive'
    event_type TEXT,
    msg_id TEXT,
    status TEXT NOT NULL,
    error_message TEXT,
    processing_time_ms INTEGER,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_callback_type (callback_type),
    INDEX idx_event_type (event_type),
    INDEX idx_status (status),
    INDEX idx_timestamp (timestamp)
);

-- 创建视图以便查询
CREATE VIEW IF NOT EXISTS v_message_details AS
SELECT 
    m.*,
    u.name as from_user_name,
    r.room_name,
    COUNT(a.id) as attachment_count
FROM messages m
LEFT JOIN users u ON m.from_user = u.user_id
LEFT JOIN rooms r ON m.room_id = r.room_id
LEFT JOIN attachments a ON m.msg_id = a.msg_id
GROUP BY m.id;

-- 创建每日消息统计视图
CREATE VIEW IF NOT EXISTS v_daily_stats AS
SELECT 
    DATE(received_time) as date,
    COUNT(*) as total_messages,
    COUNT(DISTINCT from_user) as active_users,
    COUNT(DISTINCT room_id) as active_rooms,
    SUM(CASE WHEN msg_type = 'text' THEN 1 ELSE 0 END) as text_messages,
    SUM(CASE WHEN msg_type = 'image' THEN 1 ELSE 0 END) as image_messages,
    SUM(CASE WHEN msg_type = 'file' THEN 1 ELSE 0 END) as file_messages
FROM messages
WHERE room_id IS NOT NULL
GROUP BY DATE(received_time);

-- 插入初始系统日志
INSERT INTO system_logs (level, module, message) VALUES 
('INFO', 'database', '数据库初始化完成'),
('INFO', 'database', '表结构创建成功');

-- 显示创建的表
SELECT '数据库初始化完成，创建的表:' as message;
SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;

-- 显示表结构
SELECT 'messages表结构:' as message;
PRAGMA table_info(messages);

SELECT 'attachments表结构:' as message;
PRAGMA table_info(attachments);

SELECT 'users表结构:' as message;
PRAGMA table_info(users);

SELECT 'rooms表结构:' as message;
PRAGMA table_info(rooms);