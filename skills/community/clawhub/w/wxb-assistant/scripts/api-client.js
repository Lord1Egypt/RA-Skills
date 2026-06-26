#!/usr/bin/env node

/**
 * 旺小宝数据助手 - API 客户端（主入口）
 *
 * 功能：
 * - 封装所有旺小宝后端 API 调用
 * - 自动处理认证头
 * - 统一的错误处理
 * - 模块化分类管理API
 */

const AuthManager = require('./auth-manager')
const VisitApi = require('./api/visit-api')
const CustomerApi = require('./api/customer-api')
const AudioApi = require('./api/audio-api')
const PankeApi = require('./api/panke-api')
const OtherApi = require('./api/other-api')

class ApiClient {
  constructor() {
    this.baseURL = 'wangkeapp.wangxiaobao.com'
    this.authManager = new AuthManager()
    this.token = null

    // 初始化各模块 API
    this.visit = new VisitApi(this.baseURL, () => this.getToken())
    this.customer = new CustomerApi(this.baseURL, () => this.getToken())
    this.audio = new AudioApi(this.baseURL, () => this.getToken())
    this.panke = new PankeApi(this.baseURL, () => this.getToken())
    this.other = new OtherApi(this.baseURL, () => this.getToken())
  }

  /**
   * 获取认证 Token
   * 如果没有 token，会自动启动授权流程
   */
  async getToken() {
    if (!this.token) {
      this.token = await this.authManager.authorize()
    }
    return this.token
  }

  // ========== 用户与租户相关 ==========

  /**
   * 获取当前登录用户信息
   */
  async getUserInfo() {
    return this.request({
      method: 'GET',
      path: '/saas/v2/user/info'
    })
  }

  /**
   * 获取当前用户的租户和项目列表
   */
  async getTenantAndEstateList() {
    return this.request({
      method: 'GET',
      path: '/saas/v2/estate/tenant-and-estate/by-user-id'
    })
  }

  /**
   * 切换项目
   * @param {string} projectId - 项目ID
   */
  async switchProject(projectId) {
    return this.request({
      method: 'POST',
      path: '/session/switch-project',
      params: { projectId }
    })
  }

  /**
   * 切换租户
   * @param {string} tenantId - 租户ID
   */
  async switchTenant(tenantId) {
    return this.request({
      method: 'POST',
      path: '/session/switch-tenant',
      params: { tenantId }
    })
  }

  // ========== 兼容性方法（映射到各模块）==========

  // 客户中心（customer 模块）
  async getCustomerList(params) { return this.customer.getCustomerList(params) }
  async getCustomerOne(params) { return this.customer.getCustomerOne(params) }
  async searchCustomer(params) { return this.customer.searchCustomer(params) }
  async getCustomerDetail(params) { return this.customer.getCustomerDetail(params) }
  async getCustomerTrajectory(params) { return this.customer.getCustomerTrajectory(params) }
  async getFocusWangList(params) { return this.customer.getFocusWangList(params) }
  async getPointWangList(params) { return this.customer.getPointWangList(params) }
  async predictCanView(params) { return this.customer.predictCanView(params) }
  async rePredict(params) { return this.customer.rePredict(params) }

  // 工牌客户（visit 模块）
  async getCustomerPageV2(params) { return this.visit.getCustomerPageV2(params) }
  async getCustomerDetailV2(customerId) { return this.visit.getCustomerDetailV2(customerId) }
  async searchVisitCustomer(keyword) { return this.visit.searchCustomer(keyword) }

  // 工牌接访相关
  async getVisitPage(params) { return this.visit.getVisitPage(params) }
  async getCustomerPage(params) { return this.visit.getCustomerPage(params) }
  async getVisitDetail(id) { return this.visit.getVisitDetail(id) }
  async searchVisit(params) { return this.visit.searchVisit(params) }
  async searchAudio(params) { return this.visit.searchAudio(params) }
  async getPermission() { return this.visit.getPermission() }

  // 盘客列表
  async getPankePage(params) { return this.panke.getPankePage(params) }
  async getPankePageScore(params) { return this.panke.getPankePageScore(params) }
  async getPankeSearchCondition(params) { return this.panke.getSearchCondition(params) }
  async getPankePermission(params) { return this.panke.getPermission(params) }

