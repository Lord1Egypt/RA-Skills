import { formatDisplayDate } from "./display-date.mjs";
import { WEATHER_ENDPOINT, normalizeWeather, readWeatherResponse } from "./weather.mjs";
import { assessWeatherReadiness, renderWeatherReadiness } from "./weather-readiness.mjs";
import { weatherIcon } from "./weather-presentation.mjs";

const DEFAULT = Object.freeze({ label: "Los Angeles, California", latitude: 34.0522,
  longitude: -118.2437, timezone: "America/Los_Angeles" });
const GEOCODING = "https://geocoding-api.open-meteo.com/v1/search";
const text = value => String(value ?? "").replace(/[\u0000-\u001f\u007f]/g, " ").replace(/\s+/g, " ").trim().slice(0, 160);
const escaped = value => text(value).replace(/[\\`*_\[\]<>]/g, c => `\\${c}`);
const fold = value => text(value).normalize("NFD").replace(/\p{M}/gu, "").toLowerCase();
const COUNTRY_ALIASES = new Map([["usa", "us"], ["united states", "us"], ["united states of america", "us"],
  ["uk", "gb"], ["united kingdom", "gb"]]);
const country = value => COUNTRY_ALIASES.get(fold(value)) ?? fold(value);
function place(row) {
  if (!row || typeof row.name !== "string" || !row.name.trim() ||
      !Number.isFinite(row.latitude) || Math.abs(row.latitude) > 90 ||
      !Number.isFinite(row.longitude) || Math.abs(row.longitude) > 180 || typeof row.timezone !== "string") {
    throw new Error("INVALID_WEATHER_LOCATION");
  }
  new Intl.DateTimeFormat("en", { timeZone: row.timezone });
  const label = [...new Set([row.name, row.admin1, row.country ?? row.country_code].filter(v => typeof v === "string" && v.trim()).map(text))].join(", ");
  return { label, name: text(row.name), latitude: row.latitude, longitude: row.longitude,
    timezone: row.timezone, countryCode: text(row.country_code).toUpperCase(), country: text(row.country) };
}

// The location argument is a public place name, never an arbitrary request URL.
// Per-request resolution never changes the scheduled briefing's LA constants.
export async function lookupWeather({ location, countryCode, day = "today", signal,
  fetcher = fetch, now = () => new Date() } = {}) {
  if (!["today", "tomorrow"].includes(day)) throw new Error("INVALID_WEATHER_DAY");
  if (location !== undefined && typeof location !== "string") throw new Error("INVALID_WEATHER_LOCATION");
  if (countryCode !== undefined && (typeof countryCode !== "string" || !/^[a-z]{2}$/i.test(countryCode))) throw new Error("INVALID_WEATHER_COUNTRY");
  const query = location?.trim() ?? "";
  if (query && (!/^[\p{L}\p{M}\p{N} ,.'’()-]{2,120}$/u.test(query) || query.split(",").length > 3)) throw new Error("INVALID_WEATHER_LOCATION");
  if (signal?.aborted) throw new Error("WEATHER_ABORTED");
  const timeout = AbortSignal.timeout(15000);
  const combined = signal ? AbortSignal.any([signal, timeout]) : timeout;
  const get = async url => {
    combined.throwIfAborted();
    const data = await readWeatherResponse(await fetcher(url, { method: "GET", redirect: "error",
      headers: { Accept: "application/json" }, signal: combined }));
    combined.throwIfAborted();
    return data;
  };
  try {
    let selected = DEFAULT;
    const la = ["la", "l.a.", "los angeles", "los angeles, ca", "los angeles, california", "los angeles, united states", "los angeles, us"]
      .includes(fold(query)) && (!countryCode || countryCode.toUpperCase() === "US");
    if (query && !la) {
      const parts = query.split(",").map(s => s.trim());
      if (parts.some(part => !part)) throw new Error("INVALID_WEATHER_LOCATION");
      const url = new URL(GEOCODING);
      url.searchParams.set("name", parts.slice(0, 2).join(", "));
      url.searchParams.set("count", "5"); url.searchParams.set("language", "en"); url.searchParams.set("format", "json");
      if (countryCode) url.searchParams.set("countryCode", countryCode.toUpperCase());
      const data = await get(url.toString());
      if (data.error || (data.results !== undefined && !Array.isArray(data.results))) throw new Error("INVALID_WEATHER_GEOCODING");
      let candidates = (data.results ?? []).slice(0, 5).map(place);
      if (countryCode) candidates = candidates.filter(row => row.countryCode === countryCode.toUpperCase());
      // Open-Meteo applies the first comma qualifier; honour a supplied third
      // country component ourselves instead of silently dropping that constraint.
      if (parts[2]) candidates = candidates.filter(row => [country(row.country), country(row.countryCode)].includes(country(parts[2])));
      const exact = candidates.filter(row => fold(row.name) === fold(parts[0]));
      if (exact.length) candidates = exact;
      candidates = [...new Map(candidates.map(row => [`${row.latitude},${row.longitude}`, row])).values()];
      if (!candidates.length) return { status: "not_found", query, day };
      if (candidates.length > 1) return { status: "ambiguous", query, day, choices: candidates.map(row => row.label) };
      selected = candidates[0];
    } else if (countryCode && countryCode.toUpperCase() !== "US") {
      return { status: "needs_location", day };
    }
    const url = new URL(WEATHER_ENDPOINT);
    url.searchParams.set("latitude", String(selected.latitude));
    url.searchParams.set("longitude", String(selected.longitude));
    url.searchParams.set("timezone", selected.timezone);
    const raw = await get(url.toString());
    const checked = now();
    const weather = normalizeWeather(raw, checked, { location: selected.label, timezone: selected.timezone });
    if (weather.current.humidity < 0 || weather.current.humidity > 100 || weather.current.windMph < 0 ||
      [weather.today, weather.tomorrow].some(item => item.lowF > item.highF || item.precipitationProbability < 0 || item.precipitationProbability > 100)) {
      throw new Error("INVALID_WEATHER_VALUES");
    }
    if (signal?.aborted) throw new Error("WEATHER_ABORTED");
    const result = { ...weather, day, defaultLocation: !query, checkedAt: checked.toISOString(), source: "Open-Meteo",
      ...(typeof raw.current.time === "string" && /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}$/.test(raw.current.time)
        ? { providerTime: raw.current.time } : {}) };
    return { ...result, readiness: assessWeatherReadiness(result) };
  } catch {
    if (signal?.aborted) throw new Error("WEATHER_ABORTED");
    return { status: "error", error: "WEATHER_UNAVAILABLE", day };
  }
}

export function renderWeatherLookup(result) {
  if (result.status === "ambiguous") return ["🕷️ Which location did you mean?",
    ...result.choices.map(label => `• ${escaped(label)}`), "Please include the state, region or country."].join("\n");
  if (result.status === "unsupported_day") return "🕷️ This weather lookup supports current conditions and today's or tomorrow's forecast.";
  if (["not_found", "needs_location"].includes(result.status)) return "🕷️ I couldn't identify that location. Please give a city with its state, region or country.";
  if (result.status !== "ok") return "🕷️ Weather data is unavailable right now. Please try again.";
  const n = value => String(Math.round(value));
  const lines = ["🕷️ **Weather — " + escaped(result.location) + "**", `${escaped(result.timezone)} · °F`];
  if (result.day !== "tomorrow") lines.push("", `${weatherIcon(result.current.condition)} ${escaped(result.current.condition)} · ${n(result.current.temperatureF)}°F`,
    `Feels like ${n(result.current.feelsLikeF)}°F · Wind ${n(result.current.windMph)} mph · Humidity ${n(result.current.humidity)}%`);
  const forecast = result.day === "tomorrow" ? result.tomorrow : result.today;
  lines.push("", `**${result.day === "tomorrow" ? "Tomorrow" : "Today"} · ${formatDisplayDate(forecast.date)}**`,
    `${weatherIcon(forecast.condition)} ${escaped(forecast.condition)} · High ${n(forecast.highF)}° · Low ${n(forecast.lowF)}°`,
    `Rain chance: ${n(forecast.precipitationProbability)}%`, "", "Source: [Open-Meteo](https://open-meteo.com/)");
  if (result.providerTime && result.day !== "tomorrow") lines.push(`Provider time: ${formatDisplayDate(result.providerTime.slice(0, 10))} at ${escaped(result.providerTime.slice(11))} (${escaped(result.timezone)})`);
  if (result.defaultLocation) lines.push("Default location: Los Angeles.");
  const take = renderWeatherReadiness(result);
  if (take) lines.push("", take);
  return lines.join("\n");
}

export function createWeatherTool({ lookup = lookupWeather, logger } = {}) {
  return {
    name: "weather_lookup", label: "Weather",
    description: "Get verified current weather and today's or tomorrow's forecast. Defaults to Los Angeles when no location is provided. " +
      "Use location from the user's current question (city, region/country); an override applies only to this call. " +
      "Returns a rule-based outdoor-readiness assessment and Spidey's take without additional model inference. " +
      "Uses public weather/geocoding APIs only; no calendar, email, tasks or web search. Ask to clarify ambiguous places. Fahrenheit, with local dates/timezone.",
    parameters: { type: "object", properties: {
      location: { type: "string", maxLength: 120, description: "Only the public city/place from the current question; omit for Los Angeles. Optional comma-separated state/region/country." },
      countryCode: { type: "string", minLength: 2, maxLength: 2, description: "Optional ISO two-letter country code when specified, e.g. US or FR." },
      day: { type: "string", enum: ["today", "tomorrow"], description: "Defaults to today. Use tomorrow only when asked." },
    }, additionalProperties: false },
    catalogMode: "direct-only", canDeliverSourceReply: true, resultContentSource: "network",
    async execute(_id, params, signal) {
      let result;
      try { result = await lookup({ location: params?.location, countryCode: params?.countryCode, day: params?.day, signal }); }
      catch (error) {
        if (signal?.aborted) throw new Error("WEATHER_ABORTED");
        result = { status: error?.message === "INVALID_WEATHER_DAY" ? "unsupported_day"
          : /^INVALID_WEATHER_(LOCATION|COUNTRY)$/.test(error?.message ?? "") ? "needs_location" : "error" };
      }
      logger?.info?.(`[briefing-data] weather status=${result.status} defaultLocation=${result.defaultLocation === true}`);
      const text = renderWeatherLookup(result);
      return { content: [{ type: "text", text }], details: { sourceReply: { text }, weather: result } };
    },
  };
}
