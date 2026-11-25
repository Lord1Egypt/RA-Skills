#!/usr/bin/env node
import { execFileSync } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
const root = path.resolve(import.meta.dirname, '..');
const run = fixture => {
  const output = path.join('/tmp', `video-asset-gap-${fixture}.md`);
  execFileSync(process.execPath, ['scripts/audit.mjs', `fixtures/${fixture}.json`, output], { cwd: root, stdio: 'inherit' });
  const actual = fs.readFileSync(output, 'utf8');
  const expected = fs.readFileSync(path.join(root, `fixtures/${fixture}.expected.md`), 'utf8');
  if (actual !== expected) throw new Error(`${fixture} 输出与已核验参考交付不一致。`);
};
run('success');
run('failure');
run('incomplete-same-content');
const temp = fs.mkdtempSync(path.join(os.tmpdir(), 'video-asset-format-'));
try {
  const check = (name, input) => {
    const inputPath = path.join(temp, `${name}.json`);
    const outputPath = path.join(temp, `${name}.md`);
    fs.writeFileSync(inputPath, JSON.stringify(input));
    execFileSync(process.execPath, ['scripts/audit.mjs', inputPath, outputPath], {cwd: root, stdio: 'inherit'});
    return fs.readFileSync(outputPath, 'utf8');
  };
  const asset = {id:'A1',content:'咖啡冲泡',format:'照片',aspect_ratio:'9:16',duration_seconds:8,license:'owned'};
  const unconstrained = check('optional-format', {shots:[{id:'S1',content:'咖啡冲泡',aspect_ratio:'9:16',duration_seconds:6}],assets:[asset]});
  if (!unconstrained.includes('| S1 | 咖啡冲泡；9:16；6秒 | A1 | 已覆盖 |')) throw new Error('镜头未指定形式时，合格的形式字段不应造成误报');
  const requiredMissing = check('required-format-missing', {shots:[{id:'S1',content:'咖啡冲泡',format:'录屏',aspect_ratio:'9:16',duration_seconds:6}],assets:[{...asset,format:undefined}]});
  if (!requiredMissing.includes('| S1 | 咖啡冲泡（录屏）;') && !requiredMissing.includes('| S1 | 咖啡冲泡（录屏）')) throw new Error('镜头要求形式但素材未提供时应保留为待确认');
  if (!requiredMissing.includes('S1') || !requiredMissing.includes('需确认') || !requiredMissing.includes('形式缺失')) throw new Error('缺少必需形式时没有说明具体待确认字段');
  const targetRow = requiredMissing.split('\n').find(line => line.startsWith('| S1 |'));
  if (!targetRow?.includes('A1的形式')) throw new Error('需确认的目标镜头行必须在建议动作中明确要求补充素材形式');
  const mismatch = check('required-format-mismatch', {shots:[{id:'S1',content:'咖啡冲泡',format:'录屏',aspect_ratio:'9:16',duration_seconds:6}],assets:[asset]});
  if (!mismatch.includes('规格不符') || mismatch.includes('| A1 | 已覆盖 |')) throw new Error('镜头指定形式与素材形式冲突时错误判为覆盖');
} finally { fs.rmSync(temp, {recursive:true, force:true}); }
console.log('self-test passed: all reference fixtures plus optional, required-missing, and mismatched format cases generated correct status and evidence.');
