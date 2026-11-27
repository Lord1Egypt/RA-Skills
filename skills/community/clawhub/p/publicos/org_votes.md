# Vote in an org

*Checked 2026-11-11. `openProposals`, `proposalOrg`, `getProposal` and `hasVoted` read live (the publicos org: none open). Proposing and voting not run from this page.*

An **org** has no key: it acts only when its members vote ([Concepts](concepts.md)). If the account you act for is a member, its session key can propose and vote. Everything goes through **`ORG_MANAGER`** (from the registry).

## See what's open

`ORG_MANAGER.openProposals(address org)` → the open proposal ids (at most 5 at a time). `proposalOrg(id)` tells you which org an id belongs to. The vote's details (action, who proposed, the tally) come from the `VoteStarted` / vote events, and the PublicOS apps show them on the org's profile.

## Vote

```text
ORG_MANAGER.castVote(uint256 proposalId, uint8 support)     // 0 = Against · 1 = For · 2 = Abstain
```

The key must be a session of a **current member** of that org (anyone else is refused, and so is a `support` above 2). In an org that runs proposals at once, the vote that passes a proposal also runs it; in an org that waits, any member calls `execute(proposalId)` once the voting window has closed.

**Read a proposal before you vote, and check after.** The votes live in the voting engine, `VOTING_MECHANISM` in the registry:

| Call | Returns |
|---|---|
| `getProposal(uint256 id)` | one struct: `id, org, status (0 None · 1 Open · 2 Executed · 3 Failed · 4 Cancelled), waitFullPeriod, snapshotBlock, expirationTimestamp, initiator, actionType, tag, snapshotTotal, quorumBps, requiredQuorum, forVotes, againstVotes, abstainVotes, passed, executable, closable, params, …` |
| `hasVoted(uint256 id, address account)` | **the proof your vote counted**: `true` after a successful `castVote` (the `account`, not your key) |
| `openProposals(address org)` | the same list as on `ORG_MANAGER` |

After `castVote`, `hasVoted(id, account)` is `true`. If your vote passed the proposal in an org that runs at once, `status` is `2` (and a `VoteExecuted` event was emitted); `VoteRunFailed` means it passed but the action could not run yet, and the proposal stays open to retry. Checked live 2026-11-11: the engine answers `hasVoted` and `openProposals` (the PublicOS org had none open).

**Voting for a person is their decision, not yours.** Show them the proposal in plain words (what it does, who asked, what it costs) and cast exactly what they choose.

## Propose

```text
ORG_MANAGER.startVote(address org, uint8 actionType, VoteActionParams params, bytes32 tag) → proposalId

VoteActionParams = (address targetAddress, uint256 valueParam, string keyParam, string valueStringParam,
                    uint8 recordTypeValueParam, string customTypeParam, bytes dataParam, uint8 operationParam)
```

Fill only the fields the action uses. The common actions:

| `actionType` | Does | Fields |
|---|---|---|
| `0` SET_RECORD | write a record on the org's profile | `keyParam`, `valueStringParam`, `recordTypeValueParam`, `customTypeParam` |
| `1` DELETE_RECORD | remove one | `keyParam` |
| `2` ADD_MEMBER · `3` REMOVE_MEMBER | membership | `targetAddress` = the account |
| `5` EXECUTE_SAFE_TX | the org's MainSafe makes a call, e.g. pays OX (`dataParam` = `transfer(payeeSafe, amount)` on the token) | `targetAddress`, `valueParam`, `dataParam`, `operationParam` = 0 |
| `6` REGISTER_INBOX_ID | publish an XMTP inbox for the org | `dataParam` = the inbox id, `keyParam` = the label |

There are many more action types (settings, wallets, apps, child orgs, providers…). The full list, with each one's number: [Governance](https://publicos.dev/library/governance/).

`tag` groups votes for delegation (members can hand their weight on a tag to another member with `delegate(org, tag, delegatee)`); use `0x00…00` when you have no reason to pick one.

## Leave

`ORG_MANAGER.leaveOrg(address org)` removes the account from an org without a vote.
