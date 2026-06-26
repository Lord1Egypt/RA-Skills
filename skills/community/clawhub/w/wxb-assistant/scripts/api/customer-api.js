#!/usr/bin/env node

/**
 * 旺小宝数据助手 - 客户中心 API 客户端
 *
 * 功能：
 * - 封装客户列表、详情、画像、关注点、抗性点、轨迹等 API 调用
 * - 自动处理认证头
 * - 统一的错误处理
 */

const https = require('https')

class CustomerApi {
  constructor(baseURL, tokenGetter) {
    this.baseURL = baseURL
    this.getToken = tokenGetter
  }

  /**
   * 发送 HTTPS 请求
   */
  async request(options) {
    const token = await this.getToken()
    const { method = 'GET', path, params = {} } = options

    let urlPath = path
    let body = undefined

    if (method === 'GET') {
      const queryParams = new URLSearchParams(params).toString()
      if (queryParams) urlPath += `?${queryParams}`
    } else {
      body = JSON.stringify(params)
    }

    const requestOptions = {
      hostname: this.baseURL,
      path: urlPath,
      method: method,
      headers: {
        'Content-Type': 'application/json',
        'X-Auth-Token': token,
        'X-Platform-Client': 'iwangke'
      }
    }

    if (body) {
      requestOptions.headers['Content-Length'] = Buffer.byteLength(body)
    }

    return new Promise((resolve, reject) => {
      const req = https.request(requestOptions, (res) => {
        let data = ''

        res.on('data', (chunk) => {
          data += chunk
        })

        res.on('end', () => {
          try {
            const result = JSON.parse(data)
            if (result.code !== '0') {
              reject(new Error(`API 错误: ${result.msg || '未知错误'}`))
            } else {
              resolve(result.data || result)
            }
          } catch (e) {
            reject(new Error(`解析响应失败: ${e.message}`))
          }
        })
      })

      req.on('error', (err) => {
        reject(new Error(`请求失败: ${err.message}`))
      })

      if (body) {
        req.write(body)
      }

      req.end()
    })
  }

  // ========== 客户列表 ==========

  /**
   * 获取客户列表
   * @param {Object} params - 查询参数
   */
  async getCustomerList(params = {}) {
    return this.request({
      method: 'POST',
      path: '/customer/customer/list',
      params: {
        page: params.page || 1,
        size: params.size || 20,
        ...params
      }
    })
  }

  /**
   * 获取单个客户
   * @param {Object} params - 查询参数
   */
  async getCustomerOne(params) {
    return this.request({
      method: 'GET',
      path: '/customer/customer/list/one',
      params
    })
  }

  /**
   * 搜索客户
   * @param {Object} params - 搜索参数
   */
  async searchCustomer(params) {
    return this.request({
      method: 'GET',
      path: '/customer/customer/search',
      params
    })
  }

  /**
   * 获取客户详情
   * @param {Object} params - 查询参数
   * @param {string} params.wangId - 客户ID
   */
  async getCustomerDetail(params) {
    return this.request({
      method: 'GET',
      path: `/customer/customer/detail/${params.wangId}`,
      params
    })
  }

  // ========== 客户画像 ==========

  /**
   * 获取客户轨迹
   * @param {Object} params - 查询参数
   */
  async getCustomerTrajectory(params) {
    return this.request({
      method: 'GET',
      path: '/customer/customer/trajectory',
      params
    })
  }

  /**
   * 获取关注点
   * @param {Object} params - 查询参数
   */
  async getFocusWangList(params) {
    return this.request({
      method: 'GET',
      path: '/customer/customer/focus/wang/list',
      params
    })
  }

  /**
   * 获取抗性点
   * @param {Object} params - 查询参数
   */
  async getPointWangList(params) {
    return this.request({
      method: 'GET',
      path: '/customer/customer/point/wang/list',
      params
    })
  }

  /**
   * 查看是否可以展示画像明细
   * @param {Object} params - 查询参数
   */
  async predictCanView(params = {}) {
    return this.request({
      method: 'GET',
      path: '/customer/predict/can-view',
      params
    })
  }

  /**
   * 重新预测
   * @param {Object} params - 预测参数
   */
  async rePredict(params) {
    return this.request({
      method: 'POST',
      path: `/customer/predict/re-predict/${params.wangId}`,
      params
    })
  }

  /**
   * 客户预测检测结果
   * @param {Object} params - 检测参数
   */
  async predictCanPredict(params) {
    return this.request({
      method: 'POST',
      path: `/customer/predict/can-predict/${params.wangId}`,
      params
    })
  }

  /**
   * 获取画像隐私协议
   */
  async getTagAgreement() {
    return this.request({
      method: 'GET',
      path: '/customer/estate/cfg/tag-agreement'
    })
  }

  /**
   * 新增用户流水日志
   * @param {Object} params - 日志参数
   */
  async userOperationLog(params) {
    return this.request({
      method: 'POST',
      path: '/customer/user-operation-log',
      params
    })
  }

  // ========== 客户录音 ==========

  /**
   * 获取客户录音列表
   * @param {Object} params - 查询参数
   */
  async getCustomerAudios(params) {
    return this.request({
      method: 'GET',
      path: '/ai-voice/customer/audios',
      params
    })
  }
}

module.exports = CustomerApi
