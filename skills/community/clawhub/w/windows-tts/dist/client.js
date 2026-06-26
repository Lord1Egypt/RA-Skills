"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.WindowsTtsClient = void 0;
const types_1 = require("./types");
const DEFAULT_TIMEOUT_MS = 10000;
class WindowsTtsClient {
    constructor(config) {
        this.config = config;
        this.baseUrl = config.url.replace(/\/$/, "");
        this.timeoutMs = config.timeout ?? DEFAULT_TIMEOUT_MS;
        this.defaultVoice = config.defaultVoice ?? "zh-CN-XiaoxiaoNeural";
        this.defaultVolume = config.defaultVolume ?? 1.0;
    }
    async checkConnection() {
        const status = await this.getStatus();
        return status.connected === true;
    }
    async getStatus() {
        try {
            await this.request("GET", "/status");
            return {
                status: "success",
                connected: true,
                serverUrl: this.baseUrl
            };
        }
        catch (error) {
            if (error instanceof types_1.WindowsTtsError) {
                return {
                    status: "error",
                    message: `Server returned ${error.status}`,
                    connected: false,
                    serverUrl: this.baseUrl
                };
            }
            return {
                status: "error",
                message: error instanceof Error ? error.message : "Unknown error",
                connected: false,
                serverUrl: this.baseUrl
            };
        }
    }
    async notify(input) {
        if (!input.text || input.text.trim().length === 0) {
            throw new Error("text is required and cannot be empty");
        }
        const body = {
            text: input.text,
            voice: input.voice ?? this.defaultVoice,
            volume: input.volume ?? this.defaultVolume
        };
        return this.request("POST", "/play_tts", body);
    }
    async listVoices(input) {
        const params = new URLSearchParams();
        if (input?.language) {
            params.set("language", input.language);
        }
        const suffix = params.toString() ? `?${params.toString()}` : "";
        return this.request("GET", `/voices${suffix}`);
    }
    async setVolume(input) {
        if (input.volume < 0 || input.volume > 1) {
            throw new Error("volume must be between 0.0 and 1.0");
        }
        return this.request("POST", "/volume", { volume: input.volume });
    }
    async request(method, path, body) {
        const controller = new AbortController();
        const timer = setTimeout(() => controller.abort(), this.timeoutMs);
        let response;
        try {
            response = await fetch(`${this.baseUrl}${path}`, {
                method,
                headers: {
                    "Content-Type": "application/json"
                },
                body: body === undefined ? undefined : JSON.stringify(body),
                signal: controller.signal
            });
        }
        catch (err) {
            if (err instanceof DOMException && err.name === "AbortError") {
                throw new Error(`Windows TTS request timed out after ${this.timeoutMs}ms: ${method} ${path}`);
            }
            throw err;
        }
        finally {
            clearTimeout(timer);
        }
        const raw = await response.text();
        if (!response.ok) {
            throw new types_1.WindowsTtsError(response.status, raw);
        }
        if (raw.length === 0) {
            return { status: "success" };
        }
        try {
            return JSON.parse(raw);
        }
        catch {
            return raw;
        }
    }
}
exports.WindowsTtsClient = WindowsTtsClient;
