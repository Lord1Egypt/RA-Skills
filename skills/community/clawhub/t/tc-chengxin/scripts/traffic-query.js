#!/usr/bin/env node

/**
 * 同程程心大模型 - 交通资源智能查询 API
 * 
 * 用法：
 *   node traffic-query.js --departure "北京" --destination "上海"
 *   node traffic-query.js --departure "北京" --destination "上海" --extra "明天"
 *   node traffic-query.js --departure "苏州" --destination "南京" --extra "自驾"
 *   node traffic-query.js --departure "北京" --destination "上海" --extra "最早 最便宜"
 * 
 * 参数说明：
 *   --departure <城市>        出发地城市
 *   --destination <城市>      目的地城市
 *   --extra <补充信息>        额外信息（日期、时间偏好、价格偏好、交通方式偏好等）
 *   --channel <渠道>          通信渠道（webchat/wechat 等）
 *   --surface <界面>          交互界面（mobile/desktop/table/card）
 * 
 * 说明：
 *   本接口用于用户未明确指定交通方式时的智能推荐
 *   会同时返回机票、火车票、汽车票等多种交通方式
 *   调用优先级低于专用查询接口（train-query.js, flight-query.js, bus-query.js）
 * 
 * 配置（优先级：环境变量 > config.json）：
 *   - CHENGXIN_API_KEY（环境变量）
 *   - 或创建 config.json 文件（见 config.example.json）
 */

const { create_query_runner } = require('./lib/base-query');
const { NO_MATCH_DETAIL, MORE_CHOICES_PROMPT, ROUND_TRIP_PROMPTS } = require('./lib/query-response');
const { is_transfer_trip, is_round_trip } = require('./lib/data-utils');
const {
  format_train_table,
  format_train_card,
  format_flight_table,
  format_flight_card,
  format_transfer_trip,
  format_bus_table,
  format_bus_card,
  format_supplement_traffic,
  format_transit_route
} = require('./lib/formatters');

// 交通 API 路径
const TRAFFIC_API_PATH = '/trafficResource';

/**
 * 验证参数组合
 * @param {object} params - 参数对象
 * @returns {object} - { valid: boolean, error: string }
 */
function validate_params(params) {
  if (params.departure && params.destination) {
    return { valid: true };
  }
  
  return { 
    valid: false, 
    error: `⚠️ 参数不完整，请提供出发地和目的地。
  示例：--departure "北京" --destination "上海"`
  };
}

/**
 * 格式化火车结果
 * @param {object} train_data - 火车数据
 * @param {boolean} use_table - 是否使用表格格式
 * @param {boolean} use_plain_link - 是否使用纯文本链接（转发给底层格式化函数）
 */
function format_train_result(train_data, use_table = false, use_plain_link = false) {
  if (!train_data || !train_data.trainList) {
    return '';
  }
  
  const trains = train_data.trainList;
  const direct_trains = trains.filter((t) => !is_transfer_trip(t));
  const transfer_trains = trains.filter(is_transfer_trip);

  let output = '\n🚄 **火车票**\n\n';

  if (use_table) {
    if (direct_trains.length > 0) {
      output += format_train_table(direct_trains, use_plain_link);
    }
    transfer_trains.forEach((train) => {
      output += format_transfer_trip(train, use_plain_link);
    });
  } else {
    direct_trains.forEach((train) => {
      output += format_train_card(train, use_plain_link);
    });
    transfer_trains.forEach((train) => {
      output += format_transfer_trip(train, use_plain_link);
    });
  }

  return output;
}

/**
 * 格式化机票结果
 * @param {object} flight_data - 机票数据
 * @param {boolean} use_table - 是否使用表格格式
 * @param {boolean} use_plain_link - 是否使用纯文本链接（转发给底层格式化函数）
 */
