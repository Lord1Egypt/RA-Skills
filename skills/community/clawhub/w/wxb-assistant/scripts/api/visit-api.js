#!/usr/bin/env node

/**
 * 旺小宝数据助手 - 工牌接访 API 客户端
 *
 * 功能：
 * - 封装工牌接访相关 API 调用
 * - 自动处理认证头
 * - 统一的错误处理
 */

const https = require('https')

class VisitApi {
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

  // ========== 工牌客户相关 ==========

  /**
   * 获取客户列表（V2版本）
   * @param {Object} params - 查询参数
   */
  async getCustomerPageV2(params = {}) {
    return this.request({
      method: 'POST',
      path: '/ai-voice/app/customer/pageV2',
      params: {
        page: params.page || 1,
        size: params.size || 20,
        teamId: params.teamId || '',
        startTime: params.startTime || '',
        endTime: params.endTime || '',
        ...params
      }
    })
  }

  /**
   * 获取客户详情（V2版本）
   * @param {string} customerId - 客户ID
   */
  async getCustomerDetailV2(customerId) {
    return this.request({
      method: 'GET',
      path: '/ai-voice/app/customer/detailV2',
      params: { customerId }
    })
  }

  /**
   * 搜索客户
   * @param {string} keyword - 搜索关键词
   */
  async searchCustomer(keyword) {
    return this.request({
      method: 'POST',
      path: '/ai-voice/app/customer/page',
      params: {
        page: 1,
        size: 20,
        keyword
      }
    })
  }

  // ========== 工牌接访相关 ==========

  /**
   * 工牌接访列表（分页）
   * @param {Object} params - 查询参数
   * @param {number} params.page - 页码
   * @param {number} params.size - 每页数量
   * @param {string} params.startTime - 开始时间
   * @param {string} params.endTime - 结束时间
   */
  async getVisitPage(params = {}) {
    return this.request({
      method: 'POST',
      path: '/ai-voice/app/visit/page',
      params: {
        page: params.page || 1,
        size: params.size || 20,
        startTime: params.startTime || '',
        endTime: params.endTime || '',
        ...params
      }
    })
  }

  /**
   * 工牌客户列表（分页）
   * @param {Object} params - 查询参数
   * @param {number} params.page - 页码
   * @param {number} params.size - 每页数量
   */
  async getCustomerPage(params = {}) {
    return this.request({
      method: 'POST',
      path: '/ai-voice/app/customer/page',
      params: {
        page: params.page || 1,
        size: params.size || 20,
        ...params
      }
    })
  }

  /**
   * 工牌接访详情
   * @param {string} id - 接访ID
   */
  async getVisitDetail(id) {
    return this.request({
      method: 'GET',
      path: `/ai-voice/app/visit/${id}`
    })
  }

  /**
   * 搜索来访
   * @param {Object} params - 查询参数
   * @param {string} params.keyword - 搜索关键词
   */
  async searchVisit(params = {}) {
    return this.request({
      method: 'GET',
      path: '/ai-voice/app/search/visit/page',
      params
    })
  }

  /**
   * 搜索客户
   * @param {Object} params - 查询参数
   * @param {string} params.keyword - 搜索关键词
   */
  async searchCustomer(params = {}) {
    return this.request({
      method: 'GET',
      path: '/ai-voice/app/search/customer/page',
      params
    })
  }

  /**
   * 搜索录音
   * @param {Object} params - 查询参数
   * @param {string} params.keyword - 搜索关键词
   */
  async searchAudio(params = {}) {
    return this.request({
      method: 'GET',
      path: '/ai-voice/app/search/audio/page',
      params
    })
  }

  /**
   * 获取权限
   */
  async getPermission() {
    return this.request({
      method: 'GET',
      path: '/ai-voice/permission'
    })
  }

  /**
   * 来访列表（看板）
   * @param {Object} params - 查询参数
   */
  async getBoardVisit(params = {}) {
    return this.request({
      method: 'POST',
      path: '/ai-voice/board/visit:page',
      params
    })
  }

  /**
   * 团队数据统计（用户维度）
   * @param {Object} params - 查询参数
   */
  async getBoardUserStat(params = {}) {
    return this.request({
      method: 'POST',
      path: '/ai-voice/board/user:stat',
      params
    })
  }

