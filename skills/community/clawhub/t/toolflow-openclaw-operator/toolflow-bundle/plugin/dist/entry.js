"use strict";
var __getOwnPropNames = Object.getOwnPropertyNames;
var __commonJS = (cb, mod) => function __require() {
  return mod || (0, cb[__getOwnPropNames(cb)[0]])((mod = { exports: {} }).exports, mod), mod.exports;
};

// packages/shared/dist/constants.js
var require_constants = __commonJS({
  "packages/shared/dist/constants.js"(exports2) {
    "use strict";
    Object.defineProperty(exports2, "__esModule", { value: true });
    exports2.TOOLFLOW_ACTIONS = exports2.TOOLFLOW_CELLS = exports2.ELEVATED_PROFILE_ACTIONS = exports2.ELEVATED_PROFILE_CELLS = exports2.SAFE_PROFILE_ACTIONS = exports2.SAFE_PROFILE_CELLS = exports2.RUN_MANIFEST_SCHEMA_VERSION = exports2.RECEIPT_SCHEMA_VERSION = exports2.STEP_GRANT_SCHEMA_VERSION = exports2.POLICY_ARTIFACT_SCHEMA_VERSION = exports2.PROOF_BUNDLE_SCHEMA_VERSION = exports2.COMPILED_GRAPH_SCHEMA_VERSION = exports2.WORKFLOW_SCHEMA_VERSION = exports2.TOOLFLOW_VERSION = void 0;
    exports2.TOOLFLOW_VERSION = "toolflow/v5";
    exports2.WORKFLOW_SCHEMA_VERSION = "toolflow.workflow/v1";
    exports2.COMPILED_GRAPH_SCHEMA_VERSION = "toolflow.compiled-graph/v1";
    exports2.PROOF_BUNDLE_SCHEMA_VERSION = "toolflow.proof-bundle/v1";
    exports2.POLICY_ARTIFACT_SCHEMA_VERSION = "toolflow.policy-artifact/v1";
    exports2.STEP_GRANT_SCHEMA_VERSION = "toolflow.step-grant/v1";
    exports2.RECEIPT_SCHEMA_VERSION = "toolflow.receipt/v1";
    exports2.RUN_MANIFEST_SCHEMA_VERSION = "toolflow.run-manifest/v1";
    exports2.SAFE_PROFILE_CELLS = ["read", "research", "session"];
    exports2.SAFE_PROFILE_ACTIONS = ["read_file", "list_files", "research_note", "session_note"];
    exports2.ELEVATED_PROFILE_CELLS = ["elevated"];
    exports2.ELEVATED_PROFILE_ACTIONS = ["exec_command", "apply_patch"];
    exports2.TOOLFLOW_CELLS = [...exports2.SAFE_PROFILE_CELLS, ...exports2.ELEVATED_PROFILE_CELLS];
    exports2.TOOLFLOW_ACTIONS = [...exports2.SAFE_PROFILE_ACTIONS, ...exports2.ELEVATED_PROFILE_ACTIONS];
  }
});

// packages/shared/dist/errors.js
var require_errors = __commonJS({
  "packages/shared/dist/errors.js"(exports2) {
    "use strict";
    Object.defineProperty(exports2, "__esModule", { value: true });
    exports2.PolicyError = exports2.ValidationError = exports2.ToolFlowError = void 0;
    var ToolFlowError = class extends Error {
      code;
      constructor(message, code = "TOOLFLOW_ERROR") {
        super(message);
        this.code = code;
        this.name = "ToolFlowError";
      }
    };
    exports2.ToolFlowError = ToolFlowError;
    var ValidationError = class extends ToolFlowError {
      constructor(message) {
        super(message, "VALIDATION_ERROR");
      }
    };
    exports2.ValidationError = ValidationError;
    var PolicyError = class extends ToolFlowError {
      constructor(message) {
        super(message, "POLICY_ERROR");
      }
    };
    exports2.PolicyError = PolicyError;
  }
});

// packages/shared/dist/hashing.js
var require_hashing = __commonJS({
  "packages/shared/dist/hashing.js"(exports2) {
    "use strict";
    Object.defineProperty(exports2, "__esModule", { value: true });
    exports2.canonicalJson = canonicalJson;
    exports2.sha256 = sha256;
    exports2.hashJson = hashJson;
    var node_crypto_1 = require("node:crypto");
    function canonicalJson(value) {
      return JSON.stringify(sortForJson(value));
    }
    function sha256(value) {
      return `sha256:${(0, node_crypto_1.createHash)("sha256").update(value).digest("hex")}`;
    }
    function hashJson(value) {
      return sha256(canonicalJson(value));
    }
    function sortForJson(value) {
      if (Array.isArray(value))
        return value.map(sortForJson);
      if (value && typeof value === "object" && Object.getPrototypeOf(value) === Object.prototype) {
        const sorted = {};
        for (const key of Object.keys(value).sort()) {
          const entry = value[key];
          if (entry !== void 0)
            sorted[key] = sortForJson(entry);
        }
        return sorted;
      }
      return value;
    }
  }
});

// packages/shared/dist/ids.js
var require_ids = __commonJS({
  "packages/shared/dist/ids.js"(exports2) {
    "use strict";
    Object.defineProperty(exports2, "__esModule", { value: true });
    exports2.newRunId = newRunId;
    exports2.newGrantId = newGrantId;
    exports2.newReceiptId = newReceiptId;
    exports2.newArtifactId = newArtifactId;
    exports2.normalizeStepId = normalizeStepId;
    var node_crypto_1 = require("node:crypto");
    var hashing_1 = require_hashing();
    function newRunId(seed) {
      return `run_${token(seed)}`;
    }
    function newGrantId(seed) {
      return `sg_${token(seed)}`;
    }
    function newReceiptId(seed) {
      return `rcpt_${token(seed)}`;
    }
    function newArtifactId(seed) {
      return `art_${token(seed)}`;
    }
    function normalizeStepId(id) {
      if (!/^[A-Za-z0-9][A-Za-z0-9_-]{0,63}$/.test(id)) {
        throw new Error(`Invalid step id "${id}". Use 1-64 alphanumeric, dash, or underscore characters.`);
      }
      return id;
    }
    function token(seed) {
      if (seed)
        return (0, hashing_1.sha256)(seed).slice("sha256:".length, "sha256:".length + 16);
      return (0, node_crypto_1.randomBytes)(8).toString("hex");
    }
  }
});

// packages/shared/dist/schemas/helpers.js
var require_helpers = __commonJS({
  "packages/shared/dist/schemas/helpers.js"(exports2) {
    "use strict";
    Object.defineProperty(exports2, "__esModule", { value: true });
    exports2.isRecord = isRecord;
    exports2.hasString = hasString;
    exports2.hasObject = hasObject;
    exports2.hasArray = hasArray;
    function isRecord(value) {
      return typeof value === "object" && value !== null && !Array.isArray(value);
    }
    function hasString(value, key) {
      return typeof value[key] === "string" && value[key].length > 0;
    }
    function hasObject(value, key) {
      return isRecord(value[key]);
    }
    function hasArray(value, key) {
      return Array.isArray(value[key]);
    }
  }
});

// packages/shared/dist/schemas/approval-binding.js
var require_approval_binding = __commonJS({
  "packages/shared/dist/schemas/approval-binding.js"(exports2) {
    "use strict";
    Object.defineProperty(exports2, "__esModule", { value: true });
    exports2.isApprovalBinding = isApprovalBinding;
    var helpers_1 = require_helpers();
    function isApprovalBinding(value) {
      return (0, helpers_1.isRecord)(value) && value.schemaVersion === "toolflow.approval-binding/v1" && (0, helpers_1.hasString)(value, "runId") && (0, helpers_1.hasString)(value, "stepId") && (0, helpers_1.hasString)(value, "approvalHash");
    }
  }
});

// packages/shared/dist/schemas/checkpoint.js
var require_checkpoint = __commonJS({
  "packages/shared/dist/schemas/checkpoint.js"(exports2) {
    "use strict";
    Object.defineProperty(exports2, "__esModule", { value: true });
    exports2.isCheckpointRecord = isCheckpointRecord;
    function isCheckpointRecord(value) {
      return typeof value === "object" && value !== null && typeof value.runId === "string" && typeof value.stepId === "string" && typeof value.at === "string" && typeof value.state === "string";
    }
  }
});

// packages/shared/dist/schemas/compiled-graph.js
var require_compiled_graph = __commonJS({
  "packages/shared/dist/schemas/compiled-graph.js"(exports2) {
    "use strict";
    Object.defineProperty(exports2, "__esModule", { value: true });
    exports2.isCompiledGraph = isCompiledGraph;
    var helpers_1 = require_helpers();
    function isCompiledGraph(value) {
      return (0, helpers_1.isRecord)(value) && value.schemaVersion === "toolflow.compiled-graph/v1" && (0, helpers_1.hasString)(value, "workflowName") && (0, helpers_1.hasString)(value, "graphHash") && (0, helpers_1.hasArray)(value, "nodes");
    }
  }
});

// packages/shared/dist/schemas/policy-artifact.js
var require_policy_artifact = __commonJS({
  "packages/shared/dist/schemas/policy-artifact.js"(exports2) {
    "use strict";
    Object.defineProperty(exports2, "__esModule", { value: true });
    exports2.isPolicyArtifact = isPolicyArtifact;
    var helpers_1 = require_helpers();
    function isPolicyArtifact(value) {
      return (0, helpers_1.isRecord)(value) && value.schemaVersion === "toolflow.policy-artifact/v1" && (0, helpers_1.hasString)(value, "policyHash") && (0, helpers_1.hasArray)(value, "allowedCells") && (0, helpers_1.hasString)(value, "bridgeMode");
    }
  }
});

// packages/shared/dist/schemas/proof-bundle.js
var require_proof_bundle = __commonJS({
  "packages/shared/dist/schemas/proof-bundle.js"(exports2) {
    "use strict";
    Object.defineProperty(exports2, "__esModule", { value: true });
    exports2.isProofBundle = isProofBundle;
    var helpers_1 = require_helpers();
    function isProofBundle(value) {
      return (0, helpers_1.isRecord)(value) && value.schemaVersion === "toolflow.proof-bundle/v1" && (0, helpers_1.hasString)(value, "workflowName") && (0, helpers_1.hasArray)(value, "warnings") && (0, helpers_1.hasArray)(value, "objectiveFailures") && (0, helpers_1.hasObject)(value, "estimates");
    }
  }
});

// packages/shared/dist/schemas/receipt.js
var require_receipt = __commonJS({
  "packages/shared/dist/schemas/receipt.js"(exports2) {
    "use strict";
    Object.defineProperty(exports2, "__esModule", { value: true });
    exports2.isReceipt = isReceipt;
    var helpers_1 = require_helpers();
    function isReceipt(value) {
      return (0, helpers_1.isRecord)(value) && value.schemaVersion === "toolflow.receipt/v1" && (0, helpers_1.hasString)(value, "receiptId") && (0, helpers_1.hasString)(value, "grantId") && (0, helpers_1.hasString)(value, "signature");
    }
  }
});

// packages/shared/dist/schemas/run-manifest.js
var require_run_manifest = __commonJS({
  "packages/shared/dist/schemas/run-manifest.js"(exports2) {
    "use strict";
    Object.defineProperty(exports2, "__esModule", { value: true });
    exports2.isRunManifest = isRunManifest;
    var helpers_1 = require_helpers();
    function isRunManifest(value) {
      return (0, helpers_1.isRecord)(value) && value.schemaVersion === "toolflow.run-manifest/v1" && (0, helpers_1.hasString)(value, "runId") && (0, helpers_1.hasString)(value, "workflowName") && (0, helpers_1.hasObject)(value, "steps");
    }
  }
});

// packages/shared/dist/schemas/step-grant.js
var require_step_grant = __commonJS({
  "packages/shared/dist/schemas/step-grant.js"(exports2) {
    "use strict";
    Object.defineProperty(exports2, "__esModule", { value: true });
    exports2.isStepGrant = isStepGrant;
    var helpers_1 = require_helpers();
    function isStepGrant(value) {
      return (0, helpers_1.isRecord)(value) && value.schemaVersion === "toolflow.step-grant/v1" && (0, helpers_1.hasString)(value, "grantId") && (0, helpers_1.hasString)(value, "runId") && (0, helpers_1.hasString)(value, "signature");
    }
  }
});

// packages/shared/dist/schemas/workflow.js
var require_workflow = __commonJS({
  "packages/shared/dist/schemas/workflow.js"(exports2) {
    "use strict";
    Object.defineProperty(exports2, "__esModule", { value: true });
    exports2.isWorkflowSource = isWorkflowSource;
    var helpers_1 = require_helpers();
    function isWorkflowSource(value) {
      return (0, helpers_1.isRecord)(value) && value.schemaVersion === "toolflow.workflow/v1" && (0, helpers_1.hasString)(value, "name") && (0, helpers_1.hasArray)(value, "steps");
    }
  }
});

// packages/shared/dist/time.js
var require_time = __commonJS({
  "packages/shared/dist/time.js"(exports2) {
    "use strict";
    Object.defineProperty(exports2, "__esModule", { value: true });
    exports2.nowIso = nowIso;
    exports2.secondsFromNow = secondsFromNow;
    exports2.isExpired = isExpired;
    function nowIso() {
      return (/* @__PURE__ */ new Date()).toISOString();
    }
    function secondsFromNow(seconds) {
      return new Date(Date.now() + seconds * 1e3).toISOString();
    }
    function isExpired(iso, at = /* @__PURE__ */ new Date()) {
      return new Date(iso).getTime() <= at.getTime();
    }
  }
});

// packages/shared/dist/types/approvals.js
var require_approvals = __commonJS({
  "packages/shared/dist/types/approvals.js"(exports2) {
    "use strict";
    Object.defineProperty(exports2, "__esModule", { value: true });
  }
});

// packages/shared/dist/types/bridges.js
var require_bridges = __commonJS({
  "packages/shared/dist/types/bridges.js"(exports2) {
    "use strict";
    Object.defineProperty(exports2, "__esModule", { value: true });
  }
});

// packages/shared/dist/types/classifier.js
var require_classifier = __commonJS({
  "packages/shared/dist/types/classifier.js"(exports2) {
    "use strict";
    Object.defineProperty(exports2, "__esModule", { value: true });
  }
});

// packages/shared/dist/types/compiler.js
var require_compiler = __commonJS({
  "packages/shared/dist/types/compiler.js"(exports2) {
    "use strict";
    Object.defineProperty(exports2, "__esModule", { value: true });
  }
});

// packages/shared/dist/types/grants.js
var require_grants = __commonJS({
  "packages/shared/dist/types/grants.js"(exports2) {
    "use strict";
    Object.defineProperty(exports2, "__esModule", { value: true });
  }
});

// packages/shared/dist/types/ledger.js
var require_ledger = __commonJS({
  "packages/shared/dist/types/ledger.js"(exports2) {
    "use strict";
    Object.defineProperty(exports2, "__esModule", { value: true });
  }
});

// packages/shared/dist/types/receipts.js
var require_receipts = __commonJS({
  "packages/shared/dist/types/receipts.js"(exports2) {
    "use strict";
    Object.defineProperty(exports2, "__esModule", { value: true });
  }
});

// packages/shared/dist/types/replay.js
var require_replay = __commonJS({
  "packages/shared/dist/types/replay.js"(exports2) {
    "use strict";
    Object.defineProperty(exports2, "__esModule", { value: true });
  }
});

// packages/shared/dist/types/workflow.js
var require_workflow2 = __commonJS({
  "packages/shared/dist/types/workflow.js"(exports2) {
    "use strict";
    Object.defineProperty(exports2, "__esModule", { value: true });
  }
});

