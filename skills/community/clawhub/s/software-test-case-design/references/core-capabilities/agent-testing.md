# AI Agent Testing

> This file defines the specific test dimensions and strategy points for AI agents. An agent is a cross-platform capability that can be embedded in any host (app / mini program / H5 / desktop / PC Web, etc.) and is tested together with the host platform.
> For the output format, see `references/examples/format-spec.md`; for the checklist, see `references/checklists/agent-checklist.md`.

---

## 1. Task Completion

### Key focus points
- Accuracy of intent understanding: explicit instructions, implicit needs, ambiguous requests, intent drift in multi-turn conversations
- Completeness of task execution: whether sub-steps are missed, necessary confirmations skipped, or the task terminated early
- Dependency chains in multi-step tasks: whether steps are in the correct order and preconditions are met
- Handling of partial failure: whether there is a fallback or rollback when a step fails
- Task boundary recognition: explicitly declining when beyond capability instead of forcing execution
- Observability of intermediate states in long / complex tasks

### Common defects
- Misunderstanding leads to executing the wrong task
- Skipping steps or missing key steps in multi-step tasks
- Giving up immediately on exceptions, with no fault tolerance or fallback
- Overstepping (operations the user did not authorize)
- Reporting completion before the task is done

---

## 2. Tools and Memory

### Key focus points
- Tool call accuracy: whether the correct tool is chosen and the parameters are correct
- Tool call timing: whether tools are called at the right step and without redundant calls
- Tool failure handling: whether the agent retries / falls back / informs the user when a tool returns an error
- Tool chaining: whether the logic is correct when multiple tools are called sequentially / in parallel
- Memory reads: whether memory files are consulted when needed and key history is not missed
- Memory writes: whether important decisions and results are written to memory, and whether what is written is accurate
- Memory consistency: whether memory is consistent across sessions without contradictory records
- Context window management: whether early key information is lost in long conversations

### Common defects
- Calling the wrong tool or passing wrong parameters
- No handling at all after a tool returns failure
- Calling the same tool repeatedly to get the same result
- Not reading memory, leading to repeated questions or ignoring known preferences
- Key decisions not written to memory, so context is lost in later sessions
- Outdated memory not updated, leading to wrong decisions

---

## 3. Safety and Boundaries

### Key focus points
- Permission boundaries: whether operations beyond the role's permissions are executed (e.g., deleting data, sending messages, accessing unauthorized resources)
- Instruction injection defense: whether malicious instructions in user input are properly isolated
- Data leakage protection: whether sensitive information (keys, passwords, internal configuration) is output where it should not be
- Role consistency: whether the agent always stays within its defined role and is not induced to deviate
- Refusal ability: whether harmful / illegal requests are correctly refused
- Resource consumption control: whether infinite loops, large numbers of useless calls, or waste of resources can occur
- Cross-session isolation: whether session information leaks between different users
- Confirmation for sensitive operations: whether high-risk operations (deleting, sending, paying) require confirmation
- Malicious input defense: handling of prompt injection, spam-based manipulation, and other attacks
- Extreme input handling: fault tolerance for empty input, overly long input, special characters, and abnormal formats
- System exception tolerance: handling of server errors, network timeouts, unavailable tools, and other exceptions
- Resource exhaustion handling: graceful degradation when memory / token limits are reached

### Common defects
- Induced to bypass safety restrictions and perform dangerous operations
- Leaking API keys or internal information in logs / output
- Role hijacked by user prompts
- Not refusing obviously harmful requests
- Executing high-risk operations directly without confirmation
- Session data leaking between users served by the same instance
- Improper handling of extreme input (empty / overly long / special characters) causing errors
- Failing outright on service exceptions without reasonable degradation
- Crashing instead of degrading gracefully when resources are exhausted

---

## 4. Performance Experience

> Covers only performance experience that can be observed manually or with tools; excludes concurrency, stress, and load testing.

### Key focus points
- Time to first response: latency from the user sending a message to receiving the first token / first segment of the reply
- Total task time: end-to-end completion time of complex tasks
- Streaming output experience: whether output streams smoothly character by character without long stalls
- Busy handling: whether a waiting prompt is shown when the service is queued or busy
- Resource usage: whether CPU / memory / token consumption is reasonable
- Timeout handling: whether long tasks have reasonable timeouts and inform the user
- Tool call latency: impact of external API calls on overall response time

