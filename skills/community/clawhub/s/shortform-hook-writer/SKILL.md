---
name: shortform-hook-writer
description: Create natural, high-retention hooks and opening text for TikTok, Instagram Reels, YouTube Shorts, and slideshow/carousel-style short-form content in English and German.
license: MIT
homepage: https://github.com/wotaso/shortform-hook-writer-skill
metadata: {"author":"wotaso","version":"1.0.0","openclaw":{"homepage":"https://github.com/wotaso/shortform-hook-writer-skill","requires":{"bins":[]},"tags":["short-form","hooks","tiktok","reels","shorts","copywriting","german","english"]}}
---

# Shortform Hook Writer

## Use This Skill When

- writing hooks for TikTok, Instagram Reels, YouTube Shorts, Facebook Reels, or similar vertical short-form feeds
- creating first-slide text for TikTok photo mode, Reels slideshows, YouTube Shorts made from photos, carousels, or story-style image sequences
- turning a product, story, opinion, tutorial, app, offer, or personal experience into hook variants
- generating bilingual hooks in English and German
- auditing hooks for retention, naturalness, mobile readability, and platform-native tone

## Core Goal

Write hooks that feel like something a real creator would post, not like brand copy.

A good hook does four things quickly:

1. Names the viewer or situation.
2. Creates tension, curiosity, recognition, or emotional contrast.
3. Makes the next slide or next second feel necessary.
4. Fits visually inside a 9:16 mobile frame without becoming a paragraph.

Never promise virality. Optimize for stronger retention and testing velocity.

## Research Basis

Use these principles as the baseline:

- TikTok official creative guidance: build native vertical creative, use sound, stay inside safe zones, prefer people/UGC style, and place the proposition early. TikTok recommends a hook in the first 6 seconds and the content proposition in the first 3 seconds.
- Meta/Reels official guidance: Reels creative should be built for mobile, vertical, with audio and key messages in safe zones. Meta recommends testing and learning, and cites better results for 9:16 video with audio and safe-zone key messages.
- YouTube Shorts official guidance: Shorts are vertical or square, up to 3 minutes, built from quick multi-segment creation tools with text, voiceover, filters, audio, speed, green screen, and transitions. YouTube tracks engaged views separately so continued watching matters.
- Cross-platform creator practice: avoid slow intros, logos, generic greetings, and over-explaining. Start with the most charged part of the idea.

Source links for future checks:

- https://ads.tiktok.com/help/article/creative-best-practices
- https://www.facebook.com/business/ads/facebook-instagram-reels-ads
- https://support.google.com/youtube/answer/10059070
- https://support.google.com/youtube/answer/12948448
- https://support.google.com/youtube/answer/12948118

## Inputs To Ask For

Ask only for missing context that materially changes the hook. If the user gives enough, proceed.

Useful inputs:

- language: English, German, or both
- platform: TikTok, Instagram Reels, YouTube Shorts, or all
- format: talking head, slideshow/photo mode, screen recording, product demo, storytime, list, meme, tutorial, ad, organic post
- topic or offer
- target viewer
- desired emotion: curiosity, relief, anger, aspiration, embarrassment, humor, nostalgia, urgency, surprise
- proof available: personal experience, result, screenshot, review, before/after, data, demo
- taboo words, brand voice, legal restrictions

Default if unspecified:

- output English and German
- platform all short-form feeds
- format slideshow plus video-compatible hooks
- tone direct, conversational, slightly raw, not corporate

## Output Contract

For hook generation, return:

1. `Best Hooks`: 10 to 20 polished hooks.
2. `Hook Board`: grouped by structure, with English and German versions.
3. `Visual Open`: first frame or first slide direction for each top hook.
4. `Continuation`: what slide 2 or second 2 should reveal.
5. `Why It Works`: one short explanation per structure, not per hook.
6. `A/B Test Set`: 5 hooks that test different emotions while keeping the same body.
7. `Avoid`: weak hooks, overhyped hooks, and hooks that sound too AI-generated.

For a slideshow, include:

- Slide 1: hook text
- Slide 2: tension, contradiction, or setup
- Slide 3: proof or specificity
- Slides 4-6: payoff
- Final slide: save/comment/follow CTA, only if it feels native

For a video, include:

- on-screen text
- first visual
- voiceover first line
- cut/action in the first 1-2 seconds

## Hard Rules