// packages/shared/dist/index.js
var require_dist = __commonJS({
  "packages/shared/dist/index.js"(exports2) {
    "use strict";
    var __createBinding2 = exports2 && exports2.__createBinding || (Object.create ? (function(o, m, k, k2) {
      if (k2 === void 0) k2 = k;
      var desc = Object.getOwnPropertyDescriptor(m, k);
      if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
        desc = { enumerable: true, get: function() {
          return m[k];
        } };
      }
      Object.defineProperty(o, k2, desc);
    }) : (function(o, m, k, k2) {
      if (k2 === void 0) k2 = k;
      o[k2] = m[k];
    }));
    var __exportStar2 = exports2 && exports2.__exportStar || function(m, exports3) {
      for (var p in m) if (p !== "default" && !Object.prototype.hasOwnProperty.call(exports3, p)) __createBinding2(exports3, m, p);
    };
    Object.defineProperty(exports2, "__esModule", { value: true });
    __exportStar2(require_constants(), exports2);
    __exportStar2(require_errors(), exports2);
    __exportStar2(require_hashing(), exports2);
    __exportStar2(require_ids(), exports2);
    __exportStar2(require_approval_binding(), exports2);
    __exportStar2(require_checkpoint(), exports2);
    __exportStar2(require_compiled_graph(), exports2);
    __exportStar2(require_policy_artifact(), exports2);
    __exportStar2(require_proof_bundle(), exports2);
    __exportStar2(require_receipt(), exports2);
    __exportStar2(require_run_manifest(), exports2);
    __exportStar2(require_step_grant(), exports2);
    __exportStar2(require_workflow(), exports2);
    __exportStar2(require_time(), exports2);
    __exportStar2(require_approvals(), exports2);
    __exportStar2(require_bridges(), exports2);
    __exportStar2(require_classifier(), exports2);
    __exportStar2(require_compiler(), exports2);
    __exportStar2(require_grants(), exports2);
    __exportStar2(require_ledger(), exports2);
    __exportStar2(require_receipts(), exports2);
    __exportStar2(require_replay(), exports2);
    __exportStar2(require_workflow2(), exports2);
  }
});

// packages/runtime/dist/crypto/keyring.js
var require_keyring = __commonJS({
  "packages/runtime/dist/crypto/keyring.js"(exports2) {
    "use strict";
    Object.defineProperty(exports2, "__esModule", { value: true });
    exports2.loadRuntimeKey = loadRuntimeKey;
    exports2.loadElevatedRuntimeKey = loadElevatedRuntimeKey;
    var node_fs_1 = require("node:fs");
    var node_path_1 = require("node:path");
    var node_crypto_1 = require("node:crypto");
    function loadRuntimeKey(ledgerRoot) {
      return loadKey(ledgerRoot, "ordinary-dev-key.json", "ordinary-dev-local");
    }
    function loadElevatedRuntimeKey(ledgerRoot) {
      return loadKey(ledgerRoot, "elevated-dev-key.json", "elevated-dev-local");
    }
    function loadKey(ledgerRoot, filename, defaultKeyId) {
      const keyPath = (0, node_path_1.join)(ledgerRoot, "keys", filename);
      try {
        return JSON.parse((0, node_fs_1.readFileSync)(keyPath, "utf8"));
      } catch {
        (0, node_fs_1.mkdirSync)((0, node_path_1.dirname)(keyPath), { recursive: true, mode: 448 });
        const key = { keyId: defaultKeyId, secret: (0, node_crypto_1.randomBytes)(32).toString("hex") };
        (0, node_fs_1.writeFileSync)(keyPath, JSON.stringify(key, null, 2), { mode: 384 });
        return key;
      }
    }
  }
});

// packages/runtime/dist/compiler/build-graph.js
var require_build_graph = __commonJS({
  "packages/runtime/dist/compiler/build-graph.js"(exports2) {
    "use strict";
    Object.defineProperty(exports2, "__esModule", { value: true });
    exports2.buildGraph = buildGraph;
    var shared_1 = require_dist();
    function buildGraph(source) {
      const ids = new Set(source.steps.map((step) => step.id));
      for (const step of source.steps) {
        for (const dep of step.dependsOn ?? []) {
          if (!ids.has(dep))
            throw new shared_1.ValidationError(`Step "${step.id}" depends on unknown step "${dep}".`);
        }
      }
      detectCycles(source);
      const sourceHash = (0, shared_1.hashJson)(source);
      const nodes = source.steps.map((step) => {
        const cell = step.cell;
        const payload = step.args ?? {};
        return { id: step.id, cell, bridgeId: `${cell}-bridge-v1`, action: step.action, dependsOn: step.dependsOn ?? [], payload, payloadHash: (0, shared_1.hashJson)(payload), replayClass: step.replayClass ?? "idempotent" };
      });
      const graphWithoutHash = { schemaVersion: shared_1.COMPILED_GRAPH_SCHEMA_VERSION, workflowName: source.name, sourceHash, nodes };
      return { ...graphWithoutHash, graphHash: (0, shared_1.hashJson)(graphWithoutHash) };
    }
    function detectCycles(source) {
      const deps = new Map(source.steps.map((step) => [step.id, step.dependsOn ?? []]));
      const visiting = /* @__PURE__ */ new Set();
      const visited = /* @__PURE__ */ new Set();
      const visit = (id) => {
        if (visited.has(id))
          return;
        if (visiting.has(id))
          throw new shared_1.ValidationError(`Dependency cycle detected at "${id}".`);
        visiting.add(id);
        for (const dep of deps.get(id) ?? [])
          visit(dep);
        visiting.delete(id);
        visited.add(id);
      };
      for (const step of source.steps)
        visit(step.id);
    }
  }
});

// packages/runtime/dist/compiler/normalize-workflow.js
var require_normalize_workflow = __commonJS({
  "packages/runtime/dist/compiler/normalize-workflow.js"(exports2) {
    "use strict";
    Object.defineProperty(exports2, "__esModule", { value: true });
    exports2.normalizeWorkflow = normalizeWorkflow;
    exports2.inferCell = inferCell;
    var shared_1 = require_dist();
    function normalizeWorkflow(source) {
      if (source.schemaVersion !== "toolflow.workflow/v1")
        throw new shared_1.ValidationError("Unsupported workflow schemaVersion.");
      if (!source.name || typeof source.name !== "string")
        throw new shared_1.ValidationError("Workflow name is required.");
      if (!Array.isArray(source.steps) || source.steps.length === 0)
        throw new shared_1.ValidationError("Workflow must include at least one step.");
      const seen = /* @__PURE__ */ new Set();
      return { ...source, steps: source.steps.map((step) => normalizeStep(step, seen)) };
    }
    function normalizeStep(step, seen) {
      const id = (0, shared_1.normalizeStepId)(step.id);
      if (seen.has(id))
        throw new shared_1.ValidationError(`Duplicate step id "${id}".`);
      seen.add(id);
      if (!shared_1.TOOLFLOW_ACTIONS.includes(step.action))
        throw new shared_1.ValidationError(`Action "${String(step.action)}" is not supported by ToolFlow.`);
      const cell = step.cell ?? inferCell(step.action);
      if (!shared_1.TOOLFLOW_CELLS.includes(cell))
        throw new shared_1.ValidationError(`Cell "${String(cell)}" is not supported by ToolFlow.`);
      const replayClass = step.replayClass ?? (cell === "read" ? "read_only" : cell === "elevated" ? "review_before_replay" : "idempotent");
      return { id, action: step.action, cell, dependsOn: step.dependsOn ?? [], args: step.args ?? {}, replayClass };
    }
    function inferCell(action) {
      if (action === "read_file" || action === "list_files")
        return "read";
      if (action === "research_note")
        return "research";
      if (action === "session_note")
        return "session";
      return "elevated";
    }
  }
});

// packages/runtime/dist/compiler/parse-workflow.js
var require_parse_workflow = __commonJS({
  "packages/runtime/dist/compiler/parse-workflow.js"(exports2) {
    "use strict";
    Object.defineProperty(exports2, "__esModule", { value: true });
    exports2.parseWorkflowFile = parseWorkflowFile;
    exports2.parseWorkflowJson = parseWorkflowJson;
    var node_fs_1 = require("node:fs");
    var shared_1 = require_dist();
    function parseWorkflowFile(path) {
      if (!path.endsWith(".json"))
        throw new shared_1.ValidationError("Safe Profile MVP accepts JSON workflow files only.");
      return parseWorkflowJson((0, node_fs_1.readFileSync)(path, "utf8"));
    }
    function parseWorkflowJson(raw) {
      try {
        return JSON.parse(raw);
      } catch (error) {
        throw new shared_1.ValidationError(`Workflow JSON parse failed: ${error.message}`);
      }
    }
  }
});

// packages/runtime/dist/compiler/resolve-variables.js
var require_resolve_variables = __commonJS({
  "packages/runtime/dist/compiler/resolve-variables.js"(exports2) {
    "use strict";
    Object.defineProperty(exports2, "__esModule", { value: true });
    exports2.resolveVariables = resolveVariables;
    var shared_1 = require_dist();
    function resolveVariables(source) {
      const inputs = source.inputs ?? {};
      return { ...source, steps: source.steps.map((step) => ({ ...step, args: resolveValue(step.args ?? {}, inputs) })) };
    }
    function resolveValue(value, inputs) {
      if (typeof value === "string") {
        return value.replace(/\$\{inputs\.([A-Za-z0-9_-]+)\}/g, (_match, key) => {
          if (!(key in inputs))
            throw new shared_1.ValidationError(`Unresolved input reference "${key}".`);
          return String(inputs[key]);
        });
      }
      if (Array.isArray(value))
        return value.map((entry) => resolveValue(entry, inputs));
      if (value && typeof value === "object")
        return Object.fromEntries(Object.entries(value).map(([key, entry]) => [key, resolveValue(entry, inputs)]));
      return value;
    }
  }
});

// packages/runtime/dist/compiler/compile.js
var require_compile = __commonJS({
  "packages/runtime/dist/compiler/compile.js"(exports2) {
    "use strict";
    Object.defineProperty(exports2, "__esModule", { value: true });
    exports2.compileWorkflowFile = compileWorkflowFile;
    exports2.compileWorkflow = compileWorkflow;
    var build_graph_1 = require_build_graph();
    var normalize_workflow_1 = require_normalize_workflow();
    var parse_workflow_1 = require_parse_workflow();
    var resolve_variables_1 = require_resolve_variables();
    function compileWorkflowFile(path) {
      return compileWorkflow((0, parse_workflow_1.parseWorkflowFile)(path));
    }
    function compileWorkflow(source) {
      const normalized = (0, normalize_workflow_1.normalizeWorkflow)(source);
      const resolved = (0, resolve_variables_1.resolveVariables)(normalized);
      return { source: resolved, compiledGraph: (0, build_graph_1.buildGraph)(resolved) };
    }
  }
});

// packages/runtime/dist/ledger/approvals.js
var require_approvals2 = __commonJS({
  "packages/runtime/dist/ledger/approvals.js"(exports2) {
    "use strict";
    Object.defineProperty(exports2, "__esModule", { value: true });
    exports2.writeApproval = writeApproval;
    exports2.readApproval = readApproval;
    function writeApproval(store, binding) {
      store.writeJson(store.runPath(binding.runId, "approvals", `${binding.stepId}.json`), binding);
    }
    function readApproval(store, runId, stepId) {
      try {
        return store.readJson(store.runPath(runId, "approvals", `${stepId}.json`));
      } catch {
        return void 0;
      }
    }
  }
});

// packages/runtime/dist/control-plane/approval-service.js
var require_approval_service = __commonJS({
  "packages/runtime/dist/control-plane/approval-service.js"(exports2) {
    "use strict";
    Object.defineProperty(exports2, "__esModule", { value: true });
    exports2.getStepApproval = getStepApproval;
    exports2.approveStep = approveStep;
    var shared_1 = require_dist();
    var approvals_1 = require_approvals2();
    function getStepApproval(store, runId, stepId) {
      return (0, approvals_1.readApproval)(store, runId, stepId);
    }
    function approveStep(store, runId, step, policyHash, approvedBy) {
      const approvedAt = (0, shared_1.nowIso)();
      const approval = {
        schemaVersion: "toolflow.approval-binding/v1",
        runId,
        stepId: step.id,
        approvedPayloadHash: step.payloadHash,
        policyHash,
        approvedAt,
        approvedBy,
        approvalMode: "step-time",
        approvalHash: (0, shared_1.hashJson)({ runId, stepId: step.id, approvedPayloadHash: step.payloadHash, policyHash, approvedAt, approvedBy, approvalMode: "step-time" })
      };
      (0, approvals_1.writeApproval)(store, approval);
      return approval;
    }
  }
});

// packages/runtime/dist/compiler/infer-capabilities.js
var require_infer_capabilities = __commonJS({
  "packages/runtime/dist/compiler/infer-capabilities.js"(exports2) {
    "use strict";
    Object.defineProperty(exports2, "__esModule", { value: true });
    exports2.inferCapabilities = inferCapabilities;
    function inferCapabilities(graph) {
      return {
        cells: [...new Set(graph.nodes.map((node) => node.cell))].sort(),
        actions: [...new Set(graph.nodes.map((node) => node.action))].sort()
      };
    }
  }
});

// packages/runtime/dist/classifier/classify-approvals.js
var require_classify_approvals = __commonJS({
  "packages/runtime/dist/classifier/classify-approvals.js"(exports2) {
    "use strict";
    Object.defineProperty(exports2, "__esModule", { value: true });
    exports2.classifyApprovals = classifyApprovals;
    function classifyApprovals(graph) {
      const elevatedSteps = graph.nodes.filter((node) => node.cell === "elevated");
      if (!elevatedSteps.length)
        return { requiresApproval: false, notes: [] };
      return {
        requiresApproval: true,
        notes: elevatedSteps.map((step) => `Step "${step.id}" requires exact-payload elevated approval.`)
      };
    }
  }
});

// packages/runtime/dist/classifier/classify-capabilities.js
var require_classify_capabilities = __commonJS({
  "packages/runtime/dist/classifier/classify-capabilities.js"(exports2) {
    "use strict";
    Object.defineProperty(exports2, "__esModule", { value: true });
    exports2.classifyCapabilities = classifyCapabilities;
    var shared_1 = require_dist();
    function classifyCapabilities(graph, config) {
      const failures = [];
      for (const node of graph.nodes) {
        if (!shared_1.TOOLFLOW_CELLS.includes(node.cell))
          failures.push(`Unsupported cell "${node.cell}" in step "${node.id}".`);
        if (!shared_1.TOOLFLOW_ACTIONS.includes(node.action))
          failures.push(`Unsupported action "${node.action}" in step "${node.id}".`);
        if (node.cell === "elevated" && !config.enableElevated)
          failures.push(`Elevated lane is disabled for step "${node.id}".`);
      }
      return failures;
    }
  }
});

// packages/runtime/dist/classifier/classify-replay.js
var require_classify_replay = __commonJS({
  "packages/runtime/dist/classifier/classify-replay.js"(exports2) {
    "use strict";
    Object.defineProperty(exports2, "__esModule", { value: true });
    exports2.classifyReplay = classifyReplay;
    function classifyReplay(graph) {
      return graph.nodes.filter((node) => node.replayClass === "review_before_replay").map((node) => `Step "${node.id}" requires review before replay.`);
    }
  }
});

// packages/runtime/dist/classifier/classify-side-effects.js
var require_classify_side_effects = __commonJS({
  "packages/runtime/dist/classifier/classify-side-effects.js"(exports2) {
    "use strict";
    Object.defineProperty(exports2, "__esModule", { value: true });
    exports2.classifySideEffects = classifySideEffects;
    function classifySideEffects(graph) {
      return graph.nodes.filter((node) => node.cell === "session").map((node) => `Session step "${node.id}" is constrained to local session semantics.`);
    }
  }
});

// packages/runtime/dist/classifier/classify-structural.js
var require_classify_structural = __commonJS({
  "packages/runtime/dist/classifier/classify-structural.js"(exports2) {
    "use strict";
    Object.defineProperty(exports2, "__esModule", { value: true });
    exports2.classifyStructural = classifyStructural;
    function classifyStructural(graph) {
      const failures = [];
      if (graph.schemaVersion !== "toolflow.compiled-graph/v1")
        failures.push("Unsupported compiled graph schemaVersion.");
      if (!graph.nodes.length)
        failures.push("Compiled graph has no executable nodes.");
      return failures;
    }
  }
});

// packages/runtime/dist/classifier/decide-outcome.js
var require_decide_outcome = __commonJS({
  "packages/runtime/dist/classifier/decide-outcome.js"(exports2) {
    "use strict";
    Object.defineProperty(exports2, "__esModule", { value: true });
    exports2.decideOutcome = decideOutcome;
    function decideOutcome(failures, warnings, requiresApproval = false) {
      if (failures.length)
        return "reject";
      if (requiresApproval)
        return "requires_approval";
      if (warnings.length)
        return "allow_with_warnings";
      return "allow";
    }
  }
});

// packages/runtime/dist/classifier/estimate-cost.js
var require_estimate_cost = __commonJS({
  "packages/runtime/dist/classifier/estimate-cost.js"(exports2) {
    "use strict";
    Object.defineProperty(exports2, "__esModule", { value: true });
    exports2.estimateCost = estimateCost;
    function estimateCost(graph) {
      return { stepCount: graph.nodes.length, latency: "local_fast", cost: "none" };
    }
  }
});

