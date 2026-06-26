const { spawnSync } = require('child_process');
const path = require('path');

const TUNIU_API_KEY = process.env.TUNIU_API_KEY || '';
const tuniuPath = path.join(
  process.env.APPDATA || process.env.HOME || '',
  'npm', 'node_modules', 'tuniu-cli', 'bin', 'tuniu.js'
);

// Test train query
const params = {
  departure: '杭州',
  arrival: '南京',
  departureDate: '2026-05-04'
};

console.log('=== Train Query ===');
console.log('Params:', JSON.stringify(params));
console.log('Tuniu path:', tuniuPath);

const result = spawnSync('node', [tuniuPath, 'call', 'train', 'searchLowestPriceTrain', '-a', JSON.stringify(params)], {
  env: { ...process.env, TUNIU_API_KEY },
  encoding: 'utf8',
  timeout: 30000,
  shell: false
});

console.log('Exit code:', result.status);
console.log('stdout:', result.stdout?.slice(0, 1000));
console.log('stderr:', result.stderr?.slice(0, 500));

if (result.error) {
  console.error('Error:', result.error.message);
}