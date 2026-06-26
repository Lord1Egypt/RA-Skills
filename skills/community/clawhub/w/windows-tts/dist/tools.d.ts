import { WindowsTtsClient } from "./client";
import { PluginConfig, TtsNotifyInput, TtsListVoicesInput, TtsSetVolumeInput, TtsStatusResponse, VoiceInfo } from "./types";
export declare function createTools({ client, config }: {
    client: WindowsTtsClient;
    config: PluginConfig;
}): {
    /**
     * Send text to Windows TTS for audio broadcast
     * @param input - Text and optional voice/volume settings
     * @returns Status response from TTS server
     */
    tts_notify: (input: TtsNotifyInput) => Promise<TtsStatusResponse>;
    /**
     * Check Windows TTS server connection status
     * @returns Server status and connection info
     */
    tts_get_status: () => Promise<TtsStatusResponse>;
    /**
     * List available Azure TTS voices
     * @param input - Optional language filter (e.g., "zh-CN" for Chinese)
     * @returns List of available voices
     */
    tts_list_voices: (input?: TtsListVoicesInput) => Promise<VoiceInfo[]>;
    /**
     * Set default volume level for TTS playback
     * @param input - Volume level (0.0-1.0)
     * @returns Status response
     */
    tts_set_volume: (input: TtsSetVolumeInput) => Promise<TtsStatusResponse>;
};
