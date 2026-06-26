#!/usr/bin/env node
/**
 * tag-sync.js
 * 将客户分层结果同步写入 OKKI CRM 客户标签
 *
 * 安全机制:
 *   1. 默认 dry-run 模式（只输出计划，不写入）
 *   2. 写入前备份到 data/tag-backup-{date}.json
 *   3. 先 GET 现有标签，合并后再写入（cus_tag 是全量替换）
 *   4. 只操作分层标签（SEGMENT_TAG_NAMES 白名单），保留非分层标签
 *   5. 500ms 请求间隔，逐个客户写入
 *   6. 开头输出预估 API 调用次数，配额不足提前 abort
 *
 * 用法:
 *   node tag-sync.js                          # dry-run（默认）
 *   node tag-sync.js --confirm                # 实际写入全部变动客户
 *   node tag-sync.js --confirm --limit 3      # 只写入前 3 个（验证用）
 *   node tag-sync.js --confirm --customer C001 # 只写入指定客户
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const ROOT = path.resolve(__dirname, '..');

const DATA_DIR = path.join(ROOT, 'data');
const CONFIG = JSON.parse(fs.readFileSync(path.join(ROOT, 'config/segmentation-rules.json'), 'utf8'));

// ==================== OKKI 认证 ====================
const OKKI_WORKSPACE = process.env.OKKI_WORKSPACE || path.resolve(__dirname, '../../../xiaoman-okki');
const ENV_PATH = process.env.ENV_PATH || path.resolve(__dirname, '../../../.env');
const OKKI_CONFIG_PATH = path.join(OKKI_WORKSPACE, 'api/config.json');
const TOKEN_CACHE_PATH = path.join(OKKI_WORKSPACE, 'api/token.cache');

function loadEnv() {
  if (!fs.existsSync(ENV_PATH)) return;
  const lines = fs.readFileSync(ENV_PATH, 'utf8').split('\n');
  for (const line of lines) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith('#')) continue;
    const eqIdx = trimmed.indexOf('=');
    if (eqIdx < 0) continue;
    const key = trimmed.slice(0, eqIdx).trim();
    let val = trimmed.slice(eqIdx + 1).trim();
    val = val.replace(/^["']|["']$/g, '');
    if (key && val && !process.env[key]) {
      process.env[key] = val;
    }
  }
}

function resolveEnvVars(text) {
  return text.replace(/\$\{([^}]+)\}/g, (_, expr) => {
    if (expr.includes(':-')) {
      const [varName, defaultVal] = expr.split(':-', 2);
      return process.env[varName] || defaultVal;
    }
    return process.env[expr] || '';
  });
}

function getOkkiConfig() {
  loadEnv();
  const raw = fs.readFileSync(OKKI_CONFIG_PATH, 'utf8');
  return JSON.parse(resolveEnvVars(raw));
}

async function getAccessToken(forceRefresh = false) {
  if (!forceRefresh && fs.existsSync(TOKEN_CACHE_PATH)) {
    const cached = JSON.parse(fs.readFileSync(TOKEN_CACHE_PATH, 'utf8'));
    if (cached.expires_at > Date.now() / 1000 + 300) {
      return cached.access_token;
    }
  }

  const config = getOkkiConfig();
  const body = new URLSearchParams({
    client_id: config.clientId,
    client_secret: config.clientSecret,
    grant_type: 'client_credentials',
    scope: config.scope
  });

  const resp = await fetch(`${config.baseUrl}/v1/oauth2/access_token`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: body.toString()
  });

  if (!resp.ok) throw new Error(`Token request failed: ${resp.status}`);
  const data = await resp.json();

  const tokenData = {
    access_token: data.data?.access_token || data.access_token,
    expires_at: Date.now() / 1000 + (data.data?.expires_in || data.expires_in || 28800)
  };

  fs.mkdirSync(path.dirname(TOKEN_CACHE_PATH), { recursive: true });
  fs.writeFileSync(TOKEN_CACHE_PATH, JSON.stringify(tokenData, null, 2));
  return tokenData.access_token;
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

// ==================== 标签映射配置 ====================
// 分层标签名称白名单（只有这些标签会被自动管理，其他标签不会被触碰）
const SEGMENT_TAG_PREFIX = 'SEG:';
const SEGMENT_TAG_NAMES = {
  VIP: `${SEGMENT_TAG_PREFIX}VIP`,
  active: `${SEGMENT_TAG_PREFIX}活跃`,
  normal: `${SEGMENT_TAG_PREFIX}普通`,
  dormant: `${SEGMENT_TAG_PREFIX}休眠`,
  lost: `${SEGMENT_TAG_PREFIX}流失`
};

const ALL_SEGMENT_TAG_NAMES = new Set(Object.values(SEGMENT_TAG_NAMES));

// ==================== OKKI API 调用 ====================
async function okkiGet(endpoint, token, baseUrl) {
  const resp = await fetch(`${baseUrl}${endpoint}`, {
    headers: { Authorization: token }
  });
  if (!resp.ok) throw new Error(`OKKI GET ${endpoint} failed: ${resp.status}`);
  return resp.json();
}

async function okkiPost(endpoint, body, token, baseUrl) {
  const resp = await fetch(`${baseUrl}${endpoint}`, {
    method: 'POST',
    headers: {
      Authorization: token,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(body)
  });
  if (!resp.ok) throw new Error(`OKKI POST ${endpoint} failed: ${resp.status}`);
  return resp.json();
}

/**
 * 获取所有已存在的标签列表（tag_list from companyEnums）
 */
