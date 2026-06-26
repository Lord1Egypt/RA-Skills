#!/usr/bin/env node
/**
 * 百科虾搜索脚本 - BM25 + 简单中文分词
 * 使用 N-gram + 常用词字典实现中文分词
 * 支持索引缓存：content.json 未变化时复用缓存
 */

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

// 查找 workspace
function findWorkspaceDir(startDir) {
    let dir = startDir;
    for (let i = 0; i < 5; i++) {
        const cacheDir = path.join(dir, 'cache');
        if (fs.existsSync(cacheDir)) {
            return dir;
        }
        dir = path.join(dir, '..');
    }
    return null;
}

const WORKSPACE_DIR = findWorkspaceDir(__dirname);
if (!WORKSPACE_DIR) {
    console.error('错误：找不到 agent workspace');
    process.exit(1);
}

const CONTENT_FILE = path.join(WORKSPACE_DIR, 'cache', 'content.json');
const SEARCH_CACHE_FILE = path.join(WORKSPACE_DIR, 'cache', 'search_cache.json');

// 计算文件 MD5
function md5File(filePath) {
    const content = fs.readFileSync(filePath, 'utf8');
    return crypto.createHash('md5').update(content).digest('hex');
}

// ==========================================
// 简单中文分词器
// ==========================================

// 常用中文词组字典（扩大匹配范围）
const DICT = new Set([
    '采购', '办公', '用品', '财务', '门禁', '打卡', '考勤', '绩效', '工资', '社保',
    '公积金', '团建', '入职', '离职', '转正', '报销', '发票', '合同', '辞职', '实习',
    '请假', '年假', '病假', '加班', '调休', '离职手续', '入职手续', '办公用品',
    '生活用品', '固定资产', '电子产品', '会议室', '预定', '无线网', '账号', '密码',
    'hrbp', 'hr', '行政', '人事', '组织发展', '财务资产', '供应链', '亚马逊运营',
    '见运营', '考核', '薪酬', '奖金', '福利', '商业保险', '园区', '门禁卡', '考勤卡'
]);

function tokenize(text) {
    if (!text) return [];
    
    const tokens = [];
    
    // 匹配中文词组
    const chinesePattern = /[\u4e00-\u9fa5]{2,}/g;
    let match;
    
    while ((match = chinesePattern.exec(text)) !== null) {
        const word = match[0];
        
        // 尝试最长匹配
        let matched = false;
        for (let len = Math.min(word.length, 6); len >= 2; len--) {
            for (let i = 0; i <= word.length - len; i++) {
                const sub = word.substring(i, i + len);
                if (DICT.has(sub)) {
                    tokens.push(sub);
                    i += len - 1; // 跳过已匹配的
                    matched = true;
                    break;
                }
            }
            if (matched) break;
        }
        
        // 如果没有匹配到词典词，按 2-gram 分词
        if (!matched) {
            for (let i = 0; i < word.length - 1; i++) {
                tokens.push(word.substring(i, i + 2));
            }
        }
    }
    
    // 匹配英文和数字
    const englishPattern = /[a-zA-Z0-9_]{2,}/g;
    while ((match = englishPattern.exec(text)) !== null) {
        tokens.push(match[0].toLowerCase());
    }
    
    return tokens.filter(t => t && t.length >= 2);
}

// ==========================================
// BM25 实现
// ==========================================

class BM25 {
    constructor(k1 = 1.5, b = 0.75) {
        this.k1 = k1;
        this.b = b;
        this.documents = [];
        this.termDocFreq = new Map();
        this.docLengths = [];
        this.avgDocLength = 0;
        this.N = 0;
    }

    addDocument(id, title, content, rawLine) {
        const tokens = tokenize(content);
        const titleTokens = tokenize(title);
        const allTokens = [...titleTokens, ...tokens];
        
        this.documents.push({ id, title, content, rawLine, tokens: allTokens });
        this.docLengths.push(allTokens.length);
        
        const uniqueTokens = new Set(allTokens);
        for (const term of uniqueTokens) {
            this.termDocFreq.set(term, (this.termDocFreq.get(term) || 0) + 1);
        }
    }

    build() {
        this.N = this.documents.length;
        const totalLen = this.docLengths.reduce((a, b) => a + b, 0);
        this.avgDocLength = totalLen / (this.N || 1);
    }

    termBM25(term, docIndex) {
        const df = this.termDocFreq.get(term) || 0;
        if (df === 0) return 0;
        
        const idf = Math.log((this.N - df + 0.5) / (df + 0.5) + 1);
        
        const doc = this.documents[docIndex];
        const tf = doc.tokens.filter(t => t === term).length;
        const docLen = this.docLengths[docIndex];
        
        const numerator = tf * (this.k1 + 1);
        const denominator = tf + this.k1 * (1 - this.b + this.b * docLen / this.avgDocLength);
        
        return idf * numerator / denominator;
    }

    score(queryTokens, docIndex) {
        let score = 0;
        for (const term of queryTokens) {
            score += this.termBM25(term, docIndex);
        }
        return score;
    }

