// Style Mimic - Learn writing style from reference URL
// Usage: node style-mimic.js https://example.com/article

const { execSync } = require('child');

async function fetchAndExtract(url) {
    // Use web-fetch to get content
    try {
        const content = execSync(`node -e "
            const { webFetch } = require('openclaw');
            webFetch('${url}', { extractMode: 'markdown' }).then(result => {
                console.log(JSON.stringify(result));
            });
        "`, { encoding: 'utf8', maxBuffer: 1024 * 1024 * 2 });
        
        return JSON.parse(content);
    } catch (e) {
        console.error('Failed to fetch URL:', e.message);
        return null;
    }
}

function analyzeStyle(content) {
    const lines = content.split('\n');
    const avgLineLength = lines.reduce((sum, l) => sum + l.length, 0) / lines.length;
    const emojiCount = (content.match(/[\p{Emoji}]/gu) || []).length;
    const hasShortParagraphs = lines.filter(l => l.length < 30).length / lines.length > 0.3;
    const hasNumberedLists = (content.match(/^\d+\. /gm) || []).length > 0;
    const hasBulletLists = (content.match(/^- /gm) || []).length > 0;
    
    return {
        avgLineLength,
        emojiDensity: emojiCount / content.length * 1000,
        prefersShortParagraphs: hasShortParagraphs,
        usesNumberedLists: hasNumberedLists,
        usesBulletLists: hasBulletLists
    };
}

function generateStyleGuidelines(analysis) {
    let guidelines = '## 参考文章风格分析\n\n';
    
    if (analysis.avgLineLength < 40) {
        guidelines += '- 短句为主，平均每行不到 40 字符\n';
    } else if (analysis.avgLineLength < 60) {
        guidelines += '- 中等句子长度\n';
    } else {
        guidelines += '- 可以使用较长句子\n';
    }
    
    if (analysis.emojiDensity > 2) {
        guidelines += '- 多用 emoji 点缀，风格活泼\n';
    } else if (analysis.emojiDensity > 0.5) {
        guidelines += '- 适当使用 emoji\n';
    } else {
        guidelines += '- 很少使用 emoji，风格正式\n';
    }
    
    if (analysis.prefersShortParagraphs) {
        guidelines += '- 短段落，多换行，呼吸感强\n';
    }
    
    if (analysis.usesBulletLists) {
        guidelines += '- 常用无序列表 (- ) 整理要点\n';
    }
    
    if (analysis.usesNumberedLists) {
        guidelines += '- 常用有序列表 (1. ) 排列步骤\n';
    }
    
    return guidelines;
}

module.exports = {
    fetchAndExtract,
    analyzeStyle,
    generateStyleGuidelines
};

// Run directly
if (require.main === module) {
    const url = process.argv[2];
    if (!url) {
        console.error('Usage: node style-mimic.js <url>');
        process.exit(1);
    }
    
    fetchAndExtract(url).then(result => {
        if (!result) {
            console.log(JSON.stringify({ error: 'fetch failed' }));
            return;
        }
        const analysis = analyzeStyle(result);
        const guidelines = generateStyleGuidelines(analysis);
        console.log(JSON.stringify({ analysis, guidelines, content: result }));
    });
}
