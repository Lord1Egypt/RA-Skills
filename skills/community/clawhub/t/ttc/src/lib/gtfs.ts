/**
 * Static GTFS data loader + fuzzy stop search.
 * Loads pre-processed JSON from data/ directory (bundled with npm package).
 */

import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";
import type { GtfsStop, GtfsRoute, GtfsTrip, GtfsManifest, StopSearchResult } from "./types.js";

const __dirname = dirname(fileURLToPath(import.meta.url));
const DATA_DIR = join(__dirname, "..", "..", "data");

// Lazy-loaded caches
let _stops: GtfsStop[] | null = null;
let _routes: GtfsRoute[] | null = null;
let _trips: GtfsTrip[] | null = null;
let _manifest: GtfsManifest | null = null;

// Stop index for fast ID lookups
let _stopById: Map<string, GtfsStop> | null = null;
let _stopByCode: Map<string, GtfsStop> | null = null;

// ─── Loaders ─────────────────────────────────────────────────────────────────

export function loadStops(): GtfsStop[] {
  if (_stops) return _stops;
  const raw = readFileSync(join(DATA_DIR, "stops.json"), "utf-8");
  _stops = JSON.parse(raw) as GtfsStop[];
  for (const stop of _stops) {
    stop.normalized = normalizeName(stop.stop_name);
  }
  return _stops;
}

export function loadRoutes(): GtfsRoute[] {
  if (_routes) return _routes;
  const raw = readFileSync(join(DATA_DIR, "routes.json"), "utf-8");
  _routes = JSON.parse(raw) as GtfsRoute[];
  return _routes;
}

export function loadTrips(): GtfsTrip[] {
  if (_trips) return _trips;
  const raw = readFileSync(join(DATA_DIR, "trips.json"), "utf-8");
  _trips = JSON.parse(raw) as GtfsTrip[];
  return _trips;
}

export function loadManifest(): GtfsManifest {
  if (_manifest) return _manifest;
  const raw = readFileSync(join(DATA_DIR, "manifest.json"), "utf-8");
  _manifest = JSON.parse(raw) as GtfsManifest;
  return _manifest;
}

function buildStopIndex(): void {
  if (_stopById) return;
  const stops = loadStops();
  _stopById = new Map();
  _stopByCode = new Map();
  for (const s of stops) {
    _stopById.set(s.stop_id, s);
    if (s.stop_code) _stopByCode.set(s.stop_code, s);
  }
}

// ─── Fuzzy Stop Search ───────────────────────────────────────────────────────

const NOISE_WORDS = new Set([
  "st", "ave", "rd", "dr", "blvd", "cres", "ct", "pl", "ln",
  "at", "the", "and", "&", "of", "near",
  "east", "west", "north", "south", "e", "w", "n", "s",
]);

function normalizeName(name: string): string {
  return name
    .toLowerCase()
    .replace(/[^a-z0-9\s]/g, " ")
    .split(/\s+/)
    .filter((w) => !NOISE_WORDS.has(w) && w.length > 0)
    .join(" ");
}

export function searchStops(query: string, maxResults = 10): StopSearchResult[] {
  const stops = loadStops();

  // Direct ID/code lookup
  if (/^\d+$/.test(query)) {
    buildStopIndex();
    const byId = _stopById!.get(query);
    if (byId) return [{ stop: byId, score: 1.0 }];
    const byCode = _stopByCode!.get(query);
    if (byCode) return [{ stop: byCode, score: 1.0 }];
  }

  const queryTokens = normalizeName(query).split(/\s+/).filter(Boolean);
  if (queryTokens.length === 0) return [];

  const scored: StopSearchResult[] = [];

  for (const stop of stops) {
    const normalized = stop.normalized ?? normalizeName(stop.stop_name);
    let matchCount = 0;
    for (const qt of queryTokens) {
      if (normalized.includes(qt)) matchCount++;
    }
    if (matchCount === 0) continue;
    const score = matchCount / queryTokens.length;
    scored.push({ stop, score });
  }

  scored.sort((a, b) => {
    if (b.score !== a.score) return b.score - a.score;
    return a.stop.stop_name.length - b.stop.stop_name.length;
  });

  return scored.slice(0, maxResults);
}

// ─── Lookups ─────────────────────────────────────────────────────────────────

export function getStopById(stopId: string): GtfsStop | undefined {
  buildStopIndex();
  return _stopById!.get(stopId);
}

export function getRouteById(routeId: string): GtfsRoute | undefined {
  return loadRoutes().find((r) => r.route_id === routeId);
}

export function getRouteByNumber(num: string): GtfsRoute | undefined {
  return loadRoutes().find(
    (r) => r.route_short_name === num || r.route_id === num
  );
}

export function getTripsForRoute(routeId: string): GtfsTrip[] {
  return loadTrips().filter((t) => t.route_id === routeId);
}

export function getHeadsignsForRoute(
  routeId: string
): Array<{ directionId: number; headsign: string }> {
  const trips = getTripsForRoute(routeId);
  const seen = new Map<string, { directionId: number; headsign: string }>();
  for (const t of trips) {
    const key = `${t.direction_id}:${t.trip_headsign}`;
    if (!seen.has(key)) {
      seen.set(key, { directionId: t.direction_id, headsign: t.trip_headsign });
    }
  }
  return [...seen.values()];
}

export function getStopsForRoute(routeId: string): GtfsStop[] {
  // This requires stop_times.txt which we don't bundle (too large).
  // Return empty — the CLI will note this limitation.
  return [];
}

// ─── Geo Helpers ─────────────────────────────────────────────────────────────

export function distanceMeters(
  lat1: number, lon1: number,
  lat2: number, lon2: number
): number {
  const R = 6371000;
  const toRad = (d: number) => (d * Math.PI) / 180;
  const dLat = toRad(lat2 - lat1);
  const dLon = toRad(lon2 - lon1);
  const a =
    Math.sin(dLat / 2) ** 2 +
    Math.cos(toRad(lat1)) * Math.cos(toRad(lat2)) * Math.sin(dLon / 2) ** 2;
  return R * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
}

export function findNearbyStops(
  lat: number,
  lon: number,
  maxDistance = 500,
  maxResults = 10
): Array<{ stop: GtfsStop; distanceMeters: number }> {
  const stops = loadStops();
  const results: Array<{ stop: GtfsStop; distanceMeters: number }> = [];

  for (const stop of stops) {
    const d = distanceMeters(lat, lon, stop.stop_lat, stop.stop_lon);
    if (d <= maxDistance) {
      results.push({ stop, distanceMeters: Math.round(d) });
    }
  }

  results.sort((a, b) => a.distanceMeters - b.distanceMeters);
  return results.slice(0, maxResults);
}
