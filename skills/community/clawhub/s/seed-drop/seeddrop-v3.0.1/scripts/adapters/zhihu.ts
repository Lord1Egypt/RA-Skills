// SECURITY MANIFEST:
//   Environment variables accessed: none
//   External endpoints called: https://www.zhihu.com/api/v4
//   Local files read: none
//   Local files written: none

import type {
  PlatformAdapter,
  Credential,
  Post,
  ReplyResult,
  CheckResult,
  RateLimitInfo,
  BrowserInstruction,
} from '../types.js';
import { BROWSER_INSTRUCTION_ID } from '../types.js';

const ZHIHU_API = 'https://www.zhihu.com/api/v4';

function buildHeaders(credential: Credential): Record<string, string> {
  return {
    'Cookie': credential.value,
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Referer': 'https://www.zhihu.com',
  };
}

export class ZhihuAdapter implements PlatformAdapter {
  readonly platformId = 'zhihu';
  readonly platformName = '知乎';

  async search(
    keyword: string,
    _timeRange: string,
    credential: Credential,
    _target?: string,
  ): Promise<Post[]> {
    try {
      const params = new URLSearchParams({
        t: 'general',
        q: keyword,
        correction: '1',
        offset: '0',
        limit: '20',
      });

      const response = await fetch(`${ZHIHU_API}/search_v3?${params}`, {
        headers: buildHeaders(credential),
      });

      if (!response.ok) {
        console.error(`[zhihu] Search failed: ${response.status}`);
        return [];
      }

      const data = await response.json() as {
        data?: Array<{
          type?: string;
          object?: {
            id?: number;
            question?: { id?: number; title?: string };
            title?: string;
            excerpt?: string;
            content?: string;
            author?: { name?: string };
            created_time?: number;
            updated_time?: number;
          };
        }>;
      };

      if (!data.data) return [];

      const posts: Post[] = [];
      for (const item of data.data) {
        const obj = item.object;
        if (!obj) continue;

        if (item.type === 'search_result' && obj.question) {
          posts.push({
            id: String(obj.question.id ?? obj.id ?? ''),
            url: `https://www.zhihu.com/question/${obj.question.id}`,
            title: obj.question.title ?? '',
            body: (obj.excerpt ?? obj.content ?? '').replace(/<[^>]*>/g, ''),
            author: obj.author?.name ?? '',
            createdAt: obj.created_time
              ? new Date(obj.created_time * 1000).toISOString()
              : new Date().toISOString(),
            platform: this.platformId,
          });
        }
      }

      const unique = new Map<string, Post>();
      for (const p of posts) {
        if (p.id && !unique.has(p.id)) unique.set(p.id, p);
      }
      return Array.from(unique.values());
    } catch (error) {
      console.error(`[zhihu] Search error: ${(error as Error).message}`);
      return [];
    }
  }

  async reply(
    postId: string,
    content: string,
    credential: Credential,
  ): Promise<ReplyResult> {
    const instruction: BrowserInstruction = {
      mode: 'browser',
      action: 'reply',
      steps: [
        { action: 'navigate', url: `https://www.zhihu.com/question/${postId}` },
        { action: 'wait', selector: '.AnswerForm' },
        { action: 'click', selector: '.AnswerForm .RichContent' },
        { action: 'type', text: content },
        { action: 'click', selector: 'button[type="submit"]' },
      ],
      cookies: credential.value,
    };

    return {
      success: true,
      replyId: `__browser_pending__:${JSON.stringify(instruction)}`,
      mode: 'browser',
    };
  }

  async check(credential: Credential): Promise<CheckResult> {
    try {
      const response = await fetch(`${ZHIHU_API}/me`, {
        headers: buildHeaders(credential),
      });
      if (!response.ok) return { valid: false, error: `HTTP ${response.status}` };

      const data = await response.json() as { id?: string; name?: string; error?: { message?: string } };
      if (data.error) {
        return { valid: false, error: data.error.message ?? 'Unknown error' };
      }
      return { valid: !!data.id, username: data.name };
    } catch (error) {
      return { valid: false, error: (error as Error).message };
    }
  }

  rateLimitInfo(): RateLimitInfo {
    return {
      requestsPerMinute: 10,
      repliesPerDay: 10,
      minReplyIntervalSeconds: 300,
      notes: '知乎: z_c0有效期~30天, 反爬严格, 高频触发验证码. 写入需x-zse-96签名(当前用browser模式)',
    };
  }
}

const isMainModule = process.argv[1]?.replace(/\\/g, '/').endsWith('zhihu.ts');
if (isMainModule && process.argv[2] === 'test') {
  const adapter = new ZhihuAdapter();
  console.log(JSON.stringify({
    adapter: 'zhihu',
    status: 'ok',
    platformId: adapter.platformId,
    platformName: adapter.platformName,
    rateLimit: adapter.rateLimitInfo(),
  }));
}