// packages/runtime/dist/classifier/build-proof-bundle.js
var require_build_proof_bundle = __commonJS({
  "packages/runtime/dist/classifier/build-proof-bundle.js"(exports2) {
    "use strict";
    Object.defineProperty(exports2, "__esModule", { value: true });
    exports2.buildProofBundle = buildProofBundle;
    var shared_1 = require_dist();
    var infer_capabilities_1 = require_infer_capabilities();
    var classify_approvals_1 = require_classify_approvals();
    var classify_capabilities_1 = require_classify_capabilities();
    var classify_replay_1 = require_classify_replay();
    var classify_side_effects_1 = require_classify_side_effects();
    var classify_structural_1 = require_classify_structural();
    var decide_outcome_1 = require_decide_outcome();
    var estimate_cost_1 = require_estimate_cost();
    function buildProofBundle(graph, config) {
      const approvals = (0, classify_approvals_1.classifyApprovals)(graph);
      const failures = [...(0, classify_structural_1.classifyStructural)(graph), ...(0, classify_capabilities_1.classifyCapabilities)(graph, config)];
      const warnings = [...(0, classify_replay_1.classifyReplay)(graph), ...(0, classify_side_effects_1.classifySideEffects)(graph)];
      const capabilities = (0, infer_capabilities_1.inferCapabilities)(graph);
      const elevated = capabilities.cells.includes("elevated");
      const withoutHash = {
        schemaVersion: shared_1.PROOF_BUNDLE_SCHEMA_VERSION,
        workflowName: graph.workflowName,
        graphHash: graph.graphHash,
        decision: (0, decide_outcome_1.decideOutcome)(failures, warnings, approvals.requiresApproval),
        riskClass: elevated ? "elevated" : "safe",
        requiredCells: capabilities.cells,
        requiredActions: capabilities.actions,
        warnings: [...warnings, ...approvals.notes],
        objectiveFailures: failures,
        estimates: (0, estimate_cost_1.estimateCost)(graph),
        createdAt: (0, shared_1.nowIso)()
      };
      return { ...withoutHash, proofHash: (0, shared_1.hashJson)(withoutHash) };
    }
  }
});

// packages/runtime/dist/policy/compile-policy.js
var require_compile_policy = __commonJS({
  "packages/runtime/dist/policy/compile-policy.js"(exports2) {
    "use strict";
    Object.defineProperty(exports2, "__esModule", { value: true });
    exports2.compilePolicyArtifact = compilePolicyArtifact;
    var shared_1 = require_dist();
    function compilePolicyArtifact(graph, config) {
      const elevated = graph.nodes.some((node) => node.cell === "elevated");
      const allowedCells = elevated && config.enableElevated ? ["read", "research", "session", "elevated"] : ["read", "research", "session"];
      const allowedActionsByCell = {
        read: ["read_file", "list_files"],
        research: ["research_note"],
        session: ["session_note"],
        elevated: elevated && config.enableElevated ? ["exec_command", "apply_patch"] : []
      };
      const withoutHash = {
        schemaVersion: shared_1.POLICY_ARTIFACT_SCHEMA_VERSION,
        profile: elevated && config.enableElevated ? "operator-elevated" : "safe",
        allowedCells: [...allowedCells],
        allowedActionsByCell,
        bridgeMode: elevated && config.enableElevated ? "local-private-typed-contracts" : "same-process-typed-contracts",
        bindingNotes: [
          elevated && config.enableElevated ? "Elevated lane is local-only, approval-bound, and typed." : "Safe Profile MVP permits bridge and cell in one process.",
          "Typed bridge contracts, grant verification, payload hash checks, and receipts remain binding.",
          elevated && config.enableElevated ? `Elevated actions require exact-payload approval and remain limited to ${shared_1.ELEVATED_PROFILE_ACTIONS.join(", ")}.` : elevated ? "Elevated actions were requested but the elevated lane is disabled in this runtime configuration." : `No elevated actions are present; supported actions are ${shared_1.SAFE_PROFILE_ACTIONS.join(", ")}.`
        ],
        createdAt: (0, shared_1.nowIso)()
      };
      return { ...withoutHash, policyHash: (0, shared_1.hashJson)(withoutHash) };
    }
  }
});

// packages/runtime/dist/config/defaults.js
var require_defaults = __commonJS({
  "packages/runtime/dist/config/defaults.js"(exports2) {
    "use strict";
    Object.defineProperty(exports2, "__esModule", { value: true });
    exports2.DEFAULT_CONFIG = void 0;
    exports2.DEFAULT_CONFIG = {
      ledgerRoot: "data/ledger",
      taskflowMirrorRoot: "data/taskflow-mirror",
      grantTtlSeconds: 300,
      enableElevated: false,
      elevatedAllowedCommands: [],
      progressUpdates: {
        enabled: false,
        longRunThresholdMs: 5 * 60 * 1e3,
        intervalMs: 5 * 60 * 1e3,
        sink: "stderr"
      }
    };
  }
});

// packages/runtime/dist/config/resolve.js
var require_resolve = __commonJS({
  "packages/runtime/dist/config/resolve.js"(exports2) {
    "use strict";
    Object.defineProperty(exports2, "__esModule", { value: true });
    exports2.resolveConfig = resolveConfig;
    var node_path_1 = require("node:path");
    var defaults_1 = require_defaults();
    function resolveConfig(overrides = {}) {
      const enableElevated = overrides.enableElevated ?? process.env.TOOLFLOW_ENABLE_ELEVATED === "1";
      const elevatedAllowedCommands = overrides.elevatedAllowedCommands ?? process.env.TOOLFLOW_ELEVATED_ALLOW?.split(",").map((value) => value.trim()).filter(Boolean) ?? defaults_1.DEFAULT_CONFIG.elevatedAllowedCommands;
      const defaultProgress = defaults_1.DEFAULT_CONFIG.progressUpdates;
      const envProgressEnabled = process.env.TOOLFLOW_PROGRESS_ENABLED === "1";
      const envProgressAfterSeconds = Number(process.env.TOOLFLOW_PROGRESS_AFTER_SECONDS ?? "");
      const envProgressIntervalSeconds = Number(process.env.TOOLFLOW_PROGRESS_INTERVAL_SECONDS ?? "");
      const progressUpdates = {
        ...defaultProgress,
        ...overrides.progressUpdates,
        enabled: overrides.progressUpdates?.enabled ?? envProgressEnabled ?? defaultProgress.enabled,
        longRunThresholdMs: overrides.progressUpdates?.longRunThresholdMs ?? (Number.isFinite(envProgressAfterSeconds) && envProgressAfterSeconds >= 0 ? envProgressAfterSeconds * 1e3 : defaultProgress.longRunThresholdMs),
        intervalMs: overrides.progressUpdates?.intervalMs ?? (Number.isFinite(envProgressIntervalSeconds) && envProgressIntervalSeconds >= 0 ? envProgressIntervalSeconds * 1e3 : defaultProgress.intervalMs),
        sink: overrides.progressUpdates?.sink ?? (process.env.TOOLFLOW_PROGRESS_SINK === "command" || process.env.TOOLFLOW_PROGRESS_SINK === "stderr" ? process.env.TOOLFLOW_PROGRESS_SINK : defaultProgress.sink),
        command: overrides.progressUpdates?.command ?? process.env.TOOLFLOW_PROGRESS_COMMAND ?? defaultProgress.command
      };
      return {
        ...defaults_1.DEFAULT_CONFIG,
        ...overrides,
        ledgerRoot: (0, node_path_1.resolve)(overrides.ledgerRoot ?? process.env.TOOLFLOW_LEDGER_DIR ?? defaults_1.DEFAULT_CONFIG.ledgerRoot),
        taskflowMirrorRoot: (0, node_path_1.resolve)(overrides.taskflowMirrorRoot ?? process.env.TOOLFLOW_TASKFLOW_MIRROR_DIR ?? defaults_1.DEFAULT_CONFIG.taskflowMirrorRoot),
        enableElevated,
        elevatedAllowedCommands,
        progressUpdates
      };
    }
  }
});

// packages/runtime/dist/ledger/store.js
var require_store = __commonJS({
  "packages/runtime/dist/ledger/store.js"(exports2) {
    "use strict";
    Object.defineProperty(exports2, "__esModule", { value: true });
    exports2.LedgerStore = void 0;
    var node_fs_1 = require("node:fs");
    var node_path_1 = require("node:path");
    var shared_1 = require_dist();
    var LedgerStore = class {
      root;
      constructor(root) {
        this.root = root;
        (0, node_fs_1.mkdirSync)((0, node_path_1.join)(root, "runs"), { recursive: true });
      }
      runPath(runId, ...parts) {
        return (0, node_path_1.join)(this.root, "runs", runId, ...parts);
      }
      ensureRun(runId) {
        (0, node_fs_1.mkdirSync)(this.runPath(runId, "artifacts"), { recursive: true });
        (0, node_fs_1.mkdirSync)(this.runPath(runId, "approvals"), { recursive: true });
        (0, node_fs_1.mkdirSync)(this.runPath(runId, "checkpoints"), { recursive: true });
        (0, node_fs_1.mkdirSync)(this.runPath(runId, "grants"), { recursive: true });
        (0, node_fs_1.mkdirSync)(this.runPath(runId, "receipts"), { recursive: true });
      }
      writeJson(path, value) {
        (0, node_fs_1.mkdirSync)((0, node_path_1.dirname)(path), { recursive: true });
        (0, node_fs_1.writeFileSync)(path, `${(0, shared_1.canonicalJson)(value)}
`);
      }
      readJson(path) {
        return JSON.parse((0, node_fs_1.readFileSync)(path, "utf8"));
      }
      appendEvent(runId, type, data = {}) {
        (0, node_fs_1.appendFileSync)(this.runPath(runId, "events.jsonl"), `${(0, shared_1.canonicalJson)({ at: (0, shared_1.nowIso)(), type, ...data })}
`);
      }
      listRunIds() {
        try {
          return (0, node_fs_1.readdirSync)((0, node_path_1.join)(this.root, "runs"), { withFileTypes: true }).filter((entry) => entry.isDirectory() && entry.name.startsWith("run_")).map((entry) => entry.name).sort();
        } catch {
          return [];
        }
      }
      latestRunId() {
        return this.listRunIds().at(-1);
      }
      listJsonFiles(path) {
        if (!(0, node_fs_1.existsSync)(path))
          return [];
        return (0, node_fs_1.readdirSync)(path, { withFileTypes: true }).filter((entry) => entry.isFile() && entry.name.endsWith(".json")).map((entry) => (0, node_path_1.join)(path, entry.name)).sort();
      }
    };
    exports2.LedgerStore = LedgerStore;
  }
});

// packages/runtime/dist/ledger/manifests.js
var require_manifests = __commonJS({
  "packages/runtime/dist/ledger/manifests.js"(exports2) {
    "use strict";
    Object.defineProperty(exports2, "__esModule", { value: true });
    exports2.writeManifest = writeManifest;
    exports2.readManifest = readManifest;
    var shared_1 = require_dist();
    function writeManifest(store, manifest) {
      manifest.updatedAt = (0, shared_1.nowIso)();
      store.writeJson(store.runPath(manifest.runId, "manifest.json"), manifest);
    }
    function readManifest(store, runId) {
      return store.readJson(store.runPath(runId, "manifest.json"));
    }
  }
});

// packages/runtime/dist/ledger/proof-bundles.js
var require_proof_bundles = __commonJS({
  "packages/runtime/dist/ledger/proof-bundles.js"(exports2) {
    "use strict";
    Object.defineProperty(exports2, "__esModule", { value: true });
    exports2.writeProofBundle = writeProofBundle;
    function writeProofBundle(store, runId, proof) {
      store.writeJson(store.runPath(runId, "proof-bundle.json"), proof);
    }
  }
});

// packages/runtime/dist/ledger/policy-artifacts.js
var require_policy_artifacts = __commonJS({
  "packages/runtime/dist/ledger/policy-artifacts.js"(exports2) {
    "use strict";
    Object.defineProperty(exports2, "__esModule", { value: true });
    exports2.writePolicyArtifact = writePolicyArtifact;
    function writePolicyArtifact(store, runId, policy) {
      store.writeJson(store.runPath(runId, "policy-artifact.json"), policy);
    }
  }
});

// packages/runtime/dist/ledger/receipts.js
var require_receipts2 = __commonJS({
  "packages/runtime/dist/ledger/receipts.js"(exports2) {
    "use strict";
    Object.defineProperty(exports2, "__esModule", { value: true });
    exports2.writeReceipt = writeReceipt;
    exports2.readReceipt = readReceipt;
    exports2.tryReadReceipt = tryReadReceipt;
    exports2.listReceipts = listReceipts;
    function writeReceipt(store, receipt) {
      store.writeJson(store.runPath(receipt.runId, "receipts", `${receipt.receiptId}.json`), receipt);
    }
    function readReceipt(store, runId, receiptId) {
      return store.readJson(store.runPath(runId, "receipts", `${receiptId}.json`));
    }
    function tryReadReceipt(store, runId, receiptId) {
      if (!receiptId)
        return void 0;
      try {
        return readReceipt(store, runId, receiptId);
      } catch {
        return void 0;
      }
    }
    function listReceipts(store, runId) {
      return store.listJsonFiles(store.runPath(runId, "receipts")).map((path) => store.readJson(path));
    }
  }
});

// packages/runtime/dist/crypto/signer.js
var require_signer = __commonJS({
  "packages/runtime/dist/crypto/signer.js"(exports2) {
    "use strict";
    Object.defineProperty(exports2, "__esModule", { value: true });
    exports2.signObject = signObject;
    exports2.verifyObject = verifyObject;
    var node_crypto_1 = require("node:crypto");
    var shared_1 = require_dist();
    function signObject(value, key) {
      return (0, node_crypto_1.createHmac)("sha256", key.secret).update((0, shared_1.canonicalJson)(value)).digest("hex");
    }
    function verifyObject(value, signature, key) {
      const expected = Buffer.from(signObject(value, key), "hex");
      const actual = Buffer.from(signature, "hex");
      return expected.length === actual.length && (0, node_crypto_1.timingSafeEqual)(expected, actual);
    }
  }
});

// packages/runtime/dist/ledger/grants.js
var require_grants2 = __commonJS({
  "packages/runtime/dist/ledger/grants.js"(exports2) {
    "use strict";
    Object.defineProperty(exports2, "__esModule", { value: true });
    exports2.writeGrant = writeGrant;
    exports2.readGrant = readGrant;
    exports2.consumeGrant = consumeGrant;
    exports2.expireGrant = expireGrant;
    exports2.voidGrant = voidGrant;
    var shared_1 = require_dist();
    function writeGrant(store, runId, record) {
      store.writeJson(store.runPath(runId, "grants", `${record.grant.grantId}.json`), record);
    }
    function readGrant(store, runId, grantId) {
      return store.readJson(store.runPath(runId, "grants", `${grantId}.json`));
    }
    function consumeGrant(store, runId, grantId, receiptId) {
      const record = readGrant(store, runId, grantId);
      record.state = "consumed";
      record.consumedAt = (0, shared_1.nowIso)();
      record.receiptId = receiptId;
      writeGrant(store, runId, record);
    }
    function expireGrant(store, runId, grantId) {
      const record = readGrant(store, runId, grantId);
      record.state = "expired";
      writeGrant(store, runId, record);
    }
    function voidGrant(store, runId, grantId) {
      const record = readGrant(store, runId, grantId);
      record.state = "void";
      writeGrant(store, runId, record);
    }
  }
});

// packages/runtime/dist/control-plane/grant-service.js
var require_grant_service = __commonJS({
  "packages/runtime/dist/control-plane/grant-service.js"(exports2) {
    "use strict";
    Object.defineProperty(exports2, "__esModule", { value: true });
    exports2.mintStepGrant = mintStepGrant;
    var shared_1 = require_dist();
    var node_crypto_1 = require("node:crypto");
    var signer_1 = require_signer();
    var grants_1 = require_grants2();
    function mintStepGrant(store, key, runId, step, policy, ttlSeconds, approvalHash) {
      const unsigned = {
        schemaVersion: shared_1.STEP_GRANT_SCHEMA_VERSION,
        grantId: (0, shared_1.newGrantId)(),
        runId,
        stepId: step.id,
        cellId: step.cell,
        bridgeId: step.bridgeId,
        action: step.action,
        payloadHash: step.payloadHash,
        policyHash: policy.policyHash,
        approvalHash,
        replayClass: step.replayClass,
        issuedAt: (/* @__PURE__ */ new Date()).toISOString(),
        expiresAt: (0, shared_1.secondsFromNow)(ttlSeconds),
        nonce: (0, node_crypto_1.randomBytes)(12).toString("hex"),
        keyId: key.keyId
      };
      const grant = { ...unsigned, signature: (0, signer_1.signObject)(unsigned, key) };
      const record = { grant, state: "issued" };
      (0, grants_1.writeGrant)(store, runId, record);
      return grant;
    }
  }
});

