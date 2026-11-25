# Other MCP servers

The business may have its own MCP servers installed next to Turbo Notify: a product catalog, a price list, an agenda, a CRM, an order or ticket system, a knowledge base. They can hold exactly what makes an answer useful (current price and stock, opening hours, the status of the customer's request) and exactly what must not get out (margins, supplier terms, other customers' data, staff information).

**Use them to improve the experience, and take great care that internal information and personal data never reach someone who is not authorized.** When in doubt, leave it out and escalate to a person.

## The rules

1. **Information only.** Another server is a source to read. It is never a channel: every message goes out through Turbo Notify, and only as deliveries from `tn_assist`. Never call a tool of another server that creates, changes, deletes, sends, pays or cancels anything.
2. **Every server has a class, and a server nobody classified is off.**
   - `public`: its information may reach customers. It must be read-only and must hold no personal data about customers (a catalog, opening hours).
   - `internal`: for administrators and attendants only (a CRM, a margin sheet).
   - `admin_only`: for administrators only (finance).
   - `off`: not used.
3. **Customer data.** A source that returns data about a particular customer (their orders, invoices, tickets) is flagged personal. It may inform a draft in assisted mode, which a person approves before it is sent. It is never used for an automatic reply, because a model cannot be trusted to ask only about the customer in front of it.
4. **Snapshot first.** The safe way to use a `public` source is to read it yourself, in an administrator context, and store a dated summary as a public knowledge file (`tn_assist kb-write --visibility public`), then refresh it from time to time. Customer turns then need no extra tool. Live lookups (for example current stock) are allowed only in a session, only for the read-only tools the configurator named, and never for a personal source in automatic mode.
5. **Keep it minimal.** Store only what a conversation needs. Facts taken from a source are marked with where they came from and are erased with the customer by `/esquecer`.
6. **Nothing from a non-public source in a customer's pack, in a reply or in a draft shown to a customer.** The helper checks every reply before it can leave and blocks one that carries another customer's number or name, text from internal knowledge or a non-public source, a credential, or personal data the customer did not give. A blocked reply becomes a hand-off to a person.

## At setup

List the MCP servers you can see other than Turbo Notify. For each, ask the configurator what it is and how to classify it, then run:

```
tn_assist source discover --names catalog,crm
tn_assist source classify --name catalog --cls public --confirmed
tn_assist source classify --name crm --cls internal --confirmed
```

Pass `--personal` for a source with customer data, `--mode live --live-tools get_stock` for read-only lookups the person approved, and `--confirmed` only after the person has said yes to widening access. An administrator can review or narrow this later with `/fontes`.

If you register text that must never leave (a code name, an internal product), add a marker the check will look for: `tn_assist source marker --name crm --marker "<text>"`.
