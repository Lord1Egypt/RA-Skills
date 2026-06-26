#!/usr/bin/env node
/**
 * SUPAH Research Intelligence
 * Professional web research with source verification
 * All access via x402 USDC micropayments on Base — no API keys
 */

const https = require('https');
const http = require('http');

const API_BASE = process.env.SUPAH_API_BASE || 'https://api.supah.ai';

function apiRequest(path, params = {}) {
  return new Promise((resolve, reject) => {
    const queryString = new URLSearchParams(params).toString();
    const url = `${API_BASE}${path}${queryString ? '?' + queryString : ''}`;
    const client = url.startsWith('https') ? https : http;
    
    client.get(url, { headers: { 'User-Agent': 'OpenClaw-SUPAH-Research/1.2.0' } }, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try { resolve(JSON.parse(data)); }
        catch (e) { resolve({ error: 'Invalid response', raw: data }); }
      });
    }).on('error', reject);
  });
}

async function research(topic) {
  console.log(`\n🔍 Researching: ${topic}\n`);
  try {
    const results = await apiRequest('/agent/v1/research/multi-source', { q: topic, sources: 5 });
    if (results.error) {
      console.log('⚠️  API unavailable. Try again shortly.\n');
      return;
    }
    console.log('📊 Sources Found:', results.sources?.length || 0);
    console.log('✅ Consensus:', results.consensus || 'Mixed');
    console.log('\n📝 Summary:\n');
    console.log(results.summary);
    console.log('\n🔗 Sources:\n');
    (results.sources || []).forEach((src, i) => {
      console.log(`${i + 1}. ${src.title}`);
      console.log(`   ${src.url}`);
      console.log(`   Credibility: ${src.credibility}/100\n`);
    });
  } catch (err) {
    console.error('❌ Research failed:', err.message);
  }
}

async function verify(claim) {
  console.log(`\n✓ Verifying: "${claim}"\n`);
  try {
    const result = await apiRequest('/agent/v1/research/verify', { claim });
    if (result.error) { console.log('⚠️  API unavailable. Try again shortly.\n'); return; }
    console.log('📊 Verification Status:', result.status);
    console.log('🎯 Confidence:', result.confidence + '%');
    console.log('\n📝 Conclusion:\n');
    console.log(result.conclusion);
  } catch (err) {
    console.error('❌ Verification failed:', err.message);
  }
}

async function credibility(url) {
  console.log(`\n📊 Analyzing: ${url}\n`);
  try {
    const result = await apiRequest('/agent/v1/research/credibility', { url });
    if (result.error) { console.log('⚠️  API unavailable. Try again shortly.\n'); return; }
    console.log('🎯 Overall Score:', result.score + '/100');
    console.log(`   Domain Authority: ${result.domainAuthority}/100`);
    console.log(`   Content Quality: ${result.contentQuality}/100`);
    console.log(`   Freshness: ${result.freshness}/100`);
  } catch (err) {
    console.error('❌ Analysis failed:', err.message);
  }
}

async function report(topic) {
  console.log(`\n📄 Generating Report: ${topic}\n`);
  try {
    const result = await apiRequest('/agent/v1/research/report', { topic, depth: 'comprehensive' });
    if (result.error) { console.log('⚠️  API unavailable. Try again shortly.\n'); return; }
    console.log('📄 RESEARCH REPORT\n');
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');
    console.log(`Topic: ${result.topic}`);
    console.log(`Sources: ${result.sourcesCount}`);
    console.log(`Confidence: ${result.confidence}%\n`);
    console.log('📝 EXECUTIVE SUMMARY\n');
    console.log(result.executiveSummary + '\n');
    console.log('🔍 KEY FINDINGS\n');
    (result.keyFindings || []).forEach((finding, i) => { console.log(`${i + 1}. ${finding}\n`); });
    console.log('🎯 RECOMMENDED ACTIONS\n');
    (result.recommendations || []).forEach((rec, i) => { console.log(`${i + 1}. ${rec}\n`); });
  } catch (err) {
    console.error('❌ Report generation failed:', err.message);
  }
}

async function main() {
  const args = process.argv.slice(2);
  if (args.length === 0) {
    console.log('\n📰 SUPAH Research Intelligence v1.2.0\n');
    console.log('Usage:');
    console.log('  research <topic>     - Multi-source research ($0.25)');
    console.log('  verify <claim>       - Fact verification ($0.25)');
    console.log('  credibility <url>    - Source scoring ($0.25)');
    console.log('  report <topic>       - Full research report ($0.25)\n');
    console.log('Payment: x402 USDC micropayments on Base (automatic)\n');
    process.exit(0);
  }
  const command = args[0].toLowerCase();
  const input = args.slice(1).join(' ');
  if (!input && command !== 'help') { console.error('❌ Error: Missing input'); process.exit(1); }
  switch (command) {
    case 'research': await research(input); break;
    case 'verify': await verify(input); break;
    case 'credibility': case 'cred': await credibility(input); break;
    case 'report': await report(input); break;
    default: console.error('❌ Unknown command:', command); process.exit(1);
  }
}

main().catch(console.error);
