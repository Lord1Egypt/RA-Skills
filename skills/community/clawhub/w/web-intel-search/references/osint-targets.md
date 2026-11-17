# OSINT by Target Type

Pick the target type, use the matching source pack, and keep the same verification and privacy
rules from `SKILL.md`. A hit is a lead, not proof. Check dates, cross-link identifiers, and prefer
primary sources.

## Meta-hubs and aggregators
Use these to route to the right source; they are indexes, not evidence.
- **OSINT Framework** (`osintframework.com`, `github.com/lockfale/osint-framework`) - tool tree by
  target type.
- **MetaOSINT** (`metaosint.github.io`) - ranked index of OSINT tools by task.
- **Bellingcat Toolkit** (`bellingcat.gitbook.io/toolkit`) - investigation, geolocation,
  verification, and archiving.
- **IntelTechniques** (`inteltechniques.com/tools`) - search tools and people/company lookups.
- **GIJN Online Research Tools** (`gijn.org/resource/online-research-tools`) - investigative guides
  and directories.
- **Sector035 Week in OSINT** (`sector035.nl`) - weekly OSINT tools, techniques, and community
  updates.
Cite the original source you actually used, not the hub.

## Deep web, dark web, and research aggregators
Deep web content is gated or unindexed (databases, records, libraries); the dark web is Tor/I2P.
Use lawful public access only. Do not buy, download, or redistribute illegal data, breach dumps, or
PII. For Tor, use Tor Browser, keep JavaScript disabled, never log in with a real identity, and
verify every `.onion` address against an independent official source.
- **Ahmia** (`ahmia.fi`) - filtered onion search engine; search from clearnet, open results in Tor.
- **Onion Search Engine** (`onionsearchengine.com`) - filtered, script-light onion search; use the
  official `.onion` mirror linked from its clearnet page.
- **DeepDarkCTI** (`deepdarkcti.com`, `github.com/fastfire/deepdarkCTI`) - curated index of
  deep/dark-web CTI sources; authorized monitoring only, never access illegal content.
- **SecureDrop Directory** (`securedrop.org/directory`) - verified legitimate newsroom onion
  services.
- **Intelligence X** (`intelx.io`) - search Tor, I2P, public leaks, and the web by email, domain,
  IP, CIDR, or Bitcoin address; legal/authorized use only, no PII redistribution.
- Commercial deep/dark-web intelligence: **DarkOwl** (`darkowl.com`) and **Flashpoint**
  (`flashpoint.io`) - licensed datasets and APIs; require legal review, contractual access, and
  strict no-credential-use rules.
- **ExoneraTor** (`metrics.torproject.org/exonerator.html`) - check whether an IP was a Tor relay
  at a given time; useful for attribution and false-positive checks.
- **Tor Metrics** (`metrics.torproject.org`) - relay/onion-service statistics, censorship, and
  network health; use for context, not attribution.
- Academic aggregators: **CORE** (`core.ac.uk`), **BASE** (`base-search.net`), **OpenAIRE**
  (`explore.openaire.eu`) - open-access papers and research outputs.
- Books and libraries: **HathiTrust** (`babel.hathitrust.org`), **WorldCat**
  (`search.worldcat.org`) - digitized books, editions, and library holdings; full text may be
  restricted.
- FOIA and documents: **MuckRock** (`muckrock.com`, US), **WhatDoTheyKnow**
  (`whatdotheyknow.com`, UK), **FragDenStaat** (`fragdenstaat.de`, DE), **DocumentCloud**
  (`documentcloud.org`) - requests, releases, and investigative documents.
- Court records: **CourtListener/RECAP** (`courtlistener.com`) - US opinions and PACER dockets;
  verify access, jurisdiction, and redaction before relying on a filing.
- Corporate and public records: **GLEIF** (`gleif.org`) - global Legal Entity Identifiers;
  **LittleSis** (`littlesis.org`) - corporate/political relationships; **OpenSecrets**
  (`opensecrets.org`) and **FollowTheMoney** (`followthemoney.org`) - US political finance.
