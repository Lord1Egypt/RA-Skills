import dotenv from 'dotenv';
dotenv.config();

import { Reach } from '../src/index.js';
import github from '../src/sites/github.js';
import { sendEmail } from '../src/primitives/email.js';

const reach = new Reach();
let passed = 0;
let failed = 0;

function assert(condition, name) {
  if (condition) {
    console.log(`  PASS: ${name}`);
    passed++;
  } else {
    console.log(`  FAIL: ${name}`);
    failed++;
  }
}

// --- GitHub (API — no browser needed, always testable) ---

async function testGitHub() {
  console.log('\n--- GitHub site skill ---');

  // Read a public repo
  try {
    const info = await github.getRepoInfo('Potdealer', 'exoskeletons');
    assert(info.name === 'exoskeletons', 'getRepoInfo returns correct repo name');
    assert(typeof info.stars === 'number', 'getRepoInfo returns star count');
    assert(info.url.includes('github.com'), 'getRepoInfo returns HTML URL');
  } catch (e) {
    console.log(`  FAIL: getRepoInfo — ${e.message}`);
    failed++;
  }

  // Read repo root directory
  try {
    const dir = await github.readRepo('Potdealer', 'exoskeletons');
    assert(dir.type === 'directory', 'readRepo root returns directory type');
    assert(Array.isArray(dir.entries), 'readRepo root returns entries array');
    assert(dir.entries.length > 0, 'readRepo root has entries');
  } catch (e) {
    console.log(`  FAIL: readRepo directory — ${e.message}`);
    failed++;
  }

  // Read a specific file
  try {
    const file = await github.readRepo('Potdealer', 'exoskeletons', 'README.md');
    assert(file.type === 'file', 'readRepo file returns file type');
    assert(typeof file.content === 'string', 'readRepo file returns string content');
    assert(file.content.length > 0, 'readRepo file content is not empty');
  } catch (e) {
    // README might not exist, that's ok
    console.log(`  SKIP: readRepo file — ${e.message}`);
  }

  // List issues
  try {
    const result = await github.listIssues('Potdealer', 'exoskeletons', { per_page: 5 });
    assert(Array.isArray(result.issues), 'listIssues returns issues array');
    assert(result.state === 'open', 'listIssues defaults to open state');
  } catch (e) {
    console.log(`  FAIL: listIssues — ${e.message}`);
    failed++;
  }

  // List PRs
  try {
    const result = await github.listPulls('Potdealer', 'exoskeletons', { per_page: 5 });
    assert(Array.isArray(result.pulls), 'listPulls returns pulls array');
  } catch (e) {
    console.log(`  FAIL: listPulls — ${e.message}`);
    failed++;
  }

  // Search repos
  try {
    const result = await github.search('exoskeletons solidity', 'repositories', 3);
    assert(typeof result.totalCount === 'number', 'search returns totalCount');
    assert(Array.isArray(result.items), 'search returns items array');
  } catch (e) {
    console.log(`  FAIL: search — ${e.message}`);
    failed++;
  }
}

// --- Site skills structure tests (no network) ---

async function testSiteSkillStructure() {
  console.log('\n--- Site skill structure ---');

  // Code4rena exports
  const c4 = reach.sites.code4rena;
  assert(typeof c4.login === 'function', 'code4rena has login()');
  assert(typeof c4.getActiveAudits === 'function', 'code4rena has getActiveAudits()');
  assert(typeof c4.readAuditDetails === 'function', 'code4rena has readAuditDetails()');
  assert(typeof c4.submitFinding === 'function', 'code4rena has submitFinding()');
  assert(typeof c4.checkSubmissions === 'function', 'code4rena has checkSubmissions()');

  // Upwork exports
  const uw = reach.sites.upwork;
  assert(typeof uw.login === 'function', 'upwork has login()');
  assert(typeof uw.searchJobs === 'function', 'upwork has searchJobs()');
  assert(typeof uw.readJobDetails === 'function', 'upwork has readJobDetails()');
  assert(typeof uw.submitProposal === 'function', 'upwork has submitProposal()');
  assert(typeof uw.checkMessages === 'function', 'upwork has checkMessages()');

  // GitHub exports
  const gh = reach.sites.github;
  assert(typeof gh.readRepo === 'function', 'github has readRepo()');
  assert(typeof gh.getRepoInfo === 'function', 'github has getRepoInfo()');
  assert(typeof gh.listIssues === 'function', 'github has listIssues()');
  assert(typeof gh.readIssue === 'function', 'github has readIssue()');
  assert(typeof gh.listPulls === 'function', 'github has listPulls()');
  assert(typeof gh.createIssue === 'function', 'github has createIssue()');
  assert(typeof gh.search === 'function', 'github has search()');

  // Immunefi exports
  const imm = reach.sites.immunefi;
  assert(typeof imm.listPrograms === 'function', 'immunefi has listPrograms()');
  assert(typeof imm.readProgram === 'function', 'immunefi has readProgram()');
  assert(typeof imm.submitReport === 'function', 'immunefi has submitReport()');
}

