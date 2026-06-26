/**
 * Usage Tracker - OpenClaw 技能实现
 * 主函数：与 OpenClaw 交互，处理用户请求
 * 集成真实 SkillPay.me 收费系统
 */

class UsageTracker {
  constructor() {
    this.usage = new Map();
    this.paidUsage = 0;
    this.freeLimit = 10; // 每日10次免费
    this.costPerUse = 0.001; // 每次调用 0.001U
    this.skillPayApiKey = process.env.SKILL_BILLING_API_KEY || 'sk_2842f59e03e64e418c15771b0928c3f94a1f1da73ae7e72adc8f483e9f6fe6b1';
    this.skillId = process.env.SKILL_ID || 'usage-tracker-clawhub';
  }

  trackUsage(userId, feature) {
    const key = `${userId}:${feature}`;
    const count = this.usage.get(key) || 0;
    this.usage.set(key, count + 1);
    
    // 检查是否超过免费限制
    if (count > this.freeLimit) {
      this.paidUsage += 1;
      return { 
        paid: true, 
        usage: count,
        remaining: this.freeLimit - (count % this.freeLimit)
      };
    }
    
    return { 
      paid: false, 
      usage: count,
      remaining: this.freeLimit - count
    };
  }

  getUsageReport(userId) {
    let totalCost = 0;
    let report = "📊 使用报告:\n\n";
    
    // 按用户统计
    const userUsage = {};
    for (const [key, count] of this.usage.entries()) {
      if (key.startsWith(userId)) {
        const feature = key.split(':')[1];
        const isPaid = this.paidUsage > 0;
        const cost = isPaid ? count * this.costPerUse : 0;
        totalCost += cost;
        
        userUsage[feature] = {
          usage: count,
          isPaid,
          cost: cost.toFixed(4)
        };
      }
    }
    
    // 生成报告
    report += `👤 用户: ${userId}\n`;
    report += `📈 总调用次数: ${Object.values(userUsage).reduce((sum, item) => sum + item.usage, 0)}\n`;
    report += `💰 总费用: ${totalCost.toFixed(4)} U\n`;
    report += `\n📋 功能详情:\n`;
    
    for (const [feature, data] of Object.entries(userUsage)) {
      const status = data.isPaid ? '💎 付费' : '🆓 免费';
      report += `  ${status} ${feature}: ${data.usage}次`;
      if (data.isPaid) {
        report += ` (${data.cost}U)`;
      }
      report += '\n';
    }
    
    // 预测和建议
    report += `\n💡 使用建议:\n`;
    const totalUsage = Object.values(userUsage).reduce((sum, item) => sum + item.usage, 0);
    if (totalUsage > 20) {
      report += "🚨 使用频率较高，建议升级到包月套餐\n";
    } else if (totalUsage > this.freeLimit) {
      report += "💎 已开始付费使用，建议合理规划使用量\n";
    } else {
      report += "🆓 免费额度充足，可继续探索更多功能\n";
    }
    
    return report;
  }

  getMetrics() {
    const totalUsers = new Set([...this.usage.keys()].map(key => key.split(':')[0])).size;
    const totalCalls = Array.from(this.usage.values()).reduce((sum, count) => sum + count, 0);
    const totalRevenue = this.paidUsage * this.costPerUse;
    
    return {
      users: totalUsers,
      calls: totalCalls,
      paid_calls: this.paidUsage,
      revenue: totalRevenue.toFixed(4)
    };
  }

  resetDailyUsage() {
    const today = new Date().toDateString();
    // 这里应该保存上次重置日期，简化处理只做演示
    const yesterday = new Date(Date.now() - 24 * 60 * 60 * 1000).toDateString();
    
    // 模拟每日重置逻辑
    for (const key of this.usage.keys()) {
      if (this.usage.get(key) > this.freeLimit) {
        // 重置免费部分，保留付费记录
        const paidCount = Math.floor(this.usage.get(key) / this.freeLimit);
        this.usage.set(key, paidCount * this.freeLimit);
      }
    }
  }

