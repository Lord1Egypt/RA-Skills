/**
 * Stock Master Pro - Dashboard JavaScript
 * 负责数据加载、实时更新和图表渲染
 */

// 配置
const CONFIG = {
  refreshInterval: 10000, // 10 秒刷新
  dataPath: './stocks',   // 修复：使用正确的相对路径
  checkInterval: 600000,  // 10 分钟检查持仓
  tradingHours: {
    morning: { start: 9.5, end: 11.5 }, // 9:30-11:30
    afternoon: { start: 13, end: 15 }   // 13:00-15:00
  }
};

// 全局状态
let state = {
  lastCheck: null,
  holdings: [],
  alerts: [],
  marketData: null,
  refreshTimer: null,
  isTradingTime: false
};

/**
 * 判断是否在交易时段
 */
function checkTradingTime() {
  const now = new Date();
  const hour = now.getHours() + now.getMinutes() / 60;
  const day = now.getDay();
  
  // 周末不交易
  if (day === 0 || day === 6) {
    state.isTradingTime = false;
    return false;
  }
  
  // 判断交易时段
  const { morning, afternoon } = CONFIG.tradingHours;
  const inMorning = hour >= morning.start && hour <= morning.end;
  const inAfternoon = hour >= afternoon.start && hour <= afternoon.end;
  
  state.isTradingTime = inMorning || inAfternoon;
  return state.isTradingTime;
}

// 初始化
document.addEventListener('DOMContentLoaded', () => {
  console.log('🚀 Stock Master Pro Dashboard 已加载');
  checkTradingTime();
  updateClock();
  loadMarketData();
  loadHoldings();
  startAutoRefresh();
  initCharts();
  
  // 显示交易状态
  updateTradingStatus();
});

/**
 * 更新时钟
 */
function updateClock() {
  const now = new Date();
  const timeStr = now.toLocaleTimeString('zh-CN', { hour12: false });
  document.getElementById('currentTime').textContent = timeStr;
  document.getElementById('footerUpdateTime').textContent = timeStr;
  
  // 每秒更新
  setTimeout(updateClock, 1000);
}

/**
 * 更新交易状态显示
 */
function updateTradingStatus() {
  const statusDiv = document.getElementById('tradingStatus');
  if (!statusDiv) return;
  
  if (state.isTradingTime) {
    statusDiv.innerHTML = '<span class="text-green-400">🟢 交易时段</span>';
  } else {
    statusDiv.innerHTML = '<span class="text-gray-400">⚫ 已收盘</span>';
  }
}

/**
 * 加载大盘数据
 */
async function loadMarketData() {
  try {
    // 优先读取聚合数据
    const response = await fetch(`${CONFIG.dataPath}/dashboard_data.json?t=${Date.now()}`);
    const data = await response.json();
    
    if (data.market) {
      updateMarketDisplay(data.market);
      
      // 更新交易状态
      if (data.marketStatus) {
        const statusDiv = document.getElementById('tradingStatus');
        if (statusDiv) {
          if (data.marketStatus === 'trading') {
            statusDiv.innerHTML = '<span class="text-green-400">🟢 交易时段</span>';
          } else if (data.marketStatus === 'closed') {
            statusDiv.innerHTML = '<span class="text-gray-400">⚫ 已收盘</span>';
          } else {
            statusDiv.innerHTML = '<span class="text-yellow-400">🕐 休市中</span>';
          }
        }
      }
    }
  } catch (error) {
    console.error('加载大盘数据失败:', error);
    // 使用模拟数据展示效果
    updateMarketDisplay({
      sh: { price: 3878.04, change: 64.76, changePct: 1.70, amount: 8746.2 },
      sz: { price: 13519.91, change: 174.40, changePct: 1.31, amount: 10773.7 },
      cyb: { price: 3243.65, change: 8.43, changePct: 0.26, amount: 4847.0 },
      zz: { price: 8194.33, change: 96.08, changePct: 1.19, amount: 1285.0 }
    });
  }
}

/**
 * 更新大盘显示
 */
function updateMarketDisplay(data) {
  // 上证指数
  document.getElementById('sh-price').textContent = data.sh.price.toFixed(2);
  document.getElementById('sh-change').textContent = (data.sh.change >= 0 ? '+' : '') + data.sh.change.toFixed(2);
  document.getElementById('sh-change-pct').textContent = (data.sh.changePct >= 0 ? '+' : '') + data.sh.changePct.toFixed(2) + '%';
  document.getElementById('sh-amount').textContent = data.sh.amount.toFixed(1);
  
  setColorByChange('sh-change', data.sh.change);
  setColorByChange('sh-change-pct', data.sh.changePct);
  
  // 深证成指
  document.getElementById('sz-price').textContent = data.sz.price.toFixed(2);
  document.getElementById('sz-change').textContent = (data.sz.change >= 0 ? '+' : '') + data.sz.change.toFixed(2);
  document.getElementById('sz-change-pct').textContent = (data.sz.changePct >= 0 ? '+' : '') + data.sz.changePct.toFixed(2) + '%';
  document.getElementById('sz-amount').textContent = data.sz.amount.toFixed(1);
  
  setColorByChange('sz-change', data.sz.change);
  setColorByChange('sz-change-pct', data.sz.changePct);
  
  // 创业板指
  document.getElementById('cyb-price').textContent = data.cyb.price.toFixed(2);
  document.getElementById('cyb-change').textContent = (data.cyb.change >= 0 ? '+' : '') + data.cyb.change.toFixed(2);
  document.getElementById('cyb-change-pct').textContent = (data.cyb.changePct >= 0 ? '+' : '') + data.cyb.changePct.toFixed(2) + '%';
  document.getElementById('cyb-amount').textContent = data.cyb.amount.toFixed(1);
  
  setColorByChange('cyb-change', data.cyb.change);
  setColorByChange('cyb-change-pct', data.cyb.changePct);
  
  // 中证 500
  document.getElementById('zz-price').textContent = data.zz.price.toFixed(2);
  document.getElementById('zz-change').textContent = (data.zz.change >= 0 ? '+' : '') + data.zz.change.toFixed(2);
  document.getElementById('zz-change-pct').textContent = (data.zz.changePct >= 0 ? '+' : '') + data.zz.changePct.toFixed(2) + '%';
  document.getElementById('zz-amount').textContent = data.zz.amount.toFixed(1);
  
  setColorByChange('zz-change', data.zz.change);
  setColorByChange('zz-change-pct', data.zz.changePct);
  
  // 更新图表
  updateMarketChart(data);
}

/**
 * 根据涨跌设置颜色
 */
function setColorByChange(elementId, value) {
  const element = document.getElementById(elementId);
  element.classList.remove('text-up', 'text-down', 'text-flat');
  
  if (value > 0) {
    element.classList.add('text-up'); // A 股红涨
  } else if (value < 0) {
    element.classList.add('text-down'); // A 股绿跌
  } else {
    element.classList.add('text-flat');
  }
}

