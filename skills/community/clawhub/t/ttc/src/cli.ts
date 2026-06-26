#!/usr/bin/env node
/**
 * ttc — Toronto Transit Commission from the command line
 *
 * Usage:
 *   ttc next "king spadina"          # Next arrivals at a stop
 *   ttc route 504                    # Route info + active vehicles
 *   ttc vehicles 504                 # Live vehicle positions
 *   ttc alerts                       # Service disruptions
 *   ttc nearby                       # Auto-detect location (macOS)
 *   ttc nearby 43.6453,-79.3806      # Nearest stops (manual)
 *   ttc stops 504                    # All stops on a route
 *   ttc routes                       # List all routes
 *   ttc search "broadview"           # Fuzzy search stops
 *   ttc status                       # System status overview
 */

import { Command } from "commander";
import kleur from "kleur";
import { readFileSync } from "node:fs";
import { execFileSync } from "node:child_process";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";
import { TtcClient, TtcApiError } from "./lib/client.js";
import {
  searchStops,
  getRouteByNumber,
  getRouteById,
  loadRoutes,
  loadManifest,
  getStopById,
  getHeadsignsForRoute,
  findNearbyStops,
  getTripsForRoute,
  loadStops,
} from "./lib/gtfs.js";
import { getDeviceLocation, isLocationAvailable } from "./lib/location.js";

const __dirname = dirname(fileURLToPath(import.meta.url));
const pkg = JSON.parse(
  readFileSync(join(__dirname, "..", "package.json"), "utf-8")
);

const program = new Command();
const client = new TtcClient();

program
  .name("ttc")
  .description(
    "CLI for Toronto Transit Commission — real-time bus & streetcar tracking"
  )
  .version(pkg.version)
  .addHelpText(
    "after",
    `
Examples:
  $ ttc next "king spadina"           Next arrivals at a stop
  $ ttc route 504                     Route info + active vehicles
  $ ttc nearby                        Auto-detect location (macOS)
  $ ttc nearby 43.6453,-79.3806       Nearest stops with coordinates
  $ ttc alerts                        Service disruptions
  $ ttc vehicles 504                  Live vehicle positions

Live monitoring:
  $ ttc loop 3m next "king spadina"   Watch arrivals while getting ready
  $ ttc loop 5m alerts                Monitor disruptions during storms
  $ ttc loop 2m vehicles 504          Track vehicles approaching your stop
  $ ttc loop 30s nearby               Refresh nearby arrivals as you walk`
  );

// ─── Helpers ─────────────────────────────────────────────────────────────────

function addJsonOption(cmd: Command): Command {
  return cmd.option("--json", "Output as JSON");
}

function handleError(err: unknown): never {
  if (err instanceof TtcApiError) {
    console.error(kleur.red(`Error: ${err.message}`));
    if (err.url) console.error(kleur.dim(`URL: ${err.url}`));
  } else if (err instanceof Error) {
    console.error(kleur.red(`Error: ${err.message}`));
  } else {
    console.error(kleur.red("Unknown error"));
  }
  process.exit(1);
}

function formatMinutesAway(arrivalTime: number): string {
  const now = Math.floor(Date.now() / 1000);
  const mins = Math.round((arrivalTime - now) / 60);
  if (mins <= 0) return kleur.green("NOW");
  if (mins <= 3) return kleur.green(`${mins} min`);
  if (mins <= 10) return kleur.yellow(`${mins} min`);
  return kleur.dim(`${mins} min`);
}

function formatOccupancy(status: string): string {
  switch (status) {
    case "EMPTY":
      return kleur.green("Empty");
    case "MANY_SEATS_AVAILABLE":
      return kleur.green("Many seats");
    case "FEW_SEATS_AVAILABLE":
      return kleur.yellow("Few seats");
    case "STANDING_ROOM_ONLY":
      return kleur.yellow("Standing");
    case "CRUSHED_STANDING_ROOM_ONLY":
      return kleur.red("Crowded");
    case "FULL":
      return kleur.red("Full");
    case "NOT_ACCEPTING_PASSENGERS":
      return kleur.red("Not boarding");
    default:
      return "";
  }
}

