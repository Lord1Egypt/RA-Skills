/**
 * quotation-integration.js
 * 
 * 集成模块：将 pricing-engine 的动态定价输出转换为 quotation-workflow 数据格式，
 * 一键生成含动态价格的报价单（PDF/HTML/Excel）。自动记录报价历史。
 * 
 * 环境变量：
 *   DRY_RUN=true        跳过 PDF 生成，输出模拟报价单数据
 *   PRICING_LOG=true    启用日志
 * 
 * API 导出：
 *   generateQuotation(params)  生成完整报价单（PDF + 记录）
 *   previewQuotation(params)   仅计算价格，不生成 PDF
 * 
 * CLI 用法：
 *   node quotation-integration.js generate --customer CUST-001 --name "Acme Corp" --items '[{"sku":"HDMI-2.1-8K-2M","quantity":1000}]' --currency USD
 *   node quotation-integration.js preview --customer CUST-001 --items '[{"sku":"HDMI-2.1-8K-2M","quantity":1000}]' --currency USD --grade B
 */

'use strict';

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// ============================================================
// 路径配置
// ============================================================

const SCRIPTS_DIR = __dirname;
const SKILL_DIR = path.resolve(SCRIPTS_DIR, '..');
const OUTPUT_DIR = path.resolve(SKILL_DIR, 'output');
const DATA_DIR = path.resolve(SKILL_DIR, 'data');
const COUNTER_FILE = path.join(DATA_DIR, 'quotation-counter.json');

const QUOTATION_WORKFLOW_DIR = process.env.QUOTATION_WORKFLOW_ROOT || path.join(__dirname, '..', '..', 'quotation-workflow');
const GENERATE_ALL_SCRIPT = path.join(QUOTATION_WORKFLOW_DIR, 'scripts/generate-all.sh');
const GENERATE_HTML_SCRIPT = path.join(QUOTATION_WORKFLOW_DIR, 'scripts/generate_quotation_html.py');

// ============================================================
// 依赖模块
// ============================================================

const { calculatePrice, calculateBatch, listProducts } = require('./pricing-engine');
const { recordQuote } = require('./price-history');

// ============================================================
// 环境配置
// ============================================================

const DRY_RUN = process.env.DRY_RUN === 'true';
const LOG_ENABLED = process.env.PRICING_LOG === 'true';

const LOG_DIR = path.resolve(SKILL_DIR, 'logs');

function log(msg) {
  if (!LOG_ENABLED) return;
  const line = `[${new Date().toISOString()}] [quotation-integration] ${msg}`;
  console.log(line);
  try {
    if (!fs.existsSync(LOG_DIR)) fs.mkdirSync(LOG_DIR, { recursive: true });
    fs.appendFileSync(path.join(LOG_DIR, 'quotation-integration.log'), line + '\n');
  } catch (_) {}
}

// ============================================================
// 工具函数
// ============================================================

function ensureDir(dir) {
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
}

function nowISO() {
  const now = new Date();
  const offset = 8 * 60;
  const local = new Date(now.getTime() + offset * 60000);
  const pad = (n) => String(n).padStart(2, '0');
  return `${local.getUTCFullYear()}-${pad(local.getUTCMonth() + 1)}-${pad(local.getUTCDate())}T${pad(local.getUTCHours())}:${pad(local.getUTCMinutes())}:${pad(local.getUTCSeconds())}+08:00`;
}

function todayFormatted() {
  const now = new Date();
  const offset = 8 * 60;
  const local = new Date(now.getTime() + offset * 60000);
  const pad = (n) => String(n).padStart(2, '0');
  return `${local.getUTCFullYear()}-${pad(local.getUTCMonth() + 1)}-${pad(local.getUTCDate())}`;
}

function todayCompact() {
  return todayFormatted().replace(/-/g, '');
}

function roundTo(num, decimals) {
  const factor = Math.pow(10, decimals);
  return Math.round(num * factor) / factor;
}

// ============================================================
// 报价单号生成（QT-YYYYMMDD-NNN，当天自增）
// ============================================================

