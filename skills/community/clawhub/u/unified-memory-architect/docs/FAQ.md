# 常见问题解答

## 基础问题

### Q: 如何查看系统统计？
```bash
node memory/scripts/query.cjs stats
```

### Q: 如何查询特定标签的记忆？
```bash
node memory/scripts/query.cjs tag <标签名> [数量]
```

### Q: 如何导出记忆数据？
```javascript
const { queryByTag } = require('./memory/scripts/query.cjs');
const memories = queryByTag('reflection', 100);
console.log(JSON.stringify(memories, null, 2));
```

## 数据问题

### Q: 数据存储在哪里？
- 原始数据: `memory/raw/`
- 处理后数据: `memory/processed/`
- 导入数据: `memory/import/`
- 归档数据: `memory/archive/`

### Q: 如何备份数据？
```bash
# 备份处理后的数据
cp -r memory/processed/ ./backup/processed/

# 备份索引
cp -r memory/processed/*.json ./backup/
```

### Q: 如何恢复数据？
```bash
# 从备份恢复
cp -r ./backup/processed/* memory/processed/
```

## 查询问题

### Q: 支持哪些查询类型？
1. `tag <tag> [limit]` - 按标签查询
2. `date <date> [limit]` - 按日期查询
3. `sentiment <sent> [limit]` - 按情感查询
4. `search <keyword> [limit]` - 全文搜索
5. `stats` - 统计信息

### Q: 搜索无结果怎么办？
1. 检查拼写是否正确
2. 使用 `stats` 查看可用标签
3. 尝试模糊搜索

### Q: 查询结果太多怎么办？
```bash
# 限制返回数量
node memory/scripts/query.cjs tag reflection 5
```

## 性能问题

### Q: 查询变慢怎么办？
1. 运行 `verify-system.cjs` 检查系统
2. 重建索引: `node enhance-tags.cjs`
3. 清理归档: `node cleanup.cjs`

### Q: 存储空间不足？
1. 运行 `cleanup.cjs` 清理临时文件
2. 检查 `archive/` 目录
3. 清理旧的导入文件

## 集成问题

### Q: 如何集成到其他系统？
```javascript
const query = require('./memory/scripts/query.cjs');

// REST API 包装示例
app.get('/memories/tag/:tag', async (req, res) => {
  const memories = query.queryByTag(req.params.tag, 100);
  res.json(memories);
});
```

### Q: 支持哪些平台？
- Node.js >= 14.0.0
- OpenClaw Agent Platform
- 任何支持 CommonJS 的环境
