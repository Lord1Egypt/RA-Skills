#!/usr/bin/env python3
"""
One OpenAI-compatible chat endpoint, and how this installation finds it.

**One wire format, not one client per vendor.** `POST {base_url}/chat/completions`
with `{model, messages, temperature, max_tokens}` is spoken by llama.cpp's
`llama-server`, Ollama (on its `/v1/` prefix), LM Studio, vLLM, and OpenRouter.
A provider abstraction with a branch per vendor buys nothing here and costs a
place for the four branches to drift: the only thing that actually varies
between a Raspberry Pi running a 1.7B and a hosted frontier model is the URL,
the model name, and whether a key is needed.

**Stdlib only.** `urllib.request`, no `openai` package and no `requests`. The
whole engine runs on a bare checkout with nothing installed and the tests prove
it, so the module that reaches the network is the last place to break that.

Three things this refuses to do, each of which is a real failure somebody would
otherwise ship:

  1. **Read an API key out of the config file.** `.rabbit-model` sits in a
     repository beside `.rabbit-voice` and gets committed. The file names an
     environment variable (`api_key_env`) and never holds a secret, and a file
     carrying a literal `api_key` is rejected with the reason rather than
     quietly honoured. A convenience that leaks a key once is not a convenience.
  2. **Send a document in plaintext to somewhere that is not this machine.**
     `http://` is allowed to loopback, where it is the normal local-server case,
     and refused to any other host unless the config says `allow_insecure`.
     The payload is the user's unpublished draft.
  3. **Put a key in a message a human or a log will see.** Every error here is
     built from the status, the URL host, and the server's own text, and
     `_scrub` runs over that text on the way out, because an OpenAI-compatible
     server that rejects a key sometimes echoes a prefix of it back.

`resolve` deliberately mirrors `voices.resolve`: nearest config wins, the note
says which file decided, and nothing is configured by default. There is no
"try localhost:11434 and see" fallback. A tool that silently discovers a model
server is a tool that silently ships somebody's draft to whatever is listening
on that port.

Stdlib only, 3.9+.
"""

import json
import os
import re
import urllib.error
import urllib.request

CONFIG_NAME = ".rabbit-model"

# The env fallback, for CI and for a shell that does not want a file.
ENV_BASE_URL = "RABBIT_MODEL_BASE_URL"
ENV_MODEL = "RABBIT_MODEL_NAME"
ENV_API_KEY = "RABBIT_MODEL_API_KEY"

# Defaults chosen for the smallest box this is meant to run on. 4096 is the
# context a 1.7B at Q4_K_M holds comfortably on a Pi, and the planner in
# rewrite.py sizes its units against it rather than against a desktop's 32k.
DEFAULT_CONTEXT_TOKENS = 4096
DEFAULT_MAX_OUTPUT_TOKENS = 640
DEFAULT_TEMPERATURE = 0.2
DEFAULT_TIMEOUT = 120

# Every key a config file may carry. Anything else is a typo, and a typo in a
# config that silently does nothing is the failure mode this whole module is
# written against: `max_output_tokens` misspelled means every long rewrite comes
# back truncated and the gate rejects it, with nothing anywhere saying why.
CONFIG_KEYS = frozenset((
    "base_url", "model", "api_key_env", "context_tokens", "max_output_tokens",
    "temperature", "timeout", "allow_insecure", "disable_thinking",
))

# Ask the model not to think out loud. On by default, and this is not a tuning
# preference: measured against Qwen3.5-0.8B on llama-server, thinking left on
# scored 0 accepted out of 15 passages, every one of them rejected because the
# model spent all 640 output tokens on a reasoning block and returned empty
# `content`. Off, the same model answers in 42 tokens. Most current small models
# are hybrid reasoning models, so a rewriter that does not send these fails on
# exactly the class of model it exists to use.
#
# Two spellings because there is no one spelling. llama.cpp reads
# `chat_template_kwargs`, OpenAI-compatible hosted endpoints read
# `reasoning_effort`, and each ignores the other. A server that rejects both as
# unknown fields is handled by the one-time downgrade in `complete`.
THINKING_OFF = {
    "chat_template_kwargs": {"enable_thinking": False},
    "reasoning_effort": "none",
}

LOOPBACK_HOSTS = frozenset(("localhost", "127.0.0.1", "::1", "[::1]", "0.0.0.0"))

# A key echoed back by a server that rejected it. Both common shapes, plus a
# bare long token, and the replacement keeps the prefix so the message can still
# say which key it was without saying what it is.
_KEY_RX = re.compile(r"\b(sk-[A-Za-z0-9_\-]{4})[A-Za-z0-9_\-]{8,}")
_BEARER_RX = re.compile(r"(?i)\b(bearer\s+)\S{8,}")


