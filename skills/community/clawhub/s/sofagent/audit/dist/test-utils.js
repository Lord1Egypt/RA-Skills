"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.makeDiffFile = makeDiffFile;
exports.makeCtx = makeCtx;
function makeDiffFile(path, lines = [], status = 'modified') {
    return { path, status, lines };
}
function makeCtx(diffFiles, overrides = {}) {
    return { diffFiles, logEntries: [], ...overrides };
}
//# sourceMappingURL=test-utils.js.map