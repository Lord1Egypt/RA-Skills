"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const cli_1 = require("../lib/cli");
const recognizeFuzzyProductSearch_1 = require("../recognizeFuzzyProductSearch");
const common_1 = require("../common");
async function main() {
    const argv = process.argv.slice(2);
    (0, common_1.printJson)(await (0, recognizeFuzzyProductSearch_1.recognizeRawMessage)((0, cli_1.requireOption)(argv, "raw-message")));
    return 0;
}
main().then((code) => process.exit(code), (error) => {
    console.error(error instanceof Error ? error.message : String(error));
    process.exit(1);
});
