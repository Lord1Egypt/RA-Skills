#!/usr/bin/env node

/**
 * Order Notification Script
 * 
 * Sends customer notification emails when order status changes.
 * Reuses SMTP configuration from imap-smtp-email skill.
 * 
 * Usage:
 *   node send-order-notification.js --order-id ORD-xxx [--status new_status] [--dry-run]
 * 
 * Options:
 *   --order-id    Order ID to notify (required)
 *   --status      Override status (optional, defaults to order's current status)
 *   --dry-run     Preview email without sending
 *   --orders-file Path to orders.json (default: ../data/orders.json)
 */

const fs = require('fs');
const path = require('path');
const nodemailer = require('nodemailer');
require('dotenv').config({ path: path.resolve(__dirname, '../../imap-smtp-email/.env') });

// Parse command line arguments
function parseArgs(args) {
  const parsed = {
    orderId: null,
    status: null,
    dryRun: false,
    ordersFile: null
  };

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    if (arg === '--order-id' && args[i + 1]) {
      parsed.orderId = args[++i];
    } else if (arg === '--status' && args[i + 1]) {
      parsed.status = args[++i];
    } else if (arg === '--dry-run') {
      parsed.dryRun = true;
    } else if (arg === '--orders-file' && args[i + 1]) {
      parsed.ordersFile = args[++i];
    }
  }

  return parsed;
}

