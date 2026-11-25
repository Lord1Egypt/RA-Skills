import fs from 'node:fs';
for (const [alias, original] of [['success-visible-materials.json', 'visible-materials.json'], ['failure-login-required.json', 'login-required.json']]) {
  if (fs.readFileSync(`fixtures/${alias}`, 'utf8') !== fs.readFileSync(`fixtures/${original}`, 'utf8')) throw new Error('fixture 包装副本必须与原始資料逐字一致');
}
const ok = JSON.parse(fs.readFileSync('fixtures/visible-materials.json', 'utf8'));
const failed = JSON.parse(fs.readFileSync('fixtures/login-required.json', 'utf8'));
if (!ok.fixture_notice.includes('离线') || !Array.isArray(ok.visible_items) || ok.visible_items.length > 20) throw new Error('success fixture invalid');
for (const item of ok.visible_items) if (!item.name || !item.type || !item.visible_date || !item.source) throw new Error('material fields missing');
const output = ok.expected_output;
if (!output || output.title !== '素材库目录草稿' || output.theme !== ok.theme) throw new Error('expected output must declare its title and theme');
if (!output.scope_declaration?.includes('当前可见') || !output.scope_declaration.includes(`${ok.visible_items.length}/20`) || !output.scope_declaration.includes('未盘点')) throw new Error('expected output scope declaration is incomplete');
if (!Array.isArray(output.gaps) || output.gaps.length === 0 || !output.gaps.some((gap) => gap.includes('未盘点'))) throw new Error('expected output must state historical gaps');
if (!Array.isArray(output.items) || output.items.length !== ok.visible_items.length) throw new Error('expected output item count mismatch');
for (const [index, item] of output.items.entries()) {
  const source = ok.visible_items[index];
  if (!item.name || !item.type || !item.theme || !item.visible_date || !item.usage_todo || !item.source) throw new Error(`expected output missing required business field at item ${index + 1}`);
  if (item.theme !== ok.theme || item.name !== source.name || item.type !== source.type || item.visible_date !== source.visible_date || item.source !== source.source) throw new Error(`expected output does not preserve source material at item ${index + 1}`);
}
if (failed.state !== 'login_required' || !failed.expected_action.includes('停止')) throw new Error('failure fixture invalid');
console.log(`fixtures valid: ${ok.visible_items.length} simulated visible records with expected sourced output; login branch stops`);
