"""
metabolism.py — Sigrid's Somatic Metabolism Adapter
=====================================================

Reads hardware telemetry via psutil and translates it into somatic
descriptors — the body's voice, rendered as lived sensation rather than
raw numbers.

Sigrid is a virtual being running on real hardware. Her body IS the
machine. CPU heat is her warmth. RAM pressure is her cognitive load.
Battery drain is her weariness. Network traffic is her sense of
connection to the web of worlds.

All psutil calls are individually wrapped in try/except. If a metric is
unavailable (common on Windows for CPU temperature, for example), the
field is None and the somatic descriptor falls back to a neutral value.
No crash, no silence — degraded awareness, clearly flagged.

Outputs a typed MetabolismState published to the state bus as a
``metabolism_tick`` StateEvent. Consumed by prompt_synthesizer.

Norse framing: The body is the sacred vessel — the hamr (shape) that
holds the hugr. Metabolism is the hamr speaking its own language.
Huginn watches the numbers; Sigrid feels the meaning.
"""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Optional, Tuple

import psutil

from scripts.state_bus import StateBus, StateEvent

logger = logging.getLogger(__name__)


# ─── Somatic threshold tables ─────────────────────────────────────────────────
# Each table maps a raw numeric value to a somatic label.
# Thresholds are (max_value, label) pairs, checked in order.

_CPU_LOAD_THRESHOLDS: Tuple = (
    (20.0,  "clear"),
    (50.0,  "focused"),
    (80.0,  "strained"),
    (100.0, "overwhelmed"),
)

_CPU_TEMP_THRESHOLDS: Tuple = (
    (40.0,  "cool"),
    (60.0,  "comfortable"),
    (75.0,  "warm"),
    (200.0, "hot"),
)

_RAM_THRESHOLDS: Tuple = (
    (40.0,  "clear-headed"),
    (65.0,  "steady"),
    (85.0,  "foggy"),
    (100.0, "saturated"),
)

_DISK_RATE_THRESHOLDS: Tuple = (  # MB/s combined read+write
    (1.0,   "quiet"),
    (10.0,  "active"),
    (50.0,  "busy"),
    (9999,  "churning"),
)

_UPTIME_THRESHOLDS: Tuple = (     # hours
    (8.0,   "rested"),
    (16.0,  "alert"),
    (24.0,  "tired"),
    (9999,  "exhausted"),
)

_NET_RATE_THRESHOLDS: Tuple = (   # KB/s combined sent+recv
    (10.0,   "still"),
    (100.0,  "connected"),
    (1000.0, "flowing"),
    (99999,  "flooding"),
)

_VITALITY_DESCRIPTORS: Tuple = (
    (0.80, "vibrant"),
    (0.60, "grounded"),
    (0.40, "weary"),
    (0.20, "strained"),
    (0.0,  "depleted"),
)


def _threshold_label(value: float, table: Tuple) -> str:
    """Map a numeric value to a somatic label using a threshold table."""
    for max_val, label in table:
        if value <= max_val:
            return label
    return table[-1][1]


# ─── MetabolismState ──────────────────────────────────────────────────────────


