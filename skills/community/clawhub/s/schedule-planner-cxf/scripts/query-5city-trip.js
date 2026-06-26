const { spawnSync } = require('child_process');
const fs = require('fs');
const path = require('path');

// === Mock mode support ===
const args = process.argv.slice(2);
const mockModule = path.join(__dirname, 'mock-data.js');
let useMock = args.includes('--mock');

const TUNIU_API_KEY = process.env.TUNIU_API_KEY || '';

// Auto-detect mock mode: no API key or placeholder key
if (!useMock && (!TUNIU_API_KEY || TUNIU_API_KEY.startsWith('your_'))) {
  useMock = true;
  console.log('[Auto] No valid TUNIU_API_KEY detected, falling back to mock data');
}

if (useMock) {
  console.log('[Mock mode] Generating 5-city trip with simulated data...');
  const { getMockTrains, getMockFlights, getMockHotels } = require(mockModule);

  const routes = [
    { type: 'train', from: '杭州', to: '南京', date: '2026-05-04',
      options: getMockTrains('杭州', '南京', '2026-05-04').map(t => ({
        trainNo: t.trainNum, departureTime: t.departureTime, arrivalTime: t.arrivalTime,
        duration: t.duration, price: t.price.edzPrice, seatType: '二等座'
      }))
    },
    { type: 'flight', from: '南京', to: '上海', date: '2026-05-05',
      options: getMockFlights('南京', '上海', '2026-05-05').map(f => ({
        flightNo: f.flightNumber, airline: f.airlineCompany, departureTime: f.departureTime,
        arrivalTime: f.arrivalTime, duration: f.flyTime, price: f.basePrice,
        departureAirport: f.departureAirport, arrivalAirport: f.arrivalAirport
      }))
    },
    { type: 'train', from: '上海', to: '苏州', date: '2026-05-06',
      options: getMockTrains('上海', '苏州', '2026-05-06').map(t => ({
        trainNo: t.trainNum, departureTime: t.departureTime, arrivalTime: t.arrivalTime,
        duration: t.duration, price: t.price.edzPrice, seatType: '二等座'
      }))
    },
    { type: 'train', from: '苏州', to: '北京', date: '2026-05-07',
      options: getMockTrains('苏州', '北京', '2026-05-07').map(t => ({
        trainNo: t.trainNum, departureTime: t.departureTime, arrivalTime: t.arrivalTime,
        duration: t.duration, price: t.price.edzPrice, seatType: '二等座'
      }))
    },
    { type: 'flight', from: '北京', to: '杭州', date: '2026-05-08',
      options: getMockFlights('北京', '杭州', '2026-05-08').map(f => ({
        flightNo: f.flightNumber, airline: f.airlineCompany, departureTime: f.departureTime,
        arrivalTime: f.arrivalTime, duration: f.flyTime, price: f.basePrice,
        departureAirport: f.departureAirport, arrivalAirport: f.arrivalAirport
      }))
    },
  ];

  const hotels = [
    { city: '南京', checkIn: '2026-05-04', checkOut: '2026-05-05',
      options: getMockHotels('南京') },
    { city: '上海', checkIn: '2026-05-05', checkOut: '2026-05-06',
      options: getMockHotels('上海') },
    { city: '苏州', checkIn: '2026-05-06', checkOut: '2026-05-07',
      options: getMockHotels('苏州') },
    { city: '北京', checkIn: '2026-05-07', checkOut: '2026-05-08',
      options: getMockHotels('北京') },
  ];

  const desktopPath = path.join(process.env.USERPROFILE || '~', 'Desktop');
  const data = { routes, hotels };
  const dataFile = path.join(desktopPath, '5city-trip.json');
  fs.writeFileSync(dataFile, JSON.stringify(data, null, 2));
  console.log('\n[Mock] Data saved to:', dataFile);
  process.exit(0);
}

// === Real mode: API key available ===
const tuniuPath = path.join(
  process.env.APPDATA || process.env.HOME || '',
  'npm', 'node_modules', 'tuniu-cli', 'bin', 'tuniu.js'
);

// Passenger info - use env vars, never hardcode
const passengerInfo = {
  name: process.env.PASSENGER_NAME || 'Passenger',
  id: process.env.PASSENGER_ID || '',
  phone: process.env.PASSENGER_MOBILE || ''
};

// Call Tuniu CLI
function callTuniu(server, tool, params) {
  const result = spawnSync('node', [tuniuPath, 'call', server, tool, '-a', JSON.stringify(params)], {
    env: { ...process.env, TUNIU_API_KEY },
    encoding: 'utf8',
    stdio: ['pipe', 'pipe', 'pipe'],
    timeout: 30000,
    shell: false
  });

  try {
    const parsed = JSON.parse(result.stdout);
    if (parsed.result?.structuredContent?.result) {
      return JSON.parse(parsed.result.structuredContent.result);
    }
    if (parsed.result?.content?.[0]?.text) {
      return JSON.parse(parsed.result.content[0].text);
    }
    return parsed;
  } catch (e) {
    console.error('Parse error:', e.message);
    return null;
  }
}

