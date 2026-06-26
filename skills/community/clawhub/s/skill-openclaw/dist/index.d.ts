/**
 * First-run setup flow for the Oris OpenClaw skill.
 *
 * Sequence:
 *   1. Check if already configured (abort unless forced)
 *   2. Validate API key format (oris_sk_live_ prefix, min length)
 *   3. Validate API secret format (oris_ss_live_ prefix, min length)
 *   4. Register agent via SDK
 *   5. Create ERC-4337 wallet on Base
 *   6. Set default spending policy
 *   7. Write all credentials to OpenClaw config store
 */
interface SetupInput {
    apiKey: string;
    apiSecret: string;
}
interface SetupOptions {
    force?: boolean;
}
interface SetupResult {
    agentId: string;
    walletAddress: string;
    chain: string;
    tier: string;
}
declare function validateApiKey(key: string): boolean;
declare function validateApiSecret(secret: string): boolean;
declare function runSetup(input: SetupInput, options?: SetupOptions): Promise<SetupResult>;

/**
 * Command definitions mapping to the 13 MCP server tools.
 *
 * Each command provides:
 *   - name: short command name used by OpenClaw LLM for routing
 *   - toolName: exact MCP tool identifier (matches tools.py)
 *   - description: concise explanation for ClawHub listing and LLM decision-making
 */
interface CommandDefinition {
    name: string;
    toolName: string;
    description: string;
}
declare const COMMANDS: CommandDefinition[];

/**
 * OpenClaw native configuration module.
 *
 * Stores all credentials in OpenClaw's standard config store at
 * ~/.openclaw/config.json. This follows OpenClaw's convention where
 * each skill writes its credentials to the shared config file.
 *
 * The MCP server reads these values as environment variables at runtime.
 * OpenClaw's skill runner maps config entries to env vars based on the
 * SKILL.md frontmatter.
 */
declare const CONFIG_DIR: string;
declare const CONFIG_FILE_NAME = "config.json";
interface OrisConfig {
    apiKey: string;
    apiSecret: string;
    agentId: string;
    walletAddress: string;
    chain: string;
    configuredAt?: string;
}
/**
 * Write Oris credentials to OpenClaw's native config store.
 */
declare function writeConfig(data: OrisConfig): Promise<void>;
/**
 * Read Oris credentials from OpenClaw's config store.
 */
declare function readConfig(): Promise<OrisConfig | null>;
/**
 * Check whether Oris configuration exists.
 */
declare function hasConfig(): Promise<boolean>;
/**
 * Remove Oris configuration from OpenClaw config store.
 * Preserves other skills' configuration.
 */
declare function clearConfig(): Promise<void>;

/**
 * Error translation layer.
 *
 * Converts Oris API error codes and HTTP failures into human-readable
 * messages. OpenClaw agents surface these messages to users, so they
 * must be clear and actionable.
 */
/**
 * Translate an API error into a human-readable message.
 *
 * Accepts the operation name and the raw error object from the SDK.
 * Returns a single string suitable for display to the user.
 */
declare function translateError(operation: string, err: unknown): string;
/**
 * Translate a tool execution error from MCP server response.
 *
 * Accepts the raw error object from the MCP tool call result
 * and returns a user-facing message.
 */
declare function translateToolError(toolName: string, error: Record<string, unknown>): string;

export { COMMANDS, CONFIG_DIR, CONFIG_FILE_NAME, type CommandDefinition, type OrisConfig, type SetupInput, type SetupOptions, type SetupResult, clearConfig, hasConfig, readConfig, runSetup, translateError, translateToolError, validateApiKey, validateApiSecret, writeConfig };
