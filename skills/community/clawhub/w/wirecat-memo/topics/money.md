# memo — Money: amounts, payments, refunds, business data and a source's records

**Amounts.** Give and read every amount as a decimal string with at most the currency's decimals: `"50000.00"` RUB,
`"1200"` JPY (none), `"1.250"` BHD (three). memo stores it as a whole number of the currency's minor units (kopecks,
fils) and refuses more decimals than the currency has, or a currency it does not know. Nothing is converted: add up
only amounts of one currency, and report totals per currency.

**Paid is net.** An invoice's `paid` is its confirmed payments minus their confirmed refunds, and `open` is the total
minus that. A refund is a payment the other way (`memo payments add ... --refund-of payment:<id>`), never more than
the payment it gives back for; a fully refunded invoice reads `issued` again until the owner voids it. Never subtract
refunds yourself from `paid`, and never sum `payments list` to get what an invoice still owes: read `invoices show`.

Money is not a fact. A payment you read is a finding of kind `payment` with `amount` (a decimal string),
`currency`, `direction` (`to_us`, `from_us`), `state` and `counterparty`. When the owner confirms it, a `paid` one
becomes a `payment:` row (dated `paid_at` when you give it, else `due_at`), an `expected` one an `invoice:`, which
needs a `person:` or `organization:` counterparty, and a `cancelled` one voids the invoice it `supersedes`. A paid
one that settles an expected one names that `invoice:` in `supersedes`. `memo invoices list` and
`memo payments list` show the rows; `memo projects status` sums the confirmed ones per currency under `finance`.
Only the owner confirms money, in `memo review kind:invoice,payment`.
A source's export (a payment sheet, a bank statement) comes in with `memo records check <file> --account <a>` first,
which writes nothing, then `memo records import` once the owner agrees; its invoices and payments wait for the owner.
An invoice or payment whose party is a record of the source (`organization:client`) waits until the owner says which
entry it is: show `memo records list waiting:true --account <provider>:<account>` and leave
`memo records link` to the owner.

Deals and leads: `memo deals list status:open`, `memo leads list`, `memo deals show deal:<id>`. You may add, move and
close them and make pipelines yourself (`memo deals add <title> <stage> [amount] [currency] --reason ...`,
`memo leads add <title>`, `memo deals move deal:<id> <stage>`, `memo deals close deal:<id> won|lost`); they are
written at once, no review. Name a pipeline by `pipeline:<id>` when two share a name. `memo pipelines show <pipeline>`
gives the counts and conversion per stage. To change a CRM copy on its server, run the CLI in its `writes_with`
(`tool` and `profile`); when `profile` is `null`, ask the owner which of `profiles` to use, never pick one.

Base stages are the owner's own columns for deals and for leads; every other stage maps onto one
(`memo stages show deal`, `memo stages list confirmed:false`). Move the owner's own deal to a base stage with
`memo deals move deal:<id> stage:<id>`. On `stage.choice-required`, ask the owner which of `candidates` and move to
its `stage:<id>`. On `stage.unmapped`, tell the owner which stage to map. Your `memo stages set` is a suggestion for
the owner. Editing the base stages and `memo stages confirm` are the owner's own.

Products, contracts, subscriptions, wallets and transactions: `memo products list`, `memo contracts show contract:<id>`
(the last day to give notice), `memo subscriptions show subscription:<id>` (every price it had),
`memo wallets show wallet:<id>` (the balance from the opening balance and the confirmed, booked transactions; what is
pending is beside it, never in it), `memo transactions list 'wallet:"wallet:<id>"' uncategorized:true`. A transaction is
what the bank says moved and a payment is the settlement: they meet only through `transactions update --payment`.
An agent's contract with a value, subscription, price and transaction wait for the owner in `memo review`.
`memo show <ref>` and each `show` list where an imported entry came from under `sources`: the source records mapped to
it, and those that name it (a quote `quoted-for` a deal).
One deal whole: `memo deals context deal:<id> --brief` (people with roles and standing, client, project, money
totals, counts); without `--brief` the detailed form. Its messages, mail and meetings are `proposed`: they share
people with the deal, nothing links them. A stage named Won is not a payment: money is what invoices and payments
say. A client's whole picture: `memo organizations context organization:<id>`; clients only:
`memo organizations list category:client`. A deal or a person on it copied from a CRM is `reported`: say so when only
the CRM says it. Set the project of a deal with `memo deals update deal:<id> --project <key>`.
