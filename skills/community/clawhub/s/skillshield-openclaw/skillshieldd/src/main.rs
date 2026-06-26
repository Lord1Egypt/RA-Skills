mod models;
mod policy;
mod sandbox;

use std::sync::Arc;
#[cfg(unix)]
use tokio::net::UnixListener;
use tokio::net::TcpListener;

use anyhow::Context;
use axum::{extract::State, routing::{get, post}, Json, Router};
use models::{
    Action, ActionRequest, Actor, ExecuteOutcome, ExecuteRequest, ExecuteResponse, HealthResponse,
    InterceptRequestEnvelope, InterceptResponse, RequestContext, ShellExecAction,
};
use tracing_subscriber::{layer::SubscriberExt, util::SubscriberInitExt};

use sandbox::{SandboxExecutor, get_executor};

#[derive(Clone)]
struct AppState {
    executor: Arc<dyn SandboxExecutor>,
}

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    tracing_subscriber::registry()
        .with(tracing_subscriber::EnvFilter::try_from_default_env().unwrap_or_else(|_| "skillshieldd=info,tower_http=info".into()))
        .with(tracing_subscriber::fmt::layer())
        .init();

    let executor: Arc<dyn SandboxExecutor> = get_executor().await
        .context("Cannot start without bubblewrap")?;
    tracing::info!("sandbox executor: {}", executor.name());

    let app = Router::new()
        .route("/health", get(health))
        .route("/v1/intercept", post(intercept))
        .route("/v1/execute", post(execute))
        .with_state(AppState { executor });

    let bind_mode = std::env::var("SKILLSHIELDD_BIND").unwrap_or_else(|_| "unix:/tmp/skillshieldd.sock".into());

    if bind_mode.starts_with("unix:") {
        #[cfg(unix)]
        {
            let path = bind_mode.trim_start_matches("unix:");
            let _ = std::fs::remove_file(path);
            tracing::info!("listening on unix socket: {}", path);
            let listener = UnixListener::bind(path).context("failed to bind unix socket")?;

            use tower::Service;
            loop {
                let (stream, _) = listener.accept().await?;
                let app = app.clone();
                let io = hyper_util::rt::TokioIo::new(stream);

                tokio::spawn(async move {
                    let service = hyper::service::service_fn(move |req: hyper::Request<hyper::body::Incoming>| {
                        let mut app = app.clone();
                        async move { app.call(req).await }
                    });

                    if let Err(e) = hyper_util::server::conn::auto::Builder::new(hyper_util::rt::TokioExecutor::new())
                        .serve_connection(io, service)
                        .await
                    {
                        tracing::trace!("connection closed: {}", e);
                    }
                });
            }
        }
        #[cfg(not(unix))]
        {
            anyhow::bail!("Unix sockets require a Unix-like OS");
        }
    } else {
        tracing::info!("listening on tcp: {}", bind_mode);
        let listener = TcpListener::bind(&bind_mode).await.context("failed to bind tcp")?;
        axum::serve(listener, app).await?;
        Ok(())
    }
}

async fn health(State(state): State<AppState>) -> Json<HealthResponse> {
    Json(HealthResponse {
        ok: true,
        service: "skillshieldd",
        executor: state.executor.name(),
    })
}

async fn intercept(
    State(_state): State<AppState>,
    Json(payload): Json<InterceptRequestEnvelope>,
) -> Json<InterceptResponse> {
    Json(policy::evaluate(&payload.request))
}

async fn execute(
    State(state): State<AppState>,
    Json(payload): Json<ExecuteRequest>,
) -> Json<ExecuteResponse> {
    let request = ActionRequest {
        request_id: "exec".into(),
        session_id: "exec".into(),
        timestamp: timestamp_now(),
        actor: Actor {
            agent_name: "skillshield-wrapper".into(),
            tool_name: Some("skillshield-exec.sh".into()),
            run_id: None,
        },
        action: Action::ShellExec(ShellExecAction {
            command: payload.command.clone(),
            args: vec![],
            env_diff: vec![],
        }),
        context: RequestContext {
            cwd: payload.cwd.clone(),
            workspace_root: payload.cwd.clone(),
            requires_approval: false,
        },
    };

    let decision = policy::evaluate(&request);
    let executor_name = state.executor.name().to_string();

    match decision.execution_plan {
        models::ExecutionPlan::Execute | models::ExecutionPlan::Sandbox => {
            match state
                .executor
                .execute_shell(&payload.command, payload.cwd.as_deref())
                .await
            {
                Ok(outcome) => Json(ExecuteResponse {
                    execution_plan: decision.execution_plan,
                    decision: decision.decision,
                    executor: executor_name,
                    outcome: Some(ExecuteOutcome {
                        exit_code: outcome.exit_code,
                        stdout: outcome.stdout,
                        stderr: outcome.stderr,
                    }),
                }),
                Err(error) => Json(ExecuteResponse {
                    execution_plan: models::ExecutionPlan::Block,
                    decision: models::Decision {
                        effect: models::Effect::Deny,
                        risk_level: models::RiskLevel::High,
                        reason_code: "sandbox.error",
                        reason: format!("Execution error: {error}"),
                    },
                    executor: executor_name,
                    outcome: Some(ExecuteOutcome {
                        exit_code: 125,
                        stdout: String::new(),
                        stderr: error.to_string(),
                    }),
                }),
            }
        }
        _ => {
            let stderr = decision.decision.reason.clone();
            Json(ExecuteResponse {
                execution_plan: decision.execution_plan.clone(),
                decision: decision.decision,
                executor: executor_name,
                outcome: Some(ExecuteOutcome {
                    exit_code: 126,
                    stdout: String::new(),
                    stderr,
                }),
            })
        }
    }
}

fn timestamp_now() -> String {
    use std::time::{SystemTime, UNIX_EPOCH};
    let secs = SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .unwrap_or_default()
        .as_secs();
    format!("{secs}Z")
}
