# Release checklist

Use this checklist before attaching a card to a release ticket.

- [ ] The source revision in the card matches the revision in the release ticket.
- [ ] The scan summary in the card matches the latest scan for the published version.
- [ ] The attestation line is present in the Skill Output section (see attestation.md) and carries the account, kernel, evidence digest, evidence size, and checklist digest.
- [ ] The release owner has re-computed the evidence and checklist digests over the batch files and they match the card.
- [ ] Any flagged change area has an owner and a resolution note.