  /**
   * 团队数据统计（团队维度）
   * @param {Object} params - 查询参数
   */
  async getBoardTeamStat(params = {}) {
    return this.request({
      method: 'POST',
      path: '/ai-voice/board/team:stat',
      params
    })
  }

  /**
   * 报告未认可多少组
   */
  async getReportNoAssist() {
    return this.request({
      method: 'GET',
      path: '/ai-voice/app/report/report-no-assist'
    })
  }

  /**
   * 批量重新分析
   * @param {Object} params - 分析参数
   */
  async batchAnalyze(params) {
    return this.request({
      method: 'POST',
      path: '/ai-voice/visit/batch-analyze',
      params
    })
  }

  // ========== 工牌接访管理 ==========

  /**
   * 查询wifi信息-销售顾问
   */
  async getManagerWifiStatus() {
    return this.request({
      method: 'GET',
      path: '/ai-voice/app/visit/manager/wifi-status'
    })
  }

  /**
   * 设备提供硬件信息
   */
  async deviceProvide() {
    return this.request({
      method: 'GET',
      path: '/ai-voice/app/visit/manager/device/provide'
    })
  }

  /**
   * 开始接待 - 开始录音
   * @param {Object} params - 接待参数
   */
  async startVisitAudio(params = {}) {
    return this.request({
      method: 'GET',
      path: '/ai-voice/app/visit/manager/start-visit-audio',
      params
    })
  }

  /**
   * 结束接待 - 结束录音
   * @param {Object} params - 接待参数
   */
  async stopVisitAudio(params = {}) {
    return this.request({
      method: 'GET',
      path: '/ai-voice/app/visit/manager/stop-visit-audio',
      params
    })
  }

  /**
   * 开始接待
   * @param {Object} params - 接待参数
   */
  async managerStart(params = {}) {
    return this.request({
      method: 'POST',
      path: '/ai-voice/app/visit/manager/start',
      params
    })
  }

  /**
   * 结束接访
   * @param {Object} params - 接待参数
   */
  async managerEnd(params = {}) {
    return this.request({
      method: 'POST',
      path: '/ai-voice/app/visit/manager/end',
      params
    })
  }

  /**
   * 查询销售顾问正在接待的虚拟录音 - 接待中
   */
  async getVisitAudioRunning() {
    return this.request({
      method: 'GET',
      path: '/ai-voice/app/visit/manager/visit-audio-running'
    })
  }

  /**
   * 获取接待分析流程
   */
  async getAnalyzeFlow() {
    return this.request({
      method: 'GET',
      path: '/ai-voice/app/visit/visit/analyze/flow'
    })
  }

  /**
   * 获取来访单客户信息
   * @param {Object} params - 查询参数
   */
  async getVisitCustomerInfo(params = {}) {
    return this.request({
      method: 'GET',
      path: '/ai-voice/app/visit/visit/customer/info',
      params
    })
  }

  // ========== 虚拟接访 ==========

  /**
   * 获取接访配置
   */
  async getReceiveConfig() {
    return this.request({
      method: 'GET',
      path: '/ai-voice/sysConfig'
    })
  }

  /**
   * 获取接访列表
   * @param {Object} params - 查询参数
   */
  async getReceiveList(params = {}) {
    return this.request({
      method: 'POST',
      path: '/ai-voice/app/virtually/visit/record',
      params
    })
  }

  /**
   * 上次接访记录
   */
  async getLastReceive() {
    return this.request({
      method: 'GET',
      path: '/ai-voice/app/virtually/visit/last'
    })
  }

  /**
   * 当前设备状态
   */
  async getDeviceStatus() {
    return this.request({
      method: 'GET',
      path: '/ai-voice/app/virtually/visit/status'
    })
  }

  /**
   * 当前接待中的接访
   */
  async getRunningReceive() {
    return this.request({
      method: 'GET',
      path: '/ai-voice/app/virtually/visit/running'
    })
  }

  /**
   * 修改接访单时间
   * @param {Object} params - 修改参数
   */
  async updateReceiveTime(params) {
    return this.request({
      method: 'POST',
      path: '/ai-voice/app/virtually/visit/change-time',
      params
    })
  }

