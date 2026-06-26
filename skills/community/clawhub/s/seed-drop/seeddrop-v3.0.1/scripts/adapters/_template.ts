// SECURITY MANIFEST:
//   Environment variables accessed: (list here)
//   External endpoints called: (list here)
//   Local files read: (list here)
//   Local files written: (list here)

import type {
  PlatformAdapter,
  Credential,
  Post,
  ReplyResult,
  CheckResult,
  RateLimitInfo,
} from '../types.js';

/**
 * Template for creating a new platform adapter.
 *
 * Steps:
 * 1. Copy this file to scripts/adapters/<platform>.ts
 * 2. Rename the class and update platformId / platformName
 * 3. Implement search(), reply(), check(), rateLimitInfo()
 * 4. Register in scripts/adapters/base.ts
 * 5. Create templates/reply-<platform>.md
 * 6. Add rate limits to references/safety-rules.md
 * 7. Add TOS notes to references/platform-tos-notes.md
 * 8. Test with: npx tsx scripts/adapters/<platform>.ts test
 */
export class TemplateAdapter implements PlatformAdapter {
  readonly platformId = 'template';
  readonly platformName = 'Template Platform';

  async search(
    keyword: string,
    timeRange: string,
    credential: Credential,
    target?: string,
  ): Promise<Post[]> {
    // TODO: Implement platform-specific search
    // API mode: use fetch() with credential
    // Browser mode: return BrowserInstruction wrapped in Post[]
    console.error(`[${this.platformId}] search() not implemented`);
    return [];
  }

  async reply(
    postId: string,
    content: string,
    credential: Credential,
  ): Promise<ReplyResult> {
    // TODO: Implement reply logic
    console.error(`[${this.platformId}] reply() not implemented`);
    return { success: false, error: 'Not implemented' };
  }

  async check(credential: Credential): Promise<CheckResult> {
    // TODO: Implement credential validation
    console.error(`[${this.platformId}] check() not implemented`);
    return { valid: false, error: 'Not implemented' };
  }

  rateLimitInfo(): RateLimitInfo {
    return {
      requestsPerMinute: 60,
      repliesPerDay: 10,
      minReplyIntervalSeconds: 300,
      notes: 'TODO: Add platform-specific rate limit notes',
    };
  }
}

const isMainModule = process.argv[1]?.replace(/\\/g, '/').endsWith('_template.ts');
if (isMainModule && process.argv[2] === 'test') {
  const adapter = new TemplateAdapter();
  console.log(JSON.stringify({
    adapter: 'template',
    status: 'ok',
    platformId: adapter.platformId,
    platformName: adapter.platformName,
    rateLimit: adapter.rateLimitInfo(),
  }));
}
