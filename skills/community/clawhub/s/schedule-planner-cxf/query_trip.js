const { spawnSync } = require('child_process');

const TUNIU_API_KEY = process.env.TUNIU_API_KEY || '';

// 优先 npx，降低对本地可变 npm 全局目录的直接依赖
function callTuniu(server, tool, params) {
    const result = spawnSync('npx', ['tuniu', 'call', server, tool, '-a', JSON.stringify(params)], {
        env: { ...process.env, TUNIU_API_KEY },
        encoding: 'utf8',
        timeout: 30000,
        shell: false
    });

    if (result.error) {
        console.error('Error:', result.error.message);
        return null;
    }

    try {
        const parsed = JSON.parse(result.stdout);
        if (parsed.result && parsed.result.content && parsed.result.content[0]) {
            return JSON.parse(parsed.result.content[0].text);
        }
        console.error('Invalid response structure:', parsed);
        return null;
    } catch (e) {
        console.error('Parse error:', e.message);
        return null;
    }
}

// 1. Query Hangzhou -> Beijing flight (June 4)
console.log('=== Query Hangzhou -> Beijing flight (June 4) ===');
const flights1 = callTuniu('flight', 'searchLowestPriceFlight', {
    departureCityName: '杭州',
    arrivalCityName: '北京',
    departureDate: '2026-06-04'
});
console.log('Hangzhou -> Beijing:', flights1 ? (flights1.flightList?.length || flights1.data?.length || 0) + ' flights' : 'failed');

// 2. Query Beijing -> Qinhuangdao train (June 5)
console.log('\n=== Query Beijing -> Qinhuangdao train (June 5) ===');
const trains1 = callTuniu('train', 'searchLowestPriceTrain', {
    departureCityName: '北京',
    arrivalCityName: '秦皇岛',
    departureDate: '2026-06-05'
});
console.log('Beijing -> Qinhuangdao:', trains1 ? `${trains1.data?.length || 0} trains` : 'failed');

// 3. Query Qinhuangdao -> Hangzhou flight (June 6)
console.log('\n=== Query Qinhuangdao -> Hangzhou flight (June 6) ===');
const flights2 = callTuniu('flight', 'searchLowestPriceFlight', {
    departureCityName: '秦皇岛',
    arrivalCityName: '杭州',
    departureDate: '2026-06-06'
});
console.log('Qinhuangdao -> Hangzhou:', flights2 ? (flights2.flightList?.length || flights2.data?.length || 0) + ' flights' : 'failed');

// 4. Query Beijing hotels (June 4-5)
console.log('\n=== Query Beijing hotels (June 4-5) ===');
const beijingHotels = callTuniu('hotel', 'tuniu_hotel_search', {
    cityName: '北京',
    checkIn: '2026-06-04',
    checkOut: '2026-06-05',
    keyword: '全季'
});
console.log('Beijing hotels:', beijingHotels ? `${beijingHotels.hotels?.length || 0} hotels` : 'failed');

// 5. Query Qinhuangdao hotels (June 5-6)
console.log('\n=== Query Qinhuangdao hotels (June 5-6) ===');
const qhdHotels = callTuniu('hotel', 'tuniu_hotel_search', {
    cityName: '秦皇岛',
    checkIn: '2026-06-05',
    checkOut: '2026-06-06',
    keyword: '全季'
});
console.log('Qinhuangdao hotels:', qhdHotels ? `${qhdHotels.hotels?.length || 0} hotels` : 'failed');

// Output details
console.log('\n\n=== Details ===');
console.log('\n[Hangzhou -> Beijing flights]');
if (flights1 && flights1.flightList) {
    flights1.flightList.slice(0, 5).forEach(f => {
        console.log(`  ${f.flightNo} | ${f.departureTime}-${f.arrivalTime} | ¥${f.price}`);
    });
}

console.log('\n[Beijing -> Qinhuangdao trains]');
if (trains1 && trains1.data) {
    trains1.data.slice(0, 5).forEach(t => {
        console.log(`  ${t.trainNum} | ${t.departureTime?.split(' ')[1]}-${t.arrivalTime?.split(' ')[1]} | ¥${t.price?.wzPrice || t.price}`);
    });
}

console.log('\n[Qinhuangdao -> Hangzhou flights]');
if (flights2 && flights2.flightList) {
    flights2.flightList.slice(0, 5).forEach(f => {
        console.log(`  ${f.flightNo || 'N/A'} | ${f.departureTime || 'N/A'} | ¥${f.price}`);
    });
}

console.log('\n[Beijing hotels]');
if (beijingHotels && beijingHotels.hotels) {
    beijingHotels.hotels.slice(0, 5).forEach(h => {
        console.log(`  ${h.hotelName} | ¥${h.lowestPrice} | ${h.business} | Score:${h.commentScore}`);
    });
}

console.log('\n[Qinhuangdao hotels]');
if (qhdHotels && qhdHotels.hotels) {
    qhdHotels.hotels.slice(0, 5).forEach(h => {
        console.log(`  ${h.hotelName} | ¥${h.lowestPrice} | ${h.business} | Score:${h.commentScore}`);
    });
}