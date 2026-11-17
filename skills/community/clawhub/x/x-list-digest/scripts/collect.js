// Read-only snapshot through the native host; scroll uses its mouse-wheel helper.
() => {
  const text = document.body.innerText;
  const status = /verify you are human|suspicious activity|\u9a8c\u8bc1\u7801/i.test(text) ? 'captcha'
    : /\/login|login\.x\.com/.test(location.href) ? 'login_required'
    : /rate limit|too many requests|\u8bf7\u6c42\u8fc7\u591a/i.test(text) ? 'rate_limited' : 'ok';
  const tweets = [...document.querySelectorAll('article[data-testid="tweet"]')].flatMap(a => {
    const path = t => { const href=t.closest('a')?.getAttribute('href'); return href ? new URL(href,location.href).pathname : ''; };
    const time = [...a.querySelectorAll('time[datetime]')].find(t => /^\/[^/]+\/status\/\d+$/.test(path(t)));
    let link = time?.closest('a');
    let match = time ? path(time).match(/^\/([^/]+)\/status\/(\d+)/) : null;
    let rootTime = time;
    if (!match && a === document.querySelector('article[data-testid="tweet"]')) {
      match = location.pathname.match(/^\/([^/]+)\/status\/(\d+)$/);
      rootTime = a.querySelector('time[datetime]');
      const handles = a.querySelector('[data-testid="User-Name"]')?.innerText || '';
      if (!match || !handles.split(/\s/).includes('@'+match[1])) return [];
    }
    if (!match || !rootTime) return [];
    const count = key => {
      const label = a.querySelector(`[data-testid="${key}"]${key==='like'?', [data-testid="unlike"]':''}`)?.getAttribute('aria-label') || '';
      const n = label.match(/[\d,.]+\s*[KM]?/i)?.[0];
      if (!n) return null;
      const value = parseFloat(n.replace(/,/g,''));
      return Number.isFinite(value) ? Math.round(value * (/M/i.test(n)?1e6:/K/i.test(n)?1e3:1)) : null;
    };
    return [{tweet_id:match[2],author_handle:match[1],timestamp_iso:rootTime.dateTime,
      url:'https://x.com/'+match[1]+'/status/'+match[2],text:a.querySelector('[data-testid="tweetText"]')?.innerText || '',
      media:[...a.querySelectorAll('[data-testid="tweetPhoto"] img')].map(i=>({alt:i.alt,url:i.src})),
      engagement:{likes:count('like'),replies:count('reply'),reposts:count('retweet')},
      expandable:/Show more|\u663e\u793a\u66f4\u591a|Show this thread|\u663e\u793a\u6b64\u5e16\u6587\u4e32/i.test(a.innerText)}];
  });
  const timeline=document.querySelector('[data-testid="primaryColumn"]');
  const rect=timeline?.getBoundingClientRect();
  return {status,logged_in:!!document.querySelector('[data-testid="AppTabBar_Profile_Link"]'),sorting:'unknown',
    viewport:{x:rect?Math.max(1,Math.min(innerWidth-1,rect.x+rect.width/2)):innerWidth/2,y:innerHeight/2,height:innerHeight},
    scroll_position:{y:window.scrollY,height:document.documentElement.scrollHeight,viewport_height:innerHeight},tweets};
}