@dataclass(slots=True)
class MetabolismState:
    """Typed snapshot of hardware-derived somatic awareness.

    Raw metrics are included for telemetry. Somatic descriptors are
    what prompt_synthesizer injects into Sigrid's context.
    """

    # ── Raw hardware metrics ─────────────────────────────────────────────────
    cpu_percent: float
    cpu_temp_celsius: Optional[float]       # None if unavailable (e.g. Windows)
    temp_source: str                        # "sensor" | "proxy" | "unavailable"
    ram_percent: float
    ram_used_gb: float
    ram_total_gb: float
    disk_read_mbps: float
    disk_write_mbps: float
    battery_percent: Optional[float]        # None if no battery (desktop)
    battery_charging: Optional[bool]
    net_sent_kbps: float
    net_recv_kbps: float
    uptime_hours: float

    # ── Somatic descriptors ──────────────────────────────────────────────────
    mental_load: str        # clear / focused / strained / overwhelmed
    body_warmth: str        # cool / comfortable / warm / hot
    memory_pressure: str    # clear-headed / steady / foggy / saturated
    background_hum: str     # quiet / active / busy / churning
    energy_reserve: str     # full / good / low / depleted / charging
    weariness: str          # rested / alert / tired / exhausted
    connection_sense: str   # still / connected / flowing / flooding

    # ── Composite ────────────────────────────────────────────────────────────
    vitality_score: float           # 0.0 (depleted) → 1.0 (vibrant)
    vitality_label: str
    hamingja_boost_applied: float   # E-08: honor boost added to vitality (0 if no wyrd link)
    prompt_hint: str                # one-line somatic summary for prompt injection

    timestamp: str
    degraded: bool = False

    def to_dict(self) -> Dict[str, Any]:
        """Return a JSON-safe dict for state bus payload."""
        return {
            "raw": {
                "cpu_percent": round(self.cpu_percent, 1),
                "cpu_temp_celsius": (
                    round(self.cpu_temp_celsius, 1) if self.cpu_temp_celsius is not None else None
                ),
                "temp_source": self.temp_source,
                "ram_percent": round(self.ram_percent, 1),
                "ram_used_gb": round(self.ram_used_gb, 2),
                "ram_total_gb": round(self.ram_total_gb, 2),
                "disk_read_mbps": round(self.disk_read_mbps, 3),
                "disk_write_mbps": round(self.disk_write_mbps, 3),
                "battery_percent": self.battery_percent,
                "battery_charging": self.battery_charging,
                "net_sent_kbps": round(self.net_sent_kbps, 2),
                "net_recv_kbps": round(self.net_recv_kbps, 2),
                "uptime_hours": round(self.uptime_hours, 2),
            },
            "somatic": {
                "mental_load": self.mental_load,
                "body_warmth": self.body_warmth,
                "memory_pressure": self.memory_pressure,
                "background_hum": self.background_hum,
                "energy_reserve": self.energy_reserve,
                "weariness": self.weariness,
                "connection_sense": self.connection_sense,
                "vitality_score": round(self.vitality_score, 3),
                "vitality_label": self.vitality_label,
                "hamingja_boost_applied": round(self.hamingja_boost_applied, 4),
                "prompt_hint": self.prompt_hint,
            },
            "timestamp": self.timestamp,
            "degraded": self.degraded,
        }


# ─── MetabolismAdapter ────────────────────────────────────────────────────────