async function getExistingTags(token, baseUrl) {
  const result = await okkiGet('/v1/company/companyEnums', token, baseUrl);
  const tagList = result.data?.tag_list || [];
  return tagList; // [{code: "123", name: "xxx"}, ...]
}

/**
 * 创建新标签（如果不存在）
 */
async function ensureTagExists(tagName, token, baseUrl, existingTags) {
  const found = existingTags.find(t => t.name === tagName);
  if (found) return found.code;

  const result = await okkiPost('/v1/company/pushTag', {
    tag_name: tagName,
    tag_color: getTagColor(tagName)
  }, token, baseUrl);

  const tagId = result.data?.tag_id;
  if (!tagId) throw new Error(`Failed to create tag: ${tagName}`);
  existingTags.push({ code: String(tagId), name: tagName });
  return String(tagId);
}

function getTagColor(tagName) {
  const colorMap = {
    [`${SEGMENT_TAG_PREFIX}VIP`]: '#FF4500',
    [`${SEGMENT_TAG_PREFIX}活跃`]: '#2196F3',
    [`${SEGMENT_TAG_PREFIX}普通`]: '#4CAF50',
    [`${SEGMENT_TAG_PREFIX}休眠`]: '#FF9800',
    [`${SEGMENT_TAG_PREFIX}流失`]: '#9E9E9E'
  };
  return colorMap[tagName] || '#188ae8';
}

/**
 * 获取客户当前标签（通过客户详情）
 * OKKI 客户列表返回的 cus_tag 是标签 ID 数组
 */
async function getCompanyCurrentTags(companyId, token, baseUrl) {
  const result = await okkiPost('/v1/company/list', {
    page_index: 1,
    page_size: 1,
    company_ids: [Number(companyId)]
  }, token, baseUrl);

  const companies = result.data?.list || result.data || [];
  if (companies.length === 0) return null;

  const company = companies[0];
  // cus_tag 可能是 ID 数组或名称数组
  return {
    company_id: company.company_id || company.id,
    company_name: company.name || company.company_name,
    cus_tag: company.cus_tag || [],
    raw: company
  };
}

/**
 * 合并标签: 移除旧的分层标签，加入新的分层标签
 */
function mergeSegmentTag(currentTagIds, newSegmentTagId, existingTags) {
  // 建立 tag_id => tag_name 映射
  const idToName = {};
  for (const t of existingTags) {
    idToName[String(t.code)] = t.name;
  }

  // 过滤掉所有分层标签
  const nonSegmentTags = currentTagIds.filter(id => {
    const name = idToName[String(id)];
    return !name || !ALL_SEGMENT_TAG_NAMES.has(name);
  });

  // 加入新的分层标签
  nonSegmentTags.push(Number(newSegmentTagId));
  return nonSegmentTags;
}

/**
 * 更新客户标签（通过 pushCompanyAndCustomers）
 * ⚠️ cus_tag 是全量替换，必须合并后写入
 */
async function updateCompanyTags(companyId, mergedTagIds, token, baseUrl) {
  const result = await okkiPost('/v1/company/pushCompanyAndCustomers', {
    company_id: Number(companyId),
    cus_tag: mergedTagIds.map(Number),
    customers: [] // 不修改联系人
  }, token, baseUrl);

  return result;
}

