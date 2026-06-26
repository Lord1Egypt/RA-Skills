#!/usr/bin/env node
/**
 * 微博图片/视频下载脚本
 * 支持：视频下载、单图/多图图集下载
 * 
 * 用法：
 *   node parse-weibo.js <微博URL> [输出目录]
 * 
 * 示例：
 *   node parse-weibo.js https://weibo.com/7976115583/QwgTm2OVI ./weibo-download
 */

const https = require('https');
const fs = require('fs');
const path = require('path');
const { buildAnalysis } = require('./build-content-analysis');

// 解析命令行参数
const url = process.argv[2];
const outputDir = process.argv[3] || './weibo-download';

if (!url) {
    console.error('❌ 请提供微博 URL');
    console.error('用法：node parse-weibo.js <微博URL> [输出目录]');
    process.exit(1);
}

// 从 URL 提取微博 ID
function extractWeiboId(url) {
    // 支持格式：
    // https://weibo.com/xxxx/xxxxx
    // https://m.weibo.cn/status/xxxxx
    // https://weibo.com/xxxx/xxxxx?from=...
    
    const patterns = [
        /weibo\.com\/\d+\/([a-zA-Z0-9]+)/,  // PC端
        /m\.weibo\.cn\/status\/([a-zA-Z0-9]+)/,  // 移动端
        /weibo\.com\/\d+\/([a-zA-Z0-9]+)\?/  // 带参数
    ];
    
    for (const pattern of patterns) {
        const match = url.match(pattern);
        if (match) return match[1];
    }
    
    // 如果都不匹配，尝试从最后一段提取
    const parts = url.split('/');
    const lastPart = parts[parts.length - 1];
    if (lastPart && !lastPart.includes('?')) {
        return lastPart;
    }
    
    return null;
}

// 调用微博 API 获取数据
async function fetchWeiboData(weiboId) {
    const apiUrl = `https://m.weibo.cn/statuses/show?id=${weiboId}`;
    
    return new Promise((resolve, reject) => {
        const options = {
            headers: {
                'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15',
                'Referer': 'https://m.weibo.cn/',
                'X-Requested-With': 'XMLHttpRequest'
            }
        };
        
        https.get(apiUrl, options, (res) => {
            let data = '';
            res.on('data', chunk => data += chunk);
            res.on('end', () => {
                try {
                    const json = JSON.parse(data);
                    if (json.ok === 1) {
                        resolve(json.data);
                    } else {
                        reject(new Error(`API 返回错误: ${json.msg || '未知错误'}`));
                    }
                } catch (e) {
                    reject(new Error(`解析 JSON 失败: ${e.message}`));
                }
            });
        }).on('error', reject);
    });
}

// 下载文件（支持重定向）
async function downloadFile(url, filepath) {
    return new Promise((resolve, reject) => {
        const doDownload = (downloadUrl, callback) => {
            const protocol = downloadUrl.startsWith('https') ? https : require('http');
            protocol.get(downloadUrl, { 
                headers: { 
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
                    'Referer': 'https://m.weibo.cn/'
                } 
            }, (res) => {
                if (res.statusCode === 301 || res.statusCode === 302) {
                    // 跟随重定向
                    callback(res.headers.location);
                } else if (res.statusCode === 200) {
                    const file = fs.createWriteStream(filepath);
                    res.pipe(file);
                    file.on('finish', () => {
                        file.close();
                        resolve();
                    });
                    file.on('error', reject);
                } else {
                    reject(new Error(`HTTP ${res.statusCode}`));
                }
            }).on('error', reject);
        };
        
        doDownload(url, (redirectUrl) => {
            doDownload(redirectUrl, () => {
                // 已经处理过了
            });
        });
    });
}

// 主函数
async function main() {
    console.log('🔍 解析微博链接...');
    console.log(`   URL: ${url}`);
    
    const weiboId = extractWeiboId(url);
    if (!weiboId) {
        console.error('❌ 无法从 URL 提取微博 ID');
        process.exit(1);
    }
    console.log(`   微博 ID: ${weiboId}`);
    
    // 创建输出目录
    if (!fs.existsSync(outputDir)) {
        fs.mkdirSync(outputDir, { recursive: true });
    }
    
    console.log('\n📡 获取微博数据...');
    let data;
    try {
        data = await fetchWeiboData(weiboId);
    } catch (e) {
        console.error(`❌ 获取数据失败: ${e.message}`);
        process.exit(1);
    }
    
    // 提取基本信息
    const user = data.user?.screen_name || '未知用户';
    const text = data.text?.replace(/<[^>]+>/g, '') || '';
    const picNum = data.pic_num || 0;
    
    console.log(`   用户: ${user}`);
    console.log(`   内容: ${text.substring(0, 50)}${text.length > 50 ? '...' : ''}`);
    console.log(`   图片数量: ${picNum}`);
    
    // 判断类型并下载
    if (picNum > 0) {
        // 图集类型
        console.log('\n📷 下载图集...');
        
        const pics = data.pics || [];
        const results = [];
        
        for (let i = 0; i < pics.length; i++) {
            const pic = pics[i];
            const imgUrl = pic.large?.url || pic.url;
            const filename = path.join(outputDir, `image_${String(i + 1).padStart(2, '0')}.jpg`);
            
            try {
                await downloadFile(imgUrl, filename);
                const stats = fs.statSync(filename);
                console.log(`   ✅ [${i + 1}/${pics.length}] ${path.basename(filename)} (${(stats.size / 1024).toFixed(1)} KB)`);
                results.push({ index: i + 1, filename, size: stats.size, url: imgUrl });
            } catch (e) {
                console.log(`   ❌ [${i + 1}/${pics.length}] 下载失败: ${e.message}`);
            }
        }
        
        // 输出结果
        const analysis = buildAnalysis({
            title: '',
            text,
            platform: '微博',
            mediaType: '图片',
            visual: `共下载 ${results.length} 张图片`,
            maxChars: 100,
        });
        console.log('\n✅ 下载完成！');
        console.log(JSON.stringify({
            type: 'album',
            user,
            text,
            picNum,
            outputDir,
            images: results,
            content_analysis: analysis.analysis,
            analysis_score: analysis.score,
            analysis_evidence: analysis.evidence,
        }, null, 2));
        
    } else {
        // 可能是视频，提示使用 yt-dlp
        console.log('\n⚠️ 未检测到图片，可能是视频类型');
        console.log('   请使用 yt-dlp 下载视频：');
        console.log(`   yt-dlp -f best -o "${outputDir}/video.mp4" "${url}"`);
        
        const analysis = buildAnalysis({
            title: '',
            text,
            platform: '微博',
            mediaType: '视频',
            visual: '',
            maxChars: 100,
        });
        console.log(JSON.stringify({
            type: 'video',
            user,
            text,
            suggestion: '使用 yt-dlp 下载',
            command: `yt-dlp -f best -o "${outputDir}/video.mp4" "${url}"`,
            content_analysis: analysis.analysis,
            analysis_score: analysis.score,
            analysis_evidence: analysis.evidence,
        }, null, 2));
    }
}

main().catch(console.error);