- Keep the first on-screen hook short: usually 3 to 10 words.
- Use one idea per hook.
- Write for a person, not a demographic report.
- Make the hook understandable with sound off.
- Add motion or visual contrast in the first second when giving creative direction.
- Prefer concrete nouns and situations over abstract benefits.
- Use `you`, `I`, `this`, `nobody`, `stop`, `before`, `after`, `POV`, `I tried`, `I wish`, `the mistake`, `things I would never`.
- In German, use natural spoken German. Do not translate English hooks literally.
- If German audience is casual, default to `du`, not `Sie`.
- Do not use fake proof, fake numbers, fake screenshots, or fake personal claims.
- Do not use exploitative fear, medical certainty, financial certainty, or guaranteed-result claims.
- Do not open with `Welcome`, `In this video`, `Today I will show`, brand slogans, logos, or long context.

## Naturalness Rules

Hooks should feel human and specific. They should have a little friction.

Good:

- `POV: your camera roll knows you are not over it`
- `I almost deleted this photo`
- `This is why your room never feels clean`
- `Keiner sagt dir, dass Heilen so aussieht`
- `Ich dachte, ich bin faul. War ich nicht.`

Bad:

- `Unlock the ultimate strategy for better productivity`
- `This revolutionary tool will change your life`
- `Are you ready to transform your content journey?`
- `Maximize your results with these proven tips`
- `Du wirst nicht glauben, was als Naechstes passiert`

Remove or rewrite these AI/marketing words unless the user specifically wants ad copy:

- unlock
- transform
- revolutionary
- game changer
- ultimate
- elevate
- maximize
- leverage
- seamless
- powerful
- proven secrets
- skyrocket
- traction by a lot

## Hook Decision Tree

Use this when choosing the structure.

- If the topic is emotional or relatable: use `POV`, `nobody tells you`, `the moment when`, `you are not lazy`, `I thought it was X`.
- If the topic teaches something: use `stop doing X`, `3 signs`, `the mistake`, `do this before`, `I wish I knew`.
- If the topic sells an app/product: use `I stopped doing X manually`, `this fixed X`, `before/after`, `I tested X`, `what I use instead`.
- If the topic is a slideshow: use confession, contrast, tiny story, or first-person discovery.
- If the topic is controversial: use `unpopular opinion`, `hot take`, `this sounds wrong but`, `you are solving the wrong problem`.
- If the topic is aspirational: use `the routine that`, `things I changed`, `I did X for Y days`, `how I got from A to B`.
- If proof is weak: avoid big claims and use curiosity or process hooks instead.
- If proof is strong: lead with the specific result or before/after.

## Hook Structures

### 1. POV

Use when the viewer should instantly imagine themselves inside a situation.

English:

- `POV: you finally stopped chasing people`
- `POV: your app idea is not the problem`
- `POV: the trip made it out of the group chat`
- `POV: you are the friend who notices everything`
- `POV: your room exposes your mental state`

German:

- `POV: du rennst niemandem mehr hinterher`
- `POV: deine App-Idee ist nicht das Problem`
- `POV: der Urlaub hat den Gruppenchat ueberlebt`
- `POV: du bist die Person, die alles merkt`
- `POV: dein Zimmer verrät mehr als du willst`

### 2. Nobody Tells You

Use for hidden truths, emotional nuance, or non-obvious advice.

English:

- `Nobody tells you this part`
- `Nobody tells you how quiet progress feels`
- `Nobody tells you the boring part works`
- `Nobody tells you this before your first launch`
- `Nobody tells you healing can look like this`

German:

- `Das sagt dir vorher keiner`
- `Keiner sagt dir, wie leise Fortschritt ist`
- `Keiner sagt dir, dass der langweilige Teil wirkt`
- `Das sagt dir keiner vor deinem ersten Launch`
- `Keiner sagt dir, dass Heilung so aussehen kann`

### 3. I Wish I Knew

Use for lessons, mistakes, and tutorial content.

English:

- `I wish I knew this at 22`
- `I wish I knew this before buying it`
- `I wish I knew this before posting daily`
- `I wish I knew this before building my app`
- `I wish someone told me this earlier`

German:

- `Das haette ich mit 22 wissen muessen`
- `Das haette ich vor dem Kauf wissen sollen`
- `Das haette ich wissen muessen, bevor ich taeglich gepostet habe`
- `Das haette ich vor meiner ersten App wissen sollen`
- `Warum hat mir das keiner frueher gesagt?`

### 4. Stop Doing This

Use for correction, advice, tutorials, and product education.

English:

- `Stop planning your day like this`
- `Stop using your notes app for this`
- `Stop making hooks this polite`
- `Stop posting the finished version`
- `Stop trying to look productive`

