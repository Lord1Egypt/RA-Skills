export type Provider = "google" | "openai" | "dashscope" | "replicate" | "tuzi";

export type CliArgs = {
  prompt: string | null;
  filename: string | null;
  inputImage: string | null;
  resolution: "1K" | "2K" | "4K";
  provider: Provider | null;
  model: string | null;
  apiKey: string | null;
};
