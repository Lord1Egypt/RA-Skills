import { WindowsTtsClientLike, PluginConfig, TtsStatusResponse, TtsNotifyInput, VoiceInfo, TtsListVoicesInput, TtsSetVolumeInput } from "./types";
export declare class WindowsTtsClient implements WindowsTtsClientLike {
    private readonly config;
    private readonly baseUrl;
    private readonly timeoutMs;
    private readonly defaultVoice;
    private readonly defaultVolume;
    constructor(config: PluginConfig);
    checkConnection(): Promise<boolean>;
    getStatus(): Promise<TtsStatusResponse>;
    notify(input: TtsNotifyInput): Promise<TtsStatusResponse>;
    listVoices(input?: TtsListVoicesInput): Promise<VoiceInfo[]>;
    setVolume(input: TtsSetVolumeInput): Promise<TtsStatusResponse>;
    private request;
}
