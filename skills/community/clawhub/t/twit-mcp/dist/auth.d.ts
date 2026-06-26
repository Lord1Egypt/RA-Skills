declare const CREDENTIALS_FILE: string;
export type TwitterCredentials = {
    authToken: string;
    ct0: string;
    username?: string;
};
export declare function loadCredentials(): TwitterCredentials | null;
export declare function saveCredentials(creds: TwitterCredentials): void;
export declare function clearCredentials(): void;
export { CREDENTIALS_FILE as CREDS_PATH };
