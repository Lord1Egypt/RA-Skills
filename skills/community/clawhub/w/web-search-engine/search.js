
// 搜索关键词
const keyword = process.argv?.[2] || '';
const engine = process.argv?.[3] || 'bing_web_pc';

const engines = {

    // 百度网页搜索PC
    baidu_web_pc: async (k) => {
        const url = 'https://www.baidu.com/s?ie=utf-8&rn=50&wd=' + k;
        const res = await fetch(url, {
            signal: AbortSignal.timeout(3000),
            headers: {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36 Edg/146.0.0.0',
                'Accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
                'Accept-Encoding': 'gzip, deflate, br, zstd',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'sec-ch-ua': '"Chromium";v="146", "Not-A.Brand";v="24", "Microsoft Edge";v="146"',
                'referer': 'https://www.baidu.com/'
            }
        });
        const html = await res.text();
        
        const r_listItem = /c-container xpath-log new-pmd"([.\S\s]*?)<!--\/s-frag--><\/span><\/div>/g;
        const m_listItem = html.match(r_listItem);

        const data = [];
        if (m_listItem){
            for (let i = 0; i < m_listItem.length; i++) {
                let v = m_listItem[i];
                v = `<div class="${v}`.replace(/<!--[\s\S]*?-->/g, '')
                    .replace(/<[^>]+>/g, '')
                    .replace(/\s/g, ' ')
                    .replace(/[ ]+/g, ' ')
                    .trim();
                data.push(v);
            }
        }

        return data.join('\n\n---\n\n');
    },

    // 360网页搜索 PC
    so_web_pc: async (k) => {
        const url = 'https://www.so.com/s?src=360sou_newhome&q=' + k;
        const res = await fetch(url, {
            signal: AbortSignal.timeout(3000),
            headers: {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36 Edg/146.0.0.0',
                'Accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
                'Accept-Encoding': 'gzip, deflate, br, zstd',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'sec-ch-ua': '"Chromium";v="146", "Not-A.Brand";v="24", "Microsoft Edge";v="146"',
                'referer': 'https://www.so.com/'
            }
        });
        const html = await res.text();
        
        const r_listItem = /<li class="res-list"><h3 ([.\S\s]*?res-desc[.\S\s]*?)<\/li>/g;
        const m_listItem = html.match(r_listItem);

        const data = [];
        if (m_listItem){
            for (let i = 0; i < m_listItem.length; i++) {
                let v = m_listItem[i];
                v = v
                    .replace(/<!--[\s\S]*?-->/g, '')
                    .replace(/<style[\s\S]*?<\/style>/gi, '')
                    .replace(/<script[\s\S]*?<\/script>/gi, '')
                    .replace(/<[^>]+>/g, '')
                    .replace(/\s/g, '\n')
                    .replace(/[\n]+/g, '\n')
                    .trim();
                data.push(v);
            }
        }
        
        return data.join('\n\n---\n\n');
    },

    // bing网页搜索 PC
    bing_web_pc: async (k) => {
        const url = 'https://www.bing.com/search?q=' + k;
        const res = await fetch(url, {
            signal: AbortSignal.timeout(3000),
            headers: {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36 Edg/146.0.0.0',
                'Accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
                'Accept-Encoding': 'gzip, deflate, br, zstd',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'sec-ch-ua': '"Chromium";v="146", "Not-A.Brand";v="24", "Microsoft Edge";v="146"',
                'referer': 'https://www.bing.com/'
            }
        });
        const html = await res.text();
        
        const r_listItem = /<li class="b_algo"([.\S\s]*?<p class="b_lineclamp2">[.\S\s]*?)<\/li>/g;
        const m_listItem = html.match(r_listItem);

        const data = [];
        if (m_listItem){
            for (let i = 0; i < m_listItem.length; i++) {
                let v = m_listItem[i];
                v = v
                    .replace(/<cite[\s\S]*?<\/cite>/gi, '')
                    .replace(/<!--[\s\S]*?-->/g, '')
                    .replace(/<style[\s\S]*?<\/style>/gi, '')
                    .replace(/<script[\s\S]*?<\/script>/gi, '')
                    .replace(/<[^>]+>/g, '')
                    .replace(/\s/g, ' ')
                    .replace(/[\n]+/g, '\n')
                    .trim();
                data.push(v);
            }
        }
        
        return data.join('\n\n---\n\n');
    },

    // sogou网页搜索 PC
    sogou_web_pc: async (k) => {
        const url = 'https://www.sogou.com/web?query=' + k;
        const res = await fetch(url, {
            signal: AbortSignal.timeout(3000),
            headers: {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36 Edg/146.0.0.0',
                'Accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
                'Accept-Encoding': 'gzip, deflate, br, zstd',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'sec-ch-ua': '"Chromium";v="146", "Not-A.Brand";v="24", "Microsoft Edge";v="146"',
                'referer': 'https://www.sogou.com/'
            }
        });
        const html = await res.text();
        
        const r_listItem = /<div class="vrwrap" ([.\S\s]*?text-layout[.\S\s]*?)class="citeLinkClass/g;
        const m_listItem = html.match(r_listItem);

        const data = [];
        if (m_listItem){
            for (let i = 0; i < m_listItem.length; i++) {
                let v = m_listItem[i];
                v = `${v}">`
                    .replace(/<cite[\s\S]*?<\/cite>/gi, '')
                    .replace(/<!--[\s\S]*?-->/g, '')
                    .replace(/<style[\s\S]*?<\/style>/gi, '')
                    .replace(/<script[\s\S]*?<\/script>/gi, '')
                    .replace(/<[^>]+>/g, '')
                    .replace(/\s/g, ' ')
                    .replace(/[\n]+/g, '\n')
                    .trim();
                data.push(v);
            }
        }
        
        return data.join('\n\n---\n\n');
    },
}

if (keyword){
    const awaits = engine.split(',').filter(e => e && engines?.[e]).map(e => engines[e](keyword));
    const result = await Promise.all(awaits);
    console.log(JSON.stringify(result));
}else{
    console.error('没有搜索关键词');
}