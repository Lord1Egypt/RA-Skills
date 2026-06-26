function getConfig() {
  return process.env.TMAP_LBS_CONFIG || null;
}

function setConfig(value) {
  if (!value) return false;
  process.env.TMAP_LBS_CONFIG = value;
  return true;
}

/**
 * 检查并获取配置，未设置时抛出错误
 * @returns {string} 配置值
 */
function ensureConfig() {
  const config = process.env.TMAP_LBS_CONFIG;

  if (!config) {
    console.log('\n⚠️  未找到腾讯地图配置');
    console.log('请访问以下地址创建应用并获取配置:');
    console.log('https://lbs.qq.com/dev/console/application/mine\n');
    throw new Error('请在 OpenClaw 配置页面设置腾讯位置服务配置，同时不要分享给任何陌生人');
  }

  return config;
}

/**
 * 使用 fetch 发起 HTTP GET 请求
 * @param {string} url - 请求 URL
 * @param {Object} params - 查询参数
 * @returns {Promise<Object|null>} 解析后的 JSON 响应
 */
async function http_request(url, params) {
  // 拼接查询参数
  const paramStr = Object.entries(params)
    .filter(([, v]) => v !== undefined && v !== null && v !== '')
    .map(([k, v]) => `${encodeURIComponent(k)}=${encodeURIComponent(v)}`)
    .join('&');

  const endpoint = paramStr ? `${url}?${paramStr}` : url;

  try {
    const response = await fetch(endpoint, {
      method: 'GET',
      signal: AbortSignal.timeout(15000),
    });
    return await response.json();
  } catch (error) {
    console.error('[fetch] 请求失败:', error.message);
    return null;
  }
}

/**
 * 坐标格式转换：将 "经度,纬度" 转为腾讯地图格式 "纬度,经度"
 * 腾讯地图坐标格式: lat,lng
 * @param {string} coordStr - "经度,纬度" 格式的字符串
 * @returns {string} "纬度,经度" 格式的字符串
 */
function flip_coord(coordStr) {
  const [lng, lat] = coordStr.split(',').map((s) => s.trim());
  return `${lat},${lng}`;
}

/**
 * POI 搜索
 * @param {Object} params - 搜索参数
 * @param {string} params.keywords - 查询关键字
 * @param {string} params.city - 城市名称或城市编码
 * @param {string} params.types - POI类型（分类筛选）
 * @param {string} params.location - 中心点坐标 "经度,纬度"
 * @param {number} params.radius - 搜索半径(米)
 * @param {number} params.page - 当前页数
 * @param {number} params.offset - 每页记录数(最大20)
 */
async function query_place(params) {
  const key = ensureConfig();

  const url = 'https://apis.map.qq.com/ws/place/v1/search';
  const hasCoord = params.location && params.radius;

  const queryOpts = {
    key: key,
    keyword: params.keywords || '',
    page_index: params.page || 1,
    page_size: Math.min(params.offset || 10, 20),
    output: 'json',
  };

  if (hasCoord) {
    const latLng = flip_coord(params.location);
    queryOpts.boundary = `nearby(${latLng},${params.radius})`;
  } else if (params.city) {
    const expandArea = params.cityLimit === false ? 1 : 0;
    queryOpts.boundary = `region(${params.city},${expandArea})`;
  }

  if (params.types) {
    queryOpts.filter = `category=${params.types}`;
  }

  console.log('[poi] 发起搜索请求...');
  const data = await http_request(url, queryOpts);

  if (!data) {
    console.error('[poi] 请求未返回数据');
    return null;
  }

  if (data.status === 0) {
    const count = data.count || (data.data ? data.data.length : 0);
    console.log(`[poi] 搜索完成，共 ${count} 条结果\n`);
    const pois = (data.data || []).map((item) => ({
      name: item.title,
      address: item.address || '',
      type: item.category || '',
      tel: item.tel || '',
      location: `${item.location.lng},${item.location.lat}`,
      distance: item._distance || undefined,
      id: item.id || '',
    }));
    return {
      status: '1',
      count: count,
      pois: pois,
      _raw: data,
    };
  } else {
    console.error('[poi] 搜索失败:', data.message);
    return null;
  }
}

/**
 * 步行路径规划
 * @param {Object} params - 规划参数
 * @param {string} params.origin - 起点坐标 "经度,纬度"
 * @param {string} params.destination - 终点坐标 "经度,纬度"
 */
