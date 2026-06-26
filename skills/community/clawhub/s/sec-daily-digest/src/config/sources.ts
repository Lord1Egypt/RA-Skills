import { mkdir, readFile, writeFile } from "node:fs/promises";
import path from "node:path";
import { parse, stringify } from "yaml";
import { getStateRoot } from "./paths";

export interface RssSource {
  id: string;
  type: "rss";
  name: string;
  url: string;
  enabled: boolean;
  priority: boolean;
  topics: string[];
  note?: string;
}

export interface TwitterSourceConfig {
  id: string;
  type: "twitter";
  name: string;
  handle: string;
  enabled: boolean;
  priority: boolean;
  topics: string[];
  note?: string;
}

export type SourceConfig = RssSource | TwitterSourceConfig;

export interface SourcesConfig {
  sources: SourceConfig[];
}

export const DEFAULT_SECURITY_TWITTER_SOURCES: TwitterSourceConfig[] = [
  { id: "taviso", type: "twitter", name: "Tavis Ormandy / Google Project Zero", handle: "taviso", enabled: true, priority: true, topics: ["security"] },
  { id: "thegrugq", type: "twitter", name: "The Grugq", handle: "thegrugq", enabled: true, priority: false, topics: ["security"] },
  { id: "SwiftOnSecurity", type: "twitter", name: "SwiftOnSecurity", handle: "SwiftOnSecurity", enabled: true, priority: true, topics: ["security"] },
  { id: "GossiTheDog", type: "twitter", name: "Kevin Beaumont", handle: "GossiTheDog", enabled: true, priority: true, topics: ["security"] },
  { id: "MalwareTechBlog", type: "twitter", name: "Marcus Hutchins", handle: "MalwareTechBlog", enabled: true, priority: true, topics: ["security"] },
  { id: "briankrebs", type: "twitter", name: "Brian Krebs", handle: "briankrebs", enabled: true, priority: true, topics: ["security"] },
  { id: "evacide", type: "twitter", name: "Eva Galperin / EFF", handle: "evacide", enabled: true, priority: false, topics: ["security"] },
  { id: "jduck", type: "twitter", name: "Joshua J. Drake", handle: "jduck", enabled: true, priority: false, topics: ["security"] },
  { id: "ncweaver", type: "twitter", name: "Nicholas Weaver", handle: "ncweaver", enabled: true, priority: false, topics: ["security"] },
  { id: "JohnLaTwC", type: "twitter", name: "John Lambert, Microsoft TI", handle: "JohnLaTwC", enabled: true, priority: true, topics: ["security"] },
  { id: "billdemirkapi", type: "twitter", name: "Bill Demirkapi", handle: "billdemirkapi", enabled: true, priority: false, topics: ["security"] },
  { id: "hackerfantastic", type: "twitter", name: "hackerfantastic", handle: "hackerfantastic", enabled: true, priority: false, topics: ["security"] },
  { id: "_wald0", type: "twitter", name: "Andy Robbins, BloodHound", handle: "_wald0", enabled: true, priority: false, topics: ["security"] },
  { id: "aionescu", type: "twitter", name: "Alex Ionescu", handle: "aionescu", enabled: true, priority: false, topics: ["security"] },
  { id: "tiraniddo", type: "twitter", name: "James Forshaw", handle: "tiraniddo", enabled: true, priority: false, topics: ["security"] },
];