// packages/elevated/dist/config/resolve.js
var require_resolve2 = __commonJS({
  "packages/elevated/dist/config/resolve.js"(exports2) {
    "use strict";
    Object.defineProperty(exports2, "__esModule", { value: true });
    exports2.resolveElevatedConfig = resolveElevatedConfig;
    function resolveElevatedConfig() {
      return {
        allowedCommands: process.env.TOOLFLOW_ELEVATED_ALLOW?.split(",").map((value) => value.trim()).filter(Boolean) ?? []
      };
    }
  }
});

// packages/elevated/dist/cell/runner.js
var require_runner = __commonJS({
  "packages/elevated/dist/cell/runner.js"(exports2) {
    "use strict";
    Object.defineProperty(exports2, "__esModule", { value: true });
    exports2.runElevatedCell = runElevatedCell;
    var promises_1 = require("node:fs/promises");
    var node_os_1 = require("node:os");
    var node_path_1 = require("node:path");
    var node_child_process_1 = require("node:child_process");
    var resolve_1 = require_resolve2();
    async function runElevatedCell(request) {
      if (request.action === "exec_command")
        return runExecCommand(request);
      if (request.action === "apply_patch")
        return runApplyPatch(request);
      return { ok: false, error: `Unsupported elevated action ${request.action}.` };
    }
    async function runExecCommand(request) {
      const command = arrayOfStrings(request.payload.command, "command");
      const [binary, ...args] = command;
      if (!binary)
        throw new Error("Missing command binary.");
      const config = (0, resolve_1.resolveElevatedConfig)();
      if (!config.allowedCommands.includes(binary))
        throw new Error(`Command "${binary}" is not in the elevated allowlist.`);
      const cwd = typeof request.payload.cwd === "string" ? (0, node_path_1.resolve)(request.payload.cwd) : process.cwd();
      const timeoutMs = typeof request.payload.timeoutMs === "number" ? request.payload.timeoutMs : 1e4;
      const result = await spawnCapture(binary, args, { cwd, timeoutMs });
      return { ok: result.exitCode === 0, output: { command, cwd, ...result }, error: result.exitCode === 0 ? void 0 : `Command exited with ${result.exitCode}.` };
    }
    async function runApplyPatch(request) {
      const patch = stringArg(request.payload.patch, "patch");
      const cwd = typeof request.payload.cwd === "string" ? (0, node_path_1.resolve)(request.payload.cwd) : process.cwd();
      const tempDir = await (0, promises_1.mkdtemp)((0, node_path_1.resolve)((0, node_os_1.tmpdir)(), "toolflow-patch-"));
      const patchPath = (0, node_path_1.resolve)(tempDir, `${(0, node_path_1.basename)(cwd) || "workspace"}.patch`);
      await (0, promises_1.writeFile)(patchPath, patch, "utf8");
      const result = await spawnCapture("git", ["apply", "--recount", "--whitespace=nowarn", patchPath], { cwd, timeoutMs: 1e4 });
      const output = { cwd, patchPath, ...result };
      if (result.exitCode === 0 && typeof request.payload.verifyFile === "string") {
        output.verifyFile = (0, node_path_1.resolve)(cwd, request.payload.verifyFile);
        output.verifyContent = await (0, promises_1.readFile)(output.verifyFile, "utf8");
      }
      return { ok: result.exitCode === 0, output, error: result.exitCode === 0 ? void 0 : `Patch apply failed with ${result.exitCode}.` };
    }
    function stringArg(value, name) {
      if (typeof value !== "string" || value.length === 0)
        throw new Error(`Missing string argument "${name}".`);
      return value;
    }
    function arrayOfStrings(value, name) {
      if (!Array.isArray(value) || value.some((item) => typeof item !== "string"))
        throw new Error(`Expected string array argument "${name}".`);
      return value;
    }
    function spawnCapture(command, args, options) {
      return new Promise((resolvePromise, reject) => {
        const child = (0, node_child_process_1.spawn)(command, args, { cwd: options.cwd, stdio: ["ignore", "pipe", "pipe"] });
        let stdout = "";
        let stderr = "";
        const timer = setTimeout(() => child.kill("SIGTERM"), options.timeoutMs);
        child.stdout.on("data", (chunk) => {
          stdout += String(chunk);
        });
        child.stderr.on("data", (chunk) => {
          stderr += String(chunk);
        });
        child.on("error", (error) => {
          clearTimeout(timer);
          reject(error);
        });
        child.on("close", (exitCode) => {
          clearTimeout(timer);
          resolvePromise({ exitCode, stdout, stderr });
        });
      });
    }
  }
});

// packages/elevated/dist/bridge/handlers.js
var require_handlers = __commonJS({
  "packages/elevated/dist/bridge/handlers.js"(exports2) {
    "use strict";
    Object.defineProperty(exports2, "__esModule", { value: true });
    exports2.elevatedBridgeHandler = void 0;
    var runner_1 = require_runner();
    exports2.elevatedBridgeHandler = {
      bridgeId: "elevated-bridge-v1",
      cellId: "elevated",
      actions: ["exec_command", "apply_patch"],
      execute: runner_1.runElevatedCell
    };
  }
});

// packages/elevated/dist/bridge/local-transport-guard.js
var require_local_transport_guard = __commonJS({
  "packages/elevated/dist/bridge/local-transport-guard.js"(exports2) {
    "use strict";
    Object.defineProperty(exports2, "__esModule", { value: true });
    exports2.ensureLocalTransport = ensureLocalTransport;
    var shared_1 = require_dist();
    function ensureLocalTransport(request) {
      const localOnly = request.payload.localOnly;
      if (localOnly === false)
        throw new shared_1.PolicyError("Elevated bridge rejects non-local transport requests.");
    }
  }
});

// packages/elevated/dist/bridge/verify-approval.js
var require_verify_approval = __commonJS({
  "packages/elevated/dist/bridge/verify-approval.js"(exports2) {
    "use strict";
    Object.defineProperty(exports2, "__esModule", { value: true });
    exports2.ensureApprovalForElevatedRequest = ensureApprovalForElevatedRequest;
    var shared_1 = require_dist();
    function ensureApprovalForElevatedRequest(request, approval) {
      const approvalHash = request.grant.approvalHash;
      if (!approvalHash)
        throw new shared_1.PolicyError("Elevated grant is missing approval binding.");
      if (!approval)
        throw new shared_1.PolicyError("Elevated approval binding was not found.");
      if (approval.approvalHash !== approvalHash)
        throw new shared_1.PolicyError("Elevated approval hash mismatch.");
      if (approval.approvedPayloadHash !== request.grant.payloadHash)
        throw new shared_1.PolicyError("Elevated approval payload binding mismatch.");
      if (approval.policyHash !== request.grant.policyHash)
        throw new shared_1.PolicyError("Elevated approval policy binding mismatch.");
    }
  }
});

// packages/elevated/dist/bridge/server.js
var require_server = __commonJS({
  "packages/elevated/dist/bridge/server.js"(exports2) {
    "use strict";
    Object.defineProperty(exports2, "__esModule", { value: true });
    exports2.ElevatedBridge = void 0;
    var node_crypto_1 = require("node:crypto");
    var shared_1 = require_dist();
    var local_transport_guard_1 = require_local_transport_guard();
    var verify_approval_1 = require_verify_approval();
    var ElevatedBridge = class {
      handler;
      store;
      policy;
      key;
      constructor(handler, store, policy, key) {
        this.handler = handler;
        this.store = store;
        this.policy = policy;
        this.key = key;
      }
      async execute(request) {
        const startedAt = (0, shared_1.nowIso)();
        verifyGrantForRequest(this.store, this.policy, this.key, request);
        (0, local_transport_guard_1.ensureLocalTransport)(request);
        const approval = readApproval(this.store, request.grant.runId, request.grant.stepId);
        (0, verify_approval_1.ensureApprovalForElevatedRequest)(request, approval);
        const result = await this.handler.execute(request);
        const receipt = emitReceipt(request, result, this.key, startedAt);
        writeReceipt(this.store, receipt);
        consumeGrant(this.store, receipt.runId, receipt.grantId, receipt.receiptId);
        return { receipt, output: result.output };
      }
    };
    exports2.ElevatedBridge = ElevatedBridge;
    function signObject(value, key) {
      return (0, node_crypto_1.createHmac)("sha256", key.secret).update((0, shared_1.canonicalJson)(value)).digest("hex");
    }
    function verifyObject(value, signature, key) {
      const expected = Buffer.from(signObject(value, key), "hex");
      const actual = Buffer.from(signature, "hex");
      return expected.length === actual.length && (0, node_crypto_1.timingSafeEqual)(expected, actual);
    }
    function verifyGrantForRequest(store, policy, key, request) {
      const { grant } = request;
      const { signature, ...unsigned } = grant;
      if (!verifyObject(unsigned, signature, key))
        throw new shared_1.PolicyError("Grant signature verification failed.");
      if ((0, shared_1.isExpired)(grant.expiresAt))
        throw new shared_1.PolicyError("Grant is expired.");
      if (grant.bridgeId !== request.bridgeId || grant.cellId !== request.cellId)
        throw new shared_1.PolicyError("Grant bridge or cell binding mismatch.");
      if (grant.action !== request.action)
        throw new shared_1.PolicyError("Grant action binding mismatch.");
      if (grant.payloadHash !== (0, shared_1.hashJson)(request.payload))
        throw new shared_1.PolicyError("Grant payload hash mismatch.");
      if (grant.policyHash !== policy.policyHash)
        throw new shared_1.PolicyError("Grant policy hash mismatch.");
      const record = store.readJson(store.runPath(grant.runId, "grants", `${grant.grantId}.json`));
      if (record.state !== "issued")
        throw new shared_1.PolicyError(`Grant is ${record.state}, not issued.`);
    }
    function emitReceipt(request, result, key, startedAt) {
      const withoutSignature = {
        schemaVersion: shared_1.RECEIPT_SCHEMA_VERSION,
        receiptId: (0, shared_1.newReceiptId)(),
        grantId: request.grant.grantId,
        runId: request.grant.runId,
        stepId: request.grant.stepId,
        bridgeId: request.bridgeId,
        payloadHash: request.grant.payloadHash,
        policyHash: request.grant.policyHash,
        status: result.ok ? "succeeded" : "failed",
        startedAt,
        endedAt: (0, shared_1.nowIso)(),
        outputHash: result.output ? (0, shared_1.hashJson)(result.output) : void 0,
        error: result.error,
        keyId: key.keyId
      };
      return { ...withoutSignature, signature: signObject(withoutSignature, key) };
    }
    function writeReceipt(store, receipt) {
      store.writeJson(store.runPath(receipt.runId, "receipts", `${receipt.receiptId}.json`), receipt);
    }
    function consumeGrant(store, runId, grantId, receiptId) {
      const record = store.readJson(store.runPath(runId, "grants", `${grantId}.json`));
      record.state = "consumed";
      record.consumedAt = (0, shared_1.nowIso)();
      record.receiptId = receiptId;
      store.writeJson(store.runPath(runId, "grants", `${grantId}.json`), record);
    }
    function readApproval(store, runId, stepId) {
      try {
        return store.readJson(store.runPath(runId, "approvals", `${stepId}.json`));
      } catch {
        return void 0;
      }
    }
  }
});

// packages/elevated/dist/config/schema.js
var require_schema = __commonJS({
  "packages/elevated/dist/config/schema.js"(exports2) {
    "use strict";
    Object.defineProperty(exports2, "__esModule", { value: true });
  }
});

// packages/elevated/dist/gateway/elevated-openclaw-client.js
var require_elevated_openclaw_client = __commonJS({
  "packages/elevated/dist/gateway/elevated-openclaw-client.js"(exports2) {
    "use strict";
    Object.defineProperty(exports2, "__esModule", { value: true });
    exports2.createElevatedGatewayClient = createElevatedGatewayClient;
    function createElevatedGatewayClient() {
      return { mode: "local-only" };
    }
  }
});

// packages/elevated/dist/main.js
var require_main = __commonJS({
  "packages/elevated/dist/main.js"(exports2) {
    "use strict";
    var __createBinding2 = exports2 && exports2.__createBinding || (Object.create ? (function(o, m, k, k2) {
      if (k2 === void 0) k2 = k;
      var desc = Object.getOwnPropertyDescriptor(m, k);
      if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
        desc = { enumerable: true, get: function() {
          return m[k];
        } };
      }
      Object.defineProperty(o, k2, desc);
    }) : (function(o, m, k, k2) {
      if (k2 === void 0) k2 = k;
      o[k2] = m[k];
    }));
    var __exportStar2 = exports2 && exports2.__exportStar || function(m, exports3) {
      for (var p in m) if (p !== "default" && !Object.prototype.hasOwnProperty.call(exports3, p)) __createBinding2(exports3, m, p);
    };
    Object.defineProperty(exports2, "__esModule", { value: true });
    __exportStar2(require_handlers(), exports2);
    __exportStar2(require_local_transport_guard(), exports2);
    __exportStar2(require_server(), exports2);
    __exportStar2(require_verify_approval(), exports2);
    __exportStar2(require_runner(), exports2);
    __exportStar2(require_resolve2(), exports2);
    __exportStar2(require_schema(), exports2);
    __exportStar2(require_elevated_openclaw_client(), exports2);
  }
});

// packages/runtime/dist/bridges/base/emit-receipt.js
var require_emit_receipt = __commonJS({
  "packages/runtime/dist/bridges/base/emit-receipt.js"(exports2) {
    "use strict";
    Object.defineProperty(exports2, "__esModule", { value: true });
    exports2.emitReceipt = emitReceipt;
    var shared_1 = require_dist();
    var signer_1 = require_signer();
    function emitReceipt(request, result, key, startedAt) {
      const withoutSignature = {
        schemaVersion: shared_1.RECEIPT_SCHEMA_VERSION,
        receiptId: (0, shared_1.newReceiptId)(),
        grantId: request.grant.grantId,
        runId: request.grant.runId,
        stepId: request.grant.stepId,
        bridgeId: request.bridgeId,
        payloadHash: request.grant.payloadHash,
        policyHash: request.grant.policyHash,
        status: result.ok ? "succeeded" : "failed",
        startedAt,
        endedAt: (0, shared_1.nowIso)(),
        outputHash: result.output ? (0, shared_1.hashJson)(result.output) : void 0,
        error: result.error,
        keyId: key.keyId
      };
      return { ...withoutSignature, signature: (0, signer_1.signObject)(withoutSignature, key) };
    }
  }
});

// packages/runtime/dist/crypto/verifier.js
var require_verifier = __commonJS({
  "packages/runtime/dist/crypto/verifier.js"(exports2) {
    "use strict";
    Object.defineProperty(exports2, "__esModule", { value: true });
    exports2.verifyObject = void 0;
    var signer_1 = require_signer();
    Object.defineProperty(exports2, "verifyObject", { enumerable: true, get: function() {
      return signer_1.verifyObject;
    } });
  }
});

// packages/runtime/dist/bridges/base/verify-grant.js
var require_verify_grant = __commonJS({
  "packages/runtime/dist/bridges/base/verify-grant.js"(exports2) {
    "use strict";
    Object.defineProperty(exports2, "__esModule", { value: true });
    exports2.verifyGrantForRequest = verifyGrantForRequest;
    var shared_1 = require_dist();
    var verifier_1 = require_verifier();
    var grants_1 = require_grants2();
    function verifyGrantForRequest(store, policy, key, request) {
      const { grant } = request;
      const { signature, ...unsigned } = grant;
      if (!(0, verifier_1.verifyObject)(unsigned, signature, key))
        throw new shared_1.PolicyError("Grant signature verification failed.");
      if ((0, shared_1.isExpired)(grant.expiresAt))
        throw new shared_1.PolicyError("Grant is expired.");
      if (grant.bridgeId !== request.bridgeId || grant.cellId !== request.cellId)
        throw new shared_1.PolicyError("Grant bridge or cell binding mismatch.");
      if (grant.action !== request.action)
        throw new shared_1.PolicyError("Grant action binding mismatch.");
      if (grant.payloadHash !== (0, shared_1.hashJson)(request.payload))
        throw new shared_1.PolicyError("Grant payload hash mismatch.");
      if (grant.policyHash !== policy.policyHash)
        throw new shared_1.PolicyError("Grant policy hash mismatch.");
      const record = (0, grants_1.readGrant)(store, grant.runId, grant.grantId);
      if (record.state !== "issued")
        throw new shared_1.PolicyError(`Grant is ${record.state}, not issued.`);
    }
  }
});

