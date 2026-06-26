"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.TorkConfigSchema = void 0;
const zod_1 = require("zod");
exports.TorkConfigSchema = zod_1.z.object({
    apiKey: zod_1.z.string().min(1),
    baseUrl: zod_1.z.string().url().default('https://tork.network'),
    policy: zod_1.z.enum(['strict', 'standard', 'minimal']).default('standard'),
    redactPII: zod_1.z.boolean().default(true),
    blockShellCommands: zod_1.z.array(zod_1.z.string()).default([
        'rm -rf',
        'mkfs',
        'dd if=',
        'chmod 777',
        ':(){:|:&};:',
        'shutdown',
        'reboot',
        'halt',
        'init 0',
        'init 6',
    ]),
    allowedPaths: zod_1.z.array(zod_1.z.string()).default([]),
    blockedPaths: zod_1.z.array(zod_1.z.string()).default([
        '/etc/shadow',
        '/etc/passwd',
        '~/.ssh',
        '~/.aws',
        '~/.env',
        '.env',
        '.env.local',
        'credentials.json',
        'id_rsa',
        'id_ed25519',
    ]),
    // Network policy configuration
    networkPolicy: zod_1.z.enum(['default', 'strict', 'custom']).default('default'),
    allowedInboundPorts: zod_1.z.array(zod_1.z.number().int().min(0).max(65535)).optional(),
    allowedOutboundPorts: zod_1.z.array(zod_1.z.number().int().min(0).max(65535)).optional(),
    allowedDomains: zod_1.z.array(zod_1.z.string()).optional(),
    blockedDomains: zod_1.z.array(zod_1.z.string()).optional(),
    maxConnectionsPerMinute: zod_1.z.number().int().min(1).optional(),
});
//# sourceMappingURL=config.js.map