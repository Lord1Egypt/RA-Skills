"""Tests for PII regex patterns."""

from repro_pack.redactor.patterns import PATTERNS, mask_snippet


class TestPatterns:
    """Verify each PII pattern matches expected inputs."""

    def _match(self, pii_type: str, text: str) -> bool:
        for name, pattern, _ in PATTERNS:
            if name == pii_type and pattern.search(text):
                return True
        return False

    def test_email_match(self):
        assert self._match("email", "contact: user@example.com for details")
        assert self._match("email", "send to test.user+tag@company.co.uk")

    def test_email_no_false_positive(self):
        assert not self._match("email", "this is not an email")

    def test_phone_us(self):
        assert self._match("phone", "call +1-415-555-0198")
        assert self._match("phone", "phone: (415) 555-0198")

    def test_phone_china(self):
        assert self._match("phone", "手机号 13812345678")
        assert self._match("phone", "+86 13900139000")

    def test_ip_v4(self):
        assert self._match("ip_address", "from 192.168.1.100")
        assert self._match("ip_address", "server at 10.0.0.1")

    def test_aws_key(self):
        assert self._match("aws_key", "key: AKIAFAKEKEY00EXAMPLE")

    def test_jwt(self):
        assert self._match(
            "jwt",
            "token eyJhbGciOiAibm9uZSJ9.eyJzdWIiOiAiZmFrZSIsICJkZW1vIjogdHJ1ZX0.fakesignature00000",
        )

    def test_bearer_token(self):
        assert self._match("auth_token", "Authorization: Bearer abc123def456ghi789jkl")

    def test_api_key(self):
        assert self._match("api_key", "api_key=sk-abc123def456ghi789")
        assert self._match("api_key", "API_SECRET: mysecretkey1234567890")

    def test_credit_card_visa(self):
        assert self._match("credit_card", "card: 4111111111111111")

    def test_credit_card_mc(self):
        assert self._match("credit_card", "payment with 5500000000000004")

    def test_ssn(self):
        assert self._match("ssn", "SSN: 123-45-6789")

    def test_china_id_card(self):
        assert self._match("id_card", "身份证号 110105199003071234")

    def test_uuid(self):
        assert self._match("uuid", "request_id: 550e8400-e29b-41d4-a716-446655440000")

    def test_password(self):
        assert self._match("password", "password=SuperSecret123!")
        assert self._match("password", "pwd: mypass123")

    def test_cookie(self):
        assert self._match("cookie", "Cookie: session=abc123; user_id=12345")

    def test_url_with_credentials(self):
        assert self._match("url_with_credentials", "db://admin:password@host:5432/db")

    def test_private_key(self):
        assert self._match("private_key", "-----BEGIN RSA PRIVATE KEY-----")


class TestMaskSnippet:
    def test_short_string(self):
        assert mask_snippet("ab") == "**"

    def test_normal_string(self):
        result = mask_snippet("user@example.com")
        assert result.startswith("use")
        assert "*" in result

    def test_custom_visible(self):
        result = mask_snippet("secret", max_visible=1)
        assert result[0] == "s"
        assert result[1] == "*"
