#!/usr/bin/env npx tsx
/**
 * Download TTC Surface GTFS data and pre-process to JSON.
 *
 * Usage: npm run update-gtfs
 *
 * Downloads SurfaceGTFS.zip from Open Toronto, parses CSV files,
 * and writes data/stops.json, data/routes.json, data/trips.json, data/manifest.json.
 */

import { execFileSync } from "node:child_process";
import { readFileSync, writeFileSync, mkdirSync } from "node:fs";
import { join, dirname } from "node:path";
import { tmpdir } from "node:os";
import { fileURLToPath } from "node:url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const DATA_DIR = join(__dirname, "..", "data");
const TMP_DIR = join(tmpdir(), "ttc-gtfs-" + Date.now());

const SURFACE_GTFS_URL =
  "https://ckan0.cf.opendata.inter.prod-toronto.ca/dataset/bd4809dd-e289-4de8-bbde-c5c00dafbf4f/resource/28514055-d011-4ed7-8bb0-97961dfe2b66/download/SurfaceGTFS.zip";

// ─── CSV Parser ──────────────────────────────────────────────────────────────

function parseCSV(filePath: string): Record<string, string>[] {
  const content = readFileSync(filePath, "utf-8");
  const lines = content.trim().split("\n");
  const headerLine = lines[0].replace(/^\uFEFF/, "");
  const headers = parseCSVLine(headerLine);

  return lines.slice(1).map((line) => {
    const values = parseCSVLine(line);
    const obj: Record<string, string> = {};
    headers.forEach((h, i) => {
      obj[h] = values[i] ?? "";
    });
    return obj;
  });
}

function parseCSVLine(line: string): string[] {
  const fields: string[] = [];
  let current = "";
  let inQuotes = false;

  for (let i = 0; i < line.length; i++) {
    const ch = line[i];
    if (ch === '"') {
      if (inQuotes && line[i + 1] === '"') {
        current += '"';
        i++;
      } else {
        inQuotes = !inQuotes;
      }
    } else if (ch === "," && !inQuotes) {
      fields.push(current.trim());
      current = "";
    } else {
      current += ch;
    }
  }
  fields.push(current.trim());
  return fields;
}

// ─── Main ────────────────────────────────────────────────────────────────────

function main() {
  mkdirSync(TMP_DIR, { recursive: true });
  mkdirSync(DATA_DIR, { recursive: true });

  // 1. Download
  console.log("Downloading SurfaceGTFS.zip...");
  const zipPath = join(TMP_DIR, "SurfaceGTFS.zip");
  execFileSync("curl", ["-sL", "-o", zipPath, SURFACE_GTFS_URL]);
  console.log(`  Saved to ${zipPath}`);

  // 2. Extract
  console.log("Extracting...");
  execFileSync("unzip", ["-o", zipPath, "-d", TMP_DIR], { stdio: "pipe" });

  // 3. Process stops
  console.log("Processing stops...");
  const stopsRaw = parseCSV(join(TMP_DIR, "stops.txt"));
  const stops = stopsRaw
    .filter((s) => s.stop_id && s.stop_name)
    .map((s) => ({
      stop_id: s.stop_id,
      stop_code: s.stop_code ?? "",
      stop_name: s.stop_name,
      stop_lat: parseFloat(s.stop_lat),
      stop_lon: parseFloat(s.stop_lon),
    }));
  console.log(`  ${stops.length} stops`);

  // 4. Process routes
  console.log("Processing routes...");
  const routesRaw = parseCSV(join(TMP_DIR, "routes.txt"));
  const routes = routesRaw
    .filter((r) => r.route_id)
    .map((r) => ({
      route_id: r.route_id,
      route_short_name: r.route_short_name ?? "",
      route_long_name: r.route_long_name ?? "",
      route_type: parseInt(r.route_type ?? "3"),
    }));
  console.log(`  ${routes.length} routes`);

  // 5. Process trips (deduplicated to unique route+direction+headsign combos)
  console.log("Processing trips...");
  const tripsRaw = parseCSV(join(TMP_DIR, "trips.txt"));
  const tripMap = new Map<
    string,
    { trip_id: string; route_id: string; direction_id: number; trip_headsign: string }
  >();

  for (const t of tripsRaw) {
    if (!t.trip_id || !t.route_id) continue;
    const key = `${t.route_id}:${t.direction_id ?? 0}:${t.trip_headsign ?? ""}`;
    if (!tripMap.has(key)) {
      tripMap.set(key, {
        trip_id: t.trip_id,
        route_id: t.route_id,
        direction_id: parseInt(t.direction_id ?? "0"),
        trip_headsign: t.trip_headsign ?? "",
      });
    }
  }
  const trips = [...tripMap.values()];
  console.log(`  ${tripsRaw.length} total trips → ${trips.length} unique combos`);

  // 6. Write JSON files
  const today = new Date().toISOString().split("T")[0];

  writeFileSync(join(DATA_DIR, "stops.json"), JSON.stringify(stops));
  writeFileSync(join(DATA_DIR, "routes.json"), JSON.stringify(routes));
  writeFileSync(join(DATA_DIR, "trips.json"), JSON.stringify(trips));
  writeFileSync(
    join(DATA_DIR, "manifest.json"),
    JSON.stringify(
      {
        bundled: today,
        source: "Open Toronto SurfaceGTFS",
        stop_count: stops.length,
        route_count: routes.length,
        trip_count: trips.length,
      },
      null,
      2
    )
  );

  // File sizes
  for (const f of ["stops.json", "routes.json", "trips.json", "manifest.json"]) {
    const size = readFileSync(join(DATA_DIR, f)).length;
    console.log(`  data/${f}: ${(size / 1024).toFixed(1)} KB`);
  }

  // Cleanup
  execFileSync("rm", ["-rf", TMP_DIR]);
  console.log("\nDone! Static GTFS data bundled in data/");
}

main();
