#!/usr/bin/env node
/**
 * uni-app + miniprogram-ci 发布脚本
 *
 * 用法：
 *   node scripts/build-uni.js
 *
 * 环境变量：
 *   VERSION               - 发布版本号（默认 1.0.0）
 *   WEAPP_APPID           - 小程序 AppID
 *   WEAPP_PRIVATE_KEY_PATH - 私钥文件路径
 *   WEAPP_PRIVATE_KEY     - 私钥内容（可选）
 *   CI_MODE               - 发布模式: experience | review | release（默认 experience）
 */

const ci = require('miniprogram-ci')
const path = require('path')
const fs = require('fs')

// ── 环境变量读取 ───────────────────────────────────────────
const VERSION = process.env.VERSION || '1.0.0'
const APP_ID = process.env.WEAPP_APPID
const PRIVATE_KEY = process.env.WEAPP_PRIVATE_KEY
const PRIVATE_KEY_PATH = process.env.WEAPP_PRIVATE_KEY_PATH
const CI_MODE = process.env.CI_MODE || 'experience'

// uni-app 构建产物路径
const PROJECT_PATH = path.resolve(__dirname, '../dist/build/mp-weixin')

// ── 前置检查 ────────────────────────────────────────────────
function checkEnv() {
  if (!APP_ID) {
    throw new Error('缺少环境变量 WEAPP_APPID')
  }
  if (!PRIVATE_KEY && !PRIVATE_KEY_PATH) {
    throw new Error('缺少环境变量 WEAPP_PRIVATE_KEY 或 WEAPP_PRIVATE_KEY_PATH')
  }
  if (!fs.existsSync(PROJECT_PATH)) {
    throw new Error(`构建产物不存在: ${PROJECT_PATH}\n请先运行: npm run build:mp-weixin`)
  }
}

// ── 生成私钥文件（从环境变量）───────────────────────────────
function preparePrivateKey() {
  if (PRIVATE_KEY_PATH && PRIVATE_KEY) {
    const dir = path.dirname(PRIVATE_KEY_PATH)
    if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true })
    fs.writeFileSync(PRIVATE_KEY_PATH, PRIVATE_KEY)
    console.log(`  私钥已写入: ${PRIVATE_KEY_PATH}`)
  }
}

// ── 主流程 ──────────────────────────────────────────────────
async function main() {
  console.log(`\n🚀 uni-app 微信小程序发布 v${VERSION}`)
  console.log(`   模式: ${CI_MODE}`)
  console.log(`   AppID: ${APP_ID}\n`)

  checkEnv()
  preparePrivateKey()

  const resolvedKeyPath = PRIVATE_KEY_PATH || path.resolve(__dirname, '../keys/private.key')

  const project = new ci.Project({
    appid: APP_ID,
    type: 'miniProgram',
    projectPath: PROJECT_PATH,
    privateKeyPath: resolvedKeyPath,
    ignores: [
      'node_modules/**/*',
      '*.md',
      '.git/**/*',
      'project.config.json',
    ],
  })

  // 1. 上传代码
  console.log('📤 正在上传代码...')
  const uploadResult = await ci.upload({
    project,
    version: VERSION,
    desc: `CI 自动构建 v${VERSION} - ${new Date().toLocaleString('zh-CN')}`,
    setting: {
      es6: true,
      minify: true,
      codeProtect: false,
      autoPrefixWXSS: true,
      minifyWXML: true,
      minifyWXSS: true,
      minifyJS: true,
    },
    onProgressUpdate: (info) => {
      process.stdout.write(
        `\r   [${info.status}] ${info.message} ${info.total ? `${info.current}/${info.total}` : ''}   `
      )
    },
  })
  console.log('\n✅ 代码上传成功')
  if (uploadResult.subPackageInfo) {
    console.log('   分包信息:', JSON.stringify(uploadResult.subPackageInfo))
  }

  // 2. 体验版
  if (CI_MODE === 'experience' || CI_MODE === 'review' || CI_MODE === 'release') {
    console.log('\n🎧 正在发布体验版...')
    const { testUrl } = await ci.Experience.createTestVersion({
      project,
      version: VERSION,
      desc: `CI 自动构建 v${VERSION}`,
    })
    console.log('✅ 体验版发布成功')
    console.log('   体验二维码:', testUrl)
  }

  // 3. 提交审核
  if (CI_MODE === 'review' || CI_MODE === 'release') {
    console.log('\n📋 正在提交审核...')
    await ci.Code.commitVersion({
      project,
      version: VERSION,
      desc: `CI 自动提交审核 v${VERSION}`,
    })
    console.log('✅ 已提交审核')
  }

  // 4. 发布（需审核通过）
  if (CI_MODE === 'release') {
    console.log('\n🎉 正在发布正式版...')
    await ci.Code.release({
      project,
      version: VERSION,
    })
    console.log('✅ 正式版发布成功')
  }

  console.log('\n✨ 发布全部完成!\n')
}

main().catch((err) => {
  console.error('\n❌ 发布失败:', err.message)
  if (err.message.includes('40013')) {
    console.error('   → AppID 不合法，检查 WEAPP_APPID 是否与私钥匹配')
  }
  if (err.message.includes('401')) {
    console.error('   → 密钥错误，检查私钥文件是否正确')
  }
  process.exit(1)
})
