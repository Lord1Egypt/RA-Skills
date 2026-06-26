## Description: <br>
本地图片语义搜索 helps users build a local Chinese-CLIP image index and search their own pictures with Chinese or English natural-language queries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tobemsk](https://clawhub.ai/user/tobemsk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to install dependencies, scan selected local image folders, create or update a FAISS image index, and run semantic searches for local pictures. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create a local searchable index of personal images. <br>
Mitigation: Set SCAN_ROOTS to only the folders intended for indexing and treat the image_db directory as private data. <br>
Risk: Exported search result files may reveal search terms and local file paths. <br>
Mitigation: Review, store, share, or delete Desktop result files according to the sensitivity of the indexed images. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tobemsk/tobemsk-image-search) <br>
- [Hugging Face mirror endpoint](https://hf-mirror.com) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, text] <br>
**Output Format:** [Markdown with inline shell commands and configuration references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search workflows create a local image_db index and may export Desktop text files containing queries, local paths, and similarity scores.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
