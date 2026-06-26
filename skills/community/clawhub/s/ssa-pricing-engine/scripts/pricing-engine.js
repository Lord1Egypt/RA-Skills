/**
 * pricing-engine.js
 * 
 * 核心定价引擎：整合铜价、汇率、产品成本、折扣规则、利润率目标，
 * 输出最终报价。支持协议价优先、底价红线检查、批量计算。
 * 
 * 环境变量：
 *   DRY_RUN=true       模拟模式（铜价/汇率使用模拟值）
 *   PRICING_LOG=true   启用日志
 * 
 * API 导出：
 *   calculatePrice(sku, quantity, customerGrade, currency, options)
 *   calculateBatch(items, customerGrade, currency, options)
 *   getProductCost(sku)
 *   listProducts()
 * 
 * CLI 用法：
 *   node pricing-engine.js quote <SKU> <QTY> <GRADE> [CURRENCY]
 *   node pricing-engine.js batch <JSON_FILE>
 *   node pricing-engine.js cost <SKU>
 *   node pricing-engine.js products
 */

'use strict';

const fs = require('fs');
const path = require('path');

// ============================================================
// 路径配置
// ============================================================

const CONFIG_DIR = path.resolve(__dirname, '../config');
const LOG_DIR = path.resolve(__dirname, '../logs');

const PRODUCTS_COST_FILE = path.join(CONFIG_DIR, 'products-cost.json');
const DISCOUNT_RULES_FILE = path.join(CONFIG_DIR, 'discount-rules.json');
const MARGIN_RULES_FILE = path.join(CONFIG_DIR, 'margin-rules.json');
const CUSTOMER_OVERRIDES_FILE = path.join(CONFIG_DIR, 'customer-overrides.json');

// ============================================================
// 依赖模块
// ============================================================

const { getRate, convertAmount } = require('./exchange-rate');
const { getCopperPrice, getCopperCostForProduct } = require('./copper-price-adapter');

// ============================================================
// 环境配置
// ============================================================

const LOG_ENABLED = process.env.PRICING_LOG === 'true';

// ============================================================
// 工具函数
// ============================================================

function log(msg) {
  if (!LOG_ENABLED) return;
  const line = `[${new Date().toISOString()}] [pricing-engine] ${msg}`;
  console.log(line);
  try {
    if (!fs.existsSync(LOG_DIR)) fs.mkdirSync(LOG_DIR, { recursive: true });
    fs.appendFileSync(
      path.join(LOG_DIR, 'pricing-engine.log'),
      line + '\n'
    );
  } catch (_) {}
}

function loadJSON(filePath) {
  if (!fs.existsSync(filePath)) {
    throw new Error(`Config file not found: ${filePath}`);
  }
  return JSON.parse(fs.readFileSync(filePath, 'utf-8'));
}

function roundTo(num, decimals) {
  const factor = Math.pow(10, decimals);
  return Math.round(num * factor) / factor;
}

// ============================================================
// 配置加载（带内存缓存）
// ============================================================

let _configCache = null;

function loadConfig() {
  if (_configCache) return _configCache;

  const productsCost = loadJSON(PRODUCTS_COST_FILE);
  const discountRules = loadJSON(DISCOUNT_RULES_FILE);
  const marginRules = loadJSON(MARGIN_RULES_FILE);
  const customerOverrides = loadJSON(CUSTOMER_OVERRIDES_FILE);

  _configCache = {
    products: productsCost.products || [],
    quantityTiers: discountRules.quantity_tiers || [],
    gradeDiscounts: discountRules.customer_grade_discounts || {},
    combinationRule: discountRules.combination_rule || {},
    specialRules: discountRules.special_rules || [],
    marginRules,
    overrides: customerOverrides.overrides || []
  };

  log(`Config loaded: ${_configCache.products.length} products, ${_configCache.overrides.length} overrides`);
  return _configCache;
}

/**
 * 清除配置缓存（用于测试或配置更新后）
 */
function clearConfigCache() {
  _configCache = null;
}

// ============================================================
// 查找产品
// ============================================================

