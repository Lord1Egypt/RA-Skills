# 故障排除指南

## 常见问题

### 1. 查询无响应

**症状**: 运行 `query.cjs` 无输出

**可能原因**:
- 数据文件损坏
- 内存不足
- 路径错误

**解决方案**:
```bash
# 1. 检查文件是否存在
ls -la memory/processed/

# 2. 验证系统
node memory/scripts/verify-system.cjs

# 3. 重建索引
node memory/scripts/enhance-tags.cjs
```

### 2. 数据丢失

**症状**: 记忆数据不完整

**可能原因**:
- 归档操作错误
- 导入失败
- 磁盘空间不足

**解决方案**:
```bash
# 1. 检查归档
ls -la memory/archive/

# 2. 从归档恢复
cp memory/archive/2026-04/*.jsonl memory/import/

# 3. 重新导入
node memory/scripts/import-memories.cjs
```

### 3. 索引错误

**症状**: 索引查询结果不正确

**可能原因**:
- 索引文件损坏
- 索引过期
- 数据格式错误

**解决方案**:
```bash
# 1. 删除旧索引
rm memory/processed/index*.json

# 2. 重建索引
node memory/scripts/enhance-tags.cjs

# 3. 验证索引
node memory/scripts/query.cjs stats
```

### 4. 内存溢出

**症状**: 运行脚本时内存不足

**解决方案**:
```bash
# 1. 清理缓存
node memory/scripts/cleanup.cjs

# 2. 分批处理
# 编辑 import-memories.cjs，设置 BATCH_SIZE = 50

# 3. 增加 Node.js 内存
node --max-old-space-size=4096 script.js
```

### 5. 脚本执行失败

**症状**: 脚本报错退出

**解决方案**:
```bash
# 1. 查看错误日志
node memory/scripts/<script>.js 2>&1 | tee error.log

# 2. 检查 Node.js 版本
node --version # 需要 >= 14.0.0

# 3. 重新安装依赖
npm install
```

## 诊断工具

### verify-system.cjs

验证系统完整性：
```bash
node memory/scripts/verify-system.cjs
```

检查项：
- 数据文件存在性
- 索引文件完整性
- 脚本可执行性
- 内存使用情况

### demo.cjs

运行演示：
```bash
node memory/scripts/demo.cjs
```

## 日志位置

- 系统日志: `memory/logs/`
- 错误日志: 控制台输出
- 备份日志: `memory/backups/`

## 联系支持

如问题无法解决：
1. 查看 [Issue Tracker](../../issues)
2. 查看 [Discussions](../../discussions)
3. 联系维护者
