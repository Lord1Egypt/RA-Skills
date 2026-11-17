import unittest

from sluice.core import scan
from sluice.detectors import shannon_entropy


def names(text):
    return {f.detector for f in scan(text)}


class TestHighSeverityDetectors(unittest.TestCase):
    def test_anthropic_key(self):
        t = "key is sk-ant-api03-" + "A1b2C3d4" * 6 + " ok"
        self.assertIn("anthropic_key", names(t))

    def test_openrouter_key(self):
        t = "sk-or-v1-" + "a1b2c3d4" * 8
        self.assertIn("openrouter_key", names(t))

    def test_openai_key_not_confused_with_anthropic(self):
        # an sk-ant key must NOT also register as a generic openai_key
        t = "sk-ant-api03-" + "A1b2C3d4" * 6
        n = names(t)
        self.assertIn("anthropic_key", n)
        self.assertNotIn("openai_key", n)

    def test_openai_plain_key(self):
        t = "OPENAI=sk-" + "A1b2C3d4e5" * 4
        self.assertIn("openai_key", names(t))

    def test_gitlab_pat(self):
        self.assertIn("gitlab_pat", names("REDACTED-SECRET"))

    def test_github_pat(self):
        self.assertIn("github_pat", names("ghp_" + "A1b2C3d4e5" * 4))

    def test_aws_access_key(self):
        self.assertIn("aws_access_key", names("REDACTED-SECRET"))

    def test_slack_token(self):
        self.assertIn("slack_token", names("REDACTED-SECRET"))

    def test_stripe_secret(self):
        self.assertIn("stripe_secret", names("sk_live_" + "a1B2c3D4" * 4))

    def test_telegram_bot_token(self):
        # shape: <digits>:<35 chars>
        tok = "8766746046:" + "A" * 35
        self.assertIn("telegram_bot_token", names(tok))

    def test_jwt(self):
        jwt = "eyJhbGciOiJ.eyJzdWIiOiIxMjM0.SflKxwRJSMeK"
        self.assertIn("jwt", names(jwt))

    def test_private_key_block(self):
        self.assertIn(
            "private_key_block",
            names("-----BEGIN OPENSSH PRIVATE KEY-----\nstuff"),
        )


class TestMediumLowDetectors(unittest.TestCase):
    def test_generic_secret_assignment_high_entropy(self):
        t = "password = " + "xK9mP2qR7tL4wZ8v"
        self.assertIn("generic_secret_assignment", names(t))

    def test_generic_assignment_ignores_low_entropy_prose(self):
        # "the next one" / a word is not a secret
        t = "password: thenextoneplease"
        self.assertNotIn("generic_secret_assignment", names(t))

    def test_private_path(self):
        self.assertIn(
            "private_path", names("see /home/workloft/secrets/x-account.txt")
        )

    def test_private_ip(self):
        self.assertIn("private_ip", names("ssh to 10.0.0.1 now"))


class TestEntropy(unittest.TestCase):
    def test_random_string_high(self):
        self.assertGreater(shannon_entropy("xK9mP2qR7tL4wZ8vB3nQ"), 3.2)

    def test_english_word_low(self):
        self.assertLess(shannon_entropy("thenextoneplease"), 3.2)

    def test_empty(self):
        self.assertEqual(shannon_entropy(""), 0.0)


if __name__ == "__main__":
    unittest.main()
