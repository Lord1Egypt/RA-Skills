# Agent Marketplace

Agent 市场系统，用于技能发现、评分、版本管理和交易。

## 功能特性

### 1. 技能目录
- 技能列表/搜索
- 分类标签
- 版本管理
- 依赖解析

### 2. 评分系统
- 用户评分
- 使用统计
- 质量指标
- 排行榜

### 3. 技能管理
- 发布/更新
- 下架/删除
- 版本控制
- 兼容性检查

### 4. 发现推荐
- 热门技能
- 个性化推荐
- 相关技能
- 新技能展示

### 5. 安装管理
- 一键安装
- 依赖自动解析
- 冲突检测
- 回滚支持

## 安装

```bash
npm install
```

## 使用方法

### 基础用法

```javascript
const { Marketplace } = require('./src');

// 创建市场实例
const marketplace = new Marketplace({
  registry: 'https://clawhub.com/registry',
  cacheDir: './.marketplace-cache'
});

// 搜索技能
const results = await marketplace.search({
  query: 'rag',
  category: 'data-processing',
  sort: 'rating'
});

// 获取技能详情
const skill = await marketplace.getSkill('yuyonghao-rag-retriever');
console.log(skill);

// 安装技能
await marketplace.install('yuyonghao-rag-retriever', { version: '0.1.0' });

// 评分
await marketplace.rate('yuyonghao-rag-retriever', {
  rating: 5,
  comment: 'Excellent skill for RAG!'
});
```

### 搜索技能

```javascript
// 基础搜索
const results = await marketplace.search({ query: 'rag' });

// 高级搜索
const results = await marketplace.search({
  query: 'retriever',
  category: 'data-processing',
  tags: ['rag', 'search'],
  minRating: 4.0,
  sort: 'downloads',
  limit: 10
});
```

### 获取排行榜

```javascript
// 热门技能
const trending = await marketplace.getTrending({ limit: 10 });

// 最高评分
const topRated = await marketplace.getTopRated({ limit: 10 });

// 新技能
const newest = await marketplace.getNewest({ limit: 10 });
```

### 版本管理

```javascript
// 获取所有版本
const versions = await marketplace.getVersions('yuyonghao-rag-retriever');

// 检查兼容性
const compatible = await marketplace.checkCompatibility(
  'yuyonghao-rag-retriever',
  '0.1.0'
);

// 解析依赖
const deps = await marketplace.resolveDependencies({
  'yuyonghao-rag-retriever': '0.1.0'
});
```

## API 参考

### Marketplace

#### Constructor
```javascript
new Marketplace(options)
```

Options:
- `registry`: 注册表 URL
- `cacheDir`: 缓存目录
- `timeout`: 请求超时

#### Methods
- `search(options)`: 搜索技能
- `getSkill(id)`: 获取技能详情
- `install(id, options)`: 安装技能
- `uninstall(id)`: 卸载技能
- `rate(id, rating)`: 评分
- `getTrending(options)`: 获取热门技能
- `getTopRated(options)`: 获取高评分技能

## 测试

```bash
npm test
```

## 配置选项

```javascript
{
  registry: 'https://clawhub.com/registry',
  cacheDir: './.marketplace-cache',
  timeout: 30000,
  retryAttempts: 3,
  cacheExpiry: 3600000  // 1 hour
}
```

## License

MIT
