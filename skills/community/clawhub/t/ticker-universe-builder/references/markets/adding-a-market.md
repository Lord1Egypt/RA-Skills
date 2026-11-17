# Adding a market

This document is for whoever extends the skill, not for the agent using it. Fourteen markets
ship — `us`, `cn`, `jp`, `in`, `hk`, `kr`, `uk`, `tw`, `de`, `fr`, `ca`, `au`, `br` and
`crypto`; nothing about the design stops at fourteen.

Every market-specific rule lives in one row of `MARKET_SPECS` in `scripts/universe_core.py`:

| Field | What it decides |
|---|---|
| `venues` | Which `EXCHANGE:` prefixes are accepted |
| `symbol_pattern` / `symbol_hint` | The shape of a legal symbol, and the error text when it is not |
| `venue_in_asset_id` | Whether two venues carrying one symbol are two assets or one |
| `asset_id_strip` | Suffixes removed to reach economic identity (a perpetual and its spot pair) |
| `factor_r2_required` | Whether every non-anchor member must state its redundancy with the market factor |
| `language` | Which locale the `.md` report is written in unless the caller overrides it |
| `quality_flags` | Adverse flags this market's regime issues and no other's does |

## Two ways in, and when each is right

A market outside the fourteen is not forbidden. It has two routes, and they answer different
questions:

| | **Declared** | **Registered** |
|---|---|---|
| Where the rules live | `market_spec` in the snapshot | a row in `MARKET_SPECS` |
| Who wrote them | whoever built this universe, at run time | this repository, reviewed |
| What it costs | research, with evidence | a pull request |
| What ships | nothing | a starter taxonomy, an overlay, a researched coverage plan, a locale |
| What the report says | `Market rules: declared`, on every run | nothing; silence is the reviewed case |

A declared market has no starter taxonomy, so the agent writes one from nothing;
`taxonomy --check` is the gate on that, and it is worth running before any candidate is
researched.

Declaring is the answer for a market nobody here has looked at — a smaller exchange, a market one
user cares about, a market being tried out. Registering is the answer once a market is used often
enough that leaving its venue list to be re-researched every session is the larger risk. The
first does not block on us; the second does not depend on the agent getting it right twice.

Both build under identical general logic. The only thing that differs is who vouches for those
seven fields, and the report never lets a reader confuse the two.

A new *registered* market is five additions and no edits to existing logic:

1. A `MarketSpec` row in `MARKET_SPECS`.
2. A sourced coverage plan with market-specific leader/necessary-peer duties, entity budgets,
   sector caps and references. Defaults do not size markets through breadth multipliers.
3. A starter taxonomy at `assets/taxonomy/<code>.json`. For an equity market this is a delta on
   `_equity.json`, not a new table: state `extends`, then `drop` what this market does not list,
   `add` what nobody else lists, `groups` to put the group labels in the market's own language,
   `level` to move a theme between tiers, and `weight` to say what this market is actually about.
   Eleven of the shipped tables are under fifty lines because of this. `taxonomy --check` has to
   pass clean — errors *and* warnings — for all four profiles, which is also a test.
4. An overlay at `references/markets/<code>.md` covering identity, what this market is, its
   adverse flags and where its primary sources live. Start from another market's; the shared
   equity material is in [equity-common.md](equity-common.md) and must not be repeated.
5. A researched snapshot exercising the new rules, with dated listing checks, real measurements
   and a reproducible build test. Use the Medium inputs in `examples/` as the contract reference;
   do not generate illustrative scores. Empty required themes are findings about the taxonomy,
   never reasons to invent tickers. Publishing a new example is a separate scope choice; the current release ships CN/US/Crypto examples while keeping fourteen registered markets.


