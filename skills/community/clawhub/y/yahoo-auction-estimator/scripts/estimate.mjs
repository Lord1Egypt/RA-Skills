#!/usr/bin/env node
/**
 * Yahoo Auction Estimator
 * 日本雅虎拍卖商品自动估价工具
 */

import { execSync } from 'child_process';

const PROXY = process.env.PROXY_SOCKS5 || 'socks5://127.0.0.1:1080';

// 辅助函数：格式化数字
function formatNumber(num) {
  return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
}

// 辅助函数：执行curl命令
function curl(url) {
  try {
    return execSync(
      `curl -s --proxy ${PROXY} -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)" "${url}" 2>/dev/null`,
      { encoding: 'utf8', timeout: 30000 }
    );
  } catch (e) {
    return '';
  }
}

// 步骤1: 获取商品信息
async function getProductInfo(id) {
  const url = `https://auctions.yahoo.co.jp/jp/auction/${id}`;
  const html = curl(url);
  
  if (!html || html.includes('このオークションは終了しました') || html.includes('この商品は存在しません')) {
    return { error: '商品已结束或不存在' };
  }
  
  // 提取标题（支持多种形式）
  let titleMatch = html.match(/<title>(.*?) - Yahoo!オークション<\/title>/);
  if (!titleMatch) {
    titleMatch = html.match(/<title>(.*?)<\/title>/);
  }
  let title = titleMatch ? titleMatch[1].replace(/\n/g, '').trim() : '未知商品';
  
  // 移除 <<<EXTERNAL_UNTRUSTED_CONTENT>>> 等标记
  title = title.replace(/<<<.*?>>>/g, '').trim();
  
  // 提取当前价格
  const priceMatch = html.match(/現在([\d,]+)円/);
  const currentPrice = priceMatch ? priceMatch[1] : '0';
  
  // 提取结束时间
  const endTimeMatch = html.match(/終了日時<\/span>(\d{4}年\d{1,2}月\d{1,2}日).*?(\d{1,2})時(\d{1,2})分/);
  let endTime = { date: '', jp: '', cn: '' };
  if (endTimeMatch) {
    const month = endTimeMatch[1].match(/(\d{1,2})月/)[1];
    const day = endTimeMatch[1].match(/(\d{1,2})日/)[1];
    const hour = parseInt(endTimeMatch[2]);
    const min = endTimeMatch[3];
    
    endTime.jp = `${month}/${day} ${hour}:${min}`;
    endTime.cn = `${month}/${day} ${hour-1}:${min}`; // 日本时间-1小时
  }
  
  return { id, title, currentPrice, endTime };
}

// 步骤2: 提取搜索关键词
function extractKeywords(title) {
  // 常见排除词
  const excludeWords = [
    '【美品】', '【並品】', '【希少】', '【極上美品】',
    '実用美品', '動作確認済み', '1円開始', '即日発送',
    '持病', 'プラ割れなし', '元箱付き'
  ];
  
  let cleanTitle = title;
  excludeWords.forEach(word => {
    cleanTitle = cleanTitle.replace(word, '');
  });
  
  // 提取核心信息
  // 品牌提取
  const brands = ['LEICA', 'ライカ', 'FUJIFILM', '富士', 'HASSELBLAD', 'ハッセルブラッド', 
                  'Nikon', 'Canon', 'SONY', 'MS-OPTICS', 'Avenon', 'アベノン'];
  
  let brand = '';
  for (const b of brands) {
    if (cleanTitle.includes(b)) {
      brand = b.replace('ライカ', 'LEICA').replace('ハッセルブラッド', 'HASSELBLAD')
               .replace('富士', 'FUJIFILM').replace('アベノン', 'Avenon');
      break;
    }
  }
  
  // 提取系列型号
  const seriesPatterns = [
    /SUMMICRON-M.*?35mm.*?F[\d\.]+/i,
    /GS645W/i,
    /500C\/M/i,
    /GA645Zi/i,
    /SONNETAR.*?50mm.*?F[\d\.]+/i,
    /Planar.*?80mm.*?F[\d\.]+/i,
    /Avenon.*?21mm.*?F[\d\.]+/i
  ];
  
  let series = '';
  for (const pattern of seriesPatterns) {
    const match = cleanTitle.match(pattern);
    if (match) {
      series = match[0];
      break;
    }
  }
  
  // 如果没有匹配到系列，尝试通用提取
  if (!series) {
    // 焦段+光圈
    const lensMatch = cleanTitle.match(/(\d+)mm.*?F([\d\.]+)/);
    if (lensMatch) {
      series = `${lensMatch[1]}mm F${lensMatch[2]}`;
    }
  }
  
  return brand && series ? `${brand} ${series}` : cleanTitle.trim();
}

