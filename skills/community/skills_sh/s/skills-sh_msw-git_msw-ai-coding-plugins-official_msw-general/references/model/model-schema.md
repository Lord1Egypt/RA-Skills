# `.model` Schema Detail

Normal AI authoring must not use raw `.model` schema details.

Use [`../model.md`](../model.md) and `scripts/model/msw_model_builder.cjs` instead:

- inspect with `ModelBuilder.read()` / `ModelBuilder.snapshot()`
- create with `ModelBuilder.fromTemplate()`
- patch with builder methods
- save with `write()`

This file is intentionally kept as a compatibility stub so older links do not break. It does not expose raw field details because `.model` JSON should be treated as a builder-managed format.
