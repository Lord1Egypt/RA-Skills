import axios from 'axios';

// ============================================================
// ZBJ MCP Bridge - CLI 工具调用桥接器
// ============================================================
// 用法: node bridge.js <toolName> <argsJson>
// 示例: node bridge.js get_demand_detail '{"demandId":12345}'
// ============================================================

// 基础域名
const BASE_URL = process.env.ZBJ_API_URL || 'https://zmcp.zbj.com';
const API_KEY = process.env.ZBJ_API_KEY;
const TIMEOUT = parseInt(process.env.ZBJ_API_TIMEOUT || '30000', 10);

// 工具名 + 参数
const toolName = process.argv[2];
const argsJson = process.argv[3] || '{}';

// ============================================================
// 完整工具映射（18个工具，分4个模块）
// ============================================================
const TOOL_MAP = {
  // ==================== 系统工具（1个） ====================
  health_check: {
    method: 'GET',
    path: '/zbjcheck',
    description: '检查后端服务健康状态',
  },

  // ==================== 类目服务（2个） ====================
  get_categories: {
    method: 'GET',
    path: '/api/category/list',
    description: '获取类目列表（支持层级筛选）',
  },
  search_category: {
    method: 'INTERNAL',
    path: 'search_category',
    description: '根据关键词搜索匹配类目（客户端处理）',
  },

  // ==================== 需求管理（8个） ====================
  publish_demand: {
    method: 'POST',
    path: '/api/demand/publishDemand',
    description: '发布或修改需求',
  },
  get_demand_detail: {
    method: 'GET',
    path: '/api/demand/detail',
    description: '查询需求详情（含投标情况）',
  },
  close_demand: {
    method: 'POST',
    path: '/api/demand/close',
    description: '关闭需求',
  },
  pause_demand: {
    method: 'GET',
    path: '/api/demand/pauseDemand',
    description: '暂停需求',
  },
  open_demand: {
    method: 'POST',
    path: '/api/demand/openDemand',
    description: '公开已暂停的需求',
  },
  eliminate_seller: {
    method: 'POST',
    path: '/api/demand/eliminateSeller',
    description: '淘汰服务商',
  },
  select_winner: {
    method: 'POST',
    path: '/api/demand/selectWinner',
    description: '选服务商中标',
  },
  search_demands: {
    method: 'POST',
    path: '/api/demand/search',
    description: '搜索需求（支持状态筛选）',
  },

  // ==================== 订单管理（5个） ====================
  get_order_detail: {
    method: 'GET',
    path: '/api/order/detail',
    description: '查询订单详情',
  },
  search_orders: {
    method: 'POST',
    path: '/api/order/search',
    description: '搜索订单',
  },
  eval_seller: {
    method: 'POST',
    path: '/api/order/evalSeller',
    description: '评价已完成订单的服务商',
  },
  close_order: {
    method: 'POST',
    path: '/api/order/close',
    description: '关闭订单',
  },
  get_trusteeship_pay_url: {
    method: 'POST',
    path: '/api/order/getTrusteeshipPayUrl',
    description: '获取托管支付地址',
  },

  // ==================== 搜索服务（2个） ====================
  search_services: {
    method: 'POST',
    path: '/api/service/search',
    description: '搜索服务商品',
  },
  search_shops: {
    method: 'POST',
    path: '/api/shop/search',
    description: '搜索店铺/服务商',
  },
};

// ============================================================
// 类目缓存（用于 search_category 内部处理）
// ============================================================
let categoryCache = null;

// ============================================================
// Axios 实例配置
// ============================================================
const axiosInstance = axios.create({
  baseURL: BASE_URL,
  timeout: TIMEOUT,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    ...(API_KEY && { 'X-API-Key': API_KEY }),
  },
});

