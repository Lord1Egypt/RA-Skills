/**
 * 售后分析报表数据模型
 * 
 * 提供售后数据分析的核心逻辑：
 * - 投诉统计（按类型/状态/客户/产品）
 * - 返单统计（转化率/金额/客户）
 * - 满意度统计（平均分/分布/趋势）
 * - 客户风险分析
 * - 产品质量分析
 */

const dayjs = require('dayjs');

// 模拟数据源（实际应用中应从数据库获取）
const mockData = {
  // 投诉数据
  complaints: [
    {
      id: 'CMP-001',
      customerId: 'CUST-001',
      customerName: 'ABC Trading Ltd.',
      productId: 'PROD-001',
      productName: 'HDMI Cable 2.0',
      type: 'quality',
      status: 'resolved',
      description: 'Cable stopped working after 2 weeks',
      createdAt: '2026-03-10',
      resolvedAt: '2026-03-15',
      severity: 'medium'
    },
    {
      id: 'CMP-002',
      customerId: 'CUST-002',
      customerName: 'XYZ Electronics Inc.',
      productId: 'PROD-003',
      productName: 'USB-C Cable',
      type: 'delivery',
      status: 'pending',
      description: 'Delivery delayed by 1 week',
      createdAt: '2026-03-20',
      resolvedAt: null,
      severity: 'low'
    },
    {
      id: 'CMP-003',
      customerId: 'CUST-003',
      customerName: 'Global Tech Solutions',
      productId: 'PROD-002',
      productName: 'DP Cable 1.4',
      type: 'quality',
      status: 'resolved',
      description: 'Connector loose, poor contact',
      createdAt: '2026-03-05',
      resolvedAt: '2026-03-12',
      severity: 'high'
    },
    {
      id: 'CMP-004',
      customerId: 'CUST-001',
      customerName: 'ABC Trading Ltd.',
      productId: 'PROD-004',
      productName: 'LAN Cable CAT6A',
      type: 'packaging',
      status: 'resolved',
      description: 'Packaging damaged during shipping',
      createdAt: '2026-03-18',
      resolvedAt: '2026-03-22',
      severity: 'low'
    },
    {
      id: 'CMP-005',
      customerId: 'CUST-004',
      customerName: 'Premium Cables Co.',
      productId: 'PROD-001',
      productName: 'HDMI Cable 2.0',
      type: 'quality',
      status: 'pending',
      description: 'Signal intermittent issues',
      createdAt: '2026-03-25',
      resolvedAt: null,
      severity: 'high'
    }
  ],

  // 返单数据
  repeatOrders: [
    {
      id: 'RO-001',
      customerId: 'CUST-001',
      customerName: 'ABC Trading Ltd.',
      initialOrderId: 'ORD-100',
      repeatOrderId: 'ORD-150',
      initialOrderDate: '2026-01-15',
      repeatOrderDate: '2026-03-10',
      initialAmount: 50000,
      repeatAmount: 75000,
      daysToRepeat: 54,
      status: 'completed'
    },
    {
      id: 'RO-002',
      customerId: 'CUST-002',
      customerName: 'XYZ Electronics Inc.',
      initialOrderId: 'ORD-105',
      repeatOrderId: 'ORD-160',
      initialOrderDate: '2026-02-01',
      repeatOrderDate: '2026-03-20',
      initialAmount: 120000,
      repeatAmount: 150000,
      daysToRepeat: 47,
      status: 'completed'
    },
    {
      id: 'RO-003',
      customerId: 'CUST-005',
      customerName: 'Tech Distributors LLC',
      initialOrderId: 'ORD-110',
      repeatOrderId: null,
      initialOrderDate: '2026-01-20',
      repeatOrderDate: null,
      initialAmount: 80000,
      repeatAmount: 0,
      daysToRepeat: null,
      status: 'pending'
    }
  ],

  // 满意度调查数据
  satisfactionSurveys: [
    {
      id: 'SRV-001',
      customerId: 'CUST-001',
      customerName: 'ABC Trading Ltd.',
      orderId: 'ORD-150',
      overallScore: 4,
      qualityScore: 5,
      serviceScore: 4,
      deliveryScore: 3,
      communicationScore: 4,
      feedback: 'Good quality, but delivery was slow',
      createdAt: '2026-03-12'
    },
    {
      id: 'SRV-002',
      customerId: 'CUST-002',
      customerName: 'XYZ Electronics Inc.',
      orderId: 'ORD-160',
      overallScore: 5,
      qualityScore: 5,
      serviceScore: 5,
      deliveryScore: 5,
      communicationScore: 5,
      feedback: 'Excellent service and product quality!',
      createdAt: '2026-03-22'
    },
    {
      id: 'SRV-003',
      customerId: 'CUST-003',
      customerName: 'Global Tech Solutions',
      orderId: 'ORD-145',
      overallScore: 3,
      qualityScore: 3,
      serviceScore: 4,
      deliveryScore: 4,
      communicationScore: 3,
      feedback: 'Product quality issues, needs improvement',
      createdAt: '2026-03-15'
    },
    {
      id: 'SRV-004',
      customerId: 'CUST-004',
      customerName: 'Premium Cables Co.',
      orderId: 'ORD-155',
      overallScore: 4,
      qualityScore: 4,
      serviceScore: 5,
      deliveryScore: 4,
      communicationScore: 4,
      feedback: 'Very satisfied with the service',
      createdAt: '2026-03-25'
    }
  ],

  // 客户数据
  customers: [
    { customerId: 'CUST-001', customerName: 'ABC Trading Ltd.', riskLevel: 'low', totalOrders: 15, totalAmount: 500000 },
    { customerId: 'CUST-002', customerName: 'XYZ Electronics Inc.', riskLevel: 'low', totalOrders: 20, totalAmount: 750000 },
    { customerId: 'CUST-003', customerName: 'Global Tech Solutions', riskLevel: 'medium', totalOrders: 8, totalAmount: 200000 },
    { customerId: 'CUST-004', customerName: 'Premium Cables Co.', riskLevel: 'low', totalOrders: 12, totalAmount: 400000 },
    { customerId: 'CUST-005', customerName: 'Tech Distributors LLC', riskLevel: 'high', totalOrders: 3, totalAmount: 80000 }
  ],

  // 产品数据
  products: [
    { productId: 'PROD-001', productName: 'HDMI Cable 2.0', category: 'HDMI', defectRate: 0.02 },
    { productId: 'PROD-002', productName: 'DP Cable 1.4', category: 'DP', defectRate: 0.03 },
    { productId: 'PROD-003', productName: 'USB-C Cable', category: 'USB', defectRate: 0.015 },
    { productId: 'PROD-004', productName: 'LAN Cable CAT6A', category: 'LAN', defectRate: 0.01 }
  ]
};

