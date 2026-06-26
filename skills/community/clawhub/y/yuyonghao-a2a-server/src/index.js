/**
 * A2A Server - Agent-to-Agent Communication System
 * 
 * Main entry point - exports A2AServer and A2AClient
 * 
 * @version 0.1.0
 * @author 小蒲萄 (Clawd)
 */

const { A2AServer } = require('./server');
const { A2AClient } = require('./client');

module.exports = {
  A2AServer,
  A2AClient,
};