async function walk_path(params) {
  const key = ensureConfig();

  const url = 'https://apis.map.qq.com/ws/direction/v1/walking/';
  const queryOpts = {
    key: key,
    from: flip_coord(params.origin),
    to: flip_coord(params.destination),
    output: 'json',
  };

  console.log('[route:walking] 发起步行路线请求...');
  const data = await http_request(url, queryOpts);

  if (!data) {
    console.error('[route:walking] 请求未返回数据');
    return null;
  }

  if (data.status === 0) {
    console.log('[route:walking] 路线规划完成\n');
    const route = data.result.routes[0];
    return {
      status: '1',
      route: {
        paths: [
          {
            distance: route.distance,
            duration: route.duration,
            direction: route.direction || '',
            steps: route.steps || [],
          },
        ],
      },
      _raw: data,
    };
  } else {
    console.error('[route:walking] 规划失败:', data.message);
    return null;
  }
}

/**
 * 驾车路径规划
 * @param {Object} params - 规划参数
 * @param {string} params.origin - 起点坐标 "经度,纬度"
 * @param {string} params.destination - 终点坐标 "经度,纬度"
 * @param {string} params.waypoints - 途经点坐标，多个用;分隔（"经度,纬度"格式）
 * @param {string} params.policy - 驾车策略
 * @param {string} params.plate_number - 车牌号
 */
async function drive_path(params) {
  const key = ensureConfig();

  const url = 'https://apis.map.qq.com/ws/direction/v1/driving/';
  const queryOpts = {
    key: key,
    from: flip_coord(params.origin),
    to: flip_coord(params.destination),
    output: 'json',
  };

  if (params.policy) {
    queryOpts.policy = params.policy;
  }
  if (params.plate_number) {
    queryOpts.plate_number = params.plate_number;
  }
  if (params.waypoints) {
    queryOpts.waypoints = params.waypoints
      .split(';')
      .map((wp) => flip_coord(wp))
      .join(';');
  }

  console.log('[route:driving] 发起驾车路线请求...');
  const data = await http_request(url, queryOpts);

  if (!data) {
    console.error('[route:driving] 请求未返回数据');
    return null;
  }

  if (data.status === 0) {
    console.log('[route:driving] 路线规划完成\n');
    const route = data.result.routes[0];
    return {
      status: '1',
      route: {
        paths: [
          {
            distance: route.distance,
            duration: route.duration,
            toll: route.toll || 0,
            traffic_light_count: route.traffic_light_count || 0,
            restriction: route.restriction || null,
            tags: route.tags || [],
            steps: route.steps || [],
          },
        ],
      },
      _raw: data,
    };
  } else {
    console.error('[route:driving] 规划失败:', data.message);
    return null;
  }
}

/**
 * 骑行路径规划（自行车）
 * @param {Object} params - 规划参数
 * @param {string} params.origin - 起点坐标 "经度,纬度"
 * @param {string} params.destination - 终点坐标 "经度,纬度"
 */
async function cycle_path(params) {
  const key = ensureConfig();

  const url = 'https://apis.map.qq.com/ws/direction/v1/bicycling/';
  const queryOpts = {
    key: key,
    from: flip_coord(params.origin),
    to: flip_coord(params.destination),
    output: 'json',
  };

  console.log('[route:bicycling] 发起骑行路线请求...');
  const data = await http_request(url, queryOpts);

  if (!data) {
    console.error('[route:bicycling] 请求未返回数据');
    return null;
  }

  if (data.status === 0) {
    console.log('[route:bicycling] 路线规划完成\n');
    const route = data.result.routes[0];
    return {
      status: '1',
      route: {
        paths: [
          {
            distance: route.distance,
            duration: route.duration,
            direction: route.direction || '',
            steps: route.steps || [],
          },
        ],
      },
      _raw: data,
    };
  } else {
    console.error('[route:bicycling] 规划失败:', data.message);
    return null;
  }
}

/**
 * 电动车路径规划
 * @param {Object} params - 规划参数
 * @param {string} params.origin - 起点坐标 "经度,纬度"
 * @param {string} params.destination - 终点坐标 "经度,纬度"
 */
async function ecycle_path(params) {
  const key = ensureConfig();

  const url = 'https://apis.map.qq.com/ws/direction/v1/ebicycling/';
  const queryOpts = {
    key: key,
    from: flip_coord(params.origin),
    to: flip_coord(params.destination),
    output: 'json',
  };

  console.log('[route:ebicycling] 发起电动车路线请求...');
  const data = await http_request(url, queryOpts);

  if (!data) {
    console.error('[route:ebicycling] 请求未返回数据');
    return null;
  }

  if (data.status === 0) {
    console.log('[route:ebicycling] 路线规划完成\n');
    const route = data.result.routes[0];
    return {
      status: '1',
      route: {
        paths: [
          {
            distance: route.distance,
            duration: route.duration,
            direction: route.direction || '',
            steps: route.steps || [],
          },
        ],
      },
      _raw: data,
    };
  } else {
    console.error('[route:ebicycling] 规划失败:', data.message);
    return null;
  }
}

