#!/usr/bin/env node

/**
 * LLM API 客户端
 * 
 * 统一调用接口，支持多个模型
 */

const https = require('https');

// API 配置
const API_CONFIG = {
  baseUrl: 'https://dashscope.aliyuncs.com/api/v1',
  apiKey: process.env.DASHSCOPE_API_KEY || ''
};

/**
 * 调用 LLM API
 * 
 * @param {string} prompt - 提示词
 * @param {string} model - 模型 ID
 * @param {string} thinking - 思考级别 (low/medium/high)
 * @returns {Promise<string>} AI 响应
 */
async function callLLM(prompt, model, thinking = 'medium') {
  return new Promise((resolve, reject) => {
    const postData = JSON.stringify({
      model,
      input: { messages: [{ role: 'user', content: prompt }] },
      parameters: {
        temperature: thinking === 'high' ? 0.9 : thinking === 'medium' ? 0.7 : 0.5,
        max_tokens: 8192
      }
    });
    
    const options = {
      hostname: 'dashscope.aliyuncs.com',
      port: 443,
      path: '/api/v1/services/aigc/text-generation/generation',
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${API_CONFIG.apiKey}`,
        'Content-Length': Buffer.byteLength(postData)
      }
    };
    
    const req = https.request(options, (res) => {
      let data = '';
      
      res.on('data', (chunk) => {
        data += chunk;
      });
      
      res.on('end', () => {
        try {
          const result = JSON.parse(data);
          if (result.output && result.output.text) {
            resolve(result.output.text);
          } else if (result.message) {
            reject(new Error(result.message));
          } else {
            reject(new Error('API 返回格式异常'));
          }
        } catch (error) {
          reject(new Error(`解析失败：${error.message}`));
        }
      });
    });
    
    req.on('error', (error) => {
      reject(new Error(`API 请求失败：${error.message}`));
    });
    
    req.write(postData);
    req.end();
  });
}

/**
 * 调用 LLM 并解析 JSON 响应
 */
async function callLLMJson(prompt, model, thinking = 'medium') {
  const response = await callLLM(prompt, model, thinking);
  
  try {
    // 提取 JSON
    const jsonMatch = response.match(/\{[\s\S]*\}/);
    if (!jsonMatch) {
      throw new Error('响应中未找到 JSON');
    }
    
    return JSON.parse(jsonMatch[0]);
  } catch (error) {
    throw new Error(`JSON 解析失败：${error.message}`);
  }
}

// 导出
module.exports = { callLLM, callLLMJson, API_CONFIG };
