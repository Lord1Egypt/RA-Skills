/**
 * 抖音视频解析与下载 - 无外部依赖，仅用 Node 内置模块。
 * 需 Node 18+（fetch、Readable.fromWeb、stream/promises）。
 *
 * 用法:
 *   仅解析: node parse-douyin-video.js <抖音URL>
 *   下载到临时目录: node parse-douyin-video.js <抖音URL> --download
 *   下载到指定路径: node parse-douyin-video.js <抖音URL> <输出文件路径>
 */

const { createWriteStream, statSync } = require('fs')
const { Readable } = require('stream')
const { pipeline } = require('stream/promises')
const { tmpdir } = require('os')
const path = require('path')
const { buildAnalysis } = require('./build-content-analysis')

const DEFAULT_HEADERS = {
  'User-Agent':
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
  Accept:
    'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
  'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
  Connection: 'keep-alive',
  Referer: 'https://www.douyin.com/',
}

async function extractAwemeId(url) {
  let match = url.match(/modal_id=([0-9]+)/)
  if (match) return match[1]

  match = url.match(/video\/([^/?]*)/)
  if (match) return match[1]

  match = url.match(/note\/([^/?]*)/)
  if (match) return match[1]

  match = url.match(/(https?:\/\/\S+)/)
  if (match) {
    try {
      const res = await fetch(match[1], { method: 'HEAD', redirect: 'follow' })
      const finalUrl = res.url
      match = finalUrl.match(/video\/([^/?]*)/)
      if (match) return match[1]
      match = finalUrl.match(/note\/([^/?]*)/)
      if (match) return match[1]
    } catch {
      // 重定向失败，继续抛下面的错误
    }
  }

  throw new Error(`无法从抖音URL中提取视频ID: ${url}`)
}

