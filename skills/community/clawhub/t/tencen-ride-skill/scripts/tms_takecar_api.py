import json
import random
import time
import urllib.error
import urllib.request


DEFAULT_API_BASE = "https://test.weixin.go.qq.com"
DEFAULT_POI_SUGGESTION_PATH = "/mcp/open/tms/lbs/suggestion"
DEFAULT_GET_ON_POINTS_PATH = "/mcp/open/tms/recommend/taxi/getOnPoints"
DEFAULT_GET_DROP_OFF_POINT_PATH = "/mcp/open/tms/recommend/taxi/getDropOffPointV2"
DEFAULT_ESTIMATE_PRICE_PATH = "/mcp/open/tms/takecar/estimate/price"
DEFAULT_CREATE_ORDER_PATH = "/mcp/open/tms/takecar/risk/verify/book/order"
DEFAULT_QUERY_ONGOING_ORDER_PATH = "/api/v1/query-ongoing-order"
DEFAULT_CANCEL_ORDER_PATH = "/mcp/open/tms/takecar/cancel/order"
DEFAULT_QUERY_ORDER_PATH = "/mcp/open/tms/takecar/order/detail"
DEFAULT_QUERY_DRIVER_LOCATION_PATH = "/api/v1/query-driver-location"
DEFAULT_WX_APP_ID = "wx65cc950f42e8fff1"
DEFAULT_HTTP_TIMEOUT_SECONDS = 60.0
INVALID_TOKEN_ERR_CODES = {10, 35}


def generate_timestamp_ms() -> int:
	return int(time.time() * 1000)


def generate_seq_id(timestamp_ms: int) -> str:
	# Keep seqId numeric and high-entropy for request tracing.
	random_suffix = random.randint(100000, 999999)
	return f"{timestamp_ms}{random_suffix}"


def build_request_payload(payload: dict, token: str) -> dict:
	timestamp_ms = generate_timestamp_ms()
	request_payload = {
		"seqId": generate_seq_id(timestamp_ms),
		"timestamp": timestamp_ms,
		"wxAppId": DEFAULT_WX_APP_ID,
		"token": token,
	}
	request_payload.update(payload)
	return request_payload


def is_invalid_token_error(body) -> bool:
	if not isinstance(body, dict):
		return False
	err_code = body.get("errCode")
	if isinstance(err_code, str) and err_code.isdigit():
		err_code = int(err_code)
	return err_code in INVALID_TOKEN_ERR_CODES


def post_request(
	base_url: str,
	trips_path: str,
	headers: dict,
	payload: dict,
	token: str = "",
	urlopen_func=None,
	timeout_seconds: float = DEFAULT_HTTP_TIMEOUT_SECONDS,
) -> dict:
	if urlopen_func is None:
		urlopen_func = urllib.request.urlopen
	url = base_url.rstrip("/") + "/" + trips_path.strip("/")
	request_payload = build_request_payload(payload, token)
	request = urllib.request.Request(
		url=url,
		data=json.dumps(request_payload, ensure_ascii=False).encode("utf-8"),
		headers=headers,
		method="POST",
	)
	with urlopen_func(request, timeout=timeout_seconds) as response:
		body = response.read().decode("utf-8")
		if not body.strip():
			return {"status": response.status, "body": None}
		try:
			return {"status": response.status, "body": json.loads(body)}
		except json.JSONDecodeError:
			return {"status": response.status, "body": body}


def run_json_api_command(
	environ: dict,
	stdout,
	stderr,
	payload: dict,
	api_path: str,
	success_mode: str,
	load_token_func,
	build_headers_func,
	write_json_func,
	default_api_base: str,
	result_transform=None,
	urlopen_func=None,
) -> int:
	if urlopen_func is None:
		urlopen_func = urllib.request.urlopen
	token = load_token_func(environ)
	if not token:
		stderr.write("Token is not configured. Run: save-token <token>\n")
		return 1

	base_url = default_api_base.strip()
	if not base_url:
		write_json_func(
			stdout,
			{
				"mode": "blocked",
				"reason": "DEFAULT_API_BASE is not configured",
				"payload": payload,
			},
		)
		return 2

	headers = build_headers_func(token)
	try:
		result = post_request(
			base_url,
			api_path,
			headers,
			payload,
			token=token,
			urlopen_func=urlopen_func,
			timeout_seconds=DEFAULT_HTTP_TIMEOUT_SECONDS,
		)
	except urllib.error.HTTPError as exc:
		error_body = exc.read().decode("utf-8", errors="replace")
		try:
			error_body_json = json.loads(error_body)
		except json.JSONDecodeError:
			error_body_json = None
		if is_invalid_token_error(error_body_json):
			write_json_func(
				stderr,
				{
					"mode": "error",
					"status": exc.code,
					"body": error_body,
				},
			)
			return 1
		write_json_func(
			stderr,
			{
				"mode": "error",
				"status": exc.code,
				"body": error_body,
			},
		)
		return 3
	except urllib.error.URLError as exc:
		write_json_func(
			stderr,
			{
				"mode": "error",
				"reason": str(exc),
				"hint": "Request timed out after 60s",
			},
		)
		return 4

	if result_transform is not None:
		result = result_transform(result)

	result_body = result.get("body") if isinstance(result, dict) else None
	if is_invalid_token_error(result_body):
		write_json_func(
			stderr,
			{
				"mode": "error",
				"reason": "token is missing or invalid",
				"body": result_body,
			},
		)
		return 1

	write_json_func(stdout, {"mode": success_mode, "result": result})
	return 0