/**
 * 加载持仓数据
 */
async function loadHoldings() {
  try {
    // 优先读取聚合数据
    const response = await fetch(`${CONFIG.dataPath}/dashboard_data.json?t=${Date.now()}`);
    const data = await response.json();
    
    state.lastCheck = data;
    state.holdings = data.holdings || [];
    state.alerts = data.alerts || [];
    
    updateHoldingsTable(state.holdings);
    updateAlertsDisplay(state.alerts);
    updateLastUpdateTime(data.updateTime);
    updateNextCheckTime();
  } catch (error) {
    console.error('加载持仓数据失败:', error);
    // 显示示例数据
    showDemoHoldings();
  }
}

/**
 * 更新持仓表格
 */
function updateHoldingsTable(holdings) {
  const tbody = document.getElementById('holdings-table');
  
  if (!holdings || holdings.length === 0) {
    tbody.innerHTML = `
      <tr>
        <td colspan="8" class="px-6 py-12 text-center text-gray-400">
          暂无持仓数据，请先配置持仓
        </td>
      </tr>
    `;
    return;
  }
  
  tbody.innerHTML = holdings.map((h, index) => {
    const profitClass = h.profit.profit >= 0 ? 'text-up' : 'text-down';
    const changeClass = h.quote.changePct >= 0 ? 'text-up' : 'text-down';
    
    let statusBadge = '';
    if (h.quote.changePct > 5) {
      statusBadge = '<span class="px-2 py-1 bg-red-500/20 text-red-400 rounded text-xs">🔥 强势</span>';
    } else if (h.quote.changePct > 2) {
      statusBadge = '<span class="px-2 py-1 bg-green-500/20 text-green-400 rounded text-xs">✅ 正常</span>';
    } else if (h.quote.changePct > -2) {
      statusBadge = '<span class="px-2 py-1 bg-gray-500/20 text-gray-400 rounded text-xs">😐 震荡</span>';
    } else if (h.quote.changePct > -5) {
      statusBadge = '<span class="px-2 py-1 bg-yellow-500/20 text-yellow-400 rounded text-xs">⚠️ 走弱</span>';
    } else {
      statusBadge = '<span class="px-2 py-1 bg-red-500/20 text-red-400 rounded text-xs">🚨 大跌</span>';
    }
    
    return `
      <tr class="hover:bg-white/5 transition-colors animate-slide-up" style="animation-delay: ${index * 0.1}s">
        <td class="px-6 py-4">
          <div class="flex items-center">
            <div>
              <div class="font-medium text-white">${h.name}</div>
              <div class="text-xs text-gray-500">${h.code}</div>
            </div>
          </div>
        </td>
        <td class="px-6 py-4">
          <div class="font-mono text-lg">${h.quote.price.toFixed(2)}</div>
        </td>
        <td class="px-6 py-4">
          <div class="font-mono ${changeClass}">
            ${h.quote.changePct >= 0 ? '+' : ''}${h.quote.changePct.toFixed(2)}%
          </div>
        </td>
        <td class="px-6 py-4">
          <div class="font-mono text-gray-400">${h.quote.price - (h.profit.profit / h.shares).toFixed(2)}</div>
        </td>
        <td class="px-6 py-4">
          <div class="font-mono ${profitClass}">
            ${h.profit.profitText} 元
          </div>
        </td>
        <td class="px-6 py-4">
          <div class="font-mono ${profitClass}">
            ${h.profit.profitPctText}
          </div>
        </td>
        <td class="px-6 py-4">
          <div class="font-mono text-gray-400">${h.quote.volumeRatio?.toFixed(2) || '--'}</div>
        </td>
        <td class="px-6 py-4">
          ${statusBadge}
        </td>
      </tr>
    `;
  }).join('');
}

/**
 * 更新预警显示
 */
function updateAlertsDisplay(alerts) {
  const container = document.getElementById('alerts-container');
  
  if (!alerts || alerts.length === 0) {
    container.innerHTML = `
      <div class="card p-6 text-center text-gray-400">
        ✅ 暂无预警信息
      </div>
    `;
    return;
  }
  
  container.innerHTML = alerts.map(alert => {
    let bgColor = 'bg-blue-500/20';
    let borderColor = 'border-blue-500/50';
    let icon = 'ℹ️';
    
    if (alert.level === 'urgent') {
      bgColor = 'bg-red-500/20';
      borderColor = 'border-red-500/50';
      icon = '🚨';
    } else if (alert.level === 'warning') {
      bgColor = 'bg-yellow-500/20';
      borderColor = 'border-yellow-500/50';
      icon = '⚠️';
    }
    
    const urgentClass = alert.level === 'urgent' ? 'alert-urgent' : '';
    
    return `
      <div class="card p-4 border-l-4 ${borderColor} ${urgentClass}">
        <div class="flex items-center space-x-3">
          <span class="text-2xl">${icon}</span>
          <div class="flex-1">
            <div class="font-medium">${alert.message}</div>
            <div class="text-xs text-gray-500 mt-1">
              ${new Date(alert.timestamp).toLocaleString('zh-CN')}
            </div>
          </div>
        </div>
      </div>
    `;
  }).join('');
}

/**
 * 显示示例持仓（演示用）
 */
function showDemoHoldings() {
  const demoHoldings = [
    {
      name: '穗恒运 A',
      code: '000531.SZ',
      quote: { price: 7.83, changePct: 8.45, volumeRatio: 3.00 },
      profit: { profit: 400.96, profitText: '+400.96', profitPct: 7.89, profitPctText: '+7.89%' },
      shares: 700
    }
  ];
  
  updateHoldingsTable(demoHoldings);
}

/**
 * 更新最后更新时间
 */
function updateLastUpdateTime(checkTime) {
  const time = new Date(checkTime).toLocaleTimeString('zh-CN', { hour12: false });
  document.getElementById('lastUpdate').textContent = `更新于 ${time}`;
}

/**
 * 更新下次检查时间
 */
function updateNextCheckTime() {
  const nextCheck = new Date(Date.now() + CONFIG.checkInterval);
  const timeStr = nextCheck.toLocaleTimeString('zh-CN', { hour12: false, hour: '2-digit', minute: '2-digit' });
  document.getElementById('nextCheck').textContent = timeStr;
}

/**
 * 初始化图表
 */
let marketChart = null;

