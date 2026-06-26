#!/usr/bin/env node

/**
 * Order Dashboard - Command-line order status summary view
 * 
 * Usage:
 *   node order-dashboard.js                           # Show all orders grouped by status
 *   node order-dashboard.js --status in_production    # Filter by status
 *   node order-dashboard.js --order-id ORD-20260324-001  # View single order details
 *   node order-dashboard.js --format json             # Output as JSON
 *   node order-dashboard.js --format compact          # Compact table view
 *   node order-dashboard.js --format table            # Full table view (default)
 */

const fs = require('fs');
const path = require('path');

// Configuration
const DATA_DIR = path.join(__dirname, '..', 'data');
const ORDERS_FILE = path.join(DATA_DIR, 'orders.json');

// ANSI color codes
const COLORS = {
  reset: '\x1b[0m',
  bold: '\x1b[1m',
  dim: '\x1b[2m',
  red: '\x1b[31m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  magenta: '\x1b[35m',
  cyan: '\x1b[36m',
  white: '\x1b[37m',
  bgRed: '\x1b[41m',
  bgYellow: '\x1b[43m',
  bgGreen: '\x1b[42m',
  black: '\x1b[30m',
};

// Status color mapping
const STATUS_COLORS = {
  pending_production: COLORS.yellow,
  in_production: COLORS.blue,
  ready_to_ship: COLORS.cyan,
  shipped: COLORS.magenta,
  completed: COLORS.green,
  cancelled: COLORS.red,
};

// Parse command line arguments
function parseArgs(args) {
  const result = {
    status: null,
    orderId: null,
    format: 'table',
  };

  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--status' && args[i + 1]) {
      result.status = args[++i];
    } else if (args[i] === '--order-id' && args[i + 1]) {
      result.orderId = args[++i];
    } else if (args[i] === '--format' && args[i + 1]) {
      result.format = args[++i];
    } else if (args[i] === '--help' || args[i] === '-h') {
      printHelp();
      process.exit(0);
    }
  }

  return result;
}

function printHelp() {
  console.log(`
${COLORS.bold}Order Dashboard${COLORS.reset} - Command-line order status summary view

${COLORS.bold}Usage:${COLORS.reset}
  node order-dashboard.js [options]

${COLORS.bold}Options:${COLORS.reset}
  --status <status>      Filter orders by status
                         Values: pending_production, in_production, ready_to_ship, shipped, completed, cancelled
  --order-id <id>        View details of a single order
  --format <format>      Output format: table (default), json, compact
  --help, -h             Show this help message

${COLORS.bold}Examples:${COLORS.reset}
  node order-dashboard.js                              # Show all orders grouped by status
  node order-dashboard.js --status in_production       # Show only in-production orders
  node order-dashboard.js --order-id ORD-20260324-001  # View single order details
  node order-dashboard.js --format json                # Output as JSON
`);
}

// Load orders data
function loadOrders() {
  if (!fs.existsSync(ORDERS_FILE)) {
    console.error(`${COLORS.red}Error: Orders file not found at ${ORDERS_FILE}${COLORS.reset}`);
    process.exit(1);
  }

  try {
    const data = JSON.parse(fs.readFileSync(ORDERS_FILE, 'utf8'));
    return data;
  } catch (error) {
    console.error(`${COLORS.red}Error reading orders file: ${error.message}${COLORS.reset}`);
    process.exit(1);
  }
}

// Calculate days until delivery
function daysUntilDelivery(deliveryDate) {
  const today = new Date();
  today.setHours(0, 0, 0, 0);
  const delivery = new Date(deliveryDate);
  delivery.setHours(0, 0, 0, 0);
  const diffTime = delivery - today;
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
  return diffDays;
}

// Check if order is overdue
function isOverdue(order) {
  const completedStatuses = ['completed', 'cancelled'];
  if (completedStatuses.includes(order.status)) {
    return false;
  }
  return daysUntilDelivery(order.delivery_date) < 0;
}

// Check if order is urgent (delivery ≤ 7 days)
function isUrgent(order) {
  const completedStatuses = ['completed', 'cancelled'];
  if (completedStatuses.includes(order.status)) {
    return false;
  }
  const days = daysUntilDelivery(order.delivery_date);
  return days >= 0 && days <= 7;
}

