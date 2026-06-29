#!/usr/bin/env python3
from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
WORKER = ROOT / "deploy" / "tailnet-edge" / "cloudflare-api-worker.js"
WRANGLER_EXAMPLE = ROOT / "deploy" / "tailnet-edge" / "wrangler.api-sagerouter.example.toml"
CLOUDFLARE_BIC_SKIP = ROOT / "scripts" / "configure_cloudflare_api_bic_skip.sh"
CLOUDFLARE_BIC_DOC = ROOT / "docs" / "cloudflare-api-bic-skip.md"
README = ROOT / "README.md"


class CloudflareWorkerEdgeTests(unittest.TestCase):
    def read_worker(self):
        return WORKER.read_text(encoding="utf-8")

    def read_wrangler_example(self):
        return WRANGLER_EXAMPLE.read_text(encoding="utf-8")

    def read_bic_skip_script(self):
        return CLOUDFLARE_BIC_SKIP.read_text(encoding="utf-8")

    def read_bic_skip_doc(self):
        return CLOUDFLARE_BIC_DOC.read_text(encoding="utf-8")

    def read_readme(self):
        return README.read_text(encoding="utf-8")

    def test_public_edge_health_uses_redacted_origin_snapshots(self):
        worker = self.read_worker()
        self.assertIn("function publicOriginSnapshot", worker)
        self.assertIn("function publicOriginsSnapshot", worker)
        self.assertIn("function selectedOriginId", worker)
        self.assertIn("originKind", worker)
        self.assertIn("selectedOriginId: selectedId", worker)
        self.assertIn('"x-sage-router-cloudflare-edge": "api.sagerouter.dev"', worker)
        self.assertIn('"x-sage-router-api-origin": selectedId || "origin-none"', worker)
        self.assertIn('"x-sage-router-api-origin-kind": healthy[0] ? originKind(healthy[0].url) : "none"', worker)
        self.assertNotRegex(worker, r"selected:\s*healthy\[0\]")
        self.assertNotRegex(worker, r"origins:\s*checks")

    def test_proxy_response_headers_do_not_expose_origin_urls(self):
        worker = self.read_worker()
        self.assertNotIn('"x-sage-router-api-origin-url"', worker)
        self.assertNotRegex(worker, re.compile(r"headers\.set\([^)]*origin\.url", re.DOTALL))
        self.assertIn('"x-sage-router-api-origin-kind"', worker)

    def test_outbound_origin_header_uses_redacted_origin_id(self):
        worker = self.read_worker()
        self.assertIn("function outboundHeaders(request, selectedOriginId)", worker)
        self.assertIn('headers.set("x-sage-router-origin", selectedOriginId || "origin-unknown")', worker)
        self.assertIn("headers: outboundHeaders(request, originId)", worker)
        self.assertNotIn('headers.set("x-sage-router-origin", selectedOrigin.name)', worker)

    def test_public_snapshot_does_not_return_raw_url_or_health_path(self):
        worker = self.read_worker()
        match = re.search(
            r"function publicOriginSnapshot\(check, index\) \{\n  return \{(?P<body>.*?)\n  \};\n\}",
            worker,
            re.DOTALL,
        )
        self.assertIsNotNone(match)
        body = match.group("body")
        self.assertNotRegex(body, r"\burl\s*:")
        self.assertNotRegex(body, r"\bhealthPath\s*:")
        self.assertIn("id: publicOriginId(index)", body)
        self.assertIn("originKind: originKind(check.url)", body)

    def test_worker_requires_public_edge_health_by_default(self):
        worker = self.read_worker()
        self.assertIn("const PUBLIC_EDGE_HEALTH_ERROR", worker)
        self.assertIn("function publicEdgeHealthSatisfied", worker)
        self.assertIn("SAGE_ROUTER_REQUIRE_PUBLIC_EDGE_HEALTH", worker)
        self.assertIn("payload.authMode === \"supabase\"", worker)
        self.assertIn("enforcement.rateLimitEnabled === true", worker)
        self.assertIn("enforcement.authAttemptRateLimitEnabled === true", worker)
        self.assertIn("enforcement.quotaEnabled === true", worker)
        self.assertIn("Number(enforcement.apiKeyAuthCacheSeconds) === 0", worker)
        self.assertIn("enforcement.corsWildcardAllowed === false", worker)
        self.assertIn("enforcement.corsExplicitOriginRequired === true", worker)
        self.assertIn("Number(enforcement.corsAllowedOriginsCount || 0) > 0", worker)
        self.assertIn("modelModalities.sharedEnabled === true", worker)
        self.assertIn("modelModalities.rpcConfigured === true", worker)
        self.assertIn("failover.mode === \"lowest-latency-healthy\"", worker)
        self.assertIn("!hasRawOriginUrl(payload.upstreams || [])", worker)

    def test_worker_health_requires_2xx_even_without_public_edge_proof(self):
        worker = self.read_worker()
        self.assertIn("const statusHealthy = result.response.status >= 200 && result.response.status < 300", worker)
        self.assertNotIn("const statusHealthy = result.response.status >= 200 && result.response.status < 500", worker)

    def test_worker_retries_replayable_requests_across_healthy_origins(self):
        worker = self.read_worker()
        self.assertIn("const DEFAULT_RETRY_STATUSES = [502, 503, 504]", worker)
        self.assertIn("function retryStatuses(env)", worker)
        self.assertIn("function shouldRetryOriginStatus(env, status)", worker)
        self.assertIn("function chooseOriginCandidates(env)", worker)
        self.assertIn("const retryableCandidates = replayableBody ? candidates : candidates.slice(0, 1)", worker)
        self.assertIn("if (index < retryableCandidates.length - 1 && shouldRetryOriginStatus(env, response.response.status))", worker)
        self.assertIn('headers.set("x-sage-router-retry-count", String(retryCountFromFailedAttempts(failedAttempts, true)))', worker)
        self.assertIn('"x-sage-router-retry-count": String(retryCountFromFailedAttempts(failedAttempts, false))', worker)
        self.assertIn('error: "all healthy sage-router origins failed"', worker)
        self.assertNotIn("attempts: checks", worker)

    def test_worker_health_exposes_redacted_retry_policy(self):
        worker = self.read_worker()
        self.assertIn('mode: "lowest-latency-healthy"', worker)
        self.assertIn("retryEnabled: healthy.length > 1", worker)
        self.assertIn("retryStatuses: [...retryStatuses(env)].sort((a, b) => a - b)", worker)
        self.assertIn('retryHeader: "X-Sage-Router-Retry-Count"', worker)
        self.assertIn("replayableBodyRequired: true", worker)

    def test_worker_example_uses_edge_health_origins(self):
        example = self.read_wrangler_example()
        self.assertIn('SAGE_ROUTER_REQUIRE_PUBLIC_EDGE_HEALTH = "1"', example)
        self.assertIn('SAGE_ROUTER_EDGE_RETRY_STATUSES = "502,503,504"', example)
        self.assertIn('"healthPath": "/edge/health"', example)
        self.assertNotIn("run.app", example)
        self.assertNotIn('"healthPath": "/health"', example)

    def test_worker_records_successful_model_modalities_to_supabase(self):
        worker = self.read_worker()
        self.assertIn("function recordModelModalities(env, record)", worker)
        self.assertIn("function modalityRecordFromResponseHeaders(headers, status)", worker)
        self.assertIn("function modalityRecordFromResponse(headers, status, requestBodyText = \"\", responseBodyText = \"\")", worker)
        self.assertIn("function requestModalitiesFromBodyText(bodyText)", worker)
        self.assertIn("function applyModalityHeaders(headers, record)", worker)
        self.assertIn("function boundedStreamText(stream, maxBytes)", worker)
        self.assertIn("response.response.clone()", worker)
        self.assertIn("const requestLengthKnown =", worker)
        self.assertIn("!requestLengthKnown || requestLength <= maxModalityBodyBytes", worker)
        self.assertNotIn("if (!length || length > maxBytes", worker)
        self.assertIn('headers.get("x-sage-router-modalities")', worker)
        self.assertIn('headers.get("x-sage-router-provider")', worker)
        self.assertIn('headers.get("x-sage-router-model-name")', worker)
        self.assertIn('env.SAGE_ROUTER_SUPABASE_MODEL_MODALITIES_RPC || "sage_router_record_model_modalities"', worker)
        self.assertIn("ctx.waitUntil(modalityRecord)", worker)
        self.assertIn("function modelModalitiesState(env)", worker)
        self.assertIn("modelModalities: modelModalitiesState(env)", worker)

    def test_worker_example_enables_shared_modality_ledger(self):
        example = self.read_wrangler_example()
        self.assertIn('SAGE_ROUTER_MODEL_MODALITIES_SHARED_ENABLED = "1"', example)
        self.assertIn("SAGE_ROUTER_SUPABASE_URL", example)
        self.assertIn("wrangler secret put SAGE_ROUTER_SUPABASE_SERVICE_ROLE_KEY", example)
        self.assertIn("SAGE_ROUTER_SUPABASE_MODEL_MODALITIES_RPC", example)

    def test_cloudflare_bic_skip_script_reports_ruleset_permission_failures(self):
        script = self.read_bic_skip_script()
        self.assertIn("Usage: scripts/configure_cloudflare_api_bic_skip.sh [--check|--audit-local-tokens]", script)
        self.assertIn('MODE="apply"', script)
        self.assertIn('--check)', script)
        self.assertIn('--audit-local-tokens)', script)
        self.assertIn('if [[ "$MODE" == "check" ]]', script)
        self.assertIn('if [[ "$MODE" == "audit-local-tokens" ]]', script)
        self.assertIn("cloudflare_token_candidate_audit", script)
        self.assertIn("cloudflare_token_candidate_audit_summary", script)
        self.assertIn("printsTokenValues", script)
        self.assertIn("usableRulesetTokenCandidates", script)
        self.assertIn("recommendedAction", script)
        self.assertIn("rotate_CLOUDFLARE_API_TOKEN_with_Zone_Zone_Read_and_Zone_Rulesets_Read_Edit", script)
        self.assertIn("without --check to create the host-scoped BIC skip rule", script)
        self.assertIn("without --check to apply it", script)
        self.assertIn("cloudflare_error_summary", script)
        self.assertIn("Cloudflare zone lookup for ${ZONE_NAME}", script)
        self.assertIn("api_get_ruleset_entrypoint", script)
        self.assertIn("failed with HTTP %s", script)
        self.assertIn("Zone:Zone:Read and Zone Rulesets:Read/Edit", script)
        self.assertIn("token can see the zone but is missing Zone Rulesets permissions", script)
        self.assertIn("SAGEROUTER_CLOUDFLARE_ZONE_ID/CLOUDFLARE_ZONE_ID", script)

    def test_cloudflare_bic_runbook_is_discoverable(self):
        doc = self.read_bic_skip_doc()
        readme = self.read_readme()

        self.assertIn("Cloudflare BIC Skip For api.sagerouter.dev", doc)
        self.assertIn("Zone:Zone:Read", doc)
        self.assertIn("Zone Rulesets:Read", doc)
        self.assertIn("Zone Rulesets:Edit", doc)
        self.assertIn("bash scripts/configure_cloudflare_api_bic_skip.sh --check", doc)
        self.assertIn("bash scripts/configure_cloudflare_api_bic_skip.sh --audit-local-tokens", doc)
        self.assertIn("without printing token values", doc)
        self.assertIn("usableRulesetTokenCandidates", doc)
        self.assertIn("recommendedAction", doc)
        self.assertIn("bash scripts/configure_cloudflare_api_bic_skip.sh", doc)
        self.assertIn('http.host eq "api.sagerouter.dev"', doc)
        self.assertIn("docs/cloudflare-api-bic-skip.md", readme)


if __name__ == "__main__":
    unittest.main()