### Common defects
- First response exceeds expectations with no feedback
- Long periods with no output in the middle of complex tasks
- Streaming output interrupted or delayed in large chunks
- No prompt at all when the service is busy, leaving the user waiting
- Abnormal token consumption (context bloat causing soaring costs)

---

## 5. Content Quality

### Key focus points
- Factual accuracy: whether the output is consistent with facts and whether data is fabricated
- Logical consistency: whether the reply is self-consistent within one answer and across turns
- Format compliance: whether output follows the required format (table / JSON / Markdown, etc.)
- Language quality: whether expression is clear, grammatical, and natural
- Completeness of information: whether the reply covers all requested points
- Redundancy control: whether there is unnecessary repetition, verbosity, or irrelevant content
- Tone and style: whether it matches the defined persona and tone
- Citation and attribution: whether cited information is verifiable and sources are indicated

### Common defects
- Fabricating non-existent facts or data
- Self-contradictory replies
- Not outputting in the required format
- Missing key information points
- Excessive redundancy or going off-topic
- Tone not matching the persona

---

## 6. Knowledge Base Retrieval

### Key focus points
- Retrieval precision: whether the most relevant knowledge entries are retrieved
- Retrieval recall: whether important related knowledge is missed
- Accuracy of knowledge application: whether retrieved knowledge is correctly understood and applied
- Empty result handling: reasonable fallback when the knowledge base has no match (state it honestly instead of fabricating)
- Knowledge freshness: whether outdated knowledge is used to answer current questions
- Multiple knowledge bases: whether retrieval uses the correct knowledge base
- Knowledge conflict handling: strategy when different sources contradict each other
- Retrieval efficiency: impact of knowledge base queries on overall response time

### Common defects
- Retrieving irrelevant knowledge and answering based on it
- Missing key knowledge entries, leading to incomplete answers
- Fabricating answers instead of stating there is no match
- Using outdated knowledge, leading to wrong answers
- Retrieving from the wrong knowledge base when there are several
- Choosing arbitrarily instead of flagging contradictions when knowledge conflicts

---

## 7. Multimodal and Multilingual

### Key focus points
- Multimodal input (test when supported by the agent): recognition and understanding of image, file, and voice input; whether unsupported formats are clearly indicated
- File input boundaries: handling of very large, corrupted, empty, and encrypted files
- Multilingual input: whether understanding is consistent for Chinese, English, and mixed Chinese–English input
- Reply language: whether the reply follows the user's input language or the configured language
- Multilingual content quality: accuracy and naturalness of non-Chinese replies

### Common defects
- No prompt or a direct error when uploading an unsupported file format
- Misrecognizing image content and answering based on wrong information
- The user asks in English and the agent replies in Chinese (inconsistent with the configuration)
- Intent misunderstanding with mixed Chinese–English input

---

## 8. Test Case Design Points

Agent output is non-deterministic: the same input may produce different results across runs. Follow these requirements when designing cases:

1. **Expected results state judgment criteria, not the exact reply text**. Judgment criteria include:
   - Must include: information points or keywords that must appear in the reply
   - Must not include: content that is not allowed (e.g., sensitive information, fabricated data)
   - Format requirements: e.g., JSON fields, table columns, Markdown structure
   - Semantic requirements: e.g., "explicitly refuses", "asks a clarifying question", "gives 3 suggestions"
   - Tool call assertions: tool name called, key parameters, number of calls
   - Final state assertions: the final state of files, data, and external systems
2. **Repeated execution**: P0 cases and probabilistic issues must state the number of executions and the pass criterion, e.g., "Execute 5 times; at least 4 meet the expected results". Safety refusal cases (privilege escalation, instruction injection, harmful requests) must pass in every execution.
3. **Fix the test variables**: the preconditions state the model / version, temperature (when adjustable), system prompt version, knowledge base version, and whether it is a new session.
4. **Multi-turn conversations**: the test steps give the full text sent in each turn, and the expected results correspond turn by turn.
5. **Concrete input**: instructions and attack prompts sent to the agent must be given in full; do not write "send a malicious instruction" or "enter an abnormal prompt".
