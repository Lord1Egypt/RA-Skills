"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const cli_1 = require("../lib/cli");
const m01OperationGuide_1 = require("../m01OperationGuide");
async function main() {
    const argv = process.argv.slice(2);
    return await (0, m01OperationGuide_1.emitAction)((0, cli_1.requireOption)(argv, "action"), (0, cli_1.parseOutputFormat)(argv, "md"), (0, cli_1.getOption)(argv, "raw-message") || "");
}
main().then((code) => process.exit(code), (error) => {
    console.error(error instanceof Error ? error.message : String(error));
    process.exit(1);
});