// --- Email primitive ---

async function testEmail() {
  console.log('\n--- Email primitive ---');

  // Check function exists
  assert(typeof sendEmail === 'function', 'sendEmail is exported');
  assert(typeof reach.email === 'function', 'reach.email() exists');

  // Test validation
  try {
    await sendEmail(null, null, null);
    console.log('  FAIL: sendEmail should throw on missing params');
    failed++;
  } catch (e) {
    assert(e.message.includes('requires'), 'sendEmail validates required params');
  }
}

// --- Router knowledge base ---

async function testRouterKnowledge() {
  console.log('\n--- Router knowledge base ---');

  // Check that sites.json knowledge is loaded
  const r1 = reach.route({ type: 'read', url: 'https://code4rena.com/audits' });
  assert(r1.params?.javascript === true, 'code4rena routes with javascript:true');

  const r2 = reach.route({ type: 'read', url: 'https://immunefi.com/explore' });
  assert(r2.params?.javascript === true, 'immunefi routes with javascript:true');

  const r3 = reach.route({ type: 'read', url: 'https://docs.base.org/getting-started' });
  assert(r3.layer === 'http', 'docs.base.org routes to http (no JS needed)');

  // GitHub API routing
  const r4 = reach.route({ type: 'read', url: 'https://api.github.com/repos/Potdealer/exoskeletons' });
  assert(r4.layer === 'api', 'api.github.com routes to api layer');

  // Basescan API
  const r5 = reach.route({ type: 'read', url: 'https://basescan.org/address/0x123' });
  // basescan.org has an API endpoint configured, so routes to API layer
  assert(r5.layer === 'api', 'basescan.org routes to api layer');
}

// --- MCP server structure ---

async function testMCPStructure() {
  console.log('\n--- MCP server ---');

  // Just verify the file is importable (syntax check)
  try {
    // We can't import it because it starts listening on stdin immediately,
    // but we can check the file exists
    const fs = await import('fs');
    const exists = fs.existsSync('/mnt/e/Ai Agent/Projects/reach/src/mcp.js');
    assert(exists, 'mcp.js exists');

    const content = fs.readFileSync('/mnt/e/Ai Agent/Projects/reach/src/mcp.js', 'utf-8');
    assert(content.includes('web_fetch'), 'mcp.js defines web_fetch tool');
    assert(content.includes('web_act'), 'mcp.js defines web_act tool');
    assert(content.includes('web_authenticate'), 'mcp.js defines web_authenticate tool');
    assert(content.includes('web_sign'), 'mcp.js defines web_sign tool');
    assert(content.includes('web_see'), 'mcp.js defines web_see tool');
    assert(content.includes('web_email'), 'mcp.js defines web_email tool');
    assert(content.includes('tools/list'), 'mcp.js handles tools/list');
    assert(content.includes('tools/call'), 'mcp.js handles tools/call');
  } catch (e) {
    console.log(`  FAIL: MCP structure — ${e.message}`);
    failed++;
  }
}

async function main() {
  console.log('Reach Site Skills Test Suite\n============================');

  await testSiteSkillStructure();
  await testRouterKnowledge();
  await testEmail();
  await testMCPStructure();
  await testGitHub();

  console.log(`\n============================`);
  console.log(`${passed} passed, ${failed} failed`);

  await reach.close();
  process.exit(failed > 0 ? 1 : 0);
}

main().catch(e => {
  console.error(e);
  process.exit(1);
});
