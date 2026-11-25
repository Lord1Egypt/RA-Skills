#!/usr/bin/env node
import fs from 'node:fs';

const [inputPath, outputPath] = process.argv.slice(2);
if (!inputPath || !outputPath) {
  console.error('用法：node scripts/audit.mjs <输入.json> <交付.md>');
  process.exit(2);
}
const data = JSON.parse(fs.readFileSync(inputPath, 'utf8'));
const shots = data.shots;
const assets = data.assets;
if (!Array.isArray(shots) || !Array.isArray(assets) || shots.length > 30 || assets.length > 50) {
  throw new Error('输入必须包含 shots/ assets 数组，且最多30个镜头、50项素材。');
}
const absent = v => v === undefined || v === null || v === '';
const esc = v => String(v ?? '').replaceAll('|', '\\|');
const missingFields = (a, shot = null) => [
  absent(a.content) && '内容说明',
  shot?.format && absent(a.format) && '形式',
  absent(a.aspect_ratio) && '画幅',
  absent(a.duration_seconds) && '可用时长',
  absent(a.license) && '授权信息'
].filter(Boolean);
const needsConfirm = (a, shot = null) => missingFields(a, shot).length > 0;
const label = x => `${x.content ?? '内容待确认'}${x.format ? `（${x.format}）` : ''}`;
const compatible = (s, a) => !needsConfirm(a, s) && a.content === s.content && (!s.format || a.format === s.format) && a.aspect_ratio === s.aspect_ratio && Number(a.duration_seconds) >= Number(s.duration_seconds) && (a.license === 'cleared' || a.license === 'owned');
const rows = shots.map(s => {
  const matches = assets.filter(a => compatible(s, a));
  const sameContent = assets.filter(a => a.content === s.content);
  const incomplete = sameContent.filter(a => needsConfirm(a, s));
  const status = matches.length ? '已覆盖' : incomplete.length ? '需确认' : sameContent.length ? '规格不符' : '缺失';
  const evidence = matches.length ? matches.map(a => a.id).join('、') : sameContent.map(a => `${a.id}（${a.format || '形式待确认'} / ${a.aspect_ratio || '画幅待确认'} / ${a.duration_seconds ?? '时长待确认'}秒 / ${a.license || '授权待确认'}）`).join('、') || '无';
  const action = status === '已覆盖' ? '无需补充'
    : status === '需确认' ? `先补充确认：${incomplete.map(a => `${a.id}的${missingFields(a, s).join('、')}`).join('；')}；确认后再判断是否补料`
    : `补拍或补生成：${label(s)}，${s.aspect_ratio}，至少${s.duration_seconds}秒；授权须明确`;
  return { s, status, evidence, action };
});
const confirm = assets.map(a => {
  const missing = new Set(missingFields(a));
  for (const shot of shots) if (shot.format && shot.content === a.content && absent(a.format)) missing.add('形式');
  return { asset: a, missing: [...missing] };
}).filter(x => x.missing.length);
const out = [
  '# 视频素材缺口表', '', '## 镜头需求 × 现有素材匹配', '', '| 镜头 | 需求 | 匹配素材/证据 | 状态 | 建议 |', '| --- | --- | --- | --- | --- |',
  ...rows.map(r => `| ${esc(r.s.id)} | ${esc(label(r.s))}；${esc(r.s.aspect_ratio)}；${r.s.duration_seconds}秒 | ${esc(r.evidence)} | ${r.status} | ${esc(r.action)} |`),
  '', '## 缺失或规格不符', '', ...rows.filter(r => r.status !== '已覆盖').map(r => `- ${r.s.id}：${r.status}。${r.action}`),
  ...(rows.every(r => r.status === '已覆盖') ? ['- 无。'] : []), '', '## 需确认', '',
  ...confirm.map(({asset, missing}) => `- ${asset.id}：${missing.join('、')}缺失；仅凭文件名不认定可用。`),
  ...(confirm.length ? [] : ['- 无。']), ''
];
fs.writeFileSync(outputPath, out.join('\n'));
