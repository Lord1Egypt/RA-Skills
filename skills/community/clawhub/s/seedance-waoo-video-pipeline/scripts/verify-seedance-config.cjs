const fs = require('node:fs');
const path = require('node:path');

const configPath = process.argv[2]
  ? path.resolve(process.cwd(), process.argv[2])
  : path.resolve(__dirname, '..', 'config', 'pipeline.config.json');

if (!fs.existsSync(configPath)) {
  console.error(JSON.stringify({ ok: false, error: 'config_not_found', configPath }, null, 2));
  process.exit(1);
}

const raw = fs.readFileSync(configPath, 'utf8').trim();
if (!raw) {
  console.error(JSON.stringify({ ok: false, error: 'config_empty', configPath }, null, 2));
  process.exit(1);
}

const config = JSON.parse(raw);
const seedance = config?.upstream?.seedance || {};
const missing = [];
if (!seedance['厂商']) missing.push('厂商');
if (!seedance['接口地址']) missing.push('接口地址');
if (!seedance['模型名']) missing.push('模型名');
if (!seedance['APIKey']) missing.push('API Key');

const placeholderFlags = [];
if (String(seedance['模型名'] || '').toLowerCase().includes('placeholder')) placeholderFlags.push('模型名=placeholder');
if (String(seedance['APIKey'] || '').toLowerCase() === 'demo') placeholderFlags.push('APIKey=demo');

const result = {
  ok: missing.length === 0 && placeholderFlags.length === 0,
  configPath,
  upstream: {
    seedance: {
      '厂商': seedance['厂商'] || '',
      '接口地址': seedance['接口地址'] || '',
      '模型名': seedance['模型名'] || '',
      hasApiKey: Boolean(seedance['APIKey'])
    }
  },
  missing,
  placeholderFlags
};

console.log(JSON.stringify(result, null, 2));
process.exit(result.ok ? 0 : 2);
