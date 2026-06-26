#!/usr/bin/env node

/**
 * 旺小宝数据助手 - 其他功能 API 客户端
 *
 * 功能：
 * - 封装今日代办等相关 API 调用
 * - 自动处理认证头
 * - 统一的错误处理
 */

const https = require('https')

class OtherApi {
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

  // ========== 今日代办 ==========

  /**
   * 今日代办统计
   * @param {Object} params - 查询参数
   */
  async virtuallyTodayTodoCount(params = {}) {
    return this.request({
      method: 'GET',
      path: '/ai-voice/app/virtually/visit/virtually-today-todo:count',
      params
    })
  }

  /**
   * 今日代办列表
   * @param {Object} params - 查询参数
   */
  async virtuallyTodayTodoList(params = {}) {
    return this.request({
      method: 'GET',
      path: '/ai-voice/app/virtually/visit/virtually-today-todo:all',
      params
    })
  }

  /**
   * 今日代办详情
   * @param {Object} params - 查询参数
   * @param {string} params.id - 来访ID
   */
  async virtuallyTodayTodoById(params) {
    return this.request({
      method: 'GET',
      path: `/ai-voice/app/virtually/visit/virtually-today-todo/${params.id}`,
      params
    })
  }

  /**
   * 获取最后更新
   * @param {Object} params - 查询参数
   */
  async getVirtuallyVisitDetailRangeOf(params) {
    return this.request({
      method: 'GET',
      path: '/ai-voice/app/virtually/visit/virtually-visit-detail:range-of',
      params
    })
  }

  /**
   * 获取最后更新（全部）
   * @param {Object} params - 查询参数
   */
  async getVirtuallyVisitDetailRangeOfAll(params) {
    return this.request({
      method: 'GET',
      path: '/ai-voice/app/virtually/visit/virtually-visit-detail:range-of-all',
      params
    })
  }

  /**
   * 大音频列表
   * @param {Object} params - 查询参数
   */
  async getVirtuallyBigAudio(params) {
    return this.request({
      method: 'GET',
      path: '/ai-voice/app/virtually/visit/virtually-big-audio',
      params
    })
  }

  /**
   * 忽略指定接访单
   * @param {Object} params - 查询参数
   */
  async visitIgnoreAudio(params) {
    return this.request({
      method: 'GET',
      path: '/ai-voice/app/virtually/visit/ignore-audio',
      params
    })
  }

  /**
   * 虚拟单是否需要弹窗
   * @param {Object} params - 查询参数
   */
  async needPopUp(params) {
    return this.request({
      method: 'GET',
      path: '/ai-voice/app/virtually/visit/need-pop-up',
      params
    })
  }
}

module.exports = OtherApi
