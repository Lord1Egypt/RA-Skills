import OpenAI from "openai";
import type { BrandProfile } from "./types.js";

const BRAND_ANALYSIS_PROMPT = `You are a senior brand strategist. Analyze the following website content and extract a structured brand profile.

Return ONLY a single JSON object with these fields:
- brand_name (string): The business/brand name
- voice (string): Brand voice description (e.g. "warm and approachable", "bold and authoritative")
- tone (string): Communication tone (e.g. "casual", "professional", "playful", "inspirational")
- target_audience (string): Who this brand serves — be specific about demographics and psychographics
- products_services (string[]): List of main products or services offered
- unique_selling_points (string[]): What makes this brand different — concrete differentiators
- brand_values (string[]): Core values expressed on the site
- geographic_focus (string): Where this business operates (city, region, country, or "global")
- languages (string[]): Languages used on the site

Be concrete and specific. Avoid generic filler. Base everything on the actual content provided.

No markdown. No code fences. Just the JSON object.`;

export async function analyzeBrand(
  websiteContent: string,
  url: string,
  openaiKey: string,
  model = "gpt-4o"
): Promise<BrandProfile> {
  const openai = new OpenAI({ apiKey: openaiKey });

  const completion = await openai.chat.completions.create({
    model,
    temperature: 0.3,
    max_tokens: 2000,
    messages: [
      { role: "system", content: BRAND_ANALYSIS_PROMPT },
      {
        role: "user",
        content: `Website URL: ${url}\n\nScraped content:\n${websiteContent.slice(0, 12000)}`,
      },
    ],
  });

  const text = typeof completion.choices[0]?.message?.content === "string"
    ? completion.choices[0].message.content.trim()
    : "";

  if (!text) throw new Error("Brand analysis returned empty response.");

  const cleaned = text.replace(/^```(?:json)?\s*/i, "").replace(/\s*```$/, "").trim();
  const profile = JSON.parse(cleaned) as BrandProfile;
  profile.website_url = url;
  return profile;
}
