/**
 * WebSocket Relay Server for telebiz-tt MCP Bridge
 *
 * This relay server connects:
 * - Browser (executor): has the authenticated Telegram session
 * - MCP clients: send tool execution requests
 *
 * Protocol:
 * - Executor sends: { type: 'register', role: 'executor' }
 * - Client sends: { type: 'register', role: 'client' }
 * - Client sends: { id, type: 'execute', tool, args }
 * - Relay forwards to executor, returns response to client
 *
 * Features:
 * - Connection tracking with metrics
 * - Heartbeat/ping support
 * - Graceful shutdown
 * - Status reporting
 */
export {};
