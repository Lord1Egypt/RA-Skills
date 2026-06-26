/**
 * Refund Assistant - 退换货助手
 */

const { LocalStore } = require('../../shared/storage/local-store');

class RefundAssistant {
  constructor() {
    this.store = new LocalStore('refund-assistant');
    
    // 平台规则库
    this.platformRules = {
      'taobao': {
        returnWindow: 7,
        autoRefund: true,
        shippingCost: 'seller', // 7天无理由退货运费
        qualityIssue: 'seller', // 质量问题运费
        specialCategories: ['生鲜', '定制', '虚拟']
      },
      'tmall': {
        returnWindow: 7,
        autoRefund: true,
        shippingCost: 'seller',
        qualityIssue: 'seller',
        specialCategories: []
      },
      'jd': {
        returnWindow: 7,
        autoRefund: true,
        shippingCost: 'seller',
        qualityIssue: 'seller',
        plusReturnWindow: 30
      },
      'pdd': {
        returnWindow: 7,
        autoRefund: true,
        shippingCost: 'buyer', // 拼多多通常买家承担
        qualityIssue: 'seller'
      }
    };
    
    // 退货理由策略
    this.reasonStrategies = {
      'size_wrong': {
        reason: '尺码不合适',
        evidence: ['照片'],
        successRate: 0.95,
        shippingCost: 'buyer'
      },
      'not_as_described': {
        reason: '与描述不符',
        evidence: ['对比照片', '聊天记录'],
        successRate: 0.9,
        shippingCost: 'seller'
      },
      'quality_issue': {
        reason: '质量问题',
        evidence: ['照片', '视频'],
        successRate: 0.95,
        shippingCost: 'seller',
        canClaimCompensation: true
      },
      'fake': {
        reason: '假冒品牌',
        evidence: ['鉴定报告', '对比照片'],
        successRate: 0.85,
        shippingCost: 'seller',
        canClaimCompensation: true,
        canReport: true
      },
      'damaged': {
        reason: '快递破损',
        evidence: ['开箱视频', '照片', '快递证明'],
        successRate: 0.9,
        shippingCost: 'seller'
      }
    };
  }

  /**
   * 分析订单并生成退货策略
   */
  analyzeOrder(order) {
    const { platform, orderDate, category, price, issue } = order;
    const rules = this.platformRules[platform];
    
    if (!rules) {
      return { error: '不支持的平台' };
    }
    
    // 检查退货时效
    const orderTime = new Date(orderDate);
    const now = new Date();
    const daysPassed = Math.floor((now - orderTime) / (1000 * 60 * 60 * 24));
    const daysRemaining = rules.returnWindow - daysPassed;
    
    if (daysRemaining <= 0) {
      return {
        canReturn: false,
        reason: `已超过${rules.returnWindow}天退货期限`,
        alternatives: this.getAlternativesAfterWindow(order)
      };
    }
    
    // 匹配最佳退货策略
    const strategy = this.matchStrategy(issue, platform);
    
    return {
      canReturn: true,
      urgency: daysRemaining <= 2 ? 'high' : daysRemaining <= 5 ? 'medium' : 'low',
      daysRemaining,
      strategy,
      steps: this.generateSteps(strategy, order),
      evidence: strategy.evidence,
      timeline: this.generateTimeline(strategy, order),
      compensation: this.calculateCompensation(order, strategy)
    };
  }

  matchStrategy(issue, platform) {
    const strategy = this.reasonStrategies[issue] || this.reasonStrategies.size_wrong;
    const rules = this.platformRules[platform];
    
    return {
      ...strategy,
      shippingCost: issue === 'quality_issue' || issue === 'fake' 
        ? rules.qualityIssue 
        : strategy.shippingCost
    };
  }

