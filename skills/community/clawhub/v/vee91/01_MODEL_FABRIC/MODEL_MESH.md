# Model Mesh

Adapters should support any provider that exposes a permitted interface. Maintain a capability registry rather than a favorite-model list.

Routing dimensions:
- task capability
- context requirements
- structured output support
- multimodality
- tool-use reliability
- latency
- cost
- privacy
- local availability
- historical task-specific score

Patterns:
- fast local model for triage
- stronger model for hard reasoning
- specialist model for coding/vision/audio/language
- independent model for verification
- fallback model when provider/runtime fails

Never make the router depend on one provider's proprietary API semantics.
