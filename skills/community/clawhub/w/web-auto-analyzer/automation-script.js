#!/usr/bin/env node
/**
 * Chrome DevTools Auto Analyzer
 * Automated website analysis using Lighthouse and Puppeteer
 * 
 * Usage: node automation-script.js <URL> [options]
 * Example: node automation-script.js https://example.com --mobile --output=results
 */

import lighthouse from 'lighthouse';
import * as chromeLauncher from 'chrome-launcher';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Configuration
const CONFIG = {
  logLevel: 'info',
  output: 'json',
  onlyCategories: ['performance', 'accessibility', 'best-practices', 'seo'],
  emulatedFormFactor: 'desktop', // 'mobile' or 'desktop'
  numberOfRuns: 1,
};

/**
 * Run Lighthouse audit and extract metrics
 * @param {string} url - URL to analyze
 * @param {object} options - Lighthouse options
 * @returns {Promise<object>} - Extracted metrics and issues
 */
async function runLighthouseAudit(url, options = {}) {
  const flags = {
    logLevel: CONFIG.logLevel,
    output: CONFIG.output,
    onlyCategories: CONFIG.onlyCategories,
    emulatedFormFactor: options.mobile ? 'mobile' : 'desktop',
    ...options,
  };

  console.log(`🚀 Starting Lighthouse audit for: ${url}`);
  console.log(`📱 Device: ${flags.emulatedFormFactor}`);

  // Launch Chrome
  const chrome = await chromeLauncher.launch({
    chromeFlags: [
      '--headless',
      '--no-sandbox',
      '--disable-gpu',
      '--disable-dev-shm-usage',
    ],
  });

  flags.port = chrome.port;

  try {
    // Run Lighthouse
    const runnerResult = await lighthouse(url, flags);

    if (!runnerResult || !runnerResult.lhr) {
      throw new Error('Lighthouse audit failed to return results');
    }

    // Extract metrics
    const results = extractMetrics(runnerResult.lhr);

    console.log('✅ Audit complete!');
    return results;
  } finally {
    await chrome.kill();
  }
}

/**
 * Extract performance metrics and audit issues from Lighthouse result
 * @param {object} lhr - Lighthouse Result object
 * @returns {object} - Structured results
 */
function extractMetrics(lhr) {
  const audits = lhr.audits;
  const categories = lhr.categories;

  // Performance metrics
  const performanceMetrics = {
    FCP: getValue(audits['first-contentful-paint']),
    LCP: getValue(audits['largest-contentful-paint']),
    CLS: getValue(audits['cumulative-layout-shift']),
    TBT: getValue(audits['total-blocking-time']),
    SI: getValue(audits['speed-index']),
    INP: getValue(audits['interaction-to-next-paint']),
    TTI: getValue(audits['interactive']),
    TTFB: getValue(audits['server-response-time']),
  };

  // Category scores
  const scores = {
    Performance: Math.round((categories.performance?.score || 0) * 100),
    Accessibility: Math.round((categories.accessibility?.score || 0) * 100),
    'Best Practices': Math.round((categories['best-practices']?.score || 0) * 100),
    SEO: Math.round((categories.seo?.score || 0) * 100),
  };

  // Extract failed audits (issues)
  const issues = {
    performance: getFailedAudits(audits, [
      'largest-contentful-paint',
      'cumulative-layout-shift',
      'total-blocking-time',
      'speed-index',
      'first-contentful-paint',
      'interactive',
    ]),
    accessibility: getFailedAudits(audits, [
      'color-contrast',
      'image-alt',
      'label',
      'link-name',
      'heading-order',
      'button-name',
      'html-has-lang',
      'valid-lang',
    ]),
    bestPractices: getFailedAudits(audits, [
      'is-on-https',
      'uses-http2',
      'uses-passive-event-listeners',
      'no-document-write',
      'geolocation-on-start',
      'notification-on-start',
      'deprecations',
      'errors-in-console',
    ]),
    seo: getFailedAudits(audits, [
      'document-title',
      'meta-description',
      'http-status-code',
      'link-text',
      'crawlable-anchors',
      'is-crawlable',
      'robots-txt',
      'image-alt',
      'hreflang',
      'canonical',
    ]),
  };

  return {
    url: lhr.finalDisplayedUrl,
    timestamp: lhr.fetchTime,
    device: lhr.configSettings?.emulatedFormFactor || 'desktop',
    scores,
    performanceMetrics,
    issues,
    rawLhr: lhr,
  };
}

/**
 * Get numeric value from audit
 * @param {object} audit - Lighthouse audit object
 * @returns {number|string} - Numeric value or 'N/A'
 */
function getValue(audit) {
  if (!audit || audit.score === null || audit.score === undefined) {
    return 'N/A';
  }
  if (audit.numericValue !== undefined) {
    // Convert milliseconds to seconds for display
    if (audit.numericUnit === 'millisecond') {
      return Math.round(audit.numericValue);
    }
    return Math.round(audit.numericValue * 100) / 100;
  }
  return audit.score;
}

