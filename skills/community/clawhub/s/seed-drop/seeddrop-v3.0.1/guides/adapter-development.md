# 平台适配器开发指南

## 开发步骤

### 1. 复制模板

```bash
cp scripts/adapters/_template.ts scripts/adapters/<platform-id>.ts
```

### 2. 实现 PlatformAdapter 接口

```typescript
import type { PlatformAdapter, Credential, Post, ReplyResult, CheckResult, RateLimitInfo } from '../types.js';

export class MyAdapter implements PlatformAdapter {
  readonly platformId = 'my-platform';
  readonly platformName = 'My Platform';

  async search(keyword: string, timeRange: string, credential: Credential, target?: string): Promise<Post[]> { ... }
  async reply(postId: string, content: string, credential: Credential): Promise<ReplyResult> { ... }
  async check(credential: Credential): Promise<CheckResult> { ... }
  rateLimitInfo(): RateLimitInfo { ... }
}
```

### 3. 输出格式

**search 输出**（JSONL，每行一个）：
```json
{"id":"...","url":"...","title":"...","body":"...","author":"...","createdAt":"...","platform":"<id>"}
```

**reply 输出**：
```json
{"success": true, "replyId": "..."}
```

**check 输出**：
```json
{"valid": true, "username": "..."}
```

### 4. 两种实现方式

**有 API 的平台**：使用 `fetch()` 直接调用 API，参考 `reddit.ts`。

**无 API 的平台**：返回 browser 指令，参考 `xiaohongshu.ts`：
```typescript
import { BROWSER_INSTRUCTION_ID, type BrowserInstruction } from '../types.js';

const instruction: BrowserInstruction = {
  mode: 'browser',
  action: 'search',
  steps: [
    { action: 'navigate', url: `https://example.com/search?q=${keyword}` },
    { action: 'wait', selector: '.result-item' },
    { action: 'extract', selector: '.result-item', fields: ['title', 'url'] },
  ],
  cookies: credential.value,
};

return [{ id: BROWSER_INSTRUCTION_ID, url: '', title: '', body: JSON.stringify(instruction), author: '', createdAt: new Date().toISOString(), platform: this.platformId }];
```

### 5. 注册适配器

在 `scripts/adapters/base.ts` 中添加：
```typescript
'my-platform': async () => {
  const { MyAdapter } = await import('./my-platform.js');
  return new MyAdapter();
},
```

### 6. 配套文件

| 文件 | 用途 |
|------|------|
| `templates/reply-<id>.md` | 回复风格指南 |
| `references/safety-rules.md` | 添加频率限制 |
| `references/platform-tos-notes.md` | 添加 ToS 摘要 |

### 7. 测试

```bash
npx tsx scripts/adapters/<platform-id>.ts test
```

### 8. 启用

在 `memory/brand-profile.md` 的 platforms 中添加新平台。