  /**
   * 手动开始接访
   */
  async manualStartReceive() {
    return this.request({
      method: 'GET',
      path: '/ai-voice/app/virtually/visit/start-virtually-visit'
    })
  }

  /**
   * 结束接访
   * @param {string} id - 接访ID
   */
  async finishReceive(id) {
    return this.request({
      method: 'PUT',
      path: `/ai-voice/app/virtually/visit/close-virtually-visit?id=${id}`
    })
  }

  /**
   * 忽略指定接访单
   * @param {string} id - 接访ID
   */
  async ignoreReceive(id) {
    return this.request({
      method: 'PUT',
      path: `/ai-voice/app/virtually/visit/ignore-audio?id=${id}`
    })
  }

  /**
   * 忽略全部接访单
   */
  async ignoreAllReceive() {
    return this.request({
      method: 'PUT',
      path: '/ai-voice/app/virtually/visit/ignore-audio-all'
    })
  }

  /**
   * 获取时间区间
   */
  async getDateBetween() {
    return this.request({
      method: 'GET',
      path: '/ai-voice/app/virtually/visit/date-between'
    })
  }

  /**
   * 获取客户接访录音列表
   */
  async getSegmentAudio() {
    return this.request({
      method: 'GET',
      path: '/ai-voice/app/customer/virtually/segment/audio'
    })
  }

  /**
   * 查询最新的虚拟接访详情
   */
  async getLastVisitDetail() {
    return this.request({
      method: 'GET',
      path: '/ai-voice/app/virtually/visit/virtually-last-visit-detail'
    })
  }

  /**
   * 同事帮忙接待
   */
  async colleagueReception() {
    return this.request({
      method: 'GET',
      path: '/ai-voice/app/virtually/visit/colleague-reception'
    })
  }

  /**
   * 查询虚拟接访详情
   * @param {Object} params - 查询参数
   */
  async getVirtuallyVisitDetail(params) {
    return this.request({
      method: 'GET',
      path: '/ai-voice/app/virtually/visit/virtually-visit-detail',
      params
    })
  }

  /**
   * 获取来访可绑定录音
   * @param {Object} params - 查询参数
   */
  async getCanBindAudios(params) {
    return this.request({
      method: 'POST',
      path: '/ai-voice/app/visit/virtually-can-bind-audios',
      params
    })
  }

  /**
   * 虚拟单绑定音频
   * @param {Object} params - 绑定参数
   */
  async bindAudios(params) {
    return this.request({
      method: 'POST',
      path: '/ai-voice/app/virtually/visit/virtually-bind-audios',
      params
    })
  }

  /**
   * 批量绑定音频
   * @param {Object} params - 绑定参数
   */
  async bindAudiosBatch(params) {
    return this.request({
      method: 'POST',
      path: '/ai-voice/app/virtually/visit/virtually-bind-audios:batch',
      params
    })
  }

  /**
   * 虚拟单是否关联了真实来访单
   * @param {Object} params - 查询参数
   */
  async isVirtuallyVisitBindRealVisit(params) {
    return this.request({
      method: 'GET',
      path: '/ai-voice/app/virtually/visit/check/virtually/bind',
      params
    })
  }

  /**
   * 结束录音
   * @param {Object} params - 参数
   */
  async closeVirtuallyVisit(params) {
    return this.request({
      method: 'POST',
      path: '/ai-voice/app/virtually/visit/virtually-visit/close',
      params
    })
  }

  /**
   * 开始录音
   * @param {Object} params - 参数
   */
  async createVirtuallyVisit(params) {
    return this.request({
      method: 'POST',
      path: '/ai-voice/app/virtually/visit/virtually-visit/start',
      params
    })
  }

  /**
   * 开启接待的check
   */
  async startReceptionCheck() {
    return this.request({
      method: 'GET',
      path: '/ai-voice/app/virtually/visit/start/reception/check'
    })
  }

  /**
   * 判断接待状态
   */
  async getReceiveStatusInfo() {
    return this.request({
      method: 'GET',
      path: '/ai-voice/app/virtually/visit/status/info'
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

module.exports = VisitApi
