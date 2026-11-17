/**
 * mock-data.js — Travel Planner Mock Data Module
 *
 * 提供内置模拟数据，无需 API Key 即可验证功能
 * 涵盖：景点、酒店、交通、行程等数据
 */

const mockAttractions = {
  '重庆': [
    { name: '洪崖洞', type: ['人文', '网红打卡'], ticketPrice: 0, rating: 4.6, openingHours: '11:00-23:00', estimatedDuration: '1.5-2小时', description: '重庆地标建筑，以夜景闻名，吊脚楼风格的民俗风貌区', highlight: '夜景灯光秀、巴渝民俗表演', reservationRequired: false, address: '渝中区嘉陵江滨江路88号' },
    { name: '解放碑', type: ['人文', '购物'], ticketPrice: 0, rating: 4.5, openingHours: '全天', estimatedDuration: '1小时', description: '重庆标志性商业中心，步行街集购物美食于一体', highlight: '抗战胜利纪功碑、八一好吃街', reservationRequired: false, address: '渝中区解放碑商圈' },
    { name: '长江索道', type: ['网红打卡', '自然'], ticketPrice: 30, rating: 4.4, openingHours: '07:30-22:00', estimatedDuration: '0.5小时', description: '横跨长江的空中索道，俯瞰两岸风光', highlight: '空中看重庆、山城夜景', reservationRequired: false, address: '渝中区新华路151号' },
    { name: '磁器口古镇', type: ['人文', '美食'], ticketPrice: 0, rating: 4.3, openingHours: '全天', estimatedDuration: '2-3小时', description: '千年古镇，保存完好的明清建筑群，美食汇聚', highlight: '陈麻花、毛血旺、古镇夜景', reservationRequired: false, address: '沙坪坝区磁器口镇' },
    { name: '武隆天生三桥', type: ['自然'], ticketPrice: 125, rating: 4.6, openingHours: '08:00-18:00', estimatedDuration: '3-4小时', description: '世界自然遗产，巨型天坑与天然石桥群，壮观震撼', highlight: '三桥夹两坑、变形金刚取景地', reservationRequired: false, address: '武隆区仙女山镇' },
    { name: '南山一棵树观景台', type: ['自然', '网红打卡'], ticketPrice: 30, rating: 4.5, openingHours: '09:00-22:30', estimatedDuration: '1-2小时', description: '俯瞰重庆全景的最佳观景点，夜景尤为震撼', highlight: '360度全景、夜景最佳拍摄点', reservationRequired: false, address: '南岸区南山公园路' },
    { name: '李子坝轻轨站', type: ['网红打卡'], ticketPrice: 0, rating: 4.2, openingHours: '06:30-23:00', estimatedDuration: '0.5小时', description: '轻轨穿楼而过的奇特景观，网红打卡地', highlight: '轻轨穿楼、最佳拍照点在楼下广场', reservationRequired: false, address: '渝中区李子坝正街' },
    { name: '重庆动物园', type: ['亲子'], ticketPrice: 25, rating: 4.3, openingHours: '08:00-18:00', estimatedDuration: '2-3小时', description: '大型城市动物园，国宝大熊猫众多', highlight: '熊猫馆、两栖爬行馆、儿童动物园', reservationRequired: false, address: '九龙坡区西郊一村' },
    { name: '湖广会馆', type: ['人文'], ticketPrice: 30, rating: 4.2, openingHours: '09:00-17:00', estimatedDuration: '1-1.5小时', description: '清代建筑群，见证重庆移民历史的会馆建筑', highlight: '古戏台、移民博物馆、古建筑群', reservationRequired: false, address: '渝中区长滨路' },
    { name: '三峡博物馆', type: ['人文'], ticketPrice: 0, rating: 4.5, openingHours: '09:00-17:00（周一闭馆）', estimatedDuration: '2-3小时', description: '展示三峡文化和重庆历史的大型博物馆', highlight: '三峡文物、巴蜀青铜器、重庆城市发展史', reservationRequired: true, address: '渝中区人民路236号' }
  ],
  '成都': [
    { name: '大熊猫繁育研究基地', type: ['亲子', '自然'], ticketPrice: 55, rating: 4.7, openingHours: '07:30-18:00', estimatedDuration: '3-4小时', description: '全球最大的熊猫繁育机构，近距离观察国宝', highlight: '熊猫幼崽、熊猫产房、天鹅湖', reservationRequired: true, address: '成华区熊猫大道1375号' },
    { name: '宽窄巷子', type: ['人文', '美食'], ticketPrice: 0, rating: 4.5, openingHours: '全天', estimatedDuration: '2小时', description: '成都历史文化街区，清朝古街道改造的商业步行街', highlight: '川剧变脸表演、地道小吃、文创店', reservationRequired: false, address: '青羊区长顺上街' },
    { name: '锦里古街', type: ['人文', '美食'], ticketPrice: 0, rating: 4.4, openingHours: '全天', estimatedDuration: '1.5-2小时', description: '武侯祠旁的古街，重现蜀地民俗风貌', highlight: '红灯笼夜景、三国文化工艺品、张飞牛肉', reservationRequired: false, address: '武侯区武侯祠大街231号' },
    { name: '都江堰', type: ['自然', '人文'], ticketPrice: 80, rating: 4.6, openingHours: '08:00-18:00', estimatedDuration: '3-4小时', description: '两千多年历史的水利工程，至今仍在发挥作用', highlight: '鱼嘴分水堤、飞沙堰、宝瓶口', reservationRequired: false, address: '都江堰市公园路' },
    { name: '青城山', type: ['自然'], ticketPrice: 90, rating: 4.5, openingHours: '08:00-17:30', estimatedDuration: '4-6小时', description: '道教名山，青翠幽静，有"青城天下幽"之美誉', highlight: '天师洞、上清宫、老君阁', reservationRequired: false, address: '都江堰市青城山镇' }
  ],
  '上海': [
    { name: '外滩', type: ['人文', '网红打卡'], ticketPrice: 0, rating: 4.7, openingHours: '全天', estimatedDuration: '1-2小时', description: '上海标志性景观带，万国建筑博览群与陆家嘴天际线', highlight: '万国建筑群、浦江夜景、陆家嘴天际线', reservationRequired: false, address: '黄浦区中山东一路' },
    { name: '迪士尼乐园', type: ['亲子', '娱乐'], ticketPrice: 475, rating: 4.8, openingHours: '08:30-20:30', estimatedDuration: '8-10小时', description: '中国大陆首座迪士尼主题乐园', highlight: '飞跃地平线、创极速光轮、烟花秀', reservationRequired: true, address: '浦东新区申迪北路753号' },
    { name: '豫园', type: ['人文'], ticketPrice: 40, rating: 4.4, openingHours: '09:00-16:30', estimatedDuration: '1.5-2小时', description: '明代江南古典园林，上海保存最完整的传统园林', highlight: '假山堆叠、九曲桥、湖心亭', reservationRequired: false, address: '黄浦区豫园老街' }
  ],
  '西安': [
    { name: '兵马俑', type: ['人文'], ticketPrice: 120, rating: 4.7, openingHours: '08:30-18:00', estimatedDuration: '3-4小时', description: '世界第八大奇迹，秦始皇陵陪葬坑，规模宏大令人震撼', highlight: '一号坑军阵、铜车马、精品展厅', reservationRequired: true, address: '临潼区秦陵北路' },
    { name: '大雁塔', type: ['人文'], ticketPrice: 40, rating: 4.5, openingHours: '08:00-18:00', estimatedDuration: '1.5-2小时', description: '唐代古塔，玄奘法师译经之地', highlight: '登塔俯瞰、大唐不夜城夜景、音乐喷泉', reservationRequired: false, address: '雁塔区慈恩路' },
    { name: '回民街', type: ['美食'], ticketPrice: 0, rating: 4.3, openingHours: '全天', estimatedDuration: '1.5-2小时', description: '西安最著名的美食街，汇聚西北特色小吃', highlight: '羊肉泡馍、肉夹馍、凉皮、烤肉', reservationRequired: false, address: '莲湖区北院门' }
  ]
};

