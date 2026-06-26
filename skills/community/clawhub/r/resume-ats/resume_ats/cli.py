"""
CLI interface for Resume/ATS Optimization
"""

from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

from resume_ats.config import Config
from resume_ats.storage.database import Database

app = typer.Typer(
    name="resume-ats",
    help="Resume and ATS optimization tool",
    no_args_is_help=True,
)
console = Console()


@app.command()
def init(
    force: bool = typer.Option(False, "--force", "-f", help="Overwrite existing config"),
) -> None:
    """
    Initialize configuration for resume/ATS optimization
    """
    config_path = Path(".env")

    if config_path.exists() and not force:
        console.print("[yellow]Configuration already exists.[/yellow]")
        if not typer.confirm("Do you want to overwrite?"):
            return

    # Create .env from example
    example_path = Path(__file__).parent.parent / ".env.example"
    if example_path.exists():
        import shutil

        shutil.copy(example_path, config_path)
        console.print("[green]✓ Configuration file created: .env[/green]")
        console.print("\n[yellow]Please edit .env with your settings.[/yellow]")
    else:
        console.print("[red]✗ .env.example not found[/red]")
        raise typer.Exit(1)


@app.command()
def analyze(
    resume_path: Path = typer.Argument(..., help="Path to resume file"),
) -> None:
    """
    Analyze a resume file
    """
    if not resume_path.exists():
        console.print(f"[red]✗ File not found: {resume_path}[/red]")
        raise typer.Exit(1)

    console.print(f"[cyan]Analyzing resume:[/cyan] {resume_path}")

    # Check file type
    if resume_path.suffix.lower() == ".pdf":
        console.print("[yellow]PDF file detected[/yellow]")
        # TODO: Implement PDF parsing
        console.print("[yellow]PDF parsing not yet implemented[/yellow]")
    else:
        console.print("[yellow]Text file detected[/yellow]")
        # TODO: Implement text parsing
        console.print("[yellow]Text parsing not yet implemented[/yellow]")


@app.command()
def score(
    resume_path: Path = typer.Argument(..., help="Path to resume file"),
    job_description: Path = typer.Argument(..., help="Path to job description file"),
) -> None:
    """
    Calculate ATS score for resume vs job description
    """
    if not resume_path.exists():
        console.print(f"[red]✗ Resume file not found: {resume_path}[/red]")
        raise typer.Exit(1)

    if not job_description.exists():
        console.print(f"[red]✗ Job description file not found: {job_description}[/red]")
        raise typer.Exit(1)

    console.print(f"[cyan]Calculating ATS score:[/cyan]")
    console.print(f"  Resume: {resume_path}")
    console.print(f"  Job Description: {job_description}")

    # TODO: Implement ATS scoring
    console.print("[yellow]ATS scoring not yet implemented[/yellow]")


@app.command("keywords")
def keywords(
    action: str = typer.Argument(..., help="Action: extract or compare"),
    resume_path: Path = typer.Option(None, "--resume", "-r", help="Path to resume file"),
    keywords_path: Path = typer.Option(None, "--keywords", "-k", help="Path to keywords file"),
) -> None:
    """
    Keyword operations
    """
    if action == "extract":
        if not resume_path:
            console.print("[red]✗ --resume required for extract[/red]")
            raise typer.Exit(1)

        if not resume_path.exists():
            console.print(f"[red]✗ File not found: {resume_path}[/red]")
            raise typer.Exit(1)

        console.print(f"[cyan]Extracting keywords from:[/cyan] {resume_path}")
        # TODO: Implement keyword extraction
        console.print("[yellow]Keyword extraction not yet implemented[/yellow]")

    elif action == "compare":
        if not resume_path or not keywords_path:
            console.print("[red]✗ --resume and --keywords required for compare[/red]")
            raise typer.Exit(1)

        if not resume_path.exists() or not keywords_path.exists():
            console.print("[red]✗ One or more files not found[/red]")
            raise typer.Exit(1)

        console.print(f"[cyan]Comparing keywords:[/cyan]")
        console.print(f"  Resume: {resume_path}")
        console.print(f"  Keywords: {keywords_path}")
        # TODO: Implement keyword comparison
        console.print("[yellow]Keyword comparison not yet implemented[/yellow]")


@app.command("generate")
def generate(
    template: str = typer.Option("modern", "--template", "-t", help="Resume template"),
    input_path: Path = typer.Option(None, "--input", "-i", help="Input resume file"),
    output_path: Path = typer.Option(None, "--output", "-o", help="Output file path"),
) -> None:
    """
    Generate optimized resume
    """
    if not input_path:
        console.print("[red]✗ --input required[/red]")
        raise typer.Exit(1)

    if not input_path.exists():
        console.print(f"[red]✗ File not found: {input_path}[/red]")
        raise typer.Exit(1)

    console.print(f"[cyan]Generating resume:[/cyan]")
    console.print(f"  Template: {template}")
    console.print(f"  Input: {input_path}")
    console.print(f"  Output: {output_path or 'resume.pdf'}")

    # TODO: Implement resume generation
    console.print("[yellow]Resume generation not yet implemented[/yellow]")


@app.command("config:show")
def config_show() -> None:
    """
    Show current configuration
    """
    try:
        config = Config.load()

        console.print("[cyan]Current Configuration:[/cyan]")
        console.print(f"  Default Template: {config.default_template}")
        console.print(f"  Output Format: {config.output_format}")
        console.print(f"  Font Size: {config.font_size}")
        console.print(f"  Font Family: {config.font_family}")

    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