  generateSteps(strategy, order) {
    return [
      {
        step: 1,
        action: '申请退货',
        detail: `选择理由：${strategy.reason}`,
        platform: order.platform
      },
      {
        step: 2,
        action: '准备证据',
        detail: `需要：${strategy.evidence.join('、')}`,
        tips: '照片要清晰，视频要完整'
      },
      {
        step: 3,
        action: '等待审核',
        detail: '通常1-3个工作日',
        fallback: '超时未审核可联系客服催促'
      },
      {
        step: 4,
        action: '寄回商品',
        detail: strategy.shippingCost === 'seller' 
          ? '使用运费险或垫付后申请退运费' 
          : '自行承担运费',
        tips: '保留快递单号，建议拍照留证'
      },
      {
        step: 5,
        action: '确认退款',
        detail: '卖家签收后自动退款',
        timeline: '通常1-3天到账'
      }
    ];
  }

  generateTimeline(strategy, order) {
    const now = new Date();
    const timeline = [];
    
    // 申请退货
    timeline.push({
      date: now,
      event: '提交退货申请',
      status: 'pending'
    });
    
    // 审核
    const reviewDate = new Date(now.getTime() + 2 * 24 * 60 * 60 * 1000);
    timeline.push({
      date: reviewDate,
      event: '卖家审核',
      status: 'expected'
    });
    
    // 寄回
    const shipDate = new Date(reviewDate.getTime() + 1 * 24 * 60 * 60 * 1000);
    timeline.push({
      date: shipDate,
      event: '寄回商品',
      status: 'expected'
    });
    
    // 退款
    const refundDate = new Date(shipDate.getTime() + 4 * 24 * 60 * 60 * 1000);
    timeline.push({
      date: refundDate,
      event: '退款到账',
      status: 'expected'
    });
    
    return timeline;
  }

  calculateCompensation(order, strategy) {
    const compensations = [];
    
    // 运费补偿
    if (strategy.shippingCost === 'seller' && order.shippingCost) {
      compensations.push({
        type: '运费',
        amount: order.shippingCost,
        claimMethod: '申请退运费'
      });
    }
    
    // 质量问题额外补偿
    if (strategy.canClaimCompensation && order.price > 100) {
      compensations.push({
        type: '延误补偿',
        amount: Math.min(order.price * 0.1, 50),
        claimMethod: '联系客服申请'
      });
    }
    
    // 假货赔偿
    if (strategy.reason === '假冒品牌') {
      compensations.push({
        type: '假一赔三',
        amount: order.price * 3,
        claimMethod: '平台投诉+举报',
        note: '需要提供鉴定报告'
      });
    }
    
    return compensations;
  }

  getAlternativesAfterWindow(order) {
    return [
      {
        option: '联系卖家协商',
        successRate: 0.3,
        note: '态度诚恳，说明原因'
      },
      {
        option: '二手平台转卖',
        platform: ['闲鱼', '转转'],
        note: `预计回血 ${Math.round(order.price * 0.6)}-${Math.round(order.price * 0.8)}元`
      },
      {
        option: '平台介入',
        condition: '有质量问题证据',
        note: '即使超期，质量问题仍可维权'
      }
    ];
  }

  /**
   * 生成退货申请文案
   */
  generateApplication(order, strategy) {
    const templates = {
      'quality_issue': `订单号：${order.orderId}

申请退货理由：${strategy.reason}

问题描述：
${order.issueDescription || '商品存在明显质量问题'}

证据：
已上传照片/视频

要求：
1. 全额退款
2. 退货运费由卖家承担
3. ${order.price > 100 ? '申请适当补偿' : ''}

请尽快处理，谢谢。`,

      'not_as_described': `订单号：${order.orderId}

申请退货理由：${strategy.reason}

问题描述：
收到的商品与页面描述存在以下差异：
${order.differences || '颜色/尺寸/材质不符'}

证据：
已上传对比照片

请处理退货申请，谢谢。`,

      'default': `订单号：${order.orderId}

申请7天无理由退货

商品完好，包装完整

请处理退货申请，谢谢。`
    };
    
    return templates[order.issue] || templates.default;
  }
}

module.exports = { RefundAssistant };
