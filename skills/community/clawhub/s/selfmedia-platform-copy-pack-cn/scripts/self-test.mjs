import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const required = ['SKILL.md', 'manifest.yaml', 'agents/openai.yaml', 'fixtures/success.md', 'fixtures/failure.md', 'README.md', 'README.en.md', 'icon-512.png', 'LICENSE'];
const errors = [];
for (const item of required) if (!fs.existsSync(path.join(root, item))) errors.push(`missing ${item}`);
const read = (file) => fs.readFileSync(path.join(root, file), 'utf8');
if (!errors.length) {
  const skill = read('SKILL.md');
  const manifest = read('manifest.yaml');
  const agent = read('agents/openai.yaml');
  const slug = 'selfmedia-platform-copy-pack-cn';
  if (!skill.includes(`name: ${slug}`)) errors.push('SKILL.md frontmatter name mismatch');
  for (const key of [`name: ${slug}`, `slug: ${slug}`, 'icon: icon-512.png', 'self_test: node scripts/self-test.mjs']) if (!manifest.includes(key)) errors.push(`manifest missing ${key}`);
  for (const key of ['display_name:', 'short_description:', 'default_prompt:', 'icon_small: icon-512.png', 'icon_large: icon-512.png']) if (!agent.includes(key)) errors.push(`agents/openai.yaml missing ${key}`);
  if (!agent.includes('allow_implicit_invocation: true')) errors.push('agent policy must use boolean true');
  const short = (manifest.match(/short_description: (.+)/) || [])[1] || '';
  if ([...short].length < 25 || [...short].length > 64) errors.push('short_description must be 25–64 Unicode characters');
  const png = fs.readFileSync(path.join(root, 'icon-512.png'));
  if (png.subarray(0, 8).toString('hex') !== '89504e470d0a1a0a') errors.push('icon is not PNG');
  if (png.readUInt32BE(16) !== 512 || png.readUInt32BE(20) !== 512) errors.push('icon must be 512×512');
  if (!fs.existsSync(path.join(root, 'assets/promo-1600x900.png'))) errors.push('missing promo image');
  for (const fixture of ['fixtures/success.md', 'fixtures/failure.md']) if (!read(fixture).includes('参考交付')) errors.push(`${fixture} lacks copyable delivery`);
  const sample = read('fixtures/success.md');
  const input = sample.split('## 参考交付')[0];
  const output = sample.split('## 参考交付')[1] || '';
  const urls = input.match(/https?:\/\/[^\s)]+/g) || [];
  if (!urls.length) errors.push('success input lacks original source URL');
  for (const url of urls) if (!output.includes(url)) errors.push('delivery must retain original source URL');
  if (!output.includes('来源归属') || !output.includes('用户提供')) errors.push('source attribution must remain user-supplied');

}
if (errors.length) { console.error(`SELF-TEST FAILED\n${errors.map((x) => `- ${x}`).join('\n')}`); process.exit(1); }
console.log('SELF-TEST PASSED: structure, names, icons, fixtures and independent command verified.');