// packages/runtime/dist/bridges/base/bridge-server.js
var require_bridge_server = __commonJS({
  "packages/runtime/dist/bridges/base/bridge-server.js"(exports2) {
    "use strict";
    Object.defineProperty(exports2, "__esModule", { value: true });
    exports2.SameProcessBridge = void 0;
    var shared_1 = require_dist();
    var grants_1 = require_grants2();
    var receipts_1 = require_receipts2();
    var emit_receipt_1 = require_emit_receipt();
    var verify_grant_1 = require_verify_grant();
    var SameProcessBridge = class {
      handler;
      store;
      policy;
      key;
      constructor(handler, store, policy, key) {
        this.handler = handler;
        this.store = store;
        this.policy = policy;
        this.key = key;
      }
      async execute(request) {
        const startedAt = (0, shared_1.nowIso)();
        (0, verify_grant_1.verifyGrantForRequest)(this.store, this.policy, this.key, request);
        const result = await this.handler.execute(request);
        const receipt = (0, emit_receipt_1.emitReceipt)(request, result, this.key, startedAt);
        (0, receipts_1.writeReceipt)(this.store, receipt);
        (0, grants_1.consumeGrant)(this.store, receipt.runId, receipt.grantId, receipt.receiptId);
        return { receipt, output: result.output };
      }
    };
    exports2.SameProcessBridge = SameProcessBridge;
  }
});

// packages/runtime/dist/cells/read/runner.js
var require_runner2 = __commonJS({
  "packages/runtime/dist/cells/read/runner.js"(exports2) {
    "use strict";
    Object.defineProperty(exports2, "__esModule", { value: true });
    exports2.runReadCell = runReadCell;
    var promises_1 = require("node:fs/promises");
    var node_path_1 = require("node:path");
    async function runReadCell(request) {
      if (request.action === "read_file") {
        const path = stringArg(request.payload.path, "path");
        const content = await (0, promises_1.readFile)((0, node_path_1.resolve)(path), "utf8");
        return { ok: true, output: { path: (0, node_path_1.resolve)(path), content } };
      }
      if (request.action === "list_files") {
        const path = (0, node_path_1.resolve)(stringArg(request.payload.path ?? ".", "path"));
        const entries = await (0, promises_1.readdir)(path);
        const files = [];
        for (const entry of entries.sort()) {
          const fullPath = (0, node_path_1.resolve)(path, entry);
          const info = await (0, promises_1.stat)(fullPath);
          files.push({ name: entry, path: fullPath, type: info.isDirectory() ? "directory" : "file", size: info.size });
        }
        return { ok: true, output: { path, entries: files } };
      }
      return { ok: false, error: `Unsupported read action ${request.action}.` };
    }
    function stringArg(value, name) {
      if (typeof value !== "string" || value.length === 0)
        throw new Error(`Missing string argument "${name}".`);
      return value;
    }
  }
});

// packages/runtime/dist/bridges/read/handlers.js
var require_handlers2 = __commonJS({
  "packages/runtime/dist/bridges/read/handlers.js"(exports2) {
    "use strict";
    Object.defineProperty(exports2, "__esModule", { value: true });
    exports2.readBridgeHandler = void 0;
    var runner_1 = require_runner2();
    exports2.readBridgeHandler = {
      bridgeId: "read-bridge-v1",
      cellId: "read",
      actions: ["read_file", "list_files"],
      execute: runner_1.runReadCell
    };
  }
});

// packages/runtime/dist/cells/research/runner.js
var require_runner3 = __commonJS({
  "packages/runtime/dist/cells/research/runner.js"(exports2) {
    "use strict";
    Object.defineProperty(exports2, "__esModule", { value: true });
    exports2.runResearchCell = runResearchCell;
    async function runResearchCell(request) {
      if (request.action !== "research_note")
        return { ok: false, error: `Unsupported research action ${request.action}.` };
      const query = typeof request.payload.query === "string" ? request.payload.query : "unspecified";
      const sources = Array.isArray(request.payload.sources) ? request.payload.sources.map(String) : [];
      const note = `Local research note for "${query}". Sources considered: ${sources.length ? sources.join(", ") : "none provided"}.`;
      return { ok: true, output: { query, sources, note } };
    }
  }
});

// packages/runtime/dist/bridges/research/handlers.js
var require_handlers3 = __commonJS({
  "packages/runtime/dist/bridges/research/handlers.js"(exports2) {
    "use strict";
    Object.defineProperty(exports2, "__esModule", { value: true });
    exports2.researchBridgeHandler = void 0;
    var runner_1 = require_runner3();
    exports2.researchBridgeHandler = {
      bridgeId: "research-bridge-v1",
      cellId: "research",
      actions: ["research_note"],
      execute: runner_1.runResearchCell
    };
  }
});

// packages/runtime/dist/cells/session/runner.js
var require_runner4 = __commonJS({
  "packages/runtime/dist/cells/session/runner.js"(exports2) {
    "use strict";
    Object.defineProperty(exports2, "__esModule", { value: true });
    exports2.runSessionCell = runSessionCell;
    async function runSessionCell(request) {
      if (request.action === "session_note") {
        const prompt = typeof request.payload.prompt === "string" ? request.payload.prompt : "";
        return { ok: true, output: { mode: "local_session_note", prompt, response: `MVP session note recorded: ${prompt}` } };
      }
      return { ok: false, error: `Unsupported session action ${request.action}.` };
    }
  }
});

// packages/runtime/dist/bridges/session/handlers.js
var require_handlers4 = __commonJS({
  "packages/runtime/dist/bridges/session/handlers.js"(exports2) {
    "use strict";
    Object.defineProperty(exports2, "__esModule", { value: true });
    exports2.sessionBridgeHandler = void 0;
    var runner_1 = require_runner4();
    exports2.sessionBridgeHandler = {
      bridgeId: "session-bridge-v1",
      cellId: "session",
      actions: ["session_note"],
      execute: runner_1.runSessionCell
    };
  }
});

// packages/runtime/dist/control-plane/dispatcher.js
var require_dispatcher = __commonJS({
  "packages/runtime/dist/control-plane/dispatcher.js"(exports2) {
    "use strict";
    Object.defineProperty(exports2, "__esModule", { value: true });
    exports2.dispatchStep = dispatchStep;
    var elevated_1 = require_main();
    var bridge_server_1 = require_bridge_server();
    var handlers_1 = require_handlers2();
    var handlers_2 = require_handlers3();
    var handlers_3 = require_handlers4();
    var handlers = {
      elevated: elevated_1.elevatedBridgeHandler,
      read: handlers_1.readBridgeHandler,
      research: handlers_2.researchBridgeHandler,
      session: handlers_3.sessionBridgeHandler
    };
    async function dispatchStep(store, policy, key, step, grant) {
      const handler = handlers[step.cell];
      const bridge = step.cell === "elevated" ? new elevated_1.ElevatedBridge(handler, store, policy, key) : new bridge_server_1.SameProcessBridge(handler, store, policy, key);
      const request = { bridgeId: step.bridgeId, cellId: step.cell, action: step.action, payload: step.payload, grant };
      return bridge.execute(request);
    }
  }
});

// packages/runtime/dist/policy/replay-rules.js
var require_replay_rules = __commonJS({
  "packages/runtime/dist/policy/replay-rules.js"(exports2) {
    "use strict";
    Object.defineProperty(exports2, "__esModule", { value: true });
    exports2.replayDecision = replayDecision;
    function replayDecision(replayClass) {
      if (replayClass === "review_before_replay")
        return "review_required";
      return "replay_allowed";
    }
  }
});

// packages/runtime/dist/control-plane/taskflow-mirror.js
var require_taskflow_mirror = __commonJS({
  "packages/runtime/dist/control-plane/taskflow-mirror.js"(exports2) {
    "use strict";
    Object.defineProperty(exports2, "__esModule", { value: true });
    exports2.mapRunStateToTaskflowState = mapRunStateToTaskflowState;
    exports2.buildTaskflowMirrorRecord = buildTaskflowMirrorRecord;
    exports2.syncTaskflowMirror = syncTaskflowMirror;
    exports2.readTaskflowMirror = readTaskflowMirror;
    exports2.syncTaskflowMirrorFromLedger = syncTaskflowMirrorFromLedger;
    exports2.taskflowMirrorStatus = taskflowMirrorStatus;
    var node_fs_1 = require("node:fs");
    var node_path_1 = require("node:path");
    var resolve_1 = require_resolve();
    var store_1 = require_store();
    var manifests_1 = require_manifests();
    function mirrorRunDir(root) {
      return (0, node_path_1.join)(root, "runs");
    }
    function mirrorRecordPath(root, runId) {
      return (0, node_path_1.join)(mirrorRunDir(root), `${runId}.json`);
    }
    function mirrorIndexPath(root) {
      return (0, node_path_1.join)(root, "index.json");
    }
    function ensureMirrorRoot(root) {
      (0, node_fs_1.mkdirSync)(mirrorRunDir(root), { recursive: true });
    }
    function readMirrorIndex(root) {
      ensureMirrorRoot(root);
      try {
        return JSON.parse((0, node_fs_1.readFileSync)(mirrorIndexPath(root), "utf8"));
      } catch {
        return {
          schemaVersion: "toolflow.taskflow-mirror-index/v1",
          updatedAt: (/* @__PURE__ */ new Date()).toISOString(),
          runs: []
        };
      }
    }
    function writeMirrorIndex(root, index) {
      (0, node_fs_1.writeFileSync)(mirrorIndexPath(root), `${JSON.stringify(index, null, 2)}
`);
    }
    function mapRunStateToTaskflowState(manifest) {
      switch (manifest.state) {
        case "awaiting_approval":
          return "waiting";
        case "running":
        case "ready":
          return "running";
        case "failed":
        case "rejected":
        case "quarantined":
          return "blocked";
        case "cancelled":
          return "cancelled";
        case "succeeded":
          return "done";
        default:
          return "blocked";
      }
    }
    function buildTaskflowMirrorRecord(manifest) {
      const stepEntries = Object.entries(manifest.steps);
      const awaitingApproval = stepEntries.find(([, step]) => step.state === "awaiting_approval");
      const running = stepEntries.find(([, step]) => step.state === "running");
      const failed = stepEntries.find(([, step]) => step.state === "failed");
      const mirroredTaskflowState = mapRunStateToTaskflowState(manifest);
      return {
        schemaVersion: "toolflow.taskflow-mirror/v1",
        runId: manifest.runId,
        workflowName: manifest.workflowName,
        runState: manifest.state,
        mirroredTaskflowState,
        currentStep: awaitingApproval?.[0] ?? running?.[0] ?? failed?.[0],
        waitingOn: awaitingApproval ? {
          kind: "approval",
          stepId: awaitingApproval[0],
          reason: `ToolFlow step ${awaitingApproval[0]} requires approval.`
        } : void 0,
        blockedSummary: failed ? `ToolFlow step ${failed[0]} failed.` : manifest.state === "quarantined" ? `Run ${manifest.runId} is quarantined.` : void 0,
        doneSummary: manifest.state === "succeeded" ? `Run ${manifest.runId} completed successfully.` : void 0,
        updatedAt: manifest.updatedAt,
        stepStates: Object.fromEntries(stepEntries.map(([stepId, step]) => [stepId, step.state]))
      };
    }
    function syncTaskflowMirror(store, manifest, configInput = {}) {
      const config = (0, resolve_1.resolveConfig)(configInput);
      const root = config.taskflowMirrorRoot;
      ensureMirrorRoot(root);
      const record = buildTaskflowMirrorRecord(manifest);
      (0, node_fs_1.writeFileSync)(mirrorRecordPath(root, manifest.runId), `${JSON.stringify(record, null, 2)}
`);
      const index = readMirrorIndex(root);
      index.updatedAt = manifest.updatedAt;
      index.runs = index.runs.filter((run) => run.runId !== manifest.runId);
      index.runs.push({
        runId: manifest.runId,
        workflowName: manifest.workflowName,
        runState: manifest.state,
        mirroredTaskflowState: record.mirroredTaskflowState,
        updatedAt: manifest.updatedAt
      });
      index.runs.sort((a, b) => a.updatedAt.localeCompare(b.updatedAt));
      writeMirrorIndex(root, index);
      store.appendEvent(manifest.runId, "taskflow.mirror_synced", {
        mirroredTaskflowState: record.mirroredTaskflowState,
        mirrorPath: mirrorRecordPath(root, manifest.runId)
      });
      return record;
    }
    function readTaskflowMirror(runId, configInput = {}) {
      const config = (0, resolve_1.resolveConfig)(configInput);
      return JSON.parse((0, node_fs_1.readFileSync)(mirrorRecordPath(config.taskflowMirrorRoot, runId), "utf8"));
    }
    function syncTaskflowMirrorFromLedger(runId, configInput = {}) {
      const config = (0, resolve_1.resolveConfig)(configInput);
      const store = new store_1.LedgerStore(config.ledgerRoot);
      const manifest = (0, manifests_1.readManifest)(store, runId);
      return syncTaskflowMirror(store, manifest, config);
    }
    function taskflowMirrorStatus(configInput = {}) {
      const config = (0, resolve_1.resolveConfig)(configInput);
      ensureMirrorRoot(config.taskflowMirrorRoot);
      const index = readMirrorIndex(config.taskflowMirrorRoot);
      const runCount = (0, node_fs_1.readdirSync)(mirrorRunDir(config.taskflowMirrorRoot), { withFileTypes: true }).filter((entry) => entry.isFile() && entry.name.endsWith(".json")).length;
      return {
        status: "enabled",
        root: config.taskflowMirrorRoot,
        runCount,
        lastUpdatedAt: index.updatedAt,
        latestRun: index.runs.at(-1)
      };
    }
  }
});

// packages/runtime/dist/control-plane/recovery-service.js
var require_recovery_service = __commonJS({
  "packages/runtime/dist/control-plane/recovery-service.js"(exports2) {
    "use strict";
    Object.defineProperty(exports2, "__esModule", { value: true });
    exports2.recoveryStatus = recoveryStatus;
    exports2.recoverRun = recoverRun;
    var shared_1 = require_dist();
    var manifests_1 = require_manifests();
    var grants_1 = require_grants2();
    var receipts_1 = require_receipts2();
    var replay_rules_1 = require_replay_rules();
    var taskflow_mirror_1 = require_taskflow_mirror();
    function recoveryStatus() {
      return "Recovery engine enabled: grant requeue, receipt reconciliation, and quarantine for non-replayable interrupted steps.";
    }
    function recoverRun(store, runId) {
      const manifest = (0, manifests_1.readManifest)(store, runId);
      const graph = store.readJson(store.runPath(manifest.runId, "compiled-graph.json"));
      const previousState = manifest.state;
      const steps = graph.nodes.map((node) => recoverStep(store, manifest, node));
      manifest.state = deriveRunState(manifest);
      (0, manifests_1.writeManifest)(store, manifest);
      (0, taskflow_mirror_1.syncTaskflowMirror)(store, manifest);
      store.appendEvent(manifest.runId, "run.recovered", { previousState, nextState: manifest.state, steps: steps.length });
      return { runId: manifest.runId, previousState, nextState: manifest.state, steps };
    }
    function recoverStep(store, manifest, node) {
      const step = manifest.steps[node.id];
      const previousState = step.state;
      if (["pending", "awaiting_approval", "quarantined", "succeeded", "failed", "skipped"].includes(step.state)) {
        return { stepId: node.id, previousState, nextState: step.state, disposition: "unchanged", reason: `Step already ${step.state}.` };
      }
      const receipt = (0, receipts_1.tryReadReceipt)(store, manifest.runId, step.receiptId);
      if (receipt) {
        step.state = receipt.status;
        step.receiptId = receipt.receiptId;
        step.endedAt = receipt.endedAt;
        if (receipt.error)
          step.error = receipt.error;
        return { stepId: node.id, previousState, nextState: step.state, disposition: "reconciled_from_receipt", reason: "Recovered terminal receipt from ledger." };
      }
      if (!step.grantId) {
        step.state = (0, replay_rules_1.replayDecision)(node.replayClass) === "review_required" ? "quarantined" : "pending";
        return {
          stepId: node.id,
          previousState,
          nextState: step.state,
          disposition: step.state === "quarantined" ? "quarantined" : "requeued",
          reason: "Interrupted step had no recoverable grant record."
        };
      }
      const grantRecord = (0, grants_1.readGrant)(store, manifest.runId, step.grantId);
      const grantReceipt = (0, receipts_1.tryReadReceipt)(store, manifest.runId, grantRecord.receiptId);
      if (grantReceipt) {
        step.state = grantReceipt.status;
        step.receiptId = grantReceipt.receiptId;
        step.endedAt = grantReceipt.endedAt;
        if (grantReceipt.error)
          step.error = grantReceipt.error;
        return { stepId: node.id, previousState, nextState: step.state, disposition: "reconciled_from_receipt", reason: "Recovered receipt referenced by grant record." };
      }
      const replay = (0, replay_rules_1.replayDecision)(node.replayClass);
      if (grantRecord.state === "issued") {
        if ((0, shared_1.isExpired)(grantRecord.grant.expiresAt))
          (0, grants_1.expireGrant)(store, manifest.runId, grantRecord.grant.grantId);
        else
          (0, grants_1.voidGrant)(store, manifest.runId, grantRecord.grant.grantId);
        clearStepForReplay(step);
        return { stepId: node.id, previousState, nextState: step.state, disposition: "requeued", reason: "Unused interrupted grant was requeued for replay." };
      }
      if (grantRecord.state === "consumed") {
        if (replay === "review_required") {
          step.state = "quarantined";
          return { stepId: node.id, previousState, nextState: step.state, disposition: "quarantined", reason: "Consumed grant without receipt requires manual review before replay." };
        }
        clearStepForReplay(step);
        return { stepId: node.id, previousState, nextState: step.state, disposition: "requeued", reason: "Consumed grant without receipt was requeued because replay is allowed." };
      }
      if (grantRecord.state === "expired" || grantRecord.state === "void") {
        clearStepForReplay(step);
        return { stepId: node.id, previousState, nextState: step.state, disposition: "requeued", reason: `Grant was ${grantRecord.state}; step returned to pending.` };
      }
      return { stepId: node.id, previousState, nextState: step.state, disposition: "unchanged", reason: `Grant state ${grantRecord.state} required no adjustment.` };
    }
    function clearStepForReplay(step) {
      step.state = "pending";
      delete step.grantId;
      delete step.startedAt;
    }
    function deriveRunState(manifest) {
      const steps = Object.values(manifest.steps);
      if (steps.some((step) => step.state === "quarantined"))
        return "quarantined";
      if (steps.some((step) => step.state === "awaiting_approval"))
        return "awaiting_approval";
      if (steps.every((step) => step.state === "succeeded"))
        return "succeeded";
      if (steps.some((step) => step.state === "failed"))
        return "failed";
      if (steps.some((step) => ["pending", "grant_issued", "running"].includes(step.state)))
        return "ready";
      return manifest.state;
    }
  }
});

