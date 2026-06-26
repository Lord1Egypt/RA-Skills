const fs = require('fs');
const path = require('path');
const { spawnSync } = require('child_process');

const DEFAULT_AUTHOR = 'AI源来如此';
const DEFAULT_NEED_OPEN_COMMENT = '1';
const DEFAULT_ONLY_FANS_CAN_COMMENT = '1';
const DEFAULT_ASPECT_RATIO = '16:9';

function loadEnv() {
    try {
        const skillDir = path.resolve(__dirname, '..');
        const candidates = [
            path.resolve(skillDir, '.env'),
            path.resolve(process.cwd(), '.env'),
            path.resolve(skillDir, '..', '..', '..', '.env'),
        ];
        for (const envPath of candidates) {
            if (!fs.existsSync(envPath)) continue;
            const content = fs.readFileSync(envPath, 'utf8');
            content.split('\n').forEach((line) => {
                const match = line.match(/^\s*([\w.-]+)\s*=\s*(.*)?\s*$/);
                if (!match) return;
                const key = match[1];
                const value = (match[2] || '').trim().replace(/^['"]|['"]$/g, '');
                if (!process.env[key]) {
                    process.env[key] = value;
                }
            });
            break;
        }
    } catch (error) {
        // ignore env loading errors
    }
}

function parseArgs() {
    const argv = process.argv.slice(2);
    const parsed = {};
    for (let i = 0; i < argv.length; i++) {
        const token = argv[i];
        if (!token.startsWith('--')) continue;
        const key = token.slice(2);
        const next = argv[i + 1];
        if (!next || next.startsWith('--')) {
            parsed[key] = '1';
            continue;
        }
        parsed[key] = next;
        i += 1;
    }
    return parsed;
}

function stripMarkdown(markdown) {
    return markdown
        .replace(/```[\s\S]*?```/g, ' ')
        .replace(/`([^`]+)`/g, '$1')
        .replace(/!\[[^\]]*\]\([^)]*\)/g, ' ')
        .replace(/\[([^\]]+)\]\([^)]*\)/g, '$1')
        .replace(/^#{1,6}\s+/gm, '')
        .replace(/^>\s?/gm, '')
        .replace(/[*_~>-]/g, ' ')
        .replace(/\s+/g, ' ')
        .trim();
}

function stripHtml(html) {
    return html
        .replace(/<style[\s\S]*?<\/style>/gi, ' ')
        .replace(/<script[\s\S]*?<\/script>/gi, ' ')
        .replace(/<[^>]+>/g, ' ')
        .replace(/&nbsp;/g, ' ')
        .replace(/&amp;/g, '&')
        .replace(/\s+/g, ' ')
        .trim();
}

function parseArticleInput(content, filePath) {
    const ext = path.extname(filePath || '').toLowerCase();
    const isHtml = ext === '.html' || ext === '.htm' || /<html|<section|<p\b/i.test(content);
    let title = '';
    let plainText = '';

    if (isHtml) {
        const titleMatch = content.match(/<h1\b[^>]*>([\s\S]*?)<\/h1>/i) || content.match(/<title\b[^>]*>([\s\S]*?)<\/title>/i);
        title = titleMatch ? stripHtml(titleMatch[1]) : '';
        plainText = stripHtml(content);
    } else {
        const titleMatch = content.match(/^#\s+(.+)$/m);
        title = titleMatch ? titleMatch[1].trim() : '';
        plainText = stripMarkdown(content);
    }

    const text = plainText.trim();
    const digest = text.slice(0, 120).trim();
    return {
        title,
        digest,
        plainText: text,
        isHtml
    };
}

function buildCoverPrompt(article, options = {}) {
    const author = options.author || DEFAULT_AUTHOR;
    const title = article.title || '未命名文章';
    const summary = article.digest || article.plainText.slice(0, 100) || '生成适合公众号文章的封面图';
    return [
        '请生成一张微信公众号文章封面图。',
        `文章标题：${title}`,
        `作者署名：${author}`,
        `内容摘要：${summary}`,
        '风格要求：现代中文科技编辑风，简洁、可信、高级感，适合公众号首图。',
        '画面要求：16:9 横版，突出标题主题，可包含抽象科技元素与信息感背景。',
        '文字要求：仅保留少量高质量简体中文标题，不要英文乱码，不要水印，不要二维码。'
    ].join('\n');
}

function slugifyFileBase(articlePath) {
    const base = path.basename(articlePath, path.extname(articlePath));
    return base.replace(/[^a-zA-Z0-9\u4e00-\u9fa5_-]+/g, '-').replace(/-+/g, '-').replace(/^-|-$/g, '') || 'article';
}

function getDefaultCoverPath(articlePath) {
    const dir = path.dirname(path.resolve(articlePath));
    const base = slugifyFileBase(articlePath);
    return path.join(dir, `${base}-cover.png`);
}

function runCommand(command, args, options = {}) {
    const result = spawnSync(command, args, {
        cwd: options.cwd || process.cwd(),
        encoding: 'utf8',
        env: options.env || process.env,
        shell: false
    });

    if (result.error) {
        throw result.error;
    }
    if (result.status !== 0) {
        const stderr = (result.stderr || '').trim();
        const stdout = (result.stdout || '').trim();
        throw new Error(stderr || stdout || `${command} 执行失败`);
    }
    return result;
}

function extractMediaIdFromUploadOutput(output) {
    const trimmed = String(output || '').trim();
    if (!trimmed) {
        throw new Error('上传封面后未获得任何输出');
    }

    const lines = trimmed.split(/\r?\n/).map(line => line.trim()).filter(Boolean);
    for (let index = lines.length - 1; index >= 0; index -= 1) {
        const line = lines[index];
        if (line.startsWith('{') && line.endsWith('}')) {
            const parsed = JSON.parse(line);
            if (parsed && parsed.media_id) return parsed.media_id;
        }
    }

    const match = trimmed.match(/media_id:\s*([\w-]+)/);
    if (match) return match[1];
    throw new Error('无法从上传结果中解析 media_id');
}

function getImageGenScriptPath() {
    return path.resolve(__dirname, '..', '..', 'zhy-article-illustrator', 'scripts', 'image-gen.ts');
}

function ensureFileExists(filePath, label) {
    if (!fs.existsSync(filePath)) {
        throw new Error(`${label}不存在: ${filePath}`);
    }
}

function publishWithCover(args) {
    const articlePath = path.resolve(process.cwd(), args.article || args.file || '');
    const htmlPath = path.resolve(process.cwd(), args.html || args.file || '');
    const titleArg = args.title || '';
    const author = args.author || process.env.WECHAT_DEFAULT_AUTHOR || DEFAULT_AUTHOR;
    const needOpenComment = args['need-open-comment'] || DEFAULT_NEED_OPEN_COMMENT;
    const onlyFansCanComment = args['only-fans-can-comment'] || DEFAULT_ONLY_FANS_CAN_COMMENT;
    const coverPath = path.resolve(process.cwd(), args['cover-output'] || getDefaultCoverPath(articlePath));
    const aspectRatio = args['cover-ar'] || DEFAULT_ASPECT_RATIO;

    if (!args.article && !args.file) {
        throw new Error('必须提供 --article 或 --file');
    }

    ensureFileExists(articlePath, '文章文件');
    ensureFileExists(htmlPath, 'HTML 文件');

    const rawContent = fs.readFileSync(articlePath, 'utf8');
    const article = parseArticleInput(rawContent, articlePath);
    const title = titleArg || article.title;
    if (!title) {
        throw new Error('无法从文章中提取标题，请通过 --title 显式传入');
    }

    const prompt = buildCoverPrompt({ ...article, title }, { author });
    const imageGenScript = getImageGenScriptPath();
    ensureFileExists(imageGenScript, '封面生成脚本');

    console.log('1. 正在生成封面图...');
    const imageResult = runCommand('bun', [imageGenScript, '--prompt', prompt, '--output', coverPath, '--ar', aspectRatio], {
        cwd: path.dirname(imageGenScript)
    });
    if (imageResult.stdout.trim()) {
        console.log(imageResult.stdout.trim());
    }

    console.log('2. 正在上传封面图到微信素材库...');
    const uploadScript = path.resolve(__dirname, 'upload_image.js');
    const uploadResult = runCommand('node', [uploadScript, coverPath, '--json'], {
        cwd: process.cwd()
    });
    const thumbMediaId = extractMediaIdFromUploadOutput(uploadResult.stdout);
    console.log(`   封面 media_id: ${thumbMediaId}`);

    console.log('3. 正在上传公众号草稿...');
    const draftScript = path.resolve(__dirname, 'wechat_draft.js');
    const draftArgs = [
        draftScript,
        '--title', title,
        '--file', htmlPath,
        '--author', author,
        '--thumb', thumbMediaId,
        '--need-open-comment', needOpenComment,
        '--only-fans-can-comment', onlyFansCanComment
    ];

    if (article.digest) {
        draftArgs.push('--digest', article.digest);
    }
    if (args['source-url']) {
        draftArgs.push('--source-url', args['source-url']);
    }

    const draftResult = runCommand('node', draftArgs, {
        cwd: process.cwd()
    });
    if (draftResult.stdout.trim()) {
        console.log(draftResult.stdout.trim());
    }

    return {
        title,
        author,
        coverPath,
        thumbMediaId,
        digest: article.digest
    };
}

function main() {
    loadEnv();
    const args = parseArgs();

    if (!args.article && !args.file) {
        console.error('使用方法:');
        console.error('  node publish_with_cover.js --article "article.md" --html "post.html" [--title "标题"] [--author "作者"] [--source-url "原文链接"]');
        process.exit(1);
    }

    try {
        const result = publishWithCover(args);
        console.log('\n==============================');
        console.log('自动生成封面并推送草稿成功!');
        console.log(`标题: ${result.title}`);
        console.log(`author: ${result.author}`);
        console.log(`thumb_media_id: ${result.thumbMediaId}`);
        console.log(`cover: ${result.coverPath}`);
        console.log('==============================\n');
    } catch (error) {
        console.error('\n--- 发生错误 ---');
        console.error(error.message);
        process.exit(1);
    }
}

module.exports = {
    parseArgs,
    parseArticleInput,
    buildCoverPrompt,
    getDefaultCoverPath,
    extractMediaIdFromUploadOutput,
    publishWithCover,
    main
};

if (require.main === module) {
    main();
}