  // 真实的 SkillPay.me API 调用
  async callSkillPayAPI(endpoint, params) {
    const BILLING_URL = "https://skillpay.me/api/v1/billing";
    const HEADERS = {
      "X-API-Key": this.skillPayApiKey,
      "Content-Type": "application/json"
    };

    try {
      const response = await fetch(BILLING_URL + endpoint, {
        method: 'POST',
        headers: HEADERS,
        body: JSON.stringify(params)
      });

      if (!response.ok) {
        throw new Error(`SkillPay.me API Error: ${response.status} ${response.statusText}`);
      }

      return await response.json();
    } catch (error) {
      console.error('SkillPay.me API 调用失败:', error);
      return { success: false, error: error.message };
    }
  }

  // 真实的计费函数
  async chargeUser(userId, amount = 0.001) {
    if (!this.skillPayApiKey) {
      return { success: false, error: 'SkillPay.me API Key 未配置' };
    }

    const params = {
      user_id: userId,
      skill_id: this.skillId,
      amount: amount
    };

    const result = await this.callSkillPayAPI('/charge', params);
    
    if (result.success) {
      return { 
        success: true, 
        chargeId: result.id,
        amount,
        txHash: result.txHash,
        balance: result.balance
      };
    } else {
      return { 
        success: false, 
        error: result.error || '计费失败'
      };
    }
  }

  // 真实的余额查询函数
  async getUserBalance(userId) {
    if (!this.skillPayApiKey) {
      return { success: false, error: 'SkillPay.me API Key 未配置' };
    }

    const params = { user_id: userId };
    const result = await this.callSkillPayAPI('/balance', params);
    
    return { 
      success: true, 
      balance: result.balance 
    };
  }

  // 真实的支付链接生成函数
  async getPaymentLink(userId, amount = 8) {
    if (!this.skillPayApiKey) {
      return { success: false, error: 'SkillPay.me API Key 未配置' };
    }

    const params = {
      user_id: userId,
      amount: amount
    };

    const result = await this.callSkillPayAPI('/payment-link', params);
    
    return { 
      success: true, 
      paymentUrl: result.payment_url 
    };
  }
}

