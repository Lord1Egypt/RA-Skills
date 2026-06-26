import { AgentConfig, ProvisionedAgent } from './types.js';
/**
 * Full agent provisioning flow:
 * 1. Create CSS account
 * 2. Add password login
 * 3. Create pod at /agents/{name}/
 * 4. Create client credentials
 * 5. Patch WebID profile with agent metadata
 * 6. Create standard container structure
 */
export declare function provisionAgent(config: AgentConfig): Promise<ProvisionedAgent>;
