import { OpenClawApi } from "./types";
export default function init(api: OpenClawApi): void;
export declare const manifest: {
    name: string;
    version: string;
    description: string;
    tools: string[];
    config: {
        url: {
            type: string;
            required: boolean;
            description: string;
        };
        defaultVoice: {
            type: string;
            required: boolean;
            default: string;
            description: string;
        };
        defaultVolume: {
            type: string;
            required: boolean;
            default: number;
            description: string;
        };
        timeout: {
            type: string;
            required: boolean;
            default: number;
            description: string;
        };
    };
};
export { createTools } from "./tools";
export { WindowsTtsClient } from "./client";
export { validateConfig } from "./config";
export type { PluginConfig } from "./config";
export type { TtsNotifyInput, TtsListVoicesInput, TtsSetVolumeInput, TtsStatusResponse, VoiceInfo, WindowsTtsClientLike, WindowsTtsError } from "./types";
