"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.WindowsTtsError = void 0;
class WindowsTtsError extends Error {
    constructor(status, body) {
        super(`Windows TTS error: ${status} - ${body}`);
        this.status = status;
        this.body = body;
        this.name = "WindowsTtsError";
    }
}
exports.WindowsTtsError = WindowsTtsError;
