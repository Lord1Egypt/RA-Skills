// Audio streaming utilities for XiaoZhi ESP32
// Handles Opus encoding/decoding for real-time voice communication

import { OpusEncoder, OpusDecoder } from "opusscript";

export interface AudioConfig {
  sampleRate: number;
  frameDuration: number;
  channels: number;
}

export const DEFAULT_AUDIO_CONFIG: AudioConfig = {
  sampleRate: 16000,
  frameDuration: 60, // ms
  channels: 1,
};

export class AudioStream {
  private config: AudioConfig;
  private encoder: OpusEncoder | null = null;
  private decoder: OpusDecoder | null = null;

  constructor(config: AudioConfig = DEFAULT_AUDIO_CONFIG) {
    this.config = config;
  }

  /**
   * Initialize Opus encoder
   */
  initEncoder(): void {
    const frameSize = Math.floor(
      (this.config.sampleRate * this.config.frameDuration) / 1000
    );
    this.encoder = new OpusEncoder(this.config.sampleRate, this.config.channels, OpusEncoder.Application.AUDIO);
    this.encoder.encoderCTL(4096, frameSize); // OPUS_SET_BITRATE
  }

  /**
   * Initialize Opus decoder
   */
  initDecoder(): void {
    this.decoder = new OpusDecoder(this.config.sampleRate, this.config.channels);
  }

  /**
   * Decode Opus audio frame to PCM
   */
  decodeOpus(opusFrame: Buffer): Int16Array {
    if (!this.decoder) {
      this.initDecoder();
    }
    
    try {
      const frameSize = Math.floor(
        (this.config.sampleRate * this.config.frameDuration) / 1000
      );
      return this.decoder!.decode(opusFrame, frameSize);
    } catch (error) {
      console.error("Opus decode error:", error);
      const samples = Math.floor(
        (this.config.sampleRate * this.config.frameDuration) / 1000
      );
      return new Int16Array(samples);
    }
  }

  /**
   * Encode PCM audio to Opus frame
   */
  encodeOpus(pcmData: Int16Array): Buffer {
    if (!this.encoder) {
      this.initEncoder();
    }
    
    try {
      return this.encoder!.encode(pcmData, pcmData.length);
    } catch (error) {
      console.error("Opus encode error:", error);
      return Buffer.alloc(0);
    }
  }

  /**
   * Convert PCM to WAV format for TTS processing
   */
  pcmToWav(pcmData: Int16Array, sampleRate: number): Buffer {
    const numChannels = 1;
    const bitsPerSample = 16;
    const byteRate = (sampleRate * numChannels * bitsPerSample) / 8;
    const blockAlign = (numChannels * bitsPerSample) / 8;

    const dataSize = pcmData.length * 2; // 16-bit = 2 bytes
    const bufferSize = 44 + dataSize;

    const buffer = Buffer.alloc(bufferSize);
    let offset = 0;

    // RIFF header
    buffer.write("RIFF", offset);
    offset += 4;
    buffer.writeUInt32LE(bufferSize - 8, offset);
    offset += 4;
    buffer.write("WAVE", offset);
    offset += 4;

    // fmt chunk
    buffer.write("fmt ", offset);
    offset += 4;
    buffer.writeUInt32LE(16, offset); // fmt chunk size
    offset += 4;
    buffer.writeUInt16LE(1, offset); // PCM format
    offset += 2;
    buffer.writeUInt16LE(numChannels, offset);
    offset += 2;
    buffer.writeUInt32LE(sampleRate, offset);
    offset += 2;
    buffer.writeUInt32LE(byteRate, offset);
    offset += 2;
    buffer.writeUInt16LE(blockAlign, offset);
    offset += 2;
    buffer.writeUInt16LE(bitsPerSample, offset);
    offset += 2;

    // data chunk
    buffer.write("data", offset);
    offset += 4;
    buffer.writeUInt32LE(dataSize, offset);
    offset += 4;

    // Write PCM data
    for (let i = 0; i < pcmData.length; i++) {
      buffer.writeInt16LE(pcmData[i], offset);
      offset += 2;
    }

    return buffer;
  }

  /**
   * Convert WAV to PCM for playback
   */
  wavToPcm(wavData: Buffer): Int16Array {
    // Skip 44-byte WAV header
    const pcmData = wavData.slice(44);
    const samples = new Int16Array(pcmData.length / 2);

    for (let i = 0; i < samples.length; i++) {
      samples[i] = wavData.readInt16LE(44 + i * 2);
    }

    return samples;
  }

  /**
   * Cleanup resources
   */
  cleanup(): void {
    if (this.encoder) {
      this.encoder.delete();
      this.encoder = null;
    }
    if (this.decoder) {
      this.decoder.delete();
      this.decoder = null;
    }
  }
}

export function createAudioStream(config?: AudioConfig): AudioStream {
  return new AudioStream(config);
}
