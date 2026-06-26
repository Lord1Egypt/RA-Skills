#!/usr/bin/env node

/**
 * 旺小宝数据助手 - 录音查询 API 客户端
 *
 * 功能：
 * - 封装录音相关 API 调用
 * - 自动处理认证头
 * - 统一的错误处理
 */

const https = require('https')

class AudioApi {
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

  // ========== 录音列表 ==========

  /**
   * 获取录音分页列表
   * @param {Object} params - 查询参数
   */
  async getAudioPage(params = {}) {
    return this.request({
      method: 'POST',
      path: '/ai-voice/app/audio/page',
      params: {
        page: params.page || 1,
        size: params.size || 20,
        ...params
      }
    })
  }

  /**
   * 获取录音详情
   * @param {string} audioId - 录音ID
   */
  async getAudioDetail(audioId) {
    return this.request({
      method: 'GET',
      path: `/ai-voice/audio/detail/${audioId}`
    })
  }

  /**
   * 获取录音详情中视频
   * @param {string} audioId - 录音ID
   */
  async getAudioDetailVideo(audioId) {
    return this.request({
      method: 'GET',
      path: `/ai-voice/audio/video/${audioId}`
    })
  }

  /**
   * 获取录音分析详情(NLP)
   * @param {string} audioId - 录音ID
   */
  async getNlpResult(audioId) {
    return this.request({
      method: 'GET',
      path: `/ai-voice/app/audio/nlp-result/${audioId}`
    })
  }

  /**
   * 录音文本搜索
   * @param {Object} params - 搜索参数
   */
  async audioSplitText(params) {
    return this.request({
      method: 'POST',
      path: '/ai-voice/app/visit/audio-split-text',
      params
    })
  }

  /**
   * 编辑录音
   * @param {Object} params - 编辑参数
   */
  async editAudio(params) {
    return this.request({
      method: 'POST',
      path: '/ai-voice/audio/edit/valid',
      params
    })
  }

  /**
   * 录音绑定接访单
   * @param {Object} params - 绑定参数
   */
  async bindVisit(params) {
    return this.request({
      method: 'POST',
      path: '/ai-voice/audio/bind-visit',
      params
    })
  }

  /**
   * 解绑录音
   * @param {Object} params - 解绑参数
   */
  async unbindAudios(params) {
    return this.request({
      method: 'POST',
      path: '/ai-voice/visit/unbind-audios',
      params
    })
  }

  // ========== 录音基础信息 ==========

  /**
   * 获取录音基础卡片信息
   * @param {string} id - 录音ID
   */
  async getBaseCard(id) {
    return this.request({
      method: 'GET',
      path: `/audio/app/v2/audio/base/card/${id}`
    })
  }

  /**
   * 获取单条录音信息
   * @param {string} id - 录音ID
   */
  async getAudioBase(id) {
    return this.request({
      method: 'GET',
      path: `/audio/app/v2/audio/base/${id}`
    })
  }

  /**
   * 获取单条录音文本
   * @param {string} id - 录音ID
   */
  async getAudioBaseText(id) {
    return this.request({
      method: 'GET',
      path: `/audio/app/v2/audio/base/text/${id}`
    })
  }

  /**
   * 获取外部门录音信息
   * @param {string} id - 录音ID
   */
  async getAudioBaseOut(id) {
    return this.request({
      method: 'GET',
      path: `/audio/app/v2/out/audio/base/${id}`
    })
  }

  /**
   * 获取外部门录音文本
   * @param {string} id - 录音ID
   */
  async getAudioBaseTextOut(id) {
    return this.request({
      method: 'GET',
      path: `/audio/app/v2/out/audio/base/text/${id}`
    })
  }

  /**
   * 音频分享
   * @param {Object} params - 分享参数
   */
  async shareAudio(params) {
    return this.request({
      method: 'POST',
      path: '/audio/app/v2/audio/share',
      params
    })
  }

  // ========== 录音评论 ==========

  /**
   * 获取录音评论列表
   * @param {string} id - 录音ID
   */
  async getCommentaryList(id) {
    return this.request({
      method: 'GET',
      path: `/audio/app/v2/audio/commentary/${id}`
    })
  }

  /**
   * 获取外部门录音评论列表
   * @param {string} id - 录音ID
   */
  async getCommentaryListOut(id) {
    return this.request({
      method: 'GET',
      path: `/audio/app/v2/out/audio/commentary/${id}`
    })
  }

  /**
   * 获取评论文本列表
   * @param {string} audioId - 录音ID
   */
  async getCommentaryText(audioId) {
    return this.request({
      method: 'GET',
      path: `/audio/app/v2/commentary/text/${audioId}`
    })
  }

  /**
   * 获取评论信息详情
   * @param {string} commentaryId - 评论ID
   */
  async getCommentaryDetail(commentaryId) {
    return this.request({
      method: 'GET',
      path: `/audio/app/v2/audio/commentary/${commentaryId}`
    })
  }

  /**
   * 新增录音评论
   * @param {Object} params - 评论参数
   */
  async addCommentary(params) {
    return this.request({
      method: 'POST',
      path: '/audio/app/v2/audio/commentary',
      params
    })
  }

  // ========== AI摘要与问答 ==========

  /**
   * 获取录音摘要和问答
   * @param {string} id - 录音ID
   */
  async getSummaryAndQa(id) {
    return this.request({
      method: 'GET',
      path: `/audio/app/v2/audio/agi/summary/dialogue/${id}`
    })
  }

  /**
   * 提交录音摘要和问答
   * @param {string} id - 录音ID
   */
  async submitSummaryAndQa(id) {
    return this.request({
      method: 'GET',
      path: `/audio/app/v2/audio/agi/dialogue/summary/submit/${id}`
    })
  }

  // ========== 录音扩展信息 ==========

  /**
   * 获取录音扩展信息
   * @param {string} id - 录音ID
   */
  async getAudioExpand(id) {
    return this.request({
      method: 'GET',
      path: `/audio/app/v2/audio/expand/${id}`
    })
  }

  /**
   * 获取音视频
   * @param {string} id - 录音ID
   */
  async getAudioExpandVideo(id) {
    return this.request({
      method: 'GET',
      path: `/audio/app/v2/audio/expand/video/${id}`
    })
  }

  /**
   * 音视频合并
   * @param {string} id - 录音ID
   */
  async getAudioExpandMergeVideo(id) {
    return this.request({
      method: 'GET',
      path: `/audio/app/v2/audio/expand/merge-video/${id}`
    })
  }

  /**
   * 申请音视频
   * @param {Object} params - 申请参数
   */
  async applyVideo(params) {
    return this.request({
      method: 'GET',
      path: '/audio/app/v2/audio/expand/video/apply',
      params
    })
  }
}

module.exports = AudioApi
