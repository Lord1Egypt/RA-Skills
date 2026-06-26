# Health Chat Skill Schema

## Conversation Intent Types

```typescript
type IntentType =
  | "data_query"        // Data query
  | "health_analysis"    // Health analysis
  | "risk_assessment"   // Risk assessment
  | "recommendation"     // Health recommendation
  | "record_operation"   // Record operation
  | "medical_consult"    // Medical consultation
  | "medication"         // Medication related
  | "symptom_inquiry"    // Symptom inquiry
  | "general_chat";      // General conversation
```

## User Input Parsing

```typescript
interface ParsedInput {
  original_text: string;           // User's original input
  intent: IntentType;              // Parsed intent type
  entities: Entity[];               // Recognized entities
  keywords: string[];              // Keyword list
  confidence: number;              // Confidence 0-1
}

interface Entity {
  type: "date" | "body_part" | "symptom" | "metric" | "medication" | "condition";
  value: string;
  normalized?: string;
}
```

## Data Sources Configuration

```typescript
interface DataSource {
  file_path: string;
  description: string;
  priority: "critical" | "high" | "medium" | "low";
  data_type: string;
  required_for: IntentType[];
}

const DATA_SOURCES: DataSource[] = [
  // Core Data - Read every time
  {
    file_path: "data/profile.json",
    description: "User basic information",
    priority: "critical",
    data_type: "basic_info",
    required_for: ["data_query", "health_analysis", "risk_assessment", "recommendation"]
  },
  {
    file_path: "data/user-settings.json",
    description: "User preference settings",
    priority: "critical",
    data_type: "settings",
    required_for: ["data_query", "recommendation"]
  },
  {
    file_path: "data/ai-config.json",
    description: "AI features configuration",
    priority: "critical",
    data_type: "config",
    required_for: ["health_analysis", "risk_assessment"]
  },

  // Chronic Condition Tracking Data
  {
    file_path: "data/hypertension-tracker.json",
    description: "Hypertension management",
    priority: "high",
    data_type: "chronic_condition",
    required_for: ["data_query", "health_analysis", "risk_assessment"]
  },
  {
    file_path: "data/diabetes-tracker.json",
    description: "Diabetes management",
    priority: "high",
    data_type: "chronic_condition",
    required_for: ["data_query", "health_analysis", "risk_assessment"]
  },
  {
    file_path: "data/copd-tracker.json",
    description: "COPD management",
    priority: "medium",
    data_type: "chronic_condition",
    required_for: ["data_query", "health_analysis"]
  },

  // Medication Data
  {
    file_path: "data/medications/medications.json",
    description: "Medication plans",
    priority: "high",
    data_type: "medication",
    required_for: ["medication", "recommendation", "risk_assessment"]
  },
  {
    file_path: "data/interactions/interaction-db.json",
    description: "Drug interactions",
    priority: "medium",
    data_type: "reference",
    required_for: ["medication"]
  },

  // Medical Records
  {
    file_path: "data/allergies.json",
    description: "Allergy records",
    priority: "high",
    data_type: "medical_record",
    required_for: ["medication", "recommendation"]
  },
  {
    file_path: "data/index.json",
    description: "Medical records index",
    priority: "medium",
    data_type: "index",
    required_for: ["data_query", "health_analysis"]
  },

  // Health Management Data
  {
    file_path: "data/health-feeling-logs.json",
    description: "Health feeling logs",
    priority: "medium",
    data_type: "wellness",
    required_for: ["symptom_inquiry", "health_analysis"]
  },

  // Women's Health
  {
    file_path: "data/cycle-tracker.json",
    description: "Menstrual cycle",
    priority: "medium",
    data_type: "womens_health",
    required_for: ["data_query", "health_analysis"]
  },
  {
    file_path: "data/pregnancy-tracker.json",
    description: "Pregnancy tracking",
    priority: "medium",
    data_type: "womens_health",
    required_for: ["data_query", "health_analysis"]
  },
  {
    file_path: "data/postpartum-tracker.json",
    description: "Postpartum management",
    priority: "medium",
    data_type: "womens_health",
    required_for: ["data_query", "health_analysis"]
  },
  {
    file_path: "data/menopause-tracker.json",
    description: "Menopause management",
    priority: "medium",
    data_type: "womens_health",
    required_for: ["data_query", "health_analysis"]
  },

  // Men's Health
  {
    file_path: "data/prostate-tracker.json",
    description: "Prostate health",
    priority: "medium",
    data_type: "mens_health",
    required_for: ["data_query", "health_analysis"]
  },
  {
    file_path: "data/andropause-tracker.json",
    description: "Male menopause",
    priority: "low",
    data_type: "mens_health",
    required_for: ["data_query", "health_analysis"]
  },
  {
    file_path: "data/fertility-tracker.json",
    description: "Fertility health",
    priority: "medium",
    data_type: "mens_health",
    required_for: ["data_query", "health_analysis"]
  },

  // Specialist Health
  {
    file_path: "data/cognitive-assessment.json",
    description: "Cognitive assessment",
    priority: "medium",
    data_type: "specialist",
    required_for: ["health_analysis", "risk_assessment"]
  },
  {
    file_path: "data/eye-health-tracker.json",
    description: "Eye health",
    priority: "medium",
    data_type: "specialist",
    required_for: ["data_query", "health_analysis"]
  },
  {
    file_path: "data/fall-risk-assessment.json",
    description: "Fall risk assessment",
    priority: "medium",
    data_type: "specialist",
    required_for: ["risk_assessment"]
  },
  {
    file_path: "data/growth-tracker.json",
    description: "Growth records",
    priority: "medium",
    data_type: "pediatric",
    required_for: ["data_query", "health_analysis"]
  },

  // Other Health Data
  {
    file_path: "data/family-health-tracker.json",
    description: "Family health",
    priority: "low",
    data_type: "family",
    required_for: ["health_analysis"]
  },
  {
    file_path: "data/reminders.json",
    description: "Reminders",
    priority: "low",
    data_type: "utility",
    required_for: ["data_query"]
  },
  {
    file_path: "data/vaccinations.json",
    description: "Vaccination records",
    priority: "medium",
    data_type: "medical_record",
    required_for: ["data_query", "recommendation"]
  },
  {
    file_path: "data/radiation-records.json",
    description: "Radiation exam records",
    priority: "low",
    data_type: "medical_record",
    required_for: ["data_query"]
  },

  // TCM Data
  {
    file_path: "data/constitutions.json",
    description: "TCM constitution",
    priority: "low",
    data_type: "tcm",
    required_for: ["health_analysis", "recommendation"]
  },

  // Database Files (Read on Demand)
  {
    file_path: "data/food-database.json",
    description: "Food nutrition database",
    priority: "low",
    data_type: "reference",
    required_for: ["recommendation"]
  },
  {
    file_path: "data/vaccine-database.json",
    description: "Vaccine database",
    priority: "low",
    data_type: "reference",
    required_for: ["recommendation"]
  },
  {
    file_path: "data/child-vaccine-database.json",
    description: "Child vaccine database",
    priority: "low",
    data_type: "reference",
    required_for: ["recommendation"]
  },
  {
    file_path: "data/nutritional-reference.json",
    description: "Nutrition reference standards",
    priority: "low",
    data_type: "reference",
    required_for: ["health_analysis", "recommendation"]
  },
  {
    file_path: "data/who-growth-standards.json",
    description: "WHO growth standards",
    priority: "low",
    data_type: "reference",
    required_for: ["health_analysis"]
  }
];
```