function resolveStopId(query: string): { stopId: string; stopName: string } {
  if (/^\d+$/.test(query)) {
    const stop = getStopById(query);
    if (stop) return { stopId: stop.stop_id, stopName: stop.stop_name };
    const byCode = loadStops().find((s) => s.stop_code === query);
    if (byCode)
      return { stopId: byCode.stop_id, stopName: byCode.stop_name };
  }

  const results = searchStops(query, 1);
  if (results.length === 0) {
    console.error(kleur.red(`No stop found matching "${query}"`));
    console.error(kleur.dim("Try: ttc search <query>"));
    process.exit(1);
  }
  const best = results[0];
  if (best.score < 0.5) {
    console.error(
      kleur.yellow(
        `Best match: "${best.stop.stop_name}" (${Math.round(best.score * 100)}% match)`
      )
    );
  }
  return { stopId: best.stop.stop_id, stopName: best.stop.stop_name };
}

// ─── next ────────────────────────────────────────────────────────────────────

const nextCmd = program
  .command("next <stop>")
  .description("Next arrivals at a stop (by name, stop ID, or stop code)")
  .option("--limit <n>", "Max arrivals to show", "10");
addJsonOption(nextCmd);

nextCmd.action(async (stop: string, opts: { limit: string; json?: boolean }) => {
  try {
    const { stopId, stopName } = resolveStopId(stop);
    const tripUpdates = await client.getNextArrivals(stopId);

    const now = Math.floor(Date.now() / 1000);
    const arrivals: Array<{
      routeId: string;
      routeName: string;
      headsign: string;
      vehicleId: string;
      arrivalTime: number;
      minutesAway: number;
    }> = [];

    for (const tu of tripUpdates) {
      const route = getRouteById(tu.routeId);
      const trips = getTripsForRoute(tu.routeId);
      const matchedTrip = trips.find((t) => t.trip_id === tu.tripId);
      // Fallback: find any headsign for this route
      const headsign = matchedTrip?.trip_headsign ?? trips[0]?.trip_headsign ?? "";

      for (const stu of tu.stopTimeUpdates) {
        const time = stu.arrivalTime ?? stu.departureTime;
        if (!time || time < now) continue;

        arrivals.push({
          routeId: tu.routeId,
          routeName: route?.route_long_name ?? tu.routeId,
          headsign,
          vehicleId: tu.vehicleId,
          arrivalTime: time,
          minutesAway: Math.round((time - now) / 60),
        });
      }
    }

    arrivals.sort((a, b) => a.arrivalTime - b.arrivalTime);
    const limited = arrivals.slice(0, parseInt(opts.limit) || 10);

    if (opts.json) {
      console.log(JSON.stringify({ stopId, stopName, arrivals: limited }, null, 2));
      return;
    }

    console.log(kleur.bold(`Next arrivals at ${stopName}`));
    console.log(kleur.dim(`Stop ID: ${stopId}\n`));

    if (limited.length === 0) {
      console.log(kleur.dim("No upcoming arrivals found."));
      return;
    }

    for (const a of limited) {
      console.log(
        `  ${kleur.cyan(a.routeId.padEnd(5))} ` +
          `${a.headsign.padEnd(30)} ` +
          `${formatMinutesAway(a.arrivalTime)}`
      );
    }
  } catch (err) {
    handleError(err);
  }
});

// ─── route ───────────────────────────────────────────────────────────────────

const routeCmd = program
  .command("route <number>")
  .description("Show route info and active vehicles");
addJsonOption(routeCmd);