function initCharts() {
  const ctx = document.getElementById('marketChart').getContext('2d');
  
  // 创建渐变
  const gradient = ctx.createLinearGradient(0, 0, 0, 400);
  gradient.addColorStop(0, 'rgba(59, 130, 246, 0.2)');
  gradient.addColorStop(1, 'rgba(59, 130, 246, 0)');
  
  marketChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: ['9:30', '10:00', '10:30', '11:00', '11:30', '13:00', '13:30', '14:00', '14:30', '15:00'],
      datasets: [{
        label: '上证指数',
        data: [3814, 3825, 3840, 3855, 3860, 3865, 3870, 3872, 3875, 3878],
        borderColor: '#3b82f6',
        backgroundColor: gradient,
        borderWidth: 2,
        fill: true,
        tension: 0.4,
        pointRadius: 0,
        pointHoverRadius: 6
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      interaction: {
        intersect: false,
        mode: 'index'
      },
      plugins: {
        legend: {
          display: false
        },
        tooltip: {
          backgroundColor: 'rgba(17, 24, 39, 0.9)',
          titleColor: '#f9fafb',
          bodyColor: '#9ca3af',
          borderColor: '#374151',
          borderWidth: 1,
          padding: 12,
          displayColors: false,
          callbacks: {
            label: function(context) {
              return `上证指数：${context.parsed.y.toFixed(2)}`;
            }
          }
        }
      },
      scales: {
        x: {
          grid: {
            color: '#374151',
            drawBorder: false
          },
          ticks: {
            color: '#9ca3af'
          }
        },
        y: {
          grid: {
            color: '#374151',
            drawBorder: false
          },
          ticks: {
            color: '#9ca3af',
            callback: function(value) {
              return value.toFixed(0);
            }
          }
        }
      }
    }
  });
}

/**
 * 更新图表数据
 */
function updateMarketChart(data) {
  if (!marketChart) return;
  
  // 更新数据（示例）
  marketChart.data.datasets[0].data = [
    3814, 3825, 3840, 3855, 3860, 3865, 3870, 3872, 3875, data.sh.price
  ];
  marketChart.update();
}

/**
 * 加载复盘报告（JSON 渲染）
 */
