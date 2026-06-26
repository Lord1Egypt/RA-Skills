// SECURITY MANIFEST:
//   Environment variables accessed: none
//   External endpoints called: https://api.bilibili.com
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
import { parseCookieValue } from '../types.js';

const BILIBILI_API = 'https://api.bilibili.com';

function buildHeaders(credential: Credential): Record<string, string> {
  return {
    'Cookie': credential.value,
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Referer': 'https://www.bilibili.com',
  };
}

export class BilibiliAdapter implements PlatformAdapter {
  readonly platformId = 'bilibili';
  readonly platformName = '哔哩哔哩';

  async search(
    keyword: string,
    _timeRange: string,
    credential: Credential,
    _target?: string,
  ): Promise<Post[]> {
    try {
      const params = new URLSearchParams({
        keyword,
        search_type: 'video',
        page: '1',
        page_size: '20',
      });
      const url = `${BILIBILI_API}/x/web-interface/wbi/search/type?${params}`;
      const response = await fetch(url, { headers: buildHeaders(credential) });

      if (!response.ok) {
        console.error(`[bilibili] Search failed: ${response.status}`);
        return [];
      }

      const data = await response.json() as {
        code: number;
        data?: {
          result?: Array<{
            aid: number;
            bvid: string;
            title: string;
            description: string;
            author: string;
            pubdate: number;
            typeid: number;
            typename: string;
          }>;
        };
      };

      if (data.code !== 0 || !data.data?.result) {
        console.error(`[bilibili] Search API error: code=${data.code}`);
        return [];
      }

      return data.data.result.map(item => ({
        id: String(item.aid),
        url: `https://www.bilibili.com/video/${item.bvid}`,
        title: item.title.replace(/<[^>]*>/g, ''),
        body: item.description,
        author: item.author,
        createdAt: new Date(item.pubdate * 1000).toISOString(),
        platform: this.platformId,
        community: item.typename,
        metadata: { bvid: item.bvid, aid: item.aid },
      }));
    } catch (error) {
      console.error(`[bilibili] Search error: ${(error as Error).message}`);
      return [];
    }
  }

  async reply(
    postId: string,
    content: string,
    credential: Credential,
  ): Promise<ReplyResult> {
    try {
      const csrf = parseCookieValue(credential.value, 'bili_jct');
      if (!csrf) {
        return { success: false, error: 'Missing bili_jct in cookie (required for CSRF)', mode: 'api' };
      }

      const response = await fetch(`${BILIBILI_API}/x/v2/reply/add`, {
        method: 'POST',
        headers: {
          ...buildHeaders(credential),
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
          type: '1',
          oid: postId,
          message: content,
          csrf,
        }).toString(),
      });

      if (!response.ok) {
        return { success: false, error: `HTTP ${response.status}`, mode: 'api' };
      }

      const data = await response.json() as {
        code: number;
        message?: string;
        data?: { rpid?: number };
      };

      if (data.code !== 0) {
        return { success: false, error: `B站 API: ${data.message ?? `code ${data.code}`}`, mode: 'api' };
      }

      return {
        success: true,
        replyId: data.data?.rpid ? String(data.data.rpid) : undefined,
        mode: 'api',
      };
    } catch (error) {
      return { success: false, error: (error as Error).message, mode: 'api' };
    }
  }

  async check(credential: Credential): Promise<CheckResult> {
    try {
      const response = await fetch(`${BILIBILI_API}/x/web-interface/nav`, {
        headers: buildHeaders(credential),
      });
      if (!response.ok) return { valid: false, error: `HTTP ${response.status}` };

      const data = await response.json() as {
        code: number;
        data?: { isLogin: boolean; uname?: string };
      };

      if (data.code !== 0 || !data.data?.isLogin) {
        return { valid: false, error: 'Not logged in or cookie expired' };
      }
      return { valid: true, username: data.data.uname };
    } catch (error) {
      return { valid: false, error: (error as Error).message };
    }
  }

  rateLimitInfo(): RateLimitInfo {
    return {
      requestsPerMinute: 30,
      repliesPerDay: 30,
      minReplyIntervalSeconds: 60,
      notes: 'B站: 搜索≤30次/时, 评论≤50条/天, 重复内容自动过滤',
    };
  }
}

const isMainModule = process.argv[1]?.replace(/\\/g, '/').endsWith('bilibili.ts');
if (isMainModule && process.argv[2] === 'test') {
  const adapter = new BilibiliAdapter();
  console.log(JSON.stringify({
    adapter: 'bilibili',
    status: 'ok',
    platformId: adapter.platformId,
    platformName: adapter.platformName,
    rateLimit: adapter.rateLimitInfo(),
  }));
}
