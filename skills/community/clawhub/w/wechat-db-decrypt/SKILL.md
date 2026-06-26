# wechat-db-decrypt - 微信数据库解密与消息提取

> 适用版本：微信 PC 3.x / 4.x 新架构（WeChatAppEx.exe），xwechat_files 格式
> 前提：微信已正常登录，数据库已通过 WeChatMsg.exe 或类似工具解密到 `db_storage_decrypted`

## 快速开始

### 已解密数据库路径
```
C:\Users\<用户名>\Documents\xwechat_files\<wxid>\db_storage_decrypted\
```

### 读取消息示例（Python）
```python
import sqlite3, os, datetime

decrypted_dir = r"C:\Users\<用户名>\Documents\xwechat_files\<wxid>\db_storage_decrypted"

# 连接消息数据库
msg_db = os.path.join(decrypted_dir, "message", "message_0.db")
conn = sqlite3.connect(msg_db)
cursor = conn.cursor()

# 获取所有消息表
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [r[0] for r in cursor.fetchall()]
msg_tables = [t for t in tables if t.startswith('Msg_')]

# 搜索关键词消息
for tbl in msg_tables:
    try:
        cursor.execute(f"SELECT message_content, create_time FROM {tbl} WHERE message_content LIKE ? LIMIT 10", ('%程序员%',))
        rows = cursor.fetchall()
        for content, ctime in rows:
            dt = datetime.datetime.fromtimestamp(ctime)
            print(f"[{dt}] {content[:100]}")
    except:
        pass

conn.close()
```

---

## 数据库结构解析

### 目录结构
```
<wxid>\
├── db_storage\          # 加密数据库（需密钥）
├── db_storage_decrypted\# 解密后的数据库 ← 主要操作这个
│   ├── contact\         # 联系人表
│   │   └── contact.db  # 包含 contact, chatroom_member 等表
│   ├── message\         # 消息表（按时间段分库）
│   │   ├── message_0.db  # 消息库1（~8MB）
│   │   ├── message_1.db  # 消息库2（~52MB）
│   │   └── message_2.db  # 消息库3（~43MB）
│   └── session\         # 会话列表
│       └── session.db   # SessionTable 等
└── config\              # 账号配置
```

### contact.db 表结构
```sql
contact:       username, nick_name, remark, type 等
chat_room:     群聊基础信息
chatroom_member: 群成员列表 (member_id, member_nick, chatroom_id)
```

### message_N.db 表结构
```sql
Msg_<hash>:    消息表（每个表对应一个聊天对象/群）
  - local_id:      本地消息ID
  - server_id:     服务器消息ID
  - create_time:   时间戳（秒）
  - real_sender_id: 发送者
  - message_content: 消息内容（二进制/文本）
  - source:        消息来源

TimeStamp:     时间戳表
Name2Id:       ID映射表（wxid <-> 数据库表名）
```

### 表名规律
- 消息表名是加密的 hash：`Msg_<32位hex>`
- 群ID格式：`<数字>@chatroom`
- 单人会话：`wxid_<随机字符串>`

---

## 关键操作步骤

### Step 1: 找到群的 chatroom_id
```python
# 在 contact.db 的 contact 表中搜索群名
conn = sqlite3.connect(os.path.join(decrypted_dir, "contact", "contact.db"))
cursor = conn.cursor()
cursor.execute("SELECT username, nick_name FROM contact WHERE nick_name LIKE '%程序员客栈%'")
rows = cursor.fetchall()
# 得到: ('34907532207@chatroom', '程序员客栈91群')
conn.close()
```

### Step 2: 搜索群消息
```python
# WCDB 加密表名中没有明显的群标识，需要在所有 Msg 表中搜索内容
keywords = ['开题', '报告', '开发', '报价', '项目', '需求', '接单']

for tbl in msg_tables:
    for kw in keywords:
        cursor.execute(f"SELECT message_content, create_time FROM {tbl} WHERE message_content LIKE ?", (f'%{kw}%',))
        rows = cursor.fetchall()
        # 处理结果...
```