async function loadReview(sessionType) {
  const contentDiv = document.getElementById('review-content');
  contentDiv.innerHTML = `
    <div class="flex flex-col items-center justify-center py-12">
      <div class="loading mb-4"></div>
      <div class="text-gray-400">加载${sessionType === 'noon' ? '午盘' : sessionType === 'afternoon' ? '尾盘' : '收盘'}复盘报告...</div>
    </div>
  `;
  
  try {
    const response = await fetch(`${CONFIG.dataPath}/reviews_data.json?t=${Date.now()}`);
    const data = await response.json();
    
    const session = data.sessions[sessionType];
    if (!session) {
      throw new Error('未找到复盘数据');
    }
    
    let html = `
      <div class="space-y-6">
        <!-- 标题 -->
        <div class="flex items-center justify-between mb-6">
          <h3 class="text-2xl font-bold">${session.title}</h3>
          <span class="text-sm text-gray-400">${data.date} ${session.time}</span>
        </div>
        
        <!-- 市场概览 -->
        <div class="card p-6">
          <h4 class="text-lg font-bold mb-4 flex items-center">
            <span class="text-xl mr-2">📊</span>
            市场概览
          </h4>
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
    `;
    
    // 指数卡片
    for (const idx of session.market.indices) {
      const changeColor = idx.changePct >= 0 ? 'text-up' : 'text-down';
      html += `
        <div class="bg-white/5 rounded-lg p-4">
          <div class="text-sm text-gray-400 mb-1">${idx.name}</div>
          <div class="text-2xl font-bold font-mono">${idx.price.toFixed(2)}</div>
          <div class="text-sm ${changeColor}">${idx.change >= 0 ? '+' : ''}${idx.changePct.toFixed(2)}%</div>
          <div class="text-xs text-gray-500 mt-2">成交额：${idx.amount}亿</div>
        </div>
      `;
    }
    
    html += `
          </div>
          <div class="mt-4 flex items-center space-x-4 text-sm">
            ${session.market.sentiment ? `<span class="text-gray-400">市场情绪：<span class="text-white">${session.market.sentiment}</span></span>` : ''}
            ${session.market.volume ? `<span class="text-gray-400">成交量：<span class="text-white">${session.market.volume}</span></span>` : ''}
            ${session.market.profitEffect ? `<span class="text-gray-400">赚钱效应：<span class="text-white">${session.market.profitEffect}</span></span>` : ''}
          </div>
          ${session.market.trend ? `<div class="mt-2 text-sm text-gray-300">${session.market.trend}</div>` : ''}
        </div>
        
        <!-- 热点板块 -->
        <div class="card p-6">
          <h4 class="text-lg font-bold mb-4 flex items-center">
            <span class="text-xl mr-2">🔥</span>
            热点板块
          </h4>
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
    `;
    
    for (const sector of session.sectors) {
      const hasDeepAnalysis = sector.whyRise || sector.riseLogic || sector.sustainability;
      
      html += `
        <div class="bg-white/5 rounded-lg p-4">
          <div class="flex items-center justify-between mb-3">
            <div>
              <div class="font-bold">No.${sector.rank || '-'} ${sector.name}</div>
              <div class="text-xs text-gray-400">涨停：${sector.limitUp || '-'}家</div>
            </div>
            <div class="text-right">
              <div class="text-lg font-bold ${sector.changePct >= 0 ? 'text-up' : 'text-down'}">${sector.changePct >= 0 ? '+' : ''}${sector.changePct.toFixed(2)}%</div>
              <div class="text-xs text-gray-500">流入：${sector.netInflow}亿</div>
            </div>
          </div>
          
          ${hasDeepAnalysis ? `
            <div class="space-y-3 mt-3 pt-3 border-t border-gray-700">
              ${sector.whyRise ? `
                <div class="flex items-center space-x-2">
                  <span class="text-xs font-bold text-blue-400">💡 为什么涨:</span>
                  <span class="text-xs text-gray-300">${sector.whyRise}</span>
                </div>
              ` : ''}
              
              ${sector.riseLogic ? `
                <div>
                  <div class="text-xs font-bold text-blue-400 mb-2">📊 上涨逻辑:</div>
                  <div class="space-y-1">
                    ${sector.riseLogic.map(logic => `
                      <div class="text-xs text-gray-300 pl-3">${logic}</div>
                    `).join('')}
                  </div>
                </div>
              ` : ''}
              
              ${sector.sustainability ? `
                <div class="flex items-start space-x-2">
                  <span class="text-xs font-bold text-green-400">♻️ 持续性:</span>
                  <span class="text-xs px-2 py-0.5 ${sector.sustainability === '高' ? 'bg-green-500/20 text-green-400' : sector.sustainability === '中' ? 'bg-yellow-500/20 text-yellow-400' : 'bg-red-500/20 text-red-400'} rounded">${sector.sustainability}</span>
                </div>
              ` : ''}
              
              ${sector.sustainabilityAnalysis ? `
                <div class="text-xs text-gray-400 pl-3">${sector.sustainabilityAnalysis}</div>
              ` : ''}
              
              ${sector.followStrategy ? `
                <div class="bg-blue-500/10 border border-blue-500/30 rounded-lg p-2">
                  <div class="text-xs font-bold text-blue-400 mb-1">🎯 怎么跟进:</div>
                  <div class="text-xs text-gray-300">${sector.followStrategy}</div>
                </div>
              ` : ''}
              
              ${sector.stocks && sector.stocks.length > 0 ? `
                <details class="mt-3">
                  <summary class="cursor-pointer flex items-center space-x-2 text-xs font-bold text-yellow-400">
                    <span>❗ 查看强势股（${sector.stocks.length}只）</span>
                  </summary>
                  <div class="mt-3 space-y-2">
                    ${sector.stocks.map(function(stock) {
                      var scoreColor = stock.score >= 85 ? 'text-green-400' : stock.score >= 75 ? 'text-blue-400' : 'text-gray-400';
                      return '<div class="bg-white/5 rounded-lg p-3">' +
                        '<div class="flex items-center justify-between mb-2">' +
                        '<div><div class="font-medium">' + stock.name + '</div></div>' +
                        '<div class="text-right"><div class="text-lg font-bold">' + stock.changePct.toFixed(2) + '%</div></div>' +
                        '</div>' +
                        '<div class="flex items-center justify-between">' +
                        '<span class="text-xs ' + scoreColor + '">评分：' + stock.score + '</span>' +
                        '</div></div>';
                    }).join('')}
                  </div>
                </details>
              ` : ''}
            </div>
          ` : ''}
        </div>
      `;
    }
    
    html += `
          </div>
        </div>
        
        <!-- 持仓表现 -->
        <div class="card p-6">
          <h4 class="text-lg font-bold mb-4 flex items-center">
            <span class="text-xl mr-2">💰</span>
            持仓表现
          </h4>
          <div class="space-y-4">
    `;
    
    for (const h of session.holdings) {
      const changeColor = h.changePct >= 0 ? 'text-up' : 'text-down';
      const profitColor = h.profit >= 0 ? 'text-up' : 'text-down';
      
      html += `
        <div class="bg-white/5 rounded-lg p-6">
          <div class="flex items-center justify-between mb-4">
            <div>
              <h5 class="text-xl font-bold">${h.name} <span class="text-sm text-gray-400">(${h.code})</span></h5>
              <div class="text-sm text-gray-400 mt-1">${h.notes || ''}</div>
            </div>
            <div class="text-right">
              <div class="text-3xl font-bold ${changeColor}">${h.changePct >= 0 ? '+' : ''}${h.changePct.toFixed(2)}%</div>
              <div class="text-sm text-gray-400">量比：${h.volumeRatio.toFixed(2)}</div>
            </div>
          </div>
          
          <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
            <div class="bg-white/5 rounded-lg p-3 text-center">
              <div class="text-xs text-gray-400">现价</div>
              <div class="text-lg font-mono">${h.price.toFixed(2)}</div>
            </div>
            <div class="bg-white/5 rounded-lg p-3 text-center">
              <div class="text-xs text-gray-400">盈亏</div>
              <div class="text-lg font-mono ${profitColor}">${h.profit >= 0 ? '+' : ''}${h.profit.toFixed(2)}元</div>
            </div>
            <div class="bg-white/5 rounded-lg p-3 text-center">
              <div class="text-xs text-gray-400">盈亏%</div>
              <div class="text-lg font-mono ${profitColor}">${h.profitPct >= 0 ? '+' : ''}${h.profitPct.toFixed(2)}%</div>
            </div>
            <div class="bg-white/5 rounded-lg p-3 text-center">
              <div class="text-xs text-gray-400">换手</div>
              <div class="text-lg font-mono">${h.turnover.toFixed(2)}%</div>
            </div>
          </div>
          
          ${h.riseLogic && Array.isArray(h.riseLogic) ? `
            <div class="mb-4">
              <h6 class="text-sm font-bold text-blue-400 mb-2">📊 为什么涨:</h6>
              <div class="space-y-1">
                ${h.riseLogic.map(l => `<div class="text-sm text-gray-300">${l}</div>`).join('')}
              </div>
            </div>
          ` : ''}
          
          ${h.mainForceIntention ? `
            <div class="mb-4">
              <h6 class="text-sm font-bold text-purple-400 mb-2">💰 主力意图:</h6>
              <div class="text-sm text-gray-300">${h.mainForceIntention}</div>
              ${h.mainForceAnalysis ? `<div class="text-xs text-gray-400 mt-1">${h.mainForceAnalysis}</div>` : ''}
            </div>
          ` : ''}
          
          ${h.technicalPosition ? `
            <div class="mb-4">
              <h6 class="text-sm font-bold text-green-400 mb-2">📈 技术位置:</h6>
              <div class="text-sm text-gray-300">${h.technicalPosition}</div>
              ${h.technicalAnalysis ? `<div class="text-xs text-gray-400 mt-1">${h.technicalAnalysis}</div>` : ''}
            </div>
          ` : ''}
          
          ${h.targetPrice ? `
            <div class="mb-4">
              <h6 class="text-sm font-bold text-green-400 mb-2">🎯 目标价：${h.targetPrice.toFixed(2)}元</h6>
              ${h.targetAnalysis ? `<div class="text-xs text-gray-400">${h.targetAnalysis}</div>` : ''}
            </div>
          ` : ''}
          
          ${h.stopLoss ? `
            <div class="mb-4">
              <h6 class="text-sm font-bold text-red-400 mb-2">⛔ 止损价：${h.stopLoss.toFixed(2)}元</h6>
              ${h.stopLossAnalysis ? `<div class="text-xs text-gray-400">${h.stopLossAnalysis}</div>` : ''}
            </div>
          ` : ''}
          
          ${h.targetAnalysis ? `
            <div class="mb-4">
              <h6 class="text-sm font-bold text-green-400 mb-2">🎯 目标价分析:</h6>
              <div class="text-sm text-gray-300">${h.targetAnalysis}</div>
            </div>
          ` : ''}
          
          ${h.stopLossAnalysis ? `
            <div class="mb-4">
              <h6 class="text-sm font-bold text-red-400 mb-2">⛔ 止损逻辑:</h6>
              <div class="text-sm text-gray-300">${h.stopLossAnalysis}</div>
            </div>
          ` : ''}
          
          ${h.holdAnalysis ? `
            <div class="mb-4">
              <h6 class="text-sm font-bold text-blue-400 mb-2">💡 持有逻辑:</h6>
              <div class="text-sm text-gray-300">${h.holdAnalysis}</div>
            </div>
          ` : ''}
          
          ${h.technical ? `
            <div class="mb-4">
              <h6 class="text-sm font-bold text-green-400 mb-2">技术分析:</h6>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-2">
                ${h.technical.map(t => `<div class="text-sm text-gray-300">${t}</div>`).join('')}
              </div>
            </div>
          ` : ''}
          
          ${h.capital ? `
            <div class="mb-4">
              <h6 class="text-sm font-bold text-blue-400 mb-2">资金面:</h6>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-2">
                ${h.capital.map(c => `<div class="text-sm text-gray-300">${c}</div>`).join('')}
              </div>
            </div>
          ` : ''}
          
          ${h.analysis ? `
            <div class="mb-4">
              <h6 class="text-sm font-bold mb-2">分析:</h6>
              <div class="space-y-1">
                ${h.analysis.map(a => `<div class="text-sm text-gray-300">${a}</div>`).join('')}
              </div>
            </div>
          ` : ''}
          
          <div class="bg-blue-500/10 border border-blue-500/30 rounded-lg p-4">
            <div class="flex items-center justify-between">
              <div>
                <span class="text-sm text-gray-400">操作建议:</span>
                <span class="text-lg font-bold ml-2">${h.advice}</span>
              </div>
              ${h.targetPrice ? `
                <div class="text-right">
                  <div class="text-xs text-gray-400">目标价</div>
                  <div class="text-lg font-bold text-green-400">${h.targetPrice.toFixed(2)}元</div>
                </div>
              ` : ''}
              ${h.stopLoss ? `
                <div class="text-right">
                  <div class="text-xs text-gray-400">止损价</div>
                  <div class="text-lg font-bold text-red-400">${h.stopLoss.toFixed(2)}元</div>
                </div>
              ` : ''}
            </div>
          </div>
        </div>
      `;
    }
    
    html += `
          </div>
        </div>
    `;
    
    // 龙虎榜（仅收盘总结有）
    if (session.dragonTiger) {
      const dt = session.dragonTiger;
      html += `
        <div class="card p-6">
          <h4 class="text-lg font-bold mb-4 flex items-center">
            <span class="text-xl mr-2">🐉</span>
            龙虎榜 - ${dt.name}
            <span class="text-sm text-gray-400 ml-2">(${dt.reason})</span>
          </h4>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <h5 class="text-sm font-bold text-green-400 mb-3">💰 买入席位</h5>
              <div class="space-y-2">
                ${dt.seats.buy.map((seat, i) => `
                  <div class="bg-green-500/10 border border-green-500/30 rounded-lg p-3">
                    <div class="flex items-center justify-between">
                      <div>
                        <div class="font-medium">${seat.name}</div>
                        <div class="text-xs text-gray-400">买入：${seat.buy}万 / 卖出：${seat.sell}万</div>
                      </div>
                      <div class="text-lg font-bold text-green-400">+${seat.net}万</div>
                    </div>
                  </div>
                `).join('')}
              </div>
            </div>
            <div class="card p-4 bg-blue-500/10 border border-blue-500/30">
              <div class="text-center">
                <div class="text-sm text-gray-400">净买入总计</div>
                <div class="text-4xl font-bold text-green-400 mt-2">+${dt.seats.total.net}万</div>
                <div class="text-sm text-gray-400 mt-4">
                  买入：${dt.seats.total.buy}万 / 卖出：${dt.seats.total.sell}万
                </div>
              </div>
            </div>
          </div>
        </div>
      `;
    }
    
    // 明日展望（仅收盘总结有）
    if (session.outlook) {
      const o = session.outlook;
      html += `
        <div class="card p-6">
          <h4 class="text-lg font-bold mb-4 flex items-center">
            <span class="text-xl mr-2">📌</span>
            明日展望
          </h4>
          
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
            <div>
              <h5 class="text-sm font-bold text-green-400 mb-3">✅ 利好因素</h5>
              <div class="space-y-2">
                ${o.positive.map(p => `<div class="text-sm text-gray-300">${p}</div>`).join('')}
              </div>
            </div>
            <div>
              <h5 class="text-sm font-bold text-red-400 mb-3">⚠️ 风险因素</h5>
              <div class="space-y-2">
                ${o.negative.map(n => `<div class="text-sm text-gray-300">${n}</div>`).join('')}
              </div>
            </div>
          </div>
          
          <div class="mb-6">
            <h5 class="text-sm font-bold mb-3">📝 操作策略</h5>
            <div class="bg-white/5 rounded-lg p-4">
              <div class="space-y-2">
                ${o.strategy.map(s => `<div class="text-sm text-gray-300">${s}</div>`).join('')}
              </div>
            </div>
          </div>
          
          <div>
            <h5 class="text-sm font-bold mb-3">🎯 重点关注</h5>
            <div class="space-y-2">
              ${o.focus.map(f => `<div class="text-sm text-gray-300">${f}</div>`).join('')}
            </div>
          </div>
          
          ${o.deepThinking ? `
            <div class="mt-6 bg-gradient-to-r from-blue-500/10 to-purple-500/10 border border-blue-500/30 rounded-lg p-6">
              <h5 class="text-sm font-bold text-blue-400 mb-3">🤔 深度思考</h5>
              <div class="text-sm text-gray-300 leading-relaxed">${o.deepThinking}</div>
            </div>
          ` : ''}
        </div>
      `;
    }
    
    // 策略（午盘/尾盘）
    if (session.strategy && !session.outlook) {
      const s = session.strategy;
      html += `
        <div class="card p-6">
          <h4 class="text-lg font-bold mb-4 flex items-center">
            <span class="text-xl mr-2">📌</span>
            操作策略
          </h4>
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div class="bg-white/5 rounded-lg p-4 text-center">
              <div class="text-sm text-gray-400">仓位建议</div>
              <div class="text-xl font-bold">${s.position}</div>
            </div>
            ${Array.isArray(s.focus) ? `
              <div class="bg-white/5 rounded-lg p-4">
                <div class="text-sm text-gray-400 mb-2">关注方向</div>
                <div class="space-y-1">
                  ${s.focus.map(f => `<div class="text-sm">${f}</div>`).join('')}
                </div>
              </div>
            ` : `
              <div class="bg-white/5 rounded-lg p-4 text-center">
                <div class="text-sm text-gray-400">关注方向</div>
                <div class="text-xl">${s.focus}</div>
              </div>
            `}
            ${Array.isArray(s.risk) ? `
              <div class="bg-white/5 rounded-lg p-4">
                <div class="text-sm text-gray-400 mb-2">风险提示</div>
                <div class="space-y-1">
                  ${s.risk.map(r => `<div class="text-sm">${r}</div>`).join('')}
                </div>
              </div>
            ` : `
              <div class="bg-white/5 rounded-lg p-4 text-center">
                <div class="text-sm text-gray-400">风险提示</div>
                <div class="text-xl">${s.risk}</div>
              </div>
            `}
          </div>
        </div>
      `;
    }
    
    html += `
        <!-- 免责声明 -->
        <div class="text-center text-xs text-gray-500 py-4">
          ⚠️ 免责声明：以上分析仅供参考，不构成投资建议。股市有风险，投资需谨慎。
        </div>
      </div>
    `;
    
    contentDiv.innerHTML = html;
  } catch (error) {
    console.error('加载复盘报告失败:', error);
    contentDiv.innerHTML = `
      <div class="text-center text-gray-400 py-12">
        <div class="text-6xl mb-4">📊</div>
        <div>加载复盘报告失败</div>
        <div class="text-sm mt-2">${error.message}</div>
      </div>
    `;
  }
}

