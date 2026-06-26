/**
 * Generate a fresh Stellar keypair for an agent wallet.
 *
 * Usage:
 *   npx tsx scripts/generate-keypair.ts                   # write to ./.stellar-secret
 *   npx tsx scripts/generate-keypair.ts --out wallet.key  # custom path
 * Existing wallet files are never overwritten. Pick a new --out path if
 * you need another wallet.
 *
 * The generated secret is NEVER printed to the terminal. It is written
 * directly to a file with mode 600 so it can only be read by the current
 * user. The terminal only sees the public key.
 *
 * Use the resulting file with the --secret-file flag on any command:
 *   npx tsx skills/check-balance/run.ts --secret-file .stellar-secret
 */

import { Keypair } from "@stellar/stellar-sdk";
import * as fs from "node:fs";
import * as path from "node:path";

const DEFAULT_OUT = ".stellar-secret";

function parseArgs() {
  const argv = process.argv.slice(2);
  let out = DEFAULT_OUT;
  for (let i = 0; i < argv.length; i++) {
    if (argv[i] === "--out") out = argv[++i];
    else if (argv[i] === "--force" || argv[i] === "-f") {
      console.error("❌ --force is disabled. Wallet files are never overwritten.");
      console.error("   Use --out <new-file> to create a separate wallet.");
      process.exit(1);
    }
  }
  return { out };
}

function main() {
  const { out } = parseArgs();
  const outPath = path.resolve(process.cwd(), out);

  if (fs.existsSync(outPath)) {
    console.error(
      `❌ ${out} already exists. Refusing to overwrite an existing wallet.`,
    );
    console.error(`   If you want a fresh keypair in a different file:`);
    console.error(`     npx tsx scripts/generate-keypair.ts --out stellar.key`);
    process.exit(1);
  }

  const kp = Keypair.random();
  const pubkey = kp.publicKey();
  const secret = kp.secret();

  // The secret file format is intentionally bare: one line containing
  // just the S... strkey. loadSecretFromFile in scripts/src/secret.ts
  // also accepts leading comment lines, so we include a header noting
  // that this file is sensitive.
  const body =
    "# Stellar wallet secret — DO NOT COMMIT. chmod 600.\n" +
    secret +
    "\n";

  // Write with mode 600 (owner read/write only).
  const fd = fs.openSync(outPath, "w", 0o600);
  try {
    fs.writeSync(fd, body);
  } finally {
    fs.closeSync(fd);
  }
  // Secret string goes out of scope when this function returns.

  console.log("✅ Stellar keypair generated.");
  console.log(`   Public key:    ${pubkey}`);
  console.log(`   Secret stored: ${outPath}  (mode 600)`);
  console.log("");
  console.log("The secret was NOT printed. To use it with any command, pass:");
  console.log(`   --secret-file ${out}`);
  console.log("");
  console.log("Next steps:");
  console.log(`  1. (testnet only) Fund the account:`);
  console.log(`     curl 'https://friendbot.stellar.org?addr=${pubkey}'`);
  console.log(`  2. Check the balance:`);
  console.log(
    `     npx tsx skills/check-balance/run.ts ${pubkey}`,
  );
}

main();