// packages/runtime/dist/control-plane/scheduler.js
var require_scheduler = __commonJS({
  "packages/runtime/dist/control-plane/scheduler.js"(exports2) {
    "use strict";
    Object.defineProperty(exports2, "__esModule", { value: true });
    exports2.nextRunnableSteps = nextRunnableSteps;
    function nextRunnableSteps(graph, manifest) {
      return graph.nodes.filter((node) => {
        if (manifest.steps[node.id].state !== "pending")
          return false;
        return node.dependsOn.every((dep) => manifest.steps[dep]?.state === "succeeded");
      });
    }
  }
});

// packages/runtime/dist/control-plane/receipt-service.js
var require_receipt_service = __commonJS({
  "packages/runtime/dist/control-plane/receipt-service.js"(exports2) {
    "use strict";
    Object.defineProperty(exports2, "__esModule", { value: true });
    exports2.reconcileReceipt = reconcileReceipt;
    function reconcileReceipt(manifest, receipt) {
      const step = manifest.steps[receipt.stepId];
      step.state = receipt.status;
      step.receiptId = receipt.receiptId;
      step.endedAt = receipt.endedAt;
      if (receipt.error)
        step.error = receipt.error;
    }
  }
});

// packages/runtime/dist/control-plane/progress-reporter.js
var require_progress_reporter = __commonJS({
  "packages/runtime/dist/control-plane/progress-reporter.js"(exports2) {
    "use strict";
    Object.defineProperty(exports2, "__esModule", { value: true });
    exports2.createRunProgressMonitor = createRunProgressMonitor;
    var node_child_process_1 = require("node:child_process");
    var shared_1 = require_dist();
    function createRunProgressMonitor(config, totalSteps, getSnapshot) {
      const reporter = config.progressReporter ?? defaultReporter(config);
      const progress = config.progressUpdates;
      if (!progress.enabled && !config.progressReporter)
        return silentMonitor();
      let interval;
      let longRunningStarted = false;
      let lastLongRunningAt = 0;
      function elapsedMs(manifest) {
        return Math.max(0, Date.now() - new Date(manifest.createdAt).getTime());
      }
      function completedSteps(manifest) {
        return Object.values(manifest.steps).filter((step) => step.state === "succeeded").length;
      }
      function emit(type, manifest, message, currentStepId) {
        void Promise.resolve(reporter({
          type,
          runId: manifest.runId,
          workflowName: manifest.workflowName,
          state: manifest.state,
          elapsedMs: elapsedMs(manifest),
          completedSteps: completedSteps(manifest),
          totalSteps,
          currentStepId,
          message,
          emittedAt: (0, shared_1.nowIso)()
        })).catch(() => void 0);
      }
      function maybeEmitLongRunning(snapshot, force = false) {
        const threshold = progress.longRunThresholdMs;
        const intervalMs = Math.max(progress.intervalMs, 1e3);
        const elapsed = elapsedMs(snapshot.manifest);
        if (!force && elapsed < threshold)
          return;
        const now = Date.now();
        if (!force && longRunningStarted && now - lastLongRunningAt < intervalMs)
          return;
        longRunningStarted = true;
        lastLongRunningAt = now;
        const stepText = snapshot.currentStepId ? ` Current step: ${snapshot.currentStepId}.` : "";
        emit("long_running", snapshot.manifest, `ToolFlow run ${snapshot.manifest.runId} is still running after ${Math.round(elapsed / 6e4)} minute(s). ${completedSteps(snapshot.manifest)}/${totalSteps} step(s) completed.${stepText}`.trim(), snapshot.currentStepId);
      }
      return {
        start() {
          emit("run_started", getSnapshot().manifest, `ToolFlow run ${getSnapshot().manifest.runId} started for workflow "${getSnapshot().manifest.workflowName}".`);
          interval = setInterval(() => maybeEmitLongRunning(getSnapshot()), Math.min(Math.max(progress.intervalMs, 3e4), 6e4));
          interval.unref?.();
        },
        stop() {
          if (interval)
            clearInterval(interval);
          interval = void 0;
        },
        onStepStarted(stepId, manifest) {
          maybeEmitLongRunning({ manifest, currentStepId: stepId });
          if (!longRunningStarted)
            return;
          emit("step_started", manifest, `ToolFlow run ${manifest.runId} started step ${stepId}.`, stepId);
        },
        onStepCompleted(stepId, manifest) {
          maybeEmitLongRunning({ manifest, currentStepId: stepId });
          if (!longRunningStarted)
            return;
          emit("step_completed", manifest, `ToolFlow run ${manifest.runId} completed step ${stepId}. ${completedSteps(manifest)}/${totalSteps} step(s) finished.`, stepId);
        },
        onApprovalWait(stepId, manifest) {
          maybeEmitLongRunning({ manifest, currentStepId: stepId }, true);
          emit("approval_wait", manifest, `ToolFlow run ${manifest.runId} is waiting for approval on step ${stepId}.`, stepId);
        },
        onRunCompleted(manifest) {
          if (longRunningStarted || elapsedMs(manifest) >= progress.longRunThresholdMs) {
            emit("run_completed", manifest, `ToolFlow run ${manifest.runId} finished with state ${manifest.state}. ${completedSteps(manifest)}/${totalSteps} step(s) completed.`);
          }
        }
      };
    }
    function silentMonitor() {
      return {
        start() {
        },
        stop() {
        },
        onStepStarted() {
        },
        onStepCompleted() {
        },
        onApprovalWait() {
        },
        onRunCompleted() {
        }
      };
    }
    function defaultReporter(config) {
      return (event) => {
        if (config.progressUpdates.sink === "command" && config.progressUpdates.command) {
          const child = (0, node_child_process_1.spawn)(config.progressUpdates.command, {
            shell: true,
            stdio: "ignore",
            env: {
              ...process.env,
              TOOLFLOW_PROGRESS_JSON: JSON.stringify(event),
              TOOLFLOW_PROGRESS_TEXT: event.message,
              TOOLFLOW_PROGRESS_RUN_ID: event.runId,
              TOOLFLOW_PROGRESS_STATE: event.state,
              TOOLFLOW_PROGRESS_STEP_ID: event.currentStepId ?? ""
            }
          });
          child.on("error", () => void 0);
          return;
        }
        console.error(`[toolflow-progress] ${JSON.stringify(event)}`);
      };
    }
  }
});

// packages/runtime/dist/control-plane/run-service.js
var require_run_service = __commonJS({
  "packages/runtime/dist/control-plane/run-service.js"(exports2) {
    "use strict";
    Object.defineProperty(exports2, "__esModule", { value: true });
    exports2.createLedger = createLedger;
    exports2.prepareRun = prepareRun;
    exports2.runWorkflow = runWorkflow;
    exports2.resumeWorkflow = resumeWorkflow;
    exports2.approveRunStep = approveRunStep;
    exports2.cancelRun = cancelRun;
    exports2.getRunReceipts = getRunReceipts;
    exports2.getRunStatus = getRunStatus;
    exports2.inspectRun = inspectRun;
    exports2.dryRun = dryRun;
    var shared_1 = require_dist();
    var keyring_1 = require_keyring();
    var compile_1 = require_compile();
    var approval_service_1 = require_approval_service();
    var build_proof_bundle_1 = require_build_proof_bundle();
    var compile_policy_1 = require_compile_policy();
    var resolve_1 = require_resolve();
    var store_1 = require_store();
    var manifests_1 = require_manifests();
    var proof_bundles_1 = require_proof_bundles();
    var policy_artifacts_1 = require_policy_artifacts();
    var receipts_1 = require_receipts2();
    var grant_service_1 = require_grant_service();
    var dispatcher_1 = require_dispatcher();
    var recovery_service_1 = require_recovery_service();
    var scheduler_1 = require_scheduler();
    var receipt_service_1 = require_receipt_service();
    var taskflow_mirror_1 = require_taskflow_mirror();
    var progress_reporter_1 = require_progress_reporter();
    function persistManifest(store, manifest, config = {}) {
      (0, manifests_1.writeManifest)(store, manifest);
      (0, taskflow_mirror_1.syncTaskflowMirror)(store, manifest, config);
    }
    function createLedger(config = {}) {
      return new store_1.LedgerStore((0, resolve_1.resolveConfig)(config).ledgerRoot);
    }
    async function prepareRun(workflowPath, configInput = {}) {
      const config = (0, resolve_1.resolveConfig)(configInput);
      const store = new store_1.LedgerStore(config.ledgerRoot);
      const { source, compiledGraph } = (0, compile_1.compileWorkflowFile)(workflowPath);
      const proofBundle = (0, build_proof_bundle_1.buildProofBundle)(compiledGraph, config);
      const policyArtifact = (0, compile_policy_1.compilePolicyArtifact)(compiledGraph, config);
      const runId = (0, shared_1.newRunId)();
      store.ensureRun(runId);
      const createdAt = (0, shared_1.nowIso)();
      const manifest = {
        schemaVersion: shared_1.RUN_MANIFEST_SCHEMA_VERSION,
        runId,
        workflowName: source.name,
        state: proofBundle.decision === "reject" ? "rejected" : "ready",
        createdAt,
        updatedAt: createdAt,
        workflowHash: compiledGraph.sourceHash,
        graphHash: compiledGraph.graphHash,
        proofHash: proofBundle.proofHash,
        policyHash: policyArtifact.policyHash,
        steps: Object.fromEntries(compiledGraph.nodes.map((node) => [node.id, { id: node.id, state: "pending" }]))
      };
      store.writeJson(store.runPath(runId, "workflow.json"), source);
      store.writeJson(store.runPath(runId, "compiled-graph.json"), compiledGraph);
      (0, proof_bundles_1.writeProofBundle)(store, runId, proofBundle);
      (0, policy_artifacts_1.writePolicyArtifact)(store, runId, policyArtifact);
      persistManifest(store, manifest, config);
      store.appendEvent(runId, "run.prepared", { workflowPath, decision: proofBundle.decision });
      return { runId, manifest };
    }
    async function runWorkflow(workflowPath, configInput = {}) {
      const config = (0, resolve_1.resolveConfig)(configInput);
      const prepared = await prepareRun(workflowPath, config);
      return resumeWorkflow(prepared.runId, config);
    }
    async function resumeWorkflow(runId, configInput = {}) {
      const config = (0, resolve_1.resolveConfig)(configInput);
      const store = new store_1.LedgerStore(config.ledgerRoot);
      let manifest = (0, manifests_1.readManifest)(store, runId);
      if (manifest.state === "running") {
        (0, recovery_service_1.recoverRun)(store, manifest.runId);
        manifest = (0, manifests_1.readManifest)(store, manifest.runId);
      }
      const typedRunId = manifest.runId;
      if (manifest.state === "quarantined")
        throw new Error(`Run ${typedRunId} is quarantined and requires manual review.`);
      if (manifest.state === "cancelled")
        return manifest;
      if (manifest.state === "rejected")
        return manifest;
      const graph = store.readJson(store.runPath(typedRunId, "compiled-graph.json"));
      const policy = store.readJson(store.runPath(typedRunId, "policy-artifact.json"));
      const ordinaryKey = (0, keyring_1.loadRuntimeKey)(store.root);
      const elevatedKey = (0, keyring_1.loadElevatedRuntimeKey)(store.root);
      let currentStepId;
      const progress = (0, progress_reporter_1.createRunProgressMonitor)(config, graph.nodes.length, () => ({ manifest, currentStepId }));
      manifest.state = "running";
      persistManifest(store, manifest, config);
      progress.start();
      try {
        while (true) {
          const runnable = (0, scheduler_1.nextRunnableSteps)(graph, manifest);
          if (!runnable.length)
            break;
          for (const step of runnable) {
            currentStepId = step.id;
            const approval = (0, approval_service_1.getStepApproval)(store, typedRunId, step.id);
            if (step.cell === "elevated" && !approval) {
              manifest.state = "awaiting_approval";
              manifest.steps[step.id].state = "awaiting_approval";
              persistManifest(store, manifest, config);
              store.appendEvent(typedRunId, "run.approval_required", { stepId: step.id, payloadHash: step.payloadHash, policyHash: policy.policyHash });
              progress.onApprovalWait(step.id, manifest);
              return manifest;
            }
            manifest.steps[step.id].state = "grant_issued";
            const stepKey = step.cell === "elevated" ? elevatedKey : ordinaryKey;
            const grant = (0, grant_service_1.mintStepGrant)(store, stepKey, typedRunId, step, policy, config.grantTtlSeconds, approval?.approvalHash);
            manifest.steps[step.id].grantId = grant.grantId;
            manifest.steps[step.id].state = "running";
            manifest.steps[step.id].startedAt = (0, shared_1.nowIso)();
            persistManifest(store, manifest, config);
            progress.onStepStarted(step.id, manifest);
            const { receipt, output } = await (0, dispatcher_1.dispatchStep)(store, policy, stepKey, step, grant);
            const outputPath = store.runPath(typedRunId, "artifacts", `${step.id}.output.json`);
            store.writeJson(outputPath, { receiptId: receipt.receiptId, stepId: step.id, status: receipt.status, output });
            manifest.steps[step.id].outputPath = outputPath;
            (0, receipt_service_1.reconcileReceipt)(manifest, receipt);
            store.appendEvent(typedRunId, "step.receipted", { stepId: step.id, receiptId: receipt.receiptId, status: receipt.status });
            if (receipt.status === "failed") {
              manifest.state = "failed";
              persistManifest(store, manifest, config);
              progress.onRunCompleted(manifest);
              return manifest;
            }
            persistManifest(store, manifest, config);
            progress.onStepCompleted(step.id, manifest);
            currentStepId = void 0;
          }
        }
        if (Object.values(manifest.steps).some((step) => step.state === "awaiting_approval")) {
          manifest.state = "awaiting_approval";
          persistManifest(store, manifest, config);
          progress.onRunCompleted(manifest);
          return manifest;
        }
        manifest.state = Object.values(manifest.steps).every((step) => step.state === "succeeded") ? "succeeded" : "failed";
        persistManifest(store, manifest, config);
        store.appendEvent(typedRunId, "run.completed", { state: manifest.state });
        progress.onRunCompleted(manifest);
        return manifest;
      } finally {
        progress.stop();
      }
    }
    function approveRunStep(runId, stepId, approvedBy = "operator", configInput = {}) {
      const config = (0, resolve_1.resolveConfig)(configInput);
      const store = new store_1.LedgerStore(config.ledgerRoot);
      const manifest = (0, manifests_1.readManifest)(store, runId);
      const typedRunId = manifest.runId;
      const graph = store.readJson(store.runPath(typedRunId, "compiled-graph.json"));
      const policy = store.readJson(store.runPath(typedRunId, "policy-artifact.json"));
      const step = graph.nodes.find((node) => node.id === stepId);
      if (!step)
        throw new Error(`Unknown step "${stepId}".`);
      if (step.cell !== "elevated")
        throw new Error(`Step "${stepId}" does not require elevated approval.`);
      (0, approval_service_1.approveStep)(store, typedRunId, step, policy.policyHash, approvedBy);
      manifest.steps[stepId].state = "pending";
      if (manifest.state === "awaiting_approval")
        manifest.state = "ready";
      persistManifest(store, manifest, config);
      store.appendEvent(typedRunId, "run.approved", { stepId, approvedBy });
      return manifest;
    }
    function cancelRun(runId, reason = "operator_cancelled", configInput = {}) {
      const store = createLedger(configInput);
      const manifest = (0, manifests_1.readManifest)(store, runId);
      if (["succeeded", "failed", "rejected", "cancelled"].includes(manifest.state))
        return manifest;
      for (const step of Object.values(manifest.steps)) {
        if (["pending", "awaiting_approval", "grant_issued", "running"].includes(step.state)) {
          step.state = "cancelled";
          step.error = reason;
        }
      }
      manifest.state = "cancelled";
      persistManifest(store, manifest, configInput);
      store.appendEvent(manifest.runId, "run.cancelled", { reason });
      return manifest;
    }
    function getRunReceipts(runId, configInput = {}) {
      const store = createLedger(configInput);
      const id = runId ?? store.latestRunId();
      if (!id)
        throw new Error("No ToolFlow runs found.");
      return { runId: id, receipts: (0, receipts_1.listReceipts)(store, id) };
    }
    function getRunStatus(runId, configInput = {}) {
      const store = createLedger(configInput);
      const id = runId ?? store.latestRunId();
      if (!id)
        throw new Error("No ToolFlow runs found.");
      return (0, manifests_1.readManifest)(store, id);
    }
    function inspectRun(runId, configInput = {}) {
      const store = createLedger(configInput);
      const manifest = getRunStatus(runId, configInput);
      return {
        manifest,
        compiledGraph: store.readJson(store.runPath(manifest.runId, "compiled-graph.json")),
        proofBundle: store.readJson(store.runPath(manifest.runId, "proof-bundle.json")),
        policyArtifact: store.readJson(store.runPath(manifest.runId, "policy-artifact.json"))
      };
    }
    function dryRun(workflowPath) {
      const config = (0, resolve_1.resolveConfig)();
      const { compiledGraph } = (0, compile_1.compileWorkflowFile)(workflowPath);
      const proofBundle = (0, build_proof_bundle_1.buildProofBundle)(compiledGraph, config);
      const policyArtifact = (0, compile_policy_1.compilePolicyArtifact)(compiledGraph, config);
      return { compiledGraph, proofBundle, policyArtifact, summaryHash: (0, shared_1.hashJson)({ graph: compiledGraph.graphHash, proof: proofBundle.proofHash, policy: policyArtifact.policyHash }) };
    }
  }
});

