#!/usr/bin/env python3
"""
Xlink IoT Gateway Client - Using GatewayAppClient for API calls.

This module provides a high-level interface for Xlink IoT device operations
using the GatewayAppClient library for authenticated API calls.

Environment Variables:
    XLINK_APP_ID       Gateway App ID
    XLINK_APP_SECRET   Gateway App Secret
    XLINK_API_GROUP    Gateway group
    XLINK_BASE_URL     Gateway base URL (default: "https://api-gw.xlink.cn")
"""

import os
import sys
import json
import argparse
import logging
from datetime import datetime
from typing import Any

# Setup logging (default to INFO, can be overridden by --debug flag)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


def _to_display_str(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "是" if value else "否"
    return str(value)


def _truncate_text(text: str, max_len: int) -> str:
    if max_len <= 0:
        return ""
    if len(text) <= max_len:
        return text
    if max_len == 1:
        return "…"
    return text[: max_len - 1] + "…"


def _print_table(
    headers: list[str],
    rows: list[list[Any]],
    indent: str = "   ",
    max_col_width: int = 48,
) -> None:
    if not headers:
        return

    normalized_rows: list[list[str]] = []
    for row in rows:
        normalized_rows.append([_to_display_str(v) for v in row])

    col_count = len(headers)
    widths = [len(h) for h in headers]
    for row in normalized_rows:
        for i in range(col_count):
            cell = row[i] if i < len(row) else ""
            widths[i] = min(max(widths[i], len(cell)), max_col_width)

    header_line = " | ".join(
        _truncate_text(headers[i], widths[i]).ljust(widths[i]) for i in range(col_count)
    )
    separator_line = "-+-".join("-" * widths[i] for i in range(col_count))
    print(indent + header_line)
    print(indent + separator_line)

    for row in normalized_rows:
        padded = []
        for i in range(col_count):
            cell = row[i] if i < len(row) else ""
            padded.append(_truncate_text(cell, widths[i]).ljust(widths[i]))
        print(indent + " | ".join(padded))


DEFAULT_DEVICE_LIST_FILTER: dict[str, list[str]] = {
    "device": [
        "id",
        "mac",
        "name",
        "is_active",
        "active_date",
        "mcu_mod",
        "mcu_version",
        "firmware_mod",
        "firmware_version",
        "product_id",
        "sn",
        "create_time",
        "groups",
        "last_reset",
        "gateway_id",
        "project_id",
        "tags_map",
        "space_id",
        "space_type",
    ],
    "vdevice": [
        "last_login",
        "last_logout",
        "connect_protocol",
        "connector_id",
    ],
    "online": ["is_online"],
    "geography": [
        "country",
        "city",
        "province",
        "district",
        "address",
    ],
    "product": ["name", "pics"],
}

# Import the GatewayAppClient library
try:
    from gateway_app_client import (
        GatewayAppClient,
        GatewayAppClientError,
        StageType,
        HttpResponse,
    )
except ImportError:
    print("错误：未找到 gateway_app_client.py。", file=sys.stderr)
    sys.exit(1)


def clean_env_value(value: str | None) -> str | None:
    """Clean environment variable value by removing surrounding quotes."""
    if value is None:
        return None
    value = value.strip()
    if (
        value.startswith(("'", '"', "`"))
        and value.endswith(("'", '"', "`"))
        and len(value) >= 2
    ):
        value = value[1:-1].strip()
    return value


class XlinkIoTClient:
    """High-level client for Xlink IoT device operations."""

    DEFAULT_HOST = "https://api-gw.xlink.cn"
    DEFAULT_STAGE = StageType.RELEASE

    def __init__(
        self,
        app_id: str | None = None,
        app_secret: str | None = None,
        group: str | None = None,
        host: str | None = None,
        stage: StageType = DEFAULT_STAGE,
    ):
        self.app_id = app_id or clean_env_value(os.environ.get("XLINK_APP_ID"))
        self.app_secret = app_secret or clean_env_value(
            os.environ.get("XLINK_APP_SECRET")
        )
        self.group = group or clean_env_value(os.environ.get("XLINK_API_GROUP"))
        self.host = (
            host
            or clean_env_value(os.environ.get("XLINK_BASE_URL"))
            or self.DEFAULT_HOST
        )
        self.stage = stage

        logger.info("Initializing XlinkIoTClient")
        logger.debug(
            f"Configuration - App ID: {self.app_id[:8]}... (masked), Group: {self.group}, Host: {self.host}"
        )

        if not self.app_id or not self.app_secret:
            logger.error("Missing XLINK_APP_ID or XLINK_APP_SECRET")
            raise ValueError("XLINK_APP_ID and XLINK_APP_SECRET must be set")
        if not self.group:
            logger.error("Missing XLINK_API_GROUP")
            raise ValueError("XLINK_API_GROUP must be set")

        self.client = GatewayAppClient(self.app_id, self.app_secret)
        logger.info("XlinkIoTClient initialized successfully")

    def _make_request(
        self,
        method: str,
        url: str,
        params: dict[str, str] | None = None,
        data: Any | None = None,
    ) -> str:
        """Send HTTP request via gateway client and return raw response body."""
        method = method.upper()
        logger.info(f"Making {method} request to {url}")
        logger.debug(
            f"Request details - URL: {self.host}{url}, Params: {params}, Data: {data}"
        )

        dispatch = {
            "GET": lambda: self.client.get(
                group=self.group,
                stage=self.stage,
                url=url,
                host=self.host,
                param_map=params,
            ),
            "POST": lambda: self.client.post(
                group=self.group,
                stage=self.stage,
                url=url,
                host=self.host,
                data=data,
                param_map=params,
            ),
            "PUT": lambda: self.client.put(
                group=self.group,
                stage=self.stage,
                url=url,
                host=self.host,
                data=data,
                param_map=params,
            ),
            "DELETE": lambda: self.client.delete(
                group=self.group,
                stage=self.stage,
                url=url,
                host=self.host,
                param_map=params,
            ),
        }
        handler = dispatch.get(method)
        if handler is None:
            raise ValueError(f"Unsupported HTTP method: {method}")

        response = handler()
        logger.debug(f"HTTP response code: {response.code}")
        return response.content

    def _parse_response(self, raw: str) -> Any:
        """Parse raw JSON response and return the data section."""
        try:
            result = json.loads(raw)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse response as JSON: {e}")
            raise GatewayAppClientError(f"Invalid JSON response: {e}") from e

        logger.debug(f"Parsed JSON response: {json.dumps(result, indent=2)[:500]}...")
        return self._extract_data(result)

    def _extract_data(self, result: Any) -> Any:
        """Extract data from API response, raising on business errors."""
        if not isinstance(result, dict):
            return result

        response_code = (
            result.get("code")
            if result.get("code") is not None
            else result.get("status")
        )
        if response_code is None:
            return result.get("data", {}) if "data" in result else result

        if response_code == 0 or response_code == 200:
            logger.info("Request successful, returning data section")
            return result.get("data", {})

        error_msg = (
            result.get("message")
            or result.get("msg")
            or (result.get("error", {}) or {}).get("msg")
            or "Unknown error"
        )
        logger.error(
            f"API returned error - Code: {response_code}, Message: {error_msg}"
        )
        raise GatewayAppClientError(f"API error: {error_msg}")

    def _request(
        self,
        method: str,
        url: str,
        params: dict[str, str] | None = None,
        data: Any | None = None,
    ) -> Any:
        """Make API request and return parsed data.

        Pipeline: _make_request -> _parse_response -> _extract_data
        """
        try:
            raw = self._make_request(method, url, params, data)
            return self._parse_response(raw)
        except GatewayAppClientError:
            raise
        except Exception as e:
            logger.error(f"Unexpected error during API call: {type(e).__name__}: {e}")
            raise

    def get_device_overview(
        self,
        product_id: str | None = None,
        project_id: str | None = None,
    ) -> dict[str, Any]:
        """
        Get device overview statistics.

        Args:
            product_id: Filter by product ID (optional)
            project_id: Filter by project ID (optional)

        Returns:
            Device overview with total, online, activated, online_rate, activated_rate
        """
        data: dict[str, Any] = {}
        if product_id:
            data["product_id"] = product_id
        if project_id:
            data["project_id"] = project_id

        return self._request(
            "POST", "/v3/device-service/devices/overview", data=data if data else None
        )

    def get_device_list(
        self,
        filter_config: dict[str, Any] | None = None,
        offset: int = 0,
        limit: int = 20,
        device_type: str = "all",
        query_config: dict[str, Any] | None = None,
        order_config: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """
        Get device list with pagination and advanced filtering.

        Args:
            filter_config: Filter configuration for returned fields. If omitted, uses a default
                filter based on the API documentation.
            offset: Pagination offset (default: 0)
            limit: Page size (default: 20)
            device_type: Device type filter (default: "all")
            query_config: Query conditions for filtering devices (optional)
            order_config: Order configuration for sorting (optional)

        Returns:
            Device list with count and list fields
        """
        filter_config = filter_config or DEFAULT_DEVICE_LIST_FILTER
        data: dict[str, Any] = {
            "offset": offset,
            "limit": limit,
            "filter": filter_config,
        }

        if query_config:
            data["query"] = query_config
        if order_config:
            data["order"] = order_config

        return self._request(
            "POST",
            "/v2/devices/def-filter/aggregates",
            params={"type": device_type},
            data=data,
        )

    def get_device_statistics_trend(
        self,
        start_time: str,
        end_time: str,
        granularity: str = "day",
    ) -> dict[str, Any]:
        """
        Get device statistics trend by time granularity.

        Args:
            start_time: Start time in ISO 8601 format (e.g., "2026-03-19T09:40")
            end_time: End time in ISO 8601 format (e.g., "2026-03-20T09:40")
            granularity: Time granularity - "hour", "day", "week", "month" (default: "day")

        Returns:
            Device statistics trend data

        Example:
            client.get_device_statistics_trend(
                start_time="2026-03-19T09:40",
                end_time="2026-03-20T09:40",
                granularity="hour"
            )
        """
        data: dict[str, Any] = {
            "start": start_time,
            "end": end_time,
            "interval": granularity,
        }
        return self._request("POST", "/v3/device-service/devices/statistics", data=data)

    def get_device_attribute_history(
        self,
        device_ids: list[int],
        offset: int = 0,
        limit: int = 20,
        start_time: int | None = None,
        end_time: int | None = None,
        rule_id: str | None = None,
        sort_by_date: str = "desc",
    ) -> dict[str, Any]:
        """
        Get historical attribute snapshot data for multiple devices.

        Args:
            device_ids: List of device IDs (must belong to the same product)
            offset: Pagination offset
            limit: Page size (default: 20)
            start_time: Start timestamp. If provided, end_time is required.
            end_time: End timestamp. If provided, start_time is required.
            rule_id: Snapshot rule ID
            sort_by_date: Sort order - "desc" (default) or "asc"

        Returns:
            Device attribute history with count, tml (template), and list fields
        """
        if not device_ids:
            raise ValueError("device_ids is required")
        data: dict[str, Any] = {
            "device_ids": device_ids,
            "offset": offset,
            "limit": limit,
        }

        if start_time is not None or end_time is not None:
            if start_time is None or end_time is None:
                raise ValueError("start_time and end_time must be provided together")
            data["date"] = {
                "begin": start_time,
                "end": end_time,
            }

        if rule_id:
            data["rule_id"] = rule_id

        if sort_by_date:
            data["sort_by_date"] = sort_by_date

        return self._request("POST", "/v2/snapshot/device-attribute", data=data)

    def get_device_latest_attributes(
        self,
        device_ids: list[int] | None = None,
        product_ids: list[str] | None = None,
        offset: int = 0,
        limit: int = 10,
        load_exception: bool = False,
    ) -> dict[str, Any]:
        """
        Get latest attribute information for multiple devices.

        Args:
            device_ids: List of device IDs to query (optional)
            product_ids: List of product IDs to query (optional)
            offset: Pagination offset (default: 0)
            limit: Page size, max 10000 (default: 10)
            load_exception: Load exception info (default: False)

        Returns:
            Device latest attributes with count, tmls, and list fields
        """
        data: dict[str, Any] = {
            "offset": offset,
            "limit": min(limit, 10000),
        }

        # Build query condition
        query: dict[str, Any] = {}
        if device_ids:
            query["device_id"] = {"$in": device_ids}
        if product_ids:
            query["product_id"] = {"$in": product_ids}

        if query:
            data["query"] = query

        return self._request(
            "POST",
            "/v2/device-shadow/device-attribute-query",
            params={"load_exception": str(load_exception).lower()},
            data=data,
        )

    def control_device(
        self,
        thing_id: str,
        service: str,
        input_params: dict[str, Any],
        ttl: int = -1,
    ) -> dict[str, Any]:
        """
        Invoke device service (control device by thing_id).

        Args:
            thing_id: Device ID to control
            service: Service name from product thing model
                     Use "device_attribute_set_service" for setting attributes
            input_params: Input parameters as key-value pairs
            ttl: Command cache duration in seconds (1-864000),
                 <=0 or omit for no cache

        Returns:
            Control result with thing_id, code, msg, output, and command_id

        Example:
            # Set device attributes
            client.control_device(
                thing_id="10299402",
                service="device_attribute_set_service",
                input_params={"ColorTemperature": 8}
            )

            # With command cache (10 minutes)
            client.control_device(
                thing_id="10299402",
                service="device_attribute_set_service",
                input_params={"Power": 1},
                ttl=600
            )
        """
        data: dict[str, Any] = {
            "thing_id": thing_id,
            "service": service,
            "input": input_params,
        }

        if ttl and ttl > 0:
            data["ttl"] = ttl

        return self._request("POST", "/v2/device-shadow/service_invoke", data=data)

    def get_device_alert_statistics(
        self,
        product_id: str | None = None,
        project_id: str | None = None,
        interval: str = "hour",
        start_time: str | None = None,
        end_time: str | None = None,
    ) -> dict[str, Any]:
        """
        Get device alert statistics (recent 24 hours or custom time range).

        Args:
            product_id: Filter by product ID (optional)
            project_id: Filter by project ID (optional)
            interval: Time granularity - "hour" or "day" (default: "hour")
            start_time: Start time in ISO 8601 format (optional)
            end_time: End time in ISO 8601 format (optional)

        Returns:
            Alert statistics with list of time-series data

        Example:
            # Recent 24 hours (default)
            client.get_device_alert_statistics()

            # Custom time range
            client.get_device_alert_statistics(
                project_id="ab582",
                start_time="2026-02-10T00:00:00.000Z",
                end_time="2026-02-10T23:59:59.999Z",
                interval="hour"
            )
        """
        data: dict[str, Any] = {}

        if product_id:
            data["product_id"] = product_id
        if project_id:
            data["project_id"] = project_id
        if interval:
            data["interval"] = interval
        if start_time:
            data["start"] = start_time
        if end_time:
            data["end"] = end_time

        return self._request(
            "POST", "/v3/alert/statistics", data=data if data else None
        )

    def get_event_instances(
        self,
        status: list[int] | None = None,
        start_time: str | None = None,
        end_time: str | None = None,
        device_id: int | None = None,
        event_ids: list[str] | None = None,
        project_ids: list[str] | None = None,
        applications: list[str] | None = None,
        classification_ids: list[str] | None = None,
        tag_ids: list[str] | None = None,
        rank_ids: list[str] | None = None,
        device_name: str | None = None,
        trigger_condition: str | None = None,
        name: str | None = None,
        processed_ways: list[int] | None = None,
        processed_operator_name: str | None = None,
        offset: int = 0,
        limit: int = 10,
    ) -> dict[str, Any]:
        """
        Get all event instances with optional filters.

        Args:
            status: Event status list [1:pending, 2:processing, 3:processed]
            start_time: Greater than create time (ISO 8601: "2019-11-13T14:54:00.00Z")
            end_time: Less than create time (ISO 8601: "2019-11-13T14:54:00.00Z")
            device_id: Device ID (integer)
            event_ids: Event ID list
            project_ids: Project ID list
            applications: Application type list
            classification_ids: Classification ID list
            tag_ids: Tag ID list
            rank_ids: Rank/Level ID list
            device_name: Device name (LIKE query)
            trigger_condition: Trigger condition (LIKE query)
            name: Event name (LIKE query)
            processed_ways: Processed way list [-1:unprocessed, 1:debug, 2:fault, 3:false, 4:other, 5:workorder, 6:suppress, 7:auto-recover]
            processed_operator_name: Operator name (LIKE query)
            offset: Pagination offset
            limit: Page size

        Returns:
            Event instances with count and list fields
        """
        data: dict[str, Any] = {
            "offset": offset,
            "limit": limit,
        }

        if status:
            data["status"] = status
        if start_time:
            data["gt_create_time"] = start_time
        if end_time:
            data["lt_create_time"] = end_time
        if device_id:
            data["device_id"] = device_id
        if event_ids:
            data["event_ids"] = event_ids
        if project_ids:
            data["project_ids"] = project_ids
        if applications:
            data["applications"] = applications
        if classification_ids:
            data["classification_ids"] = classification_ids
        if tag_ids:
            data["tag_ids"] = tag_ids
        if rank_ids:
            data["rank_ids"] = rank_ids
        if device_name:
            data["device_name"] = device_name
        if trigger_condition:
            data["trigger_condition"] = trigger_condition
        if name:
            data["name"] = name
        if processed_ways:
            data["processed_ways"] = processed_ways
        if processed_operator_name:
            data["processed_operator_name"] = processed_operator_name

        return self._request("POST", "/v2/service/events/all-instances", data=data)

    def get_alert_overview(
        self,
        product_id: str | None = None,
        project_id: str | None = None,
    ) -> dict[str, Any]:
        """
        Get alert overview statistics.

        Args:
            product_id: Filter by product ID (optional)
            project_id: Filter by project ID (optional)

        Returns:
            Alert overview with added_alert_num, history_alert_num, device_alert_num, device_alert_rate

        Example:
            # Overall alert overview
            client.get_alert_overview()

            # Filter by project
            client.get_alert_overview(project_id="ab582")
        """
        data: dict[str, Any] = {}
        if product_id:
            data["product_id"] = product_id
        if project_id:
            data["project_id"] = project_id

        return self._request("POST", "/v3/alert/overview", data=data if data else None)


def _setup_subparsers(subparsers):
    """Setup subparsers for CLI commands."""
    # overview command
    overview_parser = subparsers.add_parser(
        "overview", help="Get device overview statistics"
    )
    overview_parser.add_argument(
        "--product-id",
        type=str,
        dest="product_id",
        metavar="ID",
        help="Filter by product ID",
    )
    overview_parser.add_argument(
        "--project-id",
        type=str,
        dest="project_id",
        metavar="ID",
        help="Filter by project ID",
    )
    overview_parser.add_argument("--json", action="store_true", help="Output as JSON")
    overview_parser.set_defaults(func=cmd_overview)

    # device-list command
    device_list_parser = subparsers.add_parser("device-list", help="Get device list")
    device_list_parser.add_argument(
        "--offset", type=int, default=0, metavar="N", help="Pagination offset"
    )
    device_list_parser.add_argument(
        "--limit",
        type=int,
        default=20,
        choices=range(1, 101),
        metavar="N",
        help="Page size (1-100)",
    )
    device_list_parser.add_argument(
        "--filter", type=str, help="Filter config as JSON string"
    )
    device_list_parser.add_argument(
        "--query", type=str, help="Query config as JSON string"
    )
    device_list_parser.add_argument(
        "--order", type=str, help="Order config as JSON string"
    )
    device_list_parser.add_argument(
        "--json", action="store_true", help="Output as JSON"
    )
    device_list_parser.set_defaults(func=cmd_device_list)

    # device-trend command
    device_trend_parser = subparsers.add_parser(
        "device-trend", help="Get device statistics trend"
    )
    device_trend_parser.add_argument(
        "--start-time",
        type=str,
        dest="start_time",
        metavar="ISO",
        help="Start time (ISO 8601: 2026-03-19T09:40)",
    )
    device_trend_parser.add_argument(
        "--end-time",
        type=str,
        dest="end_time",
        metavar="ISO",
        help="End time (ISO 8601)",
    )
    device_trend_parser.add_argument(
        "--granularity",
        type=str,
        default="day",
        choices=["hour", "day", "week", "month"],
        help="Time granularity (default: day)",
    )
    device_trend_parser.add_argument(
        "--json", action="store_true", help="Output as JSON"
    )
    device_trend_parser.set_defaults(func=cmd_device_trend)

    # device-history command
    device_history_parser = subparsers.add_parser(
        "device-history", help="Get device attribute history"
    )
    device_history_parser.add_argument(
        "--device-ids",
        type=str,
        required=True,
        metavar="IDS",
        help="Comma-separated device IDs",
    )
    device_history_parser.add_argument(
        "--offset", type=int, default=0, metavar="N", help="Pagination offset"
    )
    device_history_parser.add_argument(
        "--limit",
        type=int,
        default=20,
        choices=range(1, 101),
        metavar="N",
        help="Page size (1-100)",
    )
    device_history_parser.add_argument(
        "--start-time",
        type=int,
        dest="start_time",
        metavar="TS",
        help="Start timestamp (requires --end-time)",
    )
    device_history_parser.add_argument(
        "--end-time",
        type=int,
        dest="end_time",
        metavar="TS",
        help="End timestamp (requires --start-time)",
    )
    device_history_parser.add_argument(
        "--rule-id", type=str, dest="rule_id", metavar="ID", help="Snapshot rule ID"
    )
    device_history_parser.add_argument(
        "--sort-by-date",
        type=str,
        default="desc",
        choices=["asc", "desc"],
        dest="sort_by_date",
        help="Sort order (default: desc)",
    )
    device_history_parser.add_argument(
        "--json", action="store_true", help="Output as JSON"
    )
    device_history_parser.set_defaults(func=cmd_device_history)

    # device-latest command
    device_latest_parser = subparsers.add_parser(
        "device-latest", help="Get latest device attributes"
    )
    device_latest_parser.add_argument(
        "--device-ids", type=str, metavar="IDS", help="Comma-separated device IDs"
    )
    device_latest_parser.add_argument(
        "--product-ids", type=str, metavar="IDS", help="Comma-separated product IDs"
    )
    device_latest_parser.add_argument(
        "--offset", type=int, default=0, metavar="N", help="Pagination offset"
    )
    device_latest_parser.add_argument(
        "--limit", type=int, default=10, metavar="N", help="Page size (1-10000)"
    )
    device_latest_parser.add_argument(
        "--load-exception",
        action="store_true",
        dest="load_exception",
        help="Load exception info",
    )
    device_latest_parser.add_argument(
        "--json", action="store_true", help="Output as JSON"
    )
    device_latest_parser.set_defaults(func=cmd_device_latest)

    # device-control command
    device_control_parser = subparsers.add_parser(
        "device-control", help="Control device by invoking service"
    )
    device_control_parser.add_argument(
        "--thing-id",
        type=str,
        required=True,
        dest="thing_id",
        metavar="ID",
        help="Device ID to control",
    )
    device_control_parser.add_argument(
        "--service",
        type=str,
        required=True,
        help="Service name (use 'device_attribute_set_service' for setting attributes)",
    )
    device_control_parser.add_argument(
        "--input", type=str, required=True, help="Input parameters as JSON string"
    )
    device_control_parser.add_argument(
        "--ttl",
        type=int,
        default=-1,
        metavar="SEC",
        help="Command cache duration in seconds (1-864000)",
    )
    device_control_parser.add_argument(
        "--json", action="store_true", help="Output as JSON"
    )
    device_control_parser.set_defaults(func=cmd_device_control)

    # alert-statistics command
    alert_stats_parser = subparsers.add_parser(
        "alert-statistics", help="Get device alert statistics"
    )
    alert_stats_parser.add_argument(
        "--product-id",
        type=str,
        dest="product_id",
        metavar="ID",
        help="Filter by product ID",
    )
    alert_stats_parser.add_argument(
        "--project-id",
        type=str,
        dest="project_id",
        metavar="ID",
        help="Filter by project ID",
    )
    alert_stats_parser.add_argument(
        "--interval",
        type=str,
        default="hour",
        choices=["hour", "day"],
        help="Time granularity (default: hour)",
    )
    alert_stats_parser.add_argument(
        "--start-time",
        "--start",
        type=str,
        dest="start_time",
        metavar="ISO",
        help="Start time (ISO 8601: 2026-02-10T00:00:00.000Z)",
    )
    alert_stats_parser.add_argument(
        "--end-time",
        "--end",
        type=str,
        dest="end_time",
        metavar="ISO",
        help="End time (ISO 8601)",
    )
    alert_stats_parser.add_argument(
        "--json", action="store_true", help="Output as JSON"
    )
    alert_stats_parser.set_defaults(func=cmd_alert_statistics)

    # alert-overview command
    alert_overview_parser = subparsers.add_parser(
        "alert-overview", help="Get alert overview statistics"
    )
    alert_overview_parser.add_argument(
        "--product-id",
        type=str,
        dest="product_id",
        metavar="ID",
        help="Filter by product ID",
    )
    alert_overview_parser.add_argument(
        "--project-id",
        type=str,
        dest="project_id",
        metavar="ID",
        help="Filter by project ID",
    )
    alert_overview_parser.add_argument(
        "--json", action="store_true", help="Output as JSON"
    )
    alert_overview_parser.set_defaults(func=cmd_alert_overview)

    # event-instances command
    event_parser = subparsers.add_parser(
        "event-instances", help="Query event instance list"
    )
    event_parser.add_argument(
        "--status",
        type=str,
        metavar="N",
        help="Event status (comma-separated: 1/2/3 or pending/processing/processed)",
    )
    event_parser.add_argument(
        "--start-time",
        type=str,
        dest="start_time",
        metavar="ISO",
        help="Greater than create time (ISO 8601: 2019-11-13T14:54:00.00Z)",
    )
    event_parser.add_argument(
        "--end-time",
        type=str,
        dest="end_time",
        metavar="ISO",
        help="Less than create time (ISO 8601)",
    )
    event_parser.add_argument(
        "--device-id",
        type=int,
        dest="device_id",
        metavar="ID",
        help="Device ID (integer)",
    )
    event_parser.add_argument(
        "--event-ids",
        type=str,
        dest="event_ids",
        metavar="IDS",
        help="Event IDs (comma-separated)",
    )
    event_parser.add_argument(
        "--project-ids",
        type=str,
        dest="project_ids",
        metavar="IDS",
        help="Project IDs (comma-separated)",
    )
    event_parser.add_argument(
        "--device-name",
        type=str,
        dest="device_name",
        metavar="NAME",
        help="Device name (LIKE query)",
    )
    event_parser.add_argument(
        "--name", type=str, metavar="NAME", help="Event name (LIKE query)"
    )
    event_parser.add_argument(
        "--processed-ways",
        type=str,
        dest="processed_ways",
        metavar="N",
        help="Processed ways (comma-separated: -1=unprocessed, 1=debug, 2=fault, 3=false, 4=other, 5=workorder, 6=suppress, 7=auto)",
    )
    event_parser.add_argument(
        "--offset", type=int, default=0, metavar="N", help="Pagination offset"
    )
    event_parser.add_argument(
        "--limit",
        type=int,
        default=10,
        choices=range(1, 101),
        metavar="N",
        help="Page size (1-100)",
    )
    event_parser.add_argument("--json", action="store_true", help="Output as JSON")
    event_parser.set_defaults(func=cmd_event_instances)


def cmd_overview(client: XlinkIoTClient, args: argparse.Namespace) -> None:
    """Execute device overview command."""
    logger.info("Executing overview command")
    logger.debug(
        f"Parameters - product_id: {args.product_id}, project_id: {args.project_id}"
    )

    result = client.get_device_overview(
        product_id=args.product_id,
        project_id=args.project_id,
    )

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        # API returns: total, online, activated, online_rate, activated_rate
        total = result.get("total", 0)
        online = result.get("online", 0)
        activated = result.get("activated", 0)
        online_rate = result.get("online_rate", 0)
        activated_rate = result.get("activated_rate", 0)

        print("\n" + "=" * 50)
        print("📊 XLINK 设备概览")
        print("=" * 50)
        print(f"\n   📱 设备总数:      {total}")
        print(f"   🟢 在线:          {online} ({online_rate * 100:.1f}%)")
        print(f"   ✅ 已激活:        {activated} ({activated_rate * 100:.1f}%)")
        print(f"   ⚫ 离线:          {total - online}")
        print(f"   ⏸️  未激活:        {total - activated}")
        print()


def cmd_device_trend(client: XlinkIoTClient, args: argparse.Namespace) -> None:
    """Execute device trend command."""
    logger.info("Executing device-trend command")
    logger.debug(
        f"Parameters - start_time: {args.start_time}, end_time: {args.end_time}, granularity: {args.granularity}"
    )

    result = client.get_device_statistics_trend(
        start_time=args.start_time,
        end_time=args.end_time,
        granularity=args.granularity,
    )

    logger.info("Device trend query completed")

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print("\n" + "=" * 50)
        print("📈 XLINK 设备统计趋势")
        print("=" * 50)

        # Handle both dict (overview) and list (trend) data formats
        if isinstance(result, dict):
            # Overview data format
            total = result.get("total", 0)
            online = result.get("online", 0)
            activated = result.get("activated", 0)
            online_rate = result.get("online_rate", 0)
            activated_rate = result.get("activated_rate", 0)

            print(f"\n   📱 设备总数:      {total}")
            print(f"   🟢 在线:          {online} ({online_rate * 100:.1f}%)")
            print(f"   ✅ 已激活:        {activated} ({activated_rate * 100:.1f}%)")
            print(f"   ⚫ 离线:          {total - online}")
            print(f"   ⏸️  未激活:        {total - activated}")
            print()
        elif isinstance(result, list):
            # Trend list format
            print(f"\n   粒度: {args.granularity}")
            print(f"   数据点: {len(result)}")
            print()

            if not result:
                print("   暂无数据。")
                print()
                return

            rows: list[list[Any]] = []
            for point in result:
                time_str = point.get("time", point.get("timestamp", "N/A"))
                total = point.get("total", 0)
                online = point.get("online", 0)
                offline = point.get("offline", 0)
                fault = point.get("fault", 0)
                rows.append([time_str, total, online, offline, fault])

            _print_table(["时间", "总数", "在线", "离线", "故障"], rows)
        else:
            print(f"\n   未知数据格式: {type(result)}")
            print(f"   数据: {result}")
            print()


def cmd_device_history(client: XlinkIoTClient, args: argparse.Namespace) -> None:
    """Execute device history command."""
    logger.info("Executing device-history command")

    # Parse device IDs from comma-separated string
    device_ids = [int(id.strip()) for id in args.device_ids.split(",")]

    logger.debug(
        f"Parameters - device_ids: {device_ids}, offset: {args.offset}, limit: {args.limit}"
    )
    logger.debug(
        f"Time range: {args.start_time} - {args.end_time}, sort: {args.sort_by_date}"
    )

    result = client.get_device_attribute_history(
        device_ids=device_ids,
        offset=args.offset,
        limit=args.limit,
        start_time=args.start_time,
        end_time=args.end_time,
        rule_id=args.rule_id,
        sort_by_date=args.sort_by_date,
    )

    logger.info(f"Device history query completed. Total: {result.get('count', 0)}")

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        count = result.get("count", 0)
        snapshots = result.get("list", [])
        tml = result.get("tml", [])

        print("\n" + "=" * 50)
        print("📜 XLINK 设备属性历史")
        print("=" * 50)
        print(f"\n   总记录数: {count}")
        print(f"   展示: {len(snapshots)} 条快照")
        print()

        if not snapshots:
            print("   未找到历史数据。")
            print()
            return

        # Show template info if available
        if tml:
            tml_rows: list[list[Any]] = []
            for idx, attr in enumerate(tml):
                field_name = attr.get("field_name", {})
                cn_name = field_name.get("cn", "N/A")
                en_name = field_name.get("en", "N/A")
                attr_type = attr.get("type", {}).get("type", "N/A")
                symbol = attr.get("symbol", "")
                tml_rows.append([idx, cn_name, en_name, attr_type, symbol])
            print("   属性模板：")
            _print_table(["序号", "中文名", "英文名", "类型", "单位"], tml_rows)
            print()

        snap_rows: list[list[Any]] = []
        for snap in snapshots:
            device_id = snap.get("device_id", "N/A")
            snapshot_date = snap.get("snapshot_date", "N/A")
            rule_id = snap.get("rule_id", "N/A")

            attrs = {k: v for k, v in snap.items() if k.isdigit()}
            values_text = ""
            if attrs and tml:
                parts: list[str] = []
                for idx, value in sorted(attrs.items(), key=lambda x: int(x[0])):
                    if int(idx) < len(tml):
                        attr_name = (
                            tml[int(idx)].get("field_name", {}).get("cn", f"属性 {idx}")
                        )
                        parts.append(f"{attr_name}={value}")
                values_text = ", ".join(parts)

            snap_rows.append([snapshot_date, device_id, rule_id, values_text])

        _print_table(["日期", "设备ID", "规则ID", "值"], snap_rows)
        print()


def cmd_device_latest(client: XlinkIoTClient, args: argparse.Namespace) -> None:
    """Execute device latest attributes command."""
    logger.info("Executing device-latest command")

    # Parse IDs from comma-separated strings
    device_ids = (
        [int(id.strip()) for id in args.device_ids.split(",")]
        if args.device_ids
        else None
    )
    product_ids = (
        [id.strip() for id in args.product_ids.split(",")] if args.product_ids else None
    )

    if not device_ids and not product_ids:
        print("❌ 错误：必须提供 --device-ids 或 --product-ids", file=sys.stderr)
        sys.exit(1)

    logger.debug(f"Parameters - device_ids: {device_ids}, product_ids: {product_ids}")
    logger.debug(
        f"Pagination - offset: {args.offset}, limit: {args.limit}, load_exception: {args.load_exception}"
    )

    result = client.get_device_latest_attributes(
        device_ids=device_ids,
        product_ids=product_ids,
        offset=args.offset,
        limit=args.limit,
        load_exception=args.load_exception,
    )

    logger.info(
        f"Device latest attributes query completed. Total: {result.get('count', 0)}"
    )

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        count = result.get("count", 0)
        devices = result.get("list", [])
        tmls = result.get("tmls", {})

        print("\n" + "=" * 50)
        print("📊 XLINK 设备最新属性")
        print("=" * 50)
        print(f"\n   设备总数: {count}")
        print(f"   展示: {len(devices)} 台设备")
        print()

        if not devices:
            print("   未找到设备。")
            print()
            return

        device_rows: list[list[Any]] = []
        for dev in devices:
            device_id = dev.get("device_id", "N/A")
            product_id = dev.get("product_id", "N/A")
            is_online = dev.get("is_online", False)
            last_update = dev.get("last_update", "N/A")
            last_login = dev.get("last_login", "N/A")
            online_count = dev.get("online_count", 0)
            attr_count = len(dev.get("attributes", []) or [])
            device_rows.append(
                [
                    device_id,
                    product_id,
                    "在线" if is_online else "离线",
                    last_update,
                    last_login,
                    online_count,
                    attr_count,
                ]
            )

        _print_table(
            [
                "设备ID",
                "产品",
                "在线",
                "最后更新",
                "最近登录",
                "在线时长(ms)",
                "属性数",
            ],
            device_rows,
        )

        for dev in devices:
            attributes = dev.get("attributes", [])
            if not attributes:
                continue

            device_id = dev.get("device_id", "N/A")
            product_id = dev.get("product_id", "N/A")
            product_tml = tmls.get(product_id, [])

            attr_rows: list[list[Any]] = []
            for attr in attributes:
                idx = attr.get("index", 0)
                field = attr.get("field", f"attr_{idx}")
                value = attr.get("value", "N/A")
                time_ms = attr.get("time")

                attr_name = field
                if product_tml and idx < len(product_tml):
                    attr_name = product_tml[idx].get("field_name", {}).get("cn", field)

                time_str = ""
            if time_ms:
                try:
                    dt = datetime.fromtimestamp(time_ms / 1000.0)
                    time_str = dt.strftime("%Y-%m-%d %H:%M:%S")
                except (ValueError, TypeError):
                    pass

                attr_rows.append([attr_name, value, time_str])

            print()
            print(f"   设备 {device_id} 属性：")
            _print_table(["名称", "值", "时间"], attr_rows)
        print()


def cmd_device_control(client: XlinkIoTClient, args: argparse.Namespace) -> None:
    """Execute device control command."""
    logger.info("Executing device-control command")

    # Parse input parameters from JSON string
    try:
        input_params = json.loads(args.input)
    except json.JSONDecodeError as e:
        print(f"❌ 错误：--input 不是合法 JSON：{e}", file=sys.stderr)
        sys.exit(1)

    logger.debug(
        f"Parameters - thing_id: {args.thing_id}, service: {args.service}, input: {input_params}, ttl: {args.ttl}"
    )

    result = client.control_device(
        thing_id=args.thing_id,
        service=args.service,
        input_params=input_params,
        ttl=args.ttl,
    )

    logger.info(f"Device control completed. Code: {result.get('code', 'N/A')}")

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        thing_id = result.get("thing_id", "N/A")
        code = result.get("code", "N/A")
        msg = result.get("msg", "N/A")
        command_id = result.get("command_id")
        output = result.get("output", {})

        print("\n" + "=" * 50)
        print("🎮 XLINK 设备控制")
        print("=" * 50)
        print(f"\n   设备ID: {thing_id}")
        print(f"   服务: {args.service}")
        print()

        # Check response code
        if code == "200":
            print("   ✅ 状态: 成功")
        elif code == "202":
            print("   ⏸️  状态: 设备离线（未下发）")
        elif code == "408":
            print("   ⚠️  状态: 连接已关闭（设备休眠）")
        elif code == "503":
            print("   ❌ 状态: 控制失败")
        else:
            print(f"   状态码: {code}")

        print(f"   消息: {msg}")

        if command_id:
            print(f"   命令ID: {command_id}")
            print("   ℹ️  可使用 command_id 查询命令状态（缓存命令）")

        if output:
            print("\n   输出：")
            for key, value in output.items():
                print(f"      {key}: {value}")

        print()


def cmd_alert_statistics(client: XlinkIoTClient, args: argparse.Namespace) -> None:
    """Execute alert statistics command."""
    logger.info("Executing alert-statistics command")
    logger.debug(
        f"Parameters - product_id: {args.product_id}, project_id: {args.project_id}, interval: {args.interval}"
    )
    logger.debug(f"Time range: {args.start_time} - {args.end_time}")

    result = client.get_device_alert_statistics(
        product_id=args.product_id,
        project_id=args.project_id,
        interval=args.interval,
        start_time=args.start_time,
        end_time=args.end_time,
    )

    logger.info(
        f"Alert statistics query completed. Data points: {len(result.get('list', []))}"
    )

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        data_list = result.get("list", [])

        print("\n" + "=" * 50)
        print("📊 XLINK 设备告警统计")
        print("=" * 50)
        print(f"\n   统计粒度: {args.interval}")
        print(f"   数据点: {len(data_list)}")
        print()

        if not data_list:
            print("   暂无数据。")
            print()
            return

        rows: list[list[Any]] = []
        for point in data_list:
            time_str = point.get("time", "N/A")
            added = point.get("added_alert_num", 0)
            history = point.get("history_alert_num", 0)
            device_alerts = point.get("device_alert_num", 0)
            rate = point.get("device_alert_rate", 0)
            rows.append([time_str, added, history, device_alerts, f"{rate * 100:.2f}%"])
        _print_table(["时间", "新增告警", "历史告警", "设备告警", "告警率"], rows)
        print()


def cmd_device_list(client: XlinkIoTClient, args: argparse.Namespace) -> None:
    """Execute device list command."""
    logger.info("Executing device-list command")

    # Parse JSON configs if provided
    try:
        filter_config = (
            json.loads(args.filter) if args.filter else DEFAULT_DEVICE_LIST_FILTER
        )
    except json.JSONDecodeError as e:
        print(f"❌ 错误：--filter 不是合法 JSON：{e}", file=sys.stderr)
        sys.exit(1)
    try:
        query_config = json.loads(args.query) if args.query else None
    except json.JSONDecodeError as e:
        print(f"❌ 错误：--query 不是合法 JSON：{e}", file=sys.stderr)
        sys.exit(1)
    try:
        order_config = json.loads(args.order) if args.order else None
    except json.JSONDecodeError as e:
        print(f"❌ 错误：--order 不是合法 JSON：{e}", file=sys.stderr)
        sys.exit(1)

    logger.debug(f"Parameters - offset: {args.offset}, limit: {args.limit}")
    logger.debug(f"Filter: {filter_config}")
    logger.debug(f"Query: {query_config}")
    logger.debug(f"Order: {order_config}")

    result = client.get_device_list(
        offset=args.offset,
        limit=args.limit,
        filter_config=filter_config,
        query_config=query_config,
        order_config=order_config,
    )

    logger.info(f"Device list query completed. Total: {result.get('count', 0)}")

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        total = result.get("count", 0)
        devices = result.get("list", [])

        print("\n" + "=" * 50)
        print("📱 XLINK 设备列表")
        print("=" * 50)
        print(f"\n   总数: {total}")
        print(f"   展示: {len(devices)} 台设备")
        print()

        if not devices:
            print("   未找到设备。")
            print()
            return

        rows: list[list[Any]] = []
        for dev in devices:
            base = dev.get("device", {}) if isinstance(dev.get("device"), dict) else {}
            vdev = (
                dev.get("vdevice", {}) if isinstance(dev.get("vdevice"), dict) else {}
            )
            online = (
                dev.get("online", {}) if isinstance(dev.get("online"), dict) else {}
            )
            product = (
                dev.get("product", {}) if isinstance(dev.get("product"), dict) else {}
            )

            name = base.get("name") or dev.get("name") or "N/A"
            device_id = base.get("id") or dev.get("id") or "N/A"
            mac = base.get("mac") or dev.get("mac") or "N/A"
            is_active = (
                base.get("is_active")
                if base.get("is_active") is not None
                else dev.get("is_active", False)
            )
            is_online = (
                online.get("is_online")
                if online.get("is_online") is not None
                else dev.get("is_online", False)
            )
            product_id = base.get("product_id") or dev.get("product_id")
            product_name = product.get("name")
            product_display = product_name or product_id or "N/A"
            last_login = vdev.get("last_login") or dev.get("last_login")

            rows.append(
                [
                    name,
                    device_id,
                    product_display,
                    mac,
                    "在线" if is_online else "离线",
                    "已激活" if is_active else "未激活",
                    last_login or "",
                ]
            )

        _print_table(
            ["设备名称", "设备ID", "产品", "MAC地址", "在线", "激活", "最近登录"], rows
        )
        print()


def cmd_alert_overview(client: XlinkIoTClient, args: argparse.Namespace) -> None:
    """Execute alert overview command."""
    logger.info("Executing alert-overview command")
    logger.debug(
        f"Parameters - product_id: {args.product_id}, project_id: {args.project_id}"
    )

    result = client.get_alert_overview(
        product_id=args.product_id,
        project_id=args.project_id,
    )

    logger.info("Alert overview query completed")

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        added = result.get("added_alert_num", 0)
        history = result.get("history_alert_num", 0)
        device_alerts = result.get("device_alert_num", 0)
        rate = result.get("device_alert_rate", 0)

        print("\n" + "=" * 50)
        print("⚠️  XLINK 告警概览")
        print("=" * 50)
        print(f"\n   🆕 新增告警:        {added}")
        print(f"   📚 历史告警:        {history}")
        print(f"   📱 设备告警:        {device_alerts}")
        print(f"   📊 告警率:          {rate * 100:.2f}%")
        print()


def cmd_event_instances(client: XlinkIoTClient, args: argparse.Namespace) -> None:
    """Execute event instances command."""
    logger.info("Executing event-instances command")

    # Parse comma-separated values
    status = None
    if args.status:
        status_map: dict[str, int] = {
            "1": 1,
            "2": 2,
            "3": 3,
            "PENDING": 1,
            "PROCESSING": 2,
            "PROCESSED": 3,
            "待处理": 1,
            "处理中": 2,
            "已处理": 3,
        }
        parsed_status: list[int] = []
        for raw in args.status.split(","):
            token = raw.strip()
            if not token:
                continue
            if token in status_map:
                parsed_status.append(status_map[token])
                continue
            token_upper = token.upper()
            if token_upper in status_map:
                parsed_status.append(status_map[token_upper])
                continue
            print(f"❌ 错误：--status 参数值不合法：{token}", file=sys.stderr)
            print("   允许值：1,2,3 或 pending,processing,processed", file=sys.stderr)
            sys.exit(1)
        status = parsed_status or None
    event_ids = args.event_ids.split(",") if args.event_ids else None
    project_ids = args.project_ids.split(",") if args.project_ids else None
    processed_ways = None
    if args.processed_ways:
        processed_way_map: dict[str, int] = {
            "-1": -1,
            "1": 1,
            "2": 2,
            "3": 3,
            "4": 4,
            "5": 5,
            "6": 6,
            "7": 7,
            "UNPROCESSED": -1,
            "DEBUG": 1,
            "FAULT": 2,
            "FALSE": 3,
            "OTHER": 4,
            "WORKORDER": 5,
            "SUPPRESS": 6,
            "AUTO": 7,
            "未处理": -1,
            "设备调试": 1,
            "真实故障": 2,
            "误报": 3,
            "其他": 4,
            "转工单": 5,
            "抑制": 6,
            "自动恢复": 7,
        }
        parsed_processed_ways: list[int] = []
        for raw in args.processed_ways.split(","):
            token = raw.strip()
            if not token:
                continue
            if token in processed_way_map:
                parsed_processed_ways.append(processed_way_map[token])
                continue
            token_upper = token.upper()
            if token_upper in processed_way_map:
                parsed_processed_ways.append(processed_way_map[token_upper])
                continue
            print(f"❌ 错误：--processed-ways 参数值不合法：{token}", file=sys.stderr)
            print(
                "   允许值：-1,1,2,3,4,5,6,7 或 unprocessed,debug,fault,false,other,workorder,suppress,auto",
                file=sys.stderr,
            )
            sys.exit(1)
        processed_ways = parsed_processed_ways or None

    logger.debug(
        f"Parameters - status: {status}, device_id: {args.device_id}, limit: {args.limit}"
    )

    result = client.get_event_instances(
        status=status,
        start_time=args.start_time,
        end_time=args.end_time,
        device_id=args.device_id,
        event_ids=event_ids,
        project_ids=project_ids,
        device_name=args.device_name,
        name=args.name,
        processed_ways=processed_ways,
        offset=args.offset,
        limit=args.limit,
    )

    logger.info(f"Event instances query completed. Total: {result.get('count', 0)}")

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        total = result.get("count", 0)
        instances = result.get("list", [])

        print("\n" + "=" * 50)
        print("📋 XLINK 事件实例")
        print("=" * 50)
        print(f"\n   总数: {total}")
        print(f"   展示: {len(instances)} 条")
        print()

        if not instances:
            print("   未找到事件。")
            print()
            return

        rows: list[list[Any]] = []
        for inst in instances:
            base = inst.get("base", {})
            status = base.get("status", "UNKNOWN")
            status_text = {1: "待处理", 2: "处理中", 3: "已处理"}.get(
                status, f"未知({status})"
            )
            status_icon = {1: "🟡", 2: "🟠", 3: "🟢"}.get(status, "⚪")
            processed_way = base.get("processed_way", -1)
            way_text = {
                -1: "未处理",
                1: "设备调试",
                2: "真实故障",
                3: "误报",
                4: "其他",
                5: "转工单",
                6: "抑制",
                7: "自动恢复",
            }.get(processed_way, f"未知({processed_way})")
            create_time = base.get("create_time", "")
            process_time = base.get("process_time", "")
            rows.append(
                [
                    f"{status_icon} {base.get('name', 'N/A')}",
                    base.get("device_name", "N/A"),
                    base.get("device_mac", "N/A"),
                    status_text,
                    way_text,
                    base.get("project_name", "N/A"),
                    create_time,
                    process_time,
                ]
            )

        _print_table(
            [
                "事件",
                "设备名",
                "MAC",
                "状态",
                "处理方式",
                "项目",
                "创建时间",
                "处理时间",
            ],
            rows,
        )
        print()


def main():
    """CLI entry point for device overview and event instances."""
    # First pass: check for --debug flag
    debug_mode = "--debug" in sys.argv

    # Configure logging level
    if debug_mode:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.debug("Debug logging enabled")

    # Remove --debug from argv before parsing
    argv = [arg for arg in sys.argv[1:] if arg != "--debug"]

    parser = argparse.ArgumentParser(
        prog="xlink-api",
        description="Xlink IoT Gateway Client - Query devices and events",
        epilog="Use '%(prog)s <command> --help' for more information about a command.",
    )
    parser.add_argument(
        "--debug", action="store_true", help=argparse.SUPPRESS
    )  # Hidden, already handled
    subparsers = parser.add_subparsers(
        dest="command", required=True, metavar="COMMAND", help="Available commands"
    )
    _setup_subparsers(subparsers)

    try:
        args = parser.parse_args(argv)

        logger.info(f"Starting xlink-api CLI with command: {args.command}")
        client = XlinkIoTClient()
        args.func(client, args)
        logger.info("Command executed successfully")

    except GatewayAppClientError as e:
        logger.error(f"API Error: {e}")
        print(f"❌ API 错误：{e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        logger.error(f"Configuration Error: {e}")
        print(f"❌ 配置错误：{e}", file=sys.stderr)
        print("\n💡 请设置环境变量：", file=sys.stderr)
        print("   export XLINK_BASE_URL='https://api-gw.xlink.cn'", file=sys.stderr)
        print("   export XLINK_APP_ID='your-app-id'", file=sys.stderr)
        print("   export XLINK_APP_SECRET='your-app-secret'", file=sys.stderr)
        print("   export XLINK_API_GROUP='your-group-id'", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        logger.exception(f"Unexpected error: {type(e).__name__}: {e}")
        print(f"❌ 未预期错误：{type(e).__name__}: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
