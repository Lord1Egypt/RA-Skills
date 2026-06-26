// SECURITY MANIFEST:
//   Environment variables accessed: none
//   External endpoints called: https://edith.xiaohongshu.com/api/sns/web/v1
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

const XHS_API = 'https://edith.xiaohongshu.com/api/sns/web/v1';

function buildHeaders(credential: Credential): Record<string, string> {
  return {
    'Cookie': credential.value,
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Referer': 'https://www.xiaohongshu.com',
    'Origin': 'https://www.xiaohongshu.com',
  };
}

export class XiaohongshuAdapter implements PlatformAdapter {
  readonly platformId = 'xiaohongshu';
  readonly platformName = '小红书';

  async search(
    keyword: string,
    _timeRange: string,
    credential: Credential,
    _target?: string,
  ): Promise<Post[]> {
    try {
      const params = new URLSearchParams({
        keyword,
        page: '1',
        page_size: '20',
        search_id: '',
        sort: 'general',
        note_type: '0',
      });
      const response = await fetch(`${XHS_API}/search/notes?${params}`, {
        headers: buildHeaders(credential),
      });

      if (response.ok) {
        const data = await response.json() as {
          code?: number;
          success?: boolean;
          data?: {
            items?: Array<{
              id: string;
              note_card?: {
                display_title?: string;
                desc?: string;
                user?: { nickname?: string };
                time?: number;
              };
            }>;
          };
        };

        if (data.success && data.data?.items?.length) {
          return data.data.items.map(item => ({
            id: item.id,
            url: `https://www.xiaohongshu.com/explore/${item.id}`,
            title: item.note_card?.display_title ?? '',
            body: item.note_card?.desc ?? '',
            author: item.note_card?.user?.nickname ?? '',
            createdAt: item.note_card?.time
              ? new Date(item.note_card.time * 1000).toISOString()
              : new Date().toISOString(),
            platform: this.platformId,
          }));
        }
      }
    } catch (error) {
      console.error(`[xiaohongshu] API search failed, falling back to browser: ${(error as Error).message}`);
    }

    console.error('[xiaohongshu] API search unavailable, returning browser instruction');
    const instruction: BrowserInstruction = {
      mode: 'browser',
      action: 'search',
      steps: [
        { action: 'navigate', url: `https://www.xiaohongshu.com/search_result?keyword=${encodeURIComponent(keyword)}&source=web_search_result_notes` },
        { action: 'wait', selector: '.note-item' },
        { action: 'extract', selector: '.note-item', fields: ['title', 'url', 'author', 'likes'] },
      ],
      cookies: credential.value,
    };

    return [{
      id: BROWSER_INSTRUCTION_ID,
      url: '',
      title: '',
      body: JSON.stringify(instruction),
      author: '',
      createdAt: new Date().toISOString(),
      platform: this.platformId,
    }];
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
        { action: 'navigate', url: `https://www.xiaohongshu.com/explore/${postId}` },
        { action: 'wait', selector: '#content-textarea' },
        { action: 'click', selector: '#content-textarea' },
        { action: 'type', text: content },
        { action: 'click', selector: '.submit-btn' },
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
    if (!credential.value || credential.value.length === 0) {
      return { valid: false, error: 'No cookie provided' };
    }
    return {
      valid: true,
      username: '(cookie mode — verify via browser, cookies expire ~12h)',
    };
  }

  rateLimitInfo(): RateLimitInfo {
    return {
      requestsPerMinute: 20,
      repliesPerDay: 10,
      minReplyIntervalSeconds: 3,
      notes: 'No public API. Browser-only. Cookies expire ~12h. Min 3s between requests. Strongly recommend SocialVault for auto cookie refresh.',
    };
  }
}

const isMainModule = process.argv[1]?.replace(/\\/g, '/').endsWith('xiaohongshu.ts');
if (isMainModule && process.argv[2] === 'test') {
  const adapter = new XiaohongshuAdapter();
  console.log(JSON.stringify({
    adapter: 'xiaohongshu',
    status: 'ok',
    platformId: adapter.platformId,
    platformName: adapter.platformName,
    rateLimit: adapter.rateLimitInfo(),
  }));
}
