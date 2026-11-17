# Verification boundaries

This is a release candidate until its owner completes the publication audit and delivery receipts. Cross-modal review was attempted but remained inconclusive; the owner explicitly waived an authoritative three-provider PASS for this first release. Read [KNOWN_GAPS](KNOWN_GAPS.md); no proven quality score is claimed.

Executed smoke checks and runtime information are saved as `examples/runtime-smoke.json`. `examples/fixture-output.json` is the representative output of all five source modes with synthetic inputs. It proves the local input-to-normalized-outcome pipeline ran; it does not prove a clean dependency installation, Google live selectors, authenticated XHS access, proxy geography or customer demand. `examples/test-results.json` records the executed unit/local integration/routing/package checks. The test command is `python3 -m unittest discover -s tests -v`.

Public-source read-only verification checked installed Python libraries and current upstream GenericProxyConfig, yt-dlp network options, XHS proxy startup and MCP argument/data shapes. Existing installed Python dependencies were reused in an isolated development venv with system-site-packages. Optional yt-dlp 2026.8.19 and yt-dlp-ejs 0.8.0 were installed only inside that venv from official PyPI. No global/application dependencies, accounts, keys, cookie files or paid managed APIs were changed.

Actual bounded live collections on 2026-10-07, summarized without raw content or credentials in `examples/live-proof-summary.json`:

- YouTube `aircAruvnKk`: three timed English caption segments and three comment ids/text/source links, one attempt per mode. Both outcomes are `partial` because of the explicit cap/ranked sampling. This does not establish full-video ingestion or representative VOC research.
- Amazon `B09B8V1LZ3`: one matching ASIN/title/visible-price-text/availability observation using an isolated context in an existing Chrome executable. Outcome `partial`; typed price/currency, checkout, delivery location and requested-variant verification remain unproven.
- A newly operator-supplied HTTP connection was passed through a private connection-file input. A previous connection's CONNECT407 refusal was preserved as a failure boundary; it was not retried or presented as extraction proof. Target request IP/country, provider-wide reliability and aggregate authentication were not verified.

Remaining live inputs and verification gaps:

- A current reviewed Google AI Mode or AI Overview DOM contract. Public page access does not guarantee an AI response for a query; each surface requires its own source-semantic validation.
- Broader product/marketplace layouts, exact requested variants and checkout/delivery context beyond the single observed Amazon ASIN. No universal marketplace claim is valid from this page.
- An existing logged-in XHS MCP endpoint whose server was started with matching `XHS_PROXY`; optional `XHS_MCP_AUTH_TOKEN`; a query or a same-source note id + `XHS_XSEC_TOKEN`. Tokens are not part of an artifact.

Executed test coverage includes:

1. Caption identity/timing/language, same-second segments, truncation and named missing/blocked responses.
2. Comments target mismatch, duplicate ids, empty data, ranked cap, yt-dlp errors, timeouts and protected explicit proxy config cleanup.
3. Google AI root/answer/marker absence or ambiguity, answer-only citation scope, Google redirect URL decoding, no organic/legal links, citation dedup and unverified regional context.
4. MCP initialization/session headers/SSE/JSON, paginated discovery cap, read-only tool allowlist, login failure, id/xsecToken mapping, selected note identity and bounded comments.
5. Amazon identity/variant/required-selector failure; JSON-LD graph traversal, exact SKU, one Offer, invalid price/currency/availability and AggregateOffer rejection.
6. Shared redaction of URL userinfo/token keys/known secrets, private output modes, deterministic evidence hashes, return codes and total process-group deadline with descendant cleanup.
7. Routing positives for the one trigger family and negatives for proxy provisioning, general research, video summarization, paid managed social APIs, session changes and Brain ingestion.
8. A trigger-to-fixture evidence side effect, Node bridge, JSON outcomes and a package allowlist/secret scanner. Proposed phrase routing is deterministic and is not an LLM resolver evaluation.

Local integrations hit real loopback HTTP/SSE endpoints and exercise a local HTTP CONNECT407 rejection, not real authenticated XHS or Google. Future live integrations must preserve these limits. Test results or fixture receipts may not substitute for missing live proof. Global resolver/manifest registration remains unverified because no deployment/global registries were changed.
