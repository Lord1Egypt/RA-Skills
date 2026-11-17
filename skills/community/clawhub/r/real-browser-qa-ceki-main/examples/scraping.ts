import { Browser } from '@ceki/sdk';

const br = new Browser({ token: 'YOUR_TOKEN' });
await br.connect();

const s = await br.openSession({
  mode: 'incognito',
  domainHints: ['news.ycombinator.com'],
  geo: 'US',
});

await s.navigate('https://news.ycombinator.com');

const items = await s.queryAll('a.titlelink', ['textContent', 'href'], 30);
for (const el of items.elements) {
  console.log(`${el.textContent} — ${el.href}`);
}

const pageHtml = await s.getHtml('body', false);
console.log(`\nPage HTML size: ${pageHtml.html.length} chars`);

const screenshot = await s.screenshot('png');
console.log(`Screenshot: ${screenshot.data.length} base64 chars`);

await s.close();
await br.close();
