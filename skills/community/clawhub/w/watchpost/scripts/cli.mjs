import { open, readFile } from "node:fs/promises";
import { failure, validToken } from "./watchpost-client.mjs";

export const MAX_INPUT_BYTES = 1300000;

export async function localCommand(args, command, token) {
	if (args.length !== 1) return undefined;
	if (args[0] === "--version") {
		const text = await readFile(new URL("../SKILL.md", import.meta.url), "utf8");
		const version = text.match(/^ {2}version: "([0-9]+\.[0-9]+\.[0-9]+)"$/m)?.[1];
		return version
			? { code: 0, output: { kind: "version", version } }
			: failure(
					3,
					"invalid_installation",
					"Skill version metadata is missing. Reinstall the skill.",
				);
	}
	if (args[0] === "--doctor") {
		const runtimeOk = Number(process.versions.node.split(".")[0]) >= 20;
		const tokenPresent = typeof token === "string" && token.length > 0;
		return {
			code: runtimeOk && validToken(token) ? 0 : 3,
			output: {
				kind: "local_diagnostic",
				nodeVersion: process.versions.node,
				runtimeOk,
				token: !tokenPresent ? "missing" : validToken(token) ? "format_accepted" : "invalid_format",
				connectionVerified: false,
				networkRequests: 0,
				message:
					"This checks local setup only. It does not verify token validity, connectivity or purchase approval.",
				setupUrl: "https://app.watchpost.systems/connections",
			},
		};
	}
	if (args[0] === "--help" || args[0] === "-h")
		return {
			code: 0,
			output: {
				kind: "help",
				command,
				usage:
					command === "check-purchase"
						? [
								"node check-purchase.mjs --file purchase.json",
								"node check-purchase.mjs --validate --file purchase.json",
								"node check-purchase.mjs '<JSON>'",
								"node check-purchase.mjs -",
							]
						: ["node check-status.mjs TRANSACTION_ID"],
				localOptions: ["--help", "--version", "--doctor"],
				exitCodes: {
					0: "Read kind: approval, local validation, help and diagnostics differ.",
					1: "blocked or declined",
					2: "review or pending",
					3: "input/setup error",
					4: "plan limit",
					5: "unconfirmed request/response",
					6: "already completed",
				},
				message:
					"Run from the installed skill's scripts directory or use an absolute script path. Local commands make no network requests and grant no approval.",
			},
		};
	return undefined;
}

export async function readPurchaseInput(args) {
	let raw;
	if (args.length === 2 && args[0] === "--file") {
		let handle;
		try {
			handle = await open(args[1], "r");
			const info = await handle.stat();
			if (!info.isFile() || info.size > MAX_INPUT_BYTES) throw new Error("invalid file");
			// Read at most the limit plus one byte, even if the file grows after stat.
			const buffer = Buffer.alloc(MAX_INPUT_BYTES + 1);
			let offset = 0;
			while (offset < buffer.length) {
				const { bytesRead } = await handle.read(buffer, offset, buffer.length - offset, null);
				if (!bytesRead) break;
				offset += bytesRead;
			}
			if (offset > MAX_INPUT_BYTES) throw new Error("file too large");
			raw = new TextDecoder("utf-8", { fatal: true }).decode(buffer.subarray(0, offset));
		} finally {
			await handle?.close();
		}
	} else if (args.length === 1 && args[0] === "-") {
		const chunks = [];
		let size = 0;
		for await (const chunk of process.stdin) {
			size += Buffer.byteLength(chunk);
			if (size > MAX_INPUT_BYTES) throw new Error("input too large");
			chunks.push(Buffer.from(chunk));
		}
		raw = new TextDecoder("utf-8", { fatal: true }).decode(Buffer.concat(chunks));
	} else if (args.length === 1 && !args[0].startsWith("--")) raw = args[0];
	else throw new Error("invalid arguments");
	if (Buffer.byteLength(raw) > MAX_INPUT_BYTES) throw new Error("input too large");
	return JSON.parse(raw.replace(/^\uFEFF/, ""));
}
