## Description: <br>
RxnIM helps agents parse chemical reaction images into structured reactants, products, reaction conditions, SMILES strings, and reaction summaries using an online Hugging Face API or a local deployment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fqiangliu](https://clawhub.ai/user/fqiangliu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to convert chemical reaction images into structured reaction data for review, downstream chemistry analysis, documentation, or optional SMILES validation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The online workflow sends reaction images to a third-party Hugging Face service. <br>
Mitigation: Use the online API only for images that are appropriate to share with that service; use a reviewed local deployment in an isolated environment for confidential, unpublished, or regulated research data. <br>
Risk: Low-resolution, blurry, handwritten, or scanned reaction images can reduce parsing quality. <br>
Mitigation: Prefer clear printed reaction images or high-resolution screenshots and ask users to resubmit higher-quality inputs when confidence is low. <br>
Risk: Parsed SMILES strings or reaction roles may be incorrect or invalid. <br>
Mitigation: Review extracted chemistry before downstream use and validate SMILES with a chemistry toolkit such as RDKit or a dedicated chemistry validation skill. <br>
Risk: Online inference may be slow, and local deployment requires substantial GPU memory. <br>
Mitigation: Use explicit timeouts and progress messaging for API calls; confirm local hardware and dependency requirements before attempting local inference. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/fqiangliu/rxn-im) <br>
- [Hugging Face RxnIM Demo](https://huggingface.co/spaces/CYF200127/RxnIM) <br>
- [RxnIM Model Weights](https://huggingface.co/datasets/CYF200127/RxnIM) <br>
- [RxnIM Source Code](https://github.com/CYF2000127/RxnIM) <br>
- [ChemEAGLE Related Work](https://github.com/CYF2000127/ChemEAGLE) <br>
- [Towards Large-scale Chemical Reaction Image Parsing via a Multimodal Large Language Model](http://dx.doi.org/10.1039/D5SC04173B) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown summaries with JSON snippets, SMILES strings, API examples, and shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include third-party API calls or local deployment steps; generated chemistry results should be reviewed and SMILES optionally validated.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