/**
 * 解析日期范围
 * @param {string} dateRange - 日期范围字符串 (e.g., '2026-03-01_2026-03-31')
 * @returns {Object} { startDate, endDate }
 */
function parseDateRange(dateRange) {
  if (!dateRange) {
    // 默认返回最近 30 天
    return {
      startDate: dayjs().subtract(30, 'day').format('YYYY-MM-DD'),
      endDate: dayjs().format('YYYY-MM-DD')
    };
  }

  const [start, end] = dateRange.split('_');
  return {
    startDate: start || dayjs().subtract(30, 'day').format('YYYY-MM-DD'),
    endDate: end || dayjs().format('YYYY-MM-DD')
  };
}

/**
 * 检查日期是否在范围内
 * @param {string} date - 日期字符串
 * @param {string} startDate - 开始日期
 * @param {string} endDate - 结束日期
 * @returns {boolean}
 */
function isDateInRange(date, startDate, endDate) {
  const targetDate = dayjs(date);
  return targetDate.isAfter(dayjs(startDate).subtract(1, 'day')) && 
         targetDate.isBefore(dayjs(endDate).add(1, 'day'));
}

/**
 * 投诉统计模型
 * @param {string} dateRange - 日期范围
 * @returns {Object} 投诉统计数据
 */
