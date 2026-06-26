/**
 * License text fingerprinting — identifies license type from file content.
 */
export type LicenseId = "MIT" | "Apache-2.0" | "BSD-2-Clause" | "BSD-3-Clause" | "GPL-2.0" | "GPL-3.0" | "LGPL-2.1" | "LGPL-3.0" | "MPL-2.0" | "ISC" | "BSL-1.1" | "SSPL-1.0" | "Unlicense" | "AGPL-3.0" | "UNKNOWN";
/**
 * Detect license type from raw license file text.
 */
export declare function detectLicenseFromText(text: string): LicenseId;
/**
 * Normalize a license SPDX identifier from package metadata.
 */
export declare function normalizeSpdx(raw: string): LicenseId;
