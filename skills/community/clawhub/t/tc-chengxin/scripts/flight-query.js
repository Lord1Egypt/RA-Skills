#!/usr/bin/env node

/**
 * 同程程心大模型 - 机票专用查询 API
 * 
 * 用法：
 *   node flight-query.js --departure "北京" --destination "上海"
 *   node flight-query.js --departure "北京" --low-price
 *   node flight-query.js --departure "上海" --destination "北京" --low-price
 *   node flight-query.js --flight-number "CA1234"
 *   node flight-query.js --departure "北京" --destination "上海" --extra "明天"
 *   node flight-query.js --departure "北京" --destination "上海" --extra "最早 直飞"
 *   node flight-query.js --departure "上海" --destination "北京" --low-price --extra "明天 最便宜"
 * 
 * 参数说明：
 *   --departure <城市>        出发地城市
 *   --destination <城市>      目的地城市
 *   --flight-number <航班号>  航班号
 *   --extra <补充信息>        额外信息（日期、时间偏好、价格偏好、舱位/航司偏好等）
 *   --low-price               查询特价/低价（可仅出发地，也可出发地+目的地；可与 --extra 同时使用）
 *   --channel <渠道>          通信渠道（webchat/wechat 等）
 *   --surface <界面>          交互界面（mobile/desktop/table/card）
 * 
 * 合法组合：
 *   1. 出发地 + 目的地
 *   2. 航班号
 *   3. 出发地 + low_price（特价/低价；可再加目的地指定航线，也可叠加 --extra）
 * 
 * 配置（优先级：环境变量 > config.json）：
 *   - CHENGXIN_API_KEY（环境变量）
 *   - 或创建 config.json 文件（见 config.example.json）
 */

const { create_query_runner } = require('./lib/base-query');
const { NO_MATCH_DETAIL, MORE_CHOICES_PROMPT, ROUND_TRIP_PROMPTS } = require('./lib/query-response');
const { is_transfer_trip, is_round_trip } = require('./lib/data-utils');
const {
  format_flight_card,
  format_flight_table,
  format_flight_table_special,
  format_transfer_trip,
  format_supplement_traffic
} = require('./lib/formatters');

// 机票 API 路径
const FLIGHT_API_PATH = '/flightResource';

/**
 * 验证参数组合
 * @param {object} params - 参数对象
 * @returns {object} - { valid: boolean, error: string }
 */
function validate_params(params) {
  const has_departure_dest = params.departure && params.destination;
  const has_flight_number = params.flight_number;
  const has_low_price = params.departure && params.low_price;
  
  if (has_departure_dest || has_flight_number || has_low_price) {
    return { valid: true };
  }
  
  if (params.departure && !params.destination) {
    return { 
      valid: false, 
      error: `⚠️ 参数不完整，请提供以下组合之一：
  1. 出发地 + 目的地（--departure "北京" --destination "上海"）
  2. 航班号（--flight-number "CA1234"）
  3. 特价/低价：仅出发地（--departure "北京" --low-price）或 出发地+目的地（再加 --low-price）`
    };
  }
  
  return { valid: false, error: '请提供查询参数' };
}

/**
 * 格式化机票结果
 * @param {object} flight_data - 机票数据
 * @param {boolean} use_table - 是否使用表格格式
 * @param {boolean} use_plain_link - 是否使用纯文本链接（转发给底层格式化函数）
 * @returns {string} - 格式化输出
 */
function format_flight_result(flight_data, use_table = false, use_plain_link = false) {
  if (!flight_data || !flight_data.flightList) {
    return '未找到相关机票信息';
  }
  
  const flights = flight_data.flightList;
  const is_special_price = flights.length > 0 && (flights[0].flightNo === null || flights[0].flightNo === undefined);
  
  let output = '✈️ 机票查询结果：\n\n';

  if (is_special_price && use_table) {
    output += format_flight_table_special(flights, use_plain_link);
  } else if (use_table) {
    const direct_flights = flights.filter((f) => !is_transfer_trip(f));
    const transfer_flights = flights.filter(is_transfer_trip);
    if (direct_flights.length > 0) {
      output += format_flight_table(direct_flights, use_plain_link);
    }
    transfer_flights.forEach((flight) => {
      output += format_transfer_trip(flight, use_plain_link);
    });
  } else {
    flights.forEach((flight) => {
      if (is_transfer_trip(flight)) {
        output += format_transfer_trip(flight, use_plain_link);
      } else {
        output += format_flight_card(flight, use_plain_link);
      }
    });
  }
  
  // 补偿交通（前往/离开机场的火车/汽车推荐）
  const supplement_output = format_supplement_traffic(flight_data, use_plain_link);
  if (supplement_output) {
    output += supplement_output;
  }
  
  output += MORE_CHOICES_PROMPT;
  output += '\n';
  return output;
}

/**
 * 处理查询结果
 */
function handle_result(response_data, { print_success_once, format_options, print_no_match, request_params }) {
  const { use_table, use_plain_link } = format_options;
  const round_trip = is_round_trip(request_params?.extra);
  const flight_data_list = response_data?.flightDataList;

  if (Array.isArray(flight_data_list) && flight_data_list.length > 0) {
    let has_output = false;

    flight_data_list.forEach((item, index) => {
      if (item.flightList && item.flightList.length > 0) {
        print_success_once();
        if (item.desc) {
          console.log(`📌 ${item.desc}\n`);
        } else if (flight_data_list.length > 1) {
          console.log(`📌 列表 ${index + 1}\n`);
        }
        console.log(format_flight_result(item, use_table, use_plain_link));
        has_output = true;
      }
    });
    if (!has_output) {
      print_no_match();
    } else {
      if (round_trip) {
        console.log(ROUND_TRIP_PROMPTS.FLIGHT);
      }
    }
  } else {
    print_no_match();
  }
}

// 创建查询运行器
const runner = create_query_runner({
  api_path: FLIGHT_API_PATH,
  param_defs: {
    departure: '',
    destination: '',
    flight_number: '',
    extra: '',
    low_price: false,
    channel: '',
    surface: ''
  },
  param_descriptions: {
    low_price: '查询特价/低价机票',
    flight_number: '航班号（如 CA1234）'
  },
  validate: validate_params,
  handle_result: handle_result,
  no_match_detail: NO_MATCH_DETAIL.FLIGHT,
  usage_example: `  node flight-query.js --departure "北京" --destination "上海"
  node flight-query.js --flight-number "CA1234"
  node flight-query.js --departure "上海" --destination "北京" --low-price
  node flight-query.js --departure "北京" --low-price --extra "明天"`
});

// 导出函数供其他模块使用
module.exports = {
  validate_params,
  format_flight_result
};

// 运行主函数
if (require.main === module) {
  runner.run();
}