async function parseDouyinVideoUrl(url) {
  const awemeId = await extractAwemeId(url)
  const requestUrl = `https://www.douyin.com/jingxuan?modal_id=${awemeId}`

  const response = await fetch(requestUrl, { method: 'GET', headers: DEFAULT_HEADERS })
  if (!response.ok) {
    throw new Error(`请求失败，状态码: ${response.status}`)
  }

  const htmlContent = await response.text()
  const pattern = /"([^"]*?(?:playAddr|searchProps|app)[^"]*?)"/g
  const matches = htmlContent.match(pattern)

  let targetMatch = null
  if (matches) {
    for (const match of matches) {
      if (
        match.includes('playAddr') &&
        match.includes('searchProps') &&
        match.includes('app')
      ) {
        targetMatch = match.slice(1, -1)
        break
      }
    }
  }

  if (!targetMatch) {
    throw new Error('未找到包含视频数据的JSON字符串')
  }

  const decodedJson = decodeURIComponent(targetMatch)
  const videoDataJson = JSON.parse(decodedJson)

  const videoDetail = videoDataJson?.app?.videoDetail
  if (!videoDetail) {
    throw new Error('未找到videoDetail数据')
  }

  const desc = videoDetail.desc ?? ''
  const videoInfo = videoDetail.video ?? {}
  const playAddr = videoInfo.playAddr ?? []

  let videoUrl = ''
  if (Array.isArray(playAddr) && playAddr.length > 0) {
    if (typeof playAddr[0] === 'object' && playAddr[0]?.src) {
      videoUrl = playAddr[0].src
    } else if (
      playAddr.length > 1 &&
      typeof playAddr[1] === 'object' &&
      playAddr[1]?.src
    ) {
      videoUrl = playAddr[1].src
    }
  }

  if (!videoUrl) {
    throw new Error('无法获取有效的视频播放地址')
  }

  // 从desc中提取标题作为文件名
  let fileName = '视频'
  if (desc) {
    // 移除话题标签，取前30个字符作为文件名
    fileName = desc.replace(/#\S+/g, '').trim().substring(0, 30) || '视频'
    // 移除特殊字符
    fileName = fileName.replace(/[\\/:*?"<>|]/g, '')
  }
  fileName += '.mp4'

  return {
    title: desc,
    desc,
    cover_url: '',
    file_name: fileName,
    video_urls: [
      {
        video_url: videoUrl,
        resolution_type: 720,
        resolution_str: '默认',
      },
    ],
  }
}

async function downloadVideoToFile(videoUrl, outputPath) {
  const response = await fetch(videoUrl, {
    method: 'GET',
    headers: {
      ...DEFAULT_HEADERS,
      Referer: 'https://www.douyin.com/',
    },
  })
  if (!response.ok) {
    throw new Error(`下载失败，状态码: ${response.status}`)
  }
  const body = response.body
  if (!body) {
    throw new Error('响应体为空')
  }
  const nodeStream = Readable.fromWeb(body)
  const dest = createWriteStream(outputPath)
  await pipeline(nodeStream, dest)
}

/**
 * 下载到系统临时目录
 * @returns {string} 临时文件路径
 */
function createTempFilePath() {
  const tmpDir = tmpdir()
  const tempDir = path.join(tmpDir, `douyin-${Date.now()}`)
  // 使用fs模块的mkdirSync
  require('fs').mkdirSync(tempDir, { recursive: true })
  return path.join(tempDir, 'video.mp4')
}



async function parseAndDownload(douyinUrl, outputPathOrFlag) {
  const result = await parseDouyinVideoUrl(douyinUrl)
  
  // 判断是否需要下载
  let downloadPath = null
  if (outputPathOrFlag === '--download' || outputPathOrFlag === '-d') {
    // 下载到系统临时目录
    downloadPath = createTempFilePath()
    await downloadVideoToFile(result.video_urls[0].video_url, downloadPath)
  } else if (outputPathOrFlag) {
    // 下载到指定路径
    downloadPath = outputPathOrFlag
    await downloadVideoToFile(result.video_urls[0].video_url, downloadPath)
  }
  
  if (downloadPath) {
    return { result, download_path: downloadPath }
  }
  return { result }
}

async function main() {
  const args = process.argv.slice(2)
  
  if (args.length < 1) {
    console.error('用法:')
    console.error('  仅解析: node parse-douyin-video.js <抖音URL>')
    console.error('  下载到临时目录: node parse-douyin-video.js <抖音URL> --download')
    console.error('  下载到指定路径: node parse-douyin-video.js <抖音URL> <输出文件路径>')
    process.exit(1)
  }

  const url = args[0]
  
  // 解析参数模式
  let mode = 'parse'  // parse, download
  let outputPath = null
  
  if (args.length >= 2) {
    if (args[1] === '--download') {
      mode = 'download'
    } else {
      // 认为是输出文件路径
      mode = 'download'
      outputPath = args[1]
    }
  }

  try {
    let output
    
    if (mode === 'download') {
      // 下载模式
      const downloadFlag = outputPath || '--download'
      const { result, download_path } = await parseAndDownload(url, downloadFlag)
      output = { ...result }
      if (download_path) {
        output.download_path = download_path
        console.error('已下载到:', download_path)
      }
    } else {
      // 仅解析
      const { result } = await parseAndDownload(url, null)
      output = result
    }
    const analysis = buildAnalysis({
      title: output.title || '',
      text: output.desc || '',
      platform: '抖音',
      mediaType: '视频',
      visual: output.download_path ? `视频已下载到 ${output.download_path}` : '已解析视频链接',
      maxChars: 100,
    })
    output.content_analysis = analysis.analysis
    output.analysis_score = analysis.score
    output.analysis_evidence = analysis.evidence
    
    console.log(JSON.stringify(output, null, 2))
  } catch (err) {
    const msg = err instanceof Error ? err.message : String(err)
    console.error('失败:', msg)
    process.exit(1)
  }
}

const isDirectRun =
  typeof process !== 'undefined' &&
  process.argv[1]?.includes('parse-douyin-video')
if (isDirectRun) {
  main()
}

module.exports = {
  parseDouyinVideoUrl,
  downloadVideoToFile,
  parseAndDownload,
  createTempFilePath,
}
