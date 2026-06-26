# 升级指南

## 版本升级

### 从 v0.x 升级到 v1.0.0

#### 主要变更

1. **目录结构变更**
   - 旧: `memory/dreams/`
   - 新: `memory/` (7层结构)

2. **数据格式变更**
   - 旧: 混合格式 (txt, json, jsonl)
   - 新: 统一 JSONL 格式

3. **API 变更**
   - 新增: `queryBySentiment()`
   - 新增: `searchMemories()`
   - 变更: `getStats()` 返回新字段

#### 升级步骤

```bash
# 1. 备份当前数据
cp -r memory memory.backup

# 2. 拉取新版本
git pull

# 3. 运行迁移脚本
node memory/scripts/migrate-simple.cjs

# 4. 增强标签
node memory/scripts/enhance-tags.cjs

# 5. 验证
node memory/scripts/verify-system.cjs

# 6. 测试查询
node memory/scripts/query.cjs stats
```

#### 回滚

```bash
# 如有问题，回滚
rm -rf memory
cp -r memory.backup memory
```

## 兼容性

### 向后兼容

- v1.0.0 完全向后兼容
- 旧数据自动迁移
- API 接口保持不变

### 依赖要求

- Node.js >= 14.0.0
- OpenClaw >= 2.7.0 (可选)

## 下一步

- 查看 [变更日志](CHANGELOG.md)
- 查看 [快速开始](QUICKSTART.md)
- 体验新功能
