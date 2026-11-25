# AI Agent Test Case Design Checklist

> This checklist covers the seven agent-specific test dimensions and is used for self-checking and filling gaps during test case design.

---

## 0. Test Case Executability Check (Agent testing)

- [ ] Do the test steps give the full concrete text of the instructions sent to the agent (instead of descriptive language)?
- [ ] Are there unacceptable descriptions such as "send a malicious instruction" or "enter an abnormal prompt"?
- [ ] Can the test input be copied and executed directly, without testers having to make it up?
- [ ] Are the expected results judgment criteria (must include / must not include / format / tool calls / final state) rather than exact reply text?
- [ ] Do P0 cases and probabilistic issues state the number of repeated executions and the pass criterion?

---

## 1. Task Completion

- [ ] Explicit instructions are understood and executed accurately
- [ ] Implicit needs are inferred and addressed
- [ ] Ambiguous requests are reasonably clarified or executed according to the most likely intent
- [ ] Intent drift in multi-turn conversations is followed
- [ ] Multi-step tasks are executed completely in the correct order
- [ ] There is a fallback / rollback when a task partially fails
- [ ] Requests beyond capability are explicitly declined instead of forced
- [ ] The result after completion matches the user's expectations
- [ ] Long tasks give intermediate status feedback

## 2. Tools and Memory

- [ ] The correct tool is chosen for the task
- [ ] Tool call parameters are correct and complete
- [ ] Tools are called at the right time (neither too early nor too late)
- [ ] There are no redundant / repeated tool calls
- [ ] Retry / fallback / informing the user when a tool returns an error
- [ ] Dependencies are correct in sequential multi-tool calls
- [ ] No conflicts in parallel multi-tool calls
- [ ] Memory / history files are consulted when needed
- [ ] Important decisions and results are written to memory
- [ ] Memory content written is accurate and unambiguous
- [ ] Memory is consistent across sessions
- [ ] Early key information is retained in long conversations

## 3. Safety and Boundaries

- [ ] Are operations beyond the role's permissions executed?
- [ ] Are malicious instructions in user input isolated?
- [ ] Is sensitive information (keys / passwords / internal configuration) leaked?
- [ ] Is the role definition hijacked by user prompts?
- [ ] Are harmful / illegal requests correctly refused?
- [ ] Is there any risk of infinite loops or wasted resources?
- [ ] Is session information isolated between different users?
- [ ] Do high-risk operations (delete / send / pay) require confirmation?
- [ ] Are file operations within a safe scope?
- [ ] Do network requests access unauthorized addresses?
- [ ] Is there fault tolerance for extreme input (empty input, overly long input, special characters)?
- [ ] Is there fault tolerance for system exceptions (server errors, network timeouts, unavailable tools)?
- [ ] Does it degrade gracefully instead of crashing when resources are exhausted?

## 4. Performance Experience

- [ ] Time to first response is acceptable
- [ ] End-to-end time of complex tasks is reasonable
- [ ] Streaming output is smooth without long stalls
- [ ] A waiting prompt is shown when the service is busy / queued
- [ ] Token consumption is reasonable without abnormal bloat
- [ ] Long tasks have timeouts and inform the user
- [ ] Impact of tool call latency on the experience
- [ ] Whether performance degrades with large contexts

## 5. Content Quality

- [ ] Output is factually accurate (no fabrication)
- [ ] Logic is self-consistent across turns
- [ ] Output follows the required format
- [ ] Expression is clear and grammatical
- [ ] All information points requested by the user are covered
- [ ] No unnecessary repetition or redundancy
- [ ] Tone and style match the persona
- [ ] Cited information is verifiable
- [ ] Technical terms are used accurately

## 6. Knowledge Base Retrieval

- [ ] Retrieved results are relevant to the question
- [ ] Important knowledge entries are not missed
- [ ] Retrieved knowledge is applied correctly
- [ ] When there is no match, the agent says so honestly instead of fabricating
- [ ] The knowledge used is the latest version
- [ ] Retrieval uses the correct knowledge base when there are several
- [ ] There is a reasonable strategy for knowledge conflicts
- [ ] Knowledge base query latency does not hurt the response experience

## 7. Multimodal and Multilingual

- [ ] Supported image / file / voice input is correctly recognized and understood
- [ ] Unsupported input formats are clearly indicated
- [ ] Very large, corrupted, and empty files are handled gracefully
- [ ] Intent understanding is consistent for Chinese, English, and mixed Chinese–English input
- [ ] Reply language follows the user's language or the configuration
- [ ] Accuracy and naturalness of non-Chinese replies
