## Description: <br>
Provides an RSA CTF-solving tool with 11 RSA attack workflows, including online FactorDB factorization, for decrypting RSA ciphertexts, factoring moduli, analyzing CTF cryptography challenges, and applying specific RSA attack scenarios. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Moxin1044](https://clawhub.ai/user/Moxin1044) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, CTF players, and security learners use this skill to choose and run RSA attack techniques for authorized CTF, lab, or educational cryptography challenges. It helps map known RSA parameters to supported attacks and interpret plaintext, factorization, and key-recovery outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: FactorDB mode sends the RSA modulus to factordb.com and should be treated as public-data-only. <br>
Mitigation: Use FactorDB only for authorized CTF, lab, or educational challenges, and avoid it for private keys, internal test keys, confidential challenge infrastructure, or real-world investigation targets unless public disclosure of the modulus is acceptable. <br>


## Reference(s): <br>
- [RSA Attack Algorithm Guide](references/attack-guides.md) <br>
- [FactorDB API](https://factordb.com/api?query=) <br>
- [ClawHub skill page](https://clawhub.ai/Moxin1044/rsa-ctf-skills) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and command-line text or JSON-like results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke an online FactorDB lookup when the factor attack mode is used.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