## Response Structure

```typescript
interface HealthChatResponse {
  timestamp: string;
  intent: IntentType;
  data_sources_used: string[];
  summary: string;              // Brief summary
  sections: ResponseSection[];
  disclaimer: string;            // Medical disclaimer
  follow_up_suggestions: string[]; // Suggested follow-up questions
}

interface ResponseSection {
  type: "summary" | "alert" | "analysis" | "recommendation" | "trend";
  title: string;
  content: string;
  priority?: "high" | "medium" | "low";
  data_references?: string[];    // Referenced data sources
}
```

## Conversation History

```typescript
interface ConversationEntry {
  timestamp: string;              // ISO 8601 format
  user_input: string;            // User's original input
  intent: IntentType;            // Recognized intent
  data_sources_used: string[];   // Data files used
  response_summary: string;       // Response summary
  follow_up_suggestions: string[]; // Suggested follow-up questions
  user_feedback?: "positive" | "neutral" | "negative"; // User feedback
}

interface AIHistory {
  conversations: ConversationEntry[];
  statistics: {
    total_conversations: number;
    common_topics: string[];
    common_intents: { intent: IntentType; count: number }[];
    last_updated: string;
  };
}
```

## Intent Keyword Mapping

```typescript
const INTENT_KEYWORDS = {
  data_query: [
    "what", "how much", "how many", "recent", "average", "trend", "data",
    "show", "view", "query", "is", "have", "have not"
  ],
  health_analysis: [
    "analyze", "assess", "how is", "status", "overall", "comprehensive",
    "check", "report"
  ],
  risk_assessment: [
    "risk", "danger", "warning", "abnormal", "problem", "serious",
    "need attention", "concerned"
  ],
  recommendation: [
    "suggest", "should", "how to", "improve", "how to increase",
    "should I", "recommend", "improve", "increase", "decrease", "reduce"
  ],
  medication: [
    "med", "medicine", "drug", "take", "dosage", "side effect",
    "interaction", "prescription"
  ],
  symptom_inquiry: [
    "symptom", "discomfort", "pain", "ache", "dizzy", "nausea",
    "fatigue", "insomnia", "cough"
  ],
  medical_consult: [
    "doctor", "hospital", "test", "treatment", "surgery",
    "department", "specialist", "visit"
  ],
  record_operation: [
    "record", "add", "update", "modify", "save", "new",
    "write", "input", "register"
  ],
  general_chat: [
    "hello", "thank", "goodbye", "good morning", "good evening"
  ]
};
```