// ==================== 主流程 ====================
async function runTagSync(options = {}) {
  const { confirm = false, limit = null, customerId = null } = options;
  const startTime = Date.now();

  console.log('=== tag-sync.js ===');
  console.log(`模式: ${confirm ? '⚠️  CONFIRM (实际写入)' : '🔍 DRY-RUN (只预览)'}`);
  if (limit) console.log(`写入限制: ${limit} 客户`);
  if (customerId) console.log(`指定客户: ${customerId}`);
  console.log('');

  // 1. 加载评分数据
  const scoresPath = path.join(DATA_DIR, 'scores-current.json');
  if (!fs.existsSync(scoresPath)) {
    console.error('[tag-sync] scores-current.json 不存在。请先运行评分流程。');
    process.exit(1);
  }
  const scoresData = JSON.parse(fs.readFileSync(scoresPath, 'utf8'));
  let results = scoresData.results || [];

  // 过滤指定客户
  if (customerId) {
    results = results.filter(r => r.company_id === customerId);
    if (results.length === 0) {
      console.error(`[tag-sync] 客户 ${customerId} 不在评分结果中。`);
      process.exit(1);
    }
  }

  // 只处理有变动的客户（与上一轮对比）
  const changes = scoresData.changes || [];
  const changedIds = new Set(changes.map(c => c.company_id));

  // 如果是首次运行或全量，处理所有客户
  const targetResults = changedIds.size > 0
    ? results.filter(r => changedIds.has(r.company_id))
    : results;

  if (limit) {
    targetResults.splice(limit);
  }

  console.log(`评分客户总数: ${results.length}`);
  console.log(`需要更新标签: ${targetResults.length} 客户`);

  // 2. 预估 API 调用次数
  // 每个客户: 1 GET (获取当前标签) + 1 POST (更新标签) = 2 次
  // 额外: 1 GET (companyEnums) + 最多 5 POST (创建标签)
  const estimatedCalls = targetResults.length * 2 + 1 + 5;
  const quotaLimit = CONFIG.settings.api_quota_limit || 1000;

  console.log(`\n预估 API 调用: ~${estimatedCalls} 次`);
  console.log(`每日配额上限: ${quotaLimit} 次`);

  if (estimatedCalls > quotaLimit * 0.8) {
    console.error(`\n⛔ 预估调用次数 (${estimatedCalls}) 超过配额 80% 阈值 (${Math.floor(quotaLimit * 0.8)})。中止执行。`);
    console.log('建议: 使用 --limit 分批执行。');
    process.exit(1);
  }

  if (!confirm) {
    // Dry-run: 只输出计划
    console.log('\n========== DRY-RUN 预览 ==========');
    for (const r of targetResults) {
      const change = changes.find(c => c.company_id === r.company_id);
      const changeType = change ? change.type : 'new';
      const arrow = changeType === 'upgrade' ? '⬆️' : changeType === 'downgrade' ? '⬇️' : '🆕';
      const tagName = SEGMENT_TAG_NAMES[r.segment] || `${SEGMENT_TAG_PREFIX}${r.segment}`;
      console.log(`${arrow} ${r.company_name} (${r.company_id}): → ${tagName} [${r.segment}, score=${r.total_score}]`);
    }
    console.log('\n✅ Dry-run 完成。使用 --confirm 实际执行写入。');
    console.log(`预计写入 ${targetResults.length} 客户的标签。`);
    return;
  }

  // 3. CONFIRM 模式: 实际写入
  console.log('\n🔐 开始 OKKI 标签同步...');

  const token = await getAccessToken();
  const okkiConfig = getOkkiConfig();
  const baseUrl = okkiConfig.baseUrl;

  // 3a. 获取现有标签列表
  console.log('[tag-sync] 获取 OKKI 标签列表...');
  const existingTags = await getExistingTags(token, baseUrl);
  console.log(`[tag-sync] 现有标签: ${existingTags.length} 个`);

  // 3b. 确保分层标签都已创建
  const segmentTagIds = {};
  for (const [segment, tagName] of Object.entries(SEGMENT_TAG_NAMES)) {
    await sleep(API_INTERVAL_MS);
    const tagId = await ensureTagExists(tagName, token, baseUrl, existingTags);
    segmentTagIds[segment] = tagId;
    console.log(`[tag-sync] 标签 "${tagName}" → ID: ${tagId}`);
  }

  // 3c. 备份当前标签状态
  const backupData = {
    backed_up_at: new Date().toISOString(),
    customers: []
  };

  // 3d. 逐客户处理
  const syncResults = [];
  let successCount = 0;
  let errorCount = 0;
  let apiCallCount = 0;

  for (let i = 0; i < targetResults.length; i++) {
    const r = targetResults[i];
    const targetTagName = SEGMENT_TAG_NAMES[r.segment];
    const targetTagId = segmentTagIds[r.segment];

    if (!targetTagId) {
      console.error(`[tag-sync] ⚠️ 未找到分层 "${r.segment}" 对应的标签 ID，跳过 ${r.company_name}`);
      errorCount++;
      continue;
    }

    console.log(`\n[${i + 1}/${targetResults.length}] ${r.company_name} (${r.company_id})`);

    try {
      // GET 当前标签
      await sleep(API_INTERVAL_MS);
      const currentInfo = await getCompanyCurrentTags(r.company_id, token, baseUrl);
      apiCallCount++;

      if (!currentInfo) {
        console.log(`  ⚠️ OKKI 中未找到客户 ${r.company_id}，跳过`);
        errorCount++;
        syncResults.push({
          company_id: r.company_id,
          status: 'not_found',
          error: 'Company not found in OKKI'
        });
        continue;
      }

      const currentTagIds = currentInfo.cus_tag || [];

      // 备份
      backupData.customers.push({
        company_id: r.company_id,
        company_name: currentInfo.company_name,
        original_tags: [...currentTagIds]
      });

      // 合并标签
      const mergedTagIds = mergeSegmentTag(currentTagIds, targetTagId, existingTags);

      console.log(`  当前标签: [${currentTagIds.join(', ')}]`);
      console.log(`  目标标签: ${targetTagName} (ID: ${targetTagId})`);
      console.log(`  合并后:   [${mergedTagIds.join(', ')}]`);

      // 写入
      await sleep(API_INTERVAL_MS);
      const updateResult = await updateCompanyTags(r.company_id, mergedTagIds, token, baseUrl);
      apiCallCount++;

      if (updateResult.code === 200 || updateResult.code === 0) {
        console.log(`  ✅ 写入成功`);
        successCount++;
        syncResults.push({
          company_id: r.company_id,
          company_name: r.company_name,
          segment: r.segment,
          tag_name: targetTagName,
          tag_id: targetTagId,
          previous_tags: currentTagIds,
          merged_tags: mergedTagIds,
          status: 'success'
        });
      } else {
        console.log(`  ❌ 写入失败: ${JSON.stringify(updateResult)}`);
        errorCount++;
        syncResults.push({
          company_id: r.company_id,
          status: 'failed',
          error: JSON.stringify(updateResult)
        });
      }
    } catch (err) {
      console.error(`  ❌ 错误: ${err.message}`);
      errorCount++;
      syncResults.push({
        company_id: r.company_id,
        status: 'error',
        error: err.message
      });
    }
  }

  // 4. 保存备份
  const dateStr = new Date().toISOString().slice(0, 10);
  const backupPath = path.join(DATA_DIR, `tag-backup-${dateStr}.json`);
  fs.mkdirSync(DATA_DIR, { recursive: true });
  fs.writeFileSync(backupPath, JSON.stringify(backupData, null, 2));
  console.log(`\n[tag-sync] 标签备份已保存: ${backupPath}`);

  // 5. 保存同步结果
  const syncReport = {
    synced_at: new Date().toISOString(),
    mode: 'confirm',
    total_customers: targetResults.length,
    success: successCount,
    errors: errorCount,
    api_calls: apiCallCount,
    duration_ms: Date.now() - startTime,
    results: syncResults
  };

  const reportPath = path.join(DATA_DIR, `tag-sync-report-${dateStr}.json`);
  fs.writeFileSync(reportPath, JSON.stringify(syncReport, null, 2));
  console.log(`[tag-sync] 同步报告已保存: ${reportPath}`);

  // 6. 输出汇总
  console.log('\n========== 同步完成 ==========');
  console.log(`成功: ${successCount}`);
  console.log(`失败: ${errorCount}`);
  console.log(`API 调用: ${apiCallCount} 次`);
  console.log(`耗时: ${Date.now() - startTime}ms`);

  return syncReport;
}

// ==================== CLI ====================
const args = process.argv.slice(2);
const confirm = args.includes('--confirm');
const limitIdx = args.indexOf('--limit');
const limit = limitIdx >= 0 ? parseInt(args[limitIdx + 1]) : null;
const customerIdx = args.indexOf('--customer');
const customerId = customerIdx >= 0 ? args[customerIdx + 1] : null;

runTagSync({ confirm, limit, customerId }).catch(err => {
  console.error(`[tag-sync] 致命错误: ${err.message}`);
  process.exit(1);
});