function getComplaintStats(dateRange) {
  const { startDate, endDate } = parseDateRange(dateRange);
  
  // 过滤日期范围内的投诉
  const filteredComplaints = mockData.complaints.filter(c => 
    isDateInRange(c.createdAt, startDate, endDate)
  );

  // 按类型统计
  const byType = {};
  filteredComplaints.forEach(c => {
    byType[c.type] = (byType[c.type] || 0) + 1;
  });

  // 按状态统计
  const byStatus = {};
  filteredComplaints.forEach(c => {
    byStatus[c.status] = (byStatus[c.status] || 0) + 1;
  });

  // 按客户统计
  const byCustomer = {};
  filteredComplaints.forEach(c => {
    if (!byCustomer[c.customerId]) {
      byCustomer[c.customerId] = {
        customerId: c.customerId,
        customerName: c.customerName,
        count: 0
      };
    }
    byCustomer[c.customerId].count++;
  });

  // 按产品统计
  const byProduct = {};
  filteredComplaints.forEach(c => {
    if (!byProduct[c.productId]) {
      byProduct[c.productId] = {
        productId: c.productId,
        productName: c.productName,
        count: 0
      };
    }
    byProduct[c.productId].count++;
  });

  // 按严重程度统计
  const bySeverity = {};
  filteredComplaints.forEach(c => {
    bySeverity[c.severity] = (bySeverity[c.severity] || 0) + 1;
  });

  // 计算解决率
  const resolvedCount = filteredComplaints.filter(c => c.status === 'resolved').length;
  const resolutionRate = filteredComplaints.length > 0 
    ? ((resolvedCount / filteredComplaints.length) * 100).toFixed(2) 
    : 0;

  // 平均解决时间（天）
  const resolvedComplaints = filteredComplaints.filter(c => c.resolvedAt);
  const avgResolutionDays = resolvedComplaints.length > 0
    ? resolvedComplaints.reduce((sum, c) => {
        return sum + dayjs(c.resolvedAt).diff(dayjs(c.createdAt), 'day');
      }, 0) / resolvedComplaints.length
    : 0;

  return {
    summary: {
      total: filteredComplaints.length,
      resolved: resolvedCount,
      pending: filteredComplaints.length - resolvedCount,
      resolutionRate: `${resolutionRate}%`,
      avgResolutionDays: avgResolutionDays.toFixed(1)
    },
    byType,
    byStatus,
    byCustomer: Object.values(byCustomer),
    byProduct: Object.values(byProduct),
    bySeverity
  };
}

/**
 * 返单统计模型
 * @param {string} dateRange - 日期范围
 * @returns {Object} 返单统计数据
 */
function getRepeatOrderStats(dateRange) {
  const { startDate, endDate } = parseDateRange(dateRange);
  
  // 过滤日期范围内的返单
  const filteredOrders = mockData.repeatOrders.filter(o => 
    o.repeatOrderDate ? isDateInRange(o.repeatOrderDate, startDate, endDate) : false
  );

  // 所有初始订单（用于计算转化率）
  const allInitialOrders = mockData.repeatOrders.filter(o => 
    isDateInRange(o.initialOrderDate, startDate, endDate)
  );

  // 转化率
  const conversionRate = allInitialOrders.length > 0
    ? ((filteredOrders.length / allInitialOrders.length) * 100).toFixed(2)
    : 0;

  // 总返单金额
  const totalRepeatAmount = filteredOrders.reduce((sum, o) => sum + o.repeatAmount, 0);

  // 平均返单金额
  const avgRepeatAmount = filteredOrders.length > 0
    ? totalRepeatAmount / filteredOrders.length
    : 0;

  // 平均返单周期（天）
  const completedOrders = filteredOrders.filter(o => o.daysToRepeat);
  const avgDaysToRepeat = completedOrders.length > 0
    ? completedOrders.reduce((sum, o) => sum + o.daysToRepeat, 0) / completedOrders.length
    : 0;

  // 按客户统计
  const byCustomer = {};
  filteredOrders.forEach(o => {
    if (!byCustomer[o.customerId]) {
      byCustomer[o.customerId] = {
        customerId: o.customerId,
        customerName: o.customerName,
        count: 0,
        totalAmount: 0
      };
    }
    byCustomer[o.customerId].count++;
    byCustomer[o.customerId].totalAmount += o.repeatAmount;
  });

  return {
    summary: {
      total: filteredOrders.length,
      conversionRate: `${conversionRate}%`,
      totalAmount: totalRepeatAmount,
      avgAmount: avgRepeatAmount.toFixed(2),
      avgDaysToRepeat: avgDaysToRepeat.toFixed(1)
    },
    byCustomer: Object.values(byCustomer)
  };
}

/**
 * 满意度统计模型
 * @param {string} dateRange - 日期范围
 * @returns {Object} 满意度统计数据
 */
