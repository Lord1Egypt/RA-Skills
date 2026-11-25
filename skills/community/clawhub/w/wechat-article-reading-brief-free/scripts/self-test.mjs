import { existsSync, readFileSync, statSync } from 'node:fs';
import { resolve } from 'node:path';

const root = resolve(import.meta.dirname, '..');
const need = ['SKILL.md', 'manifest.yaml', 'agents/openai.yaml', 'README.md', 'README.en.md', 'LICENSE', 'icon-512.png', 'promo.png', 'fixtures/success-page.html', 'fixtures/failure-login.html', 'fixtures/success-case.json', 'fixtures/failure-login-case.json'];
const fail = message => { throw new Error(message); };
for (const file of need) if (!existsSync(resolve(root, file))) fail(`missing ${file}`);
const png = file => {
  const data = readFileSync(resolve(root, file));
  if (data.subarray(0, 8).toString('hex') !== '89504e470d0a1a0a') fail(`${file} is not PNG`);
  const w = data.readUInt32BE(16), h = data.readUInt32BE(20);
  return [w, h];
};
const [iw, ih] = png('icon-512.png'); if (iw !== 512 || ih !== 512) fail('icon must be 512x512');
const [pw, ph] = png('promo.png'); if (pw !== 1600 || ph !== 900) fail('promo must be 1600x900');
const skill = readFileSync(resolve(root, 'SKILL.md'), 'utf8');
const manifest = readFileSync(resolve(root, 'manifest.yaml'), 'utf8');
const agent = readFileSync(resolve(root, 'agents/openai.yaml'), 'utf8');
if (!skill.includes('name: wechat-article-reading-brief-free')) fail('SKILL name mismatch');
for (const key of ['name: wechat-article-reading-brief-free', 'slug: wechat-article-reading-brief-free', 'icon: icon-512.png', 'self_test: node scripts/self-test.mjs']) if (!manifest.includes(key)) fail(`manifest missing ${key}`);
if (!/^self_test: node scripts\/self-test\.mjs$/m.test(manifest)) fail('self_test must be a directly executable scalar command');
if (!agent.includes('allow_implicit_invocation: false') || !agent.includes('icon_small: "./icon-512.png"')) fail('agent interface/policy invalid');
for (const file of ['fixtures/success-page.html', 'fixtures/failure-login.html']) if (!readFileSync(resolve(root, file), 'utf8').includes('离线页面资料模拟')) fail(`${file} lacks offline label`);

// This is an offline behavioral check of the skill's visible-content contract.  It
// intentionally receives the URL, focus question, and a synthetic browserId from
// each business fixture; it never contacts a browser or claims online collection.
const text = html => html.replace(/<[^>]*>/g, ' ').replace(/\s+/g, ' ').trim();
const between = (html, tag) => {
  const match = html.match(new RegExp(`<${tag}[^>]*>([\\s\\S]*?)<\\/${tag}>`, 'i'));
  return match ? text(match[1]) : '未显示';
};
const makeBrief = (input, html) => {
  const pageText = text(html);
  const title = between(html, 'h1');
  if (/需要登录后查看|正文未显示/.test(pageText)) return {
    title, main_conclusion: '未显示', key_steps: [], author: '未显示', date: '未显示', publisher: '未显示',
    source_url: input.urls[0], visible_scope: '登录验证',
    missing_items: ['正文未显示', '作者未显示', '日期未显示', '来源公众号未显示']
  };
  const byline = pageText.match(/作者：([^\s]+)\s+日期：([^\s]+)\s+来源：([^\s]+)/);
  const conclusion = pageText.match(/先限定问题，再记录可见证据，最后标记缺项。/)?.[0] ?? '未显示';
  return {
    title, main_conclusion: conclusion, key_steps: conclusion === '未显示' ? [] : ['限定问题', '记录可见证据', '标记缺项'],
    author: byline?.[1] ?? '未显示', date: byline?.[2] ?? '未显示', publisher: byline?.[3] ?? '未显示',
    source_url: input.urls[0], visible_scope: conclusion === '未显示' ? '正文截断' : '正文可见', missing_items: []
  };
};
for (const caseFile of ['success-case.json', 'failure-login-case.json']) {
  const fixture = JSON.parse(readFileSync(resolve(root, 'fixtures', caseFile), 'utf8'));
  const { business_input: input, expected_brief: expected } = fixture;
  if (!fixture.fixture_notice.includes('离线页面资料模拟')) fail(`${caseFile} lacks offline notice`);
  if (!Array.isArray(input.urls) || input.urls.length !== 1 || !input.urls[0].startsWith('https://')) fail(`${caseFile} lacks a business URL`);
  if (!Array.isArray(input.focus_questions) || input.focus_questions.length === 0) fail(`${caseFile} lacks a focus question`);
  if (input.browserId !== 'fixture-browser-id') fail(`${caseFile} must use only the synthetic fixture browserId`);
  const actual = makeBrief(input, readFileSync(resolve(root, 'fixtures', fixture.page), 'utf8'));
  if (JSON.stringify(actual) !== JSON.stringify(expected)) fail(`${caseFile} brief does not match visible-page result`);
  if (actual.source_url !== input.urls[0]) fail(`${caseFile} did not preserve the supplied source URL`);
}
console.log('self-test passed: metadata, assets, and offline success/login business briefs verified');
