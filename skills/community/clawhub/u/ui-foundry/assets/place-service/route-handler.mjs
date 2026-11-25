/**
 * Framework-neutral, server-only route adapter. Mount it at a same-origin
 * endpoint such as POST /api/place-search. Authentication, authorization,
 * rate limiting and CSRF policy remain application responsibilities.
 */
import { PlaceServiceError } from "./amap-place-service.mjs";

const MAX_BODY_BYTES = 8_192;

class BodyTooLargeError extends Error {}

/**
 * @param {{
 *   placeService: {search(request: {query: string, city?: string, limit?: number, signal?: AbortSignal}): Promise<unknown>},
 *   origin: string,
 *   authenticate: (request: Request) => Promise<boolean> | boolean,
 *   rateLimit: (request: Request) => Promise<boolean> | boolean
 * }} dependencies
 */
export function createPlaceSearchHandler(dependencies) {
	if (
		!dependencies?.placeService ||
		typeof dependencies.authenticate !== "function" ||
		typeof dependencies.rateLimit !== "function"
	) {
		throw new Error("Place search handler requires service, authentication, and rate-limit hooks.");
	}
	const expectedOrigin = new URL(dependencies.origin).origin;

	return async function handlePlaceSearch(request) {
		if (request.method !== "POST") return json({ error: "Method not allowed." }, 405);
		const origin = request.headers.get("origin");
		if (origin && origin !== expectedOrigin) return json({ error: "Forbidden." }, 403);
		if (!(await dependencies.authenticate(request))) return json({ error: "Unauthorized." }, 401);
		if (!(await dependencies.rateLimit(request))) return json({ error: "Too many requests." }, 429);
		if (!request.headers.get("content-type")?.toLowerCase().startsWith("application/json")) {
			return json({ error: "Unsupported content type." }, 415);
		}

		let body;
		try {
			body = await readJsonBody(request);
		} catch (error) {
			if (error instanceof BodyTooLargeError)
				return json({ error: "Request body is too large." }, 413);
			return json({ error: "Invalid request." }, 400);
		}

		try {
			const places = await dependencies.placeService.search({
				query: body?.query,
				city: body?.city,
				limit: body?.limit,
				signal: request.signal,
			});
			return json({ places }, 200);
		} catch (error) {
			if (error instanceof PlaceServiceError)
				return json({ error: error.message, code: error.code }, statusFor(error.code));
			return json({ error: "Place search is temporarily unavailable.", code: "UNAVAILABLE" }, 503);
		}
	};
}

function statusFor(code) {
	if (code === "INVALID_REQUEST") return 400;
	if (code === "ABORTED") return 499;
	if (code === "TIMEOUT" || code === "UNAVAILABLE" || code === "CONFIGURATION") return 503;
	return 500;
}

async function readJsonBody(request) {
	const declaredLength = request.headers.get("content-length");
	if (
		declaredLength &&
		(!/^\d+$/.test(declaredLength) || Number(declaredLength) > MAX_BODY_BYTES)
	) {
		throw new BodyTooLargeError();
	}
	if (!request.body) throw new Error("Missing body.");

	const reader = request.body.getReader();
	const chunks = [];
	let length = 0;
	try {
		while (true) {
			const { done, value } = await reader.read();
			if (done) break;
			length += value.byteLength;
			if (length > MAX_BODY_BYTES) {
				await reader.cancel();
				throw new BodyTooLargeError();
			}
			chunks.push(value);
		}
	} finally {
		reader.releaseLock();
	}

	const bytes = new Uint8Array(length);
	let offset = 0;
	for (const chunk of chunks) {
		bytes.set(chunk, offset);
		offset += chunk.byteLength;
	}
	return JSON.parse(new TextDecoder().decode(bytes));
}

function json(body, status) {
	return Response.json(body, {
		status,
		headers: { "Cache-Control": "no-store" },
	});
}
