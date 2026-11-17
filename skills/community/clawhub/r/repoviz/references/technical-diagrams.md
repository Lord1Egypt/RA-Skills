# Technical Diagrams — ERD, Class, Dataflow, Use Case

Four node/edge diagram families for modeling data and behavior, sharing the
`n=id;type;label[;sub][;pos]` / `e=from;to[;label[;main|dash]]` / `b=label;ids`
grammar with `archmap` (see `references/architecture.md` for the shared rules,
position escapes, and encoding table — every rule there applies here too).
Read only the section you are drawing. All example URLs are live-tested.

## ERD — `/draw/erd` (`table` / `view`)

**When to use**: database schema design, data-model reviews, migration planning.
Trigger phrases: *"draw the schema"*, *"ER diagram of the models"*, *"which tables
reference which"*.

- Node: `n=id;table;TableName;<fields>` — the 4th field is the column list, one
  column per **real newline** (`%0A`). Mark keys inline: `id:uuid (pk)`,
  `tenant_id:uuid (fk)`, `slug:text (uk)`. Type `view` works the same for DB views.
- Edge: `e=from;to;1:N` — cardinality goes in the edge label (`1:1`, `1:N`, `N:M`).
- Positions: grid cells (`r0c0` …) work well for schema neighborhoods; keep related
  tables adjacent.

Minimal (2 tables, live):

```
https://x-cmd.com/draw/erd?n=users;table;users;id%3Auuid%20(pk)%0Aemail%3Atext%20(uk)&n=posts;table;posts;id%3Auuid%20(pk)%0Auser_id%3Auuid%20(fk)&e=users;posts;1%3AN
```

Production example (multi-tenant SaaS, 6 tables, live):

```
https://x-cmd.com/draw/erd?title=Multi-tenant%20SaaS%20schema&n=tenants;table;tenants;id%3Auuid%20(pk)%0Aslug%3Atext%20(uk)%0Aplan%3Atext%0Acreated_at%3Atimestamp;r0c0&n=users;table;users;id%3Auuid%20(pk)%0Aemail%3Atext%20(uk)%0Acreated_at%3Atimestamp;r0c2&n=memberships;table;memberships;tenant_id%3Auuid%20(fk)%0Auser_id%3Auuid%20(fk)%0Arole%3Atext%0Ajoined_at%3Atimestamp;r1c1&n=projects;table;projects;id%3Auuid%20(pk)%0Atenant_id%3Auuid%20(fk)%0Aname%3Atext%0Aarchived_at%3Atimestamp;r2c0&n=tasks;table;tasks;id%3Auuid%20(pk)%0Aproject_id%3Auuid%20(fk)%0Aassignee_id%3Auuid%20(fk)%0Atitle%3Atext%0Astatus%3Atext%0Adue_at%3Atimestamp;r2c2&n=comments;table;comments;id%3Auuid%20(pk)%0Atask_id%3Auuid%20(fk)%0Aauthor_id%3Auuid%20(fk)%0Abody%3Atext%0Acreated_at%3Atimestamp;r3c1&e=tenants;memberships;1%3AN&e=users;memberships;1%3AN&e=tenants;projects;1%3AN&e=projects;tasks;1%3AN&e=users;tasks;1%3AN&e=tasks;comments;1%3AN&e=users;comments;1%3AN
```

**Encoding trap**: the field list uses **real newlines encoded as `%0A`** —
do not double-encode as `%250A`. Labels with `()` `:` are safe literal inside the
field list, but encode the whole 4th field with your URL encoder anyway.

## Class — `/draw/class` (`class` / `iface` / `enum`)

**When to use**: OOP design reviews, inheritance hierarchies, interface contracts,
refactoring plans. Trigger phrases: *"class diagram of the domain"*, *"what
implements this interface"*.

- Node: `n=id;class;Name;<members>` — members in the 4th field, one per `%0A`
  (`name:string`, `speak():void`, `static count:int`). `iface` renders an
  interface stereotype, `enum` a value list (`DOG,CAT,BIRD` — `,` is safe).