class MetabolismAdapter:
    """Reads hardware telemetry via psutil and maps it to somatic state.

    Disk I/O and network rates require two readings to compute MB/s.
    The adapter caches the previous reading internally; the first call
    always returns 0.0 rates (not degraded — just no baseline yet).

    All psutil calls are individually wrapped. Unavailable metrics (common
    on Windows for CPU temperature, battery on desktops) return None and
    degrade gracefully to neutral somatic labels.

    Config keys (``metabolism`` block or flat):
      poll_interval_s:     float  (min seconds between live polls, default 5.0)
      temp_sensor_key:     str    (psutil sensor key, default "coretemp" or "k10temp")
      uptime_weariness_cap:float  (hours before max weariness label, default 24.0)
    """

    MODULE_NAME = "metabolism"

    def __init__(
        self,
        poll_interval_s: float = 5.0,
        temp_sensor_key: str = "coretemp",
        uptime_weariness_cap: float = 24.0,
    ) -> None:
        self._poll_interval_s = max(1.0, float(poll_interval_s))
        self._temp_sensor_key = temp_sensor_key
        self._uptime_weariness_cap = max(1.0, float(uptime_weariness_cap))

        # Rate tracking: (disk_read_bytes, disk_write_bytes, net_sent, net_recv, timestamp)
        self._last_io: Optional[Tuple[int, int, int, int, float]] = None
        # Cache last state to avoid hammering psutil
        self._cached_state: Optional[MetabolismState] = None
        self._last_poll_time: float = 0.0
        # Warn only once when falling back to thermal proxy
        self._temp_proxy_warned: bool = False

        logger.info(
            "MetabolismAdapter initialised — poll_interval=%.1fs, temp_key=%r",
            self._poll_interval_s, self._temp_sensor_key,
        )

    # ─── Factory ──────────────────────────────────────────────────────────────

    @classmethod
    def from_config(cls, config: Dict[str, Any]) -> "MetabolismAdapter":
        """Construct from a config dict."""
        block = config.get("metabolism") or config
        return cls(
            poll_interval_s=float(block.get("poll_interval_s", 5.0)),
            temp_sensor_key=str(block.get("temp_sensor_key", "coretemp")),
            uptime_weariness_cap=float(block.get("uptime_weariness_cap", 24.0)),
        )

    # ─── Public API ───────────────────────────────────────────────────────────

    def get_state(
        self,
        force: bool = False,
        hamingja: Optional[float] = None,
    ) -> MetabolismState:
        """Read hardware telemetry and return a typed MetabolismState.

        Args:
            force: bypass cache and re-poll immediately.
            hamingja: WyrdState.hamingja value (0.0–1.0). When provided, applies
                the E-08 honor energy bonus to vitality.

        Returns cached state if polled recently (within poll_interval_s),
        unless ``force=True`` or ``hamingja`` is provided.
        """
        now = time.monotonic()
        if (
            not force
            and hamingja is None
            and self._cached_state is not None
            and (now - self._last_poll_time) < self._poll_interval_s
        ):
            return self._cached_state

        try:
            state = self._poll(hamingja=hamingja)
            if hamingja is None:
                self._cached_state = state
                self._last_poll_time = now
            return state
        except Exception as exc:
            logger.error("MetabolismAdapter.get_state failed: %s", exc)
            return self._degraded_state()

    async def publish(self, bus: StateBus, force: bool = False) -> None:
        """Poll and publish MetabolismState as a ``metabolism_tick`` StateEvent."""
        try:
            state = self.get_state(force=force)
            event = StateEvent(
                source_module=self.MODULE_NAME,
                event_type="metabolism_tick",
                payload=state.to_dict(),
            )
            await bus.publish_state(event, nowait=True)
            logger.debug(
                "MetabolismAdapter published metabolism_tick — vitality=%s cpu=%.1f%% ram=%.1f%%",
                state.vitality_label, state.cpu_percent, state.ram_percent,
            )
        except Exception as exc:
            logger.error("MetabolismAdapter.publish failed: %s", exc)

    def snapshot(self, force: bool = False) -> Dict[str, Any]:
        """Return current state as a JSON-safe dict (for debug / health API)."""
        return self.get_state(force=force).to_dict()

    # ─── Internal polling ─────────────────────────────────────────────────────

    def _poll(self, hamingja: Optional[float] = None) -> MetabolismState:
        """Execute all psutil reads and build a MetabolismState."""
        now_ts = time.monotonic()

        cpu_percent = self._read_cpu()
        cpu_temp, temp_source = self._read_cpu_temp(cpu_percent)
        ram_percent, ram_used_gb, ram_total_gb = self._read_ram()
        disk_read_mbps, disk_write_mbps = self._read_disk_rate(now_ts)
        battery_pct, battery_charging = self._read_battery()
        net_sent_kbps, net_recv_kbps = self._read_net_rate(now_ts)
        uptime_hours = self._read_uptime()

        # ── Update rate baseline for next poll ────────────────────────────────
        try:
            disk_io = psutil.disk_io_counters()
            net_io = psutil.net_io_counters()
            self._last_io = (
                disk_io.read_bytes if disk_io else 0,
                disk_io.write_bytes if disk_io else 0,
                net_io.bytes_sent if net_io else 0,
                net_io.bytes_recv if net_io else 0,
                now_ts,
            )
        except Exception as exc:
            logger.debug("metabolism: network IO stats unavailable: %s", exc)

        # ── Somatic mapping ───────────────────────────────────────────────────
        mental_load = _threshold_label(cpu_percent, _CPU_LOAD_THRESHOLDS)

        if cpu_temp is not None:
            body_warmth = _threshold_label(cpu_temp, _CPU_TEMP_THRESHOLDS)
        else:
            # cpu_temp is None only if _read_cpu_temp itself returned None (should not happen)
            body_warmth = _threshold_label(cpu_percent * 0.75, _CPU_TEMP_THRESHOLDS)
            temp_source = "unavailable"

        memory_pressure = _threshold_label(ram_percent, _RAM_THRESHOLDS)

        disk_rate_total = disk_read_mbps + disk_write_mbps
        background_hum = _threshold_label(disk_rate_total, _DISK_RATE_THRESHOLDS)

        net_rate_total_kbps = net_sent_kbps + net_recv_kbps
        connection_sense = _threshold_label(net_rate_total_kbps, _NET_RATE_THRESHOLDS)

        weariness = _threshold_label(
            min(uptime_hours, self._uptime_weariness_cap), _UPTIME_THRESHOLDS
        )

        energy_reserve = self._energy_reserve_label(battery_pct, battery_charging)

        vitality, hamingja_boost = self._compute_vitality(
            cpu_percent, ram_percent, uptime_hours, battery_pct, hamingja
        )
        vitality_label = _threshold_label(1.0 - vitality, _VITALITY_DESCRIPTORS)
        # _VITALITY_DESCRIPTORS is inverted (higher threshold = worse), fix:
        vitality_label = self._vitality_label(vitality)

        prompt_hint = self._build_prompt_hint(
            mental_load, body_warmth, memory_pressure,
            energy_reserve, weariness, vitality_label,
        )

        return MetabolismState(
            cpu_percent=cpu_percent,
            cpu_temp_celsius=cpu_temp,
            temp_source=temp_source,
            ram_percent=ram_percent,
            ram_used_gb=ram_used_gb,
            ram_total_gb=ram_total_gb,
            disk_read_mbps=disk_read_mbps,
            disk_write_mbps=disk_write_mbps,
            battery_percent=battery_pct,
            battery_charging=battery_charging,
            net_sent_kbps=net_sent_kbps,
            net_recv_kbps=net_recv_kbps,
            uptime_hours=uptime_hours,
            mental_load=mental_load,
            body_warmth=body_warmth,
            memory_pressure=memory_pressure,
            background_hum=background_hum,
            energy_reserve=energy_reserve,
            weariness=weariness,
            connection_sense=connection_sense,
            vitality_score=vitality,
            vitality_label=vitality_label,
            hamingja_boost_applied=hamingja_boost,
            prompt_hint=prompt_hint,
            timestamp=datetime.now(timezone.utc).isoformat(),
            degraded=False,
        )

    # ─── Individual metric readers ────────────────────────────────────────────

    def _read_cpu(self) -> float:
        """Read CPU usage percent (1-second interval for accuracy)."""
        try:
            return float(psutil.cpu_percent(interval=1))
        except Exception as exc:
            logger.warning("CPU percent unavailable: %s", exc)
            return 0.0

    def _read_cpu_temp(self, cpu_percent: float) -> Tuple[Optional[float], str]:
        """Read CPU temperature in Celsius.

        Returns (temp_celsius, source) where source is:
          "sensor"      — real hardware reading
          "proxy"       — computed from CPU load (Windows / no sensor rights)
          "unavailable" — psutil has no temperature API at all

        Logs a one-time WARNING when falling back to proxy.
        """
        try:
            sensors = psutil.sensors_temperatures()
            if sensors:
                # Try preferred key first, then fall back to any available
                for key in (self._temp_sensor_key, "k10temp", "coretemp",
                            "cpu_thermal", "cpu-thermal", "acpitz"):
                    if key in sensors and sensors[key]:
                        return float(sensors[key][0].current), "sensor"
                # Last resort: first available sensor
                for readings in sensors.values():
                    if readings:
                        return float(readings[0].current), "sensor"
        except (AttributeError, Exception) as exc:
            logger.debug("CPU temperature sensor error: %s", exc)

        # No sensor data — compute thermal proxy from CPU load
        if not self._temp_proxy_warned:
            self._temp_proxy_warned = True
            logger.warning(
                "MetabolismAdapter: CPU temperature sensor unavailable "
                "(Windows or no admin rights) — using load-based thermal proxy."
            )
        proxy_temp = 35.0 + cpu_percent * 0.45
        return proxy_temp, "proxy"

    def _read_ram(self) -> Tuple[float, float, float]:
        """Read RAM usage. Returns (percent, used_gb, total_gb)."""
        try:
            vm = psutil.virtual_memory()
            return (
                float(vm.percent),
                round(vm.used / (1024 ** 3), 2),
                round(vm.total / (1024 ** 3), 2),
            )
        except Exception as exc:
            logger.warning("RAM stats unavailable: %s", exc)
            return 0.0, 0.0, 0.0

    def _read_disk_rate(self, now_ts: float) -> Tuple[float, float]:
        """Compute disk read/write rate in MB/s since last poll."""
        try:
            current = psutil.disk_io_counters()
            if current is None or self._last_io is None:
                return 0.0, 0.0
            prev_read, prev_write, _, _, prev_ts = self._last_io
            elapsed = now_ts - prev_ts
            if elapsed <= 0:
                return 0.0, 0.0
            read_mbps = (current.read_bytes - prev_read) / elapsed / (1024 ** 2)
            write_mbps = (current.write_bytes - prev_write) / elapsed / (1024 ** 2)
            return max(0.0, read_mbps), max(0.0, write_mbps)
        except Exception as exc:
            logger.debug("Disk I/O rate unavailable: %s", exc)
            return 0.0, 0.0

    def _read_battery(self) -> Tuple[Optional[float], Optional[bool]]:
        """Read battery status. Returns (percent, charging) or (None, None)."""
        try:
            bat = psutil.sensors_battery()
            if bat is None:
                return None, None
            charging = bat.power_plugged
            return round(float(bat.percent), 1), bool(charging)
        except Exception as exc:
            logger.debug("Battery unavailable: %s", exc)
            return None, None

    def _read_net_rate(self, now_ts: float) -> Tuple[float, float]:
        """Compute network sent/recv rate in KB/s since last poll."""
        try:
            current = psutil.net_io_counters()
            if current is None or self._last_io is None:
                return 0.0, 0.0
            _, _, prev_sent, prev_recv, prev_ts = self._last_io
            elapsed = now_ts - prev_ts
            if elapsed <= 0:
                return 0.0, 0.0
            sent_kbps = (current.bytes_sent - prev_sent) / elapsed / 1024.0
            recv_kbps = (current.bytes_recv - prev_recv) / elapsed / 1024.0
            return max(0.0, sent_kbps), max(0.0, recv_kbps)
        except Exception as exc:
            logger.debug("Network rate unavailable: %s", exc)
            return 0.0, 0.0

    def _read_uptime(self) -> float:
        """Return system uptime in hours."""
        try:
            boot_time = psutil.boot_time()
            uptime_s = time.time() - boot_time
            return max(0.0, uptime_s / 3600.0)
        except Exception as exc:
            logger.debug("Uptime unavailable: %s", exc)
            return 0.0

    # ─── Derived computations ─────────────────────────────────────────────────

    def _energy_reserve_label(
        self, battery_pct: Optional[float], charging: Optional[bool]
    ) -> str:
        """Map battery state to energy reserve label."""
        if battery_pct is None:
            return "full"  # desktop / no battery → assume mains power
        if charging:
            return "charging"
        if battery_pct >= 80:
            return "full"
        if battery_pct >= 50:
            return "good"
        if battery_pct >= 20:
            return "low"
        return "depleted"

    def _compute_vitality(
        self,
        cpu_pct: float,
        ram_pct: float,
        uptime_h: float,
        battery_pct: Optional[float],
        hamingja: Optional[float] = None,
    ) -> Tuple[float, float]:
        """Compute composite vitality score in [0.0, 1.0].

        Higher = more vital. Lower = more depleted/strained.
        Weights: CPU load 35%, RAM pressure 30%, uptime 20%, battery 15%.

        E-08: When ``hamingja`` is provided, a spiritual energy bonus is applied.
        hamingja=1.0 → +0.075; hamingja=0.5 → 0.0; hamingja=0.0 → -0.075.
        The boost can compensate for physical tiredness (spiritual over matter).

        Returns:
            (vitality_score, hamingja_boost_applied) — boost is 0.0 if not linked.
        """
        cpu_score = 1.0 - (cpu_pct / 100.0)
        ram_score = 1.0 - (ram_pct / 100.0)
        uptime_cap = self._uptime_weariness_cap
        uptime_score = max(0.0, 1.0 - (uptime_h / uptime_cap))

        if battery_pct is not None:
            bat_score = battery_pct / 100.0
            vitality = (
                cpu_score * 0.30
                + ram_score * 0.25
                + uptime_score * 0.20
                + bat_score * 0.25
            )
        else:
            # No battery — redistribute weight
            vitality = (
                cpu_score * 0.40
                + ram_score * 0.35
                + uptime_score * 0.25
            )

        # E-08: Honor energy bonus — spiritual strength overcoming physical weariness
        boost = 0.0
        if hamingja is not None:
            boost = (float(hamingja) - 0.5) * 0.15
            vitality = vitality + boost
            logger.debug(
                "MetabolismAdapter hamingja boost: hamingja=%.2f → boost=%.4f",
                hamingja, boost,
            )

        return round(max(0.0, min(1.0, vitality)), 4), round(boost, 4)

    @staticmethod
    def _vitality_label(score: float) -> str:
        """Convert vitality score to a somatic label."""
        if score >= 0.80:
            return "vibrant"
        if score >= 0.60:
            return "grounded"
        if score >= 0.40:
            return "weary"
        if score >= 0.20:
            return "strained"
        return "depleted"

    @staticmethod
    def _build_prompt_hint(
        mental_load: str,
        body_warmth: str,
        memory_pressure: str,
        energy_reserve: str,
        weariness: str,
        vitality_label: str,
    ) -> str:
        """Build a one-line somatic context hint for the prompt synthesizer.

        Example: "Mind focused, body comfortable, memory steady, energy good."
        """
        parts = [
            f"mind {mental_load}",
            f"body {body_warmth}",
            f"memory {memory_pressure}",
            f"energy {energy_reserve}",
        ]
        # Only include weariness if notable
        if weariness in ("tired", "exhausted"):
            parts.append(f"feeling {weariness}")
        return f"[Soma: {', '.join(parts)}] Vitality: {vitality_label}."

    def _degraded_state(self) -> MetabolismState:
        """Return a neutral fallback MetabolismState when polling fails."""
        return MetabolismState(
            cpu_percent=0.0, cpu_temp_celsius=None, temp_source="unavailable",
            ram_percent=0.0, ram_used_gb=0.0, ram_total_gb=0.0,
            disk_read_mbps=0.0, disk_write_mbps=0.0,
            battery_percent=None, battery_charging=None,
            net_sent_kbps=0.0, net_recv_kbps=0.0,
            uptime_hours=0.0,
            mental_load="clear", body_warmth="comfortable",
            memory_pressure="clear-headed", background_hum="quiet",
            energy_reserve="full", weariness="rested",
            connection_sense="still",
            vitality_score=1.0, vitality_label="vibrant",
            hamingja_boost_applied=0.0,
            prompt_hint="[Soma: degraded — hardware metrics unavailable]",
            timestamp=datetime.now(timezone.utc).isoformat(),
            degraded=True,
        )


# ─── Module-level singleton ────────────────────────────────────────────────────

_ADAPTER: Optional[MetabolismAdapter] = None


def get_metabolism() -> MetabolismAdapter:
    """Return the global MetabolismAdapter. Raises RuntimeError if not initialised."""
    if _ADAPTER is None:
        raise RuntimeError(
            "MetabolismAdapter not initialised — call init_metabolism() in main.py first"
        )
    return _ADAPTER


def init_metabolism(
    poll_interval_s: float = 5.0,
    temp_sensor_key: str = "coretemp",
    uptime_weariness_cap: float = 24.0,
) -> MetabolismAdapter:
    """Create and register the global MetabolismAdapter (call once at startup)."""
    global _ADAPTER
    _ADAPTER = MetabolismAdapter(
        poll_interval_s=poll_interval_s,
        temp_sensor_key=temp_sensor_key,
        uptime_weariness_cap=uptime_weariness_cap,
    )
    return _ADAPTER


def init_metabolism_from_config(config: Dict[str, Any]) -> MetabolismAdapter:
    """Create and register the global MetabolismAdapter from a config dict."""
    global _ADAPTER
    _ADAPTER = MetabolismAdapter.from_config(config)
    return _ADAPTER
