/**
 * Devil's Advocate Agent
 *
 * Core implementation of the devil's advocate skill.
 * Challenges ideas by generating strong counterarguments from multiple LLMs.
 */

import { readFileSync, mkdirSync, writeFileSync } from 'fs';
import { dirname, join } from 'path';
import { fileURLToPath } from 'url';
import { BailianClient, OpenRouterClient, OpenAICompliantClient } from './clients/index.js';
import type { ChatMessage, ChatCompletionResponse } from './clients/bailian.js';

/** Configuration file structure */
interface ConfigFile {
  judge_model: string;
  max_models: number;
  max_tokens: number;
  max_tokens_judge: number;
  depth: string;
  models: Record<string, {
    provider: string;
    model_id: string;
    api_base: string;
    api_key_env: string;
    timeout: number;
  }>;
}

/** Load configuration from config.json */
function loadConfig(): ConfigFile {
  const __dirname = dirname(fileURLToPath(import.meta.url));
  const configPath = join(__dirname, '..', 'config.json');
  const raw = readFileSync(configPath, 'utf-8');
  return JSON.parse(raw);
}

/** Load a prompt template from the prompts directory */
function loadPrompt(name: string): string {
  const __dirname = dirname(fileURLToPath(import.meta.url));
  const promptPath = join(__dirname, '..', 'prompts', `${name}.txt`);
  return readFileSync(promptPath, 'utf-8');
}

/** Build model registry from config */
function buildModelRegistry(config: ConfigFile): Record<string, ModelConfig> {
  const registry: Record<string, ModelConfig> = {};
  for (const [name, model] of Object.entries(config.models)) {
    registry[name] = {
      name,
      provider: model.provider as ModelConfig['provider'],
      modelId: model.model_id,
      apiBase: model.api_base,
      apiKeyEnv: model.api_key_env,
      timeout: model.timeout,
    };
  }
  return registry;
}

/** Supported model names */
export type ModelName = string;

/** Research request parameters */
export interface ResearchRequest {
  query: string;
  models?: ModelName[];
  maxModels?: number;
  depth?: 'simple' | 'tree';
  domain?: string;
}

/** Normalized model response - counterargument structure */
export interface NormalizedResponse {
  model: ModelName;
  keyAssumptions: string[];
  counterarguments: string[];
  failureScenarios: string[];
  whatWouldProveWrong: string[];
  rawResponse: string;
}

/** Failed model record */
export interface FailedModel {
  model: ModelName;
  reason: string;
}

/** Judge evaluation output */
export interface JudgeEvaluation {
  restatedThesis: string;
  criticalRisks: string[];
  survivability: string;
  verdict: 'fatal' | 'risky' | 'robust';
  confidence: number;
  recommendation: 'kill' | 'pivot' | 'proceed';
  nextSteps: string;
  raw: string;
}

/** Research response */
export interface ResearchResponse {
  query: string;
  modelsUsed: ModelName[];
  modelsFailed?: FailedModel[];
  answers: NormalizedResponse[];
  evaluation?: JudgeEvaluation;
  reportPath?: string;
  judgeRaw?: string;
  warning?: string;
  error?: string;
  finalAnswer?: string;
}

/** Model configuration */
interface ModelConfig {
  name: string;
  provider: 'openrouter' | 'bailian' | 'openai_compliant';
  modelId: string;
  apiBase: string;
  apiKeyEnv: string;
  timeout: number;
}

/** Load application config and build registry */
const appConfig = loadConfig();
const MODEL_REGISTRY = buildModelRegistry(appConfig);
const DEFAULT_MODELS: string[] = Object.keys(appConfig.models).slice(0, appConfig.max_models);

/** Maximum query length */
const MAX_QUERY_LENGTH = 4000;

/** Debater system prompt */
const DEBATER_PROMPT = loadPrompt('debater');

/** Judge prompt template */
const JUDGE_PROMPT_TEMPLATE = loadPrompt('judge');

/**
 * Devil's Advocate Agent
 */
export class ResearchAgent {
  private bailianClient?: BailianClient;
  private openrouterClient?: OpenRouterClient;
  private openaiCompliantClient?: OpenAICompliantClient;
  private judgeModel: ModelName = appConfig.judge_model || 'glm-5-judge';