function findProduct(sku) {
  const config = loadConfig();
  const product = config.products.find(
    p => p.sku.toLowerCase() === sku.toLowerCase()
  );
  if (!product) {
    const available = config.products.map(p => p.sku).join(', ');
    throw new Error(`Product not found: ${sku}. Available: ${available}`);
  }
  return product;
}

// ============================================================
// 协议价查询
// ============================================================

/**
 * 查询客户协议价。
 * 匹配条件：customer_id + sku + 有效期内 + 数量达到最低要求
 * 
 * @param {string} sku
 * @param {number} quantity
 * @param {object} options - { customerId }
 * @returns {object|null} 匹配的协议价记录，或 null
 */
function findOverridePrice(sku, quantity, options) {
  if (!options || !options.customerId) return null;

  const config = loadConfig();
  const now = new Date().toISOString().slice(0, 10); // YYYY-MM-DD

  const match = config.overrides.find(o => {
    if (o.customer_id !== options.customerId) return false;
    if (o.sku.toLowerCase() !== sku.toLowerCase()) return false;
    if (o.valid_from && now < o.valid_from) return false;
    if (o.valid_until && now > o.valid_until) return false;
    if (o.min_qty && quantity < o.min_qty) return false;
    return true;
  });

  if (match) {
    log(`Override price found: ${match.customer_id} / ${match.sku} = $${match.agreed_price_usd}`);
  }

  return match || null;
}

// ============================================================
// 折扣计算
// ============================================================

/**
 * 获取数量阶梯折扣百分比
 */
function getQuantityDiscount(quantity) {
  const config = loadConfig();
  const tiers = config.quantityTiers;

  // 从高到低匹配
  for (let i = tiers.length - 1; i >= 0; i--) {
    const tier = tiers[i];
    if (quantity >= tier.min_qty) {
      log(`Quantity tier: ${tier.tier} (${tier.label}), discount ${tier.discount_pct}%`);
      return {
        tier: tier.tier,
        label: tier.label,
        discountPct: tier.discount_pct
      };
    }
  }

  return { tier: 'T0', label: 'Below minimum', discountPct: 0 };
}

/**
 * 获取客户等级折扣百分比
 */
function getGradeDiscount(grade) {
  const config = loadConfig();
  const g = (grade || 'D').toUpperCase();
  const rule = config.gradeDiscounts[g];

  if (!rule) {
    log(`Unknown grade: ${grade}, defaulting to D (0%)`);
    return { grade: g, label: 'Unknown', discountPct: 0 };
  }

  log(`Grade discount: ${g} (${rule.label}), discount ${rule.discount_pct}%`);
  return {
    grade: g,
    label: rule.label,
    discountPct: rule.discount_pct
  };
}

/**
 * 组合折扣计算（multiplicative，带上限）
 */
function calculateCombinedDiscount(quantityDiscountPct, gradeDiscountPct) {
  const config = loadConfig();
  const maxCombined = config.combinationRule.max_combined_discount_pct || 25;

  // 乘法组合: 1 - (1 - q/100) * (1 - g/100)
  const combined = 1 - (1 - quantityDiscountPct / 100) * (1 - gradeDiscountPct / 100);
  let combinedPct = roundTo(combined * 100, 2);

  let capped = false;
  if (combinedPct > maxCombined) {
    log(`Combined discount ${combinedPct}% exceeds max ${maxCombined}%, capping`);
    combinedPct = maxCombined;
    capped = true;
  }

  return {
    combinedDiscountPct: combinedPct,
    capped,
    maxAllowed: maxCombined
  };
}

// ============================================================
// 利润率计算
// ============================================================

/**
 * 获取目标利润率
 */