class EndpointError(Exception):
    """Anything that stopped a completion from coming back.

    One exception type on purpose. Every caller does the same thing with it
    (report it and leave the document alone), and a hierarchy would invite a
    caller to retry the one case that must not be retried.
    """


class _FieldsRejected(EndpointError):
    """A 400 on a request carrying the thinking-off fields.

    Private, and never raised past `complete`, which downgrades and retries.
    A caller must not be able to distinguish "this server wants plain OpenAI
    fields" from a successful call, because it is not a fact about the document.
    """


class Truncated(EndpointError):
    """The server stopped at max_tokens. The partial text is discarded.

    Named separately because it is the one failure a caller may usefully retry
    with a smaller unit, and because a partial rewrite is worse than no rewrite:
    it verifies clean against every preservation rule right up to the point it
    stops.
    """


import urllib.parse


def _scrub(text, secret=None):
    """Strip key shapes and URL credentials from server output, plus `secret` itself when given.

    The regexes only know the common shapes, and a server that echoes an
    Anthropic-, HF-, or custom-shaped key back in an error body matches
    neither. The exact key cannot false-positive, so callers that hold one
    pass it in.
    """
    text = _KEY_RX.sub(r"\1...", text or "")
    text = _BEARER_RX.sub(r"\1...", text)
    text = re.sub(r"(https?://[^:/@]+:)[^@]+(@)", r"\1...\2", text)
    if secret and len(secret) >= 8:
        text = text.replace(secret, secret[:4] + "...")
    return text


def _host_of(url):
    try:
        parsed = urllib.parse.urlsplit(url or "")
        scheme = parsed.scheme.lower() if parsed.scheme else None
        if not parsed.netloc and not parsed.scheme:
            return (None, None)
        hostname = parsed.hostname.lower() if parsed.hostname else None
        if hostname and ":" in hostname:
            hostname = f"[{hostname}]"
        return (scheme, hostname)
    except Exception:
        return (None, None)


def estimate_tokens(text):
    """A deliberately pessimistic token count for `text`.

    Characters over three, not the usual four. The error is asymmetric and only
    one direction is cheap: overestimating costs a smaller unit and one more
    round trip, and underestimating costs a truncated completion that the gate
    then rejects, which is a wasted call plus a rewrite nobody gets. Markdown
    also tokenizes worse than prose does, because punctuation and file paths
    fragment, and the units this measures are markdown.

    This is a budget, not a tokenizer. Nothing downstream may treat it as an
    exact count, which is why it is not named `count_tokens`.
    """
    return (len(text or "") + 2) // 3


