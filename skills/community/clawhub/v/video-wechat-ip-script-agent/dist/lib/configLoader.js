"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.loadJsonConfig = loadJsonConfig;
const node_fs_1 = __importDefault(require("node:fs"));
const node_path_1 = __importDefault(require("node:path"));
function resolveProjectRoot(rootDir) {
    if (rootDir)
        return rootDir;
    const currentDir = node_path_1.default.resolve(__dirname, "..");
    const configPath = node_path_1.default.join(currentDir, "config");
    if (node_fs_1.default.existsSync(configPath))
        return currentDir;
    return node_path_1.default.resolve(currentDir, "..");
}
function loadJsonConfig(fileName, rootDir) {
    const projectRoot = resolveProjectRoot(rootDir);
    const configPath = node_path_1.default.join(projectRoot, "config", fileName);
    return JSON.parse(node_fs_1.default.readFileSync(configPath, "utf8"));
}
