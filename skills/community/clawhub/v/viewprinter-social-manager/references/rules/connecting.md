# connecting: Only the user can finish it

## Priority: MEDIUM

## What goes wrong

The agent tries to complete a connection it cannot complete, or polls
`accounts_connect` in a loop waiting for something that needs a human.

## The flow

`accounts_connect` returns a link. **You cannot complete the connection** — it
needs the person's own session and their consent on the platform's site.

Hand over the link, tell them to sign in and approve, and **stop**. Call
`accounts_connect` again afterwards and it reports the connected account.

**Do not poll.** Wait until they say they are done.

## Reconnecting is the same flow

Accounts fall out of authorisation on their own — tokens expire, permissions get
revoked, platforms change their terms. `accounts_list` and `groups_list` both
report which accounts are in that state.

There is no repair tool. Reconnecting is the same `accounts_connect` flow, and
it is the user's to complete.

## Context

- Start any posting work from `accounts_list`. Assuming an account is connected
  and discovering otherwise at schedule time wastes the whole composition.
