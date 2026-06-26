#!/usr/bin/env node
// 人民日报电子版爬虫 - 获取每日报纸 PDF 下载地址
// 用法:
//   node crawl-paper.js                    # 今日报纸
//   node crawl-paper.js --date=2026-03-11  # 指定日期
//   node crawl-paper.js --date=yesterday   # 昨日报纸
//   node crawl-paper.js --pages=1,2,3      # 只获取指定版面

const UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'

function formatDate(date) {
    const y = date.getFullYear()
    const m = String(date.getMonth() + 1).padStart(2, '0')
    const d = String(date.getDate()).padStart(2, '0')
    return { full: `${y}-${m}-${d}`, path: `${y}${m}/${d}` }
}

function parseDate(str) {
    const now = new Date()
    // 转换为北京时间
    const utc = now.getTime() + now.getTimezoneOffset() * 60000
    const beijing = new Date(utc + 8 * 3600000)

    if (!str || str === 'today') return beijing
    if (str === 'yesterday') {
        beijing.setDate(beijing.getDate() - 1)
        return beijing
    }
    // 支持 YYYY-MM-DD 格式
    const parts = str.split('-')
    if (parts.length === 3) {
        return new Date(parseInt(parts[0]), parseInt(parts[1]) - 1, parseInt(parts[2]))
    }
    return beijing
}

// 从 node_01.html 获取当日所有版面列表
async function fetchPageList(datePath) {
    const url = `https://paper.people.com.cn/rmrb/pc/layout/${datePath}/node_01.html`
    const res = await fetch(url, { headers: { 'User-Agent': UA } })
    if (!res.ok) return []
    const html = await res.text()

    // 匹配所有版面链接: [01版：要闻](url) 或 node_XX.html
    const pages = []
    const regex = /node_(\d+)\.html[^"]*"[^>]*>(\d+版[：:][^<]*)</g
    let match
    while ((match = regex.exec(html)) !== null) {
        const pageNum = parseInt(match[1])
        const title = match[2].trim()
        if (!pages.find(p => p.page === pageNum)) {
            pages.push({ page: pageNum, title })
        }
    }

    // 备选：如果上面没匹配到，用更宽松的正则
    if (pages.length === 0) {
        const regex2 = /node_(\d+)\.html/g
        const seen = new Set()
        while ((match = regex2.exec(html)) !== null) {
            const num = parseInt(match[1])
            if (!seen.has(num)) {
                seen.add(num)
                pages.push({ page: num, title: `第${String(num).padStart(2, '0')}版` })
            }
        }
    }

    // 再从页面提取版面标题（更可靠的方式）
    const titleRegex = /(\d+)版[：:]([^<\]"]+)/g
    const titleMap = {}
    while ((match = titleRegex.exec(html)) !== null) {
        titleMap[parseInt(match[1])] = `${match[1].padStart(2, '0')}版：${match[2].trim()}`
    }
    for (const p of pages) {
        if (titleMap[p.page]) p.title = titleMap[p.page]
    }

    return pages.sort((a, b) => a.page - b.page)
}

// 从单个版面页面提取 PDF 下载链接
async function fetchPdfUrl(datePath, pageNum) {
    const nodeId = String(pageNum).padStart(2, '0')
    const url = `https://paper.people.com.cn/rmrb/pc/layout/${datePath}/node_${nodeId}.html`
    const res = await fetch(url, { headers: { 'User-Agent': UA } })
    if (!res.ok) return null
    const html = await res.text()

    const result = { url: null, fileName: null, imageUrl: null }

    // 匹配 PDF 下载链接
    // 格式1: href="../../../attachement/YYYYMM/DD/xxx.pdf"
    // 格式2: href="https://paper.people.com.cn/rmrb/pc/attachement/xxx.pdf"
    const pdfMatch = html.match(/href="([^"]*\.pdf)"[^>]*download="([^"]*)"/)
    if (pdfMatch) {
        let pdfUrl = pdfMatch[1]
        const fileName = pdfMatch[2]
        // 将相对路径转为绝对路径
        if (pdfUrl.startsWith('../../../')) {
            pdfUrl = `https://paper.people.com.cn/rmrb/pc/${pdfUrl.replace('../../../', '')}`
        } else if (!pdfUrl.startsWith('http')) {
            pdfUrl = `https://paper.people.com.cn/rmrb/pc/attachement/${pdfUrl}`
        }
        result.url = pdfUrl
        result.fileName = fileName
    } else {
        // 备选：直接匹配 attachement 路径
        const altMatch = html.match(/attachement\/[^"'\s]*\.pdf/)
        if (altMatch) {
            result.url = `https://paper.people.com.cn/rmrb/pc/${altMatch[0]}`
            result.fileName = `rmrb${datePath.replace('/', '')}${nodeId}.pdf`
        }
    }

    // 匹配版面高清图片 (新增: 解决 PDF 转图片的需求，直接返回高清大图)
    // 格式: src="../../../pic/202603/12/xxx.jpg.2"
    const imgMatch = html.match(/src="([^"]*\.jpg)(?:\.\d+)?"/)
    if (imgMatch) {
        let imgUrl = imgMatch[1]
        if (imgUrl.startsWith('../../../')) {
            imgUrl = `https://paper.people.com.cn/rmrb/pc/${imgUrl.replace('../../../', '')}`
        } else if (!imgUrl.startsWith('http')) {
            imgUrl = `https://paper.people.com.cn/rmrb/pc/pic/${imgUrl}`
        }
        result.imageUrl = imgUrl
    }

    return result
}

async function main() {
    const args = process.argv.slice(2)
    let dateStr = 'today'
    let filterPages = null

    for (const arg of args) {
        if (arg.startsWith('--date=')) dateStr = arg.split('=')[1]
        if (arg.startsWith('--pages=')) filterPages = arg.split('=')[1].split(',').map(Number)
    }

    const date = parseDate(dateStr)
    const { full, path } = formatDate(date)

    // 获取版面列表
    const pageList = await fetchPageList(path)

    if (pageList.length === 0) {
        console.log(JSON.stringify({
            status: 'error',
            message: `未找到 ${full} 的人民日报数据，可能当天报纸尚未发布或日期不正确`
        }, null, 2))
        process.exit(1)
    }

    // 筛选版面
    const targetPages = filterPages
        ? pageList.filter(p => filterPages.includes(p.page))
        : pageList

    // 获取每个版面的 PDF 链接和图片链接
    const results = []
    for (const page of targetPages) {
        const pageData = await fetchPdfUrl(path, page.page)
        results.push({
            page: page.page,
            title: page.title,
            pdf_url: pageData?.url || null,
            file_name: pageData?.fileName || null,
            image_url: pageData?.imageUrl || null
        })
    }

    const output = {
        status: 'ok',
        date: full,
        paper: '人民日报',
        total_pages: pageList.length,
        fetched_pages: results.length,
        pages: results
    }

    console.log(JSON.stringify(output, null, 2))
}

main().catch(e => {
    console.error(JSON.stringify({ status: 'error', message: e.message }))
    process.exit(1)
})
