/**
 * 抖音图集图片提取工具
 * 用法：node extract-douyin-images.js <抖音 URL> <输出目录>
 */

const { mkdirSync, writeFileSync } = require('fs')
const path = require('path')
const { buildAnalysis } = require('./build-content-analysis')

const DEFAULT_HEADERS = {
  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
  Referer: 'https://www.douyin.com/',
}

async function extractImages(url, outputDir) {
  const awemeId = url.match(/video\/([^/?]*)/)?.[1] || url.match(/note\/([^/?]*)/)?.[1]
  if (!awemeId) throw new Error('无法提取视频 ID')
  
  const requestUrl = `https://www.douyin.com/jingxuan?modal_id=${awemeId}`
  console.log(`正在获取：${requestUrl}`)
  
  const response = await fetch(requestUrl, { headers: DEFAULT_HEADERS })
  if (!response.ok) throw new Error(`请求失败：${response.status}`)
  
  const html = await response.text()
  
  // 提取 videoDetail JSON
  const pattern = /"([^"]*?(?:videoDetail)[^"]*?)"/g
  const matches = html.match(pattern)
  
  let images = []
  if (matches) {
    for (const m of matches) {
      try {
        const decoded = decodeURIComponent(m.slice(1, -1))
        const data = JSON.parse(decoded)
        const videoDetail = data?.app?.videoDetail
        if (videoDetail?.images) {
          images = videoDetail.images
          console.log(`找到 ${images.length} 张图片`)
          break
        }
      } catch (e) {}
    }
  }
  
  if (images.length === 0) {
    throw new Error('未找到图片数据')
  }
  
  // 创建输出目录
  mkdirSync(outputDir, { recursive: true })
  
  // 下载图片
  const downloadedImages = []
  for (let i = 0; i < images.length; i++) {
    const img = images[i]
    let imgUrl = img.urlList?.[0] || img.url_list?.[0] || img.download_addr?.url_list?.[0]
    
    if (!imgUrl) {
      console.log(`跳过图片 ${i + 1}：无法获取 URL`)
      continue
    }
    
    console.log(`下载图片 ${i + 1}/${images.length}...`)
    
    try {
      const imgResponse = await fetch(imgUrl, { headers: DEFAULT_HEADERS })
      if (!imgResponse.ok) {
        console.log(`图片 ${i + 1} 下载失败：${imgResponse.status}`)
        continue
      }
      
      const buffer = Buffer.from(await imgResponse.arrayBuffer())
      const ext = imgUrl.match(/\.(\w+)(?:\?|$)/)?.[1] || 'jpg'
      const filename = `image-${String(i + 1).padStart(2, '0')}.${ext}`
      const filepath = path.join(outputDir, filename)
      
      writeFileSync(filepath, buffer)
      downloadedImages.push({ index: i + 1, path: filepath, url: imgUrl })
      console.log(`✅ 已保存：${filename} (${img.width}x${img.height})`)
    } catch (e) {
      console.log(`图片 ${i + 1} 下载错误：${e.message}`)
    }
  }
  
  return {
    total: images.length,
    downloaded: downloadedImages.length,
    images: downloadedImages,
    outputDir,
  }
}

// 主程序
(async () => {
  const url = process.argv[2]
  const outputDir = process.argv[3] || './douyin-images'
  
  if (!url) {
    console.log('用法：node extract-douyin-images.js <抖音 URL> [输出目录]')
    process.exit(1)
  }
  
  console.log(`开始提取抖音图集：${url}`)
  console.log(`输出目录：${outputDir}`)
  console.log('---')
  
  try {
    const result = await extractImages(url, outputDir)
    console.log('---')
    console.log(`完成！共 ${result.total} 张图片，成功下载 ${result.downloaded} 张`)
    console.log(`保存位置：${result.outputDir}`)
    
    if (result.images.length > 0) {
      console.log('\n图片列表:')
      result.images.forEach(img => {
        console.log(`  ${img.index}. ${path.basename(img.path)}`)
      })
    }
    const analysis = buildAnalysis({
      title: '',
      text: '',
      platform: '抖音',
      mediaType: '图片',
      visual: `图集共 ${result.total} 张，成功下载 ${result.downloaded} 张`,
      maxChars: 100,
    })
    console.log('\n---')
    console.log(JSON.stringify({
      type: 'album',
      total_images: result.total,
      downloaded_images: result.downloaded,
      output_dir: result.outputDir,
      content_analysis: analysis.analysis,
      analysis_score: analysis.score,
      analysis_evidence: analysis.evidence,
    }, null, 2))
  } catch (e) {
    console.error(`错误：${e.message}`)
    process.exit(1)
  }
})()
