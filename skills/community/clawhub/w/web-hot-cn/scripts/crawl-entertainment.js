#!/usr/bin/env node
// 影视/游戏爬虫 - 支持猫眼票房、App Store 排行
// 用法: node crawl-entertainment.js [--type=movie|tv|web|variety|game_free|game_paid|app_free|app_paid|all]

const UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
const HEADERS = { 'User-Agent': UA, 'Referer': 'https://piaofang.maoyan.com/' }

function clean(str) {
    return (str || '').replace(/'/g, '').replace(/\\/g, '')
}

// 猫眼电影票房
async function crawlMovie() {
    const ts = Math.floor(Date.now() / 1000)
    const url = `https://piaofang.maoyan.com/dashboard-ajax/movie?orderType=0&timeStamp=${ts}&channelId=40009&sVersion=2`
    const res = await fetch(url, { headers: HEADERS })
    const json = await res.json()
    return (json?.movieList?.list || []).map(i => ({
        syts: clean(i?.movieInfo?.releaseInfo || ''),
        pfzb: clean(i?.splitBoxRate || ''),
        name: clean(i?.movieInfo?.movieName || ''),
        piaofang: i?.sumBoxDesc || ''
    }))
}

// 猫眼电视剧
async function crawlTV() {
    const ts = Math.floor(Date.now() / 1000)
    const url = `https://piaofang.maoyan.com/dashboard-ajax?orderType=0&timeStamp=${ts}&channelId=40009&sVersion=2`
    const res = await fetch(url, { headers: HEADERS })
    const json = await res.json()
    return (json?.tvList?.data?.list || []).map(i => ({
        pfzb: clean(i?.channelName || ''),
        name: clean(i?.programmeName || ''),
        piaofang: i?.marketRateDesc || ''
    }))
}

// 猫眼网播
async function crawlWeb() {
    const ts = Math.floor(Date.now() / 1000)
    const url = `https://piaofang.maoyan.com/dashboard-ajax?orderType=0&timeStamp=${ts}&channelId=40009&sVersion=2`
    const res = await fetch(url, { headers: HEADERS })
    const json = await res.json()
    return (json?.webList?.data?.list || []).map(i => ({
        pfzb: clean(i?.seriesInfo?.platformDesc || ''),
        name: clean(i?.seriesInfo?.name || ''),
        piaofang: i?.currHeatDesc || ''
    }))
}

// 猫眼综艺
async function crawlVariety() {
    const ts = Math.floor(Date.now() / 1000)
    const today = new Date().toISOString().substring(0, 10).replace(/-/g, '')
    const url = `https://piaofang.maoyan.com/dashboard/webHeatData?showDate=${today}&seriesType=2&timeStamp=${ts}&channelId=40009&sVersion=2`
    const res = await fetch(url, { headers: HEADERS })
    const json = await res.json()
    return (json?.dataList?.list || []).map(i => ({
        pfzb: clean(i?.seriesInfo?.platformDesc || ''),
        name: clean(i?.seriesInfo?.name || ''),
        piaofang: i?.currHeat || ''
    }))
}

// Apple Store 榜单
async function crawlAppStore(chart, genreId) {
    const url = `https://apps.apple.com/cn/iphone/charts/${genreId}?chart=${chart}`
    const res = await fetch(url, {
        headers: { 'User-Agent': UA, 'Accept-Language': 'zh-CN,zh;q=0.9' }
    })
    const text = await res.text()
    const s = '<script type="application/json" id="serialized-server-data">'
    const si = text.indexOf(s)
    if (si === -1) return []
    const ei = text.indexOf('</script>', si + s.length)
    if (ei === -1) return []
    const json = JSON.parse(text.substring(si + s.length, ei))
    const items = json?.data?.[0]?.data?.segments?.[0]?.shelves?.[0]?.items || []
    return items.map(i => {
        const iconUrl = i?.icon?.template || ''
        return {
            img: iconUrl ? iconUrl.replace('{w}x{h}{c}.{f}', '320x0w.webp') : '',
            url: 'https://apps.apple.com/cn/app/' + encodeURIComponent(i?.title || '') + '/id' + (i?.adamId || ''),
            name: i?.title || '',
            pingfen: String(i?.rating || 0) + '⭐'
        }
    })
}

const CRAWLERS = {
    movie: { fn: () => crawlMovie(), label: '电影票房' },
    tv: { fn: () => crawlTV(), label: '电视剧收视' },
    web: { fn: () => crawlWeb(), label: '网播热度' },
    variety: { fn: () => crawlVariety(), label: '综艺热度' },
    game_free: { fn: () => crawlAppStore('top-free', '6014'), label: 'App Store 免费游戏' },
    game_paid: { fn: () => crawlAppStore('top-paid', '6014'), label: 'App Store 付费游戏' },
    app_free: { fn: () => crawlAppStore('top-free', '36'), label: 'App Store 免费应用' },
    app_paid: { fn: () => crawlAppStore('top-paid', '36'), label: 'App Store 付费应用' }
}

async function main() {
    const args = process.argv.slice(2)
    let type = 'all'
    for (const arg of args) {
        if (arg.startsWith('--type=')) type = arg.split('=')[1]
    }

    const targets = type === 'all' ? Object.keys(CRAWLERS) : [type]
    const now = new Date().toISOString().replace('T', ' ').substring(0, 19)
    const results = {}

    for (const name of targets) {
        const crawler = CRAWLERS[name]
        if (!crawler) { results[name] = { success: false, error: '不支持的类型: ' + name }; continue }
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