// Query trains
function queryTrain(from, to, date) {
  const result = callTuniu('train', 'searchLowestPriceTrain', {
    departureCityName: from,
    arrivalCityName: to,
    departureDate: date
  });
  const trains = result?.data || [];
  const highSpeed = trains.filter(t => t.trainType === 'high-speed' || t.trainNum?.startsWith('G') || t.trainNum?.startsWith('D'));
  return (highSpeed.length > 0 ? highSpeed : trains).slice(0, 3).map(t => ({
    trainNo: t.trainNum,
    departureTime: t.departureTime?.split(' ')[1] || t.departureTime,
    arrivalTime: t.arrivalTime?.split(' ')[1] || t.arrivalTime,
    duration: t.duration,
    price: parseFloat(t.price?.edzPrice || t.price?.ydzPrice || t.price?.wzPrice || 0),
    seatType: t.price?.edzPrice ? '二等座' : '硬座'
  }));
}

// Query flights
function queryFlight(from, to, date) {
  const result = callTuniu('flight', 'searchLowestPriceFlight', {
    departureCityName: from,
    arrivalCityName: to,
    departureDate: date
  });
  const flights = result?.data || [];
  return flights.slice(0, 3).map(f => ({
    flightNo: f.flightNumber,
    airline: f.airlineCompany,
    departureTime: f.departureTime?.split(' ')[1] || f.departureTime,
    arrivalTime: f.arrivalTime?.split(' ')[1] || f.arrivalTime,
    duration: f.flyTime || f.totalDuration,
    price: parseFloat(f.basePrice || 0),
    departureAirport: f.departureAirport,
    arrivalAirport: f.arrivalAirport
  }));
}

// Query hotels
function queryHotel(city, checkIn, checkOut) {
  const result = callTuniu('hotel', 'tuniu_hotel_search', {
    cityName: city,
    checkIn: checkIn,
    checkOut: checkOut,
    pageNum: 1
  });
  const hotels = result?.hotels || [];
  return hotels.slice(0, 3).map(h => ({
    hotelId: String(h.hotelId),
    name: h.hotelName,
    address: h.address,
    business: h.business,
    price: h.lowestPrice,
    rating: h.commentScore,
    starName: h.starName,
    meal: h.meal,
    refund: h.refund,
    reviewCount: h.reviewCount || 0
  }));
}

// Main function
function main() {
  const tripData = {
    passenger: passengerInfo,
    startDate: '2026-05-04',
    routes: [],
    hotels: []
  };

  // 1. Hangzhou -> Nanjing (train)
  tripData.routes.push({
    type: 'train', from: '杭州', to: '南京', date: '2026-05-04',
    options: queryTrain('杭州', '南京', '2026-05-04')
  });

  // 2. Nanjing -> Shanghai (flight)
  tripData.routes.push({
    type: 'flight', from: '南京', to: '上海', date: '2026-05-05',
    options: queryFlight('南京', '上海', '2026-05-05')
  });

  // 3. Shanghai -> Suzhou (train)
  tripData.routes.push({
    type: 'train', from: '上海', to: '苏州', date: '2026-05-06',
    options: queryTrain('上海', '苏州', '2026-05-06')
  });

  // 4. Suzhou -> Beijing (train)
  tripData.routes.push({
    type: 'train', from: '苏州', to: '北京', date: '2026-05-07',
    options: queryTrain('苏州', '北京', '2026-05-07')
  });

  // 5. Beijing -> Hangzhou (flight)
  tripData.routes.push({
    type: 'flight', from: '北京', to: '杭州', date: '2026-05-08',
    options: queryFlight('北京', '杭州', '2026-05-08')
  });

  // Hotels
  tripData.hotels.push({
    city: '南京', checkIn: '2026-05-04', checkOut: '2026-05-05',
    options: queryHotel('南京', '2026-05-04', '2026-05-05')
  });
  tripData.hotels.push({
    city: '上海', checkIn: '2026-05-05', checkOut: '2026-05-06',
    options: queryHotel('上海', '2026-05-05', '2026-05-06')
  });
  tripData.hotels.push({
    city: '苏州', checkIn: '2026-05-06', checkOut: '2026-05-07',
    options: queryHotel('苏州', '2026-05-06', '2026-05-07')
  });
  tripData.hotels.push({
    city: '北京', checkIn: '2026-05-07', checkOut: '2026-05-08',
    options: queryHotel('北京', '2026-05-07', '2026-05-08')
  });

  // Save data
  const desktopPath = path.join(process.env.USERPROFILE || '~', 'Desktop');
  const dataFile = path.join(desktopPath, '5city-trip.json');
  fs.writeFileSync(dataFile, JSON.stringify(tripData, null, 2));
  console.log('Data saved to:', dataFile);

  return tripData;
}

if (require.main === module) {
  main();
}
module.exports = { main, queryTrain, queryFlight, queryHotel };