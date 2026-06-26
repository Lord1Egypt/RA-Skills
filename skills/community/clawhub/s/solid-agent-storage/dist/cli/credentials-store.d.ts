export interface StoredCredentials {
    webId: string;
    podUrl: string;
    id: string;
    secret: string;
    email?: string;
    password?: string;
}
export declare function initStore(passphrase: string): void;
export declare function isStoreInitialised(): boolean;
export declare function saveCredentials(name: string, credentials: StoredCredentials): void;
export declare function loadCredentials(name: string): StoredCredentials;
export declare function deleteAgentCredentials(name: string): void;
export declare function listAgents(): string[];