  // 盘客详情
  async getPankeDetail(params) { return this.panke.getPankeDetail(params) }
  async getPankeDetailV2(params) { return this.panke.getPankeDetailV2(params) }
  async getWangPankeDetailV2(params) { return this.panke.getWangPankeDetailV2(params) }
  async getPankeCompleteTable(params) { return this.panke.getCompleteTable(params) }
  async getPankeCompleteTableV2(params) { return this.panke.getCompleteTableV2(params) }
  async getPankeSellingPointReach(params) { return this.panke.getSellingPointReach(params) }
  async getPankeRiskList(params) { return this.panke.getRiskList(params) }
  async getPankeFocusList(params) { return this.panke.getFocusList(params) }
  async getPankeTableCusVisitInfo(params) { return this.panke.getTableCusVisitInfo(params) }

  // 盘客收集表
  async getPankeTable(params) { return this.panke.getTable(params) }
  async submitPankeTable(params) { return this.panke.submitTable(params) }
  async editPankeTableField(params) { return this.panke.editTableField(params) }
  async getPankeCheckTable(params) { return this.panke.getCheckTable(params) }
  async markPankeSpecialVisits(params) { return this.panke.markSpecialVisits(params) }
  async getPankeAiAssistedRecall(params) { return this.panke.getAiAssistedRecall(params) }

  // 盘客SOP
  async getGoldenContentByAudioId(params) { return this.panke.getGoldenContentByAudioId(params) }
  async goldenContentAccept(params) { return this.panke.goldenContentAccept(params) }
  async createGoldenAnalysisTask(params) { return this.panke.createGoldenAnalysisTask(params) }
  async getSalesPitchIntent() { return this.panke.getSalesPitchIntent() }
  async updateSalesPitchIntent(params) { return this.panke.updateSalesPitchIntent(params) }

  // 盘客评论
  async getPankeCommentList(params) { return this.panke.getCommentList(params) }
  async addPankeComment(params) { return this.panke.addComment(params) }

  // 盘客其他
  async getEventIdByCustomerId(params) { return this.panke.getEventIdByCustomerId(params) }
  async getPankeIdByVisitId(params) { return this.panke.getPankeIdByVisitId(params) }

  // 今日代办
  async virtuallyTodayTodoCount(params) { return this.other.virtuallyTodayTodoCount(params) }
  async virtuallyTodayTodoList(params) { return this.other.virtuallyTodayTodoList(params) }
  async virtuallyTodayTodoById(params) { return this.other.virtuallyTodayTodoById(params) }

  // 录音相关
  async getAudioPage(params) { return this.audio.getAudioPage(params) }
  async getAudioDetail(audioId) { return this.audio.getAudioDetail(audioId) }
  async getAudioDetailVideo(audioId) { return this.audio.getAudioDetailVideo(audioId) }
  async getNlpResult(audioId) { return this.audio.getNlpResult(audioId) }
  async audioSplitText(params) { return this.audio.audioSplitText(params) }
  async editAudio(params) { return this.audio.editAudio(params) }
  async bindVisit(params) { return this.audio.bindVisit(params) }
  async unbindAudios(params) { return this.audio.unbindAudios(params) }
  async getBaseCard(id) { return this.audio.getBaseCard(id) }
  async getAudioBase(id) { return this.audio.getAudioBase(id) }
  async getAudioBaseText(id) { return this.audio.getAudioBaseText(id) }
  async getAudioBaseOut(id) { return this.audio.getAudioBaseOut(id) }
  async getAudioBaseTextOut(id) { return this.audio.getAudioBaseTextOut(id) }
  async getCommentaryList(id) { return this.audio.getCommentaryList(id) }
  async getCommentaryListOut(id) { return this.audio.getCommentaryListOut(id) }
  async getCommentaryText(audioId) { return this.audio.getCommentaryText(audioId) }
  async getCommentaryDetail(commentaryId) { return this.audio.getCommentaryDetail(commentaryId) }
  async addCommentary(params) { return this.audio.addCommentary(params) }
  async getSummaryAndQa(id) { return this.audio.getSummaryAndQa(id) }
  async submitSummaryAndQa(id) { return this.audio.submitSummaryAndQa(id) }
  async getAudioExpand(id) { return this.audio.getAudioExpand(id) }
  async getAudioExpandVideo(id) { return this.audio.getAudioExpandVideo(id) }
  async getAudioExpandMergeVideo(id) { return this.audio.getAudioExpandMergeVideo(id) }
  async applyVideo(params) { return this.audio.applyVideo(params) }