/**
 * 公交路径规划
 * @param {Object} params - 规划参数
 * @param {string} params.origin - 起点坐标 "经度,纬度"
 * @param {string} params.destination - 终点坐标 "经度,纬度"
 * @param {string} params.departure_time - 出发时间
 * @param {string} params.policy - 公交策略
 */
async function bus_path(params) {
  const key = ensureConfig();

  const url = 'https://apis.map.qq.com/ws/direction/v1/transit/';
  const queryOpts = {
    key: key,
    from: flip_coord(params.origin),
    to: flip_coord(params.destination),
    output: 'json',
  };

  if (params.policy) {
    queryOpts.policy = params.policy;
  }
  if (params.departure_time) {
    queryOpts.departure_time = params.departure_time;
  }

  console.log('[route:transit] 发起公交路线请求...');
  const data = await http_request(url, queryOpts);

  if (!data) {
    console.error('[route:transit] 请求未返回数据');
    return null;
  }

  if (data.status === 0) {
    console.log('[route:transit] 路线规划完成\n');
    const routes = data.result.routes || [];
    return {
      status: '1',
      route: {
        transits: routes.map((route) => ({
          duration: route.duration,
          distance: route.distance || 0,
          bounds: route.bounds || '',
          steps: route.steps || [],
        })),
      },
      _raw: data,
    };
  } else {
    console.error('[route:transit] 规划失败:', data.message);
    return null;
  }
}

/**
 * 旅游规划助手
 * @param {Object} params - 规划参数
 * @param {string} params.city - 城市名称
 * @param {Array<string>} params.interests - 兴趣点关键词数组
 * @param {string} params.travelMode - 路线类型
 */
async function trip_advisor(params) {
  const { city, interests = [], travelMode = 'walking' } = params;

  console.log(`\n[travel] 开始规划 ${city} 行程...\n`);

  const renderItems = [];
  const placeList = [];

  // 搜索各类兴趣点
  for (const interest of interests) {
    console.log(`[travel] 搜索 ${interest}...`);
    const result = await query_place({
      keywords: interest,
      city: city,
      page: 1,
      offset: 5,
    });

    if (result && result.pois && result.pois.length > 0) {
      placeList.push(...result.pois);

      result.pois.forEach((poi) => {
        const [lng, lat] = poi.location.split(',').map(Number);
        renderItems.push({
          type: 'poi',
          lnglat: [lng, lat],
          sort: poi.type || interest,
          text: poi.name,
          remark: poi.address || `${interest}推荐`,
        });
      });
    }
  }

  // 如果有多个POI，规划路线
  if (placeList.length >= 2) {
    console.log(`\n[travel] 规划游览路线 (${travelMode})...\n`);

    for (let i = 0; i < placeList.length - 1; i++) {
      const start = placeList[i];
      const end = placeList[i + 1];

      const [startLng, startLat] = start.location.split(',').map(Number);
      const [endLng, endLat] = end.location.split(',').map(Number);

      const pathItem = {
        type: 'route',
        routeType: travelMode,
        start: [startLng, startLat],
        end: [endLng, endLat],
        remark: `从 ${start.name} 到 ${end.name}`,
      };

      if (travelMode === 'transfer') {
        pathItem.city = city;
      }

      renderItems.push(pathItem);
    }
  }

  console.log('\n[travel] 行程规划完成\n');
  console.log('推荐地点:');
  placeList.forEach((poi, index) => {
    console.log(`${index + 1}. ${poi.name}`);
    console.log(`   地址: ${poi.address}`);
    console.log(`   类型: ${poi.type}\n`);
  });

  return {
    pois: placeList,
    mapTaskData: renderItems,
  };
}

// 导出函数供其他脚本使用
module.exports = {
  getConfig,
  setConfig,
  ensureConfig,
  http_request,
  flip_coord,
  query_place,
  walk_path,
  drive_path,
  cycle_path,
  ecycle_path,
  bus_path,
  trip_advisor,
};

// 如果直接运行此文件，执行示例搜索
if (require.main === module) {
  (async () => {
    try {
      const result = await query_place({
        keywords: '肯德基',
        city: '北京',
        page: 1,
        offset: 10,
      });

      if (result && result.pois) {
        console.log('搜索结果:');
        result.pois.forEach((poi, index) => {
          console.log(`${index + 1}. ${poi.name}`);
          console.log(`   地址: ${poi.address}`);
          console.log(`   类型: ${poi.type}`);
          console.log(`   坐标: ${poi.location}\n`);
        });
      }
    } catch (error) {
      console.error('执行失败:', error.message);
      process.exit(1);
    }
  })();
}
