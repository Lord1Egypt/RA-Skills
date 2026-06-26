# Buffers and Feedback

Use this reference when a ShaderToy effect is not just an `Image` pass.

## Signals that the shader is multi-pass

- The description mentions `Buffer A`, `Buffer B`, `Buffer C`, or `Buffer D`.
- The shader samples a channel that is actually another pass output.
- The visual result depends on previous frames, trails, accumulation, reaction-diffusion, or simulation state.

## Practical rule

Do not pretend a feedback effect is a plain single-pass fragment shader.

Before porting, answer these:

1. Which pass produces the intermediate state?
2. Which pass consumes it?
3. Does the effect depend on previous-frame persistence?
4. Does the target host need ping-pong render targets?

## Porting implication

- `Image` only: easiest export
- `Image` + buffer passes: needs render targets
- previous-frame feedback: likely needs ping-pong buffers

## Debugging implication

If the result is blank or unstable:

- verify pass order first
- verify sampled buffer content second
- only then debug the final image pass
