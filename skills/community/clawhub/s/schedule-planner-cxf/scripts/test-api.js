const { spawnSync } = require('child_process');
const path = require('path');

const TUNIU_API_KEY = process.env.TUNIU_API_KEY || '';
const tuniuPath = path.join(
  process.env.APPDATA || process.env.HOME || '',
  'npm', 'node_modules', 'tuniu-cli', 'bin', 'tuniu.js'
);

// Test train query
const trainParams = {
  departureCityName: '杭州',
  arrivalCityName: '南京',
  departureDate: '2026-05-04'
};
console.log('=== Train Query ===');
const trainResult = spawnSync('node', [tuniuPath, 'call', 'train', 'searchLowestPriceTrain', '-a', JSON.stringify(trainParams)], {
  env: { ...process.env, TUNIU_API_KEY },
  encoding: 'utf8',
  timeout: 30000,
  shell: false
});
console.log('Train stdout:', trainResult.stdout?.slice(0, 500));
console.log('Train stderr:', trainResult.stderr?.slice(0, 500));

// Test flight query
const flightSearchParams = {
  departureCityName: '南京',
  arrivalCityName: '上海',
  departureDate: '2026-05-05'
};
console.log('\n=== Flight Query ===');
const flightSearchResult = spawnSync('node', [tuniuPath, 'call', 'flight', 'searchLowestPriceFlight', '-a', JSON.stringify(flightSearchParams)], {
  env: { ...process.env, TUNIU_API_KEY },
  encoding: 'utf8',
  timeout: 30000,
  shell: false
});
console.log('Flight stdout:', flightSearchResult.stdout?.slice(0, 500));
console.log('Flight stderr:', flightSearchResult.stderr?.slice(0, 500));

// Test hotel query
const hotelParams = {
  cityName: '杭州',
  checkIn: '2026-05-04',
  checkOut: '2026-05-05',
  pageNum: 1
};
console.log('\n=== Hotel Query ===');
const hotelResult = spawnSync('node', [tuniuPath, 'call', 'hotel', 'tuniu_hotel_search', '-a', JSON.stringify(hotelParams)], {
  env: { ...process.env, TUNIU_API_KEY },
  encoding: 'utf8',
  timeout: 30000,
  shell: false
});
console.log('Hotel stdout:', hotelResult.stdout?.slice(0, 500));
console.log('Hotel stderr:', hotelResult.stderr?.slice(0, 500));