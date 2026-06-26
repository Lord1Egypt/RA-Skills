use anyhow::{Result, bail};
use async_trait::async_trait;

#[derive(Debug, Clone)]
pub struct ExecutionOutcome {
    pub exit_code: i32,
    pub stdout: String,
    pub stderr: String,
}

#[async_trait]
pub trait SandboxExecutor: Send + Sync {
    async fn execute_shell(
        &self,
        command: &str,
        working_dir: Option<&str>,
    ) -> Result<ExecutionOutcome>;

    fn name(&self) -> &'static str;
}

/// Runs commands inside a Bubblewrap (`bwrap`) user namespace.
/// The root filesystem is read-only; only `/tmp` and the working directory
/// (if supplied) are writable.
pub struct BwrapExecutor;

#[async_trait]
impl SandboxExecutor for BwrapExecutor {
    async fn execute_shell(
        &self,
        command: &str,
        working_dir: Option<&str>,
    ) -> Result<ExecutionOutcome> {
        let mut cmd = tokio::process::Command::new("bwrap");

        cmd.arg("--unshare-all")
            .arg("--ro-bind")
            .arg("/usr")
            .arg("/usr")
            .arg("--symlink")
            .arg("usr/lib")
            .arg("/lib")
            .arg("--symlink")
            .arg("usr/lib64")
            .arg("/lib64")
            .arg("--symlink")
            .arg("usr/bin")
            .arg("/bin")
            .arg("--symlink")
            .arg("usr/sbin")
            .arg("/sbin")
            .arg("--dir")
            .arg("/tmp")
            .arg("--dev")
            .arg("/dev")
            .arg("--proc")
            .arg("/proc");

        if let Some(dir) = working_dir {
            cmd.arg("--bind").arg(dir).arg(dir);
            cmd.current_dir(dir);
        }

        cmd.arg("--").arg("sh").arg("-c").arg(command);

        let output = cmd.output().await?;

        Ok(ExecutionOutcome {
            exit_code: output.status.code().unwrap_or(-1),
            stdout: String::from_utf8_lossy(&output.stdout).to_string(),
            stderr: String::from_utf8_lossy(&output.stderr).to_string(),
        })
    }

    fn name(&self) -> &'static str {
        "bubblewrap-linux"
    }
}

/// Return a BwrapExecutor if `bwrap` is available, otherwise return an error.
pub async fn get_executor() -> Result<std::sync::Arc<dyn SandboxExecutor>> {
    #[cfg(target_os = "linux")]
    {
        if std::process::Command::new("which")
            .arg("bwrap")
            .output()
            .is_ok_and(|out| out.status.success())
        {
            return Ok(std::sync::Arc::new(BwrapExecutor));
        }
    }

    bail!("bubblewrap (bwrap) is not installed on this host")
}