// 步骤3: 查询历史成交价
async function getHistoricalPrices(keyword) {
  const encodedKeyword = encodeURIComponent(keyword);
  const url = `https://aucfree.com/search?from=2015-06&o=t2&q=${encodedKeyword}&to=2026-02`;
  
  const html = curl(url);
  if (!html) return [];
  
  // 提取价格
  const prices = [];
  const priceMatches = html.matchAll(/([\d,]+)円/g);
  for (const match of priceMatches) {
    const price = parseInt(match[1].replace(/,/g, ''));
    if (price > 1000 && !prices.includes(price)) { // 排除1円起拍
      prices.push(price);
    }
  }
  
  return prices.slice(0, 30); // 取前30条
}

// 步骤4: 计算建议出价
function calculateSuggestion(prices) {
  if (prices.length === 0) return { avg: 0, suggested: 0 };
  
  const sum = prices.reduce((a, b) => a + b, 0);
  const avg = Math.floor(sum / prices.length);
  const suggested = Math.floor(avg * 0.85);
  
  return { avg, suggested, min: Math.min(...prices), max: Math.max(...prices) };
}

// 步骤5: 输出报告
function printReport(info, keywords, calc) {
  const status = calc.suggested === 0 ? '⚪ 无历史数据' :
                 parseInt(info.currentPrice.replace(/,/g, '')) < calc.suggested * 0.5 ? '🔴 极低' :
                 parseInt(info.currentPrice.replace(/,/g, '')) < calc.suggested ? '🟡 偏低' :
                 parseInt(info.currentPrice.replace(/,/g, '')) > calc.suggested * 1.2 ? '🔴 已超价' : '🟢 合理';
  
  console.log(`\n┌─ ${info.id} ─────────────────────────────┐`);
  console.log(`│ 商品: ${info.title.substring(0, 35)}${info.title.length > 35 ? '...' : ''}`);
  console.log(`│ 关键词: ${keywords}`);
  console.log(`│ 当前: ${info.currentPrice} | 结束: ${info.endTime.cn || '未知'}`);
  if (calc.suggested > 0) {
    console.log(`│ 历史: 均${formatNumber(calc.avg)} 低${formatNumber(calc.min)} 高${formatNumber(calc.max)}`);
    console.log(`│ 建议: ${formatNumber(calc.suggested)} (均价×85%)`);
  }
  console.log(`│ 状态: ${status}`);
  console.log(`└────────────────────────────────────────┘`);
}

// 主函数
async function main() {
  const ids = process.argv.slice(2);
  
  if (ids.length === 0) {
    console.log('用法: node estimate.mjs <商品ID> [<商品ID> ...]');
    console.log('示例: node estimate.mjs b1220553804');
    console.log('      node estimate.mjs id1 id2 id3');
    process.exit(1);
  }
  
  console.log('🏷️ Yahoo Auction Estimator');
  console.log(`🌐 代理: ${PROXY}`);
  console.log(`📦 共 ${ids.length} 个商品\n`);
  
  for (const id of ids) {
    try {
      // 步骤1: 获取商品信息
      const info = await getProductInfo(id);
      if (info.error) {
        console.log(`\n❌ ${id}: ${info.error}`);
        continue;
      }
      
      // 步骤2: 提取关键词
      const keywords = extractKeywords(info.title);
      
      // 步骤3: 查询历史价格
      const prices = await getHistoricalPrices(keywords);
      
      // 步骤4: 计算建议出价
      const calc = calculateSuggestion(prices);
      
      // 步骤5: 输出报告
      printReport(info, keywords, calc);
      
      // 避免请求过快
      await new Promise(r => setTimeout(r, 2000));
    } catch (e) {
      console.log(`\n❌ ${id}: 处理出错 - ${e.message}`);
    }
  }
  
  console.log('\n✅ 估价完成');
}

main();