  constructor(options?: {
    bailianClient?: BailianClient;
    openrouterClient?: OpenRouterClient;
    openaiCompliantClient?: OpenAICompliantClient;
    judgeModel?: ModelName;
  }) {
    this.bailianClient = options?.bailianClient;
    this.openrouterClient = options?.openrouterClient;
    this.openaiCompliantClient = options?.openaiCompliantClient;
    if (options?.judgeModel) {
      this.judgeModel = options.judgeModel;
    }
  }

  /**
   * Execute attack mode - generate counterarguments and evaluate
   */
  async research(request: ResearchRequest): Promise<ResearchResponse> {
    const startTime = Date.now();
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);

    try {
      console.log(`[DevilsAdvocate] ═══ Attack mode started ═══`);
      console.log(`[DevilsAdvocate] Timestamp: ${timestamp}`);
      console.log(`[DevilsAdvocate] Result files will use this timestamp:`);
      console.log(`[DevilsAdvocate]   - reports/report-${timestamp}.txt`);
      console.log(`[DevilsAdvocate]   - intermediate/<model>-${timestamp}.txt`);

      // Step 1: Input sanitization
      const sanitizedQuery = this.sanitizeInput(request.query);
      console.log(`[DevilsAdvocate] Query sanitized in ${Date.now() - startTime}ms`);

      // Step 2: Select models
      const selectedModels = request.models || this.selectModels(request.maxModels ?? appConfig.max_models);
      console.log(`[DevilsAdvocate] Models selected: ${selectedModels.join(', ')}`);

      // Step 3: Parallel execution - get counterarguments from all models
      const modelResponses = await this.executeParallel(selectedModels, sanitizedQuery);
      console.log(`[DevilsAdvocate] Parallel execution completed in ${Date.now() - startTime}ms`);

      // Save each model's response to intermediate/
      this.saveModelResponses(modelResponses, timestamp, sanitizedQuery);

      // Check if all models failed
      const successfulResponses = modelResponses.filter(r => r !== null) as NormalizedResponse[];
      const failedModels: FailedModel[] = [];

      modelResponses.forEach((response, index) => {
        if (response === null) {
          failedModels.push({
            model: selectedModels[index],
            reason: 'timeout_or_error',
          });
        }
      });

      if (successfulResponses.length === 0) {
        return {
          query: sanitizedQuery,
          modelsUsed: [],
          modelsFailed: failedModels,
          answers: [],
          error: 'All models failed. Please retry.',
        };
      }

      // Step 4: Judge - evaluate survivability
      const evaluation = await this.judge(sanitizedQuery, successfulResponses, timestamp);
      console.log(`[DevilsAdvocate] Judge evaluation completed in ${Date.now() - startTime}ms`);

      // Build response
      const reportPath = this.saveReport(sanitizedQuery, evaluation, successfulResponses, timestamp);

      const response: ResearchResponse = {
        query: sanitizedQuery,
        modelsUsed: successfulResponses.map(r => r.model),
        modelsFailed: failedModels.length > 0 ? failedModels : undefined,
        answers: successfulResponses,
        evaluation,
        reportPath,
        judgeRaw: evaluation.raw,
        finalAnswer: this.formatFinalAnswer(evaluation),
      };

      if (failedModels.length > 0) {
        response.warning = 'Evaluation based on partial responses. Confidence may be reduced.';
      }

      console.log(`[DevilsAdvocate] Total execution time: ${Date.now() - startTime}ms`);
      return response;

    } catch (error) {
      console.error('[DevilsAdvocate] Attack error:', error);
      return {
        query: request.query,
        modelsUsed: [],
        answers: [],
        error: error instanceof Error ? error.message : 'Unknown error occurred',
      };
    }
  }

  /**
   * Format final answer from evaluation
   */
  private formatFinalAnswer(evaluation: JudgeEvaluation): string {
    return [
      `Verdict: ${evaluation.verdict.toUpperCase()}`,
      `Recommendation: ${evaluation.recommendation.toUpperCase()}`,
      `Confidence: ${(evaluation.confidence * 100).toFixed(1)}%`,
      ``,
      `Critical Risks:`,
      ...evaluation.criticalRisks.map(r => `- ${r}`),
      ``,
      `Next Steps: ${evaluation.nextSteps}`,
    ].join('\n');
  }

  /**
   * Select models
   */
  private selectModels(maxModels: number = appConfig.max_models): ModelName[] {
    return DEFAULT_MODELS.slice(0, maxModels);
  }

  /**
   * Input sanitization - protect against prompt injection
   */
  private sanitizeInput(query: string): string {
    let sanitized = query.trim();

    if (sanitized.length > MAX_QUERY_LENGTH) {
      sanitized = sanitized.substring(0, MAX_QUERY_LENGTH);
    }

    sanitized = sanitized.replace(/[\x00-\x08\x0B-\x0C\x0E-\x1F\x7F]/g, '');

    const injectionPatterns = [
      /ignore previous instructions/gi,
      /system prompt/gi,
      /you are now/gi,
      /disregard/gi,
      /forget/gi,
      /</g,
      />/g,
    ];

    injectionPatterns.forEach(pattern => {
      sanitized = sanitized.replace(pattern, '[REDACTED]');
    });

    return sanitized;
  }

  /**
   * Execute model calls in parallel to generate counterarguments
   */
  private async executeParallel(
    models: ModelName[],
    query: string
  ): Promise<(NormalizedResponse | null)[]> {
    const promises = models.map(model => {
      const config = MODEL_REGISTRY[model];
      const timeoutMs = (config?.timeout ?? 60) * 1000;
      return this.executeWithTimeout(model, query, timeoutMs);
    });

    return Promise.all(promises);
  }

  /**
   * Execute a single model with timeout and retry
   */
  private async executeWithTimeout(
    model: ModelName,
    query: string,
    timeoutMs: number
  ): Promise<NormalizedResponse | null> {
    const messages: ChatMessage[] = [
      { role: 'system', content: DEBATER_PROMPT },
      { role: 'user', content: `Thesis to challenge:\n\n${query}` },
    ];

    for (let attempt = 0; attempt < 2; attempt++) {
      try {
        const response = await Promise.race([
          this.callModel(model, messages),
          new Promise<never>((_, reject) =>
            setTimeout(() => reject(new Error('Timeout')), timeoutMs)
          ),
        ]);

        return this.normalizeResponse(model, response);

      } catch (error) {
        const isLastAttempt = attempt === 1;
        if (isLastAttempt) {
          console.error(`[DevilsAdvocate] Model ${model} failed after retry:`, error);
          return null;
        }
        console.warn(`[DevilsAdvocate] Model ${model} attempt ${attempt + 1} failed, retrying...`);
      }
    }

    return null;
  }

  /**
   * Get or create Bailian client (lazy initialization)
   */
  private getBailianClient(): BailianClient {
    if (!this.bailianClient) {
      this.bailianClient = new BailianClient();
    }
    return this.bailianClient;
  }

  /**
   * Get or create OpenRouter client (lazy initialization)
   */
  private getOpenRouterClient(): OpenRouterClient {
    if (!this.openrouterClient) {
      this.openrouterClient = new OpenRouterClient();
    }
    return this.openrouterClient;
  }

  /**
   * Call a model through its configured provider
   */
  private async callModel(
    model: ModelName,
    messages: ChatMessage[],
    options?: { maxTokens?: number }
  ): Promise<ChatCompletionResponse> {
    const config = MODEL_REGISTRY[model];
    const maxTokens = options?.maxTokens ?? appConfig.max_tokens;

    switch (config.provider) {
      case 'bailian':
        return this.getBailianClient().chatCompletion(config.modelId, messages, {
          temperature: 0.7,
          maxTokens,
        });
      case 'openrouter':
        return this.getOpenRouterClient().chatCompletion(config.modelId, messages, {
          temperature: 0.7,
          maxTokens,
        });
      case 'openai_compliant':
      default:
        if (!this.openaiCompliantClient) {
          throw new Error(`Model ${model} requires openaiCompliantClient, but it is not configured`);
        }
        return this.openaiCompliantClient.chatCompletion(config.modelId, messages, {
          temperature: 0.7,
          maxTokens,
        });
    }
  }

  /**
   * Normalize model response to counterargument structure
   */
  private normalizeResponse(
    model: ModelName,
    response: ChatCompletionResponse
  ): NormalizedResponse {
    const message = response.choices[0]?.message;
    const content = message?.content ?? (message as any)?.reasoning ?? '';

    // Parse the structured response - looking for exact format sections
    const keyAssumptionsMatch = content.match(/Key Assumptions:\s*\n((?:- [^\n]*\n)+)/i);
    const counterargumentsMatch = content.match(/Strong Counterarguments:\s*\n((?:- [^\n]*\n)+)/i);
    const failureScenariosMatch = content.match(/Failure Scenarios:\s*\n((?:- [^\n]*\n)+)/i);
    const proveWrongMatch = content.match(/What Would Prove You Wrong:\s*\n((?:- [^\n]*\n)+)/i);

    const parseList = (match: RegExpMatchArray | null): string[] => {
      if (!match) return [];
      return match[1]
        .split('\n')
        .map(line => line.replace(/^- /, '').trim())
        .filter(line => line.length > 0);
    };

    return {
      model,
      keyAssumptions: parseList(keyAssumptionsMatch),
      counterarguments: parseList(counterargumentsMatch),
      failureScenarios: parseList(failureScenariosMatch),
      whatWouldProveWrong: parseList(proveWrongMatch),
      rawResponse: content,
    };
  }

  /**
   * Judge - evaluate whether the idea survives adversarial scrutiny
   */
  private async judge(
    query: string,
    responses: NormalizedResponse[],
    timestamp: string
  ): Promise<JudgeEvaluation> {
    const counterargumentsText = responses.map(r => `
Model: ${r.model}
Key Assumptions: ${r.keyAssumptions.join(', ')}
Counterarguments: ${r.counterarguments.join(', ')}
Failure Scenarios: ${r.failureScenarios.join(', ')}
`).join('\n---\n');

    const judgePrompt = `Thesis to evaluate:
${query}

Counterarguments from multiple models:
${counterargumentsText}

${JUDGE_PROMPT_TEMPLATE}`;

    const messages: ChatMessage[] = [
      { role: 'user', content: judgePrompt },
    ];

    const response = await this.callModel(this.judgeModel, messages, { maxTokens: appConfig.max_tokens_judge });
    if (!response.choices || response.choices.length === 0) {
      console.error('[DevilsAdvocate] Judge response missing choices:', JSON.stringify(response).substring(0, 500));
      throw new Error('Judge model returned invalid response (no choices)');
    }

    const message = response.choices[0]?.message;
    const content = message?.content ?? (message as any)?.reasoning ?? '';

    // Save raw judge response
    this.saveIntermediate(`${this.judgeModel}-judge-raw`, content, timestamp);

    // Parse judge output
    return this.parseJudgeOutput(content);
  }

  /**
   * Parse judge output into structured evaluation
   */
  private parseJudgeOutput(content: string): JudgeEvaluation {
    const restatedMatch = content.match(/Restated Thesis:?\s*\n?([^\n]+(?:\n(?!(?:Critical Risks?:|Survivability:|Verdict:|Confidence:|Recommendation:|Next Steps?:))[^\n]+)*)/i);
    const risksMatch = content.match(/Critical Risks?:?\s*\n?((?:- [^\n]*\n?)+)/i);
    const survivabilityMatch = content.match(/Survivability:?\s*\n?([^\n]+)/i);
    const verdictMatch = content.match(/Verdict:?\s*\n?(fatal|risky|robust)/i);
    const confidenceMatch = content.match(/Confidence:?\s*\n?([0-9.]+)/i);
    const recommendationMatch = content.match(/Recommendation:?\s*\n?(kill|pivot|proceed)/i);
    const nextStepsMatch = content.match(/Next Steps?:?\s*\n?([^\n]+(?:\n(?!(?:\d+\. |$))[^\n]+)*)/i);

    const parseList = (match: RegExpMatchArray | null): string[] => {
      if (!match) return [];
      return match[1]
        .split('\n')
        .map(line => line.replace(/^- /, '').trim())
        .filter(line => line.length > 0);
    };

    return {
      restatedThesis: restatedMatch ? restatedMatch[1].trim() : '',
      criticalRisks: parseList(risksMatch),
      survivability: survivabilityMatch ? survivabilityMatch[1].trim() : '',
      verdict: verdictMatch ? (verdictMatch[1].toLowerCase() as 'fatal' | 'risky' | 'robust') : 'risky',
      confidence: confidenceMatch ? Math.min(1, Math.max(0, parseFloat(confidenceMatch[1]))) : 0.5,
      recommendation: recommendationMatch ? (recommendationMatch[1].toLowerCase() as 'kill' | 'pivot' | 'proceed') : 'pivot',
      nextSteps: nextStepsMatch ? nextStepsMatch[1].trim() : '',
      raw: content,
    };
  }

  /**
   * Save each model's response to intermediate/<model>-<timestamp>.txt
   */
  private saveModelResponses(
    modelResponses: (NormalizedResponse | null)[],
    timestamp: string,
    query: string
  ): void {
    const __dirname = dirname(fileURLToPath(import.meta.url));
    const dir = join(__dirname, '..', 'intermediate');
    mkdirSync(dir, { recursive: true });

    modelResponses.forEach((response) => {
      if (response) {
        const filename = `${response.model}-${timestamp}.txt`;
        const filepath = join(dir, filename);
        const content = [
          `Model: ${response.model}`,
          `Timestamp: ${timestamp}`,
          `Query: ${query}`,
          ``,
          `=== Key Assumptions ===`,
          ...response.keyAssumptions.map(p => `- ${p}`),
          ``,
          `=== Counterarguments ===`,
          ...response.counterarguments.map(p => `- ${p}`),
          ``,
          `=== Failure Scenarios ===`,
          ...response.failureScenarios.map(p => `- ${p}`),
          ``,
          `=== What Would Prove You Wrong ===`,
          ...response.whatWouldProveWrong.map(p => `- ${p}`),
          ``,
          `=== Raw Response ===`,
          response.rawResponse,
        ].join('\n');
        writeFileSync(filepath, content, 'utf-8');
        console.log(`[DevilsAdvocate] Saved: intermediate/${filename}`);
      }
    });
  }

  /**
   * Save content to intermediate/<name>-<timestamp>.txt
   */
  private saveIntermediate(name: string, content: string, timestamp: string): void {
    const __dirname = dirname(fileURLToPath(import.meta.url));
    const dir = join(__dirname, '..', 'intermediate');
    mkdirSync(dir, { recursive: true });

    const filename = `${name}-${timestamp}.txt`;
    const filepath = join(dir, filename);
    writeFileSync(filepath, content, 'utf-8');
    console.log(`[DevilsAdvocate] Saved: intermediate/${filename}`);
  }

  /**
   * Save judge result to reports/report-<timestamp>.txt
   */
  private saveReport(
    query: string,
    evaluation: JudgeEvaluation,
    responses: NormalizedResponse[],
    timestamp: string
  ): string {
    const __dirname = dirname(fileURLToPath(import.meta.url));
    const dir = join(__dirname, '..', 'reports');
    mkdirSync(dir, { recursive: true });

    const filepath = join(dir, `report-${timestamp}.txt`);
    const content = [
      `Query: ${query}`,
      `Timestamp: ${timestamp}`,
      `Models: ${responses.map(r => r.model).join(', ')}`,
      ``,
      `═══════════════════════════════════════`,
      `           JUDGE EVALUATION`,
      `═══════════════════════════════════════`,
      ``,
      `Restated Thesis:`,
      evaluation.restatedThesis,
      ``,
      `Critical Risks:`,
      ...evaluation.criticalRisks.map(r => `- ${r}`),
      ``,
      `Survivability: ${evaluation.survivability}`,
      ``,
      `Verdict: ${evaluation.verdict.toUpperCase()}`,
      `Confidence: ${(evaluation.confidence * 100).toFixed(1)}%`,
      ``,
      `Recommendation: ${evaluation.recommendation.toUpperCase()}`,
      ``,
      `Next Steps:`,
      evaluation.nextSteps,
      ``,
      `═══════════════════════════════════════`,
      `         COUNTERARGUMENTS`,
      `═══════════════════════════════════════`,
      ``,
      ...responses.flatMap(r => [
        `--- ${r.model} ---`,
        `Key Assumptions:`,
        ...r.keyAssumptions.map(a => `- ${a}`),
        ``,
        `Counterarguments:`,
        ...r.counterarguments.map(c => `- ${c}`),
        ``,
        `Failure Scenarios:`,
        ...r.failureScenarios.map(f => `- ${f}`),
        ``,
      ]),
      `═══════════════════════════════════════`,
      `              RAW OUTPUT`,
      `═══════════════════════════════════════`,
      ``,
      evaluation.raw,
    ].join('\n');

    writeFileSync(filepath, content, 'utf-8');
    console.log(`[DevilsAdvocate] Saved: reports/report-${timestamp}.txt`);
    return filepath;
  }
}

/**
 * Factory function to create a devil's advocate agent
 */
export function createResearchAgent(options?: {
  bailianClient?: BailianClient;
  openrouterClient?: OpenRouterClient;
  judgeModel?: ModelName;
}): ResearchAgent {
  return new ResearchAgent(options);
}

// Export default
export default ResearchAgent;
