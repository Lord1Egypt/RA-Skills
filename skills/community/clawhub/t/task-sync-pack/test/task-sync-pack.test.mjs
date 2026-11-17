import assert from 'node:assert/strict';
import { mkdtemp, readFile, rm } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import test from 'node:test';
import { build, renderPackage, verify } from '../scripts/task-sync-pack.mjs';

const fixture = new URL('../examples/官网改版.task.json', import.meta.url);

test('同一合同生成字节一致的包，并可重复校验', async () => {
  const directory = await mkdtemp(path.join(os.tmpdir(), 'task-sync-pack-'));
  try {
    const first = path.join(directory, 'first.task-sync.zip');
    const second = path.join(directory, 'second.task-sync.zip');
    const one = await build({ inputPath: fixture, outputPath: first });
    const two = await build({ inputPath: fixture, outputPath: second });
    assert.equal(one.changed, true);
    assert.equal(two.changed, true);
    assert.deepEqual(await readFile(first), await readFile(second));
    assert.equal((await build({ inputPath: fixture, outputPath: first })).changed, false);
    const checked = await verify(first);
    assert.equal(checked.ok, true);
    assert.equal(checked.task_id, 'TS-WEBSITE-001');
  } finally {
    await rm(directory, { recursive: true, force: true });
  }
});

test('投影包含相同合同哈希和全部完成判据', async () => {
  const contract = JSON.parse(await readFile(fixture, 'utf8'));
  const rendered = renderPackage(contract);
  const human = rendered.files.get('任务说明.md');
  const ai = rendered.files.get('AI任务说明.md');
  assert.match(human, new RegExp(rendered.contractHash));
  assert.match(ai, new RegExp(rendered.contractHash));
  for (const criterion of contract.definition_of_done) {
    assert.match(human, new RegExp(criterion));
    assert.match(ai, new RegExp(criterion));
  }
});
