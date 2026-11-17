## Description:

Create text-to-speech narration and MP3 audio with UnlimitedTTS using x402 USDC payments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[unlimitedtts](https://clawhub.ai/user/unlimitedtts)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate narration, read-aloud audio, voice output, and MP3 files through UnlimitedTTS while keeping wallet secrets out of the agent conversation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A user could authorize an unintended x402 payment amount, voice, text, wallet network, or payee.

Mitigation: Confirm the quote amount, voice, text, wallet network, and payee before signing, and enforce any user-stated maximum USDC budget.

Risk: Wallet secrets could be exposed if an agent asks for seed phrases, private keys, or broad signing authority.

Mitigation: Never request or expose seed phrases or private keys; use only a wallet or signing tool that signs the specific quoted payment requirement.

Risk: A timeout, missing receipt, or ambiguous payment response could cause duplicate payment attempts.

Mitigation: Do not retry ambiguous payment outcomes automatically; inspect wallet or settlement status and ask the user before creating a new quote or authorization.

Risk: Splitting text over the voice character limit can create multiple separately paid requests.

Mitigation: Explain the aggregate chunking plan and get approval before synthesizing multiple paid chunks.

## Reference(s):

- [Direct x402 mode](references/direct-x402.md)
- [Error recovery](references/errors.md)
- [UnlimitedTTS API documentation](https://api.unlimitedtts.com/docs)
- [UnlimitedTTS voices](https://api.unlimitedtts.com/tts/voices)
- [ClawHub skill page](https://clawhub.ai/unlimitedtts/skills/unlimitedtts-skill)

## Skill Output:

**Output Type(s):** [Files, Guidance]

**Output Format:** [MP3 audio file with concise Markdown status or guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Paid synthesis should return an MP3 attachment or resource; large text may require approved paid chunks.]

## Skill Version(s):

0.1.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
