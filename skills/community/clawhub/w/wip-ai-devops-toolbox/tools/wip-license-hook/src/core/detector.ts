/**
 * License text fingerprinting — identifies license type from file content.
 */

export type LicenseId =
  | "MIT"
  | "Apache-2.0"
  | "BSD-2-Clause"
  | "BSD-3-Clause"
  | "GPL-2.0"
  | "GPL-3.0"
  | "LGPL-2.1"
  | "LGPL-3.0"
  | "MPL-2.0"
  | "ISC"
  | "BSL-1.1"
  | "SSPL-1.0"
  | "Unlicense"
  | "AGPL-3.0"
  | "UNKNOWN";

interface Fingerprint {
  id: LicenseId;
  markers: string[];       // All must match (case-insensitive)
  antiMarkers?: string[];  // None must match
}

const FINGERPRINTS: Fingerprint[] = [
  {
    id: "MIT",
    markers: ["permission is hereby granted, free of charge", "the software is provided \"as is\""],
    antiMarkers: ["apache", "gnu general public"],
  },
  {
    id: "Apache-2.0",
    markers: ["apache license", "version 2.0"],
  },
  {
    id: "GPL-3.0",
    markers: ["gnu general public license", "version 3"],
    antiMarkers: ["lesser general public"],
  },
  {
    id: "GPL-2.0",
    markers: ["gnu general public license", "version 2"],
    antiMarkers: ["lesser general public", "version 3"],
  },
  {
    id: "LGPL-3.0",
    markers: ["gnu lesser general public license", "version 3"],
  },
  {
    id: "LGPL-2.1",
    markers: ["gnu lesser general public license", "version 2.1"],
  },
  {
    id: "AGPL-3.0",
    markers: ["gnu affero general public license", "version 3"],
  },
  {
    id: "BSD-3-Clause",
    markers: ["redistribution and use in source and binary forms", "neither the name"],
  },
  {
    id: "BSD-2-Clause",
    markers: ["redistribution and use in source and binary forms"],
    antiMarkers: ["neither the name"],
  },
  {
    id: "MPL-2.0",
    markers: ["mozilla public license", "version 2.0"],
  },
  {
    id: "ISC",
    markers: ["isc license", "permission to use, copy, modify"],
  },
  {
    id: "BSL-1.1",
    markers: ["business source license", "1.1"],
  },
  {
    id: "SSPL-1.0",
    markers: ["server side public license"],
  },
  {
    id: "Unlicense",
    markers: ["this is free and unencumbered software released into the public domain"],
  },
];

/**
 * Detect license type from raw license file text.
 */
export function detectLicenseFromText(text: string): LicenseId {
  const lower = text.toLowerCase();

  for (const fp of FINGERPRINTS) {
    const allMatch = fp.markers.every((m) => lower.includes(m));
    const anyAnti = fp.antiMarkers?.some((m) => lower.includes(m)) ?? false;
    if (allMatch && !anyAnti) return fp.id;
  }

  return "UNKNOWN";
}

/**
 * Normalize a license SPDX identifier from package metadata.
 */
export function normalizeSpdx(raw: string): LicenseId {
  const map: Record<string, LicenseId> = {
    mit: "MIT",
    "apache-2.0": "Apache-2.0",
    apache2: "Apache-2.0",
    "bsd-2-clause": "BSD-2-Clause",
    "bsd-3-clause": "BSD-3-Clause",
    "gpl-2.0": "GPL-2.0",
    "gpl-3.0": "GPL-3.0",
    "gpl-3.0-only": "GPL-3.0",
    "lgpl-2.1": "LGPL-2.1",
    "lgpl-3.0": "LGPL-3.0",
    "mpl-2.0": "MPL-2.0",
    isc: "ISC",
    "bsl-1.1": "BSL-1.1",
    "sspl-1.0": "SSPL-1.0",
    unlicense: "Unlicense",
    "agpl-3.0": "AGPL-3.0",
    "agpl-3.0-only": "AGPL-3.0",
  };
  return map[raw.toLowerCase().trim()] ?? "UNKNOWN";
}
