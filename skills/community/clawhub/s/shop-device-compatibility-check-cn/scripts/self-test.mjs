#!/usr/bin/env node
import { execFileSync } from 'node:child_process';
import fs from 'node:fs';
const run = (file) => JSON.parse(execFileSync(process.execPath, ['scripts/check-compatibility.mjs', file], { encoding: 'utf8' }));
const runText = (file) => execFileSync(process.execPath, ['scripts/check-compatibility.mjs', file], { encoding: 'utf8' });
for (const [input, expected] of [['fixtures/success-input.json', 'fixtures/success-output.json'], ['fixtures/failure-input.json', 'fixtures/failure-output.json']]) {
  if (runText(input) !== fs.readFileSync(expected, 'utf8')) throw new Error(`${input} 的实际 CLI 交付与 ${expected} 不一致`);
}
const ok = run('fixtures/success-input.json').results;
if (ok.map(x => x.status).join(',') !== '确认适配,明确不适配,未知') throw new Error('成功样例状态不符合预期');
if (!ok[2].basis.includes('未列出')) throw new Error('未知样例未请求补充资料');
const fail = run('fixtures/failure-input.json').results[0];
if (fail.status !== '未知' || !fail.basis.includes('完整设备型号') || !fail.basis.includes('接口协议')) throw new Error('失败样例未阻止外观或协议推断');
const conditionalInput = { devices: [{ model: 'X2', conditions: { region_version: '国行', interface_protocol: 'USB 2.0', system_version: '13' } }], accessories: [{ specification: '扩展坞A' }], compatibility_rules: [{ device_model: 'X2', accessory_specification: '扩展坞A', status: '确认适配', required_conditions: { region_version: '国行', interface_protocol: 'USB 3.2', system_version: '>=14' }, evidence: '厂家条件表。' }] };
const conditional = JSON.parse(execFileSync(process.execPath, ['scripts/check-compatibility.mjs', '-'], { input: JSON.stringify(conditionalInput), encoding: 'utf8' })).results[0];
if (conditional.status !== '未知' || !conditional.basis.includes('接口协议') || !conditional.basis.includes('系统版本')) throw new Error('厂家条件限制未阻止确认适配');
const empty = JSON.parse(execFileSync(process.execPath, ['scripts/check-compatibility.mjs', '-'], { input: JSON.stringify({ compatibility_rules: [] }), encoding: 'utf8' })).results[0];
if (!empty || empty.status !== '未知' || !empty.basis.includes('完整设备型号') || !empty.basis.includes('完整配件规格')) throw new Error('空输入未请求补充型号和配件规格');
const missingAccessories = JSON.parse(execFileSync(process.execPath, ['scripts/check-compatibility.mjs', '-'], { input: JSON.stringify({ devices: [{ model: 'X2' }], compatibility_rules: [] }), encoding: 'utf8' })).results[0];
if (missingAccessories.status !== '未知' || !missingAccessories.basis.includes('完整配件规格')) throw new Error('缺少配件时未请求补充配件规格');
const orderedConflict = JSON.parse(execFileSync(process.execPath, ['scripts/check-compatibility.mjs', '-'], { input: JSON.stringify({ devices: [{model:'X2'}], accessories:[{specification:'扩展坞A'}], compatibility_rules:[{device_model:'X2',accessory_specification:'扩展坞A',status:'确认适配',evidence:'厂家适配条目A'},{device_model:'X2',accessory_specification:'扩展坞A',status:'明确不适配',evidence:'厂家排除条目B'}] }), encoding: 'utf8' })).results[0];
if (orderedConflict.status !== '明确不适配' || !orderedConflict.basis.includes('排除条目B')) throw new Error('规则数组中的通用适配不得遮蔽已满足的明确排除');
const noEvidence = JSON.parse(execFileSync(process.execPath, ['scripts/check-compatibility.mjs', '-'], { input: JSON.stringify({ devices:[{model:'X2'}], accessories:[{specification:'扩展坞A'}], compatibility_rules:[{device_model:'X2',accessory_specification:'扩展坞A',status:'确认适配'}] }), encoding:'utf8' })).results[0];
if (noEvidence.status !== '未知' || !noEvidence.basis.includes('依据')) throw new Error('缺少证据的厂家适配规则不能输出确认');
const connectorOnly = JSON.parse(execFileSync(process.execPath, ['scripts/check-compatibility.mjs', '-'], { input: JSON.stringify({ devices:[{model:'X2'}], accessories:[{specification:'USB-C'}], compatibility_rules:[{device_model:'X2',accessory_specification:'USB-C',status:'确认适配',evidence:'仅接口描述'}] }), encoding:'utf8' })).results[0];
if (connectorOnly.status !== '未知' || !connectorOnly.basis.includes('接口协议')) throw new Error('仅有USB-C接口形状、未给协议时不能确认兼容');
for (const p of ['fixtures/success-output.json', 'fixtures/failure-output.json']) {
  if (!fs.existsSync(p)) throw new Error(`缺少参考交付：${p}`);
}
const readme = fs.readFileSync('README.md', 'utf8');
const firstScreen = readme.split(/\n## /u, 1)[0];
if (!firstScreen.includes('node scripts/check-compatibility.mjs fixtures/success-input.json') || !firstScreen.includes('确认适配 / 明确不适配 / 未知')) throw new Error('README 首屏必须说明能力、结论状态和可直接运行的示例');
console.log('self-test passed: 成功、不适配、厂家条件限制、资料不足与空输入分支均已真实运行。');
