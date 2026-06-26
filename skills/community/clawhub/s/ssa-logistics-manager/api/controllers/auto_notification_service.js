// logistics/api/controllers/auto_notification_service.js
/**
 * 自动通知服务
 * 
 * 负责在物流状态变更时自动发送通知邮件
 * 并可选同步到 OKKI CRM
 */

const { getLogisticsDetails } = require('../logistics_api');
const okkiSyncController = require('./okki_sync_controller');

// 邮件发送配置（待实现）
const EMAIL_CONFIG = {
  enabled: true,
  smtpHost: 'smtphz.qiye.163.com',
  smtpPort: 465,
  from: 'sale-9@farreach-electronic.com'
};

/**
 * 发送物流通知邮件
 * @param {string} logisticsId - 物流 ID
 * @param {string} notificationType - 通知类型 (booking/shipment/arrival/delivery)
 * @param {object} recipient - 收件人信息
 * @param {boolean} syncToOKKI - 是否同步到 OKKI
 * @returns {Promise<object>}
 */
async function sendLogisticsNotification(logisticsId, notificationType, recipient = {}, syncToOKKI = false) {
  try {
    // 步骤 1: 获取物流记录详情
    const logisticsData = await getLogisticsDetails(logisticsId);
    if (!logisticsData) {
      throw new Error(`物流记录 ${logisticsId} 未找到`);
    }
    
    // 步骤 2: 构建邮件内容
    const emailContent = buildEmailContent(logisticsData, notificationType);
    
    // 步骤 3: 发送邮件（这里调用 SMTP 模块，待实际实现）
    const emailResult = await sendEmail({
      to: recipient.email || logisticsData.customerInfo?.email,
      cc: recipient.cc,
      subject: emailContent.subject,
      html: emailContent.html,
      text: emailContent.text
    });
    
    // 步骤 4: 记录通知历史
    const notificationRecord = {
      notificationId: `NT-${Date.now()}`,
      logisticsId,
      type: notificationType,
      method: 'email',
      recipient: recipient.email || logisticsData.customerInfo?.email,
      content: emailContent.subject,
      status: emailResult.success ? 'sent' : 'failed',
      timestamp: new Date().toISOString()
    };
    
    // 步骤 5: 可选 - 同步到 OKKI
    let okkiSyncResult = null;
    if (syncToOKKI && emailResult.success) {
      try {
        okkiSyncResult = await okkiSyncController.syncLogisticsToOKKI(logisticsId);
      } catch (okkiError) {
        console.warn('OKKI 同步失败，但不影响邮件发送:', okkiError.message);
        okkiSyncResult = {
          success: false,
          error: okkiError.message
        };
      }
    }
    
    return {
      success: true,
      notification: notificationRecord,
      email: emailResult,
      okki_sync: okkiSyncResult
    };
  } catch (e) {
    console.error('发送物流通知失败:', e.message);
    return {
      success: false,
      error: e.message,
      logistics_id: logisticsId
    };
  }
}

/**
 * 构建邮件内容
 * @param {object} logisticsData - 物流数据
 * @param {string} notificationType - 通知类型
 * @returns {object} 邮件内容 {subject, html, text}
 */
