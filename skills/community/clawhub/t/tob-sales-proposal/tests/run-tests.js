// tob-sales-proposal smoke test
const fs = require('fs');
const path = require('path');

let ok = true;

// 1. Check generator.js structure
const genPath = path.join(__dirname, '..', 'src', 'generator.js');
const gen = fs.readFileSync(genPath, 'utf8');
for (const [name, pattern] of [['PROPOSAL_TEMPLATE', 'const PROPOSAL_TEMPLATE'], ['module.exports', 'module.exports']]) {
  if (!gen.includes(pattern)) {
    console.error(`FAIL: ${name} not found`);
    ok = false;
  } else {
    console.log(`✅ ${name} found in generator.js`);
  }
}

// 2. Check data files
const dataDir = path.join(__dirname, '..', 'data');
for (const f of ['methodologies.json', 'cases.json']) {
  try {
    JSON.parse(fs.readFileSync(path.join(dataDir, f), 'utf8'));
    console.log(`✅ data/${f} valid JSON`);
  } catch (e) {
    console.error(`FAIL: data/${f} - ${e.message}`);
    ok = false;
  }
}

// 3. Sensitive info check
const files = ['SKILL.md', 'README.md', 'src/generator.js', 'src/cli.js', 'src/index.js', 'data/methodologies.json', 'data/cases.json'];
for (const f of files) {
  const fp = path.join(__dirname, '..', f);
  if (!fs.existsSync(fp)) continue;
  const content = fs.readFileSync(fp, 'utf8');
  const forbidden = [
    String.fromCharCode(0x674e, 0x5b81),
    'lin' + 'ing434',
    String.fromCharCode(0x4e2d, 0x4fe1, 0x96c6, 0x56e2),
    String.fromCharCode(0x529b, 0x65b9, 0x529b, 0x5408),
    String.fromCharCode(0x6167, 0x535a),
  ];
  if (forbidden.some(w => content.includes(w))) {
    console.error(`FAIL: ${f} contains sensitive info`);
    ok = false;
  }
}
console.log(`✅ sensitive info check passed`);

if (ok) {
  console.log('\ntob-sales-proposal smoke test passed ✅');
  process.exit(0);
} else {
  console.error('\ntob-sales-proposal smoke test FAILED ❌');
  process.exit(1);
}
