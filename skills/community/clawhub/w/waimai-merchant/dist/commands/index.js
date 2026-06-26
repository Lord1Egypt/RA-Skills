"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.registerCommands = registerCommands;
const merchant_1 = require("./merchant");
const product_1 = require("./product");
function registerCommands(program) {
    program.addCommand((0, merchant_1.createMerchantCommands)());
    program.addCommand((0, product_1.createProductCommands)());
}
//# sourceMappingURL=index.js.map