function buildEmailContent(logisticsData, notificationType) {
  const customerName = logisticsData.customerInfo?.name || '尊敬的客户';
  const logisticsId = logisticsData.logisticsId;
  const orderId = logisticsData.orderId;
  
  let subject = '';
  let htmlContent = '';
  let textContent = '';
  
  switch (notificationType) {
    case 'booking':
      subject = `📦 订舱确认 - 物流单号：${logisticsId}`;
      htmlContent = `
        <h2>订舱确认通知</h2>
        <p>尊敬的 ${customerName}，</p>
        <p>您的订单 <strong>${orderId}</strong> 已成功订舱，详细信息如下：</p>
        <table style="border-collapse: collapse; width: 100%;">
          <tr><td style="padding: 8px; border: 1px solid #ddd;"><strong>物流单号</strong></td><td style="padding: 8px; border: 1px solid #ddd;">${logisticsId}</td></tr>
          <tr><td style="padding: 8px; border: 1px solid #ddd;"><strong>运输方式</strong></td><td style="padding: 8px; border: 1px solid #ddd;">${logisticsData.transportMode || '海运'}</td></tr>
          <tr><td style="padding: 8px; border: 1px solid #ddd;"><strong>船名/航次</strong></td><td style="padding: 8px; border: 1px solid #ddd;">${logisticsData.vesselName || '待确认'} ${logisticsData.voyageNo ? '(' + logisticsData.voyageNo + ')' : ''}</td></tr>
          <tr><td style="padding: 8px; border: 1px solid #ddd;"><strong>ETD (预计离港)</strong></td><td style="padding: 8px; border: 1px solid #ddd;">${logisticsData.etd || '待确认'}</td></tr>
          <tr><td style="padding: 8px; border: 1px solid #ddd;"><strong>ETA (预计到港)</strong></td><td style="padding: 8px; border: 1px solid #ddd;">${logisticsData.eta || '待确认'}</td></tr>
          <tr><td style="padding: 8px; border: 1px solid #ddd;"><strong>起运港</strong></td><td style="padding: 8px; border: 1px solid #ddd;">${logisticsData.portOfLoading || '待确认'}</td></tr>
          <tr><td style="padding: 8px; border: 1px solid #ddd;"><strong>目的港</strong></td><td style="padding: 8px; border: 1px solid #ddd;">${logisticsData.portOfDischarge || '待确认'}</td></tr>
        </table>
        <p>我们将持续更新物流状态，敬请关注。</p>
        <p>如有任何疑问，请随时联系我们。</p>
        <p>祝商祺！<br/>Farreach Electronic Team</p>
      `;
      textContent = `订舱确认通知\n\n尊敬的 ${customerName}，\n\n您的订单 ${orderId} 已成功订舱。\n物流单号：${logisticsId}\nETD: ${logisticsData.etd || '待确认'}\nETA: ${logisticsData.eta || '待确认'}\n\n祝商祺！\nFarreach Electronic Team`;
      break;
      
    case 'shipment':
      subject = `🚢 发货通知 - 物流单号：${logisticsId}`;
      htmlContent = `
        <h2>发货通知</h2>
        <p>尊敬的 ${customerName}，</p>
        <p>您的订单 <strong>${orderId}</strong> 已发货，详细信息如下：</p>
        <table style="border-collapse: collapse; width: 100%;">
          <tr><td style="padding: 8px; border: 1px solid #ddd;"><strong>物流单号</strong></td><td style="padding: 8px; border: 1px solid #ddd;">${logisticsId}</td></tr>
          <tr><td style="padding: 8px; border: 1px solid #ddd;"><strong>提单号</strong></td><td style="padding: 8px; border: 1px solid #ddd;">${logisticsData.billOfLading?.blNo || '待提供'}</td></tr>
          <tr><td style="padding: 8px; border: 1px solid #ddd;"><strong>船名/航次</strong></td><td style="padding: 8px; border: 1px solid #ddd;">${logisticsData.vesselName || '待确认'} ${logisticsData.voyageNo ? '(' + logisticsData.voyageNo + ')' : ''}</td></tr>
          <tr><td style="padding: 8px; border: 1px solid #ddd;"><strong>ATD (实际离港)</strong></td><td style="padding: 8px; border: 1px solid #ddd;">${logisticsData.atd || logisticsData.etd || '待确认'}</td></tr>
          <tr><td style="padding: 8px; border: 1px solid #ddd;"><strong>ETA (预计到港)</strong></td><td style="padding: 8px; border: 1px solid #ddd;">${logisticsData.eta || '待确认'}</td></tr>
          <tr><td style="padding: 8px; border: 1px solid #ddd;"><strong>剩余天数</strong></td><td style="padding: 8px; border: 1px solid #ddd;">${calculateDaysToETA(logisticsData.eta)} 天</td></tr>
        </table>
        <p>我们将持续追踪货物状态，到港后会及时通知您。</p>
        <p>祝商祺！<br/>Farreach Electronic Team</p>
      `;
      textContent = `发货通知\n\n尊敬的 ${customerName}，\n\n您的订单 ${orderId} 已发货。\n物流单号：${logisticsId}\n提单号：${logisticsData.billOfLading?.blNo || '待提供'}\nATD: ${logisticsData.atd || logisticsData.etd || '待确认'}\nETA: ${logisticsData.eta || '待确认'}\n\n祝商祺！\nFarreach Electronic Team`;
      break;
      
    case 'arrival':
      subject = `✅ 到港通知 - 物流单号：${logisticsId}`;
      htmlContent = `
        <h2>到港通知</h2>
        <p>尊敬的 ${customerName}，</p>
        <p>您的货物已到达目的港，详细信息如下：</p>
        <table style="border-collapse: collapse; width: 100%;">
          <tr><td style="padding: 8px; border: 1px solid #ddd;"><strong>物流单号</strong></td><td style="padding: 8px; border: 1px solid #ddd;">${logisticsId}</td></tr>
          <tr><td style="padding: 8px; border: 1px solid #ddd;"><strong>目的港</strong></td><td style="padding: 8px; border: 1px solid #ddd;">${logisticsData.portOfDischarge}</td></tr>
          <tr><td style="padding: 8px; border: 1px solid #ddd;"><strong>ATA (实际到港)</strong></td><td style="padding: 8px; border: 1px solid #ddd;">${logisticsData.ata || new Date().toISOString().split('T')[0]}</td></tr>
        </table>
        <p>请尽快安排清关和提货手续。</p>
        <p>祝商祺！<br/>Farreach Electronic Team</p>
      `;
      textContent = `到港通知\n\n尊敬的 ${customerName}，\n\n您的货物已到达目的港 ${logisticsData.portOfDischarge}。\n物流单号：${logisticsId}\n\n请尽快安排清关和提货手续。\n\n祝商祺！\nFarreach Electronic Team`;
      break;
      
    case 'delivery':
      subject = `🎉 送达通知 - 物流单号：${logisticsId}`;
      htmlContent = `
        <h2>送达通知</h2>
        <p>尊敬的 ${customerName}，</p>
        <p>您的货物已成功送达，详细信息如下：</p>
        <table style="border-collapse: collapse; width: 100%;">
          <tr><td style="padding: 8px; border: 1px solid #ddd;"><strong>物流单号</strong></td><td style="padding: 8px; border: 1px solid #ddd;">${logisticsId}</td></tr>
          <tr><td style="padding: 8px; border: 1px solid #ddd;"><strong>订单号</strong></td><td style="padding: 8px; border: 1px solid #ddd;">${orderId}</td></tr>
          <tr><td style="padding: 8px; border: 1px solid #ddd;"><strong>送达时间</strong></td><td style="padding: 8px; border: 1px solid #ddd;">${new Date().toISOString().split('T')[0]}</td></tr>
        </table>
        <p>感谢您的信任与支持！期待再次合作。</p>
        <p>祝商祺！<br/>Farreach Electronic Team</p>
      `;
      textContent = `送达通知\n\n尊敬的 ${customerName}，\n\n您的货物已成功送达。\n物流单号：${logisticsId}\n订单号：${orderId}\n\n感谢您的信任与支持！\n\n祝商祺！\nFarreach Electronic Team`;
      break;
      
    default:
      subject = `物流更新通知 - ${logisticsId}`;
      htmlContent = `<p>物流状态已更新，请登录系统查看详情。</p>`;
      textContent = '物流状态已更新，请登录系统查看详情。';
  }
  
  return {
    subject,
    html: htmlContent,
    text: textContent
  };
}