routeCmd.action(async (number: string, opts: { json?: boolean }) => {
  try {
    const route = getRouteByNumber(number);
    if (!route) {
      console.error(kleur.red(`Route "${number}" not found.`));
      process.exit(1);
    }

    const [vehicles, alerts] = await Promise.all([
      client.getVehicles(route.route_id),
      client.getAlerts(route.route_id),
    ]);

    const headsigns = getHeadsignsForRoute(route.route_id);

    if (opts.json) {
      console.log(JSON.stringify({ route, headsigns, vehicles, alerts }, null, 2));
      return;
    }

    const typeLabel = route.route_type === 0 ? "Streetcar" : "Bus";
    console.log(
      kleur.bold(`${route.route_short_name} — ${route.route_long_name}`)
    );
    console.log(`  Type: ${typeLabel}`);
    console.log(`  Directions:`);
    for (const h of headsigns) {
      console.log(
        `    ${h.directionId === 0 ? "\u2192" : "\u2190"} ${h.headsign}`
      );
    }
    console.log(
      `  Active vehicles: ${kleur.cyan(String(vehicles.length))}`
    );
    if (alerts.length > 0) {
      console.log(kleur.yellow(`  Alerts: ${alerts.length}`));
      for (const a of alerts) {
        console.log(`    ${kleur.yellow("!")} ${a.headerText}`);
      }
    }
  } catch (err) {
    handleError(err);
  }
});

// ─── vehicles ────────────────────────────────────────────────────────────────

const vehiclesCmd = program
  .command("vehicles [route]")
  .description("Live vehicle positions (all or by route)");
addJsonOption(vehiclesCmd);

vehiclesCmd.action(async (routeNum: string | undefined, opts: { json?: boolean }) => {
  try {
    let routeId: string | undefined;
    if (routeNum) {
      const route = getRouteByNumber(routeNum);
      if (!route) {
        console.error(kleur.red(`Route "${routeNum}" not found.`));
        process.exit(1);
      }
      routeId = route.route_id;
    }

    const vehicles = await client.getVehicles(routeId);

    if (opts.json) {
      console.log(JSON.stringify(vehicles, null, 2));
      return;
    }

    console.log(
      kleur.bold(
        routeId
          ? `Vehicles on route ${routeNum} (${vehicles.length})`
          : `All active vehicles (${vehicles.length})`
      )
    );
    console.log();

    for (const v of vehicles) {
      const route = getRouteById(v.routeId);
      const stop = getStopById(v.stopId);
      const occupancy = formatOccupancy(v.occupancyStatus);
      console.log(
        `  ${kleur.cyan(v.vehicleId.padEnd(6))} ` +
          `${(route?.route_short_name ?? v.routeId).padEnd(5)} ` +
          `${v.currentStatus.padEnd(14)} ` +
          `${kleur.dim((stop?.stop_name ?? v.stopId).substring(0, 30).padEnd(30))}` +
          (occupancy ? ` ${occupancy}` : "")
      );
    }
  } catch (err) {
    handleError(err);
  }
});

// ─── alerts ──────────────────────────────────────────────────────────────────

const alertsCmd = program
  .command("alerts [route]")
  .description("Current service alerts and disruptions")
  .option("--broad", "Include subway and broader alerts (gtfsrt.ttc.ca)");
addJsonOption(alertsCmd);

alertsCmd.action(
  async (routeNum: string | undefined, opts: { broad?: boolean; json?: boolean }) => {
    try {
      let routeId: string | undefined;
      if (routeNum) {
        const route = getRouteByNumber(routeNum);
        routeId = route?.route_id;
      }

      const alertSets = await Promise.all([
        client.getAlerts(routeId),
        opts.broad ? client.getBroadAlerts(routeId) : Promise.resolve([]),
      ]);

      // Deduplicate by headerText
      const seen = new Set<string>();
      const alerts = [];
      for (const set of alertSets) {
        for (const a of set) {
          if (!seen.has(a.headerText)) {
            seen.add(a.headerText);
            alerts.push(a);
          }
        }
      }

      if (opts.json) {
        console.log(JSON.stringify(alerts, null, 2));
        return;
      }

      if (alerts.length === 0) {
        console.log(kleur.green("No active alerts."));
        return;
      }

      console.log(kleur.bold(`Service Alerts (${alerts.length})`));
      console.log();

      for (const a of alerts) {
        const routes =
          a.routeIds.length > 0
            ? kleur.cyan(a.routeIds.join(", "))
            : kleur.dim("system-wide");
        console.log(`  ${kleur.yellow("!")} ${kleur.bold(a.headerText)}`);
        console.log(`    Routes: ${routes}`);
        if (a.descriptionText) {
          const desc =
            a.descriptionText.length > 120
              ? a.descriptionText.slice(0, 120) + "..."
              : a.descriptionText;
          console.log(`    ${kleur.dim(desc)}`);
        }
        console.log();
      }
    } catch (err) {
      handleError(err);
    }
  }
);

