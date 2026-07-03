"use strict";
/**
 * 日志系统
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.logger = exports.Logger = exports.LogLevel = void 0;
var LogLevel;
(function (LogLevel) {
    LogLevel[LogLevel["DEBUG"] = 0] = "DEBUG";
    LogLevel[LogLevel["INFO"] = 1] = "INFO";
    LogLevel[LogLevel["WARN"] = 2] = "WARN";
    LogLevel[LogLevel["ERROR"] = 3] = "ERROR";
})(LogLevel || (exports.LogLevel = LogLevel = {}));
class Logger {
    constructor(prefix = 'ClawCompany', level = LogLevel.INFO) {
        this.prefix = prefix;
        this.level = level;
    }
    setLevel(level) {
        this.level = level;
    }
    debug(message, ...args) {
        if (this.level <= LogLevel.DEBUG) {
            console.log(`[${this.prefix}] DEBUG: ${message}`, ...args);
        }
    }
    info(message, ...args) {
        if (this.level <= LogLevel.INFO) {
            console.log(`[${this.prefix}] ${message}`, ...args);
        }
    }
    warn(message, ...args) {
        if (this.level <= LogLevel.WARN) {
            console.warn(`[${this.prefix}] ⚠️  ${message}`, ...args);
        }
    }
    error(message, error) {
        if (this.level <= LogLevel.ERROR) {
            console.error(`[${this.prefix}] ❌ ${message}`);
            if (error) {
                console.error(error);
            }
        }
    }
    success(message) {
        console.log(`[${this.prefix}] ✅ ${message}`);
    }
    step(step, total, message) {
        console.log(`[${this.prefix}] [${step}/${total}] ${message}`);
    }
}
exports.Logger = Logger;
exports.logger = new Logger();
