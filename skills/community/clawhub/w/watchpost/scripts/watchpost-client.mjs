// Shared transport. The CLI helpers cannot select another network origin.
export const API_ORIGIN = "https://api.watchpost.systems";
export const TIMEOUT_MS = 30000;
export const isObject = (v) => v !== null && typeof v === "object" && !Array.isArray(v);
export const validId = (v) => typeof v === "string" && /^[A-Za-z0-9_-]{1,128}$/.test(v);
export const failure = (code, error, message) => ({
	code,
	output: { kind: "error", error, message },
});
// Accept current and legacy URL-safe token bodies. Authentication stays server-side.
export const validToken = (token) =>
	typeof token === "string" && /^wp_[A-Za-z0-9_-]+$/.test(token) && token.length <= 512;

export async function request(path, init, token, fetchImpl = fetch) {
	if (!validToken(token))
		return failure(
			3,
			"missing_token",
			"Set WATCHPOST_TOKEN to a connection token from https://app.watchpost.systems/connections. Do not paste it into chat.",
		);
	if (path !== "/v1/verify" && !/^\/v1\/transactions\/[A-Za-z0-9_-]{1,128}\/status$/.test(path))
		return failure(3, "invalid_path", "Unsupported Watchpost API path.");
	const controller = new AbortController();
	const timeout = setTimeout(() => controller.abort(), TIMEOUT_MS);
	try {
		const response = await fetchImpl(`${API_ORIGIN}${path}`, {
			...init,
			redirect: "error",
			signal: controller.signal,
			headers: { "content-type": "application/json", authorization: `Bearer ${token}` },
		});
		if (response.status >= 300 && response.status < 400)
			return failure(
				5,
				"redirect_rejected",
				"Watchpost returned a redirect. No redirected request was sent.",
			);
		if (response.status === 401 || response.status === 403)
			return failure(
				3,
				"authentication_failed",
				"Watchpost rejected the connection token. Reconnect the agent before checking again.",
			);
		if (response.status === 429) {
			const seconds = response.headers.get("retry-after");
			return {
				...failure(
					5,
					"rate_limited",
					"Watchpost is rate limiting requests. Wait before checking again; no automatic retry was made.",
				),
				output: {
					kind: "error",
					error: "rate_limited",
					message: "Wait before checking again. No automatic retry was made.",
					retryAfterSeconds: /^\d+$/.test(seconds ?? "")
						? Math.min(3600, Math.max(3, Number(seconds)))
						: 30,
				},
			};
		}
		const reader = response.body?.getReader();
		if (!reader)
			return failure(5, "invalid_response", "Watchpost returned an empty response. Do not pay.");
		const chunks = [];
		let size = 0;
		for (;;) {
			const { done, value } = await reader.read();
			if (done) break;
			size += value.byteLength;
			if (size > 262144) {
				await reader.cancel();
				return failure(5, "invalid_response", "Watchpost returned too much data. Do not pay.");
			}
			chunks.push(value);
		}
		let body;
		try {
			body = JSON.parse(Buffer.concat(chunks).toString("utf8"));
		} catch {
			return failure(5, "invalid_response", "Watchpost returned invalid JSON. Do not pay.");
		}
		if (response.status === 402 && isObject(body) && body.error === "free_limit_reached")
			return {
				code: 4,
				output: {
					kind: "error",
					error: "free_limit_reached",
					message: "This purchase was not checked. Review your allowance or plan before retrying.",
					upgradeUrl: "https://app.watchpost.systems/billing",
				},
			};
		if (response.status === 400 || response.status === 422)
			return failure(
				3,
				"invalid_input",
				"Watchpost rejected the purchase details. Check the currency, merchant and required fields. No usable verdict was returned.",
			);
		if (!response.ok)
			return failure(
				5,
				"api_error",
				`Watchpost returned HTTP ${response.status}. No usable result was received. Do not pay.`,
			);
		return { body };
	} catch {
		return failure(
			5,
			"request_failed",
			"Watchpost could not complete the request within 30 seconds, or the connection failed. Do not pay. The server may have recorded the check; do not retry automatically.",
		);
	} finally {
		clearTimeout(timeout);
		// Close unread error/redirect bodies as well as timed-out requests.
		controller.abort();
	}
}

export function printResult(result) {
	console.log(JSON.stringify(result.output, null, 2));
	process.exitCode = result.code;
}