const mockHotels = {
  '重庆': [
    { name: '重庆解放碑威斯汀酒店', area: '解放碑', price: 899, rating: 4.7, features: '江景房、行政酒廊、屋顶泳池', distance: '步行5分钟到解放碑' },
    { name: '全季酒店（解放碑店）', area: '解放碑', price: 380, rating: 4.5, features: '含早、地铁口、免费洗衣', distance: '步行10分钟到洪崖洞' },
    { name: '亚朵酒店（观音桥店）', area: '观音桥', price: 420, rating: 4.6, features: '含早、健身房、24h书吧', distance: '近地铁3号线' }
  ],
  '成都': [
    { name: '成都博舍', area: '太古里', price: 1280, rating: 4.8, features: '设计酒店、院落房型、米其林餐厅', distance: '紧邻太古里' },
    { name: '全季酒店（春熙路店）', area: '春熙路', price: 360, rating: 4.5, features: '含早、免费停车、自助洗衣', distance: '步行5分钟到IFS' }
  ]
};

const mockTransport = {
  '重庆': {
    airport: '重庆江北国际机场',
    trainStation: '重庆北站 / 重庆西站 / 沙坪坝站',
    metroNote: '轨道交通覆盖主要景点，下载"渝畅行"APP扫码乘车',
    tips: '重庆道路复杂，虽然有地图导航但仍易走错，建议多利用地铁出行'
  },
  '成都': {
    airport: '成都双流国际机场 / 天府国际机场',
    trainStation: '成都东站 / 成都南站 / 成都西站',
    metroNote: '地铁覆盖主要市区景点，下载"成都地铁"APP扫码乘车',
    tips: '市区景点地铁均可到达，建议购买地铁日票更划算'
  }
};