Cite the underlying record; aggregators are discovery aids, not evidence.

## Domain / website
- WHOIS/RDAP (`rdap.org`, `whois`), historical WHOIS, registrar and creation date.
- DNS: A/AAAA/MX/NS/TXT/SOA/CNAME, zone-transfer attempt (authorized), DNSSEC.
- Certificate transparency: `crt.sh`, Cert Spotter, Censys, `ssl:` pivots.
- Subdomains: passive DNS (SecurityTrails, VirusTotal), CT logs, subfinder/amass/assetfinder,
  `bbot`, `chaos`.
- Archives: Wayback CDX API, archive.today, Common Crawl index.
- Tech fingerprint: WhatWeb, Wappalyzer, httpx, response headers, favicon hash.
- Source-code search: **PublicWWW** (`publicwww.com`) - HTML/JS snippets, analytics IDs, and
  technologies across sites; respect site terms and do not collect PII at scale.
- URLs/params: gau, waybackurls, katana, urlscan.io, VirusTotal.
- Reputation: Google Safe Browsing, URLhaus, PhishTank, OpenPhish, **PhishStats**
  (`phishstats.info`), Talos.

## IP / ASN / network
- Geolocation and ownership: ipinfo, ipapi, RIPEstat, BGP.he.net, PeeringDB.
- Reverse DNS, passive DNS, TLS certs on the IP.
- Shodan/Censys/FOFA/ZoomEye host detail; InternetDB for a quick summary.
- Reputation: AbuseIPDB, GreyNoise, AlienVault OTX, ThreatFox, Spamhaus.
- Neighbor discovery: same /24, same ASN, same org, shared certificates.

## Email
- Validate syntax/MX/SMTP (carefully, no spam), catch-all detection.
- Breach exposure: Have I Been Pwned (API or web), DeHashed, LeakCheck, BreachDirectory.
- Infostealer exposure: **Hudson Rock Cavalier** (`cavalier.hudsonrock.com`) - infected-machine and
  stealer-log intelligence by domain/email; authorized/legal use only, never use credentials.
- Account discovery: holehe, GHunt (Google), Epieos; Gravatar MD5 lookup; PGP keyservers.
- Format inference from public sources; verify before relying on it.
- Never redistribute breach data; report exposure, not dumps.

## Username / person
- Username enumeration: WhatsMyName (700+), Sherlock, Maigret (3000+), Namechk, Blackbird,
  social-analyzer. Expect false positives; confirm by profile content and cross-links.
- Social platforms: X/Twitter, LinkedIn, Facebook, Instagram, TikTok, Reddit, Telegram, Discord,
  BlueSky, Mastodon, YouTube, GitHub, Strava.
- Social/Telegram analytics: **TGStat** (`tgstat.com`), **Telemetr.io** (`telemetr.io`),
  **Social Searcher** (`social-searcher.com`) - channel/profile and mention discovery; verify
  current data, provenance, and privacy before use.
- Public records: company registries, court records, sanctions/PEP lists, news archives.
- Correlation: reused bio, avatar hash, writing style, timezone/activity pattern, linked domains.
- Respect privacy: focus on public, relevant, lawful information; avoid harassment or doxxing.

## Phone
- Carrier/line type: PhoneInfoga, numverify, Twilio Lookup, carrier public lookups.
- Messaging-app presence: WhatsApp/Telegram/Signal checks (careful, may notify).
- Breach and social correlation; validate against public records.
- Country/format normalization (E.164) before searching.

## Image / video / geolocation
- Metadata: exiftool, `identify -verbose`, JPEGsnoop; GPS, device, timestamps, edit history.
- Reverse image: Google Lens, Yandex (strong for faces/objects), Bing Visual Search, TinEye,
  Baidu (China), PimEyes (face; ethical/legal constraints).