// AI / frontier-tech KOLs (sourced from tech-news-digest defaults)
export const DEFAULT_TECH_TWITTER_SOURCES: TwitterSourceConfig[] = [
  // AI Labs & CEOs
  { id: "sama-twitter", type: "twitter", name: "Sam Altman (OpenAI CEO)", handle: "sama", enabled: true, priority: true, topics: ["llm", "ai-agent", "frontier-tech"], note: "OpenAI CEO" },
  { id: "openai-twitter", type: "twitter", name: "OpenAI official", handle: "OpenAI", enabled: true, priority: true, topics: ["llm", "ai-agent", "frontier-tech"], note: "OpenAI official" },
  { id: "anthropic-twitter", type: "twitter", name: "Anthropic official", handle: "AnthropicAI", enabled: true, priority: true, topics: ["llm", "ai-agent", "frontier-tech"], note: "Anthropic official" },
  { id: "dario-twitter", type: "twitter", name: "Dario Amodei (Anthropic CEO)", handle: "DarioAmodei", enabled: true, priority: true, topics: ["llm", "ai-agent"], note: "Anthropic CEO" },
  { id: "demis-twitter", type: "twitter", name: "Demis Hassabis (DeepMind CEO)", handle: "demishassabis", enabled: true, priority: true, topics: ["llm", "frontier-tech"], note: "DeepMind CEO, Nobel laureate" },
  { id: "deepmind-twitter", type: "twitter", name: "Google DeepMind official", handle: "GoogleDeepMind", enabled: true, priority: true, topics: ["llm", "frontier-tech"], note: "Google DeepMind official" },
  { id: "googleai-twitter", type: "twitter", name: "Google AI official", handle: "GoogleAI", enabled: true, priority: true, topics: ["llm", "ai-agent", "frontier-tech"], note: "Google AI official" },
  { id: "xai-twitter", type: "twitter", name: "xAI official", handle: "xai", enabled: true, priority: true, topics: ["llm", "ai-agent", "frontier-tech"], note: "xAI official" },
  { id: "mistral-twitter", type: "twitter", name: "Mistral AI official", handle: "MistralAI", enabled: true, priority: true, topics: ["llm", "frontier-tech"], note: "Mistral AI official" },
  // AI Researchers & Educators
  { id: "ylecun-twitter", type: "twitter", name: "Yann LeCun (Meta AI)", handle: "ylecun", enabled: true, priority: true, topics: ["llm", "frontier-tech"], note: "Meta AI" },
  { id: "karpathy-twitter", type: "twitter", name: "Andrej Karpathy", handle: "karpathy", enabled: true, priority: true, topics: ["llm", "ai-agent", "frontier-tech"], note: "AI researcher" },
  { id: "andrewng-twitter", type: "twitter", name: "Andrew Ng", handle: "AndrewYNg", enabled: true, priority: true, topics: ["llm", "ai-agent"], note: "AI educator" },
  { id: "jimfan-twitter", type: "twitter", name: "Jim Fan (NVIDIA)", handle: "DrJimFan", enabled: true, priority: true, topics: ["ai-agent", "frontier-tech"], note: "NVIDIA AI" },
  { id: "yudkowsky-twitter", type: "twitter", name: "Eliezer Yudkowsky", handle: "ESYudkowsky", enabled: true, priority: false, topics: ["llm", "frontier-tech"], note: "AI safety pioneer" },
  { id: "rowancheung-twitter", type: "twitter", name: "Rowan Cheung (The Rundown AI)", handle: "rowancheung", enabled: true, priority: true, topics: ["llm", "ai-agent"], note: "AI newsletter founder" },
  { id: "swyx-twitter", type: "twitter", name: "Swyx", handle: "swyx", enabled: true, priority: false, topics: ["llm", "ai-agent"], note: "AI Engineer community, Latent Space podcast" },
  { id: "sebastian-twitter", type: "twitter", name: "Sebastian Raschka", handle: "rasbt", enabled: true, priority: false, topics: ["llm", "frontier-tech"], note: "AI researcher" },
  { id: "emad-twitter", type: "twitter", name: "Emad Mostaque", handle: "EMostaque", enabled: true, priority: false, topics: ["llm", "frontier-tech"], note: "Stability AI" },
  { id: "erikbryn-twitter", type: "twitter", name: "Erik Brynjolfsson", handle: "erikbryn", enabled: true, priority: false, topics: ["frontier-tech"], note: "Stanford Digital Economy Lab" },
  // AI Tooling & Ecosystem
  { id: "hf-twitter", type: "twitter", name: "Hugging Face official", handle: "huggingface", enabled: true, priority: true, topics: ["llm", "ai-agent"], note: "Hugging Face official" },
  { id: "langchain-twitter", type: "twitter", name: "LangChain official", handle: "LangChain", enabled: true, priority: false, topics: ["ai-agent"], note: "LangChain official" },
  { id: "hwchase-twitter", type: "twitter", name: "Harrison Chase (LangChain)", handle: "hwchase17", enabled: true, priority: true, topics: ["ai-agent"], note: "LangChain founder" },
  { id: "llamaindex-twitter", type: "twitter", name: "LlamaIndex official", handle: "llama_index", enabled: true, priority: false, topics: ["ai-agent"], note: "LlamaIndex official" },
  // General Tech Leaders
  { id: "satya-twitter", type: "twitter", name: "Satya Nadella", handle: "satyanadella", enabled: true, priority: false, topics: ["frontier-tech"], note: "Microsoft CEO" },
  { id: "sundar-twitter", type: "twitter", name: "Sundar Pichai", handle: "sundarpichai", enabled: true, priority: false, topics: ["frontier-tech"], note: "Google CEO" },
  { id: "elon-twitter", type: "twitter", name: "Elon Musk", handle: "elonmusk", enabled: true, priority: false, topics: ["frontier-tech"], note: "Entrepreneur" },
  { id: "pmarca-twitter", type: "twitter", name: "Marc Andreessen", handle: "pmarca", enabled: true, priority: false, topics: ["frontier-tech", "crypto"], note: "a16z" },
  { id: "levie-twitter", type: "twitter", name: "Aaron Levie", handle: "levie", enabled: true, priority: false, topics: ["frontier-tech"], note: "Box CEO" },
];