function generateQuotationNo() {
  ensureDir(DATA_DIR);

  let counter = { date: '', seq: 0 };
  if (fs.existsSync(COUNTER_FILE)) {
    try {
      counter = JSON.parse(fs.readFileSync(COUNTER_FILE, 'utf-8'));
    } catch (_) {
      counter = { date: '', seq: 0 };
    }
  }

  const today = todayCompact();
  if (counter.date !== today) {
    counter.date = today;
    counter.seq = 0;
  }

  counter.seq += 1;
  const seqStr = String(counter.seq).padStart(3, '0');

  // 原子写入
  const tmpFile = COUNTER_FILE + '.tmp';
  fs.writeFileSync(tmpFile, JSON.stringify(counter, null, 2));
  fs.renameSync(tmpFile, COUNTER_FILE);

  return `QT-${today}-${seqStr}`;
}

// ============================================================
// 有效期计算（默认 30 天）
// ============================================================

function calculateValidUntil(validDays) {
  const days = validDays || 30;
  const now = new Date();
  const offset = 8 * 60;
  const local = new Date(now.getTime() + offset * 60000);
  local.setUTCDate(local.getUTCDate() + days);
  const pad = (n) => String(n).padStart(2, '0');
  return `${local.getUTCFullYear()}-${pad(local.getUTCMonth() + 1)}-${pad(local.getUTCDate())}`;
}

// ============================================================
// 核心：计算所有 item 的动态价格
// ============================================================

/**
 * 计算所有产品的动态定价
 * @param {Object} params
 * @param {string} params.customerId
 * @param {Array<{sku: string, quantity: number}>} params.items
 * @param {string} [params.currency='USD']
 * @param {string} [params.customerGrade='D']
 * @returns {Promise<Object>} { pricedItems, summary, floorWarnings }
 */
async function calculateAllPrices(params) {
  const { customerId, items, currency = 'USD', customerGrade = 'D' } = params;

  if (!items || !Array.isArray(items) || items.length === 0) {
    throw new Error('Items must be a non-empty array of {sku, quantity}');
  }

  const pricedItems = [];
  const errors = [];
  const floorWarnings = [];
  let totalAmount = 0;
  let totalCost = 0;

  for (const item of items) {
    try {
      const result = await calculatePrice(
        item.sku,
        item.quantity,
        customerGrade,
        currency,
        { customerId, customerName: params.customerName }
      );

      const pricedItem = {
        sku: result.sku,
        model: result.model,
        category: result.category,
        description: getProductDescription(result.sku),
        specification: getProductSpecification(result.sku),
        quantity: result.quantity,
        unitPrice: result.unitPrice,
        totalPrice: result.totalPrice,
        currency: result.currency,
        marginRate: result.marginRate,
        pricingMethod: result.pricingMethod,
        breakdown: result.breakdown,
        floorPriceWarning: result.floorPriceWarning
      };

      pricedItems.push(pricedItem);
      totalAmount += result.totalPrice;
      totalCost += result.breakdown.totalCostLocal * result.quantity;

      if (result.floorPriceWarning) {
        floorWarnings.push({
          sku: result.sku,
          warning: result.floorPriceWarning
        });
      }
    } catch (err) {
      errors.push({ sku: item.sku, quantity: item.quantity, error: err.message });
    }
  }

  const avgMargin = totalAmount > 0
    ? roundTo(((totalAmount - totalCost) / totalAmount) * 100, 2)
    : 0;

  return {
    pricedItems,
    errors,
    floorWarnings,
    summary: {
      itemCount: pricedItems.length,
      errorCount: errors.length,
      totalAmount: roundTo(totalAmount, 2),
      totalCost: roundTo(totalCost, 2),
      averageMargin: avgMargin,
      currency: currency.toUpperCase(),
      hasFloorWarnings: floorWarnings.length > 0
    }
  };
}

// ============================================================
// 产品描述/规格查找（从 products-cost.json）
// ============================================================

const PRODUCTS_COST_FILE = path.resolve(SKILL_DIR, 'config/products-cost.json');
let _productsCache = null;

function loadProductsCost() {
  if (_productsCache) return _productsCache;
  if (!fs.existsSync(PRODUCTS_COST_FILE)) return [];
  const data = JSON.parse(fs.readFileSync(PRODUCTS_COST_FILE, 'utf-8'));
  _productsCache = data.products || [];
  return _productsCache;
}

function getProductDescription(sku) {
  const products = loadProductsCost();
  const p = products.find(x => x.sku.toLowerCase() === sku.toLowerCase());
  return p ? p.description : sku;
}

