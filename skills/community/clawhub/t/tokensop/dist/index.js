"use strict";
/**
 * ClawMind Skill Entry Point
 *
 * Exports the two hooks registered in skill.json:
 * - interceptIntent: fires on every user intent, queries cloud for cached macros
 * - onSessionComplete: fires after successful sessions, contributes new workflows
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.onSessionComplete = exports.interceptIntent = void 0;
var interceptor_js_1 = require("./interceptor.js");
Object.defineProperty(exports, "interceptIntent", { enumerable: true, get: function () { return interceptor_js_1.interceptIntent; } });
Object.defineProperty(exports, "onSessionComplete", { enumerable: true, get: function () { return interceptor_js_1.onSessionComplete; } });