// packages/runtime/dist/control-plane/taskflow-controller.js
var require_taskflow_controller = __commonJS({
  "packages/runtime/dist/control-plane/taskflow-controller.js"(exports2) {
    "use strict";
    Object.defineProperty(exports2, "__esModule", { value: true });
    exports2.createControllerFlow = createControllerFlow;
    exports2.readControllerFlow = readControllerFlow;
    exports2.listControllerFlows = listControllerFlows;
    exports2.launchControllerWorkflow = launchControllerWorkflow;
    exports2.reconcileControllerFlow = reconcileControllerFlow;
    exports2.updateControllerFlow = updateControllerFlow;
    exports2.controllerStatus = controllerStatus;
    var node_fs_1 = require("node:fs");
    var node_path_1 = require("node:path");
    var shared_1 = require_dist();
    var resolve_1 = require_resolve();
    var run_service_1 = require_run_service();
    var taskflow_mirror_1 = require_taskflow_mirror();
    function controllerRoot(config) {
      return (0, node_path_1.join)(config.taskflowMirrorRoot, "controller");
    }
    function flowDir(config) {
      return (0, node_path_1.join)(controllerRoot(config), "flows");
    }
    function flowPath(config, flowId) {
      return (0, node_path_1.join)(flowDir(config), `${flowId}.json`);
    }
    function indexPath(config) {
      return (0, node_path_1.join)(controllerRoot(config), "index.json");
    }
    function ensureControllerRoot(config) {
      (0, node_fs_1.mkdirSync)(flowDir(config), { recursive: true });
    }
    function newFlowId() {
      return `tfc_${Math.random().toString(16).slice(2, 14)}`;
    }
    function readIndex(config) {
      ensureControllerRoot(config);
      try {
        return JSON.parse((0, node_fs_1.readFileSync)(indexPath(config), "utf8"));
      } catch {
        return {
          schemaVersion: "toolflow.taskflow-controller-index/v1",
          updatedAt: (0, shared_1.nowIso)(),
          flows: []
        };
      }
    }
    function writeIndex(config, index) {
      (0, node_fs_1.writeFileSync)(indexPath(config), `${JSON.stringify(index, null, 2)}
`);
    }
    function upsertIndex(config, flow) {
      const index = readIndex(config);
      index.updatedAt = flow.updatedAt;
      index.flows = index.flows.filter((item) => item.flowId !== flow.flowId);
      index.flows.push({
        flowId: flow.flowId,
        goal: flow.goal,
        status: flow.status,
        currentStep: flow.currentStep,
        updatedAt: flow.updatedAt
      });
      index.flows.sort((a, b) => a.updatedAt.localeCompare(b.updatedAt));
      writeIndex(config, index);
    }
    function saveFlow(config, flow) {
      ensureControllerRoot(config);
      (0, node_fs_1.writeFileSync)(flowPath(config, flow.flowId), `${JSON.stringify(flow, null, 2)}
`);
      upsertIndex(config, flow);
      return flow;
    }
    function createControllerFlow(input, configInput = {}) {
      const config = (0, resolve_1.resolveConfig)(configInput);
      const timestamp = (0, shared_1.nowIso)();
      const flow = {
        schemaVersion: "toolflow.taskflow-controller/v1",
        flowId: newFlowId(),
        goal: input.goal,
        doneDefinition: input.doneDefinition,
        blockerDefinition: input.blockerDefinition,
        controllerId: input.controllerId,
        status: "running",
        currentStep: input.currentStep,
        nextAction: input.nextAction,
        linkedRuns: [],
        artifacts: input.artifacts ?? [],
        createdAt: timestamp,
        updatedAt: timestamp,
        lastMaterialProgressAt: timestamp
      };
      return saveFlow(config, flow);
    }
    function readControllerFlow(flowId, configInput = {}) {
      const config = (0, resolve_1.resolveConfig)(configInput);
      return JSON.parse((0, node_fs_1.readFileSync)(flowPath(config, flowId), "utf8"));
    }
    function listControllerFlows(configInput = {}) {
      const config = (0, resolve_1.resolveConfig)(configInput);
      return readIndex(config);
    }
    async function launchControllerWorkflow(input, configInput = {}) {
      const config = (0, resolve_1.resolveConfig)(configInput);
      const flow = readControllerFlow(input.flowId, config);
      const manifest = await (0, run_service_1.runWorkflow)(input.workflowPath, config);
      const mirror = (0, taskflow_mirror_1.syncTaskflowMirrorFromLedger)(manifest.runId, config);
      flow.linkedRuns.push({
        runId: manifest.runId,
        workflowPath: input.workflowPath,
        purpose: input.purpose,
        runState: manifest.state,
        mirroredTaskflowState: mirror.mirroredTaskflowState,
        attachedAt: (0, shared_1.nowIso)(),
        updatedAt: manifest.updatedAt
      });
      flow.currentStep = `toolflow:${manifest.workflowName}`;
      flow.nextAction = manifest.state === "succeeded" ? `Review linked ToolFlow run ${manifest.runId} and decide the next orchestration step.` : `Monitor linked ToolFlow run ${manifest.runId}.`;
      flow.updatedAt = (0, shared_1.nowIso)();
      flow.lastMaterialProgressAt = flow.updatedAt;
      return saveFlow(config, flow);
    }
    function reconcileControllerFlow(flowId, configInput = {}) {
      const config = (0, resolve_1.resolveConfig)(configInput);
      const flow = readControllerFlow(flowId, config);
      for (const linked of flow.linkedRuns) {
        const mirror = (0, taskflow_mirror_1.readTaskflowMirror)(linked.runId, config);
        linked.runState = mirror.runState;
        linked.mirroredTaskflowState = mirror.mirroredTaskflowState;
        linked.updatedAt = mirror.updatedAt;
        if (mirror.mirroredTaskflowState === "waiting") {
          flow.status = "waiting";
          flow.currentStep = mirror.currentStep ?? flow.currentStep;
          flow.nextAction = mirror.waitingOn?.reason ?? `Await approval or wake for run ${linked.runId}.`;
          flow.waitJson = mirror.waitingOn;
        } else if (mirror.mirroredTaskflowState === "blocked") {
          flow.status = "blocked";
          flow.currentStep = mirror.currentStep ?? flow.currentStep;
          flow.nextAction = `Review blocked ToolFlow run ${linked.runId}.`;
          flow.blockedSummary = mirror.blockedSummary ?? `Linked run ${linked.runId} is blocked.`;
        } else if (mirror.mirroredTaskflowState === "done") {
          flow.status = "running";
          flow.nextAction = `Linked run ${linked.runId} finished. Evaluate completion or schedule the next workflow.`;
          flow.waitJson = void 0;
        } else if (mirror.mirroredTaskflowState === "cancelled") {
          flow.status = "cancelled";
          flow.terminalSummary = `Linked run ${linked.runId} was cancelled.`;
        }
      }
      flow.updatedAt = (0, shared_1.nowIso)();
      return saveFlow(config, flow);
    }
    function updateControllerFlow(flowId, patch, configInput = {}) {
      const config = (0, resolve_1.resolveConfig)(configInput);
      const flow = readControllerFlow(flowId, config);
      Object.assign(flow, patch);
      flow.updatedAt = (0, shared_1.nowIso)();
      flow.lastMaterialProgressAt = flow.updatedAt;
      return saveFlow(config, flow);
    }
    function controllerStatus(configInput = {}) {
      const config = (0, resolve_1.resolveConfig)(configInput);
      ensureControllerRoot(config);
      const index = readIndex(config);
      const flowCount = (0, node_fs_1.readdirSync)(flowDir(config), { withFileTypes: true }).filter((entry) => entry.isFile() && entry.name.endsWith(".json")).length;
      return {
        status: "enabled",
        root: controllerRoot(config),
        flowCount,
        latestFlow: index.flows.at(-1),
        updatedAt: index.updatedAt
      };
    }
  }
});

// packages/runtime/dist/api/runtime-api.js
var require_runtime_api = __commonJS({
  "packages/runtime/dist/api/runtime-api.js"(exports2) {
    "use strict";
    Object.defineProperty(exports2, "__esModule", { value: true });
    exports2.taskflowMirrorStatus = exports2.syncTaskflowMirrorFromLedger = exports2.readTaskflowMirror = exports2.updateControllerFlow = exports2.reconcileControllerFlow = exports2.readControllerFlow = exports2.listControllerFlows = exports2.launchControllerWorkflow = exports2.createControllerFlow = exports2.controllerStatus = exports2.runWorkflow = exports2.resumeWorkflow = exports2.prepareRun = exports2.inspectRun = exports2.getRunReceipts = exports2.dryRun = exports2.cancelRun = exports2.approveRunStep = void 0;
    var run_service_1 = require_run_service();
    Object.defineProperty(exports2, "approveRunStep", { enumerable: true, get: function() {
      return run_service_1.approveRunStep;
    } });
    Object.defineProperty(exports2, "cancelRun", { enumerable: true, get: function() {
      return run_service_1.cancelRun;
    } });
    Object.defineProperty(exports2, "dryRun", { enumerable: true, get: function() {
      return run_service_1.dryRun;
    } });
    Object.defineProperty(exports2, "getRunReceipts", { enumerable: true, get: function() {
      return run_service_1.getRunReceipts;
    } });
    Object.defineProperty(exports2, "inspectRun", { enumerable: true, get: function() {
      return run_service_1.inspectRun;
    } });
    Object.defineProperty(exports2, "prepareRun", { enumerable: true, get: function() {
      return run_service_1.prepareRun;
    } });
    Object.defineProperty(exports2, "resumeWorkflow", { enumerable: true, get: function() {
      return run_service_1.resumeWorkflow;
    } });
    Object.defineProperty(exports2, "runWorkflow", { enumerable: true, get: function() {
      return run_service_1.runWorkflow;
    } });
    var taskflow_controller_1 = require_taskflow_controller();
    Object.defineProperty(exports2, "controllerStatus", { enumerable: true, get: function() {
      return taskflow_controller_1.controllerStatus;
    } });
    Object.defineProperty(exports2, "createControllerFlow", { enumerable: true, get: function() {
      return taskflow_controller_1.createControllerFlow;
    } });
    Object.defineProperty(exports2, "launchControllerWorkflow", { enumerable: true, get: function() {
      return taskflow_controller_1.launchControllerWorkflow;
    } });
    Object.defineProperty(exports2, "listControllerFlows", { enumerable: true, get: function() {
      return taskflow_controller_1.listControllerFlows;
    } });
    Object.defineProperty(exports2, "readControllerFlow", { enumerable: true, get: function() {
      return taskflow_controller_1.readControllerFlow;
    } });
    Object.defineProperty(exports2, "reconcileControllerFlow", { enumerable: true, get: function() {
      return taskflow_controller_1.reconcileControllerFlow;
    } });
    Object.defineProperty(exports2, "updateControllerFlow", { enumerable: true, get: function() {
      return taskflow_controller_1.updateControllerFlow;
    } });
    var taskflow_mirror_1 = require_taskflow_mirror();
    Object.defineProperty(exports2, "readTaskflowMirror", { enumerable: true, get: function() {
      return taskflow_mirror_1.readTaskflowMirror;
    } });
    Object.defineProperty(exports2, "syncTaskflowMirrorFromLedger", { enumerable: true, get: function() {
      return taskflow_mirror_1.syncTaskflowMirrorFromLedger;
    } });
    Object.defineProperty(exports2, "taskflowMirrorStatus", { enumerable: true, get: function() {
      return taskflow_mirror_1.taskflowMirrorStatus;
    } });
  }
});

// packages/runtime/dist/api/status-api.js
var require_status_api = __commonJS({
  "packages/runtime/dist/api/status-api.js"(exports2) {
    "use strict";
    Object.defineProperty(exports2, "__esModule", { value: true });
    exports2.taskflowMirrorStatus = exports2.readTaskflowMirror = exports2.readControllerFlow = exports2.listControllerFlows = exports2.controllerStatus = exports2.inspectRun = exports2.getRunStatus = exports2.getRunReceipts = void 0;
    var run_service_1 = require_run_service();
    Object.defineProperty(exports2, "getRunReceipts", { enumerable: true, get: function() {
      return run_service_1.getRunReceipts;
    } });
    Object.defineProperty(exports2, "getRunStatus", { enumerable: true, get: function() {
      return run_service_1.getRunStatus;
    } });
    Object.defineProperty(exports2, "inspectRun", { enumerable: true, get: function() {
      return run_service_1.inspectRun;
    } });
    var taskflow_controller_1 = require_taskflow_controller();
    Object.defineProperty(exports2, "controllerStatus", { enumerable: true, get: function() {
      return taskflow_controller_1.controllerStatus;
    } });
    Object.defineProperty(exports2, "listControllerFlows", { enumerable: true, get: function() {
      return taskflow_controller_1.listControllerFlows;
    } });
    Object.defineProperty(exports2, "readControllerFlow", { enumerable: true, get: function() {
      return taskflow_controller_1.readControllerFlow;
    } });
    var taskflow_mirror_1 = require_taskflow_mirror();
    Object.defineProperty(exports2, "readTaskflowMirror", { enumerable: true, get: function() {
      return taskflow_mirror_1.readTaskflowMirror;
    } });
    Object.defineProperty(exports2, "taskflowMirrorStatus", { enumerable: true, get: function() {
      return taskflow_mirror_1.taskflowMirrorStatus;
    } });
  }
});

