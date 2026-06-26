#!/usr/bin/env node
/**
 * 生成途牛订单页面二维码并嵌入 HTML
 * 使用方法：node qrcode.js <支付链接> <输出 HTML 路径>
 */

const QRCode = require('qrcode');
const fs = require('fs');
const path = require('path');

async function generateQRCodeHTML(url, outputPath) {
    console.log('📱 生成支付二维码 HTML...');
    console.log(`🔗 支付链接：${url}`);

    try {
        // 生成 base64 二维码
        const qrCodeBase64 = await QRCode.toDataURL(url, {
            margin: 2,
            width: 300,
            color: {
                dark: '#667eea',
                light: '#ffffff'
            }
        });

        // 生成 HTML
        const html = `<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>途牛订单支付二维码</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Microsoft YaHei', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        .container {
            background: white;
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            text-align: center;
            max-width: 400px;
        }
        h1 { color: #333; margin-bottom: 10px; font-size: 24px; }
        .subtitle { color: #666; margin-bottom: 30px; font-size: 14px; }
        .qrcode-wrapper {
            border: 2px solid #667eea;
            border-radius: 12px;
            padding: 20px;
            margin: 20px 0;
            display: inline-block;
        }
        .qrcode-wrapper img { display: block; }
        .tip { color: #666; font-size: 14px; margin-top: 20px; }
        .btn {
            display: inline-block;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 12px 30px;
            border-radius: 8px;
            text-decoration: none;
            font-weight: 600;
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>💳 订单支付</h1>
        <p class="subtitle">打开途牛 App 扫一扫完成支付</p>
        <div class="qrcode-wrapper">
            <img src="${qrCodeBase64}" alt="支付二维码" />
        </div>
        <p class="tip">或点击下方按钮直接跳转</p>
        <a href="${url}" class="btn" target="_blank">前往支付页面</a>
    </div>
</body>
</html>`;

        // 写入文件
        fs.writeFileSync(outputPath, html, 'utf8');
        
        console.log(`✅ 二维码 HTML 已生成：${outputPath}`);
        
        return {
            success: true,
            outputPath: outputPath,
            qrCodeBase64: qrCodeBase64
        };

    } catch (error) {
        console.error('❌ 二维码生成失败:', error.message);
        return {
            success: false,
            error: error.message
        };
    }
}

async function main() {
    const args = process.argv.slice(2);

    if (args.length < 2) {
        console.error('❌ 请提供支付链接和输出路径');
        console.log('使用方法：node qrcode.js <支付链接> <输出 HTML 路径>');
        console.log('示例：node qrcode.js https://m.tuniu.com/u/order?page=1 ./output/qrcode.html');
        process.exit(1);
    }

    const paymentUrl = args[0];
    const outputPath = args[1];

    const result = await generateQRCodeHTML(paymentUrl, outputPath);

    if (result.success) {
        console.log('');
        console.log('✅ 二维码生成成功！');
        console.log(`📄 文件已保存：${result.outputPath}`);
    } else {
        console.log('');
        console.log('❌ 二维码生成失败');
        process.exit(1);
    }
}

if (require.main === module) {
    main();
}

module.exports = { generateQRCodeHTML };
