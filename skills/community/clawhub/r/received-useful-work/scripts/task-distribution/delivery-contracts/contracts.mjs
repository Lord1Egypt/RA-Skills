import { createHash } from "node:crypto";

export class DeliveryContractError extends Error {
  constructor(code, message) { super(message); this.name = "DeliveryContractError"; this.code = code; }
}
function refuse(code, message) { throw new DeliveryContractError(code, message); }
export function canonicalJson(value) {
  let nodes = 0;
  const ancestors = new Set();
  function visit(v, depth) {
    if (++nodes > 10000 || depth > 40) refuse("input_limit", "canonical input is too large");
    if (v === null || typeof v === "boolean" || typeof v === "string") return JSON.stringify(v);
    if (typeof v === "number" && Number.isFinite(v)) return JSON.stringify(v);
    if (typeof v !== "object" || ancestors.has(v)) refuse("non_json", "expected acyclic JSON values");
    if (Object.getOwnPropertySymbols(v).length) refuse("non_json", "symbol keys are unsupported");
    ancestors.add(v);
    let result;
    if (Array.isArray(v)) {
      if (Object.keys(v).length !== v.length || Array.from({length:v.length}, (_,i)=>i).some(i=>!Object.hasOwn(v,i)))
        refuse("non_json", "expected a dense JSON array");
      if (Array.from({length:v.length}, (_,i)=>i).some(i=>!Object.hasOwn(Object.getOwnPropertyDescriptor(v,String(i)), "value")))
        refuse("non_json", "array accessors are unsupported");
      result = "[" + v.map(item => visit(item, depth + 1)).join(",") + "]";
    } else {
      if (![Object.prototype, null].includes(Object.getPrototypeOf(v))) refuse("non_json", "expected a plain JSON object");
      const keys = Object.keys(v).sort();
      const descriptors = Object.getOwnPropertyDescriptors(v);
      if (keys.some(key => !Object.hasOwn(descriptors[key], "value"))) refuse("non_json", "accessors are unsupported");
      result = "{" + keys.map(key => JSON.stringify(key) + ":" + visit(descriptors[key].value, depth + 1)).join(",") + "}";
    }
    ancestors.delete(v);
    return result;
  }
  const encoded = visit(value, 0);
  if (Buffer.byteLength(encoded) > 65536) refuse("input_limit", "canonical input exceeds 64KiB");
  return encoded;
}
export function digestOf(value) { return createHash("sha256").update(canonicalJson(value)).digest("hex"); }
const requestFields = ["taskId", "operation", "functionId", "version", "callerInputs", "expectedOutput", "context", "contract", "executionMode"];
export function requestIdentity(request) {
  if (!request || typeof request !== "object" || Array.isArray(request)) refuse("request_missing", "request is required");
  const normalized = { schema: "neomorphic.delivery-request.v1" };
  for (const field of requestFields) {
    if (!Object.hasOwn(request, field) || request[field] === undefined) refuse("request_missing", "missing request field: " + field);
    normalized[field] = request[field];
  }
  for (const field of ["taskId", "operation", "functionId", "version", "executionMode"])
    if (typeof normalized[field] !== "string" || !normalized[field].trim()) refuse("request_missing", "nonempty request field: " + field);
  if (normalized.callerInputs === null || normalized.expectedOutput === null || normalized.context === null || normalized.contract === null)
    refuse("request_missing", "input, output, context and contract must be explicit");
  return digestOf(normalized);
}
export function observationIdentity(observation) {
  if (!observation || !/^[a-f0-9]{64}$/.test(observation.requestIdentity || "") ||
      typeof observation.attemptId !== "string" || !observation.attemptId ||
      !["success", "failed", "refused"].includes(observation.outcome) || !Object.hasOwn(observation, "result"))
    refuse("observation_missing", "request, attempt, outcome and result are required");
  return digestOf({schema:"neomorphic.delivery-observation.v1", requestIdentity:observation.requestIdentity,
    attemptId:observation.attemptId, outcome:observation.outcome, exit:observation.exit,
    failure:observation.failure ?? null, result:observation.result});
}
// Only caller-owned, validated execution records belong in this collection.
// This selector is not a proof verifier, grant issuer or customer-usefulness classifier.
export function selectSuccessfulObservation(records, request, { attemptId } = {}) {
  if (!Array.isArray(records) || records.length > 10000) refuse("evidence_limit", "bounded observation records are required");
  const identity = requestIdentity(request);
  const matching = records.filter(row => row && row.kind === "observed_output" && row.requestIdentity === identity &&
    (attemptId === undefined || row.attemptId === attemptId));
  if (!matching.length) return {ok:false, code:"missing_evidence", requestIdentity:identity};
  if (matching.length !== 1) return {ok:false, code:"ambiguous_evidence", requestIdentity:identity};
  const row = matching[0];
  if (row.outcome !== "success" || row.exit !== 0 || row.failure != null || row.result == null)
    return {ok:false, code:"execution_not_successful", requestIdentity:identity};
  const observation = observationIdentity(row);
  if (row.observationIdentity !== observation) return {ok:false, code:"observation_mismatch", requestIdentity:identity};
  return {ok:true, requestIdentity:identity, observationIdentity:observation, attemptId:row.attemptId,
    result:row.result, useful:null, settlement:null, laterUse:null};
}
export function createOutputBudget(limit) {
  if (!Number.isSafeInteger(limit) || limit < 0) refuse("budget_invalid", "output limit must be a nonnegative safe integer");
  let consumed = 0;
  let exhausted = false;
  return Object.freeze({
    charge(bytes) {
      const size = typeof bytes === "number" ? bytes : Buffer.isBuffer(bytes) || typeof bytes === "string" ? Buffer.byteLength(bytes) : NaN;
      if (!Number.isSafeInteger(size) || size < 0) refuse("budget_invalid", "charge needs a byte count or bytes");
      if (exhausted || size > limit - consumed) {
        exhausted = true;
        refuse("output_budget", "operation output budget exhausted");
      }
      consumed += size;
      return {limit, consumed, remaining:limit-consumed};
    },
    snapshot() { return {limit, consumed, remaining:limit-consumed, exhausted}; }
  });
}
export function predicateTransition(prior, current) {
  // Consumer builds a vector of every enrolled predicate including actual metric/
  // release values. A false/true vector alone would hide changed unmet values.
  if (!Array.isArray(current) || !current.length || current.length > 128 ||
      current.some(p => !p || typeof p.id !== "string" || !p.id || typeof p.matched !== "boolean" || !Object.hasOwn(p,"state")) ||
      new Set(current.map(p=>p.id)).size !== current.length)
    refuse("predicate_invalid", "unique complete predicate states are required");
  const normalize = vector => [...vector].sort((a,b)=>a.id < b.id ? -1 : a.id > b.id ? 1 : 0).map(({id,state,matched})=>({id,state,matched}));
  const now = normalize(current);
  const matched = now.every(p=>p.matched);
  if (prior === null) return {baseline:true, stateVector:now, stateDigest:digestOf(now), valueChanged:false, requiredOutputMatched:matched, usefulChangedDecision:false};
  if (!Array.isArray(prior) || prior.length !== now.length || prior.some(p=>!p || typeof p.id!=="string" ||
      typeof p.matched!=="boolean" || !Object.hasOwn(p,"state")) ||
      new Set(prior.map(p=>p.id)).size !== prior.length ||
      canonicalJson(prior.map(p=>p.id).sort()) !== canonicalJson(now.map(p=>p.id).sort()))
    refuse("predicate_contract_changed", "prior predicate contract does not match");
  const before = normalize(prior);
  const changed = canonicalJson(before) !== canonicalJson(now);
  return {baseline:false, stateVector:now, stateDigest:digestOf(now), valueChanged:changed,
    requiredOutputMatched:matched, usefulChangedDecision:changed && matched};
}
