#!/usr/bin/env node
// 热搜爬虫 - 支持抖音、微博、百度、B站、快手
// 用法: node crawl-hot.js [--platform=douyin|weibo|baidu|bilibili|kuaishou|all]

const UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'

function clean(str) {
    return (str || '').replace(/'/g, '').replace(/\\/g, '')
}

// 抖音热搜
async function crawlDouyin() {
    const res = await fetch('https://www.iesdouyin.com/web/api/v2/hotsearch/billboard/word/?reflow_source=reflow_page', {
        headers: { 'User-Agent': UA }
    })
    const json = await res.json()
    return (json.word_list || []).map(i => ({
        url: 'https://douyin.com/root/search/' + (i.word || ''),
        label: i.label || '',
        word: i.word || '',
        hot_value: i.hot_value || ''
    }))
}

// 微博热搜
async function crawlWeibo() {
    const res = await fetch('https://api.weibo.cn/2/guest/search/hot/word?from=10DA093010&c=iphone', {
        headers: { 'User-Agent': UA }
    })
    const json = await res.json()
    return (json?.data || []).map(i => ({
        url: 'https://s.weibo.com/weibo?q=' + encodeURIComponent(i.word || ''),
        label: String(i.flag || ''),
        word: i.word || '',
        hot_value: i.num || '🔥'
    }))
}

// 百度热搜
async function crawlBaidu() {
    const res = await fetch('https://top.baidu.com/board?tab=realtime', {
        headers: { 'User-Agent': UA, 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8' }
    })
    const html = await res.text()
    const marker = '<!--s-data:'
    const si = html.indexOf(marker)
    if (si === -1) return []
    const ei = html.indexOf('-->', si + marker.length)
    if (ei === -1) return []
    const json = JSON.parse(html.substring(si + marker.length, ei))
    const list = json?.data?.cards?.[0]?.content || []
    return list.filter(b => b.word).map(b => ({
        url: clean(b.url || b.rawUrl || ''),
        label: b.hotTag || '',
        word: (b.word || '').replace(/['"\\"\n]/g, ''),
        hot_value: b.hotScore || '',
        img: b.img || ''
    }))
}

// B站热搜
async function crawlBilibili() {
    const res = await fetch('https://app.bilibili.com/x/v2/search/trending/ranking?limit=50', {
        headers: { 'User-Agent': UA }
    })
    const json = await res.json()
    return ((json.data && json.data.list) || []).map(b => ({
        url: 'https://search.bilibili.com/all?keyword=' + encodeURIComponent(b.keyword || ''),
        label: b.position || '',
        word: b.keyword || '',
        hot_value: '🔥'
    }))
}

// 快手热搜
async function crawlKuaishou() {
    try {
        const res = await fetch('https://www.kuaishou.com/?isHome=1', {
            headers: { 'User-Agent': UA, 'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"' }
        })
        const text = await res.text()
        const start = '},"__typename":"VisionHotRankItem"},'
        const end = ',"clients":'
        const startIdx = text.indexOf(start)
        const endIdx = text.indexOf(end, startIdx)
        if (startIdx === -1 || endIdx === -1) return []
        const jsonStr = '{' + text.substring(startIdx + start.length, endIdx)
        const match = JSON.parse(jsonStr)
        const data = []
        for (const key of Object.keys(match)) {
            const b = match[key]
            const photoId = (b.photoIds && b.photoIds.json && b.photoIds.json[0]) || ''
            data.push({
                url: 'https://www.kuaishou.com/short-video/' + photoId + '?streamSource=hotrank&trendingId=' + (b.id || ''),
                label: b.rank || '',
                word: b.name || '',
                hot_value: b.hotValue || ''
            })
        }
        return data
    } catch {
        return []
    }
}

const CRAWLERS = {
    douyin: { fn: crawlDouyin, label: '抖音热搜' },
    weibo: { fn: crawlWeibo, label: '微博热搜' },
    baidu: { fn: crawlBaidu, label: '百度热搜' },
    bilibili: { fn: crawlBilibili, label: 'B站热搜' },
    kuaishou: { fn: crawlKuaishou, label: '快手热搜' }
}

async function main() {
    const args = process.argv.slice(2)
    let platform = 'all'
    for (const arg of args) {
        if (arg.startsWith('--platform=')) platform = arg.split('=')[1]
    }

    const targets = platform === 'all' ? Object.keys(CRAWLERS) : [platform]
    const now = new Date().toISOString().replace('T', ' ').substring(0, 19)
    const results = {}

    for (const name of targets) {
        const crawler = CRAWLERS[name]
        if (!crawler) {
            results[name] = { success: false, error: '不支持的平台: ' + name }
            continue
        }
        try {
            const data = await crawler.fn()
            results[name] = { success: true, label: crawler.label, data: { sj: data, time: now }, count: data.length }
        } catch (e) {
            results[name] = { success: false, error: e.message }
        }
    }

    console.log(JSON.stringify({ status: 'ok', results }, null, 2))
}

main().catch(e => {
    console.error(JSON.stringify({ status: 'error', message: e.message }))
    process.exit(1)
})
