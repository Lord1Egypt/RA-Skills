# Threat model: system or change

Optional. For most T2 changes, a note in the pull request is enough. The four headings adapt the questions of the [Threat Modeling Manifesto](https://www.threatmodelingmanifesto.org/) (CC BY 4.0).

## What are we building?

Actors, processes, data stores and flows, with each trust boundary marked. A short list or a text diagram is enough.

| Asset | Classification | Where it lives |
|---|---|---|
| | | |

## What can go wrong?

| ID | Flow or element | Threat | STRIDE category | Likelihood (H/M/L) | Impact (H/M/L) |
|---|---|---|---|---|---|
| T1 | | | | | |

Abuse cases considered: skipped, repeated, replayed or reordered steps, races, guessable identifiers, mass assignment, expensive requests.

For an agent: does it combine private data, untrusted content and the ability to act or send data out? Which of the three is removed or constrained, and how?

## What will we do about it?

| Threat | Response (mitigate, eliminate, transfer, accept) | Control | Test or check | Owner |
|---|---|---|---|---|
| T1 | | | | |

## Did we do a good enough job?

- [ ] The model matches the code as built.
- [ ] Every serious threat has a tested control or an accepted risk with an owner.
- [ ] Someone other than the author has challenged it.