function format_flight_result(flight_data, use_table = false, use_plain_link = false) {
  if (!flight_data || !flight_data.flightList) {
    return '';
  }
  
  const flights = flight_data.flightList;
  const direct_flights = flights.filter((f) => !is_transfer_trip(f));
  const transfer_flights = flights.filter(is_transfer_trip);
  let output = '\n✈️ **机票**\n\n';

  if (use_table) {
    if (direct_flights.length > 0) {
      output += format_flight_table(direct_flights, use_plain_link);
    }
    transfer_flights.forEach((flight) => {
      output += format_transfer_trip(flight, use_plain_link);
    });
  } else {
    direct_flights.forEach((flight) => {
      output += format_flight_card(flight, use_plain_link);
    });
    transfer_flights.forEach((flight) => {
      output += format_transfer_trip(flight, use_plain_link);
    });
  }
  
  // 补偿交通（前往/离开机场的火车/汽车推荐）
  const supplement_output = format_supplement_traffic(flight_data, use_plain_link);
  if (supplement_output) {
    output += supplement_output;
  }
  
  return output;
}

/**
 * 格式化汽车票结果
 * @param {object} bus_data - 汽车票数据
 * @param {boolean} use_table - 是否使用表格格式
 * @param {boolean} use_plain_link - 是否使用纯文本链接（转发给底层格式化函数）
 */
function format_bus_result(bus_data, use_table = false, use_plain_link = false) {
  if (!bus_data || !bus_data.busList) {
    return '';
  }
  
  const buses = bus_data.busList;
  let output = '\n🚌 **汽车票**\n\n';
  
  if (use_table) {
    output += format_bus_table(buses, use_plain_link);
  } else {
    buses.forEach((bus) => {
      output += format_bus_card(bus, use_plain_link);
    });
  }
  
  return output;
}


/**
 * 交通资源处理器配置（配置驱动，避免火车/机票/汽车三块重复 if）
 * 保持输出顺序：火车 → 机票 → 汽车
 */
const RESOURCE_HANDLERS = [
  { dataKey: 'trainDataList', listKey: 'trainList', formatter: format_train_result },
  { dataKey: 'flightDataList', listKey: 'flightList', formatter: format_flight_result },
  { dataKey: 'busDataList', listKey: 'busList', formatter: format_bus_result },
];

/**
 * 处理查询结果
 */
function handle_result(response_data, { print_success_once, format_options, print_no_match, request_params }) {
  const { use_table, use_plain_link } = format_options;
  const round_trip = is_round_trip(request_params?.extra);

  let has_output = false;

  RESOURCE_HANDLERS.forEach(({ dataKey, listKey, formatter }) => {
    const data_list = response_data?.[dataKey];
    const has_any = Array.isArray(data_list) && data_list.some(item =>
      Array.isArray(item[listKey]) && item[listKey].length > 0
    );
    if (has_any) {
      print_success_once();
      data_list.forEach((item) => {
        if (item.desc) {
          console.log(`📌 ${item.desc}\n`);
        }
        if (item[listKey] && item[listKey].length > 0) {
          console.log(formatter(item, use_table, use_plain_link));
          has_output = true;
        }
      });
    }
  });

  // 公交地铁（transitRoute）：在火车/机票/汽车之后展示
  const transitRoute = response_data?.transitRoute;
  if (transitRoute && Array.isArray(transitRoute.routes) && transitRoute.routes.length > 0) {
    print_success_once();
    const transit_output = format_transit_route(transitRoute, use_plain_link);
    if (transit_output) {
      console.log(transit_output);
      has_output = true;
    }
  }

  if (!has_output) {
    print_no_match();
  } else {
    if (round_trip) {
      console.log(ROUND_TRIP_PROMPTS.TRAFFIC);
    }
    console.log(MORE_CHOICES_PROMPT);
  }
}

// 创建查询运行器
const runner = create_query_runner({
  api_path: TRAFFIC_API_PATH,
  param_defs: {
    departure: '',
    destination: '',
    extra: '',
    channel: '',
    surface: ''
  },
  validate: validate_params,
  handle_result: handle_result,
  no_match_detail: NO_MATCH_DETAIL.TRAFFIC,
  usage_example: `  node traffic-query.js --departure "北京" --destination "上海"
  node traffic-query.js --departure "北京" --destination "上海" --extra "明天"`
});

// 导出函数供其他模块使用
module.exports = {
  validate_params
};

// 运行主函数
if (require.main === module) {
  runner.run();
}
