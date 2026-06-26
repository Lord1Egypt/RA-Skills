/**
 * tracking-extractor.js - 运单号提取器
 *
 * 功能：
 *  - extractTrackingNumbers(text)        从文本中提取所有可能的运单号（带快递商识别）
 *  - extractFromEmail(emailObj)          从邮件对象（subject+body）中提取运单号
 *  - extractFromFile(filePath)           从文件内容中提取运单号
 *  - identifyCarrier(trackingNumber)     识别单个运单号的快递商
 *  - validateTrackingNumber(num, carrier) 验证运单号格式是否匹配指定快递商
 *  - linkToOrder(trackingNumber, ordersPath) 将运单号关联到订单
 *  - processEmailBatch(emails, opts)     批量处理邮件，提取并关联运单号
 *
 * 支持快递商：
 *  DHL / FedEx / UPS / SF Express / EMS / Yanwen / CNE / 4PX
 *  + 通用国际运单号格式 (IATA/UPU)
 *
 * 特性：
 *  - 从邮件正文/主题/附件文本中自动提取运单号
 *  - 多模式正则匹配，覆盖常见格式变体
 *  - 去重 + 置信度评分
 *  - 关联到 order-tracker 订单（按发件人邮件域名匹配）
 *  - 自动注册到 shipment-store
 *  - dry-run 模式
 *  - 可通过 require() 导入
 *
 * 配置文件：../config/logistics-config.json
 *
 * @module tracking-extractor
 */

'use strict';

const fs = require('fs');
const path = require('path');

// ---------------------------------------------------------------------------
// Paths
// ---------------------------------------------------------------------------

const CONFIG_PATH = path.resolve(__dirname, '../config/logistics-config.json');
const ORDER_TRACKER_ORDERS_PATH = path.resolve(
  __dirname,
  '../../order-tracker/data/orders.json'
);

// ---------------------------------------------------------------------------
// Carrier pattern definitions
// Each entry: { code, name, patterns: [{ regex, confidence }], examples }
// Higher confidence = more specific pattern
// ---------------------------------------------------------------------------

const CARRIER_PATTERNS = [
  {
    code: 'ups',
    name: 'UPS',
    patterns: [
      { regex: /\b1Z[A-Z0-9]{16}\b/gi, confidence: 0.95 },
    ],
    examples: ['1Z999AA10123456784'],
  },
  {
    code: 'fedex',
    name: 'FedEx',
    patterns: [
      // FedEx Ground 96-digit barcode (15 digits after 96)
      { regex: /\b96\d{20}\b/g, confidence: 0.92 },
      // FedEx Express 12-digit
      { regex: /\b\d{12}\b/g, confidence: 0.55 },
      // FedEx 15-digit (international)
      { regex: /\b\d{15}\b/g, confidence: 0.60 },
      // FedEx 20-digit
      { regex: /\b\d{20}\b/g, confidence: 0.60 },
      // FedEx 22-digit
      { regex: /\b\d{22}\b/g, confidence: 0.60 },
    ],
    examples: ['123456789012', '9612345678901234567890'],
  },
  {
    code: 'sf',
    name: 'SF Express',
    patterns: [
      { regex: /\bSF\d{12,15}\b/gi, confidence: 0.95 },
      // SF without prefix (13 digits starting with specific ranges)
      { regex: /\b7\d{12}\b/g, confidence: 0.70 },
    ],
    examples: ['SF1234567890123'],
  },
  {
    code: 'ems',
    name: 'EMS / China Post',
    patterns: [
      // UPU S10 format: 2 letters + 8 digits + check digit + 2 letters
      { regex: /\b[A-Z]{2}\d{8}\d[A-Z]{2}\b/gi, confidence: 0.90 },
      // Also matches EE/EM/EA/CP/CX prefix
      { regex: /\b(?:EE|EM|EA|CP|CX|LX|RX|RA|RF|RV)\d{9}(?:CN|HK|TW|US|GB|DE|FR|NL|AU|CA|JP|KR)\b/gi, confidence: 0.93 },
    ],
    examples: ['EA123456789CN', 'EE987654321CN'],
  },
  {
    code: 'dhl',
    name: 'DHL Express',
    patterns: [
      // DHL Express 10-digit
      { regex: /\b\d{10}\b/g, confidence: 0.50 },
      // DHL Express 11-digit
      { regex: /\b\d{11}\b/g, confidence: 0.50 },
      // DHL eCommerce with prefix
      { regex: /\bJD\d{18}\b/gi, confidence: 0.88 },
      // DHL Parcel (Germany)
      { regex: /\b00340\d{17}\b/g, confidence: 0.88 },
    ],
    examples: ['1234567890', '12345678901'],
  },
  {
    code: 'yanwen',
    name: 'Yanwen Logistics',
    patterns: [
      { regex: /\bYW\d{15,20}\b/gi, confidence: 0.95 },
      { regex: /\bUQ\d{12}\b/gi, confidence: 0.88 },
    ],
    examples: ['YW123456789012345'],
  },
  {
    code: 'cne',
    name: 'CNE Express',
    patterns: [
      { regex: /\bCNE\d{10,15}\b/gi, confidence: 0.95 },
    ],
    examples: ['CNE1234567890'],
  },
  {
    code: '4px',
    name: '4PX',
    patterns: [
      { regex: /\b4PX\d{10,15}\b/gi, confidence: 0.95 },
      // 4PX sometimes uses RP/RT prefix
      { regex: /\b(?:RP|RT)\d{13}SG\b/gi, confidence: 0.88 },
    ],
    examples: ['4PX1234567890'],
  },
];

