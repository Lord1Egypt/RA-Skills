#!/usr/bin/env node
import { pathToFileURL } from "node:url";
import { localCommand, readPurchaseInput } from "./cli.mjs";
import { CURRENCY_CODES } from "./currency-codes.mjs";
import { failure, isObject, printResult, request, validId } from "./watchpost-client.mjs";

function publicHost(host) {
	if (
		typeof host !== "string" ||
		host.length > 253 ||
		!host.includes(".") ||
		!host.split(".").every((label) => /^[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?$/i.test(label))
	)
		throw new Error("merchant must be a bare public DNS hostname, without a URL, port or path.");
	const normalized = new URL(`https://${host}`).hostname.toLowerCase().replace(/^www\./, "");
	if (
		/^\d+(?:\.\d+){3}$/.test(normalized) ||
		normalized === "localhost.localdomain" ||
		/\.(?:localhost|local|internal|home|lan)$/.test(normalized)
	)
		throw new Error("Use a public merchant hostname, not an IP address or local hostname.");
	return normalized;
}

function purchaseBody(p) {
	if (!isObject(p)) throw new Error("Purchase must be a JSON object.");
	const merchant = publicHost(p.merchant);
	if (typeof p.title !== "string" || !p.title.trim() || p.title.length > 500)
		throw new Error("title must be nonempty text of at most 500 characters.");
	if (!Number.isSafeInteger(p.amountMinor) || p.amountMinor <= 0)
		throw new Error("amountMinor must be a positive safe integer in the currency's minor units.");
	if (typeof p.currency !== "string" || !CURRENCY_CODES.has(p.currency.toUpperCase()))
		throw new Error("currency must be an explicit currency code supported by Watchpost.");
	if (typeof p.isRecurring !== "boolean")
		throw new Error("isRecurring must be explicitly true or false.");
	for (const [field, max] of [
		["description", 8000],
		["rawListingHtml", 200000],
	]) {
		if (p[field] !== undefined && (typeof p[field] !== "string" || p[field].length > max))
			throw new Error(`${field} must be text of at most ${max} characters.`);
	}
	if (p.url !== undefined) {
		let url;
		try {
			url = new URL(p.url);
		} catch {
			throw new Error("url must be a valid HTTP or HTTPS URL.");
		}
		if (
			typeof p.url !== "string" ||
			!["http:", "https:"].includes(url.protocol) ||
			url.username ||
			url.password
		)
			throw new Error("url must be an HTTP or HTTPS URL without credentials.");
		const urlHost = publicHost(url.hostname);
		if (url.port || (urlHost !== merchant && !urlHost.endsWith(`.${merchant}`)))
			throw new Error(
				"url must be on the declared merchant's host or a subdomain. Use the actual listing URL, not a payment provider's checkout URL; omit it if none is available.",
			);
		if (
			url.hash ||
			[...url.searchParams.keys()].some((key) =>
				/token|password|secret|session|auth|signature|api.?key/i.test(key),
			)
		)
			throw new Error(
				"url contains a fragment or a sensitive query parameter. Supply a public listing URL without account or authentication data.",
			);
	}
	if (
		p.agent !== undefined &&
		(!isObject(p.agent) ||
			typeof p.agent.name !== "string" ||
			!p.agent.name.trim() ||
			p.agent.name.length > 64 ||
			(p.agent.runtime !== undefined &&
				(typeof p.agent.runtime !== "string" || p.agent.runtime.length > 128)))
	)
		throw new Error(
			"agent must contain a nonempty name of at most 64 characters and an optional runtime of at most 128 characters.",
		);
	return {
		agent: p.agent
			? { name: p.agent.name, runtime: p.agent.runtime }
			: { name: "watchpost-skill", runtime: "agentskills" },
		merchant: { domain: merchant },
		product: {
			title: p.title,
			url: p.url,
			description: p.description,
			rawListingHtml: p.rawListingHtml,
		},
		payment: {
			amountMinor: p.amountMinor,
			currency: p.currency.toUpperCase(),
			isRecurring: p.isRecurring,
		},
	};
}

function submittedPurchase(body) {
	return { merchant: body.merchant.domain, title: body.product.title, ...body.payment };
}

export function validatePurchase(purchase) {
	try {
		const body = purchaseBody(purchase);
		return {
			code: 0,
			output: {
				kind: "input_validation",
				submittedPurchase: submittedPurchase(body),
				message: "Input is valid locally. No Watchpost check ran and no purchase was approved.",
				networkRequests: 0,
			},
		};
	} catch (error) {
		return failure(3, "invalid_input", error.message);
	}
}

function coverageNote(c) {
	if (c === undefined)
		return "Coverage is unknown: this response does not report which listing checks ran.";
	if (!isObject(c) || c.mechanicalChecks !== true) return null;
	if (c.status === "complete" && c.reason === null && c.modelCheck === "completed")
		return "Model analysis completed on an excerpt of up to 16,000 characters. This is not a guarantee of safety.";
	if (
		c.status === "mechanical_only" &&
		c.modelCheck === "skipped" &&
		["insufficient_text", "high_risk_detected"].includes(c.reason)
	)
		return "Only mechanical listing checks ran. Model analysis was skipped; the score covers the detected signals.";
	if (
		c.status === "unavailable" &&
		c.reason === "model_unavailable" &&
		c.modelCheck === "unavailable"
	)
		return "Model analysis was unavailable. Human review is required unless another rule blocks this request.";
	return null;
}

function cleanCoverage(c) {
	return c === undefined
		? undefined
		: {
				status: c.status,
				reason: c.reason,
				mechanicalChecks: c.mechanicalChecks,
				modelCheck: c.modelCheck,
			};
}

export async function checkPurchase(purchase, token, fetchImpl = fetch) {
	let body;
	try {
		body = purchaseBody(purchase);
	} catch (error) {
		return failure(3, "invalid_input", error.message);
	}
	const result = await request(
		"/v1/verify",
		{ method: "POST", body: JSON.stringify(body) },
		token,
		fetchImpl,
	);
	if (result.code !== undefined) return result;
	const verdict = result.body;
	if (
		!isObject(verdict) ||
		verdict.error !== undefined ||
		!validId(verdict.transactionId) ||
		!["approve", "review", "block"].includes(verdict.decision) ||
		![verdict.trustScore, verdict.listingRiskScore].every(
			(n) => Number.isInteger(n) && n >= 0 && n <= 100,
		) ||
		!(verdict.category === null || typeof verdict.category === "string") ||
		!(verdict.ruleMatched === null || typeof verdict.ruleMatched === "string") ||
		(verdict.credential !== undefined && typeof verdict.credential !== "string") ||
		(verdict.reviewExpectedWithinSeconds !== undefined &&
			(!Number.isInteger(verdict.reviewExpectedWithinSeconds) ||
				verdict.reviewExpectedWithinSeconds < 0)) ||
		!Array.isArray(verdict.reasoning) ||
		verdict.reasoning.length !== 3 ||
		new Set(verdict.reasoning.map((r) => r?.pillar)).size !== 3 ||
		!verdict.reasoning.every(
			(r) =>
				isObject(r) &&
				typeof r.summary === "string" &&
				["merchant", "listing", "rules"].includes(r.pillar) &&
				["pass", "warn", "fail"].includes(r.verdict) &&
				(r.details === undefined ||
					(Array.isArray(r.details) && r.details.every((d) => typeof d === "string"))) &&
				(r.coverage === undefined || coverageNote(r.coverage) !== null),
		)
	)
		return failure(5, "invalid_response", "Watchpost returned an invalid verdict. Do not pay.");
	const note = coverageNote(verdict.listingScan);
	const nestedCoverage = verdict.reasoning.find((r) => r.pillar === "listing").coverage;
	const contradictoryCoverage =
		verdict.listingScan !== undefined &&
		nestedCoverage !== undefined &&
		JSON.stringify(cleanCoverage(verdict.listingScan)) !==
			JSON.stringify(cleanCoverage(nestedCoverage));
	if (
		!note ||
		contradictoryCoverage ||
		(verdict.decision === "approve" &&
			[verdict.listingScan, nestedCoverage].some((c) => c?.status === "unavailable"))
	)
		return failure(
			5,
			"inconsistent_coverage",
			"Watchpost returned inconsistent listing coverage. Do not pay.",
		);
	return {
		code: verdict.decision === "approve" ? 0 : verdict.decision === "review" ? 2 : 1,
		output: {
			kind: "verdict",
			transactionId: verdict.transactionId,
			decision: verdict.decision,
			trustScore: verdict.trustScore,
			listingRiskScore: verdict.listingRiskScore,
			category: verdict.category,
			ruleMatched: verdict.ruleMatched,
			listingScan: cleanCoverage(verdict.listingScan),
			reasoning: verdict.reasoning.map((r) => ({
				pillar: r.pillar,
				verdict: r.verdict,
				summary: r.summary,
				details: r.details,
				coverage: cleanCoverage(r.coverage),
			})),
			credential: verdict.credential,
			reviewExpectedWithinSeconds: verdict.reviewExpectedWithinSeconds,
			submittedPurchase: submittedPurchase(body),
			coverageNote: note,
			...(verdict.decision === "review"
				? {
						reviewUrl: `https://app.watchpost.systems/transactions?selected=${encodeURIComponent(verdict.transactionId)}`,
					}
				: {}),
		},
	};
}

export async function main(args, token) {
	try {
		const local = await localCommand(args, "check-purchase", token);
		if (local) return local;
		const validate = args[0] === "--validate";
		const purchase = await readPurchaseInput(validate ? args.slice(1) : args);
		return validate ? validatePurchase(purchase) : await checkPurchase(purchase, token);
	} catch {
		return failure(
			3,
			"invalid_input",
			"Provide valid UTF-8 JSON as one argument, standard input (-), or --file PATH. The named file must be readable, regular and at most 1,300,000 bytes. Run --help for usage.",
		);
	}
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href)
	printResult(await main(process.argv.slice(2), process.env.WATCHPOST_TOKEN));
