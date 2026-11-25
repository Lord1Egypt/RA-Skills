# Offline security regressions

Requires Python 3 (standard library only), Bash 3.2+, jq 1.6+, Node.js and ordinary shell utilities. No dependency installation or credentials are needed. From the repository root, use an existing writable scratch directory:

```bash
python3 tests/test_security.py --scratch /path/to/scratch -v
```

Temporary fixtures are created only under `--scratch` and removed afterward. The harness constructs a private HOME/PATH and a minimal environment with a synthetic API key. It runs real scripts/encoders/parsers; curl and DNS tools record argv/stdin locally and never connect. No SQL/database behavior is involved. Do not replace these recording transports with real network clients.

For baseline proof, export the known commit to a new empty directory in scratch, then run the candidate's tests against that export:

```bash
mkdir /path/to/scratch/sendgrid-baseline
git archive 6d6b44b27d634544a5049f823f906a8992a1802c | tar -x -C /path/to/scratch/sendgrid-baseline
python3 tests/test_security.py --scratch /path/to/scratch \
  --root /path/to/scratch/sendgrid-baseline -v \
  HelperTests.test_test_email_values_remain_data \
  HelperTests.test_json_structure_cannot_add_recipients \
  HelperTests.test_webhook_arguments_are_rejected_before_any_network
```

Those baseline tests are expected to fail; the corrected tree must pass. One URL argument and an empty second argument exercise the removed-capability boundary. Neither case tests URL/IP classification, DNS rebinding or connection pinning; no webhook target is resolved or connected to.

The suite also executes the actual curl documentation blocks against the recorder, including standalone outbound references without sibling scripts, and checks exact argv/data. Parser tests characterize a local data/code boundary, not production multipart fidelity. It intentionally remains a lossy diagnostic parser. Human-facing approval/privacy prose is reviewed as guidance, not claimed as a runtime permission gate or agent-behavior guarantee.

Send tests cover both helpers and self-contained Bash curl examples: stdin JSON,
config-descriptor authentication, key-injection rejection, HTTP/transport failures,
no retry/redirect, explicit proxy bypass, and connect/total timeout arguments. A jq
wrapper records argv before executing the real encoder; a large approved HTML
fixture checks that its content never becomes a process argument. This is not a
claim of privacy from the invoking shell, environment, output logs or other local
processes. Curl/DNS policy is asserted at the recording boundary, not by connecting
to any service.

HTML file tests use the host's real `realpath`, including native macOS, with synthetic
files only: bare/relative/absolute paths, spaces and leading dashes, missing files,
directories, traversal, explicit `--file`/`--html`, and allowed/rejected symlink
suffixes. They do not establish a privacy sandbox or eliminate filesystem races.
Mode tests reject standalone `--dry-run` and `--unknown` before transport, retain
four-argument unknown-option rejection, and preserve `--html '--dry-run'` as literal content.
MX tests cover both dig and nslookup fixtures, exact normalized exchange fields,
lookalikes/malformed answers and lookup failures. Line-ending tests preserve the
plain part and render CRLF, LF and CR as HTML breaks after escaping.

Select the exact installed runtimes when checking version-specific behavior:

```bash
python3 tests/test_security.py --scratch /path/to/scratch --bash /bin/bash --jq /usr/bin/jq -v
# If Homebrew jq is already installed, repeat with --jq /opt/homebrew/bin/jq.
```

The harness reports the selected binary paths and versions. UTF-8 fixtures check
accented, BMP and astral characters at byte offsets 4092–4100 in recipient, sender,
subject and body fields in both helpers, plus long single-line HTML files larger
than a process argument limit. Exact recorded payloads and encoder/transport argv
are checked; no decoder receives payload data on argv. Encoder partial-output and
real descriptor-read failures must stop before transport and preserve exit status.
Unrelated stdin (including NUL) must not enter the JSON. Shell arguments themselves
cannot contain NUL. Missing uppercase/mixed-case HTML filenames are rejected while
explicit `--html` literals, markup and non-HTML prose retain their existing behavior.
