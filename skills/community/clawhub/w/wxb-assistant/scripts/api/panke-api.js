#!/usr/bin/env node

/**
 * 旺小宝数据助手 - 盘客 API 客户端
 *
 * 功能：
 * - 封装盘客列表、详情、收集表、SOP、评论等 API 调用
 * - 自动处理认证头
 * - 统一的错误处理
 */

const https = require('https')

class PankeApi {
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

  // ========== 盘客列表 ==========

  /**
   * 盘客分页列表
   * @param {Object} params - 查询参数
   */
  async getPankePage(params = {}) {
    return this.request({
      method: 'POST',
      path: '/panke/app/panke/page',
      params: {
        page: params.page || 1,
        size: params.size || 20,
        ...params
      }
    })
  }

  /**
   * 盘客列表进度率
   * @param {Object} params - 查询参数
   */
  async getPankePageScore(params = {}) {
    return this.request({
      method: 'POST',
      path: '/panke/app/panke/page/score',
      params
    })
  }

  /**
   * 盘客筛选条件
   * @param {Object} params - 查询参数
   */
  async getSearchCondition(params = {}) {
    return this.request({
      method: 'GET',
      path: '/panke/common/searchCondition',
      params
    })
  }

  /**
   * 查询盘客权限
   * @param {Object} params - 查询参数
   */
  async getPermission(params = {}) {
    return this.request({
      method: 'GET',
      path: '/panke/permission',
      params
    })
  }

  // ========== 盘客详情 ==========

  /**
   * 盘客详情
   * @param {Object} params - 查询参数
   */
  async getPankeDetail(params = {}) {
    return this.request({
      method: 'GET',
      path: '/panke/app/panke/detail',
      params
    })
  }

  /**
   * 盘客详情V2
   * @param {Object} params - 查询参数
   */
  async getPankeDetailV2(params = {}) {
    return this.request({
      method: 'GET',
      path: '/panke/app/panke/v2/detail',
      params
    })
  }

  /**
   * 盘客详情（通过customerId，客户中心版本）
   * @param {Object} params - 查询参数
   */
  async getWangPankeDetailV2(params = {}) {
    return this.request({
      method: 'GET',
      path: '/panke/app/panke/wang/v2/detail',
      params
    })
  }

  /**
   * 盘客详情画像
   * @param {Object} params - 查询参数
   */
  async getCompleteTable(params = {}) {
    return this.request({
      method: 'GET',
      path: '/panke/app/panke/complete-table',
      params
    })
  }

  /**
   * 盘客详情画像V2
   * @param {Object} params - 查询参数
   */
  async getCompleteTableV2(params = {}) {
    return this.request({
      method: 'GET',
      path: '/panke/app/panke/v2/complete-table',
      params
    })
  }

  /**
   * 盘客详情买点
   * @param {Object} params - 查询参数
   */
  async getSellingPointReach(params = {}) {
    return this.request({
      method: 'GET',
      path: '/panke/app/panke/customer/selling-point-reach',
      params
    })
  }

  /**
   * 盘客详情风控
   * @param {Object} params - 查询参数
   */
  async getRiskList(params = {}) {
    return this.request({
      method: 'GET',
      path: '/panke/risk/list',
      params
    })
  }

  /**
   * 盘客详情关注点
   * @param {Object} params - 查询参数
   */
  async getFocusList(params = {}) {
    return this.request({
      method: 'GET',
      path: '/panke/focus/list',
      params
    })
  }

  /**
   * 盘客客户来访信息
   * @param {Object} params - 查询参数
   */
  async getTableCusVisitInfo(params = {}) {
    return this.request({
      method: 'POST',
      path: '/panke/app/panke/tableCusVisitInfo',
      params
    })
  }

  // ========== 盘客收集表 ==========

  /**
   * 获取盘客收集表
   * @param {Object} params - 查询参数
   */
  async getTable(params = {}) {
    return this.request({
      method: 'GET',
      path: '/panke/app/panke/table',
      params
    })
  }

  /**
   * 提交盘客收集表
   * @param {Object} params - 表单数据
   */
  async submitTable(params = {}) {
    return this.request({
      method: 'POST',
      path: '/panke/app/panke/table',
      params
    })
  }

