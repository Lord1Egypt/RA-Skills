/**
 * Type definitions for the video studio project.
 */

// --- Config Types ---

export type TtsEngine = "edge" | "qwen";
export type SubtitleStyle = "tiktok" | "bottom" | "center";
export type SubtitleDisplayMode = "sentence" | "full";
export type TransitionType = "fade" | "slide" | "wipe" | "none";

export type EdgeTtsConfig = {
  voice: string;
  rate: string;
  volume: string;
};

export type QwenTtsConfig = {
  conda_python: string;
  model: string;
  voice: string;
  lang_code: string;
  speed: number;
  temperature: number;
  tokens_per_char: number;
  min_max_tokens: number;
  max_max_tokens: number;
  short_text_threshold: number;
  sentence_gap_sec: number;
  silence_threshold: number;
  chars_per_second: number;
  hallucination_headroom: number;
};

export type TtsConfig = {
  engine: TtsEngine;
  speedRate: number;
  edge: EdgeTtsConfig;
  qwen: QwenTtsConfig;
};

export type VideoConfig = {
  width: number;
  height: number;
  fps: number;
  codec: string;
  crf: number;
  concurrency: number;
};

export type PathsConfig = {
  audioDir: string;
  buildDir: string;
  defaultContent: string;
};

export type SubtitleConfig = {
  enabled: boolean;
  style: SubtitleStyle;
  displayMode: SubtitleDisplayMode;
  fontSize: number;
  fontFamily: string;
  color: string;
  highlightColor: string;
  strokeColor: string;
  strokeWidth: number;
  combineTokensWithinMs: number;
  marginBottom: number;
  fadeDurationSec: number;
  backgroundColor: string;
  maxWidth: string;
  padding: string;
  borderRadius: number;
};

export type AnimationConfig = {
  transition: TransitionType;
  transitionDurationFrames: number;
  entranceSpring: { damping: number };
  paddingFrames: number;
  textEntryDelay: number;
};

export type ThemeConfig = {
  backgroundColor: string;
  primaryColor: string;
  secondaryColor: string;
  textColor: string;
  titleFontSize: number;
  bodyFontSize: number;
  fontFamily: string;
  slidePadding: number;
  bodyMaxWidth: number;
  decorLineWidth: number;
  backgroundImageOpacity: number;
};

export type BgmConfig = {
  enabled: boolean;
  file: string;
  volume: number;
  loop: boolean;
};

/** Maps speaker names to TTS voice IDs */
export type SpeakersConfig = Record<string, string>;

export type ProjectConfig = {
  video: VideoConfig;
  paths: PathsConfig;
  tts: TtsConfig;
  subtitle: SubtitleConfig;
  animation: AnimationConfig;
  theme: ThemeConfig;
  bgm?: BgmConfig;
  speakers?: SpeakersConfig;
};

// --- Content Types ---

/** Slide type: intro/outro get special treatment, content is the default */
export type SlideType = "intro" | "outro" | "content";

export type Slide = {
  id: string;
  title: string;
  text: string;
  speaker: string;
  notes?: string;
  /** Slide type: intro/outro/content (default: content) */
  type?: SlideType;
  /** Path to the audio file (populated after TTS generation) */
  audioFile?: string;
  /** Duration of the audio in seconds (populated after TTS generation) */
  audioDuration?: number;
};

export type SubtitlesContent = {
  title: string;
  slides: Slide[];
};

// --- Render Props ---

export type SlideRenderData = {
  id: string;
  title: string;
  text: string;
  audioFile: string;
  audioDurationInSeconds: number;
  durationInFrames: number;
  /** Slide type: intro/outro/content */
  type?: SlideType;
  /** Optional background image path */
  backgroundImage?: string;
};

export type MainVideoProps = {
  slides: SlideRenderData[];
  config: ProjectConfig;
};