function getTargetMargin(category, grade, quantity) {
  const config = loadConfig();
  const mr = config.marginRules;

  // 基础利润率（按品类）
  const catMargins = mr.category_margins || {};
  const catRule = catMargins[category] || mr.default_margin;
  let targetPct = catRule.target_pct;
  let minPct = catRule.min_acceptable_pct;

  // 客户等级微调
  const gradeAdj = (mr.grade_margin_adjustment || {})[grade.toUpperCase()] || 0;
  targetPct += gradeAdj;

  // 大单减让
  const volAdj = (mr.volume_margin_adjustment || [])
    .filter(v => quantity >= v.min_qty)
    .reduce((max, v) => Math.max(max, v.margin_reduction_pct), 0);
  targetPct -= volAdj;

  // 不低于 0
  targetPct = Math.max(targetPct, 0);

  log(`Target margin: ${targetPct}% (cat=${category}, grade=${grade}, volAdj=${volAdj})`);

  return {
    targetPct,
    minAcceptablePct: minPct,
    gradeAdjustment: gradeAdj,
    volumeReduction: volAdj
  };
}

// ============================================================
// 底价红线检查
// ============================================================

/**
 * 检查报价是否低于底价红线
 * 
 * @returns {{ triggered: boolean, reason: string|null, details: object }}
 */
function checkFloorPrice(unitPrice, costPrice, marginPct, sku, config) {
  const floorRules = config.marginRules.floor_price;
  if (!floorRules) return { triggered: false, reason: null, details: {} };

  const checks = [];

  // 绝对值检查：单价低于成本
  if (floorRules.absolute && floorRules.absolute.enabled) {
    if (unitPrice < costPrice) {
      checks.push({
        type: 'absolute',
        reason: `Unit price $${unitPrice.toFixed(4)} is below cost $${costPrice.toFixed(4)}`
      });
    }
  }

  // 百分比检查：利润率低于最低线
  if (floorRules.percentage && floorRules.percentage.enabled) {
    const minMarginPct = floorRules.percentage.min_margin_pct || 5;
    if (marginPct < minMarginPct) {
      checks.push({
        type: 'percentage',
        reason: `Margin ${marginPct.toFixed(2)}% is below floor ${minMarginPct}%`
      });
    }
  }

  if (checks.length === 0) {
    return { triggered: false, reason: null, details: {} };
  }

  const trigger = floorRules.on_trigger || {};
  return {
    triggered: true,
    reason: checks.map(c => c.reason).join('; '),
    checks,
    action: trigger.action || 'notify_and_hold',
    discordChannel: trigger.discord_channel || 'pricing-alerts',
    messageTemplate: trigger.message_template || null,
    requireApproval: trigger.require_approval !== false
  };
}

// ============================================================
// 核心定价 API
// ============================================================

/**
 * 计算单个产品报价
 * 
 * @param {string} sku - 产品 SKU
 * @param {number} quantity - 数量
 * @param {string} customerGrade - 客户等级 (A/B/C/D)
 * @param {string} currency - 目标货币 (USD/EUR/GBP/CNY)
 * @param {object} [options] - 额外选项
 * @param {string} [options.customerId] - 客户 ID（用于匹配协议价）
 * @param {string} [options.customerName] - 客户名称（用于红线通知）
 * 
 * @returns {Promise<object>} 报价结果
 */