// 主要处理函数
async function handleCommand(command, args, user) {
  const tracker = new UsageTracker();
  
  switch(command) {
    case 'init':
    case 'setup':
      // 初始化 SkillPay.me
      if (!tracker.skillPayApiKey) {
        return '❌ 请设置 SKILL_BILLING_API_KEY 环境变量:\n' +
               'export SKILL_BILLING_API_KEY="sk_2842f59e03e64e418c15771b0928c3f94a1f1da73ae7e72adc8f483e9f6fe6b1"\n' +
               'export SKILL_ID="usage-tracker-clawhub"\n' +
               '@openclaw setup YOUR_API_KEY';
      }
      
      return '✅ SkillPay.me 已初始化，可以开始收费\n' +
             `🔑 API Key: ${tracker.skillPayApiKey.substring(0, 10)}...\n` +
             `🆔 Skill ID: ${tracker.skillId}`;
      
    case 'track':
    case 'use':
    case '调用':
    case '跟踪':
      const feature = args[0] || '默认功能';
      const result = tracker.trackUsage(user, feature);
      
      let response = `📊 功能调用记录:\n`;
      response += `👤 用户: ${user}\n`;
      response += `🔧 功能: ${feature}\n`;
      response += `📈 使用次数: ${result.usage}\n`;
      response += `🆓 剩余免费次数: ${result.remaining}\n`;
      
      if (result.paid) {
        response += `💎 已开始付费使用 (本次费用: 0.001U)\n`;
      } else {
        response += `🆓 仍在免费额度内\n`;
      }
      
      return response;
      
    case 'report':
    case '报告':
    case 'usage':
      const report = tracker.getUsageReport(user);
      return report;
      
    case 'charge':
    case '计费':
    case '付款':
      const feature = args[0] || '使用功能';
      const amount = parseFloat(args[1]) || 0.001;
      const chargeResult = await tracker.chargeUser(user, amount);
      
      let response = `💳 计费记录:\n\n`;
      response += `👤 用户: ${user}\n`;
      response += `💰 功能: ${feature}\n`;
      response += `🔢 金额: ${amount} U\n\n`;
      
      if (chargeResult.success) {
        response += `✅ 计费成功!\n`;
        response += `📋 交易ID: ${chargeResult.chargeId}\n`;
        response += `⛓ 链上哈希: ${chargeResult.txHash}\n`;
        response += `💎 您的余额: ${chargeResult.balance} U\n`;
      } else {
        response += `❌ 计费失败: ${chargeResult.error}\n`;
      }
      
      return response;
      
    case 'balance':
    case '查询余额':
    case 'check_balance':
      const balanceResult = await tracker.getUserBalance(user);
      
      let response = `💳 账户余额查询:\n\n`;
      response += `👤 用户: ${user}\n`;
      
      if (balanceResult.success) {
        response += `💰 当前余额: ${balanceResult.balance} U\n`;
      } else {
        response += `❌ 查询失败: ${balanceResult.error}\n`;
      }
      
      return response;
      
    case 'recharge':
    case '充值':
      const rechargeAmount = parseFloat(args[0]) || 8;
      const linkResult = await tracker.getPaymentLink(user, rechargeAmount);
      
      let response = `💳 充值链接:\n\n`;
      response += `👤 用户: ${user}\n`;
      response += `💰 充值金额: ${rechargeAmount} U\n\n`;
      
      if (linkResult.success) {
        response += `🔗 充值链接: ${linkResult.paymentUrl}\n`;
        response += `💡 请在浏览器中打开链接完成充值\n`;
      } else {
        response += `❌ 生成充值链接失败: ${linkResult.error}\n`;
      }
      
      return response;
      
    case 'metrics':
    case '统计':
    case '系统':
      const metrics = tracker.getMetrics();
      let response = `📈 系统使用统计:\n\n`;
      response += `👥 总用户数: ${metrics.users}\n`;
      response += `📞 总调用次数: ${metrics.calls}\n`;
      response += `💎 付费调用次数: ${metrics.paid_calls}\n`;
      response += `💰 总收入: ${metrics.revenue} U\n`;
      
      // 添加增长率计算
      if (metrics.paid_calls > 0) {
        const conversionRate = ((metrics.paid_calls / metrics.calls) * 100).toFixed(1);
        response += `📊 付费转化率: ${conversionRate}%\n`;
      }
      
      return response;
      
    case 'reset':
      tracker.resetDailyUsage();
      return '🔄 每日使用量已重置';
      
    default:
      return `❓ 未知命令: ${command}\n\n` +
             `📋 可用命令:\n` +
             `• setup <API_KEY> - 初始化 SkillPay.me 支付\n` +
             `• 跟踪 <功能名> - 记录功能使用\n` +
             `• 计费 <功能名> <金额> - 触发付费功能使用\n` +
             `• 报告 - 生成个人使用报告\n` +
             `• 查询余额 - 查看账户余额\n` +
             `• 充值 <金额> - 生成充值链接\n` +
             `• 统计 - 查看系统整体统计\n` +
             `• 重置 - 重置每日免费额度\n\n` +
             `💎 付费功能: 详细报告、趋势预测、数据导出\n` +
             `🆓 免费功能: 基础统计、使用记录\n` +
             `💳 支付系统: SkillPay.me 集成，支持 USDT、BNB Chain`;
  }
}

// OpenClaw 技能入口
module.exports = {
  name: "Usage Tracker",
  description: "AI Agent usage tracking and billing verification tool with real SkillPay.me integration",
  version: "1.0.0",
  
  // 主处理函数
  async handle: async function(input, context) {
    const user = context.user || 'default_user';
    
    // 解析用户输入
    const tokens = input.trim().split(/\s+/);
    const command = tokens[0]?.toLowerCase();
    const args = tokens.slice(1);
    
    // 处理命令
    return await handleCommand(command, args, user);
  },
  
  // 技能信息
  info: function() {
    return `🎯 Usage Tracker v1.0.0 (真实支付集成)\n\n` +
           `💰 真实 SkillPay.me 计费系统\n\n` +
           `📋 功能:\n` +
           `• setup <API_KEY> - 初始化 SkillPay.me 支付\n` +
           `• 跟踪 <功能名> - 记录功能使用\n` +
           `• 计费 <功能名> <金额> - 触发付费功能使用\n` +
           `• 报告 - 生成个人使用报告\n` +
           `• 查询余额 - 查看账户余额\n` +
           `• 充值 <金额> - 生成充值链接\n` +
           `• 统计 - 查看系统整体统计\n` +
           `• 重置 - 重置每日免费额度\n\n` +
           `💎 付费功能: 详细报告、趋势预测、数据导出\n` +
           `🆓 免费功能: 基础统计、使用记录\n` +
           `💳 支付系统: SkillPay.me 集成，支持 USDT、BNB Chain\n` +
           `🔑 API Key: 已配置真实密钥`;
  }
};