/**
 * Get failed audits for specific IDs
 * @param {object} audits - All audits
 * @param {string[]} auditIds - Audit IDs to check
 * @returns {Array} - Failed audits with details
 */
function getFailedAudits(audits, auditIds) {
  const failed = [];

  for (const id of auditIds) {
    const audit = audits[id];
    if (audit && audit.score !== null && audit.score < 1) {
      failed.push({
        id,
        title: audit.title || id,
        description: audit.description || '',
        score: audit.score,
        numericValue: audit.numericValue,
        displayValue: audit.displayValue,
        details: audit.details,
      });
    }
  }

  return failed;
}

/**
 * Get fix suggestions for common issues
 * @param {string} auditId - Audit ID
 * @param {number} value - Metric value
 * @returns {string} - Fix suggestion
 */
function getFixSuggestion(auditId, value) {
  const fixes = {
    'cumulative-layout-shift': value > 0.25
      ? '🔴 CRITICAL: Add width/height to images, reserve space for ads/embeds, use CSS aspect-ratio'
      : '🟡 Add explicit dimensions to dynamic content, preload critical fonts',
    'largest-contentful-paint': value > 4000
      ? '🔴 CRITICAL: Optimize server response, preload LCP image, remove render-blocking resources'
      : '🟡 Compress images, use CDN, reduce JavaScript execution',
    'total-blocking-time': value > 600
      ? '🔴 CRITICAL: Break up long tasks, defer non-critical JavaScript, use web workers'
      : '🟡 Code split, remove unused JavaScript, optimize event listeners',
    'speed-index': value > 5800
      ? '🔴 CRITICAL: Minimize above-fold content, inline critical CSS, defer non-critical resources'
      : '🟡 Optimize image delivery, enable text compression',
    'first-contentful-paint': value > 3000
      ? '🔴 CRITICAL: Reduce server response time, eliminate render-blocking resources'
      : '🟡 Preload critical assets, optimize CSS/JavaScript delivery',
    'interactive': value > 7300
      ? '🔴 CRITICAL: Reduce JavaScript execution time, minimize main-thread work'
      : '🟡 Defer offscreen images, reduce third-party scripts',
    'color-contrast': '🔴 Increase contrast ratio to at least 4.5:1 for normal text',
    'image-alt': '🔴 Add descriptive alt attributes to all images',
    'label': '🔴 Associate labels with form inputs using for/id attributes',
    'link-name': '🔴 Use descriptive link text that makes sense out of context',
    'heading-order': '🔴 Fix heading hierarchy - use h1→h2→h3 sequentially',
    'document-title': '🔴 Add a descriptive <title> element in the <head>',
    'meta-description': '🔴 Add meta description (150-160 characters)',
    'is-on-https': '🔴 Enable HTTPS and redirect all HTTP traffic',
    'uses-http2': '🟡 Enable HTTP/2 on your server for better performance',
    'no-document-write': '🔴 Replace document.write() with modern DOM manipulation',
  };
  return fixes[auditId] || '🔧 Review documentation for fix guidance';
}

/**
 * Format results for console output
 * @param {object} results - Analysis results
 */
function printResults(results) {
  console.log('\n' + '='.repeat(70));
  console.log(`📊 Analysis Results for: ${results.url}`);
  console.log(`🕐 Timestamp: ${results.timestamp}`);
  console.log(`📱 Device: ${results.device}`);
  console.log('='.repeat(70));

  // Scores
  console.log('\n📈 Category Scores:');
  for (const [category, score] of Object.entries(results.scores)) {
    const status = getScoreStatus(score);
    console.log(`  ${category}: ${score}/100 ${status}`);
  }

  // Performance Metrics
  console.log('\n⚡ Core Web Vitals & Performance Metrics:');
  for (const [metric, value] of Object.entries(results.performanceMetrics)) {
    if (value !== 'N/A') {
      const unit = ['CLS'].includes(metric) ? '' : 'ms';
      const status = getMetricStatus(metric, value);
      const threshold = getMetricThreshold(metric);
      console.log(`  ${metric}: ${value}${unit} ${status} (target: ${threshold})`);
    }
  }

  // Issues with fix suggestions
  const allIssues = [
    ...results.issues.performance.map(i => ({ ...i, category: 'Performance' })),
    ...results.issues.accessibility.map(i => ({ ...i, category: 'Accessibility' })),
    ...results.issues.bestPractices.map(i => ({ ...i, category: 'Best Practices' })),
    ...results.issues.seo.map(i => ({ ...i, category: 'SEO' })),
  ];

  if (allIssues.length > 0) {
    console.log('\n❌ Critical Issues & Fixes:\n');
    allIssues.forEach(issue => {
      const fix = getFixSuggestion(issue.id, issue.numericValue);
      console.log(`  [${issue.category}] ${issue.title}`);
      if (issue.displayValue) console.log(`    Value: ${issue.displayValue}`);
      console.log(`    Fix: ${fix}\n`);
    });
  } else {
    console.log('\n✅ No critical issues found! Great job!\n');
  }

  // Summary
  const perfScore = results.scores.Performance;
  const accScore = results.scores.Accessibility;
  const bpScore = results.scores['Best Practices'];
  const seoScore = results.scores.SEO;
  const overall = Math.round((perfScore + accScore + bpScore + seoScore) / 4);

  console.log('='.repeat(70));
  console.log(`📊 Overall Score: ${overall}/100 ${getScoreStatus(overall)}`);
  console.log('='.repeat(70));
  console.log('\n💡 Tip: Run with --mobile flag to test mobile performance\n');
}

