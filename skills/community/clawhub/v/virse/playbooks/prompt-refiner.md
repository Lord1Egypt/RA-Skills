# Prompt Refiner

Iteratively refine a prompt through multiple generation rounds with a visual timeline.

**Trigger keywords:** "refine this prompt", "iterate", "keep tweaking", "improve step by step"

## Steps

1. **Check balance** — `get_account` → plan for 3-5 rounds
2. **Choose model** — `list_image_models` → use user-specified or recommend one
3. **Calculate element size** — Based on the chosen `aspect_ratio`, compute `size_w` and `size_h` (longer side = 512, default 512×512 for 1:1).
4. **Round 1** — Generate with initial prompt:
   ```
   generate_image(prompt=user_prompt, model=..., position_x=0, position_y=0, size_width=size_w, size_height=size_h, aspect_ratio=...)
   create_element(element_type="text", text="Round 1: <prompt>", position_x=0, position_y=-60)
   create_edge(source=label_id, target=image_id)
   ```
5. **Refine** — Apply prompt engineering. Each round, vary **ONE dimension** (style / lighting / composition / detail) — avoid contradictory changes.
   **Ask user for feedback between rounds** — Claude cannot see generated images.
   After 3 rounds without convergence, suggest trying a different model.
6. **Rounds 2-N** — Place each round to the right:
   ```
   round_x = (round - 1) * (size_w + 60)
   generate_image(prompt=refined_prompt, position_x=round_x, position_y=0, size_width=size_w, size_height=size_h, aspect_ratio=...)
   create_edge(source=prev_image_id, target=new_image_id)  # evolution chain
   ```
   Pause after each round for user feedback.
7. **Group** — `create_group(element_ids=[all images + labels])`

## Output

Timeline showing prompt evolution across rounds. Best prompt version highlighted.
