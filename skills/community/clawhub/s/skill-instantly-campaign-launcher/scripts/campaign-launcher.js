#!/usr/bin/env node
/**
 * skill-instantly-campaign-launcher
 * Creates an Instantly campaign with D0/D3/D8 sequences and imports leads.
 *
 * Usage:
 *   node campaign-launcher.js --config campaign.config.js --leads leads.json
 *   INSTANTLY_KEY=<token> node campaign-launcher.js --config campaign.config.js --leads leads.json
 */

const https = require('https');
const fs = require('fs');
const path = require('path');

// ── Config ──────────────────────────────────────────────────────────────────
const args = process.argv.slice(2);
const configPath = args[args.indexOf('--config') + 1] || path.join(__dirname, 'campaign.config.js');
const leadsPath = args[args.indexOf('--leads') + 1] || path.join(process.cwd(), 'leads.json');

const config = require(path.resolve(configPath));
const INSTANTLY_KEY = process.env.INSTANTLY_KEY || config.instantlyKey;

if (!INSTANTLY_KEY) {
  console.error('❌ Missing INSTANTLY_KEY — set env var or add instantlyKey to campaign.config.js');
  process.exit(1);
}

// ── HTTP helper ──────────────────────────────────────────────────────────────
function httpsRequest(options, body = null) {
  return new Promise((resolve, reject) => {
    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', chunk => (data += chunk));
      res.on('end', () => {
        try { resolve({ status: res.statusCode, body: JSON.parse(data) }); }
        catch { resolve({ status: res.statusCode, body: data }); }
      });
    });
    req.on('error', reject);
    if (body) req.write(JSON.stringify(body));
    req.end();
  });
}

function instantly(method, path_, body = null) {
  return httpsRequest({
    hostname: 'api.instantly.ai',
    path: `/api/v2${path_}`,
    method,
    headers: {
      Authorization: `Bearer ${INSTANTLY_KEY}`,
      'Content-Type': 'application/json',
    },
  }, body);
}

function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }

// ── Main ─────────────────────────────────────────────────────────────────────
async function main() {
  const { campaignName, schedule, sequences } = config;

  console.log('='.repeat(56));
  console.log(`📧 Instantly Campaign Launcher`);
  console.log(`   Campaign: ${campaignName}`);
  console.log('='.repeat(56));

  // ── Step 1: Find or create campaign ────────────────────────────────────────
  console.log('\n🔍 Step 1: Find or create campaign...');
  let campaignId = null;

  const listRes = await instantly('GET', '/campaigns?limit=100');
  if (listRes.status === 200 && listRes.body?.items) {
    const found = listRes.body.items.find(c => c.name === campaignName);
    if (found) {
      campaignId = found.id;
      console.log(`  ✅ Found existing campaign: ${campaignId}`);
    }
  }

  if (!campaignId) {
    const createRes = await instantly('POST', '/campaigns', {
      name: campaignName,
      campaign_schedule: {
        schedules: [
          {
            name: schedule.name,
            timing: schedule.timing,
            days: schedule.days,
            timezone: schedule.timezone,
          },
        ],
      },
    });

    if (createRes.status === 200 || createRes.status === 201) {
      campaignId = createRes.body?.id;
      console.log(`  ✅ Campaign created: ${campaignId}`);
    } else {
      console.error(`  ❌ Create failed: ${createRes.status}`, JSON.stringify(createRes.body));
      process.exit(1);
    }
  }

  // ── Step 2: Add sequences ───────────────────────────────────────────────────
  console.log('\n✉️  Step 2: Adding D0/D3/D8 sequences...');

  const seqPayload = sequences.map(s => ({
    step: s.step,
    type: 'email',
    delay: s.delay,
    variants: [{ subject: s.subject, body: s.body }],
  }));

  const seqRes = await instantly('POST', `/campaigns/${campaignId}/sequences`, {
    campaign_id: campaignId,
    sequences: seqPayload,
  });

  if (seqRes.status === 200 || seqRes.status === 201) {
    console.log(`  ✅ Sequences added (${sequences.length} steps)`);
  } else {
    console.warn(`  ⚠️  Sequences: ${seqRes.status} — ${JSON.stringify(seqRes.body).substring(0, 120)}`);
    console.warn('  ↳ Add sequences manually in Instantly dashboard if this persists (known API v2 quirk)');
  }

  // ── Step 3: Import leads ────────────────────────────────────────────────────
  if (!fs.existsSync(leadsPath)) {
    console.log(`\n⚠️  No leads file found at ${leadsPath}. Campaign created but no leads imported.`);
    console.log(`   To import leads later, create leads.json and re-run with --leads leads.json`);
    return { campaignId, imported: 0, skipped: 0, failed: 0 };
  }

  const leadsRaw = JSON.parse(fs.readFileSync(leadsPath, 'utf8'));
  const leads = Array.isArray(leadsRaw) ? leadsRaw : leadsRaw.leads || [];
  console.log(`\n📥 Step 3: Importing ${leads.length} leads...`);

  let imported = 0, skipped = 0, failed = 0;

  for (const lead of leads) {
    const res = await instantly('POST', '/leads', {
      campaign_id: campaignId,
      email: lead.email,
      first_name: lead.firstName || lead.first_name || 'there',
      last_name: lead.lastName || lead.last_name || '',
      company_name: lead.companyName || lead.company_name || '',
      website: lead.website || '',
    });

    if (res.status === 200 || res.status === 201) {
      imported++;
      process.stdout.write(`  ✅ ${lead.email}\n`);
    } else if (res.status === 409) {
      skipped++;
      process.stdout.write(`  ⏭️  ${lead.email} (already exists)\n`);
    } else {
      failed++;
      process.stdout.write(`  ❌ ${lead.email} — ${res.status}\n`);
    }

    await sleep(200); // Avoid rate limits
  }

  // ── Summary ─────────────────────────────────────────────────────────────────
  console.log('\n' + '='.repeat(56));
  console.log('✅ DONE');
  console.log(`   Campaign: ${campaignName} (${campaignId})`);
  console.log(`   Leads: ${leads.length} total | ${imported} imported | ${skipped} skipped | ${failed} failed`);
  console.log('='.repeat(56));

  return { campaignId, imported, skipped, failed };
}

main().catch(e => { console.error('Fatal:', e.message); process.exit(1); });
