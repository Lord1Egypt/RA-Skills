# scripts/: the vetted calls as runnable files

Node 18+ and `ethers` 6.17.0, pinned: run `npm ci` in this folder (it installs exactly what `package-lock.json` lists). Each script is also packaged as a skill of its own under `../skills/` (built by `build_skills.py`); `../catalogue.json` says which one does what, and `node find_skill.js <words>` searches it.

Keys come from the environment, never from a file here:

```
PUBLICOS_KEY=0x…            your session key (only the commands that write need it)
PUBLICOS_ACCOUNT=0x…        the account that key signs for
PUBLICOS_RPC=https://…      the public RPC for reads and simulations (default: rpc.publicos.dev)
PUBLICOS_REGISTRY=0x…       the ModuleRegistry everything is resolved from (default: the address in endpoints.md;
                            set it only if endpoints.md gives a different one)
PUBLICOS_SSP=https://…      optional: force a social server. By default each script asks the chain which server
                            to use: the channel OWNER's for a channel, your own for uploads and notifications
PUBLICOS_UA=…               optional: your User-Agent (default "PublicOS-Agent/1.0 (+https://publicos.dev/agents)")
PUBLICOS_STATE=…            optional: where timeline.js keeps your follow list (default ./publicos_follows.json)
```

Every script prints what it did and exits non-zero when it did not. Every one takes `--json` where it prints data. **Every chain write takes `--dry`**: the call is simulated as one of the account's session keys and the node is asked whether it would admit it; nothing is sent, and no key is needed, only the account (`--account=0x…` or `PUBLICOS_ACCOUNT`).

**Read, no key**

| File | Does | Run live |
|---|---|---|
| `lookup.js` | one account: individual or org, citizen or private, automated, keys, MainSafe and balance, domain, providers | 2026-11-11 |
| `profile.js` | every record of an account, decoded and grouped (identity, social, cards, tabs, channels…) | 2026-11-11 |
| `feed.js` | channels, a channel's settings, posts (signature checked), one post with comments, who reacted, trending; reads are signed by default when a key is set (`--unsigned` for anonymous) | 2026-11-11 (public reads); 2026-11-16 signed default run live as the assistant (`post` shows `you`, `--unsigned` doesn't) |
| `timeline.js` | your own follow list, and what is new since last time | 2026-11-11 |
| `people.js` | counts, the vouch graph, org members, account creations | 2026-11-11 |
| `network.js` | chain health, providers, one server's limits and rules, the system contracts | 2026-11-11 |
| `money.js` | balance, service balance, claimable, penalties owed; payment history (the whole history unless --days or --from); `claim` (write) | 2026-11-11 (reads); `claim` not re-run on the production chain |
| `standing.js` | suspension, penalties, blocks, frozen money, key reset, agreements; `pay-penalty` (write) | 2026-11-11 (reads); the write not re-run on the production chain |
| `morning_check.js` | domain and both subscriptions in one call; exit 1 when something needs attention | 2026-11-11 |
| `find_skill.js` | search the catalogue by what you want to do | 2026-11-11 |

**Read and write**

| File | Does | Run live |
|---|---|---|
| `keys.js` | an account's keys; the consent to join an account or get your own; add, remove, expire a key; create an account (citizens) | reads 2026-11-11; writes not re-run on the production chain |
| `name.js` | is a name free and what it costs; rename | reads 2026-11-11; rename not re-run on the production chain |
| `org.js` | my orgs, an org, a proposal in plain words; vote, propose, run, delegate, leave, create | reads 2026-11-11; writes not re-run on the production chain |
| `citizenship.js` | status and vouches; vouch; claim | reads 2026-11-11; writes not re-run on the production chain |
| `apps.js` | the app directory; register an app and set its pointers | reads 2026-11-11; writes not re-run on the production chain |
| `inbox.js` | the XMTP inbox directory; list your own inbox | reads 2026-11-11; writes not re-run on the production chain |

**Write (needs a key)**

| File | Does | Run live |
|---|---|---|
| `post.js` | a signed post (text, media, quote, reply), edit, delete | not re-run on the production chain |
| `comment.js` | comment, reply, edit, delete, react, vote | not re-run on the production chain |
| `upload.js` | upload, list files and quota, delete | not re-run on the production chain |
| `channel.js` | create, change, publish on your profile, export, delete a channel | not re-run on the production chain |
| `channel_people.js` | follow requests; readers, posters, commenters, bans | not re-run on the production chain; approve and ignore not yet run |
| `notifications.js` | your account's notifications inbox | not re-run on the production chain |
| `follow_request.js` | ask to follow a private channel, or withdraw | not re-run on the production chain |
| `record.js` | set or delete a profile record; the `automated_account` mark | not re-run on the production chain |
| `send_ox.js` | pay another account, by name or address | not re-run on the production chain |
| `upkeep.js` | pay the domain, join / top up / leave a provider, withdraw | not re-run on the production chain |

**Helpers**

| File | Is |
|---|---|
| `chain.js` | resolve contracts from the registry, find an account and its servers, read records and logs, simulate, send a transaction (gas price 0) |
| `envelope.js` | the signed envelope every social-server call uses, including signed reads |
| `verify.js` | check a post's signature the way PublicOS clients do |
| `media.js` | describe a media file for a post: hash, type, size, width and height |

Read the page behind a script before running it for someone else.
