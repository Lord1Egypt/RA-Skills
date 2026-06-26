# Things Plus Integrated Test Prompt

Run one realistic end-to-end test that covers the core workflows: pre-flight, capture, deduping, scheduling, deadlines, recurring tasks, checklist handling, project placement, tag behavior, read-back, updates, deletes, recommendations, and cleanup.

## Main integrated prompt

I'd like to use Things as my default to-do system.

Help me add the following:
- I need to finish the Q3 report today.
- I have to submit the expense claim before Friday.
- I want to find time to review the onboarding docs for the new project.
- I'd like to read "Atomic Habits" at some point.
- I also have a vague item called "presentation" — help me break it down into something more actionable.

A few things have specific times:
- remind me tomorrow at 8am to join the standup call;
- remind me tomorrow afternoon to follow up with the client;
- remind me tonight to prep my bag for tomorrow;
- remind me on March 28 to renew my gym membership;
- remind me tomorrow at 9am to submit the expense claim — and the deadline for that is also tomorrow.

I also have some recurring tasks:
- review my weekly priorities every Monday morning;
- pay rent on the 1st of every month;
- log work hours every evening;
- do a weekly inbox zero cleanup.

Add a few more structured tasks:
- buy a desk lamp, tagged "shopping" and "home office";
- prepare for tomorrow's team sync with subtasks: update the slide deck, review action items, test screen sharing;
- put "compile Q3 metrics and update dashboard" into a project called "Q3 Review";
- put "book an eye exam" under "Personal Health".

Assume I may already have an expense-claim task — don't create a duplicate if an obvious open match already exists.

Once everything is added, show me:
- what's in Today,
- anything due soon,
- anything related to the expense claim,
- my current projects,
- my current tags.

Then update a few existing tasks:
- rename "submit form" to "submit reimbursement form";
- add a note to "confirm time with manager" saying "also ask about the team offsite dates";
- add a "logistics" tag to "pick up package";
- move the reminder for "send weekly update" to tomorrow at 8am;
- update the deadline for "expense claim" to this Friday.

Finally, delete "buy coffee pods".

I'm feeling a bit overwhelmed with today — tell me which tasks make sense to keep in Today and which ones could be pushed back. Don't move anything yet, just give me a recommendation.

After all that, delete everything added in this test run, including the new one-off tasks, the recurring items, the new projects, and any new tags. Do not stop at the first delete attempt: re-check search/results after cleanup and retry if anything remains. Only report cleanup complete after the final read-back is empty. If anything still cannot be deleted after retries, list the exact leftovers explicitly.

## Supplementary prompt — missing target safety

Try to update these tasks if they exist, but don't invent duplicates if they don't:
- submit form
- confirm time with manager
- pick up package
- send weekly update
- buy coffee pods

If any are missing, say so clearly.