// Email templates by status
const EMAIL_TEMPLATES = {
  in_production: {
    subject: {
      en: (order) => `Your Order ${order.order_id} Has Started Production`,
      zh: (order) => `您的订单 ${order.order_id} 已开始生产`
    },
    body: {
      en: (order) => `
Dear ${order.customer_name},

We are pleased to inform you that your order ${order.order_id} has started production.

Order Summary:
- Order ID: ${order.order_id}
- Current Status: In Production
- Estimated Delivery Date: ${order.delivery_date}
- Total Quantity: ${order.quantity} units
- Total Amount: ${order.total_amount?.toFixed(2) || 'N/A'} ${order.currency}

Product List:
${order.product_list.map(p => `  - ${p.name} (SKU: ${p.sku}): ${p.quantity} units @ ${p.unit_price.toFixed(2)} ${p.currency || order.currency}`).join('\n')}

Our team is now working on your order with priority. We will keep you updated on the progress.

If you have any questions, please don't hesitate to contact us.

Best regards,
Farreach Electronic Co., Ltd
sale-9@farreach-electronic.com
      `.trim(),
      zh: (order) => `
尊敬的 ${order.customer_name}：

我们很高兴地通知您，您的订单 ${order.order_id} 已开始生产。

订单摘要：
- 订单号：${order.order_id}
- 当前状态：生产中
- 预计交期：${order.delivery_date}
- 总数量：${order.quantity} 件
- 总金额：${order.total_amount?.toFixed(2) || 'N/A'} ${order.currency}

产品清单：
${order.product_list.map(p => `  - ${p.name} (SKU: ${p.sku}): ${p.quantity} 件 @ ${p.unit_price.toFixed(2)} ${p.currency || order.currency}`).join('\n')}

我们的团队正在优先处理您的订单。我们将随时向您更新生产进度。

如有任何疑问，请随时与我们联系。

此致
敬礼
远达电子有限公司
sale-9@farreach-electronic.com
      `.trim()
    }
  },
  ready_to_ship: {
    subject: {
      en: (order) => `Your Order ${order.order_id} Is Ready to Ship`,
      zh: (order) => `您的订单 ${order.order_id} 已备货完成，即将发货`
    },
    body: {
      en: (order) => `
Dear ${order.customer_name},

Great news! Your order ${order.order_id} has completed production and is ready to ship.

Order Summary:
- Order ID: ${order.order_id}
- Current Status: Ready to Ship
- Estimated Delivery Date: ${order.delivery_date}
- Total Quantity: ${order.quantity} units

Product List:
${order.product_list.map(p => `  - ${p.name} (SKU: ${p.sku}): ${p.quantity} units`).join('\n')}

We are arranging the shipment and will provide you with the tracking information shortly.

Thank you for your patience and trust in Farreach Electronic.

Best regards,
Farreach Electronic Co., Ltd
sale-9@farreach-electronic.com
      `.trim(),
      zh: (order) => `
尊敬的 ${order.customer_name}：

好消息！您的订单 ${order.order_id} 已完成生产，即将发货。

订单摘要：
- 订单号：${order.order_id}
- 当前状态：待发货
- 预计交期：${order.delivery_date}
- 总数量：${order.quantity} 件

产品清单：
${order.product_list.map(p => `  - ${p.name} (SKU: ${p.sku}): ${p.quantity} 件`).join('\n')}

我们正在安排发货，稍后将为您提供物流跟踪信息。

感谢您对远达电子的信任与耐心。

此致
敬礼
远达电子有限公司
sale-9@farreach-electronic.com
      `.trim()
    }
  },
  shipped: {
    subject: {
      en: (order) => `Your Order ${order.order_id} Has Been Shipped`,
      zh: (order) => `您的订单 ${order.order_id} 已发货`
    },
    body: {
      en: (order) => `
Dear ${order.customer_name},

Your order ${order.order_id} has been shipped!

Order Summary:
- Order ID: ${order.order_id}
- Current Status: Shipped
- Carrier: ${order.carrier || 'To be confirmed'}
- Tracking Number: ${order.tracking_number || 'To be provided'}
- Estimated Delivery Date: ${order.delivery_date}

Shipping Address:
${order.shipping_address ? [
  order.shipping_address.address_line1,
  order.shipping_address.address_line2,
  order.shipping_address.city,
  order.shipping_address.state,
  order.shipping_address.postal_code,
  order.shipping_address.country
].filter(Boolean).join('\n') : 'N/A'}

You can track your shipment using the tracking number above. Please allow 1-2 business days for the tracking information to be updated.

Thank you for choosing Farreach Electronic!

Best regards,
Farreach Electronic Co., Ltd
sale-9@farreach-electronic.com
      `.trim(),
      zh: (order) => `
尊敬的 ${order.customer_name}：

您的订单 ${order.order_id} 已发货！

订单摘要：
- 订单号：${order.order_id}
- 当前状态：已发货
- 物流公司：${order.carrier || '待确认'}
- 运单号：${order.tracking_number || '待提供'}
- 预计交期：${order.delivery_date}

收货地址：
${order.shipping_address ? [
  order.shipping_address.address_line1,
  order.shipping_address.address_line2,
  order.shipping_address.city,
  order.shipping_address.state,
  order.shipping_address.postal_code,
  order.shipping_address.country
].filter(Boolean).join('\n') : 'N/A'}

您可以使用上述运单号跟踪您的货物。物流信息可能需要 1-2 个工作日更新。

感谢您选择远达电子！

此致
敬礼
远达电子有限公司
sale-9@farreach-electronic.com
      `.trim()
    }
  },
  completed: {
    subject: {
      en: (order) => `Your Order ${order.order_id} Is Complete`,
      zh: (order) => `您的订单 ${order.order_id} 已完成`
    },
    body: {
      en: (order) => `
Dear ${order.customer_name},

Your order ${order.order_id} has been completed successfully!

Order Summary:
- Order ID: ${order.order_id}
- Status: Completed
- Total Amount: ${order.total_amount?.toFixed(2) || 'N/A'} ${order.currency}

We hope you are satisfied with our products and service. Your feedback is valuable to us.

If you have any questions or need further assistance, please don't hesitate to contact us.

We look forward to serving you again!

Best regards,
Farreach Electronic Co., Ltd
sale-9@farreach-electronic.com
      `.trim(),
      zh: (order) => `
尊敬的 ${order.customer_name}：

您的订单 ${order.order_id} 已顺利完成！

订单摘要：
- 订单号：${order.order_id}
- 状态：已完成
- 总金额：${order.total_amount?.toFixed(2) || 'N/A'} ${order.currency}

希望您对我们的产品和服务满意。您的反馈对我们非常重要。

如有任何疑问或需要进一步协助，请随时与我们联系。

期待再次为您服务！

此致
敬礼
远达电子有限公司
sale-9@farreach-electronic.com
      `.trim()
    }
  },
  cancelled: {
    subject: {
      en: (order) => `Your Order ${order.order_id} Has Been Cancelled`,
      zh: (order) => `您的订单 ${order.order_id} 已取消`
    },
    body: {
      en: (order) => `
Dear ${order.customer_name},

Your order ${order.order_id} has been cancelled.

Order Summary:
- Order ID: ${order.order_id}
- Status: Cancelled
- Original Delivery Date: ${order.delivery_date}

If you have any questions about this cancellation or would like to place a new order, please contact us.

We apologize for any inconvenience caused.

Best regards,
Farreach Electronic Co., Ltd
sale-9@farreach-electronic.com
      `.trim(),
      zh: (order) => `
尊敬的 ${order.customer_name}：

您的订单 ${order.order_id} 已取消。

订单摘要：
- 订单号：${order.order_id}
- 状态：已取消
- 原定交期：${order.delivery_date}

如果您对此次取消有任何疑问，或希望重新下单，请与我们联系。

对给您带来的不便，我们深表歉意。

此致
敬礼
远达电子有限公司
sale-9@farreach-electronic.com
      `.trim()
    }
  }
};

