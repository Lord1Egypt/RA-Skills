/**
 * Meta Marketing API targeting & schedule normalization.
 * Adapted from coachbot/src/lib/meta-targeting.ts for standalone use.
 */

const GEO_ARRAY_KEYS = ["countries", "regions", "cities", "zips", "custom_locations"] as const;
const DEFAULT_GEO = { countries: ["US"] };
const DEFAULT_SCHEDULE: unknown[] = [
  { start_minute: 0, end_minute: 1439, days: [0, 1, 2, 3, 4, 5, 6] },
];

function coerceIntInRange(v: unknown, fallback: number, min: number, max: number): number {
  let n: number;
  if (typeof v === "number" && Number.isFinite(v)) n = Math.round(v);
  else if (typeof v === "string" && v.trim() !== "") {
    const p = Number.parseInt(v.trim(), 10);
    n = Number.isFinite(p) ? p : fallback;
  } else n = fallback;
  return Math.min(max, Math.max(min, n));
}

function normalizeGeoArrayEntry(x: unknown): string | Record<string, unknown> | null {
  if (typeof x === "string") {
    const t = x.trim();
    return t.length > 0 ? t : null;
  }
  if (typeof x === "number" && Number.isFinite(x)) return String(Math.round(x));
  if (x && typeof x === "object" && !Array.isArray(x)) return { ...(x as Record<string, unknown>) };
  return null;
}

function normalizeGeoLocations(raw: unknown): Record<string, unknown> {
  if (!raw || typeof raw !== "object" || Array.isArray(raw)) return { ...DEFAULT_GEO };
  const g = { ...(raw as Record<string, unknown>) };
  for (const key of GEO_ARRAY_KEYS) {
    const v = g[key];
    if (typeof v === "string" && v.trim()) {
      g[key] = [v.trim()];
    } else if (Array.isArray(v)) {
      g[key] = v.map(normalizeGeoArrayEntry).filter((item): item is string | Record<string, unknown> => item != null);
    }
  }
  const hasAny = GEO_ARRAY_KEYS.some((key) => Array.isArray(g[key]) && (g[key] as unknown[]).length > 0);
  return hasAny ? g : { ...DEFAULT_GEO };
}

function normalizeGenders(raw: unknown): number[] {
  if (!Array.isArray(raw) || raw.length === 0) return [1, 2];
  const labelMap: Record<string, number> = {
    "1": 1, "2": 2, male: 1, female: 2, Male: 1, Female: 2, MALE: 1, FEMALE: 2,
  };
  const out: number[] = [];
  for (const g of raw) {
    if (g === 1 || g === 2) out.push(g);
    else if (typeof g === "string") {
      const fromLabel = labelMap[g.trim()];
      if (fromLabel !== undefined) out.push(fromLabel);
      else {
        const n = Number.parseInt(g.trim(), 10);
        if (n === 1 || n === 2) out.push(n);
      }
    }
  }
  const uniq = Array.from(new Set(out));
  return uniq.length > 0 ? uniq : [1, 2];
}

function validateTargeting(input: Record<string, unknown>): Record<string, unknown> {
  const t = input;
  const geo = t.geo_locations;
  if (!geo || typeof geo !== "object" || Array.isArray(geo)) {
    throw new Error("targeting.geo_locations must be an object.");
  }
  const geoRecord = geo as Record<string, unknown>;
  const hasValidGeo = GEO_ARRAY_KEYS.some(
    (key) => Array.isArray(geoRecord[key]) && (geoRecord[key] as unknown[]).length > 0
  );
  if (!hasValidGeo) {
    throw new Error("targeting.geo_locations must include at least one non-empty area array.");
  }
  if (typeof t.age_min !== "number" || typeof t.age_max !== "number") {
    throw new Error("targeting must include numeric age_min and age_max.");
  }
  if (t.age_min < 13 || t.age_max < t.age_min) {
    throw new Error("targeting age_min/age_max are invalid.");
  }
  if (!Array.isArray(t.genders) || t.genders.length === 0) {
    throw new Error("targeting.genders must be a non-empty array.");
  }
  return t;
}

function validateSchedule(input: unknown[]): unknown[] {
  if (input.length === 0) throw new Error("adset_schedule must have at least one segment.");
  for (let i = 0; i < input.length; i++) {
    const seg = input[i];
    if (!seg || typeof seg !== "object" || Array.isArray(seg)) {
      throw new Error(`adset_schedule[${i}] must be an object.`);
    }
    const s = seg as Record<string, unknown>;
    if (typeof s.start_minute !== "number" || typeof s.end_minute !== "number") {
      throw new Error(`adset_schedule[${i}] must include start_minute and end_minute.`);
    }
    if (!Array.isArray(s.days) || s.days.length === 0) {
      throw new Error(`adset_schedule[${i}].days must be a non-empty array.`);
    }
  }
  return input;
}

export function normalizeTargeting(input: unknown): Record<string, unknown> {
  const base =
    input && typeof input === "object" && !Array.isArray(input)
      ? { ...(input as Record<string, unknown>) }
      : {};
  base.geo_locations = normalizeGeoLocations(base.geo_locations);
  let ageMin = coerceIntInRange(base.age_min, 18, 13, 99);
  let ageMax = coerceIntInRange(base.age_max, 55, 13, 99);
  if (ageMax < ageMin) [ageMin, ageMax] = [ageMax, ageMin];
  base.age_min = ageMin;
  base.age_max = ageMax;
  base.genders = normalizeGenders(base.genders);
  return validateTargeting(base);
}

export function normalizeSchedule(input: unknown): unknown[] {
  if (!Array.isArray(input) || input.length === 0) return validateSchedule(DEFAULT_SCHEDULE);
  const out: unknown[] = [];
  for (const seg of input) {
    if (!seg || typeof seg !== "object" || Array.isArray(seg)) continue;
    const s = { ...(seg as Record<string, unknown>) };
    let start = coerceIntInRange(s.start_minute, 0, 0, 1439);
    let end = coerceIntInRange(s.end_minute, 1439, 0, 1439);
    if (end < start) [start, end] = [end, start];
    s.start_minute = start;
    s.end_minute = end;
    const days = s.days;
    if (!Array.isArray(days) || days.length === 0) {
      s.days = [0, 1, 2, 3, 4, 5, 6];
    } else {
      const coerced = days.map((d) => coerceIntInRange(d, 0, 0, 6));
      const uniq = Array.from(new Set(coerced));
      s.days = uniq.length > 0 ? uniq : [0, 1, 2, 3, 4, 5, 6];
    }
    out.push(s);
  }
  return out.length === 0 ? validateSchedule(DEFAULT_SCHEDULE) : validateSchedule(out);
}
