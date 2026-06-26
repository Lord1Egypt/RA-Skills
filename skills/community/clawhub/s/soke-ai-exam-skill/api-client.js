import axios from 'axios';
import FormData from 'form-data';
import fs from 'fs';
import { config } from './config.js';

/**
 * API客户端类
 */
class ApiClient {
  constructor() {
    this.baseUrl = config.baseUrl;
  }

  /**
   * 获取access_token
   */
  async getAccessToken() {
    // 检查缓存的token是否有效
    if (config.accessToken && config.tokenExpireTime && Date.now() < config.tokenExpireTime) {
      return config.accessToken;
    }

    const url = `${this.baseUrl}/service/corp/gettoken`;
    const params = {
      app_key: config.appKey,
      app_secret: config.appSecret,
      corpid: config.corpId
    };

    try {
      const response = await axios.get(url, { params });
      if (response.data.code === '200') {
        config.accessToken = response.data.data;
        // token有效期2小时，提前5分钟刷新
        config.tokenExpireTime = Date.now() + (115 * 60 * 1000);
        return config.accessToken;
      }
      throw new Error(response.data.message || '获取access_token失败');
    } catch (error) {
      throw new Error(`获取access_token失败: ${error.message}`);
    }
  }

  /**
   * 通用请求方法
   */
  async request(method, endpoint, data = null, params = null) {
    const token = await this.getAccessToken();
    const url = `${this.baseUrl}${endpoint}`;

    const requestConfig = {
      method,
      url,
      params: { ...params, access_token: token },
      headers: {},
      maxContentLength: Infinity,
      maxBodyLength: Infinity,
      timeout: 300000 // 5分钟超时
    };

    if (data) {
      if (data instanceof FormData) {
        requestConfig.data = data;
        requestConfig.headers = { ...data.getHeaders() };
      } else {
        requestConfig.data = data;
        requestConfig.headers['Content-Type'] = 'application/json';
      }
    }

    try {
      const response = await axios(requestConfig);
      return response.data;
    } catch (error) {
      throw new Error(`API请求失败: ${error.message}`);
    }
  }
}

export default new ApiClient();
