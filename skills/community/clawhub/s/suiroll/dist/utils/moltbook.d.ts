/**
 * Moltbook API Integration
 * Authentication and identity verification for AI agents
 */
export interface MoltbookAgent {
    id: string;
    name: string;
    description: string;
    karma: number;
    avatar_url?: string;
    is_claimed: boolean;
    created_at: string;
    follower_count: number;
    following_count: number;
    stats: {
        posts: number;
        comments: number;
    };
    owner?: {
        x_handle: string;
        x_name: string;
        x_avatar?: string;
        x_verified: boolean;
        x_follower_count: number;
    };
}
export interface IdentityToken {
    success: boolean;
    identity_token: string;
    expires_in: number;
    expires_at: string;
    audience?: string;
}
export interface VerificationResponse {
    success: boolean;
    valid: boolean;
    agent: MoltbookAgent;
    error?: string;
    hint?: string;
}
/**
 * Get Moltbook API key from environment or credentials file
 */
export declare function getMoltbookApiKey(): string | null;
/**
 * Get Moltbook app key (developer API key) for verification
 */
export declare function getMoltbookAppKey(): string | null;
/**
 * Get the audience value for token verification
 */
export declare function getAudience(): string;
/**
 * Generate a temporary identity token for the agent
 * This is called by the bot to get a token to authenticate with external services
 */
export declare function generateIdentityToken(apiKey: string, audience?: string): Promise<IdentityToken>;
/**
 * Verify an identity token and get agent information
 * This is called by the external service to verify the bot's identity
 */
export declare function verifyIdentityToken(token: string, audience?: string): Promise<MoltbookAgent>;
/**
 * Interactive login - prompt for credentials and get API key
 * For CLI use when no saved credentials exist
 */
export declare function interactiveLogin(): Promise<{
    apiKey: string;
    agent: MoltbookAgent;
}>;
/**
 * Get agent information from stored credentials
 * Reads from ~/.config/moltbook/credentials.json
 */
export declare function getAgentFromCredentials(): Promise<{
    apiKey: string;
    agent: MoltbookAgent;
} | null>;
/**
 * Format agent information for display
 */
export declare function formatAgentInfo(agent: MoltbookAgent): string;
//# sourceMappingURL=moltbook.d.ts.map