async function calculatePrice(sku, quantity, customerGrade, currency, options) {
  // 参数校验
  if (!sku || typeof sku !== 'string') {
    throw new Error('Invalid SKU: must be a non-empty string');
  }
  if (!quantity || typeof quantity !== 'number' || quantity < 1) {
    throw new Error(`Invalid quantity: ${quantity}. Must be a positive integer.`);
  }
  const grade = (customerGrade || 'D').toUpperCase();
  if (!['A', 'B', 'C', 'D'].includes(grade)) {
    throw new Error(`Invalid customer grade: ${customerGrade}. Must be A/B/C/D.`);
  }
  const cur = (currency || 'USD').toUpperCase();
  const opts = options || {};

  log(`=== calculatePrice(${sku}, qty=${quantity}, grade=${grade}, cur=${cur}) ===`);

  const config = loadConfig();
  const product = findProduct(sku);

  // ---- Step 1: 检查协议价 ----
  const override = findOverridePrice(sku, quantity, opts);
  if (override) {
    // 协议价直接使用，跳过公式
    let agreedUnitPrice = override.agreed_price_usd;
    let agreedCurrency = override.currency || 'USD';

    // 币种转换（协议价通常是 USD，如果目标不同需转换）
    if (cur !== agreedCurrency) {
      agreedUnitPrice = await convertAmount(agreedUnitPrice, agreedCurrency, cur);
    }

    const totalPrice = roundTo(agreedUnitPrice * quantity, 2);

    // 计算参考利润率（仍需知道成本）
    const copperInfo = getCopperCostForProduct(sku);
    const costUsd = product.base_material_cost_usd
      + product.processing_cost_usd
      + copperInfo.copperCost_usd;
    let costInCur = costUsd;
    if (cur !== 'USD') {
      costInCur = await convertAmount(costUsd, 'USD', cur);
    }
    const refMargin = costInCur > 0
      ? roundTo(((agreedUnitPrice - costInCur) / agreedUnitPrice) * 100, 2)
      : 0;

    // 协议价也做底价红线检查
    const floorCheck = checkFloorPrice(agreedUnitPrice, costInCur, refMargin, sku, config);

    return {
      sku: product.sku,
      model: product.model,
      category: product.category,
      quantity,
      customerGrade: grade,
      currency: cur,
      pricingMethod: 'override',
      override: {
        customerId: override.customer_id,
        customerName: override.customer_name,
        agreedPrice: override.agreed_price_usd,
        agreedCurrency: override.currency || 'USD',
        validFrom: override.valid_from,
        validUntil: override.valid_until
      },
      unitPrice: roundTo(agreedUnitPrice, 4),
      totalPrice,
      marginRate: refMargin,
      floorPriceWarning: floorCheck.triggered ? floorCheck : null,
      breakdown: {
        baseMaterialCost: product.base_material_cost_usd,
        processingCost: product.processing_cost_usd,
        copperCost: copperInfo.copperCost_usd,
        totalCostUsd: roundTo(costUsd, 4),
        totalCostLocal: roundTo(costInCur, 4),
        exchangeRate: cur !== 'USD' ? roundTo(agreedUnitPrice / override.agreed_price_usd, 6) : 1,
        margin: null,
        discount: null,
        note: 'Override price applied. Margin is reference only.'
      }
    };
  }

  // ---- Step 2: 公式定价 ----

  // 2a. 计算成本（USD）
  const copperInfo = getCopperCostForProduct(sku);
  const baseCost = product.base_material_cost_usd;
  const processingCost = product.processing_cost_usd;
  const copperCost = copperInfo.copperCost_usd;
  const totalCostUsd = baseCost + processingCost + copperCost;

  log(`Cost breakdown: base=$${baseCost} + process=$${processingCost} + copper=$${copperCost} = $${totalCostUsd.toFixed(4)}`);

  // 2b. 利润率加成
  const marginInfo = getTargetMargin(product.category, grade, quantity);
  const marginMultiplier = 1 / (1 - marginInfo.targetPct / 100);
  const priceBeforeDiscountUsd = totalCostUsd * marginMultiplier;

  log(`Margin: target=${marginInfo.targetPct}%, multiplier=${marginMultiplier.toFixed(4)}, preBefore=$${priceBeforeDiscountUsd.toFixed(4)}`);

  // 2c. 折扣
  const qtyDiscount = getQuantityDiscount(quantity);
  const gradeDiscount = getGradeDiscount(grade);
  const combinedDiscount = calculateCombinedDiscount(
    qtyDiscount.discountPct,
    gradeDiscount.discountPct
  );

  const discountMultiplier = 1 - combinedDiscount.combinedDiscountPct / 100;
  const unitPriceUsd = priceBeforeDiscountUsd * discountMultiplier;

  log(`Discount: qty=${qtyDiscount.discountPct}%, grade=${gradeDiscount.discountPct}%, combined=${combinedDiscount.combinedDiscountPct}%`);
  log(`Unit price (USD): $${unitPriceUsd.toFixed(4)}`);

  // 2d. 币种转换
  let unitPriceLocal = unitPriceUsd;
  let exchangeRate = 1;
  if (cur !== 'USD') {
    exchangeRate = await getRate('USD', cur);
    unitPriceLocal = roundTo(unitPriceUsd * exchangeRate, 4);
  }

  // 2e. 计算实际利润率
  let totalCostLocal = totalCostUsd;
  if (cur !== 'USD') {
    totalCostLocal = roundTo(totalCostUsd * exchangeRate, 4);
  }
  const actualMarginPct = unitPriceLocal > 0
    ? roundTo(((unitPriceLocal - totalCostLocal) / unitPriceLocal) * 100, 2)
    : 0;

  const totalPrice = roundTo(unitPriceLocal * quantity, 2);

  // 2f. 底价红线检查
  const floorCheck = checkFloorPrice(unitPriceLocal, totalCostLocal, actualMarginPct, sku, config);
  let suggestedPrice = null;
  if (floorCheck.triggered) {
    // 计算建议价格：保证最低 5% 利润率
    const floorMinMargin = (config.marginRules.floor_price.percentage || {}).min_margin_pct || 5;
    const suggestedUnitLocal = roundTo(totalCostLocal / (1 - floorMinMargin / 100), 4);
    suggestedPrice = {
      unitPrice: suggestedUnitLocal,
      totalPrice: roundTo(suggestedUnitLocal * quantity, 2),
      marginRate: floorMinMargin,
      note: `Suggested price at floor margin ${floorMinMargin}%`
    };
    log(`Floor price triggered. Suggested: $${suggestedUnitLocal.toFixed(4)} (${floorMinMargin}% margin)`);
  }

  const result = {
    sku: product.sku,
    model: product.model,
    category: product.category,
    quantity,
    customerGrade: grade,
    currency: cur,
    pricingMethod: 'formula',
    unitPrice: roundTo(unitPriceLocal, 4),
    totalPrice,
    marginRate: actualMarginPct,
    floorPriceWarning: floorCheck.triggered ? {
      ...floorCheck,
      suggestedPrice
    } : null,
    breakdown: {
      baseMaterialCost: baseCost,
      processingCost,
      copperCost: roundTo(copperCost, 4),
      copperPricePerTon: copperInfo.copperPrice_usd_per_ton,
      copperSource: copperInfo.priceSource,
      totalCostUsd: roundTo(totalCostUsd, 4),
      totalCostLocal: roundTo(totalCostLocal, 4),
      margin: {
        targetPct: marginInfo.targetPct,
        actualPct: actualMarginPct,
        minAcceptablePct: marginInfo.minAcceptablePct,
        gradeAdjustment: marginInfo.gradeAdjustment,
        volumeReduction: marginInfo.volumeReduction
      },
      discount: {
        quantityTier: qtyDiscount.tier,
        quantityLabel: qtyDiscount.label,
        quantityDiscountPct: qtyDiscount.discountPct,
        gradeDiscountPct: gradeDiscount.discountPct,
        combinedDiscountPct: combinedDiscount.combinedDiscountPct,
        discountCapped: combinedDiscount.capped
      },
      priceBeforeDiscount: cur !== 'USD'
        ? roundTo(priceBeforeDiscountUsd * exchangeRate, 4)
        : roundTo(priceBeforeDiscountUsd, 4),
      exchangeRate: roundTo(exchangeRate, 6),
      isDryRun: copperInfo.isDryRun,
      isCopperFallback: copperInfo.isFallback
    }
  };

  log(`Result: unitPrice=${result.unitPrice} ${cur}, margin=${actualMarginPct}%, floor=${floorCheck.triggered}`);
  return result;
}

