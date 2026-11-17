---
name: tencent-pg-rest-deploy
description: Route one natural-language TencentDB for PostgreSQL REST request into service control, read-only PostgREST invocation, or 502 troubleshooting. Resolve the target instance and runtime defaults, run read-only preflight first, execute OpenPostgRESTService or ClosePostgRESTService when the request is explicit, directly execute safe read-only REST calls through QueryPostgRESTService when the user is trying to use the REST endpoint, and diagnose common 502 blockers such as missing internal-port security-group exposure.
description_zh: PostgreSQL 一句话开通 / 调用 / 排障 REST 服务
description_en: One-sentence REST service control, invocation, and troubleshooting for PostgreSQL
disable: false
agent_created: true
---

# tencent-pg-rest-deploy

## When to use
- Need one natural-language entry to **open, close, use, or troubleshoot** Tencent Cloud PostgreSQL REST / PostgREST service.
- Need the skill to infer whether the real goal is **service control**, **read-only REST invocation**, or **REST troubleshooting**, instead of forcing the user to choose the lane manually.
- Need the skill to auto-fill region or default instance, run read-only checks first, and either execute the safe request directly or return the exact next action and blocker.

## Steps
1. Detect the primary REST lane before any API call. Route into exactly one primary lane: `service-control`, `rest-readonly-call`, or `rest-troubleshooting`. Prioritize the user's requested outcome over surface keywords.
2. Use `service-control` only when the sentence explicitly asks to **open / enable / deploy / bring up** REST or to **close / disable / take down** REST. If the sentence is mainly about actually using the REST endpoint, do not stay in the control lane.
3. Use `rest-readonly-call` when the user is clearly trying to **call a REST capability**, such as viewing the OpenAPI description, querying a path, checking current exposed resources, or executing a safe read-only GET request against the PostgREST endpoint.
4. Use `rest-troubleshooting` when the user is mainly reporting a symptom such as `502`、`504`、超时、入口不可用、连通性异常、路径报错、或想确认为什么 REST 访问不通。
5. Extract the minimum slot set for the chosen lane: always resolve `region` and `DBInstanceId`; when relevant also capture REST `Path`, raw query string, expected resource, observed HTTP status, whether the request is public or private, and whether the user is explicitly asking for a fix instead of just diagnosis.
6. Normalize region before any API call by following `@references/common/region_normalization.md`. Accept standard region codes and supported Chinese aliases. If the region cannot be normalized safely, stop and use the `invalid-region` template in `@references/common/error_handling.md`.
7. Check runtime prerequisites in a strict order by following `@references/api_reference.md`: Tencent Cloud credentials first, REST-specific runtime defaults second. If required runtime values are missing, stop with a direct message that lists the missing items and includes one copyable environment-variable example. For non-secret missing slots that the current toolchain can resolve safely, also offer an agent-assisted lookup option.
8. Resolve the target instance with the smallest safe path. Prefer explicit `DBInstanceId`. Otherwise use a runtime default if present. Only fall back to `DescribeDBInstances` discovery when region is known and the result can be narrowed to exactly one suitable instance. If multiple candidates remain, stop and ask for `region + instance ID` in one direct sentence.
9. Run read-only preflight first for every lane. Use `DescribeDBInstanceAttribute` and `DescribePostgRESTService` to confirm that the instance exists, the target scope is correct, the REST service status is known, and a public access address is available when public invocation is needed.
10. If the current instance region does not support REST / PostgREST service control, immediately switch to the unsupported-region fallback in `@references/api_reference.md`. Return the blocked region, the API evidence, the supported-region candidates, and one copyable next-step suggestion.
11. In the `service-control` lane, interpret the current REST state before writing. If the user wants to **open** REST and the service is already ready, return the current service status, current network exposure facts, and explicitly remind the user that **公网 / 外网访问默认应保持关闭** unless external access is truly required. If the user wants to **close** REST and the service is already closed or not opened, return the current state instead of calling `ClosePostgRESTService`. If REST is in a transition state such as creating or deleting, stop and report the current blocker rather than stacking another write request.
12. Do **not** equate `开通 REST 服务` with `开启公网 / 外网访问`. For a normal open request, treat the safe default as: execute `OpenPostgRESTService` with `EnableWanNet=false`, which means **open REST service but keep public exposure closed by default**.
13. Therefore, when the user clearly asks to open or enable REST service, the target scope is unambiguous, and read-only preflight found no material blocker, the skill may execute `OpenPostgRESTService` directly with `EnableWanNet=false` without adding a second confirmation turn solely for service enablement.
14. Only when the user explicitly asks the skill to **open public / external access** on their behalf, or otherwise requests `EnableWanNet=true`, should the skill switch to the confirmation-waiting response shape. In that branch, explicitly say that public exposure is a risky security change, explain the main risks such as broader attack surface, accidental data exposure, unauthorized probing, and misuse of the public endpoint, and wait for the user's second explicit confirmation before executing the exposure-changing call.
15. In the `rest-readonly-call` lane, prefer `QueryPostgRESTService` for direct execution. Normalize a missing path to `/` only when the user is clearly asking for the service content overview or OpenAPI description; otherwise require the concrete path. Execute only safe read-only GET requests through the public PostgREST address.
16. If the user is implicitly trying to switch database by guessing `db=smoke`、`dbname=...`、or `/smoke`, do not claim success based on guesswork. First inspect the currently exposed resources and the returned HTTP result. If the requested resource is not exposed, clearly state that the current PostgREST schema cache does not expose it.
17. Do not automatically probe private PostgREST addresses. Only use the public address for direct execution in this skill. If the environment currently has only private PostgREST access, explain that this skill does not auto-issue internal HTTP probes and tell the user what explicit follow-up is needed.
18. In the `rest-troubleshooting` lane, collect evidence in order: `DescribePostgRESTService`, one minimal public `QueryPostgRESTService` probe such as `/`, and `DescribeDBInstanceSecurityGroups` when the symptom looks network-related or gateway-related.
19. When troubleshooting a `502` or similar gateway symptom, distinguish at least these cases: service not running, public address missing, public endpoint reachable but resource missing, and likely backend path issues such as internal-port connectivity blocked by security-group rules.
20. If the evidence points to security-group exposure as the likely blocker, explain the limit precisely: this repository can query current security-group bindings and can switch the PostgreSQL instance to another security-group set through `ModifyDBInstanceSecurityGroups`, but it does **not** directly edit ingress or egress rules inside an existing security group.
21. Therefore, if the user only needs diagnosis, stop after returning the current security-group evidence and the likely missing internal-port rule. If the user explicitly asks to fix it and already provides the target security-group set to attach, you may move to the confirmation-waiting response shape and then use `ModifyDBInstanceSecurityGroups` after explicit confirmation. If the real fix requires editing rules inside the currently bound security group, tell the user to modify the rule manually in the console instead of pretending the skill can do it.
22. When the next step requires a risky or scope-changing action, including enabling public REST exposure or replacing the instance's security-group binding, switch to the confirmation-waiting response shape in `@references/api_reference.md`. Explicitly say the skill is waiting, using wording such as `等你确认` or `确认后我再继续`, and explain both the pending action and the main risks before stopping.
23. Poll `DescribePostgRESTService` with the bounded retry policy defined in `@references/api_reference.md` only after `OpenPostgRESTService` or `ClosePostgRESTService`. Never poll forever, and never call the opposite action automatically as a recovery step.
24. Summarize as a final REST result: target scope, recognized lane and routing reason, resolved slots and their sources, read-only evidence, executed actions, whether `EnableWanNet` stayed false or was explicitly requested to become true, current REST status, direct HTTP result for read-only calls when executed, security-group findings for 502 troubleshooting, whether the repository can auto-fix the blocker, and the exact next copyable step.

