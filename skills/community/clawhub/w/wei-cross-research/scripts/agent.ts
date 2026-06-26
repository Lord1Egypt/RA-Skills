/**
 * Cross Research Agent
 *
 * Core implementation of the cross-research skill.
 * Queries multiple LLMs in parallel and synthesizes their responses into a single high-quality answer.
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
  /** Question domain — when 'financial', uses a finance-specific judge prompt */
  domain?: string;
}

/** Normalized model response */
export interface NormalizedResponse {
  model: ModelName;
  summary: string;
  keyPoints: string[];
  confidence: number;
  sourcesClaimed: string[];
  rawResponse?: string;
}

/** Failed model record */
export interface FailedModel {
  model: ModelName;
  reason: string;
}

/** Research response */
export interface ResearchResponse {
  query: string;
  modelsUsed: ModelName[];
  modelsFailed?: FailedModel[];
  answers: NormalizedResponse[];
  reportPath?: string;
  judgeRaw?: string;
  warning?: string;
  error?: string;
}

/** Router output */
interface RouterOutput {
  models: ModelName[];
  domain?: string | null;
}

/** Judge output */
interface JudgeOutput {
  raw: string;
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

/** Judge prompt template (general) */
const JUDGE_PROMPT_TEMPLATE = loadPrompt('judge');

/** Judge prompt template (financial) */
const JUDGE_FINANCIAL_PROMPT_TEMPLATE = loadPrompt('judge_financial');

/** Router prompt template */
const ROUTER_PROMPT_TEMPLATE = loadPrompt('router');

/**
 * Multi-Model Researcher Agent
 */
export class ResearchAgent {
  private bailianClient?: BailianClient;
  private openrouterClient?: OpenRouterClient;
  private openaiCompliantClient?: OpenAICompliantClient;
  private judgeModel: ModelName = appConfig.judge_model;

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
   * Execute research query
   */
  async research(request: ResearchRequest): Promise<ResearchResponse> {
    const startTime = Date.now();
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);

    try {
      console.log(`[ResearchAgent] ═══ Research started ═══`);
      console.log(`[ResearchAgent] Timestamp: ${timestamp}`);
      console.log(`[ResearchAgent] Result files will use this timestamp:`);
      console.log(`[ResearchAgent]   - reports/report-${timestamp}.txt`);
      console.log(`[ResearchAgent]   - intermediate/<model>-${timestamp}.txt`);

      // Step 1: Input sanitization
      const sanitizedQuery = this.sanitizeInput(request.query);
      console.log(`[ResearchAgent] Query sanitized in ${Date.now() - startTime}ms`);

      // Step 2: Router - select models and domain (or use provided models)
      let selectedModels: ModelName[];
      let domain: string | undefined = request.domain;
      if (request.models) {
        selectedModels = request.models;
      } else {
        const routerResult = await this.router(sanitizedQuery, request.maxModels ?? appConfig.max_models);
        selectedModels = routerResult.models;
        // Use router-provided domain only if caller didn't specify one
        if (!domain) domain = routerResult.domain;
      }
      console.log(`[ResearchAgent] Models selected: ${selectedModels.join(', ')}`);

      // Step 3: Parallel execution - query all models
      const modelResponses = await this.executeParallel(selectedModels, sanitizedQuery);
      console.log(`[ResearchAgent] Parallel execution completed in ${Date.now() - startTime}ms`);

      // Save each model's response to intermediate/
      this.saveModelResponses(modelResponses, selectedModels, timestamp);

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
          finalAnswer: '',
          confidence: 0,
          error: 'All models failed. Please retry.',
        };
      }

      // Step 4: Judge - synthesize responses
      const finalResult = await this.judge(sanitizedQuery, successfulResponses, timestamp, domain);
      console.log(`[ResearchAgent] Judge synthesis completed in ${Date.now() - startTime}ms`);

      // Build response
      const reportPath = this.saveReport(sanitizedQuery, finalResult.raw, successfulResponses, timestamp);

      const response: ResearchResponse = {
        query: sanitizedQuery,
        modelsUsed: successfulResponses.map(r => r.model),
        modelsFailed: failedModels.length > 0 ? failedModels : undefined,
        answers: successfulResponses,
        reportPath,
        judgeRaw: finalResult.raw,
      };

      if (failedModels.length > 0) {
        response.warning = 'Synthesis based on partial responses. Confidence may be reduced.';
      }