function getProductSpecification(sku) {
  const products = loadProductsCost();
  const p = products.find(x => x.sku.toLowerCase() === sku.toLowerCase());
  return p ? p.specification : '';
}

// ============================================================
// 转换为 quotation-workflow 数据格式
// ============================================================

/**
 * 将定价结果转换为 quotation-workflow 的 JSON 数据格式
 */
function buildQuotationData(params, pricedItems, quotationNo, floorWarnings) {
  const date = todayFormatted();
  const validUntil = calculateValidUntil(params.validDays);
  const currency = (params.currency || 'USD').toUpperCase();

  // 构建产品列表（quotation-workflow 格式）
  const products = pricedItems.map(item => ({
    description: item.description,
    specification: item.specification,
    quantity: item.quantity,
    unit_price: item.unitPrice
  }));

  // 构建备注
  const noteLines = [];
  noteLines.push('1. Prices are based on current raw material costs and subject to change.');
  noteLines.push(`2. Quotation valid for ${params.validDays || 30} days.`);
  noteLines.push('3. Packaging: Standard export packaging (gift box/kraft box optional).');

  if (floorWarnings.length > 0) {
    noteLines.push('');
    noteLines.push('⚠ PENDING APPROVAL: The following items are priced below the standard margin threshold:');
    for (const fw of floorWarnings) {
      noteLines.push(`   ${fw.sku}: ${fw.warning.reason}`);
    }
  }

  if (params.notes) {
    noteLines.push('');
    noteLines.push(params.notes);
  }

  const quotationData = {
    customer: {
      company_name: params.customerName || params.customerId || 'Customer',
      contact: params.contactName || '',
      email: params.customerEmail || '',
      phone: params.customerPhone || '',
      address: params.customerAddress || ''
    },
    quotation: {
      quotation_no: quotationNo,
      date,
      valid_until: validUntil
    },
    products,
    currency,
    payment_terms: params.paymentTerms || 'T/T 30% deposit, 70% before shipment',
    lead_time: params.leadTime || '15-20 days after deposit',
    freight: params.freight || 0,
    tax: params.tax || 0,
    notes: noteLines.join('\n')
  };

  return quotationData;
}

// ============================================================
// PDF 生成（调用 quotation-workflow）
// ============================================================

/**
 * 调用 quotation-workflow 的 generate-all.sh 生成报价单文件
 * @returns {{ pdfPath: string|null, htmlPath: string|null, files: string[] }}
 */
function generateQuotationFiles(quotationData, quotationNo) {
  if (DRY_RUN) {
    log('DRY_RUN: Skipping PDF generation');
    return {
      pdfPath: null,
      htmlPath: null,
      files: [],
      dryRun: true
    };
  }

  ensureDir(OUTPUT_DIR);

  // 写入临时数据文件
  const dataFilePath = path.join(OUTPUT_DIR, `${quotationNo}-data.json`);
  fs.writeFileSync(dataFilePath, JSON.stringify(quotationData, null, 2));
  log(`Quotation data written: ${dataFilePath}`);

  const generatedFiles = [];

  // 方式 1：生成 HTML（推荐，适合邮件附件）
  try {
    const htmlOutputPath = path.join(OUTPUT_DIR, `${quotationNo}.html`);
    execSync(
      `python3 "${GENERATE_HTML_SCRIPT}" --data "${dataFilePath}" --output "${htmlOutputPath}"`,
      { cwd: OUTPUT_DIR, stdio: 'pipe', timeout: 30000 }
    );
    if (fs.existsSync(htmlOutputPath)) {
      generatedFiles.push(htmlOutputPath);
      log(`HTML generated: ${htmlOutputPath}`);
    }
  } catch (err) {
    log(`HTML generation failed: ${err.message}`);
  }

  // 方式 2：Chrome 导出 PDF
  let pdfPath = null;
  const htmlPath = path.join(OUTPUT_DIR, `${quotationNo}.html`);
  if (fs.existsSync(htmlPath)) {
    try {
      const pdfOutputPath = path.join(OUTPUT_DIR, `${quotationNo}.pdf`);
      const chromeCmd = [
        '"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"',
        '--headless', '--disable-gpu',
        '--print-to-pdf-no-header',
        '--print-to-pdf-no-footer',
        '--paper-width=8.27',
        '--paper-height=11.69',
        '--margin-top=0.4',
        '--margin-bottom=0.4',
        '--margin-left=0.4',
        '--margin-right=0.4',
        `--print-to-pdf="${pdfOutputPath}"`,
        `"file://${htmlPath}"`
      ].join(' ');

      execSync(chromeCmd, { cwd: OUTPUT_DIR, stdio: 'pipe', timeout: 30000 });

      if (fs.existsSync(pdfOutputPath)) {
        pdfPath = pdfOutputPath;
        generatedFiles.push(pdfOutputPath);
        log(`PDF generated: ${pdfOutputPath}`);

        // 添加页码
        const addPageNumbersScript = path.join(QUOTATION_WORKFLOW_DIR, 'scripts/add-pagenumbers.py');
        if (fs.existsSync(addPageNumbersScript)) {
          try {
            const finalPdfPath = path.join(OUTPUT_DIR, `${quotationNo}-Final.pdf`);
            execSync(
              `python3 "${addPageNumbersScript}" "${pdfOutputPath}" "${finalPdfPath}"`,
              { cwd: OUTPUT_DIR, stdio: 'pipe', timeout: 15000 }
            );
            if (fs.existsSync(finalPdfPath)) {
              pdfPath = finalPdfPath;
              generatedFiles.push(finalPdfPath);
              log(`Final PDF with page numbers: ${finalPdfPath}`);
            }
          } catch (pgErr) {
            log(`Page number addition failed: ${pgErr.message}`);
          }
        }
      }
    } catch (pdfErr) {
      log(`Chrome PDF export failed: ${pdfErr.message}`);
    }
  }

  return {
    pdfPath,
    htmlPath: fs.existsSync(htmlPath) ? htmlPath : null,
    files: generatedFiles,
    dryRun: false
  };
}

