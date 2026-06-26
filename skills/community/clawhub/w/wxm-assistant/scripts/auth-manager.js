#!/usr/bin/env node

/**
 * 旺小美数据助手 - 授权管理器
 *
 * 功能：
 * - 使用远程授权服务器进行扫码授权
 * - 管理 token 的存储和验证
 */

let openModule = null
try {
  openModule = require('open')
} catch (e) {
  // open 包可能未安装，不影响主流程
}
const https = require('https')
const http = require('http')
const fs = require('fs')
const path = require('path')
const crypto = require('crypto')

const AUTH_BASE_URL = 'https://www.wangxiaobao.com'

class AuthManager {
  constructor() {
    this.tokenPath = path.join(process.env.HOME, '.wangke-auth-token')
  }

  /**
   * 启动授权流程
   * @returns {Promise<string>} 返回 token
   */
  async authorize() {
    // 优先使用已保存的 token
    const existingToken = this.getSavedToken()
    if (existingToken) {
      return existingToken
    }

    // 扫码授权
    console.error('📱 开始授权流程...')
    const token = await this.startRemoteAuthServer()
    this.saveToken(token)
    console.error('✅ 授权成功！')
    return token
  }

  /**
   * 使用远程授权服务器
   */
  async startRemoteAuthServer() {
    const sessionId = this.generateSessionId()
    const authPageUrl = `${AUTH_BASE_URL}/auth.html?session=${sessionId}`

    console.error(`\n📱 旺小美数据授权\n`)
    console.error(`🔗 授权链接: ${authPageUrl}`)
    console.error(`\n步骤:`)
    console.error(`  1. 用浏览器打开上面的链接`)
    console.error(`  2. 用旺小美 App 扫描页面上的二维码`)
    console.error(`  3. 授权成功后这里会自动继续\n`)

    // 尝试自动打开浏览器（有桌面环境时）
    if (openModule) {
      try {
        await openModule(authPageUrl)
        console.error('✅ 已在浏览器中打开授权页面，等待扫码...\n')
      } catch (e) {
        console.error(`ℹ️  无法自动打开浏览器 (${e.message})，请手动复制上面的链接到浏览器打开\n`)
      }
    } else {
      console.error('ℹ️  当前环境不支持自动打开浏览器，请手动复制上面的链接\n')
    }

    const maxAttempts = 150 // 5分钟
    let attempts = 0

    while (attempts < maxAttempts) {
      attempts++

      try {
        const result = await this.httpGet(`${AUTH_BASE_URL}/auth/check?session=${sessionId}`)
        const data = JSON.parse(result)

        if (data.authorized) {
          console.error('✅ 扫码授权成功，正在获取 token...\n')
          const tokenResult = await this.httpGet(`${AUTH_BASE_URL}/auth/token?session=${sessionId}`)
          const tokenData = JSON.parse(tokenResult)

          if (tokenData.token) {
            return tokenData.token
          }
        }

        await new Promise(resolve => setTimeout(resolve, 2000))
      } catch (error) {
        await new Promise(resolve => setTimeout(resolve, 2000))
      }
    }

    throw new Error('授权超时（5分钟）')
  }

  /**
   * HTTP GET 请求封装
   */
  httpGet(url) {
    return new Promise((resolve, reject) => {
      const client = url.startsWith('https') ? https : http

      const req = client.get(url, (res) => {
        let data = ''

        res.on('data', (chunk) => {
          data += chunk
        })

        res.on('end', () => {
          if (res.statusCode === 200) {
            resolve(data)
          } else {
            reject(new Error(`HTTP ${res.statusCode}`))
          }
        })
      })

      req.on('error', reject)
      req.setTimeout(10000, () => {
        req.destroy()
        reject(new Error('请求超时'))
      })
    })
  }

  /**
   * 获取已保存的 token
   * @returns {string|null}
   */
  getSavedToken() {
    try {
      if (fs.existsSync(this.tokenPath)) {
        const token = fs.readFileSync(this.tokenPath, 'utf-8').trim()
        if (token && token.length > 10) {
          return token
        }
      }
    } catch (e) {
      console.error('读取 token 失败:', e.message)
    }
    return null
  }

  /**
   * 保存 token
   */
  saveToken(token) {
    try {
      fs.writeFileSync(this.tokenPath, token, 'utf-8')
      try {
        fs.chmodSync(this.tokenPath, 0o600)
      } catch (e) {
        // chmod 在某些系统上可能失败，不影响主流程
      }
    } catch (e) {
      console.error('保存 token 失败:', e.message)
      throw e
    }
  }

  /**
   * 清除 token
   */
  clearToken() {
    if (fs.existsSync(this.tokenPath)) {
      fs.unlinkSync(this.tokenPath)
      console.error('🗑️  已清除授权信息')
    }
  }

  /**
   * 生成随机会话 ID
   */
  generateSessionId() {
    return crypto.randomBytes(16).toString('hex')
  }
}

// CLI 接口
if (require.main === module) {
  const manager = new AuthManager()

  const command = process.argv[2]

  if (command === 'clear') {
    manager.clearToken()
  } else if (command === 'check') {
    const token = manager.getSavedToken()
    if (token) {
      console.error('✅ 已授权')
      console.log(token)
    } else {
      console.error('❌ 未授权')
      process.exit(1)
    }
  } else {
    manager.authorize()
      .then(token => {
        console.log(token)
      })
      .catch(err => {
        console.error('❌ 授权失败:', err.message)
        process.exit(1)
      })
  }
}

module.exports = AuthManager
