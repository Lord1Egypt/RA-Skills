#!/usr/bin/env node

/**
 * Order Status Update Script
 * 
 * Updates order status with validation, logging, and optional notification trigger.
 * 
 * Usage:
 *   node update-order-status.js --order-id ORD-xxx --status new_status [--notes "note"] [--dry-run] [--trigger-notification]
 * 
 * Options:
 *   --order-id          Order ID to update (required)
 *   --status            New status (required)
 *   --notes             Optional notes for the status change
 *   --dry-run           Preview changes without writing
 *   --trigger-notification  Mark that customer notification should be sent
 *   --orders-file       Path to orders.json (default: ../data/orders.json)
 *   --schema-file       Path to order-schema.json (default: ../config/order-schema.json)
 */

const fs = require('fs');
const path = require('path');
const { argv } = require('process');

// Parse command line arguments
function parseArgs(args) {
  const parsed = {
    orderId: null,
    status: null,
    notes: null,
    dryRun: false,
    triggerNotification: false,
    ordersFile: null,
    schemaFile: null
  };

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    if (arg === '--order-id' && args[i + 1]) {
      parsed.orderId = args[++i];
    } else if (arg === '--status' && args[i + 1]) {
      parsed.status = args[++i];
    } else if (arg === '--notes' && args[i + 1]) {
      parsed.notes = args[++i];
    } else if (arg === '--dry-run') {
      parsed.dryRun = true;
    } else if (arg === '--trigger-notification') {
      parsed.triggerNotification = true;
    } else if (arg === '--orders-file' && args[i + 1]) {
      parsed.ordersFile = args[++i];
    } else if (arg === '--schema-file' && args[i + 1]) {
      parsed.schemaFile = args[++i];
    }
  }

  return parsed;
}

// Valid order statuses
const VALID_STATUSES = [
  'pending_production',
  'in_production',
  'ready_to_ship',
  'shipped',
  'completed',
  'cancelled'
];

// Status transition rules (from the order status model)
const ALLOWED_TRANSITIONS = {
  'pending_production': ['in_production', 'cancelled'],
  'in_production': ['ready_to_ship', 'cancelled'],
  'ready_to_ship': ['shipped', 'cancelled'],
  'shipped': ['completed', 'cancelled'],
  'completed': [],  // Terminal state
  'cancelled': []   // Terminal state
};

// Status change notification triggers
const NOTIFICATION_TRIGGERS = {
  'pending_production→in_production': 'order_production_started',
  'in_production→ready_to_ship': 'order_ready_to_ship',
  'ready_to_ship→shipped': 'order_shipped',
  'shipped→completed': 'order_completed',
  '*→cancelled': 'order_cancelled'
};

// Log function
function log(message, level = 'INFO') {
  const timestamp = new Date().toISOString();
  const logLine = `[${timestamp}] [${level}] ${message}`;
  console.log(logLine);
  return logLine;
}

// Validate status transition
function validateTransition(currentStatus, newStatus) {
  if (!VALID_STATUSES.includes(newStatus)) {
    return {
      valid: false,
      error: `Invalid status "${newStatus}". Valid statuses: ${VALID_STATUSES.join(', ')}`
    };
  }

  const allowed = ALLOWED_TRANSITIONS[currentStatus];
  if (!allowed) {
    return {
      valid: false,
      error: `Unknown current status "${currentStatus}"`
    };
  }

  if (!allowed.includes(newStatus)) {
    return {
      valid: false,
      error: `Invalid transition from "${currentStatus}" to "${newStatus}". Allowed transitions: ${allowed.join(', ') || 'none (terminal state)'}`
    };
  }

  return { valid: true };
}

// Get notification template for transition
function getNotificationTemplate(fromStatus, toStatus) {
  const key = `${fromStatus}→${toStatus}`;
  if (NOTIFICATION_TRIGGERS[key]) {
    return NOTIFICATION_TRIGGERS[key];
  }
  if (toStatus === 'cancelled') {
    return NOTIFICATION_TRIGGERS['*→cancelled'];
  }
  return null;
}