## Pitfalls
- Do not force every REST-related sentence into open / close flow; first distinguish service control, actual REST invocation, and troubleshooting intent.
- Do not guess resource paths or database switching semantics and then claim the REST call succeeded.
- Do not auto-issue internal-network HTTP probes or private-address requests in this skill.
- Do not run `OpenPostgRESTService` or `ClosePostgRESTService` on an ambiguous target or when multiple candidate instances remain.
- Do not stop a confirmation-required branch with vague wording such as `要继续吗`; explicitly say `等你确认` or equivalent, and explain the pending action's meaning and main risk.
- Do not auto-call `ClosePostgRESTService` after an open failure, or `OpenPostgRESTService` after a close failure.
- Do not say `可以直接改安全组规则` when the current tool surface only supports replacing the bound security-group set, not editing the rule entries themselves.
- Do not claim that a 502 root cause is confirmed security-group exposure unless the current evidence really points there; keep the wording at `高概率` or `当前最可疑` when the platform signal is indirect.

## Verification
- Include region, instance ID, recognized lane, and routing reason in the final answer.
- State which slots came from the user and which came from runtime defaults.
- State which read-only actions were used before any write action or troubleshooting conclusion.
- For `service-control`, include the final REST status, whether `EnableWanNet` was effectively false or true, and either the usable access address on public-open success or the explicit note that service is enabled while public access remains closed.
- For `rest-readonly-call`, include the exact executed path, HTTP status code, and a compact summary of the returned body.
- For `rest-troubleshooting`, include the observed symptom, the probe result, the current security-group evidence when checked, and whether the blocker can be fixed automatically by this skill or requires manual console changes.
- If the next step requires confirmation, explicitly say `等你确认` or an equally direct waiting phrase, state what action will happen after confirmation, explain why that action matters, and summarize the main risk or impact.
- If execution is blocked, clearly state the blocker and the exact reply, confirmation, or console fix needed next.
