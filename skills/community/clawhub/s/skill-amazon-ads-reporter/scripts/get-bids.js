#!/usr/bin/env node
'use strict';
/**
 * Amazon Ads — Quick Bid Inspector
 * Lists all ENABLED + PAUSED keywords with current bids for specified campaigns.
 * Uses the live v3 keyword list endpoint (no async report needed).
 *
 * Usage: node get-bids.js
 * Config: AMAZON_ADS_PATH env var (default: ~/amazon-ads-api.json)
 */
const https = require('https');
const fs = require('fs');

const ADS_PATH = process.env.AMAZON_ADS_PATH || require('os').homedir() + '/amazon-ads-api.json';
const creds = JSON.parse(fs.readFileSync(ADS_PATH, 'utf8'));

// Set your campaign IDs here
const CAMPAIGN_IDS = process.env.CAMPAIGN_IDS
  ? process.env.CAMPAIGN_IDS.split(',').map(Number)
  : [];

if (CAMPAIGN_IDS.length === 0) {
  console.error('Set CAMPAIGN_IDS env var (comma-separated) or edit the array in this script.');
  process.exit(1);
}

function apiReq(hostname, path, method, headers, body) {
  const payload = body ? JSON.stringify(body) : null;
  if (payload) headers['Content-Length'] = Buffer.byteLength(payload);
  return new Promise((resolve, reject) => {
    const req = https.request({ hostname, path, method, headers }, res => {
      let d = ''; res.on('data', c => d += c);
      res.on('end', () => {
        try { resolve({ status: res.statusCode, body: JSON.parse(d) }); }
        catch { resolve({ status: res.statusCode, body: d }); }
      });
    });
    req.on('error', reject);
    if (payload) req.write(payload);
    req.end();
  });
}

async function getToken() {
  const params = `grant_type=refresh_token&refresh_token=${encodeURIComponent(creds.refreshToken)}&client_id=${encodeURIComponent(creds.lwaClientId)}&client_secret=${encodeURIComponent(creds.lwaClientSecret)}`;
  return new Promise((resolve, reject) => {
    const req = https.request({
      hostname: 'api.amazon.com', path: '/auth/o2/token', method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded', 'Content-Length': Buffer.byteLength(params) }
    }, res => {
      let d = ''; res.on('data', c => d += c);
      res.on('end', () => {
        const t = JSON.parse(d);
        if (!t.access_token) reject(new Error('LWA failed: ' + d));
        else resolve(t.access_token);
      });
    });
    req.on('error', reject); req.write(params); req.end();
  });
}

(async () => {
  const token = await getToken();
  const endpoint = 'advertising-api-eu.amazon.com';
  const headers = {
    Authorization: `Bearer ${token}`,
    'Amazon-Advertising-API-ClientId': creds.lwaClientId,
    'Amazon-Advertising-API-Scope': String(creds.profileId),
    'Content-Type': 'application/json',
  };

  for (const campaignId of CAMPAIGN_IDS) {
    const r = await apiReq(endpoint, '/sp/keywords/list', 'POST', { ...headers }, {
      campaignIdFilter: { include: [String(campaignId)] },
      stateFilter: { include: ['ENABLED', 'PAUSED'] },
      maxResults: 50
    });
    console.log(`\nCampaign ${campaignId} keywords (HTTP ${r.status}):`);
    if (r.status === 200 && r.body.keywords) {
      for (const kw of r.body.keywords) {
        console.log(`  keywordId=${kw.keywordId} text="${kw.keywordText}" matchType=${kw.matchType} bid=${kw.bid} state=${kw.state}`);
      }
    } else {
      console.log('  Response:', JSON.stringify(r.body).substring(0, 400));
    }
  }
})().catch(e => { console.error(e.message); process.exit(1); });
