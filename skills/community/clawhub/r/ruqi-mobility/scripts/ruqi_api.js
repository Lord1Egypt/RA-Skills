#!/usr/bin/env node
/**
 * 如祺出行 API 调用工具
 *
 * 用法:
 *   node scripts/ruqi_api.js <tool_name> --key1 value1 --key2 value2 ...
 *
 * 示例:
 *   node scripts/ruqi_api.js text_search --keyword "广州塔"
 *   node scripts/ruqi_api.js query_ride_order --orderId 1234567890
 */

import { httpRequest } from "./request.js";

/**
 * 参数类型映射表
 * 每个命令的参数类型定义
 */
const PARAM_TYPES_BY_COMMAND = {
  send_verification_code: {
    phone: "string",
  },
  login_with_verification_code: {
    phone: "string",
    msgCode: "string",
  },
  estimate_price: {
    startLat: "number",
    startLng: "number",
    endLat: "number",
    endLng: "number",
    startAddress: "string",
    endAddress: "string",
  },
  create_ride_order: {
    estimateId: "string",
    fromLat: "number",
    fromLng: "number",
    fromAddress: "string",
    toLat: "number",
    toLng: "number",
    toAddress: "string",
  },
  query_ride_order: {
    orderId: "string",
  },
  cancel_order: {
    orderId: "string",
  },
  get_driver_location: {
    orderId: "string",
  },
  reverse_geocode: {
    lat: "number",
    lng: "number",
  },
  driving_route_planning: {
    startLat: "number",
    startLng: "number",
    endLat: "number",
    endLng: "number",
  },
  nearby_search: {
    keyword: "string",
  },
  get_recommended_boarding_point: {
    latitude: "number",
    longitude: "number",
  },
};

/**
 * 解析命令行参数
 * 支持 --key value 格式，根据命令自动转换类型
 */
function parseArguments() {
  const args = process.argv.slice(2);

  if (args.length < 1) {
    return null;
  }

  const command = args[0];
  const params = {};
  const types = PARAM_TYPES_BY_COMMAND[command] || {};

  for (let i = 1; i < args.length; i++) {
    const arg = args[i];

    if (arg.startsWith("--") && i + 1 < args.length) {
      const key = arg.substring(2);
      let value = args[i + 1];

      if (value && !value.startsWith("--")) {
        const type = types[key];
        if (type === "number") {
          value = Number(value);
        } else if (type === "integer") {
          value = parseInt(value, 10);
        } else if (type === "boolean") {
          value = value === "true";
        } else {
          value = String(value);
        }
        params[key] = value;
        i++;
      }
    }
  }

  const requiredParams = Object.keys(types);
  const missingParams = requiredParams.filter((key) => !(key in params));

  if (missingParams.length > 0) {
    throw new Error(
      `${missingParams.join("、")}字段是必传参数，请补齐字段重新发起请求试试`,
    );
  }

  return { command, params };
}

/**
 * 发送验证码
 */
async function sendVerificationCode(params) {
  return httpRequest("send_verification_code", {
    ...params,
    ticket: "ticket_123",
    randStr: "randstr_123",
    sceneType: 1
   });
}

/**
 * 验证码登录
 */
async function loginWithVerificationCode(params) {
  const res = await httpRequest(
    "login_with_verification_code",
    {
      ...params,
      mac: "mac_123",
      imei: "imei_123",
      imsi: "imsi_123",
      longitude: 113.938383,
      latitude: 22.545545
    },
    true,
  );

  // 从 header 中提取 token
  const token =
    res.headers && (res.headers["Set-Cookie"] || res.headers["set-cookie"]);

  return {
    ...res.data,
    token: token,
  };
}

/**
 * 价格预估
 */
async function estimatePrice(params) {
  return httpRequest("estimate_price", params);
}

/**
 * 创建订单
 */
async function createRideOrder(params) {
  return httpRequest("create_ride_order", {
    ...params,
    transportCarList: [
      {
        transportChannel: 1,
        supplierId: 100,
        carModelId: 1,
      },
    ],
    uncheckedTransportCarList: [],
  });
}

/**
 * 查询订单
 */
async function queryRideOrder(params) {
  return httpRequest("query_ride_order", params);
}

/**
 * 查询订单列表
 */
async function queryOrderList(params) {
  return httpRequest("query_order_list", {
    pageIndex: 1,
    pageSize: 10,
    type: "1",
  });
}

/**
 * 取消订单
 */
async function cancelOrder(params) {
  return httpRequest("cancel_order", params);
}

/**
 * 获取司机位置
 */
async function getDriverLocation(params) {
  return httpRequest("get_driver_location", params);
}

/**
 * 逆地理编码
 */
async function reverseGeocode(params) {
  return httpRequest("reverse_geocode", {
    ...params,
    getPoi: 1,
  });
}

/**
 * 驾车路径规划
 */
async function drivingRoutePlanning(params) {
  return httpRequest("driving_route_planning", {
    ...params,
    policy: 3,
    preferencePolicy: 1,
  });
}

/**
 * 文本搜索
 */
async function textSearch(params) {
  return httpRequest("text_search", {
    ...params,
    region: "广州",
    cityCode: "440100",
    latitude: 23.118531,
    longitude: 113.332164,
  });
}

/**
 * 周边检索
 */
async function nearbySearch(params) {
  return httpRequest("nearby_search", {
    ...params,
    latitude: 23.118531,
    longitude: 113.332164,
  });
}

/**
 * 获取推荐上车点
 */
async function getRecommendedBoardingPoint(params) {
  return httpRequest("get_recommended_boarding_point", params);
}

let ruqiApi = {
  send_verification_code: sendVerificationCode,
  login_with_verification_code: loginWithVerificationCode,
  estimate_price: estimatePrice,
  create_ride_order: createRideOrder,
  query_ride_order: queryRideOrder,
  query_order_list: queryOrderList,
  cancel_order: cancelOrder,
  get_driver_location: getDriverLocation,
  reverse_geocode: reverseGeocode,
  driving_route_planning: drivingRoutePlanning,
  text_search: textSearch,
  nearby_search: nearbySearch,
  get_recommended_boarding_point: getRecommendedBoardingPoint,
};

/**
 * 主函数
 */
async function main() {
  try {
    const parsed = parseArguments();
    if (!parsed) {
      process.exit(0);
    }

    const { command, params } = parsed;
    if (!ruqiApi[command]) {
      console.error(`未知命令: ${command}`);
      process.exit(1);
    } else {
      let result = await ruqiApi[command](params);
      console.log(JSON.stringify(result, null, 2));
      process.exit(0);
    }
  } catch (error) {
    console.error(`错误: ${error.message}`);
    process.exit(1);
  }
}

// 导出函数供其他模块使用
export default ruqiApi;

// 执行主函数（仅在直接运行时执行）
if (process.argv[1] && process.argv[1].includes("ruqi_api.js")) {
  main();
}
