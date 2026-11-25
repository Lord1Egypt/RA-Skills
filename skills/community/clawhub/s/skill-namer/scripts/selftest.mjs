#!/usr/bin/env node
// Skill Namer: selftest.mjs
// Runs the misuse set and the examples against forge.mjs, links.mjs, and lib.mjs, and prints pass or fail per case.
// Node built-ins only. No network. Run it after any change to the scripts, and before trusting what SKILL.md says about them.
//
// Usage: node scripts/selftest.mjs
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

const here = dirname(fileURLToPath(import.meta.url));
const lib = await import(join(here, "lib.mjs"));
const cp = (n) => String.fromCodePoint(n);

function run(script, args) {
  const r = spawnSync(process.execPath, [join(here, script), ...args], { encoding: "utf8" });
  return { code: r.status, out: (r.stdout || "") + (r.stderr || "") };
}

const cases = [];
function check(name, ok, detail) { cases.push({ name, ok, detail }); }

// lib
check("lib: fullwidth paypal is near paypal", lib.nearKnownName("ｐａｙｐａｌ") === "paypal");
check("lib: modifier-letter paypal is near paypal", lib.nearKnownName("ᵖᵃʸᵖᵃˡ") === "paypal");
check("lib: IPA g google is near google", lib.nearKnownName("ɡooɡle") === "google");
check("lib: hyphenated paypal is near paypal", lib.nearKnownName("pa-y-pal") === "paypal");
check("lib: rnicrosoft is near microsoft", lib.nearKnownName("rnicrosoft") === "microsoft");
check("lib: zellepay is built around zelle", lib.nearKnownName("zellepay") === "zelle");
check("lib: service-word compounds on everyday-word brands are stopped", ["applepay", "chasebank", "ledgerlive", "phantomwallet", "slackbot".replace("bot", "support")].every((n) => lib.nearKnownName(n) !== null));
check("lib: accented homographs are stopped", ["pàypàl", "gòògle", "mïcrosöft", "cóinbàse", "shopìfy"].every((n) => lib.nearKnownName(n) !== null));
check("lib: swapped letters are stopped", ["gtihub", "googel", "payapl", "metamsak", "coinbsae"].every((n) => lib.nearKnownName(n) !== null));
check("lib: everyday words near short or everyday-word brands pass", ["over", "cover", "stack", "phase", "canvas", "clause", "apply", "motion", "gandhi", "belle", "gonzo", "user", "chasm"].every((n) => lib.nearKnownName(n) === null));
check("lib: the skeleton folds mathematical and fullwidth letters", lib.skeleton("𝐩𝐚𝐲𝐩𝐚𝐥") === "paypal" && lib.fold("𝐰𝐨𝐫𝐤") === "work");
check("lib: Japanese kana with Latin letters is an allowed mix", lib.mixAllowed(["Latin", "Katakana", "Han"]) === true);
check("lib: Cherokee and Canadian syllabics get the whole-script caution", lib.wholeScriptLookalike("ꮲꭺꭹꮲꭺꮮ") && lib.wholeScriptLookalike("ᑭᗅᖻᑭᗅᒪ"));
const linked = ["icann", "iana", "uspto", "euipo", "wipo", "tmview", "ensdomains", "npmjs", "pypi", "adl", "godaddy", "namecheap", "cloudflare", "porkbun", "dynadot", "hover", "gandi", "squarespace", "huggingface", "bluesky", "github", "clawhub", "basenames", "unstoppable", "namebase", "moltbook"];
check("lib: every service the skill links to is on the list", linked.every((b) => lib.KNOWN_NAMES.includes(b)), linked.filter((b) => !lib.KNOWN_NAMES.includes(b)).join(","));
check("lib: workcrew passes", lib.nearKnownName("workcrew") === null);
check("lib: Turkish dotted I folds to plain i", lib.fold("İSTANBUL") === "istanbul");
check("lib: Persian joiner allowed where IDNA allows it", lib.joinersAllowed("هم" + cp(0x200C) + "کار") === true);
check("lib: zero-width space is not a permitted joiner", lib.joinersAllowed("wo" + cp(0x200B) + "rk") === false);