### Step 3: 解析 message_content 二进制
```python
# message_content 是 protobuf 或二进制编码，需要解码
content_bytes = row[0]
if content_bytes:
    text = content_bytes.decode('utf-8', errors='replace')
    # 通常是 XML 格式: <msg><appmsg>...
    # 或直接是文本
```

### Step 4: 导出需求数据
```python
# 按时间段统计需求类型
results = []
for tbl in msg_tables:
    cursor.execute(f"SELECT message_content, create_time FROM {tbl} WHERE message_content LIKE '%报价%' OR message_content LIKE '%需求%'")
    for content, ctime in cursor.fetchall():
        if content:
            dt = datetime.datetime.fromtimestamp(ctime)
            results.append({'time': dt, 'content': str(content)[:200]})
```

---

## 解密状态判断

### 已解密
- `db_storage_decrypted` 目录存在且包含 `.db` 文件
- sqlite3 可直接打开，Tables 有 `Msg_` 前缀
- HMAC 验证：数据库文件头不是 `SQLite format 3`（加密头）

### 未解密
- `db_storage` 中 `.db` 文件 sqlite3 打开报错：`file is not a database`
- `.material` 文件存在（加密分片）

### 解决方案（未解密时）

**方案A：下载 WeChatMsg.exe**
1. https://memotrace.lc044.love/ 或夸克网盘
2. 下载编译好的 exe，直接运行
3. 它会自动找到微信进程、提取密钥、解密数据库

**方案B：修复 pywxdump**
```python
# 如果是 WeChatAppEx.exe 进程名问题，修改 pywxdump 源码
site_pkg = r"C:\Users\<用户名>\AppData\Local\Programs\Python\Python312\Lib\site-packages\pywxdump"

# 修改 PROCESS_NAMES
with open(f"{site_pkg}\\wx_core\\wx_info.py", 'r') as f:
    content = f.read()
content = content.replace(
    'if name == "WeChat.exe"',
    'if name in ["WeChatAppEx.exe", "WeChat.exe"]'
)
with open(f"{site_pkg}\\wx_core\\wx_info.py", 'w') as f:
    f.write(content)
```

**方案C：手动内存扫描（进阶）**
1. 附加 pymem 到 WeChatAppEx.exe
2. 搜索 android/iphone string 附近的高熵数据
3. 用 HMAC 验证候选密钥
4. 参考 `simple_key_scan.py` / `pymem_key_scan.py` 脚本

---

## 已知问题

### 微信版本太新（2.4.1.19433）
- `pywxdump` 和 `WeChatMsg` 源码不支持
- 解决：用编译好的 exe（已更新版本）

### android string 在 flue.dll 而非 xweb_elf.dll
- 密钥不在 xweb_elf.dll 中
- `flue.dll`（209MB）里的 android string 是音频引擎的协议数据，不是密钥附近

### pymem pattern_scan_module 在大模块上失败
- 某些模块内存不可读，跳过即可
- 用 `read_bytes` 分段读取更稳定

---

## 相关文件

| 文件 | 说明 |
|------|------|
| `read_decrypted_db.py` | 读取已解密数据库示例 |
| `search_group_messages.py` | 搜索群消息示例 |
| `full_msg_search.py` | 全库关键词搜索 |
| `sqlite_mem_scan.py` | 内存中搜索 SQLite 明文 |
| `pymem_key_scan.py` | pymem 内存扫描找密钥 |

---

## 使用场景

- 微信群需求分析（程序员客栈91群等）
- 聊天记录导出备份
- 对手情报收集（竞品动态）
- 客户需求挖掘（AI接单方向选择）

> 安全提醒：仅用于个人数据备份和本人合法用途，禁止非法采集他人信息。