      console.log(`[ResearchAgent] Total execution time: ${Date.now() - startTime}ms`);
      return response;

    } catch (error) {
      console.error('[ResearchAgent] Research error:', error);
      return {
        query: request.query,
        modelsUsed: [],
        answers: [],
        finalAnswer: '',
        confidence: 0,
        error: error instanceof Error ? error.message : 'Unknown error occurred',
      };
    }
  }

  /**
   * Input sanitization - protect against prompt injection
   *
   * SECURITY NOTE: The patterns below (e.g., "ignore previous instructions") are
   * used for DEFENSIVE purposes to detect and neutralize potential prompt injection
   * attacks. These strings are matched against user input and redacted to prevent
   * manipulation of the LLM. This is a security feature, not a vulnerability.
   *
   * Pre-scan tools may flag these patterns as suspicious - this is a false positive.
   */
  private sanitizeInput(query: string): string {
    // Trim whitespace
    let sanitized = query.trim();

    // Enforce maximum length
    if (sanitized.length > MAX_QUERY_LENGTH) {
      sanitized = sanitized.substring(0, MAX_QUERY_LENGTH);
    }

    // Remove control characters
    sanitized = sanitized.replace(/[\x00-\x08\x0B-\x0C\x0E-\x1F\x7F]/g, '');

    // Remove potential prompt injection patterns
    const injectionPatterns = [
      /ignore previous instructions/gi,
      /system prompt/gi,
      /you are now/gi,
      /disregard/gi,
      /forget/gi,
      /<\|/g,
      /\|>/g,
    ];

    injectionPatterns.forEach(pattern => {
      sanitized = sanitized.replace(pattern, '[REDACTED]');
    });

    return sanitized;
  }

  /**
   * Router - select best models and domain for the query
   */
  private async router(query: string, maxModels: number = 2): Promise<{ models: ModelName[]; domain?: string }> {
    const routerPrompt = ROUTER_PROMPT_TEMPLATE
      .replace(/\{\{maxModels\}\}/g, String(maxModels))
      .replace('{{query}}', query);

    try {
      const messages: ChatMessage[] = [
        { role: 'user', content: routerPrompt },
      ];

      // Use judge model (glm-5) for routing
      const response = await this.callModel(this.judgeModel, messages);
      const content = response.choices[0]?.message?.content ?? '';

      // Parse JSON response
      const jsonMatch = content.match(/\{[\s\S]*\}/);
      if (jsonMatch) {
        const parsed: RouterOutput = JSON.parse(jsonMatch[0]);
        if (Array.isArray(parsed.models) && parsed.models.length > 0) {
          // Validate models
          const validModels = parsed.models
            .filter((m): m is ModelName => m in MODEL_REGISTRY);

          if (validModels.length > 0) {
            // Pad with default models if router returned fewer than maxModels
            const padded = [...validModels];
            for (const m of DEFAULT_MODELS) {
              if (padded.length >= maxModels) break;
              if (!padded.includes(m)) padded.push(m);
            }
            const domain = parsed.domain ?? undefined;
            return { models: padded.slice(0, maxModels), domain: domain || undefined };
          }
        }
      }

      // Fallback to default models
      console.log('[ResearchAgent] Router failed, using default models');
      return { models: DEFAULT_MODELS.slice(0, maxModels) };

    } catch (error) {
      console.error('[ResearchAgent] Router error:', error);
      return { models: DEFAULT_MODELS.slice(0, maxModels) };
    }
  }

  /**
   * Execute model calls in parallel
   */
  private async executeParallel(
    models: ModelName[],
    query: string
  ): Promise<(NormalizedResponse | null)[]> {
    const answerPrompt = `You are a research analyst.

Question:
${query}

Instructions:
1. Provide a clear, factual answer based on your knowledge.
2. List the most important insights as key points.
3. Explicitly note any uncertainties or limitations in your answer.
4. Do NOT fabricate citations or URLs. If you are not certain a source exists,
   omit it entirely.
5. Keep the response concise and focused.

Return your response in exactly this format:

Summary:
[Your answer here]

Key Points:
- [Point 1]
- [Point 2]
- [Point 3]

Sources (only if you are certain they exist):
- [Source 1, or omit this section entirely]

Confidence: [0.0–1.0]
Uncertainties: [Brief note on what you are unsure about, or "None"]`;

    const promises = models.map(model => {
      const config = MODEL_REGISTRY[model];
      const timeoutMs = (config?.timeout ?? 25) * 1000;
      return this.executeWithTimeout(model, answerPrompt, timeoutMs);
    });

    return Promise.all(promises);
  }

  /**
   * Execute a single model with timeout and retry
   */
  private async executeWithTimeout(
    model: ModelName,
    prompt: string,
    timeoutMs: number
  ): Promise<NormalizedResponse | null> {
    const messages: ChatMessage[] = [
      { role: 'user', content: prompt },
    ];

    // Try once, then retry once on failure
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
          console.error(`[ResearchAgent] Model ${model} failed after retry:`, error);
          return null;
        }
        console.warn(`[ResearchAgent] Model ${model} attempt ${attempt + 1} failed, retrying...`);
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
          temperature: 0.1,
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
   * Normalize model response to standard structure
   */
  private normalizeResponse(
    model: ModelName,
    response: ChatCompletionResponse
  ): NormalizedResponse {
    const message = response.choices[0]?.message;
    const content = message?.content ?? (message as any)?.reasoning ?? '';

    // Parse the structured response
    const summaryMatch = content.match(/Summary:\s*\n?([^\n]+(?:\n(?!(?:Key Points:|Sources:|Confidence:|Uncertainties:))[^\n]+)*)/i);
    const keyPointsMatch = content.match(/Key Points:\s*\n?((?:- [^\n]*\n?)+)/i);
    const confidenceMatch = content.match(/Confidence:\s*([0-9.]+)/i);
    const sourcesMatch = content.match(/Sources[^:]*:\s*\n?((?:- [^\n]*\n?)+)/i);
    const uncertaintiesMatch = content.match(/Uncertainties:\s*\n?([^\n]+)/i);

    const summary = summaryMatch ? summaryMatch[1].trim() : content;

    const keyPoints = keyPointsMatch
      ? keyPointsMatch[1]
          .split('\n')
          .map(line => line.replace(/^- /, '').trim())
          .filter(line => line.length > 0)
      : [];

    const confidence = confidenceMatch
      ? Math.min(1, Math.max(0, parseFloat(confidenceMatch[1])))
      : 0.5;

    const sourcesClaimed = sourcesMatch
      ? sourcesMatch[1]
          .split('\n')
          .map(line => line.replace(/^- /, '').trim())
          .filter(line => line.length > 0 && !line.toLowerCase().includes('omit'))
      : [];

    return {
      model,
      summary,
      keyPoints,
      confidence,
      sourcesClaimed,
      rawResponse: content,
    };
  }

  /**
   * Judge - synthesize multiple responses into final answer
   */
  private async judge(
    query: string,
    responses: NormalizedResponse[],
    timestamp: string,
    domain?: string
  ): Promise<JudgeOutput> {
    const modelResponsesText = responses.map(r => `
Model: ${r.model}
Summary: ${r.summary}
Key Points: ${r.keyPoints.join(', ')}
Confidence: ${r.confidence}
`).join('\n---\n');

    const template = domain === 'financial' ? JUDGE_FINANCIAL_PROMPT_TEMPLATE : JUDGE_PROMPT_TEMPLATE;
    const judgePrompt = template
      .replace('{{query}}', query)
      .replace('{{modelResponsesText}}', modelResponsesText)
      .replace('{{critiqueSection}}', '');

    const messages: ChatMessage[] = [
      { role: 'user', content: judgePrompt },
    ];

    const response = await this.callModel(this.judgeModel, messages, { maxTokens: appConfig.max_tokens_judge });
    if (!response.choices || response.choices.length === 0) {
      console.error('[ResearchAgent] Judge response missing choices:', JSON.stringify(response).substring(0, 500));
      throw new Error('Judge model returned invalid response (no choices)');
    }
    // Some models return content in 'reasoning' field when content is null
    const message = response.choices[0]?.message;
    const content = message?.content ?? (message as any)?.reasoning ?? '';

    // Save raw judge response
    this.saveIntermediate(`${this.judgeModel}-judge-raw`, content, timestamp);

    return { raw: content };
  }

  /**
   * Save each model's response to intermediate/<model>-<timestamp>.txt
   */
  private saveModelResponses(
    modelResponses: (NormalizedResponse | null)[],
    selectedModels: ModelName[],
    timestamp: string
  ): void {
    const __dirname = dirname(fileURLToPath(import.meta.url));
    const dir = join(__dirname, '..', 'intermediate');
    mkdirSync(dir, { recursive: true });

    modelResponses.forEach((response, index) => {
      if (response) {
        const filename = `${response.model}-${timestamp}.txt`;
        const filepath = join(dir, filename);
        const content = [
          `Model: ${response.model}`,
          `Timestamp: ${timestamp}`,
          `Query: [saved in report]`,
          ``,
          `=== Summary ===`,
          response.summary,
          ``,
          `=== Key Points ===`,
          ...response.keyPoints.map(p => `- ${p}`),
          ``,
          `=== Confidence ===`,
          `${response.confidence}`,
          ``,
          `=== Raw Response ===`,
          response.rawResponse || '',
        ].join('\n');
        writeFileSync(filepath, content, 'utf-8');
        console.log(`[ResearchAgent] Saved: intermediate/${filename}`);
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
    console.log(`[ResearchAgent] Saved: intermediate/${filename}`);
  }

  /**
   * Save judge result to reports/report-<timestamp>.txt
   */
  private saveReport(
    query: string,
    judgeRaw: string,
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
      judgeRaw,
    ].join('\n');

    writeFileSync(filepath, content, 'utf-8');
    console.log(`[ResearchAgent] Saved: reports/report-${timestamp}.txt`);
    return filepath;
  }

}

/**
 * Factory function to create a research agent
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
