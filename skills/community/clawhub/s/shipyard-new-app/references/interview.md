# Interview

Ask at most 5 questions, one at a time, in plain words. Ask about outcomes, never technology choices (not "React or Vue", not "which database"). If the student rambles or dictates a long idea, that is fine: pull the answers out of it and only ask what is still missing. Always say which answer you recommend.

1. **Who is it for, and what problem does it solve?** ("Who will open this, and what do they want to get done?")
2. **What is the one main thing a person does in it?** Everything else is secondary. Build this first.
3. **How will it make money, if at all?** Free / paid subscribers / an email list / both. Free is the default. Payments and email lists come in a later step, so only note the answer in `SPEC.md`. Remind them that taking real payments needs Vercel Pro ($20 a month).
4. **Will people use it on phones, and should it be installable?** Recommend yes for most apps (phone-first layout and an install shortcut). Tools and dashboards used at a desk: sidebar layout. Site-like apps (content, a public face): top-nav layout.
5. **Is there a look you like?** A name, a website, a screenshot in the project folder. Note it in `SPEC.md`; the design step uses it right after the scaffold. If none, the design skill offers choices then.

If they already told you something, do not ask again. If they say "you decide", decide and say what you chose.

## What goes into SPEC.md

- One line: what the app is and who it is for.
- The main action, in one sentence.
- Features as a short numbered list, each small enough to build and check in one go. Mark "first version" and "later".
- Data: what is stored, and whose it is (almost always "each person's own").
- Money and email plans (note only).
- Look: the reference they gave, or "starter look".
- Hard rules: copy the list from `build-rules.md`.

## Plan

5 to 8 steps in plain words, for example: "1. Set up the app. 2. Add the list page. 3. Add the form. 4. Create the database. 5. Publish. 6. Check everything." End with: "Say 'go' and I will build it, or tell me what to change."
