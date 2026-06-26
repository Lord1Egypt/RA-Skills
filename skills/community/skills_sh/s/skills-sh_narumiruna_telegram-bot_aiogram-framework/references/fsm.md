# Finite State Machine (FSM)

Core flow
- Define states with `StatesGroup`.
- Use `FSMContext` in handlers to set state, update data, and clear.
- Separate handlers by state to guide multi-step dialogs.

Storage options
- `MemoryStorage` for dev/test.
- `RedisStorage` and `MongoStorage` for production/persistence.
- Customize keys with `KeyBuilder` if needed.

Managing other users
- Use `dispatcher.fsm.get_context(bot=..., chat_id=..., user_id=...)` to access another user's state.

See:
- `docs/dispatcher/finite_state_machine/index.rst`
- `docs/dispatcher/finite_state_machine/storages.rst`
- `examples/finite_state_machine.py`
- `examples/scene.py`, `examples/quiz_scene.py`