/**
 * 简单的 Markdown 转 HTML
 */
function markdownToHtml(markdown) {
  return markdown
    .replace(/^# (.*$)/gm, '<h1 class="text-2xl font-bold mb-4 mt-6">$1</h1>')
    .replace(/^## (.*$)/gm, '<h2 class="text-xl font-bold mb-3 mt-6">$1</h2>')
    .replace(/^### (.*$)/gm, '<h3 class="text-lg font-bold mb-2 mt-4">$1</h3>')
    .replace(/^\- (.*$)/gm, '<li class="ml-4">$1</li>')
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/\n/g, '<br>');
}

/**
 * 立即检查持仓
 */
async function checkHoldings() {
  const button = event.target;
  const originalText = button.textContent;
  button.textContent = '检查中...';
  button.disabled = true;
  
  try {
    // 这里应该调用后端 API，暂时只是刷新显示
    await loadHoldings();
  } catch (error) {
    console.error('检查持仓失败:', error);
  } finally {
    button.textContent = originalText;
    button.disabled = false;
  }
}

/**
 * 刷新数据
 */
function refreshData() {
  console.log('🔄 刷新数据...');
  loadMarketData();
  loadHoldings();
}

/**
 * 启动自动刷新
 */
function startAutoRefresh() {
  if (state.refreshTimer) {
    clearInterval(state.refreshTimer);
  }
  
  state.refreshTimer = setInterval(() => {
    refreshData();
  }, CONFIG.refreshInterval);
  
  console.log(`⏱️ 自动刷新已启动，间隔 ${CONFIG.refreshInterval / 1000} 秒`);
}

/**
 * 停止自动刷新
 */
function stopAutoRefresh() {
  if (state.refreshTimer) {
    clearInterval(state.refreshTimer);
    state.refreshTimer = null;
  }
}

// 页面可见性变化时控制刷新
document.addEventListener('visibilitychange', () => {
  if (document.hidden) {
    stopAutoRefresh();
    console.log('⏸️ 页面隐藏，暂停刷新');
  } else {
    startAutoRefresh();
    console.log('▶️ 页面显示，恢复刷新');
  }
});

/**
 * 加载公告数据
 */
async function loadAnnouncements() {
  const contentDiv = document.getElementById('announcements-content');
  contentDiv.innerHTML = `
    <div class="flex flex-col items-center justify-center py-12">
      <div class="loading mb-4"></div>
      <div class="text-gray-400">加载公告数据...</div>
    </div>
  `;
  
  try {
    const response = await fetch(`${CONFIG.dataPath}/announcements.json?t=${Date.now()}`);
    const data = await response.json();
    
    if (!data.announcements || data.announcements.length === 0) {
      contentDiv.innerHTML = `
        <div class="text-center text-gray-400 py-12">
          <div class="text-6xl mb-4">📢</div>
          <div>暂无公告数据</div>
        </div>
      `;
      return;
    }
    
    // 分类统计
    const positive = data.announcements.filter(a => a.type === 'positive');
    const negative = data.announcements.filter(a => a.type === 'negative');
    const neutral = data.announcements.filter(a => a.type === 'neutral');
    
    let html = `
      <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
        <div class="card p-4 text-center">
          <div class="text-2xl font-bold text-blue-400">${data.count}</div>
          <div class="text-sm text-gray-400">总公告数</div>
        </div>
        <div class="card p-4 text-center">
          <div class="text-2xl font-bold text-green-400">${positive.length}</div>
          <div class="text-sm text-gray-400">利好公告</div>
        </div>
        <div class="card p-4 text-center">
          <div class="text-2xl font-bold text-red-400">${negative.length}</div>
          <div class="text-sm text-gray-400">利空公告</div>
        </div>
        <div class="card p-4 text-center">
          <div class="text-2xl font-bold text-gray-400">${neutral.length}</div>
          <div class="text-sm text-gray-400">中性公告</div>
        </div>
      </div>
      
      <div class="space-y-4">
    `;
    
    for (const item of data.announcements) {
      let bgColor = 'bg-blue-500/10';
      let borderColor = 'border-blue-500/30';
      let icon = 'ℹ️';
      let label = '中性';
      
      if (item.type === 'positive') {
        bgColor = 'bg-green-500/10';
        borderColor = 'border-green-500/30';
        icon = '✅';
        label = '利好';
      } else if (item.type === 'negative') {
        bgColor = 'bg-red-500/10';
        borderColor = 'border-red-500/30';
        icon = '❌';
        label = '利空';
      }
      
      html += `
        <div class="${bgColor} border ${borderColor} rounded-lg p-4">
          <div class="flex items-start space-x-3">
            <span class="text-2xl">${icon}</span>
            <div class="flex-1">
              <div class="flex items-center space-x-2 mb-2">
                <span class="font-bold text-white">${item.name}</span>
                <span class="text-xs text-gray-500">${item.code}</span>
                <span class="px-2 py-1 ${item.type === 'positive' ? 'bg-green-500/20 text-green-400' : item.type === 'negative' ? 'bg-red-500/20 text-red-400' : 'bg-gray-500/20 text-gray-400'} rounded text-xs">${label}</span>
              </div>
              <div class="text-sm text-gray-300 mb-1">${item.title}</div>
              <div class="text-xs text-gray-500">日期：${item.date}</div>
              ${item.summary ? `<div class="text-xs text-gray-400 mt-2">${item.summary}</div>` : ''}
            </div>
          </div>
        </div>
      `;
    }
    
    html += `</div>`;
    contentDiv.innerHTML = html;
  } catch (error) {
    console.error('加载公告数据失败:', error);
    contentDiv.innerHTML = `
      <div class="text-center text-gray-400 py-12">
        <div class="text-6xl mb-4">📢</div>
        <div>加载公告数据失败</div>
        <div class="text-sm mt-2">${error.message}</div>
      </div>
    `;
  }
}

/**
 * 加载龙虎榜数据
 */
async function loadDragonTiger() {
  const contentDiv = document.getElementById('dragon-tiger-content');
  contentDiv.innerHTML = `
    <div class="flex flex-col items-center justify-center py-12">
      <div class="loading mb-4"></div>
      <div class="text-gray-400">加载龙虎榜数据...</div>
    </div>
  `;
  
  try {
    const response = await fetch(`${CONFIG.dataPath}/dragon_tiger.json?t=${Date.now()}`);
    const data = await response.json();
    
    if (!data.data || data.data.length === 0) {
      contentDiv.innerHTML = `
        <div class="text-center text-gray-400 py-12">
          <div class="text-6xl mb-4">🐉</div>
          <div>今日无龙虎榜数据</div>
          <div class="text-sm mt-2">只有涨跌幅偏离值达 7%、换手率超 20% 等情况下才会上龙虎榜</div>
        </div>
      `;
      return;
    }
    
    let html = '';
    
    for (const item of data.data) {
      const netColor = item.netAmount > 0 ? 'text-green-400' : 'text-red-400';
      const netSign = item.netAmount > 0 ? '+' : '';
      
      html += `
        <div class="mb-8 last:mb-0">
          <div class="flex items-center justify-between mb-4">
            <div>
              <h3 class="text-xl font-bold">${item.name} <span class="text-sm text-gray-400">(${item.code})</span></h3>
              <div class="text-sm text-gray-400 mt-1">${item.date}</div>
            </div>
            <div class="text-right">
              <div class="text-2xl font-bold ${netColor}">${netSign}${(item.netAmount / 1e4).toFixed(2)}万元</div>
              <div class="text-xs text-gray-400">净买卖</div>
            </div>
          </div>
          
          <div class="grid grid-cols-2 md:grid-cols-5 gap-4 mb-4">
            <div class="card p-3 text-center">
              <div class="text-xs text-gray-400">收盘价</div>
              <div class="text-lg font-mono">${item.closePrice}</div>
            </div>
            <div class="card p-3 text-center">
              <div class="text-xs text-gray-400">涨跌幅</div>
              <div class="text-lg font-mono ${item.changePct >= 0 ? 'text-up' : 'text-down'}">${item.changePct}%</div>
            </div>
            <div class="card p-3 text-center">
              <div class="text-xs text-gray-400">机构净买卖</div>
              <div class="text-lg font-mono ${(item.institutionalBuy - item.institutionalSell) > 0 ? 'text-green-400' : 'text-red-400'}'>${((item.institutionalBuy - item.institutionalSell) / 1e4).toFixed(1)}万</div>
            </div>
            <div class="card p-3 text-center">
              <div class="text-xs text-gray-400">游资净买卖</div>
              <div class="text-lg font-mono ${(item.hotMoneyBuy - item.hotMoneySell) > 0 ? 'text-green-400' : 'text-red-400'}'>${((item.hotMoneyBuy - item.hotMoneySell) / 1e4).toFixed(1)}万</div>
            </div>
            <div class="card p-3 text-center">
              <div class="text-xs text-gray-400">北向净买卖</div>
              <div class="text-lg font-mono ${(item.northboundBuy - item.northboundSell) > 0 ? 'text-green-400' : 'text-red-400'}'>${((item.northboundBuy - item.northboundSell) / 1e4).toFixed(1)}万</div>
            </div>
          </div>
          
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <h4 class="text-sm font-bold text-green-400 mb-2">💰 买入席位</h4>
              <div class="space-y-2">
                ${item.buySeats.map((seat, i) => `
                  <div class="flex items-center justify-between bg-green-500/10 border border-green-500/30 rounded-lg px-4 py-2">
                    <div>
                      <div class="font-medium">${seat.name}</div>
                      <div class="text-xs text-gray-400">${seat.type}</div>
                    </div>
                    <div class="font-mono text-green-400">${(seat.amount / 1e4).toFixed(2)}万</div>
                  </div>
                `).join('')}
              </div>
            </div>
            
            <div>
              <h4 class="text-sm font-bold text-red-400 mb-2">💸 卖出席位</h4>
              <div class="space-y-2">
                ${item.sellSeats.map((seat, i) => `
                  <div class="flex items-center justify-between bg-red-500/10 border border-red-500/30 rounded-lg px-4 py-2">
                    <div>
                      <div class="font-medium">${seat.name}</div>
                      <div class="text-xs text-gray-400">${seat.type}</div>
                    </div>
                    <div class="font-mono text-red-400">${(seat.amount / 1e4).toFixed(2)}万</div>
                  </div>
                `).join('')}
              </div>
            </div>
          </div>
          
          <div class="mt-4 p-4 bg-blue-500/10 border border-blue-500/30 rounded-lg">
            <div class="text-sm text-gray-300"><span class="font-bold">📊 分析:</span> ${item.summary}</div>
          </div>
        </div>
      `;
    }
    
    contentDiv.innerHTML = html;
  } catch (error) {
    console.error('加载龙虎榜数据失败:', error);
    contentDiv.innerHTML = `
      <div class="text-center text-gray-400 py-12">
        <div class="text-6xl mb-4">🐉</div>
        <div>加载龙虎榜数据失败</div>
        <div class="text-sm mt-2">${error.message}</div>
      </div>
    `;
  }
}

/**
 * 加载财报日历
 */
async function loadEarningsCalendar() {
  const contentDiv = document.getElementById('earnings-content');
  contentDiv.innerHTML = `
    <div class="flex flex-col items-center justify-center py-12">
      <div class="loading mb-4"></div>
      <div class="text-gray-400">加载财报日历...</div>
    </div>
  `;
  
  try {
    const response = await fetch(`${CONFIG.dataPath}/earnings_calendar.json?t=${Date.now()}`);
    const data = await response.json();
    
    if (!data.calendar || data.calendar.length === 0) {
      contentDiv.innerHTML = `
        <div class="text-center text-gray-400 py-12">
          <div class="text-6xl mb-4">📅</div>
          <div>暂无财报日历数据</div>
        </div>
      `;
      return;
    }
    
    // 分类
    const urgent = data.calendar.filter(c => c.daysUntil <= 5);
    const soon = data.calendar.filter(c => c.daysUntil > 5 && c.daysUntil <= 15);
    const normal = data.calendar.filter(c => c.daysUntil > 15);
    
    let html = `
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        <div class="card p-4 text-center border-l-4 border-red-500">
          <div class="text-2xl font-bold text-red-400">${urgent.length}</div>
          <div class="text-sm text-gray-400">临近财报（&lt;5 天）</div>
        </div>
        <div class="card p-4 text-center border-l-4 border-yellow-500">
          <div class="text-2xl font-bold text-yellow-400">${soon.length}</div>
          <div class="text-sm text-gray-400">近期财报（5-15 天）</div>
        </div>
        <div class="card p-4 text-center border-l-4 border-green-500">
          <div class="text-2xl font-bold text-green-400">${normal.length}</div>
          <div class="text-sm text-gray-400">远期财报（&gt;15 天）</div>
        </div>
      </div>
    `;
    
    if (urgent.length > 0) {
      html += `
        <div class="mb-6">
          <h3 class="text-lg font-bold text-red-400 mb-3">🚨 临近财报（&lt;5 天）</h3>
          <div class="space-y-3">
      `;
      
      for (const item of urgent) {
        const date = new Date(item.estimatedDate);
        const dateStr = `${date.getMonth() + 1}月${date.getDate()}日`;
        
        html += `
          <div class="bg-red-500/10 border border-red-500/30 rounded-lg p-4">
            <div class="flex items-center justify-between">
              <div>
                <div class="font-bold">${item.name} <span class="text-sm text-gray-400">(${item.code})</span></div>
                <div class="text-sm text-gray-400 mt-1">${item.earningsType}</div>
              </div>
              <div class="text-right">
                <div class="text-2xl font-bold text-red-400">${item.daysUntil}天</div>
                <div class="text-xs text-gray-400">${dateStr}</div>
              </div>
            </div>
            <div class="mt-2 flex items-center space-x-2">
              <span class="text-xs px-2 py-1 ${item.forecast === '预增' || item.forecast === '预盈' ? 'bg-green-500/20 text-green-400' : item.forecast === '预减' || item.forecast === '预亏' ? 'bg-red-500/20 text-red-400' : 'bg-gray-500/20 text-gray-400'} rounded">
                预报：${item.forecast}
              </span>
              <span class="text-xs text-gray-500">${item.isEstimated ? '估算' : '官方'}</span>
            </div>
          </div>
        `;
      }
      
      html += `</div></div>`;
    }
    
    // 近期和远期财报（简化显示）
    const remaining = [...soon, ...normal].slice(0, 10);
    if (remaining.length > 0) {
      html += `
        <div>
          <h3 class="text-lg font-bold text-gray-400 mb-3">📅 其他财报</h3>
          <div class="space-y-2">
      `;
      
      for (const item of remaining) {
        const date = new Date(item.estimatedDate);
        const dateStr = `${date.getMonth() + 1}月${date.getDate()}日`;
        
        html += `
          <div class="flex items-center justify-between bg-white/5 rounded-lg px-4 py-2">
            <div>
              <span class="font-medium">${item.name}</span>
              <span class="text-sm text-gray-400 ml-2">(${item.code})</span>
              <span class="text-sm text-gray-500 ml-2">${item.earningsType}</span>
            </div>
            <div class="text-sm text-gray-400">${dateStr}（${item.daysUntil}天后）</div>
          </div>
        `;
      }
      
      html += `</div></div>`;
    }
    
    contentDiv.innerHTML = html;
  } catch (error) {
    console.error('加载财报日历数据失败:', error);
    contentDiv.innerHTML = `
      <div class="text-center text-gray-400 py-12">
        <div class="text-6xl mb-4">📅</div>
        <div>加载财报日历失败</div>
        <div class="text-sm mt-2">${error.message}</div>
      </div>
    `;
  }
}

/**
 * 加载选股结果
 */
async function loadScreenerResults() {
  const contentDiv = document.getElementById('screener-content');
  contentDiv.innerHTML = `
    <div class="flex flex-col items-center justify-center py-12">
      <div class="loading mb-4"></div>
      <div class="text-gray-400">加载选股结果...</div>
    </div>
  `;
  
  try {
    const response = await fetch(`${CONFIG.dataPath}/screener_results.json?t=${Date.now()}`);
    const data = await response.json();
    
    if (!data.results || data.results.length === 0) {
      contentDiv.innerHTML = `
        <div class="text-center text-gray-400 py-12">
          <div class="text-6xl mb-4">🎯</div>
          <div>暂无选股结果</div>
          <div class="text-sm mt-2">请先运行选股脚本</div>
        </div>
      `;
      return;
    }
    
    // 表格头部
    let html = `
      <div class="overflow-x-auto">
        <table class="w-full">
          <thead class="bg-white/5 border-b border-gray-700">
            <tr>
              <th class="px-6 py-4 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">排名</th>
              <th class="px-6 py-4 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">股票</th>
              <th class="px-6 py-4 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">现价</th>
              <th class="px-6 py-4 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">今日</th>
              <th class="px-6 py-4 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">量比</th>
              <th class="px-6 py-4 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">评分</th>
              <th class="px-6 py-4 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">评级</th>
              <th class="px-6 py-4 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">亮点</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-700">
    `;
    
    // 排序
    const sortedResults = data.results.sort((a, b) => b.score - a.score);
    
    for (let i = 0; i < sortedResults.length; i++) {
      const stock = sortedResults[i];
      const rank = i + 1;
      const rankColor = rank <= 3 ? 'text-yellow-400' : 'text-gray-400';
      const starColor = stock.rating.includes('⭐⭐⭐⭐⭐') ? 'text-green-400' : stock.rating.includes('⭐⭐⭐⭐') ? 'text-blue-400' : 'text-gray-400';
      
      html += `
        <tr class="hover:bg-white/5 transition-colors">
          <td class="px-6 py-4">
            <span class="text-lg font-bold ${rankColor}">#${rank}</span>
          </td>
          <td class="px-6 py-4">
            <div>
              <div class="font-bold text-white">${stock.name}</div>
              <div class="text-xs text-gray-500">${stock.code}</div>
            </div>
          </td>
          <td class="px-6 py-4">
            <div class="font-mono">${stock.price.toFixed(2)}</div>
          </td>
          <td class="px-6 py-4">
            <div class="font-mono ${stock.changePct >= 0 ? 'text-up' : 'text-down'}">
              ${stock.changePct >= 0 ? '+' : ''}${stock.changePct.toFixed(2)}%
            </div>
          </td>
          <td class="px-6 py-4">
            <div class="font-mono text-gray-400">${stock.volumeRatio.toFixed(2)}</div>
          </td>
          <td class="px-6 py-4">
            <div class="font-mono font-bold ${stock.score >= 80 ? 'text-green-400' : stock.score >= 70 ? 'text-blue-400' : 'text-gray-400'}">
              ${stock.score}
            </div>
          </td>
          <td class="px-6 py-4">
            <span class="${starColor}">${stock.rating}</span>
          </td>
          <td class="px-6 py-4">
            <div class="flex flex-wrap gap-1">
              ${stock.reasons.map(r => `<span class="px-2 py-1 bg-blue-500/20 text-blue-400 rounded text-xs">${r}</span>`).join('')}
            </div>
          </td>
        </tr>
      `;
    }
    
    html += `</tbody></table></div>`;
    contentDiv.innerHTML = html;
  } catch (error) {
    console.error('加载选股结果失败:', error);
    contentDiv.innerHTML = `
      <div class="text-center text-gray-400 py-12">
        <div class="text-6xl mb-4">🎯</div>
        <div>加载选股结果失败</div>
        <div class="text-sm mt-2">${error.message}</div>
      </div>
    `;
  }
}

// 页面加载时初始化所有模块
window.addEventListener('DOMContentLoaded', () => {
  // 延迟加载其他模块数据
  setTimeout(() => {
    loadAnnouncements();
    loadDragonTiger();
    loadEarningsCalendar();
    loadScreenerResults();
  }, 1000);
});