// Context keywords that boost confidence when near a number
const CONTEXT_KEYWORDS = [
  /tracking\s*(?:number|#|no\.?|id)/gi,
  /waybill\s*(?:number|#|no\.?)?/gi,
  /运单\s*[号码]/gi,
  /快递\s*[单号]/gi,
  /shipment\s*(?:id|number|#)/gi,
  /parcel\s*(?:id|number|#)/gi,
  /package\s*(?:id|number|#)/gi,
  /order\s*(?:shipped|dispatched)/gi,
  /shipped\s*via/gi,
  /tracking\s*link/gi,
  /17track/gi,
  /track.*package/gi,
  /dhl|fedex|ups|sf express|ems|yanwen|cne|4px/gi,
];

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

/**
 * Load config from disk (cached)
 */
let _config = null;
function loadConfig() {
  if (_config) return _config;
  try {
    _config = JSON.parse(fs.readFileSync(CONFIG_PATH, 'utf8'));
  } catch (e) {
    _config = { carriers: [] };
  }
  return _config;
}

/**
 * Check if text near a match position contains context keywords
 * @param {string} text Full text
 * @param {number} matchIndex Position of the match
 * @param {number} windowSize Characters to look before/after
 */
function hasContextKeyword(text, matchIndex, windowSize = 120) {
  const start = Math.max(0, matchIndex - windowSize);
  const end = Math.min(text.length, matchIndex + windowSize);
  const context = text.slice(start, end);
  return CONTEXT_KEYWORDS.some((kw) => kw.test(context));
}

/**
 * Deduplicate an array of extraction results by tracking number
 * Keeps the entry with highest confidence
 */
function deduplicateResults(results) {
  const map = new Map();
  for (const r of results) {
    const key = r.trackingNumber.toUpperCase();
    if (!map.has(key) || map.get(key).confidence < r.confidence) {
      map.set(key, r);
    }
  }
  return Array.from(map.values());
}

/**
 * Filter out false positives:
 * - Pure numbers that look like dates (e.g. 20240315)
 * - Phone numbers patterns
 * - Very common number sequences
 */
function looksLikeFalsePositive(num) {
  // Date-like 8-digit numbers
  if (/^20\d{6}$/.test(num) || /^19\d{6}$/.test(num)) return true;
  // All same digits
  if (/^(\d)\1+$/.test(num)) return true;
  // Sequential ascending (1234567890)
  if (num === '1234567890' || num === '0123456789') return true;
  return false;
}

// ---------------------------------------------------------------------------
// Core: identifyCarrier
// ---------------------------------------------------------------------------

/**
 * Identify the carrier for a given tracking number.
 * Returns the best match based on pattern confidence.
 *
 * @param {string} trackingNumber
 * @returns {{ code: string, name: string, confidence: number } | null}
 */
function identifyCarrier(trackingNumber) {
  if (!trackingNumber || typeof trackingNumber !== 'string') return null;
  const num = trackingNumber.trim();

  let best = null;
  for (const carrier of CARRIER_PATTERNS) {
    for (const { regex, confidence } of carrier.patterns) {
      // Reset lastIndex for global regexes
      const r = new RegExp(regex.source, regex.flags);
      const match = r.exec(num);
      if (match && match[0].length === num.length) {
        if (!best || confidence > best.confidence) {
          best = { code: carrier.code, name: carrier.name, confidence };
        }
      }
    }
  }
  return best;
}

// ---------------------------------------------------------------------------
// Core: validateTrackingNumber
// ---------------------------------------------------------------------------

/**
 * Validate a tracking number against a specific carrier's patterns.
 *
 * @param {string} trackingNumber
 * @param {string} carrierCode  e.g. 'dhl', 'fedex', 'ups'
 * @returns {boolean}
 */
function validateTrackingNumber(trackingNumber, carrierCode) {
  if (!trackingNumber || !carrierCode) return false;
  const num = trackingNumber.trim();
  const carrier = CARRIER_PATTERNS.find(
    (c) => c.code.toLowerCase() === carrierCode.toLowerCase()
  );
  if (!carrier) return false;
  return carrier.patterns.some(({ regex }) => {
    const r = new RegExp(`^(?:${regex.source})$`, regex.flags.replace('g', ''));
    return r.test(num);
  });
}

// ---------------------------------------------------------------------------
// Core: extractTrackingNumbers
// ---------------------------------------------------------------------------

/**
 * Extract all potential tracking numbers from a text string.
 *
 * @param {string} text  Raw text (email body, subject, etc.)
 * @param {object} [opts]
 * @param {number} [opts.minConfidence=0.5]  Minimum confidence threshold
 * @param {boolean} [opts.useContext=true]   Boost confidence for context keywords
 * @returns {Array<{
 *   trackingNumber: string,
 *   carrier: { code: string, name: string } | null,
 *   confidence: number,
 *   matchedPattern: string,
 * }>}
 */
function extractTrackingNumbers(text, opts = {}) {
  const { minConfidence = 0.5, useContext = true } = opts;

  if (!text || typeof text !== 'string') return [];

  const allMatches = [];

  for (const carrier of CARRIER_PATTERNS) {
    for (const { regex, confidence } of carrier.patterns) {
      // Clone regex to reset lastIndex
      const r = new RegExp(regex.source, regex.flags.includes('g') ? regex.flags : regex.flags + 'g');
      let match;
      while ((match = r.exec(text)) !== null) {
        const num = match[0].trim();
        if (looksLikeFalsePositive(num)) continue;

        let score = confidence;

        // Boost if surrounded by context keywords
        if (useContext && hasContextKeyword(text, match.index)) {
          score = Math.min(1.0, score + 0.15);
        }

        if (score < minConfidence) continue;

        allMatches.push({
          trackingNumber: num,
          carrier: { code: carrier.code, name: carrier.name },
          confidence: Math.round(score * 100) / 100,
          matchedPattern: regex.source,
        });
      }
    }
  }

  // Deduplicate: keep highest confidence per number
  return deduplicateResults(allMatches).sort((a, b) => b.confidence - a.confidence);
}

// ---------------------------------------------------------------------------
// Core: extractFromEmail
// ---------------------------------------------------------------------------

/**
 * Extract tracking numbers from an email object.
 * Searches subject + text body + html body (stripped of tags).
 *
 * @param {object} emailObj
 * @param {string} [emailObj.subject]
 * @param {string} [emailObj.body]       Plain text body
 * @param {string} [emailObj.html]       HTML body
 * @param {string} [emailObj.from]       Sender address
 * @param {string} [emailObj.uid]        Email UID for dedup reference
 * @param {object} [opts]
 * @param {number} [opts.minConfidence=0.5]
 * @returns {Array<{trackingNumber,carrier,confidence,source,emailUid,from}>}
 */
function extractFromEmail(emailObj, opts = {}) {
  const { minConfidence = 0.5 } = opts;
  if (!emailObj || typeof emailObj !== 'object') return [];

  const parts = [];

  if (emailObj.subject) {
    parts.push({ text: emailObj.subject, source: 'subject' });
  }
  if (emailObj.body) {
    parts.push({ text: emailObj.body, source: 'body' });
  }
  if (emailObj.html) {
    // Strip HTML tags for extraction
    const stripped = emailObj.html
      .replace(/<style[^>]*>[\s\S]*?<\/style>/gi, '')
      .replace(/<script[^>]*>[\s\S]*?<\/script>/gi, '')
      .replace(/<[^>]+>/g, ' ')
      .replace(/&nbsp;/g, ' ')
      .replace(/&amp;/g, '&')
      .replace(/\s+/g, ' ');
    parts.push({ text: stripped, source: 'html' });
  }

  const allResults = [];
  const seen = new Set();

  for (const { text, source } of parts) {
    const results = extractTrackingNumbers(text, { minConfidence });
    for (const r of results) {
      const key = r.trackingNumber.toUpperCase();
      if (!seen.has(key)) {
        seen.add(key);
        allResults.push({
          ...r,
          source,
          emailUid: emailObj.uid || null,
          from: emailObj.from || null,
        });
      }
    }
  }

  return allResults.sort((a, b) => b.confidence - a.confidence);
}

// ---------------------------------------------------------------------------
// Core: extractFromFile
// ---------------------------------------------------------------------------

/**
 * Extract tracking numbers from a file (plain text, CSV, JSON string, etc.)
 *
 * @param {string} filePath  Absolute path to file
 * @param {object} [opts]
 * @returns {Array<{trackingNumber,carrier,confidence}>}
 */
function extractFromFile(filePath, opts = {}) {
  let text;
  try {
    text = fs.readFileSync(filePath, 'utf8');
  } catch (e) {
    throw new Error(`extractFromFile: cannot read file ${filePath}: ${e.message}`);
  }
  return extractTrackingNumbers(text, opts);
}

// ---------------------------------------------------------------------------
// Core: linkToOrder
// ---------------------------------------------------------------------------

/**
 * Try to link a tracking number to an existing order in order-tracker.
 * Matching strategy:
 *  1. Exact tracking number match in order fields
 *  2. Sender email domain match against order customer email
 *
 * @param {string} trackingNumber
 * @param {string} [ordersPath]  Path to orders.json (defaults to order-tracker/data/orders.json)
 * @param {object} [opts]
 * @param {string} [opts.fromEmail]  Sender email address for domain matching
 * @returns {{ order: object, matchType: string } | null}
 */
function linkToOrder(trackingNumber, ordersPath, opts = {}) {
  const p = ordersPath || ORDER_TRACKER_ORDERS_PATH;
  let orders;
  try {
    const raw = fs.readFileSync(p, 'utf8');
    orders = JSON.parse(raw);
  } catch (e) {
    return null; // order-tracker not available
  }

  // Normalize to array
  if (!Array.isArray(orders)) {
    orders = Object.values(orders);
  }

  const numUpper = trackingNumber.toUpperCase();

  // 1. Direct tracking number match
  for (const order of orders) {
    const orderTracking = (order.trackingNumber || order.tracking_number || '').toUpperCase();
    if (orderTracking && orderTracking === numUpper) {
      return { order, matchType: 'tracking_number_exact' };
    }
  }

  // 2. Email domain match
  if (opts.fromEmail) {
    const domain = opts.fromEmail.split('@')[1] || '';
    if (domain) {
      for (const order of orders) {
        const customerEmail = order.customerEmail || order.customer_email || '';
        if (customerEmail.endsWith('@' + domain) || customerEmail === opts.fromEmail) {
          return { order, matchType: 'email_domain' };
        }
      }
    }
  }

  return null;
}

// ---------------------------------------------------------------------------
// Core: processEmailBatch
// ---------------------------------------------------------------------------

/**
 * Batch-process a list of emails: extract tracking numbers, identify carriers,
 * optionally link to orders and register in shipment-store.
 *
 * @param {Array<object>} emails  Array of email objects (subject, body, html, from, uid)
 * @param {object} [opts]
 * @param {boolean} [opts.linkOrders=true]   Try to link to order-tracker orders
 * @param {boolean} [opts.registerShipments=false]  Register in shipment-store
 * @param {number}  [opts.minConfidence=0.6]
 * @param {boolean} [opts.dryRun=false]
 * @returns {{
 *   processed: number,
 *   found: number,
 *   linked: number,
 *   registered: number,
 *   results: Array<object>,
 *   skipped: number,
 * }}
 */
function processEmailBatch(emails, opts = {}) {
  const {
    linkOrders = true,
    registerShipments = false,
    minConfidence = 0.6,
    dryRun = false,
  } = opts;

  let processed = 0;
  let found = 0;
  let linked = 0;
  let registered = 0;
  let skipped = 0;
  const results = [];

  for (const email of emails) {
    processed++;
    const extracted = extractFromEmail(email, { minConfidence });

    if (extracted.length === 0) {
      skipped++;
      continue;
    }

    for (const item of extracted) {
      found++;
      const result = { ...item };

      // Link to order
      if (linkOrders) {
        const link = linkToOrder(item.trackingNumber, null, {
          fromEmail: email.from,
        });
        if (link) {
          result.linkedOrder = link.order;
          result.matchType = link.matchType;
          linked++;
        }
      }

      // Register in shipment-store
      if (registerShipments && !dryRun) {
        try {
          const store = require('./shipment-store');
          const existing = store.getShipment(item.trackingNumber);
          if (!existing) {
            store.upsertShipment({
              trackingNumber: item.trackingNumber,
              carrier: item.carrier ? item.carrier.code : 'unknown',
              status: 'pending',
              source: 'email_extractor',
              extractedFromEmail: email.uid || null,
              orderId: result.linkedOrder ? (result.linkedOrder.id || result.linkedOrder.orderId) : null,
              createdAt: new Date().toISOString(),
            });
            registered++;
          }
        } catch (e) {
          console.warn(`[tracking-extractor] Could not register shipment ${item.trackingNumber}:`, e.message);
        }
      } else if (registerShipments && dryRun) {
        console.log(`[DRY-RUN] Would register shipment: ${item.trackingNumber} (${item.carrier ? item.carrier.code : 'unknown'})`);
        registered++;
      }

      results.push(result);
    }
  }

  return { processed, found, linked, registered, skipped, results };
}

// ---------------------------------------------------------------------------
// CLI entry point
// ---------------------------------------------------------------------------

if (require.main === module) {
  const args = process.argv.slice(2);
  const dryRun = args.includes('--dry-run');
  const minConf = parseFloat(args.find((a) => a.startsWith('--min-confidence='))?.split('=')[1] || '0.5');

  // Mode: extract from text argument
  const textIdx = args.findIndex((a) => a === '--text');
  const fileIdx = args.findIndex((a) => a === '--file');

  if (textIdx !== -1 && args[textIdx + 1]) {
    const text = args[textIdx + 1];
    const results = extractTrackingNumbers(text, { minConfidence: minConf });
    console.log(`Extracted ${results.length} tracking number(s):`);
    results.forEach((r) => {
      console.log(`  ${r.trackingNumber} [${r.carrier ? r.carrier.code : 'unknown'}] confidence=${r.confidence}`);
    });
  } else if (fileIdx !== -1 && args[fileIdx + 1]) {
    const filePath = path.resolve(args[fileIdx + 1]);
    const results = extractFromFile(filePath, { minConfidence: minConf });
    console.log(`Extracted ${results.length} tracking number(s) from ${filePath}:`);
    results.forEach((r) => {
      console.log(`  ${r.trackingNumber} [${r.carrier ? r.carrier.code : 'unknown'}] confidence=${r.confidence}`);
    });
  } else {
    console.log(`Usage:
  node tracking-extractor.js --text "Your shipment 1Z999AA10123456784 has been shipped"
  node tracking-extractor.js --file /path/to/email.txt
  node tracking-extractor.js --text "..." --min-confidence=0.7
  node tracking-extractor.js --text "..." --dry-run

Options:
  --text <text>               Extract from inline text
  --file <path>               Extract from file
  --min-confidence=<0-1>      Minimum confidence threshold (default: 0.5)
  --dry-run                   Print without registering

Supported carriers:
  UPS, FedEx, DHL, SF Express, EMS/China Post, Yanwen, CNE, 4PX`);
    process.exit(0);
  }
}

// ---------------------------------------------------------------------------
// Exports
// ---------------------------------------------------------------------------

module.exports = {
  extractTrackingNumbers,
  extractFromEmail,
  extractFromFile,
  identifyCarrier,
  validateTrackingNumber,
  linkToOrder,
  processEmailBatch,
  // Internal helpers (exported for testing)
  _hasContextKeyword: hasContextKeyword,
  _looksLikeFalsePositive: looksLikeFalsePositive,
  _deduplicateResults: deduplicateResults,
  CARRIER_PATTERNS,
};