/**
 * 计算到 ETA 的天数
 * @param {string} etaDate - ETA 日期
 * @returns {number}
 */
function calculateDaysToETA(etaDate) {
  if (!etaDate) return null;
  const now = new Date();
  const eta = new Date(etaDate);
  const diffTime = eta - now;
  return Math.ceil(diffTime / (1000 * 60 * 60 * 24));
}

/**
 * 发送邮件（占位符，待实际实现）
 * @param {object} emailData - 邮件数据
 * @returns {Promise<object>}
 */
async function sendEmail(emailData) {
  // TODO: 集成 SMTP 邮件发送模块
  // 参考：/Users/wilson/.openclaw/workspace/skills/imap-smtp-email/scripts/smtp.js
  console.log('发送邮件:', emailData.to, emailData.subject);
  return {
    success: true,
    messageId: `MSG-${Date.now()}`
  };
}

/**
 * 自动触发通知（根据物流状态）
 * @param {string} logisticsId - 物流 ID
 * @param {string} newStatus - 新状态
 * @param {boolean} syncToOKKI - 是否同步到 OKKI
 * @returns {Promise<object>}
 */
async function autoNotifyOnStatusChange(logisticsId, newStatus, syncToOKKI = false) {
  const logisticsData = await getLogisticsDetails(logisticsId);
  if (!logisticsData) {
    return { success: false, error: '物流记录未找到' };
  }
  
  let notificationType = null;
  
  // 根据状态映射通知类型
  switch (newStatus) {
    case '已订舱':
      notificationType = 'booking';
      break;
    case '已装船':
      notificationType = 'shipment';
      break;
    case '已到港':
      notificationType = 'arrival';
      break;
    case '已送达':
      notificationType = 'delivery';
      break;
    default:
      // 其他状态不自动通知
      return { success: true, message: '无需通知的状态变更' };
  }
  
  // 发送通知
  const result = await sendLogisticsNotification(
    logisticsId,
    notificationType,
    {},
    syncToOKKI
  );
  
  return result;
}

module.exports = {
  sendLogisticsNotification,
  autoNotifyOnStatusChange,
  buildEmailContent
};
