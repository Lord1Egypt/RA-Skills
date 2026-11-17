# Registry examples

This package includes all ten build specs, seven researched market snapshots, provenance and
the deterministic example builder. Generated outputs are kept in the upstream repository to
reduce registry transfer and server processing; no research fields are removed.

Run `python examples/build_examples.py` from the skill root to recreate all ten qualified
examples, including HTML, Markdown, JSON, validation JSON and TradingView TXT. This is an
offline replay of dated facts, not new market research. US depths share the US Medium snapshot.

For the rendered reports, input dates and research limits, see
[the full examples](https://github.com/bitpunklabs/ticker-universe-builder/tree/377f33140112ba66d7bbc3575d9a0f627ee0f870/examples).
