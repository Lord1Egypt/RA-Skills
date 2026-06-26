#!/usr/bin/env node
/**
 * A股日报自动生成器（Node.js版本）
 * 功能：抓取东方财富板块数据，生成日报
 */

const https = require('https');
const http = require('http');
const path = require('path');

// 配置
const CONFIG = {
  eastmoneyBoardApi: 'http://push2.eastmoney.com/api/qt/clist/get',
  eastmoneyStockApi: 'http://push2.eastmoney.com/api/qt/stock/get',
};

/**
 * HTTP请求封装
 */
function httpGet(url, options = {}) {
  return new Promise((resolve, reject) => {
    const client = url.startsWith('https') ? https : http;
    const req = client.get(url, options, (res) => {
      let data = '';
      res.on('data', (chunk) => data += chunk);
      res.on('end', () => {
        try {
          resolve(JSON.parse(data));
        } catch (e) {
          reject(e);
        }
      });
    });

    req.on('error', reject);
    req.setTimeout(10000, () => {
      req.destroy();
      reject(new Error('Request timeout'));
    });
  });
}

/**
 * 获取板块数据
 */
async function fetchBoardData() {
  const params = new URLSearchParams({
    pn: '1',
    pz: '50',
    po: '1',
    np: '1',
    ut: 'bd1d9ddb04089700cf9c27f6f7426281',
    fltt: '2',
    invt: '2',
    fid: 'f3',
    fs: 'm:90+t:2',
    fields: 'f1,f2,f3,f4,f5,f6,f7,f12,f14',
  });

  const url = `${CONFIG.eastmoneyBoardApi}?${params.toString()}`;
  const options = {
    headers: {
      'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
      'Referer': 'http://quote.eastmoney.com/',
    },
  };

  try {
    const data = await httpGet(url, options);
    const boards = [];

    if (data?.data?.diff) {
      data.data.diff.forEach((item) => {
        const changeVal = item.f3 || 0;
        const changeStr = changeVal > 0 ? `+${changeVal.toFixed(2)}%` : `${changeVal.toFixed(2)}%`;

        boards.push({
          code: item.f12 || '',
          name: item.f14 || '',
          change: changeStr,
          amount: item.f6 || 0,
        });
      });
    }

    return boards;
  } catch (e) {
    console.error(`[ERROR] API 获取板块数据失败: ${e.message}`);
    return [];
  }
}

/**
 * 获取大盘指数数据
 */
async function fetchIndexData() {
  const indicesConfig = [
    { secid: '1.000001', key: 'sh_index', name: '上证指数' },
    { secid: '0.399001', key: 'sz_index', name: '深证成指' },
    { secid: '0.399006', key: 'cy_index', name: '创业板指' },
    { secid: '1.000688', key: 'kc_index', name: '科创板指' },
  ];

  const result = { failed: [], success: [] };

  for (const { secid, key, name } of indicesConfig) {
    const params = new URLSearchParams({
      secid: secid,
      fields: 'f43,f44,f45,f46,f47,f48,f49,f50,f51,f52,f55,f57,f58,f60,f170,f171',
    });

    const url = `${CONFIG.eastmoneyStockApi}?${params.toString()}`;
    const options = {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)',
        'Referer': 'http://quote.eastmoney.com/',
      },
    };

    try {
      const data = await httpGet(url, options);
      if (data?.data) {
        const d = data.data;
        result[key] = (d.f43 / 100).toFixed(2);
        result[`${key}_change`] = `${(d.f170 / 100).toFixed(2)}%`;
        result.success.push(name);
      } else {
        throw new Error('数据为空');
      }
    } catch (e) {
      console.error(`[ERROR] 获取 ${name} 失败: ${e.message}`);
      result[key] = '--';
      result[`${key}_change`] = '--';
      result.failed.push(name);
    }
  }

  return result;
}

/**
 * 分析数据并构建报告数据
 */
function analyzeAndBuildReportData(boards, indices) {
  const boardFailed = !boards || boards.length === 0;

  // 热门板块（涨幅前5）
  let hotBoards = [];
  let focusBoards = [];
  let riskBoards = [];

  if (!boardFailed) {
    // 按涨幅排序
    const getChangeVal = (b) => {
      try {
        return parseFloat(b.change.replace('%', '').replace('+', '')) || 0;
      } catch {
        return 0;
      }
    };

    const sortedBoards = [...boards].sort((a, b) => getChangeVal(b) - getChangeVal(a));

    hotBoards = sortedBoards.slice(0, 5).map((b) => ({
      name: b.name,
      change: b.change,
      leader: '--',
      reason: '资金关注',
    }));

    // 明日关注板块
    focusBoards = sortedBoards.slice(2, 5).map((b) => ({
      name: b.name,
      reason: '资金持续流入',
      technical: '趋势向好',
      suggestion: '逢低关注',
    }));

    // 风险板块（跌幅前3）
    riskBoards = sortedBoards.slice(-3).reverse().map((b) => ({
      name: b.name,
      reason: '资金流出',
      suggestion: '谨慎参与',
    }));
  }

  // 判断市场情绪
  let sentiment = '中性';
  try {
    const shChange = parseFloat((indices.sh_index_change || '0%').replace('%', ''));
    sentiment = shChange > 0 ? '偏多' : '偏空';
  } catch {
    sentiment = '中性';
  }

  // 构建完整数据
  const data = {
    ...indices,
    market_sentiment: sentiment,
    hot_boards: hotBoards,
    focus_boards: focusBoards,
    risk_boards: riskBoards,
    north_money: '--',
    main_inflow: hotBoards.length > 0 ? hotBoards.slice(0, 3).map((b) => b.name).join('、') : '--',
    margin_balance: '--',
    board_failed: boardFailed,
    index_failed: indices.failed || [],
    index_success: indices.success || [],
    strategy: `1. **仓位控制**：建议维持6-7成仓位
2. **关注方向**：今日热点板块的持续性
3. **风险控制**：设置止损位，避免追高
4. **操作节奏**：低吸高抛，不追涨杀跌`,
  };

  return data;
}

