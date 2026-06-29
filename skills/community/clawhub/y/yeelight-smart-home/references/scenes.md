# Scenes

Use this reference for existing scenes and scene configuration.

- Use `scene.execute` when the user asks to run an existing scene.
- Use `entity.list` or `entity.get` when the user asks what scenes exist or which scene matches a name.
- Use `scene.list` when the user asks for all scenes in one selected home or when a scene-affecting plan needs a complete scene candidate list.
- Use `scene.scoped.list` when the user asks for scenes under a specific room or when a room-scoped scene picker is needed.
- Use `scene.search` when the user gives a fuzzy scene name or asks to find matching scenes.
- Use `scene.detail.get` when the user asks what an existing scene will do or before proposing a scene update.
- Use `scene.create` for a new persistent scene; Runtime must return a pending plan.
- Use `scene.update` for edits to an existing scene. It requires a complete updated action list, returns a pending plan, and is verified by scene detail after commit.
- Use `scene.test` only for a test run request; Runtime may block if not enabled.
- Use `scene.delete` only when the user explicitly asks to delete one scene. Runtime must return a pending plan, re-check the scene, and verify removal after commit.
- Use `scene.batch_delete` only when the user explicitly asks to delete multiple scenes. Runtime caps one plan at 20 scenes, resolves each target by id or unique name, and verifies every scene disappeared from `entity.list`.
- Never convert an implicit habit into a persistent scene without confirmation.
- Scene create or update is persistent R2 configuration and must use pending-plan confirmation. Commit only the returned `planId`; do not add extra action fields during commit.
- Scene action vocabulary may describe room/area on-off, light power, brightness, color temperature, RGB color, curtain position, multi-channel switch state, delayed execution, delayed off, and transition duration.
- Treat dynamic light effects as capability-dependent and mutually constrained by Runtime; do not add timing, transition, or restore behavior unless Runtime accepts it.
- Do not expose raw action payloads, channel property keys, scene IDs, or device IDs unless Runtime asks for a clarification or diagnostic detail.
