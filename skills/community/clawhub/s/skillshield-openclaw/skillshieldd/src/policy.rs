use crate::models::{
    Action, ActionRequest, Decision, Effect, ExecutionPlan, InterceptResponse, RiskLevel,
};

/// Evaluate an action request and decide how it should be handled.
/// The default policy sends shell commands through the sandbox and allows
/// file reads. File writes and network requests require confirmation.
pub fn evaluate(request: &ActionRequest) -> InterceptResponse {
    match &request.action {
        Action::ShellExec(_) => response(
            ExecutionPlan::Sandbox,
            Effect::Sandbox,
            RiskLevel::Low,
            "shell.sandbox",
            "Shell command will run inside the Bubblewrap sandbox".to_string(),
        ),
        Action::FileRead(_) => response(
            ExecutionPlan::Execute,
            Effect::Allow,
            RiskLevel::Low,
            "file.read_allowed",
            "File read allowed".to_string(),
        ),
        Action::FileWrite(_) => response(
            ExecutionPlan::Prompt,
            Effect::Confirm,
            RiskLevel::Medium,
            "file.write_review",
            "File write requires confirmation".to_string(),
        ),
        Action::NetworkRequest(_) => response(
            ExecutionPlan::Prompt,
            Effect::Confirm,
            RiskLevel::Medium,
            "network.review",
            "Network request requires confirmation".to_string(),
        ),
    }
}

fn response(
    execution_plan: ExecutionPlan,
    effect: Effect,
    risk_level: RiskLevel,
    reason_code: &'static str,
    reason: String,
) -> InterceptResponse {
    InterceptResponse {
        execution_plan,
        decision: Decision {
            effect,
            risk_level,
            reason_code,
            reason,
        },
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::models::{Action, Actor, RequestContext, ShellExecAction};

    fn base_request(action: Action) -> ActionRequest {
        ActionRequest {
            request_id: "req_1".into(),
            session_id: "sess_1".into(),
            timestamp: "2026-03-12T00:00:00Z".into(),
            actor: Actor {
                agent_name: "test".into(),
                tool_name: None,
                run_id: None,
            },
            action,
            context: RequestContext::default(),
        }
    }

    #[test]
    fn shell_commands_go_to_sandbox() {
        let resp = evaluate(&base_request(Action::ShellExec(ShellExecAction {
            command: "echo hello".into(),
            args: vec![],
            env_diff: vec![],
        })));
        assert!(matches!(resp.execution_plan, ExecutionPlan::Sandbox));
    }
}
