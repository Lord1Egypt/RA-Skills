#!/usr/bin/env node
/**
 * URL图片提取并生成PDF
 * 用法: node extract.js <URL> [输出文件名]
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');
const https = require('https');
const http = require('http');

// 配置
const TEMP_DIR = '/tmp/url-images-to-pdf';

// 帮助函数：下载文件
function downloadFile(url, filename) {
    return new Promise((resolve, reject) => {
        const protocol = url.startsWith('https') ? https : http;
        
        protocol.get(url, (response) => {
            // 处理重定向
            if (response.statusCode >= 300 && response.statusCode < 400 && response.headers.location) {
                downloadFile(response.headers.location, filename).then(resolve).catch(reject);
                return;
            }
            
            const file = fs.createWriteStream(filename);
            response.pipe(file);
            file.on('finish', () => {
                file.close();
                resolve();
            });
        }).on('error', (err) => {
            reject(err);
        });
    });
}

// 主函数
async function main() {
    const url = process.argv[2];
    const outputName = process.argv[3] || 'output';
    
    if (!url) {
        console.log('用法: node extract.js <URL> [输出文件名]');
        process.exit(1);
    }
    
    console.log(`正在提取: ${url}`);
    
    // 创建临时目录
    if (!fs.existsSync(TEMP_DIR)) {
        fs.mkdirSync(TEMP_DIR, { recursive: true });
    }
    
    // 获取网页内容
    console.log('正在获取网页内容...');
    const html = execSync(`curl -sL -A "Mozilla/5.0" "${url}"`, { encoding: 'utf8' });
    
    // 提取图片URL - 保持原始顺序去重
    const imgRegex = /data-src="(https:\/\/mmbiz\.qpic\.cn[^"]+)"/g;
    const imgUrls = [];
    let match;
    
    while ((match = imgRegex.exec(html)) !== null) {
        const cleanUrl = match[1].replace(/\\&amp;/g, '&').replace(/\\"/g, '');
        // 保持顺序去重
        if (!imgUrls.includes(cleanUrl)) {
            imgUrls.push(cleanUrl);
        }
    }
    
    // 也尝试其他图片格式
    const otherRegex = /https:\/\/mmbiz\.[a-z]+\/[^"]+\.(jpg|jpeg|png)/g;
    while ((match = otherRegex.exec(html)) !== null) {
        const cleanUrl = match[0].replace(/\\&amp;/g, '&');
        if (!imgUrls.includes(cleanUrl)) {
            imgUrls.push(cleanUrl);
        }
    }
    
    console.log(`找到 ${imgUrls.length} 张图片`);
    
    if (imgUrls.length === 0) {
        console.log('未找到图片，尝试其他方式...');
        process.exit(1);
    }
    
    // 下载图片
    console.log('正在下载图片...');
    const downloadedFiles = [];
    
    for (let i = 0; i < Math.min(imgUrls.length, 50); i++) {
        const imgUrl = imgUrls[i];
        const ext = imgUrl.includes('.jpg') ? 'jpg' : 'png';
        const filename = path.join(TEMP_DIR, `img_${String(i+1).padStart(3, '0')}.${ext}`);
        
        try {
            console.log(`下载 ${i+1}/${imgUrls.length}: ${imgUrl.substring(0, 50)}...`);
            await downloadFile(imgUrl, filename);
            downloadedFiles.push(filename);
        } catch (err) {
            console.log(`下载失败: ${err.message}`);
        }
    }
    
    console.log(`成功下载 ${downloadedFiles.length} 张图片`);
    
    if (downloadedFiles.length === 0) {
        console.log('没有成功下载任何图片');
        process.exit(1);
    }
    
    // 生成PDF
    console.log('正在生成PDF...');
    
    try {
        const PDFDocument = require('pdfkit');
        const doc = new PDFDocument({ autoFirstPage: false });
        const outputPath = path.join(process.cwd(), `${outputName}.pdf`);
        const output = fs.createWriteStream(outputPath);
        
        doc.pipe(output);
        
        // 按序号排序文件
        downloadedFiles.sort();
        
        downloadedFiles.forEach((file, i) => {
            console.log(`添加页面 ${i+1}...`);
            doc.addPage({ size: 'A4' });
            
            try {
                const img = doc.openImage(file);
                const pageWidth = doc.page.width;
                const pageHeight = doc.page.height;
                const scale = Math.min(pageWidth / img.width, pageHeight / img.height) * 0.9;
                const scaledWidth = img.width * scale;
                const scaledHeight = img.height * scale;
                const x = (pageWidth - scaledWidth) / 2;
                const y = (pageHeight - scaledHeight) / 2;
                
                doc.image(file, x, y, { width: scaledWidth, height: scaledHeight });
            } catch (e) {
                console.log(`图片格式错误: ${e.message}`);
            }
        });
        
        doc.end();
        
        output.on('finish', () => {
            console.log(`PDF生成完成: ${outputPath}`);
            
            // 清理临时文件
            downloadedFiles.forEach(f => {
                try { fs.unlinkSync(f); } catch(e) {}
            });
        });
        
    } catch (e) {
        console.log(`PDF生成失败: ${e.message}`);
        console.log('请确保已安装pdfkit: npm install -g pdfkit');
    }
}

main().catch(console.error);
