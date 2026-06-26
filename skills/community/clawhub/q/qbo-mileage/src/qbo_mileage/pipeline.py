from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .adapters import build_adapters
from .config import MileageConfig
from .csv_writer import write_qbo_csv
from .dates import month_bounds
from .distance import build_distance_engine
from .models import CalendarEvent, RunResult, RunWarning
from .report import write_report
from .senders import maybe_send_email
from .trip_builder import TripBuilder


@dataclass(frozen=True)
class GenerateOptions:
    month: str
    dry_run: bool = False
    skip_distance: bool = False
    skip_email: bool = False


def generate(config: MileageConfig, options: GenerateOptions) -> RunResult:
    start, end = month_bounds(options.month, config.timezone)

    rate: float | None = None
    if not options.skip_distance:
        # Fail fast on a missing IRS rate before spending any source API calls.
        rate = config.rate_for_year(start.year)

    events: list[CalendarEvent] = []
    warnings: list[RunWarning] = []

    for adapter in build_adapters(config):
        try:
            events.extend(adapter.fetch_events(start, end))
        except Exception as exc:  # noqa: BLE001 - report and continue other sources
            warnings.append(
                RunWarning(
                    code="source_failed",
                    message=f"{adapter.source_name} failed: {exc}",
                    source=adapter.source_name,
                )
            )

    builder = TripBuilder(
        home_base=config.home_base,
        default_vehicle=config.vehicle,
        chain_threshold_hours=config.chain_threshold_hours,
        assume_round_trip_if_alone=config.assume_round_trip_if_alone,
        reset_chain_on_day_boundary=config.reset_chain_on_day_boundary,
    )
    legs, build_warnings = builder.build(events)
    warnings.extend(build_warnings)

    if not options.skip_distance:
        engine, cache = build_distance_engine(config.distance)
        resolved_legs = []
        for leg in legs:
            try:
                leg.distance_miles = engine.miles(leg.start_address, leg.end_address)
                if leg.trip_type == "BUSINESS":
                    leg.deduction = round(leg.distance_miles * rate, 2)
                else:
                    # Personal mileage is not deductible; export 0.00 so the
                    # CSV never overstates the deduction total.
                    leg.deduction = 0.0
                resolved_legs.append(leg)
            except Exception as exc:  # noqa: BLE001 - keep run report useful
                warnings.append(
                    RunWarning(
                        code="distance_failed",
                        message=f"{leg.start_address} -> {leg.end_address}: {exc}",
                        event_id=leg.source_event_id,
                        source=leg.source,
                    )
                )
        cache.save()
        legs = resolved_legs
    elif not options.dry_run:
        warnings.append(
            RunWarning(
                code="distance_skipped",
                message="Distance calculation was skipped; exported rows will have blank Distance and Deduction values.",
            )
        )

    result = RunResult(month=options.month, events=sorted(events, key=lambda e: e.start), legs=legs, warnings=warnings)

    if options.dry_run:
        return result

    output_dir = output_directory(config, options.month)
    attachments: list[Path] = []

    if config.output.write_csv:
        csv_path = output_dir / f"mileage_{options.month}.csv"
        result.csv_path = str(write_qbo_csv(csv_path, result.legs))
        attachments.append(Path(result.csv_path))

    if config.output.write_report:
        report_path = output_dir / "run_report.md"
        result.report_path = str(write_report(report_path, result))
        attachments.append(Path(result.report_path))

    if not options.skip_email:
        maybe_send_email(config.email, result, attachments)

    return result


def output_directory(config: MileageConfig, month: str) -> Path:
    directory = Path(config.output.directory)
    if not directory.is_absolute():
        directory = config.path.parent / directory
    return directory / month
