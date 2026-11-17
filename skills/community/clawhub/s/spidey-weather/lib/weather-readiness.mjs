import { WEATHER_CODES } from "./weather.mjs";

const KNOWN = new Set(Object.values(WEATHER_CODES));
const LABELS = { comfortable: "Comfortable", plan_ahead: "Plan ahead", use_caution: "Use caution" };
const number = value => Number.isInteger(value) ? String(value) : value.toFixed(1);
const LIMITS = Object.freeze({ warmHighF: 90, hotHighF: 100, coolLowF: 45, freezingLowF: 32,
  rainPercent: 40, breezyMph: 15, windyMph: 25 });
export const WEATHER_READINESS_RULES = LIMITS;

// Product planning heuristics, not meteorological alert criteria. Pure evaluation:
// no model calls, network, calendar/task access, inferred UV, gusts or heat index.
export function assessWeatherReadiness(weather) {
  if (weather?.status !== "ok") return undefined;
  const day = weather.day ?? "today";
  const forecast = day === "tomorrow" ? weather.tomorrow : weather.today;
  const unavailable = () => ({ status: "unavailable", day, rulesVersion: 1,
    explanation: "I don't have enough reported condition data for an outdoor-readiness rating." });
  if (!["today", "tomorrow"].includes(day) || !forecast || !KNOWN.has(forecast.condition) ||
      ![forecast.highF, forecast.lowF, forecast.precipitationProbability].every(Number.isFinite) ||
      forecast.highF < forecast.lowF || forecast.precipitationProbability < 0 || forecast.precipitationProbability > 100) return unavailable();
  const current = day === "today" ? weather.current : undefined;
  if (day === "today" && (!current || !KNOWN.has(current.condition) ||
      ![current.windMph, current.temperatureF, current.feelsLikeF].every(Number.isFinite) || current.windMph < 0)) return unavailable();
  const flags = [];
  const add = (severity, code, basis, advice) => flags.push({ severity, code, basis, advice });
  const conditions = [["Forecast", forecast.condition], ...(current ? [["Current", current.condition]] : [])];
  for (const [scope, condition] of conditions) {
    if (/thunderstorm|freezing|heavy (?:rain|snow)|violent rain/i.test(condition)) {
      add(2, "conditions", `${scope} conditions: ${condition}`, "Consider postponing exposed outdoor plans and check official local advisories.");
    } else if (/snow|rain|drizzle|showers/i.test(condition)) {
      add(1, /snow/i.test(condition) ? "snow" : "rain", `${scope} conditions: ${condition}`,
        /snow/i.test(condition) ? "Plan for wintry conditions and check your route before leaving." : "Pack a rain layer and have a sheltered backup plan.");
    } else if (/fog/i.test(condition)) {
      add(1, "fog", `${scope} conditions: ${condition}`, "Allow extra travel time and check visibility along your route.");
    }
  }
  if (forecast.highF >= LIMITS.warmHighF) add(forecast.highF >= LIMITS.hotHighF ? 2 : 1, "heat",
    `Forecast high: ${number(forecast.highF)}°F`, "Consider a cooler part of the day for outdoor plans.");
  if (forecast.lowF <= LIMITS.coolLowF) add(forecast.lowF <= LIMITS.freezingLowF ? 2 : 1, "cold",
    `Forecast low: ${number(forecast.lowF)}°F`, "Bring a warm layer, especially for early or late outings.");
  if (current && Math.max(current.temperatureF, current.feelsLikeF) >= LIMITS.warmHighF) add(
    Math.max(current.temperatureF, current.feelsLikeF) >= LIMITS.hotHighF ? 2 : 1, "heat",
    `Current temperature / feels like: ${number(current.temperatureF)} / ${number(current.feelsLikeF)}°F`,
    "Consider a cooler part of the day for outdoor plans.");
  if (current && Math.min(current.temperatureF, current.feelsLikeF) <= LIMITS.coolLowF) add(
    Math.min(current.temperatureF, current.feelsLikeF) <= LIMITS.freezingLowF ? 2 : 1, "cold",
    `Current temperature / feels like: ${number(current.temperatureF)} / ${number(current.feelsLikeF)}°F`,
    "Bring a warm layer, especially for early or late outings.");
  if (forecast.precipitationProbability >= LIMITS.rainPercent) add(1, "rain",
    `Forecast rain chance: ${number(forecast.precipitationProbability)}%`, "Pack a rain layer and have a sheltered backup plan.");
  if (current && current.windMph >= LIMITS.breezyMph) add(current.windMph >= LIMITS.windyMph ? 2 : 1, "wind",
    `Current wind: ${number(current.windMph)} mph`, "Secure loose items and consider a more sheltered route.");
  flags.sort((a, b) => b.severity - a.severity);
  const severity = flags[0]?.severity ?? 0;
  const category = severity === 2 ? "use_caution" : severity === 1 ? "plan_ahead" : "comfortable";
  const recommendations = [...new Set(flags.map(flag => flag.advice))].slice(0, 3);
  if (!recommendations.length) recommendations.push("These readings look relatively mild for routine outdoor plans; recheck before heading out.");
  if (severity === 2 && !recommendations.some(line => line.includes("official local advisories"))) {
    recommendations.unshift("Check official local advisories before making outdoor plans.");
    recommendations.length = Math.min(3, recommendations.length);
  }
  const has = code => flags.some(flag => flag.code === code);
  const remark = severity === 2 ? undefined : has("rain") ? "Your friendly neighborhood forecast says: keep a rain layer in your utility belt."
    : has("snow") || has("cold") ? "A warm layer belongs in your friendly neighborhood utility belt."
      : has("wind") ? "Keep the utility belt secure; capes are overrated."
        : has("heat") ? "Your friendly neighborhood plan: save the long stroll for a cooler hour."
          : has("fog") ? "A little extra planning belongs in the utility belt."
            : "A promising forecast for a neighborhood stroll—web-slinging optional.";
  const basis = flags.length ? [...new Set(flags.map(flag => flag.basis))].slice(0, 3) : [
    `Forecast conditions: ${forecast.condition}`, `Forecast range: ${number(forecast.lowF)}–${number(forecast.highF)}°F`,
    `Forecast rain chance: ${number(forecast.precipitationProbability)}%`,
  ];
  return { status: "ok", day, category, label: LABELS[category], basis, recommendations,
    ...(remark ? { remark } : {}), rulesVersion: 1 };
}

export function renderWeatherReadiness(weather) {
  const assessment = assessWeatherReadiness(weather);
  if (!assessment) return undefined;
  if (assessment.status !== "ok") return `🕸️ **Spidey’s take**\n${assessment.explanation}`;
  return [`🕸️ **Spidey’s take — ${assessment.label}**`, ...assessment.recommendations.map(line => `• ${line}`),
    ...(assessment.remark ? [assessment.remark] : []), `Why: ${assessment.basis.join("; ")}.`,
    "Rule-based planning guidance, not an official weather alert."].join("\n");
}