// ============================================================
// 辅助函数：获取类目数据
// ============================================================
async function fetchCategories() {
  if (categoryCache) {
    return categoryCache;
  }

  try {
    const response = await axiosInstance.get('/api/category/list');
    if (response.data.code === 200 && response.data.data) {
      categoryCache = response.data.data;
      return categoryCache;
    }
    return [];
  } catch (error) {
    return [];
  }
}

// ============================================================
// 辅助函数：搜索类目（客户端处理）
// ============================================================
async function searchCategory(keyword, level) {
  const categories = await fetchCategories();

  // 搜索关键词（不区分大小写）
  const lowerKeyword = keyword.toLowerCase();
  let results = categories.filter((c) =>
    c.name.toLowerCase().includes(lowerKeyword)
  );

  // 按层级筛选
  if (level !== undefined) {
    results = results.filter((c) => c.level === level);
  }

  // 按相关性排序（精确匹配优先）
  results.sort((a, b) => {
    const aExact = a.name.toLowerCase() === lowerKeyword ? 0 : 1;
    const bExact = b.name.toLowerCase() === lowerKeyword ? 0 : 1;
    if (aExact !== bExact) return aExact - bExact;
    return a.level - b.level;
  });

  // 限制结果数量
  return results.slice(0, 20);
}

// ============================================================
// 主执行函数
// ============================================================
async function main() {
  // 检查工具名
  if (!toolName) {
    console.error(JSON.stringify({
      code: 400,
      message: 'Missing tool name. Usage: node bridge.js <toolName> <argsJson>',
      data: null,
      timestamp: Date.now(),
    }, null, 2));
    process.exit(1);
  }

  // 获取工具配置
  const toolConfig = TOOL_MAP[toolName];
  if (!toolConfig) {
    console.error(JSON.stringify({
      code: 404,
      message: `Unknown tool: ${toolName}`,
      data: null,
      timestamp: Date.now(),
    }, null, 2));
    process.exit(1);
  }

  // 解析参数
  let args = {};
  try {
    args = JSON.parse(argsJson);
  } catch (error) {
    console.error(JSON.stringify({
      code: 400,
      message: `Invalid JSON arguments: ${argsJson}`,
      data: null,
      timestamp: Date.now(),
    }, null, 2));
    process.exit(1);
  }

  try {
    let result;

    // 处理内部工具（search_category）
    if (toolConfig.method === 'INTERNAL') {
      if (toolName === 'search_category') {
        const { keyword, level } = args;
        if (!keyword) {
          throw new Error('keyword is required for search_category');
        }
        const results = await searchCategory(keyword, level);
        result = {
          code: 200,
          message: 'success',
          data: results,
          total: results.length,
          keyword,
        };
      } else {
        throw new Error(`Unknown internal tool: ${toolName}`);
      }
    }
    // 处理 GET 请求
    else if (toolConfig.method === 'GET') {
      const response = await axiosInstance.get(toolConfig.path, {
        params: args,
      });
      result = response.data;
    }
    // 处理 POST 请求
    else if (toolConfig.method === 'POST') {
      const response = await axiosInstance.post(toolConfig.path, args);
      result = response.data;
    }
    // 处理 PUT 请求
    else if (toolConfig.method === 'PUT') {
      const response = await axiosInstance.put(toolConfig.path, args);
      result = response.data;
    }
    // 处理 DELETE 请求
    else if (toolConfig.method === 'DELETE') {
      const response = await axiosInstance.delete(toolConfig.path, {
        data: args,
      });
      result = response.data;
    }
    else {
      throw new Error(`Unsupported method: ${toolConfig.method}`);
    }

    // 输出结果
    console.log(JSON.stringify(result, null, 2));
    process.exit(0);

  } catch (error) {
    // 错误处理
    const errorResponse = {
      code: error.response?.status || 500,
      message: error.response?.data?.message || error.message || 'Unknown error',
      data: null,
      timestamp: Date.now(),
    };

    if (error.response?.data) {
      errorResponse.data = error.response.data;
    }

    console.error(JSON.stringify(errorResponse, null, 2));
    process.exit(1);
  }
}

// 执行
main();
