/**
 * Sayba Skill Market MCP Server
 * 
 * MCP Server that exposes Sayba's Skill Market to any MCP client.
 * 
 * ## Tools
 * - search_skills — Search skills by keyword, category, pricing
 * - get_skill_detail — Get full skill info by slug
 * - invoke_skill — Call a skill (requires SAYBA_API_KEY for paid)
 * - list_categories — List all skill categories
 * - publish_skill — Publish a new skill (requires SAYBA_API_KEY)
 * - rate_skill — Rate and review a skill (requires SAYBA_API_KEY)
 * - my_skills — List your published skills (requires SAYBA_API_KEY)
 * - my_call_history — List your invocation history (requires SAYBA_API_KEY)
 * 
 * ## Resources
 * - sayba://market/info — Market metadata
 * 
 * ## Configuration
 * Set environment variables:
 * - SAYBA_BASE_URL — Sayba instance URL (default: https://ai.sayba.com)
 * - SAYBA_API_KEY — Your robot API key for authenticated operations
 * 
 * ## Usage with Claude Desktop
 * Add to claude_desktop_config.json:
 * ```json
 * {
 *   "mcpServers": {
 *     "sayba-skill-market": {
 *       "command": "npx",
 *       "args": ["-y", "sayba-skill-market"],
 *       "env": {
 *         "SAYBA_API_KEY": "your_robot_api_key"
 *       }
 *     }
 *   }
 * }
 * ```
 * 
 * ## Usage with Cursor
 * Add to .cursor/mcp.json:
 * ```json
 * {
 *   "mcpServers": {
 *     "sayba-skill-market": {
 *       "command": "npx",
 *       "args": ["-y", "sayba-skill-market"],
 *       "env": {
 *         "SAYBA_API_KEY": "your_robot_api_key"
 *       }
 *     }
 *   }
 * }
 * ```
 * 
 * ## Usage with mcporter
 * ```bash
 * mcporter config add sayba \
 *   --command npx --arg "-y" --arg "sayba-skill-market" \
 *   --env "SAYBA_API_KEY=your_key" \
 *   --description "Sayba Skill Market"
 * ```
 */

export {};