German:

- `Plan deinen Tag nicht mehr so`
- `Hoer auf, deine Notizen-App dafuer zu benutzen`
- `Schreib Hooks nicht so brav`
- `Poste nicht nur die fertige Version`
- `Hoer auf, produktiv aussehen zu wollen`

### 5. The Mistake

Use when the viewer is probably doing something wrong but should not feel attacked.

English:

- `The mistake that made my videos invisible`
- `The mistake I kept calling discipline`
- `The mistake almost every beginner makes`
- `The mistake hiding in your morning routine`
- `The mistake was not the price`

German:

- `Der Fehler, der meine Videos unsichtbar gemacht hat`
- `Der Fehler, den ich Disziplin genannt habe`
- `Der Fehler, den fast alle am Anfang machen`
- `Der Fehler steckt in deiner Morgenroutine`
- `Der Preis war nicht das Problem`

### 6. Tiny Confession

Use for human, raw, slideshow-friendly hooks.

English:

- `I almost did not post this`
- `I kept this in my drafts for weeks`
- `I was embarrassed by this photo`
- `I thought I was the only one`
- `I still think about this message`

German:

- `Ich wollte das fast nicht posten`
- `Das lag wochenlang in meinen Entwuerfen`
- `Dieses Foto war mir peinlich`
- `Ich dachte, nur ich bin so`
- `Ich denke immer noch an diese Nachricht`

### 7. Specific Result

Use only when the result is true and can be supported.

English:

- `This saved me 6 hours last week`
- `This got 3x more saves than my normal posts`
- `I cut my edit time from 40 minutes to 8`
- `This one screen fixed my onboarding drop-off`
- `I changed one sentence and more people replied`

German:

- `Das hat mir letzte Woche 6 Stunden gespart`
- `Das bekam 3x mehr Saves als meine normalen Posts`
- `Ich habe meine Edit-Zeit von 40 auf 8 Minuten gedrueckt`
- `Dieser eine Screen hat mein Onboarding verbessert`
- `Ich habe einen Satz geaendert und mehr Leute haben geantwortet`

### 8. Wrong Assumption

Use when the viewer believes the wrong thing.

English:

- `You do not need more motivation`
- `Your content is not too niche`
- `The algorithm is not your first problem`
- `You are not bad at discipline`
- `Your app does not need more features yet`

German:

- `Du brauchst nicht mehr Motivation`
- `Dein Content ist nicht zu nischig`
- `Der Algorithmus ist nicht dein erstes Problem`
- `Du bist nicht schlecht in Disziplin`
- `Deine App braucht noch keine neuen Features`

### 9. Green Flags / Red Flags

Use for dating, lifestyle, tools, clients, creators, apps, habits.

English:

- `Green flags in a productivity app`
- `Red flags in a morning routine`
- `Green flags in someone who is actually healing`
- `Red flags in your content strategy`
- `Green flags in a first client`

German:

- `Green Flags bei einer Produktivitaets-App`
- `Red Flags in deiner Morgenroutine`
- `Green Flags bei jemandem, der wirklich heilt`
- `Red Flags in deiner Content-Strategie`
- `Green Flags beim ersten Kunden`

### 10. Ranked / Rated

Use for list content and slideshows.

English:

- `Rating my worst purchases`
- `Ranking hooks I would actually use`
- `Things in my room that expose me`
- `Apps I deleted after one week`
- `Outfits I thought were a personality`

German:

- `Ich bewerte meine schlimmsten Kaeufe`
- `Hooks, die ich wirklich benutzen wuerde`
- `Dinge in meinem Zimmer, die mich verraten`
- `Apps, die ich nach einer Woche geloescht habe`
- `Outfits, die ich fuer eine Persoenlichkeit hielt`

### 11. If You Are X

Use for audience targeting without sounding like an ad.

English:

- `If you overthink every text, watch this`
- `If your app has users but no retention`
- `If you are always tired after work`
- `If you post daily and nothing happens`
- `If you hate your own first drafts`

German:

- `Wenn du jede Nachricht zerdenkst`
- `Wenn deine App Nutzer hat, aber keine Retention`
- `Wenn du nach der Arbeit immer platt bist`
- `Wenn du taeglich postest und nichts passiert`
- `Wenn du deine ersten Entwuerfe hasst`

### 12. Before You X

Use when timing matters.

English:

- `Before you delete the app`
- `Before you buy another course`
- `Before you text them again`
- `Before you redesign your landing page`
- `Before you post that carousel`