// Main function
function main() {
  const args = parseArgs(argv.slice(2));
  const logLines = [];

  logLines.push(log('=== Order Status Update Script ==='));

  // Validate required arguments
  if (!args.orderId) {
    console.error('Error: --order-id is required');
    console.error('Usage: node update-order-status.js --order-id ORD-xxx --status new_status [--notes "note"] [--dry-run] [--trigger-notification]');
    process.exit(1);
  }

  if (!args.status) {
    console.error('Error: --status is required');
    console.error('Usage: node update-order-status.js --order-id ORD-xxx --status new_status [--notes "note"] [--dry-run] [--trigger-notification]');
    process.exit(1);
  }

  logLines.push(log(`Order ID: ${args.orderId}`));
  logLines.push(log(`New Status: ${args.status}`));
  logLines.push(log(`Dry Run: ${args.dryRun}`));
  logLines.push(log(`Trigger Notification: ${args.triggerNotification}`));
  if (args.notes) {
    logLines.push(log(`Notes: ${args.notes}`));
  }

  // Determine file paths
  const scriptDir = __dirname;
  const ordersFile = args.ordersFile || path.join(scriptDir, '..', 'data', 'orders.json');
  const schemaFile = args.schemaFile || path.join(scriptDir, '..', 'config', 'order-schema.json');
  const logFile = path.join(scriptDir, '..', 'logs', 'status-changes.log');
  const backupFile = ordersFile + '.bak';

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
  logLines.push(log(`Found order: ${order.order_id} (current status: ${order.status})`));

  // Validate transition
  const transition = validateTransition(order.status, args.status);
  if (!transition.valid) {
    const errorMsg = `Validation failed: ${transition.error}`;
    logLines.push(log(errorMsg, 'ERROR'));
    fs.appendFileSync(logFile, logLines.join('\n') + '\n');
    console.error(errorMsg);
    process.exit(1);
  }

  logLines.push(log(`Transition validated: ${order.status} → ${args.status}`));

  // Check notification template
  const notificationTemplate = getNotificationTemplate(order.status, args.status);
  if (notificationTemplate) {
    logLines.push(log(`Notification template: ${notificationTemplate}`));
  }

  // Prepare the update
  const now = new Date().toISOString();
  const statusHistoryEntry = {
    status: args.status,
    changed_at: now,
    changed_by: 'manual',
    notes: args.notes || null,
    notification_sent: false
  };

  if (args.triggerNotification && notificationTemplate) {
    statusHistoryEntry.notification_sent = true;
    statusHistoryEntry.notification_template = notificationTemplate;
  }

  // Show what will be updated
  logLines.push(log('--- Changes to apply ---'));
  logLines.push(log(`  status: ${order.status} → ${args.status}`));
  logLines.push(log(`  updated_at: ${order.updated_at} → ${now}`));
  logLines.push(log(`  status_history: adding 1 entry`));
  if (args.triggerNotification) {
    logLines.push(log(`  notification: will be triggered (template: ${notificationTemplate})`));
  }

  if (args.dryRun) {
    logLines.push(log('DRY RUN: No changes written'));
    console.log('\n=== DRY RUN COMPLETE ===');
    console.log(logLines.join('\n'));
    fs.appendFileSync(logFile, logLines.join('\n') + '\n');
    process.exit(0);
  }

  // Create backup
  try {
    fs.copyFileSync(ordersFile, backupFile);
    logLines.push(log(`Backup created: ${backupFile}`));
  } catch (err) {
    const errorMsg = `Failed to create backup: ${err.message}`;
    logLines.push(log(errorMsg, 'ERROR'));
    fs.appendFileSync(logFile, logLines.join('\n') + '\n');
    console.error(errorMsg);
    process.exit(1);
  }

  // Apply the update
  order.status = args.status;
  order.updated_at = now;
  order.status_history.push(statusHistoryEntry);

  // Update metadata if exists
  if (ordersData.metadata) {
    ordersData.metadata.updated_at = now;
    ordersData.metadata.updated_by = 'manual';
    
    // Update status summary
    const oldStatus = ordersData.orders[orderIndex].status === args.status ? args.status : 
      (ordersData.orders.find(o => o.order_id === args.orderId)?.status || order.status);
    
    // Recalculate status summary
    const statusSummary = {};
    VALID_STATUSES.forEach(s => statusSummary[s] = 0);
    ordersData.orders.forEach(o => {
      if (statusSummary[o.status] !== undefined) {
        statusSummary[o.status]++;
      }
    });
    ordersData.metadata.status_summary = statusSummary;
  }

  // Write the updated file
  try {
    const updatedContent = JSON.stringify(ordersData, null, 2);
    fs.writeFileSync(ordersFile, updatedContent, 'utf8');
    logLines.push(log(`Orders file updated successfully`));
  } catch (err) {
    const errorMsg = `Failed to write orders file: ${err.message}`;
    logLines.push(log(errorMsg, 'ERROR'));
    // Restore backup
    try {
      fs.copyFileSync(backupFile, ordersFile);
      logLines.push(log(`Backup restored due to write failure`));
    } catch (restoreErr) {
      logLines.push(log(`Failed to restore backup: ${restoreErr.message}`, 'ERROR'));
    }
    fs.appendFileSync(logFile, logLines.join('\n') + '\n');
    console.error(errorMsg);
    process.exit(1);
  }

  // Write log
  logLines.push(log('=== Update Complete ==='));
  fs.appendFileSync(logFile, logLines.join('\n') + '\n');

  console.log('\n=== UPDATE COMPLETE ===');
  console.log(`Order ${args.orderId} status updated: ${order.status} → ${args.status}`);
  if (args.triggerNotification && notificationTemplate) {
    console.log(`Notification triggered: ${notificationTemplate}`);
  }
  console.log(`Log written to: ${logFile}`);
  console.log(`Backup saved to: ${backupFile}`);
}

// Run
main();
