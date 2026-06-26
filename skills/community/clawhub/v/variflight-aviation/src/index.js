/**
 * Variflight Aviation Skill - Main Entry
 * OpenClaw Skill for flight information query (Powered by VariFlight MCP)
 */

const { VariflightClient } = require('./lib/variflight-client');

// 导出核心类供外部使用
module.exports = {
    VariflightClient,

    // 便捷方法：创建客户端实例
    createClient: () => new VariflightClient(),

    // Skill 元数据
    metadata: {
        name: 'variflight-aviation',
        version: '3.0.0',
        description: '航班信息查询（飞常准 MCP 官方方案）'
    }
};