function getSatisfactionStats(dateRange) {
  const { startDate, endDate } = parseDateRange(dateRange);
  
  // 过滤日期范围内的调查
  const filteredSurveys = mockData.satisfactionSurveys.filter(s => 
    isDateInRange(s.createdAt, startDate, endDate)
  );

  if (filteredSurveys.length === 0) {
    return {
      summary: {
        total: 0,
        avgOverallScore: 0,
        avgQualityScore: 0,
        avgServiceScore: 0,
        avgDeliveryScore: 0,
        avgCommunicationScore: 0
      },
      distribution: {},
      trend: []
    };
  }

  // 计算平均分
  const avgOverallScore = filteredSurveys.reduce((sum, s) => sum + s.overallScore, 0) / filteredSurveys.length;
  const avgQualityScore = filteredSurveys.reduce((sum, s) => sum + s.qualityScore, 0) / filteredSurveys.length;
  const avgServiceScore = filteredSurveys.reduce((sum, s) => sum + s.serviceScore, 0) / filteredSurveys.length;
  const avgDeliveryScore = filteredSurveys.reduce((sum, s) => sum + s.deliveryScore, 0) / filteredSurveys.length;
  const avgCommunicationScore = filteredSurveys.reduce((sum, s) => sum + s.communicationScore, 0) / filteredSurveys.length;

  // 分数分布
  const distribution = { '1': 0, '2': 0, '3': 0, '4': 0, '5': 0 };
  filteredSurveys.forEach(s => {
    distribution[s.overallScore.toString()]++;
  });

  // 满意度趋势（按周）
  const weeklyData = {};
  filteredSurveys.forEach(s => {
    const week = dayjs(s.createdAt).week();
    if (!weeklyData[week]) {
      weeklyData[week] = { week, count: 0, totalScore: 0 };
    }
    weeklyData[week].count++;
    weeklyData[week].totalScore += s.overallScore;
  });

  const trend = Object.values(weeklyData).map(w => ({
    week: w.week,
    avgScore: (w.totalScore / w.count).toFixed(2),
    count: w.count
  }));

  return {
    summary: {
      total: filteredSurveys.length,
      avgOverallScore: avgOverallScore.toFixed(2),
      avgQualityScore: avgQualityScore.toFixed(2),
      avgServiceScore: avgServiceScore.toFixed(2),
      avgDeliveryScore: avgDeliveryScore.toFixed(2),
      avgCommunicationScore: avgCommunicationScore.toFixed(2)
    },
    distribution,
    trend
  };
}

/**
 * 客户风险分析模型
 * @returns {Object} 客户风险分析数据
 */
function getCustomerRiskAnalysis() {
  // 按风险等级统计
  const byRiskLevel = { low: 0, medium: 0, high: 0 };
  mockData.customers.forEach(c => {
    byRiskLevel[c.riskLevel]++;
  });

  // 高风险客户列表
  const highRiskCustomers = mockData.customers
    .filter(c => c.riskLevel === 'high')
    .map(c => ({
      customerId: c.customerId,
      customerName: c.customerName,
      totalOrders: c.totalOrders,
      totalAmount: c.totalAmount
    }));

  // 风险指标
  const totalCustomers = mockData.customers.length;
  const highRiskRatio = ((byRiskLevel.high / totalCustomers) * 100).toFixed(2);

  return {
    summary: {
      totalCustomers,
      lowRisk: byRiskLevel.low,
      mediumRisk: byRiskLevel.medium,
      highRisk: byRiskLevel.high,
      highRiskRatio: `${highRiskRatio}%`
    },
    highRiskCustomers
  };
}

/**
 * 产品质量分析模型
 * @returns {Object} 产品质量分析数据
 */
function getProductQualityAnalysis() {
  // 按类别统计缺陷率
  const byCategory = {};
  mockData.products.forEach(p => {
    if (!byCategory[p.category]) {
      byCategory[p.category] = {
        category: p.category,
        productCount: 0,
        avgDefectRate: 0,
        totalDefectRate: 0
      };
    }
    byCategory[p.category].productCount++;
    byCategory[p.category].totalDefectRate += p.defectRate;
  });

  Object.values(byCategory).forEach(c => {
    c.avgDefectRate = (c.totalDefectRate / c.productCount).toFixed(4);
  });

  // 缺陷率最高的产品
  const productsByDefectRate = [...mockData.products].sort((a, b) => b.defectRate - a.defectRate);

  // 投诉关联分析
  const complaintByProduct = {};
  mockData.complaints.filter(c => c.type === 'quality').forEach(c => {
    if (!complaintByProduct[c.productId]) {
      complaintByProduct[c.productId] = 0;
    }
    complaintByProduct[c.productId]++;
  });

  const qualityIssues = mockData.products.map(p => ({
    productId: p.productId,
    productName: p.productName,
    category: p.category,
    defectRate: p.defectRate,
    qualityComplaints: complaintByProduct[p.productId] || 0
  }));

  return {
    summary: {
      totalProducts: mockData.products.length,
      avgDefectRate: (mockData.products.reduce((sum, p) => sum + p.defectRate, 0) / mockData.products.length).toFixed(4)
    },
    byCategory: Object.values(byCategory),
    qualityIssues: qualityIssues.sort((a, b) => b.defectRate - a.defectRate)
  };
}

module.exports = {
  getComplaintStats,
  getRepeatOrderStats,
  getSatisfactionStats,
  getCustomerRiskAnalysis,
  getProductQualityAnalysis,
  parseDateRange
};
