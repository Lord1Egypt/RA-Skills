#!/usr/bin/env node

/**
 * 旺小美数据助手 - API 客户端
 *
 * 功能：
 * - 封装所有旺小美后端 API 调用
 * - 自动处理认证头
 * - 统一的错误处理
 */

const AuthManager = require('./auth-manager')
const https = require('https')

class ApiClient {
  constructor() {
    this.baseURL = 'wangkeapp.wangxiaobao.com'
    this.authManager = new AuthManager()
    this.token = null
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

  /**
   * 发送 HTTPS 请求
   * @param {Object} options - 请求选项
   * @param {string} options.method - HTTP 方法
   * @param {string} options.path - 请求路径
   * @param {Object} options.params - 请求参数
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

  // ========== 录音相关 ==========

  /**
   * 获取录音列表
   * @param {Object} params - 查询参数
   * @param {number} params.page - 页码
   * @param {number} params.size - 每页数量
   * @param {string} params.fromDate - 开始日期，格式：YYYY-MM-DD HH:mm:ss
   * @param {string} params.toDate - 结束日期，格式：YYYY-MM-DD HH:mm:ss
   * @param {string} params.sortField - 排序字段，默认 startTime
   * @param {string} params.sortOrder - 排序方向，desc/asc
   * @param {string} params.status - 录音状态筛选
   * @param {string} params.hasValid - 有效性筛选
   * @param {string} params.hasAudio - 是否有录音筛选
   * @param {string} params.warn - 预警筛选
   * @param {string} params.visitGroup - 来访分组筛选
   * @param {Array} params.userList - 用户列表筛选
   * @param {Array} params.masterList - 主访人列表筛选
   * @param {Array} params.deputyList - 副访人列表筛选
   * @param {string} params.audioStatus - 录音状态
   */
  async getAudioList(params = {}) {
    const data = await this.request({
      method: 'POST',
      path: '/beautx-ai-voice/app/audio/page',
      params: {
        page: params.page || 1,
        size: params.size || 10,
        sortList: [{ sortField: params.sortField || 'startTime', sortOrder: params.sortOrder || 'desc' }],
        fromDate: params.fromDate || '',
        toDate: params.toDate || '',
        hasValid: params.hasValid !== undefined ? params.hasValid : '',
        hasAudio: params.hasAudio !== undefined ? params.hasAudio : '',
        status: params.status !== undefined ? params.status : '',
        warn: params.warn !== undefined ? params.warn : '',
        visitGroup: params.visitGroup !== undefined ? params.visitGroup : '',
        userList: params.userList || [],
        masterList: params.masterList || [],
        deputyList: params.deputyList || [],
        audioStatus: params.audioStatus !== undefined ? params.audioStatus : '',
        ...params
      }
    })
    return data
  }

  /**
   * 获取录音详情
   * @param {string} audioId - 录音ID
   */
  async getAudioDetail(audioId) {
    return this.request({
      method: 'GET',
      path: `/beautx-ai-voice/audio/detail/${audioId}`
    })
  }

  /**
   * 获取录音 NLP 分析结果
   * @param {string} audioId - 录音ID
   */
  async getAudioNLP(audioId) {
    return this.request({
      method: 'GET',
      path: `/beautx-ai-voice/app/audio/nlp-result/${audioId}`
    })
  }

  // ========== 接访相关 ==========

  /**
   * 获取接访/接诊列表
   * @param {Object} params - 查询参数
   * @param {number} params.page - 页码
   * @param {number} params.size - 每页数量
   * @param {string} params.startTime - 开始时间，格式：YYYY-MM-DD HH:mm:ss
   * @param {string} params.endTime - 结束时间，格式：YYYY-MM-DD HH:mm:ss
   */
  async getVisitList(params = {}) {
    const data = await this.request({
      method: 'GET',
      path: '/beautx-ai-voice/visit',
      params: {
        page: params.page || 1,
        size: params.size || 10,
        ...params
      }
    })
    return data
  }

  /**
   * 获取来访详情
   * @param {string} visitId - 来访ID
   */
  async getVisitDetail(visitId) {
    return this.request({
      method: 'GET',
      path: `/app/visit/${visitId}`
    })
  }

  // ========== 客户相关 ==========

  /**
   * 获取客户列表
   * @param {Object} params - 查询参数
   * @param {number} params.page - 页码
   * @param {number} params.size - 每页数量
   * @param {string} params.teamId - 团队ID
   * @param {string} params.startTime - 开始时间
   * @param {string} params.endTime - 结束时间
   * @param {Array} params.majorUserIds - 主用户ID列表
   * @param {Array} params.portraitTypeIds - 画像类型ID列表
   * @param {Array} params.portraitValueIds - 画像值ID列表
   * @param {Array} params.ownerConsultantIds - 所属顾问ID列表
   * @param {Array} params.guestTypes - 客户类型列表
   * @param {Array} params.dealStatuses - 成交状态列表
   * @param {Array} params.guestPurposes - 来访目的列表
   * @param {Array} params.guestSources - 客户来源列表
   * @param {Array} params.appointExperts - 指定专家列表
   * @param {Array} params.guestDepartments - 客户部门列表
   * @param {Array} params.guestLevels - 客户级别列表
   * @param {Array} params.customerIntentionLevels - 意向程度列表
   * @param {Array} params.customerValueLevels - 客户价值等级列表
   * @param {Array} params.evaluationGrades - 评估等级列表
   * @param {string} params.hasAudio - 是否有录音
   */
  async getCustomerList(params = {}) {
    const data = await this.request({
      method: 'POST',
      path: '/beautx-ai-voice/app/customer/pageV2',
      params: {
        page: params.page || 1,
        size: params.size || 20,
        teamId: params.teamId || '',
        startTime: params.startTime || '',
        endTime: params.endTime || '',
        majorUserIds: params.majorUserIds || [],
        portraitTypeIds: params.portraitTypeIds || [],
        portraitValueIds: params.portraitValueIds || [],
        ownerConsultantIds: params.ownerConsultantIds || [],
        guestTypes: params.guestTypes || [],
        dealStatuses: params.dealStatuses || [],
        guestPurposes: params.guestPurposes || [],
        guestSources: params.guestSources || [],
        appointExperts: params.appointExperts || [],
        guestDepartments: params.guestDepartments || [],
        guestLevels: params.guestLevels || [],
        customerIntentionLevels: params.customerIntentionLevels || [],
        customerValueLevels: params.customerValueLevels || [],
        evaluationGrades: params.evaluationGrades || [],
        hasAudio: params.hasAudio || '',
        ...params
      }
    })
    return data
  }

  /**
   * 获取客户详情
   * @param {string} customerId - 客户ID
   */
  async getCustomerDetail(customerId) {
    return this.request({
      method: 'GET',
      path: '/beautx-ai-voice/app/customer/detailV2',
      params: { customerId }
    })
  }

  /**
   * 搜索客户
   * @param {string} keyword - 搜索关键词
   */
  async searchCustomer(keyword) {
    const data = await this.request({
      method: 'POST',
      path: '/beautx-ai-voice/app/customer/page',
      params: {
        page: 1,
        size: 20,
        keyword
      }
    })
    return data
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

        case 'audio':
          // 支持: audio [page] [size] 或 audio --fromDate "YYYY-MM-DD HH:mm:ss" --toDate "YYYY-MM-DD HH:mm:ss"
          const audioParams = {}
          for (let i = 0; i < args.length; i++) {
            if (args[i] === '--fromDate' && args[i+1]) { audioParams.fromDate = args[i+1]; i++ }
            else if (args[i] === '--toDate' && args[i+1]) { audioParams.toDate = args[i+1]; i++ }
            else if (!audioParams.fromDate && !args[i].startsWith('--')) {
              if (!audioParams.page) audioParams.page = parseInt(args[i])
              else audioParams.size = parseInt(args[i])
            }
          }
          const audioList = await client.getAudioList(audioParams)
          console.log(JSON.stringify(audioList, null, 2))
          break

        case 'customer':
          const customerList = await client.getCustomerList()
          console.log(JSON.stringify(customerList, null, 2))
          break

        case 'visit':
          const visitList = await client.getVisitList()
          console.log(JSON.stringify(visitList, null, 2))
          break

        case 'audio-detail':
          const audioDetail = await client.getAudioDetail(args[0])
          console.log(JSON.stringify(audioDetail, null, 2))
          break

        case 'customer-detail':
          const customerDetail = await client.getCustomerDetail(args[0])
          console.log(JSON.stringify(customerDetail, null, 2))
          break

        default:
          console.error(`
用法:
  node api-client.js user-info          # 获取当前登录用户信息
  node api-client.js tenant-list        # 获取用户的租户和项目列表
  node api-client.js switch-project <id> # 切换到指定项目
  node api-client.js switch-tenant <id>  # 切换到指定租户
  node api-client.js audio [page] [size]             # 获取录音列表
  node api-client.js audio --fromDate "2026-04-27 00:00:00" --toDate "2026-04-27 23:59:59"  # 按日期查询录音
  node api-client.js audio-detail <id>  # 获取录音详情
  node api-client.js customer           # 获取客户列表
  node api-client.js customer-detail <id> # 获取客户详情
  node api-client.js visit              # 获取接访列表
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
