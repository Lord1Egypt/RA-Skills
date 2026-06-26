#!/usr/bin/env node
/**
 * Monitor Script for telebiz-mcp
 *
 * Checks health and maintains state file for status tracking.
 * Outputs alerts when state changes (for integration with notifications).
 *
 * Usage:
 *   node monitor.js              # Check and output status
 *   node monitor.js --json       # Output JSON
 *   node monitor.js --quiet      # Only output on state change
 *
 * Exit codes:
 *   0 = healthy (relay up, executor connected)
 *   1 = degraded (relay up, executor disconnected)
 *   2 = down (relay not running)
 *   3 = state changed (for alerting)
 */
export {};
