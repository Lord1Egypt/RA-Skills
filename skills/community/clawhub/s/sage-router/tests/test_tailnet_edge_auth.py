#!/usr/bin/env python3
import hashlib
import importlib.util
import json
import os
import sys
import unittest
from io import BytesIO
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EDGE_PROXY = ROOT / "deploy" / "tailnet-edge" / "edge_proxy.py"


def load_edge_proxy():
    env = {
        "SAGE_ROUTER_UPSTREAMS": "http://backend.local:8790",
        "SAGE_ROUTER_EDGE_AUTH_MODE": "supabase",
        "SAGE_ROUTER_SUPABASE_URL": "https://example.supabase.co",
        "SAGE_ROUTER_SUPABASE_ANON_KEY": "anon",
        "SAGE_ROUTER_SUPABASE_SERVICE_ROLE_KEY": "service",
        "SAGE_ROUTER_API_KEY_HASH_PEPPER": "pepper",
        "SAGE_ROUTER_EDGE_AUTH_CACHE_SECONDS": "0",
        "SAGE_ROUTER_EDGE_RATE_LIMIT_WINDOW_SECONDS": "60",
        "SAGE_ROUTER_EDGE_RATE_LIMITS": "pro=2,default=1",
        "SAGE_ROUTER_EDGE_AUTH_ATTEMPT_RATE_LIMIT": "2",
        "SAGE_ROUTER_EDGE_QUOTA_ENABLED": "1",
        "SAGE_ROUTER_EDGE_MONTHLY_QUOTAS": "pro=2,default=0",
    }
    old = {key: os.environ.get(key) for key in env}
    os.environ.update(env)
    try:
        sys.modules.pop("edge_proxy_under_test", None)
        spec = importlib.util.spec_from_file_location("edge_proxy_under_test", EDGE_PROXY)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    finally:
        for key, value in old.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value