// Format currency
function formatCurrency(amount, currency) {
  const symbols = { USD: '$', EUR: '€', GBP: '£', CNY: '¥' };
  const symbol = symbols[currency] || currency;
  return `${symbol}${amount.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
}

// Format date
function formatDate(dateStr) {
  const date = new Date(dateStr);
  return date.toISOString().split('T')[0];
}

// Colorize status
function colorizeStatus(status) {
  const color = STATUS_COLORS[status] || COLORS.white;
  return `${color}${status}${COLORS.reset}`;
}

// Get status label with emoji
function getStatusLabel(status) {
  const labels = {
    pending_production: '⏳ Pending Production',
    in_production: '🏭 In Production',
    ready_to_ship: '📦 Ready to Ship',
    shipped: '🚚 Shipped',
    completed: '✅ Completed',
    cancelled: '❌ Cancelled',
  };
  return labels[status] || status;
}

// Print table header
function printTableHeader() {
  const header = [
    'Order ID',
    'Customer',
    'Products',
    'Qty',
    'Amount',
    'Status',
    'Delivery',
    'Days',
  ];
  
  console.log(`\n${COLORS.bold}${COLORS.cyan}${header.join(' │ ')}${COLORS.reset}`);
  console.log(`${COLORS.dim}${'─'.repeat(120)}${COLORS.reset}`);
}

// Print order row (table format)
function printOrderRow(order) {
  const days = daysUntilDelivery(order.delivery_date);
  let daysLabel = days.toString();
  
  if (isOverdue(order)) {
    daysLabel = `${COLORS.bgRed}${COLORS.white} OVERDUE ${COLORS.reset}`;
  } else if (isUrgent(order)) {
    daysLabel = `${COLORS.bgYellow}${COLORS.black} ${days}d ⚠️ ${COLORS.reset}`;
  } else if (days < 0) {
    daysLabel = `${COLORS.dim}${days}d${COLORS.reset}`;
  } else {
    daysLabel = `${COLORS.green}${days}d${COLORS.reset}`;
  }

  const productSummary = order.product_list.length > 1
    ? `${order.product_list.length} items`
    : order.product_list[0]?.sku || 'N/A';

  const row = [
    order.order_id,
    order.customer_company?.substring(0, 20) || order.customer_name,
    productSummary,
    order.quantity.toString(),
    formatCurrency(order.total_amount, order.currency),
    colorizeStatus(order.status),
    formatDate(order.delivery_date),
    daysLabel,
  ];

  console.log(row.join(' │ '));
}

// Print compact order row
function printCompactRow(order) {
  const days = daysUntilDelivery(order.delivery_date);
  let statusIcon = '';
  
  if (isOverdue(order)) {
    statusIcon = '🔴';
  } else if (isUrgent(order)) {
    statusIcon = '🟡';
  } else {
    statusIcon = '🟢';
  }

  console.log(`  ${statusIcon} ${order.order_id} │ ${order.customer_company} │ ${colorizeStatus(order.status)} │ ${formatDate(order.delivery_date)} (${days}d) │ ${formatCurrency(order.total_amount, order.currency)}`);
}

// Print single order details
function printOrderDetails(order) {
  const days = daysUntilDelivery(order.delivery_date);
  
  console.log(`\n${COLORS.bold}${COLORS.cyan}═══════════════════════════════════════════════════════════${COLORS.reset}`);
  console.log(`${COLORS.bold}${COLORS.cyan}  ORDER DETAILS: ${order.order_id}${COLORS.reset}`);
  console.log(`${COLORS.bold}${COLORS.cyan}═══════════════════════════════════════════════════════════${COLORS.reset}\n`);

  console.log(`${COLORS.bold}Customer:${COLORS.reset}`);
  console.log(`  Name: ${order.customer_name}`);
  console.log(`  Company: ${order.customer_company}`);
  console.log(`  Email: ${order.customer_email}`);
  console.log(`  Shipping: ${order.shipping_address?.city}, ${order.shipping_address?.country}`);

  console.log(`\n${COLORS.bold}Order Summary:${COLORS.reset}`);
  console.log(`  Status: ${colorizeStatus(order.status)}`);
  console.log(`  Total Amount: ${formatCurrency(order.total_amount, order.currency)}`);
  console.log(`  Delivery Date: ${formatDate(order.delivery_date)} (${days} days)`);
  
  if (isOverdue(order)) {
    console.log(`  ${COLORS.bgRed}${COLORS.white} ⚠️  OVERDUE ${COLORS.reset}`);
  } else if (isUrgent(order)) {
    console.log(`  ${COLORS.bgYellow}${COLORS.black} ⚠️  URGENT (≤7 days) ${COLORS.reset}`);
  }

  console.log(`\n${COLORS.bold}Products:${COLORS.reset}`);
  order.product_list.forEach((product, idx) => {
    console.log(`  ${idx + 1}. ${product.name} (${product.sku})`);
    console.log(`     Qty: ${product.quantity} × ${formatCurrency(product.unit_price, product.currency)} = ${formatCurrency(product.quantity * product.unit_price, product.currency)}`);
  });

  console.log(`\n${COLORS.bold}Status History:${COLORS.reset}`);
  order.status_history?.forEach((entry, idx) => {
    const date = new Date(entry.changed_at).toISOString().split('T')[0];
    console.log(`  ${idx + 1}. ${colorizeStatus(entry.status)} - ${date} by ${entry.changed_by}`);
    if (entry.notes) {
      console.log(`     "${entry.notes}"`);
    }
  });

  if (order.tracking_number) {
    console.log(`\n${COLORS.bold}Shipping:${COLORS.reset}`);
    console.log(`  Carrier: ${order.carrier || 'N/A'}`);
    console.log(`  Tracking: ${order.tracking_number}`);
  }

  if (order.notes) {
    console.log(`\n${COLORS.bold}Notes:${COLORS.reset}`);
    console.log(`  ${order.notes}`);
  }

  console.log(`\n${COLORS.bold}${COLORS.cyan}═══════════════════════════════════════════════════════════${COLORS.reset}\n`);
}

// Print summary statistics
function printSummary(orders) {
  const statusCounts = {};
  let totalAmount = 0;
  let overdueCount = 0;
  let urgentCount = 0;

  orders.forEach(order => {
    statusCounts[order.status] = (statusCounts[order.status] || 0) + 1;
    totalAmount += order.total_amount;
    if (isOverdue(order)) overdueCount++;
    if (isUrgent(order)) urgentCount++;
  });

  console.log(`\n${COLORS.bold}${COLORS.cyan}═══════════════════════════════════════════════════════════${COLORS.reset}`);
  console.log(`${COLORS.bold}${COLORS.cyan}  ORDER SUMMARY${COLORS.reset}`);
  console.log(`${COLORS.bold}${COLORS.cyan}═══════════════════════════════════════════════════════════${COLORS.reset}\n`);

  console.log(`${COLORS.bold}Total Orders:${COLORS.reset} ${orders.length}`);
  console.log(`${COLORS.bold}Total Value:${COLORS.reset} ${formatCurrency(totalAmount, 'USD')} (mixed currencies)\n`);

  console.log(`${COLORS.bold}Status Breakdown:${COLORS.reset}`);
  Object.entries(statusCounts).forEach(([status, count]) => {
    const label = getStatusLabel(status);
    console.log(`  ${colorizeStatus(status)}: ${count}`);
  });

  if (overdueCount > 0) {
    console.log(`\n${COLORS.bgRed}${COLORS.white} ⚠️  OVERDUE ORDERS: ${overdueCount} ${COLORS.reset}`);
  }
  if (urgentCount > 0) {
    console.log(`${COLORS.bgYellow}${COLORS.black} ⚠️  URGENT ORDERS (≤7 days): ${urgentCount} ${COLORS.reset}`);
  }

  console.log(`\n${COLORS.bold}${COLORS.cyan}═══════════════════════════════════════════════════════════${COLORS.reset}\n`);
}

// Main dashboard view (grouped by status)
function printDashboard(orders, format) {
  if (format === 'json') {
    const output = {
      generated_at: new Date().toISOString(),
      total_orders: orders.length,
      status_groups: {},
      summary: {
        total_value: orders.reduce((sum, o) => sum + o.total_amount, 0),
        overdue_count: orders.filter(isOverdue).length,
        urgent_count: orders.filter(isUrgent).length,
      },
    };

    orders.forEach(order => {
      if (!output.status_groups[order.status]) {
        output.status_groups[order.status] = [];
      }
      output.status_groups[order.status].push({
        order_id: order.order_id,
        customer: order.customer_company,
        amount: order.total_amount,
        currency: order.currency,
        delivery_date: order.delivery_date,
        days_until_delivery: daysUntilDelivery(order.delivery_date),
        is_overdue: isOverdue(order),
        is_urgent: isUrgent(order),
      });
    });

    console.log(JSON.stringify(output, null, 2));
    return;
  }

  // Print summary
  printSummary(orders);

  // Group orders by status
  const grouped = {};
  orders.forEach(order => {
    if (!grouped[order.status]) {
      grouped[order.status] = [];
    }
    grouped[order.status].push(order);
  });

  // Print each status group
  const statusOrder = ['pending_production', 'in_production', 'ready_to_ship', 'shipped', 'completed', 'cancelled'];
  
  statusOrder.forEach(status => {
    const statusOrders = grouped[status];
    if (!statusOrders || statusOrders.length === 0) return;

    console.log(`\n${COLORS.bold}${getStatusLabel(status)} (${statusOrders.length} orders)${COLORS.reset}`);
    console.log(`${COLORS.dim}${'─'.repeat(80)}${COLORS.reset}`);

    if (format === 'compact') {
      statusOrders.forEach(order => printCompactRow(order));
    } else {
      printTableHeader();
      statusOrders.forEach(order => printOrderRow(order));
    }
    console.log();
  });

  // Print overdue orders section if any
  const overdueOrders = orders.filter(isOverdue);
  if (overdueOrders.length > 0) {
    console.log(`\n${COLORS.bold}${COLORS.red}🚨 OVERDUE ORDERS - IMMEDIATE ACTION REQUIRED${COLORS.reset}`);
    console.log(`${COLORS.dim}${'─'.repeat(80)}${COLORS.reset}`);
    overdueOrders.forEach(order => {
      const days = Math.abs(daysUntilDelivery(order.delivery_date));
      console.log(`  ${COLORS.red}${order.order_id}${COLORS.reset} - ${order.customer_company} - ${days} days overdue`);
    });
  }

  // Print urgent orders section if any
  const urgentOrders = orders.filter(o => isUrgent(o) && !isOverdue(o));
  if (urgentOrders.length > 0) {
    console.log(`\n${COLORS.bold}${COLORS.yellow}⚠️  URGENT ORDERS - Delivery within 7 days${COLORS.reset}`);
    console.log(`${COLORS.dim}${'─'.repeat(80)}${COLORS.reset}`);
    urgentOrders.forEach(order => {
      const days = daysUntilDelivery(order.delivery_date);
      console.log(`  ${COLORS.yellow}${order.order_id}${COLORS.reset} - ${order.customer_company} - ${days} days remaining`);
    });
  }
}

// Main function
function main() {
  const args = parseArgs(process.argv.slice(2));
  const data = loadOrders();
  let orders = data.orders || [];

  // Filter by status if specified
  if (args.status) {
    orders = orders.filter(o => o.status === args.status);
  }

  // View single order if order-id specified
  if (args.orderId) {
    const order = orders.find(o => o.order_id === args.orderId);
    if (!order) {
      console.error(`${COLORS.red}Error: Order ${args.orderId} not found${COLORS.reset}`);
      process.exit(1);
    }
    
    if (args.format === 'json') {
      console.log(JSON.stringify(order, null, 2));
    } else {
      printOrderDetails(order);
    }
    return;
  }

  // Print dashboard
  if (orders.length === 0) {
    console.log(`${COLORS.dim}No orders found.${COLORS.reset}`);
    return;
  }

  printDashboard(orders, args.format);
}

// Run
main();
