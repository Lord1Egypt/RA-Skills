/**
 * 飞书日历授权消息构建器
 * 用于生成包含授权链接的格式化消息
 */

export interface CalendarAuthConfig {
  appId: string;
  appSecret: string;
  redirectUri: string;
}

export function buildCalendarAuthMessage(authUrl: string): string {
  return [
    '📅 日历授权请求',
    '需要你的授权才能以你的身份管理日历和会议室预约。',
    '请点击下方链接完成授权:',
    authUrl,
    '',
    '授权步骤:',
    '1. 点击上方链接',
    '2. 同意授权',
    '3. 页面跳转后,把 URL 中的 code 参数值发给我',
    '',
    '例如跳转后的 URL 是:',
    'https://your-domain.com/api/feishu/oauth/callback?code=abcd1234&state=...',
    '你只需要把 abcd1234 发给我即可。',
  ].join('\n');
}

export function generateAuthUrl(config: CalendarAuthConfig): string {
  const state = `calendar_auth_${Date.now()}`;
  const encodedRedirectUri = encodeURIComponent(config.redirectUri);
  return `https://open.feishu.cn/open-apis/authen/v1/authorize?app_id=${config.appId}&redirect_uri=${encodedRedirectUri}&state=${state}`;
}

export function parseAuthCode(callbackUrl: string): string | null {
  try {
    const url = new URL(callbackUrl);
    return url.searchParams.get('code');
  } catch {
    return null;
  }
}