Plus a locale at `assets/locales/<language>.json` if the market's language has none yet, and, if
the market's regulator issues flags the universal seven cannot express, a `quality_flags` set on
the row with a `flag.<code>` entry in that market's own locale and in `en`. Three tests decide
whether a flag belongs there: does this regime issue it as a discrete, lookupable status; does
recording it as `risk_warning` or `regulatory_action` lose something that would change a
selection; and is the code meaningless in every other market. A flag that fails the third is a
universal code that has not been added yet — add it to `QUALITY_FLAG_CODES` instead, where it is
comparable across markets, rather than to two market specs where it silently is not.

CI checks the registry, starter taxonomy and locale for all registered markets.
The current worked examples additionally receive full offline build and CLI checks.

Writing the research snapshot is also how the registry row gets tested. Two shipped symbol rules were wrong
until a real listing hit them — `de` rejected `4GLD` and `br` rejected `B3SA3` — and neither
would have surfaced from reading the rule.

## Report language

A universe is read by the people who trade that market, so the human-readable report follows the
market rather than the tool: `language` is a field of the registry the same way the symbol shape
is. `--language` overrides it per run; nothing else about the build changes.

Only the chrome is translated — headings, labels, and the closed vocabularies (roles, exclusion
and audit codes, profiles, bases, review depths). Those are finite, so
`assets/locales/<lang>.json` can be complete and `LocalizationTests` proves it is. Everything
else in the report is content the research wrote: a Chinese A-share snapshot carries Chinese
names, themes, reasons and methods without the renderer knowing anything about them, which is
also why the taxonomy's `l1_name` is authored in the market's language rather than translated.
Codes are printed beside their translation, never in place of it — `基准 (BENCHMARK)` — because
the code is what the documentation names and what a reader greps for. Validation diagnostics stay
English for the same reason: they name policy fields and code paths, and `.validation.json`
carries the identical text.

Adding a language is one JSON file with the same keys as `en.json`. `zh-Hans`, `zh-Hant` and `en`
ship. One vocabulary is deliberately outside this: a `quality_flags` code a snapshot declared at
run time has no key in any locale, because no lexicon can carry a vocabulary invented after it
shipped. Those print as the bare code, and the build warns that they will.

### Writing a locale

A wrong word is caught by reading the file. The failures that survive a careful read are the ones
that only look wrong in the rendered page, so `LocalizationTests` checks for those four directly:

| Rule | Why it is a test and not a habit |
|---|---|
| Every key present, every closed vocabulary covered | Adding a role or an exclusion code without a word for it would print a bare code into a translated report |
| CJK text uses CJK punctuation | An ASCII comma between two Chinese characters is the single clearest tell that a page was generated rather than written. `punct.colon` is part of the lexicon for the same reason |
| No word means two things in one report | `review.depth` and `depth.deep` print on one line; giving both `深度` renders "深度：深度", which is how the first draft shipped |
| `zh-Hant` stays a conversion of `zh-Hans` | Maintained as two independent translations, one term becomes two — `NEW_LISTING` was `次新` in one and `新上市` in the other. Length parity is the proxy; a regional term that changes length goes in the test's exemption set, visibly |

Two more rules the tests cannot check, so they are written here:

- **Translate the register, not the words.** `profile.light/medium/heavy` are `精简档 / 标准档 /
  完整档` — one axis, three points. The first draft mixed three axes (`轻量 / 标准 / 完整`) and
  read like three unrelated settings.
- **Watch for terms the market already owns.** `turnover` here is the share of members replaced
  in a review, and `换手` in a Chinese market report means trading turnover — a word already
  spoken for by `liquidity`. It is `成分变动`.

The example is held to the same standard as the chrome: `cn-medium/universe.zh-Hans.md` is checked
line by line, because an example that reads like machine output teaches the agent to write machine
output. A new market ships two example reports, its own and English, exactly as a build writes
two.

## The classification

Deciding a market's language after the fact means two A-share universes built a month apart read
differently. So the language is settled in the registry, before any market is implemented, and it
is a fact about the market rather than a preference of the caller.

All fourteen have registered rules, a starter and a report locale. Worked examples ship for
CN/US/Crypto separately:

| Market | Code | Venues | Language | Symbol |
|---|---|---|---|---|
| United States | `us` | `NASDAQ` `NYSE` `AMEX` `ARCA` `NYSEARCA` `CBOE` `IEX` `OTC` | `en` | one to fifteen characters starting with a letter |
| China A-shares | `cn` | `SSE` `SZSE` `BSE` | `zh-Hans` | six digits |
| Japan | `jp` | `TSE` | `ja` | four characters: three digits then a digit or a letter |
| Hong Kong | `hk` | `HKEX` | `zh-Hant` | one to five digits, unpadded |
| India | `in` | `NSE` `BSE` | `en` | an alphanumeric code, ampersand and hyphen allowed |
| Korea | `kr` | `KRX` | `ko` | six digits |
| Taiwan | `tw` | `TWSE` `TPEX` | `zh-Hant` | four to six digits, optionally one trailing letter |
| United Kingdom | `uk` | `LSE` | `en` | two to six characters starting with a letter |
| Germany | `de` | `XETR` `FWB` | `de` | one to six alphanumeric characters |
| France | `fr` | `EURONEXT` | `fr` | one to five characters starting with a letter |
| Canada | `ca` | `TSX` `TSXV` | `en` | one to ten characters starting with a letter |
| Australia | `au` | `ASX` | `en` | three to six characters starting with a letter |
| Brazil | `br` | `BMFBOVESPA` | `pt-BR` | four characters starting with a letter, then one or two digits |
| Crypto | `crypto` | `BINANCE` | `en` | a USDT-quoted spot or perpetual symbol |

Two rows that an earlier draft of this table carried are worth recording as decisions rather than
quietly dropping.

**There is no `eu`.** A single European row was the plan, on the reasoning that Frankfurt, Paris
and Zurich share a readership and could share English. Splitting it into `de` and `fr` was not a
scope increase — it was the identity rule refusing to average. A cross-border row has to carry
venue *in* the identity or Daimler in Frankfurt and Daimler in Paris collapse into one member;
every other row strips the venue. One market cannot hold both rules, and a German report in
English is a worse answer than two rows. Zurich has no row yet for the ordinary reason: nobody
has written its taxonomy.

**`sa` and `sg` are not registered.** Both were listed as above-scale and neither has a theme
table, a locale or an example, so neither is in `MARKET_SPECS`. They build today by declaring
themselves in the snapshot, which is the point of the declared route. Registering `sa` also
means writing `ar.json` and the first right-to-left report the renderer has seen.

Two more markets ship without an `ar`-style surprise but with a rule correction each: `de` and
`br` are the reason the symbol column above is worth reading carefully. See the closing note.

## What the registry does not decide

Admission roles, evidence/measurement contracts, turnover controls and identity validation
are shared. Markets supply their researched economic branches, leaders, sector caps/weights
and references. Display theme weights never allocate current coverage. Max follows its own
qualified Heavy’s distribution. The explicit archived policy retains legacy weighted scoring;
its vocabulary is not a reason to add new product roles.

## What building the last eleven actually cost

The three sketches this section used to hold were `hk`, `jp` and `eu`. Two of them ship, and the
third turned into `de` and `fr` for the identity reason above — which is the useful lesson: the
part of a new market that is hard to guess is never the venue list.

The two wrong symbol rules are noted above. The nine wrong theme tables are the finding that
generalises, because the tables had all been reviewed.

Nine of them claimed sectors their market does not list, which matters more than an unused
row: required economic duties must have real representatives, so a made-up duty cannot be
repaired by allocating more candidates. Managed care left Light in `jp`, `kr`, `hk` and
`uk`, where cover is single-payer and no insurer lists. Energy, payments and the data-centre
theme left the German table outright. `br` raised managed care *into* Light, alone among the
fourteen. None of that was visible from reading the tables — only from trying to fill them.

This is why the researched snapshot is item 5 on the list above and not an optional extra.
