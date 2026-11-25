#!/usr/bin/env node
import { readFile, writeFile } from 'node:fs/promises';
import { homedir } from 'node:os';
import { join } from 'node:path';
import { existsSync } from 'node:fs';
import { spawnSync } from 'node:child_process';
import { randomUUID } from 'node:crypto';

const MAX_ROWS = 100;
const visibleFields = [
  ['规格', '颜色', 'spec.color'], ['规格', '尺码', 'spec.size'], ['规格', '库存', 'spec.stock'],
  ['图文', '主图', 'media.mainImage'], ['图文', '详情图', 'media.detailImages'], ['图文', '详情文案', 'media.description'],
  ['物流', '运费模板', 'shipping.freightTemplate'], ['物流', '发货地', 'shipping.origin'],
  ['售后', '退货承诺', 'afterSale.returnPolicy'], ['售后', '售后说明', 'afterSale.serviceNote']
];
const aliases = {
  'spec.color': ['颜色', '色彩'], 'spec.size': ['尺码', '尺寸'], 'spec.stock': ['库存', '库存数量'],
  'media.mainImage': ['主图', '商品主图'], 'media.detailImages': ['详情图', '详情图片'], 'media.description': ['详情文案', '商品描述', '详情描述'],
  'shipping.freightTemplate': ['运费模板', '物流模板'], 'shipping.origin': ['发货地', '发货地址'],
  'afterSale.returnPolicy': ['退货承诺', '退换货', '退货政策'], 'afterSale.serviceNote': ['售后说明', '售后服务']
};
const usage = `用法：\n  node scripts/check-listing.mjs --offline-page fixtures/success-page.json [--rules fixtures/rules.json] --output result.json\n  node scripts/check-listing.mjs --browser-id <用户指定ID> --page-url <用户指定商品编辑页URL> [--rules rules.json] --output result.json\n\n默认只读：不会填写、保存或上架。`;
function arg(name) { const i = process.argv.indexOf(name); return i < 0 ? undefined : process.argv[i + 1]; }
function pending(value) {
  // These are UI prompts, not a value supplied by the merchant.  Keep this
  // deliberately broad: back offices use many variants such as “暂无运费模板”.
  if (typeof value !== 'string') return false;
  // This explicit marker is documented by the skill. Check it before the
  // broader UI-prompt expression so a semantic field pair cannot become 已见.
  const compact = value.trim().replace(/\s+/gu, '');
  if (compact === '暂无运费模板') return true;
  return /^(?:未确认(?:[：:].*)?|未填写(?:[：:].*)?|待确认(?:[：:].*)?|请(?:先)?(?:选择|填写|上传|输入|添加).*$|待(?:选择|上传|填写|补充).*$|暂无(?:可用)?(?:运费模板|模板|图片|主图|详情图|规格|素材|内容|选项|可选项|文件|附件)|(?:示例|例如|比如)\s*[：:].*$|[-—–\s]*请选择.*|[-—–\s]*选择[^\s].*|--[^-]+--)$/u.test(value.trim());
}
function normalizeFieldLabel(value) {
  // Back-office labels frequently combine a leading/trailing asterisk,
  // parenthesised required marker, and a colon in any order.  Peel those
  // decorations repeatedly so they cannot create a duplicate custom field.
  let label = String(value || '').trim();
  let previous;
  do {
    previous = label;
    label = label.replace(/^[*＊]\s*/u, '').replace(/\s*[*＊]\s*$/u, '')
      .replace(/\s*[（(【\[]?\s*(?:必填|选填|必选|可选|required|optional)\s*[）)】\]]?\s*$/iu, '')
      .replace(/\s*[:：]\s*$/u, '').trim();
  } while (label !== previous);
  return label;
}
function sensitiveLabel(value) { return /password|token|secret|api[_ -]?key|credential|访问密钥|密钥|令牌|口令|凭据/iu.test(String(value || '')); }
// A pending marker is evidence that the page has not been confirmed, not an
// explicit empty value.  It must therefore never become a missing-field row.
function missing(value) { return !pending(value) && (value === null || (typeof value === 'string' && !value.trim()) || (Array.isArray(value) && value.length === 0)); }
const forbiddenPathSegments = new Set(['__proto__', 'prototype', 'constructor']);
function safeFieldPath(path) {
  return typeof path === 'string' && path.length > 0 && path.split('.').every(part =>
    part.length > 0 && !forbiddenPathSegments.has(part) && /^[\p{L}\p{N}_-]+$/u.test(part));
}
function ruleRequirements(rules) {
  // Rules are external JSON. Do not let a property inherited from Object's
  // prototype become a requirement (notably `constructor`).
  return rules && typeof rules === 'object' && Object.hasOwn(rules, 'requirements') && Array.isArray(rules.requirements)
    ? rules.requirements.filter(rule => rule && typeof rule === 'object') : [];
}
function ruleField(rule) {
  return Object.hasOwn(rule, 'field') ? rule.field : undefined;
}
function validateRulePaths(rules) {
  for (const requirement of ruleRequirements(rules)) {
    const field = ruleField(requirement);
    if (field !== undefined && !safeFieldPath(field)) throw new Error('商家规则包含不安全的字段路径；已停止读取并未生成结果。');
  }
}
function get(object, path) {
  if (!safeFieldPath(path)) return undefined;
  let value = object;
  for (const key of path.split('.')) {
    if (value == null || (typeof value !== 'object' && typeof value !== 'function') || !Object.hasOwn(value, key)) return undefined;
    value = value[key];
  }
  return value;
}
function pageValue(page, path) {
  const raw = get(page.fields || {}, path);
  return raw && typeof raw === 'object' && !Array.isArray(raw) && Object.hasOwn(raw, 'value') ? raw : { value: raw, source: page.source };
}
function safePageUrl(raw) {
  if (!raw) return '未提供URL';
  try { const url = new URL(raw); return `${url.origin}${url.pathname}`; }
  catch { return '未提供URL'; }
}
function pageIdentity(raw) {
  const url = new URL(raw);
  if (!/^https?:$/.test(url.protocol)) throw new Error('页面身份不是 HTTP(S) 地址。');
  const ignored = /^(?:access_token|token|signature|sign|secret|api_key|apikey|authorization)$/i;
  const query = [...url.searchParams.entries()].filter(([key]) => !ignored.test(key)).sort(([a,av],[b,bv]) => a.localeCompare(b) || av.localeCompare(bv));
  // Hash routes can identify a completely different product while retaining
  // the same path and query.  Keep the fragment in the canonical identity so
  // every later viewport read is tied to the product first observed.
  return JSON.stringify([url.origin, url.pathname.replace(/\/$/u,'') || '/', query, url.hash]);
}
function samePageIdentity(actual, requested) {
  try {
    const finalUrl = new URL(actual), requestedUrl = new URL(requested);
    // A user may open a hash-routed editor through its fragmentless entry URL.
    // In that one case accept the initial resolved fragment, then freeze it as
    // the actual page identity for the remainder of the scan.
    if (!requestedUrl.hash) {
      finalUrl.hash = '';
      requestedUrl.hash = '';
    }
    return pageIdentity(finalUrl.href) === pageIdentity(requestedUrl.href);
  } catch { return false; }
}
function safeEvidenceSource(value) {
  return String(value || '').replace(/https?:\/\/[^\s"'<>]+/giu, url => safePageUrl(url))
    .replace(/\b(access_token|token|signature|sign|secret|api_key|apikey|authorization)=([^&#\s]+)/giu, '$1=[REDACTED]');
}
function sourceFor(value, fallback) { return safeEvidenceSource(value.source || fallback || '可见页面资料'); }
function addSource(...sources) { return [...new Set(sources.filter(Boolean).map(safeEvidenceSource))].join('；'); }
function missingRuleAction(label, rules) {
  const instructions = rules.flatMap(rule => {
    const parts = [];
    if (rule.expected !== undefined) parts.push(`按商家规则补充：${rule.expected}`);
    if (rule.action) parts.push(rule.action);
    return parts;
  });
  return [`请人工补充${label}资料`, ...new Set(instructions)].join('；');
}
function pendingRuleAction(label, rules) {
  const instructions = rules.flatMap(rule => {
    const parts = [];
    if (rule.expected !== undefined) parts.push(`对照商家规则确认：${rule.expected}`);
    if (rule.action) parts.push(rule.action);
    return parts;
  });
  return [`请先核实${label}资料`, ...new Set(instructions)].join('；');
}
function conflictRuleAction(label, rules) {
  const instructions = rules.flatMap(rule => {
    const parts = [];
    if (rule.expected !== undefined) parts.push(`规则要求：${rule.expected}`);
    if (rule.action) parts.push(rule.action);
    return parts;
  });
  return [`请按商家规则处理${label}`, ...new Set(instructions)].join('；');
}
// `snapshot --text-mode page` is intentionally not an evidence input here:
// Easy WebBridge uses it for page-level text, which can include text that is
// outside the viewport or visually obscured. `visibleText` is separately
// collected from rendered, hit-testable DOM text below.
function pageFromSnapshot(snapshot, labelledValues, visibleControls, visibleImages, rules = null) {
  const fields = {};
  const customFields = new Map();
  // A tab id becomes meaningless after the task session is closed. Keep the
  // browser-provided, human-auditable page identity with every derived value.
  const pageSource = `可见商品编辑页快照：标题=${snapshot.title || '未提供标题'}；URL=${safePageUrl(snapshot.url)}`;
  const assign = (path, value, append = false, pendingControl = false) => {
    if (!safeFieldPath(path)) throw new Error('页面字段映射包含不安全的字段路径；已停止读取并未生成结果。');
    const parts = path.split('.'); let cursor = fields;
    for (const part of parts.slice(0, -1)) cursor = cursor[part] ||= {};
    const existed = Object.hasOwn(cursor, parts.at(-1));
    const old = cursor[parts.at(-1)]?.value;
    // Repeated rows (for example, one inventory control per SKU) are
    // evidence in their own right. Keep their order and even equal values.
    const next = append && existed
      ? [...(Array.isArray(old) ? old : [old]), ...(Array.isArray(value) ? value : [value])]
      : value;
    // Keep an empty control's prompt as state, never as a merchant value.
    // In particular, placeholder/aria-placeholder and a disabled selected
    // option must not later turn into an "已见" value.
    cursor[parts.at(-1)] = { value: next, source: pageSource, pending: Boolean(cursor[parts.at(-1)]?.pending || pendingControl) };
  };
  const addCustomField = (label, category, value, pendingControl = false) => {
    const cleanLabel = normalizeFieldLabel(label);
    // An unknown section is not evidence that a value belongs to 商品信息.
    // Keeping it out is safer than inventing a category (and avoids mixing
    // unrelated controls such as account settings into the result).
    if (!cleanLabel || !['规格', '图文', '物流', '售后'].includes(category)) return;
    // Category is deliberately part of the key: “卖点” may legitimately
    // occur in both 规格 and 图文 and must not overwrite the other value.
    // Labels are user-visible prose and may contain spaces, brackets, slashes,
    // or punctuation.  They must not be used verbatim as an object path: use a
    // deterministic base64url key while retaining the original label for output.
    const labelKey = Buffer.from(cleanLabel, 'utf8').toString('base64url');
    const path = `custom.${String(category).replace(/[.]/gu, '·')}.label_${labelKey}`;
    customFields.set(path, { label: cleanLabel, category });
    assign(path, value, true, pendingControl);
  };
  const customPath = (label, category) => `custom.${String(category).replace(/[.]/gu, '·')}.label_${Buffer.from(normalizeFieldLabel(label), 'utf8').toString('base64url')}`;
  const categoryByPath = Object.fromEntries(visibleFields.map(([category,,path])=>[path,category]));
  const unscopedRulePaths = new Set(ruleRequirements(rules)
    .filter(rule => ruleField(rule) && !rule.category)
    .map(ruleField));
  // Rules may repeat an internal field and its label (for example 运费模板).
  // Store one canonical candidate for each field/label pair; category is a
  // disambiguator, not a reason to turn one field into several candidates.
  const paths = Object.entries(aliases).flatMap(([path, names]) => names.map(name => ({ path, name:normalizeFieldLabel(name), category:categoryByPath[path] })));
  for (const rule of ruleRequirements(rules)) {
    const field = ruleField(rule);
    if (!field || !Object.hasOwn(rule, 'label')) continue;
    const name = normalizeFieldLabel(rule.label);
    if (name) paths.push({ path: field, name, category: categoryByPath[field] || rule.category || '' });
  }
  const uniquePaths = [...new Map(paths.filter(item => item.name).map(item => [`${item.path}\u0000${item.name}`, item])).values()]
    .sort((a, b) => b.name.length - a.name.length);
  const resolvePath = (label, category) => {
    const candidates = uniquePaths.filter(item => item.name === label);
    const scoped = category ? candidates.filter(item => item.category === category) : candidates;
    // A merchant rule can intentionally omit category. When its label maps to
    // exactly one rule path, a page section is still useful disambiguation and
    // must not split one value into a custom page field plus a pending rule.
    // Do not fall back to a known field from a different category.
    const applicable = scoped.length || !category
      ? scoped
      : candidates.filter(item => !item.category);
    const candidatePaths = [...new Map(applicable.map(item => [item.path, item])).values()];
    return candidatePaths.length === 1 ? candidatePaths[0] : null;
  };
  const assignMatched = (match, label, category, value, pendingControl = false) => {
    if (unscopedRulePaths.has(match.path) && !categoryByPath[match.path] && category) {
      // An unscoped rule inherits the visible page section.  Keep the
      // section in the storage key too: labels such as “卖点” may occur in
      // both 规格 and 图文, and must remain two independently reviewable rows.
      const path = customPath(label, category);
      customFields.set(path, { label, category, rulePath: match.path });
      assign(path, value, true, pendingControl);
      return;
    }
    assign(match.path, value, true, pendingControl);
  };
  // Only pairs extracted from a semantic field container are accepted here.
  // Never infer a value from arbitrary page prose such as a help tip, rule,
  // or another SKU row that happens to look like “字段：文字”.
  for (const pair of labelledValues || []) {
    if (!pair || typeof pair.label !== 'string' || !Object.hasOwn(pair, 'visibleValue')) continue;
    const label = normalizeFieldLabel(pair.label);
    if (sensitiveLabel(label)) continue;
    const match = resolvePath(label, pair.category);
    if (match) assignMatched(match, label, pair.category, pair.visibleValue);
    else if (pair.category) addCustomField(label, pair.category, pair.visibleValue);
  }
  // interactive values have no stable labels. Only caller-extracted explicit
  // visible label associations are safe; never join by index or proximity.
  for (const control of visibleControls || []) {
    if (!control || typeof control.label !== 'string') continue;
    // Form UIs commonly render a label as "颜色：" (and some insert a
    // space before the punctuation).  That punctuation decorates the label;
    // it is not an empty field value.
    const controlLabel = normalizeFieldLabel(control.option && control.groupLabel ? control.groupLabel : control.label);
    if (sensitiveLabel(control.label)) continue;
    const match = resolvePath(controlLabel, control.category);
    // A label relationship is stronger evidence than static prose. This also
    // prevents a nearby help line from winning over the selected control.
    if (match && Object.hasOwn(control, 'visibleValue')) assignMatched(match, controlLabel, control.category, control.visibleValue, control.pending === true);
    else if (!match && control.category && Object.hasOwn(control, 'visibleValue')) addCustomField(controlLabel, control.category, control.visibleValue, control.pending === true);
  }
  for (const [label, path] of [['主图','media.mainImage'],['商品主图','media.mainImage'],['详情图','media.detailImages'],['详情图片','media.detailImages']]) {
    // A same-named image in another panel (for example a logistics template
    // thumbnail) is not evidence for a product image field.
    const related=(visibleImages||[]).filter(image=>normalizeFieldLabel(image.label)===label && image.category === '图文');
    const unique=[...new Map(related.map(image=>[image.key,image])).values()];
    if(unique.length)assign(path,`${unique.length}张可见图片预览`);
  }
  return { source: pageSource, fields, customFields: [...customFields.entries()].map(([path, value]) => ({ path, ...value })) };
}
function makeRow(category, field, status, value, source, manual_action = '') { return { category, field, status, visible_value: value == null || (typeof value === 'string' && !value.trim()) || (Array.isArray(value) && value.length === 0) ? '' : value, source, manual_action }; }
function fieldStatus(value, present, expectedValues = [], pendingControl = false) {
  if (expectedValues.length > 1) return '冲突';
  if (!present || pendingControl) return '待确认';
  if (Array.isArray(value) && value.length === 0) return '缺项';
  const values = Array.isArray(value) ? value : [value];
  if (values.every(pending)) return '待确认';
  if (values.every(missing)) return '缺项';
  if (values.some(item => pending(item) || missing(item))) return '待确认';
  const conflict = expectedValues.some(expected => values.some(item => String(item) !== expected));
  return conflict ? '冲突' : '已见';
}
function check(page, rules) {
  validateRulePaths(rules);
  const requirements = ruleRequirements(rules);
  const rows = []; let total = 0;
  const add = value => { total += 1; if (rows.length < MAX_ROWS) rows.push(value); };
  const knownPaths = new Set(visibleFields.map(([, , path]) => path));
  for (const [category, label, path] of visibleFields) {
    const item = pageValue(page, path);
    const matching = requirements.filter(rule => ruleField(rule) === path);
    const expectedValues = [...new Set(matching.filter(rule => rule.expected !== undefined).map(rule => String(rule.expected)))];
    const status = fieldStatus(item.value, get(page.fields || {}, path) !== undefined, expectedValues, item.pending === true);
    const action = status === '待确认' ? pendingRuleAction(label, matching)
      : status === '缺项' ? missingRuleAction(label, matching)
        : status === '冲突' ? conflictRuleAction(label, matching) : '';
    add(makeRow(category, label, status, item.value, addSource(sourceFor(item, page.source), ...matching.map(rule => rule.source || '用户提供的商家规则')), action));
  }
  const dynamicPagePaths = new Set();
  for (const field of page.customFields || []) {
    dynamicPagePaths.add(field.path);
    if (field.rulePath) dynamicPagePaths.add(field.rulePath);
    const item = pageValue(page, field.path);
    const valuePresent = get(page.fields || {}, field.path) !== undefined;
    // A page label can have been mapped to a dynamic rule path even when the
    // rule omitted `category`.  Compare that visible value to the rule here,
    // rather than treating it as an unrelated custom field and losing a
    // required-value conflict.
    const matching = requirements.filter(rule => ruleField(rule) === field.path || ruleField(rule) === field.rulePath);
    const expectedValues = [...new Set(matching.filter(rule => rule.expected !== undefined).map(rule => String(rule.expected)))];
    const status = fieldStatus(item.value, valuePresent, expectedValues, item.pending === true);
    const action = status === '待确认' ? pendingRuleAction(field.label, matching)
      : status === '缺项' ? missingRuleAction(field.label, matching)
        : status === '冲突' ? conflictRuleAction(field.label, matching) : '';
    add(makeRow(field.category, field.label, status, item.value,
      addSource(sourceFor(item, page.source), ...matching.map(rule => rule.source || '用户提供的商家规则')), action));
  }
  const dynamicGroups = new Map();
  for (const rule of requirements) {
    const field = ruleField(rule);
    if (field === undefined || knownPaths.has(field) || dynamicPagePaths.has(field)) continue;
    if (!dynamicGroups.has(field)) dynamicGroups.set(field, []);
    dynamicGroups.get(field).push(rule);
  }
  for (const [path, matching] of dynamicGroups) {
    const first = matching[0], label = first.label || path, category = first.category || '商家规则';
    const item = pageValue(page, path), valuePresent = get(page.fields || {}, path) !== undefined;
    const expectedValues = [...new Set(matching.filter(rule => rule.expected !== undefined).map(rule => String(rule.expected)))];
    const status = fieldStatus(item.value, valuePresent, expectedValues, item.pending === true);
    const action = status === '待确认' ? pendingRuleAction(label, matching)
      : status === '缺项' ? missingRuleAction(label, matching)
        : status === '冲突' ? conflictRuleAction(label, matching) : '';
    add(makeRow(category, label, status, item.value, addSource(sourceFor(item, page.source), ...matching.map(rule => rule.source || '用户提供的商家规则')), action));
  }
  return { mode: 'read-only', notice: '仅基于可见资料与用户提供规则；不可见字段留空，未提供规则不推断；未保存或上架。', sources: [...new Set(rows.map(r => r.source))], rows, total_candidate_rows: total, truncated: total > MAX_ROWS, next_batch: total > MAX_ROWS ? `结果超过${MAX_ROWS}行，请分批提供规则或页面资料后继续检查。` : '' };
}
async function main() {
  const offline = arg('--offline-page'), output = arg('--output');
  const ruleFile = arg('--rules'); const rules = ruleFile ? JSON.parse(await readFile(ruleFile, 'utf8')) : null;
  validateRulePaths(rules);
  let page;
  if (offline) page = JSON.parse(await readFile(offline, 'utf8'));
  else {
    const browserId = arg('--browser-id'), pageUrl = arg('--page-url');
    if (!browserId || !pageUrl) throw new Error('请提供 --browser-id 与 --page-url；本工具只打开自己的任务页面，不接管已有 tabId。');
    if (!/^https?:\/\//i.test(pageUrl)) throw new Error('商品编辑页必须是用户指定的 HTTP(S) URL。');
    const bridgeUrl = process.env.EASY_WEBBRIDGE_URL || 'http://127.0.0.1:17777';
    const tokenPath = process.env.EASY_WEBBRIDGE_TOKEN_FILE || join(homedir(), '.easy-webbridge', 'bridge-token');
    const token = (process.env.EASY_WEBBRIDGE_TOKEN || await readFile(tokenPath, 'utf8').catch(() => '')).trim();
    if (!token) throw new Error('没有找到 EasyBR 内置 Bridge token；请先启动 EasyBR。');
    const session = `shop-listing-missing-fields-free-${randomUUID()}`;
    const call = async args => {
      // The checked-in self-test uses this fixture CLI adapter. Production runs
      // use EasyBR's built-in HTTP API below and never require the CLI.
      if (process.env.LISTING_TEST_MODE && process.env.EASY_WEBBRIDGE_CLI && existsSync(process.env.EASY_WEBBRIDGE_CLI)) {
        const r = spawnSync('node', [process.env.EASY_WEBBRIDGE_CLI, ...args], { encoding: 'utf8', timeout: 30000 });
        if (r.status !== 0) throw new Error('Easy WebBridge 命令失败；未作商品写入。');
        const fixture = JSON.parse(r.stdout);
        if (fixture.ok !== true) throw new Error('Easy WebBridge 没有确认命令成功。');
        return fixture.result;
      }
      let action, commandArgs;
      if (args[0] === 'command') {
        action = args[2];
        commandArgs = JSON.parse(args[3] || '{}');
      } else if (args[0] === 'snapshot') {
        action = 'snapshot';
        commandArgs = { tabId: Number(args[2]), visibility: args[4], textMode: args[6] };
      } else throw new Error('不支持的 Easy WebBridge 操作。');
      const response = await fetch(`${bridgeUrl}/v1/browsers/${encodeURIComponent(browserId)}/commands`, {
        method: 'POST',
        headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' },
        body: JSON.stringify({ action, args: commandArgs }),
        signal: AbortSignal.timeout(30000),
      });
      const parsed = await response.json();
      if (!response.ok) throw new Error('Easy WebBridge 命令失败；未作商品写入。');
      if (parsed.ok !== true) throw new Error('Easy WebBridge 没有确认命令成功。');
      return parsed.result;
    };
    let opened = false, ownedTabConfirmed = false, tabId, originalScrollTop;
    try {
      const nav = await call(['command', browserId, 'navigate', JSON.stringify({url:pageUrl,newTab:true,session,groupTitle:'商品缺项检查'})]);
      opened = true;
      tabId = Number(nav.tabId);
      if (!Number.isInteger(tabId)) throw new Error('导航没有返回有效标签页编号。');
      const deadline = Date.now() + 15000;
      while (true) {
        const tabsResult = await call(['command', browserId, 'list_tabs', JSON.stringify({session})]);
        const tabs = Array.isArray(tabsResult) ? tabsResult : tabsResult?.tabs;
        const tab = Array.isArray(tabs) ? tabs.find(t => Number(t.id) === tabId) : null;
        if (!tab) throw new Error('返回页面不属于本次任务标签组。');
        ownedTabConfirmed = true;
        const status = String(tab.status || '').toLowerCase();
        if (['complete', 'loaded', 'ready'].includes(status)) break;
        if (!['loading', 'pending', 'navigating'].includes(status)) throw new Error('页面加载状态缺失或未知；未读取未完成的快照。');
        if (Date.now() >= deadline) throw new Error('页面仍在加载；等待超时，未读取未完成的快照。');
        await new Promise(resolve => setTimeout(resolve, 250));
      }
      let shot, previousSignature = '', stableSamples = 0, stableSince = 0;
      const stableDeadline = Date.now() + 12000;
      const testFastStabilization = process.env.LISTING_TEST_FAST_STABLE_WAIT === '1';
      const requiredStableSamples = testFastStabilization ? 1 : 3;
      const requiredStableMs = testFastStabilization ? 0 : 900;
      const pollIntervalMs = testFastStabilization ? 10 : 300;
      while (Date.now() < stableDeadline) {
        shot = await call(['snapshot', browserId, String(tabId), '--visibility', 'visible', '--text-mode', 'page']);
        if (!shot || typeof shot !== 'object') throw new Error('快照结果无效，不能把包装 JSON 当页面证据。');
        if (shot.textTruncated || shot.truncated || shot.budgetTruncated) throw new Error('暂停：页面快照截断，请缩小检查范围后分批处理，未把未读取字段判缺项。');
        if (!Array.isArray(shot.interactive)) throw new Error('快照缺少 result.interactive；不能从包装文本或模拟 HTML 猜测控件值。');
        const readiness = await call(['command', browserId, 'evaluate', JSON.stringify({tabId, code: '({readyState:document.readyState,busy:[...document.querySelectorAll("[aria-busy=\"true\"],[role=\"progressbar\"],[data-loading=\"true\"]")].filter(el=>{const r=el.getBoundingClientRect(),s=getComputedStyle(el);return r.width>0&&r.height>0&&s.display!=="none"&&s.visibility!=="hidden"}).length})'})]);
        if (!readiness || !['interactive','complete'].includes(readiness.readyState) || !Number.isFinite(readiness.busy)) throw new Error('页面异步状态不可读；未扫描可能尚未回填的字段。');
        const signature = JSON.stringify({text: shot.text || '', interactive: shot.interactive.map(({tag,role,text,value,visible,disabled}) => [tag,role,text,value,visible,disabled])});
        // `complete` only describes the document; product-editor SPAs can
        // still be filling fields. Do not treat arbitrary page copy such as
        // “图片加载失败说明” as a loading state. This narrow fallback is used
        // only for a snapshot that is solely a loading-status message and
        // has not exposed any interactive evidence yet.
        const snapshotText = String(shot.text || '').trim().replace(/\s+/gu, ' ');
        const businessLoading = shot.interactive.length === 0
          && /^(?:(?:商品信息|商品数据)?(?:正在加载|加载中)|加载数据|数据加载中|loading(?:\.{3}|…)?)[.!。…]*$/iu.test(snapshotText);
        if (readiness.busy === 0 && !businessLoading && signature === previousSignature) stableSamples += 1;
        else { previousSignature = signature; stableSamples = 0; stableSince = Date.now(); }
        if (readiness.busy === 0 && !businessLoading && stableSamples >= requiredStableSamples && Date.now() - stableSince >= requiredStableMs) break;
        if (Date.now() >= stableDeadline) throw new Error('商品编辑页面字段未稳定回填；等待超时，未生成缺项表。');
        await new Promise(resolve => setTimeout(resolve, pollIntervalMs));
      }
      if (!shot || typeof shot !== 'object') throw new Error('快照结果无效，不能把包装 JSON 当页面证据。');
      if (typeof shot.url !== 'string' || !samePageIdentity(shot.url, pageUrl)) throw new Error('快照最终页面与用户指定的商品编辑页不一致；未读取或输出检查表。');
      const initialPageIdentity = pageIdentity(shot.url);
      const initial = await call(['command', browserId, 'evaluate', JSON.stringify({tabId, code: '({pageHeight:Math.max(document.documentElement.scrollHeight,document.body?.scrollHeight||0),viewportHeight:document.documentElement.clientHeight,scrollTop:window.scrollY})'})]);
      if (!initial || !Number.isFinite(initial.pageHeight) || !Number.isFinite(initial.viewportHeight) || initial.viewportHeight <= 0) throw new Error('页面高度信息不可读；未把未扫描区域判为缺项。');
      if (!Number.isFinite(initial.scrollTop)) throw new Error('初始滚动位置不可读；未开始页面扫描。');
      // Keep the original position until the outer cleanup.  A visibility
      // read can fail mid-scan too, and `scroll` is relative (scrollBy), so
      // restoration must calculate a fresh delta on every exit path.
      originalScrollTop = initial.scrollTop;
      const maxViewports = 20, stride = Math.max(1, Math.floor(initial.viewportHeight * 0.8));
      const positions = [];
      for (let y = 0; y < Math.max(1, initial.pageHeight); y += stride) positions.push(y);
      const lastY = Math.max(0, initial.pageHeight - initial.viewportHeight);
      if (!positions.includes(lastY)) positions.push(lastY);
      positions.sort((a,b)=>a-b);
      if (positions.length > maxViewports) throw new Error(`页面过长，超过只读扫描上限 ${maxViewports} 屏；未生成不完整缺项表。`);
      const textParts = [], pairsByKey = new Map(), controlsByKey = new Map(), imagesByKey = new Map();
      const assertCurrentPage = async () => {
        const currentUrl = await call(['command',browserId,'evaluate',JSON.stringify({tabId,code:'location.href'})]);
        if (typeof currentUrl !== 'string' || !samePageIdentity(currentUrl, pageUrl) || pageIdentity(currentUrl) !== initialPageIdentity) throw new Error('扫描过程中商品编辑页身份发生变化；已停止并丢弃混合页面结果。');
      };
      const scanCode = `(() => {
        const shown = el => { const r=el.getBoundingClientRect(), vw=document.documentElement.clientWidth, vh=document.documentElement.clientHeight;
          for(let node=el;node&&node.nodeType===1;node=node.parentElement){const s=getComputedStyle(node);if(s.display==='none'||s.visibility==='hidden'||Number(s.opacity)===0||s.contentVisibility==='hidden')return false;}
          if(r.width<=0||r.height<=0||r.right<=0||r.bottom<=0||r.left>=vw||r.top>=vh)return false;
          const x=Math.min(vw-1,Math.max(0,r.left+r.width/2)),y=Math.min(vh-1,Math.max(0,r.top+r.height/2)),hit=document.elementFromPoint(x,y);return !!hit&&(hit===el||el.contains(hit)||(hit.matches?.('label[for]')&&hit.contains(el))); };
        // view returns only rendered, hit-testable text. Do not use
        // textContent for labels: hidden descendants can otherwise leak.
        // DOM paths are deliberately not cross-viewport evidence identities:
        // virtual SKU tables recycle row nodes while their visible SKU data
        // changes. They are retained only as a local fallback.
        const nodeKey = el => {const parts=[];for(let node=el;node&&node.nodeType===1&&parts.length<10;node=node.parentElement){const parent=node.parentElement,index=parent?[...parent.children].indexOf(node):0;parts.push((node.id?'#'+node.id:node.tagName)+':'+index);}return parts.reverse().join('/');};
        const view = node => {
          if(node.nodeType===Node.TEXT_NODE){const value=node.nodeValue||'';if(!value.trim())return '';const range=document.createRange();range.selectNodeContents(node);const rects=[...range.getClientRects()],vw=document.documentElement.clientWidth,vh=document.documentElement.clientHeight;
            const visible=rects.some(r=>{if(r.width<=0||r.height<=0||r.right<=0||r.bottom<=0||r.left>=vw||r.top>=vh)return false;const x=Math.min(vw-1,Math.max(0,r.left+r.width/2)),y=Math.min(vh-1,Math.max(0,r.top+r.height/2)),hit=document.elementFromPoint(x,y);return !!hit&&(hit===node.parentElement||node.parentElement?.contains(hit));});if(!visible)return '';
            for(let el=node.parentElement;el&&el.nodeType===1;el=el.parentElement){const s=getComputedStyle(el);if(s.display==='none'||s.visibility==='hidden'||Number(s.opacity)===0||s.contentVisibility==='hidden')return ''; }return value;}
          if(node.nodeType!==Node.ELEMENT_NODE)return '';const el=node,tag=el.tagName;if(['SCRIPT','STYLE','NOSCRIPT','TEMPLATE','SVG'].includes(tag))return '';const s=getComputedStyle(el);if(s.display==='none'||s.visibility==='hidden'||Number(s.opacity)===0||s.contentVisibility==='hidden')return '';const content=[...el.childNodes].map(view).join('');return /^(block|flow-root|flex|grid|table-row|list-item)$/u.test(s.display)||/^(DIV|P|LI|TR|SECTION|ARTICLE|HEADER|FOOTER|H[1-6]|DT|DD|HR|BR)$/u.test(tag)?'\\n'+content+'\\n':content;
        };
        // Labels and section names must come from rendered text, never from
        // aria-label/data attributes or textContent (which can expose hidden
        // metadata and visually hidden descendants).
        const text = el => view(el).trim();
        // A rendered row signature distinguishes different virtualized SKU
        // records even when the browser reuses the same DOM node path.
        const rowEvidenceKey = el => {const row=el.closest('tr,[role="row"],[data-sku-id],[data-row-key],li');return row&&shown(row)?text(row).replace(/\s+/gu,' ').slice(0,500):'';};
        const labelFor = el => {const direct=el.closest('label'),id=el.id,linked=id?document.querySelector('label[for="'+CSS.escape(id)+'"]'):null,aria=(el.getAttribute('aria-labelledby')||'').split(/\\s+/).filter(Boolean).map(x=>document.getElementById(x)).filter(node=>node&&shown(node)).map(text).filter(Boolean).join(' ');return (direct&&shown(direct)?text(direct):'')||(linked&&shown(linked)?text(linked):'')||aria;};
        const categoryFor = node => {for(let parent=node;parent&&parent.nodeType===1;parent=parent.parentElement){const heading=parent.querySelector(':scope > legend,:scope > h1,:scope > h2,:scope > h3,:scope > [class*="title"]'),hint=heading&&shown(heading)?text(heading):'';if(/规格|SKU|属性/u.test(hint))return '规格';if(/图文|图片|媒体|详情/u.test(hint))return '图文';if(/物流|配送|发货/u.test(hint))return '物流';if(/售后|退货|保障|服务/u.test(hint))return '售后';}return '';};
        const sensitive = value => /password|token|secret|api[_ -]?key|credential|访问密钥|密钥|令牌|口令|凭据/i.test(String(value||''));
        const controls=[...document.querySelectorAll('input:not([type="file"]),textarea,select,[role="textbox"],[role="combobox"],[role="checkbox"],[role="radio"],[contenteditable]:not([contenteditable="false"])')].filter(shown).map(el=>{
          // Resolve the rendered label before reading any control value.  A
          // harmless-looking text input may be labelled “API Token” through
          // label[for] or aria-labelledby, so type/name/id checks alone are
          // never a sufficient credential filter.
          const label=labelFor(el),attributeHint=(el.name||'')+' '+(el.id||'')+' '+(el.getAttribute('autocomplete')||'');
          if(!label||sensitive(label)||el.matches('input[type="password"]')||sensitive(attributeHint))return null;
          if(el.matches('input[type="checkbox"],input[type="radio"],[role="checkbox"],[role="radio"]')){if(!(el.checked||el.getAttribute('aria-checked')==='true'))return null;const group=el.closest('fieldset,[role="radiogroup"],[role="group"]'),legend=group?.querySelector(':scope > legend'),labelledby=group?.getAttribute('aria-labelledby')?.split(/\s+/u)||[],labelledText=labelledby.map(id=>document.getElementById(id)).filter(node=>node&&shown(node)).map(node=>view(node).trim()).filter(Boolean).join(' '),groupLabel=(legend&&shown(legend)?text(legend):'')||labelledText;return {label,groupLabel:groupLabel||undefined,category:categoryFor(el),visibleValue:label,option:true,key:nodeKey(el),evidenceKey:rowEvidenceKey(el)};}
          if(el.tagName==='SELECT'){const selectedOptions=[...el.selectedOptions],selected=selectedOptions.filter(option=>!option.disabled&&String(option.value||'').trim()).map(option=>String(option.label||option.text||'').trim()).filter(Boolean),optionText=el.multiple?selected:(selected[0]||''),prompt=el.getAttribute('placeholder')||el.getAttribute('aria-placeholder')||selectedOptions.find(option=>option.disabled||!String(option.value||'').trim())?.label||selectedOptions[0]?.text||'';
            // A disabled selected option is often the visible "请选择…" prompt.
            // Keep the prompt as state only: it is not merchant-entered data.
            return {label,category:categoryFor(el),visibleValue:Array.isArray(optionText)?optionText:(optionText||''),pending:!Array.isArray(optionText)&&!optionText&&Boolean(prompt)};}
          const activeId=el.getAttribute('aria-activedescendant'),active=activeId&&document.getElementById(activeId),selected=el.querySelector('[aria-selected="true"],[role="option"][data-selected="true"]')||active;
          const candidates=[el.value,el.getAttribute('aria-valuetext'),selected&&shown(selected)?view(selected).trim():'',el.getAttribute('aria-selected')==='true'?view(el).trim():'',el.matches('[contenteditable]:not([contenteditable="false"])')?view(el).trim():'',(el.getAttribute('role')==='combobox'||el.getAttribute('role')==='textbox')?view(el).trim():''];
          const raw=candidates.find(value=>String(value??'').trim())??'';const prompt=el.getAttribute('placeholder')||el.getAttribute('aria-placeholder')||'';const hasValue=Boolean(String(raw).trim());return {key:nodeKey(el),evidenceKey:rowEvidenceKey(el),label,category:categoryFor(el),visibleValue:hasValue?String(raw):'',pending:!hasValue&&Boolean(prompt)};
        }).filter(Boolean);
        const interactiveValueSelector='input,textarea,select,[role="textbox"],[role="combobox"],[role="checkbox"],[role="radio"],[contenteditable]:not([contenteditable="false"])';
        const pairs=[...document.querySelectorAll('dl,[data-field-label],[data-field-value],.form-item,.form-row,[role="group"]')].filter(shown).map(box=>{const labelNode=box.querySelector(':scope > dt,:scope > [data-field-label],:scope > [class*="label"],:scope > label');const valueNode=box.querySelector(':scope > dd,:scope > [data-field-value],:scope > [class*="value"]');if(!labelNode||!valueNode||!shown(labelNode)||!shown(valueNode)||valueNode.matches(interactiveValueSelector)||valueNode.querySelector(interactiveValueSelector))return null;const label=view(labelNode).trim().replace(/\\s*[:：]\\s*$/,'').trim(),visibleValue=view(valueNode).trim();if(!visibleValue&&valueNode.querySelector('img'))return null;return label?{key:nodeKey(box),evidenceKey:rowEvidenceKey(box),label,category:categoryFor(box),visibleValue}:null;}).filter(Boolean);
        const imageLabel = el => {for(let n=el;n&&n.nodeType===1;n=n.parentElement){const label=labelFor(n);if(label)return label;}return '';};
        const images=[...document.querySelectorAll('img')].filter(el=>{if(!shown(el)||!el.naturalWidth||!el.naturalHeight||el.naturalWidth<80||el.naturalHeight<80||/upload|placeholder|empty|add|icon|上传|添加|占位|默认/u.test((el.alt||'')+' '+(el.title||'')+' '+(el.className?.baseVal||el.className||'')))return false;for(let node=el;node&&node.nodeType===1;node=node.parentElement)if(node.matches('button,[role="button"]'))return false;return true;}).map(el=>{const label=imageLabel(el),category=categoryFor(el);if(!label||(category&&category!=='图文')||sensitive(label))return null;return {label,category:category||'图文',key:el.currentSrc||el.src||el.alt||el.title||'visible-image',visibleValue:el.alt||el.title||'已显示图片'};}).filter(Boolean);
        return {text:view(document.body).replace(/[\\t\\f\\v ]+/gu,' ').replace(/ *\\n */gu,'\\n').replace(/\\n{2,}/gu,'\\n').trim(),pairs,controls,images};
      })()`;
      for (const y of positions) {
        await assertCurrentPage();
        const current = await call(['command',browserId,'evaluate',JSON.stringify({tabId,code:'window.scrollY'})]);
        if(!Number.isFinite(current))throw new Error('当前滚动位置不可读；未将未扫描区域判缺项。');
        const delta = y - current;
        if(delta)await call(['command', browserId, 'scroll', JSON.stringify({tabId,x:0,y:delta})]);
        await new Promise(resolve=>setTimeout(resolve,100));
        const scan=await call(['command',browserId,'evaluate',JSON.stringify({tabId,code:scanCode})]);
        await assertCurrentPage();
        if(!scan||typeof scan.text!=='string'||!Array.isArray(scan.pairs)||!Array.isArray(scan.controls)||!Array.isArray(scan.images))throw new Error('分屏可见内容读取失败；未将未读取字段判缺项。');
        if(scan.text)textParts.push(scan.text);
        // Prefer rendered row identity over DOM path: a virtualized table can
        // reuse a node for another SKU between two viewports.
        for(const item of scan.pairs){const key=`${item.evidenceKey||item.label}\u0000${item.label}\u0000${JSON.stringify(item.visibleValue)}`;pairsByKey.set(key,item);}
        for(const item of scan.controls){const key=`${item.evidenceKey||`${item.label}\u0000${item.groupLabel||''}`}\u0000${item.label}\u0000${item.groupLabel||''}\u0000${JSON.stringify(item.visibleValue)}`;controlsByKey.set(key,item);}
        for(const item of scan.images){const key=`${item.label}\u0000${item.key}`;imagesByKey.set(key,item);}
      }
      await assertCurrentPage();
      const visibleText=[...new Set(textParts)].join('\n');
      // Do not search arbitrary product copy for “登录后”. Only page identity
      // and standalone access-gate lines can stop a read-only scan.
      const gateLines = visibleText.split(/\r?\n/u).map(line => line.trim()).filter(Boolean);
      const pageIdentityText = `${shot.title || ''}\n${shot.url || ''}`;
      const loginGate = /验证码|滑块|安全验证|风控|captcha|\bsign[ -]?in\b|\/login\b/i.test(pageIdentityText)
        || /(?:^|\s|[-—])登录(?:$|\s|[-—])/u.test(String(shot.title || ''))
        || gateLines.some(line => /^(?:请)?(?:登录|登录后继续|请先登录|账号登录|安全验证|验证码|滑块验证|访问受限|captcha)$/iu.test(line));
      if (loginGate) throw new Error('暂停：页面要求登录或安全验证，未检查、未修改商品。');
      page = pageFromSnapshot(shot, [...pairsByKey.values()], [...controlsByKey.values()], [...imagesByKey.values()], rules);
    } finally {
      if (opened && ownedTabConfirmed && Number.isFinite(originalScrollTop)) {
        const current = await call(['command',browserId,'evaluate',JSON.stringify({tabId,code:'window.scrollY'})]);
        if (!Number.isFinite(current)) throw new Error('扫描后滚动位置不可读；未恢复页面位置。');
        const restoreDelta = originalScrollTop - current;
        if (restoreDelta) await call(['command',browserId,'scroll',JSON.stringify({tabId,x:0,y:restoreDelta})]);
      }
      if (opened && ownedTabConfirmed) {
        const latest = await call(['command',browserId,'list_tabs',JSON.stringify({session})]);
        const tabs = Array.isArray(latest) ? latest : latest?.tabs;
        const ids = Array.isArray(tabs) ? tabs.map(tab=>Number(tab.id)).sort((a,b)=>a-b) : [];
        if (ids.length !== 1 || ids[0] !== tabId) throw new Error('任务标签组已包含其他页面或归属无法确认；为避免关闭用户页面，未关闭该标签组。');
        await call(['command', browserId, 'close_session', JSON.stringify({session})]);
      }
    }
  }
  const result = check(page, rules);
  const text = JSON.stringify(result, null, 2) + '\n';
  if (output) await writeFile(output, text); else process.stdout.write(text);
}
main().catch(e => { console.error(e.message); process.exit(1); });
