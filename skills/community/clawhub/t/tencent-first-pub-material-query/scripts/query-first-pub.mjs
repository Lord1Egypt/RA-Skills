#!/usr/bin/env node
/**
 * 首发素材消耗查询
 * 直接接收账户ID列表，查询首发素材消耗
 *
 * 用法：
 *   node query-first-pub.mjs '{"account_ids":["31079027","12345678"],"start_date":"2026-04-01","end_date":"2026-04-30"}'
 *   node query-first-pub.mjs --base64 <Base64>
 */

import { execSync } from 'child_process';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// ─── 解析参数 ───
let argsJson;
if (process.argv.includes('--base64')) {
  const idx = process.argv.indexOf('--base64');
  argsJson = Buffer.from(process.argv[idx + 1], 'base64').toString('utf8');
} else {
  argsJson = process.argv[2];
}

const args = JSON.parse(argsJson);
const { account_ids, start_date, end_date } = args;

if (!account_ids?.length || !start_date || !end_date) {
  console.error(JSON.stringify({ error: '缺少必填参数: account_ids, start_date, end_date' }));
  process.exit(1);
}

const MGMT_SKILL = path.resolve(__dirname, '..', '..', 'tencentads-management');

function runReportQuery(params) {
  const json = JSON.stringify(params);
  const base64 = Buffer.from(json).toString('base64');
  const cmd = `node scripts/query-report.mjs --base64 ${base64}`;
  try {
    const out = execSync(cmd, { cwd: MGMT_SKILL, encoding: 'utf8', timeout: 180000, stdio: ['pipe', 'pipe', 'ignore'] });
    const data = JSON.parse(out);
    // If script returned a file_path, read the full data from it
    if (data.file_path) {
      try {
        const fullData = JSON.parse(fs.readFileSync(data.file_path, 'utf8'));
        return fullData;
      } catch {}
    }
    return data;
  } catch (e) {
    const stderr = e.stderr || e.stdout || e.message || '';
    const match = stderr.match(/\{[\s\S]*\}/);
    if (match) { try { return JSON.parse(match[0]); } catch {} }
    console.error(`  [WARN] query-report failed: ${(e.message || '').slice(0, 200)}`);
    return null;
  }
}

function runReportQueryAll(params) {
  const results = [];
  let pg = 1;
  const ps = 100;
  while (true) {
    const data = runReportQuery({ ...params, page: pg, page_size: ps });
    if (!data?.list || data.list.length === 0) break;
    results.push(...data.list);
    const total = data.page_info?.total_number || 0;
    if (results.length >= total || data.list.length < ps) break;
    pg++;
  }
  return results;
}

// ─── 查询首发素材 ───
console.error(`查询 ${account_ids.length} 个账户，${start_date} ~ ${end_date}`);

const BATCH = 20;
const imgFirstPubMap = {};
const vidFirstPubMap = {};

for (let i = 0; i < account_ids.length; i += BATCH) {
  const batch = account_ids.slice(i, i + BATCH).map(String);
  console.error(`  IMAGE 第 ${i+1}-${Math.min(i+BATCH, account_ids.length)} 个账户...`);

  const imgList = runReportQueryAll({
    account_ids: batch,
    date_range: { start_date, end_date },
    level: 'IMAGE',
    fields: [
      'image.image_id', 'image.image_name', 'image.first_publication_status',
      'image.first_publication_status_cn', 'image.quality_status', 'image.quality_status_cn',
      'report.cost', 'report.view_count', 'report.valid_click_count',
      'report.ctr', 'report.conversions_count', 'report.conversions_cost'
    ],
    order_by: [{ sort_field: 'report.cost', sort_type: 'DESCENDING' }]
  });

  for (const item of imgList) {
    if (item.image?.first_publication_status === 'FIRST_PUBLICATION_STATUS_FIRST_PUBLICATION') {
      const acctId = String(item.report?.account_id || item.account_id);
      if (!imgFirstPubMap[acctId]) imgFirstPubMap[acctId] = [];
      imgFirstPubMap[acctId].push(item);
    }
  }

  console.error(`  VIDEO 第 ${i+1}-${Math.min(i+BATCH, account_ids.length)} 个账户...`);
  const vidList = runReportQueryAll({
    account_ids: batch,
    date_range: { start_date, end_date },
    level: 'VIDEO',
    fields: [
      'video.video_id', 'video.video_name', 'video.first_publication_status',
      'video.first_publication_status_cn', 'video.quality_status', 'video.quality_status_cn',
      'report.cost', 'report.view_count', 'report.valid_click_count',
      'report.ctr', 'report.conversions_count', 'report.conversions_cost'
    ],
    order_by: [{ sort_field: 'report.cost', sort_type: 'DESCENDING' }]
  });

  for (const item of vidList) {
    if (item.video?.first_publication_status === 'FIRST_PUBLICATION_STATUS_FIRST_PUBLICATION') {
      const acctId = String(item.report?.account_id || item.account_id);
      if (!vidFirstPubMap[acctId]) vidFirstPubMap[acctId] = [];
      vidFirstPubMap[acctId].push(item);
    }
  }
}

