#!/usr/bin/env node
import fs from 'node:fs';

const inputPath = process.argv[2];
if (!inputPath) throw new Error('用法：node scripts/check-compatibility.mjs <input.json>');
const input = JSON.parse(inputPath === '-' ? fs.readFileSync(0, 'utf8') : fs.readFileSync(inputPath, 'utf8'));
const devices = input.devices ?? [];
const accessories = input.accessories ?? [];
const rules = input.compatibility_rules ?? [];
if (!Array.isArray(devices) || !Array.isArray(accessories) || !Array.isArray(rules)) {
  throw new Error('devices、accessories 和 compatibility_rules 必须是数组');
}
if (devices.length > 10 || accessories.length > 10) throw new Error('最多核对10种设备和10个配件');
const norm = (value) => String(value ?? '').trim().toLowerCase();
const display = (value, fallback) => String(value ?? '').trim() || fallback;
const conditionMap = (item) => {
  const conditions = item?.conditions ?? item?.customer_conditions ?? {};
  return conditions && typeof conditions === 'object' && !Array.isArray(conditions) ? conditions : {};
};
const ruleConditions = (rule) => {
  const conditions = rule?.required_conditions ?? rule?.conditions ?? {};
  return conditions && typeof conditions === 'object' && !Array.isArray(conditions) ? conditions : {};
};
const asList = (value) => Array.isArray(value) ? value : [value];
const versionParts = (value) => String(value).replace(/^v/i, '').split('.').map(Number);
const compareVersions = (left, right) => {
  const a = versionParts(left); const b = versionParts(right);
  if (a.some(Number.isNaN) || b.some(Number.isNaN)) return null;
  for (let i = 0; i < Math.max(a.length, b.length); i += 1) {
    if ((a[i] ?? 0) !== (b[i] ?? 0)) return (a[i] ?? 0) - (b[i] ?? 0);
  }
  return 0;
};
const conditionMatches = (actual, expected) => asList(expected).some((candidate) => {
  const text = String(candidate ?? '').trim();
  const comparison = text.match(/^(>=|<=|>|<|=)\s*v?([0-9]+(?:\.[0-9]+)*)$/);
  if (comparison) {
    const result = compareVersions(actual, comparison[2]);
    if (result === null) return false;
    return ({ '>': result > 0, '>=': result >= 0, '<': result < 0, '<=': result <= 0, '=': result === 0 })[comparison[1]];
  }
  return norm(actual) === norm(candidate);
});
const missingConditions = (conditions, required) => Object.keys(required).filter((key) => !String(conditions[key] ?? '').trim());
const mismatchedConditions = (conditions, required) => Object.keys(required).filter((key) => String(conditions[key] ?? '').trim() && !conditionMatches(conditions[key], required[key]));
const conditionLabel = (key) => ({ region_version: '地区版本', interface_protocol: '接口协议', system_version: '系统版本' }[key] ?? key);
const needConditions = (keys) => keys.map(conditionLabel).join('、');
const incompleteSpec = (spec) => /接口照片|仅.*接口|无协议说明|未知协议/i.test(spec)
  || (/(?:USB[- ]?C|Type[- ]?C|C口)/i.test(spec) && !/(?:USB\s*[123](?:\.[0-9]+)?|USB\s*4|Thunderbolt|雷电|PD\s*\d|DisplayPort|DP Alt|协议)/i.test(spec));
const makeResult = (device, accessory) => {
  const model = String(device?.model ?? '').trim();
  const spec = String(accessory?.specification ?? '').trim();
  let status = '未知';
  let basis = '未提供可核对的厂家型号适配资料。';
  if (!model || !spec || incompleteSpec(spec)) {
    const needs = [];
    if (!model) needs.push('完整设备型号');
    if (!spec || incompleteSpec(spec)) needs.push('完整配件规格（含接口协议/功能标准）');
    basis = `请补充${needs.join('和')}；接口外观相同不足以判断兼容。`;
  } else {
    const exact = rules.filter((rule) => norm(rule.device_model) === norm(model) && norm(rule.accessory_specification) === norm(spec));
    const conditions = { ...conditionMap(input), ...conditionMap(accessory), ...conditionMap(device) };
    const evaluated = exact.map((rule) => {
      const required = ruleConditions(rule);
      const missing = missingConditions(conditions, required);
      const mismatch = mismatchedConditions(conditions, required);
      return { rule, missing, mismatch, applicable: !missing.length && !mismatch.length };
    });
    const applicable = evaluated.filter((item) => item.applicable);
    const verified = applicable.filter(({ rule }) => ['确认适配', '明确不适配'].includes(rule.status) && String(rule.evidence ?? '').trim());
    const exclusions = verified.filter(({ rule }) => rule.status === '明确不适配');
    const adaptations = verified.filter(({ rule }) => rule.status === '确认适配');
    const unsupported = applicable.filter(({ rule }) => ['确认适配', '明确不适配'].includes(rule.status) && !String(rule.evidence ?? '').trim());
    const uncertainSpecific = evaluated.filter((item) => item.missing.length && !item.mismatch.length);
    if (exclusions.length) {
      status = '明确不适配';
      basis = exclusions.map(({ rule }) => String(rule.evidence).trim()).join('；');
    } else if (uncertainSpecific.length) {
      const missing = [...new Set(uncertainSpecific.flatMap((item) => item.missing))];
      basis = `厂家规则要求${needConditions(missing)}；请补充顾客具体条件后再核对。`;
    } else if (unsupported.length) {
      basis = '厂家规则没有可引用依据；请补充来源或原始条目后再判断。';
    } else if (adaptations.length) {
      status = '确认适配'; basis = adaptations.map(({ rule }) => String(rule.evidence).trim()).join('；');
    } else if (applicable.length && verified.length === 0) {
      basis = '厂家适配/排除条目缺少可引用依据或有效结论；请补充原始资料证据后再判断。';
    } else if (exact.length) {
      const missing = [...new Set(evaluated.flatMap((item) => item.missing))];
      const mismatch = [...new Set(evaluated.flatMap((item) => item.mismatch))];
      if (missing.length) basis = `厂家规则要求${needConditions(missing)}；请补充顾客具体条件后再核对。`;
      else if (mismatch.length) basis = `顾客${needConditions(mismatch)}不满足厂家规则限制；不能确认适配。`;
      else basis = '厂家资料未给出可判定的适配状态；请补充适配或排除结论及依据。';
    } else if (rules.some(r => norm(r.device_model) === norm(model))) {
      basis = '厂家资料未列出该配件规格；请补充对应型号的适配或排除条目。';
    } else {
      basis = '厂家资料未列出该设备型号；请补充完整型号及厂家适配/排除表。';
    }
  }
  return { device_model: display(model, '（未提供）'), accessory_specification: display(spec, '（未提供）'), status, basis };
};
const resultDevices = devices.length ? devices : [{}];
const resultAccessories = accessories.length ? accessories : [{}];
const results = resultDevices.flatMap((device) => resultAccessories.map((accessory) => makeResult(device, accessory)));
process.stdout.write(JSON.stringify({ scope_note: '仅核对明确提供的适配条件；不做实际测试，不承诺电气性能，也不因插头相同推断全功能兼容。', results }, null, 2) + '\n');
