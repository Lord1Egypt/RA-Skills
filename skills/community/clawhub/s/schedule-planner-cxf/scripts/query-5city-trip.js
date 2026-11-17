'use strict';
const { callTuniu, validateQuery } = require('./lib/tuniu');
const { readJson, object, array, writeOutput } = require('./lib/safety');
const mock = require('./mock-data');
const str = value => value == null ? '' : String(value);
const price = value => value == null || value === '' ? null : Number(value);
function queryTrain(from, to, date, useMock = false) {
  const result = useMock ? { data: mock.getMockTrains(from, to, date) } : callTuniu('train', 'searchLowestPriceTrain', {
    departureCityName: from, arrivalCityName: to, departureDate: date
  });
  return (result.data || []).slice(0, 3).map(t => ({
    trainNo: str(t.trainNum), departureTime: str(t.departureTime), arrivalTime: str(t.arrivalTime),
    duration: str(t.duration), price: price(t.price?.edzPrice ?? t.price?.ydzPrice ?? t.price?.wzPrice ?? (typeof t.price === 'object' ? null : t.price)), seatType: t.price?.edzPrice ? '二等座' : ''
  }));
}
function queryFlight(from, to, date, useMock = false) {
  const result = useMock ? { data: mock.getMockFlights(from, to, date) } : callTuniu('flight', 'searchLowestPriceFlight', {
    departureCityName: from, arrivalCityName: to, departureDate: date
  });
  return (result.data || result.flightList || []).slice(0, 3).map(f => ({
    flightNo: str(f.flightNumber ?? f.flightNo), airline: str(f.airlineCompany), departureTime: str(f.departureTime),
    arrivalTime: str(f.arrivalTime), duration: str(f.flyTime ?? f.totalDuration), price: price(f.basePrice ?? f.price),
    departureAirport: str(f.departureAirport), arrivalAirport: str(f.arrivalAirport)
  }));
}
function queryHotel(city, checkIn, checkOut, useMock = false) {
  const result = useMock ? { hotels: mock.getMockHotels(city) } : callTuniu('hotel', 'tuniu_hotel_search', { cityName: city, checkIn, checkOut, pageNum: 1 });
  return (result.hotels || []).slice(0, 3).map(h => ({
    hotelId: str(h.hotelId), name: str(h.hotelName), address: str(h.address), business: str(h.business),
    price: price(h.lowestPrice), rating: Number(h.commentScore ?? 0), starName: str(h.starName), meal: str(h.meal), refund: str(h.refund)
  }));
}
function main(args = process.argv.slice(2)) {
  const useMock = args.includes('--mock');
  let input;
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--input') { input = args[++i]; if (!input || input.startsWith('--')) throw new Error('--input requires a file.'); }
    else if (!['--mock', '--desktop'].includes(args[i])) throw new Error('Unsupported query argument.');
  }
  if (useMock && input) throw new Error('--mock uses only the bundled example plan.');
  if (!useMock && !input) throw new Error('Use --input PLAN.json for live queries, or --mock for an offline demo.');
  const plan = readJson(input || require('node:path').join(__dirname, '../examples/query-plan.json'));
  object(plan, ['routes', 'hotels'], 'query plan'); array(plan.routes, 'routes', 10); array(plan.hotels, 'hotels', 10);
  // Validate the whole plan before the first external call.
  for (const r of plan.routes) {
    object(r, ['type', 'from', 'to', 'date'], 'route');
    if (!['train', 'flight'].includes(r.type)) throw new Error('Unsupported route type.');
    validateQuery(r.type, r.type === 'train' ? 'searchLowestPriceTrain' : 'searchLowestPriceFlight', { departureCityName: r.from, arrivalCityName: r.to, departureDate: r.date });
  }
  for (const h of plan.hotels) {
    object(h, ['city', 'checkIn', 'checkOut'], 'hotel');
    validateQuery('hotel', 'tuniu_hotel_search', { cityName: h.city, checkIn: h.checkIn, checkOut: h.checkOut });
  }
  const result = {
    mock: useMock,
    routes: plan.routes.map(r => ({ ...r, options: (r.type === 'train' ? queryTrain : queryFlight)(r.from, r.to, r.date, useMock) })),
    hotels: plan.hotels.map(h => ({ ...h, options: queryHotel(h.city, h.checkIn, h.checkOut, useMock) }))
  };
  require('./generate-5city-trip').generateHTML(result);
  console.log(useMock ? 'MOCK DATA: not live prices.' : 'Live query results: prices may change.');
  console.log('Results saved:', writeOutput(JSON.stringify(result, null, 2), 'comparison', 'json', args.includes('--desktop')));
  return result;
}
if (require.main === module) {
  try { main(); } catch { console.error('Query failed. Check plan schema, dependencies and API configuration. No automatic mock fallback.'); process.exitCode = 1; }
}
module.exports = { main, queryTrain, queryFlight, queryHotel };
