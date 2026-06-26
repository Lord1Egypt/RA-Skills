// SECURITY MANIFEST:
//   Environment variables accessed: none
//   External endpoints called: https://tieba.baidu.com
//   Local files read: none
//   Local files written: none

import type {
  PlatformAdapter,
  Credential,
  Post,
  ReplyResult,
  CheckResult,
  RateLimitInfo,
} from '../types.js';

const TIEBA_BASE = 'https://tieba.baidu.com';

function buildHeaders(credential: Credential): Record<string, string> {
  return {
    'Cookie': credential.value,
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
  };
}

async function getTbs(credential: Credential): Promise<string | null> {
  try {
    const response = await fetch(`${TIEBA_BASE}/dc/common/tbs`, {
      headers: buildHeaders(credential),
    });
    if (!response.ok) return null;
    const data = await response.json() as { tbs?: string; is_login?: number };
    return data.tbs ?? null;
  } catch {
    return null;
  }
}

export class TiebaAdapter implements PlatformAdapter {
  readonly platformId = 'tieba';
  readonly platformName = '百度贴吧';

  async search(
    keyword: string,
    _timeRange: string,
    credential: Credential,
    target?: string,
  ): Promise<Post[]> {
    try {
      const url = target
        ? `${TIEBA_BASE}/f?kw=${encodeURIComponent(target)}&ie=utf-8&pn=0`
        : `${TIEBA_BASE}/f/search/res?qw=${encodeURIComponent(keyword)}&rn=20&pn=1`;

      const response = await fetch(url, { headers: buildHeaders(credential) });
      if (!response.ok) {
        console.error(`[tieba] Search failed: ${response.status}`);
        return [];
      }

      const html = await response.text();
      const posts: Post[] = [];

      const threadPattern = /href="\/p\/(\d+)"[^>]*>([^<]+)<\/a>/g;
      let match;
      while ((match = threadPattern.exec(html)) !== null) {
        const [, threadId, title] = match;
        if (!threadId || !title) continue;
        const cleanTitle = title.trim();
        if (cleanTitle.length < 4) continue;

        posts.push({
          id: threadId,
          url: `${TIEBA_BASE}/p/${threadId}`,
          title: cleanTitle,
          body: '',
          author: '',
          createdAt: new Date().toISOString(),
          platform: this.platformId,
          community: target,
        });
      }

      const uniquePosts = new Map<string, Post>();
      for (const p of posts) {
        if (!uniquePosts.has(p.id)) uniquePosts.set(p.id, p);
      }
      return Array.from(uniquePosts.values()).slice(0, 20);
    } catch (error) {
      console.error(`[tieba] Search error: ${(error as Error).message}`);
      return [];
    }
  }

  async reply(
    postId: string,
    content: string,
    credential: Credential,
  ): Promise<ReplyResult> {
    try {
      const tbs = await getTbs(credential);
      if (!tbs) {
        return { success: false, error: 'Failed to get tbs token', mode: 'api' };
      }

      const metadata = (this as unknown as { _lastReplyMeta?: { kw: string; fid: string } })._lastReplyMeta;
      const kw = metadata?.kw ?? '';
      const fid = metadata?.fid ?? '';

      const response = await fetch(`${TIEBA_BASE}/f/commit/post/add`, {
        method: 'POST',
        headers: {
          ...buildHeaders(credential),
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
          ie: 'utf-8',
          kw,
          fid,
          tid: postId,
          content,
          tbs,
        }).toString(),
      });

      if (!response.ok) {
        return { success: false, error: `HTTP ${response.status}`, mode: 'api' };
      }

      const data = await response.json() as {
        err_code?: number;
        error?: string;
        data?: { tid?: string };
      };

      if (data.err_code && data.err_code !== 0) {
        return { success: false, error: data.error ?? `err_code ${data.err_code}`, mode: 'api' };
      }

      return { success: true, mode: 'api' };
    } catch (error) {
      return { success: false, error: (error as Error).message, mode: 'api' };
    }
  }

  async check(credential: Credential): Promise<CheckResult> {
    try {
      const response = await fetch(`${TIEBA_BASE}/dc/common/tbs`, {
        headers: buildHeaders(credential),
      });
      if (!response.ok) return { valid: false, error: `HTTP ${response.status}` };

      const data = await response.json() as { tbs?: string; is_login?: number };
      if (data.is_login !== 1) {
        return { valid: false, error: 'Not logged in or BDUSS expired' };
      }
      return { valid: true, username: '(logged in via BDUSS)' };
    } catch (error) {
      return { valid: false, error: (error as Error).message };
    }
  }

  rateLimitInfo(): RateLimitInfo {
    return {
      requestsPerMinute: 20,
      repliesPerDay: 20,
      minReplyIntervalSeconds: 120,
      notes: '贴吧: BDUSS有效期6个月+, 回帖≤30条/天, 重复内容被删, 需从请求头获取BDUSS(非Cookie-Editor的BDUSS_BFESS)',
    };
  }
}

const isMainModule = process.argv[1]?.replace(/\\/g, '/').endsWith('tieba.ts');
if (isMainModule && process.argv[2] === 'test') {
  const adapter = new TiebaAdapter();
  console.log(JSON.stringify({
    adapter: 'tieba',
    status: 'ok',
    platformId: adapter.platformId,
    platformName: adapter.platformName,
    rateLimit: adapter.rateLimitInfo(),
  }));
}
