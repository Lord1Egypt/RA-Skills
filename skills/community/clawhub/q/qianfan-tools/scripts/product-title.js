#!/usr/bin/env node

const axios = require('axios');
const { resolveApiKey, emptyResult, successResult, BASE_URL, TIMEOUT_MS } = require('./shared');

const PRODUCT_URL = `${BASE_URL}/wenku/product_title`;

async function productTitle(imageUrl, description = '') {
  const apiKey = resolveApiKey();
  if (!apiKey) {
    return emptyResult('未配置 BAIDU_API_KEY，请在 OpenClaw Skills 配置页面填入，或本地编辑 config.json。');
  }

  if (!imageUrl) {
    return emptyResult('商品图片URL不能为空。');
  }

  try {
    const body = {
      image_url: imageUrl
    };
    
    if (description) {
      body.description = description;
    }

    const { data } = await axios.post(PRODUCT_URL, body, {
      timeout: TIMEOUT_MS,
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${apiKey}`,
      },
    });

    if (data && data.code) {
      return emptyResult(`服务错误: ${data.message || '未知错误'}`);
    }

    const result = data?.result || {};
    const titles = result?.titles || result?.result || [];
    
    return successResult({
      imageUrl,
      description,
      titles: Array.isArray(titles) ? titles : [titles],
      count: titles.length || 1,
      engine: 'baidu-product-title'
    });

  } catch (e) {
    return emptyResult(`商品标题生成失败: ${e.message}`);
  }
}

async function main() {
  const args = process.argv.slice(2);
  const imageUrl = args[0];
  const description = args.slice(1).join(' ');

  if (!imageUrl) {
    console.log(JSON.stringify(emptyResult('用法: node product-title.js <商品图片URL> [商品描述]')));
    process.exit(1);
  }

  const result = await productTitle(imageUrl, description);
  console.log(JSON.stringify(result, null, 2));
}

main();
