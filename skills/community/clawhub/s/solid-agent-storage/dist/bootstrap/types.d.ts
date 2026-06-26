export interface AgentConfig {
    name: string;
    displayName: string;
    serverUrl: string;
    capabilities?: string[];
}
export interface ProvisionedAgent {
    webId: string;
    podUrl: string;
    email: string;
    password: string;
    clientCredentials: {
        id: string;
        secret: string;
    };
    config: AgentConfig;
}
export interface CssAccount {
    cookie: string;
    accountUrl: string;
}
