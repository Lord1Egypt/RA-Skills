# Hand-off, takeover and resuming

## When the assistant escalates

The knowledge does not answer a question about a price, stock, a deadline, a promise, a commitment or a policy, the customer asks for a person, is upset or hostile, asks something outside the business, brings up a payment problem, a refund or exchange, a complaint or a legal matter (or asks the assistant to promise or confirm something in writing), two replies in a row did not get the customer closer to what they need, or the message is a file with no text that cannot be read. The decision carries `escalate`; the helper does the rest:

- the customer gets one message saying a person will continue (in their language, from the decision or a default);
- the assistant stops answering that customer (state `handoff`);
- the administrators and the number's chat with itself receive one notice with the reason, a short summary and the last message;
- after four hours without action, one reminder.

## When it says nothing

A customer whose new message only closes the conversation (a thank you, an "ok", a thumbs up) is not answered and is not handed to a person: the assistant stays active for their next message. The decision carries `no_reply_needed` for that, and the helper checks the customer's words before it agrees ([contact-turn.md](contact-turn.md)). A `reply` of null without the flag still hands the customer over, and so does the flag on a message that is more than a thanks.

## Takeover by the phone

Any message that a person writes to a customer from the connected phone or WhatsApp Web pauses the assistant for that customer (state `paused`). It stays paused until someone resumes it. There is no automatic resume.

## Giving it back by itself

If `auto_resume_after_minutes` is set in `memory-policy.json` (off by default, minimum 5), a conversation that a person took over comes back to the assistant after that many minutes without a message from a person, and the administrators and the number's own chat get one notice. It never applies to an administrator's pause, to a conversation still waiting for a person (state handoff) or to a customer who asked to stop. `tn_assist reminders` does it, together with the escalation reminders.

## Who can resume

An administrator (`/retomar` from their number) or an attendant (`/retomar` in the number's chat with itself). Never the customer, never you. Resume by the position shown in `/fila` or by the customer's number.

## Customers who asked to stop

A customer who asks to stop receiving messages is marked `do_not_contact` and gets one confirmation. After that the assistant stays silent, and neither a takeover, a pause nor `/retomar` by an attendant changes it. Only an administrator, with a confirmation code, can undo it. Drafts prepared before the request are discarded.

## Loops and abuse

Two near-identical long messages in a row from the same number look like an automatic reply: the customer is paused and the administrators are told. A customer who receives more than the allowed replies per hour or per day is paused the same way (the numbers are in `/politica`).

## Plan and quota refusals

If the platform refuses a send for quota, plan or connection reasons, do not retry. `tn_assist report-failure` tells the administrators once per cause and billing cycle.