class Endpoint:
    """Where the model is, and what it costs to ask it something."""

    def __init__(self, base_url, model, api_key=None,
                 context_tokens=DEFAULT_CONTEXT_TOKENS,
                 max_output_tokens=DEFAULT_MAX_OUTPUT_TOKENS,
                 temperature=DEFAULT_TEMPERATURE, timeout=DEFAULT_TIMEOUT,
                 allow_insecure=False, disable_thinking=True, source=None):
        self.base_url = (base_url or "").rstrip("/")
        self.model = model
        self.api_key = api_key
        self.context_tokens = int(context_tokens)
        self.max_output_tokens = int(max_output_tokens)
        self.temperature = float(temperature)
        self.timeout = int(timeout)
        self.allow_insecure = bool(allow_insecure)
        self.disable_thinking = bool(disable_thinking)
        # Set once, when a server rejects the thinking-off fields as unknown.
        # Sticky, so one 400 is the whole cost of finding out rather than one
        # per passage.
        self._thinking_fields_rejected = False
        # Which file or env var decided this, for the report. Never the key.
        self.source = source
        self._check_transport()

    def _check_transport(self):
        scheme, host = _host_of(self.base_url)
        if scheme is None:
            raise EndpointError(
                "base_url must start with http:// or https://, got %r"
                % (self.base_url or "",))
        if scheme == "http" and host not in LOOPBACK_HOSTS and not self.allow_insecure:
            # The CLI has no spelling for allow_insecure, so pointing a
            # --model-endpoint user at "set it in --model-endpoint" is an
            # instruction nobody can follow.
            if self.source == "--model-endpoint":
                hint = ("Use https, or move the endpoint into a %s config "
                        "with \"allow_insecure\": true if that host is on a "
                        "trusted network you control." % CONFIG_NAME)
            else:
                hint = ("Use https, or set \"allow_insecure\": true in %s if "
                        "that host is on a trusted network you control."
                        % (self.source or CONFIG_NAME))
            raise EndpointError(
                "refusing to send document text over plain http to %s. This "
                "is somebody's unpublished draft. %s" % (host, hint))

    def describe(self):
        """One line for a report. Never carries the key, only whether there is one."""
        return "%s @ %s (%s, ctx %d)" % (
            self.model, _scrub(self.base_url),
            "keyed" if self.api_key else "no key", self.context_tokens)

    # The budget a caller has for one unit: the context, less what the model is
    # allowed to write back, less headroom for the system prompt and the chat
    # template's own scaffolding. The 256 is measured against nothing and does
    # not need to be: it is slack in a budget that is already pessimistic, and
    # the cost of being wrong is one rejected unit rather than a bad edit.
    def input_budget(self):
        return max(0, self.context_tokens - self.max_output_tokens - 256)

    def complete(self, system, user, temperature=None, opener=None):
        """The assistant's reply, or an EndpointError. Never a partial one.

        `opener` is the urlopen to use, injected so the tests exercise this
        module rather than a mock of it. Same inversion `stylometry.fingerprint`
        uses for its measurements.

        One retry, and only one: a server that rejects the thinking-off fields
        with a 400 gets the same request again without them, and the fact is
        remembered so the next passage does not pay for it. Anything else is
        raised, because a retry loop over an unknown failure is how a rewriter
        hammers a broken endpoint fifteen times per document.
        """
        want_thinking_off = (self.disable_thinking
                             and not self._thinking_fields_rejected)
        try:
            return self._request(system, user, temperature, opener,
                                 thinking_off=want_thinking_off)
        except _FieldsRejected:
            # Not sticky yet: any 400 while the fields were present raises
            # this, and an oversized prompt 400s too. Only a retry that
            # *succeeds* without the fields proves the fields were the problem;
            # if the retry fails the same way, the flag stays unset and the
            # next passage sends them again.
            reply = self._request(system, user, temperature, opener,
                                  thinking_off=False)
            self._thinking_fields_rejected = True
            return reply

    def _request(self, system, user, temperature, opener, thinking_off):
        payload = {
            "model": self.model,
            "messages": [{"role": "system", "content": system},
                         {"role": "user", "content": user}],
            "temperature": (self.temperature if temperature is None
                            else float(temperature)),
            "max_tokens": self.max_output_tokens,
            # llama-server and Ollama both stream by default in some builds and
            # a streamed body does not parse as one JSON object. Said out loud.
            "stream": False,
        }
        if thinking_off:
            payload.update(THINKING_OFF)
        body = json.dumps(payload).encode("utf-8")
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = "Bearer %s" % self.api_key
        url = self.base_url + "/chat/completions"
        request = urllib.request.Request(url, data=body, headers=headers,
                                         method="POST")
        opener = opener or urllib.request.urlopen
        try:
            with opener(request, timeout=self.timeout) as response:
                raw = response.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as exc:
            detail = ""
            try:
                detail = exc.read().decode("utf-8", "replace")[:400]
            except Exception:
                pass
            if exc.code == 400 and thinking_off:
                raise _FieldsRejected(_scrub(detail, self.api_key))
            raise EndpointError("HTTP %s from %s: %s"
                                % (exc.code, _host_of(url)[1], _scrub(detail, self.api_key)))
        except urllib.error.URLError as exc:
            raise EndpointError(
                "could not reach %s: %s. Is the server running? A local one is "
                "usually `llama-server -m model.gguf --port 8080` or "
                "`ollama serve`." % (self.base_url, _scrub(str(exc.reason), self.api_key)))
        except OSError as exc:
            raise EndpointError("could not reach %s: %s"
                                % (self.base_url, _scrub(str(exc), self.api_key)))

        try:
            data = json.loads(raw)
        except ValueError:
            raise EndpointError(
                "%s did not return JSON. First 200 bytes: %r"
                % (self.base_url, _scrub(raw[:200], self.api_key)))

        if isinstance(data, dict) and data.get("error"):
            err = data["error"]
            message = err.get("message") if isinstance(err, dict) else str(err)
            raise EndpointError("server error: %s"
                                % _scrub(str(message), self.api_key)[:400])

        choices = (data or {}).get("choices") or []
        if not choices:
            raise EndpointError("no choices in the response from %s"
                                % self.base_url)
        choice = choices[0]
        finish = choice.get("finish_reason") or choice.get("stop_reason")
        message = choice.get("message") or {}
        text = message.get("content") or choice.get("text") or ""
        # A reasoning model's scratchpad, which several servers return in its own
        # field. Never the rewrite, and named in the error because "empty
        # response" sends somebody to the wrong problem: the request worked, the
        # model just never got to the answer.
        thought = (message.get("reasoning_content")
                   or message.get("reasoning") or "")

        if finish == "length":
            if thought and not (text or "").strip():
                raise Truncated(
                    "the model spent all %d output tokens on a reasoning block "
                    "and never wrote the rewrite. This endpoint ignored the "
                    "thinking-off request, so raise `max_output_tokens` in the "
                    "config or pick a model without a reasoning mode."
                    % self.max_output_tokens)
            raise Truncated(
                "the model stopped at max_tokens (%d) with the rewrite "
                "unfinished, so it was discarded" % self.max_output_tokens)
        if not (text or "").strip():
            if thought:
                raise EndpointError(
                    "the model returned a reasoning block and no rewrite")
            raise EndpointError("the model returned an empty rewrite")
        return text


