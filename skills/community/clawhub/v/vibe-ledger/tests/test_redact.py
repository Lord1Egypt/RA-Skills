import base64
import json

import redact

# Built by concatenation so this file never contains a contiguous secret.
OPENAI = "sk-proj-" + "Ab3dE5fG7hJ9kL1mN3pQ5rS7tU9vW1xY"
ANTHROPIC = "sk-ant-api03-" + "Zz9Yy8Xx7Ww6Vv5Uu4Tt3Ss2Rr1Qq0Pp"
STRIPE = "sk_live_" + "51Hq8kLmNoPqRsTuVwXy"
AWS = "AKIA" + "IOSFODNN7EXAMPLE"


def jwt(payload: dict) -> str:
    enc = lambda d: base64.urlsafe_b64encode(json.dumps(d).encode()).decode().rstrip("=")
    return enc({"alg": "HS256", "typ": "JWT"}) + "." + enc(payload) + "." + "s1gnatureS1gnature"


def test_prefixed_secrets_are_masked_keeping_prefix_and_last4():
    for secret, prefix in ((OPENAI, "sk-proj-"), (ANTHROPIC, "sk-ant-"), (STRIPE, "sk_live_"), (AWS, "AKIA")):
        out = redact.redact(f"key is {secret} ok")
        assert secret not in out
        assert f"{prefix}…{secret[-4:]}" in out


def test_jwt_is_masked():
    token = jwt({"role": "service_role"})
    out = redact.redact(f"SUPABASE={token}")
    assert token not in out and "eyJ…" in out


def test_high_entropy_assignment_is_masked_low_entropy_is_not():
    assert "q8Zr2Lx9Vb4Nm7Kp3Wd6Ty1" not in redact.redact('API_TOKEN="q8Zr2Lx9Vb4Nm7Kp3Wd6Ty1"')
    plain = "PASSWORD_HINT=aaaaaaaaaaaaaaaaaaaaaaaa"
    assert redact.redact(plain) == plain


def test_private_key_block_is_replaced():
    block = "-----BEGIN RSA " + "PRIVATE KEY-----\nMIIBOgIBAAJBAKj34GkxFhD90vcNLYLInFEX6Ppy1tPf9Cnzj4p4WGeKLs1Pt8Qu\n-----END RSA " + "PRIVATE KEY-----"  # built in pieces: no key-shaped literal in the repo
    assert redact.redact(block) == "[PRIVATE KEY REDACTED]"


def test_masking_is_idempotent_and_leaves_nothing_detectable():
    text = f"{OPENAI} {ANTHROPIC} {STRIPE} {AWS} {jwt({'role': 'anon'})} API_TOKEN=q8Zr2Lx9Vb4Nm7Kp3Wd6Ty1"
    once = redact.redact(text)
    assert redact.redact(once) == once
    assert redact.find_secrets(once) == []
    assert len(redact.find_secrets(text)) >= 6


def test_prose_is_untouched():
    s = "skip the sk- prefix discussion; AKIA alone is fine"
    assert redact.redact(s) == s


def test_entropy():
    assert redact.shannon_entropy("") == 0.0
    assert redact.shannon_entropy("aaaa") == 0.0
    assert redact.shannon_entropy("abcd") == 2.0


def test_references_to_env_var_names_are_not_masked():
    for code in ("apiKey: process.env.OPENAI_API_KEY",
                 "const key = import.meta.env.VITE_OPENAI_API_KEY",
                 "api_key = os.environ.OPENAI_API_KEY_VALUE",
                 'SECRET_NAME = "STRIPE_SECRET_KEY_LIVE"'):
        assert redact.redact(code) == code, code
        assert redact.find_secrets(code) == [], code


PW = "Zq8vK2!mXp9@Lr4#Tn6$Wb3"
DISCORD = "MTA5NjM4NzQ1Njc4OTAxMjM0NQ" + ".GaBcDe." + "xYz0aBcDeFgHiJkLmNoPqRsTuVwXyZ01"
GOOGLE = "AIza" + "SyD3x9Kq2Lm8Np4Rs7Tv1Wx5Yz0AbCdEfGh"
WHSEC = "whsec_" + "Mz8kQ2vL9xP4rT7wB1nC5yH0"
BEARER = "eyJhbGciOiJIUzI1NiJ9abc" + "Zq8vK2mXp9Lr4Tn6"


def test_common_secret_shapes_are_masked():
    cases = [f'{{"password": "{PW}"}}', f"{{'api_key': '{PW}'}}", f'password = "{PW}"',
             f"DATABASE_URL=postgresql://postgres:{PW}@db.example.supabase.co:5432/postgres",
             f"DISCORD_TOKEN={DISCORD}", f"const firebaseKey = '{GOOGLE}'", f"STRIPE_WEBHOOK={WHSEC}",
             f"Authorization: Bearer {BEARER}"]
    for text in cases:
        out = redact.redact(text)
        for secret in (PW, DISCORD, GOOGLE, WHSEC, BEARER):
            assert secret not in out, (text, out)
        assert redact.redact(out) == out
        assert redact.find_secrets(out) == [], out


def test_ordinary_words_ending_in_sk_or_pk_are_not_secrets():
    for text in ("src/taREDACTED-SECRET.tsx", 'className="taREDACTED-SECRET"',
                 "riREDACTED-SECRET.ts", "deREDACTED-SECRET"):
        assert redact.redact(text) == text
        assert redact.find_secrets(text) == []
