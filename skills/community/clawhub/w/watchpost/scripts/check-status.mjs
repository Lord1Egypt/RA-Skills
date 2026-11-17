#!/usr/bin/env node
import { pathToFileURL } from "node:url";
import { localCommand } from "./cli.mjs";
import { failure, isObject, printResult, request, validId } from "./watchpost-client.mjs";

export async function checkStatus(transactionId, token, fetchImpl = fetch) {
	if (!validId(transactionId))
		return failure(3, "invalid_input", "Pass the transactionId from the original review result.");
	const result = await request(
		`/v1/transactions/${transactionId}/status`,
		{ method: "GET" },
		token,
		fetchImpl,
	);
	if (result.code !== undefined) return result;
	const body = result.body;
	if (
		!isObject(body) ||
		body.error !== undefined ||
		body.transactionId !== transactionId ||
		body.decision !== "review" ||
		typeof body.outcome !== "string"
	)
		return failure(
			5,
			"invalid_response",
			"Watchpost did not return the requested review. Do not pay.",
		);
	const states = {
		PENDING: ["pending", false, 2],
		USER_APPROVED: ["approved", true, 0],
		USER_BLOCKED: ["blocked", true, 1],
		FAILED: ["blocked", true, 1],
		DISPUTED: ["blocked", true, 1],
		EXPIRED: ["expired", true, 1],
		COMPLETED: ["approved", true, 6],
	};
	const expected = Object.hasOwn(states, body.outcome) ? states[body.outcome] : undefined;
	if (!expected || body.status !== expected[0] || body.resolved !== expected[1])
		return failure(
			5,
			"invalid_response",
			"Watchpost returned an inconsistent review status. Do not pay.",
		);
	return {
		code: expected[2],
		output: {
			kind: "review_status",
			transactionId: body.transactionId,
			decision: body.decision,
			outcome: body.outcome,
			status: body.status,
			resolved: body.resolved,
			reviewUrl: `https://app.watchpost.systems/transactions?selected=${encodeURIComponent(transactionId)}`,
			...(expected[2] === 2 ? { nextCheckAfterSeconds: 3 } : {}),
			message:
				expected[2] === 0
					? "The user approved this review in Watchpost. This applies only to the original unchanged purchase and does not authorize a duplicate payment."
					: expected[2] === 6
						? "This purchase is already recorded as completed. Do not pay again."
						: "Do not pay. The review is pending, declined, expired or otherwise closed.",
		},
	};
}

export async function main(args, token) {
	try {
		return (
			(await localCommand(args, "check-status", token)) ??
			(args.length === 1
				? await checkStatus(args[0], token)
				: failure(
						3,
						"invalid_input",
						"Pass exactly one transactionId from the original review result, or --help.",
					))
		);
	} catch {
		return failure(
			3,
			"invalid_installation",
			"Could not read the installed skill. Reinstall it before retrying.",
		);
	}
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href)
	printResult(await main(process.argv.slice(2), process.env.WATCHPOST_TOKEN));
