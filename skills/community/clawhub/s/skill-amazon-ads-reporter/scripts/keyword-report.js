/**
 * Fetch keyword-level performance report across all active campaigns
 * Filters: only ENABLED keywords with meaningful data
 * "Winning" = clicks > 0 OR impressions > 50
 */
const zlib = require('zlib');
const fs = require('fs');

const CREDS_PATH = process.env.AMAZON_ADS_PATH || `${process.env.HOME}/amazon-ads-api.json`;
const API_BASE = 'https://advertising-api-eu.amazon.com';

function getCreds() { return JSON.parse(fs.readFileSync(CREDS_PATH, 'utf8')); }

async function getAccessToken() {
  const creds = getCreds();
  const res = await fetch('https://api.amazon.com/auth/o2/token', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({
      grant_type: 'refresh_token',
      refresh_token: creds.refreshToken,
      client_id: creds.lwaClientId,
      client_secret: creds.lwaClientSecret,
    }),
  });
  const t = await res.json();
  if (!t.access_token) throw new Error('Ads auth failed: ' + JSON.stringify(t));
  return t.access_token;
}

async function apiCall(path, method = 'GET', body = null, contentType = 'application/json') {
  const creds = getCreds();
  const token = await getAccessToken();
  const opts = {
    method,
    headers: {
      'Authorization': `Bearer ${token}`,
      'Amazon-Advertising-API-ClientId': creds.lwaClientId,
      'Amazon-Advertising-API-Scope': creds.profileId,
      'Content-Type': contentType,
      'Accept': contentType,
    }
  };
  if (body) opts.body = JSON.stringify(body);
  const res = await fetch(API_BASE + path, opts);
  const text = await res.text();
  try { return JSON.parse(text); } catch(e) { return text; }
}

async function downloadGzip(url) {
  const res = await fetch(url);
  const buf = Buffer.from(await res.arrayBuffer());
  return new Promise((resolve, reject) => {
    zlib.gunzip(buf, (err, decoded) => {
      if (err) reject(err);
      else resolve(JSON.parse(decoded.toString()));
    });
  });
}

async function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }

async function main() {
  // Date range: last 14 days for more signal
  const end = new Date(); end.setDate(end.getDate() - 1);
  const start = new Date(); start.setDate(start.getDate() - 14);
  const fmt = d => d.toISOString().split('T')[0];

  console.error(`Requesting keyword report ${fmt(start)}–${fmt(end)}...`);

  const created = await apiCall('/reporting/reports', 'POST', {
    name: `kw-perf-${fmt(start)}`,
    startDate: fmt(start),
    endDate: fmt(end),
    configuration: {
      adProduct: 'SPONSORED_PRODUCTS',
      groupBy: ['adGroup'],
      columns: ['keywordId', 'keywordText', 'matchType', 'impressions', 'clicks', 'cost', 'purchases7d', 'sales7d', 'startDate', 'endDate'],
      reportTypeId: 'spKeywords',
      timeUnit: 'SUMMARY',
      format: 'GZIP_JSON'
    }
  }, 'application/vnd.createasyncreportrequest.v3+json');

  if (!created.reportId) {
    console.error('Failed:', JSON.stringify(created));
    process.exit(1);
  }

  const reportId = created.reportId;
  console.error(`Report ID: ${reportId} — polling...`);

  // Poll up to 20 times (10 min)
  let status;
  for (let i = 0; i < 20; i++) {
    await sleep(30000);
    status = await apiCall(`/reporting/reports/${reportId}`, 'GET', null, 'application/json');
    console.error(`  [${i+1}/20] Status: ${status.status}`);
    if (status.status === 'COMPLETED') break;
    if (status.status === 'FAILED') { console.error('Report failed:', JSON.stringify(status)); process.exit(1); }
  }

  if (status.status !== 'COMPLETED') {
    console.error('Timed out waiting for report');
    process.exit(1);
  }

  const rows = await downloadGzip(status.url);
  console.error(`Downloaded ${rows.length} keyword rows`);

  // Filter: only ENABLED keywords
  const enabled = rows.filter(r => r.state === 'ENABLED');

  // Winning = clicks > 0 OR impressions >= 50
  const winners = enabled.filter(r => (r.clicks || 0) > 0 || (r.impressions || 0) >= 50);

  // Sort by clicks desc, then impressions desc
  winners.sort((a, b) => {
    const clickDiff = (b.clicks || 0) - (a.clicks || 0);
    if (clickDiff !== 0) return clickDiff;
    return (b.impressions || 0) - (a.impressions || 0);
  });

  console.log('\n🏆 WINNING KEYWORDS (14-day, ENABLED only, clicks>0 OR imp≥50)\n');
  console.log(`${'Campaign'.padEnd(25)} ${'Ad Group'.padEnd(18)} ${'Keyword'.padEnd(35)} ${'Match'.padEnd(7)} ${'Bid'.padStart(6)} ${'Imp'.padStart(6)} ${'Clk'.padStart(4)} ${'CTR'.padStart(6)} ${'Spend'.padStart(8)} ${'Sales'.padStart(8)} ${'ACoS'.padStart(6)}`);
  console.log('-'.repeat(140));

  for (const r of winners) {
    const imp = r.impressions || 0;
    const clk = r.clicks || 0;
    const spend = r.spend || 0;
    const sales = r.sales7d || 0;
    const ctr = imp > 0 ? ((clk / imp) * 100).toFixed(2) + '%' : '0.00%';
    const acos = sales > 0 ? ((spend / sales) * 100).toFixed(0) + '%' : '—';
    const camp = (r.campaignName || '').slice(0, 24).padEnd(25);
    const ag = (r.adGroupName || '').slice(0, 17).padEnd(18);
    const kw = (r.keywordText || '').slice(0, 34).padEnd(35);
    const match = (r.matchType || '').slice(0, 6).padEnd(7);
    const bid = (r.keywordBid || 0).toFixed(2).padStart(6);
    console.log(`${camp} ${ag} ${kw} ${match} ${bid} ${String(imp).padStart(6)} ${String(clk).padStart(4)} ${ctr.padStart(6)} ${spend.toFixed(2).padStart(8)} ${sales.toFixed(2).padStart(8)} ${acos.padStart(6)}`);
  }

  console.log(`\nTotal winning keywords: ${winners.length} / ${enabled.length} enabled`);

  // Also show zero-performers for awareness
  const zeros = enabled.filter(r => (r.clicks || 0) === 0 && (r.impressions || 0) < 50);
  console.log(`Dead keywords (0 clicks, <50 imp): ${zeros.length}`);
}

main().catch(e => { console.error(e); process.exit(1); });
