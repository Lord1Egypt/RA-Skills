# Viking Memory System Ultra - 使用说明

## 角色
你是一个具备分层记忆管理能力的助手。当用户需要写入、读取、搜索记忆时，使用 Viking 记忆系统。

## 核心功能
1. **分层记忆**: hot → warm → cold → archive
2. **动态回流**: 语义相似度驱动的冷记忆自动晋升
3. **智能权重**: 对数增长 + 上下文相关性
4. **可逆归档**: 多粒度摘要 + 按需解压

## 使用方法
```bash
# 写入记忆
sv_write "agent/memories/hot/test.md" "# 内容" --importance high

# 读取记忆
sv_read "agent/memories/hot/test.md"

# 搜索记忆
sv_find "关键词" --layer hot

# 自动加载
sv_autoload.sh --promote
```

## 注意事项
1. 确保 VIKING_HOME 和 SV_WORKSPACE 环境变量已设置
2. 重要记忆标记 importance: high 可避免被自动压缩
3. 归档层记忆可用 sv_decompress.sh 恢复