// ─── 汇总 ───
const activeAcctIds = new Set([...Object.keys(imgFirstPubMap), ...Object.keys(vidFirstPubMap)]);

function agg(items) {
  let cost = 0, views = 0, clicks = 0, conv = 0;
  for (const item of items) {
    const r = item.report || {};
    cost += parseFloat(String(r.cost || '0').replace(/,/g, ''));
    views += parseFloat(String(r.view_count || '0').replace(/,/g, ''));
    clicks += parseFloat(String(r.valid_click_count || '0').replace(/,/g, ''));
    conv += parseFloat(String(r.conversions_count || '0').replace(/,/g, ''));
  }
  return {
    cost: cost.toFixed(2), views, clicks, conversions: conv,
    ctr: views > 0 ? (clicks / views * 100).toFixed(2) + '%' : '0%',
    conv_cost: conv > 0 ? (cost / conv).toFixed(2) : '-'
  };
}

function toDetail(items, typeKey, idKey, nameKey) {
  return items.map(item => {
    const obj = item[typeKey] || {};
    const r = item.report || {};
    return {
      id: obj[idKey], name: obj[nameKey], quality: obj.quality_status_cn,
      cost: r.cost, views: r.view_count, clicks: r.valid_click_count,
      ctr: r.ctr, conversions: r.conversions_count, conv_cost: r.conversions_cost
    };
  });
}

const results = [];
for (const acctId of activeAcctIds) {
  const imgItems = imgFirstPubMap[acctId] || [];
  const vidItems = vidFirstPubMap[acctId] || [];
  const imgSum = agg(imgItems);
  const vidSum = agg(vidItems);
  const totalCost = parseFloat(imgSum.cost) + parseFloat(vidSum.cost);
  const totalConv = imgSum.conversions + vidSum.conversions;
  const totalViews = imgSum.views + vidSum.views;
  const totalClicks = imgSum.clicks + vidSum.clicks;

  results.push({
    account_id: parseInt(acctId),
    first_pub: {
      total: {
        material_count: imgItems.length + vidItems.length,
        cost: totalCost.toFixed(2), views: totalViews, clicks: totalClicks,
        conversions: totalConv,
        ctr: totalViews > 0 ? (totalClicks / totalViews * 100).toFixed(2) + '%' : '0%',
        conv_cost: totalConv > 0 ? (totalCost / totalConv).toFixed(2) : '-'
      },
      image: { first_pub_count: imgItems.length, ...imgSum, details: toDetail(imgItems, 'image', 'image_id', 'image_name') },
      video: { first_pub_count: vidItems.length, ...vidSum, details: toDetail(vidItems, 'video', 'video_id', 'video_name') }
    }
  });
}

results.sort((a, b) => parseFloat(b.first_pub.total.cost) - parseFloat(a.first_pub.total.cost));

console.error(`\n完成！${activeAcctIds.size}/${account_ids.length} 个账户有首发素材`);
console.log(JSON.stringify({ query: { account_ids, start_date, end_date }, queried_accounts: account_ids.length, active_accounts: activeAcctIds.size, results }, null, 2));
