# Security — The Python-Specific Foot-Guns

Everything here is a function that looks ordinary and executes attacker input, or a default that is safe for a script and unsafe for a service.

## Deserialization = Code Execution

- `pickle.loads` on data you did not produce is remote code execution by design: `__reduce__` runs during unpickling, before you inspect anything. No "validate then unpickle" exists.
- The same hole, wearing other names: `yaml.load` without `SafeLoader` (use `yaml.safe_load`), `marshal`, `shelve`, `dill`, `joblib.load`, `numpy.load(allow_pickle=True)`, `pandas.read_pickle`, and `torch.load` without `weights_only=True`.
- Cache and IPC formats between YOUR processes may use pickle if the channel is trusted; anything crossing a network or a user boundary uses JSON, msgpack, or protobuf.
- A signed pickle (HMAC over the bytes, `hmac.compare_digest` to verify) is the escape hatch when a format change is impossible — the signature must be verified before `loads`, not after.

## Evaluating Strings

- `eval`/`exec` on user input is unfixable by sandboxing: `().__class__.__mro__` walks from any literal to `object` and back to imports. Restricted globals slow an attacker down and stop nobody.
- Parsing a literal: `ast.literal_eval` (numbers, strings, tuples, lists, dicts, booleans, None — nothing callable). Parsing a config: JSON, TOML (`tomllib`, `python >=3.11`), or YAML-safe.
- Arithmetic from users needs a real parser or an allowlisted AST walk, not `eval` with a regex in front of it.
- `string.Template.substitute` is the safe interpolation primitive when the TEMPLATE itself is untrusted; f-strings and `str.format` expose attributes (`"{x.__class__}"`) and can leak object internals from a user-supplied format string.

## Injection At The Edges

- SQL: parameters, always — `cur.execute("SELECT * FROM t WHERE id = %s", (id,))`. Identifiers (table and column names) cannot be parameterized: validate them against an allowlist you wrote, never interpolate user text.
- Shell: `shell=True` with any interpolated value is command injection (`subprocess.md`).
- Paths: `Path(base) / user_input` escapes the base with `../` or an absolute component. The check:

```python
target = (base / user_input).resolve()
if not target.is_relative_to(base.resolve()):     # python >=3.9
    raise ValueError("path escapes base directory")
```

- Archives: `tarfile.extractall` writes wherever the archive says, including `../../etc/cron.d` (CVE-2007-4559). `python >=3.12` takes `filter="data"`; on older versions validate every member's resolved path first. Also check the uncompressed size — a zip bomb is a few KB that expands to gigabytes.
- XML: `xml.etree` and `minidom` are vulnerable to entity expansion and external entity reads on untrusted input; use `defusedxml`.
- URLs: `urllib.parse.urljoin` with an attacker-controlled second argument can replace the host entirely. Validate the scheme and host against an allowlist before fetching (server-side request forgery).

## Secrets and Randomness

- `random` is a Mersenne Twister: predictable from a handful of outputs, and never acceptable for tokens, passwords, salts, or session ids. `secrets.token_urlsafe(32)` for tokens, `secrets.choice` for picks.
- Compare secrets with `hmac.compare_digest`, not `==`. Short-circuit comparison leaks the length and prefix through timing.
- Passwords need a slow KDF: argon2 (`argon2-cffi`) or bcrypt. Stdlib-only fallback: `hashlib.scrypt`, or `hashlib.pbkdf2_hmac("sha256", ..., 600_000)` — 600k iterations is the OWASP Password Storage recommendation for PBKDF2-HMAC-SHA256. A SHA-256 of a password is not password storage.
- Secrets never live in source, default arguments, or `repr`: dataclass fields holding tokens get `repr=False` (`data-modeling.md`), and log filters redact them (`logging.md`). Everything in `os.environ` is inherited by every child process you spawn (`subprocess.md`).
- `assert user.is_admin` is not an authorization check: `python -O` removes every assert (`testing.md`). Raise explicitly.

## TLS and Network

- `verify=False` in requests, or `ssl._create_unverified_context()`, disables authentication of the peer entirely — a corporate proxy error is fixed by installing the CA (`REQUESTS_CA_BUNDLE`, `SSL_CERT_FILE`, or `certifi`), not by turning off verification.
- `ssl.create_default_context()` is the correct starting point (verification and hostname checking on). `ssl.wrap_socket` was removed in `python >=3.12`.
- Set a timeout on every outbound call or a slow server becomes your outage (`errors.md`).
- Cloud metadata endpoints (169.254.169.254) are reachable from most runtimes: an SSRF in a service becomes credential theft. Validate outbound hosts.

## Temp Files and Filesystem

- `tempfile.mkstemp`/`NamedTemporaryFile`, never a hand-built `/tmp/app-<pid>` path — predictable names in a world-writable directory are a symlink race.
- Create secrets with restrictive permissions from the start: `os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)`. Chmod after writing leaves a window.
- `shutil.rmtree` follows into directories you may not intend; `os.walk(followlinks=False)` is the default for a reason — keep it.

## Supply Chain

- `pip install` runs arbitrary code from an sdist's build step. Prefer wheels (`--only-binary :all:` where the tree allows it), pin with hashes (`--require-hashes`, `packaging.md`), and review new transitive dependencies the way you review code.
- `--extra-index-url` lets a public package with a higher version number shadow your internal one — the dependency-confusion attack (`packaging.md`).
- Typosquatting is a name-similarity attack: `requsts`, `python-dateutil` vs `dateutil`. Copy names from the project's own docs, not from memory or a model's suggestion.
- Run `pip-audit` (or an equivalent) in CI, and again on a schedule — a CVE published after your last build affects the artifact already in production.

## Framework Defaults Worth Checking

- Debug mode off in production: the Werkzeug/Flask debugger exposes an interactive console (remote code execution) and Django's `DEBUG=True` leaks settings and stack frames. Framework specifics: the `flask` and `django` skills (https://clawic.com/skills/flask, https://clawic.com/skills/django).
- Binding a dev server to `0.0.0.0` publishes it beyond localhost; `http.server` has no authentication and no rate limit and is not a deployment target.