- Geolocation from pixels: signage, license plates, bollards, vegetation, architecture, shadows
  and sun angle (SunCalc), Street View/Mapillary/Overpass.
- Video: frame extraction (ffmpeg), keyframe metadata, audio fingerprinting, subtitle/OCR.
- Preserve original files; hashes and metadata can be altered by screenshots.

## Company / organization
- Registries: OpenCorporates, Companies House (UK), SEC EDGAR (US), local business registries.
- Corporate tree: subsidiaries, acquisitions, filings, annual reports.
- Employees/tech stack: LinkedIn, job postings, engineering blogs, GitHub orgs.
- IP/intangible assets: trademark (USPTO, EUIPO, WIPO), patents (Google Patents, Espacenet).
- Risk: sanctions (OFAC, EU, UN), litigation, adverse media, leak databases.
- Sanctions/PEP aggregation: **OpenSanctions** (`opensanctions.org`) - 470+ watchlists and PEP
  sources, 2M+ entities; verify match quality, names are not unique.
- Investigative datasets: **OCCRP Aleph** (`aleph.occrp.org`) - 219 public datasets and public
  records; **ICIJ Offshore Leaks** (`offshoreleaks.icij.org`) - 810k+ offshore entities.
  Use lawful public access; do not redistribute personal data.
- Beneficial ownership: **Open Ownership** (`openownership.org`) - guidance and the Beneficial
  Ownership Data Standard (`standard.openownership.org`); not a global register, so use national
  registries and OpenSanctions/Aleph for records.
- Infrastructure: domains, ASNs, certificates, cloud buckets, mobile apps.

## Chinese-language and gated databases
- Academic: **CNKI** (`cnki.net`), **Wanfang** (`wanfangdata.com.cn`), **VIP** (`cqvip.com`),
  **NSTL** (`nstl.gov.cn`) - journals, theses, standards, patents; subscription or document
  delivery, authorized access only.
- Corporate: **National Enterprise Credit Information Publicity System** (`gsxt.gov.cn`),
  **Qichacha** (`qcc.com`), **Tianyancha** (`tianyancha.com`), **Aiqicha**
  (`aiqicha.baidu.com`) - official registry vs commercial aggregators; verify identifiers and
  respect terms/anti-scraping controls.
- Patents: **CNIPA** (`cnipa.gov.cn`) and the CNIPA patent search system
  (`pss-system.cponline.cnipa.gov.cn`) - Chinese patents and legal status.
- Courts: **China Judgements Online** (`wenshu.court.gov.cn`) - published judgments; access
  varies, documents may be removed, and PII must be redacted.
- Many of these databases block automated access or require real-name/paid accounts. Use a
  browser, lawful credentials, and the minimum data necessary.

## Cryptocurrency
- Explorers: Etherscan, Blockchain.com, Blockchair, Solscan, Mempool.space.
- Clustering: reused addresses, change addresses, exchange deposit tags.
- Attribution: sanctions lists, court records, chain-analysis blogs.
- Entity labeling: **Arkham Intelligence** (`arkm.com`) - address/entity intelligence; labels are
  leads, verify independently, and use only for lawful fraud/AML investigations.
- Never deanonymize private individuals; focus on fraud/AML use cases.

## Flights / ships / physical
- Flights: FlightRadar24, ADS-B Exchange, OpenSky Network (ICAO hex vs tail number).
- Ships: MarineTraffic, VesselFinder, Equasis (IMO vs MMSI), port calls.
- Satellites: Sentinel Hub, Google Earth, historical imagery.
- Maps: OpenStreetMap, Overpass Turbo, Google Street View, Mapillary.

## Privacy and ethics
- Collect only what is necessary for the stated, lawful objective.
- Do not access private accounts, bypass access controls, or use leaked credentials.
- Redact PII and sensitive identifiers in reports.
- Verify before publishing; avoid misidentification and reputational harm.
