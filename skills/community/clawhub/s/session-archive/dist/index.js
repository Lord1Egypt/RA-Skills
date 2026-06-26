import { join } from "node:path";
import { homedir } from "node:os";
import { createSessionArchiveDb } from "./db.js";
import { SessionArchiveEngine } from "./engine.js";
function resolveDbPath(dbPath) {
    if (dbPath && dbPath.trim())
        return dbPath.trim();
    return join(homedir(), ".openclaw", "session-archive.db");
}
const sessionArchivePlugin = {
    id: "session-archive",
    name: "Session Archive",
    description: "Archive every conversation message to SQLite in real-time",
    configSchema: {
        parse(value) {
            const raw = value && typeof value === "object" && !Array.isArray(value)
                ? value
                : {};
            return {
                dbPath: typeof raw.dbPath === "string" ? raw.dbPath.trim() : undefined,
            };
        },
    },
    register(api) {
        const pluginConfig = api.pluginConfig && typeof api.pluginConfig === "object" && !Array.isArray(api.pluginConfig)
            ? api.pluginConfig
            : undefined;
        const dbPath = typeof pluginConfig?.dbPath === "string" ? pluginConfig.dbPath : undefined;
        const db = createSessionArchiveDb(dbPath);
        const engine = new SessionArchiveEngine(db);
        // 注册为 session-archive（总是成功）
        api.registerContextEngine("session-archive", () => engine);
        // 尝试注册为 default（失败不影响主功能）
        // 注意：OpenClaw 支持多个插件注册同一个 name，都会触发
        try {
            api.registerContextEngine("default", () => engine);
        }
        catch (e) {
            // 静默失败，不影响主功能
        }
        api.logger.info(`[session-archive] Plugin loaded (db=${resolveDbPath(dbPath)})`);
    },
};
export default sessionArchivePlugin;
