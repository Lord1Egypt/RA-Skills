import type { ExecutionMode, OutputType, VideoToKnowledgeRequest } from "../schemas.js";
import { sha256 } from "../utils/hash.js";

export type ModeProfile = {
  mode: ExecutionMode;
  chunkSize: number;
  maxTopics: number;
  maxKeyPoints: number;
  qaPairs: number;
  flashcards: number;
  processingDepth: "shallow" | "standard" | "deep";
  modelLabels: {
    planning: string;
    transcription: string;
    semantic: string;
    knowledge: string;
    evaluation: string;
  };
};

export type ExecutionPlan = {
  requestHash: string;
  modeProfile: ModeProfile;
  requestedOutputs: OutputType[];
  transcriptionFingerprint: string;
  chunkConfigHash: string;
};

const MODE_PROFILES: Record<ExecutionMode, ModeProfile> = {
  fast: {
    mode: "fast",
    chunkSize: 1800,
    maxTopics: 4,
    maxKeyPoints: 5,
    qaPairs: 4,
    flashcards: 4,
    processingDepth: "shallow",
    modelLabels: {
      planning: "planner-fast:v1",
      transcription: "transcriber-fast:v1",
      semantic: "semantic-fast:v1",
      knowledge: "knowledge-fast:v1",
      evaluation: "evaluation-fast:v1",
    },
  },
  balanced: {
    mode: "balanced",
    chunkSize: 1200,
    maxTopics: 6,
    maxKeyPoints: 7,
    qaPairs: 6,
    flashcards: 6,
    processingDepth: "standard",
    modelLabels: {
      planning: "planner-balanced:v1",
      transcription: "transcriber-balanced:v1",
      semantic: "semantic-balanced:v1",
      knowledge: "knowledge-balanced:v1",
      evaluation: "evaluation-balanced:v1",
    },
  },
  high_accuracy: {
    mode: "high_accuracy",
    chunkSize: 800,
    maxTopics: 8,
    maxKeyPoints: 10,
    qaPairs: 8,
    flashcards: 10,
    processingDepth: "deep",
    modelLabels: {
      planning: "planner-high-accuracy:v1",
      transcription: "transcriber-high-accuracy:v1",
      semantic: "semantic-high-accuracy:v1",
      knowledge: "knowledge-high-accuracy:v1",
      evaluation: "evaluation-high-accuracy:v1",
    },
  },
};

export class PlannerAgent {
  plan(request: VideoToKnowledgeRequest): ExecutionPlan {
    const requestedOutputs = [...new Set(request.outputs)] as OutputType[];
    const modeProfile = MODE_PROFILES[request.mode];
    return {
      requestHash: sha256(JSON.stringify({ media_url: request.media_url, outputs: requestedOutputs, mode: request.mode })),
      modeProfile,
      requestedOutputs,
      transcriptionFingerprint: sha256(JSON.stringify({ media_url: request.media_url, mode: request.mode, transcription: modeProfile.modelLabels.transcription })),
      chunkConfigHash: sha256(JSON.stringify({ chunkSize: modeProfile.chunkSize, semantic: modeProfile.modelLabels.semantic, processingDepth: modeProfile.processingDepth })),
    };
  }

  getModeProfiles(): Record<ExecutionMode, ModeProfile> {
    return MODE_PROFILES;
  }
}
