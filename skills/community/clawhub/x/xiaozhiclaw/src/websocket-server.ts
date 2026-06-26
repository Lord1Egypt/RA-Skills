import WebSocket, { WebSocketServer } from "ws";
import type { ChannelContext } from "openclaw/plugin-sdk";
import { createAudioStream, type AudioConfig } from "./audio-stream.js";
import { createDoubaoService, type DoubaoConfig } from "./doubao-service.js";

interface XiaoZhiMessage {
  type: string;
  state?: string;
  text?: string;
  audio?: Buffer;
}

interface DeviceSession {
  ws: WebSocket;
  audioStream: any;
  audioBuffer: Buffer[];
  isListening: boolean;
  doubaoService: any;
}

let wss: WebSocketServer | null = null;
const clients = new Map<string, DeviceSession>();
const AUDIO_CONFIG: AudioConfig = {
  sampleRate: 16000,
  frameDuration: 60,
  channels: 1,
};

// Doubao configuration
const DOUBAO_CONFIG: DoubaoConfig = {
  appId: process.env.DOUBAO_APP_ID || '',
  accessToken: process.env.DOUBAO_ACCESS_TOKEN || '',
  cluster: 'volcano_tts',
  apiHost: 'openspeech.bytedance.com',
};

export function startXiaozhiWebSocketServer(
  port: number,
  ctx: ChannelContext
) {
  wss = new WebSocketServer({ port });

  wss.on("connection", (ws: WebSocket, req) => {
    const deviceId = req.url?.split("?")[0].slice(1) || "unknown";
    console.log(`🎤 XiaoZhi device connected: ${deviceId}`);
    
    const audioStream = createAudioStream(AUDIO_CONFIG);
    const doubaoService = createDoubaoService(DOUBAO_CONFIG);
    
    clients.set(deviceId, {
      ws,
      audioStream,
      audioBuffer: [],
      isListening: false,
      doubaoService,
    });

    ws.on("message", async (data: Buffer) => {
      try {
        const message: XiaoZhiMessage = JSON.parse(data.toString());
        await handleXiaozhiMessage(deviceId, message, ctx);
      } catch (error) {
        // Binary audio data - process through Opus decoder
        const session = clients.get(deviceId);
        if (session && session.isListening) {
          session.audioBuffer.push(data);
          // Decode and buffer for STT processing
          try {
            const pcm = session.audioStream.decodeOpus(data);
            // Buffer PCM data for STT processing
          } catch (err) {
            console.error("Opus decode error:", err);
          }
        }
      }
    });

    ws.on("close", () => {
      console.log(`🔌 XiaoZhi device disconnected: ${deviceId}`);
      const session = clients.get(deviceId);
      if (session) {
        session.audioStream.cleanup();
      }
      clients.delete(deviceId);
    });

    // Send hello response
    ws.send(JSON.stringify({
      type: "hello",
      transport: "websocket",
      audio_params: AUDIO_CONFIG
    }));
  });

  console.log(`🚀 XiaoZhi WebSocket server listening on port ${port}`);
  console.log(`🤖 Doubao STT/TTS service initialized`);
}

async function handleXiaozhiMessage(
  deviceId: string,
  message: XiaoZhiMessage,
  ctx: ChannelContext
) {
  console.log(`💬 Message from ${deviceId}:`, message.type, message.state);

  if (message.type === "listen") {
    const session = clients.get(deviceId);
    if (!session) return;

    if (message.state === "start") {
      // Start listening
      session.isListening = true;
      session.audioBuffer = [];
      console.log(`🎤 Start listening from ${deviceId}`);
    } else if (message.state === "stop") {
      // Stop listening and process
      session.isListening = false;
      console.log(`⏹️ Stop listening from ${deviceId}`);
      
      let userText = message.text;
      
      // If no text provided, use STT to transcribe audio
      if (!userText && session.audioBuffer.length > 0) {
        try {
          console.log(`🎙️ Processing STT for ${deviceId}...`);
          // Concatenate all audio frames
          const fullAudio = Buffer.concat(session.audioBuffer);
          // Convert Opus to WAV for Doubao STT
          const wavData = session.audioStream.pcmToWav(
            session.audioBuffer.flatMap(buf => session.audioStream.decodeOpus(buf)),
            AUDIO_CONFIG.sampleRate
          );
          // Call Doubao STT API
          userText = await session.doubaoService.speechToText(wavData, AUDIO_CONFIG.sampleRate);
          console.log(`📝 STT result: "${userText}"`);
        } catch (error) {
          console.error("STT error:", error);
          userText = "Sorry, I couldn't understand that.";
        }
      }
      
      userText = userText || "Hello PocketAI!";
      
      // Send to OpenClaw for processing
      const response = await ctx.agent.processMessage({
        from: deviceId,
        text: userText,
        channel: "xiaozhi",
      });

      // Send TTS response back
      if (response && response.text) {
        await sendTTSResponse(deviceId, response.text, session);
      }
    }
  }
}

async function sendTTSResponse(deviceId: string, text: string, session: DeviceSession) {
  console.log(`🔊 Sending TTS response: "${text}"`);

  // Send TTS start
  session.ws.send(JSON.stringify({
    type: "tts",
    state: "start",
    text: text
  }));

  try {
    // Call Doubao TTS API
    console.log(`🤖 Calling Doubao TTS...`);
    const ttsAudio = await session.doubaoService.textToSpeech(text);
    
    // Convert WAV to PCM, then encode to Opus
    const pcmData = session.audioStream.wavToPcm(ttsAudio);
    
    // Stream Opus frames to device
    const frameSize = Math.floor((AUDIO_CONFIG.sampleRate * AUDIO_CONFIG.frameDuration) / 1000);
    for (let i = 0; i < pcmData.length; i += frameSize) {
      const chunk = pcmData.slice(i, i + frameSize);
      const opusFrame = session.audioStream.encodeOpus(chunk);
      if (opusFrame.length > 0) {
        session.ws.send(opusFrame);
        // Small delay to simulate real-time streaming
        await new Promise(resolve => setTimeout(resolve, AUDIO_CONFIG.frameDuration));
      }
    }
    
    console.log(`✅ TTS response complete`);
    
    // Send TTS stop
    session.ws.send(JSON.stringify({
      type: "tts",
      state: "stop"
    }));
  } catch (error) {
    console.error("TTS error:", error);
    session.ws.send(JSON.stringify({
      type: "tts",
      state: "stop"
    }));
  }
}

export function stopXiaozhiWebSocketServer() {
  if (wss) {
    wss.close();
    wss = null;
  }
  // Cleanup all sessions
  clients.forEach((session) => {
    session.audioStream.cleanup();
  });
  clients.clear();
}
