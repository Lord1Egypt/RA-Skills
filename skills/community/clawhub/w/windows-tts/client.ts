import { WindowsTtsClientLike, PluginConfig, TtsStatusResponse, TtsNotifyInput, VoiceInfo, TtsListVoicesInput, TtsSetVolumeInput, WindowsTtsError } from "./types";

const DEFAULT_TIMEOUT_MS = 10_000;

export class WindowsTtsClient implements WindowsTtsClientLike {
  private readonly baseUrl: string;
  private readonly timeoutMs: number;
  private readonly defaultVoice: string;
  private readonly defaultVolume: number;

  public constructor(private readonly config: PluginConfig) {
    this.baseUrl = config.url.replace(/\/$/, "");
    this.timeoutMs = config.timeout ?? DEFAULT_TIMEOUT_MS;
    this.defaultVoice = config.defaultVoice ?? "zh-CN-XiaoxiaoNeural";
    this.defaultVolume = config.defaultVolume ?? 1.0;
  }

  public async checkConnection(): Promise<boolean> {
    const status = await this.getStatus();
    return status.connected === true;
  }

  public async getStatus(): Promise<TtsStatusResponse> {
    try {
      await this.request<TtsStatusResponse>("GET", "/status");
      return {
        status: "success",
        connected: true,
        serverUrl: this.baseUrl
      };
    } catch (error) {
      if (error instanceof WindowsTtsError) {
        return {
          status: "error",
          message: `Server returned ${error.status}`,
          connected: false,
          serverUrl: this.baseUrl
        };
      }
      return {
        status: "error",
        message: error instanceof Error ? error.message : "Unknown error",
        connected: false,
        serverUrl: this.baseUrl
      };
    }
  }

  public async notify(input: TtsNotifyInput): Promise<TtsStatusResponse> {
    if (!input.text || input.text.trim().length === 0) {
      throw new Error("text is required and cannot be empty");
    }

    const body = {
      text: input.text,
      voice: input.voice ?? this.defaultVoice,
      volume: input.volume ?? this.defaultVolume
    };

    return this.request<TtsStatusResponse>("POST", "/play_tts", body);
  }

  public async listVoices(input?: TtsListVoicesInput): Promise<VoiceInfo[]> {
    const params = new URLSearchParams();
    if (input?.language) {
      params.set("language", input.language);
    }

    const suffix = params.toString() ? `?${params.toString()}` : "";
    return this.request<VoiceInfo[]>("GET", `/voices${suffix}`);
  }

  public async setVolume(input: TtsSetVolumeInput): Promise<TtsStatusResponse> {
    if (input.volume < 0 || input.volume > 1) {
      throw new Error("volume must be between 0.0 and 1.0");
    }

    return this.request<TtsStatusResponse>("POST", "/volume", { volume: input.volume });
  }

  private async request<T>(method: string, path: string, body?: unknown): Promise<T> {
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), this.timeoutMs);

    let response: Response;
    try {
      response = await fetch(`${this.baseUrl}${path}`, {
        method,
        headers: {
          "Content-Type": "application/json"
        },
        body: body === undefined ? undefined : JSON.stringify(body),
        signal: controller.signal
      });
    } catch (err: unknown) {
      if (err instanceof DOMException && err.name === "AbortError") {
        throw new Error(`Windows TTS request timed out after ${this.timeoutMs}ms: ${method} ${path}`);
      }
      throw err;
    } finally {
      clearTimeout(timer);
    }

    const raw = await response.text();
    if (!response.ok) {
      throw new WindowsTtsError(response.status, raw);
    }

    if (raw.length === 0) {
      return { status: "success" } as T;
    }

    try {
      return JSON.parse(raw) as T;
    } catch {
      return raw as T;
    }
  }
}
