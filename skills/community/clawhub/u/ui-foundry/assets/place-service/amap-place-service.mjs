/**
 * Server-only AMap POI v5 adapter.
 *
 * Never import this module into a browser bundle. `key` is deliberately added
 * only while constructing the server-to-server request URL, and is never
 * exposed by returned values or errors.
 *
 * Official API: https://lbs.amap.com/api/webservice/guide/api-advanced/newpoisearch
 */

const AMAP_TEXT_SEARCH_ENDPOINT = "https://restapi.amap.com/v5/place/text";
const DEFAULT_TIMEOUT_MS = 5_000;
const DEFAULT_LIMIT = 8;
const MAX_LIMIT = 25;

export class PlaceServiceError extends Error {
	constructor(code, message) {
		super(message);
		this.name = "PlaceServiceError";
		this.code = code;
	}
}

/**
 * @typedef {{
 *   id: string,
 *   label: string,
 *   address: string,
 *   latitude: number,
 *   longitude: number,
 *   coordinateSystem: "GCJ-02",
 *   source: "amap"
 * }} PlaceResult
 */

/**
 * Create a POI search service backed by AMap Web Service API v5.
 *
 * Pass `key` from a server-only secret store, or set AMAP_WEB_SERVICE_KEY in
 * the server process. Do not expose either value as a public build variable.
 * `fetchImpl` exists for runtimes and deterministic tests; it is never sent to
 * the client.
 *
 * @param {{key?: string, fetchImpl?: typeof fetch, timeoutMs?: number}} options
 */
export function createAMapPlaceService(options = {}) {
	const key = options.key ?? globalThis.process?.env?.AMAP_WEB_SERVICE_KEY;
	const fetchImpl = options.fetchImpl ?? globalThis.fetch;
	const timeoutMs = options.timeoutMs ?? DEFAULT_TIMEOUT_MS;

	if (typeof fetchImpl !== "function") {
		throw new PlaceServiceError("CONFIGURATION", "Place search is not configured.");
	}
	if (!Number.isFinite(timeoutMs) || timeoutMs <= 0) {
		throw new PlaceServiceError("CONFIGURATION", "Place search is not configured.");
	}

	return {
		/**
		 * @param {{query: string, city?: string, limit?: number, signal?: AbortSignal}} request
		 * @returns {Promise<PlaceResult[]>}
		 */
		async search(request) {
			const query = normalizeQuery(request?.query);
			const city = normalizeCity(request?.city);
			const limit = normalizeLimit(request?.limit);
			if (request?.signal?.aborted) {
				throw new PlaceServiceError("ABORTED", "Place search was cancelled.");
			}

			if (typeof key !== "string" || key.trim().length === 0) {
				throw new PlaceServiceError("CONFIGURATION", "Place search is not configured.");
			}

			const url = new URL(AMAP_TEXT_SEARCH_ENDPOINT);
			url.searchParams.set("key", key);
			url.searchParams.set("keywords", query);
			url.searchParams.set("page_size", String(limit));
			url.searchParams.set("page_num", "1");
			url.searchParams.set("output", "json");
			if (city) {
				url.searchParams.set("region", city);
				url.searchParams.set("city_limit", "true");
			}

			const timeoutController = new AbortController();
			const combined = combineSignals(request?.signal, timeoutController.signal);
			const timeout = setTimeout(() => timeoutController.abort("timeout"), timeoutMs);

			try {
				const response = await fetchImpl(url, {
					method: "GET",
					headers: { Accept: "application/json" },
					redirect: "error",
					signal: combined.signal,
				});

				if (!response?.ok) {
					throw new PlaceServiceError("UNAVAILABLE", "Place search is temporarily unavailable.");
				}

				const payload = await response.json();

				if (!payload || payload.status !== "1" || !Array.isArray(payload.pois)) {
					throw new PlaceServiceError("UNAVAILABLE", "Place search is temporarily unavailable.");
				}

				return payload.pois.map(mapPoi).filter((place) => place !== null);
			} catch (error) {
				if (error instanceof PlaceServiceError) throw error;
				if (request?.signal?.aborted) {
					throw new PlaceServiceError("ABORTED", "Place search was cancelled.");
				}
				if (timeoutController.signal.aborted) {
					throw new PlaceServiceError("TIMEOUT", "Place search timed out.");
				}
				throw new PlaceServiceError("UNAVAILABLE", "Place search is temporarily unavailable.");
			} finally {
				clearTimeout(timeout);
				combined.dispose();
			}
		},
	};
}

function normalizeQuery(value) {
	if (typeof value !== "string") {
		throw new PlaceServiceError("INVALID_REQUEST", "Enter a place to search.");
	}
	const query = value.trim();
	if (query.length === 0 || query.length > 80) {
		throw new PlaceServiceError("INVALID_REQUEST", "Enter a place to search.");
	}
	return query;
}

function normalizeCity(value) {
	if (value == null || value === "") return undefined;
	if (typeof value !== "string") {
		throw new PlaceServiceError("INVALID_REQUEST", "Choose a valid city.");
	}
	const city = value.trim();
	if (city.length === 0 || city.length > 64) {
		throw new PlaceServiceError("INVALID_REQUEST", "Choose a valid city.");
	}
	return city;
}

function normalizeLimit(value) {
	if (value == null) return DEFAULT_LIMIT;
	if (!Number.isInteger(value) || value < 1 || value > MAX_LIMIT) {
		throw new PlaceServiceError("INVALID_REQUEST", "Choose a valid result limit.");
	}
	return value;
}

function mapPoi(poi) {
	if (!poi || typeof poi !== "object") return null;
	if (typeof poi.id !== "string" || poi.id.trim().length === 0) return null;
	if (typeof poi.name !== "string" || poi.name.trim().length === 0) return null;
	if (typeof poi.address !== "string" || poi.address.trim().length === 0) return null;
	const coordinates = parseCoordinates(poi.location);
	if (!coordinates) return null;

	return {
		id: poi.id.trim(),
		label: poi.name.trim(),
		address: poi.address.trim(),
		latitude: coordinates.latitude,
		longitude: coordinates.longitude,
		coordinateSystem: "GCJ-02",
		source: "amap",
	};
}

function parseCoordinates(value) {
	if (typeof value !== "string") return null;
	const match = /^\s*(-?(?:\d+\.?\d*|\.\d+))\s*,\s*(-?(?:\d+\.?\d*|\.\d+))\s*$/.exec(value);
	if (!match) return null;
	const longitude = Number(match[1]);
	const latitude = Number(match[2]);
	if (!Number.isFinite(longitude) || !Number.isFinite(latitude)) return null;
	if (longitude < -180 || longitude > 180 || latitude < -90 || latitude > 90) return null;
	return { latitude, longitude };
}

function combineSignals(externalSignal, timeoutSignal) {
	const controller = new AbortController();
	const abort = () => controller.abort();
	const signals = [externalSignal, timeoutSignal].filter(Boolean);
	for (const signal of signals) {
		if (signal.aborted) abort();
		else signal.addEventListener("abort", abort, { once: true });
	}
	return {
		signal: controller.signal,
		dispose() {
			for (const signal of signals) signal.removeEventListener("abort", abort);
		},
	};
}
