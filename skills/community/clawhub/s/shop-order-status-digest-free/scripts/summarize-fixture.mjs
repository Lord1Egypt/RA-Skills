#!/usr/bin/env node
import fs from 'node:fs';

const file = process.argv[2];
if (!file) throw new Error('用法：node scripts/summarize-fixture.mjs <fixture.json>');
const data = JSON.parse(fs.readFileSync(file, 'utf8'));
const authorizedInContext = data.authorization?.owner_confirmed === true
  || data.authorization?.explicit_in_current_request === true;
if (!authorizedInContext) {
  console.log(JSON.stringify({
    reportable: false,
    reason: '当前请求未明确店铺归属或用户授权；不读取或报告订单信息。',
    source: data.source,
    missing: ['说明该店铺属于本人或用户有权查看']
  }, null, 2));
  process.exit(2);
}
const orders = data.orders.slice(0, 20);
const maskOrderId = orderId => {
  const value = String(orderId ?? '');
  if (value.length <= 3) return '***';
  const prefix = value.match(/^[A-Za-z]+-/)?.[0] ?? '';
  return `${prefix}…${value.slice(-3)}`;
};
if (!data.filters?.confirmed) {
  console.log(JSON.stringify({
    reportable: false,
    reason: '日期或状态筛选未确认；不报告全店总数。',
    source: data.source,
    missing: ['已确认日期范围', '已确认状态筛选']
  }, null, 2));
  process.exit(2);
}
const counts = Object.fromEntries(orders.reduce((m, order) => m.set(order.status, (m.get(order.status) || 0) + 1), new Map()));
const needs_action = orders.filter(order => order.action_needed).map(({order_id, status, action_needed, evidence}) => ({order_id: maskOrderId(order_id), status, action_needed, evidence}));
console.log(JSON.stringify({
  reportable: true,
  scope: {date_range: data.filters.date_range, status: data.filters.status, visible_orders: orders.length, limit: 20},
  status_counts: counts,
  needs_action,
  source: data.source,
  missing: []
}, null, 2));
