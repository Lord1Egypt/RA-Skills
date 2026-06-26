#!/usr/bin/env node
// 音乐榜爬虫 - 支持QQ音乐、网易云、酷狗、酷我
// 用法: node crawl-music.js [--platform=qq|wangyi|kugou|kuwo|all] [--type=hot|rising|all]

const UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'

function clean(str) {
    return (str || '').replace(/'/g, '').replace(/\\/g, '')
}

// QQ音乐榜单
async function crawlQQ(type) {
    const idMap = { hot: 26, rising: 62 }
    const id = idMap[type] || 26
    const url = `https://i.y.qq.com/n2/m/share/details/toplist.html?ADTAG=ryqq.toplist&type=0&id=${id}`
    const res = await fetch(url, {
        headers: { 'User-Agent': UA, 'Referer': 'https://y.qq.com/' }
    })
    const html = await res.text()
    const data = []
    const items = html.match(/<li class="song_list__item"[\s\S]*?<\/li>/g) || []
    for (const item of items) {
        const nameMatch = item.match(/<span class="song_list__txt">([^<]*)<\/span>/)
        const descMatch = item.match(/<p class="song_list__desc">([^<]*)<\/p>/)
        const changeMatch = item.match(/<span class="song_list__index_change">[^<]*?(\S+)<\/span>/)
        if (nameMatch) {
            const desc = descMatch ? descMatch[1].trim() : ''
            let artist = desc
            if (desc.includes('·')) artist = desc.split('·')[0].trim()
            data.push({
                geshou: clean(artist),
                name: clean(nameMatch[1].trim()),
                hot: changeMatch ? clean(changeMatch[1]) : ''
            })
        }
    }
    return data
}

// 酷狗音乐榜单
async function crawlKugou(type) {
    const idMap = { hot: 8888, rising: 6666 }
    const id = idMap[type] || 8888
    const res = await fetch(`https://m.kugou.com/rank/info/${id}/`, {
        headers: { 'User-Agent': UA }
    })
    const html = await res.text()
    const data = []
    const items = html.match(/<a href="https:\/\/m\.kugou\.com\/mixsong\/[^"]*"[\s\S]*?<\/a>/g) || []
    let rank = 1
    for (const item of items) {
        const nameMatch = item.match(/class="song_name"[^>]*>([^<]*)</)
        const singerMatch = item.match(/class="singer_name"[^>]*>([^<]*)</)
        const urlMatch = item.match(/href="([^"]*)"/)
        if (nameMatch && singerMatch) {
            data.push({
                geshou: clean(singerMatch[1].trim()),
                name: clean(nameMatch[1].trim()),
                hot: String(rank),
                img: urlMatch ? clean(urlMatch[1]) : ''
            })
            rank++
        }
    }
    return data
}

// 酷我音乐榜单
async function crawlKuwo(type) {
    const idMap = { hot: 16, rising: 93 }
    const id = idMap[type] || 16
    const res = await fetch(`https://m.kuwo.cn/newh5app/ranklist_detail/${id}`, {
        headers: { 'User-Agent': UA }
    })
    const html = await res.text()
    const data = []
    const items = html.match(/<div class="singersMusicList"[\s\S]*?<\/div>\s*<\/div>\s*<\/div>/g) || []
    for (const item of items) {
        const rankMatch = item.match(/class="numberTop[^"]*"[^>]*>([^<]*)</)
        const titleMatch = item.match(/class="wordBody_title[^"]*"[^>]*>([^<]*)</)
        const smallMatch = item.match(/class="small[^"]*"[^>]*>([^<]*)</)
        if (titleMatch) {
            let singer = '', songName = titleMatch[1].trim()
            if (smallMatch) {
                const parts = smallMatch[1].split('-')
                singer = parts[0] ? parts[0].trim() : ''
                songName = parts[1] ? parts[1].trim() : songName
            }
            data.push({
                geshou: singer,
                name: songName,
                hot: rankMatch ? rankMatch[1].trim() : ''
            })
        }
    }
    return data
}

// 网易云音乐榜单
async function crawlWangyi(type) {
    const urlMap = {
        hot: 'https://music.163.com/discover/toplist?id=3778678',
        rising: 'https://music.163.com/discover/toplist'
    }
    const url = urlMap[type] || urlMap.rising
    const res = await fetch(url, {
        headers: { 'User-Agent': UA, 'Referer': 'https://music.163.com/', 'Accept-Encoding': 'gzip, deflate' }
    })
    const text = await res.text()
    const start = '<textarea id="song-list-pre-data" style="display:none;">'
    const end = '</textarea>'
    const startIdx = text.indexOf(start)
    if (startIdx === -1) return []
    const jsonStart = startIdx + start.length
    const endIdx = text.indexOf(end, jsonStart)
    if (endIdx === -1) return []
    const list = JSON.parse(text.substring(jsonStart, endIdx))
    const data = []
    let count = 0
    for (const i of list) {
        if (type === 'hot' && count >= 50) break
        data.push({
            geshou: ((i.artists && i.artists[0] && i.artists[0].name) || '').replace(/['"\\().]/g, ''),
            name: (i.name || '').replace(/['"\\():]/g, ''),
            hot: ((i.album && i.album.name) || '').replace(/['"\\().]/g, ''),
            img: ((i.album && i.album.picUrl) || '').replace(/['"\\]/g, '')
        })
        count++
    }
    return data
}

const PLATFORMS = {
    qq: { fn: crawlQQ, label: 'QQ音乐' },
    wangyi: { fn: crawlWangyi, label: '网易云音乐' },
    kugou: { fn: crawlKugou, label: '酷狗音乐' },
    kuwo: { fn: crawlKuwo, label: '酷我音乐' }
}

async function main() {
    const args = process.argv.slice(2)
    let platform = 'all'
    let type = 'all'
    for (const arg of args) {
        if (arg.startsWith('--platform=')) platform = arg.split('=')[1]
        if (arg.startsWith('--type=')) type = arg.split('=')[1]
    }

    const targets = platform === 'all' ? Object.keys(PLATFORMS) : [platform]
    const types = type === 'all' ? ['hot', 'rising'] : [type]
    const now = new Date().toISOString().replace('T', ' ').substring(0, 19)
    const results = {}

    for (const name of targets) {
        const p = PLATFORMS[name]
        if (!p) { results[name] = { success: false, error: '不支持的平台: ' + name }; continue }
        results[name] = {}
        for (const t of types) {
            try {
                const data = await p.fn(t)
                results[name][t] = { success: true, label: p.label + (t === 'hot' ? '热歌榜' : '飙升榜'), data: { sj: data, time: now }, count: data.length }
            } catch (e) {
                results[name][t] = { success: false, error: e.message }
            }
        }
    }

    console.log(JSON.stringify({ status: 'ok', results }, null, 2))
}

main().catch(e => {
    console.error(JSON.stringify({ status: 'error', message: e.message }))
    process.exit(1)
})
