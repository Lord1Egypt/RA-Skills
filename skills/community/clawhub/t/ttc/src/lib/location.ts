/**
 * macOS device location via CoreLocation.
 * Uses a compiled .app bundle helper launched via `open -W` to get precise
 * GPS/WiFi coordinates. The .app bundle is required because macOS Ventura+
 * only grants location permission to proper app bundles, not CLI tools.
 */

import { execFile } from "node:child_process";
import { existsSync, readFileSync, unlinkSync, writeFileSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { platform, tmpdir } from "node:os";

const __dirname = dirname(fileURLToPath(import.meta.url));
const HELPER_APP = join(
  __dirname, "..", "..", "helpers", "TTC Location.app"
);

export interface DeviceLocation {
  latitude: number;
  longitude: number;
}

export function isLocationAvailable(): boolean {
  return platform() === "darwin" && existsSync(
    join(HELPER_APP, "Contents", "MacOS", "ttc-location")
  );
}

export function getDeviceLocation(): Promise<DeviceLocation> {
  return new Promise((resolve, reject) => {
    if (platform() !== "darwin") {
      reject(new Error("Location detection is only available on macOS."));
      return;
    }

    if (!isLocationAvailable()) {
      reject(new Error(
        "Location helper not compiled. Reinstall: npm install -g @lucasygu/ttc"
      ));
      return;
    }

    const tmpFile = join(tmpdir(), `ttc-location-${process.pid}.txt`);
    // Create empty file so we can detect if it was written to
    writeFileSync(tmpFile, "");

    // Launch as proper .app via `open -W` so macOS grants location permission
    execFile("open", ["-W", HELPER_APP, "--args", tmpFile], { timeout: 20000 }, (err) => {
      try {
        const result = existsSync(tmpFile)
          ? readFileSync(tmpFile, "utf-8").trim()
          : "";

        // Clean up
        try { unlinkSync(tmpFile); } catch {}

        if (!result || result === "") {
          reject(new Error("Location request failed — no response from helper."));
          return;
        }

        if (result === "denied") {
          reject(new Error(
            "Location access denied. Grant permission in System Settings → Privacy & Security → Location Services → TTC Location."
          ));
          return;
        }

        if (result === "timeout") {
          reject(new Error("Location request timed out. Ensure Location Services is enabled in System Settings."));
          return;
        }

        if (result.startsWith("error:")) {
          reject(new Error(result.slice(6)));
          return;
        }

        const parts = result.split(",");
        if (parts.length !== 2) {
          reject(new Error(`Unexpected location output: ${result}`));
          return;
        }

        const latitude = parseFloat(parts[0]);
        const longitude = parseFloat(parts[1]);
        if (isNaN(latitude) || isNaN(longitude)) {
          reject(new Error(`Invalid coordinates: ${result}`));
          return;
        }

        resolve({ latitude, longitude });
      } catch (readErr: any) {
        reject(new Error(`Location failed: ${readErr.message}`));
      }
    });
  });
}