German:

- `Bevor du die App loeschst`
- `Bevor du noch einen Kurs kaufst`
- `Bevor du ihnen wieder schreibst`
- `Bevor du deine Landingpage neu machst`
- `Bevor du diesen Carousel postest`

### 13. Hot Take

Use for opinionated content. Make the body fair and specific.

English:

- `Hot take: discipline is overrated`
- `Unpopular opinion: your hooks are too clean`
- `This sounds wrong, but discounts can hurt`
- `Most advice about consistency is useless`
- `Your niche is not boring. Your angle is.`

German:

- `Hot Take: Disziplin wird ueberschaetzt`
- `Unpopular Opinion: deine Hooks sind zu sauber`
- `Klingt falsch, aber Rabatte koennen schaden`
- `Die meisten Tipps zu Konsistenz bringen nichts`
- `Deine Nische ist nicht langweilig. Dein Winkel ist es.`

### 14. Mini Story

Use for content that has a beginning, turn, and payoff.

English:

- `I tried to fix my sleep and found the real problem`
- `I posted the ugly version and it worked better`
- `I asked 10 users why they quit`
- `I deleted one habit and my evenings changed`
- `I built the feature nobody clicked`

German:

- `Ich wollte meinen Schlaf fixen und fand das echte Problem`
- `Ich habe die haessliche Version gepostet und sie lief besser`
- `Ich habe 10 Nutzer gefragt, warum sie gegangen sind`
- `Ich habe eine Gewohnheit gestrichen und meine Abende wurden anders`
- `Ich habe das Feature gebaut, auf das niemand geklickt hat`

### 15. Painfully Specific

Use when the hook should feel like mind-reading.

English:

- `For the person with 47 unfinished notes`
- `For anyone who opens the app and instantly forgets why`
- `For founders refreshing Stripe at midnight`
- `For people who clean everything except the one corner`
- `For creators with a folder called final-final`

German:

- `Fuer die Person mit 47 unfertigen Notizen`
- `Fuer alle, die eine App oeffnen und sofort vergessen warum`
- `Fuer Founder, die nachts Stripe aktualisieren`
- `Fuer Leute, die alles putzen ausser diese eine Ecke`
- `Fuer Creator mit einem Ordner namens final-final`

## Slideshow Formula

For TikTok photo mode, Reels slideshows, or Shorts made from images, use this rhythm:

1. Slide 1: short hook with tension.
2. Slide 2: make the viewer feel seen or surprised.
3. Slide 3: add concrete proof, a screenshot, a messy detail, or a before state.
4. Slide 4: reveal the insight.
5. Slide 5: show the fix, list, or transformation.
6. Slide 6: end with a saveable takeaway or understated CTA.

Good first-slide patterns:

- `I almost missed this`
- `Save this before you need it`
- `The photo I did not understand until later`
- `This looked normal at first`
- `The slide nobody wants to admit`
- `Das sah erst ganz normal aus`
- `Speicher das, bevor du es brauchst`
- `Dieses Foto habe ich erst spaeter verstanden`
- `Die Folie will keiner zugeben`

Slideshow examples:

Example 1, personal growth:

- Slide 1: `I thought I was lazy`
- Slide 2: `Then I noticed when it happened`
- Slide 3: `Only after people-pleasing days`
- Slide 4: `My body was not avoiding work`
- Slide 5: `It was avoiding another performance`
- Slide 6: `Rest is not always the problem`

German:

- Slide 1: `Ich dachte, ich bin faul`
- Slide 2: `Dann habe ich gemerkt, wann es passiert`
- Slide 3: `Immer nach People-Pleasing-Tagen`
- Slide 4: `Mein Koerper hat Arbeit nicht vermieden`
- Slide 5: `Er hat die naechste Rolle vermieden`
- Slide 6: `Ruhe ist nicht immer das Problem`

Example 2, app/product:

- Slide 1: `I stopped tracking habits like this`
- Slide 2: `Because I kept lying to myself`
- Slide 3: `A perfect streak taught me nothing`
- Slide 4: `So I started tracking the trigger`
- Slide 5: `Now I know what breaks the habit`
- Slide 6: `Track causes, not just checkmarks`

German:

- Slide 1: `Ich tracke Gewohnheiten nicht mehr so`
- Slide 2: `Weil ich mich selbst angelogen habe`
- Slide 3: `Eine perfekte Serie hat mir nichts gezeigt`
- Slide 4: `Also tracke ich jetzt den Ausloeser`
- Slide 5: `Jetzt weiss ich, was die Gewohnheit bricht`
- Slide 6: `Tracke Ursachen, nicht nur Haken`

