> **Language**: This document is in Chinese only. For English overview, see [README.md](../README.md).
>
> **语言说明**: 本文档仅提供中文版本。英文概述请查看 [README.md](../README.md)。

---
# 并发控制协议 v1.0

> 防止API限流和资源耗尽

---

## 并发限制

### 默认并发数

| 任务类型 | 默认并发 | 环境变量 |
|---------|---------|---------|
| 图片生成 | 30 | `SEEDANCER_IMAGE_CONCURRENCY` |
| 视频生成 | 50 | `SEEDANCER_VIDEO_CONCURRENCY` |
| 视频分析 | 10 | `SEEDANCER_ANALYSIS_CONCURRENCY` |
| 音频生成 | 20 | `SEEDANCER_AUDIO_CONCURRENCY` |

---

## 并发策略

### 1. 令牌桶算法

```javascript
class ConcurrencyLimiter {
  constructor(maxConcurrent) {
    this.maxConcurrent = maxConcurrent;
    this.currentConcurrent = 0;
    this.queue = [];
  }

  async acquire() {
    if (this.currentConcurrent < this.maxConcurrent) {
      this.currentConcurrent++;
      return true;
    }
    
    return new Promise(resolve => {
      this.queue.push(resolve);
    });
  }

  release() {
    this.currentConcurrent--;
    if (this.queue.length > 0) {
      this.currentConcurrent++;
      const next = this.queue.shift();
      next();
    }
  }
}
```

### 2. 批量任务并发

```javascript
async function executeBatch(tasks, limiter) {
  const results = [];
  
  for (const task of tasks) {
    await limiter.acquire();
    
    try {
      const result = await task.execute();
      results.push(result);
    } finally {
      limiter.release();
    }
  }
  
  return results;
}
```

---

## 限流保护

### 1. 指数退避

```javascript
async function retryWithBackoff(fn, maxRetries = 3) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fn();
    } catch (error) {
      if (error.code === 429) { // Rate limit
        const delay = Math.pow(2, i) * 1000; // 1s, 2s, 4s
        await new Promise(resolve => setTimeout(resolve, delay));
      } else {
        throw error;
      }
    }
  }
  throw new Error('Max retries exceeded');
}
```

### 2. 错误处理

- 429 Too Many Requests: 自动重试，指数退避
- 503 Service Unavailable: 自动重试，固定延迟
- 其他错误: 记录日志，继续执行

---

## 实施检查清单

- [ ] 实现并发限制器
- [ ] 实现令牌桶算法
- [ ] 实现批量任务执行
- [ ] 实现指数退避重试
- [ ] 实现错误处理和日志

---

**版本**: v1.0  
**创建时间**: 2026-09-10