/**
 * Get score status emoji
 * @param {number} score - Score 0-100
 * @returns {string} - Emoji status
 */
function getScoreStatus(score) {
  if (score >= 90) return '⚪ Good';
  if (score >= 50) return '🟡 Needs Improvement';
  return '🔴 Poor';
}

/**
 * Get metric status emoji
 * @param {string} metric - Metric name
 * @param {number} value - Metric value
 * @returns {string} - Emoji status
 */
function getMetricStatus(metric, value) {
  const thresholds = {
    FCP: { good: 1800, poor: 3000 },
    LCP: { good: 2500, poor: 4000 },
    CLS: { good: 0.1, poor: 0.25 },
    TBT: { good: 200, poor: 600 },
    SI: { good: 3400, poor: 5800 },
    INP: { good: 200, poor: 500 },
  };

  const threshold = thresholds[metric];
  if (!threshold) return '';

  if (value <= threshold.good) return '⚪ Good';
  if (value <= threshold.poor) return '🟡 Needs Improvement';
  return '🔴 Poor';
}

/**
 * Get metric target threshold string
 * @param {string} metric - Metric name
 * @returns {string} - Target threshold
 */
function getMetricThreshold(metric) {
  const targets = {
    FCP: '<1800ms',
    LCP: '<2500ms',
    CLS: '<0.1',
    TBT: '<200ms',
    SI: '<3400ms',
    INP: '<200ms',
    TTI: '<3800ms',
    TTFB: '<800ms',
  };
  return targets[metric] || 'N/A';
}

/**
 * Save results to JSON file
 * @param {object} results - Analysis results
 * @param {string} outputPath - Output directory
 */
function saveResults(results, outputPath = './results') {
  if (!fs.existsSync(outputPath)) {
    fs.mkdirSync(outputPath, { recursive: true });
  }

  const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
  const urlSafe = results.url.replace(/[^a-zA-Z0-9]/g, '_');
  const filename = `${urlSafe}_${timestamp}.json`;
  const filepath = path.join(outputPath, filename);

  // Save full results
  fs.writeFileSync(filepath, JSON.stringify(results, null, 2));
  console.log(`\n💾 Results saved to: ${filepath}`);

  // Save HTML report
  const htmlReport = results.rawLhr.report;
  if (htmlReport) {
    const htmlPath = path.join(outputPath, `${urlSafe}_${timestamp}.html`);
    fs.writeFileSync(htmlPath, htmlReport);
    console.log(`📄 HTML report saved to: ${htmlPath}`);
  }

  return filepath;
}

/**
 * Main execution
 */
async function main() {
  const args = process.argv.slice(2);

  if (args.length === 0) {
    console.log('Usage: node automation-script.js <URL> [options]');
    console.log('Options:');
    console.log('  --mobile     Run with mobile emulation');
    console.log('  --output=DIR Save results to directory');
    console.log('  --help       Show this help');
    process.exit(1);
  }

  const url = args.find(arg => !arg.startsWith('--'));
  const mobile = args.includes('--mobile');
  const outputArg = args.find(arg => arg.startsWith('--output='));
  const outputDir = outputArg ? outputArg.split('=')[1] : './results';

  if (!url) {
    console.error('❌ Error: URL is required');
    process.exit(1);
  }

  try {
    // Run audit
    const results = await runLighthouseAudit(url, { mobile });

    // Print results
    printResults(results);

    // Save results
    saveResults(results, outputDir);

    // Exit with appropriate code
    const hasCriticalIssues = 
      results.scores.Performance < 50 ||
      results.scores.Accessibility < 50 ||
      results.scores['Best Practices'] < 50 ||
      results.scores.SEo < 50;

    process.exit(hasCriticalIssues ? 1 : 0);
  } catch (error) {
    console.error('❌ Error during analysis:', error.message);
    process.exit(1);
  }
}

// Run if executed directly
if (process.argv[1] && process.argv[1].includes('automation-script.js')) {
  main();
}

export { runLighthouseAudit, extractMetrics, printResults, saveResults };
