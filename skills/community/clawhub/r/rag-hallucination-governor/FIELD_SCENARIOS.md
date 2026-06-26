# Field Scenarios

Synthetic ToB delivery scenarios only. Do not add real customer names, project prices, corpus snippets, contracts, or private implementation details.

## S1: High-Score Wrong Top1

Shape:

- user asks a narrow operational question;
- Top1 has high vector score but is from a neighboring product, policy, or workflow;
- Top2 or Top3 has the correct scope but lower score;
- the answer follows Top1 and becomes confidently wrong.

Required control:

- compare Top1 against Top2/Top3 by subject, version, department, and conclusion;
- add a high-score conflict reject band;
- route to clarification or human review if the conflict cannot be resolved.

## S2: Citation-Looking Unsupported Claim

Shape:

- answer cites a retrieved policy or SOP;
- citation supports background context but not the key conclusion, date, amount, owner, or approval condition;
- user sees a citation and assumes the answer is grounded.

Required control:

- sentence-level or key-claim citation coverage;
- remove unsupported claims;
- strict citation mode for policy, amount, date, ownership, and compliance answers.

## S3: Version Conflict Blend

Shape:

- retrieval returns old and new versions of the same policy or SOP;
- model merges clauses into an answer no single source supports;
- generated answer looks plausible but cannot be audited.

Required control:

- version and publish-time resolver;
- organization scope resolver;
- if unresolved, expose the conflict and ask for applicable scope.

## S4: Query Rewrite Scope Drift

Shape:

- original query is narrow, such as store, product, tenant, department, or role-specific;
- rewrite expands it into a generic policy or cross-domain search;
- final evidence answers a broader question than the user asked.

Required control:

- log pre-rewrite and post-rewrite queries;
- compare TopK overlap and scope fields;
- block generation or clarify when entity, department, product, tenant, or policy domain changes.

## S5: Permission Or Tenant Scope Mismatch

Shape:

- user context belongs to one tenant, department, or role;
- retrieval returns chunks from another scope;
- answer leaks or misuses restricted evidence.

Required control:

- apply ACL and tenant filters before retrieval;
- log scope fields with every cited chunk;
- refuse and escalate when evidence scope does not match user context.

## S6: Low-Confidence Hard Answer

Shape:

- all evidence scores are below threshold or scattered across unrelated chunks;
- model still produces a direct answer because fallback prompt asks it to help;
- user receives a confident answer without enough support.

Required control:

- answer, clarify, and refuse bands;
- conservative answer only when evidence is mutually consistent;
- human handoff for below-threshold or unrelated evidence.