def problems(config, source=CONFIG_NAME):
    """Everything wrong with a parsed config, as a list of lines.

    Separate from loading, so `validate.py` and the bench can check a file
    without building an Endpoint and without reaching the network.
    """
    out = []
    if not isinstance(config, dict):
        return ["%s must hold a JSON object" % source]
    if "api_key" in config:
        out.append(
            "%s carries an `api_key`. This file gets committed. Name the "
            "environment variable instead: \"api_key_env\": \"RABBIT_MODEL_API_KEY\""
            % source)
    env_name = config.get("api_key_env")
    if env_name is not None and (not isinstance(env_name, str)
                                 or not re.match(r"^RABBIT_[A-Z0-9_]+$", env_name)):
        # The config file travels with the repository, and `api_key_env` names
        # a variable in the environment of whoever runs the scan. Unrestricted,
        # a hostile checkout can pair "api_key_env": "GITHUB_TOKEN" with its
        # own base_url and --apply-model mails that secret out as a Bearer
        # header. RABBIT_* names nothing else on the machine, so a stranger's
        # config can only ask for a key the user set aside for this tool.
        out.append(
            "%s: `api_key_env` must name a RABBIT_* variable, got %r. A "
            "committed config may not reach for arbitrary secrets: export "
            "RABBIT_MODEL_API_KEY=$YOUR_PROVIDER_KEY and name that instead."
            % (source, env_name))
    unknown = sorted(set(config) - CONFIG_KEYS)
    if unknown:
        out.append("%s: unknown key(s) %s. Known keys: %s"
                   % (source, ", ".join(repr(k) for k in unknown),
                      ", ".join(sorted(CONFIG_KEYS))))
    if not config.get("base_url"):
        out.append("%s: `base_url` is required, e.g. http://127.0.0.1:8080/v1"
                   % source)
    if not config.get("model"):
        out.append("%s: `model` is required. A local llama-server ignores the "
                   "string and still needs one: any name will do." % source)
    for key in ("context_tokens", "max_output_tokens", "timeout"):
        if key in config:
            val = config[key]
            if isinstance(val, bool) or not isinstance(val, int) or val <= 0:
                out.append("%s: `%s` must be a positive integer" % (source, key))
    if "temperature" in config:
        val = config["temperature"]
        if isinstance(val, bool) or not isinstance(val, (int, float)) or not (0.0 <= val <= 2.0):
            out.append("%s: `temperature` must be a number between 0.0 and 2.0" % source)
    for key in ("allow_insecure", "disable_thinking"):
        if key in config and not isinstance(config[key], bool):
            out.append("%s: `%s` must be true or false" % (source, key))
    ctx = config.get("context_tokens", DEFAULT_CONTEXT_TOKENS)
    out_cap = config.get("max_output_tokens", DEFAULT_MAX_OUTPUT_TOKENS)
    if isinstance(ctx, int) and not isinstance(ctx, bool) and isinstance(out_cap, int) and not isinstance(out_cap, bool) and out_cap >= ctx:
        out.append("%s: `max_output_tokens` (%d) leaves no room in "
                   "`context_tokens` (%d) for the text being rewritten"
                   % (source, out_cap, ctx))
    return out


def _find_config(start_dir):
    """The nearest `.rabbit-model` at or above `start_dir`, or None.

    Bounded exactly like `voices._find_rabbit_voice`, and for a sharper reason:
    a stray config in a home directory would point every unrelated checkout on
    the machine at one person's endpoint, and this one sends document text.
    """
    curr = os.path.abspath(start_dir)
    home = os.path.abspath(os.path.expanduser("~"))
    while True:
        candidate = os.path.join(curr, CONFIG_NAME)
        if os.path.exists(candidate):
            return candidate
        if os.path.exists(os.path.join(curr, ".git")) or curr == home:
            break
        parent = os.path.dirname(curr)
        if parent == curr:
            break
        curr = parent
    return None