// ─── nearby ──────────────────────────────────────────────────────────────────

const nearbyCmd = program
  .command("nearby [coordinates]")
  .description("Nearest stops and upcoming arrivals (auto-detects location on macOS)")
  .option("--radius <meters>", "Search radius in meters", "500")
  .option("--limit <n>", "Max stops to show", "5");
addJsonOption(nearbyCmd);

nearbyCmd.action(
  async (
    coordinates: string | undefined,
    opts: { radius: string; limit: string; json?: boolean }
  ) => {
    try {
      let lat: number;
      let lng: number;

      if (coordinates) {
        const [latStr, lngStr] = coordinates.split(",");
        lat = parseFloat(latStr);
        lng = parseFloat(lngStr);

        if (isNaN(lat) || isNaN(lng)) {
          console.error(kleur.red("Invalid coordinates. Use format: lat,lng"));
          console.error(kleur.dim("Example: ttc nearby 43.6453,-79.3806"));
          process.exit(1);
        }
      } else {
        if (!isLocationAvailable()) {
          console.error(kleur.red("No coordinates provided and location detection unavailable."));
          console.error(kleur.dim("Usage: ttc nearby <lat,lng>"));
          console.error(kleur.dim("Location auto-detect requires macOS with Xcode Command Line Tools."));
          process.exit(1);
        }
        if (!opts.json) {
          process.stderr.write(kleur.dim("Detecting location..."));
        }
        try {
          const loc = await getDeviceLocation();
          lat = loc.latitude;
          lng = loc.longitude;
          if (!opts.json) {
            process.stderr.write(`\r${kleur.green("✓")} Location: ${lat.toFixed(4)}, ${lng.toFixed(4)}\n`);
          }
        } catch (locErr: any) {
          if (!opts.json) process.stderr.write("\n");
          console.error(kleur.red(locErr.message));
          process.exit(1);
        }
      }

      const radius = parseInt(opts.radius) || 500;
      const limit = parseInt(opts.limit) || 5;
      const nearbyStops = findNearbyStops(lat, lng, radius, limit);

      if (nearbyStops.length === 0) {
        console.log(kleur.dim(`No stops found within ${radius}m.`));
        return;
      }

      // Fetch arrivals for each nearby stop in parallel
      const results = await Promise.all(
        nearbyStops.map(async (ns) => {
          const tripUpdates = await client
            .getNextArrivals(ns.stop.stop_id)
            .catch(() => []);
          return { ...ns, tripUpdates };
        })
      );

      if (opts.json) {
        console.log(JSON.stringify(results, null, 2));
        return;
      }

      console.log(kleur.bold(`Stops near ${lat.toFixed(4)}, ${lng.toFixed(4)}`));
      console.log();

      const now = Math.floor(Date.now() / 1000);
      for (const r of results) {
        console.log(
          `  ${kleur.bold(r.stop.stop_name)} ` +
            `${kleur.dim(`(${r.distanceMeters}m, ID: ${r.stop.stop_id})`)}`
        );

        const arrivals = r.tripUpdates
          .flatMap((tu) =>
            tu.stopTimeUpdates
              .filter((stu) => (stu.arrivalTime ?? 0) > now)
              .map((stu) => ({
                routeId: tu.routeId,
                arrivalTime: stu.arrivalTime!,
              }))
          )
          .sort((a, b) => a.arrivalTime - b.arrivalTime)
          .slice(0, 3);

        if (arrivals.length > 0) {
          for (const a of arrivals) {
            console.log(
              `    ${kleur.cyan(a.routeId.padEnd(5))} ${formatMinutesAway(a.arrivalTime)}`
            );
          }
        } else {
          console.log(kleur.dim("    No upcoming arrivals"));
        }
        console.log();
      }
    } catch (err) {
      handleError(err);
    }
  }
);

