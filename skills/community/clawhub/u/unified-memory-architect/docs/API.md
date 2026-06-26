# API接口文档

## 查询接口

### queryByTag(tag, limit)

按标签查询记忆。

**参数**:
- `tag` (string): 标签名称
- `limit` (number): 返回数量限制

**返回值**: Array<Memory>

**示例**:
```javascript
const memories = queryByTag('reflection', 10);
```

### queryByDate(date, limit)

按日期查询记忆。

**参数**:
- `date` (string): 日期，格式 YYYY-MM-DD
- `limit` (number): 返回数量限制

**返回值**: Array<Memory>

**示例**:
```javascript
const memories = queryByDate('2026-04-12', 5);
```

### searchMemories(keyword, limit)

全文搜索记忆。

**参数**:
- `keyword` (string): 搜索关键词
- `limit` (number): 返回数量限制

**返回值**: Array<SearchResult>

**示例**:
```javascript
const results = searchMemories('water mirror', 10);
```

### queryBySentiment(sentiment, limit)

按情感查询记忆。

**参数**:
- `sentiment` (string): 情感类型 (neutral/positive/negative)
- `limit` (number): 返回数量限制

**返回值**: Array<Memory>

**示例**:
```javascript
const memories = queryBySentiment('positive', 5);
```

### getStats()

获取系统统计信息。

**返回值**: Stats

**示例**:
```javascript
const stats = getStats();
// { totalMemories: 1760, uniqueTags: 49, uniqueEntities: 181, ... }
```

## 数据类型

### Memory

```typescript
interface Memory {
  id: string;
  type: 'dream' | 'reflection' | 'event' | 'memory';
  timestamp: string;
  source: {
    file: string;
    session: string;
    userLine: string;
    assistantLine: string;
  };
  content: {
    user: string;
    assistant: string;
    language: 'zh' | 'en';
    format: 'markdown' | 'text';
  };
  metadata: {
    confidence: number;
    tags: string[];
    entities: string[];
    sentiment: 'neutral' | 'positive' | 'negative';
    wordCount: {
      user: number;
      assistant: number;
      total: number;
    };
  };
  attribution: {
    agent: string;
    channel: string;
    user: string;
  };
  date: string;
  analysis: {
    hasReflection: boolean;
    hasWaterImagery: boolean;
    hasMemoryTheme: boolean;
    isTechnical: boolean;
  };
}
```

### Stats

```typescript
interface Stats {
  totalMemories: number;
  uniqueTags: number;
  uniqueEntities: number;
  byType: Record<string, number>;
  byDate: Record<string, number>;
  byTag: Record<string, number>;
  bySentiment: Record<string, number>;
  byLanguage: Record<string, number>;
}
```

### SearchResult

```typescript
interface SearchResult {
  memory: Memory;
  score: number;
  matches: string[];
}
```

## CLI接口

```bash
node query.cjs <command> [args]

Commands:
  tag <tag> [limit]       按标签查询
  date <date> [limit]      按日期查询
  sentiment <sent> [limit] 按情感查询
  search <keyword> [limit] 全文搜索
  stats                    显示统计
  help                     显示帮助
```