// Detect customer language preference (simple heuristic based on email domain or name)
function detectLanguage(order) {
  const email = order.customer_email?.toLowerCase() || '';
  const name = order.customer_name?.toLowerCase() || '';
  const company = order.customer_company?.toLowerCase() || '';

  // Check for Chinese indicators
  const chineseIndicators = ['.cn', 'china', '中文', 'cn'];
  if (chineseIndicators.some(ind => email.includes(ind) || company.includes(ind))) {
    return 'zh';
  }

  // Default to English for international customers
  return 'en';
}

// Log function
function log(message, level = 'INFO') {
  const timestamp = new Date().toISOString();
  const logLine = `[${timestamp}] [${level}] ${message}`;
  console.log(logLine);
  return logLine;
}

// Create SMTP transporter
function createTransporter() {
  const config = {
    host: process.env.SMTP_HOST,
    port: parseInt(process.env.SMTP_PORT) || 587,
    secure: process.env.SMTP_SECURE === 'true',
    auth: {
      user: process.env.SMTP_USER,
      pass: process.env.SMTP_PASS,
    },
    tls: {
      rejectUnauthorized: process.env.SMTP_REJECT_UNAUTHORIZED !== 'false',
    },
  };

  if (!config.host || !config.auth.user || !config.auth.pass) {
    throw new Error('Missing SMTP configuration. Please check imap-smtp-email/.env');
  }

  return nodemailer.createTransport(config);
}

// Send email
async function sendEmail(to, subject, text) {
  const transporter = createTransporter();

  try {
    await transporter.verify();
  } catch (err) {
    throw new Error(`SMTP connection failed: ${err.message}`);
  }

  const mailOptions = {
    from: process.env.SMTP_FROM || process.env.SMTP_USER,
    to: to,
    subject: subject,
    text: text,
  };

  const info = await transporter.sendMail(mailOptions);

  return {
    success: true,
    messageId: info.messageId,
    response: info.response,
  };
}