// ─── stops ───────────────────────────────────────────────────────────────────

const stopsCmd = program
  .command("stops <route>")
  .description("List stops on a route (from static data)");
addJsonOption(stopsCmd);

stopsCmd.action(async (routeNum: string, opts: { json?: boolean }) => {
  try {
    const route = getRouteByNumber(routeNum);
    if (!route) {
      console.error(kleur.red(`Route "${routeNum}" not found.`));
      process.exit(1);
    }

    // Get active vehicles to find which stops this route serves
    const vehicles = await client.getVehicles(route.route_id);
    const stopIds = new Set<string>();
    for (const v of vehicles) {
      if (v.stopId) stopIds.add(v.stopId);
    }

    // Also get trip updates for more stop coverage
    const tripUpdates = await client.getTripUpdates(route.route_id);
    for (const tu of tripUpdates) {
      for (const stu of tu.stopTimeUpdates) {
        stopIds.add(stu.stopId);
      }
    }

    const stops = [...stopIds]
      .map((id) => getStopById(id))
      .filter((s): s is NonNullable<typeof s> => s != null);

    if (opts.json) {
      console.log(JSON.stringify({ route, stops }, null, 2));
      return;
    }

    console.log(
      kleur.bold(
        `Stops on ${route.route_short_name} — ${route.route_long_name} (${stops.length} active)`
      )
    );
    console.log();

    for (const s of stops) {
      console.log(
        `  ${kleur.cyan(s.stop_id.padEnd(6))} ${s.stop_name}`
      );
    }
  } catch (err) {
    handleError(err);
  }
});

// ─── routes ──────────────────────────────────────────────────────────────────

const routesCmd = program
  .command("routes")
  .description("List all surface routes")
  .option("--type <type>", "Filter by type: bus, streetcar, all", "all");
addJsonOption(routesCmd);

routesCmd.action((opts: { type: string; json?: boolean }) => {
  try {
    let routes = loadRoutes();
    if (opts.type === "bus") {
      routes = routes.filter((r) => r.route_type === 3);
    } else if (opts.type === "streetcar") {
      routes = routes.filter((r) => r.route_type === 0);
    }

    if (opts.json) {
      console.log(JSON.stringify(routes, null, 2));
      return;
    }

    console.log(kleur.bold(`TTC Surface Routes (${routes.length})`));
    console.log();
    for (const r of routes) {
      const type =
        r.route_type === 0
          ? kleur.yellow("streetcar")
          : kleur.blue("bus      ");
      console.log(
        `  ${kleur.cyan(r.route_short_name.padEnd(5))} ${type} ${r.route_long_name}`
      );
    }
  } catch (err) {
    handleError(err);
  }
});

// ─── search ──────────────────────────────────────────────────────────────────

const searchCmd = program
  .command("search <query>")
  .description("Fuzzy search for stops by name")
  .option("--limit <n>", "Max results", "10");
addJsonOption(searchCmd);

searchCmd.action((query: string, opts: { limit: string; json?: boolean }) => {
  try {
    const results = searchStops(query, parseInt(opts.limit) || 10);

    if (opts.json) {
      console.log(JSON.stringify(results, null, 2));
      return;
    }

    if (results.length === 0) {
      console.log(kleur.dim(`No stops matching "${query}".`));
      return;
    }

    console.log(kleur.bold(`Stops matching "${query}"`));
    console.log();
    for (const r of results) {
      const pct = Math.round(r.score * 100);
      console.log(
        `  ${kleur.cyan(r.stop.stop_id.padEnd(6))} ` +
          `${r.stop.stop_name.padEnd(40)} ` +
          `${kleur.dim(`${pct}%  code:${r.stop.stop_code}`)}`
      );
    }
  } catch (err) {
    handleError(err);
  }
});

// ─── status ──────────────────────────────────────────────────────────────────

const statusCmd = program
  .command("status")
  .description("System status — alerts summary + data freshness");
