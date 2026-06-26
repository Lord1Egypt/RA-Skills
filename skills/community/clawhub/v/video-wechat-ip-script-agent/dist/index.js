"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.validateOpenClawSkillRequest = exports.checkCompliance = exports.rewriteStyle = exports.generateScript = exports.generateTopics = exports.createModelInvoker = exports.invokeModel = exports.getSupportedActions = exports.dispatchSkillRequest = void 0;
exports.runOpenClawSkill = runOpenClawSkill;
const modelInvoker_1 = require("./lib/modelInvoker");
Object.defineProperty(exports, "createModelInvoker", { enumerable: true, get: function () { return modelInvoker_1.createModelInvoker; } });
Object.defineProperty(exports, "invokeModel", { enumerable: true, get: function () { return modelInvoker_1.invokeModel; } });
const skillRegistry_1 = require("./lib/skillRegistry");
Object.defineProperty(exports, "dispatchSkillRequest", { enumerable: true, get: function () { return skillRegistry_1.dispatchSkillRequest; } });
Object.defineProperty(exports, "getSupportedActions", { enumerable: true, get: function () { return skillRegistry_1.getSupportedActions; } });
Object.defineProperty(exports, "validateOpenClawSkillRequest", { enumerable: true, get: function () { return skillRegistry_1.validateOpenClawSkillRequest; } });
const checkCompliance_1 = require("./services/checkCompliance");
Object.defineProperty(exports, "checkCompliance", { enumerable: true, get: function () { return checkCompliance_1.checkCompliance; } });
const generateScript_1 = require("./services/generateScript");
Object.defineProperty(exports, "generateScript", { enumerable: true, get: function () { return generateScript_1.generateScript; } });
const generateTopics_1 = require("./services/generateTopics");
Object.defineProperty(exports, "generateTopics", { enumerable: true, get: function () { return generateTopics_1.generateTopics; } });
const rewriteStyle_1 = require("./services/rewriteStyle");
Object.defineProperty(exports, "rewriteStyle", { enumerable: true, get: function () { return rewriteStyle_1.rewriteStyle; } });
async function runOpenClawSkill(request, options = {}) {
    const validatedRequest = (0, skillRegistry_1.validateOpenClawSkillRequest)(request);
    const modelInvoker = options.invoker ?? (0, modelInvoker_1.createModelInvoker)(options);
    return (0, skillRegistry_1.dispatchSkillRequest)(validatedRequest, modelInvoker);
}
