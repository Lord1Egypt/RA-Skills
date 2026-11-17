import { readFile, stat } from 'node:fs/promises';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const required = ['SKILL.md', 'manifest.yaml', 'agents/openai.yaml', 'README.md', 'README.en.md', 'LICENSE', 'icon-512.png', 'assets/promo-1600x900.png', 'fixtures/success-input.md', 'fixtures/success-output.md', 'fixtures/failure-input.md', 'fixtures/failure-output.md'];
for (const file of required) await stat(resolve(root, file));
const skill = await readFile(resolve(root, 'SKILL.md'), 'utf8');
const manifest = await readFile(resolve(root, 'manifest.yaml'), 'utf8');
const agent = await readFile(resolve(root, 'agents/openai.yaml'), 'utf8');
const successInput = await readFile(resolve(root, 'fixtures/success-input.md'), 'utf8');
const success = await readFile(resolve(root, 'fixtures/success-output.md'), 'utf8');
const failure = await readFile(resolve(root, 'fixtures/failure-output.md'), 'utf8');
const checks = [
  [/^name: selfmedia-editorial-style-sheet-cn$/m, skill, 'SKILL name'],
  [/^name: selfmedia-editorial-style-sheet-cn$/m, manifest, 'manifest name'],
  [/^slug: selfmedia-editorial-style-sheet-cn$/m, manifest, 'manifest slug'],
  [/^icon: icon-512\.png$/m, manifest, 'manifest icon'],
  [/^  allow_implicit_invocation: true$/m, agent, 'agent policy'],
  [/人工智能（AI）/, success, 'success terminology delivery'],
  [/三稿都反复用短句成组推进操作/, success, 'repeated short-paragraph style'],
  [/稿 1：“先列出…3个问题。再按问题…”；稿 2：“先把工作流拆成两步。再逐项…”；稿 3：“先选1篇旧稿做测试。再记录…”/, success, 'cross-draft sentence evidence'],
  [/禁用词“链路”不应出现在成稿中/, success, 'approved forbidden term'],
  [/只出现一次，属于玩笑，不要求后续稿件采用/, success, 'one-off joke boundary'],
  [/不会依据账号名称或一句口号编造文风/, failure, 'failure branch delivery'],
];
for (const [pattern, content, label] of checks) if (!pattern.test(content)) throw new Error(`missing ${label}`);
for (const quote of ['先列出读者最关心的 3 个问题。再按问题整理素材。', '先把工作流拆成两步。再逐项补齐材料。', '先选 1 篇旧稿做测试。再记录读者反馈。', '让工具当主编？它可能先催你交稿。']) {
  if (!successInput.includes(quote)) throw new Error(`fixture evidence not found in input: ${quote}`);
}
if ((success.match(/让工具当主编/g) ?? []).length !== 1 || /\[ \] .*工具当主编/.test(success)) throw new Error('single-use joke must be recorded as an exception, not a reusable rule');
for (const [content, label] of [[manifest, 'manifest'], [agent, 'agent']]) {
  const match = content.match(/^\s*short_description: (.+)$/m);
  if (!match || [...match[1]].length < 25 || [...match[1]].length > 64) throw new Error(`${label} short_description must be 25–64 characters`);
}
const png = await readFile(resolve(root, 'icon-512.png'));
if (png.readUInt32BE(16) !== 512 || png.readUInt32BE(20) !== 512) throw new Error('icon must be 512×512 PNG');
const promo = await readFile(resolve(root, 'assets/promo-1600x900.png'));
if (promo.readUInt32BE(16) !== 1600 || promo.readUInt32BE(20) !== 900) throw new Error('promo must be 1600×900 PNG');
console.log('self-test passed: publish structure, artwork dimensions, and evidence-grounded success/failure deliveries verified');
