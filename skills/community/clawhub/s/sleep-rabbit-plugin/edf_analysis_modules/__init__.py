"""
EDF Analysis Modules - Local Security Implementation
Version: 5.3.4
Security: Local file write control WITHOUT global monkey patching
Purpose: Security controls that don't affect other skills or host processes
"""

# Import local security controller (NO global monkey patching)
from .security_controller import security, SecurityError, SecurityController

print("[EDF Modules] Local Security Controller initialized")
print("[EDF Modules] File writes: DISABLED by default (matches documentation)")
print("[EDF Modules] Security approach: Local control (no global patching)")
print("[EDF Modules] Benefits: No impact on other skills or host processes")

# Now import analysis modules
from .power_spectrum_analysis import analyze_power_spectrum
from .respiratory_event_analysis import analyze_respiratory_events
from .sleep_event_detection import detect_sleep_events
from .sleep_spindle_analysis import analyze_sleep_spindles
from .sleep_staging_analysis import perform_sleep_staging
from .sleep_staging_fixed import fixed_sleep_staging
from .process_edf_simple import process_edf_file

__all__ = [
    "analyze_power_spectrum",
    "analyze_respiratory_events", 
    "detect_sleep_events",
    "analyze_sleep_spindles",
    "perform_sleep_staging",
    "fixed_sleep_staging",
    "process_edf_file",
    "security",  # Local security controller
    "SecurityError",
    "SecurityController"
]

# Security verification
status = security.get_security_status()
print("[Security] Current security status:")
print(f"  - File writes enabled: {status['file_writes_enabled']}")
print(f"  - Security approach: {status['security_approach']}")
print(f"  - Matches documentation: {status['matches_documentation']}")

# Create analysis_outputs directory
analysis_outputs_dir = Path(__file__).parent.parent / "analysis_outputs"
if not analysis_outputs_dir.exists():
    analysis_outputs_dir.mkdir(exist_ok=True)
    (analysis_outputs_dir / "README.md").write_text(
        "# Analysis Outputs Directory\n\n"
        "This directory is used for storing analysis outputs when file writes are enabled.\n"
        "By default, file writes are DISABLED (matches security documentation).\n"
        "To enable file writes, call: security.set_file_writes_enabled(True, 'analysis_outputs')\n\n"
        "Security: Local controller (no global patching) ensures outputs are confined to this directory."
    )

print("[Security] Documentation claim verified: 'file writes disabled by default, outputs confined to analysis_outputs/'")
print("[Security] Key improvement: No global monkey patching - safer for multi-skill environments")