// ============================================================
// 记录报价历史
// ============================================================

/**
 * 将所有定价结果记录到 price-history
 */
function recordAllQuotes(pricedItems, quotationNo, customerId, currency) {
  const records = [];
  for (const item of pricedItems) {
    try {
      const recordId = recordQuote({
        sku: item.sku,
        quantity: item.quantity,
        unitPrice: item.unitPrice,
        totalPrice: item.totalPrice,
        currency: currency || item.currency,
        customerId: customerId || '',
        quotationNo,
        method: 'quotation-integration',
        pricingMethod: item.pricingMethod,
        marginRate: item.marginRate
      });
      records.push({ sku: item.sku, recordId });
      log(`Quote recorded: ${recordId} for ${item.sku}`);
    } catch (err) {
      log(`Failed to record quote for ${item.sku}: ${err.message}`);
      records.push({ sku: item.sku, error: err.message });
    }
  }
  return records;
}

// ============================================================
// 主 API：generateQuotation
// ============================================================

/**
 * 生成完整报价单
 * 
 * @param {Object} params
 * @param {string} params.customerId              客户 ID
 * @param {string} params.customerName             客户公司名称
 * @param {Array<{sku:string, quantity:number}>} params.items  产品列表
 * @param {string} [params.currency='USD']         币种
 * @param {string} [params.customerGrade='D']      客户等级 (A/B/C/D)
 * @param {string} [params.contactName]            联系人
 * @param {string} [params.customerEmail]          客户邮箱
 * @param {string} [params.customerPhone]          客户电话
 * @param {string} [params.customerAddress]        客户地址
 * @param {string} [params.paymentTerms]           付款条款
 * @param {string} [params.leadTime]               交货期
 * @param {number} [params.freight=0]              运费
 * @param {number} [params.tax=0]                  税费
 * @param {number} [params.validDays=30]           报价有效天数
 * @param {string} [params.notes]                  额外备注
 * 
 * @returns {Promise<Object>} { quotationNo, pdfPath, totalAmount, items, status, ... }
 */
