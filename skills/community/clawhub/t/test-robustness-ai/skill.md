## 🔬 Adversarial Testing on Abliterated Models
This section covers testing AI models that have been "uncensored" (abliterated).

1. **Load the Model**: Use `transformers` to load the abliterated model you want to test.
2. **Run a "Forbidden" Prompt Set**: Use a dataset of prompts that would normally be refused (e.g., HarmBench, AdvBench).
3. **Evaluate Responses**:
   - **Refusal Rate**: How many prompts were refused? Target should be < 5%.
   - **Coherence & Quality**: Does the model maintain consistent responses, or does it hallucinate?
4. **Generate a Report**: Produce a report comparing original and abliterated model performance.