// Main function
async function main() {
  const args = parseArgs(process.argv.slice(2));
  const logLines = [];

  logLines.push(log('=== Order Notification Script ==='));

  // Validate required arguments
  if (!args.orderId) {
    console.error('Error: --order-id is required');
    console.error('Usage: node send-order-notification.js --order-id ORD-xxx [--status new_status] [--dry-run]');
    process.exit(1);
  }

  logLines.push(log(`Order ID: ${args.orderId}`));
  logLines.push(log(`Dry Run: ${args.dryRun}`));

  // Determine file paths
  const scriptDir = __dirname;
  const ordersFile = args.ordersFile || path.join(scriptDir, '..', 'data', 'orders.json');
  const logFile = path.join(scriptDir, '..', 'logs', 'notifications.log');

  logLines.push(log(`Orders file: ${ordersFile}`));
  logLines.push(log(`Log file: ${logFile}`));

  // Check if orders file exists
  if (!fs.existsSync(ordersFile)) {
    const errorMsg = `Orders file not found: ${ordersFile}`;
    logLines.push(log(errorMsg, 'ERROR'));
    fs.appendFileSync(logFile, logLines.join('\n') + '\n');
    console.error(errorMsg);
    process.exit(1);
  }

  // Read orders file
  let ordersData;
  try {
    const ordersContent = fs.readFileSync(ordersFile, 'utf8');
    ordersData = JSON.parse(ordersContent);
    logLines.push(log(`Loaded ${ordersData.orders?.length || 0} orders`));
  } catch (err) {
    const errorMsg = `Failed to read orders file: ${err.message}`;
    logLines.push(log(errorMsg, 'ERROR'));
    fs.appendFileSync(logFile, logLines.join('\n') + '\n');
    console.error(errorMsg);
    process.exit(1);
  }

  // Find the order
  const orderIndex = ordersData.orders?.findIndex(o => o.order_id === args.orderId);
  if (orderIndex === undefined || orderIndex === -1) {
    const errorMsg = `Order not found: ${args.orderId}`;
    logLines.push(log(errorMsg, 'ERROR'));
    fs.appendFileSync(logFile, logLines.join('\n') + '\n');
    console.error(errorMsg);
    process.exit(1);
  }

  const order = ordersData.orders[orderIndex];
  const currentStatus = args.status || order.status;
  logLines.push(log(`Found order: ${order.order_id} (status: ${currentStatus})`));

  // Check if template exists for this status
  if (!EMAIL_TEMPLATES[currentStatus]) {
    const errorMsg = `No email template for status: ${currentStatus}`;
    logLines.push(log(errorMsg, 'ERROR'));
    fs.appendFileSync(logFile, logLines.join('\n') + '\n');
    console.error(errorMsg);
    console.error(`Available statuses: ${Object.keys(EMAIL_TEMPLATES).join(', ')}`);
    process.exit(1);
  }

  // Detect language
  const lang = detectLanguage(order);
  logLines.push(log(`Detected language: ${lang}`));

  // Generate email content
  const template = EMAIL_TEMPLATES[currentStatus];
  const subject = template.subject[lang](order);
  const body = template.body[lang](order);

  logLines.push(log(`Email subject: ${subject}`));
  logLines.push(log(`Email recipient: ${order.customer_email}`));

  if (args.dryRun) {
    logLines.push(log('DRY RUN: Email preview (not sending)'));
    console.log('\n=== EMAIL PREVIEW ===');
    console.log(`To: ${order.customer_email}`);
    console.log(`Subject: ${subject}`);
    console.log('\n--- Body ---');
    console.log(body);
    console.log('--- End Body ---\n');
    console.log(logLines.join('\n'));
    fs.appendFileSync(logFile, logLines.join('\n') + '\n');
    process.exit(0);
  }

  // Send email
  logLines.push(log('Sending email...'));
  try {
    const result = await sendEmail(order.customer_email, subject, body);
    logLines.push(log(`Email sent successfully! Message ID: ${result.messageId}`));
    console.log('\n=== NOTIFICATION SENT ===');
    console.log(`Order: ${order.order_id}`);
    console.log(`To: ${order.customer_email}`);
    console.log(`Subject: ${subject}`);
    console.log(`Message ID: ${result.messageId}`);
  } catch (err) {
    const errorMsg = `Failed to send email: ${err.message}`;
    logLines.push(log(errorMsg, 'ERROR'));
    fs.appendFileSync(logFile, logLines.join('\n') + '\n');
    console.error(errorMsg);
    process.exit(1);
  }

  // Update orders.json to mark notification as sent
  const now = new Date().toISOString();
  const latestHistoryEntry = order.status_history[order.status_history.length - 1];
  if (latestHistoryEntry) {
    latestHistoryEntry.notification_sent = true;
    latestHistoryEntry.notification_sent_at = now;
    latestHistoryEntry.notification_message_id = logLines.find(l => l.includes('Message ID:'))?.split('Message ID: ')[1] || null;
  }
  order.updated_at = now;

  // Update metadata if exists
  if (ordersData.metadata) {
    ordersData.metadata.updated_at = now;
    ordersData.metadata.updated_by = 'notification-script';
  }

  // Write updated orders file
  try {
    const backupFile = ordersFile + '.bak';
    fs.copyFileSync(ordersFile, backupFile);
    logLines.push(log(`Backup created: ${backupFile}`));

    const updatedContent = JSON.stringify(ordersData, null, 2);
    fs.writeFileSync(ordersFile, updatedContent, 'utf8');
    logLines.push(log(`Orders file updated (notification_sent marked)`));
  } catch (err) {
    const errorMsg = `Failed to update orders file: ${err.message}`;
    logLines.push(log(errorMsg, 'ERROR'));
    fs.appendFileSync(logFile, logLines.join('\n') + '\n');
    console.error(errorMsg);
    process.exit(1);
  }

  // Write log
  logLines.push(log('=== Notification Complete ==='));
  fs.appendFileSync(logFile, logLines.join('\n') + '\n');

  console.log(`\nLog written to: ${logFile}`);
  console.log(`Backup saved to: ${ordersFile}.bak`);
}

// Run
main().catch(err => {
  console.error('Fatal error:', err.message);
  process.exit(1);
});
