# 微信聊天记录快速命令参考

## 常用命令速查

### 查看会话
```bash
# 最近会话
wechat-cli sessions

# 未读消息
wechat-cli unread

# 指定数量
wechat-cli sessions --limit 10
```

### 读取聊天记录
```bash
# 基础用法
wechat-cli history "联系人名称"

# 指定数量
wechat-cli history "联系人名称" --limit 100

# 时间范围
wechat-cli history "联系人名称" --start-time "2026-01-01" --end-time "2026-01-31"

# 仅文本消息
wechat-cli history "联系人名称" --type text

# 仅链接
wechat-cli history "联系人名称" --type link

# 输出为文本格式
wechat-cli history "联系人名称" --format text
```

### 搜索消息
```bash
# 全局搜索
wechat-cli search "关键词"

# 指定聊天搜索
wechat-cli search "关键词" --chat "群名"

# 多聊天搜索
wechat-cli search "关键词" --chat "群A" --chat "群B"

# 时间范围
wechat-cli search "关键词" --start-time "2026-01-01" --end-time "2026-01-31"
```

### 联系人管理
```bash
# 搜索联系人
wechat-cli contacts --query "姓名"

# 联系人详情
wechat-cli contacts --detail "联系人名称"

# 群成员列表
wechat-cli members "群名称"
```

### 统计与分析
```bash
# 聊天统计
wechat-cli stats "群名称"

# 指定时间范围
wechat-cli stats "群名称" --start-time "2026-01-01" --end-time "2026-01-31"
```

### 导出功能
```bash
# 导出为 Markdown
wechat-cli export "联系人名称" --format markdown

# 导出到文件
wechat-cli export "联系人名称" --format txt --output chat.txt

# 导出收藏
wechat-cli favorites
```

### 增量获取
```bash
# 获取新消息（首次运行获取未读，后续仅返回新消息）
wechat-cli new-messages
```

## 消息类型过滤器

| 类型 | 说明 | 用途示例 |
|------|------|---------|
| `text` | 纯文本 | 搜索对话内容 |
| `image` | 图片 | 查找图片分享 |
| `voice` | 语音 | 查找语音消息 |
| `video` | 视频 | 查找视频分享 |
| `link` | 链接 | 查找文章/小程序 |
| `file` | 文件 | 查找文档分享 |
| `location` | 位置 | 查找位置分享 |

## 与 AI 结合使用

### 查看未读消息
```
wechat-cli unread --format text
```

### 搜索待办事项
```
wechat-cli search "需要" --format json | python extract_key_info.py
```

### 导出特定联系人的对话
```
wechat-cli export "老板" --format markdown --output boss_chat.md
```

## 常见问题

### 微信未运行
确保微信已启动后再执行命令

### 权限被拒绝
macOS: 系统设置 → 隐私与安全 → 完整磁盘访问权限 → 添加终端

### 找不到联系人
使用 `wechat-cli sessions` 查看正确的联系人名称（注意群名和备注名）

### 初始化失败
```bash
# macOS
sudo wechat-cli init

# Windows
wechat-cli init
```
