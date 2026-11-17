---
name: "tiktok-publish-flow"
description: "Post/publish TikTok videos and photos with TikTok music, edit captions, delete posts via Playwright on TikTok Studio web — no official API, no paid services. Use for TikTok automation, scheduled posting crons, photo posts with sound, caption edits."
license: "MIT"
homepage: "https://github.com/alexsax777/tiktok-publish-flow"
---

# TikTok publish flow — postare automată pe TikTok Studio via Playwright

_Corpul skill-ului e în română (limba de lucru a agentului care l-a construit); pașii, comenzile și selectorii sunt universali._

Fluxul VERIFICAT end-to-end (24.09 seara): 3 video + 1 foto-cu-muzică + 1 editare descriere, toate reușite, 0 credite. Sesiunea TikTok persistă în profilul Chromium ``TIKTOK_PROFILE_DIR` (default `~/.tiktok-poster/profile`)` — o dată logat (QR scanat din app), toate fluxurile rulează singure, fără re-login.

**Cine postează**: pentru automatizare (cron), un subagent dedicat face tot pipeline-ul inclusiv postarea (regula owner-ului: cronul postează prin subagent; sesiunea principală nu atinge TikTok decât la cerere explicită). **Înainte de orice postare**: verifică lista de pe `/tiktokstudio/content` — owner-ul poate posta manual în paralel (s-a întâmplat în producție); fără duplicate.

Scripturi (în `scripts/`, toate headed, profil persistent, portabile: `TIKTOK_PROFILE_DIR` / `TIKTOK_SHOTS_DIR` suprascriu căile default `~/.tiktok-poster/`):

## 1. Video — `scripts/tiktok_post3.py`

```bash
python3 <skill-dir>/scripts/tiktok_post3.py \
  --video <cale.mp4> --caption '<citat + emoji + #CitatulZilei #citate #motivatie #mindset #inspiratie #fyp>' --tag <tag-scurt>
```

Flux: `/tiktokstudio/upload` → `input[type=file]` → caption (contenteditable) → Escape + click neutral (închide popup) → privacy „Toată lumea"/Everyone → Post.

- ⭐ **Dialogul „Continue to post?"** („We're still checking your video...") apare după click pe Post. Trebuie click **„Post now"** imediat (în 1–2s de la apariție) — lăsat nesupravegheat se închide singur FĂRĂ să posteze (2 eșecuri consecutive înainte de fix). Scriptul poll-ează și apasă singur.
- Succes = redirect la `/tiktokstudio/content` + postarea apare după reload. Postările video primesc dialogul; cele foto de obicei nu.

## 2. Foto cu piesă TikTok — `scripts/tiktok_photo_music.py`

```bash
python3 .../tiktok_photo_music.py --image <cale.png> --caption '<citat + taguri>' --query '<mood EN pentru căutarea piesei>' --tag <tag-scurt>
```

- ⭐ **Tab-ul „Photos" se clickă ÎNAINTE de upload** — input-ul default are `accept=video/*` și ignoră silențios PNG-urile: FILE_SET apare în log, dar editorul de caption nu mai vine niciodată (diagnosticat în producție).
- Sunet: click pe butonul real `button:has-text("Add sound")` — click pe text cu `force=True` NU deschide panoul. Căsuța de căutare se ia DOAR din modal (`[role=dialog] input`, `input[placeholder*=earch]`) — primul `input[type=text]` de pe pagină e câmpul Description (titlu): query-ul scris acolo poluează titlul postării.
- Alegere piesă: click pe sugestia potrivită (ex. „golden hour jvke" → piesa JVKE), apoi **click JS pe primul buton „Use" vizibil** (`offsetParent !== null`; preferă rândul cu cuvântul-cheie din query). Click-ul Playwright normal dă timeout — 20 butoane „Use" găsite, toate cu TimeoutError, dropdown-ul de sugestii le acoperă; `.click()` prin evaluate merge.
- Dacă piesa nu se poate selecta → ABORT, nu posta fără muzică.

## 3. Editare descriere postare existentă — `scripts/tiktok_edit_post.py`

```bash
python3 <skill-dir>/scripts/tiktok_edit_post.py --match '<fragment caption curent>' --caption '<text nou complet>' --guard '<fragment din caption-ul curent pt. gard>'
```

- Găsește rândul pe `/content` după un fragment din caption (JS: text node → walk-up la strămoșul cu ≥4 svg și text scurt; **sortează candidații după `textContent.length` crescător** — strămoșul comun al mai multor rânduri e mai lung și altfel câștigă sortarea greșit).
- Creionul de editare = primul `span.px-icon` cu **x > 65% din lățimea viewport-ului** (coloana Actions; px-icon-urile din stânga rândului sunt badge-uri de thumbnail). Click prin `page.mouse.click(x, y)` la coordonate — `.click()` JS pe wrapper nu navighează.
- Se deschide `/tiktokstudio/upload/post/photo?item_id=<post_id>&from=creator_center` (URL direct navigabil odată cunoscut item_id).
- ⭐ **Gard anti-greșeală**: citește textul curent al editorului înainte de tastare; dacă NU conține caption-ul postării țintă → ABORT fără nicio modificare (a oprit editări pe rândul greșit în teste).
- Save cu butonul „Save" → status „**Under review**", postarea rămâne live în timpul re-verificării — normal, nu o reposta.

## Capcane verificate

- Rândurile din Content au doar **2 `<button>` reale** (privacy + 1) — pictogramele Actions sunt `span.px-icon` fără data-e2e/aria-label. Nu căuta butoane de acțiune în rând.
- Privacy dropdown-ul (Everyone/Friends/Only me) se deschide ușor din greșeală la click-uri în zonaActions — nimic nu se schimbă până nu alegi o opțiune; dă Escape.
- QCode QR de login: se capturează și se trimite pe WhatsApp, expiră în ~2–3 min („A expirat" → rulare nouă). Google OAuth e blocat în Chromium Playwright („browser not secure") — login TikTok doar prin QR din app, nu Google.
- Editarea postărilor video funcționează la fel ca foto (același creion); URL-ul de editare diferă doar prin item_id.

## Drum blocat: conectorul Higgsfield (nu reîncerca fără motiv)

Publicarea prin conector (`tiktok_prepare_publish` + publish-form widget) nu a mers niciodată end-to-end la Alex ): widget-ul „Approve TikTok post" rămâne cu Continue disabled + „Preview unavailable", aplicația Higgsfield nu afișează sesiunile de publish, sesiunea expiră în ~2h. Hosting-ul pentru conector (catbox.moe → `media_import_url` → URL cloudfront; presigned PUT pică cu InvalidToken) și scripturile CDP (`scripts/hf_*.py` în skill) rămân utile doar dacă TikTok/Higgsfield repară widget-ul. Regula consimțământului: conectorul cere confirmarea în publish-form; fluxul Playwright rulează sub autorizarea owner-ului contului.