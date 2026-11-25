# Position review

Use when the user asks whether to hold, add to, or close an existing position.

1. **Ask first, analyse second.** "What is your stop, your target, and your
   planned exit date?" If the journal or idea log has them (with the journal:
   `trade --json show <id>` or `trade --json positions`), confirm them with
   the user instead of asking.
   Do not give a view before you know the stop.
2. **Find the original thesis**: the idea card in the idea log, or with the
   journal the trade's `notes`, its `idea-*` tag and the matching plan entry. If there is none, write down the user's
   thesis now and record it.
3. **Check each exit trigger** from the idea card. Has any fired? Cite the
   event with date and source.
4. **Re-run a mini scan** limited to the thesis's drivers (sections of the
   macro checklist that the thesis depends on), plus the calendar until the
   time stop.
5. **State the trade as it stands now**: distance to stop and target from the
   current price, R multiple, days left to time stop, binary events ahead.
   Take P&L from the journal (`trade --json positions`) or the user's broker,
   never compute it by hand.
6. **Scenarios**: for each upcoming binary event, what happens to the
   position in each outcome and what the plan is.
7. **View**: thesis holds / weakened / broken. If broken, the default is to
   exit (risk rule 7); say what would have to be true to argue otherwise.
8. **Record** the review: a `REVIEW` entry in the idea log, or with the
   journal `trade --json journal add "<review>" --ticker T --kind review
   --tags <idea id>,ai-idea`. If the thesis broke, also add a lesson
   (`LESSON` entry / `--kind lesson`).

## Long-term portfolio (DCA / periodic contributions)

For investors who add money on a schedule rather than trade ideas:

1. Get holdings from the journal (`trade --json positions`) or from the user
   (a paste or broker export), and the stated target allocation. If there is
   no target allocation, ask for it and record it (idea log or a journal
   `--kind plan` entry).
2. Compare current weights with the targets (same currency method as risk
   rule 6, and say which one you used).
3. Run a short macro scan limited to what affects the holdings (rates,
   valuations, currency) and check each holding's original thesis as in the
   steps above. A long-term holding still needs an invalidation condition,
   even if it is not a price stop.
4. Suggest where the contribution goes as a rebalancing rule ("underweight
   bucket first"), not as a market call, and record the review.