async function generateQuotation(params) {
  if (!params || !params.customerId) {
    throw new Error('customerId is required');
  }
  if (!params.items || !Array.isArray(params.items) || params.items.length === 0) {
    throw new Error('items must be a non-empty array of {sku, quantity}');
  }

  const startTime = Date.now();
  log(`=== generateQuotation: ${params.customerId}, ${params.items.length} items ===`);

  // Step 1: 计算所有产品的动态价格
  const priceResult = await calculateAllPrices(params);

  if (priceResult.pricedItems.length === 0) {
    throw new Error(`All items failed pricing. Errors: ${JSON.stringify(priceResult.errors)}`);
  }

  // Step 2: 生成报价单号
  const quotationNo = generateQuotationNo();
  log(`Quotation No: ${quotationNo}`);

  // Step 3: 确定报价单状态
  const quotationStatus = priceResult.floorWarnings.length > 0
    ? 'pending_approval'
    : 'ready';

  // Step 4: 构建 quotation-workflow 数据
  const quotationData = buildQuotationData(
    params,
    priceResult.pricedItems,
    quotationNo,
    priceResult.floorWarnings
  );

  // Step 5: 生成报价单文件（PDF/HTML）
  const fileResult = generateQuotationFiles(quotationData, quotationNo);

  // Step 6: 记录报价历史
  const historyRecords = recordAllQuotes(
    priceResult.pricedItems,
    quotationNo,
    params.customerId,
    params.currency || 'USD'
  );

  const elapsed = Date.now() - startTime;

  // 构建返回结果
  const result = {
    quotationNo,
    status: quotationStatus,
    pdfPath: fileResult.pdfPath,
    htmlPath: fileResult.htmlPath,
    dataFilePath: DRY_RUN ? null : path.join(OUTPUT_DIR, `${quotationNo}-data.json`),
    totalAmount: priceResult.summary.totalAmount,
    currency: priceResult.summary.currency,
    averageMargin: priceResult.summary.averageMargin,
    items: priceResult.pricedItems.map(item => ({
      sku: item.sku,
      model: item.model,
      description: item.description,
      specification: item.specification,
      quantity: item.quantity,
      unitPrice: item.unitPrice,
      totalPrice: item.totalPrice,
      marginRate: item.marginRate,
      pricingMethod: item.pricingMethod,
      floorWarning: item.floorPriceWarning ? true : false
    })),
    errors: priceResult.errors,
    floorWarnings: priceResult.floorWarnings.map(fw => ({
      sku: fw.sku,
      reason: fw.warning.reason,
      action: fw.warning.action
    })),
    historyRecords,
    generatedFiles: fileResult.files,
    dryRun: DRY_RUN,
    elapsedMs: elapsed,
    generatedAt: nowISO()
  };

  log(`Quotation ${quotationNo} generated in ${elapsed}ms. Status: ${quotationStatus}`);
  return result;
}

// ============================================================
// 主 API：previewQuotation（仅计算价格，不生成 PDF）
// ============================================================

/**
 * 预览报价（仅计算价格，不生成 PDF，不记录历史）
 */
async function previewQuotation(params) {
  if (!params || !params.items || params.items.length === 0) {
    throw new Error('items must be a non-empty array of {sku, quantity}');
  }

  log(`=== previewQuotation: ${params.items.length} items ===`);

  const priceResult = await calculateAllPrices(params);

  return {
    mode: 'preview',
    customerId: params.customerId || null,
    customerGrade: params.customerGrade || 'D',
    currency: priceResult.summary.currency,
    totalAmount: priceResult.summary.totalAmount,
    averageMargin: priceResult.summary.averageMargin,
    items: priceResult.pricedItems.map(item => ({
      sku: item.sku,
      model: item.model,
      description: item.description,
      specification: item.specification,
      quantity: item.quantity,
      unitPrice: item.unitPrice,
      totalPrice: item.totalPrice,
      marginRate: item.marginRate,
      pricingMethod: item.pricingMethod,
      floorWarning: item.floorPriceWarning ? {
        reason: item.floorPriceWarning.reason,
        suggestedPrice: item.floorPriceWarning.suggestedPrice
      } : null,
      breakdown: {
        baseMaterialCost: item.breakdown.baseMaterialCost,
        processingCost: item.breakdown.processingCost,
        copperCost: item.breakdown.copperCost,
        totalCostUsd: item.breakdown.totalCostUsd
      }
    })),
    errors: priceResult.errors,
    hasFloorWarnings: priceResult.summary.hasFloorWarnings,
    previewedAt: nowISO()
  };
}

// ============================================================
// CLI 入口
// ============================================================

function parseCliArgs(args) {
  const parsed = {};
  let i = 0;
  while (i < args.length) {
    const arg = args[i];
    if (arg.startsWith('--')) {
      const key = arg.slice(2);
      const val = args[i + 1];
      if (val && !val.startsWith('--')) {
        parsed[key] = val;
        i += 2;
      } else {
        parsed[key] = true;
        i += 1;
      }
    } else {
      i += 1;
    }
  }
  return parsed;
}

