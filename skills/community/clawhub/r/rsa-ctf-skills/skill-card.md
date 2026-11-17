## Description:

rsa-ctf-skills helps agents solve RSA cryptography CTF challenges using 11 common attack techniques, including optional FactorDB-assisted factorization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[moxin1044](https://clawhub.ai/user/moxin1044)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, security learners, and CTF participants use this skill to choose and run RSA attack workflows for intentionally shared challenge data, then interpret recovered factors, private exponents, plaintext, or candidate messages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: FactorDB mode sends the supplied RSA modulus to factordb.com.

Mitigation: Use FactorDB only for CTF or intentionally shared RSA challenge data; avoid private keys, embargoed challenge material, investigation targets, or production RSA moduli unless external disclosure is acceptable.

Risk: The skill automates RSA attack techniques intended for challenge solving.

Mitigation: Use it only for CTFs, training, or other authorized cryptography exercises where the target data is intentionally provided for analysis.

Risk: Help text and CLI output may be in Chinese.

Mitigation: Have outputs reviewed by a Chinese reader or translate them before relying on the results.

## Reference(s):

- [RSA Attack Algorithm Guide](references/attack-guides.md)
- [FactorDB API](https://factordb.com/api?query=)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown guidance with command examples and JSON or plaintext CLI results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include recovered RSA factors, private exponents, plaintext, candidate messages, warnings, and error messages.]

## Skill Version(s):

1.0.0 (source: server release evidence and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
