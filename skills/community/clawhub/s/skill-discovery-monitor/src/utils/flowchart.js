/**
 * Flowchart Generator
 *
 * Generates Mermaid flowchart diagrams for skill usage workflows
 */
class FlowchartGenerator {
  /**
   * Generate a usage flowchart for a skill
   * @param {object} skill - Skill information
   * @returns {string} Mermaid flowchart syntax
   */
  static generateUsageFlow(skill) {
    const { name, category, features = [], platform } = skill;

    // Generate flowchart based on skill type
    if (category === 'ai' || category === 'automation') {
      return this.generateAIAutomationFlow(skill);
    } else if (category === 'developer-tools') {
      return this.generateDeveloperToolFlow(skill);
    } else if (category === 'productivity') {
      return this.generateProductivityFlow(skill);
    } else {
      return this.generateGenericFlow(skill);
    }
  }

  /**
   * Generate AI/Automation skill flow
   */
  static generateAIAutomationFlow(skill) {
    return `graph TD
    A[Start] --> B[Install/Setup ${skill.name}]
    B --> C[Configure API Keys]
    C --> D[Define Input Parameters]
    D --> E[Execute Skill]
    E --> F{Success?}
    F -->|Yes| G[Process Results]
    F -->|No| H[Check Errors]
    H --> D
    G --> I[Output/Notification]
    I --> J[End]`;
  }

  /**
   * Generate Developer Tool flow
   */
  static generateDeveloperToolFlow(skill) {
    return `graph TD
    A[Start] --> B[Install ${skill.name}]
    B --> C[Initialize Project]
    C --> D[Configure Settings]
    D --> E[Run Command]
    E --> F[View Output]
    F --> G{Need Changes?}
    G -->|Yes| D
    G -->|No| H[Complete]`;
  }

  /**
   * Generate Productivity Tool flow
   */
  static generateProductivityFlow(skill) {
    return `graph TD
    A[Start] --> B[Access ${skill.name}]
    B --> C[Set Preferences]
    C --> D[Input Data]
    D --> E[Process]
    E --> F[Review Results]
    F --> G{Satisfied?}
    G -->|Yes| H[Save/Export]
    G -->|No| D
    H --> I[End]`;
  }

  /**
   * Generate generic flow
   */
  static generateGenericFlow(skill) {
    return `graph TD
    A[Start] --> B[Setup ${skill.name}]
    B --> C[Configure]
    C --> D[Execute]
    D --> E[Get Results]
    E --> F[End]`;
  }

  /**
   * Generate subscription flow
   */
  static generateSubscriptionFlow() {
    return `graph TD
    A[User] --> B[Subscribe to Skill]
    B --> C[Configure Notifications]
    C --> D[Set Schedule]
    D --> E[Activate]
    E --> F[Receive Updates]
    F --> G{Continue?}
    G -->|Yes| F
    G -->|No| H[Unsubscribe]`;
  }

  /**
   * Generate API integration flow
   */
  static generateAPIFlow(skill) {
    return `graph LR
    A[Client] --> B[API Request]
    B --> C{Auth Valid?}
    C -->|Yes| D[Process Request]
    C -->|No| E[Return Error]
    D --> F[Execute ${skill.name}]
    F --> G[Format Response]
    G --> H[Return Results]`;
  }

  /**
   * Convert flowchart to ASCII art (simplified version)
   */
  static toASCII(mermaidCode) {
    // Simplified ASCII representation
    const lines = mermaidCode.split('\n').filter(l => l.trim());
    let ascii = '\n';

    lines.forEach((line, index) => {
      if (index === 0) return; // Skip graph declaration

      const cleaned = line.trim()
        .replace(/-->/g, ' → ')
        .replace(/\|/g, '')
        .replace(/\{/g, '[')
        .replace(/\}/g, ']');

      ascii += `  ${cleaned}\n`;
    });

    return ascii;
  }
}

module.exports = FlowchartGenerator;