addJsonOption(statusCmd);

statusCmd.action(async (opts: { json?: boolean }) => {
  try {
    const [vehicles, alerts, manifest] = await Promise.all([
      client.getVehicles(),
      client.getAlerts(),
      Promise.resolve(loadManifest()),
    ]);

    const routeSet = new Set(vehicles.map((v) => v.routeId).filter(Boolean));

    const statusData = {
      activeVehicles: vehicles.length,
      activeRoutes: routeSet.size,
      alertCount: alerts.length,
      staticDataBundled: manifest.bundled,
      staticDataSource: manifest.source,
      stops: manifest.stop_count,
      routes: manifest.route_count,
    };

    if (opts.json) {
      console.log(JSON.stringify(statusData, null, 2));
      return;
    }

    console.log(kleur.bold("TTC System Status"));
    console.log();
    console.log(
      `  Active vehicles: ${kleur.cyan(String(statusData.activeVehicles))}`
    );
    console.log(
      `  Active routes:   ${kleur.cyan(String(statusData.activeRoutes))}`
    );
    console.log(
      `  Alerts:          ${statusData.alertCount > 0 ? kleur.yellow(String(statusData.alertCount)) : kleur.green("0")}`
    );
    console.log();
    console.log(kleur.dim("Static Data:"));
    console.log(`  Bundled:  ${manifest.bundled}`);
    console.log(`  Stops:    ${manifest.stop_count}`);
    console.log(`  Routes:   ${manifest.route_count}`);
    console.log(`  Source:   ${manifest.source}`);

    if (alerts.length > 0) {
      console.log();
      console.log(kleur.yellow("Active Alerts:"));
      for (const a of alerts.slice(0, 5)) {
        console.log(`  ${kleur.yellow("!")} ${a.headerText}`);
      }
      if (alerts.length > 5) {
        console.log(
          kleur.dim(`  ... and ${alerts.length - 5} more. Run: ttc alerts`)
        );
      }
    }
  } catch (err) {
    handleError(err);
  }
});

// ─── loop ───────────────────────────────────────────────────────────────────

function parseInterval(input: string): number {
  const match = input.match(/^(\d+)(s|m|h)?$/);
  if (!match) return 0;
  const val = parseInt(match[1]);
  switch (match[2]) {
    case "h": return val * 3600;
    case "m": return val * 60;
    case "s": return val;
    default: return val;
  }
}

const loopCmd = program
  .command("loop <interval> <command> [args...]")
  .description("Re-run a ttc command on an interval (e.g. ttc loop 3m nearby)")
  .addHelpText("after", `
Examples:
  $ ttc loop 3m next "king spadina"    Watch arrivals every 3 minutes
  $ ttc loop 5m alerts                 Monitor alerts every 5 minutes
  $ ttc loop 2m vehicles 504           Track vehicles every 2 minutes
  $ ttc loop 30s nearby                Refresh nearby stops every 30 seconds

Interval format: 30s, 3m, 1h, or just seconds (e.g. 180)`);

loopCmd.action(
  async (interval: string, command: string, args: string[]) => {
    const seconds = parseInterval(interval);
    if (seconds < 5) {
      console.error(kleur.red("Interval must be at least 5 seconds."));
      process.exit(1);
    }

    const cliPath = join(__dirname, "cli.js");
    const cmdArgs = [cliPath, command, ...args];

    const run = () => {
      process.stdout.write("\x1B[2J\x1B[H"); // clear screen
      const time = new Date().toLocaleTimeString();
      console.log(kleur.dim(`[${time}] ttc ${command} ${args.join(" ")}  (every ${interval}, Ctrl+C to stop)\n`));
      try {
        execFileSync(process.execPath, cmdArgs, { stdio: "inherit" });
      } catch {
        // command failed — show error but keep looping
      }
    };

    run();
    const timer = setInterval(run, seconds * 1000);
    process.on("SIGINT", () => {
      clearInterval(timer);
      console.log(kleur.dim("\nStopped."));
      process.exit(0);
    });
  }
);

program.parse();