class TailnetEdgeAuthTests(unittest.TestCase):
    def setUp(self):
        self.edge = load_edge_proxy()

    def test_generated_api_key_requires_active_paid_customer(self):
        raw_key = "sk_sage_test_key"
        digest = hashlib.sha256(("pepper" + raw_key).encode("utf-8")).hexdigest()
        patches = []

        def fake_get(path, service=False, token=None, timeout=6):
            self.assertTrue(service)
            if self.edge.SUPABASE_API_KEYS_TABLE in path:
                self.assertIn(digest, path)
                return [{
                    "id": "key-1",
                    "customer_id": "customer-1",
                    "status": "active",
                    "api_key_hash": digest,
                }]
            if self.edge.SUPABASE_CUSTOMERS_TABLE in path:
                return [{
                    "id": "customer-1",
                    "user_id": "user-1",
                    "plan": "pro",
                    "status": "active",
                }]
            return []

        def fake_patch(path, payload, timeout=4):
            patches.append((path, payload))

        self.edge.supabase_get_json = fake_get
        self.edge.supabase_patch_json = fake_patch

        ctx = self.edge.verify_supabase_generated_key(raw_key)
        self.assertEqual("generated_key", ctx["type"])
        self.assertEqual("key-1", ctx["key_id"])
        self.assertEqual("customer-1", ctx["customer_id"])
        self.assertEqual("pro", ctx["plan"])
        self.assertFalse(ctx["preserve_authorization"])
        self.assertEqual(1, len(patches))

    def test_generated_api_key_auth_rechecks_by_default_for_revocation(self):
        raw_key = "sk_sage_test_key"
        digest = hashlib.sha256(("pepper" + raw_key).encode("utf-8")).hexdigest()
        active = True
        key_lookups = 0

        def fake_get(path, service=False, token=None, timeout=6):
            nonlocal key_lookups
            self.assertTrue(service)
            if self.edge.SUPABASE_API_KEYS_TABLE in path:
                key_lookups += 1
                self.assertIn(digest, path)
                if not active:
                    return []
                return [{
                    "id": "key-1",
                    "customer_id": "customer-1",
                    "status": "active",
                    "api_key_hash": digest,
                }]
            if self.edge.SUPABASE_CUSTOMERS_TABLE in path:
                return [{
                    "id": "customer-1",
                    "user_id": "user-1",
                    "plan": "pro",
                    "status": "active",
                }]
            return []

        self.edge.supabase_get_json = fake_get
        self.edge.supabase_patch_json = lambda *_args, **_kwargs: None

        self.assertEqual("generated_key", self.edge.verify_supabase_generated_key(raw_key)["type"])
        active = False
        self.assertFalse(self.edge.verify_supabase_generated_key(raw_key))
        self.assertEqual(2, key_lookups)

    def test_generated_api_key_rejects_free_or_inactive_customer(self):
        self.edge.supabase_get_json = lambda path, **_kwargs: (
            [{"id": "key-1", "customer_id": "customer-1", "status": "active"}]
            if self.edge.SUPABASE_API_KEYS_TABLE in path
            else [{"id": "customer-1", "user_id": "user-1", "plan": "free", "status": "active"}]
        )
        self.assertFalse(self.edge.verify_supabase_generated_key("sk_sage_test_key"))

    def test_user_jwt_paths_preserve_authorization(self):
        self.edge.verify_supabase_user_jwt = lambda token: {
            "type": "supabase_user",
            "user_id": "user-1",
            "preserve_authorization": True,
        }

        class Handler:
            path = "/account/api-keys"
            headers = {"Authorization": "Bearer jwt"}

        ctx = self.edge.EdgeHandler._auth_context(Handler())
        self.assertEqual("supabase_user", ctx["type"])
        self.assertTrue(ctx["preserve_authorization"])

    def test_public_control_plane_metadata_does_not_require_auth(self):
        self.edge.verify_supabase_generated_key = lambda token: self.fail("public metadata should not require an API key")

        for path in ("/pricing", "/plans", "/model-catalog", "/features/agent-native"):
            with self.subTest(path=path):
                class Handler:
                    headers = {}

                Handler.path = path
                ctx = self.edge.EdgeHandler._auth_context(Handler())
                self.assertEqual("public_control_plane", ctx["type"])
                self.assertFalse(ctx["preserve_authorization"])

    def test_supabase_customer_keys_are_limited_to_model_api_paths(self):
        calls = []

        def fake_verify(token):
            calls.append(token)
            return {"type": "generated_key", "preserve_authorization": False}

        self.edge.verify_supabase_generated_key = fake_verify

        class Handler:
            headers = {"Authorization": "Bearer sk_sage_test"}

        for path in ("/v1/models", "/v1/chat/completions", "/v1beta/models/gemini:generateContent"):
            with self.subTest(path=path):
                Handler.path = path
                ctx = self.edge.EdgeHandler._auth_context(Handler())
                self.assertEqual("generated_key", ctx["type"])

        for path in ("/analytics", "/analytics/funnel", "/admin/blocks", "/admin/customers", "/discovery"):
            with self.subTest(path=path):
                Handler.path = path
                self.assertIsNone(self.edge.EdgeHandler._auth_context(Handler()))

        self.assertEqual(["sk_sage_test", "sk_sage_test", "sk_sage_test"], calls)

    def test_model_api_retries_stale_route_404_and_405(self):
        self.assertTrue(self.edge.should_retry_upstream_status("/v1/chat/completions", 404))
        self.assertTrue(self.edge.should_retry_upstream_status("/v1/responses", 405))
        self.assertTrue(self.edge.should_retry_upstream_status("/account", 503))
        self.assertFalse(self.edge.should_retry_upstream_status("/account", 404))

    def test_edge_reroutes_known_ollama_subscription_model_to_sibling(self):
        body = b'{"model":"ollama/kimi-k2.7-code","messages":[{"role":"user","content":"hi"}]}'
        rewritten = self.edge.reroute_known_ollama_subscription_body("/v1/chat/completions", body)
        self.assertIn(b'"model":"ollama-2/kimi-k2.7-code"', rewritten)

    def test_edge_does_not_reroute_other_ollama_models(self):
        body = b'{"model":"ollama/glm-5","messages":[{"role":"user","content":"hi"}]}'
        self.assertEqual(body, self.edge.reroute_known_ollama_subscription_body("/v1/chat/completions", body))

    def test_edge_recalculates_content_length_after_body_rewrite(self):
        source = EDGE_PROXY.read_text()
        self.assertIn('lower == "content-length" and body is not None', source)
        self.assertIn('value = str(len(body))', source)

    def test_model_api_auth_errors_include_onboarding_links(self):
        payload = self.edge.edge_error_payload("unauthorized", "/v1/models")
        headers = self.edge.edge_error_headers("unauthorized", "/v1/models")

        self.assertEqual("unauthorized", payload["error"])
        self.assertEqual("https://app.sagerouter.dev/account.html", payload["accountUrl"])
        self.assertEqual("https://sagerouter.dev/pricing", payload["pricingUrl"])
        self.assertEqual("https://app.sagerouter.dev/status", payload["statusUrl"])
        self.assertEqual("https://api.sagerouter.dev/v1", payload["openaiBaseUrl"])
        self.assertEqual("sk_sage_", payload["apiKeyPrefix"])
        self.assertIn("WWW-Authenticate", headers)
        self.assertIn("Sage Router", headers["WWW-Authenticate"])
        self.assertIn('rel="account"', headers["Link"])
        self.assertIn('rel="pricing"', headers["Link"])

    def test_public_api_browser_auth_errors_point_to_app_not_dashboard(self):
        for path in ("/", "/dashboard"):
            with self.subTest(path=path):
                payload = self.edge.edge_error_payload("unauthorized", path)
                headers = self.edge.edge_error_headers("unauthorized", path)

                self.assertEqual("unauthorized", payload["error"])
                self.assertTrue(payload["apiOnly"])
                self.assertEqual("https://app.sagerouter.dev/login.html", payload["loginUrl"])
                self.assertEqual("https://app.sagerouter.dev/account.html", payload["accountUrl"])
                self.assertEqual("https://app.sagerouter.dev/status", payload["statusUrl"])
                self.assertEqual("https://api.sagerouter.dev/v1", payload["openaiBaseUrl"])
                self.assertIn('rel="account"', headers["Link"])
                self.assertIn('rel="status"', headers["Link"])

    def test_reject_json_drains_post_body_and_closes_connection(self):
        class Handler:
            command = "POST"
            headers = {"Content-Length": "13"}
            rfile = BytesIO(b'{"ok": true}\n')
            wfile = BytesIO()
            path = "/setup/model-modalities/update"
            close_connection = False
            status = None
            sent_headers = {}

            def send_response(self, status):
                self.status = status

            def send_header(self, key, value):
                self.sent_headers[key] = value

            def end_headers(self):
                pass

            _json = self.edge.EdgeHandler._json
            _cors_headers = self.edge.EdgeHandler._cors_headers

        handler = Handler()
        self.edge.EdgeHandler._reject_json(handler, 401, {"error": "unauthorized"})

        self.assertEqual(401, handler.status)
        self.assertEqual(b"", handler.rfile.read())
        self.assertTrue(handler.close_connection)
        self.assertEqual("close", handler.sent_headers["Connection"])

    def test_edge_health_exposes_public_safe_enforcement_state(self):
        self.edge.UPSTREAMS[0].set_health(True, 12.3, "")

        class Handler:
            payload = None
            status = None
            extra_headers = None

            def _json(self, status, payload, extra_headers=None):
                self.status = status
                self.payload = payload
                self.extra_headers = extra_headers or {}

        handler = Handler()
        self.edge.EdgeHandler._edge_health(handler)

        self.assertEqual(200, handler.status)
        self.assertEqual("supabase", handler.payload["authMode"])
        self.assertEqual("upstream-1", handler.payload["selected"])
        self.assertEqual("upstream-1", handler.payload["selectedUpstreamId"])
        self.assertEqual("tailnet-lowest-latency", handler.extra_headers["X-Sage-Router-Edge"])
        self.assertEqual("upstream-1", handler.extra_headers["X-Sage-Router-Selected-Upstream"])
        self.assertEqual("upstream-1", handler.payload["upstreams"][0]["id"])
        self.assertEqual("Upstream 1", handler.payload["upstreams"][0]["label"])
        self.assertEqual("custom", handler.payload["upstreams"][0]["originKind"])
        self.assertNotIn("url", handler.payload["upstreams"][0])
        self.assertNotIn("backend.local", str(handler.payload))
        self.assertEqual({
            "rateLimitEnabled": True,
            "rateLimitWindowSeconds": 60,
            "authAttemptRateLimit": 2,
            "authAttemptRateLimitEnabled": True,
            "browserOriginGuardEnabled": True,
            "trustClientIpHeaders": True,
            "quotaEnabled": True,
            "apiKeyAuthCacheSeconds": 0.0,
            "apiKeyPrefix": "sk_sage_",
            "corsWildcardAllowed": False,
            "corsExplicitOriginRequired": True,
            "corsAllowedOriginsCount": 4,
        }, handler.payload["enforcement"])
        self.assertEqual({
            "mode": "lowest-latency-healthy",
            "healthyUpstreamCount": 1,
            "controlPlanePinned": False,
            "retryEnabled": True,
            "retryStatuses": [401, 404, 405, 429, 502, 503, 504],
            "retryHeader": "X-Sage-Router-Retry-Count",
        }, handler.payload["failover"])
        self.assertEqual({
            "sharedEnabled": True,
            "supabaseConfigured": True,
            "rpcConfigured": True,
        }, handler.payload["modelModalities"])

    def test_public_response_headers_use_redacted_upstream_id(self):
        source = EDGE_PROXY.read_text(encoding="utf-8")

        self.assertIn('self.send_header("X-Sage-Router-Upstream", public_upstream_id(upstream))', source)
        self.assertNotIn('self.send_header("X-Sage-Router-Upstream", upstream.raw_url)', source)

    def test_edge_health_flags_wildcard_cors_as_not_launch_ready(self):
        self.edge.CORS_ORIGINS = ["*"]

        self.assertEqual({
            "corsWildcardAllowed": True,
            "corsExplicitOriginRequired": False,
            "corsAllowedOriginsCount": 3,
        }, self.edge.edge_cors_state())

    def test_upstream_health_requires_success_status(self):
        class FakeResponse:
            def __init__(self, status):
                self.status = status

            def read(self, _limit):
                return b""

        class FakeConnection:
            def __init__(self, status):
                self.status = status
                self.closed = False

            def request(self, method, path, headers=None):
                self.method = method
                self.path = path
                self.headers = headers or {}

            def getresponse(self):
                return FakeResponse(self.status)

            def close(self):
                self.closed = True

        for status, expected in ((200, True), (204, True), (302, False), (401, False), (503, False)):
            with self.subTest(status=status):
                upstream = self.edge.Upstream("http://backend.local:8790")
                conn = FakeConnection(status)
                upstream.connection = lambda timeout, conn=conn: conn

                self.edge.check_upstream(upstream)
                snapshot = upstream.snapshot()

                self.assertEqual(expected, snapshot["healthy"])
                self.assertTrue(conn.closed)
                if expected:
                    self.assertEqual("", snapshot["last_error"])
                else:
                    self.assertEqual(f"HTTP {status}", snapshot["last_error"])

    def test_browser_origin_guard_rejects_untrusted_account_billing_and_admin_mutations(self):
        for path in (
            "/account/api-keys",
            "/account/api-keys/key_1/revoke",
            "/billing/stripe/checkout",
            "/billing/stripe/portal",
            "/billing/crypto/intent",
            "/admin/customers/customer_1/suspend",
            "/admin/customers/customer_1/unsuspend",
            "/admin/payment-intents/pi_1/approve",
        ):
            with self.subTest(path=path):
                class Handler:
                    command = "POST"
                    headers = {"Origin": "https://evil.example"}
                    status = None
                    payload = None
                    extra_headers = None

                    def _json(self, status, payload, extra_headers=None):
                        self.status = status
                        self.payload = payload
                        self.extra_headers = extra_headers or {}

                Handler.path = path
                handler = Handler()
                blocked = self.edge.EdgeHandler._reject_untrusted_browser_origin(handler)

                self.assertTrue(blocked)
                self.assertEqual(403, handler.status)
                self.assertEqual("origin_not_allowed", handler.payload["error"])
                self.assertEqual("origin_guard", handler.extra_headers["X-Sage-Router-Edge-Auth-Type"])

    def test_browser_origin_guard_allows_trusted_origins_and_non_browser_clients(self):
        class Handler:
            command = "POST"
            path = "/account/api-keys"
            status = None
            payload = None

            def _json(self, status, payload, extra_headers=None):
                self.status = status
                self.payload = payload

        for origin in ("https://app.sagerouter.dev", "http://localhost:3000", ""):
            with self.subTest(origin=origin or "none"):
                handler = Handler()
                handler.headers = {"Origin": origin} if origin else {}

                self.assertFalse(self.edge.EdgeHandler._reject_untrusted_browser_origin(handler))
                self.assertIsNone(handler.status)

    def test_browser_origin_guard_drains_rejected_post_body_and_closes_connection(self):
        class Handler:
            command = "POST"
            path = "/account/api-keys"
            headers = {
                "Origin": "https://evil.example",
                "Content-Length": "29",
            }

            def __init__(self):
                self.rfile = BytesIO(b'{"name":"origin-guard-probe"}')
                self.status = None
                self.payload = None
                self.extra_headers = None
                self.close_connection = False

            def _json(self, status, payload, extra_headers=None):
                self.status = status
                self.payload = payload
                self.extra_headers = extra_headers or {}

        handler = Handler()
        blocked = self.edge.EdgeHandler._reject_untrusted_browser_origin(handler)

        self.assertTrue(blocked)
        self.assertEqual(403, handler.status)
        self.assertEqual(b"", handler.rfile.read())
        self.assertTrue(handler.close_connection)
        self.assertEqual("close", handler.extra_headers["Connection"])

    def test_billing_portal_uses_supabase_user_auth(self):
        self.edge.verify_supabase_user_jwt = lambda token: {
            "type": "supabase_user",
            "user_id": "user-1",
            "preserve_authorization": True,
        }

        class Handler:
            path = "/billing/stripe/portal"
            headers = {"Authorization": "Bearer jwt"}

        ctx = self.edge.EdgeHandler._auth_context(Handler())
        self.assertEqual("supabase_user", ctx["type"])
        self.assertTrue(ctx["preserve_authorization"])

    def test_head_json_response_sends_headers_without_body(self):
        class Handler:
            command = "HEAD"
            headers = {"Origin": "https://app.sagerouter.dev"}

            def __init__(self):
                self.status = None
                self.sent_headers = {}
                self.wfile = BytesIO()

            def send_response(self, status):
                self.status = status

            def send_header(self, key, value):
                self.sent_headers[key] = value

            def end_headers(self):
                pass

            _cors_headers = self.edge.EdgeHandler._cors_headers

        handler = Handler()
        self.edge.EdgeHandler._json(handler, 200, {"status": "ok"})

        self.assertEqual(200, handler.status)
        self.assertEqual("application/json", handler.sent_headers["Content-Type"])
        self.assertGreater(int(handler.sent_headers["Content-Length"]), 0)
        self.assertIn("HEAD", handler.sent_headers["Access-Control-Allow-Methods"])
        self.assertEqual(b"", handler.wfile.getvalue())

    def test_control_plane_route_predicate_is_narrow(self):
        self.assertTrue(self.edge.should_use_control_plane("/pricing"))
        self.assertTrue(self.edge.should_use_control_plane("/plans?currency=usd"))
        self.assertTrue(self.edge.should_use_control_plane("/model-catalog"))
        self.assertTrue(self.edge.should_use_control_plane("/features/agent-native"))
        self.assertTrue(self.edge.should_use_control_plane("/account/api-keys"))
        self.assertTrue(self.edge.should_use_control_plane("/analytics/funnel?days=30"))
        self.assertTrue(self.edge.should_use_control_plane("/admin/customers?limit=1"))
        self.assertTrue(self.edge.should_use_control_plane("/admin/customers/customer_1/suspend"))
        self.assertTrue(self.edge.should_use_control_plane("/admin/payment-intents/pi_1/approve"))
        self.assertTrue(self.edge.should_use_control_plane("/billing/stripe/webhook"))
        self.assertTrue(self.edge.should_use_control_plane("/v1/models"))
        self.assertFalse(self.edge.should_use_control_plane("/health"))

    def test_launch_funnel_edge_transform_promotes_auth_provider_state(self):
        body = (
            b'{"marketingIntent":{"authProviderState":{"total":4,"loaded":4,'
            b'"unavailable":0,"unknown":0,"githubEnabled":4,"githubDisabled":0,'
            b'"enabledProviders":{"github":4,"google":4,"discord":4,"none":0,"other":0},'
            b'"disabledProviders":{"github":0,"google":0,"discord":0,"none":4,"other":0}}}}'
        )
        headers = [("Content-Type", "application/json"), ("Content-Length", str(len(body)))]

        transformed = self.edge.transform_edge_response_body("/analytics/funnel?days=30", headers, 200, body)
        payload = self.edge.json.loads(transformed.decode("utf-8"))
        auth_state = payload["authProviderState"]

        self.assertEqual(4, auth_state["total"])
        self.assertEqual(4, auth_state["githubEnabled"])
        self.assertTrue(auth_state["githubAvailable"])
        self.assertEqual("marketing_funnel", auth_state["source"])
        self.assertEqual("email_first", auth_state["recommendedRecoveryAuth"])
        self.assertIn("email/password", auth_state["operatorGuidance"])
        self.assertEqual(4, auth_state["enabledProviders"]["github"])
        self.assertEqual(4, auth_state["disabledProviders"]["none"])

    def test_launch_funnel_edge_transform_keeps_current_auth_provider_state(self):
        body = b'{"authProviderState":{"total":1},"marketingIntent":{"authProviderState":{"total":4}}}'
        headers = [("Content-Type", "application/json"), ("Content-Length", str(len(body)))]

        transformed = self.edge.transform_edge_response_body("/analytics/funnel", headers, 200, body)

        self.assertEqual(body, transformed)

    def test_launch_funnel_edge_transform_only_buffers_small_uncompressed_json(self):
        body = b'{"marketingIntent":{}}'
        json_headers = [("Content-Type", "application/json"), ("Content-Length", str(len(body)))]
        encoded_headers = json_headers + [("Content-Encoding", "gzip")]

        self.assertTrue(self.edge.should_buffer_response_for_edge_transform("/analytics/funnel", json_headers, 200))
        self.assertFalse(self.edge.should_buffer_response_for_edge_transform("/analytics", json_headers, 200))
        self.assertFalse(self.edge.should_buffer_response_for_edge_transform("/analytics/funnel", encoded_headers, 200))
        self.assertFalse(self.edge.should_buffer_response_for_edge_transform("/analytics/funnel", json_headers, 500))

    def test_generated_key_model_routes_include_control_plane_fallback(self):
        upstream = self.edge.Upstream("http://tailnet.local:8790")
        upstream.set_health(True, latency_ms=10)
        control_plane = self.edge.Upstream("https://control.example.test")
        control_plane.set_health(True, latency_ms=500)
        old_upstreams = self.edge.UPSTREAMS
        old_control_plane = self.edge.CONTROL_PLANE_UPSTREAM
        try:
            self.edge.UPSTREAMS = [upstream]
            self.edge.CONTROL_PLANE_UPSTREAM = control_plane

            candidates = self.edge.generated_api_key_upstreams("/v1/chat/completions")
        finally:
            self.edge.UPSTREAMS = old_upstreams
            self.edge.CONTROL_PLANE_UPSTREAM = old_control_plane

        self.assertEqual([upstream, control_plane], candidates)

    def test_edge_token_bypasses_supabase_for_private_admin_access(self):
        self.edge.EDGE_TOKEN = "edge-secret"

        class Handler:
            path = "/v1/models"
            headers = {"Authorization": "Bearer edge-secret"}

        ctx = self.edge.EdgeHandler._auth_context(Handler())
        self.assertEqual("edge_token", ctx["type"])
        self.assertFalse(ctx["preserve_authorization"])

    def test_analytics_token_only_unlocks_operator_analytics(self):
        self.edge.ANALYTICS_TOKEN = "analytics-secret"

        class Handler:
            headers = {"Authorization": "Bearer analytics-secret"}

        for path in ("/analytics", "/analytics/funnel?days=30"):
            with self.subTest(path=path):
                Handler.path = path
                ctx = self.edge.EdgeHandler._auth_context(Handler())
                self.assertEqual("analytics_token", ctx["type"])
                self.assertFalse(ctx["preserve_authorization"])

        for path in ("/admin/customers", "/setup/model-modalities", "/v1/models"):
            with self.subTest(path=path):
                Handler.path = path
                self.assertIsNone(self.edge.EdgeHandler._auth_context(Handler()))

    def test_control_plane_routes_can_use_separate_outbound_token(self):
        self.edge.BACKEND_TOKEN = "tailnet-backend"
        self.edge.CONTROL_PLANE_TOKEN = "hosted-control-plane"

        self.assertEqual(
            "hosted-control-plane",
            self.edge.outbound_bearer_token("/analytics/funnel", {"type": "edge_token", "preserve_authorization": False}),
        )
        self.assertEqual(
            "hosted-control-plane",
            self.edge.outbound_bearer_token("/admin/customers", {"type": "edge_token", "preserve_authorization": False}),
        )
        self.assertEqual(
            None,
            self.edge.outbound_bearer_token("/v1/models", {"type": "generated_key", "preserve_authorization": False}),
        )
        self.assertEqual(
            "tailnet-backend",
            self.edge.outbound_bearer_token("/v1/chat/completions", {"type": "generated_key", "preserve_authorization": False}),
        )
        control_plane = self.edge.Upstream("https://control.example.test")
        old_control_plane = self.edge.CONTROL_PLANE_UPSTREAM
        try:
            self.edge.CONTROL_PLANE_UPSTREAM = control_plane
            self.assertEqual(
                "hosted-control-plane",
                self.edge.outbound_bearer_token(
                    "/v1/chat/completions",
                    {"type": "generated_key", "preserve_authorization": False},
                    control_plane,
                ),
            )
        finally:
            self.edge.CONTROL_PLANE_UPSTREAM = old_control_plane
        self.assertIsNone(
            self.edge.outbound_bearer_token("/account/api-keys", {"type": "supabase_user", "preserve_authorization": True})
        )

    def test_edge_identity_headers_forward_generated_key_customer_context(self):
        headers = self.edge.edge_identity_headers({
            "type": "generated_key",
            "key_id": "key-1",
            "customer_id": "customer-1",
            "user_id": "user-1",
            "plan": "pro",
            "customer_status": "active",
        })

        self.assertEqual("generated_key", headers["X-Sage-Router-Edge-Auth-Type"])
        self.assertEqual("customer-1", headers["X-Sage-Router-Customer-Id"])
        self.assertEqual("user-1", headers["X-Sage-Router-User-Id"])
        self.assertEqual("pro", headers["X-Sage-Router-Customer-Plan"])
        self.assertEqual("active", headers["X-Sage-Router-Customer-Status"])

    def test_generated_api_key_rate_limit_uses_plan_limit(self):
        ctx = {
            "type": "generated_key",
            "key_id": "key-1",
            "customer_id": "customer-1",
            "plan": "pro",
        }

        allowed, first = self.edge.check_rate_limit(ctx, "/v1/models")
        self.assertTrue(allowed)
        self.assertEqual(2, first["limit"])
        self.assertEqual(1, first["remaining"])

        allowed, second = self.edge.check_rate_limit(ctx, "/v1/chat/completions")
        self.assertTrue(allowed)
        self.assertEqual(0, second["remaining"])

        allowed, limited = self.edge.check_rate_limit(ctx, "/v1/models")
        self.assertFalse(allowed)
        self.assertEqual(2, limited["limit"])
        self.assertEqual(0, limited["remaining"])

    def test_generated_key_auth_attempts_are_rate_limited_before_auth_lookup(self):
        class Handler:
            path = "/v1/models"
            headers = {
                "Authorization": "Bearer sk_sage_random",
                "CF-Connecting-IP": "203.0.113.10",
            }
            client_address = ("127.0.0.1", 12345)

        allowed, first = self.edge.check_auth_attempt_rate_limit(Handler())
        self.assertTrue(allowed)
        self.assertEqual(2, first["limit"])
        self.assertEqual(1, first["remaining"])

        allowed, second = self.edge.check_auth_attempt_rate_limit(Handler())
        self.assertTrue(allowed)
        self.assertEqual(0, second["remaining"])

        allowed, limited = self.edge.check_auth_attempt_rate_limit(Handler())
        self.assertFalse(allowed)
        self.assertEqual(0, limited["remaining"])

    def test_auth_attempt_rate_limit_exempts_private_edge_token(self):
        self.edge.EDGE_TOKEN = "edge-secret"

        class Handler:
            path = "/v1/models"
            headers = {"Authorization": "Bearer edge-secret"}
            client_address = ("203.0.113.10", 12345)

        for _ in range(5):
            allowed, state = self.edge.check_auth_attempt_rate_limit(Handler())
            self.assertTrue(allowed)
            self.assertIsNone(state)

    def test_rate_limit_exempts_private_edge_token(self):
        ctx = {"type": "edge_token", "preserve_authorization": False}
        for _ in range(5):
            allowed, state = self.edge.check_rate_limit(ctx, "/v1/models")
            self.assertTrue(allowed)
            self.assertIsNone(state)

    def test_rate_limit_exempts_public_control_plane_metadata(self):
        ctx = {"type": "public_control_plane", "preserve_authorization": False}
        for _ in range(5):
            allowed, state = self.edge.check_rate_limit(ctx, "/pricing")
            self.assertTrue(allowed)
            self.assertIsNone(state)

    def test_default_rate_limit_applies_to_account_user_paths(self):
        ctx = {
            "type": "supabase_user",
            "user_id": "user-1",
            "preserve_authorization": True,
        }
        allowed, first = self.edge.check_rate_limit(ctx, "/account")
        self.assertTrue(allowed)
        self.assertEqual(1, first["limit"])

        allowed, limited = self.edge.check_rate_limit(ctx, "/account/api-keys")
        self.assertFalse(allowed)
        self.assertEqual(0, limited["remaining"])

    def test_generated_key_quota_uses_supabase_usage_rpc(self):
        calls = []
        ctx = {
            "type": "generated_key",
            "key_id": "key-1",
            "customer_id": "customer-1",
            "user_id": "user-1",
            "plan": "pro",
            "customer_status": "active",
        }

        def fake_post(path, payload, timeout=6):
            calls.append((path, payload))
            return {
                "customer_id": payload["p_customer_id"],
                "period": payload["p_period"],
                "requests": 1,
                "quota": payload["p_quota"],
                "remaining": 1,
                "allowed": True,
            }

        self.edge.supabase_post_json = fake_post
        allowed, state = self.edge.check_usage_quota(ctx, "/v1/models")

        self.assertTrue(allowed)
        self.assertEqual(1, len(calls))
        path, payload = calls[0]
        self.assertIn("/rest/v1/rpc/sage_router_increment_usage", path)
        self.assertEqual("customer-1", payload["p_customer_id"])
        self.assertEqual("user-1", payload["p_user_id"])
        self.assertEqual("pro", payload["p_plan"])
        self.assertEqual(2, payload["p_quota"])
        self.assertEqual(1, state["remaining"])
        self.assertEqual("1", str(self.edge.quota_headers(state)["X-Quota-Remaining"]))

    def test_generated_key_quota_denies_exhausted_plan(self):
        ctx = {
            "type": "generated_key",
            "key_id": "key-1",
            "customer_id": "customer-1",
            "user_id": "user-1",
            "plan": "pro",
            "customer_status": "active",
        }
        self.edge.supabase_post_json = lambda path, payload, timeout=6: {
            "customer_id": "customer-1",
            "period": payload["p_period"],
            "requests": 3,
            "quota": 2,
            "remaining": 0,
            "allowed": False,
        }

        allowed, state = self.edge.check_usage_quota(ctx, "/v1/chat/completions")

        self.assertFalse(allowed)
        self.assertEqual(3, state["requests"])
        self.assertEqual(0, state["remaining"])
        self.assertEqual("2", str(self.edge.quota_headers(state)["X-Quota-Limit"]))

    def test_quota_exhaustion_payload_guides_upgrade_without_secrets(self):
        ctx = {
            "type": "generated_key",
            "key_id": "key-1",
            "customer_id": "customer-1",
            "user_id": "user-1",
            "plan": "pro",
            "customer_status": "active",
        }
        state = {
            "customer_id": "customer-1",
            "period": "2026-06",
            "plan": "pro",
            "requests": 3,
            "quota": 2,
            "remaining": 0,
            "allowed": False,
            "reset_epoch": self.edge.quota_reset_epoch("2026-06"),
        }

        payload = self.edge.quota_recovery_payload("quota_exceeded", "/v1/chat/completions", state, ctx)
        encoded = str(payload)

        self.assertEqual("quota_exceeded", payload["error"])
        self.assertEqual("pro", payload["plan"])
        self.assertEqual(3, payload["used"])
        self.assertEqual(0, payload["remaining"])
        self.assertIn("upgrade=quota", payload["upgradeUrl"])
        self.assertIn("plan=pro", payload["upgradeUrl"])
        self.assertEqual("https://sagerouter.dev/billing", payload["billingUrl"])
        self.assertEqual("https://sagerouter.dev/support", payload["supportUrl"])
        self.assertEqual("upgrade_or_contact_support", payload["recovery"]["nextAction"])
        self.assertNotIn("sk_sage_test_key", encoded)
        self.assertNotIn("pepper", encoded)
        self.assertNotIn("service", encoded)

    def test_quota_infrastructure_payload_does_not_suggest_upgrade(self):
        state = {
            "error": "edge_quota_unavailable",
            "period": "2026-06",
            "plan": "pro",
            "quota": 2,
            "remaining": 0,
            "reset_epoch": self.edge.quota_reset_epoch("2026-06"),
        }

        payload = self.edge.quota_recovery_payload("edge_quota_unavailable", "/v1/models", state)

        self.assertEqual("edge_quota_unavailable", payload["error"])
        self.assertNotIn("upgradeUrl", payload)
        self.assertIn("statusUrl", payload)
        self.assertIn("supportUrl", payload)
        self.assertNotIn("recovery", payload)

    def test_quota_exempts_edge_token_and_non_model_paths(self):
        self.edge.supabase_post_json = lambda *_args, **_kwargs: self.fail("quota should not call Supabase")

        allowed, state = self.edge.check_usage_quota({"type": "edge_token"}, "/v1/models")
        self.assertTrue(allowed)
        self.assertIsNone(state)

        allowed, state = self.edge.check_usage_quota({
            "type": "generated_key",
            "customer_id": "customer-1",
            "plan": "pro",
        }, "/account")
        self.assertTrue(allowed)
        self.assertIsNone(state)

    def test_edge_records_model_modalities_from_router_headers(self):
        calls = []

        class ImmediateThread:
            def __init__(self, target, daemon=False, **_kwargs):
                self.target = target
                self.daemon = daemon

            def start(self):
                self.target()

        original_thread = self.edge.threading.Thread
        original_supabase_post_json = self.edge.supabase_post_json
        try:
            self.edge.threading.Thread = ImmediateThread
            self.edge.supabase_post_json = lambda path, payload, timeout=6: calls.append((path, payload, timeout)) or {}

            self.edge.record_model_modalities_from_response_headers([
                ("X-Sage-Router-Provider", "google"),
                ("X-Sage-Router-Model-Name", "gemini-2.5-pro"),
                ("X-Sage-Router-Modalities", "text,image,video"),
            ], 200)
        finally:
            self.edge.threading.Thread = original_thread
            self.edge.supabase_post_json = original_supabase_post_json

        self.assertEqual(1, len(calls))
        path, payload, _timeout = calls[0]
        self.assertIn("/rest/v1/rpc/", path)
        self.assertEqual("google", payload["provider_name"])
        self.assertEqual("gemini-2.5-pro", payload["model_name"])
        self.assertEqual(["image", "text", "video"], payload["modalities_in"])

    def test_edge_derives_model_modalities_from_body_when_headers_missing(self):
        request_body = b'{"model":"sage-router/frontier","input":[{"role":"user","content":[{"type":"input_image","image_url":"https://example.test/a.png"}]}]}'
        response_body = b'{"id":"resp_1","model":"openai-codex/gpt-5.4-mini","output":[]}'

        record = self.edge.modality_record_from_response(
            [("Content-Type", "application/json"), ("Content-Length", str(len(response_body)))],
            200,
            request_body=request_body,
            response_body=response_body,
        )

        self.assertEqual("openai-codex", record["provider"])
        self.assertEqual("gpt-5.4-mini", record["model"])
        self.assertEqual(["image", "text"], record["modalities"])

    def test_router_profile_response_keeps_client_visible_profile_model(self):
        request_body = b'{"model":"sage-router/frontier","messages":[{"role":"user","content":"hi"}]}'
        response_body = (
            b'{"id":"chatcmpl_1","model":"ollama/kimi-k2.5",'
            b'"choices":[{"message":{"role":"assistant","content":"[ollama/kimi-k2.5] [ollama/kimi-k2.5] done"}}]}'
        )
        headers = [
            ("Content-Type", "application/json"),
            ("Content-Length", str(len(response_body))),
            ("X-Sage-Router-Model", "ollama/kimi-k2.5"),
            ("X-Sage-Router-Provider", "ollama"),
            ("X-Sage-Router-Model-Name", "kimi-k2.5"),
            ("X-Sage-Router-Modalities", "text"),
        ]

        rewritten_headers, rewritten_body = self.edge.rewrite_router_profile_response(
            "/v1/chat/completions",
            request_body,
            headers,
            200,
            response_body,
        )
        payload = json.loads(rewritten_body.decode("utf-8"))
        header_map = {key.lower(): value for key, value in rewritten_headers}

        self.assertEqual("sage-router/frontier", payload["model"])
        self.assertEqual("ollama/kimi-k2.5", payload["upstream_model"])
        self.assertEqual("done", payload["choices"][0]["message"]["content"])
        self.assertEqual("sage-router/frontier", header_map["x-sage-router-model"])
        self.assertEqual("sage-router", header_map["x-sage-router-provider"])
        self.assertEqual("frontier", header_map["x-sage-router-model-name"])
        self.assertEqual("ollama/kimi-k2.5", header_map["x-sage-router-upstream-model"])
        self.assertEqual("ollama", header_map["x-sage-router-upstream-provider"])
        self.assertEqual("kimi-k2.5", header_map["x-sage-router-upstream-model-name"])
        self.assertNotIn("content-length", header_map)

    def test_router_profile_response_strips_prefix_from_responses_payload(self):
        request_body = b'{"model":"sage-router/frontier","input":[{"role":"user","content":"hi"}]}'
        response_body = (
            b'{"id":"resp_1","model":"ollama/glm-5.1",'
            b'"output_text":"[ollama/glm-5.1] prefix probe ok",'
            b'"output":[{"type":"message","content":[{"type":"output_text","text":"[ollama/glm-5.1] prefix probe ok"}]}]}'
        )
        headers = [
            ("Content-Type", "application/json"),
            ("Content-Length", str(len(response_body))),
            ("X-Sage-Router-Model", "ollama/glm-5.1"),
            ("X-Sage-Router-Provider", "ollama"),
            ("X-Sage-Router-Model-Name", "glm-5.1"),
        ]

        _headers, rewritten_body = self.edge.rewrite_router_profile_response(
            "/v1/responses",
            request_body,
            headers,
            200,
            response_body,
        )
        payload = json.loads(rewritten_body.decode("utf-8"))

        self.assertEqual("sage-router/frontier", payload["model"])
        self.assertEqual("prefix probe ok", payload["output_text"])
        self.assertEqual("prefix probe ok", payload["output"][0]["content"][0]["text"])

    def test_router_profile_sse_strips_prefix_from_responses_events(self):
        line = (
            b'data: {"type":"response.output_text.delta",'
            b'"delta":"[ollama/glm-5.1] [ollama/glm-5.1] streaming prefix probe ok"}\n'
        )

        sanitized = self.edge.sanitize_router_profile_sse_line(line)
        payload = json.loads(sanitized.decode("utf-8")[len("data: "):])

        self.assertEqual("streaming prefix probe ok", payload["delta"])

    def test_router_profile_sse_rewrites_profile_headers(self):
        request_body = b'{"model":"sage-router/frontier","input":[{"role":"user","content":"hi"}],"stream":true}'
        headers = [
            ("Content-Type", "text/event-stream"),
            ("X-Sage-Router-Model", "ollama/glm-5.1"),
            ("X-Sage-Router-Provider", "ollama"),
            ("X-Sage-Router-Model-Name", "glm-5.1"),
        ]

        rewritten_headers = self.edge.rewrite_router_profile_stream_headers(
            "/v1/responses",
            request_body,
            headers,
        )
        header_map = {key.lower(): value for key, value in rewritten_headers}

        self.assertEqual("sage-router/frontier", header_map["x-sage-router-model"])
        self.assertEqual("sage-router", header_map["x-sage-router-provider"])
        self.assertEqual("frontier", header_map["x-sage-router-model-name"])
        self.assertEqual("ollama/glm-5.1", header_map["x-sage-router-upstream-model"])
        self.assertEqual("ollama", header_map["x-sage-router-upstream-provider"])
        self.assertEqual("glm-5.1", header_map["x-sage-router-upstream-model-name"])

    def test_model_modality_record_prefers_upstream_headers(self):
        response_body = b'{"id":"chatcmpl_1","model":"sage-router/frontier","upstream_model":"ollama/kimi-k2.5","choices":[]}'

        record = self.edge.modality_record_from_response(
            [
                ("Content-Type", "application/json"),
                ("X-Sage-Router-Model", "sage-router/frontier"),
                ("X-Sage-Router-Provider", "sage-router"),
                ("X-Sage-Router-Model-Name", "frontier"),
                ("X-Sage-Router-Upstream-Model", "ollama/kimi-k2.5"),
                ("X-Sage-Router-Upstream-Provider", "ollama"),
                ("X-Sage-Router-Upstream-Model-Name", "kimi-k2.5"),
                ("X-Sage-Router-Modalities", "text"),
            ],
            200,
            request_body=b'{"model":"sage-router/frontier","messages":[{"role":"user","content":"hi"}]}',
            response_body=response_body,
        )

        self.assertEqual("ollama", record["provider"])
        self.assertEqual("kimi-k2.5", record["model"])
        self.assertEqual(["text"], record["modalities"])

    def test_model_modality_setup_routes_to_control_plane(self):
        self.assertTrue(self.edge.should_use_control_plane("/setup/model-modalities"))
        self.assertTrue(self.edge.should_use_control_plane("/setup/model-modalities/update"))
        self.assertFalse(self.edge.should_use_control_plane("/setup/credentials"))

    def test_public_api_dashboard_routes_to_control_plane(self):
        self.assertTrue(self.edge.should_use_control_plane("/"))
        self.assertTrue(self.edge.should_use_control_plane("/dashboard"))
        self.assertTrue(self.edge.should_use_control_plane("/dashboard/"))
        self.assertTrue(self.edge.should_use_control_plane("/v1/models"))


if __name__ == "__main__":
    unittest.main()
