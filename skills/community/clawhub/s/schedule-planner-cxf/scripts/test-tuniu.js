const { spawnSync } = require('child_process');

const TUNIU_API_KEY = process.env.TUNIU_API_KEY || '';

// 优先使用 npx tuniu，减少直接信任用户环境中的 npm 全局安装路径
console.log('=== Train Query (via npx tuniu) ===');

const params = {
  departure: '杭州',
  arrival: '南京',
  departureDate: '2026-05-04'
};

console.log('Params:', JSON.stringify(params));

const result = spawnSync('npx', ['tuniu', 'call', 'train', 'searchLowestPriceTrain', '-a', JSON.stringify(params)], {
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