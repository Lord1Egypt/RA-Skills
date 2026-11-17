"""
rwlib - the shared engine behind rabbit-writes, rabbit-readme-improver, and the corpus
research scripts.

Stdlib only, and importable by path, because these scripts run from a plugin
directory that is not on anybody's PYTHONPATH. Every consumer bootstraps the
same way:

    HERE = os.path.dirname(os.path.abspath(__file__))
    if HERE not in sys.path:
        sys.path.insert(0, HERE)
    from rwlib import markdown as md

Modules:

    artifacts   artifact path resolution and normalization.
    cli_error   formatted LLM error reporting.
    corpus      the README corpus figures, and the drift check against them.
    docx_text   Word document visible text and hidden run extraction.
    endpoint    one OpenAI-compatible chat endpoint, and how to find it.
    facts       preservation tracking for numbers, dates, ranges, and quotes.
    findings    the finding schema and its version.
    fixes       the mechanically safe subset of edits, for scan.py --apply-safe.
    inflect     inflection engine for word and phrase bans.
    injection   the safety band: concealed text, and text aimed at an agent.
    language    the English-only scope check. Warns, never fails.
    lexicon     the pattern catalogue, its version, and the regex builders.
    links       reference-link definition discovery and bracket/parenthesis balancing.
    markdown    spans: fences, links, images, tables, quotes, dashes, badges.
    outputstyle a voice profile, rendered as a Claude Code output style.
    registers   the tolerance matrix, read from registers.json.
    rewrite     model-backed rewriting, one finding at a time, behind the gate.
    sarif       findings as SARIF 2.1.0, for PR annotations.
    sections    what counts as an "installation" heading, for README work.
    sentences   English sentence and word segmentation.
    ste         ASD-STE100 structural rules, from ste_lexicon.json.
    stylometry  stylometric distance calculations and exemplars.
    suppress    in-document finding suppression comment parser.
    voice_check rule validator for voice profiles.
    voices      voice rules files, including `extends` inheritance and blending.

Nothing here decides what good writing is. That lives in the reference files,
where a person can argue with it.
"""

from .voices import load_scan

__all__ = [
    "artifacts", "cli_error", "corpus", "docx_text", "endpoint", "facts",
    "findings", "fixes", "inflect", "injection", "language", "lexicon",
    "links", "markdown", "outputstyle", "registers", "rewrite", "sarif",
    "sections", "sentences",
    "ste", "stylometry", "suppress", "voice_check", "voices"
]