- Edge: a plain edge `e=dog;animal;extends` draws generalization; add a label like
  `implements` / `uses` for clarity; `dash` for dependencies you want de-emphasized.

Production example (live):

```
https://x-cmd.com/draw/class?t=shadcn&title=Order%20domain%20model&n=animal;class;Animal;name%3Astring%0Aspeak()%3Avoid&n=dog;class;Dog;speak()%3Avoid&n=cat;class;Cat;speak()%3Avoid&n=w;iface;Walker;walk()&n=pet;enum;PetKind;DOG%2CCAT%2CBIRD&n=reg;class;Registry;pets%3AMap%3CPetKind%2CAnimal%3E%0Aregister(a)%3Avoid&e=dog;animal;extends&e=cat;animal;extends&e=dog;w;implements&e=cat;w;implements&e=reg;animal;uses
```

**Limits**: keep it to one hierarchy neighborhood per diagram (~10 classes);
generalization arrows read poorly beyond that, so split by package.

## Dataflow — `/draw/dataflow` (`source` / `process` / `store` / `sink`)

**When to use**: data pipelines, ETL shape, event flows, trust-boundary reviews.
Trigger phrases: *"dataflow diagram"*, *"where does this data come from and where
does it end up"*, *"DFD for the pipeline"*.

- Node types: `source` (produces data), `process` (transforms), `store` (persists),
  `sink` (consumes). The renderer shapes each distinctly — pick honestly.
- Edge = a flow of data; label it with the payload when it isn't obvious
  (`e=val;db;orders`).

Production example (live):

```
https://x-cmd.com/draw/dataflow?t=shadcn&title=Order%20pipeline&n=ev;source;Order%20events&n=val;process;Validate%20%2B%20enrich&n=db;store;Orders%20DB&n=inv;process;Update%20inventory&n=ntf;process;Send%20receipt&n=mail;sink;Customer%20email&e=ev;val&e=val;db&e=db;inv&e=inv;db&e=val;ntf&e=ntf;mail
```

**Limits**: a DFD should be acyclic and readable left-to-right; >12 nodes means you
are mixing abstraction levels — split by stage (ingest / transform / serve).

## Use Case — `/draw/uc` (`actor` / `uc`)

**When to use**: capability maps, requirement scoping, actor/system-boundary
discussions. Trigger phrases: *"use case diagram"*, *"model which actors can
perform which actions"*, *"scope the features per role"* (plain authorization
questions deserve a textual answer -- this page is for diagram requests).

- Node: `n=id;actor;Name` (stick figure) and `n=id;uc;Use case name` (ellipse).
- Edge: `e=actor;uc` = participation. Between use cases: an edge labeled
  `<<include>>` (encode `%3C%3Cinclude%3E%3E`) draws a dashed dependency —
  required sub-behavior; `<<extend>>` (encode `%3C%3Cextend%3E%3E`) = optional
  behavior.

Production example (live):

```
https://x-cmd.com/draw/uc?t=shadcn&title=Shop%20use%20cases&n=customer;actor;Customer&n=admin;actor;Admin&n=browse;uc;Browse%20catalog&n=pay;uc;Pay%20for%20order&n=verify;uc;Verify%20payment&n=ship;uc;Ship%20order&n=restock;uc;Restock%20inventory&e=customer;browse&e=customer;pay&e=pay;verify;%3C%3Cinclude%3E%3E&e=admin;ship&e=admin;restock
```

**Limits**: use cases are capabilities, not screens and not steps — if you catch
yourself writing "click X then Y", switch to a flowchart (`references/flowchart.md`).

## Shared Anti-Patterns

- Don't encode `<<include>>` as literal `<>` in the URL — `%3C%3Cinclude%3E%3E`
  always (bare `<`/`>` break the query).
- Don't exceed ~15 nodes per diagram; these four types are for neighborhoods, not
  whole-system posters.
- All four render with `t=shadcn` for the production look; `title=` and
  `scheme=dark|light` behave as usual. PNG note applies (`format=png` embeds only
  the GB2312 level-1 CJK subset — prefer SVG for Chinese labels).