## Health Domain Keyword Mapping

```typescript
const DOMAIN_KEYWORDS = {
  hypertension: ["blood pressure", "hypertension", "systolic", "diastolic", "mmHg", "BP"],
  diabetes: ["blood sugar", "diabetes", "a1c", "insulin", "glucose"],
  cardiovascular: ["heart", "heart rate", "ecg", "chest pain", "palpitation"],
  respiratory: ["lung", "breathing", "cough", "asthma", "copd"],
  sleep: ["sleep", "insomnia", "dreams", "sleep quality"],
  mental: ["mood", "anxiety", "depression", "stress", "emotion"],
  nutrition: ["diet", "nutrition", "eat", "food", "calories", "weight", "BMI"],
  exercise: ["exercise", "workout", "activity", "steps", "fitness"],
  medication: ["medication", "medicine", "pill", "prescription"],
  womens_health: ["period", "menstruation", "pregnant", "pregnancy", "postpartum", "menopause"],
  mens_health: ["prostate", "male", "testicle", "sperm", "andropause"],
  pediatric: ["child", "kid", "baby", "growth", "development", "vaccine"],
  eye: ["eye", "vision", "sight", "eye pressure", "glasses"],
  cognitive: ["memory", "cognition", "dementia", "alzheimer", "MMSE", "MoCA"],
  allergy: ["allergy", "allergen", "hives", "rhinitis"],
  vaccination: ["vaccine", "vaccination", "shot", "immunization"]
};
```

## Risk Level Definition

```typescript
type RiskLevel = "low" | "moderate" | "high" | "very_high";

interface RiskAssessment {
  category: string;              // Risk category
  level: RiskLevel;              // Risk level
  score: number;                 // Risk score 0-1
  factors: RiskFactor[];         // Risk factors
  recommendations: string[];     // Recommendations
  referral_needed: boolean;      // Whether referral is needed
}

interface RiskFactor {
  name: string;
  value: string | number;
  impact: "positive" | "negative" | "neutral";
  modifiable: boolean;           // Whether it can be changed
}
```

## Medical Disclaimer

```typescript
const MEDICAL_DISCLAIMER = `
⚕️ Medical Disclaimer

The health information provided by this system is for reference only and cannot replace
professional medical advice, diagnosis, or treatment.

• This system does not provide medical diagnosis
• This system does not provide prescription recommendations
• Please consult a healthcare professional for health concerns
• For emergencies, please seek immediate medical attention or call emergency services

Risk assessment results are for reference only; actual risks should be
assessed by a medical professional.
`;
```