    search(query, topK = 5) {
        const queryTokens = tokenize(query);
        if (queryTokens.length === 0) return [];
        
        const scores = [];
        for (let i = 0; i < this.documents.length; i++) {
            const s = this.score(queryTokens, i);
            if (s > 0) {
                scores.push({ index: i, score: s });
            }
        }
        
        scores.sort((a, b) => b.score - a.score);
        return scores.slice(0, topK).map(({ index, score }) => ({
            ...this.documents[index],
            score
        }));
    }

    toJSON() {
        return {
            documents: this.documents,
            termDocFreq: Array.from(this.termDocFreq.entries()),
            docLengths: this.docLengths,
            avgDocLength: this.avgDocLength,
            N: this.N
        };
    }
}

function loadIndexFromCache(bm25) {
    try {
        const cache = JSON.parse(fs.readFileSync(SEARCH_CACHE_FILE, 'utf8'));
        const currentHash = md5File(CONTENT_FILE);
        if (cache.contentHash !== currentHash) return false;
        
        bm25.documents = cache.documents;
        bm25.termDocFreq = new Map(cache.termDocFreq);
        bm25.docLengths = cache.docLengths;
        bm25.avgDocLength = cache.avgDocLength;
        bm25.N = cache.N;
        return true;
    } catch {
        return false;
    }
}

function saveIndexToCache(bm25) {
    try {
        const cache = {
            contentHash: md5File(CONTENT_FILE),
            builtAt: new Date().toISOString(),
            ...bm25.toJSON()
        };
        fs.writeFileSync(SEARCH_CACHE_FILE, JSON.stringify(cache), 'utf8');
    } catch (e) {
        // 缓存写入失败不影响主流程
    }
}

// 从 content.json 构建索引（带缓存）
function buildIndex() {
    if (!fs.existsSync(CONTENT_FILE)) {
        console.error('错误：找不到 content.json，请先同步知识库');
        process.exit(1);
    }

    // 尝试从缓存加载
    const bm25 = new BM25();
    if (loadIndexFromCache(bm25)) {
        return bm25;
    }

    // 缓存未命中，从头构建索引
    const content = fs.readFileSync(CONTENT_FILE, 'utf8');
    const lines = content.split('\n');
    
    for (let i = 0; i < lines.length; i++) {
        const line = lines[i].trim();
        if (!line || line.length < 4) continue;
        
        // 提取标题（= 之间）
        let title = '';
        let body = line;
        
        if (line.startsWith('=====')) {
            const endIdx = line.indexOf('=====', 4);
            if (endIdx > 4) {
                title = line.substring(4, endIdx).trim();
                body = line.substring(endIdx + 4).trim();
            }
        }
        
        bm25.addDocument(i, title, body, line);
    }
    
    bm25.build();
    
    // 保存缓存
    saveIndexToCache(bm25);
    
    return bm25;
}

// 提取 AT 标签上下文
function extractAtContext(line) {
    const atRegex = /<at user_id="([^"]+)">([^<]*)<\/at>/g;
    const results = [];
    let match;
    
    while ((match = atRegex.exec(line)) !== null) {
        results.push({
            userId: match[1],
            name: match[2] || match[1]
        });
    }
    
    return results;
}

async function main() {
    const args = process.argv.slice(2);
    if (args.length === 0) {
        console.error('用法: node search.js <关键词> [返回条数]');
        console.error('示例: node search.js 采购 3');
        process.exit(1);
    }

    const keyword = args[0];
    const topK = parseInt(args[1]) || 5;

    console.log(`正在构建搜索索引...`);
    const index = buildIndex();
    console.log(`索引构建完成，共 ${index.N} 个文档`);
    console.log('');

    const results = index.search(keyword, topK);

    if (results.length === 0) {
        console.log('未找到相关内容');
        return;
    }

    console.log(`找到 ${results.length} 个结果:\n`);
    
    // 输出结构化数据，方便程序解析
    const structured = [];
    
    for (const result of results) {
        const atTags = extractAtContext(result.rawLine);
        const hasMedia = result.rawLine.includes('MEDIA:');
        
        structured.push({
            index: structured.length + 1,
            score: result.score.toFixed(4),
            atTags: atTags,
            hasMedia: hasMedia,
            rawLine: result.rawLine
        });
    }
    
    // 打印结构化结果
    for (const r of structured) {
        console.log(`结果${r.index}【得分: ${r.score}】`);
        if (r.hasMedia) {
            console.log('  包含媒体文件');
            // 提取 MEDIA 行
            const mediaLines = r.rawLine.split('\n').filter(l => l.includes('MEDIA:'));
            for (const line of mediaLines) {
                console.log(`  ${line}`);
            }
        }
        if (r.atTags.length > 0) {
            for (const at of r.atTags) {
                console.log(`  AT: 『AT:${at.userId}』`);
            }
        }
        console.log(`  完整内容: ${r.rawLine}`);
        console.log('');
    }
}

main();