def _inside_git_tree(path):
    """True when `path` sits at or below a directory carrying `.git`.

    `_find_config`'s docstring worries about a stray config in `$HOME`
    reaching across unrelated checkouts; the opposite direction is the one
    with no guard at all. A `.rabbit-model` that ships inside a cloned repo
    travels with it exactly like this module's docstring warns a home config
    would travel the other way, and unlike `api_key_env` (locked to
    `RABBIT_*`), `base_url` has no restriction stopping it from naming an
    attacker's server. This doesn't prove the file is committed, only that it
    sits inside a git working tree, which is the same boundary signal
    `_find_config` already uses.
    """
    curr = os.path.dirname(os.path.abspath(path))
    home = os.path.abspath(os.path.expanduser("~"))
    while True:
        if os.path.exists(os.path.join(curr, ".git")):
            return True
        if curr == home:
            return False
        parent = os.path.dirname(curr)
        if parent == curr:
            return False
        curr = parent


def _from_env():
    base = os.environ.get(ENV_BASE_URL)
    if not base:
        return None
    return {"base_url": base,
            "model": os.environ.get(ENV_MODEL) or "local",
            "_key": os.environ.get(ENV_API_KEY) or None}


def resolve(target_path=None, overrides=None):
    """(Endpoint or None, note). Which model server applies, and who said so.

    Order: an explicit override from the command line, then the nearest
    `.rabbit-model` beside the document, then the nearest one above the working
    directory, then the environment, then nothing. Nothing is the default and it
    is not an error: a scan that is not asking for a rewrite never needs a model.

    The note is always a sentence a person can act on, including in the success
    case, because "which endpoint just received my draft" is not a question a
    report should make somebody guess at.
    """
    overrides = overrides or {}
    if overrides.get("base_url"):
        config = dict(overrides)
        key = config.pop("_key", None) or os.environ.get(ENV_API_KEY)
        source = "--model-endpoint"
        bad = problems(config, source)
        if bad:
            return None, " ".join(bad)
        try:
            return _build(config, key, source), "endpoint from %s" % source
        except EndpointError as exc:
            return None, str(exc)

    start_dirs = []
    if target_path:
        start_dirs.append(os.path.dirname(os.path.abspath(target_path)))
    start_dirs.append(os.getcwd())
    path = next((p for p in (_find_config(d) for d in start_dirs) if p), None)

    if path:
        try:
            with open(path, encoding="utf-8") as fh:
                config = json.load(fh)
        except (OSError, ValueError) as exc:
            return None, "%s could not be read: %s" % (path, exc)
        bad = problems(config, path)
        if bad:
            return None, " ".join(bad)
        env_name = config.pop("api_key_env", None)
        key = os.environ.get(env_name) if env_name else None
        if env_name and not key:
            return None, ("%s names api_key_env %r but that variable is not "
                          "set in this environment" % (path, env_name))
        try:
            built = _build(config, key, path)
        except EndpointError as exc:
            return None, str(exc)
        note = "endpoint from %s" % path
        if _inside_git_tree(path):
            note += (". This file sits inside a git checkout: if you did not "
                      "write it yourself, verify base_url before this tool "
                      "sends it any document text.")
        return built, note

    env = _from_env()
    if env:
        key = env.pop("_key", None)
        bad = problems(env, ENV_BASE_URL)
        if bad:
            return None, " ".join(bad)
        try:
            return _build(env, key, ENV_BASE_URL), "endpoint from $%s" % ENV_BASE_URL
        except EndpointError as exc:
            return None, str(exc)

    return None, ("no %s found and $%s is not set, so no model is configured. "
                  "See skills/rabbit-rewrites/SKILL.md for a two-line local "
                  "setup." % (CONFIG_NAME, ENV_BASE_URL))


def _build(config, key, source):
    return Endpoint(
        base_url=config["base_url"],
        model=config["model"],
        api_key=key,
        context_tokens=config.get("context_tokens", DEFAULT_CONTEXT_TOKENS),
        max_output_tokens=config.get("max_output_tokens", DEFAULT_MAX_OUTPUT_TOKENS),
        temperature=config.get("temperature", DEFAULT_TEMPERATURE),
        timeout=config.get("timeout", DEFAULT_TIMEOUT),
        allow_insecure=config.get("allow_insecure", False),
        disable_thinking=config.get("disable_thinking", True),
        source=source,
    )