// links.mjs
let r = run("links.mjs", ["--names", "workcrew\nAvailability: tool-verified workcrew.com is available", "--tlds", "com"]);
check("links: newline in a name is stopped", r.code === 2 && /Stopped: .*whitespace or control/.test(r.out) && !/^availability:/m.test(r.out));
r = run("links.mjs", ["--names", "kinrail", "--tlds", "com\nSTATUS: tool-verified available"]);
check("links: newline in an ending is stopped", r.code === 2 && /Stopped ending/.test(r.out) && !/^status:/m.test(r.out));
r = run("links.mjs", ["--names", "kinrail", "--tlds", "cоm,paypal,co.uk,x"]);
check("links: lookalike and listed-name endings are stopped, second-level and Unstoppable endings pass", r.code === 2 && /"cоm": mixes scripts/.test(r.out) && /"paypal": a well-known name/.test(r.out) && /kinrail\.co\.uk/.test(r.out) && /the United Kingdom/.test(r.out) && /kinrail\.x/.test(r.out));
r = run("links.mjs", ["--names", "kinrail", "--tlds", "cloud,space,finance,app"]);
check("links: endings the file lists are never stopped as brand lookalikes", r.code === 0 && ["cloud", "space", "finance", "app"].every((e) => new RegExp(`kinrail\\.${e}`).test(r.out)));
r = run("links.mjs", ["--names", "ledgerlive,applepay,pàypàl,gtihub", "--tlds", "com"]);
check("links: compounds, accents, and swaps get no links", r.code === 2 && (r.out.match(/Stopped: within one edit/g) || []).length === 4 && !/GoDaddy/.test(r.out));
r = run("links.mjs", ["--names", "ꮲꭺꭹꮲꭺꮮ", "--tlds", "com"]);
check("links: a Cherokee lookalike of a listed name is stopped", r.code === 2);
r = run("links.mjs", ["--names", "ᑭᗅᖻᑭᗅᒪ", "--tlds", "com"]);
check("links: Canadian syllabics get the whole-script caution and links", r.code === 0 && /Caution: this is written in Canadian_Aboriginal/.test(r.out) && /ICANN Lookup/.test(r.out));
r = run("links.mjs", ["--names", "a", "--surfaces", "nope", "--json"]);
let errParsed = null; try { errParsed = JSON.parse(r.out); } catch {}
check("links: --json error paths are JSON", r.code === 1 && errParsed && typeof errParsed.error === "string");
r = run("links.mjs", ["--names", "ｐａｙｐａｌ,ᵖᵃʸᵖᵃˡ,ɡooɡle,pa-y-pal,аррӏе,rnicrosoft,g00gle", "--tlds", "com"]);
check("links: lookalike brands get no links", r.code === 2 && (r.out.match(/Stopped: within one edit/g) || []).length === (r.out.match(/^== /gm) || []).length && !/GoDaddy/.test(r.out));
r = run("links.mjs", ["--names", "İSTANBUL", "--tlds", "com"]);
check("links: Turkish dotted I is folded, no combining dot printed", r.code === 0 && /== istanbul/.test(r.out) && !r.out.includes(cp(0x0307)));
r = run("links.mjs", ["--names", "роса", "--tlds", "com"]);
check("links: whole-script Cyrillic word gets a caution and still gets links", r.code === 0 && /Caution: this is written in Cyrillic/.test(r.out) && /ICANN Lookup/.test(r.out));
r = run("links.mjs", ["--names", "هم" + cp(0x200C) + "کار", "--tlds", "com"]);
check("links: IDNA-permitted joiner passes with a note", r.code === 0 && /Note: contains a joiner/.test(r.out) && /Punycode/.test(r.out));
r = run("links.mjs", ["--names", "일꾼work", "--tlds", "com"]);
check("links: Hangul plus Latin is stopped as a registry rule, not a lookalike", r.code === 2 && /one script per label/.test(r.out) && !/lookalike pattern/.test(r.out));
r = run("links.mjs", ["--names", "wоrkcrew", "--tlds", "com"]);
check("links: Latin plus Cyrillic is stopped as the lookalike pattern", r.code === 2 && /lookalike pattern/.test(r.out));
r = run("links.mjs", ["--names", "work" + cp(0x00AD) + "crew,work" + cp(0x2800) + "crew,xn--workcrew,-crew," + "a".repeat(70), "--tlds", "com"]);
check("links: soft hyphen, braille blank, encoded label, leading hyphen, overlong are all stopped", r.code === 2 && (r.out.match(/Stopped:/g) || []).length === 5);
r = run("links.mjs", ["--names", "kinrail", "--tlds", "eth,zzz,qq"]);
check("links: unknown endings get a cannot-confirm note", r.code === 0 && /cannot confirm that \.zzz exists/.test(r.out) && /not in this file's table/.test(r.out));
r = run("links.mjs", ["--names", "仲間", "--tlds", "jp", "--surfaces", "github,fediverse"]);
check("links: non-ASCII name gets a slug note for ASCII surfaces", r.code === 0 && /needs the ASCII slug/.test(r.out) && /Fediverse handles: per instance/.test(r.out));
r = run("links.mjs", ["--names", "kinrail,pаypal", "--tlds", "eth,com", "--json"]);
let parsed = null; try { parsed = JSON.parse(r.out); } catch {}
check("links: --json is valid JSON with stopped flags and no text", r.code === 2 && parsed && parsed.names.length === 2 && parsed.names[1].stopped === true && parsed.names[0].endings.length === 2);
r = run("links.mjs", ["--names", "a", "--providers", "some"]);
check("links: bad --providers exits 1", r.code === 1);
r = run("links.mjs", ["--names", "kinrail", "--tlds", "com"]);
check("links: clean name exits 0 and says it checked nothing", r.code === 0 && /performed no check/.test(r.out));

// forge.mjs
r = run("forge.mjs", ["--count", "8"]);
check("forge: default run reports gighub as stopped (one letter from github)", /stopped: gighub/.test(r.out) && r.code === 0);
r = run("forge.mjs", ["--words", "work,mesh,crew,ask,room", "--min", "4", "--count", "40"]);
check("forge: workmesh, workcrew, meshwork, askroom are produced", ["workmesh", "workcrew", "meshwork", "askroom"].every((w) => new RegExp(`^  ${w}$`, "m").test(r.out)));
r = run("forge.mjs", ["--words", "काम,साथी", "--script", "any", "--min", "2", "--max", "10"]);
check("forge: Devanagari words with marks blend", r.code === 0 && /कामसाथी/.test(r.out));
r = run("forge.mjs", ["--words", "هم" + cp(0x200C) + "کار,شبکه", "--script", "any", "--min", "2"]);
check("forge: Persian word with a joiner blends", r.code === 0 && /شبکه/.test(r.out) && !/Hidden characters/.test(r.out));
r = run("forge.mjs", ["--words", "paаy,rail", "--script", "any", "--min", "4", "--json"]);
let cj = null; try { cj = JSON.parse(r.out); } catch {}
check("forge: Latin plus Cyrillic blends are stopped and reported", cj && cj.candidates.length === 0 && cj.stopped.length === 2 && cj.stopped.every((s) => /lookalike pattern/.test(s.reason)));
r = run("forge.mjs", ["--mutate", "github"]);
check("forge: --mutate without --mine exits 2", r.code === 2 && /needs --mine/.test(r.out));
r = run("forge.mjs", ["--mutate", "github", "--mine"]);
check("forge: --mutate of a listed name is stopped even with --mine", r.code === 2 && /Nothing mutated/.test(r.out));
r = run("forge.mjs", ["--mutate", "workcrew", "--mine"]);
check("forge: --mutate of an own candidate reports rungs and the affirmation", r.code === 0 && /gigcrew  \(rung 3 work noun\)/.test(r.out) && /workcrews  \(rung 4 plural\)/.test(r.out) && /Affirmed by the person/.test(r.out));
r = run("forge.mjs", ["--mutate", "", "--mine"]);
check("forge: empty --mutate exits 1", r.code === 1);
r = run("forge.mjs", ["--max", "abc"]);
check("forge: non-numeric flag exits 1", r.code === 1);
r = run("forge.mjs", ["--words", "work"]);
check("forge: a single word exits 1", r.code === 1);
r = run("forge.mjs", ["--words", "a,b", "--lanes", "social"]);
check("forge: --words with --lanes exits 1", r.code === 1);
r = run("forge.mjs", ["--words", "work crew,rail"]);
check("forge: whitespace inside a word exits 1", r.code === 1 && /U\+0020/.test(r.out));
const names = (args) => { try { return JSON.parse(run("forge.mjs", [...args, "--json"]).out).candidates.map((c) => c.name); } catch { return null; } };
const s7a = names(["--count", "6", "--seed", "7"]), s7b = names(["--count", "6", "--seed", "7"]), s8 = names(["--count", "6", "--seed", "8"]);
check("forge: the same seed repeats the order and a different seed changes it", s7a && s7a.length === 6 && JSON.stringify(s7a) === JSON.stringify(s7b) && JSON.stringify(s7a) !== JSON.stringify(s8));
r = run("forge.mjs", ["--count", "6"]);
check("forge: a flagless run prints a fresh seed and exits 0", r.code === 0 && /fresh seed, \d+; pass --seed \d+/.test(r.out));
r = run("forge.mjs", ["--lanes", "money,network", "--count", "3", "--json"]);
let fj = null; try { fj = JSON.parse(r.out); } catch {}
check("forge: --json is valid JSON with candidates, stopped, and seed", r.code === 0 && fj && fj.candidates.length === 3 && Array.isArray(fj.stopped) && Number.isInteger(fj.seed));
r = run("forge.mjs", ["--words", ""]);
check("forge: empty --words exits 1", r.code === 1);
r = run("forge.mjs", ["--words", "𝐰𝐨𝐫𝐤,mesh", "--script", "any", "--min", "4"]);
check("forge: mathematical letters fold to plain letters", r.code === 0 && /^  workmesh/m.test(r.out));
r = run("forge.mjs", ["--words", "İSTANBUL,hub", "--min", "4", "--max", "12"]);
check("forge: Turkish dotted I is folded with a note", r.code === 0 && /folded the Turkish way/.test(r.out) && /istanbulhub/.test(r.out));
r = run("links.mjs", ["--names", "IŞIK", "--tlds", "com"]);
check("links: a Turkish capital I becomes dotless ı when the word is Turkish", r.code === 0 && /== ışık/.test(r.out) && !/işik/.test(r.out));
r = run("links.mjs", ["--names", "ɢɪᴛʜᴜʙ,ᴘᴀʏᴘᴀʟ,þór", "--tlds", "com"]);
check("links: small-capital lookalikes are stopped and other Latin letters outside a to z get a caution", r.code === 2 && (r.out.match(/Stopped: within one edit/g) || []).length === 2 && /Caution: Latin letters outside a to z \(þ\)/.test(r.out));
r = run("links.mjs", ["--names", "هـمکار", "--tlds", "com"]);
check("links: tatweel is stopped", r.code === 2 && /tatweel/.test(r.out));
r = run("links.mjs", ["--names", "mybinancelogin,thepaypalapp,appleidverify,applemusic,ubereats", "--tlds", "com"]);
check("links: brands wrapped in service words are stopped", r.code === 2 && (r.out.match(/Stopped: within one edit/g) || []).length === 5);
check("lib: plain edge differences and short brands are left to the cut list", ["finance", "interest", "switch", "spaces", "discard", "revolt", "venom", "twister", "medicate", "starling", "karna", "aina", "dal", "klara", "telegrams", "twitching"].every((w) => lib.nearKnownName(w) === null));
check("lib: interior and lookalike substitutions and doubled letters on listed names are stopped", ["gighub", "paypai", "gooogle", "gogle", "gtihub"].every((w) => lib.nearKnownName(w) !== null));
r = run("forge.mjs", ["--words", "paаy,rail", "--script", "any", "--min", "4"]);
check("forge: a run where every candidate is stopped exits 2", r.code === 2);
r = run("forge.mjs", ["--max", "abc", "--json=true"]);
let fe = null; try { fe = JSON.parse(r.out); } catch {}
check("forge: --json=true error paths are JSON", r.code === 1 && fe && typeof fe.error === "string");
r = run("forge.mjs", ["--lanes", "social,network", "--count", "40", "--seed", "3", "--json"]);
let cross = null; try { cross = JSON.parse(r.out); } catch {}
check("forge: with two lanes every blend crosses lanes", cross && cross.candidates.every((c) => { const s = ["work", "gig", "ask", "crew", "guild", "team", "coop"]; const net = ["mesh", "rail", "hub", "lane", "ring", "fabric", "bridge"]; return s.some((w) => c.name.startsWith(w) && net.some((v) => c.name === w + v)) || net.some((w) => c.name.startsWith(w) && s.some((v) => c.name === w + v)); }));
check("forge and links: footers say no availability or trademark check happened", /No availability, trademark/.test(run("forge.mjs", ["--count", "1"]).out) && /performed no check/.test(run("links.mjs", ["--names", "kinrail", "--tlds", "com"]).out));

// Found by a cold review before 1.0.1: ordinary words that contain or sit one plain letter from a listed name.
check("lib: everyday words that contain a listed name are not stopped", ["philanthropic", "misanthropic", "revolution", "solanaceous", "unstoppably", "goggle", "tremor"].every((w) => lib.nearKnownName(w) === null));
check("lib: listed names plus ai or labs, neighboring-key slips, and outside-Latin letters are stopped", ["anthropicai", "openailabs", "revolutpay", "goigle", "micrpsoft", "pa" + cp(0xAB79) + "pal"].every((w) => lib.nearKnownName(w) !== null));
r = run("forge.mjs", ["--words", "work," + cp(0x0301), "--script", "any", "--min", "2"]);
check("forge: a combining mark on its own is not a word", r.code === 1 && /Letters only/.test(r.out));
r = run("forge.mjs", ["--mutate", "שלום", "--mine", "--script", "any"]);
check("forge: a mutation run that produces nothing exits 2", r.code === 2);
r = run("forge.mjs", ["--words", "bob,dad", "--min", "4", "--json"]);
let sa = null; try { sa = JSON.parse(r.out); } catch {}
check("forge: blends set aside by the sound heuristics are counted, not silent", r.code === 2 && sa && sa.set_aside && sa.set_aside.seam_or_mirror_heuristic >= 1 && sa.notes.some((n) => /Set aside, not stopped/.test(n)));
r = run("links.mjs", ["--names", "kinrail", "--tlds", "gtihub,gooogle,thepaypalapp,paypalpay"]);
check("links: endings get the same lookalike screen as names", r.code === 2 && (r.out.match(/Stopped ending/g) || []).length === 4);
r = run("links.mjs", ["--names", "काम", "--tlds", "भारत,বাংলা"]);
check("links: endings written with combining marks are accepted", r.code === 0 && /xn--h2brj9c/.test(r.out) && /xn--54b7fta0cc/.test(r.out));
check("links: an empty name list or ending list is an error, and ALL is all", run("links.mjs", ["--names", ",", "--tlds", "com"]).code === 1 && run("links.mjs", ["--names", "kinrail", "--tlds", ""]).code === 1 && /ClawHub/.test(run("links.mjs", ["--names", "kinrail", "--tlds", "com", "--surfaces", "ALL"]).out));
r = run("links.mjs", ["--names", cp(0x16A0) + cp(0x1681) + cp(0x16A0), "--tlds", "com"]);
check("links: two scripts outside the main list are reported as a mix", r.code === 2 && /mixed scripts \(Runic/.test(r.out) && /Ogham/.test(r.out));
r = run("links.mjs", ["--names", "kinrail", "--tlds", "eth,com", "--json"]);
let shape = null; try { shape = JSON.parse(r.out); } catch {}
check("links: every ending record carries kind and a notes array", shape && shape.names[0].endings.length === 2 && shape.names[0].endings.every((e) => ["name-system", "icann"].includes(e.kind) && Array.isArray(e.notes)));

// Document lint: the claims the card makes about itself, checked against the files.
import { readFileSync, readdirSync, existsSync } from "node:fs";
const root = join(here, "..");
const read = (f) => readFileSync(join(root, f), "utf8");
const card = read("SKILL.md");
const fmText = card.split("---")[1] || "";
const fmKeys = fmText.split("\n").map((l) => l.split(":")[0].trim()).filter(Boolean);
check("docs: frontmatter is exactly name, description, version", JSON.stringify(fmKeys) === JSON.stringify(["name", "description", "version"]), fmKeys.join(","));
const descMatch = fmText.match(/^description: "(.*)"$/m);
check("docs: description is one quoted line of 300 characters or fewer", Boolean(descMatch) && descMatch[1].length <= 300, descMatch ? String(descMatch[1].length) : "none");
const ledger = (s) => (s.match(/    Checks ledger\n(?:    .*\n)+/) || [""])[0];
check("docs: the ledger template in SKILL.md and blocks.md is identical", ledger(card) !== "" && ledger(card) === ledger(read("references/blocks.md")));
const textFiles = ["SKILL.md", "CHANGELOG.md", ...readdirSync(join(root, "references")).map((f) => "references/" + f), ...readdirSync(join(root, "scripts")).map((f) => "scripts/" + f)];
const dashes = textFiles.filter((f) => /[\u2013\u2014]/.test(read(f)));
check("docs: no em or en dashes in any file", dashes.length === 0, dashes.join(","));
const never = /\b(disabled|disability|dyslexi\w*|ambush\w*|orphan\w*|danger\w*|protocol\w*|non-human|enforce\w*|verdict\w*|finalist\w*|master\w*|bounty|bounties|dispatch\w*|ecosystem\w*|hq)\b/i;
const found = [];
for (const f of textFiles) {
  if (f === "scripts/selftest.mjs") continue; // this file names the words in order to look for them
  for (const line of read(f).split("\n")) if (never.test(line) && !/rather than bounty|rather than dispatch/.test(line)) found.push(`${f}: ${line.trim().slice(0, 60)}`);
}
check("docs: none of the words this skill never uses appear", found.length === 0, found.slice(0, 3).join(" | "));
const refs = [...(card + read("references/workflow.md")).matchAll(/\{baseDir\}\/([\w\/.-]+)/g)].map((m) => m[1]);
const missing = [...new Set(refs)].filter((r) => !existsSync(join(root, r)));
check("docs: every {baseDir} path in the card and workflow exists", missing.length === 0, missing.join(","));
const creditLines = card.split("\n").filter((l) => /^- \[.+\]\(https:\/\/en\.wikipedia\.org\/wiki\//.test(l));
check("docs: every lineage credit line carries a Wikidata Q-number link and the written URL", creditLines.length >= 5 && creditLines.every((l) => /\[Q\d+\]\(https:\/\/www\.wikidata\.org\/wiki\/Q\d+\) https:\/\/www\.wikidata\.org\/wiki\/Q\d+/.test(l)), creditLines.filter((l) => !/\[Q\d+\]/.test(l)).map((l) => l.slice(0, 40)).join(" | "));
check("docs: the workflow's surveillance test is the 'any answer' form", /If any answer is nobody, the operator, or no/.test(read("references/workflow.md")));
check("docs: the workflow's script lines use --json", (read("references/workflow.md").match(/scripts\/(forge|links)\.mjs[^\n]*--json/g) || []).length >= 2);
check("docs: no file says 'these three' about the trademark offices", !/these three/.test(read("references/workflow.md")) && !/these three/.test(read("scripts/links.mjs")));
check("docs: the card and the workflow agree on the availability statuses", /page-read/.test(card) && /page-read/.test(read("references/availability.md")) && /page-read/.test(read("references/blocks.md")));
check("docs: no file claims a check the scripts do not run", !/stops at any name that mixes scripts in the lookalike pattern or carries hidden characters\. If not/.test(card));

const failed = cases.filter((c) => !c.ok);
for (const c of cases) console.log(`${c.ok ? "pass" : "FAIL"}  ${c.name}${c.ok || !c.detail ? "" : `  (${c.detail})`}`);
console.log("");
console.log(`${cases.length - failed.length} of ${cases.length} passed. This self-test proves only what it tests; it is not an availability, trademark, language, or cultural check.`);
process.exit(failed.length ? 1 : 0);
