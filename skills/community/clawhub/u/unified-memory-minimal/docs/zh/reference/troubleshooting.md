# 故障排除指南

> Unified Memory 常见问题的解决方案。

## 📚 内容

1. [安装问题](#安装问题)
2. [启动问题](#启动问题)
3. [存储问题](#存储问题)
4. [搜索问题](#搜索问题)
5. [向量存储问题](#向量存储问题)
6. [插件问题](#插件问题)
7. [数据恢复](#数据恢复)

## 安装问题

### "command not found: unified-memory"

**原因：** 安装不在 PATH 中

**解决方案：**
```bash
npm install -g unified-memory
export PATH="$(npm root -g)/bin:$PATH"
```

### "Node.js version too old"

**原因：** Node.js 版本 < 18.0.0

**解决方案：**
```bash
nvm install 18
nvm use 18
```

## 启动问题

### "Failed to initialize storage"

**原因：** 无法创建/读取存储目录

**解决方案：**
```bash
mkdir -p ~/.unified-memory
chmod 755 ~/.unified-memory
unified-memory init
```

### "Port already in use"

**原因：** 其他进程使用端口 3851

**解决方案：**
```bash
lsof -i :3851
unified-memory serve --port 3852
```

## 存储问题

### "Memory file corrupted"

**原因：** JSON 文件格式错误

**解决方案：**
```bash
# 从备份恢复
cp ~/.unified-memory/backups/memories-YYYY-MM-DD.json ~/.unified-memory/memories.json
```

### "Disk full"

**原因：** 磁盘空间不足

**解决方案：**
```bash
rm -rf ~/.unified-memory/backups/*
rm -rf ~/.unified-memory/vector.lance
unified-memory init
```

## 搜索问题

### "Search returns no results"

**原因：** 空索引或查询错误

**解决方案：**
```bash
unified-memory list
unified-memory rebuild-index
```

### "Search very slow"

**原因：** 大数据集，无缓存

**解决方案：**
```bash
# 检查 Ollama 是否运行
ollama serve
ollama list
```

## 向量存储问题

### "LanceDB initialization failed"

**原因：** 向量存储损坏

**解决方案：**
```bash
rm -rf ~/.unified-memory/vector.lance
unified-memory init
```

### "Ollama connection failed"

**原因：** Ollama 未运行或无模型

**解决方案：**
```bash
ollama serve
ollama pull nomic-embed-text
```

## 数据恢复

### "Recover from crash"

```bash
unified-memory wal --action list
unified-memory recover
```

### "Restore from backup"

```bash
ls ~/.unified-memory/backups/
cp ~/.unified-memory/backups/memories-YYYY-MM-DD.json ~/.unified-memory/memories.json
```

## 获取帮助

### 调试模式

```bash
UNIFIED_MEMORY_DEBUG=1 unified-memory serve
tail -f ~/.unified-memory/logs/app.log
```

### 健康检查

```bash
unified-memory health
```
