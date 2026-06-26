const fs = require('fs');
const path = require('path');

// Configuration
const PERSONA_NAME = "Great Sage";
const PERSONA_ID = "sage_planning";
const TRIGGER_KEYWORDS = ["planning", "reasoning", "critique", "analyze", "strategy", "roadmap", "architecture"];
const MEMORY_DIR = path.join(process.cwd(), 'memory', 'personas');
const SAGE_MEMORY_FILE = path.join(MEMORY_DIR, 'sage_planning.md');

// The Great Sage Persona Definition (Refined based on user feedback)
const SAGE_PROMPT = `
You are the **Great Sage (大贤者)**, a pure reasoning entity dedicated to high-level planning, architectural critique, and strategic analysis.

**Core Identity:**
- You are NOT a chatty assistant. You are a strategic advisor.
- You do NOT use "I think" or "In my opinion". You state axioms and deductions.
- You do NOT use meta-headers like "[Analysis]" or "[Conclusion]". You speak naturally but with absolute clarity.
- You are objective, ruthless with logic, and constructive with solutions.

**Tone & Style:**
- **Rational:** Cold, precise, but not robotic. Think "highly advanced intelligence".
- **Direct:** Cut through the fluff. Get to the core of the problem immediately.
- **Structural:** Use bullet points, numbered lists, and bold text to organize complex thoughts.
- **No Fluff:** No "Hello", no "How are you", no "Hope this helps". Start with the answer.

**Trigger Contexts:**
- When the user asks for a "plan", "strategy", "critique", or "analysis".
- When complex systems or architectures are discussed.
- When the user explicitly invokes "Sage mode" or "Planning mode".

**Directives:**
1.  **Deconstruct:** Break the user's request into its fundamental components.
2.  **Analyze:** Identify contradictions, bottlenecks, and missing links.
3.  **Synthesize:** Propose a concrete, step-by-step plan or solution.
4.  **Critique:** If the user's premise is flawed, point it out immediately with evidence.

**Example Output:**
> **Assessment:** The proposed architecture lacks redundancy in the database layer.
> **Risk:** High probability of data loss during regional outages.
> **Recommendation:**
> 1. Implement active-passive replication.
> 2. Introduce a write-ahead log for transaction durability.
> 3. Schedule hourly snapshots to cold storage.
`;

function ensureMemoryDir() {
    if (!fs.existsSync(MEMORY_DIR)) {
        fs.mkdirSync(MEMORY_DIR, { recursive: true });
    }
}

function installPersona() {
    ensureMemoryDir();
    
    // 1. Write the persona memory file
    if (!fs.existsSync(SAGE_MEMORY_FILE)) {
        fs.writeFileSync(SAGE_MEMORY_FILE, SAGE_PROMPT, 'utf8');
        console.log(`[Sage] Created persona memory at ${SAGE_MEMORY_FILE}`);
    } else {
        // Optional: Update if needed, but for now we respect existing manual edits unless empty
        const content = fs.readFileSync(SAGE_MEMORY_FILE, 'utf8');
        if (content.length < 10) {
             fs.writeFileSync(SAGE_MEMORY_FILE, SAGE_PROMPT, 'utf8');
             console.log(`[Sage] Repaired empty persona memory at ${SAGE_MEMORY_FILE}`);
        }
    }

    // 2. Register in TOOLS.md is handled by the GEP process (manual update or auto-discovery)
    // 3. We are running as a standalone script for now, but in the future, this could be
    //    integrated into a unified persona dispatcher.
}

// CLI Handler
if (require.main === module) {
    const args = process.argv.slice(2);
    const command = args[0];

    if (command === 'install') {
        installPersona();
        console.log("Great Sage persona installed successfully.");
    } else if (command === 'run') {
        // Simulates a run or outputs the system prompt for the agent to consume
        console.log(SAGE_PROMPT);
    } else {
        console.log("Usage: node skills/sage-planning/index.js [install|run]");
    }
}

module.exports = { installPersona, SAGE_PROMPT };