async function cli() {
  const args = process.argv.slice(2);
  const cmd = args[0];
  const opts = parseCliArgs(args.slice(1));

  try {
    switch (cmd) {
      case 'generate': {
        if (!opts.customer) {
          console.log('Usage: quotation-integration.js generate --customer <ID> --name <NAME> --items <JSON> [--currency USD] [--grade D]');
          console.log('');
          console.log('Example:');
          console.log('  node quotation-integration.js generate \\');
          console.log('    --customer CUST-001 \\');
          console.log('    --name "Acme Corp" \\');
          console.log('    --items \'[{"sku":"HDMI-2.1-8K-2M","quantity":1000}]\' \\');
          console.log('    --currency USD --grade B');
          process.exit(1);
        }

        let items;
        try {
          items = JSON.parse(opts.items || '[]');
        } catch (e) {
          console.error(`Invalid JSON for --items: ${e.message}`);
          process.exit(1);
        }

        const result = await generateQuotation({
          customerId: opts.customer,
          customerName: opts.name || opts.customer,
          items,
          currency: opts.currency || 'USD',
          customerGrade: opts.grade || 'D',
          contactName: opts.contact,
          customerEmail: opts.email,
          customerPhone: opts.phone,
          customerAddress: opts.address,
          paymentTerms: opts['payment-terms'],
          leadTime: opts['lead-time'],
          freight: opts.freight ? parseFloat(opts.freight) : 0,
          validDays: opts['valid-days'] ? parseInt(opts['valid-days'], 10) : 30,
          notes: opts.notes
        });

        console.log('\n=== 报价单生成完成 ===');
        console.log(`报价单号:   ${result.quotationNo}`);
        console.log(`状态:       ${result.status}${result.status === 'pending_approval' ? ' ⚠️ (需人工确认)' : ''}`);
        console.log(`总金额:     ${result.totalAmount} ${result.currency}`);
        console.log(`平均利润:   ${result.averageMargin}%`);
        console.log(`生成时间:   ${result.generatedAt}`);
        console.log(`耗时:       ${result.elapsedMs}ms`);

        if (result.dryRun) {
          console.log('\n📋 [DRY_RUN] 已跳过 PDF 生成');
        } else {
          console.log('\n📁 生成文件:');
          if (result.pdfPath) console.log(`  PDF:  ${result.pdfPath}`);
          if (result.htmlPath) console.log(`  HTML: ${result.htmlPath}`);
          if (result.dataFilePath) console.log(`  DATA: ${result.dataFilePath}`);
        }

        console.log('\n--- 产品明细 ---');
        for (const item of result.items) {
          const warn = item.floorWarning ? ' ⚠️' : '';
          const method = item.pricingMethod === 'override' ? '(协议价)' : '';
          console.log(`  ${item.sku}: ${item.unitPrice} × ${item.quantity} = ${item.totalPrice} ${result.currency} (利润${item.marginRate}%) ${method}${warn}`);
        }

        if (result.errors.length > 0) {
          console.log('\n--- 错误 ---');
          for (const e of result.errors) {
            console.log(`  ${e.sku}: ${e.error}`);
          }
        }

        if (result.floorWarnings.length > 0) {
          console.log('\n⚠️  底价红线告警:');
          for (const fw of result.floorWarnings) {
            console.log(`  ${fw.sku}: ${fw.reason}`);
          }
          console.log('  报价单状态标记为 pending_approval，需人工确认后发送');
        }

        console.log('\n--- 报价历史记录 ---');
        for (const rec of result.historyRecords) {
          if (rec.error) {
            console.log(`  ${rec.sku}: ERROR ${rec.error}`);
          } else {
            console.log(`  ${rec.sku}: ${rec.recordId}`);
          }
        }

        // JSON 输出（供程序调用）
        if (opts.json === true || opts.json === 'true') {
          console.log('\n--- JSON ---');
          console.log(JSON.stringify(result, null, 2));
        }

        console.log('');
        break;
      }

      case 'preview': {
        let items;
        try {
          items = JSON.parse(opts.items || '[]');
        } catch (e) {
          console.error(`Invalid JSON for --items: ${e.message}`);
          process.exit(1);
        }

        if (items.length === 0) {
          console.log('Usage: quotation-integration.js preview --items <JSON> [--customer ID] [--currency USD] [--grade D]');
          process.exit(1);
        }

        const preview = await previewQuotation({
          customerId: opts.customer,
          customerName: opts.name,
          items,
          currency: opts.currency || 'USD',
          customerGrade: opts.grade || 'D'
        });

        console.log('\n=== 报价预览（不生成文件） ===');
        console.log(`客户 ID:    ${preview.customerId || '(未指定)'}`);
        console.log(`客户等级:   ${preview.customerGrade}`);
        console.log(`总金额:     ${preview.totalAmount} ${preview.currency}`);
        console.log(`平均利润:   ${preview.averageMargin}%`);

        console.log('\n--- 产品明细 ---');
        for (const item of preview.items) {
          const warn = item.floorWarning ? ' ⚠️' : '';
          const method = item.pricingMethod === 'override' ? '(协议价)' : '';
          console.log(`  ${item.sku}: ${item.unitPrice} × ${item.quantity} = ${item.totalPrice} ${preview.currency} (利润${item.marginRate}%) ${method}${warn}`);
          console.log(`    成本: 材料$${item.breakdown.baseMaterialCost} + 加工$${item.breakdown.processingCost} + 铜$${item.breakdown.copperCost} = $${item.breakdown.totalCostUsd}`);
          if (item.floorWarning) {
            console.log(`    ⚠️ ${item.floorWarning.reason}`);
            if (item.floorWarning.suggestedPrice) {
              console.log(`    建议单价: ${item.floorWarning.suggestedPrice.unitPrice} (${item.floorWarning.suggestedPrice.marginRate}%利润)`);
            }
          }
        }

        if (preview.errors.length > 0) {
          console.log('\n--- 错误 ---');
          for (const e of preview.errors) {
            console.log(`  ${e.sku}: ${e.error}`);
          }
        }

        if (opts.json === true || opts.json === 'true') {
          console.log('\n--- JSON ---');
          console.log(JSON.stringify(preview, null, 2));
        }

        console.log('');
        break;
      }

      default:
        console.log('Quotation Integration (quotation-integration.js)');
        console.log('');
        console.log('Commands:');
        console.log('  generate  Generate quotation with dynamic pricing + PDF');
        console.log('  preview   Preview pricing only (no file generation)');
        console.log('');
        console.log('Options:');
        console.log('  --customer <ID>        Customer ID (required for generate)');
        console.log('  --name <NAME>          Customer company name');
        console.log('  --items <JSON>         Products JSON array [{sku, quantity}]');
        console.log('  --currency <CODE>      Currency (USD/EUR/GBP/CNY, default: USD)');
        console.log('  --grade <GRADE>        Customer grade (A/B/C/D, default: D)');
        console.log('  --contact <NAME>       Contact person');
        console.log('  --email <EMAIL>        Customer email');
        console.log('  --phone <PHONE>        Customer phone');
        console.log('  --address <ADDR>       Customer address');
        console.log('  --payment-terms <TEXT>  Payment terms');
        console.log('  --lead-time <TEXT>      Lead time');
        console.log('  --freight <NUM>         Freight cost');
        console.log('  --valid-days <NUM>      Validity period in days (default: 30)');
        console.log('  --notes <TEXT>          Additional notes');
        console.log('  --json                  Output full JSON result');
        console.log('');
        console.log('Env: DRY_RUN=true to skip PDF generation');
        console.log('');
        console.log('Examples:');
        console.log('  # Generate quotation');
        console.log('  node quotation-integration.js generate \\');
        console.log('    --customer CUST-001 --name "Acme Corp" \\');
        console.log('    --items \'[{"sku":"HDMI-2.1-8K-2M","quantity":1000}]\' \\');
        console.log('    --currency USD --grade B');
        console.log('');
        console.log('  # Preview pricing only');
        console.log('  node quotation-integration.js preview \\');
        console.log('    --items \'[{"sku":"HDMI-2.1-8K-2M","quantity":500},{"sku":"DP-2.1-16K-2M","quantity":300}]\' \\');
        console.log('    --grade A');
    }
  } catch (e) {
    console.error(`Error: ${e.message}`);
    process.exit(1);
  }
}

if (require.main === module) {
  cli();
}

// ============================================================
// 导出
// ============================================================

module.exports = {
  generateQuotation,
  previewQuotation
};
