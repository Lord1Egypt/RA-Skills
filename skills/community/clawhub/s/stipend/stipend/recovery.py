"""Who owns fixing this.

Three people on Moltbook arrived at the same missing thing independently, and
the sharpest way it was put was this:

    "the cap is a static line, not a state machine"

Every limit here could say what it refused. None of them could say what happens
next, or whose job it was. So an agent that hit a cap had two options that look
identical from inside the model: give up, or rephrase and try again. The second
is the behaviour we spend the rest of this package trying to prevent, and we
were leaving it as the only obvious move.

Recovery has exactly four owners, and every failure names one:

    agent       Safe to act on now, without asking anyone. Send less, or retry.
    time        Nobody needs to do anything. It clears on its own, at a stated
                moment. A daily cap is not a problem to be solved.
    human       Needs a decision or money. The agent cannot resolve it and
                should stop trying — that is the whole point of the limit.
    reconcile   The outcome is unknown. One command finds out, and it must be
                run before anything else moves.

The distinction that matters most is `time` versus `human`. An agent told only
"refused" treats a daily cap as an obstacle to route around. An agent told "this
clears at midnight UTC, nobody needs to do anything" does not.

Nothing here is a control. It changes no decision and grants no permission — it
is the sentence the refusal was always missing.
"""

from datetime import datetime, timedelta, timezone

AGENT = "agent"
TIME = "time"
HUMAN = "human"
RECONCILE = "reconcile"


def _midnight_utc():
    now = datetime.now(timezone.utc)
    return (now + timedelta(days=1)).replace(hour=0, minute=0, second=0,
                                             microsecond=0)


# kind -> (owner, what to do, may the agent simply try again)
_OWNERS = {
    "allowlist": (
        HUMAN,
        "Only your human can widen the destination allowlist. Do not retry: "
        "this address is refused by configuration, not by circumstance.",
        False),
    "over_per_transaction": (
        AGENT,
        "Send an amount at or under the per-transaction cap. Splitting one "
        "payment into several to get around the cap will hit the daily and "
        "per-recipient limits instead, which is intended.",
        True),
    "over_daily": (
        TIME,
        "The daily allowance is spent. It resets at midnight UTC and nobody "
        "has to do anything for that to happen.",
        False),
    "over_counterparty": (
        TIME,
        "Today's allowance for this recipient is spent. It resets at midnight "
        "UTC. Payments to other recipients are unaffected.",
        False),
    "needs_confirmation": (
        HUMAN,
        "This amount needs a one-time approval from your human before it can "
        "be sent.",
        False),
    "new_destination": (
        HUMAN,
        "First payment to an address needs a human to confirm it once. After "
        "that the address is known and payments flow normally.",
        False),
    "lapsed_destination": (
        HUMAN,
        "This address has not been paid in months, so its confirmation has "
        "expired and a human has to renew it. Nothing is known to be wrong "
        "with the address; trust simply does not last forever unused.",
        False),
    # not policy refusals, but the same question is asked of them
    "unresolved_payment": (
        RECONCILE,
        "A payment was sent and never confirmed. Run `stipend payout resolve` "
        "before anything else moves — it asks what actually happened rather "
        "than assuming.",
        False),
    "pending_unreadable": (
        HUMAN,
        "The outstanding-payment record is damaged, so a payment may or may "
        "not have gone out. A human should check the recipient's balance "
        "before deleting it.",
        False),
    "insufficient_funds": (
        HUMAN,
        "The wallet does not hold enough. Only a human can add funds.",
        False),
    "no_credits": (
        HUMAN,
        "No gas credits and no ETH, so nothing can be broadcast. A human can "
        "buy credits; alternatively the referral commission pays in credits.",
        False),
    "locked_out": (
        AGENT,
        "Another payment holds the lock. Wait for it and try again — this is "
        "the limits being measured correctly, not a failure.",
        True),
}


def ownership(kind):
    """Who owns this failure, what happens next, and whether to try again.

    Unknown kinds default to the human. Guessing that an unrecognised failure
    is safe for an agent to retry is the one wrong answer available here.
    """
    owner, what, retryable = _OWNERS.get(
        kind,
        (HUMAN,
         "Unrecognised failure. Treated as needing a human, because assuming "
         "otherwise would make retrying the default for things we do not "
         "understand.",
         False))
    out = {
        "owner": owner,
        "what_happens_next": what,
        "agent_may_retry": retryable,
    }
    if owner == TIME:
        out["clears_at"] = _midnight_utc().isoformat()
    return out


def line(kind):
    """One sentence to append to a refusal message."""
    o = ownership(kind)
    who = {
        AGENT: "You can resolve this yourself.",
        TIME: "Nobody needs to act; this clears at midnight UTC.",
        HUMAN: "This one is your human's to resolve, not yours.",
        RECONCILE: "The outcome is unknown until you reconcile it.",
    }[o["owner"]]
    return "%s %s" % (who, o["what_happens_next"])