/**
 * 生成Markdown报告
 */
function generateReport(boardData) {
  const today = new Date().toLocaleDateString('zh-CN', { year: 'numeric', month: '2-digit', day: '2-digit' }).replace(/\//g, '年').replace('年', '年').replace(/年(\d{2})$/, '月$1日');

  let report = `# 📊 A股市场日报
**${today}**

---

## 🎯 大盘概览

| 指数 | 收盘点位 | 涨跌幅 |
|------|---------|--------|
| 上证指数 | ${boardData.sh_index || '--'} | ${boardData.sh_index_change || '--'} |
| 深证成指 | ${boardData.sz_index || '--'} | ${boardData.sz_index_change || '--'} |
| 创业板指 | ${boardData.cy_index || '--'} | ${boardData.cy_index_change || '--'} |
| 科创板指 | ${boardData.kc_index || '--'} | ${boardData.kc_index_change || '--'} |

**市场情绪**: ${boardData.market_sentiment || '中性'}
`;

  // 添加数据获取失败提示
  const warnings = [];
  if (boardData.index_failed && boardData.index_failed.length > 0) {
    warnings.push(`指数数据 - ${boardData.index_failed.join('、')}`);
  }
  if (boardData.board_failed) {
    warnings.push(`板块数据`);
  }
  if (warnings.length > 0) {
    report += `\n⚠️ **数据获取提示**: 以下数据获取失败 (${warnings.join('；')})，可能原因：非交易时间/网络异常/API 暂时不可用\n`;
  }

  report += `
---

## 🔥 热门板块 TOP 5

| 排名 | 板块名称 | 涨跌幅 | 领涨股 |
|------|---------|--------|--------|
`;

  const hotBoards = boardData.hot_boards || [];
  hotBoards.slice(0, 5).forEach((board, i) => {
    report += `| ${i + 1} | ${board.name} | ${board.change} | ${board.leader} |\n`;
  });

  report += `---

## 📈 明日关注

| 板块名称 | 关注理由 | 技术面 | 操作建议 |
|---------|---------|--------|---------|
`;

  const focusBoards = boardData.focus_boards || [];
  focusBoards.forEach((board) => {
    report += `| ${board.name} | ${board.reason} | ${board.technical} | ${board.suggestion} |\n`;
  });

  report += `---

## ⚠️ 风险提示

| 板块名称 | 风险理由 | 建议 |
|---------|---------|------|
`;

  const riskBoards = boardData.risk_boards || [];
  riskBoards.forEach((board) => {
    report += `| ${board.name} | ${board.reason} | ${board.suggestion} |\n`;
  });

  report += `---

## 💰 资金动向

`;

  if (hotBoards.length > 0) {
    const hotBoardsNames = hotBoards.slice(0, 3).map((b) => b.name).join('、');
    report += `- **主力流入方向**: ${hotBoardsNames}\n`;
  } else {
    report += `- **主力流入方向**: --\n`;
  }

  report += `- **北向资金**: ${boardData.north_money || '--'}
- **融资余额**: ${boardData.margin_balance || '--'}

---

## 📝 操作策略

${boardData.strategy || '1. **仓位控制**：建议维持6-7成仓位\n2. **关注方向**：今日热点板块的持续性\n3. **风险控制**：设置止损位，避免追高\n4. **操作节奏**：低吸高抛，不追涨杀跌'}

---

**数据来源**: 东方财富网
**生成时间**: ${new Date().toLocaleDateString('zh-CN').replace(/\//g, '-')}
`;

  return report;
}

/**
 * 主函数
 */
async function main() {
  const args = process.argv.slice(2);
  const command = args[0];

  // 判断输出格式
  const outputJson = command === 'json' || command === '--json';

  try {
    // 获取指数数据
    const indices = await fetchIndexData();

    // 获取板块数据
    const boards = await fetchBoardData();

    // 分析并构建报告数据
    const reportData = analyzeAndBuildReportData(boards, indices);

    // 根据命令输出不同格式
    if (outputJson) {
      // JSON 输出
      console.log(JSON.stringify(reportData, null, 2));
    } else {
      // 格式化输出（默认）
      const report = generateReport(reportData);
      console.log(report);
    }

    return 0;
  } catch (error) {
    console.error(`[ERROR] 生成报告失败: ${error.message}`);
    console.error(error.stack);
    return 1;
  }
}

// 如果是直接运行此脚本
if (require.main === module) {
  main()
    .then((code) => process.exit(code))
    .catch((error) => {
      console.error('[ERROR]', error);
      process.exit(1);
    });
}

module.exports = { generateReport, fetchBoardData, fetchIndexData };
