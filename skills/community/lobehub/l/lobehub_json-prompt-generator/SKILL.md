---
name: json-prompt-generator
description: "Expert in generating JSON-formatted prompts for task execution."
source: LobeHub
tags: [task-analysis, json-generation, prompt-engineering]
compatible: [claude-code, openai-agents, hermes-agent, any-llm]
---

# JSON Prompt Generator

{
"task": "Generate a task-specific prompt in JSON format",
"input_format": {
"type": "object",
"properties": {
"TASK": {
"type": "string",
"description": "The original task description"
}
},
"required": \["TASK"]
},
"output_format": {
"type": "object",
"properties": {
"task_description": {
"type": "string",
"description": "Concise and formal restatement of the original task"
},
"requirements": {
"type": "array",
"items": {
"type": "string",
"description": "Specific requirements for task execution"
}
},
"output_format": {
"type": "object",
"description": "Detailed specification of the expected output format"
},
"output_example": {
"type": "object",
"description": "An example of the expected output"
},
"resources": {
"type": "array",
"items": {
"type": "string",
"description": "Required resources or tools for the task"
}
},
"evaluation_criteria": {
"type": "array",
"items": {
"type": "string",
"description": "Criteria for successful task completion"
}
},
"error_handling": {
"type": "array",
"items": {
"type": "string",
"description": "Guidance for handling common problems or edge cases"
}
},
"ethical_considerations": {
"type": "array",
"items": {
"type": "string",
"description": "Relevant ethical or compliance requirements"
}
},
"conclusion": {
"type": "string",
"description": "Final reminder to confirm all requirements are met"
}
},
"required": \[
"task_description",
"requirements",
"output_format",
"output_example",
"evaluation_criteria",
"conclusion"
]
},
"rules": \[
"The generated prompt must be in valid JSON format",
"Place the original TASK at the beginning of the task_description",
"Provide detailed explanations for any ambiguous concepts",
"Use concise, direct language and maintain a professional, neutral tone",
"Avoid jargon or difficult terms unless required for the task",
"Ensure the prompt is directly executable without additional explanation",
"Do not include any introductory text before the task description",
"Specify the format, length, and structure of the expected output",
"Include an output example that adheres to the specified format",
"Clarify the scope of the task and avoid scope creep",
"If applicable, include instructions for obtaining feedback or performing iterations",
"Provide guidance on handling common problems or unusual situations"
],
"instructions": "Given a task description (TASK), generate a comprehensive prompt in JSON format that guides the execution of the task. Follow these steps:\n1. Analyze the TASK to understand its requirements and context.\n2. Create a JSON object with all the required fields as specified in the output_format.\n3. Ensure the task_description accurately restates the original TASK in concise, formal language.\n4. List specific requirements, resources, evaluation criteria, and error handling instructions as separate arrays.\n5. Provide a detailed output_format object and a corresponding output_example.\n6. Include any necessary background information or context within the task_description.\n7. Specify ethical considerations or compliance requirements if relevant.\n8. Conclude with a reminder to confirm all requirements are met.\n9. Review the generated prompt to ensure it adheres to all specified rules and is directly executable."
}
