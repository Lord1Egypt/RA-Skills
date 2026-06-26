/**
 * 导出对比报告为图片
 * 
 * 使用 Canvas 生成 PNG 图片，支持分享
 */

import { createCanvas, registerFont } from 'canvas';
import { renderComparison } from './renderer.js';

/**
 * 生成对比报告图片
 */
export function generateComparisonImage(result, outputPath) {
  const { products, recommendation } = result;
  
  // 图片尺寸
  const width = 800;
  const lineHeight = 60;
  const padding = 40;
  const headerHeight = 120;
  const productHeight = lineHeight * 8;
  const footerHeight = 150;
  
  const height = headerHeight + (products.length * productHeight) + footerHeight + (padding * 2);
  
  // 创建 Canvas
  const canvas = createCanvas(width, height);
  const ctx = canvas.getContext('2d');
  
  // 背景
  ctx.fillStyle = '#ffffff';
  ctx.fillRect(0, 0, width, height);
  
  // 标题
  ctx.fillStyle = '#1a1a1a';
  ctx.font = 'bold 32px -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto';
  ctx.textAlign = 'center';
  ctx.fillText('📊 线路对比报告', width / 2, padding + 40);
  
  // 副标题
  ctx.font = '18px -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto';
  ctx.fillStyle = '#666666';
  ctx.fillText(`共对比 ${products.length} 个商品`, width / 2, padding + 75);
  
  // 分隔线
  ctx.strokeStyle = '#e0e0e0';
  ctx.lineWidth = 1;
  ctx.beginPath();
  ctx.moveTo(padding, headerHeight + padding);
  ctx.lineTo(width - padding, headerHeight + padding);
  ctx.stroke();
  
  // 表头
  let y = headerHeight + padding + 30;
  ctx.font = 'bold 16px -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto';
  ctx.fillStyle = '#999999';
  ctx.textAlign = 'left';
  
  const columns = [
    { label: '商品', x: padding, width: 250 },
    { label: '价格', x: padding + 250, width: 100 },
    { label: '评分', x: padding + 350, width: 80 },
    { label: '购物店', x: padding + 430, width: 80 },
    { label: '酒店', x: padding + 510, width: 80 },
    { label: '评分', x: padding + 590, width: 80 }
  ];
  
  columns.forEach(col => {
    ctx.fillText(col.label, col.x, y);
  });
  
  // 分隔线
  y += 10;
  ctx.strokeStyle = '#f0f0f0';
  ctx.beginPath();
  ctx.moveTo(padding, y);
  ctx.lineTo(width - padding, y);
  ctx.stroke();
  
  // 商品列表
  y += 40;
  products.forEach((product, index) => {
    const isRecommended = index === 0;
    
    // 背景色
    if (isRecommended) {
      ctx.fillStyle = '#f0f9ff';
      ctx.fillRect(padding, y - 30, width - (padding * 2), productHeight);
    }
    
    ctx.font = isRecommended ? 'bold 18px -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto' : '16px -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto';
    ctx.fillStyle = isRecommended ? '#0066cc' : '#1a1a1a';
    
    // 商品名称
    const name = product.title || '未知商品';
    const platform = product.platform ? `[${product.platform}]` : '';
    ctx.fillText(`${platform} ${name}`, padding, y);
    
    // 推荐标记
    if (isRecommended) {
      ctx.fillStyle = '#ff6b00';
      ctx.font = 'bold 14px -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto';
      ctx.fillText('🥇 推荐', padding + 260, y);
    }
    
    // 价格
    ctx.fillStyle = '#1a1a1a';
    ctx.font = '16px -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto';
    ctx.fillText(product.price ? `¥${product.price}` : '-', padding + 250, y);
    
    // 评分
    ctx.fillText(product.rating ? `⭐${product.rating}` : '-', padding + 350, y);
    
    // 购物店
    const shoppingColor = product.shoppingStops === 0 ? '#00cc66' : product.shoppingStops > 3 ? '#ff4444' : '#ffaa00';
    ctx.fillStyle = shoppingColor;
    ctx.fillText(product.shoppingStops !== undefined ? `${product.shoppingStops}个` : '-', padding + 430, y);
    
    // 酒店
    ctx.fillStyle = '#1a1a1a';
    ctx.fillText(product.hotelStars ? `${product.hotelStars}钻` : '-', padding + 510, y);
    
    // 综合评分
    ctx.fillStyle = '#0066cc';
    ctx.font = 'bold 18px -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto';
    const score = calculateScore(product);
    ctx.fillText(`${score}分`, padding + 590, y);
    
    y += productHeight;
    
    // 分隔线
    ctx.strokeStyle = '#f0f0f0';
    ctx.beginPath();
    ctx.moveTo(padding, y - 10);
    ctx.lineTo(width - padding, y - 10);
    ctx.stroke();
  });
  
  // 底部说明
  y += padding;
  ctx.fillStyle = '#999999';
  ctx.font = '14px -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto';
  ctx.textAlign = 'center';
  ctx.fillText('⚠️  数据仅供参考，实际价格和服务以官网为准', width / 2, y);
  ctx.fillText(`生成时间：${new Date().toLocaleString('zh-CN')}`, width / 2, y + 25);
  
  // 生成图片
  const buffer = canvas.toBuffer('image/png');
  
  // 写入文件（需要 fs 模块）
  import('fs').then(({ writeFileSync }) => {
    writeFileSync(outputPath, buffer);
    console.log(`✅ 图片已保存：${outputPath}`);
  });
  
  return buffer;
}

/**
 * 计算商品综合评分
 */
function calculateScore(product) {
  let score = 50;
  
  if (product.price) {
    if (product.price < 2000) score -= 10;
    else if (product.price < 4000) score += 10;
    else if (product.price < 6000) score += 5;
    else score -= 5;
  }
  
  if (product.rating) {
    if (product.rating >= 4.8) score += 20;
    else if (product.rating >= 4.5) score += 15;
    else if (product.rating >= 4.0) score += 5;
    else score -= 10;
  }
  
  if (product.shoppingStops !== undefined) {
    score -= product.shoppingStops * 5;
    if (product.shoppingStops === 0) score += 15;
  }
  
  if (product.hotelStars) {
    score += product.hotelStars * 3;
  }
  
  return Math.max(0, Math.min(100, score));
}

export default {
  generateComparisonImage
};
