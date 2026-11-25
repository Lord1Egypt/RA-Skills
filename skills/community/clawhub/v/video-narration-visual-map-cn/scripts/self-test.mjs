#!/usr/bin/env node
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import path from 'node:path';
import fs from 'node:fs';
import { mkdtempSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const required = ['SKILL.md', 'manifest.yaml', 'agents/openai.yaml', 'README.md', 'README.en.md', 'icon-512.png', 'assets/promo-1600x900.png', 'fixtures/success-input.json', 'fixtures/success-output.md', 'fixtures/failure-input.json', 'fixtures/failure-output.md'];
for (const file of required) if (!fs.existsSync(path.join(root, file))) throw new Error(`缺少发布文件: ${file}`);
const run = (fixture) => spawnSync(process.execPath, ['scripts/validate-input.mjs', fixture], { cwd: root, encoding: 'utf8' });
const success = run('fixtures/success-input.json');
const successExpected = fs.readFileSync(path.join(root, 'fixtures/success-output.md'), 'utf8');
const successInput = JSON.parse(fs.readFileSync(path.join(root, 'fixtures/success-input.json'), 'utf8'));
const successActual = JSON.parse(success.stdout);
const expectedRows = [
  { narrationId: 'N1', shotIds: ['S01'], status: '画不支撑话' },
  { narrationId: 'N2', shotIds: ['S01'], status: '已支撑' },
  { narrationId: 'N3', shotIds: ['S02', 'S03'], status: '已支撑' },
  { narrationId: 'N4', shotIds: ['S02', 'S03'], status: '需补素材' },
  { narrationId: 'N5', shotIds: [], status: '有声无画' },
];
if (success.status !== 0 || successActual.status !== 'mapped' || expectedRows.length === 0) throw new Error(`成功样例未产生可比对的对应表:\n${success.stdout}${success.stderr}`);
for (const expected of expectedRows) {
  const actual = successActual.rows.find((row) => row.narration_id === expected.narrationId);
  if (!actual || JSON.stringify(actual.shot_ids) !== JSON.stringify(expected.shotIds) || actual.status !== expected.status) {
    throw new Error(`成功样例与参考交付不符（${expected.narrationId}）:\n${success.stdout}`);
  }
}
const n1 = successActual.rows.find((row) => row.narration_id === 'N1');
const n2 = successActual.rows.find((row) => row.narration_id === 'N2');
const fixtureN1 = successInput.narration.find((line) => line.id === 'N1');
const fixtureN2 = successInput.narration.find((line) => line.id === 'N2');
const fixtureS01 = successInput.shots.find((shot) => shot.id === 'S01');
if (fixtureN1?.claims?.[0] !== '已生成海报' || fixtureN1?.shot_ids?.[0] !== 'S01' || fixtureN2?.text !== '海报可以一键下载。' || fixtureN2?.claims?.[0] !== '下载按钮可见' || fixtureS01?.visible_claims?.includes('已生成海报') || !successExpected.includes('已经下载完成') || n1?.status !== '画不支撑话' || n2?.status !== '已支撑') {
  throw new Error('成功样例必须区分“已生成结果缺失”和“可以下载入口可见”：不能把能力旁白标成已下载，也不能以输入表单支撑已生成结果。');
}
if (!successExpected.includes('已支撑') || !successExpected.includes('有声无画') || !successExpected.includes('画不支撑话') || !successExpected.includes('需补素材')) throw new Error('成功参考交付必须展示四种逐句状态');
if (!successActual.evidence_coverage || JSON.stringify(successActual.missing_materials) !== '["价格"]') throw new Error('全局必需证据须独立汇总覆盖情况，不能强加到每句旁白');
const temp = mkdtempSync(path.join(tmpdir(), 'narration-visual-map-'));
try {
  const input = {
    narration: [
      {id: 'N3', text: '标题和人物都已出现。', claims: ['标题已显示', '人物已显示'], shot_ids: ['S02', 'S03'], required_evidence: ['标题', '人物肖像']},
      {id: 'N4', text: '海报已下载。', claims: ['海报已下载'], shot_ids: ['S04']},
    ],
    shots: [
      {id: 'S02', description: '海报标题清晰可见。', visible_claims: ['标题已显示'], visible_evidence: ['标题']},
      {id: 'S03', description: '海报中的人物肖像清晰可见。', visible_claims: ['人物已显示'], visible_evidence: ['人物肖像']},
      {id: 'S04', description: '海报编辑页面显示下载按钮。', visible_claims: ['下载按钮可见'], visible_evidence: ['下载按钮']},
    ],
    required_evidence: ['标题', '人物肖像'],
  };
  const inputPath = path.join(temp, 'input.json');
  fs.writeFileSync(inputPath, JSON.stringify(input));
  const result = run(inputPath);
  const actual = JSON.parse(result.stdout);
  if (result.status !== 0 || actual.rows.find((row) => row.narration_id === 'N3')?.status !== '已支撑' || JSON.stringify(actual.rows.find((row) => row.narration_id === 'N3')?.shot_ids) !== '["S02","S03"]') throw new Error(`分布在多个镜头的主张和证据应合并支持同一句旁白：\n${result.stdout}`);
  if (actual.rows.find((row) => row.narration_id === 'N4')?.status !== '画不支撑话') throw new Error('仅显示下载按钮不能支撑“海报已下载”这一完成结果主张');
  if (actual.missing_materials.length !== 0) throw new Error('全片已覆盖的必需证据不应重复列为缺料');
} finally { rmSync(temp, {recursive: true, force: true}); }
const failure = run('fixtures/failure-input.json');
const failureExpected = fs.readFileSync(path.join(root, 'fixtures/failure-output.md'), 'utf8');
const failureActual = JSON.parse(failure.stdout);
if (failure.status !== 2 || failureActual.status !== 'needs_input' || !failureActual.request.includes('候选镜头') || !failureExpected.includes('不能完成句画对照')) throw new Error(`失败样例未按参考交付请求补料:\n${failure.stdout}${failure.stderr}`);
console.log('PASS: 成功样例覆盖已支撑、有声无画、画不支撑话、需补素材；验证动作/结果不按同名词误判、多个镜头可联合支撑、全片证据独立汇总；失败样例按参考交付请求候选镜头说明。');