/**
 * 获取指定城市的模拟景点数据
 */
function getMockAttractions(city) {
  return structuredClone(mockAttractions[city] || []);
}

/**
 * 获取指定城市的模拟酒店数据
 */
function getMockHotels(city) {
  return structuredClone(mockHotels[city] || []);
}

/**
 * 获取指定城市的模拟交通信息
 */
function getMockTransport(city) {
  return structuredClone(mockTransport[city] || null);
}

/**
 * 获取所有支持的城市列表
 */
function getSupportedCities() {
  return Object.keys(mockAttractions);
}

/**
 * 根据偏好筛选景点
 */
function filterByPreference(attractions, preferences) {
  if (!preferences || preferences.length === 0) return attractions;

  return attractions.map(a => {
    const matchCount = a.type.filter(t => preferences.includes(t)).length;
    return { ...a, _matchScore: matchCount / Math.max(preferences.length, 1) };
  }).sort((a, b) => (b._matchScore || 0) - (a._matchScore || 0));
}

/**
 * 按预算筛选景点
 * @param {Array} attractions - 景点列表
 * @param {number} totalBudget - 总预算
 * @param {number} days - 天数
 * @param {number} dailyAttractions - 每天预计景点数
 */
function filterByBudget(attractions, totalBudget, days, dailyAttractions = 2) {
  const ticketBudget = totalBudget * 0.12; // 门票占总预算12%
  const totalSpots = days * dailyAttractions;
  const perSpotMax = ticketBudget / totalSpots;

  return attractions.map(a => {
    const price = a.ticketPrice || 0;
    return {
      ...a,
      _budgetFit: price === 0 ? 1.0 : (price <= perSpotMax * 0.5 ? 0.8 : (price <= perSpotMax ? 0.5 : 0.0)),
      _withinBudget: price <= perSpotMax || price === 0
    };
  }).sort((a, b) => (b._budgetFit || 0) - (a._budgetFit || 0));
}

module.exports = {
  mockAttractions,
  mockHotels,
  mockTransport,
  getMockAttractions,
  getMockHotels,
  getMockTransport,
  getSupportedCities,
  filterByPreference,
  filterByBudget
};
