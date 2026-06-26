"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.createTools = createTools;
function createTools({ client, config }) {
    return {
        /**
         * Send text to Windows TTS for audio broadcast
         * @param input - Text and optional voice/volume settings
         * @returns Status response from TTS server
         */
        tts_notify: async (input) => {
            if (!input.text || input.text.trim().length === 0) {
                throw new Error("text is required for TTS notification");
            }
            return client.notify({
                text: input.text,
                voice: input.voice,
                volume: input.volume
            });
        },
        /**
         * Check Windows TTS server connection status
         * @returns Server status and connection info
         */
        tts_get_status: async () => {
            return client.getStatus();
        },
        /**
         * List available Azure TTS voices
         * @param input - Optional language filter (e.g., "zh-CN" for Chinese)
         * @returns List of available voices
         */
        tts_list_voices: async (input) => {
            return client.listVoices(input);
        },
        /**
         * Set default volume level for TTS playback
         * @param input - Volume level (0.0-1.0)
         * @returns Status response
         */
        tts_set_volume: async (input) => {
            if (input.volume < 0 || input.volume > 1) {
                throw new Error("volume must be between 0.0 and 1.0");
            }
            return client.setVolume(input);
        }
    };
}
