export interface PluginConfig {
    url: string;
    defaultVoice?: string;
    defaultVolume?: number;
    timeout?: number;
}
export interface TtsNotifyInput {
    text: string;
    voice?: string;
    volume?: number;
}
export interface TtsSetVolumeInput {
    volume: number;
}
export interface TtsListVoicesInput {
    language?: string;
}
export interface VoiceInfo {
    name: string;
    language: string;
    gender: string;
    style?: string;
}
export interface TtsStatusResponse {
    status: "success" | "error";
    message?: string;
    serverUrl?: string;
    connected?: boolean;
}
export interface WindowsTtsClientLike {
    checkConnection(): Promise<boolean>;
    getStatus(): Promise<TtsStatusResponse>;
    notify(input: TtsNotifyInput): Promise<TtsStatusResponse>;
    listVoices(input?: TtsListVoicesInput): Promise<VoiceInfo[]>;
    setVolume(input: TtsSetVolumeInput): Promise<TtsStatusResponse>;
}
export declare class WindowsTtsError extends Error {
    readonly status: number;
    readonly body: string;
    constructor(status: number, body: string);
}
export interface OpenClawApi {
    config?: Record<string, unknown>;
    registerTool?: (name: string, handler: (input: unknown) => Promise<unknown>) => void;
    tool?: (name: string, handler: (input: unknown) => Promise<unknown>) => void;
}