  /**
   * 发送 HTTPS 请求（内部方法）
   */
  async request(options) {
    const token = await this.getToken()
    const https = require('https')

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
}

// CLI 接口
if (require.main === module) {
  const client = new ApiClient()
  const command = process.argv[2]
  const args = process.argv.slice(3)

  async function runCommand() {
    try {
      switch (command) {
        case 'user-info':
          const userInfo = await client.getUserInfo()
          console.log(JSON.stringify(userInfo, null, 2))
          break

        case 'tenant-list':
          const tenantList = await client.getTenantAndEstateList()
          console.log(JSON.stringify(tenantList, null, 2))
          break

        case 'switch-project':
          const switchProjectRes = await client.switchProject(args[0])
          console.log(JSON.stringify(switchProjectRes, null, 2))
          break

        case 'switch-tenant':
          const switchTenantRes = await client.switchTenant(args[0])
          console.log(JSON.stringify(switchTenantRes, null, 2))
          break

        // 客户管理
        case 'customer':
          const customerList = await client.getCustomerList()
          console.log(JSON.stringify(customerList, null, 2))
          break

        case 'customer-detail':
          const customerDetail = await client.getCustomerDetail(args[0])
          console.log(JSON.stringify(customerDetail, null, 2))
          break

        // 工牌接访
        case 'visit-page':
          const visitPage = await client.getVisitPage()
          console.log(JSON.stringify(visitPage, null, 2))
          break

        case 'visit-detail':
          const visitDetail = await client.getVisitDetail(args[0])
          console.log(JSON.stringify(visitDetail, null, 2))
          break

        // 盘客
        case 'panke-page':
          const pankePage = await client.getPankePage()
          console.log(JSON.stringify(pankePage, null, 2))
          break

        case 'panke-detail':
          const pankeDetail = await client.getPankeDetail({ id: args[0] })
          console.log(JSON.stringify(pankeDetail, null, 2))
          break

        case 'panke-golden':
          const pankeGolden = await client.getGoldenContentByAudioId({ audioId: args[0] })
          console.log(JSON.stringify(pankeGolden, null, 2))
          break

        // 今日代办
        case 'today-todo-count':
          const todoCount = await client.virtuallyTodayTodoCount()
          console.log(JSON.stringify(todoCount, null, 2))
          break

        case 'today-todo-list':
          const todoList = await client.virtuallyTodayTodoList()
          console.log(JSON.stringify(todoList, null, 2))
          break

        // 录音
        case 'audio-base':
          const audioBase = await client.getAudioBase(args[0])
          console.log(JSON.stringify(audioBase, null, 2))
          break

        case 'audio-text':
          const audioText = await client.getAudioBaseText(args[0])
          console.log(JSON.stringify(audioText, null, 2))
          break

        case 'audio-summary':
          const audioSummary = await client.getAudioSummaryAndQa(args[0])
          console.log(JSON.stringify(audioSummary, null, 2))
          break

        case 'audio-expand':
          const audioExpand = await client.getAudioExpand(args[0])
          console.log(JSON.stringify(audioExpand, null, 2))
          break

        default:
          console.error(`
用法:
  # 用户与租户
  node api-client.js user-info                # 获取当前登录用户信息
  node api-client.js tenant-list              # 获取用户的租户和项目列表
  node api-client.js switch-project <id>      # 切换到指定项目
  node api-client.js switch-tenant <id>       # 切换到指定租户

  # 客户管理
  node api-client.js customer                 # 获取客户列表
  node api-client.js customer-detail <id>     # 获取客户详情

  # 工牌接访
  node api-client.js visit-page               # 获取接访列表
  node api-client.js visit-detail <id>        # 获取接访详情

  # 盘客
  node api-client.js panke-page               # 获取盘客列表
  node api-client.js panke-detail <id>        # 获取盘客详情
  node api-client.js panke-golden <audioId>   # 获取盘客金句

  # 今日代办
  node api-client.js today-todo-count         # 获取待办统计
  node api-client.js today-todo-list          # 获取待办列表

  # 录音
  node api-client.js audio-base <id>          # 获取录音信息
  node api-client.js audio-text <id>          # 获取录音文本
  node api-client.js audio-summary <id>       # 获取录音摘要和问答
  node api-client.js audio-expand <id>        # 获取录音扩展信息

  # 模块化调用
  node api-client.js visit.getVisitPage       # 使用工牌接访模块
  node api-client.js customer.getCustomerPage # 使用客户中心模块
  node api-client.js panke.getSalesPitchIntent # 使用盘客模块
  node api-client.js other.getGoldenContentPage # 使用其他功能模块
          `)
          process.exit(1)
      }
    } catch (err) {
      console.error('错误:', err.message)
      process.exit(1)
    }
  }

  runCommand()
}

module.exports = ApiClient