/**
 * 批量计算报价
 * 
 * @param {Array<{sku: string, quantity: number}>} items - 产品列表
 * @param {string} customerGrade - 客户等级
 * @param {string} currency - 目标货币
 * @param {object} [options] - 额外选项
 * 
 * @returns {Promise<object>} { results: [...], errors: [...], summary: {...} }
 */
async function calculateBatch(items, customerGrade, currency, options) {
  if (!Array.isArray(items) || items.length === 0) {
    throw new Error('Items must be a non-empty array of {sku, quantity}');
  }

  log(`=== calculateBatch: ${items.length} items ===`);

  const results = [];
  const errors = [];

  for (const item of items) {
    try {
      const result = await calculatePrice(
        item.sku,
        item.quantity,
        customerGrade,
        currency,
        options
      );
      results.push(result);
    } catch (err) {
      errors.push({
        sku: item.sku,
        quantity: item.quantity,
        error: err.message
      });
    }
  }

  // 汇总
  const totalAmount = results.reduce((sum, r) => sum + r.totalPrice, 0);
  const totalCost = results.reduce((sum, r) => sum + r.breakdown.totalCostLocal * r.quantity, 0);
  const avgMargin = totalAmount > 0
    ? roundTo(((totalAmount - totalCost) / totalAmount) * 100, 2)
    : 0;
  const hasFloorWarnings = results.some(r => r.floorPriceWarning);

  return {
    results,
    errors,
    summary: {
      itemCount: results.length,
      errorCount: errors.length,
      totalAmount: roundTo(totalAmount, 2),
      totalCost: roundTo(totalCost, 2),
      averageMargin: avgMargin,
      currency: (currency || 'USD').toUpperCase(),
      hasFloorWarnings
    }
  };
}

