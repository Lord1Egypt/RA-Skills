import type { WebsiteToAdsResult, NumberedAd } from "./types.js";
import { AD_TONES } from "./types.js";

const DAYS = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];

function minuteToTime(m: number): string {
  const h = Math.floor(m / 60);
  const min = m % 60;
  const period = h >= 12 ? "PM" : "AM";
  const h12 = h === 0 ? 12 : h > 12 ? h - 12 : h;
  return `${h12}:${String(min).padStart(2, "0")} ${period}`;
}

function formatGeo(geo: Record<string, unknown>): string {
  const parts: string[] = [];
  if (Array.isArray(geo.countries) && geo.countries.length) {
    parts.push(`Countries: ${geo.countries.join(", ")}`);
  }
  if (Array.isArray(geo.regions) && geo.regions.length) {
    const names = geo.regions.map((r: unknown) =>
      typeof r === "object" && r !== null && "name" in r ? (r as { name: string }).name : String(r)
    );
    parts.push(`Regions: ${names.join(", ")}`);
  }
  if (Array.isArray(geo.cities) && geo.cities.length) {
    const names = geo.cities.map((c: unknown) =>
      typeof c === "object" && c !== null && "name" in c ? (c as { name: string }).name : String(c)
    );
    parts.push(`Cities: ${names.join(", ")}`);
  }
  return parts.join(" | ") || "US (default)";
}

function formatSchedule(schedule: unknown[]): string {
  return schedule.map((seg: unknown) => {
    const s = seg as { start_minute: number; end_minute: number; days: number[] };
    const days = s.days.map((d) => DAYS[d] ?? d).join(", ");
    return `${minuteToTime(s.start_minute)}–${minuteToTime(s.end_minute)} on ${days}`;
  }).join("\n             ");
}

function formatGenders(genders: unknown): string {
  if (!Array.isArray(genders)) return "All";
  const labels = genders.map((g) => (g === 1 ? "Male" : g === 2 ? "Female" : String(g)));
  return labels.join(", ");
}

function toneBadge(tone: string): string {
  const info = AD_TONES.find((t) => t.key === tone);
  return info ? `${info.emoji} ${info.label}` : tone;
}

function formatAd(ad: NumberedAd): string {
  const t = ad.targeting as Record<string, unknown>;
  const geo = (t.geo_locations ?? {}) as Record<string, unknown>;

  return `
┌─────────────────────────────────────────────────────────────────┐
│  #${ad.number}  ${toneBadge(ad.tone)}
│  Strategy: ${ad.intent}
└─────────────────────────────────────────────────────────────────┘

  Hook:       "${ad.hook}"

  Body:       ${ad.body}

  CTA:        ${ad.cta}

  Visual:     ${ad.visual_direction}

  Why it      ${ad.why_it_works}
  works:

  ── Targeting ──────────────────────────────────────────────────
  Geo:        ${formatGeo(geo)}
  Age:        ${t.age_min}–${t.age_max}
  Gender:     ${formatGenders(t.genders)}

  ── Schedule ───────────────────────────────────────────────────
  Run at:     ${formatSchedule(ad.adset_schedule)}`;
}

export function formatResult(result: WebsiteToAdsResult): string {
  const b = result.brand;
  const toneKeys = [...new Set(result.ads.map((a) => a.tone))];
  const toneLabels = toneKeys.map((t) => toneBadge(t));

  const header = `
── Brand Profile ────────────────────────────────────────────────

  Name:       ${b.brand_name}
  Voice:      ${b.voice}
  Tone:       ${b.tone}
  Audience:   ${b.target_audience}
  Products:   ${b.products_services.join(", ")}
  USPs:       ${b.unique_selling_points.join(", ")}
  Values:     ${b.brand_values.join(", ")}
  Geo Focus:  ${b.geographic_focus}
  Languages:  ${b.languages.join(", ")}

── Settings ─────────────────────────────────────────────────────

  Ad Tones:   ${toneLabels.join("  +  ")}
  Budget:     ${result.budget}

── Ads (${result.ads.length}) ───────────────────────────────────────────────`;

  const ads = result.ads.map((ad) => formatAd(ad)).join("\n");

  const nums = result.ads.map((a) => `#${a.number}`).join(", ");
  const footer = `
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ✓ ${result.ads.length} ads: ${nums}
  Select which to push to Meta below.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`;

  return header + "\n" + ads + "\n" + footer;
}
