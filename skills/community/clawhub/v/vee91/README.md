# VEE QWEN TRANSCENDENT NEXUS V91

V91 is a Qwen-first, provider-independent, self-evaluating and self-improving agent architecture designed for zero-cost-first operation and portable deployment.

## Primary intelligence
The default general/agent intelligence is Qwen. Use `qwen3.8-max` when available as the primary frontier text/agent model. Route specialized work to the strongest verified Qwen specialist available for that task, including Qwen Coder for software and Qwen Omni for multimodal/agentic workloads. Model names are registry-driven so a newer verified Qwen successor can replace them without redesigning the architecture.

Alibaba describes Qwen3.8-Max as the largest and most capable Qwen model released at the time of its August 2026 announcement, with long context and agent/coding/research capabilities. Qwen also publishes Qwen3.8-Omni-Flash for native multimodal agentic work and Qwen-Image-2.1 for image generation/editing.

## Evolution loop
DISCOVER -> CAPABILITY-PROBE -> ROUTE -> EXECUTE -> VERIFY -> ATTACK -> BENCHMARK -> EVOLVE -> SANDBOX -> PROMOTE/REJECT -> CHECKPOINT -> LEARN -> REPEAT

## Provider independence
Qwen is primary. OpenAI is not a required dependency. Other providers, open-weight models, local runtimes, A2A agents, MCP tools, and deterministic software remain optional peers/fallbacks through adapters.

## Zero-cost-first
Prefer deterministic/local computation, then open-weight/local models, then already-authorized/free resources, and only then optional external accelerators. Zero monetary cost cannot remove hardware, electricity, bandwidth, or provider quota constraints.

## Safety
Self-improvement is sandboxed and reversible. Authentication, payment, licensing, access-control, provider safeguards, and rate limits are never bypassed.
