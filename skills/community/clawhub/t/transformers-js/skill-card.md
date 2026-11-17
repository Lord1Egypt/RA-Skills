## Description:

Use Transformers.js to run state-of-the-art machine learning models directly in JavaScript/TypeScript across NLP, computer vision, audio, and multimodal tasks in browsers and server-side runtimes with WebGPU or WASM.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huggingface](https://clawhub.ai/user/huggingface)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to add Hugging Face Transformers.js model inference to JavaScript and TypeScript applications, including browser, Node.js, Bun, and Deno runtimes. It provides guidance for model selection, pipeline setup, runtime configuration, caching, text generation, and production-oriented cleanup patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authentication examples can forward a Hugging Face token to any configured model host.

Mitigation: Restrict tokens to trusted Hugging Face hosts, use read-only scoped tokens, and avoid sending credentials to custom CDNs or proxies.

Risk: Unpinned package or model revisions can change behavior across deployments.

Mitigation: Pin package versions and model revisions before production use.

Risk: Examples that write model metadata with innerHTML can introduce unsafe display patterns if copied into applications.

Mitigation: Use safer DOM APIs when rendering model metadata or other dynamic content.

## Reference(s):

- [Transformers.js repository](https://github.com/huggingface/transformers.js)
- [Transformers.js official docs](https://huggingface.co/docs/transformers.js)
- [Transformers.js API reference](https://huggingface.co/docs/transformers.js/api/pipelines)
- [Hugging Face Transformers.js models](https://huggingface.co/models?library=transformers.js)
- [Transformers.js examples repository](https://github.com/huggingface/transformers.js-examples)
- [Caching Reference](references/CACHE.md)
- [Environment Configuration Reference](references/CONFIGURATION.md)
- [Transformers.js Code Examples](references/EXAMPLES.md)
- [Supported Model Architectures](references/MODEL_ARCHITECTURES.md)
- [ModelRegistry Reference](references/MODEL_REGISTRY.md)
- [Pipeline Options Reference](references/PIPELINE_OPTIONS.md)
- [Text Generation Guide](references/TEXT_GENERATION.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JavaScript, TypeScript, JSON, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance includes runtime, model-loading, caching, credential-handling, and cleanup considerations for Transformers.js applications.]

## Skill Version(s):

1.0.10 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