const DEFAULT_TWITTER_SOURCES: TwitterSourceConfig[] = [
  ...DEFAULT_SECURITY_TWITTER_SOURCES,
  ...DEFAULT_TECH_TWITTER_SOURCES,
];

const DEFAULT_SOURCES_CONFIG: SourcesConfig = {
  sources: DEFAULT_TWITTER_SOURCES,
};

function mergeWithDefaults(userSources: SourceConfig[], defaults: SourceConfig[]): SourceConfig[] {
  const merged = new Map<string, SourceConfig>();

  // Start with defaults
  for (const src of defaults) {
    merged.set(src.id, src);
  }

  // Apply user overrides
  for (const userSrc of userSources) {
    const existing = merged.get(userSrc.id);
    if (existing) {
      // Full replacement if user provided all required fields; otherwise just toggle enabled
      const hasType = "type" in userSrc && userSrc.type;
      if (hasType) {
        merged.set(userSrc.id, userSrc);
      } else {
        merged.set(userSrc.id, { ...existing, enabled: (userSrc as { enabled?: boolean }).enabled ?? existing.enabled });
      }
    } else {
      // New source: append
      merged.set(userSrc.id, userSrc);
    }
  }

  return [...merged.values()];
}

export async function loadSourcesConfig(env: NodeJS.ProcessEnv): Promise<SourcesConfig> {
  const root = getStateRoot(env);
  await mkdir(root, { recursive: true });

  const filePath = path.join(root, "sources.yaml");

  try {
    const content = await readFile(filePath, "utf8");
    const parsed = parse(content) as { sources?: SourceConfig[] } | null;
    if (!parsed || !Array.isArray(parsed.sources)) {
      return DEFAULT_SOURCES_CONFIG;
    }

    const merged = mergeWithDefaults(parsed.sources, DEFAULT_TWITTER_SOURCES);
    return { sources: merged };
  } catch {
    // First run: write defaults
    await writeFile(filePath, stringify(DEFAULT_SOURCES_CONFIG), "utf8");
    return DEFAULT_SOURCES_CONFIG;
  }
}

export async function saveSourcesConfig(config: SourcesConfig, env: NodeJS.ProcessEnv): Promise<void> {
  const root = getStateRoot(env);
  await mkdir(root, { recursive: true });
  const filePath = path.join(root, "sources.yaml");
  await writeFile(filePath, stringify(config), "utf8");
}

export function getTwitterSources(config: SourcesConfig): TwitterSourceConfig[] {
  return config.sources.filter(
    (s): s is TwitterSourceConfig => s.type === "twitter" && s.enabled,
  );
}

export function getRssSources(config: SourcesConfig): RssSource[] {
  return config.sources.filter((s): s is RssSource => s.type === "rss");
}