Example 3, creator/content:

- Slide 1: `Your hook is too polite`
- Slide 2: `It waits for permission`
- Slide 3: `People scroll before context`
- Slide 4: `Start with the uncomfortable part`
- Slide 5: `Then explain why it is true`
- Slide 6: `Rewrite the first slide first`

German:

- Slide 1: `Dein Hook ist zu brav`
- Slide 2: `Er wartet auf Erlaubnis`
- Slide 3: `Leute scrollen vor dem Kontext`
- Slide 4: `Starte mit dem unbequemen Teil`
- Slide 5: `Dann erklaerst du, warum es stimmt`
- Slide 6: `Schreib zuerst Slide 1 neu`

## Visual Direction Rules

For every top hook, pair the text with a visual open:

- close-up of the object/result/problem
- screenshot with one part blurred or circled
- face already reacting, not waiting to talk
- hand entering frame immediately
- messy before state
- quick zoom into the surprising detail
- first slide with high-contrast text and a real photo behind it
- screen recording already mid-action, not on a home screen

Avoid:

- blank title cards
- slow cinematic pans
- logo intros
- perfectly centered product beauty shots as the first frame
- text blocks that cover the whole screen
- tiny caption text near platform UI

## Mobile Text Rules

- Use 3 to 10 words on the first frame when possible.
- Keep important text away from the bottom caption area and right-side buttons.
- Use high contrast.
- Break long German compounds across lines if needed.
- For slideshows, let each slide carry one sentence or one emotional beat.
- If a hook needs more than 12 words, split it into Slide 1 and Slide 2.

## German Style Guide

German hooks should sound spoken, not translated.

Prefer:

- `Das sagt dir keiner`
- `Ich dachte, ich bin das Problem`
- `Hoer auf, das so zu machen`
- `Wenn du alles zerdenkst`
- `Das ist der eigentliche Fehler`
- `Ich hab das erst zu spaet verstanden`

Avoid:

- `Entsperre dein volles Potenzial`
- `Revolutioniere deinen Alltag`
- `Maximiere deine Produktivitaet`
- `Dieses Tool wird dein Leben veraendern`
- `Du wirst nicht glauben`

Use `krass`, `ehrlich`, `komisch`, `wild`, `unangenehm`, `brav`, `kaputtoptimiert`, `zerdenken`, and `hinterherrennen` when they fit the audience. Do not force slang.

## English Style Guide

English hooks should sound direct and lived-in.

Prefer:

- `I thought I was the problem`
- `This felt stupid until it worked`
- `Stop making this so complicated`
- `The boring version worked better`
- `I kept ignoring this`

Avoid:

- `Unlock your potential`
- `Here is the ultimate guide`
- `Boost your productivity instantly`
- `This will change your life`
- `You will not believe what happened`

## Product And App Hook Examples

English:

- `I stopped using spreadsheets for this`
- `This is why users quit after day one`
- `The onboarding screen I should have deleted`
- `I built the feature nobody asked for`
- `Your paywall is answering the wrong question`
- `This tiny button changed the whole flow`
- `I asked users what confused them`
- `The app was fine. The promise was not.`
- `Before you add another feature`
- `If your app gets downloads but no habits`

German:

- `Ich nutze dafuer keine Tabellen mehr`
- `Darum sind Nutzer nach Tag 1 weg`
- `Der Onboarding-Screen, den ich haette loeschen sollen`
- `Ich habe das Feature gebaut, das keiner wollte`
- `Deine Paywall beantwortet die falsche Frage`
- `Dieser kleine Button hat den Flow veraendert`
- `Ich habe Nutzer gefragt, was sie verwirrt`
- `Die App war okay. Das Versprechen nicht.`
- `Bevor du noch ein Feature baust`
- `Wenn deine App Downloads bekommt, aber keine Gewohnheit wird`

## Lifestyle And Relatable Hook Examples

English:

- `I was not tired. I was overstimulated.`
- `The clean girl routine did not survive my Monday`
- `This corner of my room explains everything`
- `I kept buying solutions for the wrong problem`
- `A weirdly specific sign you need a reset`
- `I romanticized my life for 7 days`
- `The habit that made evenings feel longer`
- `I deleted this and slept better`
- `For anyone who feels behind for no reason`
- `Nobody talks about the after part`

German:

- `Ich war nicht muede. Ich war ueberreizt.`
- `Die Clean-Girl-Routine hat meinen Montag nicht ueberlebt`
- `Diese Ecke in meinem Zimmer erklaert alles`
- `Ich habe Loesungen fuer das falsche Problem gekauft`
- `Ein komisch spezifisches Zeichen fuer einen Reset`
- `Ich habe mein Leben 7 Tage romantisiert`
- `Die Gewohnheit, durch die Abende laenger wirken`
- `Ich habe das geloescht und besser geschlafen`
- `Fuer alle, die sich grundlos hinten dran fuehlen`
- `Ueber den Teil danach spricht keiner`

## Creator And Business Hook Examples

English:

- `Your content sounds like a brochure`
- `The first slide is doing too much`
- `I rewrote 30 hooks. These won.`
- `Your niche is not the reason`
- `The ugly draft had the best angle`
- `I stopped posting tips and started posting tension`
- `The hook should not explain. It should pull.`
- `This is why your carousel gets likes but no saves`
- `The line I would cut from every ad`
- `Founders keep making this content mistake`

German:

- `Dein Content klingt wie ein Flyer`
- `Die erste Slide will zu viel`
- `Ich habe 30 Hooks umgeschrieben. Diese waren besser.`
- `Deine Nische ist nicht der Grund`
- `Der haessliche Entwurf hatte den besten Winkel`
- `Ich habe aufgehoert Tipps zu posten und Spannung gepostet`
- `Der Hook soll nicht erklaeren. Er soll ziehen.`
- `Darum bekommt dein Carousel Likes, aber keine Saves`
- `Diesen Satz wuerde ich aus jeder Ad streichen`
- `Founder machen diesen Content-Fehler staendig`

## Hook Audit Checklist

Score each hook from 0 to 2:

- Viewer fit: would the target viewer know it is for them?
- Tension: is there a reason to keep watching?
- Specificity: could this only apply to this topic or audience?
- Brevity: can it be read in one glance?
- Native tone: does it sound like a creator, not a brand?
- Visual potential: is there an obvious first image or motion?
- Payoff promise: is there a clear next beat?
- Integrity: is the claim true or supportable?

Interpretation:

- 13-16: strong test candidate
- 9-12: usable but needs sharper wording or stronger visual
- 0-8: rewrite

## Rewrite Process

When improving weak hooks:

1. Remove the intro.
2. Replace abstract benefit with concrete situation.
3. Add a person, moment, mistake, contradiction, or proof.
4. Cut filler words.
5. Make it sound like a text a creator would send to a friend.
6. Create 5 variants with different emotional angles.

Example:

Weak:

- `How to improve your productivity with better task management`

Better:

- `Your to-do list is lying to you`
- `I stopped planning my day by tasks`
- `The mistake hiding in your to-do list`
- `Your list is full. Your day is not planned.`
- `Du planst Aufgaben, nicht Energie`

## A/B Testing Guidance

For one video body, test hooks across different emotional mechanisms:

- recognition: `If you keep rewriting the same note`
- contradiction: `Your notes app is making this worse`
- confession: `I kept pretending this system worked`
- result: `This cut my planning time in half`
- warning: `Before you rebuild your routine again`

Keep the rest of the video or slideshow the same when testing hook performance.

Track:

- 1-second hold or thumb-stop if available
- 3-second view rate
- average watch time
- completion rate
- rewatches
- saves
- shares
- profile clicks or conversions if commercial

## Response Templates

### Hook Pack

```text
Context:
- Platform:
- Format:
- Audience:
- Desired emotion:

Best hooks:
1.
2.
3.

German versions:
1.
2.
3.

Top visual opens:
1.
2.
3.

Slide/video continuation:
1.
2.
3.

A/B set:
- Curiosity:
- Relatable:
- Contrarian:
- Proof:
- Confession:

Avoid:
-
-
```

### Slideshow Script

```text
Slide 1:
Slide 2:
Slide 3:
Slide 4:
Slide 5:
Slide 6:

Caption:
CTA:
```

### Hook Audit

```text
Original:
Score:
Problem:
Rewrite:
Why:
```

## Final Quality Bar

Before returning hooks, silently check:

- Would this make sense in the first second without context?
- Is the strongest word near the beginning?
- Does the hook create a next-question?
- Does it avoid fake certainty?
- Does it sound natural in the requested language?
- Can it fit as large mobile text?
- Is there a concrete visual for the first frame?

If the answer is no, rewrite before showing the user.
