// 引入 HTTP 请求库
const axios = require('axios');

// OpenClaw 技能标准入口函数
module.exports = async function run(params, context) {
  try {
    // 1. 从环境变量读取 API Key
    const apiKey = context.env.WAVESPEED_API_KEY;
    if (!apiKey) {
      return {
        error: "MISSING_API_KEY",
        message: "未配置 WAVESPEED_API_KEY 环境变量"
      };
    }

    // 2. 提取用户输入参数
    const { prompt, resolution = "1k" } = params;
    if (!prompt) {
      return {
        error: "MISSING_PROMPT",
        message: "缺少必填参数 prompt"
      };
    }

    // 3. 构造 Wavespeed API 请求（正确的 v2 接口）
const apiUrl = "https://api.wavespeed.ai/api/v2/wavespeed-ai/z-image/turbo";
const requestBody = {
  prompt: prompt,
  width: 1024,
  height: 1024,
  steps: 20
};

    // 4. 发送请求
    const response = await axios.post(apiUrl, requestBody, {
      headers: {
        "Authorization": `Bearer ${apiKey}`,
        "Content-Type": "application/json"
      }
    });

    // 5. 返回成功结果
    return {
      success: true,
      data: response.data
    };

  } catch (error) {
    // 6. 返回错误信息，方便调试
    return {
      error: "API_CALL_FAILED",
      message: error.message,
      details: error.response?.data || "无更多详情"
    };
  }
};
// 本地测试代码（仅用于调试，正式部署时可删除）
(async () => {
  const testParams = {
    prompt: "蓝色海洋",
    resolution: "1k"
  };

  const testContext = {
    env: {
      WAVESPEED_API_KEY: "3894f953f394c83e582e199fbc98c812f449e14334615219d08ed682c238f4cb"
    }
  };

  try {
    const result = await module.exports(testParams, testContext);
    console.log("\n✅ 测试结果:", JSON.stringify(result, null, 2));
  } catch (err) {
    console.error("\n❌ 测试失败:", err);
  }
})();