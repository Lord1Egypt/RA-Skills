import fs from 'node:fs';
import path from 'node:path';

const root = path.resolve(import.meta.dirname, '..');
const read = (file) => fs.readFileSync(path.join(root, file), 'utf8');
const fail = (message) => { throw new Error(message); };
const must = (value, message) => { if (!value) fail(message); };

const skill = read('SKILL.md');
const manifest = read('manifest.yaml');
const agent = read('agents/openai.yaml');
must(/^name: shop-shipping-policy-compare-free$/m.test(skill), 'SKILL.md frontmatter name 不匹配');
must(/^name: shop-shipping-policy-compare-free$/m.test(manifest), 'manifest name 不匹配');
must(/^slug: shop-shipping-policy-compare-free$/m.test(manifest), 'manifest slug 不匹配');
must(/icon: icon-512\.png/.test(manifest), 'manifest 缺少根图标');
must(/icon_(small|large): icon-512\.png/g.test(agent), 'agent 图标引用缺失');
must(/allow_implicit_invocation: true/.test(agent), 'policy 布尔值缺失');
must(fs.existsSync(path.join(root, 'icon-512.png')), '根图标不存在');
const png = fs.readFileSync(path.join(root, 'icon-512.png'));
must(png.subarray(0, 8).equals(Buffer.from([137,80,78,71,13,10,26,10])), '根图标不是 PNG');
const width = png.readUInt32BE(16), height = png.readUInt32BE(20);
must(width === 512 && height === 512, `图标尺寸应为 512×512，实际为 ${width}×${height}`);
for (const file of ['README.md', 'README.en.md', 'LICENSE', 'fixtures/success-policy-pages.json', 'fixtures/failure-policy-pages.json']) {
  must(fs.existsSync(path.join(root, file)), `缺少 ${file}`);
}
for (const file of ['fixtures/success-policy-pages.json', 'fixtures/failure-policy-pages.json']) {
  const fixture = JSON.parse(read(file));
  must(fixture.fixture_type.includes('离线页面资料模拟'), `${file} 未标注离线模拟`);
}
const success = JSON.parse(read('fixtures/success-policy-pages.json'));
const storeA = success.pages[0].visible_text;
must(storeA.includes('满 99 元免运费') && storeA.includes('未满时结算页显示运费'), 'success fixture must preserve both free-shipping branches');
must(success.expected.store_a.includes('未满99元时结算页显示运费'), 'expected comparison must include the below-threshold branch');
must(success.expected.store_b.includes('发货时效未见明确条款') && success.expected.store_b.includes('库存确认后安排发货'), 'ambiguous dispatch wording must not be presented as a duration');
const failure = JSON.parse(read('fixtures/failure-policy-pages.json'));
must(failure.pages.every(page => !page.store), 'unseen store attribution must not come from a hidden store field');
must(failure.expected.includes('不得将两条费用条件归属于任何指定店铺'), 'failure fixture must mark unattributed conditions as unknown');
must(/关闭前.*list_tabs.*每个 tabId.*本次 navigate 返回/.test(skill), 'session ownership must be checked before close_session');
console.log('PASS: structure, icon dimensions, agent policy, both fee branches, ambiguous dispatch duration, unknown store attribution, session ownership check, and offline-only fixtures are valid.');
