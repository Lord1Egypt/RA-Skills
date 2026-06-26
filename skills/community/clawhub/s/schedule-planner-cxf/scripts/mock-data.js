/**
 * mock-data.js — Mock 数据模块
 *
 * 当无 API Key 或指定 --mock 参数时，提供预置的模拟数据，
 * 使得本技能无需外部依赖即可运行和演示。
 *
 * 使用方法：
 *   const { getMockTrains, getMockFlights, getMockHotels } = require('./mock-data');
 *   const trains = getMockTrains('杭州', '南京', '2026-06-15');
 */

// ========== 模拟交通数据 ==========

const MOCK_TRAINS = {
  '杭州-南京': [
    { trainNum: 'G7650', departureTime: '2026-05-04 07:30', arrivalTime: '2026-05-04 09:15', duration: '1小时45分', price: { edzPrice: 117.5 } },
    { trainNum: 'G7582', departureTime: '2026-05-04 09:00', arrivalTime: '2026-05-04 10:45', duration: '1小时45分', price: { edzPrice: 117.5 } },
    { trainNum: 'G7666', departureTime: '2026-05-04 14:00', arrivalTime: '2026-05-04 15:45', duration: '1小时45分', price: { edzPrice: 117.5 } },
  ],
  '上海-苏州': [
    { trainNum: 'G7006', departureTime: '2026-05-06 08:00', arrivalTime: '2026-05-06 08:30', duration: '30分', price: { edzPrice: 34.5 } },
    { trainNum: 'G7012', departureTime: '2026-05-06 09:00', arrivalTime: '2026-05-06 09:30', duration: '30分', price: { edzPrice: 34.5 } },
    { trainNum: 'G7028', departureTime: '2026-05-06 14:00', arrivalTime: '2026-05-06 14:30', duration: '30分', price: { edzPrice: 34.5 } },
  ],
  '苏州-北京': [
    { trainNum: 'G108', departureTime: '2026-05-07 08:00', arrivalTime: '2026-05-07 12:36', duration: '4小时36分', price: { edzPrice: 523.5 } },
    { trainNum: 'G112', departureTime: '2026-05-07 09:00', arrivalTime: '2026-05-07 13:37', duration: '4小时37分', price: { edzPrice: 523.5 } },
    { trainNum: 'G128', departureTime: '2026-05-07 14:00', arrivalTime: '2026-05-07 18:26', duration: '4小时26分', price: { edzPrice: 523.5 } },
  ],
};

const MOCK_FLIGHTS = {
  '南京-上海': [
    { flightNumber: 'MU2881', airlineCompany: '东方航空', departureTime: '2026-05-05 08:00', arrivalTime: '2026-05-05 09:00', flyTime: '1小时', basePrice: 320, departureAirport: '南京禄口T2', arrivalAirport: '上海虹桥T2' },
    { flightNumber: 'CA4518', airlineCompany: '中国国航', departureTime: '2026-05-05 10:00', arrivalTime: '2026-05-05 11:00', flyTime: '1小时', basePrice: 380, departureAirport: '南京禄口T1', arrivalAirport: '上海浦东T2' },
  ],
  '北京-杭州': [
    { flightNumber: 'CA1704', airlineCompany: '中国国航', departureTime: '2026-05-08 07:30', arrivalTime: '2026-05-08 09:45', flyTime: '2小时15分', basePrice: 480, departureAirport: '北京首都T3', arrivalAirport: '杭州萧山T3' },
    { flightNumber: 'HU7181', airlineCompany: '海南航空', departureTime: '2026-05-08 09:30', arrivalTime: '2026-05-08 11:45', flyTime: '2小时15分', basePrice: 520, departureAirport: '北京首都T2', arrivalAirport: '杭州萧山T2' },
  ],
};