/**
 * 获取产品成本信息（不含利润和折扣）
 */
function getProductCost(sku) {
  const product = findProduct(sku);
  const copperInfo = getCopperCostForProduct(sku);
  const totalCost = product.base_material_cost_usd
    + product.processing_cost_usd
    + copperInfo.copperCost_usd;

  return {
    sku: product.sku,
    model: product.model,
    category: product.category,
    baseMaterialCost: product.base_material_cost_usd,
    processingCost: product.processing_cost_usd,
    copperCost: roundTo(copperInfo.copperCost_usd, 4),
    copperWeight_kg: product.copper_weight_kg,
    copperPricePerTon: copperInfo.copperPrice_usd_per_ton,
    totalCostUsd: roundTo(totalCost, 4),
    moq: product.moq
  };
}

/**
 * 列出所有可报价产品
 */
function listProducts() {
  const config = loadConfig();
  return config.products.map(p => ({
    sku: p.sku,
    model: p.model,
    category: p.category,
    description: p.description,
    specification: p.specification,
    moq: p.moq
  }));
}

// ============================================================
// CLI 入口
// ============================================================

async function cli() {
  const args = process.argv.slice(2);
  const cmd = args[0];

  try {
    switch (cmd) {
      case 'quote': {
        const [, sku, qty, grade, currency] = args;
        if (!sku || !qty || !grade) {
          console.log('Usage: pricing-engine.js quote <SKU> <QTY> <GRADE> [CURRENCY]');
          console.log('Example: pricing-engine.js quote HDMI-2.1-8K-2M 1000 B USD');
          process.exit(1);
        }
        const result = await calculatePrice(
          sku,
          parseInt(qty, 10),
          grade,
          currency || 'USD'
        );

        console.log('\n=== 报价结果 ===');
        console.log(`产品:     ${result.sku} (${result.model})`);
        console.log(`数量:     ${result.quantity}`);
        console.log(`客户等级: ${result.customerGrade}`);
        console.log(`定价方式: ${result.pricingMethod}`);
        console.log(`单价:     ${result.unitPrice} ${result.currency}`);
        console.log(`总价:     ${result.totalPrice} ${result.currency}`);
        console.log(`利润率:   ${result.marginRate}%`);

        if (result.floorPriceWarning) {
          console.log('\n⚠️  底价红线触发!');
          console.log(`原因: ${result.floorPriceWarning.reason}`);
          if (result.floorPriceWarning.suggestedPrice) {
            console.log(`建议单价: ${result.floorPriceWarning.suggestedPrice.unitPrice} ${result.currency}`);
          }
        }

        console.log('\n--- 成本分解 ---');
        const bd = result.breakdown;
        console.log(`材料成本:   $${bd.baseMaterialCost}`);
        console.log(`加工成本:   $${bd.processingCost}`);
        console.log(`铜材成本:   $${bd.copperCost} (铜价 $${bd.copperPricePerTon}/吨, ${bd.copperSource})`);
        console.log(`总成本:     $${bd.totalCostUsd} USD`);
        if (bd.margin) {
          console.log(`目标利润率: ${bd.margin.targetPct}%`);
          console.log(`实际利润率: ${bd.margin.actualPct}%`);
        }
        if (bd.discount) {
          console.log(`数量折扣:   ${bd.discount.quantityDiscountPct}% (${bd.discount.quantityLabel})`);
          console.log(`等级折扣:   ${bd.discount.gradeDiscountPct}%`);
          console.log(`组合折扣:   ${bd.discount.combinedDiscountPct}%${bd.discount.discountCapped ? ' (已截断)' : ''}`);
        }
        if (bd.exchangeRate !== 1) {
          console.log(`汇率:       1 USD = ${bd.exchangeRate} ${result.currency}`);
        }
        if (bd.isDryRun) console.log('模式:       DRY_RUN');
        console.log('');
        break;
      }

      case 'batch': {
        const jsonFile = args[1];
        if (!jsonFile) {
          console.log('Usage: pricing-engine.js batch <JSON_FILE>');
          console.log('JSON format: { "items": [{sku, quantity}], "grade": "B", "currency": "USD" }');
          process.exit(1);
        }
        const input = JSON.parse(fs.readFileSync(jsonFile, 'utf-8'));
        const batchResult = await calculateBatch(
          input.items,
          input.grade || 'D',
          input.currency || 'USD',
          input.options
        );

        console.log('\n=== 批量报价结果 ===');
        console.log(`产品数:   ${batchResult.summary.itemCount}`);
        console.log(`错误数:   ${batchResult.summary.errorCount}`);
        console.log(`总金额:   ${batchResult.summary.totalAmount} ${batchResult.summary.currency}`);
        console.log(`平均利润: ${batchResult.summary.averageMargin}%`);

        if (batchResult.summary.hasFloorWarnings) {
          console.log('⚠️  部分产品触发底价红线');
        }

        console.log('\n--- 明细 ---');
        for (const r of batchResult.results) {
          const warn = r.floorPriceWarning ? ' ⚠️' : '';
          console.log(`  ${r.sku}: ${r.unitPrice} × ${r.quantity} = ${r.totalPrice} ${r.currency} (${r.marginRate}%)${warn}`);
        }
        for (const e of batchResult.errors) {
          console.log(`  ${e.sku}: ERROR ${e.error}`);
        }
        console.log('');
        break;
      }

      case 'cost': {
        const sku = args[1];
        if (!sku) {
          console.log('Usage: pricing-engine.js cost <SKU>');
          process.exit(1);
        }
        const cost = getProductCost(sku);
        console.log('\n=== 产品成本 ===');
        console.log(`SKU:      ${cost.sku} (${cost.model})`);
        console.log(`分类:     ${cost.category}`);
        console.log(`材料:     $${cost.baseMaterialCost}`);
        console.log(`加工:     $${cost.processingCost}`);
        console.log(`铜材:     $${cost.copperCost} (${cost.copperWeight_kg}kg × $${cost.copperPricePerTon}/吨)`);
        console.log(`总成本:   $${cost.totalCostUsd}`);
        console.log(`MOQ:      ${cost.moq}`);
        console.log('');
        break;
      }

      case 'products': {
        const products = listProducts();
        console.log('\n=== 可报价产品 ===\n');
        console.log(
          'SKU'.padEnd(24) +
          'Model'.padEnd(20) +
          'Category'.padEnd(14) +
          'MOQ'
        );
        console.log('-'.repeat(65));
        for (const p of products) {
          console.log(
            p.sku.padEnd(24) +
            p.model.padEnd(20) +
            p.category.padEnd(14) +
            String(p.moq)
          );
        }
        console.log('');
        break;
      }

      default:
        console.log('Pricing Engine (pricing-engine.js)');
        console.log('');
        console.log('Commands:');
        console.log('  quote <SKU> <QTY> <GRADE> [CURRENCY]  Calculate price');
        console.log('  batch <JSON_FILE>                     Batch calculate');
        console.log('  cost <SKU>                            Show product cost');
        console.log('  products                              List all products');
        console.log('');
        console.log('Env: DRY_RUN=true for mock data, PRICING_LOG=true for logging');
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
  calculatePrice,
  calculateBatch,
  getProductCost,
  listProducts,
  clearConfigCache
};
