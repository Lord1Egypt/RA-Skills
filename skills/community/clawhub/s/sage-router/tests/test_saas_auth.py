#!/usr/bin/env python3
import json
import os
import tempfile
import unittest
from io import BytesIO
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
os.environ.setdefault('SAGE_ROUTER_DARIO_AUTOSTART', '0')
os.environ.setdefault('SAGE_ROUTER_BUNDLED_OLLAMA_AUTOSTART', '0')
os.environ.setdefault('SAGE_ROUTER_SUPABASE_AUTH_ENABLED', '0')

import sys
sys.path.insert(0, str(ROOT))
import router  # noqa: E402
# Tests in this module exercise the hosted billing tier. The router
# does not collect user identities by default, so opt in here.
os.environ.setdefault('SAGE_ROUTER_BILLING_ENABLED', '1')



class SaaSAuthTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        # Hosted billing tier is required to look up a customer for a user.
        self._billing_env = os.environ.get('SAGE_ROUTER_BILLING_ENABLED')
        os.environ['SAGE_ROUTER_BILLING_ENABLED'] = '1'
        self.old = {
            'CUSTOMER_STORE_PATH': router.CUSTOMER_STORE_PATH,
            'SUPABASE_URL': router.SUPABASE_URL,
            'SUPABASE_SERVICE_ROLE_KEY': router.SUPABASE_SERVICE_ROLE_KEY,
            'SUPABASE_USAGE_COUNTERS_TABLE': router.SUPABASE_USAGE_COUNTERS_TABLE,
            'SUPABASE_FUNNEL_EVENTS_TABLE': router.SUPABASE_FUNNEL_EVENTS_TABLE,
            'supabase_select': router.supabase_select,
            'CLIENT_API_KEYS': list(router.CLIENT_API_KEYS),
            'CLIENT_AUTH_REQUIRED': router.CLIENT_AUTH_REQUIRED,
            'ANALYTICS_TOKEN': router.ANALYTICS_TOKEN,
            'SUPABASE_AUTH_ENABLED': router.SUPABASE_AUTH_ENABLED,
            'REQUIRE_VERIFIED_EMAIL': router.REQUIRE_VERIFIED_EMAIL,
            'STRIPE_SECRET_KEY': router.STRIPE_SECRET_KEY,
            'STRIPE_PRICE_ID': router.STRIPE_PRICE_ID,
            'STRIPE_PRICE_IDS_RAW': router.STRIPE_PRICE_IDS_RAW,
            'STRIPE_WEBHOOK_SECRET': router.STRIPE_WEBHOOK_SECRET,
            'stripe_request': router.stripe_request,
            'CRYPTO_PAYMENT_ADDRESS': router.CRYPTO_PAYMENT_ADDRESS,
            'PUBLIC_BASE_URL': router.PUBLIC_BASE_URL,
            'MARKETING_BASE_URL': router.MARKETING_BASE_URL,
            'APP_BASE_URL': router.APP_BASE_URL,
            'API_BASE_URL': router.API_BASE_URL,
            'MAX_ACTIVE_API_KEYS_PER_CUSTOMER': router.MAX_ACTIVE_API_KEYS_PER_CUSTOMER,
            'PUBLIC_PLAN_RATE_LIMITS_RAW': router.PUBLIC_PLAN_RATE_LIMITS_RAW,
            'PUBLIC_PLAN_MONTHLY_QUOTAS_RAW': router.PUBLIC_PLAN_MONTHLY_QUOTAS_RAW,
            'supabase_user_for_bearer': router.supabase_user_for_bearer,
            'ROUTE_EVENTS_PATH': router.ROUTE_EVENTS_PATH,
            'FIRESTORE_ENABLED': router.FIRESTORE_ENABLED,
            'SUPABASE_MIRROR_ENABLED': router.SUPABASE_MIRROR_ENABLED,
            'read_launch_waitlist_counts': router.read_launch_waitlist_counts,
            'read_launch_marketing_funnel_counts': router.read_launch_marketing_funnel_counts,
            'read_launch_auth_user_rows': router.read_launch_auth_user_rows,
            'ACTIVATION_EMAIL_PROVIDER': router.ACTIVATION_EMAIL_PROVIDER,
            'ACTIVATION_EMAIL_API_KEY': router.ACTIVATION_EMAIL_API_KEY,
            'ACTIVATION_EMAIL_FROM': router.ACTIVATION_EMAIL_FROM,
            'ACTIVATION_EMAIL_REPLY_TO': router.ACTIVATION_EMAIL_REPLY_TO,
            'ACTIVATION_EMAIL_MAX_BATCH': router.ACTIVATION_EMAIL_MAX_BATCH,
            'ACTIVATION_EMAIL_REDIRECT_TO': router.ACTIVATION_EMAIL_REDIRECT_TO,
            'SUPABASE_URL': router.SUPABASE_URL,
            'SUPABASE_ANON_KEY': router.SUPABASE_ANON_KEY,
            'send_activation_email': router.send_activation_email,
        }
        router.CUSTOMER_STORE_PATH = os.path.join(self.tmp.name, 'customers.json')
        router.SUPABASE_URL = ''
        router.SUPABASE_SERVICE_ROLE_KEY = ''
        router.SUPABASE_USAGE_COUNTERS_TABLE = 'sage_router_usage_counters'
        router.SUPABASE_FUNNEL_EVENTS_TABLE = 'sage_router_funnel_events'
        router.CLIENT_API_KEYS = []
        router.CLIENT_AUTH_REQUIRED = True
        router.ANALYTICS_TOKEN = ''
        router.SUPABASE_AUTH_ENABLED = False
        router.REQUIRE_VERIFIED_EMAIL = True
        router.STRIPE_SECRET_KEY = ''
        router.STRIPE_PRICE_ID = ''
        router.STRIPE_PRICE_IDS_RAW = ''
        router.STRIPE_WEBHOOK_SECRET = ''
        router.CRYPTO_PAYMENT_ADDRESS = ''
        router.PUBLIC_BASE_URL = 'https://app.sagerouter.dev'
        router.MARKETING_BASE_URL = 'https://sagerouter.dev'
        router.APP_BASE_URL = 'https://app.sagerouter.dev'
        router.API_BASE_URL = 'https://api.sagerouter.dev'
        router.MAX_ACTIVE_API_KEYS_PER_CUSTOMER = 5
        router.PUBLIC_PLAN_RATE_LIMITS_RAW = 'trial=30,lite=60,pro=180,max=600,manual=600,paid=180,active=180,default=60'
        router.PUBLIC_PLAN_MONTHLY_QUOTAS_RAW = 'trial=1000,lite=10000,pro=50000,max=200000,paid=50000,active=50000,default=0'
        router.ROUTE_EVENTS_PATH = os.path.join(self.tmp.name, 'route-events.jsonl')
        router.FIRESTORE_ENABLED = False
        router.SUPABASE_MIRROR_ENABLED = False
        router.ACTIVATION_EMAIL_PROVIDER = 'resend'
        router.ACTIVATION_EMAIL_API_KEY = ''
        router.ACTIVATION_EMAIL_FROM = ''
        router.ACTIVATION_EMAIL_REPLY_TO = ''
        router.ACTIVATION_EMAIL_MAX_BATCH = 25
        router.ACTIVATION_EMAIL_REDIRECT_TO = 'https://app.sagerouter.dev/account?activation=recovery'

    def tearDown(self):
        router.CUSTOMER_STORE_PATH = self.old['CUSTOMER_STORE_PATH']
        router.SUPABASE_URL = self.old['SUPABASE_URL']
        router.SUPABASE_SERVICE_ROLE_KEY = self.old['SUPABASE_SERVICE_ROLE_KEY']
        router.SUPABASE_USAGE_COUNTERS_TABLE = self.old['SUPABASE_USAGE_COUNTERS_TABLE']
        router.SUPABASE_FUNNEL_EVENTS_TABLE = self.old['SUPABASE_FUNNEL_EVENTS_TABLE']
        router.supabase_select = self.old['supabase_select']
        router.CLIENT_API_KEYS = self.old['CLIENT_API_KEYS']
        router.CLIENT_AUTH_REQUIRED = self.old['CLIENT_AUTH_REQUIRED']
        router.ANALYTICS_TOKEN = self.old['ANALYTICS_TOKEN']
        router.SUPABASE_AUTH_ENABLED = self.old['SUPABASE_AUTH_ENABLED']
        router.REQUIRE_VERIFIED_EMAIL = self.old['REQUIRE_VERIFIED_EMAIL']
        router.STRIPE_SECRET_KEY = self.old['STRIPE_SECRET_KEY']
        router.STRIPE_PRICE_ID = self.old['STRIPE_PRICE_ID']
        router.STRIPE_PRICE_IDS_RAW = self.old['STRIPE_PRICE_IDS_RAW']
        router.STRIPE_WEBHOOK_SECRET = self.old['STRIPE_WEBHOOK_SECRET']
        router.stripe_request = self.old['stripe_request']
        router.CRYPTO_PAYMENT_ADDRESS = self.old['CRYPTO_PAYMENT_ADDRESS']
        router.PUBLIC_BASE_URL = self.old['PUBLIC_BASE_URL']
        router.MARKETING_BASE_URL = self.old['MARKETING_BASE_URL']
        router.APP_BASE_URL = self.old['APP_BASE_URL']
        router.API_BASE_URL = self.old['API_BASE_URL']
        router.MAX_ACTIVE_API_KEYS_PER_CUSTOMER = self.old['MAX_ACTIVE_API_KEYS_PER_CUSTOMER']
        router.PUBLIC_PLAN_RATE_LIMITS_RAW = self.old['PUBLIC_PLAN_RATE_LIMITS_RAW']
        router.PUBLIC_PLAN_MONTHLY_QUOTAS_RAW = self.old['PUBLIC_PLAN_MONTHLY_QUOTAS_RAW']
        router.supabase_user_for_bearer = self.old['supabase_user_for_bearer']
        router.ROUTE_EVENTS_PATH = self.old['ROUTE_EVENTS_PATH']
        router.FIRESTORE_ENABLED = self.old['FIRESTORE_ENABLED']
        router.SUPABASE_MIRROR_ENABLED = self.old['SUPABASE_MIRROR_ENABLED']
        router.read_launch_waitlist_counts = self.old['read_launch_waitlist_counts']
        router.read_launch_marketing_funnel_counts = self.old['read_launch_marketing_funnel_counts']
        router.read_launch_auth_user_rows = self.old['read_launch_auth_user_rows']
        router.ACTIVATION_EMAIL_PROVIDER = self.old['ACTIVATION_EMAIL_PROVIDER']
        router.ACTIVATION_EMAIL_API_KEY = self.old['ACTIVATION_EMAIL_API_KEY']
        router.ACTIVATION_EMAIL_FROM = self.old['ACTIVATION_EMAIL_FROM']
        router.ACTIVATION_EMAIL_REPLY_TO = self.old['ACTIVATION_EMAIL_REPLY_TO']
        router.ACTIVATION_EMAIL_MAX_BATCH = self.old['ACTIVATION_EMAIL_MAX_BATCH']
        router.ACTIVATION_EMAIL_REDIRECT_TO = self.old['ACTIVATION_EMAIL_REDIRECT_TO']
        router.SUPABASE_URL = self.old['SUPABASE_URL']
        router.SUPABASE_ANON_KEY = self.old['SUPABASE_ANON_KEY']
        router.send_activation_email = self.old['send_activation_email']
        if self._billing_env is None:
            os.environ.pop('SAGE_ROUTER_BILLING_ENABLED', None)
        else:
            os.environ['SAGE_ROUTER_BILLING_ENABLED'] = self._billing_env
        self.tmp.cleanup()

    def active_customer(self):
        customer = router.customer_for_user({'id': 'user-1', 'email': 'u@example.com'})
        data = router.local_customer_store()
        data['customers'][0]['plan'] = 'pro'
        data['customers'][0]['status'] = 'active'
        router.write_local_customer_store(data)
        return router.customer_for_user({'id': 'user-1'}, create=False)

    def signed_stripe_webhook_handler(self, event):
        body = json.dumps(event, separators=(',', ':')).encode()
        timestamp = str(router.now_epoch())
        sig = router.hmac.new(
            router.STRIPE_WEBHOOK_SECRET.encode(),
            f'{timestamp}.{body.decode()}'.encode(),
            router.hashlib.sha256,
        ).hexdigest()

        class Dummy:
            path = '/billing/stripe/webhook'
            def __init__(self):
                self.headers = {'Content-Length': str(len(body)), 'Stripe-Signature': f't={timestamp},v1={sig}'}
                self.rfile = BytesIO(body)
                self.status = None
                self.payload = None
            def write_json(self, status, payload, extra_headers=None):
                self.status = status
                self.payload = payload

        return Dummy()

    def test_generated_key_is_hashed_and_verifies_when_active(self):
        customer = self.active_customer()
        raw, row = router.create_api_key_for_customer(customer, 'prod')
        self.assertNotIn(raw, json.dumps(router.local_customer_store()))
        self.assertEqual(router.api_key_hash(raw), row['api_key_hash'])
        ctx = router.verify_generated_api_key(raw)
        self.assertEqual('generated_key', ctx['type'])
        self.assertEqual(customer['id'], ctx['customer']['id'])

    def test_active_api_key_limit_blocks_new_keys_until_revoke(self):
        router.MAX_ACTIVE_API_KEYS_PER_CUSTOMER = 2
        customer = self.active_customer()
        first_raw, first_row = router.create_api_key_for_customer(customer, 'first')
        router.create_api_key_for_customer(customer, 'second')

        with self.assertRaisesRegex(ValueError, 'active_api_key_limit_reached:2'):
            router.create_api_key_for_customer(customer, 'third')

        router.revoke_api_key_for_customer(customer['id'], first_row['id'])
        replacement_raw, _replacement = router.create_api_key_for_customer(customer, 'replacement')

        self.assertNotEqual(first_raw, replacement_raw)
        self.assertEqual(2, router.active_api_key_count_for_customer(customer['id']))

    def test_account_api_key_endpoint_returns_conflict_at_active_key_limit(self):
        router.MAX_ACTIVE_API_KEYS_PER_CUSTOMER = 1
        router.supabase_user_for_bearer = lambda token: {'id': 'user-1', 'email': 'u@example.com'}
        customer = router.customer_for_user({'id': 'user-1', 'email': 'u@example.com'})
        router.update_customer(customer['id'], {'plan': 'pro', 'status': 'active'})
        router.create_api_key_for_customer(router.customer_by_id(customer['id']), 'existing')
        body = b'{"name":"overflow"}'

        class Dummy:
            path = '/account/api-keys'
            headers = {'Authorization': 'Bearer valid-user-jwt', 'Content-Length': str(len(body))}
            rfile = BytesIO(body)
            status = None
            payload = None

            def write_json(self, status, payload, extra_headers=None):
                self.status = status
                self.payload = payload

        handler = Dummy()
        router.Handler.do_POST(handler)

        self.assertEqual(409, handler.status)
        self.assertEqual('active_api_key_limit_reached', handler.payload['error'])
        self.assertEqual(1, handler.payload['maxActiveApiKeysPerCustomer'])

    def test_hosted_account_reports_unverified_email_state(self):
        router.SUPABASE_AUTH_ENABLED = True
        router.REQUIRE_VERIFIED_EMAIL = True
        router.supabase_user_for_bearer = lambda token: {
            'id': 'user-verify',
            'email': 'verify@example.com',
            'user_metadata': {'email': 'verify@example.com'},
        } if token == 'valid-user-jwt' else None

        class Dummy:
            path = '/account'
            headers = {'Authorization': 'Bearer valid-user-jwt'}
            status = None
            payload = None

            def write_json(self, status, payload, extra_headers=None):
                self.status = status
                self.payload = payload

        handler = Dummy()
        router.Handler.do_GET(handler)

        self.assertEqual(200, handler.status)
        self.assertEqual('verify@example.com', handler.payload['emailVerification']['email'])
        self.assertTrue(handler.payload['emailVerification']['required'])
        self.assertFalse(handler.payload['emailVerification']['verified'])

    def test_unverified_hosted_user_can_create_non_routing_key_but_not_checkout(self):
        router.SUPABASE_AUTH_ENABLED = True
        router.REQUIRE_VERIFIED_EMAIL = True
        router.STRIPE_SECRET_KEY = 'sk_test'
        router.STRIPE_PRICE_IDS_RAW = 'pro=price_pro'
        router.supabase_user_for_bearer = lambda token: {
            'id': 'user-unverified',
            'email': 'unverified@example.com',
        } if token == 'valid-user-jwt' else None

        class Dummy:
            def __init__(self, path, body=b'{}'):
                self.path = path
                self.headers = {'Authorization': 'Bearer valid-user-jwt', 'Content-Length': str(len(body))}
                self.rfile = BytesIO(body)
                self.status = None
                self.payload = None

            def write_json(self, status, payload, extra_headers=None):
                self.status = status
                self.payload = payload

        key_handler = Dummy('/account/api-keys', b'{"name":"prod"}')
        router.Handler.do_POST(key_handler)
        self.assertEqual(201, key_handler.status)
        self.assertTrue(key_handler.payload['key'].startswith('sk_sage_'))
        self.assertFalse(key_handler.payload['api_key']['routing_enabled'])
        self.assertFalse(key_handler.payload['emailVerification']['verified'])
        customer = router.customer_for_user({'id': 'user-unverified'}, create=False)
        self.assertEqual(1, router.active_api_key_count_for_customer(customer['id']))
        self.assertIsNone(router.verify_generated_api_key(key_handler.payload['key']))

        checkout_handler = Dummy('/billing/stripe/checkout', b'{"plan":"pro"}')
        router.Handler.do_POST(checkout_handler)
        self.assertEqual(403, checkout_handler.status)
        self.assertEqual('email_verification_required', checkout_handler.payload['error'])

    def test_unverified_hosted_user_can_revoke_own_generated_key(self):
        router.SUPABASE_AUTH_ENABLED = True
        router.REQUIRE_VERIFIED_EMAIL = True
        router.supabase_user_for_bearer = lambda token: {
            'id': 'user-unverified',
            'email': 'unverified@example.com',
        } if token == 'valid-user-jwt' else None
        customer = router.customer_for_user({'id': 'user-unverified', 'email': 'unverified@example.com'})
        router.update_customer(customer['id'], {'plan': 'pro', 'status': 'active'})
        active_customer = router.customer_by_id(customer['id'])
        raw, row = router.create_api_key_for_customer(active_customer, 'leaked')
        self.assertIsNotNone(router.verify_generated_api_key(raw))

        class Dummy:
            def __init__(self):
                self.path = f'/account/api-keys/{row["id"]}/revoke'
                self.headers = {'Authorization': 'Bearer valid-user-jwt', 'Content-Length': '2'}
                self.rfile = BytesIO(b'{}')
                self.status = None
                self.payload = None

            def write_json(self, status, payload, extra_headers=None):
                self.status = status
                self.payload = payload

        handler = Dummy()
        router.Handler.do_POST(handler)

        self.assertEqual(200, handler.status)
        self.assertEqual('revoked', handler.payload['api_key']['status'])
        self.assertEqual('api_key.revoke', handler.payload['auditEvent']['action'])
        self.assertEqual('customer', handler.payload['auditEvent']['actor'])
        self.assertEqual('customer_request', handler.payload['auditEvent']['reason_code'])
        self.assertEqual(1, handler.payload['auditEvent']['revoked_api_keys_count'])
        self.assertNotIn('api_key_hash', json.dumps(handler.payload['auditEvent']))
        self.assertEqual(1, len(router.operator_audit_events_for_customer(customer['id'])))
        self.assertIsNone(router.verify_generated_api_key(raw))

        second = Dummy()
        router.Handler.do_POST(second)
        self.assertEqual(200, second.status)
        self.assertIsNone(second.payload['auditEvent'])
        self.assertEqual(1, len(router.operator_audit_events_for_customer(customer['id'])))

    def test_hosted_user_cannot_revoke_another_customers_key(self):
        router.SUPABASE_AUTH_ENABLED = True
        router.REQUIRE_VERIFIED_EMAIL = True
        router.supabase_user_for_bearer = lambda token: {
            'id': 'user-a',
            'email': 'a@example.com',
            'email_confirmed_at': '2026-06-20T00:00:00Z',
        } if token == 'valid-user-jwt' else None
        customer_a = router.customer_for_user({'id': 'user-a', 'email': 'a@example.com'})
        customer_b = router.customer_for_user({'id': 'user-b', 'email': 'b@example.com'})
        router.update_customer(customer_a['id'], {'plan': 'pro', 'status': 'active'})
        router.update_customer(customer_b['id'], {'plan': 'pro', 'status': 'active'})
        active_b = router.customer_by_id(customer_b['id'])
        raw_b, row_b = router.create_api_key_for_customer(active_b, 'belongs-to-b')

        class Dummy:
            def __init__(self):
                self.path = f'/account/api-keys/{row_b["id"]}/revoke'
                self.headers = {'Authorization': 'Bearer valid-user-jwt', 'Content-Length': '2'}
                self.rfile = BytesIO(b'{}')
                self.status = None
                self.payload = None

            def write_json(self, status, payload, extra_headers=None):
                self.status = status
                self.payload = payload

        handler = Dummy()
        router.Handler.do_POST(handler)

        self.assertEqual(404, handler.status)
        self.assertEqual('api_key_not_found', handler.payload['error'])
        self.assertIsNotNone(router.verify_generated_api_key(raw_b))

    def test_verified_hosted_user_can_create_generated_key(self):
        router.SUPABASE_AUTH_ENABLED = True
        router.REQUIRE_VERIFIED_EMAIL = True
        router.supabase_user_for_bearer = lambda token: {
            'id': 'user-verified',
            'email': 'verified@example.com',
            'email_confirmed_at': '2026-06-20T00:00:00Z',
        } if token == 'valid-user-jwt' else None

        class Dummy:
            path = '/account/api-keys'
            headers = {'Authorization': 'Bearer valid-user-jwt', 'Content-Length': '15'}
            rfile = BytesIO(b'{"name":"prod"}')
            status = None
            payload = None

            def write_json(self, status, payload, extra_headers=None):
                self.status = status
                self.payload = payload

        handler = Dummy()
        router.Handler.do_POST(handler)

        self.assertEqual(201, handler.status)
        self.assertTrue(handler.payload['key'].startswith('sk_sage_'))
        self.assertNotIn(handler.payload['key'], json.dumps(router.local_customer_store()))

    def test_untrusted_browser_origin_cannot_mutate_account_billing_or_operator_state(self):
        calls = []

        def fail_if_called(token):
            calls.append(token)
            return {'id': 'user-1', 'email': 'u@example.com'}

        router.supabase_user_for_bearer = fail_if_called

        class Dummy:
            def __init__(self, path, body=b'{}'):
                self.path = path
                self.headers = {
                    'Authorization': 'Bearer valid-user-jwt',
                    'Content-Length': str(len(body)),
                    'Origin': 'https://evil.example',
                }
                self.rfile = BytesIO(body)
                self.status = None
                self.payload = None

            def write_json(self, status, payload, extra_headers=None):
                self.status = status
                self.payload = payload

        for path in (
            '/account/api-keys',
            '/account/api-keys/key_1/revoke',
            '/billing/stripe/checkout',
            '/billing/stripe/portal',
            '/billing/crypto/intent',
            '/admin/customers/customer_1/suspend',
            '/admin/customers/customer_1/unsuspend',
        ):
            handler = Dummy(path)
            router.Handler.do_POST(handler)
            self.assertEqual(403, handler.status, path)
            self.assertEqual('origin_not_allowed', handler.payload['error'], path)

        self.assertEqual([], calls)

    def test_trusted_browser_origin_can_create_generated_key(self):
        router.SUPABASE_AUTH_ENABLED = True
        router.REQUIRE_VERIFIED_EMAIL = True
        router.supabase_user_for_bearer = lambda token: {
            'id': 'user-trusted-origin',
            'email': 'trusted@example.com',
            'email_confirmed_at': '2026-06-20T00:00:00Z',
        } if token == 'valid-user-jwt' else None

        class Dummy:
            path = '/account/api-keys'
            headers = {
                'Authorization': 'Bearer valid-user-jwt',
                'Content-Length': '15',
                'Origin': 'https://app.sagerouter.dev',
            }
            rfile = BytesIO(b'{"name":"prod"}')
            status = None
            payload = None

            def write_json(self, status, payload, extra_headers=None):
                self.status = status
                self.payload = payload

        handler = Dummy()
        router.Handler.do_POST(handler)

        self.assertEqual(201, handler.status)
        self.assertTrue(handler.payload['key'].startswith('sk_sage_'))

    def test_revoked_and_inactive_generated_keys_do_not_authorize(self):
        customer = self.active_customer()
        raw, row = router.create_api_key_for_customer(customer, 'prod')
        router.revoke_api_key_for_customer(customer['id'], row['id'])
        self.assertIsNone(router.verify_generated_api_key(raw))

        customer = router.customer_for_user({'id': 'user-2', 'email': 'u2@example.com'})
        raw, _row = router.create_api_key_for_customer(customer, 'inactive')
        self.assertIsNone(router.verify_generated_api_key(raw))

    def test_private_analytics_token_authorizes_operator_setup(self):
        router.CLIENT_AUTH_REQUIRED = True
        router.CLIENT_API_KEYS = []
        router.ANALYTICS_TOKEN = 'private-admin-token'

        class Dummy:
            headers = {'Authorization': 'Bearer private-admin-token'}

        self.assertTrue(router.operator_request_authorized(Dummy()))

    def test_operator_suspend_customer_revokes_active_keys_and_blocks_routing(self):
        router.CLIENT_API_KEYS = ['operator-token']
        customer = self.active_customer()
        first_raw, _first = router.create_api_key_for_customer(customer, 'first')
        second_raw, _second = router.create_api_key_for_customer(customer, 'second')
        body = b'{"reasonCode":"provider_risk"}'

        class Dummy:
            def __init__(self):
                self.path = f'/admin/customers/{customer["id"]}/suspend'
                self.headers = {'Authorization': 'Bearer operator-token', 'Content-Length': str(len(body))}
                self.rfile = BytesIO(body)
                self.status = None
                self.payload = None

            def write_json(self, status, payload, extra_headers=None):
                self.status = status
                self.payload = payload

        handler = Dummy()
        router.Handler.do_POST(handler)

        self.assertEqual(200, handler.status)
        self.assertEqual('suspended', handler.payload['status'])
        self.assertEqual(2, handler.payload['revokedApiKeys'])
        self.assertEqual('customer.suspend', handler.payload['auditEvent']['action'])
        self.assertEqual('provider_risk', handler.payload['auditEvent']['reason_code'])
        self.assertEqual('active', handler.payload['auditEvent']['status_before'])
        self.assertEqual('suspended', handler.payload['auditEvent']['status_after'])
        self.assertEqual(2, handler.payload['auditEvent']['revoked_api_keys_count'])
        self.assertNotIn('api_key_hash', json.dumps(handler.payload['auditEvent']))
        self.assertEqual('suspended', router.customer_by_id(customer['id'])['status'])
        self.assertEqual(0, router.active_api_key_count_for_customer(customer['id']))
        self.assertIsNone(router.verify_generated_api_key(first_raw))
        self.assertIsNone(router.verify_generated_api_key(second_raw))
        self.assertEqual(1, len(router.operator_audit_events_for_customer(customer['id'])))

    def test_operator_unsuspend_defaults_to_inactive_and_keeps_keys_revoked(self):
        router.CLIENT_API_KEYS = ['operator-token']
        customer = self.active_customer()
        raw, _row = router.create_api_key_for_customer(customer, 'first')
        router.suspend_customer_for_operator(customer['id'])

        class Dummy:
            def __init__(self):
                self.path = f'/admin/customers/{customer["id"]}/unsuspend'
                self.headers = {'Authorization': 'Bearer operator-token', 'Content-Length': '2'}
                self.rfile = BytesIO(b'{}')
                self.status = None
                self.payload = None

            def write_json(self, status, payload, extra_headers=None):
                self.status = status
                self.payload = payload

        handler = Dummy()
        router.Handler.do_POST(handler)

        updated = router.customer_by_id(customer['id'])
        self.assertEqual(200, handler.status)
        self.assertEqual('inactive', handler.payload['status'])
        self.assertTrue(handler.payload['revokedApiKeysRemainRevoked'])
        self.assertEqual('customer.unsuspend', handler.payload['auditEvent']['action'])
        self.assertEqual('suspended', handler.payload['auditEvent']['status_before'])
        self.assertEqual('inactive', handler.payload['auditEvent']['status_after'])
        self.assertEqual('inactive', updated['status'])
        self.assertFalse(router.customer_is_active(updated))
        self.assertEqual(0, router.active_api_key_count_for_customer(customer['id']))
        self.assertIsNone(router.verify_generated_api_key(raw))

    def test_operator_unsuspend_can_reactivate_without_restoring_revoked_keys(self):
        router.CLIENT_API_KEYS = ['operator-token']
        customer = self.active_customer()
        raw, _row = router.create_api_key_for_customer(customer, 'first')
        router.suspend_customer_for_operator(customer['id'])
        body = b'{"status":"active"}'

        class Dummy:
            def __init__(self):
                self.path = f'/admin/customers/{customer["id"]}/unsuspend'
                self.headers = {'Authorization': 'Bearer operator-token', 'Content-Length': str(len(body))}
                self.rfile = BytesIO(body)
                self.status = None
                self.payload = None

            def write_json(self, status, payload, extra_headers=None):
                self.status = status
                self.payload = payload

        handler = Dummy()
        router.Handler.do_POST(handler)

        updated = router.customer_by_id(customer['id'])
        self.assertEqual(200, handler.status)
        self.assertEqual('active', handler.payload['status'])
        self.assertEqual('customer.unsuspend', handler.payload['auditEvent']['action'])
        self.assertEqual('active', handler.payload['auditEvent']['status_after'])
        self.assertEqual('active', updated['status'])
        self.assertTrue(router.customer_is_active(updated))
        self.assertEqual(0, router.active_api_key_count_for_customer(customer['id']))
        self.assertIsNone(router.verify_generated_api_key(raw))

        fresh_raw, _fresh = router.create_api_key_for_customer(updated, 'after-review')
        self.assertIsNotNone(router.verify_generated_api_key(fresh_raw))

    def test_operator_customer_lookup_is_private_and_omits_key_hashes(self):
        router.CLIENT_API_KEYS = ['operator-token']
        customer = self.active_customer()
        _raw, _row = router.create_api_key_for_customer(customer, 'prod')
        other = router.customer_for_user({'id': 'user-2', 'email': 'other@example.com'})

        class Dummy:
            def __init__(self, path, token='operator-token'):
                self.path = path
                self.headers = {'Authorization': f'Bearer {token}'}
                self.status = None
                self.payload = None

            def write_json(self, status, payload, extra_headers=None):
                self.status = status
                self.payload = payload

        unauthorized = Dummy('/admin/customers', token='bad-token')
        router.Handler.do_GET(unauthorized)
        self.assertEqual(401, unauthorized.status)

        listing = Dummy('/admin/customers?q=u%40example.com&limit=10')
        router.Handler.do_GET(listing)
        self.assertEqual(200, listing.status)
        self.assertEqual(1, listing.payload['count'])
        self.assertEqual(1, listing.payload['returned'])
        self.assertEqual({'active': 1}, listing.payload['statusCounts'])
        self.assertEqual({'send_first_request': 1}, listing.payload['nextActions'])
        self.assertIn('verified', listing.payload['emailVerification'])
        self.assertEqual(0, listing.payload['noKeyCreateKey'])
        self.assertTrue(listing.payload['hasEmails'])
        self.assertEqual(customer['id'], listing.payload['customers'][0]['customer']['id'])
        self.assertIn('no_first_request', listing.payload['customers'][0]['review']['flagCodes'])
        self.assertEqual('warn', listing.payload['customers'][0]['review']['severity'])
        self.assertIn('emailVerification', listing.payload['customers'][0])
        self.assertIn('verified', listing.payload['customers'][0]['emailVerification'])
        self.assertIn('followUp', listing.payload['customers'][0])
        self.assertIn('/login.html?', listing.payload['customers'][0]['followUp']['passwordFallback'])
        self.assertIn('auth=email', listing.payload['customers'][0]['followUp']['passwordFallback'])
        self.assertIn('signup_to_key_recovery', listing.payload['customers'][0]['followUp']['passwordFallback'])
        self.assertIn('/account.html?', listing.payload['customers'][0]['followUp']['githubOAuth'])
        self.assertIn('auth=github', listing.payload['customers'][0]['followUp']['githubOAuth'])
        self.assertTrue(listing.payload['privacy']['operatorOnly'])
        self.assertFalse(listing.payload['privacy']['containsApiKeyHashes'])
        self.assertNotIn('api_key_hash', json.dumps(listing.payload))

        detail = Dummy(f'/admin/customers/{other["id"]}')
        router.Handler.do_GET(detail)
        self.assertEqual(200, detail.status)
        self.assertEqual(other['id'], detail.payload['customer']['id'])
        self.assertEqual('inactive', detail.payload['activation']['status'])
        self.assertIn('new_signup', detail.payload['review']['flagCodes'])
        self.assertEqual('create_key', detail.payload['followUp']['nextAction'])
        self.assertEqual('same_email_password', detail.payload['followUp']['primaryCtaKind'])
        self.assertEqual(['passwordFallback', 'githubOAuth'], detail.payload['followUp']['recommendedCtaOrder'])
        self.assertEqual([], detail.payload['auditEvents'])

        router.suspend_customer_for_operator(customer['id'], reason_code='security')
        detail = Dummy(f'/admin/customers/{customer["id"]}')
        router.Handler.do_GET(detail)
        self.assertEqual(200, detail.status)
        self.assertEqual('customer.suspend', detail.payload['latestAuditEvent']['action'])
        self.assertEqual('security', detail.payload['latestAuditEvent']['reason_code'])
        self.assertEqual(1, len(detail.payload['auditEvents']))
        self.assertNotIn('api_key_hash', json.dumps(detail.payload['auditEvents']))

    def test_operator_activation_contact_export_is_explicit_and_bounded(self):
        router.CLIENT_API_KEYS = ['operator-token']
        router.SUPABASE_AUTH_ENABLED = True
        verified = router.customer_for_user({'id': 'auth-verified', 'email': 'verified@example.com'})
        unverified = router.customer_for_user({'id': 'auth-unverified', 'email': 'unverified@example.com'})
        suspended = router.customer_for_user({'id': 'auth-suspended', 'email': 'suspended@example.com'})
        active = router.customer_for_user({'id': 'auth-active', 'email': 'active@example.com'})
        router.update_customer(verified['id'], {'plan': 'free', 'status': 'inactive'})
        router.update_customer(unverified['id'], {'plan': 'free', 'status': 'inactive'})
        router.update_customer(suspended['id'], {'plan': 'free', 'status': 'suspended'})
        router.update_customer(active['id'], {'plan': 'pro', 'status': 'active'})
        router.create_api_key_for_customer(router.customer_by_id(active['id']), 'already-active')
        router.read_launch_auth_user_rows = lambda limit=1000: [
            {'id': 'auth-verified', 'email': 'verified@example.com', 'email_confirmed': True},
            {'id': 'auth-unverified', 'email': 'unverified@example.com', 'email_confirmed': False},
            {'id': 'auth-suspended', 'email': 'suspended@example.com', 'email_confirmed': True},
            {'id': 'auth-active', 'email': 'active@example.com', 'email_confirmed': True},
        ]

        class Dummy:
            def __init__(self, path, token='operator-token'):
                self.path = path
                self.headers = {'Authorization': f'Bearer {token}'}
                self.status = None
                self.payload = None

            def write_json(self, status, payload, extra_headers=None):
                self.status = status
                self.payload = payload

        unauthorized = Dummy('/admin/customers?contactExport=activation', token='bad-token')
        router.Handler.do_GET(unauthorized)
        self.assertEqual(401, unauthorized.status)

        default_listing = Dummy('/admin/customers?status=inactive&limit=10')
        router.Handler.do_GET(default_listing)
        self.assertEqual(200, default_listing.status)
        self.assertNotIn('contacts', default_listing.payload)

        export = Dummy('/admin/customers?status=inactive&limit=10&contactExport=activation')
        router.Handler.do_GET(export)

        self.assertEqual(200, export.status)
        self.assertEqual('activation_contact_export', export.payload['kind'])
        self.assertEqual(2, export.payload['count'])
        self.assertEqual({'unverified': 1, 'verified': 1}, export.payload['segments'])
        self.assertTrue(export.payload['privacy']['operatorOnly'])
        self.assertTrue(export.payload['privacy']['explicitContactExport'])
        self.assertTrue(export.payload['privacy']['containsEmails'])
        self.assertFalse(export.payload['privacy']['containsCustomerIds'])
        self.assertFalse(export.payload['privacy']['containsRawApiKeys'])
        self.assertFalse(export.payload['privacy']['containsApiKeyHashes'])
        self.assertFalse(export.payload['privacy']['containsProviderCredentials'])
        self.assertFalse(export.payload['privacy']['containsPrompts'])
        self.assertFalse(export.payload['privacy']['containsRawProviderResponses'])
        emails = [row['email'] for row in export.payload['contacts']]
        self.assertEqual(['unverified@example.com', 'verified@example.com'], emails)
        self.assertNotIn('suspended@example.com', emails)
        self.assertNotIn('active@example.com', emails)
        for contact in export.payload['contacts']:
            self.assertIn('start=create_key', contact['passwordFallback'])
            self.assertIn('auth=email', contact['passwordFallback'])
            self.assertIn('auth=github', contact['githubOAuth'])
            self.assertIn('generated sk_sage setup key', contact['body'])
            self.assertNotIn('auth-', json.dumps(contact))
            self.assertNotIn('customer_', json.dumps(contact))
        self.assertIn('operator_no_key_contact_export_copied', export.payload['telemetry']['copyEvents'])
        self.assertIn('verified@example.com', export.payload['csv'])
        self.assertNotIn('api_key_hash', json.dumps(export.payload))
        self.assertNotIn('sk_sage_', json.dumps(export.payload))

    def test_operator_activation_followup_sender_is_gated_and_dry_runnable(self):
        router.CLIENT_API_KEYS = ['operator-token']
        router.SUPABASE_AUTH_ENABLED = True
        verified = router.customer_for_user({'id': 'send-verified', 'email': 'verified-send@example.com'})
        unverified = router.customer_for_user({'id': 'send-unverified', 'email': 'unverified-send@example.com'})
        router.update_customer(verified['id'], {'plan': 'free', 'status': 'inactive'})
        router.update_customer(unverified['id'], {'plan': 'free', 'status': 'inactive'})
        router.read_launch_auth_user_rows = lambda limit=1000: [
            {'id': 'send-verified', 'email': 'verified-send@example.com', 'email_confirmed': True},
            {'id': 'send-unverified', 'email': 'unverified-send@example.com', 'email_confirmed': False},
        ]

        class Dummy:
            def __init__(self, body):
                self.path = '/admin/customers/send-activation-followups'
                self.headers = {
                    'Authorization': 'Bearer operator-token',
                    'Content-Length': str(len(body)),
                    'Origin': 'https://app.sagerouter.dev',
                }
                self.rfile = BytesIO(body)
                self.status = None
                self.payload = None

            def write_json(self, status, payload, extra_headers=None):
                self.status = status
                self.payload = payload

        dry_run = Dummy(b'{"status":"inactive","segment":"verified","dryRun":true,"limit":10}')
        router.Handler.do_POST(dry_run)
        self.assertEqual(200, dry_run.status)
        self.assertEqual('activation_followup_send', dry_run.payload['kind'])
        self.assertTrue(dry_run.payload['dryRun'])
        self.assertFalse(dry_run.payload['configured'])
        self.assertEqual(1, dry_run.payload['queued'])
        self.assertEqual(0, dry_run.payload['sent'])
        self.assertEqual('verified-send@example.com', dry_run.payload['results'][0]['email'])
        self.assertEqual('verified', dry_run.payload['results'][0]['segment'])
        self.assertEqual('verified', dry_run.payload['results'][0]['emailVerificationSegment'])
        self.assertEqual('dry_run', dry_run.payload['results'][0]['status'])

        missing_confirmation = Dummy(b'{"status":"inactive","segment":"verified","limit":10}')
        router.Handler.do_POST(missing_confirmation)
        self.assertEqual(400, missing_confirmation.status)
        self.assertEqual('activation_followup_send_confirmation_required', missing_confirmation.payload['error'])
        self.assertEqual('SEND_ACTIVATION_FOLLOWUPS', missing_confirmation.payload['requiredConfirmation'])
        self.assertTrue(missing_confirmation.payload['dryRunSupported'])

        not_configured = Dummy(
            b'{"status":"inactive","segment":"verified","limit":10,'
            b'"sendConfirmation":"SEND_ACTIVATION_FOLLOWUPS"}'
        )
        router.Handler.do_POST(not_configured)
        self.assertEqual(503, not_configured.status)
        self.assertEqual('activation_email_not_configured', not_configured.payload['error'])
        self.assertEqual(1, not_configured.payload['failed'])
        self.assertIn('SAGE_ROUTER_ACTIVATION_EMAIL_FROM', not_configured.payload['requiredEnv'])
        self.assertTrue(not_configured.payload['privacy']['operatorOnly'])
        self.assertTrue(not_configured.payload['privacy']['containsEmails'])
        self.assertFalse(not_configured.payload['privacy']['containsRawApiKeys'])
        self.assertNotIn('api_key_hash', json.dumps(not_configured.payload))
        self.assertNotIn('sk_sage_', json.dumps(not_configured.payload))

    def test_operator_activation_followup_sender_uses_configured_provider(self):
        router.CLIENT_API_KEYS = ['operator-token']
        router.SUPABASE_AUTH_ENABLED = True
        router.ACTIVATION_EMAIL_API_KEY = 'resend-key'
        router.ACTIVATION_EMAIL_FROM = 'Sage Router <activation@sagerouter.dev>'
        router.ACTIVATION_EMAIL_REPLY_TO = 'support@sagerouter.dev'
        customer = router.customer_for_user({'id': 'send-configured', 'email': 'buyer@example.com'})
        router.update_customer(customer['id'], {'plan': 'free', 'status': 'inactive'})
        router.read_launch_auth_user_rows = lambda limit=1000: [
            {'id': 'send-configured', 'email': 'buyer@example.com', 'email_confirmed': True},
        ]
        sent = []
        router.send_activation_email = lambda contact: sent.append(contact) or {'id': 'email_123', 'status': 200}
        body = b'{"status":"inactive","limit":10,"sendConfirmation":"SEND_ACTIVATION_FOLLOWUPS"}'

        class Dummy:
            path = '/admin/customers/send-activation-followups'
            headers = {
                'Authorization': 'Bearer operator-token',
                'Content-Length': str(len(body)),
                'Origin': 'https://app.sagerouter.dev',
            }
            rfile = BytesIO(body)
            status = None
            payload = None

            def write_json(self, status, payload, extra_headers=None):
                self.status = status
                self.payload = payload

        handler = Dummy()
        router.Handler.do_POST(handler)

        self.assertEqual(200, handler.status)
        self.assertTrue(handler.payload['configured'])
        self.assertFalse(handler.payload['dryRun'])
        self.assertEqual(1, handler.payload['sent'])
        self.assertEqual(0, handler.payload['failed'])
        self.assertEqual('sent', handler.payload['results'][0]['status'])
        self.assertEqual('email_123', handler.payload['results'][0]['providerMessageId'])
        self.assertEqual(1, len(sent))
        self.assertEqual('buyer@example.com', sent[0]['email'])
        self.assertIn('generated sk_sage setup key', sent[0]['body'])

    def test_activation_email_sender_uses_resend_idempotency_key(self):
        router.ACTIVATION_EMAIL_API_KEY = 'resend-key'
        router.ACTIVATION_EMAIL_FROM = 'Sage Router <activation@sagerouter.dev>'
        router.ACTIVATION_EMAIL_REPLY_TO = 'support@sagerouter.dev'
        captured = []

        class FakeResponse:
            status = 200

            def read(self):
                return b'{"id":"email_123"}'

            def __enter__(self):
                return self

            def __exit__(self, *_args):
                return False

        def fake_urlopen(req, timeout=12):
            captured.append(req)
            return FakeResponse()

        original_urlopen = router.urllib.request.urlopen
        try:
            router.urllib.request.urlopen = fake_urlopen
            sent = router.send_activation_email({
                'email': 'buyer@example.com',
                'subject': 'Create your Sage Router setup key',
                'body': 'Use the generated-key-first recovery link.',
            })
        finally:
            router.urllib.request.urlopen = original_urlopen

        self.assertEqual('email_123', sent['id'])
        self.assertEqual(1, len(captured))
        headers = dict(captured[0].header_items())
        self.assertEqual('sage-router-activation-followup/1.0', headers['User-agent'])
        self.assertIn('Idempotency-key', headers)
        self.assertTrue(headers['Idempotency-key'].startswith('sage-router-activation-'))
        self.assertLessEqual(len(headers['Idempotency-key']), 256)

    def test_activation_email_sender_can_use_supabase_recovery(self):
        router.ACTIVATION_EMAIL_PROVIDER = 'supabase-recovery'
        router.SUPABASE_URL = 'https://example.supabase.co'
        router.SUPABASE_ANON_KEY = 'anon-key'
        router.ACTIVATION_EMAIL_REDIRECT_TO = 'https://app.sagerouter.dev/account?activation=recovery'
        captured = []

        class FakeResponse:
            status = 200

            def read(self):
                return b'{}'

            def __enter__(self):
                return self

            def __exit__(self, *_args):
                return False

        def fake_urlopen(req, timeout=12):
            captured.append(req)
            return FakeResponse()

        original_urlopen = router.urllib.request.urlopen
        try:
            router.urllib.request.urlopen = fake_urlopen
            sent = router.send_activation_email({
                'email': 'buyer@example.com',
                'subject': 'ignored by Supabase recovery',
                'body': 'ignored by Supabase recovery',
            })
        finally:
            router.urllib.request.urlopen = original_urlopen

        self.assertEqual('supabase-recovery', sent['provider'])
        self.assertEqual(1, len(captured))
        self.assertIn('/auth/v1/recover?redirect_to=', captured[0].full_url)
        self.assertEqual({'email': 'buyer@example.com'}, json.loads(captured[0].data.decode()))
        headers = dict(captured[0].header_items())
        self.assertEqual('anon-key', headers['Apikey'])
        self.assertEqual('Bearer anon-key', headers['Authorization'])

    def test_public_activation_readiness_supports_supabase_recovery(self):
        router.ACTIVATION_EMAIL_PROVIDER = 'supabase-recovery'
        router.SUPABASE_URL = 'https://example.supabase.co'
        router.SUPABASE_ANON_KEY = 'anon-key'
        router.ACTIVATION_EMAIL_REDIRECT_TO = 'https://app.sagerouter.dev/account?activation=recovery'

        readiness = router.public_activation_email_readiness()

        self.assertEqual('supabase-recovery', readiness['provider'])
        self.assertTrue(readiness['configured'])
        self.assertTrue(readiness['sendsEmailWhenConfigured'])
        self.assertTrue(readiness['supabaseConfigured'])
        self.assertTrue(readiness['recoveryRedirectConfigured'])
        self.assertEqual([], readiness['requiredEnv'])
        self.assertFalse(readiness['privacy']['containsSecrets'])

    def test_operator_can_hydrate_auth_signups_to_inactive_customers(self):
        router.CLIENT_API_KEYS = ['operator-token']
        router.read_launch_auth_user_rows = lambda limit=1000: [
            {'id': 'auth-user-1', 'email': 'buyer@example.com', 'created_at': router.now_epoch(), 'email_confirmed': True},
            {'id': 'auth-user-2', 'email': 'pending@example.com', 'created_at': router.now_epoch(), 'email_confirmed': False},
        ]
        existing = router.customer_for_user({'id': 'auth-user-2', 'email': 'pending@example.com'})

        class Dummy:
            path = '/admin/customers/hydrate-auth-users'
            headers = {'Authorization': 'Bearer operator-token', 'Content-Length': '2'}
            rfile = BytesIO(b'{}')
            status = None
            payload = None

            def write_json(self, status, payload, extra_headers=None):
                self.status = status
                self.payload = payload

        handler = Dummy()
        router.Handler.do_POST(handler)

        self.assertEqual(200, handler.status)
        self.assertEqual('ok', handler.payload['status'])
        self.assertEqual(2, handler.payload['authUsers'])
        self.assertEqual(1, handler.payload['confirmedAuthUsers'])
        self.assertEqual(1, handler.payload['created'])
        self.assertEqual(1, handler.payload['existing'])
        self.assertEqual(0, handler.payload['failed'])
        self.assertFalse(handler.payload['privacy']['containsEmails'])
        self.assertFalse(handler.payload['privacy']['containsUserIds'])
        self.assertNotIn('buyer@example.com', json.dumps(handler.payload))
        self.assertNotIn('auth-user-1', json.dumps(handler.payload))
        created = router.customer_for_user({'id': 'auth-user-1'}, create=False)
        self.assertEqual('buyer@example.com', created['email'])
        self.assertEqual('free', created['plan'])
        self.assertEqual('inactive', created['status'])
        self.assertEqual(existing['id'], router.customer_for_user({'id': 'auth-user-2'}, create=False)['id'])

    def test_operator_customer_review_flags_are_bounded_and_actionable(self):
        customer = self.active_customer()
        _raw, _row = router.create_api_key_for_customer(customer, 'prod')

        review = router.operator_customer_review(customer)
        self.assertIn('no_first_request', review['flagCodes'])
        self.assertEqual('warn', review['severity'])
        self.assertEqual(router.MAX_ACTIVE_API_KEYS_PER_CUSTOMER, review['activeKeyLimit'])

        usage = {
            'customer_id': customer['id'],
            'period': router.current_usage_period(),
            'plan': 'pro',
            'status': 'active',
            'requests': 47000,
            'quota': 50000,
            'remaining': 3000,
            'unlimited': False,
            'rateLimitPerMinute': 180,
            'routing_enabled': True,
            'updated_at_epoch': router.now_epoch(),
        }
        quota_review = router.operator_customer_review(customer, usage=usage)
        self.assertIn('quota_high', quota_review['flagCodes'])
        self.assertEqual('warn', quota_review['severity'])
        self.assertNotIn('api_key_hash', json.dumps(quota_review))

        suspended = router.update_customer(customer['id'], {'status': 'suspended'})
        suspended_review = router.operator_customer_review(suspended, usage={**usage, 'routing_enabled': False})
        self.assertIn('suspended', suspended_review['flagCodes'])
        self.assertIn('routing_blocked', suspended_review['flagCodes'])
        self.assertEqual('bad', suspended_review['severity'])

    def test_stripe_payment_success_does_not_reactivate_suspended_customer(self):
        router.STRIPE_WEBHOOK_SECRET = 'whsec_test'
        router.STRIPE_PRICE_IDS_RAW = 'lite=price_lite,pro=price_pro,max=price_max'
        customer = self.active_customer()
        router.update_customer(customer['id'], {
            'status': 'suspended',
            'stripe_customer_id': 'cus_1',
            'stripe_subscription_id': 'sub_1',
        })

        event = {
            'id': 'evt_suspended_payment_success',
            'type': 'invoice.payment_succeeded',
            'data': {'object': {
                'customer': 'cus_1',
                'subscription': 'sub_1',
                'metadata': {'customer_id': customer['id'], 'plan': 'pro'},
                'lines': {'data': [{'price': {'id': 'price_max'}}]},
            }},
        }
        handler = self.signed_stripe_webhook_handler(event)
        router.Handler.do_POST(handler)

        updated = router.customer_by_id(customer['id'])
        self.assertEqual(200, handler.status)
        self.assertEqual('suspended', updated['status'])
        self.assertFalse(router.customer_is_active(updated))
        self.assertEqual('max', updated['plan'])

    def test_public_api_key_uses_effective_customer_plan_and_routing_state(self):
        customer = router.customer_for_user({'id': 'user-2', 'email': 'u2@example.com'})
        _raw, row = router.create_api_key_for_customer(customer, 'prepaid')
        inactive_public = router.public_api_key(row, customer)
        self.assertEqual('free', inactive_public['plan'])
        self.assertFalse(inactive_public['routing_enabled'])
        self.assertEqual('inactive', inactive_public['customer_status'])

        data = router.local_customer_store()
        data['customers'][0]['plan'] = 'max'
        data['customers'][0]['status'] = 'active'
        router.write_local_customer_store(data)
        active_customer = router.customer_for_user({'id': 'user-2'}, create=False)
        active_public = router.public_api_key(row, active_customer)
        self.assertEqual('max', active_public['plan'])
        self.assertEqual('free', active_public['key_plan'])
        self.assertTrue(active_public['routing_enabled'])

    def test_account_usage_defaults_to_current_plan_limits(self):
        customer = self.active_customer()
        usage = router.account_usage_for_customer(customer)

        self.assertEqual(customer['id'], usage['customer_id'])
        self.assertEqual('pro', usage['plan'])
        self.assertEqual(0, usage['requests'])
        self.assertEqual(50000, usage['quota'])
        self.assertEqual(50000, usage['remaining'])
        self.assertEqual(180, usage['rateLimitPerMinute'])
        self.assertFalse(usage['unlimited'])
        self.assertTrue(usage['routing_enabled'])

    def test_account_activation_reports_next_conversion_step(self):
        customer = self.active_customer()

        activation = router.account_activation_for_customer(customer)
        self.assertEqual('create_key', activation['nextAction'])
        self.assertTrue(activation['routingEnabled'])
        self.assertEqual(0, activation['activeKeyCount'])
        self.assertFalse(activation['firstRequestComplete'])

        _raw, key = router.create_api_key_for_customer(customer, 'prod')
        activation = router.account_activation_for_customer(customer, api_keys=[key])
        self.assertEqual('send_first_request', activation['nextAction'])
        self.assertEqual(1, activation['activeKeyCount'])
        self.assertEqual(0, activation['requestCount'])

        usage = router.account_usage_for_customer(customer)
        usage.update({'requests': 49950, 'quota': 50000})
        activation = router.account_activation_for_customer(customer, usage=usage, api_keys=[key])
        self.assertEqual('upgrade_before_quota', activation['nextAction'])
        self.assertTrue(activation['firstRequestComplete'])
        self.assertEqual(99.9, activation['quotaUsedPercent'])

        usage.update({'requests': 40000, 'quota': 50000})
        activation = router.account_activation_for_customer(customer, usage=usage, api_keys=[key])
        self.assertEqual('watch_quota', activation['nextAction'])
        self.assertEqual(80.0, activation['quotaUsedPercent'])

        inactive_customer = router.customer_for_user({'id': 'user-free', 'email': 'free@example.com'})
        activation = router.account_activation_for_customer(inactive_customer)
        self.assertEqual('create_key', activation['nextAction'])
        self.assertFalse(activation['routingEnabled'])

        _free_raw, free_key = router.create_api_key_for_customer(inactive_customer, 'setup')
        activation = router.account_activation_for_customer(inactive_customer, api_keys=[free_key])
        self.assertEqual('choose_plan', activation['nextAction'])
        self.assertFalse(activation['routingEnabled'])

    def test_account_usage_reads_only_current_customer_period_from_supabase(self):
        router.SUPABASE_URL = 'https://example.supabase.co'
        router.SUPABASE_SERVICE_ROLE_KEY = 'service'
        captured = {}
        customer = {
            'id': 'customer/1',
            'user_id': 'user-1',
            'plan': 'lite',
            'status': 'active',
            'created_at_epoch': router.now_epoch(),
        }

        def fake_select(table, query, timeout=8):
            captured.update({'table': table, 'query': query, 'timeout': timeout})
            return [{'requests': 321, 'updated_at_epoch': 123456}]

        router.supabase_select = fake_select
        usage = router.account_usage_for_customer(customer)

        self.assertEqual('sage_router_usage_counters', captured['table'])
        self.assertIn('customer_id=eq.customer%2F1', captured['query'])
        self.assertIn(f'period=eq.{router.current_usage_period()}', captured['query'])
        self.assertEqual(321, usage['requests'])
        self.assertEqual(10000, usage['quota'])
        self.assertEqual(9679, usage['remaining'])
        self.assertEqual(123456, usage['updated_at_epoch'])

    def test_public_launch_metadata_exposes_10k_mrr_positioning(self):
        metadata = router.public_launch_metadata()
        launch = metadata['publicLaunch']

        self.assertEqual(10000, launch['targetMrrUsd'])
        self.assertEqual('hosted_routing_control_plane', launch['primaryRevenueModel'])
        self.assertEqual('https://sagerouter.dev/pricing', launch['pricingPage'])
        self.assertEqual('https://sagerouter.dev/compare/model-gateways', launch['comparisonPage'])
        self.assertEqual('https://sagerouter.dev/models', launch['modelCatalogPage'])
        self.assertEqual('https://sagerouter.dev/model-routing-calculator', launch['calculatorPage'])
        self.assertEqual('https://app.sagerouter.dev/account.html', launch['accountPage'])
        self.assertEqual(10200, launch['recommendedMix']['monthlyRevenueUsd'])
        self.assertEqual(4, len(launch['revenuePaths']))
        self.assertTrue(any(
            path['label'] == 'Pro-only'
            and path['mix']['proCustomers'] == 334
            and path['monthlyRevenueUsd'] == 10020
            for path in launch['revenuePaths']
        ))
        self.assertTrue(any(
            path['label'] == 'Max-only'
            and path['mix']['maxCustomers'] == 139
            and path['monthlyRevenueUsd'] == 10008
            for path in launch['revenuePaths']
        ))
        self.assertTrue(any(
            path['label'] == 'Recommended mixed path'
            and path['mix']['liteCustomers'] == 100
            and path['mix']['proCustomers'] == 200
            and path['mix']['maxCustomers'] == 50
            and path['monthlyRevenueUsd'] == 10200
            for path in launch['revenuePaths']
        ))
        self.assertEqual(
            ['visitor_to_signup', 'signup_to_generated_key', 'generated_key_to_first_routed_request', 'trial_or_free_to_paid', 'paid_logo_monthly_retention'],
            [target['stage'] for target in launch['conversionFunnelTargets']],
        )
        self.assertEqual(0.60, launch['conversionFunnelTargets'][1]['targetRate'])
        self.assertIn('sagerouter.dev/pricing', router.PUBLIC_LAUNCH_POSITIONING['conversionSurfaces'])
        self.assertIn('sagerouter.dev/models', router.PUBLIC_LAUNCH_POSITIONING['conversionSurfaces'])
        self.assertIn('https://sagerouter.dev/models', launch['conversionSurfaces'])
        self.assertIn('sagerouter.dev/agent-native', router.PUBLIC_LAUNCH_POSITIONING['conversionSurfaces'])
        self.assertIn('https://sagerouter.dev/agent-native', launch['conversionSurfaces'])
        self.assertIn('sagerouter.dev/model-routing-calculator', router.PUBLIC_LAUNCH_POSITIONING['conversionSurfaces'])
        self.assertIn('https://sagerouter.dev/model-routing-calculator', launch['conversionSurfaces'])
        self.assertIn('usage quotas and request-per-minute limits', launch['sells'])
        self.assertIn('does not grant unauthorized model access', launch['complianceBoundary'])
        managed = launch['managedProviderAccess']
        self.assertFalse(managed['enabled'])
        self.assertFalse(managed['requested'])
        self.assertFalse(managed['readinessSatisfied'])
        self.assertEqual('disabled_pending_provider_terms', managed['status'])
        self.assertIn('provider_resale_terms', managed['requiredControls'])
        self.assertIn('margin_policy', managed['requiredControls'])
        self.assertIn('positive_unit_economics', managed['requiredControls'])
        self.assertIn('provider_terms_acknowledgment', managed['requiredControls'])
        self.assertIn('provider_authorization_evidence', managed['requiredControls'])
        self.assertIn('authorized_provider_allowlist', managed['requiredControls'])
        self.assertIn('provider_cost_metering', managed['requiredControls'])
        self.assertIn('per_plan_usage_caps', managed['requiredControls'])
        self.assertIn('rate_limits_and_durable_quotas', managed['requiredControls'])
        self.assertIn('generated_key_revocation', managed['requiredControls'])
        self.assertIn('operator_abuse_review', managed['requiredControls'])
        self.assertIn('operator_audit_events', managed['requiredControls'])
        self.assertIn('acceptable_use_managed_access_terms', managed['requiredControls'])
        self.assertTrue(managed['requiresPositiveUnitEconomics'])
        self.assertFalse(managed['providerTermsAcknowledged'])
        self.assertEqual([], managed['allowedProviderFamilies'])
        self.assertEqual(['ollama', 'openai', 'anthropic'], managed['resaleEligibleProviderFamilies'])
        self.assertIn('openrouter', managed['byokOnlyProviderFamilies'])
        family_rows = {row['family']: row for row in managed['providerFamilyReadiness']}
        self.assertEqual('not_allowlisted', family_rows['ollama']['status'])
        self.assertTrue(family_rows['ollama']['resaleEligible'])
        self.assertFalse(family_rows['ollama']['ready'])
        self.assertEqual('byok_supported_not_managed_resale', family_rows['openrouter']['status'])
        self.assertTrue(family_rows['openrouter']['byokOnly'])
        self.assertFalse(family_rows['openrouter']['ready'])
        self.assertEqual('one-subscription', managed['oneSubscriptionReadiness']['commercialPreference'])
        self.assertTrue(managed['oneSubscriptionReadiness']['safeForPublicDisplay'])
        self.assertEqual([], managed['oneSubscriptionReadiness']['readyProviderFamilies'])
        self.assertIn('openrouter', managed['oneSubscriptionReadiness']['blockedProviderFamilies'])
        self.assertIn('openrouter', managed['oneSubscriptionReadiness']['byokOnlyProviderFamilies'])
        self.assertIn('provider_resale_terms', managed['missingControls'])
        self.assertIn('provider_terms_acknowledgment', managed['missingControls'])
        self.assertIn('provider_authorization_evidence', managed['missingControls'])
        self.assertIn('authorized_provider_allowlist', managed['missingControls'])
        self.assertIn('margin_policy', managed['missingControls'])
        self.assertIn('provider_cost_model', managed['missingControls'])
        self.assertIn('positive_unit_economics', managed['missingControls'])
        setup = managed['readinessSetup']
        self.assertEqual('scripts/configure_managed_provider_resale_readiness.sh', setup['setupScript'])
        self.assertIn('SAGEROUTER_PROVIDER_RESALE_ALLOWED_PROVIDERS', setup['setupCommand'])
        self.assertIn('SAGEROUTER_PROVIDER_RESALE_AUTHORIZATION_REF', setup['setupCommand'])
        self.assertIn('SAGEROUTER_PROVIDER_RESALE_COST_CENTS_PER_1K_REQUESTS', setup['setupCommand'])
        self.assertIn('SAGEROUTER_MANAGED_PROVIDER_RESALE_ENABLE_PUBLIC', setup['setupCommand'])
        self.assertEqual('scripts/configure_managed_provider_resale_readiness.sh --check', setup['dryRunCommand'])
        self.assertEqual(
            "SAGEROUTER_PROVIDER_RESALE_COST_CENTS_PER_1K_REQUESTS='REVIEWED_PRIVATE_COST' "
            "scripts/configure_managed_provider_resale_readiness.sh --unit-economics",
            setup['unitEconomicsCommand'],
        )
        self.assertIn('SAGEROUTER_MANAGED_PROVIDER_RESALE_ENABLE_PUBLIC', setup['enableCommandTemplate'])
        self.assertFalse(setup['defaultPublicEnable'])
        self.assertIn('SAGEROUTER_PROVIDER_RESALE_COST_CENTS_PER_1K_REQUESTS', setup['secretManagerNames'])
        self.assertFalse(setup['privacy']['containsSecrets'])
        self.assertFalse(setup['privacy']['containsActualProviderCosts'])
        self.assertFalse(setup['privacy']['containsGrossMarginPercent'])
        self.assertFalse(managed['providerAuthorizationEvidenceConfigured'])
        self.assertEqual(
            'SAGEROUTER_PROVIDER_RESALE_AUTHORIZATION_REF',
            managed['providerAuthorizationEvidenceEnv'],
        )
        activation_email = metadata['activationEmailReadiness']
        self.assertEqual('resend', activation_email['provider'])
        self.assertFalse(activation_email['configured'])
        self.assertEqual('copy_mailto_operator_packet', activation_email['fallback'])
        self.assertIn('SAGE_ROUTER_ACTIVATION_EMAIL_FROM', activation_email['requiredEnv'])
        self.assertIn('SAGE_ROUTER_RESEND_API_KEY', activation_email['secretManagerNames'])
        self.assertEqual('scripts/configure_activation_email_sender.sh', activation_email['setupScript'])
        self.assertEqual('scripts/configure_activation_email_sender.sh --check', activation_email['setupCheckCommand'])
        self.assertTrue(activation_email['sendConfirmationRequired'])
        self.assertEqual('SEND_ACTIVATION_FOLLOWUPS', activation_email['sendConfirmation'])
        self.assertFalse(activation_email['supabaseConfigured'])
        self.assertTrue(activation_email['recoveryRedirectConfigured'])
        self.assertFalse(activation_email['privacy']['containsSecrets'])
        self.assertFalse(activation_email['privacy']['containsEmails'])
        self.assertFalse(activation_email['privacy']['containsAdminCommands'])
        self.assertNotIn('dryRunCommand', activation_email)
        self.assertNotIn('sendCommandTemplate', activation_email)
        self.assertGreaterEqual(managed['minimumGrossMarginPercent'], 30)
        self.assertFalse(managed['unitEconomics']['costModelConfigured'])
        self.assertFalse(managed['unitEconomics']['satisfied'])
        self.assertEqual(
            'SAGEROUTER_PROVIDER_RESALE_COST_CENTS_PER_1K_REQUESTS',
            managed['unitEconomics']['costModelEnv'],
        )
        plan_margins = {row['plan']: row for row in managed['unitEconomics']['evaluatedPlans']}
        self.assertEqual(60.0, plan_margins['lite']['revenueCentsPerThousandRequests'])
        self.assertEqual(39.0, plan_margins['lite']['maximumProviderCostCentsPerThousandRequests'])
        self.assertEqual(36.0, plan_margins['max']['revenueCentsPerThousandRequests'])
        self.assertEqual(23.4, plan_margins['max']['maximumProviderCostCentsPerThousandRequests'])
        for row in plan_margins.values():
            self.assertNotIn('grossMarginPercent', row)
        self.assertIn('per_plan_monthly_quotas', managed['costControls'])
        self.assertIn('request_per_minute_limits', managed['costControls'])
        self.assertIn('durable_usage_accounting', managed['costControls'])
        self.assertIn('generated_key_revocation', managed['costControls'])
        self.assertIn('operator_customer_review', managed['costControls'])
        self.assertIn('operator_audit_events', managed['costControls'])
        self.assertIn('authorized_provider_allowlist', managed['costControls'])
        self.assertEqual('https://sagerouter.dev/acceptable-use', managed['acceptableUseUrl'])

    def test_public_get_routes_ignore_cachebuster_query_strings(self):
        class Dummy:
            def __init__(self, path):
                self.path = path
                self.headers = {}
                self.status = None
                self.payload = None

            def write_json(self, status, payload, extra_headers=None):
                self.status = status
                self.payload = payload

        cases = {
            '/pricing?cb=deploy-smoke': 'publicLaunch',
            '/plans?utm_source=pages': 'plans',
            '/model-catalog?cb=deploy-smoke': 'modelCatalog',
            '/features/agent-native?preview=true': 'agentNativeFeatures',
        }
        for path, expected_key in cases.items():
            handler = Dummy(path)
            router.Handler.do_GET(handler)

            self.assertEqual(200, handler.status, path)
            self.assertIn(expected_key, handler.payload, path)

    def test_public_model_catalog_is_safe_discovery_metadata(self):
        catalog = router.public_model_catalog()

        self.assertTrue(catalog['modelApiRequiresGeneratedKey'])
        self.assertEqual('https://sagerouter.dev/models', catalog['catalogPage'])
        self.assertEqual('/v1/models', catalog['modelApiPath'])
        self.assertEqual('sage-router/frontier', catalog['recommendedModel'])
        self.assertEqual('https://api.sagerouter.dev/v1', catalog['openaiBaseUrl'])
        self.assertIn('sk_sage_', catalog['apiKeyPrefix'])
        family_ids = {row['id'] for row in catalog['families']}
        self.assertIn('sage-router-profiles', family_ids)
        self.assertIn('ollama', family_ids)
        self.assertIn('byok-compatible', family_ids)
        profile_family = next(row for row in catalog['families'] if row['id'] == 'sage-router-profiles')
        self.assertIn('sage-router/fusion', profile_family['examples'])
        byok_family = next(row for row in catalog['families'] if row['id'] == 'byok-compatible')
        self.assertIn('openrouter/free-models', byok_family['examples'])
        self.assertIn('OpenRouter', byok_family['access'])
        self.assertIn('not a promise of bundled model resale', catalog['safetyBoundary'])

    def test_managed_provider_access_requires_terms_and_margin_policy(self):
        old_env = {
            'SAGEROUTER_MANAGED_PROVIDER_RESALE_ENABLED': os.environ.get('SAGEROUTER_MANAGED_PROVIDER_RESALE_ENABLED'),
            'SAGEROUTER_PROVIDER_RESALE_TERMS_URL': os.environ.get('SAGEROUTER_PROVIDER_RESALE_TERMS_URL'),
            'SAGEROUTER_PROVIDER_RESALE_MARGIN_POLICY_URL': os.environ.get('SAGEROUTER_PROVIDER_RESALE_MARGIN_POLICY_URL'),
            'SAGEROUTER_PROVIDER_RESALE_TERMS_ACKNOWLEDGED': os.environ.get('SAGEROUTER_PROVIDER_RESALE_TERMS_ACKNOWLEDGED'),
            'SAGEROUTER_PROVIDER_RESALE_AUTHORIZATION_REF': os.environ.get('SAGEROUTER_PROVIDER_RESALE_AUTHORIZATION_REF'),
            'SAGEROUTER_PROVIDER_RESALE_ALLOWED_PROVIDERS': os.environ.get('SAGEROUTER_PROVIDER_RESALE_ALLOWED_PROVIDERS'),
            'SAGEROUTER_PROVIDER_RESALE_MIN_GROSS_MARGIN_PERCENT': os.environ.get('SAGEROUTER_PROVIDER_RESALE_MIN_GROSS_MARGIN_PERCENT'),
            'SAGEROUTER_PROVIDER_RESALE_COST_CENTS_PER_1K_REQUESTS': os.environ.get('SAGEROUTER_PROVIDER_RESALE_COST_CENTS_PER_1K_REQUESTS'),
        }
        try:
            os.environ['SAGEROUTER_MANAGED_PROVIDER_RESALE_ENABLED'] = '1'
            os.environ.pop('SAGEROUTER_PROVIDER_RESALE_TERMS_URL', None)
            os.environ.pop('SAGEROUTER_PROVIDER_RESALE_MARGIN_POLICY_URL', None)
            os.environ.pop('SAGEROUTER_PROVIDER_RESALE_TERMS_ACKNOWLEDGED', None)
            os.environ.pop('SAGEROUTER_PROVIDER_RESALE_AUTHORIZATION_REF', None)
            os.environ.pop('SAGEROUTER_PROVIDER_RESALE_ALLOWED_PROVIDERS', None)
            os.environ.pop('SAGEROUTER_PROVIDER_RESALE_MIN_GROSS_MARGIN_PERCENT', None)
            os.environ.pop('SAGEROUTER_PROVIDER_RESALE_COST_CENTS_PER_1K_REQUESTS', None)
            managed = router.public_launch_metadata()['publicLaunch']['managedProviderAccess']
            self.assertFalse(managed['enabled'])
            self.assertTrue(managed['requested'])
            self.assertFalse(managed['readinessSatisfied'])
            self.assertEqual('requires_readiness_verification', managed['status'])
            self.assertIn('provider_resale_terms', managed['missingControls'])
            self.assertIn('provider_terms_acknowledgment', managed['missingControls'])
            self.assertIn('provider_authorization_evidence', managed['missingControls'])
            self.assertIn('authorized_provider_allowlist', managed['missingControls'])
            self.assertIn('margin_policy', managed['missingControls'])
            self.assertIn('provider_cost_model', managed['missingControls'])
            self.assertIn('positive_unit_economics', managed['missingControls'])

            os.environ['SAGEROUTER_PROVIDER_RESALE_TERMS_URL'] = 'https://sagerouter.dev/provider-resale-terms'
            os.environ['SAGEROUTER_PROVIDER_RESALE_MARGIN_POLICY_URL'] = 'https://sagerouter.dev/margin-policy'
            os.environ['SAGEROUTER_PROVIDER_RESALE_MIN_GROSS_MARGIN_PERCENT'] = '10'
            os.environ['SAGEROUTER_PROVIDER_RESALE_COST_CENTS_PER_1K_REQUESTS'] = '30'
            managed = router.public_launch_metadata()['publicLaunch']['managedProviderAccess']
            self.assertFalse(managed['enabled'])
            self.assertTrue(managed['requested'])
            self.assertFalse(managed['readinessSatisfied'])
            self.assertEqual('requires_readiness_verification', managed['status'])
            self.assertEqual(10, managed['minimumGrossMarginPercent'])
            self.assertIn('minimum_gross_margin', managed['missingControls'])
            self.assertTrue(managed['unitEconomics']['costModelConfigured'])
            self.assertTrue(managed['unitEconomics']['satisfied'])

            os.environ['SAGEROUTER_PROVIDER_RESALE_MIN_GROSS_MARGIN_PERCENT'] = '35'
            managed = router.public_launch_metadata()['publicLaunch']['managedProviderAccess']
            self.assertFalse(managed['enabled'])
            self.assertTrue(managed['requested'])
            self.assertFalse(managed['readinessSatisfied'])
            self.assertEqual('requires_readiness_verification', managed['status'])
            self.assertFalse(managed['providerTermsAcknowledged'])
            self.assertFalse(managed['providerAuthorizationEvidenceConfigured'])
            self.assertEqual([], managed['allowedProviderFamilies'])
            self.assertNotIn('minimum_gross_margin', managed['missingControls'])
            self.assertIn('positive_unit_economics', managed['missingControls'])
            self.assertFalse(managed['unitEconomics']['satisfied'])

            os.environ['SAGEROUTER_PROVIDER_RESALE_TERMS_ACKNOWLEDGED'] = '1'
            os.environ['SAGEROUTER_PROVIDER_RESALE_AUTHORIZATION_REF'] = 'provider-auth-review-2026-06'
            os.environ['SAGEROUTER_PROVIDER_RESALE_ALLOWED_PROVIDERS'] = 'openrouter'
            os.environ['SAGEROUTER_PROVIDER_RESALE_COST_CENTS_PER_1K_REQUESTS'] = '1'
            managed = router.public_launch_metadata()['publicLaunch']['managedProviderAccess']
            self.assertFalse(managed['enabled'])
            self.assertTrue(managed['requested'])
            self.assertFalse(managed['readinessSatisfied'])
            self.assertEqual(['openrouter'], managed['configuredProviderFamilies'])
            self.assertEqual([], managed['allowedProviderFamilies'])
            self.assertIn('openrouter', managed['byokOnlyProviderFamilies'])
            self.assertEqual(['openrouter'], managed['byokOnlyConfiguredProviderFamilies'])
            family_rows = {row['family']: row for row in managed['providerFamilyReadiness']}
            self.assertTrue(family_rows['openrouter']['configured'])
            self.assertEqual('byok_supported_not_managed_resale', family_rows['openrouter']['status'])
            self.assertFalse(family_rows['openrouter']['ready'])
            self.assertIn('openrouter', managed['oneSubscriptionReadiness']['blockedProviderFamilies'])
            self.assertIn('authorized_provider_allowlist', managed['missingControls'])

            os.environ['SAGEROUTER_PROVIDER_RESALE_ALLOWED_PROVIDERS'] = 'ollama,openai,anthropic'
            os.environ['SAGEROUTER_PROVIDER_RESALE_COST_CENTS_PER_1K_REQUESTS'] = '30'
            managed = router.public_launch_metadata()['publicLaunch']['managedProviderAccess']
            self.assertFalse(managed['enabled'])
            self.assertTrue(managed['requested'])
            self.assertFalse(managed['readinessSatisfied'])
            self.assertEqual('requires_readiness_verification', managed['status'])
            self.assertIn('positive_unit_economics', managed['missingControls'])

            os.environ['SAGEROUTER_PROVIDER_RESALE_COST_CENTS_PER_1K_REQUESTS'] = '0'
            managed = router.public_launch_metadata()['publicLaunch']['managedProviderAccess']
            self.assertFalse(managed['enabled'])
            self.assertTrue(managed['requested'])
            self.assertFalse(managed['readinessSatisfied'])
            self.assertIn('provider_cost_model', managed['missingControls'])
            self.assertIn('positive_unit_economics', managed['missingControls'])
            self.assertFalse(managed['unitEconomics']['costModelConfigured'])
            self.assertFalse(managed['unitEconomics']['satisfied'])

            os.environ['SAGEROUTER_PROVIDER_RESALE_COST_CENTS_PER_1K_REQUESTS'] = '1'
            managed = router.public_launch_metadata()['publicLaunch']['managedProviderAccess']
            self.assertTrue(managed['enabled'])
            self.assertTrue(managed['requested'])
            self.assertTrue(managed['readinessSatisfied'])
            self.assertEqual('ready_for_private_beta', managed['status'])
            self.assertEqual('https://sagerouter.dev/provider-resale-terms', managed['providerTermsUrl'])
            self.assertTrue(managed['providerTermsAcknowledged'])
            self.assertTrue(managed['providerAuthorizationEvidenceConfigured'])
            self.assertEqual(['ollama', 'openai', 'anthropic'], managed['allowedProviderFamilies'])
            self.assertEqual('https://sagerouter.dev/margin-policy', managed['marginPolicyUrl'])
            self.assertEqual(35, managed['minimumGrossMarginPercent'])
            self.assertTrue(managed['requiresPositiveUnitEconomics'])
            self.assertTrue(managed['unitEconomics']['costModelConfigured'])
            self.assertTrue(managed['unitEconomics']['satisfied'])
            for row in managed['unitEconomics']['evaluatedPlans']:
                self.assertNotIn('grossMarginPercent', row)
            family_rows = {row['family']: row for row in managed['providerFamilyReadiness']}
            self.assertTrue(family_rows['ollama']['ready'])
            self.assertTrue(family_rows['openai']['ready'])
            self.assertTrue(family_rows['anthropic']['ready'])
            self.assertFalse(family_rows['openrouter']['ready'])
            self.assertEqual('byok_supported_not_managed_resale', family_rows['openrouter']['status'])
            self.assertEqual(
                ['ollama', 'openai', 'anthropic'],
                managed['oneSubscriptionReadiness']['readyProviderFamilies'],
            )
            self.assertIn('openrouter', managed['oneSubscriptionReadiness']['blockedProviderFamilies'])
            self.assertEqual([], managed['missingControls'])
            self.assertEqual('', managed['readinessSetup']['setupCommand'])
            self.assertIn('ready for private beta', managed['readinessSetup']['operatorAction'])
        finally:
            for key, value in old_env.items():
                if value is None:
                    os.environ.pop(key, None)
                else:
                    os.environ[key] = value

    def test_account_usage_endpoint_requires_signed_in_customer(self):
        router.supabase_user_for_bearer = lambda token: {'id': 'user-1', 'email': 'u@example.com'} if token == 'valid-user-jwt' else None
        customer = router.customer_for_user({'id': 'user-1', 'email': 'u@example.com'})
        router.update_customer(customer['id'], {'plan': 'max', 'status': 'active'})

        class Dummy:
            path = '/account/usage'
            headers = {'Authorization': 'Bearer valid-user-jwt'}
            status = None
            payload = None

            def write_json(self, status, payload, extra_headers=None):
                self.status = status
                self.payload = payload

        handler = Dummy()
        router.Handler.do_GET(handler)

        self.assertEqual(200, handler.status)
        self.assertEqual('max', handler.payload['usage']['plan'])
        self.assertEqual(200000, handler.payload['usage']['quota'])
        self.assertEqual('max', handler.payload['activation']['plan'])
        self.assertTrue(handler.payload['activation']['routingEnabled'])
        self.assertEqual('create_key', handler.payload['activation']['nextAction'])
        self.assertEqual(0, handler.payload['activation']['requestCount'])


    def test_route_events_are_scoped_to_generated_customer_keys(self):
        customer = self.active_customer()
        raw, _row = router.create_api_key_for_customer(customer, 'prod')
        ctx = router.verify_generated_api_key(raw)
        router.set_route_auth_context(ctx)
        try:
            router.append_route_event({
                'request_id': 'r1',
                'status': 'ok',
                'intent': 'GENERAL',
                'selected': {'provider': 'test', 'model': 'fast'},
                'attempts': [{'provider': 'test', 'model': 'fast', 'ok': True, 'elapsedMs': 10}],
                'totalElapsedMs': 10,
            })
        finally:
            router.clear_route_auth_context()
        router.append_route_event({
            'request_id': 'r2',
            'status': 'ok',
            'intent': 'GENERAL',
            'selected': {'provider': 'other', 'model': 'slow'},
            'attempts': [],
            'totalElapsedMs': 20,
            'customer_id': 'other-customer',
        })
        snapshot = router.build_analytics_snapshot(7 * 24 * 3600, customer_id=customer['id'])
        self.assertEqual(1, snapshot['eventsAnalyzed'])
        self.assertEqual(customer['id'], snapshot['scope']['customer_id'])
        self.assertIn('test', [p['id'] for p in snapshot['providers']])

    def test_route_events_keep_edge_verified_customer_identity_behind_backend_token(self):
        router.CLIENT_API_KEYS = ['backend-token']
        customer = self.active_customer()

        class Dummy:
            headers = {
                'Authorization': 'Bearer backend-token',
                'X-Sage-Router-Edge-Auth-Type': 'generated_key',
                'X-Sage-Router-Customer-Id': customer['id'],
                'X-Sage-Router-Customer-Plan': customer['plan'],
                'X-Sage-Router-Customer-Status': customer['status'],
                'X-Sage-Router-User-Id': customer['user_id'],
            }

        ctx = router.client_auth_context(Dummy())
        self.assertEqual('generated_key', ctx['type'])
        self.assertTrue(ctx['edge_authenticated'])
        self.assertEqual(customer['id'], ctx['customer']['id'])
        self.assertEqual('pro', ctx['customer']['plan'])

        router.set_route_auth_context(ctx)
        try:
            router.append_route_event({
                'request_id': 'r-edge',
                'status': 'ok',
                'intent': 'GENERAL',
                'selected': {'provider': 'edge', 'model': 'frontier'},
                'attempts': [{'provider': 'edge', 'model': 'frontier', 'ok': True, 'elapsedMs': 10}],
                'totalElapsedMs': 10,
            })
        finally:
            router.clear_route_auth_context()

        snapshot = router.build_analytics_snapshot(7 * 24 * 3600, customer_id=customer['id'])
        self.assertEqual(1, snapshot['eventsAnalyzed'])
        self.assertEqual(customer['id'], snapshot['scope']['customer_id'])
        self.assertEqual('generated_key', router.read_recent_route_events()[0]['auth_type'])
        self.assertEqual('pro', router.read_recent_route_events()[0]['customer_plan'])

    def test_edge_customer_headers_are_ignored_without_backend_token_auth(self):
        customer = self.active_customer()

        class Dummy:
            headers = {
                'Authorization': 'Bearer not-backend-token',
                'X-Sage-Router-Edge-Auth-Type': 'generated_key',
                'X-Sage-Router-Customer-Id': customer['id'],
                'X-Sage-Router-Customer-Plan': customer['plan'],
            }

        self.assertIsNone(router.client_auth_context(Dummy()))

    def test_global_analytics_rejects_customer_generated_key_when_hosted_auth_enabled(self):
        router.SUPABASE_AUTH_ENABLED = True
        customer = self.active_customer()
        raw, _row = router.create_api_key_for_customer(customer, 'prod')

        class Dummy:
            path = '/analytics?days=7'
            headers = {'Authorization': f'Bearer {raw}'}
            status = None
            payload = None

            def write_json(self, status, payload, extra_headers=None):
                self.status = status
                self.payload = payload

        handler = Dummy()
        router.Handler.do_GET(handler)

        self.assertEqual(401, handler.status)
        self.assertEqual('unauthorized', handler.payload['error'])

    def test_account_analytics_accepts_customer_generated_key_and_scopes_events(self):
        customer = self.active_customer()
        raw, _row = router.create_api_key_for_customer(customer, 'prod')
        ctx = router.verify_generated_api_key(raw)
        router.set_route_auth_context(ctx)
        try:
            router.append_route_event({
                'request_id': 'r-account',
                'status': 'ok',
                'intent': 'GENERAL',
                'selected': {'provider': 'local', 'model': 'frontier'},
                'attempts': [{'provider': 'local', 'model': 'frontier', 'ok': True, 'elapsedMs': 12}],
                'totalElapsedMs': 12,
            })
        finally:
            router.clear_route_auth_context()
        router.append_route_event({
            'request_id': 'r-other',
            'status': 'ok',
            'intent': 'GENERAL',
            'selected': {'provider': 'other', 'model': 'model'},
            'attempts': [{'provider': 'other', 'model': 'model', 'ok': True, 'elapsedMs': 99}],
            'totalElapsedMs': 99,
            'customer_id': 'other-customer',
        })

        class Dummy:
            path = '/account/analytics?days=7'
            headers = {'Authorization': f'Bearer {raw}'}
            status = None
            payload = None

            def write_json(self, status, payload, extra_headers=None):
                self.status = status
                self.payload = payload

        handler = Dummy()
        router.Handler.do_GET(handler)

        self.assertEqual(200, handler.status)
        self.assertEqual(customer['id'], handler.payload['scope']['customer_id'])
        self.assertEqual(customer['id'], handler.payload['account']['customer_id'])
        self.assertEqual(1, handler.payload['eventsAnalyzed'])
        provider_requests = {p['id']: p.get('requests') for p in handler.payload['providers']}
        self.assertEqual(1, provider_requests.get('local'))
        self.assertNotIn('other', provider_requests)

    def test_launch_funnel_snapshot_seeds_acquisition_actions_without_traffic(self):
        router.read_launch_waitlist_counts = lambda _since, limit=10000: ({
            'total': 0,
            'interest': {
                'general': 0,
                'managedAccess': 0,
                'other': 0,
                'unknown': 0,
            },
            'managedAccessDemand': {
                'targetProviderFamily': {
                    'mixed-frontier': 0,
                    'ollama': 0,
                    'openai': 0,
                    'anthropic': 0,
                    'byok-compatible': 0,
                    'unknown': 0,
                },
                'commercialPreference': {
                    'one-subscription': 0,
                    'byok-plus-routing': 0,
                    'private-contract': 0,
                    'unknown': 0,
                },
                'intent': {
                    'max-implementation': 0,
                    'private-deployment': 0,
                    'gateway-migration': 0,
                    'one-subscription': 0,
                    'ollama': 0,
                    'openai': 0,
                    'anthropic': 0,
                    'unknown': 0,
                },
            },
        }, None)
        router.read_launch_marketing_funnel_counts = lambda _since, limit=10000: ({
            'total': 0,
            'events': {},
            'plans': {},
            'sourceSurfaces': {
                'pricing': 0,
                'model-routing-calculator': 0,
                'model-catalog': 0,
                'compare-gateways': 0,
                'launch-plan': 0,
                'landing': 0,
                'unknown': 0,
            },
            'attributionChannels': {
                'direct': 0,
                'github': 0,
                'model-gateway': 0,
                'unknown': 0,
            },
            'authProviderState': router.new_auth_provider_state_metrics(),
            'modelCatalogDemand': router.new_model_catalog_demand_metrics(),
        }, None)

        snapshot = router.build_launch_funnel_snapshot(30 * 24 * 3600)

        self.assertEqual(0, snapshot['stages']['marketingIntentEvents'])
        self.assertEqual(snapshot['acquisitionActions'], snapshot['marketingIntent']['acquisitionActions'])
        buckets = [row['bucket'] for row in snapshot['acquisitionActions']]
        self.assertIn('model-gateway', buckets)
        self.assertIn('github', buckets)
        self.assertIn('pricing', buckets)
        self.assertIn('model-routing-calculator', buckets)
        self.assertIn('model-catalog', buckets)
        self.assertIn('launch-plan', buckets)
        self.assertTrue(all(row['clicks'] == 0 for row in snapshot['acquisitionActions']))
        self.assertTrue(all(row['priority'] == 'seed_launch_channel' for row in snapshot['acquisitionActions']))
        self.assertIn('$10k MRR outreach', json.dumps(snapshot['acquisitionActions']))
        self.assertNotIn('buyer@example.com', json.dumps(snapshot['acquisitionActions']))

    def test_launch_funnel_snapshot_counts_private_conversion_stages(self):
        router.read_launch_waitlist_counts = lambda _since, limit=10000: ({
            'total': 3,
            'interest': {
                'general': 1,
                'managedAccess': 2,
                'other': 0,
                'unknown': 0,
            },
            'managedAccessDemand': {
                'targetProviderFamily': {
                    'mixed-frontier': 1,
                    'ollama': 0,
                    'openai': 1,
                    'anthropic': 0,
                    'byok-compatible': 0,
                    'unknown': 0,
                },
                'commercialPreference': {
                    'one-subscription': 2,
                    'byok-plus-routing': 0,
                    'private-contract': 0,
                    'unknown': 0,
                },
                'intent': {
                    'max-implementation': 1,
                    'private-deployment': 0,
                    'gateway-migration': 1,
                    'one-subscription': 0,
                    'ollama': 0,
                    'openai': 0,
                    'anthropic': 0,
                    'unknown': 0,
                },
            },
        }, None)
        router.read_launch_marketing_funnel_counts = lambda _since, limit=10000: ({
            'total': 29,
            'events': {
                'landing_account_clicked': 1,
                'landing_key_first_direct_clicked': 1,
                'model_catalog_viewed': 1,
                'model_catalog_search_bucketed': 2,
                'model_catalog_filter_clicked': 1,
                'model_catalog_key_activation_clicked': 1,
                'pricing_key_activation_clicked': 1,
                'content_article_key_activation_clicked': 1,
                'fusion_key_activation_clicked': 1,
                'codex_docs_key_activation_clicked': 1,
                'gateway_compare_key_activation_clicked': 1,
                'launch_plan_key_activation_clicked': 1,
                'account_api_key_created': 1,
                'account_key_recovery_viewed': 1,
                'account_auto_oauth_skipped': 1,
                'account_checkout_key_first_redirected': 1,
                'account_intent_create_key_clicked': 1,
                'account_snippet_copied': 1,
                'quickstart_snippet_copied': 1,
                'account_usage_upgrade_clicked': 1,
                'calculator_checkout_clicked': 2,
                'calculator_checkout_unavailable': 1,
                'account_checkout_failed': 1,
                'account_checkout_unavailable': 1,
                'account_billing_portal_failed': 1,
                'account_crypto_intent_failed': 1,
                'launch_plan_checkout_clicked': 1,
                'pricing_checkout_clicked': 1,
                'managed_access_interest_clicked': 1,
                'gateway_compare_checkout_clicked': 1,
                'auth_provider_state_checked': 2,
            },
            'plans': {
                'pro': 4,
                'max': 1,
            },
            'sourceSurfaces': {
                'landing': 1,
                'launch-plan': 1,
                'pricing': 2,
                'model-catalog': 4,
                'compare-gateways': 2,
                'account': 1,
                'login': 1,
            },
            'attributionChannels': {
                'github': 2,
                'model-gateway': 1,
                'direct': 2,
            },
            'authProviderState': {
                'total': 2,
                'loaded': 1,
                'unavailable': 1,
                'unknown': 0,
                'githubEnabled': 1,
                'githubDisabled': 1,
                'enabledProviders': {
                    'github': 1,
                    'google': 0,
                    'discord': 0,
                    'none': 1,
                    'other': 0,
                },
                'disabledProviders': {
                    'github': 1,
                    'google': 2,
                    'discord': 2,
                    'none': 0,
                    'other': 0,
                },
            },
            'modelCatalogDemand': {
                'modelFamily': {
                    'ollama': 2,
                    'openai-codex': 1,
                    'other': 1,
                },
                'queryBucket': {
                    'ollama': 2,
                    'empty': 1,
                    'other': 1,
                },
            },
            'setupSnippetCopies': 2,
            'setupSnippetCopiesBySnippet': {
                'codex-cli': 1,
                'quickstart-curl': 1,
            },
            'keyFirstRedirects': 10,
            'keyFirstRedirectsByState': {
                'checkout_key_first': 1,
                'codex-docs-main': 1,
                'compare-gateways-hero': 1,
                'content-article-dock': 1,
                'fusion-hero': 1,
                'hero-key-first': 1,
                'launch-plan-hero': 1,
                'model-catalog-hero': 1,
                'pricing-pro': 1,
                'saved_key_recovery_auto_key': 1,
            },
            'keyRecoveryViews': 1,
            'keyRecoveryViewsByState': {
                'github': 1,
            },
            'keyCreateAttempts': 1,
            'keyCreateAttemptsByState': {
                'saved_key_recovery_auto_key': 1,
            },
            'keyCreateSuccesses': 1,
            'keyCreateSuccessesByState': {
                'created': 1,
            },
            'keyCreateFailures': 0,
            'keyCreateFailuresByState': {},
            'operatorFollowUpCopies': 2,
            'operatorFollowUpCopiesByKind': {
                'single_copied': 1,
                'batch_copied': 1,
            },
            'operatorFollowUpWorked': 1,
            'operatorFollowUpWorkedByKind': {
                'verified_marked_worked': 1,
            },
            'operatorFollowUpSendDryRuns': 1,
            'operatorFollowUpSendDryRunsByKind': {
                'verified_send_dry_run': 1,
            },
            'operatorFollowUpSendDryRunRecipients': 2,
            'operatorFollowUpSends': 1,
            'operatorFollowUpSendsByKind': {
                'verified_sent': 1,
            },
            'operatorFollowUpSentRecipients': 2,
            'operatorFollowUpSendFailures': 0,
            'operatorFollowUpSendFailuresByKind': {},
            'operatorFollowUpSendFailureRecipients': 0,
        }, None)
        customer = self.active_customer()
        raw, _row = router.create_api_key_for_customer(customer, 'prod')
        ctx = router.verify_generated_api_key(raw)
        router.set_route_auth_context(ctx)
        try:
            router.append_route_event({
                'request_id': 'r-funnel',
                'status': 'ok',
                'intent': 'GENERAL',
                'selected': {'provider': 'local', 'model': 'frontier'},
                'attempts': [{'provider': 'local', 'model': 'frontier', 'ok': True, 'elapsedMs': 12}],
                'totalElapsedMs': 12,
            })
        finally:
            router.clear_route_auth_context()
        router.customer_for_user({'id': 'user-2', 'email': 'second@example.com'})

        snapshot = router.build_launch_funnel_snapshot(30 * 24 * 3600)

        self.assertEqual(3, snapshot['stages']['waitlistLeads'])
        self.assertEqual(29, snapshot['stages']['marketingIntentEvents'])
        self.assertEqual(1, snapshot['marketingIntent']['events']['landing_account_clicked'])
        self.assertEqual(1, snapshot['marketingIntent']['events']['landing_key_first_direct_clicked'])
        self.assertEqual(1, snapshot['marketingIntent']['events']['model_catalog_viewed'])
        self.assertEqual(2, snapshot['marketingIntent']['events']['model_catalog_search_bucketed'])
        self.assertEqual(1, snapshot['marketingIntent']['events']['model_catalog_filter_clicked'])
        self.assertEqual(1, snapshot['marketingIntent']['events']['model_catalog_key_activation_clicked'])
        self.assertEqual(1, snapshot['marketingIntent']['events']['pricing_key_activation_clicked'])
        self.assertEqual(1, snapshot['marketingIntent']['events']['content_article_key_activation_clicked'])
        self.assertEqual(1, snapshot['marketingIntent']['events']['fusion_key_activation_clicked'])
        self.assertEqual(1, snapshot['marketingIntent']['events']['codex_docs_key_activation_clicked'])
        self.assertEqual(1, snapshot['marketingIntent']['events']['gateway_compare_key_activation_clicked'])
        self.assertEqual(1, snapshot['marketingIntent']['events']['launch_plan_key_activation_clicked'])
        self.assertEqual(1, snapshot['marketingIntent']['events']['account_api_key_created'])
        self.assertEqual(1, snapshot['marketingIntent']['events']['account_key_recovery_viewed'])
        self.assertEqual(1, snapshot['marketingIntent']['events']['account_checkout_key_first_redirected'])
        self.assertEqual(1, snapshot['marketingIntent']['events']['account_intent_create_key_clicked'])
        self.assertEqual(10, snapshot['marketingIntent']['keyFirstRedirects'])
        self.assertEqual(1, snapshot['marketingIntent']['keyFirstRedirectsByState']['checkout_key_first'])
        self.assertEqual(1, snapshot['marketingIntent']['keyFirstRedirectsByState']['codex-docs-main'])
        self.assertEqual(1, snapshot['marketingIntent']['keyFirstRedirectsByState']['compare-gateways-hero'])
        self.assertEqual(1, snapshot['marketingIntent']['keyFirstRedirectsByState']['content-article-dock'])
        self.assertEqual(1, snapshot['marketingIntent']['keyFirstRedirectsByState']['fusion-hero'])
        self.assertEqual(1, snapshot['marketingIntent']['keyFirstRedirectsByState']['hero-key-first'])
        self.assertEqual(1, snapshot['marketingIntent']['keyFirstRedirectsByState']['launch-plan-hero'])
        self.assertEqual(1, snapshot['marketingIntent']['keyFirstRedirectsByState']['model-catalog-hero'])
        self.assertEqual(1, snapshot['marketingIntent']['keyFirstRedirectsByState']['pricing-pro'])
        self.assertEqual(1, snapshot['marketingIntent']['keyFirstRedirectsByState']['saved_key_recovery_auto_key'])
        self.assertEqual(1, snapshot['marketingIntent']['keyRecoveryViews'])
        self.assertEqual(1, snapshot['marketingIntent']['keyRecoveryViewsByState']['github'])
        self.assertEqual(1, snapshot['marketingIntent']['keyCreateAttempts'])
        self.assertEqual(1, snapshot['marketingIntent']['keyCreateAttemptsByState']['saved_key_recovery_auto_key'])
        self.assertEqual(1, snapshot['marketingIntent']['keyCreateSuccesses'])
        self.assertEqual(1, snapshot['marketingIntent']['keyCreateSuccessesByState']['created'])
        self.assertEqual(0, snapshot['marketingIntent']['keyCreateFailures'])
        self.assertEqual(1, snapshot['marketingIntent']['events']['account_snippet_copied'])
        self.assertEqual(1, snapshot['marketingIntent']['events']['quickstart_snippet_copied'])
        self.assertEqual(2, snapshot['marketingIntent']['setupSnippetCopies'])
        self.assertEqual(1, snapshot['marketingIntent']['setupSnippetCopiesBySnippet']['codex-cli'])
        self.assertEqual(1, snapshot['marketingIntent']['setupSnippetCopiesBySnippet']['quickstart-curl'])
        self.assertEqual(2, snapshot['marketingIntent']['events']['calculator_checkout_clicked'])
        self.assertEqual(1, snapshot['marketingIntent']['events']['calculator_checkout_unavailable'])
        self.assertEqual(1, snapshot['marketingIntent']['events']['account_checkout_failed'])
        self.assertEqual(1, snapshot['marketingIntent']['events']['account_checkout_unavailable'])
        self.assertEqual(1, snapshot['marketingIntent']['events']['account_billing_portal_failed'])
        self.assertEqual(1, snapshot['marketingIntent']['events']['account_crypto_intent_failed'])
        self.assertEqual(11, snapshot['marketingIntent']['checkoutFriction']['totalCheckoutIntent'])
        self.assertEqual(5, snapshot['marketingIntent']['checkoutFriction']['unavailableEvents'])
        self.assertEqual(0.4545, snapshot['marketingIntent']['checkoutFriction']['unavailableRate'])
        self.assertEqual(1, snapshot['marketingIntent']['checkoutFriction']['unavailableByEvent']['calculator_checkout_unavailable'])
        self.assertEqual(1, snapshot['marketingIntent']['checkoutFriction']['unavailableByEvent']['account_checkout_unavailable'])
        self.assertEqual(1, snapshot['marketingIntent']['checkoutFriction']['unavailableByEvent']['account_checkout_failed'])
        self.assertEqual(1, snapshot['marketingIntent']['checkoutFriction']['unavailableByEvent']['account_billing_portal_failed'])
        self.assertEqual(1, snapshot['marketingIntent']['checkoutFriction']['unavailableByEvent']['account_crypto_intent_failed'])
        self.assertEqual(1, snapshot['marketingIntent']['events']['launch_plan_checkout_clicked'])
        self.assertEqual(1, snapshot['marketingIntent']['events']['gateway_compare_checkout_clicked'])
        self.assertEqual(2, snapshot['marketingIntent']['events']['auth_provider_state_checked'])
        self.assertEqual(2, snapshot['marketingIntent']['authProviderState']['total'])
        self.assertEqual(1, snapshot['marketingIntent']['authProviderState']['githubEnabled'])
        self.assertEqual(1, snapshot['marketingIntent']['authProviderState']['githubDisabled'])
        self.assertEqual(2, snapshot['authProviderState']['total'])
        self.assertEqual(1, snapshot['authProviderState']['githubEnabled'])
        self.assertEqual(1, snapshot['authProviderState']['githubDisabled'])
        self.assertEqual('marketing_funnel', snapshot['authProviderState']['source'])
        self.assertTrue(snapshot['authProviderState']['githubAvailable'])
        self.assertEqual('email_first', snapshot['authProviderState']['recommendedRecoveryAuth'])
        self.assertIn('Use email/password recovery first', snapshot['authProviderState']['operatorGuidance'])
        self.assertEqual(4, snapshot['marketingIntent']['plans']['pro'])
        self.assertEqual(1, snapshot['marketingIntent']['sourceSurfaces']['landing'])
        self.assertEqual(1, snapshot['marketingIntent']['sourceSurfaces']['launch-plan'])
        self.assertEqual(2, snapshot['marketingIntent']['sourceSurfaces']['pricing'])
        self.assertEqual(4, snapshot['marketingIntent']['sourceSurfaces']['model-catalog'])
        self.assertEqual(2, snapshot['marketingIntent']['sourceSurfaces']['compare-gateways'])
        self.assertEqual(2, snapshot['marketingIntent']['modelCatalogDemand']['modelFamily']['ollama'])
        self.assertEqual(1, snapshot['marketingIntent']['modelCatalogDemand']['modelFamily']['openai-codex'])
        self.assertEqual(2, snapshot['marketingIntent']['modelCatalogDemand']['queryBucket']['ollama'])
        self.assertEqual(1, snapshot['marketingIntent']['modelCatalogDemand']['queryBucket']['empty'])
        self.assertEqual(2, snapshot['marketingIntent']['attributionChannels']['github'])
        self.assertEqual(1, snapshot['marketingIntent']['attributionChannels']['model-gateway'])
        self.assertEqual(snapshot['acquisitionActions'], snapshot['marketingIntent']['acquisitionActions'])
        acquisition_buckets = [row['bucket'] for row in snapshot['acquisitionActions']]
        self.assertIn('github', acquisition_buckets)
        self.assertIn('launch-plan', acquisition_buckets)
        self.assertIn('pricing', acquisition_buckets)
        self.assertIn('model-catalog', acquisition_buckets)
        self.assertIn('compare-gateways', acquisition_buckets)
        self.assertIn('Publish gateway migration proof', json.dumps(snapshot['acquisitionActions']))
        self.assertIn('Turn launch-plan readers into Pro checkout', json.dumps(snapshot['acquisitionActions']))
        self.assertIn('Turn catalog demand into hosted key activation', json.dumps(snapshot['acquisitionActions']))
        self.assertNotIn('buyer@example.com', json.dumps(snapshot['acquisitionActions']))
        self.assertEqual(2, snapshot['stages']['managedAccessBetaInterest'])
        self.assertEqual(2, snapshot['waitlistInterest']['managedAccess'])
        self.assertEqual(1, snapshot['managedAccessDemand']['targetProviderFamily']['mixed-frontier'])
        self.assertEqual(1, snapshot['managedAccessDemand']['targetProviderFamily']['openai'])
        self.assertEqual(2, snapshot['managedAccessDemand']['commercialPreference']['one-subscription'])
        self.assertEqual(1, snapshot['managedAccessDemand']['intent']['max-implementation'])
        self.assertEqual(1, snapshot['managedAccessDemand']['intent']['gateway-migration'])
        self.assertEqual(0.6667, snapshot['rates']['managedAccessShareOfWaitlist'])
        self.assertEqual(2, snapshot['stages']['signups'])
        self.assertEqual(1, snapshot['stages']['customersWithGeneratedApiKeys'])
        self.assertEqual(1, snapshot['stages']['customersWithActiveApiKeys'])
        self.assertEqual(1, snapshot['activationFollowUps']['total'])
        self.assertEqual(1, snapshot['activationFollowUps']['windowedNewSignups'])
        self.assertEqual('create_key', snapshot['activationFollowUps']['nextAction'])
        self.assertEqual('pro', snapshot['activationFollowUps']['suggestedPlan'])
        self.assertEqual(1, snapshot['activationFollowUps']['countsBySuggestedPlan']['pro'])
        self.assertEqual(1, snapshot['activationFollowUps']['countsByStatus']['inactive'])
        self.assertIn('signup_to_key_recovery', snapshot['activationFollowUps']['primaryCtaUrl'])
        self.assertIn('start=create_key', snapshot['activationFollowUps']['primaryCtaUrl'])
        self.assertIn('/login.html', snapshot['activationFollowUps']['primaryCtaUrl'])
        self.assertIn('auth=email', snapshot['activationFollowUps']['primaryCtaUrl'])
        self.assertEqual('same_email_password', snapshot['activationFollowUps']['primaryCtaKind'])
        self.assertEqual(['passwordFallback', 'githubOAuth'], snapshot['activationFollowUps']['recommendedCtaOrder'])
        self.assertIn('primaryCtaUrls', snapshot['activationFollowUps'])
        self.assertEqual(snapshot['activationFollowUps']['primaryCtaUrls']['passwordFallback'], snapshot['activationFollowUps']['primaryCtaUrl'])
        self.assertIn('/account.html', snapshot['activationFollowUps']['primaryCtaUrls']['githubOAuth'])
        self.assertIn('auth=github', snapshot['activationFollowUps']['primaryCtaUrls']['githubOAuth'])
        self.assertIn('/login.html', snapshot['activationFollowUps']['primaryCtaUrls']['passwordFallback'])
        self.assertIn('auth=email', snapshot['activationFollowUps']['primaryCtaUrls']['passwordFallback'])
        self.assertIn('signup_to_key_recovery', snapshot['activationFollowUps']['primaryCtaUrls']['passwordFallback'])
        self.assertIn('generated-key-first', snapshot['activationFollowUps']['recommendedOperatorAction'])
        self.assertEqual(1, snapshot['activationFollowUps']['countsByEmailVerification']['not_required'])
        self.assertEqual(1, snapshot['activationFollowUps']['sendableQueued'])
        self.assertEqual(0, snapshot['activationFollowUps']['reviewOnlyQueued'])
        self.assertEqual(0, snapshot['activationFollowUps']['unknownQueued'])
        self.assertEqual(['not_required'], snapshot['activationFollowUps']['sendableSegments'])
        self.assertEqual([], snapshot['activationFollowUps']['reviewOnlySegments'])
        self.assertEqual(2, snapshot['activationFollowUps']['operatorFollowUpCopies'])
        self.assertEqual(1, snapshot['activationFollowUps']['operatorFollowUpWorked'])
        self.assertEqual(1, snapshot['activationFollowUps']['operatorFollowUpSendDryRuns'])
        self.assertEqual(2, snapshot['activationFollowUps']['operatorFollowUpSendDryRunRecipients'])
        self.assertEqual(1, snapshot['activationFollowUps']['operatorFollowUpSends'])
        self.assertEqual(2, snapshot['activationFollowUps']['operatorFollowUpSentRecipients'])
        self.assertEqual(0, snapshot['activationFollowUps']['operatorFollowUpSendFailures'])
        self.assertEqual(0, snapshot['activationFollowUps']['operatorFollowUpSendFailureRecipients'])
        self.assertEqual(1, snapshot['activationFollowUps']['keyRecoveryViews'])
        self.assertEqual(1, snapshot['activationFollowUps']['keyRecoveryViewsByState']['github'])
        self.assertEqual(1, snapshot['activationFollowUps']['keyCreateAttempts'])
        self.assertEqual(1, snapshot['activationFollowUps']['keyCreateSuccesses'])
        self.assertEqual(0, snapshot['activationFollowUps']['keyCreateFailures'])
        self.assertEqual(1, snapshot['activationFollowUps']['operatorFollowUpCopiesByKind']['single_copied'])
        self.assertEqual(1, snapshot['activationFollowUps']['operatorFollowUpCopiesByKind']['batch_copied'])
        self.assertEqual(1, snapshot['activationFollowUps']['operatorFollowUpWorkedByKind']['verified_marked_worked'])
        self.assertEqual(1, snapshot['activationFollowUps']['operatorFollowUpSendDryRunsByKind']['verified_send_dry_run'])
        self.assertEqual(1, snapshot['activationFollowUps']['operatorFollowUpSendsByKind']['verified_sent'])
        self.assertFalse(snapshot['activationFollowUps']['emailReadiness']['configured'])
        self.assertEqual('resend', snapshot['activationFollowUps']['emailReadiness']['provider'])
        self.assertTrue(snapshot['activationFollowUps']['emailReadiness']['dryRunSupported'])
        self.assertEqual('/admin/customers/send-activation-followups', snapshot['activationFollowUps']['emailReadiness']['sendEndpoint'])
        self.assertIn('SAGE_ROUTER_ACTIVATION_EMAIL_FROM', snapshot['activationFollowUps']['emailReadiness']['requiredEnv'])
        self.assertIn('SAGE_ROUTER_RESEND_API_KEY', snapshot['activationFollowUps']['emailReadiness']['secretManagerNames'])
        self.assertEqual('scripts/configure_activation_email_sender.sh', snapshot['activationFollowUps']['emailReadiness']['setupScript'])
        self.assertIn("SAGE_ROUTER_RESEND_API_KEY='re_...'", snapshot['activationFollowUps']['emailReadiness']['setupCommand'])
        self.assertIn('/admin/customers/send-activation-followups', snapshot['activationFollowUps']['emailReadiness']['dryRunCommand'])
        self.assertIn('"dryRun":true', snapshot['activationFollowUps']['emailReadiness']['dryRunCommand'])
        self.assertIn('"dryRun":false', snapshot['activationFollowUps']['emailReadiness']['sendCommandTemplate'])
        self.assertIn('"sendConfirmation":"SEND_ACTIVATION_FOLLOWUPS"', snapshot['activationFollowUps']['emailReadiness']['sendCommandTemplate'])
        self.assertIn('segmentCommandTemplates', snapshot['activationFollowUps']['emailReadiness'])
        self.assertIn('"segment":"verified"', snapshot['activationFollowUps']['emailReadiness']['segmentCommandTemplates']['verified']['sendCommand'])
        self.assertIn('"segment":"unverified"', snapshot['activationFollowUps']['emailReadiness']['segmentCommandTemplates']['unverified']['sendCommand'])
        self.assertEqual('SEND_ACTIVATION_FOLLOWUPS', snapshot['activationFollowUps']['emailReadiness']['sendConfirmation'])
        self.assertFalse(snapshot['activationFollowUps']['emailReadiness']['privacy']['containsSecrets'])
        self.assertFalse(snapshot['activationFollowUps']['emailReadiness']['privacy']['containsEmails'])
        self.assertFalse(snapshot['activationFollowUps']['privacy']['containsEmails'])
        self.assertFalse(snapshot['activationFollowUps']['privacy']['containsCustomerIds'])
        self.assertFalse(snapshot['activationFollowUps']['privacy']['containsApiKeys'])
        pricing_managed = snapshot['pricing']['publicLaunch']['managedProviderAccess']
        self.assertEqual(
            'scripts/configure_managed_provider_resale_readiness.sh',
            pricing_managed['readinessSetup']['setupScript'],
        )
        self.assertIn(
            'SAGEROUTER_MANAGED_PROVIDER_RESALE_ENABLE_PUBLIC',
            pricing_managed['readinessSetup']['enableCommandTemplate'],
        )
        self.assertFalse(pricing_managed['readinessSetup']['privacy']['containsSecrets'])
        self.assertEqual('signupToGeneratedKey', snapshot['nextBestAction']['metric'])
        self.assertEqual('fix_now', snapshot['nextBestAction']['priority'])
        self.assertIn('start=create_key', snapshot['nextBestAction']['ctaPath'])
        self.assertIn('auth=email', snapshot['nextBestAction']['ctaPath'])
        self.assertEqual(1, snapshot['nextBestAction']['evidence']['noKeyFollowUpsQueued'])
        self.assertEqual(1, snapshot['nextBestAction']['evidence']['sendableQueued'])
        self.assertEqual(0, snapshot['nextBestAction']['evidence']['reviewOnlyQueued'])
        self.assertEqual(0, snapshot['nextBestAction']['evidence']['unknownQueued'])
        self.assertEqual(['not_required'], snapshot['nextBestAction']['evidence']['sendableSegments'])
        self.assertEqual([], snapshot['nextBestAction']['evidence']['reviewOnlySegments'])
        self.assertEqual(2, snapshot['nextBestAction']['evidence']['operatorFollowUpCopies'])
        self.assertEqual(1, snapshot['nextBestAction']['evidence']['operatorFollowUpWorked'])
        self.assertEqual(1, snapshot['nextBestAction']['evidence']['operatorFollowUpSendDryRuns'])
        self.assertEqual(2, snapshot['nextBestAction']['evidence']['operatorFollowUpSendDryRunRecipients'])
        self.assertEqual(1, snapshot['nextBestAction']['evidence']['operatorFollowUpSends'])
        self.assertEqual(2, snapshot['nextBestAction']['evidence']['operatorFollowUpSentRecipients'])
        self.assertEqual(0, snapshot['nextBestAction']['evidence']['operatorFollowUpSendFailures'])
        self.assertEqual(0, snapshot['nextBestAction']['evidence']['operatorFollowUpSendFailureRecipients'])
        self.assertEqual(1, snapshot['nextBestAction']['evidence']['keyRecoveryViews'])
        self.assertEqual(1, snapshot['nextBestAction']['evidence']['keyCreateAttempts'])
        self.assertEqual(1, snapshot['nextBestAction']['evidence']['keyCreateSuccesses'])
        self.assertEqual(0, snapshot['nextBestAction']['evidence']['keyCreateFailures'])
        self.assertFalse(snapshot['nextBestAction']['privacy']['containsEmails'])
        self.assertNotIn('buyer@example.com', json.dumps(snapshot['nextBestAction']))
        packet = snapshot['operatorExecutionPacket']
        self.assertEqual('signup_to_key_recovery', packet['kind'])
        self.assertEqual('Signup-to-key recovery packet', packet['title'])
        self.assertEqual('signupToGeneratedKey', packet['metric'])
        self.assertIn('generated-key-first', packet['recommendedAction'])
        self.assertEqual(snapshot['nextBestAction']['ctaPath'], packet['ctaPath'])
        self.assertEqual(snapshot['nextBestAction']['successMetric'], packet['successMetric'])
        self.assertEqual(snapshot['nextBestAction']['executionChecklist'], packet['executionChecklist'])
        self.assertEqual(1, packet['totalQueued'])
        self.assertIn('sendTelemetry', packet)
        self.assertEqual(1, packet['sendTelemetry']['dryRunActions'])
        self.assertEqual(2, packet['sendTelemetry']['dryRunRecipients'])
        self.assertEqual(1, packet['sendTelemetry']['sendActions'])
        self.assertEqual(2, packet['sendTelemetry']['sentRecipients'])
        self.assertEqual(0, packet['sendTelemetry']['failedRecipients'])
        self.assertTrue(packet['sendTelemetry']['dryRunVerified'])
        self.assertFalse(packet['sendTelemetry']['sendApprovalRequired'])
        self.assertIn('not_required', packet['segmentCounts'])
        self.assertEqual('not_required', packet['segmentActions'][0]['segment'])
        self.assertIn('start=create_key', packet['recoveryUrls']['passwordFallback'])
        self.assertIn('auth=email', packet['recoveryUrls']['passwordFallback'])
        self.assertIn('auth=github', packet['recoveryUrls']['githubOAuth'])
        self.assertIn('Finish your Sage Router setup key', packet['draft']['subject'])
        self.assertIn('same email/password path first', packet['draft']['body'])
        self.assertIn('operator_no_key_followup_batch_copied', packet['telemetry']['copyEvents'])
        self.assertIn('account_key_recovery_viewed', packet['telemetry']['recoveryViewEvents'])
        self.assertIn('account_api_key_create_clicked', packet['telemetry']['keyCreateAttemptEvents'])
        self.assertIn('account_key_recovery_key_created', packet['telemetry']['keyCreateSuccessEvents'])
        self.assertFalse(packet['emailReadiness']['configured'])
        self.assertEqual('resend', packet['emailReadiness']['provider'])
        self.assertIn('copy fallback', packet['emailReadiness']['operatorAction'])
        self.assertIn('scripts/configure_activation_email_sender.sh', packet['emailReadiness']['setupCommand'])
        self.assertIn('"dryRun":true', packet['emailReadiness']['dryRunCommand'])
        self.assertIn('Origin: https://app.sagerouter.dev', packet['emailReadiness']['dryRunCommand'])
        self.assertIn('"sendConfirmation":"SEND_ACTIVATION_FOLLOWUPS"', packet['emailReadiness']['sendCommandTemplate'])
        self.assertIn('segmentCommandTemplates', packet['emailReadiness'])
        self.assertFalse(packet['emailReadiness']['privacy']['containsApiKeyValues'])
        self.assertTrue(packet['privacy']['aggregateOnly'])
        self.assertFalse(packet['privacy']['containsEmails'])
        self.assertFalse(packet['privacy']['containsCustomerIds'])
        self.assertNotIn('buyer@example.com', json.dumps(packet))
        self.assertNotIn(raw, json.dumps(packet))
        self.assertEqual(2, snapshot['stages']['setupSnippetCopies'])
        self.assertEqual(1, snapshot['stages']['customersWithFirstRoutedRequest'])
        self.assertEqual(1, snapshot['stages']['paidConversions'])
        self.assertEqual(1, snapshot['stages']['paidCustomers'])
        self.assertEqual(1, snapshot['stages']['retainedPaidCustomers'])
        self.assertEqual(10000, snapshot['mrr']['targetMrrUsd'])
        self.assertEqual(30, snapshot['mrr']['estimatedCurrentMrrUsd'])
        self.assertEqual(0.003, snapshot['mrr']['targetAttainment'])
        self.assertEqual(1, snapshot['mrr']['byPlan']['pro']['paidCustomers'])
        self.assertEqual(30, snapshot['mrr']['byPlan']['pro']['monthlyPriceUsd'])
        self.assertEqual(199, snapshot['mrr']['byPlan']['pro']['remainingToTarget'])
        self.assertEqual(6000, snapshot['mrr']['byPlan']['pro']['targetMrrUsd'])
        self.assertEqual(5970, snapshot['mrr']['byPlan']['pro']['remainingMrrToTargetUsd'])
        self.assertEqual('pro', snapshot['mrr']['planRevenueActions'][0]['plan'])
        self.assertEqual(199, snapshot['mrr']['planRevenueActions'][0]['customerGap'])
        self.assertEqual(5970, snapshot['mrr']['planRevenueActions'][0]['remainingMrrToTargetUsd'])
        self.assertIn('Convert active generated-key users into Pro', snapshot['mrr']['planRevenueActions'][0]['action'])
        self.assertEqual('max', snapshot['mrr']['planRevenueActions'][1]['plan'])
        self.assertFalse(snapshot['mrr']['assumptions']['managedProviderAccessIncluded'])
        self.assertEqual(0.60, snapshot['targets']['signupToGeneratedKey']['targetRate'])
        self.assertEqual(0.50, snapshot['targets']['generatedKeyToFirstRequest']['targetRate'])
        self.assertEqual(0.35, snapshot['targets']['setupCopyToFirstRequest']['targetRate'])
        self.assertEqual(0.15, snapshot['targets']['signupToPaidConversion']['targetRate'])
        self.assertEqual(0.85, snapshot['targets']['paidRecentUsage']['targetRate'])
        self.assertEqual(1.0, snapshot['targets']['mrrTargetAttainment']['targetRate'])
        self.assertEqual(0.0, snapshot['targets']['checkoutReadinessFriction']['targetRate'])
        self.assertEqual(0.4545, snapshot['targets']['checkoutReadinessFriction']['actualRate'])
        self.assertEqual('below_target', snapshot['targets']['checkoutReadinessFriction']['status'])
        self.assertEqual(0.5, snapshot['targets']['signupToGeneratedKey']['actualRate'])
        self.assertEqual('below_target', snapshot['targets']['signupToGeneratedKey']['status'])
        self.assertEqual('on_track', snapshot['targets']['generatedKeyToFirstRequest']['status'])
        self.assertEqual(0.5, snapshot['rates']['setupCopyToFirstRequest'])
        self.assertEqual('on_track', snapshot['targets']['setupCopyToFirstRequest']['status'])
        bottleneck_metrics = [row['metric'] for row in snapshot['bottlenecks']]
        self.assertIn('mrrTargetAttainment', bottleneck_metrics)
        self.assertIn('checkoutReadinessFriction', bottleneck_metrics)
        self.assertIn('signupToGeneratedKey', bottleneck_metrics)
        conversion_metrics = [row['metric'] for row in snapshot['conversionActions']]
        self.assertIn('mrrTargetAttainment', conversion_metrics)
        self.assertIn('checkoutReadinessFriction', conversion_metrics)
        self.assertIn('signupToGeneratedKey', conversion_metrics)
        self.assertIn('owner', snapshot['conversionActions'][0])
        self.assertIn('surface', snapshot['conversionActions'][0])
        self.assertIn('ctaPath', snapshot['conversionActions'][0])
        self.assertIn('successMetric', snapshot['conversionActions'][0])
        self.assertNotIn('buyer@example.com', json.dumps(snapshot['conversionActions']))
        self.assertFalse(snapshot['privacy']['containsEmails'])
        self.assertFalse(snapshot['privacy']['containsApiKeys'])
        self.assertNotIn('u@example.com', json.dumps(snapshot))
        self.assertNotIn(raw, json.dumps(snapshot))

    def test_next_best_action_points_to_operator_queue_until_followups_are_worked(self):
        stages = {'signups': 2, 'customersWithGeneratedApiKeys': 0, 'customersWithFirstRoutedRequest': 0, 'paidCustomers': 0}
        rates = {'signupToGeneratedKey': 0.0}
        privacy = {'containsEmails': False, 'containsCustomerIds': False, 'containsApiKeys': False, 'containsProviderCredentials': False}
        activation_follow_ups = {
            'total': 2,
            'windowedNewSignups': 2,
            'operatorFollowUpCopies': 0,
            'operatorFollowUpWorked': 0,
            'keyFirstRedirects': 1,
            'keyFirstRedirectsByState': {'checkout_key_first': 1},
            'countsByEmailVerification': {'verified': 1, 'unverified': 1},
            'primaryCtaUrl': 'https://app.sagerouter.dev/login.html?start=create_key&plan=pro&auth=email',
            'privacy': privacy,
        }

        action = router.launch_next_best_action(stages, rates, {'estimatedCurrentMrrUsd': 0, 'targetMrrUsd': 10000}, activation_follow_ups, [])

        self.assertEqual('signupToGeneratedKey', action['metric'])
        self.assertEqual('launch funnel', action['surface'])
        self.assertIn('/launch-funnel.html#no-key-followups:segments', action['ctaPath'])
        self.assertIn('operator no-key signup queue', action['action'])
        self.assertIn('auth-repair segments separately', action['action'])
        self.assertEqual(2, action['evidence']['sendableQueued'])
        self.assertEqual(0, action['evidence']['reviewOnlyQueued'])
        self.assertEqual(0, action['evidence']['unknownQueued'])
        self.assertEqual(['verified', 'unverified'], action['evidence']['sendableSegments'])
        self.assertEqual([], action['evidence']['reviewOnlySegments'])
        self.assertEqual(0, action['evidence']['operatorFollowUpCopies'])
        self.assertEqual(0, action['evidence']['operatorFollowUpWorked'])
        self.assertEqual(0, action['evidence']['operatorFollowUpSendDryRuns'])
        self.assertEqual(0, action['evidence']['operatorFollowUpSendDryRunRecipients'])
        self.assertEqual(0, action['evidence']['operatorFollowUpSends'])
        self.assertEqual(0, action['evidence']['operatorFollowUpSentRecipients'])
        self.assertEqual(0, action['evidence']['operatorFollowUpSendFailures'])
        self.assertEqual(0, action['evidence']['operatorFollowUpSendFailureRecipients'])
        self.assertEqual(1, action['evidence']['keyFirstRedirects'])
        self.assertEqual(1, action['evidence']['keyFirstRedirectsByState']['checkout_key_first'])
        self.assertEqual(['verified', 'unverified'], action['evidence']['recommendedSegments'])
        self.assertEqual('verified', action['executionChecklist'][0]['segment'])
        self.assertIn('verified drafts first', action['executionChecklist'][0]['action'])
        self.assertEqual('unverified', action['executionChecklist'][1]['segment'])
        self.assertIn('Mark the worked segment', action['executionChecklist'][2]['action'])
        self.assertEqual('measure', action['executionChecklist'][3]['segment'])
        self.assertFalse(action['privacy']['containsEmails'])

        worked = router.launch_next_best_action(
            stages,
            rates,
            {'estimatedCurrentMrrUsd': 0, 'targetMrrUsd': 10000},
            {**activation_follow_ups, 'operatorFollowUpCopies': 1, 'operatorFollowUpWorked': 1, 'operatorFollowUpWorkedByKind': {'verified_marked_worked': 1}},
            [],
        )

        self.assertEqual('account', worked['surface'])
        self.assertIn('start=create_key', worked['ctaPath'])
        self.assertIn('/login.html', worked['ctaPath'])
        self.assertIn('auth=email', worked['ctaPath'])
        self.assertEqual(1, worked['evidence']['operatorFollowUpCopies'])
        self.assertEqual(1, worked['evidence']['operatorFollowUpWorked'])

        copied_only = router.launch_next_best_action(
            stages,
            rates,
            {'estimatedCurrentMrrUsd': 0, 'targetMrrUsd': 10000},
            {**activation_follow_ups, 'operatorFollowUpCopies': 1, 'operatorFollowUpWorked': 0},
            [],
        )
        self.assertEqual('launch funnel', copied_only['surface'])
        self.assertIn('/launch-funnel.html#no-key-followups:segments', copied_only['ctaPath'])

    def test_activation_delivery_counts_mark_auth_repair_review_only(self):
        delivery = router.launch_activation_delivery_counts({
            'total': 4,
            'countsByEmailVerification': {
                'verified': 1,
                'unverified': 1,
                'missing_auth_user': 1,
            },
        })

        self.assertEqual(2, delivery['sendableQueued'])
        self.assertEqual(1, delivery['reviewOnlyQueued'])
        self.assertEqual(1, delivery['unknownQueued'])
        self.assertEqual(['verified', 'unverified'], delivery['sendableSegments'])
        self.assertEqual(['missing_auth_user'], delivery['reviewOnlySegments'])

    def test_operator_execution_packet_is_aggregate_only(self):
        privacy = {'containsEmails': False, 'containsCustomerIds': False, 'containsApiKeys': False, 'containsProviderCredentials': False}
        activation_follow_ups = {
            'total': 2,
            'windowedNewSignups': 2,
            'countsByEmailVerification': {'verified': 1, 'unverified': 1},
            'suggestedPlan': 'pro',
            'primaryCtaKind': 'same_email_password',
            'primaryCtaUrl': 'https://app.sagerouter.dev/login.html?start=create_key&plan=pro&auth=email',
            'primaryCtaUrls': {
                'passwordFallback': 'https://app.sagerouter.dev/login.html?start=create_key&plan=pro&auth=email',
                'githubOAuth': 'https://app.sagerouter.dev/account.html?start=create_key&plan=pro&auth=github',
            },
            'recommendedCtaOrder': ['passwordFallback', 'githubOAuth'],
            'successMetric': 'Move no-key signups into generated-key accounts, then first routed request.',
            'privacy': privacy,
        }
        action = {
            'metric': 'signupToGeneratedKey',
            'priority': 'fix_now',
            'owner': 'Activation',
            'surface': 'launch funnel',
            'successMetric': activation_follow_ups['successMetric'],
            'evidence': {'recommendedSegments': ['verified', 'unverified']},
        }

        packet = router.launch_operator_execution_packet(action, activation_follow_ups)

        self.assertEqual('signup_to_key_recovery', packet['kind'])
        self.assertEqual(2, packet['totalQueued'])
        self.assertEqual(2, packet['sendableQueued'])
        self.assertEqual(0, packet['reviewOnlyQueued'])
        self.assertEqual(2, packet['windowedNewSignups'])
        self.assertEqual(['passwordFallback', 'githubOAuth'], packet['recommendedCtaOrder'])
        self.assertEqual(['verified', 'unverified'], [row['segment'] for row in packet['segmentActions']])
        self.assertTrue(packet['segmentActions'][0]['sendable'])
        self.assertEqual('send', packet['segmentActions'][0]['deliveryMode'])
        self.assertEqual('verified_aggregate_draft_copied', packet['segmentActions'][0]['copyKind'])
        self.assertEqual('verified_marked_worked', packet['segmentActions'][0]['workedKind'])
        self.assertEqual('unverified_marked_worked', packet['segmentActions'][1]['workedKind'])
        self.assertIn('"segment":"verified"', packet['segmentActions'][0]['dryRunCommand'])
        self.assertIn('"segment":"verified"', packet['segmentActions'][0]['sendCommand'])
        self.assertIn('"sendConfirmation":"SEND_ACTIVATION_FOLLOWUPS"', packet['segmentActions'][0]['sendCommand'])
        self.assertIn('"segment":"unverified"', packet['segmentActions'][1]['sendCommand'])
        self.assertEqual(0, packet['sendTelemetry']['dryRunRecipients'])
        self.assertEqual(0, packet['sendTelemetry']['sentRecipients'])
        self.assertFalse(packet['sendTelemetry']['dryRunVerified'])
        self.assertTrue(packet['sendTelemetry']['sendApprovalRequired'])
        self.assertIn('Dry-run the activation sender before real outreach.', packet['instructions'][0])
        self.assertIn('No provider key, prompt text, OAuth token, generated API key, or checkout', packet['draft']['body'])
        self.assertFalse(packet['privacy']['containsEmails'])
        self.assertFalse(packet['privacy']['containsCustomerIds'])
        self.assertFalse(packet['privacy']['containsApiKeys'])
        self.assertTrue(packet['privacy']['aggregateOnly'])
        self.assertNotIn('buyer@example.com', json.dumps(packet))
        self.assertNotIn('cus_', json.dumps(packet))

    def test_operator_execution_packet_marks_auth_repair_segments_review_only(self):
        action = {
            'metric': 'signupToGeneratedKey',
            'priority': 'fix_now',
            'evidence': {'recommendedSegments': ['verified', 'unverified', 'missing_auth_user']},
        }
        activation_follow_ups = {
            'total': 3,
            'windowedNewSignups': 3,
            'countsByEmailVerification': {'verified': 1, 'unverified': 1, 'missing_auth_user': 1},
            'suggestedPlan': 'pro',
        }

        packet = router.launch_operator_execution_packet(action, activation_follow_ups)

        self.assertEqual(3, packet['totalQueued'])
        self.assertEqual(2, packet['sendableQueued'])
        self.assertEqual(1, packet['reviewOnlyQueued'])
        self.assertTrue(packet['sendTelemetry']['sendApprovalRequired'])
        self.assertEqual('verified', packet['sendTelemetry']['nextSendSegment'])
        rows = {row['segment']: row for row in packet['segmentActions']}
        self.assertTrue(rows['verified']['sendable'])
        self.assertEqual('send', rows['verified']['deliveryMode'])
        self.assertFalse(rows['missing_auth_user']['sendable'])
        self.assertEqual('review', rows['missing_auth_user']['deliveryMode'])
        self.assertIn('auth-user repair', rows['missing_auth_user']['reviewReason'])
        self.assertIn('sendCommand', rows['verified'])
        self.assertIn('"segment":"verified"', rows['verified']['sendCommand'])
        self.assertNotIn('sendCommand', rows['missing_auth_user'])

    def test_launch_funnel_counts_supabase_auth_signups_without_customer_rows(self):
        now = router.now_epoch()
        router.SUPABASE_URL = 'https://example.supabase.co'
        router.SUPABASE_SERVICE_ROLE_KEY = 'service'
        router.read_launch_auth_user_rows = lambda limit=1000: [
            {'id': 'auth-user-1', 'email': 'buyer@example.com', 'created_at': now - 60, 'email_confirmed': True},
            {'id': 'auth-user-2', 'email': 'pending@example.com', 'created_at': now - 120, 'email_confirmed': False},
        ]
        router.read_launch_waitlist_counts = lambda _since, limit=10000: ({
            'total': 0,
            'interest': {'managedAccess': 0},
            'managedAccessDemand': router.new_managed_access_demand_metrics(),
        }, None)
        router.read_launch_marketing_funnel_counts = lambda _since, limit=10000: ({
            'total': 0,
            'events': {},
            'plans': {},
            'sourceSurfaces': {},
            'attributionChannels': {},
            'authProviderState': router.new_auth_provider_state_metrics(),
            'modelCatalogDemand': router.new_model_catalog_demand_metrics(),
            'setupSnippetCopies': 0,
            'setupSnippetCopiesBySnippet': {},
        }, None)

        snapshot = router.build_launch_funnel_snapshot(30 * 24 * 3600)

        self.assertEqual(2, snapshot['stages']['signups'])
        self.assertEqual(2, snapshot['signupHydration']['authSignups'])
        self.assertEqual(1, snapshot['signupHydration']['confirmedAuthSignups'])
        self.assertEqual(0, snapshot['signupHydration']['customerRowsCreated'])
        self.assertEqual(2, snapshot['signupHydration']['authSignupsWithoutCustomerRows'])
        self.assertEqual('supabase_auth_admin', snapshot['signupHydration']['source'])
        self.assertEqual('supabase', snapshot['source']['authUsers'])
        self.assertIn('auth_signups_without_customer_rows:2', snapshot['notes'])
        self.assertNotIn('auth-user-1', json.dumps(snapshot))
        self.assertNotIn('auth-user-2', json.dumps(snapshot))
        self.assertNotIn('buyer@example.com', json.dumps(snapshot))
        self.assertNotIn('pending@example.com', json.dumps(snapshot))
        self.assertEqual(0, snapshot['activationFollowUps']['total'])
        self.assertFalse(snapshot['activationFollowUps']['privacy']['containsEmails'])
        self.assertEqual('marketing_funnel_empty', snapshot['authProviderState']['source'])
        self.assertFalse(snapshot['authProviderState']['githubAvailable'])
        self.assertEqual('email_first', snapshot['authProviderState']['recommendedRecoveryAuth'])

    def test_launch_funnel_uses_customer_signup_rows_when_auth_page_is_incomplete(self):
        now = router.now_epoch()
        router.read_launch_auth_user_rows = lambda limit=1000: [
            {'id': 'auth-user-1', 'email': 'buyer@example.com', 'created_at': now - 60, 'email_confirmed': True},
        ]
        router.read_launch_waitlist_counts = lambda _since, limit=10000: ({
            'total': 0,
            'interest': {'managedAccess': 0},
            'managedAccessDemand': router.new_managed_access_demand_metrics(),
        }, None)
        router.read_launch_marketing_funnel_counts = lambda _since, limit=10000: ({
            'total': 0,
            'events': {},
            'plans': {},
            'sourceSurfaces': {},
            'attributionChannels': {},
            'authProviderState': router.new_auth_provider_state_metrics(),
            'modelCatalogDemand': router.new_model_catalog_demand_metrics(),
            'setupSnippetCopies': 0,
            'setupSnippetCopiesBySnippet': {},
        }, None)
        first = router.customer_for_user({'id': 'auth-user-1', 'email': 'buyer@example.com'})
        second = router.customer_for_user({'id': 'auth-user-2', 'email': 'pending@example.com'})
        router.update_customer(first['id'], {'created_at_epoch': now - 60})
        router.update_customer(second['id'], {'created_at_epoch': now - 120})

        snapshot = router.build_launch_funnel_snapshot(30 * 24 * 3600)

        self.assertEqual(2, snapshot['stages']['signups'])
        self.assertEqual(1, snapshot['signupHydration']['authSignups'])
        self.assertEqual(2, snapshot['signupHydration']['customerRowsCreated'])
        self.assertEqual(2, snapshot['signupHydration']['effectiveSignups'])
        self.assertEqual(1, snapshot['signupHydration']['customerSignupsWithoutAuthRows'])
        self.assertIn('customer_signups_without_auth_rows:1', snapshot['notes'])
        self.assertEqual(2, snapshot['activationFollowUps']['total'])
        self.assertNotIn('buyer@example.com', json.dumps(snapshot))
        self.assertNotIn('pending@example.com', json.dumps(snapshot))

    def test_launch_waitlist_counts_group_managed_access_interest(self):
        router.SUPABASE_URL = 'https://example.supabase.co'
        router.SUPABASE_SERVICE_ROLE_KEY = 'service-role'

        def fake_select(table, query, timeout=8):
            self.assertIn('created_at=gte.', query)
            if table == router.SUPABASE_WAITLIST_TABLE:
                self.assertIn('select=created_at,metadata', query)
                return [
                    {
                        'created_at': '2026-06-19T00:00:00Z',
                        'metadata': {
                            'interest': 'managed-access',
                            'target_provider_family': 'openai',
                            'commercial_preference': 'one-subscription',
                            'intent': 'max-implementation',
                        },
                    },
                    {
                        'created_at': '2026-06-19T00:00:00Z',
                        'metadata': json.dumps({
                            'interest': 'managed-access',
                            'targetProviderFamily': 'anthropic',
                            'commercialPreference': 'private-contract',
                            'intent': 'gateway-migration',
                        }),
                    },
                    {'created_at': '2026-06-19T00:00:00Z', 'metadata': {'interest': 'managed-access'}},
                    {'created_at': '2026-06-19T00:00:00Z', 'metadata': {'interest': 'general'}},
                    {'created_at': '2026-06-19T00:00:00Z', 'metadata': json.dumps({'interest': 'enterprise'})},
                ]
            return []

        router.supabase_select = fake_select

        metrics, error = router.read_launch_waitlist_counts(0)
        self.assertIsNone(error)
        self.assertEqual(5, metrics['total'])
        self.assertEqual(3, metrics['interest']['managedAccess'])
        self.assertEqual(1, metrics['interest']['general'])
        self.assertEqual(1, metrics['interest']['other'])
        self.assertEqual(0, metrics['interest']['unknown'])
        self.assertEqual(1, metrics['managedAccessDemand']['targetProviderFamily']['openai'])
        self.assertEqual(1, metrics['managedAccessDemand']['targetProviderFamily']['anthropic'])
        self.assertEqual(1, metrics['managedAccessDemand']['targetProviderFamily']['unknown'])
        self.assertEqual(1, metrics['managedAccessDemand']['commercialPreference']['one-subscription'])
        self.assertEqual(1, metrics['managedAccessDemand']['commercialPreference']['private-contract'])
        self.assertEqual(1, metrics['managedAccessDemand']['commercialPreference']['unknown'])
        self.assertEqual(1, metrics['managedAccessDemand']['intent']['max-implementation'])
        self.assertEqual(1, metrics['managedAccessDemand']['intent']['gateway-migration'])
        self.assertEqual(1, metrics['managedAccessDemand']['intent']['unknown'])

        count, error = router.read_launch_waitlist_count(0)
        self.assertIsNone(error)
        self.assertEqual(5, count)

    def test_launch_marketing_funnel_counts_group_events_without_identity(self):
        router.SUPABASE_URL = 'https://example.supabase.co'
        router.SUPABASE_SERVICE_ROLE_KEY = 'service-role'

        def fake_select(table, query, timeout=8):
            self.assertEqual(router.SUPABASE_FUNNEL_EVENTS_TABLE, table)
            self.assertIn('select=event,plan,created_at,source_page,metadata', query)
            self.assertIn('created_at=gte.', query)
            return [
                {
                    'event': 'landing_account_clicked',
                    'plan': 'pro',
                    'created_at': '2026-06-19T00:00:00Z',
                    'metadata': {
                        'source': 'landing',
                        'utmSource': 'discord',
                    },
                },
                {
                    'event': 'landing_key_first_direct_clicked',
                    'plan': 'pro',
                    'created_at': '2026-06-19T00:00:00Z',
                    'metadata': {
                        'source': 'landing',
                        'state': 'hero-key-first',
                    },
                },
                {
                    'event': 'landing_viewed',
                    'plan': None,
                    'created_at': '2026-06-19T00:00:00Z',
                    'metadata': {
                        'source': 'landing',
                        'utmSource': 'google',
                    },
                },
                {
                    'event': 'landing_key_recovery_clicked',
                    'plan': 'pro',
                    'created_at': '2026-06-19T00:00:00Z',
                    'metadata': {
                        'source': 'landing',
                        'state': 'landing-returning-user',
                    },
                },
                {
                    'event': 'content_article_key_recovery_clicked',
                    'plan': 'pro',
                    'created_at': '2026-06-19T00:00:00Z',
                    'metadata': {
                        'source': 'article',
                        'state': 'article-returning-user',
                    },
                },
                {
                    'event': 'pricing_key_recovery_clicked',
                    'plan': 'pro',
                    'created_at': '2026-06-19T00:00:00Z',
                    'metadata': {
                        'source': 'pricing',
                        'state': 'pricing_returning_no_key',
                    },
                },
                {
                    'event': 'account_api_key_created',
                    'plan': 'pro',
                    'created_at': '2026-06-19T00:00:00Z',
                    'metadata': {
                        'source': 'account',
                        'state': 'created',
                    },
                },
                {
                    'event': 'account_key_recovery_viewed',
                    'plan': 'pro',
                    'created_at': '2026-06-19T00:00:00Z',
                    'metadata': {
                        'source': 'account',
                        'state': 'github',
                    },
                },
                {
                    'event': 'account_auto_oauth_skipped',
                    'plan': 'pro',
                    'created_at': '2026-06-19T00:00:00Z',
                    'metadata': {
                        'source': 'account',
                        'state': 'email_auth_requested',
                    },
                },
                {
                    'event': 'account_checkout_key_first_redirected',
                    'plan': 'pro',
                    'created_at': '2026-06-19T00:00:00Z',
                    'metadata': {
                        'source': 'account',
                        'state': 'checkout_key_first',
                    },
                },
                {
                    'event': 'account_intent_create_key_clicked',
                    'plan': 'pro',
                    'created_at': '2026-06-19T00:00:00Z',
                    'metadata': {
                        'source': 'account',
                        'state': 'saved_key_recovery_auto_key',
                    },
                },
                {
                    'event': 'login_key_recovery_shown',
                    'plan': 'pro',
                    'created_at': '2026-06-19T00:00:00Z',
                    'metadata': {
                        'source': 'login',
                        'state': 'login_recovery_cta',
                    },
                },
                {
                    'event': 'login_key_recovery_landed',
                    'plan': 'pro',
                    'created_at': '2026-06-19T00:00:00Z',
                    'metadata': {
                        'source': 'login',
                        'state': 'password_fallback',
                    },
                },
                {
                    'event': 'login_key_recovery_clicked',
                    'plan': 'pro',
                    'created_at': '2026-06-19T00:00:00Z',
                    'metadata': {
                        'source': 'login',
                        'state': 'login_recovery_cta',
                    },
                },
                {
                    'event': 'login_key_recovery_same_account_prompted',
                    'plan': 'pro',
                    'created_at': '2026-06-19T00:00:00Z',
                    'metadata': {
                        'source': 'login',
                        'state': 'manual_same_email_focus',
                    },
                },
                {
                    'event': 'login_key_recovery_session_redirected',
                    'plan': 'pro',
                    'created_at': '2026-06-19T00:00:00Z',
                    'metadata': {
                        'source': 'login',
                        'state': 'signed_in_recovery_redirect',
                    },
                },
                {
                    'event': 'model_catalog_viewed',
                    'plan': None,
                    'created_at': '2026-06-19T00:00:00Z',
                    'metadata': {
                        'source': 'model-catalog',
                        'modelFamily': 'all',
                        'queryBucket': 'empty',
                        'utmSource': 'model-gateway',
                        'search': 'gpt raw text must not appear',
                    },
                },
                {
                    'event': 'model_catalog_search_bucketed',
                    'plan': None,
                    'created_at': '2026-06-19T00:00:00Z',
                    'metadata': {
                        'source': 'model-catalog',
                        'modelFamily': 'ollama',
                        'queryBucket': 'ollama',
                    },
                },
                {
                    'event': 'model_catalog_filter_clicked',
                    'plan': None,
                    'created_at': '2026-06-19T00:00:00Z',
                    'metadata': json.dumps({
                        'source': 'model-catalog',
                        'modelFamily': 'openai-codex',
                        'queryBucket': 'openai-codex',
                    }),
                },
                {
                    'event': 'account_snippet_copied',
                    'plan': 'pro',
                    'created_at': '2026-06-19T00:00:00Z',
                    'metadata': {
                        'source': 'account',
                        'snippet': 'codex-cli',
                    },
                },
                {
                    'event': 'quickstart_snippet_copied',
                    'plan': None,
                    'created_at': '2026-06-19T00:00:00Z',
                    'metadata': {
                        'source': 'quickstart',
                        'snippet': 'quickstart-curl',
                    },
                },
                {
                    'event': 'operator_no_key_followup_copied',
                    'plan': 'pro',
                    'created_at': '2026-06-19T00:00:00Z',
                    'metadata': {
                        'source': 'launch-plan',
                        'state': 'single_copied',
                        'snippet': 'no-key-followup',
                    },
                },
                {
                    'event': 'operator_no_key_followup_batch_copied',
                    'plan': 'pro',
                    'created_at': '2026-06-19T00:00:00Z',
                    'metadata': {
                        'source': 'launch-plan',
                        'state': 'batch_copied',
                        'snippet': 'no-key-followup',
                    },
                },
                {
                    'event': 'operator_no_key_followup_batch_copied',
                    'plan': 'pro',
                    'created_at': '2026-06-19T00:00:00Z',
                    'metadata': {
                        'source': 'launch-plan',
                        'state': 'verified_batch_copied',
                        'snippet': 'no-key-followup',
                    },
                },
                {
                    'event': 'operator_no_key_followup_mailto_opened',
                    'plan': 'pro',
                    'created_at': '2026-06-19T00:00:00Z',
                    'metadata': {
                        'source': 'launch-plan',
                        'state': 'verified_mailto_opened',
                        'snippet': 'no-key-followup',
                    },
                },
                {
                    'event': 'operator_no_key_followup_csv_copied',
                    'plan': 'pro',
                    'created_at': '2026-06-19T00:00:00Z',
                    'metadata': {
                        'source': 'launch-plan',
                        'state': 'verified_csv_copied',
                        'snippet': 'no-key-followup',
                    },
                },
                {
                    'event': 'operator_no_key_followup_send_dry_run',
                    'plan': 'pro',
                    'created_at': '2026-06-19T00:00:00Z',
                    'metadata': {
                        'source': 'launch-plan',
                        'state': 'verified_send_dry_run',
                        'snippet': 'no-key-followup',
                        'resultCount': 2,
                    },
                },
                {
                    'event': 'operator_no_key_followup_sent',
                    'plan': 'pro',
                    'created_at': '2026-06-19T00:00:00Z',
                    'metadata': {
                        'source': 'launch-plan',
                        'state': 'verified_sent',
                        'snippet': 'no-key-followup',
                        'resultCount': 2,
                    },
                },
                {
                    'event': 'operator_no_key_followup_send_failed',
                    'plan': 'pro',
                    'created_at': '2026-06-19T00:00:00Z',
                    'metadata': {
                        'source': 'launch-plan',
                        'state': 'unverified_send_failed',
                        'snippet': 'no-key-followup',
                        'resultCount': 1,
                    },
                },
                {
                    'event': 'operator_no_key_followup_batch_copied',
                    'plan': 'pro',
                    'created_at': '2026-06-19T00:00:00Z',
                    'metadata': {
                        'source': 'launch-plan',
                        'state': 'verified_marked_worked',
                        'snippet': 'no-key-followup',
                    },
                },
                {
                    'event': 'account_login_submitted',
                    'plan': None,
                    'created_at': '2026-06-19T00:00:00Z',
                    'metadata': {
                        'source': 'login',
                        'button': 'password_login',
                        'state': 'password',
                    },
                },
                {
                    'event': 'auth_provider_state_checked',
                    'plan': None,
                    'created_at': '2026-06-19T00:00:00Z',
                    'metadata': {
                        'source': 'login',
                        'state': 'loaded',
                        'enabledProviders': 'github',
                        'disabledProviders': 'google,discord',
                        'githubEnabled': True,
                    },
                },
                {
                    'event': 'auth_provider_state_checked',
                    'plan': None,
                    'created_at': '2026-06-19T00:00:00Z',
                    'metadata': json.dumps({
                        'source': 'account',
                        'state': 'unavailable',
                        'enabledProviders': 'none',
                        'disabledProviders': 'github,google,discord',
                        'githubEnabled': False,
                    }),
                },
                {
                    'event': 'calculator_checkout_clicked',
                    'plan': 'pro',
                    'created_at': '2026-06-19T00:00:00Z',
                    'metadata': {
                        'source': 'model-routing-calculator',
                        'utmSource': 'github',
                        'email': 'buyer@example.com',
                    },
                },
                {
                    'event': 'calculator_viewed',
                    'plan': None,
                    'created_at': '2026-06-19T00:00:00Z',
                    'metadata': {
                        'source': 'model-routing-calculator',
                        'utmSource': 'model-gateway',
                    },
                },
                {
                    'event': 'calculator_checkout_clicked',
                    'plan': 'pro',
                    'created_at': '2026-06-19T00:00:00Z',
                    'metadata': json.dumps({
                        'source': 'compare-gateways',
                        'referrerHost': 'model-gateway.example',
                    }),
                },
                {
                    'event': 'gateway_compare_viewed',
                    'plan': None,
                    'created_at': '2026-06-19T00:00:00Z',
                    'metadata': json.dumps({
                        'source': 'compare-gateways',
                        'referrerHost': 'model-gateway.example',
                    }),
                },
                {
                    'event': 'launch_plan_checkout_clicked',
                    'plan': 'pro',
                    'created_at': '2026-06-19T00:00:00Z',
                    'metadata': {
                        'source': 'launch-plan',
                        'utmSource': 'newsletter',
                    },
                },
                {
                    'event': 'launch_plan_viewed',
                    'plan': None,
                    'created_at': '2026-06-19T00:00:00Z',
                    'metadata': {
                        'source': 'launch-plan',
                        'utmSource': 'newsletter',
                    },
                },
                {
                    'event': 'pricing_checkout_clicked',
                    'plan': 'lite',
                    'created_at': '2026-06-19T00:00:00Z',
                    'metadata': {
                        'source': 'pricing',
                        'referrerHost': 'google.com',
                    },
                },
                {
                    'event': 'pricing_viewed',
                    'plan': None,
                    'created_at': '2026-06-19T00:00:00Z',
                    'metadata': {
                        'source': 'pricing',
                        'referrerHost': 'github.com',
                    },
                },
                {
                    'event': 'billing_payment_recovery_clicked',
                    'plan': 'manual',
                    'created_at': '2026-06-19T00:00:00Z',
                    'metadata': {
                        'source': 'billing',
                        'billing': 'payment-recovery',
                    },
                },
                {
                    'event': 'billing_account_clicked',
                    'plan': 'pro',
                    'created_at': '2026-06-19T00:00:00Z',
                    'metadata': {
                        'source': 'billing',
                        'state': 'key-recovery',
                    },
                },
                {
                    'event': 'model_catalog_key_recovery_clicked',
                    'plan': 'pro',
                    'created_at': '2026-06-19T00:00:00Z',
                    'metadata': {
                        'source': 'model-catalog',
                        'state': 'model-catalog-returning-user',
                    },
                },
                {
                    'event': 'model_catalog_key_activation_clicked',
                    'plan': 'pro',
                    'created_at': '2026-06-19T00:00:00Z',
                    'metadata': {
                        'source': 'model-catalog',
                        'state': 'model-catalog-hero',
                    },
                },
                {
                    'event': 'pricing_key_activation_clicked',
                    'plan': 'pro',
                    'created_at': '2026-06-19T00:00:00Z',
                    'metadata': {
                        'source': 'pricing',
                        'state': 'pricing-pro',
                    },
                },
                {
                    'event': 'content_article_key_activation_clicked',
                    'plan': 'pro',
                    'created_at': '2026-06-19T00:00:00Z',
                    'metadata': {
                        'source': 'article-dock',
                        'state': 'content-article-dock',
                    },
                },
                {
                    'event': 'fusion_key_activation_clicked',
                    'plan': 'pro',
                    'created_at': '2026-06-19T00:00:00Z',
                    'metadata': {
                        'source': 'fusion',
                        'state': 'fusion-hero',
                    },
                },
                {
                    'event': 'codex_docs_key_activation_clicked',
                    'plan': 'pro',
                    'created_at': '2026-06-19T00:00:00Z',
                    'metadata': {
                        'source': 'codex-docs',
                        'state': 'codex-docs-main',
                    },
                },
                {
                    'event': 'gateway_compare_key_activation_clicked',
                    'plan': 'pro',
                    'created_at': '2026-06-19T00:00:00Z',
                    'metadata': {
                        'source': 'compare-gateways',
                        'state': 'compare-gateways-hero',
                    },
                },
                {
                    'event': 'launch_plan_key_activation_clicked',
                    'plan': 'pro',
                    'created_at': '2026-06-19T00:00:00Z',
                    'metadata': {
                        'source': 'launch-plan',
                        'state': 'launch-plan-hero',
                    },
                },
                {
                    'event': 'status_key_recovery_clicked',
                    'plan': 'pro',
                    'created_at': '2026-06-19T00:00:00Z',
                    'metadata': {
                        'source': 'status',
                        'state': 'status-hero',
                    },
                },
                {
                    'event': 'support_key_recovery_clicked',
                    'plan': 'pro',
                    'created_at': '2026-06-19T00:00:00Z',
                    'metadata': {
                        'source': 'support',
                        'state': 'support-quota-api-keys',
                    },
                },
                {'event': '', 'plan': None, 'created_at': '2026-06-19T00:00:00Z', 'metadata': {}},
            ]

        router.supabase_select = fake_select

        metrics, error = router.read_launch_marketing_funnel_counts(0)

        self.assertIsNone(error)
        self.assertEqual(54, metrics['total'])
        self.assertEqual(1, metrics['events']['landing_account_clicked'])
        self.assertEqual(1, metrics['events']['landing_key_first_direct_clicked'])
        self.assertEqual(1, metrics['events']['landing_key_recovery_clicked'])
        self.assertEqual(1, metrics['events']['content_article_key_recovery_clicked'])
        self.assertEqual(1, metrics['events']['pricing_key_recovery_clicked'])
        self.assertEqual(1, metrics['events']['landing_viewed'])
        self.assertEqual(1, metrics['events']['account_api_key_created'])
        self.assertEqual(1, metrics['events']['account_key_recovery_viewed'])
        self.assertEqual(1, metrics['events']['account_auto_oauth_skipped'])
        self.assertEqual(1, metrics['events']['account_checkout_key_first_redirected'])
        self.assertEqual(1, metrics['events']['account_intent_create_key_clicked'])
        self.assertEqual(1, metrics['events']['login_key_recovery_shown'])
        self.assertEqual(1, metrics['events']['login_key_recovery_landed'])
        self.assertEqual(1, metrics['events']['login_key_recovery_clicked'])
        self.assertEqual(1, metrics['events']['login_key_recovery_same_account_prompted'])
        self.assertEqual(1, metrics['events']['login_key_recovery_session_redirected'])
        self.assertEqual(1, metrics['events']['model_catalog_viewed'])
        self.assertEqual(1, metrics['events']['model_catalog_search_bucketed'])
        self.assertEqual(1, metrics['events']['model_catalog_filter_clicked'])
        self.assertEqual(1, metrics['events']['model_catalog_key_recovery_clicked'])
        self.assertEqual(1, metrics['events']['model_catalog_key_activation_clicked'])
        self.assertEqual(1, metrics['events']['pricing_key_activation_clicked'])
        self.assertEqual(1, metrics['events']['content_article_key_activation_clicked'])
        self.assertEqual(1, metrics['events']['fusion_key_activation_clicked'])
        self.assertEqual(1, metrics['events']['codex_docs_key_activation_clicked'])
        self.assertEqual(1, metrics['events']['gateway_compare_key_activation_clicked'])
        self.assertEqual(1, metrics['events']['launch_plan_key_activation_clicked'])
        self.assertEqual(1, metrics['events']['account_snippet_copied'])
        self.assertEqual(1, metrics['events']['quickstart_snippet_copied'])
        self.assertEqual(1, metrics['events']['operator_no_key_followup_copied'])
        self.assertEqual(3, metrics['events']['operator_no_key_followup_batch_copied'])
        self.assertEqual(1, metrics['events']['operator_no_key_followup_mailto_opened'])
        self.assertEqual(1, metrics['events']['operator_no_key_followup_csv_copied'])
        self.assertEqual(1, metrics['events']['operator_no_key_followup_send_dry_run'])
        self.assertEqual(1, metrics['events']['operator_no_key_followup_sent'])
        self.assertEqual(1, metrics['events']['operator_no_key_followup_send_failed'])
        self.assertEqual(2, metrics['setupSnippetCopies'])
        self.assertEqual(1, metrics['setupSnippetCopiesBySnippet']['codex-cli'])
        self.assertEqual(1, metrics['setupSnippetCopiesBySnippet']['quickstart-curl'])
        self.assertEqual(6, metrics['operatorFollowUpCopies'])
        self.assertEqual(1, metrics['operatorFollowUpWorked'])
        self.assertEqual(1, metrics['operatorFollowUpSendDryRuns'])
        self.assertEqual(2, metrics['operatorFollowUpSendDryRunRecipients'])
        self.assertEqual(1, metrics['operatorFollowUpSends'])
        self.assertEqual(2, metrics['operatorFollowUpSentRecipients'])
        self.assertEqual(1, metrics['operatorFollowUpSendFailures'])
        self.assertEqual(1, metrics['operatorFollowUpSendFailureRecipients'])
        self.assertEqual(10, metrics['keyFirstRedirects'])
        self.assertEqual(1, metrics['keyFirstRedirectsByState']['checkout_key_first'])
        self.assertEqual(1, metrics['keyFirstRedirectsByState']['codex-docs-main'])
        self.assertEqual(1, metrics['keyFirstRedirectsByState']['compare-gateways-hero'])
        self.assertEqual(1, metrics['keyFirstRedirectsByState']['content-article-dock'])
        self.assertEqual(1, metrics['keyFirstRedirectsByState']['fusion-hero'])
        self.assertEqual(1, metrics['keyFirstRedirectsByState']['hero-key-first'])
        self.assertEqual(1, metrics['keyFirstRedirectsByState']['launch-plan-hero'])
        self.assertEqual(1, metrics['keyFirstRedirectsByState']['model-catalog-hero'])
        self.assertEqual(1, metrics['keyFirstRedirectsByState']['pricing-pro'])
        self.assertEqual(1, metrics['keyFirstRedirectsByState']['saved_key_recovery_auto_key'])
        self.assertEqual(12, metrics['keyRecoveryViews'])
        self.assertEqual(1, metrics['keyRecoveryViewsByState']['github'])
        self.assertEqual(1, metrics['keyCreateAttempts'])
        self.assertEqual(1, metrics['keyCreateAttemptsByState']['saved_key_recovery_auto_key'])
        self.assertEqual(1, metrics['keyCreateSuccesses'])
        self.assertEqual(1, metrics['keyCreateSuccessesByState']['created'])
        self.assertEqual(0, metrics['keyCreateFailures'])
        self.assertEqual(1, metrics['keyRecoveryViewsByState']['password_fallback'])
        self.assertEqual(1, metrics['keyRecoveryViewsByState']['login_recovery_cta'])
        self.assertEqual(1, metrics['keyRecoveryViewsByState']['manual_same_email_focus'])
        self.assertEqual(1, metrics['keyRecoveryViewsByState']['key-recovery'])
        self.assertEqual(1, metrics['keyRecoveryViewsByState']['model-catalog-returning-user'])
        self.assertEqual(1, metrics['keyRecoveryViewsByState']['landing-returning-user'])
        self.assertEqual(1, metrics['keyRecoveryViewsByState']['article-returning-user'])
        self.assertEqual(1, metrics['keyRecoveryViewsByState']['pricing_returning_no_key'])
        self.assertEqual(1, metrics['keyRecoveryViewsByState']['status-hero'])
        self.assertEqual(1, metrics['keyRecoveryViewsByState']['support-quota-api-keys'])
        self.assertEqual(1, metrics['keyRecoveryViewsByState']['signed_in_recovery_redirect'])
        self.assertEqual(1, metrics['operatorFollowUpCopiesByKind']['single_copied'])
        self.assertEqual(1, metrics['operatorFollowUpCopiesByKind']['batch_copied'])
        self.assertEqual(1, metrics['operatorFollowUpCopiesByKind']['verified_batch_copied'])
        self.assertEqual(1, metrics['operatorFollowUpCopiesByKind']['verified_csv_copied'])
        self.assertEqual(1, metrics['operatorFollowUpCopiesByKind']['verified_mailto_opened'])
        self.assertEqual(1, metrics['operatorFollowUpCopiesByKind']['verified_marked_worked'])
        self.assertEqual(1, metrics['operatorFollowUpWorkedByKind']['verified_marked_worked'])
        self.assertEqual(1, metrics['operatorFollowUpSendDryRunsByKind']['verified_send_dry_run'])
        self.assertEqual(1, metrics['operatorFollowUpSendsByKind']['verified_sent'])
        self.assertEqual(1, metrics['operatorFollowUpSendFailuresByKind']['unverified_send_failed'])
        self.assertEqual(1, metrics['events']['account_login_submitted'])
        self.assertEqual(2, metrics['events']['auth_provider_state_checked'])
        self.assertEqual(2, metrics['events']['calculator_checkout_clicked'])
        self.assertEqual(1, metrics['events']['calculator_viewed'])
        self.assertEqual(1, metrics['events']['gateway_compare_viewed'])
        self.assertEqual(1, metrics['events']['launch_plan_checkout_clicked'])
        self.assertEqual(1, metrics['events']['launch_plan_viewed'])
        self.assertEqual(1, metrics['events']['pricing_checkout_clicked'])
        self.assertEqual(1, metrics['events']['pricing_viewed'])
        self.assertEqual(1, metrics['events']['billing_payment_recovery_clicked'])
        self.assertEqual(1, metrics['events']['unknown'])
        self.assertEqual(39, metrics['plans']['pro'])
        self.assertEqual(1, metrics['plans']['lite'])
        self.assertEqual(1, metrics['plans']['manual'])
        self.assertEqual(4, metrics['sourceSurfaces']['landing'])
        self.assertEqual(12, metrics['sourceSurfaces']['launch-plan'])
        self.assertEqual(2, metrics['sourceSurfaces']['model-routing-calculator'])
        self.assertEqual(5, metrics['sourceSurfaces']['model-catalog'])
        self.assertEqual(3, metrics['sourceSurfaces']['compare-gateways'])
        self.assertEqual(4, metrics['sourceSurfaces']['pricing'])
        self.assertEqual(7, metrics['sourceSurfaces']['account'])
        self.assertEqual(7, metrics['sourceSurfaces']['login'])
        self.assertEqual(1, metrics['sourceSurfaces']['quickstart'])
        self.assertEqual(0, metrics['sourceSurfaces']['agent-native'])
        self.assertEqual(0, metrics['sourceSurfaces']['integrations'])
        self.assertEqual(2, metrics['sourceSurfaces']['billing'])
        self.assertEqual(1, metrics['sourceSurfaces']['status'])
        self.assertEqual(1, metrics['sourceSurfaces']['support'])
        self.assertEqual(1, metrics['sourceSurfaces']['unknown'])
        self.assertEqual(2, metrics['attributionChannels']['github'])
        self.assertEqual(4, metrics['attributionChannels']['model-gateway'])
        self.assertEqual(2, metrics['attributionChannels']['newsletter'])
        self.assertEqual(2, metrics['attributionChannels']['google'])
        self.assertEqual(1, metrics['attributionChannels']['discord'])
        self.assertEqual(43, metrics['attributionChannels']['direct'])
        self.assertEqual(1, metrics['modelCatalogDemand']['modelFamily']['all'])
        self.assertEqual(1, metrics['modelCatalogDemand']['modelFamily']['ollama'])
        self.assertEqual(1, metrics['modelCatalogDemand']['modelFamily']['openai-codex'])
        self.assertEqual(1, metrics['modelCatalogDemand']['queryBucket']['empty'])
        self.assertEqual(1, metrics['modelCatalogDemand']['queryBucket']['ollama'])
        self.assertEqual(1, metrics['modelCatalogDemand']['queryBucket']['openai-codex'])
        self.assertEqual(2, metrics['authProviderState']['total'])
        self.assertEqual(1, metrics['authProviderState']['loaded'])
        self.assertEqual(1, metrics['authProviderState']['unavailable'])
        self.assertEqual(1, metrics['authProviderState']['githubEnabled'])
        self.assertEqual(1, metrics['authProviderState']['githubDisabled'])
        self.assertEqual(1, metrics['authProviderState']['enabledProviders']['github'])
        self.assertEqual(1, metrics['authProviderState']['enabledProviders']['none'])
        self.assertEqual(1, metrics['authProviderState']['disabledProviders']['github'])
        self.assertEqual(2, metrics['authProviderState']['disabledProviders']['google'])
        actions = router.launch_acquisition_actions(metrics)
        buckets = [row['bucket'] for row in actions]
        self.assertIn('direct', buckets)
        self.assertIn('pro', json.dumps(metrics['plans']))
        self.assertIn('launch-plan', buckets)
        self.assertIn('pricing', buckets)
        self.assertIn('model-catalog', buckets)
        self.assertIn('Tighten pricing CTAs', json.dumps(actions))
        self.assertIn('Turn catalog demand into hosted key activation', json.dumps(actions))
        self.assertIn('Turn launch-plan readers into Pro checkout', json.dumps(actions))
        self.assertEqual('agent-native', router.marketing_source_surface_bucket({'source': 'agent-native'}))
        self.assertEqual('integrations', router.marketing_source_surface_bucket({'source': 'integrations'}))
        self.assertIn('first agent request proof', router.launch_acquisition_action('sourceSurface', 'agent-native'))
        self.assertIn('first routed requests', router.launch_acquisition_action('sourceSurface', 'integrations'))
        # Ensure no raw email values leak into aggregate marketing funnel metrics.
        # State names like 'email_auth_requested' are intentional and allowed.
        metrics_json = json.dumps(metrics)
        self.assertNotIn('buyer@example.com', metrics_json)
        self.assertNotIn('email@example.com', metrics_json)
        self.assertNotIn('"email": "buyer@example.com"', metrics_json)
        self.assertNotIn("'email': 'buyer@example.com'", metrics_json)
        self.assertNotIn('gpt raw text must not appear', json.dumps(metrics))

    def test_launch_marketing_funnel_filters_synthetic_sweeps(self):
        router.SUPABASE_URL = 'https://example.supabase.co'
        router.SUPABASE_SERVICE_ROLE_KEY = 'service'
        old_chrome = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/79.0.3945.79 Safari/537.36'
        sweep_ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/125.0.0.0 Safari/537.36'

        def fake_select(_table, query, timeout=8):
            self.assertIn('source_page', query)
            rows = [{
                'event': 'pricing_viewed',
                'plan': 'pro',
                'created_at': '2026-06-19T00:00:00Z',
                'source_page': 'https://sagerouter.dev/pricing',
                'metadata': {'source': 'pricing', 'user_agent': 'Mozilla/5.0 real buyer'},
            }, {
                'event': 'content_article_snippet_copied',
                'plan': 'pro',
                'created_at': '2026-06-19T00:00:20Z',
                'source_page': 'https://sagerouter.dev/openai-api-router',
                'metadata': {'source': 'article', 'snippet': 'article-hosted-setup', 'user_agent': 'Mozilla/5.0 real buyer'},
            }, {
                'event': 'content_article_viewed',
                'plan': None,
                'created_at': '2026-06-19T00:01:00Z',
                'source_page': 'https://sagerouter.dev/openai-api-router',
                'metadata': {'source': 'article', 'user_agent': old_chrome},
            }]
            for idx in range(8):
                rows.append({
                    'event': 'content_article_viewed',
                    'plan': None,
                    'created_at': f'2026-06-19T00:02:0{idx % 6}Z',
                    'source_page': f'https://sagerouter.dev/article-{idx}',
                    'metadata': {'source': 'article', 'user_agent': sweep_ua},
                })
            return rows

        router.supabase_select = fake_select

        metrics, error = router.read_launch_marketing_funnel_counts(0)

        self.assertIsNone(error)
        self.assertEqual(2, metrics['total'])
        self.assertEqual(9, metrics['filteredSyntheticEvents'])
        self.assertEqual(1, metrics['events']['pricing_viewed'])
        self.assertEqual(1, metrics['events']['content_article_snippet_copied'])
        self.assertNotIn('content_article_viewed', metrics['events'])
        self.assertEqual(1, metrics['setupSnippetCopies'])
        self.assertEqual(1, metrics['setupSnippetCopiesBySnippet']['article-hosted-setup'])
        self.assertEqual(1, metrics['sourceSurfaces']['pricing'])
        self.assertEqual(1, metrics['sourceSurfaces']['article'])

    def test_analytics_funnel_requires_operator_auth_when_hosted_auth_enabled(self):
        router.SUPABASE_AUTH_ENABLED = True
        router.CLIENT_API_KEYS = ['operator-secret']

        class Dummy:
            path = '/analytics/funnel?days=30'

            def __init__(self, authorization=''):
                self.headers = {'Authorization': authorization} if authorization else {}
                self.status = None
                self.payload = None

            def write_json(self, status, payload, extra_headers=None):
                self.status = status
                self.payload = payload

        anonymous = Dummy()
        router.Handler.do_GET(anonymous)
        self.assertEqual(401, anonymous.status)
        self.assertEqual('unauthorized', anonymous.payload['error'])

        operator = Dummy('Bearer operator-secret')
        router.Handler.do_GET(operator)
        self.assertEqual(200, operator.status)
        self.assertIn('stages', operator.payload)
        self.assertIn('privacy', operator.payload)

    def test_legacy_key_still_authorizes(self):
        router.CLIENT_API_KEYS = ['legacy-key']

        class H:
            headers = {'Authorization': 'Bearer legacy-key'}

        self.assertTrue(router.client_request_authorized(H()))

    def test_arbitrary_supabase_jwt_is_not_paid_routing(self):
        router.supabase_user_for_bearer = lambda token: {'id': 'user-1', 'email': 'u@example.com'}

        class H:
            headers = {'Authorization': 'Bearer valid-user-jwt'}

        self.assertFalse(router.client_request_authorized(H()))

    def test_origin_model_listing_requires_paid_or_operator_auth_when_enabled(self):
        class Dummy:
            path = '/v1/models'
            command = 'GET'

            def __init__(self, authorization=''):
                self.headers = {'Authorization': authorization} if authorization else {}
                self.status = None
                self.payload = None
                self.extra_headers = None

            def write_json(self, status, payload, extra_headers=None):
                self.status = status
                self.payload = payload
                self.extra_headers = extra_headers

        anonymous = Dummy()
        router.Handler.do_GET(anonymous)
        self.assertEqual(401, anonymous.status)
        self.assertEqual('unauthorized', anonymous.payload['error'])
        self.assertEqual('https://app.sagerouter.dev/account.html', anonymous.payload['accountUrl'])
        self.assertEqual('https://sagerouter.dev/pricing', anonymous.payload['pricingUrl'])
        self.assertEqual('https://app.sagerouter.dev/status', anonymous.payload['statusUrl'])
        self.assertEqual('https://api.sagerouter.dev/v1', anonymous.payload['openaiBaseUrl'])
        self.assertEqual('sk_sage_', anonymous.payload['apiKeyPrefix'])
        self.assertIn('WWW-Authenticate', anonymous.extra_headers)
        self.assertIn('Sage Router', anonymous.extra_headers['WWW-Authenticate'])
        self.assertIn('rel="account"', anonymous.extra_headers['Link'])

        customer = self.active_customer()
        raw, _row = router.create_api_key_for_customer(customer, 'prod')
        generated = Dummy(f'Bearer {raw}')
        router.Handler.do_GET(generated)
        self.assertEqual(200, generated.status)
        self.assertEqual('list', generated.payload['object'])
        self.assertIn('data', generated.payload)
        self.assertNotIn('models', generated.payload)
        model_ids = {row['id'] for row in generated.payload['data']}
        self.assertIn('sage-router/frontier', model_ids)
        self.assertIn('sage-router/fusion', model_ids)
        self.assertTrue(all(row.get('object') == 'model' for row in generated.payload['data']))

        router.CLIENT_API_KEYS = ['operator-secret']
        operator = Dummy('Bearer operator-secret')
        router.Handler.do_GET(operator)
        self.assertEqual(200, operator.status)
        self.assertEqual('list', operator.payload['object'])
        self.assertIn('data', operator.payload)

    def test_v1beta_model_listing_keeps_google_shape(self):
        customer = self.active_customer()
        raw, _row = router.create_api_key_for_customer(customer, 'prod')

        class Dummy:
            path = '/v1beta/models'
            command = 'GET'
            headers = {'Authorization': f'Bearer {raw}'}
            status = None
            payload = None
            extra_headers = None

            def write_json(self, status, payload, extra_headers=None):
                self.status = status
                self.payload = payload
                self.extra_headers = extra_headers

        handler = Dummy()
        router.Handler.do_GET(handler)
        self.assertEqual(200, handler.status)
        self.assertIn('models', handler.payload)
        self.assertNotIn('data', handler.payload)
        self.assertTrue(all('supportedGenerationMethods' in row for row in handler.payload['models']))

    def test_origin_model_post_auth_error_includes_onboarding_guidance(self):
        body = b'{}'

        class Dummy:
            path = '/v1/chat/completions?cb=smoke'
            command = 'POST'
            headers = {'Content-Length': str(len(body))}
            rfile = BytesIO(body)
            status = None
            payload = None
            extra_headers = None

            def write_json(self, status, payload, extra_headers=None):
                self.status = status
                self.payload = payload
                self.extra_headers = extra_headers

        handler = Dummy()
        router.Handler.do_POST(handler)

        self.assertEqual(401, handler.status)
        self.assertEqual('unauthorized', handler.payload['error'])
        self.assertEqual('https://app.sagerouter.dev/account.html', handler.payload['accountUrl'])
        self.assertEqual('https://sagerouter.dev/pricing', handler.payload['pricingUrl'])
        self.assertEqual('https://api.sagerouter.dev/v1', handler.payload['openaiBaseUrl'])
        self.assertEqual('sk_sage_', handler.payload['apiKeyPrefix'])
        self.assertIn('WWW-Authenticate', handler.extra_headers)
        self.assertIn('rel="pricing"', handler.extra_headers['Link'])

    def test_operator_origin_routes_reject_generated_customer_keys(self):
        customer = self.active_customer()
        raw, _row = router.create_api_key_for_customer(customer, 'prod')
        body = b'{}'

        class Dummy:
            command = 'POST'

            def __init__(self, path, authorization=''):
                self.path = path
                self.headers = {
                    'Authorization': authorization,
                    'Content-Length': str(len(body)),
                }
                self.rfile = BytesIO(body)
                self.status = None
                self.payload = None

            def write_json(self, status, payload, extra_headers=None):
                self.status = status
                self.payload = payload

        for path in (
            '/setup/provider',
            '/setup/codex-auth',
            '/setup/codex-oauth/start',
            '/setup/codex-oauth/poll',
            '/setup/codex-oauth/cancel',
            '/api/restart',
        ):
            with self.subTest(path=path):
                handler = Dummy(path, f'Bearer {raw}')
                router.Handler.do_POST(handler)
                self.assertEqual(401, handler.status)
                self.assertEqual('unauthorized', handler.payload['error'])

        for path in ('/setup/state', '/dashboard', '/admin/blocks', '/admin/clear-blocks', '/discovery'):
            with self.subTest(path=path):
                handler = Dummy(path, f'Bearer {raw}')
                router.Handler.do_GET(handler)
                self.assertEqual(401, handler.status)
                self.assertEqual('unauthorized', handler.payload['error'])


    def test_stripe_signature_requires_current_timestamp(self):
        secret = 'whsec_test'
        router.STRIPE_WEBHOOK_SECRET = secret
        payload = b'{"id":"evt_test"}'
        fresh_ts = str(router.now_epoch())
        fresh_sig = router.hmac.new(secret.encode(), f'{fresh_ts}.{payload.decode()}'.encode(), router.hashlib.sha256).hexdigest()
        self.assertTrue(router.verify_stripe_signature(payload, f't={fresh_ts},v1={fresh_sig}'))

        stale_ts = str(router.now_epoch() - 1000)
        stale_sig = router.hmac.new(secret.encode(), f'{stale_ts}.{payload.decode()}'.encode(), router.hashlib.sha256).hexdigest()
        self.assertFalse(router.verify_stripe_signature(payload, f't={stale_ts},v1={stale_sig}'))
        self.assertFalse(router.verify_stripe_signature(payload, f't=not-a-time,v1={fresh_sig}'))

    def test_stripe_checkout_reuses_existing_customer(self):
        router.STRIPE_SECRET_KEY = 'sk_test'
        router.STRIPE_PRICE_IDS_RAW = 'lite=price_lite,pro=price_pro,max=price_max'
        router.supabase_user_for_bearer = lambda token: {'id': 'user-1', 'email': 'u@example.com'}
        customer = router.customer_for_user({'id': 'user-1', 'email': 'u@example.com'})
        router.update_customer(customer['id'], {'stripe_customer_id': 'cus_existing'})
        captured = {}
        router.stripe_request = lambda path, fields, timeout=10: captured.update({'path': path, 'fields': fields}) or {'id': 'cs_test', 'url': 'https://checkout.test'}

        body = b'{"plan":"pro"}'

        class Dummy:
            path = '/billing/stripe/checkout'
            headers = {'Authorization': 'Bearer valid-user-jwt', 'Content-Length': str(len(body))}
            rfile = BytesIO(body)
            status = None
            payload = None
            def write_json(self, status, payload, extra_headers=None):
                self.status = status
                self.payload = payload

        handler = Dummy()
        router.Handler.do_POST(handler)
        self.assertEqual(200, handler.status)
        self.assertEqual('/v1/checkout/sessions', captured['path'])
        self.assertEqual('cus_existing', captured['fields']['customer'])
        self.assertIsNone(captured['fields']['customer_email'])
        self.assertEqual('price_pro', captured['fields']['line_items[0][price]'])
        self.assertEqual(
            'https://app.sagerouter.dev/account.html?checkout=success&plan=pro&session_id={CHECKOUT_SESSION_ID}',
            captured['fields']['success_url'],
        )
        self.assertEqual(
            'https://app.sagerouter.dev/account.html?checkout=cancel&plan=pro',
            captured['fields']['cancel_url'],
        )

    def test_stripe_checkout_rejects_unknown_plan_before_config_lookup(self):
        router.STRIPE_SECRET_KEY = 'sk_test'
        router.STRIPE_PRICE_IDS_RAW = 'lite=price_lite,pro=price_pro,max=price_max'
        router.supabase_user_for_bearer = lambda token: {'id': 'user-1', 'email': 'u@example.com'}
        router.customer_for_user({'id': 'user-1', 'email': 'u@example.com'})
        called = {'stripe': False}
        router.stripe_request = lambda path, fields, timeout=10: called.update({'stripe': True}) or {}

        body = b'{"plan":"enterprise"}'

        class Dummy:
            path = '/billing/stripe/checkout'
            headers = {'Authorization': 'Bearer valid-user-jwt', 'Content-Length': str(len(body))}
            rfile = BytesIO(body)
            status = None
            payload = None
            def write_json(self, status, payload, extra_headers=None):
                self.status = status
                self.payload = payload

        handler = Dummy()
        router.Handler.do_POST(handler)
        self.assertEqual(400, handler.status)
        self.assertEqual('invalid_plan', handler.payload['error'])
        self.assertEqual('enterprise', handler.payload['plan'])
        self.assertEqual(['lite', 'max', 'pro'], handler.payload['validPlans'])
        self.assertFalse(called['stripe'])

    def test_stripe_billing_portal_uses_existing_customer(self):
        router.STRIPE_SECRET_KEY = 'sk_test'
        router.supabase_user_for_bearer = lambda token: {'id': 'user-1', 'email': 'u@example.com'}
        customer = router.customer_for_user({'id': 'user-1', 'email': 'u@example.com'})
        router.update_customer(customer['id'], {'stripe_customer_id': 'cus_existing'})
        captured = {}
        router.stripe_request = lambda path, fields, timeout=10: captured.update({'path': path, 'fields': fields}) or {'id': 'bps_test', 'url': 'https://billing.test'}

        class Dummy:
            path = '/billing/stripe/portal'
            headers = {'Authorization': 'Bearer valid-user-jwt', 'Content-Length': '2'}
            rfile = BytesIO(b'{}')
            status = None
            payload = None
            def write_json(self, status, payload, extra_headers=None):
                self.status = status
                self.payload = payload

        handler = Dummy()
        router.Handler.do_POST(handler)
        self.assertEqual(200, handler.status)
        self.assertEqual('/v1/billing_portal/sessions', captured['path'])
        self.assertEqual('cus_existing', captured['fields']['customer'])
        self.assertEqual('https://app.sagerouter.dev/account.html?billing=portal', captured['fields']['return_url'])
        self.assertEqual('https://billing.test', handler.payload['portal_url'])

    def test_stripe_billing_portal_requires_existing_customer(self):
        router.STRIPE_SECRET_KEY = 'sk_test'
        router.supabase_user_for_bearer = lambda token: {'id': 'user-1', 'email': 'u@example.com'}

        class Dummy:
            path = '/billing/stripe/portal'
            headers = {'Authorization': 'Bearer valid-user-jwt', 'Content-Length': '2'}
            rfile = BytesIO(b'{}')
            status = None
            payload = None
            def write_json(self, status, payload, extra_headers=None):
                self.status = status
                self.payload = payload

        handler = Dummy()
        router.Handler.do_POST(handler)
        self.assertEqual(409, handler.status)
        self.assertEqual('stripe_customer_missing', handler.payload['error'])

    def test_stripe_webhook_duplicate_event_is_ignored(self):
        router.STRIPE_WEBHOOK_SECRET = 'whsec_test'
        customer = router.customer_for_user({'id': 'user-1', 'email': 'u@example.com'})
        event = {
            'id': 'evt_checkout_1',
            'type': 'checkout.session.completed',
            'data': {
                'object': {
                    'customer': 'cus_1',
                    'subscription': 'sub_1',
                    'payment_status': 'paid',
                    'client_reference_id': customer['id'],
                    'metadata': {'customer_id': customer['id'], 'plan': 'pro'},
                },
            },
        }
        first = self.signed_stripe_webhook_handler(event)
        router.Handler.do_POST(first)
        self.assertEqual(200, first.status)
        self.assertEqual({'received': True, 'event_id': 'evt_checkout_1'}, first.payload)
        updated = router.customer_by_id(customer['id'])
        self.assertEqual('pro', updated['plan'])
        self.assertEqual('active', updated['status'])
        self.assertEqual('cus_1', updated['stripe_customer_id'])
        self.assertEqual(1, len(router.local_customer_store()['payment_intents']))

        second = self.signed_stripe_webhook_handler(event)
        router.Handler.do_POST(second)
        self.assertEqual(200, second.status)
        self.assertTrue(second.payload['duplicate'])
        self.assertEqual('evt_checkout_1', second.payload['event_id'])
        self.assertEqual(1, len(router.local_customer_store()['payment_intents']))

    def test_stripe_checkout_completed_unpaid_does_not_activate_routing(self):
        router.STRIPE_WEBHOOK_SECRET = 'whsec_test'
        customer = router.customer_for_user({'id': 'user-1', 'email': 'u@example.com'})
        router.update_customer(customer['id'], {'plan': 'lite', 'status': 'inactive'})
        raw, _row = router.create_api_key_for_customer(router.customer_by_id(customer['id']), 'prepaid')

        event = {
            'id': 'evt_checkout_unpaid',
            'type': 'checkout.session.completed',
            'data': {
                'object': {
                    'customer': 'cus_unpaid',
                    'subscription': 'sub_unpaid',
                    'payment_status': 'unpaid',
                    'client_reference_id': customer['id'],
                    'metadata': {'customer_id': customer['id'], 'plan': 'max'},
                },
            },
        }

        handler = self.signed_stripe_webhook_handler(event)
        router.Handler.do_POST(handler)

        self.assertEqual(200, handler.status)
        updated = router.customer_by_id(customer['id'])
        self.assertEqual('lite', updated['plan'])
        self.assertEqual('inactive', updated['status'])
        self.assertFalse(router.customer_is_active(updated))
        self.assertIsNone(router.verify_generated_api_key(raw))
        self.assertEqual(1, len(router.local_customer_store()['payment_intents']))

    def test_stripe_subscription_lifecycle_controls_customer_routing_status(self):
        router.STRIPE_WEBHOOK_SECRET = 'whsec_test'
        customer = self.active_customer()
        router.update_customer(customer['id'], {'stripe_customer_id': 'cus_1', 'stripe_subscription_id': 'sub_1'})

        subscription_update = {
            'id': 'evt_sub_past_due',
            'type': 'customer.subscription.updated',
            'data': {
                'object': {
                    'id': 'sub_1',
                    'customer': 'cus_1',
                    'status': 'past_due',
                    'metadata': {'customer_id': customer['id'], 'plan': 'pro'},
                },
            },
        }
        handler = self.signed_stripe_webhook_handler(subscription_update)
        router.Handler.do_POST(handler)
        self.assertEqual(200, handler.status)
        updated = router.customer_by_id(customer['id'])
        self.assertEqual('past_due', updated['status'])
        self.assertFalse(router.customer_is_active(updated))

        subscription_recovered = {
            'id': 'evt_sub_active',
            'type': 'customer.subscription.updated',
            'data': {
                'object': {
                    'id': 'sub_1',
                    'customer': 'cus_1',
                    'status': 'active',
                    'metadata': {'customer_id': customer['id'], 'plan': 'pro'},
                },
            },
        }
        handler = self.signed_stripe_webhook_handler(subscription_recovered)
        router.Handler.do_POST(handler)
        self.assertEqual(200, handler.status)
        updated = router.customer_by_id(customer['id'])
        self.assertEqual('active', updated['status'])
        self.assertTrue(router.customer_is_active(updated))

        subscription_deleted = {
            'id': 'evt_sub_deleted',
            'type': 'customer.subscription.deleted',
            'data': {
                'object': {
                    'id': 'sub_1',
                    'customer': 'cus_1',
                    'metadata': {'customer_id': customer['id']},
                },
            },
        }
        handler = self.signed_stripe_webhook_handler(subscription_deleted)
        router.Handler.do_POST(handler)
        self.assertEqual(200, handler.status)
        updated = router.customer_by_id(customer['id'])
        self.assertEqual('inactive', updated['status'])
        self.assertFalse(router.customer_is_active(updated))

    def test_stripe_subscription_update_derives_plan_from_price_id(self):
        router.STRIPE_WEBHOOK_SECRET = 'whsec_test'
        router.STRIPE_PRICE_IDS_RAW = 'lite=price_lite,pro=price_pro,max=price_max'
        customer = self.active_customer()
        router.update_customer(customer['id'], {
            'plan': 'pro',
            'stripe_customer_id': 'cus_1',
            'stripe_subscription_id': 'sub_1',
        })

        event = {
            'id': 'evt_sub_plan_change',
            'type': 'customer.subscription.updated',
            'data': {
                'object': {
                    'id': 'sub_1',
                    'customer': 'cus_1',
                    'status': 'active',
                    'metadata': {'customer_id': customer['id'], 'plan': 'pro'},
                    'items': {
                        'data': [
                            {'price': {'id': 'price_max'}},
                        ],
                    },
                },
            },
        }

        handler = self.signed_stripe_webhook_handler(event)
        router.Handler.do_POST(handler)
        self.assertEqual(200, handler.status)
        updated = router.customer_by_id(customer['id'])
        self.assertEqual('max', updated['plan'])
        self.assertEqual('active', updated['status'])
        self.assertTrue(router.customer_is_active(updated))
        self.assertEqual(200000, router.account_usage_for_customer(updated)['quota'])

    def test_stripe_subscription_update_preserves_current_plan_without_metadata_or_price(self):
        router.STRIPE_WEBHOOK_SECRET = 'whsec_test'
        customer = self.active_customer()
        router.update_customer(customer['id'], {
            'plan': 'max',
            'stripe_customer_id': 'cus_1',
            'stripe_subscription_id': 'sub_1',
        })

        event = {
            'id': 'evt_sub_no_plan_metadata',
            'type': 'customer.subscription.updated',
            'data': {
                'object': {
                    'id': 'sub_1',
                    'customer': 'cus_1',
                    'status': 'active',
                    'metadata': {'customer_id': customer['id']},
                },
            },
        }

        handler = self.signed_stripe_webhook_handler(event)
        router.Handler.do_POST(handler)
        self.assertEqual(200, handler.status)
        updated = router.customer_by_id(customer['id'])
        self.assertEqual('max', updated['plan'])
        self.assertEqual('active', updated['status'])

    def test_stripe_subscription_update_resolves_existing_customer_without_metadata(self):
        router.STRIPE_WEBHOOK_SECRET = 'whsec_test'
        router.STRIPE_PRICE_IDS_RAW = 'lite=price_lite,pro=price_pro,max=price_max'
        customer = self.active_customer()
        router.update_customer(customer['id'], {
            'plan': 'pro',
            'stripe_customer_id': 'cus_1',
            'stripe_subscription_id': 'sub_1',
        })

        event = {
            'id': 'evt_sub_by_stripe_customer',
            'type': 'customer.subscription.updated',
            'data': {
                'object': {
                    'id': 'sub_1',
                    'customer': 'cus_1',
                    'status': 'active',
                    'items': {'data': [{'price': {'id': 'price_max'}}]},
                },
            },
        }

        handler = self.signed_stripe_webhook_handler(event)
        router.Handler.do_POST(handler)
        self.assertEqual(200, handler.status)
        updated = router.customer_by_id(customer['id'])
        self.assertEqual('max', updated['plan'])
        self.assertEqual('active', updated['status'])

    def test_stripe_webhook_rejects_metadata_customer_mismatch(self):
        router.STRIPE_WEBHOOK_SECRET = 'whsec_test'
        customer_a = self.active_customer()
        router.update_customer(customer_a['id'], {
            'plan': 'pro',
            'stripe_customer_id': 'cus_a',
            'stripe_subscription_id': 'sub_a',
        })
        customer_b = router.customer_for_user({'id': 'user-2', 'email': 'u2@example.com'})
        router.update_customer(customer_b['id'], {
            'plan': 'lite',
            'status': 'active',
            'stripe_customer_id': 'cus_b',
            'stripe_subscription_id': 'sub_b',
        })

        event = {
            'id': 'evt_sub_mismatch',
            'type': 'customer.subscription.updated',
            'data': {
                'object': {
                    'id': 'sub_b',
                    'customer': 'cus_b',
                    'status': 'past_due',
                    'metadata': {'customer_id': customer_a['id'], 'plan': 'max'},
                },
            },
        }

        handler = self.signed_stripe_webhook_handler(event)
        router.Handler.do_POST(handler)
        self.assertEqual(409, handler.status)
        self.assertEqual('stripe_customer_mismatch', handler.payload['error'])
        self.assertEqual('active', router.customer_by_id(customer_a['id'])['status'])
        self.assertEqual('active', router.customer_by_id(customer_b['id'])['status'])
        self.assertEqual(0, len(router.local_customer_store()['payment_intents']))

    def test_crypto_intent_derives_amount_from_selected_plan(self):
        router.SUPABASE_AUTH_ENABLED = True
        router.REQUIRE_VERIFIED_EMAIL = True
        router.CRYPTO_PAYMENT_ADDRESS = 'wallet_123'
        router.supabase_user_for_bearer = lambda token: {
            'id': 'user-verified',
            'email': 'verified@example.com',
            'email_confirmed_at': '2026-06-20T00:00:00Z',
        } if token == 'valid-user-jwt' else None

        body = b'{"plan":"pro","note":"sk-secret customer note should not echo"}'

        class Dummy:
            path = '/billing/crypto/intent'
            headers = {
                'Authorization': 'Bearer valid-user-jwt',
                'Content-Length': str(len(body)),
                'Origin': 'https://app.sagerouter.dev',
            }
            rfile = BytesIO(body)
            status = None
            payload = None

            def write_json(self, status, payload, extra_headers=None):
                self.status = status
                self.payload = payload

        handler = Dummy()
        router.Handler.do_POST(handler)

        self.assertEqual(201, handler.status)
        intent = handler.payload['intent']
        self.assertEqual('30', intent['amount'])
        self.assertEqual('USDC', intent['asset'])
        self.assertEqual('wallet_123', intent['address'])
        self.assertEqual('pro', intent['metadata']['plan'])
        self.assertEqual('public_plan_catalog', intent['metadata']['amount_source'])
        self.assertNotIn('sk-secret customer note', json.dumps(handler.payload))

    def test_crypto_intent_preserves_explicit_amount_override(self):
        router.SUPABASE_AUTH_ENABLED = True
        router.REQUIRE_VERIFIED_EMAIL = True
        router.CRYPTO_PAYMENT_ADDRESS = 'wallet_123'
        router.supabase_user_for_bearer = lambda token: {
            'id': 'user-verified',
            'email': 'verified@example.com',
            'email_confirmed_at': '2026-06-20T00:00:00Z',
        } if token == 'valid-user-jwt' else None

        body = b'{"plan":"lite","amount":"27","asset":"USDC","network":"algorand"}'

        class Dummy:
            path = '/billing/crypto/intent'
            headers = {
                'Authorization': 'Bearer valid-user-jwt',
                'Content-Length': str(len(body)),
                'Origin': 'https://app.sagerouter.dev',
            }
            rfile = BytesIO(body)
            status = None
            payload = None

            def write_json(self, status, payload, extra_headers=None):
                self.status = status
                self.payload = payload

        handler = Dummy()
        router.Handler.do_POST(handler)

        self.assertEqual(201, handler.status)
        intent = handler.payload['intent']
        self.assertEqual('27', intent['amount'])
        self.assertEqual('USDC', intent['asset'])
        self.assertEqual('algorand', intent['network'])
        self.assertEqual('lite', intent['metadata']['plan'])
        self.assertEqual('request', intent['metadata']['amount_source'])

    def test_crypto_status_returns_public_intent_without_customer_note(self):
        router.SUPABASE_AUTH_ENABLED = True
        router.REQUIRE_VERIFIED_EMAIL = True
        router.CRYPTO_PAYMENT_ADDRESS = 'wallet_123'
        router.supabase_user_for_bearer = lambda token: {
            'id': 'user-verified',
            'email': 'verified@example.com',
            'email_confirmed_at': '2026-06-20T00:00:00Z',
        } if token == 'valid-user-jwt' else None

        body = b'{"plan":"max","note":"do not echo this manual settlement note"}'

        class PostDummy:
            path = '/billing/crypto/intent'
            headers = {
                'Authorization': 'Bearer valid-user-jwt',
                'Content-Length': str(len(body)),
                'Origin': 'https://app.sagerouter.dev',
            }
            rfile = BytesIO(body)
            status = None
            payload = None

            def write_json(self, status, payload, extra_headers=None):
                self.status = status
                self.payload = payload

        created = PostDummy()
        router.Handler.do_POST(created)
        self.assertEqual(201, created.status)
        intent_id = created.payload['intent']['id']
        router.update_payment_intent(intent_id, {
            'status': 'settled_manual_review',
            'metadata': {
                **router.payment_intent_by_id(intent_id)['metadata'],
                'approved_at_epoch': 123,
                'settlement_reference': 'tx_123',
            },
        })

        class GetDummy:
            def __init__(self):
                self.path = f'/billing/crypto/status?id={intent_id}'
                self.headers = {'Authorization': 'Bearer valid-user-jwt'}
                self.status = None
                self.payload = None

            def write_json(self, status, payload, extra_headers=None):
                self.status = status
                self.payload = payload

        status = GetDummy()
        router.Handler.do_GET(status)

        self.assertEqual(200, status.status)
        self.assertEqual('settled_manual_review', status.payload['intent']['status'])
        self.assertEqual('max', status.payload['intent']['metadata']['plan'])
        self.assertEqual('tx_123', status.payload['intent']['metadata']['settlement_reference'])
        self.assertNotIn('do not echo this manual settlement note', json.dumps(status.payload))

    def test_crypto_status_without_id_recovers_latest_customer_manual_intent(self):
        router.SUPABASE_AUTH_ENABLED = True
        router.REQUIRE_VERIFIED_EMAIL = True
        router.supabase_user_for_bearer = lambda token: {
            'id': 'user-verified',
            'email': 'verified@example.com',
            'email_confirmed_at': '2026-06-20T00:00:00Z',
        } if token == 'valid-user-jwt' else None
        customer = router.customer_for_user({'id': 'user-verified', 'email': 'verified@example.com'})
        other = router.customer_for_user({'id': 'other-user', 'email': 'other@example.com'})
        router.store_payment_intent({
            'id': 'older-own',
            'kind': 'crypto_manual',
            'customer_id': customer['id'],
            'user_id': customer['user_id'],
            'status': 'pending_manual_review',
            'amount': '6',
            'metadata': {'plan': 'lite', 'note': 'old private note'},
            'created_at_epoch': 10,
        })
        router.store_payment_intent({
            'id': 'latest-own',
            'kind': 'crypto_manual',
            'customer_id': customer['id'],
            'user_id': customer['user_id'],
            'status': 'settled_manual_review',
            'amount': '30',
            'metadata': {'plan': 'pro', 'note': 'latest private note', 'approved_at_epoch': 123},
            'created_at_epoch': 20,
        })
        router.store_payment_intent({
            'id': 'newer-other',
            'kind': 'crypto_manual',
            'customer_id': other['id'],
            'user_id': other['user_id'],
            'status': 'pending_manual_review',
            'amount': '72',
            'metadata': {'plan': 'max', 'note': 'other customer private note'},
            'created_at_epoch': 30,
        })

        class GetDummy:
            path = '/billing/crypto/status'
            headers = {'Authorization': 'Bearer valid-user-jwt'}
            status = None
            payload = None

            def write_json(self, status, payload, extra_headers=None):
                self.status = status
                self.payload = payload

        status = GetDummy()
        router.Handler.do_GET(status)

        self.assertEqual(200, status.status)
        self.assertEqual('latest-own', status.payload['intent']['id'])
        self.assertEqual('settled_manual_review', status.payload['intent']['status'])
        self.assertEqual('pro', status.payload['intent']['metadata']['plan'])
        self.assertNotIn('private note', json.dumps(status.payload))
        self.assertNotIn('newer-other', json.dumps(status.payload))

    def test_operator_can_approve_manual_payment_intent_and_activate_customer(self):
        router.CLIENT_API_KEYS = ['operator-token']
        customer = router.customer_for_user({'id': 'user-1', 'email': 'u@example.com'})
        intent = router.store_payment_intent({
            'kind': 'crypto_manual',
            'customer_id': customer['id'],
            'user_id': customer['user_id'],
            'status': 'pending_manual_review',
            'asset': 'USDC',
            'network': 'base',
            'amount': '72',
            'address': 'wallet_123',
            'metadata': {
                'settlement': 'manual',
                'automatic_settlement': False,
                'plan': 'max',
                'amount_source': 'public_plan_catalog',
                'note': 'customer supplied note stays out of operator response',
            },
        })
        body = b'{"settlementReference":"tx_123","reasonCode":"billing_review","note":"sk-secret-should-not-return"}'

        class Dummy:
            def __init__(self):
                self.path = f'/admin/payment-intents/{intent["id"]}/approve'
                self.headers = {
                    'Authorization': 'Bearer operator-token',
                    'Content-Length': str(len(body)),
                    'Origin': 'https://app.sagerouter.dev',
                }
                self.rfile = BytesIO(body)
                self.status = None
                self.payload = None

            def write_json(self, status, payload, extra_headers=None):
                self.status = status
                self.payload = payload

        handler = Dummy()
        router.Handler.do_POST(handler)

        self.assertEqual(200, handler.status)
        updated = router.customer_by_id(customer['id'])
        self.assertEqual('max', updated['plan'])
        self.assertEqual('active', updated['status'])
        self.assertTrue(router.customer_is_active(updated))
        self.assertEqual('settled_manual_review', handler.payload['intent']['status'])
        self.assertEqual('tx_123', handler.payload['intent']['metadata']['settlement_reference'])
        self.assertEqual('payment_intent.approve', handler.payload['auditEvent']['action'])
        self.assertEqual('billing_review', handler.payload['auditEvent']['reason_code'])
        self.assertEqual('inactive', handler.payload['auditEvent']['status_before'])
        self.assertEqual('active', handler.payload['auditEvent']['status_after'])
        self.assertNotIn('sk-secret', json.dumps(handler.payload))
        self.assertNotIn('customer supplied note', json.dumps(handler.payload))

    def test_operator_manual_payment_approval_respects_suspended_customer(self):
        router.CLIENT_API_KEYS = ['operator-token']
        customer = self.active_customer()
        raw, _row = router.create_api_key_for_customer(customer, 'prod')
        router.suspend_customer_for_operator(customer['id'], reason_code='provider_risk')
        intent = router.store_payment_intent({
            'kind': 'crypto_manual',
            'customer_id': customer['id'],
            'user_id': customer['user_id'],
            'status': 'pending_manual_review',
            'asset': 'USDC',
            'network': 'base',
            'amount': '72',
            'address': 'wallet_123',
            'metadata': {'plan': 'max', 'settlement': 'manual', 'automatic_settlement': False},
        })
        body = b'{}'

        class Dummy:
            def __init__(self):
                self.path = f'/admin/payment-intents/{intent["id"]}/approve'
                self.headers = {
                    'Authorization': 'Bearer operator-token',
                    'Content-Length': str(len(body)),
                    'Origin': 'https://app.sagerouter.dev',
                }
                self.rfile = BytesIO(body)
                self.status = None
                self.payload = None

            def write_json(self, status, payload, extra_headers=None):
                self.status = status
                self.payload = payload

        handler = Dummy()
        router.Handler.do_POST(handler)

        updated = router.customer_by_id(customer['id'])
        self.assertEqual(200, handler.status)
        self.assertEqual('max', updated['plan'])
        self.assertEqual('suspended', updated['status'])
        self.assertFalse(router.customer_is_active(updated))
        self.assertFalse(handler.payload['routingEnabled'])
        self.assertEqual('suspended', handler.payload['auditEvent']['status_before'])
        self.assertEqual('suspended', handler.payload['auditEvent']['status_after'])
        self.assertIsNone(router.verify_generated_api_key(raw))

    def test_operator_manual_payment_approval_rejects_non_manual_intent(self):
        router.CLIENT_API_KEYS = ['operator-token']
        customer = self.active_customer()
        intent = router.store_payment_intent({
            'kind': 'stripe_webhook',
            'customer_id': customer['id'],
            'event_id': 'evt_1',
            'status': 'received',
        })

        class Dummy:
            def __init__(self):
                self.path = f'/admin/payment-intents/{intent["id"]}/approve'
                self.headers = {
                    'Authorization': 'Bearer operator-token',
                    'Content-Length': '2',
                    'Origin': 'https://app.sagerouter.dev',
                }
                self.rfile = BytesIO(b'{}')
                self.status = None
                self.payload = None

            def write_json(self, status, payload, extra_headers=None):
                self.status = status
                self.payload = payload

        handler = Dummy()
        router.Handler.do_POST(handler)

        self.assertEqual(400, handler.status)
        self.assertEqual('invalid_payment_intent_kind', handler.payload['error'])

    def test_operator_manual_payment_approval_rejects_replay_without_duplicate_audit(self):
        router.CLIENT_API_KEYS = ['operator-token']
        customer = router.customer_for_user({'id': 'user-1', 'email': 'u@example.com'})
        intent = router.store_payment_intent({
            'kind': 'crypto_manual',
            'customer_id': customer['id'],
            'user_id': customer['user_id'],
            'status': 'pending_manual_review',
            'asset': 'USDC',
            'network': 'base',
            'amount': '72',
            'address': 'wallet_123',
            'metadata': {'plan': 'max', 'settlement': 'manual', 'automatic_settlement': False},
        })
        body = b'{"settlementReference":"tx_123"}'

        class Dummy:
            def __init__(self):
                self.path = f'/admin/payment-intents/{intent["id"]}/approve'
                self.headers = {
                    'Authorization': 'Bearer operator-token',
                    'Content-Length': str(len(body)),
                    'Origin': 'https://app.sagerouter.dev',
                }
                self.rfile = BytesIO(body)
                self.status = None
                self.payload = None

            def write_json(self, status, payload, extra_headers=None):
                self.status = status
                self.payload = payload

        first = Dummy()
        router.Handler.do_POST(first)
        self.assertEqual(200, first.status)
        self.assertEqual(1, len(router.operator_audit_events_for_customer(customer['id'])))
        approved_intent = router.payment_intent_by_id(intent['id'])
        first_approved_at = approved_intent['metadata']['approved_at_epoch']

        second = Dummy()
        router.Handler.do_POST(second)

        self.assertEqual(409, second.status)
        self.assertEqual('payment_intent_already_settled', second.payload['error'])
        self.assertEqual(1, len(router.operator_audit_events_for_customer(customer['id'])))
        replayed_intent = router.payment_intent_by_id(intent['id'])
        self.assertEqual('settled_manual_review', replayed_intent['status'])
        self.assertEqual(first_approved_at, replayed_intent['metadata']['approved_at_epoch'])

    def test_operator_manual_payment_approval_rejects_non_pending_manual_intent(self):
        router.CLIENT_API_KEYS = ['operator-token']
        customer = self.active_customer()
        intent = router.store_payment_intent({
            'kind': 'crypto_manual',
            'customer_id': customer['id'],
            'user_id': customer['user_id'],
            'status': 'rejected_manual_review',
            'asset': 'USDC',
            'network': 'base',
            'amount': '72',
            'address': 'wallet_123',
            'metadata': {'plan': 'max', 'settlement': 'manual', 'automatic_settlement': False},
        })

        class Dummy:
            def __init__(self):
                self.path = f'/admin/payment-intents/{intent["id"]}/approve'
                self.headers = {
                    'Authorization': 'Bearer operator-token',
                    'Content-Length': '2',
                    'Origin': 'https://app.sagerouter.dev',
                }
                self.rfile = BytesIO(b'{}')
                self.status = None
                self.payload = None

            def write_json(self, status, payload, extra_headers=None):
                self.status = status
                self.payload = payload

        handler = Dummy()
        router.Handler.do_POST(handler)

        self.assertEqual(409, handler.status)
        self.assertEqual('payment_intent_not_pending', handler.payload['error'])
        self.assertEqual(0, len(router.operator_audit_events_for_customer(customer['id'])))
        self.assertEqual('rejected_manual_review', router.payment_intent_by_id(intent['id'])['status'])

    def test_stripe_invoice_payment_failure_disables_generated_key_routing(self):
        router.STRIPE_WEBHOOK_SECRET = 'whsec_test'
        customer = self.active_customer()
        router.update_customer(customer['id'], {'stripe_customer_id': 'cus_1', 'stripe_subscription_id': 'sub_1'})
        raw, _row = router.create_api_key_for_customer(router.customer_by_id(customer['id']), 'prod')
        self.assertIsNotNone(router.verify_generated_api_key(raw))

        event = {
            'id': 'evt_invoice_failed',
            'type': 'invoice.payment_failed',
            'data': {
                'object': {
                    'customer': 'cus_1',
                    'subscription': 'sub_1',
                },
            },
        }
        handler = self.signed_stripe_webhook_handler(event)
        router.Handler.do_POST(handler)
        self.assertEqual(200, handler.status)
        updated = router.customer_by_id(customer['id'])
        self.assertEqual('past_due', updated['status'])
        self.assertFalse(router.customer_is_active(updated))
        self.assertIsNone(router.verify_generated_api_key(raw))

    def test_stripe_invoice_payment_success_recovers_routing_from_invoice_line_price(self):
        router.STRIPE_WEBHOOK_SECRET = 'whsec_test'
        router.STRIPE_PRICE_IDS_RAW = 'lite=price_lite,pro=price_pro,max=price_max'
        customer = self.active_customer()
        router.update_customer(customer['id'], {
            'plan': 'pro',
            'status': 'past_due',
            'stripe_customer_id': 'cus_1',
            'stripe_subscription_id': 'sub_1',
        })
        raw, _row = router.create_api_key_for_customer(router.customer_by_id(customer['id']), 'prod')
        self.assertIsNone(router.verify_generated_api_key(raw))

        event = {
            'id': 'evt_invoice_paid',
            'type': 'invoice.payment_succeeded',
            'data': {
                'object': {
                    'customer': 'cus_1',
                    'subscription': 'sub_1',
                    'lines': {
                        'data': [
                            {'price': {'id': 'price_max'}},
                        ],
                    },
                },
            },
        }

        handler = self.signed_stripe_webhook_handler(event)
        router.Handler.do_POST(handler)
        self.assertEqual(200, handler.status)
        updated = router.customer_by_id(customer['id'])
        self.assertEqual('max', updated['plan'])
        self.assertEqual('active', updated['status'])
        self.assertTrue(router.customer_is_active(updated))
        self.assertIsNotNone(router.verify_generated_api_key(raw))

    def test_stripe_crypto_missing_config_and_options_cors(self):
        router.supabase_user_for_bearer = lambda token: {'id': 'user-1', 'email': 'u@example.com'}

        class Dummy:
            def __init__(self, path, body=b'{}'):
                self.path = path
                self.headers = {'Authorization': 'Bearer valid-user-jwt', 'Content-Length': str(len(body)), 'Origin': 'https://sagerouter.dev'}
                self.rfile = BytesIO(body)
                self.status = None
                self.payload = None
                self.sent_headers = {}
            def send_response(self, status):
                self.status = status
            def send_header(self, key, value):
                self.sent_headers[key] = value
            def end_headers(self):
                pass
            def write_json(self, status, payload, extra_headers=None):
                self.status = status
                self.payload = payload
            send_cors_headers = router.Handler.send_cors_headers

        opt = Dummy('/account/api-keys')
        router.Handler.do_OPTIONS(opt)
        self.assertEqual(204, opt.status)
        self.assertIn('Authorization', opt.sent_headers.get('Access-Control-Allow-Headers'))
        self.assertIn('HEAD', opt.sent_headers.get('Access-Control-Allow-Methods'))

        for path, expected in (
            ('/billing/stripe/checkout', 'stripe_not_configured'),
            ('/billing/stripe/portal', 'stripe_not_configured'),
            ('/billing/crypto/intent', 'crypto_not_configured'),
        ):
            handler = Dummy(path)
            router.Handler.do_POST(handler)
            self.assertEqual(expected, handler.payload['error'])

    def test_head_json_response_sends_headers_without_body(self):
        class Dummy:
            command = 'HEAD'
            headers = {'Origin': 'https://sagerouter.dev'}

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

            send_cors_headers = router.Handler.send_cors_headers

        handler = Dummy()
        router.Handler.write_json(handler, 200, {'status': 'ok'})

        self.assertEqual(200, handler.status)
        self.assertEqual('application/json', handler.sent_headers['Content-Type'])
        self.assertGreater(int(handler.sent_headers['Content-Length']), 0)
        self.assertIn('HEAD', handler.sent_headers['Access-Control-Allow-Methods'])
        self.assertEqual(b'', handler.wfile.getvalue())

    def test_public_launch_metadata_exposes_onboarding_urls(self):
        metadata = router.public_launch_metadata()
        self.assertEqual('https://app.sagerouter.dev', metadata['publicBaseUrl'])
        self.assertEqual('https://sagerouter.dev', metadata['marketingBaseUrl'])
        self.assertEqual('https://app.sagerouter.dev', metadata['appBaseUrl'])
        self.assertEqual('https://api.sagerouter.dev', metadata['apiBaseUrl'])
        self.assertEqual('https://api.sagerouter.dev/v1', metadata['openaiBaseUrl'])
        self.assertEqual('https://api.sagerouter.dev', metadata['anthropicBaseUrl'])
        self.assertEqual('https://app.sagerouter.dev/account.html', metadata['accountUrl'])
        self.assertEqual('https://app.sagerouter.dev/login.html', metadata['loginUrl'])
        self.assertEqual('/billing/stripe/checkout', metadata['checkoutPath'])
        self.assertEqual('/billing/stripe/portal', metadata['billingPortalPath'])
        self.assertEqual('sk_sage_', metadata['apiKeyPrefix'])
        self.assertEqual(5, metadata['maxActiveApiKeysPerCustomer'])

    def test_public_launch_metadata_exposes_secret_free_billing_readiness(self):
        router.STRIPE_SECRET_KEY = 'sk_test'
        router.STRIPE_PRICE_IDS_RAW = 'lite=price_lite,pro=price_pro,max=price_max'
        router.SUPABASE_AUTH_ENABLED = True
        router.REQUIRE_VERIFIED_EMAIL = True
        router.CRYPTO_PAYMENT_ADDRESS = '0xsettlement'

        metadata = router.public_launch_metadata()
        billing = metadata['billing']
        self.assertEqual('/billing/stripe/checkout', billing['stripe']['checkoutPath'])
        self.assertEqual('/billing/stripe/portal', billing['stripe']['billingPortalPath'])
        self.assertTrue(billing['stripe']['configured'])
        self.assertTrue(billing['stripe']['checkoutReady'])
        self.assertTrue(billing['stripe']['billingPortalReady'])
        self.assertEqual(['lite', 'max', 'pro'], billing['stripe']['configuredPlans'])
        self.assertTrue(billing['stripe']['requiresSignedInUser'])
        self.assertTrue(billing['stripe']['requiresVerifiedEmail'])
        self.assertNotIn('price_lite', json.dumps(billing))
        self.assertNotIn('sk_test', json.dumps(billing))
        self.assertTrue(billing['manualSettlement']['enabled'])
        self.assertEqual('/billing/crypto/intent', billing['manualSettlement']['intentPath'])
        self.assertEqual('/billing/crypto/status', billing['manualSettlement']['statusPath'])
        self.assertTrue(billing['manualSettlement']['requiresOperatorApproval'])
        self.assertEqual('sk_sage_', billing['activation']['generatedApiKeyPrefix'])
        self.assertIn('pro', billing['activation']['apiPlans'])

    def test_public_billing_metadata_distinguishes_price_ids_from_checkout_ready(self):
        router.STRIPE_SECRET_KEY = ''
        router.STRIPE_PRICE_IDS_RAW = 'pro=price_pro'

        billing = router.public_billing_metadata()
        self.assertFalse(billing['stripe']['configured'])
        self.assertFalse(billing['stripe']['checkoutReady'])
        self.assertFalse(billing['stripe']['billingPortalReady'])
        self.assertEqual(['pro'], billing['stripe']['configuredPlans'])
        self.assertFalse(billing['manualSettlement']['enabled'])

    def test_public_plan_catalog_exposes_edge_limits(self):
        plans = router.public_plan_catalog()
        self.assertEqual(10000, plans['lite']['limits']['monthlyRequests'])
        self.assertEqual(60, plans['lite']['limits']['rateLimitPerMinute'])
        self.assertEqual(50000, plans['pro']['limits']['monthlyRequests'])
        self.assertEqual(180, plans['pro']['limits']['rateLimitPerMinute'])
        self.assertEqual(200000, plans['max']['limits']['monthlyRequests'])
        self.assertEqual(600, plans['max']['limits']['rateLimitPerMinute'])
        self.assertFalse(plans['free']['apiAccess'])
        self.assertTrue(plans['pro']['apiAccess'])
        self.assertNotIn('fusion', plans['lite']['routingProfiles'])
        self.assertIn('fusion', plans['pro']['routingProfiles'])
        self.assertIn('fusion', plans['max']['routingProfiles'])

    def test_public_plan_catalog_uses_edge_limit_overrides(self):
        router.PUBLIC_PLAN_RATE_LIMITS_RAW = 'lite=7,pro=8,max=9,default=3'
        router.PUBLIC_PLAN_MONTHLY_QUOTAS_RAW = 'lite=70,pro=80,max=90,default=0'
        plans = router.public_plan_catalog()
        self.assertEqual({'monthlyRequests': 70, 'rateLimitPerMinute': 7}, plans['lite']['limits'])
        self.assertEqual({'monthlyRequests': 80, 'rateLimitPerMinute': 8}, plans['pro']['limits'])
        self.assertEqual({'monthlyRequests': 90, 'rateLimitPerMinute': 9}, plans['max']['limits'])

    def test_fusion_rejects_lite_generated_key_plan(self):
        class Dummy:
            def write_json(self, status, payload, extra_headers=None):
                self.status = status
                self.payload = payload
                self.headers = extra_headers or {}

        router.set_route_auth_context({'type': 'generated_key', 'customer': {'id': 'customer_1', 'plan': 'lite'}})
        try:
            handler = Dummy()
            router.handle_sage_router_fusion(
                handler,
                {'model': 'sage-router/fusion', 'messages': [{'role': 'user', 'content': 'Compare these options.'}]},
                'req-fusion-lite',
                router.time.time(),
            )
        finally:
            router.clear_route_auth_context()

        self.assertEqual(402, handler.status)
        self.assertEqual('fusion_plan_required', handler.payload['error']['code'])
        self.assertEqual('lite', handler.payload['error']['plan'])

    def test_fusion_uses_sage_router_product_aliases_only(self):
        self.assertTrue(router.is_sage_router_fusion_request({'model': 'sage-router/fusion'}))
        self.assertFalse(router.is_sage_router_fusion_request({'model': 'openrouter/fusion'}))
        self.assertTrue(router.is_sage_router_fusion_request({'profile': 'fusion'}))

    def test_fusion_server_tool_rejects_lite_generated_key_plan(self):
        class Dummy:
            def write_json(self, status, payload, extra_headers=None):
                self.status = status
                self.payload = payload
                self.headers = extra_headers or {}

        router.set_route_auth_context({'type': 'generated_key', 'customer': {'id': 'customer_1', 'plan': 'lite'}})
        try:
            handler = Dummy()
            router.handle_openai_chat_completions(
                handler,
                {
                    'model': 'sage-router/frontier',
                    'messages': [{'role': 'user', 'content': 'Compare these options.'}],
                    'tools': [{'type': 'sage-router:fusion'}],
                    'tool_choice': 'required',
                },
                'req-fusion-tool-lite',
                router.time.time(),
            )
        finally:
            router.clear_route_auth_context()

        self.assertEqual(402, handler.status)
        self.assertEqual('fusion_plan_required', handler.payload['error']['code'])
        self.assertEqual('lite', handler.payload['error']['plan'])

    def test_fusion_synthesizes_paid_plan_without_logging_panel_content(self):
        original_select = router.select_fusion_panel_chain
        original_run = router.run_fusion_panel_candidate

        class Dummy:
            def routing_headers(self, payload=None, request_id=''):
                return router.Handler.routing_headers(self, payload, request_id)

            def write_json(self, status, payload, extra_headers=None):
                self.status = status
                self.payload = payload
                self.headers = extra_headers or {}

        def fake_select(messages, request_id, thinking, route_mode, requirements, want_json):
            return [('provider-a', 'model-a'), ('provider-b', 'model-b')]

        def fake_run(provider_name, model, payload, request_id, thinking, debug_mode=False):
            if request_id.endswith('-judge'):
                return {
                    'provider': provider_name,
                    'model': model,
                    'ok': True,
                    'elapsedMs': 7,
                    'detail': '',
                    'content': 'fused answer',
                    'usage': {'prompt_tokens': 3, 'completion_tokens': 4, 'total_tokens': 7},
                }
            return {
                'provider': provider_name,
                'model': model,
                'ok': True,
                'elapsedMs': 5,
                'detail': '',
                'content': f'private panel answer from {provider_name}',
                'usage': {'prompt_tokens': 1, 'completion_tokens': 2, 'total_tokens': 3},
            }

        router.select_fusion_panel_chain = fake_select
        router.run_fusion_panel_candidate = fake_run
        router.set_route_auth_context({'type': 'generated_key', 'customer': {'id': 'customer_1', 'plan': 'pro'}})
        try:
            handler = Dummy()
            router.handle_sage_router_fusion(
                handler,
                {'model': 'sage-router/fusion', 'messages': [{'role': 'user', 'content': 'high stakes prompt text'}], 'debug': True},
                'req-fusion-pro',
                router.time.time(),
            )
        finally:
            router.select_fusion_panel_chain = original_select
            router.run_fusion_panel_candidate = original_run
            router.clear_route_auth_context()

        self.assertEqual(200, handler.status)
        self.assertEqual('sage-router/fusion', handler.payload['model'])
        self.assertEqual('fused answer', handler.payload['choices'][0]['message']['content'])
        self.assertEqual('1', handler.headers['X-Sage-Router-Fusion'])
        self.assertEqual(2, handler.payload['sage_router']['fusion']['panelSize'])
        with open(router.ROUTE_EVENTS_PATH) as f:
            event = json.loads(f.read())
        self.assertEqual({'provider': 'sage-router', 'model': 'fusion'}, event['selected'])
        self.assertEqual('pro', event['customer_plan'])
        self.assertNotIn('high stakes prompt text', json.dumps(event))
        self.assertNotIn('private panel answer', json.dumps(event))

    def test_fusion_server_tool_synthesizes_paid_plan(self):
        original_select = router.select_fusion_panel_chain
        original_run = router.run_fusion_panel_candidate

        class Dummy:
            def routing_headers(self, payload=None, request_id=''):
                return router.Handler.routing_headers(self, payload, request_id)

            def write_json(self, status, payload, extra_headers=None):
                self.status = status
                self.payload = payload
                self.headers = extra_headers or {}

        def fake_select(messages, request_id, thinking, route_mode, requirements, want_json):
            return [('provider-a', 'model-a'), ('provider-b', 'model-b')]

        def fake_run(provider_name, model, payload, request_id, thinking, debug_mode=False):
            self.assertNotIn('tools', payload)
            self.assertNotIn('tool_choice', payload)
            if request_id.endswith('-judge'):
                return {
                    'provider': provider_name,
                    'model': model,
                    'ok': True,
                    'elapsedMs': 8,
                    'detail': '',
                    'content': 'server tool fused answer',
                    'usage': {'prompt_tokens': 3, 'completion_tokens': 4, 'total_tokens': 7},
                }
            return {
                'provider': provider_name,
                'model': model,
                'ok': True,
                'elapsedMs': 5,
                'detail': '',
                'content': f'private panel answer from {provider_name}',
                'usage': {'prompt_tokens': 1, 'completion_tokens': 2, 'total_tokens': 3},
            }

        router.select_fusion_panel_chain = fake_select
        router.run_fusion_panel_candidate = fake_run
        router.set_route_auth_context({'type': 'generated_key', 'customer': {'id': 'customer_1', 'plan': 'pro'}})
        try:
            handler = Dummy()
            router.handle_openai_chat_completions(
                handler,
                {
                    'model': 'sage-router/frontier',
                    'messages': [{'role': 'user', 'content': 'Survey the strongest arguments for and against launch sequencing.'}],
                    'tools': [{'type': 'sage-router:fusion', 'parameters': {'analysis_models': ['model-a', 'model-b']}}],
                    'tool_choice': 'required',
                    'debug': True,
                },
                'req-fusion-tool-pro',
                router.time.time(),
            )
        finally:
            router.select_fusion_panel_chain = original_select
            router.run_fusion_panel_candidate = original_run
            router.clear_route_auth_context()

        self.assertEqual(200, handler.status)
        self.assertEqual('sage-router/fusion', handler.payload['model'])
        self.assertEqual('server tool fused answer', handler.payload['choices'][0]['message']['content'])
        self.assertEqual('1', handler.headers['X-Sage-Router-Fusion'])
        with open(router.ROUTE_EVENTS_PATH) as f:
            event = json.loads(f.read())
        self.assertEqual({'provider': 'sage-router', 'model': 'fusion'}, event['selected'])
        self.assertNotIn('private panel answer', json.dumps(event))

    def test_fusion_server_tool_auto_strips_tool_when_not_triggered(self):
        payload = {
            'model': 'sage-router/frontier',
            'messages': [{'role': 'user', 'content': 'Say hello.'}],
            'tools': [{'type': 'sage-router:fusion'}],
        }

        self.assertFalse(router.fusion_server_tool_should_invoke(payload))
        stripped = router.strip_fusion_server_tools_from_payload(payload)
        self.assertNotIn('tools', stripped)
        self.assertNotIn('tool_choice', stripped)
        self.assertEqual('sage-router/frontier', stripped['model'])

    def test_fusion_server_tool_auto_triggers_for_comparison_prompt(self):
        payload = {
            'model': 'sage-router/frontier',
            'messages': [{'role': 'user', 'content': 'Compare the strongest arguments for and against this launch.'}],
            'tools': [{'type': 'sage-router:fusion'}],
        }

        self.assertTrue(router.fusion_server_tool_should_invoke(payload))


class AnalyticsModelConsolidationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self._billing_env = os.environ.get('SAGE_ROUTER_BILLING_ENABLED')
        os.environ['SAGE_ROUTER_BILLING_ENABLED'] = '1'
        self.old = {
            'ROUTE_EVENTS_PATH': router.ROUTE_EVENTS_PATH,
            'FIRESTORE_ENABLED': router.FIRESTORE_ENABLED,
            'SUPABASE_MIRROR_ENABLED': router.SUPABASE_MIRROR_ENABLED,
        }
        router.ROUTE_EVENTS_PATH = os.path.join(self.tmp.name, 'route-events.jsonl')
        router.FIRESTORE_ENABLED = False
        router.SUPABASE_MIRROR_ENABLED = False

    def tearDown(self):
        router.ROUTE_EVENTS_PATH = self.old['ROUTE_EVENTS_PATH']
        router.FIRESTORE_ENABLED = self.old['FIRESTORE_ENABLED']
        router.SUPABASE_MIRROR_ENABLED = self.old['SUPABASE_MIRROR_ENABLED']
        if self._billing_env is None:
            os.environ.pop('SAGE_ROUTER_BILLING_ENABLED', None)
        else:
            os.environ['SAGE_ROUTER_BILLING_ENABLED'] = self._billing_env
        self.tmp.cleanup()

    def test_analytics_consolidates_provider_prefixed_model_chains(self):
        router.append_route_event({
            'request_id': 'r1', 'status': 'ok', 'intent': 'GENERAL',
            'selected': {'provider': 'openrouter', 'model': 'anthropic/claude-sonnet-4.5'},
            'attempts': [{'provider': 'openrouter', 'model': 'anthropic/claude-sonnet-4.5', 'ok': True, 'elapsedMs': 100}],
            'totalElapsedMs': 100,
        })
        router.append_route_event({
            'request_id': 'r2', 'status': 'ok', 'intent': 'GENERAL',
            'selected': {'provider': 'anthropic', 'model': 'claude-sonnet-4.5'},
            'attempts': [{'provider': 'anthropic', 'model': 'claude-sonnet-4.5', 'ok': True, 'elapsedMs': 200}],
            'totalElapsedMs': 200,
        })
        snapshot = router.build_analytics_snapshot(7 * 24 * 3600)
        model_rows = {row['id']: row for row in snapshot['models']}
        self.assertIn('claude-sonnet-4.5', model_rows)
        self.assertEqual(2, model_rows['claude-sonnet-4.5']['requests'])
        self.assertEqual(['anthropic', 'openrouter'], model_rows['claude-sonnet-4.5']['providers'])


if __name__ == '__main__':
    unittest.main()