const MOCK_HOTELS = {
  '南京': [
    { hotelId: '2108379001', hotelName: '南京金陵饭店', address: '鼓楼区新街口广场', business: '新街口商圈', lowestPrice: 498, commentScore: 4.7, starName: '五星级', meal: '含双早', refund: '可免费取消' },
    { hotelId: '2108379002', hotelName: '南京中心大酒店', address: '鼓楼区中山南路', business: '新街口商圈', lowestPrice: 358, commentScore: 4.5, starName: '四星级', meal: '含早', refund: '可取消' },
  ],
  '上海': [
    { hotelId: '2108379003', hotelName: '上海国际饭店', address: '黄浦区南京西路', business: '人民广场', lowestPrice: 598, commentScore: 4.6, starName: '四星级', meal: '含双早', refund: '可免费取消' },
    { hotelId: '2108379004', hotelName: '全季酒店（南京路店）', address: '黄浦区南京东路', business: '南京路商圈', lowestPrice: 378, commentScore: 4.5, starName: '舒适型', meal: '含早', refund: '可取消' },
  ],
  '苏州': [
    { hotelId: '2108379005', hotelName: '苏州凯悦酒店', address: '工业园区华池街88号', business: '金鸡湖商圈', lowestPrice: 589, commentScore: 4.8, starName: '五星级', meal: '含双早', refund: '可免费取消' },
    { hotelId: '2108379006', hotelName: '全季酒店（苏州观前街店）', address: '姑苏区观前街', business: '观前街商圈', lowestPrice: 328, commentScore: 4.6, starName: '舒适型', meal: '含早', refund: '可免费取消' },
  ],
  '北京': [
    { hotelId: '2108379007', hotelName: '北京国贸大酒店', address: '朝阳区建国门外大街1号', business: '国贸CBD', lowestPrice: 898, commentScore: 4.8, starName: '五星级', meal: '含双早', refund: '可免费取消' },
    { hotelId: '2108379008', hotelName: '全季酒店（北京国贸店）', address: '朝阳区建国路', business: '国贸CBD', lowestPrice: 458, commentScore: 4.5, starName: '舒适型', meal: '含早', refund: '可取消' },
  ],
  '杭州': [
    { hotelId: '2108379009', hotelName: '万斯酒店（阿里巴巴西溪园区店）', address: '余杭塘路未来星宸6号楼', business: '未来科技城', lowestPrice: 497, commentScore: 4.8, starName: '高档型', meal: '含双早', refund: '可免费取消' },
    { hotelId: '2108379010', hotelName: '全季酒店（杭州海创园店）', address: '文一西路1000号', business: '未来科技城', lowestPrice: 391, commentScore: 4.7, starName: '舒适型', meal: '含早', refund: '可免费取消' },
  ],
};


/**
 * 检查是否应使用 Mock 模式
 * 条件：--mock 参数 或 缺少 TUNIU_API_KEY
 */
function shouldUseMock(args) {
  if (args && args.includes('--mock')) {
    return true;
  }
  const apiKey = process.env.TUNIU_API_KEY || process.env.AMAP_API_KEY;
  if (!apiKey || apiKey === '' || apiKey.startsWith('your_')) {
    return true;
  }
  return false;
}

/**
 * 获取 mock 火车数据
 */
function getMockTrains(from, to, date) {
  const key = `${from}-${to}`;
  const trains = MOCK_TRAINS[key];
  if (!trains) return [];
  return trains.map(t => ({ ...t, departureTime: t.departureTime, arrivalTime: t.arrivalTime }));
}

/**
 * 获取 mock 航班数据
 */
function getMockFlights(from, to, date) {
  const key = `${from}-${to}`;
  return MOCK_FLIGHTS[key] || [];
}

/**
 * 获取 mock 酒店数据
 */
function getMockHotels(city) {
  return MOCK_HOTELS[city] || [];
}

/**
 * 获取 mock 行程总数据（用于 generate-trip-page.js）
 */
function getMockTripData() {
  return {
    tripType: '出差',
    destination: '杭州',
    duration: '2026-06-15 至 2026-06-17（2晚3天）',
    passenger: '张明（Mock）',
    segments: [
      { type: 'train', segmentNo: 'G7535', departure: '上海虹桥 08:00', arrival: '杭州东 09:00', date: '2026-06-15', price: 73, seat: '二等座', duration: '1小时', orderId: 'MOCK-TRAIN-001' },
      { type: 'hotel', name: '万斯酒店（阿里巴巴西溪园区店）', address: '余杭塘路未来星宸6号楼', roomType: '高级大床房-含双早', checkIn: '2026-06-15 14:00后', checkOut: '2026-06-17 12:00前', nights: 2, price: 497, orderId: 'MOCK-HOTEL-001' },
      { type: 'train', segmentNo: 'G7540', departure: '杭州东 18:00', arrival: '上海虹桥 19:00', date: '2026-06-17', price: 73, seat: '二等座', duration: '1小时', orderId: 'MOCK-TRAIN-002' },
    ],
    dailyPlan: [
      { day: 'Day 1（06-15）', title: '上海 → 杭州，入住酒店', items: ['🚄 G7535 上海虹桥 08:00 → 杭州东 09:00', '🏨 入住万斯酒店（阿里巴巴店）', '💼 下午前往阿里巴巴西溪园区拜访客户'] },
      { day: 'Day 2（06-16）', title: '全天工作', items: ['🏨 酒店早餐（含双早）', '💼 全天阿里巴巴西溪园区办公'] },
      { day: 'Day 3（06-17）', title: '返程', items: ['🏨 酒店早餐，12:00前退房', '🚄 G7540 杭州东 18:00 → 上海虹桥 19:00'] },
    ],
    costs: { train1: 73, train2: 73, hotel: 994, total: 1140 },
    tips: ['请提前30分钟到达火车站', '杭州6月气温25-32℃，注意防晒', '酒店距阿里步行10分钟', '本行程为模拟演示数据'],
    paymentUrl: 'https://m.tuniu.com/u/order?page=1&filter=0-0-1'
  };
}

module.exports = {
  shouldUseMock,
  getMockTrains,
  getMockFlights,
  getMockHotels,
  getMockTripData,
  MOCK_TRAINS,
  MOCK_FLIGHTS,
  MOCK_HOTELS,
};