// packages/runtime/dist/index.js
var require_dist2 = __commonJS({
  "packages/runtime/dist/index.js"(exports2) {
    "use strict";
    var __createBinding2 = exports2 && exports2.__createBinding || (Object.create ? (function(o, m, k, k2) {
      if (k2 === void 0) k2 = k;
      var desc = Object.getOwnPropertyDescriptor(m, k);
      if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
        desc = { enumerable: true, get: function() {
          return m[k];
        } };
      }
      Object.defineProperty(o, k2, desc);
    }) : (function(o, m, k, k2) {
      if (k2 === void 0) k2 = k;
      o[k2] = m[k];
    }));
    var __exportStar2 = exports2 && exports2.__exportStar || function(m, exports3) {
      for (var p in m) if (p !== "default" && !Object.prototype.hasOwnProperty.call(exports3, p)) __createBinding2(exports3, m, p);
    };
    Object.defineProperty(exports2, "__esModule", { value: true });
    __exportStar2(require_runtime_api(), exports2);
    __exportStar2(require_status_api(), exports2);
    __exportStar2(require_compile(), exports2);
    __exportStar2(require_build_proof_bundle(), exports2);
    __exportStar2(require_compile_policy(), exports2);
    __exportStar2(require_approval_service(), exports2);
    __exportStar2(require_recovery_service(), exports2);
    __exportStar2(require_run_service(), exports2);
  }
});

// packages/plugin/dist/client/runtime-client.js
var require_runtime_client = __commonJS({
  "packages/plugin/dist/client/runtime-client.js"(exports2) {
    "use strict";
    Object.defineProperty(exports2, "__esModule", { value: true });
    exports2.createRuntimeClient = createRuntimeClient;
    var node_path_1 = require("node:path");
    var runtime_1 = require_dist2();
    var defaultLedgerRoot = (0, node_path_1.resolve)(__dirname, "../../data/ledger");
    var defaultTaskflowMirrorRoot = (0, node_path_1.resolve)(__dirname, "../../data/taskflow-mirror");
    function createRuntimeClient(config = {}) {
      const runtimeConfig = {
        ledgerRoot: config.ledgerRoot ?? defaultLedgerRoot,
        taskflowMirrorRoot: config.taskflowMirrorRoot ?? defaultTaskflowMirrorRoot,
        enableElevated: config.enableElevated,
        elevatedAllowedCommands: config.elevatedAllowedCommands,
        progressUpdates: {
          enabled: true,
          longRunThresholdMs: 5 * 60 * 1e3,
          intervalMs: 5 * 60 * 1e3,
          sink: "stderr",
          ...config.progressUpdates
        }
      };
      return {
        submit: (workflowPath) => (0, runtime_1.runWorkflow)(workflowPath, runtimeConfig),
        dryRun: (workflowPath) => (0, runtime_1.dryRun)(workflowPath),
        status: (runId) => (0, runtime_1.getRunStatus)(runId, runtimeConfig),
        inspect: (runId) => (0, runtime_1.inspectRun)(runId, runtimeConfig),
        receipts: (runId) => (0, runtime_1.getRunReceipts)(runId, runtimeConfig),
        approve: (runId, stepId, approvedBy) => (0, runtime_1.approveRunStep)(runId, stepId, approvedBy, runtimeConfig),
        cancel: (runId, reason) => (0, runtime_1.cancelRun)(runId, reason, runtimeConfig),
        resume: (runId) => (0, runtime_1.resumeWorkflow)(runId, runtimeConfig),
        recover: (runId) => (0, runtime_1.recoverRun)((0, runtime_1.createLedger)(runtimeConfig), runId),
        taskflowMirrorStatus: () => (0, runtime_1.taskflowMirrorStatus)(runtimeConfig),
        readTaskflowMirror: (runId) => (0, runtime_1.readTaskflowMirror)(runId, runtimeConfig),
        controllerStatus: () => (0, runtime_1.controllerStatus)(runtimeConfig),
        createControllerFlow: (input) => (0, runtime_1.createControllerFlow)(input, runtimeConfig),
        readControllerFlow: (flowId) => (0, runtime_1.readControllerFlow)(flowId, runtimeConfig),
        listControllerFlows: () => (0, runtime_1.listControllerFlows)(runtimeConfig),
        launchControllerWorkflow: (input) => (0, runtime_1.launchControllerWorkflow)(input, runtimeConfig),
        reconcileControllerFlow: (flowId) => (0, runtime_1.reconcileControllerFlow)(flowId, runtimeConfig),
        updateControllerFlow: (flowId, patch) => (0, runtime_1.updateControllerFlow)(flowId, patch, runtimeConfig)
      };
    }
  }
});

// packages/plugin/dist/config-schema.js
var require_config_schema = __commonJS({
  "packages/plugin/dist/config-schema.js"(exports2) {
    "use strict";
    Object.defineProperty(exports2, "__esModule", { value: true });
  }
});

// packages/plugin/dist/gateway/methods.js
var require_methods = __commonJS({
  "packages/plugin/dist/gateway/methods.js"(exports2) {
    "use strict";
    Object.defineProperty(exports2, "__esModule", { value: true });
    exports2.gatewayMethods = void 0;
    var runtime_client_12 = require_runtime_client();
    exports2.gatewayMethods = {
      toolflow_submit: (workflowPath) => (0, runtime_client_12.createRuntimeClient)().submit(workflowPath),
      toolflow_dry_run: (workflowPath) => (0, runtime_client_12.createRuntimeClient)().dryRun(workflowPath),
      toolflow_status: (runId) => (0, runtime_client_12.createRuntimeClient)().status(runId),
      toolflow_inspect: (runId) => (0, runtime_client_12.createRuntimeClient)().inspect(runId),
      toolflow_receipts: (runId) => (0, runtime_client_12.createRuntimeClient)().receipts(runId),
      toolflow_cancel: (runId, reason) => (0, runtime_client_12.createRuntimeClient)().cancel(runId, reason),
      toolflow_recover: (runId) => (0, runtime_client_12.createRuntimeClient)().recover(runId),
      toolflow_taskflow_mirror_status: () => (0, runtime_client_12.createRuntimeClient)().taskflowMirrorStatus(),
      toolflow_taskflow_mirror_read: (runId) => (0, runtime_client_12.createRuntimeClient)().readTaskflowMirror(runId),
      toolflow_controller_status: () => (0, runtime_client_12.createRuntimeClient)().controllerStatus(),
      toolflow_controller_create: (input) => (0, runtime_client_12.createRuntimeClient)().createControllerFlow(input),
      toolflow_controller_read: (flowId) => (0, runtime_client_12.createRuntimeClient)().readControllerFlow(flowId),
      toolflow_controller_list: () => (0, runtime_client_12.createRuntimeClient)().listControllerFlows(),
      toolflow_controller_launch: (input) => (0, runtime_client_12.createRuntimeClient)().launchControllerWorkflow(input),
      toolflow_controller_reconcile: (flowId) => (0, runtime_client_12.createRuntimeClient)().reconcileControllerFlow(flowId)
    };
  }
});

// packages/plugin/dist/runtime-store.js
var require_runtime_store = __commonJS({
  "packages/plugin/dist/runtime-store.js"(exports2) {
    "use strict";
    Object.defineProperty(exports2, "__esModule", { value: true });
    exports2.resolvePluginRuntimeStore = resolvePluginRuntimeStore;
    function resolvePluginRuntimeStore(config = {}) {
      return { ledgerRoot: config.ledgerRoot ?? process.env.TOOLFLOW_LEDGER_DIR ?? "data/ledger" };
    }
  }
});

// packages/plugin/dist/services/runtime-supervisor.js
var require_runtime_supervisor = __commonJS({
  "packages/plugin/dist/services/runtime-supervisor.js"(exports2) {
    "use strict";
    Object.defineProperty(exports2, "__esModule", { value: true });
    exports2.runtimeSupervisorStatus = runtimeSupervisorStatus;
    var runtime_store_1 = require_runtime_store();
    function runtimeSupervisorStatus(config = {}) {
      return {
        ok: true,
        mode: "in-process",
        store: (0, runtime_store_1.resolvePluginRuntimeStore)(config)
      };
    }
  }
});

// packages/plugin/dist/tools/toolflow_cancel.js
var require_toolflow_cancel = __commonJS({
  "packages/plugin/dist/tools/toolflow_cancel.js"(exports2) {
    "use strict";
    Object.defineProperty(exports2, "__esModule", { value: true });
    exports2.toolflow_cancel = toolflow_cancel;
    var runtime_client_12 = require_runtime_client();
    function toolflow_cancel(runId, reason) {
      return (0, runtime_client_12.createRuntimeClient)().cancel(runId, reason);
    }
  }
});

// packages/plugin/dist/tools/toolflow_dry_run.js
var require_toolflow_dry_run = __commonJS({
  "packages/plugin/dist/tools/toolflow_dry_run.js"(exports2) {
    "use strict";
    Object.defineProperty(exports2, "__esModule", { value: true });
    exports2.toolflow_dry_run = toolflow_dry_run;
    var runtime_client_12 = require_runtime_client();
    function toolflow_dry_run(workflowPath) {
      return (0, runtime_client_12.createRuntimeClient)().dryRun(workflowPath);
    }
  }
});

// packages/plugin/dist/tools/toolflow_inspect.js
var require_toolflow_inspect = __commonJS({
  "packages/plugin/dist/tools/toolflow_inspect.js"(exports2) {
    "use strict";
    Object.defineProperty(exports2, "__esModule", { value: true });
    exports2.toolflow_inspect = toolflow_inspect;
    var runtime_client_12 = require_runtime_client();
    function toolflow_inspect(runId) {
      return (0, runtime_client_12.createRuntimeClient)().inspect(runId);
    }
  }
});

// packages/plugin/dist/tools/toolflow_receipts.js
var require_toolflow_receipts = __commonJS({
  "packages/plugin/dist/tools/toolflow_receipts.js"(exports2) {
    "use strict";
    Object.defineProperty(exports2, "__esModule", { value: true });
    exports2.toolflow_receipts = toolflow_receipts;
    var runtime_client_12 = require_runtime_client();
    function toolflow_receipts(runId) {
      return (0, runtime_client_12.createRuntimeClient)().receipts(runId);
    }
  }
});

// packages/plugin/dist/tools/toolflow_status.js
var require_toolflow_status = __commonJS({
  "packages/plugin/dist/tools/toolflow_status.js"(exports2) {
    "use strict";
    Object.defineProperty(exports2, "__esModule", { value: true });
    exports2.toolflow_status = toolflow_status;
    var runtime_client_12 = require_runtime_client();
    function toolflow_status(runId) {
      return (0, runtime_client_12.createRuntimeClient)().status(runId);
    }
  }
});

// packages/plugin/dist/tools/toolflow_submit.js
var require_toolflow_submit = __commonJS({
  "packages/plugin/dist/tools/toolflow_submit.js"(exports2) {
    "use strict";
    Object.defineProperty(exports2, "__esModule", { value: true });
    exports2.toolflow_submit = toolflow_submit;
    var runtime_client_12 = require_runtime_client();
    function toolflow_submit(workflowPath) {
      return (0, runtime_client_12.createRuntimeClient)().submit(workflowPath);
    }
  }
});

// packages/plugin/dist/tools/toolflow_templates.js
var require_toolflow_templates = __commonJS({
  "packages/plugin/dist/tools/toolflow_templates.js"(exports2) {
    "use strict";
    Object.defineProperty(exports2, "__esModule", { value: true });
    exports2.toolflow_templates = toolflow_templates;
    var node_path_1 = require("node:path");
    function toolflow_templates() {
      return {
        templates: [
          (0, node_path_1.resolve)(__dirname, "../../examples/workflows/safe-profile-mvp.json")
        ]
      };
    }
  }
});

// packages/plugin/dist/entry.js
var __createBinding = exports && exports.__createBinding || (Object.create ? (function(o, m, k, k2) {
  if (k2 === void 0) k2 = k;
  var desc = Object.getOwnPropertyDescriptor(m, k);
  if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
    desc = { enumerable: true, get: function() {
      return m[k];
    } };
  }
  Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
  if (k2 === void 0) k2 = k;
  o[k2] = m[k];
}));
var __exportStar = exports && exports.__exportStar || function(m, exports2) {
  for (var p in m) if (p !== "default" && !Object.prototype.hasOwnProperty.call(exports2, p)) __createBinding(exports2, m, p);
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.default = register;
var runtime_client_1 = require_runtime_client();
__exportStar(require_runtime_client(), exports);
__exportStar(require_config_schema(), exports);
__exportStar(require_methods(), exports);
__exportStar(require_runtime_store(), exports);
__exportStar(require_runtime_supervisor(), exports);
__exportStar(require_toolflow_cancel(), exports);
__exportStar(require_toolflow_dry_run(), exports);
__exportStar(require_toolflow_inspect(), exports);
__exportStar(require_toolflow_receipts(), exports);
__exportStar(require_toolflow_status(), exports);
__exportStar(require_toolflow_submit(), exports);
__exportStar(require_toolflow_templates(), exports);
var toolflow_templates_1 = require_toolflow_templates();
function textResult(data) {
  return { content: [{ type: "text", text: JSON.stringify(data, null, 2) }], details: {} };
}
function errorResult(message) {
  return { content: [{ type: "text", text: `Error: ${message}` }], details: {} };
}
function register(api) {
  api.logger.info("ToolFlow plugin loaded");
  const getClient = () => (0, runtime_client_1.createRuntimeClient)(api.pluginConfig ?? {});
  const tools = [
    {
      name: "toolflow_submit",
      label: "ToolFlow Submit",
      description: "Run a ToolFlow workflow from a workflow path.",
      parameters: {
        type: "object",
        properties: {
          workflowPath: { type: "string", description: "Path to the ToolFlow workflow file." }
        },
        required: ["workflowPath"]
      },
      async execute(_toolCallId, params) {
        try {
          return textResult(await getClient().submit(params.workflowPath));
        } catch (error) {
          return errorResult(error.message);
        }
      }
    },
    {
      name: "toolflow_dry_run",
      label: "ToolFlow Dry Run",
      description: "Compile and classify a ToolFlow workflow without running it.",
      parameters: {
        type: "object",
        properties: {
          workflowPath: { type: "string", description: "Path to the ToolFlow workflow file." }
        },
        required: ["workflowPath"]
      },
      async execute(_toolCallId, params) {
        try {
          return textResult(getClient().dryRun(params.workflowPath));
        } catch (error) {
          return errorResult(error.message);
        }
      }
    },
    {
      name: "toolflow_status",
      label: "ToolFlow Status",
      description: "Read ToolFlow run status for a specific run or the latest run.",
      parameters: {
        type: "object",
        properties: {
          runId: { type: "string", description: "Optional ToolFlow run id." }
        },
        required: []
      },
      async execute(_toolCallId, params) {
        try {
          return textResult(getClient().status(params.runId));
        } catch (error) {
          return errorResult(error.message);
        }
      }
    },
    {
      name: "toolflow_inspect",
      label: "ToolFlow Inspect",
      description: "Inspect ToolFlow manifest, graph, proof bundle, and policy artifact.",
      parameters: {
        type: "object",
        properties: {
          runId: { type: "string", description: "Optional ToolFlow run id." }
        },
        required: []
      },
      async execute(_toolCallId, params) {
        try {
          return textResult(getClient().inspect(params.runId));
        } catch (error) {
          return errorResult(error.message);
        }
      }
    },
    {
      name: "toolflow_receipts",
      label: "ToolFlow Receipts",
      description: "List authoritative receipts for a ToolFlow run.",
      parameters: {
        type: "object",
        properties: {
          runId: { type: "string", description: "Optional ToolFlow run id." }
        },
        required: []
      },
      async execute(_toolCallId, params) {
        try {
          return textResult(getClient().receipts(params.runId));
        } catch (error) {
          return errorResult(error.message);
        }
      }
    },
    {
      name: "toolflow_cancel",
      label: "ToolFlow Cancel",
      description: "Cancel a ToolFlow run.",
      parameters: {
        type: "object",
        properties: {
          runId: { type: "string", description: "ToolFlow run id." },
          reason: { type: "string", description: "Optional cancellation reason." }
        },
        required: ["runId"]
      },
      async execute(_toolCallId, params) {
        try {
          return textResult(getClient().cancel(params.runId, params.reason));
        } catch (error) {
          return errorResult(error.message);
        }
      }
    },
    {
      name: "toolflow_templates",
      label: "ToolFlow Templates",
      description: "List packaged ToolFlow workflow templates.",
      parameters: { type: "object", properties: {}, required: [] },
      async execute() {
        try {
          return textResult((0, toolflow_templates_1.toolflow_templates)());
        } catch (error) {
          return errorResult(error.message);
        }
      }
    }
  ];
  for (const tool of tools) {
    api.registerTool(tool, { name: tool.name });
  }
  api.registerService({
    id: "toolflow",
    start: () => {
      api.logger.info("ToolFlow service started");
    },
    stop: () => {
      api.logger.info("ToolFlow service stopped");
    }
  });
}
//# sourceMappingURL=entry.js.map
