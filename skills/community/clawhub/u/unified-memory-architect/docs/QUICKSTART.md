# 快速开始指南

## 5分钟上手

### 环境要求

- Node.js >= 14.0.0
- npm 或 yarn
- 磁盘空间 >= 100MB

### 安装步骤

```bash
# 1. 克隆项目
git clone https://github.com/your-repo/unified-memory-architect.git
cd unified-memory-architect

# 2. 安装依赖
npm install

# 3. 验证安装
node memory/scripts/verify-system.cjs
```

## 基础使用

### 1. 查询记忆

```bash
# 查看统计
node memory/scripts/query.cjs stats

# 按标签查询（前5个）
node memory/scripts/query.cjs tag reflection 5

# 按日期查询
node memory/scripts/query.cjs date 2026-04-12 3

# 全文搜索
node memory/scripts/query.cjs search "water" 3

# 按情感查询
node memory/scripts/query.cjs sentiment neutral 2
```

### 2. 编程使用

```javascript
// 引入查询模块
const { queryByTag, queryByDate, searchMemories, getStats } = 
  require('./memory/scripts/query.cjs');

// 获取统计
const stats = getStats();
console.log(`总记忆数: ${stats.totalMemories}`);
console.log(`唯一标签: ${stats.uniqueTags}`);
console.log(`唯一实体: ${stats.uniqueEntities}`);

// 按标签查询
const memories = queryByTag('reflection', 10);
memories.forEach(m => console.log(m.content.assistant));

// 按日期查询
const todayMemories = queryByDate('2026-04-13', 5);

// 全文搜索
const results = searchMemories('memory system', 10);
```

## 示例场景

### 场景1: 查找关于"记忆"的梦境

```bash
node memory/scripts/query.cjs tag memory 10
```

### 场景2: 查看某天的所有记忆

```bash
node memory/scripts/query.cjs date 2026-04-12 20
```

### 场景3: 搜索关键词

```bash
node memory/scripts/query.cjs search "mirror" 5
```

### 场景4: 分析情感分布

```bash
node memory/scripts/query.cjs sentiment positive 5
```

## 下一步

- 查看 [用户指南](USER_GUIDE.md) 了解更多功能
- 查看 [API文档](API.md) 了解更多接口
- 查看 [常见问题](FAQ.md) 解决疑问
