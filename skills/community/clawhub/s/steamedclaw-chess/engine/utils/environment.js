"use strict";
/**
 * Environment detection utilities
 * Helps optimize memory usage based on runtime environment
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.isNodeEnvironment = isNodeEnvironment;
exports.isBrowserEnvironment = isBrowserEnvironment;
exports.getDefaultTTSize = getDefaultTTSize;
/**
 * Detect if code is running in Node.js environment
 *
 * @returns true if running in Node.js, false if in browser
 */
function isNodeEnvironment() {
    // Check for Node.js-specific globals
    return (typeof process !== 'undefined' &&
        process.versions != null &&
        process.versions.node != null);
}
/**
 * Detect if code is running in browser environment
 *
 * @returns true if running in browser, false if in Node.js
 */
function isBrowserEnvironment() {
    return !isNodeEnvironment();
}
/**
 * Get default transposition table size based on environment
 *
 * Node.js: 4 MB (level 3 default)
 * Browser: 2 MB (level 3 default)
 *
 * @returns Recommended TT size in MB
 */
function getDefaultTTSize() {
    return isNodeEnvironment() ? 4 : 2;
}
//# sourceMappingURL=environment.js.map