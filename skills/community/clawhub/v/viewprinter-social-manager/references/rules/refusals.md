# refusals: Nothing was saved, and it is not a sales opening

## Priority: HIGH

## What goes wrong

`posts_save` comes back saying publishing is not set up on the account, and
the response is either to invent a pending state that does not exist, or to turn
the refusal into a pitch.

## Nothing was saved

The post does not exist in any partial state. There is nothing to clean up, and
nothing to tell the user is pending.

## Relay it as written, and stop

**Do not offer to sell anything, do not describe plans or prices, and do not go
looking for a signup, trial or upgrade link.**

You are running inside somebody else's client. Turning a refusal into a sales
pitch is unwelcome there, and it is against the rules of every app directory
this plugin is distributed through.

## Keep working on the rest

Connecting accounts, uploading media and every read stay available regardless.
Carry on with whatever part of the request still functions rather than treating
the whole thing as blocked.

## Context

- This is one specific refusal. Other errors — a malformed post, a group with a
  disconnected member — are ordinary failures; fix and retry those.