  /**
   * 编辑盘客收集表单字段
   * @param {Object} params - 字段数据
   */
  async editTableField(params = {}) {
    return this.request({
      method: 'POST',
      path: '/panke/app/panke/table/field',
      params
    })
  }

  /**
   * 盘客收集表校验查询
   * @param {Object} params - 查询参数
   */
  async getCheckTable(params = {}) {
    return this.request({
      method: 'GET',
      path: '/panke/app/panke/check-table',
      params
    })
  }

  /**
   * 标记为特殊来访
   * @param {Object} params - 标记参数
   */
  async markSpecialVisits(params = {}) {
    return this.request({
      method: 'POST',
      path: '/panke/app/panke/mark-special-visits',
      params
    })
  }

  /**
   * AI辅助回想
   * @param {Object} params - 查询参数
   */
  async getAiAssistedRecall(params = {}) {
    return this.request({
      method: 'GET',
      path: '/panke/app/panke/ai-assisted-recall',
      params
    })
  }

  // ========== 盘客SOP ==========

  /**
   * 根据录音ID查询金句内容
   * @param {Object} params - 查询参数
   * @param {string} params.audioId - 录音ID
   */
  async getGoldenContentByAudioId(params) {
    return this.request({
      method: 'POST',
      path: '/panke/panke/new/sop/getGoldenContentByAudioId',
      params
    })
  }

  /**
   * 金句内容认可
   * @param {Object} params - 认可参数
   */
  async goldenContentAccept(params) {
    return this.request({
      method: 'POST',
      path: '/panke/panke/new/sop/goldenContentAccept',
      params
    })
  }

  /**
   * 创建金句分析任务
   * @param {Object} params - 任务参数
   */
  async createGoldenAnalysisTask(params) {
    return this.request({
      method: 'POST',
      path: '/panke/panke/sop/createGoldenAnalysisTask',
      params
    })
  }

  /**
   * 获取销售意向级别
   */
  async getSalesPitchIntent() {
    return this.request({
      method: 'GET',
      path: '/panke/panke/sop/v1/options/salesPitchIntent'
    })
  }

  /**
   * 更新销售意向级别
   * @param {Object} params - 更新参数
   */
  async updateSalesPitchIntent(params) {
    return this.request({
      method: 'POST',
      path: '/panke/panke/sop/v1/options/salesPitchIntent/update',
      params
    })
  }

  /**
   * SOP2阶段客户概览状态
   * @param {Object} params - 查询参数
   */
  async getSopTwoStageResultStatus(params = {}) {
    return this.request({
      method: 'GET',
      path: '/panke/panke/new/sop/two/stage/result/status',
      params
    })
  }

  /**
   * SOP2阶段客户概览
   * @param {Object} params - 查询参数
   */
  async getSopTwoStageSketch(params = {}) {
    return this.request({
      method: 'GET',
      path: '/panke/panke/new/sop/two/stage/sketch',
      params
    })
  }

  // ========== 盘客评论 ==========

  /**
   * 获取评论列表
   * @param {Object} params - 查询参数
   */
  async getCommentList(params = {}) {
    return this.request({
      method: 'GET',
      path: '/panke/comment/list',
      params
    })
  }

  /**
   * 新增评论
   * @param {Object} params - 评论参数
   */
  async addComment(params = {}) {
    return this.request({
      method: 'POST',
      path: '/panke/comment/add',
      params
    })
  }

  // ========== 其他 ==========

  /**
   * 通过customerId获取eventId
   * @param {Object} params - 查询参数
   */
  async getEventIdByCustomerId(params) {
    return this.request({
      method: 'GET',
      path: '/panke/app/panke/wang/event/detail',
      params
    })
  }

  /**
   * 根据来访ID获取盘客ID
   * @param {Object} params - 查询参数
   */
  async getPankeIdByVisitId(params) {
    return this.request({
      method: 'GET',
      path: '/panke/app/panke/get-pankeId-by-visitId',
      params
    })
  }

  /**
   * 删除关注点
   * @param {Object} params - 删除参数
   */
  async deleteFocus(params = {}) {
    return this.request({
      method: 'DELETE',
      path: '/panke/focus/delete-focus',
      params
    })
  }
}

module.exports = PankeApi
