#!/usr/bin/env python3
import argparse
import json
import math
import os
import platform
import re
import sys
from typing import List, Optional, Tuple
import urllib.parse
import urllib.request

from tms_takecar_api import (
	DEFAULT_HTTP_TIMEOUT_SECONDS,
	DEFAULT_WX_APP_ID,
	generate_seq_id,
	generate_timestamp_ms,
	is_invalid_token_error,
	post_request,
	run_json_api_command,
)
DEFAULT_API_BASE = "https://weixin.go.qq.com"
DEFAULT_POI_SUGGESTION_PATH = "/mcp/open/tms/lbs/suggestion"
DEFAULT_GET_ON_POINTS_PATH = "/mcp/open/tms/recommend/taxi/getOnPoints"
DEFAULT_GET_DROP_OFF_POINT_PATH = "/mcp/open/tms/recommend/taxi/getDropOffPointV2"
DEFAULT_ESTIMATE_PRICE_PATH = "/mcp/open/tms/takecar/estimate/price"
DEFAULT_CREATE_ORDER_PATH = "/mcp/open/tms/takecar/risk/verify/book/order"
DEFAULT_QUERY_ONGOING_ORDER_PATH = "/mcp/open/tms/takecar/order/ongoing"
DEFAULT_CANCEL_ORDER_PATH = "/mcp/open/tms/takecar/cancel/order"
DEFAULT_QUERY_ORDER_PATH = "/mcp/open/tms/takecar/order/detail"
DEFAULT_QUERY_DRIVER_LOCATION_PATH = "/mcp/open/tms/takecar/passenger/order/driverPassengerDisplay"
DEFAULT_STATIC_MAP_PATH = "/mcp/open/tms/lbs/staticMap"
DEFAULT_STATIC_MAP_SIZE = "800*600"
DEFAULT_STATIC_MAP_SCALE = 2
DEFAULT_STATIC_MAP_MAPTYPE = "roadmap"
SCENE_TO_POLICY = {0: 0, 1: 10, 2: 11}
ALLOWED_RIDE_TYPES = {1, 2, 3, 4, 5, 6, 7}
STATIC_MAP_MARKER_PRESETS = {
	"起": {"color": "red", "label": "起"},
	"终": {"color": "green", "label": "终"},
	"P": {"color": "blue", "label": "P"},
}
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), "assets")
TOKEN_CONFIG_DIR = os.path.join(os.path.expanduser("~"), ".config", "tms-takecar")
TOKEN_CONFIG_FILE = os.path.join(TOKEN_CONFIG_DIR, "token")
ENV_CONFIG_FILE = os.path.join(TOKEN_CONFIG_DIR, "env.json")
PREFERENCE_FILE_PATH = os.path.join(ASSETS_DIR, "preference.md")
STATE_FILE_PATH = os.path.join(TOKEN_CONFIG_DIR, "state.json")
ADDR_FILE_PATH = os.path.join(TOKEN_CONFIG_DIR, "addr.json")
SHORT_CUT_FILE_PATH = os.path.join(TOKEN_CONFIG_DIR, "short-cut.json")


def build_default_env_config() -> dict:
	return {
		"env": {
			"python": False,
		},
		"resident_city": "",
		"token": "",
		"updated_at": "",
	}


def build_default_state() -> dict:
	return {
		"pickup": [],
		"dropoff": [],
		"estimate": None,
		"userPreferLabels": [],
		"orderId": None,
	}


def _ensure_state_parent_dir(state_file: str) -> None:
	parent = os.path.dirname(state_file)
	if parent:
		os.makedirs(parent, exist_ok=True)


def _ensure_env_parent_dir(env_file: str) -> None:
	parent = os.path.dirname(env_file)
	if parent:
		os.makedirs(parent, exist_ok=True)


def _ensure_json_parent_dir(file_path: str) -> None:
	parent = os.path.dirname(file_path)
	if parent:
		os.makedirs(parent, exist_ok=True)


def _resolve_env_file_path(env_file: Optional[str] = None) -> str:
	if env_file:
		return env_file
	token_dir = os.path.dirname(TOKEN_CONFIG_FILE)
	if token_dir:
		return os.path.join(token_dir, "env.json")
	return ENV_CONFIG_FILE


def _normalize_env_config(data: dict) -> dict:
	env_config = build_default_env_config()
	env = data.get("env")
	if isinstance(env, dict):
		python_ok = env.get("python")
		env_config["env"]["python"] = bool(python_ok) if isinstance(python_ok, bool) else False
	resident_city = data.get("resident_city")
	if isinstance(resident_city, str):
		env_config["resident_city"] = resident_city.strip()
	token = data.get("token")
	if isinstance(token, str):
		env_config["token"] = token.strip()
	updated_at = data.get("updated_at")
	if isinstance(updated_at, str):
		env_config["updated_at"] = updated_at.strip()
	return env_config


def load_env_config(env_file: Optional[str] = None) -> dict:
	env_file = _resolve_env_file_path(env_file)
	try:
		with open(env_file, "r", encoding="utf-8") as handle:
			data = json.load(handle)
			if isinstance(data, dict):
				return _normalize_env_config(data)
	except (OSError, json.JSONDecodeError):
		pass
	return build_default_env_config()


def save_env_config(env_config: dict, env_file: Optional[str] = None) -> str:
	env_file = _resolve_env_file_path(env_file)
	_ensure_env_parent_dir(env_file)
	normalized = _normalize_env_config(env_config)
	with open(env_file, "w", encoding="utf-8") as handle:
		json.dump(normalized, handle, ensure_ascii=False, indent=2)
		handle.write("\n")
	return env_file


def _load_legacy_token(config_file: Optional[str] = None) -> str:
	config_file = config_file or TOKEN_CONFIG_FILE
	try:
		with open(config_file, "r", encoding="utf-8") as f:
			return f.read().strip()
	except OSError:
		return ""


def load_state_file(state_file: Optional[str] = None) -> dict:
	state_file = state_file or STATE_FILE_PATH
	try:
		with open(state_file, "r", encoding="utf-8") as handle:
			data = json.load(handle)
			if isinstance(data, dict):
				state = build_default_state()
				pickup = data.get("pickup")
				dropoff = data.get("dropoff")
				state["pickup"] = pickup if isinstance(pickup, list) else []
				state["dropoff"] = dropoff if isinstance(dropoff, list) else []
				state["estimate"] = data.get("estimate")
				user_prefer_labels = data.get("userPreferLabels")
				state["userPreferLabels"] = user_prefer_labels if isinstance(user_prefer_labels, list) else []
				state["orderId"] = data.get("orderId")
				return state
	except (OSError, json.JSONDecodeError):
		pass
	return build_default_state()


def save_state_file(state: dict, state_file: Optional[str] = None) -> str:
	state_file = state_file or STATE_FILE_PATH
	_ensure_state_parent_dir(state_file)
	with open(state_file, "w", encoding="utf-8") as handle:
		json.dump(state, handle, ensure_ascii=False, indent=2)
		handle.write("\n")
	return state_file


def _load_json_key_value_store(file_path: str) -> dict:
	try:
		with open(file_path, "r", encoding="utf-8") as handle:
			data = json.load(handle)
			if isinstance(data, dict):
				return data
	except (OSError, json.JSONDecodeError):
		pass
	return {}


def _save_json_key_value_store(file_path: str, data: dict) -> str:
	_ensure_json_parent_dir(file_path)
	with open(file_path, "w", encoding="utf-8") as handle:
		json.dump(data, handle, ensure_ascii=False, indent=2)
		handle.write("\n")
	return file_path


def _resolve_addr_file_path(addr_file: Optional[str] = None) -> str:
	return addr_file or ADDR_FILE_PATH


def _resolve_short_cut_file_path(short_cut_file: Optional[str] = None) -> str:
	return short_cut_file or SHORT_CUT_FILE_PATH


def _parse_json_object_arg(raw_text: str, field_name: str) -> dict:
	try:
		parsed = json.loads(raw_text)
	except json.JSONDecodeError as exc:
		raise ValueError(f"invalid {field_name} json: {exc}")
	if not isinstance(parsed, dict):
		raise ValueError(f"{field_name} must be a JSON object")
	return parsed


def _list_store_keys(file_path: str) -> dict:
	store = _load_json_key_value_store(file_path)
	return {
		"keys": list(store.keys()),
		"count": len(store),
	}


def _get_store_value_by_key(file_path: str, key: str) -> dict:
	store = _load_json_key_value_store(file_path)
	lookup_key = key.strip()
	if not lookup_key:
		raise ValueError("key is required")
	return {
		"key": lookup_key,
		"found": lookup_key in store,
		"value": store.get(lookup_key),
	}


def _upsert_store_value(file_path: str, key: str, value: dict) -> dict:
	store = _load_json_key_value_store(file_path)
	lookup_key = key.strip()
	if not lookup_key:
		raise ValueError("key is required")
	existed = lookup_key in store
	store[lookup_key] = value
	written_file = _save_json_key_value_store(file_path, store)
	return {
		"updated": True,
		"created": not existed,
		"key": lookup_key,
		"value": value,
		"file": written_file,
	}


def get_addr_keys(addr_file: Optional[str] = None) -> dict:
	addr_file = _resolve_addr_file_path(addr_file)
	payload = _list_store_keys(addr_file)
	payload["addr_file"] = addr_file
	return payload


def get_addr_value_by_key(key: str, addr_file: Optional[str] = None) -> dict:
	addr_file = _resolve_addr_file_path(addr_file)
	payload = _get_store_value_by_key(addr_file, key)
	payload["addr_file"] = addr_file
	return payload


def upsert_addr_value(key: str, value: dict, addr_file: Optional[str] = None) -> dict:
	addr_file = _resolve_addr_file_path(addr_file)
	payload = _upsert_store_value(addr_file, key, value)
	payload["addr_file"] = addr_file
	return payload


def sync_addr_value_to_state(key: str, scene: int, addr_file: Optional[str] = None, state_file: Optional[str] = None) -> dict:
	addr_file = _resolve_addr_file_path(addr_file)
	lookup_key = key.strip()
	if not lookup_key:
		raise ValueError("key is required")
	scene_key = _get_scene_key(scene)
	addr_payload = get_addr_value_by_key(lookup_key, addr_file=addr_file)
	if not addr_payload.get("found"):
		raise ValueError(f"key not found in addr store: {lookup_key}")
	value = addr_payload.get("value")
	if not isinstance(value, dict):
		raise ValueError(f"invalid addr value for key: {lookup_key}")
	normalized = _normalize_poi_item(value)
	if not str(normalized.get("poiid", "")).strip():
		raise ValueError(f"missing required field: {lookup_key}.poiid")
	state = load_state_file(state_file=state_file)
	state[scene_key] = [normalized]
	state["estimate"] = None
	state["userPreferLabels"] = []
	state["orderId"] = None
	written_state_file = save_state_file(state, state_file=state_file)
	return {
		"updated": True,
		"key": lookup_key,
		"scene": scene,
		"scene_key": scene_key,
		"state_file": written_state_file,
		"addr_file": addr_file,
	}


def get_short_cut_keys(short_cut_file: Optional[str] = None) -> dict:
	short_cut_file = _resolve_short_cut_file_path(short_cut_file)
	payload = _list_store_keys(short_cut_file)
	payload["short_cut_file"] = short_cut_file
	return payload


def get_short_cut_value_by_key(key: str, short_cut_file: Optional[str] = None) -> dict:
	short_cut_file = _resolve_short_cut_file_path(short_cut_file)
	payload = _get_store_value_by_key(short_cut_file, key)
	payload["short_cut_file"] = short_cut_file
	return payload


def upsert_short_cut_value(key: str, value: dict, short_cut_file: Optional[str] = None) -> dict:
	short_cut_file = _resolve_short_cut_file_path(short_cut_file)
	payload = _upsert_store_value(short_cut_file, key, value)
	payload["short_cut_file"] = short_cut_file
	return payload


def _parse_prefer_labels_json(raw_text: str) -> List[int]:
	try:
		parsed = json.loads(raw_text)
	except json.JSONDecodeError as exc:
		raise ValueError(f"invalid user prefer labels json: {exc}")
	if not isinstance(parsed, list):
		raise ValueError("user prefer labels must be a JSON array")
	result: List[int] = []
	for item in parsed:
		if isinstance(item, bool):
			raise ValueError("user prefer labels must contain integers")
		if not isinstance(item, int):
			raise ValueError("user prefer labels must contain integers")
		result.append(item)
	return result


def _parse_price_estimate_keys_json(raw_text: str) -> List[str]:
	try:
		parsed = json.loads(raw_text)
	except json.JSONDecodeError as exc:
		raise ValueError(f"invalid price estimate keys json: {exc}")
	if not isinstance(parsed, list):
		raise ValueError("priceEstimateKeys must be a JSON array")
	result: List[str] = []
	for item in parsed:
		if not isinstance(item, str):
			raise ValueError("priceEstimateKeys must contain strings")
		result.append(item)
	return result


def _require_dict(parent: dict, key: str, path: str) -> dict:
	value = parent.get(key)
	if not isinstance(value, dict):
		raise ValueError(f"missing required object: {path}")
	return value


def _require_non_empty(value, path: str):
	if value in (None, ""):
		raise ValueError(f"missing required field: {path}")
	return value


def _require_number(value, path: str) -> float:
	if isinstance(value, bool):
		raise ValueError(f"invalid number field: {path}")
	if not isinstance(value, (int, float)):
		raise ValueError(f"invalid number field: {path}")
	return float(value)


def _get_scene_key(scene: int) -> str:
	if scene == 1:
		return "pickup"
	if scene == 2:
		return "dropoff"
	raise ValueError("scene must be one of 1, 2")


def _normalize_poi_item(item: dict) -> dict:
	return {
		"name": item.get("name", ""),
		"address": item.get("address", ""),
		"longitude": item.get("longitude", ""),
		"latitude": item.get("latitude", ""),
		"poiid": item.get("poiid", ""),
		"citycode": item.get("citycode", ""),
		"point_name": item.get("point_name", ""),
		"point_longitude": item.get("point_longitude", ""),
		"point_latitude": item.get("point_latitude", ""),
	}


def _parse_static_map_markers_json(raw_text: str) -> List[dict]:
	try:
		parsed = json.loads(raw_text)
	except json.JSONDecodeError as exc:
		raise ValueError(f"invalid markers json: {exc}")
	if not isinstance(parsed, list) or not parsed:
		raise ValueError("markers must be a non-empty JSON array")
	result: List[dict] = []
	for index, item in enumerate(parsed):
		if not isinstance(item, dict):
			raise ValueError(f"markers[{index}] must be a JSON object")
		result.append(item)
	return result


def _coerce_static_map_coordinate(value, field_name: str, index: int) -> float:
	if isinstance(value, bool) or not isinstance(value, (int, float, str)):
		raise ValueError(f"markers[{index}].{field_name} must be a number")
	try:
		number = float(value)
	except (TypeError, ValueError):
		raise ValueError(f"markers[{index}].{field_name} must be a number")
	return number


def _normalize_static_map_marker_type(value, index: int) -> str:
	text = str(value).strip() if value is not None else ""
	if text not in STATIC_MAP_MARKER_PRESETS:
		raise ValueError("markers[%d].marker must be one of: %s" % (index, ", ".join(STATIC_MAP_MARKER_PRESETS.keys())))
	return text


def normalize_static_map_markers(markers: List[dict]) -> List[dict]:
	normalized: List[dict] = []
	for index, item in enumerate(markers):
		latitude = _coerce_static_map_coordinate(item.get("latitude"), "latitude", index)
		longitude = _coerce_static_map_coordinate(item.get("longitude"), "longitude", index)
		if latitude < -90 or latitude > 90:
			raise ValueError(f"markers[{index}].latitude out of range: {latitude}")
		if longitude < -180 or longitude > 180:
			raise ValueError(f"markers[{index}].longitude out of range: {longitude}")
		marker_type = _normalize_static_map_marker_type(item.get("marker"), index)
		normalized.append({
			"latitude": latitude,
			"longitude": longitude,
			"marker": marker_type,
		})
	return normalized


def _parse_static_map_size(size_text: str) -> Tuple[int, int]:
	match = re.fullmatch(r"\s*(\d+)\s*\*\s*(\d+)\s*", str(size_text))
	if not match:
		raise ValueError("size must be in WIDTH*HEIGHT format")
	width = int(match.group(1))
	height = int(match.group(2))
	if width < 50 or width > 1680:
		raise ValueError("size width must be between 50 and 1680")
	if height < 50 or height > 1200:
		raise ValueError("size height must be between 50 and 1200")
	return width, height


def _lat_to_mercator_rad(latitude: float) -> float:
	sin_value = math.sin(math.radians(latitude))
	rad_x2 = math.log((1 + sin_value) / (1 - sin_value)) / 2
	return max(min(rad_x2, math.pi), -math.pi) / 2


def _zoom_for_fraction(map_pixels: float, world_pixels: float, fraction: float) -> float:
	if map_pixels <= 0 or world_pixels <= 0:
		return 4.0
	if fraction <= 0:
		return 18.0
	return math.log(map_pixels / world_pixels / fraction, 2)


def calculate_static_map_center(markers: List[dict]) -> Tuple[float, float]:
	latitudes = [item["latitude"] for item in markers]
	longitudes = [item["longitude"] for item in markers]
	return (min(latitudes) + max(latitudes)) / 2.0, (min(longitudes) + max(longitudes)) / 2.0


def calculate_static_map_zoom(markers: List[dict], width: int, height: int, scale: int = 2, padding: int = 40) -> int:
	if len(markers) == 1:
		return 17 if scale == 2 else 18
	usable_width = max(width - padding * 2, 1)
	usable_height = max(height - padding * 2, 1)
	if scale == 2:
		usable_width *= 2
		usable_height *= 2

	latitudes = [item["latitude"] for item in markers]
	longitudes = [item["longitude"] for item in markers]
	max_lat = max(latitudes)
	min_lat = min(latitudes)
	max_lng = max(longitudes)
	min_lng = min(longitudes)

	lat_fraction = (_lat_to_mercator_rad(max_lat) - _lat_to_mercator_rad(min_lat)) / math.pi
	lng_diff = max_lng - min_lng
	if lng_diff < 0:
		lng_diff += 360
	lng_fraction = lng_diff / 360.0

	lat_zoom = _zoom_for_fraction(usable_height, 256.0, lat_fraction)
	lng_zoom = _zoom_for_fraction(usable_width, 256.0, lng_fraction)
	max_zoom = 17 if scale == 2 else 18
	return max(4, min(int(math.floor(min(lat_zoom, lng_zoom))), max_zoom))


def build_static_map_marker_params(markers: List[dict]) -> List[str]:
	grouped = {}
	for item in markers:
		preset = STATIC_MAP_MARKER_PRESETS[item["marker"]]
		group_key = (preset["color"], preset["label"])
		grouped.setdefault(group_key, []).append(f'{item["latitude"]:.6f},{item["longitude"]:.6f}')
	params = []
	for (color, label), locations in grouped.items():
		style_parts = [f"size:large", f"color:{color}", f"label:{label}"]
		params.append("|".join(style_parts + locations))
	return params


def build_static_map_url(markers: List[dict], token: str = "") -> str:
	size = DEFAULT_STATIC_MAP_SIZE
	scale = DEFAULT_STATIC_MAP_SCALE
	maptype = DEFAULT_STATIC_MAP_MAPTYPE
	if scale not in (1, 2):
		raise ValueError("scale must be 1 or 2")
	if maptype not in ("roadmap", "satellite", "hybrid"):
		raise ValueError("maptype must be one of: roadmap, satellite, hybrid")
	normalized_markers = normalize_static_map_markers(markers)
	width, height = _parse_static_map_size(size)
	center_lat, center_lng = calculate_static_map_center(normalized_markers)
	zoom = calculate_static_map_zoom(normalized_markers, width=width, height=height, scale=scale)
	timestamp_ms = generate_timestamp_ms()
	seq_id = generate_seq_id(timestamp_ms)
	query_params = [
		("seqId", seq_id),
		("wxAppId", DEFAULT_WX_APP_ID),
		("token", token),
		("timestamp", str(timestamp_ms)),
		("size", f"{width}*{height}"),
		("center", f"{center_lat:.6f},{center_lng:.6f}"),
		("zoom", str(zoom)),
		("scale", str(scale)),
		("maptype", maptype),
	]
	for marker_param in build_static_map_marker_params(normalized_markers):
		query_params.append(("markers", marker_param))
	url = "%s%s?%s" % (
		DEFAULT_API_BASE.rstrip("/"),
		DEFAULT_STATIC_MAP_PATH,
		urllib.parse.urlencode(query_params, doseq=True),
	)
	return url


def _append_poi_candidates(existing: list, items: list) -> list:
	poiid_to_index = {}
	for idx, entry in enumerate(existing):
		if not isinstance(entry, dict):
			continue
		poiid = str(entry.get("poiid", "")).strip()
		if poiid:
			poiid_to_index[poiid] = idx
	for item in items:
		if not isinstance(item, dict):
			continue
		normalized = _normalize_poi_item(item)
		poiid = str(normalized.get("poiid", "")).strip()
		if not poiid:
			continue
		if poiid in poiid_to_index:
			existing[poiid_to_index[poiid]] = normalized
		else:
			poiid_to_index[poiid] = len(existing)
			existing.append(normalized)
	return existing


def update_state_from_poi_search(scene: int, items: list, state_file: Optional[str] = None) -> Optional[str]:
	if scene not in (1, 2) or not items:
		return None
	state = load_state_file(state_file=state_file)
	scene_key = _get_scene_key(scene)
	candidates = state.get(scene_key)
	if not isinstance(candidates, list):
		candidates = []
	state[scene_key] = _append_poi_candidates(candidates, items)
	return save_state_file(state, state_file=state_file)


def apply_select_poi(poiid: str, scene: int, state_file: Optional[str] = None) -> dict:
	selected_poiid = poiid.strip()
	if not selected_poiid:
		raise ValueError("poiid is required")
	scene_key = _get_scene_key(scene)
	state = load_state_file(state_file=state_file)
	candidates = state.get(scene_key)
	if not isinstance(candidates, list) or not candidates:
		raise ValueError(f"missing candidates for scene={scene}")

	selected = None
	for item in candidates:
		if not isinstance(item, dict):
			continue
		if str(item.get("poiid", "")).strip() == selected_poiid:
			selected = _normalize_poi_item(item)
			break
	if selected is None:
		raise ValueError(f"poiid not found in scene={scene}: {selected_poiid}")

	state[scene_key] = [selected]
	state["estimate"] = None
	state["userPreferLabels"] = []
	state["orderId"] = None
	written_state_file = save_state_file(state, state_file=state_file)
	return {
		"updated": True,
		"scene": scene,
		"poiid": selected_poiid,
		"state_file": written_state_file,
	}


def _require_selected_scene_item(state: dict, scene: int) -> dict:
	scene_key = _get_scene_key(scene)
	candidates = state.get(scene_key)
	if not isinstance(candidates, list) or len(candidates) != 1:
		raise ValueError(f"missing selected candidate: {scene_key}")
	selected = candidates[0]
	if not isinstance(selected, dict):
		raise ValueError(f"missing selected candidate: {scene_key}")
	return selected


def build_estimate_state_products(data: dict) -> list:
	products = []
	product_list = data.get("product") if isinstance(data, dict) else []
	default_estimate_time = data.get("estimateTime") if isinstance(data, dict) else None
	default_estimate_distance = data.get("distance") if isinstance(data, dict) else None
	if not isinstance(product_list, list):
		return products
	for product in product_list:
		if not isinstance(product, dict):
			continue
		rider_info = product.get("riderInfo")
		if not isinstance(rider_info, dict):
			continue
		estimate_list = product.get("priceEstimate")
		if not isinstance(estimate_list, list):
			continue
		for estimate_item in estimate_list:
			if not isinstance(estimate_item, dict):
				continue
			sp = estimate_item.get("sp")
			if not isinstance(sp, dict):
				sp = {}
			default_checked = estimate_item.get("defaultChecked")
			products.append({
				"isTop": product.get("isTop", 0),
				"topStyle": product.get("topStyle", 1),
				"riderInfo": {
					"rideType": rider_info.get("rideType"),
					"riderClassify": rider_info.get("riderClassify"),
					"riderDesc": rider_info.get("riderDesc"),
				},
				"id": estimate_item.get("id"),
				"priceEstimateKey": estimate_item.get("priceEstimateKey"),
				"defaultChecked": default_checked,
				"discountType": estimate_item.get("discountType"),
				"discountAmount": estimate_item.get("discountAmount"),
				"discountPercentage": estimate_item.get("discountPercentage"),
				"estimatePrice": estimate_item.get("estimatePrice"),
				"estimateTime": estimate_item.get("estimateTime", default_estimate_time),
				"estimateDistance": estimate_item.get("estimateDistance", default_estimate_distance),
				"estimateDuration": estimate_item.get("estimateDuration", default_estimate_time),
				"isPriceChange": estimate_item.get("isPriceChange"),
				"platEstimatePriceType": estimate_item.get("platEstimatePriceType"),
				"platEstimatePrice": estimate_item.get("platEstimatePrice"),
				"userSelect": 1 if default_checked == 1 else 0,
				"sp": {
					"code": sp.get("code"),
					"name": sp.get("name"),
					"avatar": sp.get("avatar", ""),
				},
			})
	return products


def update_state_from_estimate_result(result: dict, user_prefer_labels: List[int], state_file: Optional[str] = None) -> Optional[str]:
	if not isinstance(result, dict):
		return None
	body = result.get("body")
	if not isinstance(body, dict):
		return None
	if body.get("code") != 0:
		return None
	data = body.get("data")
	if not isinstance(data, dict):
		return None
	if data.get("estimateKey") in (None, ""):
		return None

	state = load_state_file(state_file=state_file)
	state["estimate"] = {
		"estimateKey": data.get("estimateKey"),
		"distance": data.get("distance"),
		"estimateTime": data.get("estimateTime"),
		"products": build_estimate_state_products(data),
		"userPreferLabels": user_prefer_labels,
	}
	state["userPreferLabels"] = user_prefer_labels
	state["orderId"] = None
	return save_state_file(state, state_file=state_file)


def update_state_from_create_order_result(result: dict, state_file: Optional[str] = None) -> Optional[str]:
	if not isinstance(result, dict):
		return None
	body = result.get("body")
	if not isinstance(body, dict):
		return None
	code, _message, data = extract_create_order_business_fields(body)
	if code != 0:
		return None
	order_id = normalize_order_id(data.get("orderId"))
	if not order_id:
		return None
	state = load_state_file(state_file=state_file)
	state["orderId"] = order_id
	return save_state_file(state, state_file=state_file)


def build_estimate_price_payload_from_state(state: dict) -> dict:
	pickup = _require_selected_scene_item(state, scene=1)
	dropoff = _require_selected_scene_item(state, scene=2)

	city_code = normalize_city_code(str(_require_non_empty(pickup.get("citycode"), "pickup[0].citycode")))
	dest_city_code = normalize_city_code(str(_require_non_empty(dropoff.get("citycode"), "dropoff[0].citycode")))
	from_lat = _require_number(pickup.get("point_latitude"), "pickup[0].point_latitude")
	from_lng = _require_number(pickup.get("point_longitude"), "pickup[0].point_longitude")
	to_lat = _require_number(dropoff.get("point_latitude"), "dropoff[0].point_latitude")
	to_lng = _require_number(dropoff.get("point_longitude"), "dropoff[0].point_longitude")

	timestamp_ms = generate_timestamp_ms()
	payload = {
		"seqId": generate_seq_id(timestamp_ms),
		"timestamp": timestamp_ms,
		"departureTime": timestamp_ms,
		"orderServiceType": 1,
		"cityCode": city_code,
		"destCityCode": dest_city_code,
		"fromLat": from_lat,
		"fromLng": from_lng,
		"fromName": _require_non_empty(pickup.get("name"), "pickup[0].name"),
		"fromAddress": _require_non_empty(pickup.get("address"), "pickup[0].address"),
		"toId": _require_non_empty(dropoff.get("poiid"), "dropoff[0].poiid"),
		"toLat": to_lat,
		"toLng": to_lng,
		"toName": _require_non_empty(dropoff.get("name"), "dropoff[0].name"),
		"toAddress": _require_non_empty(dropoff.get("address"), "dropoff[0].address"),
	}
	payload["currentLat"] = from_lat
	payload["currentLng"] = from_lng
	return payload


def _validate_user_prefer_labels(value) -> List[int]:
	if not isinstance(value, list):
		raise ValueError("missing required field: estimate.userPreferLabels")
	result: List[int] = []
	for item in value:
		if isinstance(item, bool) or not isinstance(item, int):
			raise ValueError("invalid user prefer labels in estimate.userPreferLabels")
		result.append(item)
	return result


def normalize_order_id(value) -> str:
	if value is None:
		return ""
	text = str(value).strip()
	if not text or text.lower() == "null":
		return ""
	return text


def extract_create_order_business_fields(body: dict) -> Tuple[object, object, dict]:
	if not isinstance(body, dict):
		return None, "", {}
	business_code = body.get("code")
	business_message = body.get("message")
	data = body.get("data")
	if not isinstance(data, dict):
		return business_code, business_message, {}

	nested_data = data.get("data")
	nested_code = data.get("code")
	nested_message = data.get("message")
	if isinstance(nested_data, dict):
		if nested_code is not None:
			business_code = nested_code
		if nested_message is not None:
			business_message = nested_message
		return business_code, business_message, nested_data

	return business_code, business_message, data


def build_create_order_result_data(body: dict) -> dict:
	code, message, data = extract_create_order_business_fields(body)
	order_id = normalize_order_id(data.get("orderId"))
	unfinished_order = data.get("unfinishedOrder")
	if not isinstance(unfinished_order, bool):
		unfinished_order = code == 101 or (not order_id and isinstance(message, str) and ("未完成" in message or "进行中" in message))
	return {
		"orderId": order_id,
		"unfinishedOrder": unfinished_order,
	}


def transform_create_order_result(result: dict) -> dict:
	if not isinstance(result, dict):
		return result
	body = result.get("body")
	if not isinstance(body, dict):
		return result
	result["body"] = {
		"code": body.get("code"),
		"message": body.get("message"),
		"data": build_create_order_result_data(body),
	}
	return result


def _get_point_value(item: dict, point_key: str, fallback_key: str):
	point_value = item.get(point_key)
	if point_value not in (None, ""):
		return point_value
	return item.get(fallback_key)


def _build_estimate_price_entry(item: dict, idx: int) -> dict:
	rider_info = _require_dict(item, "riderInfo", f"estimate.products[{idx}].riderInfo")
	ride_type = _require_non_empty(rider_info.get("rideType"), f"estimate.products[{idx}].riderInfo.rideType")
	rider_classify = _require_non_empty(rider_info.get("riderClassify"), f"estimate.products[{idx}].riderInfo.riderClassify")
	sp = _require_dict(item, "sp", f"estimate.products[{idx}].sp")
	sp_code = _require_non_empty(sp.get("code"), f"estimate.products[{idx}].sp.code")
	price_estimate_key = _require_non_empty(item.get("priceEstimateKey"), f"estimate.products[{idx}].priceEstimateKey")
	entry_id = item.get("id")
	if entry_id in (None, ""):
		entry_id = f"{rider_classify}-{ride_type}-{sp_code}"
	return {
		"id": entry_id,
		"choosed": True,
		"spName": sp.get("name", ""),
		"spCode": sp_code,
		"spAvatar": sp.get("avatar", ""),
		"isPriceChange": item.get("isPriceChange"),
		"estimateTime": item.get("estimateTime"),
		"discountType": item.get("discountType"),
		"estimatePrice": item.get("estimatePrice"),
		"discountAmount": item.get("discountAmount"),
		"priceEstimateKey": price_estimate_key,
		"platEstimatePriceType": item.get("platEstimatePriceType"),
		"platEstimatePrice": item.get("platEstimatePrice"),
		"estimateDistance": item.get("estimateDistance"),
		"estimateDuration": item.get("estimateDuration"),
	}


def build_product_str_from_estimate_products(products: list) -> str:
	if not isinstance(products, list):
		raise ValueError("missing required field: estimate.products")
	built = []
	for idx, item in enumerate(products):
		if not isinstance(item, dict):
			continue
		if item.get("userSelect") != 1:
			continue
		rider_info = _require_dict(item, "riderInfo", f"estimate.products[{idx}].riderInfo")
		ride_type = _require_non_empty(rider_info.get("rideType"), f"estimate.products[{idx}].riderInfo.rideType")
		rider_classify = _require_non_empty(rider_info.get("riderClassify"), f"estimate.products[{idx}].riderInfo.riderClassify")
		built.append({
			"isTop": item.get("isTop", 0),
			"topStyle": item.get("topStyle", 1),
			"riderInfo": {
				"rideType": ride_type,
				"riderClassify": rider_classify,
			},
			"estimatePrices": [_build_estimate_price_entry(item, idx)],
		})
	if not built:
		raise ValueError("missing selected products: estimate.products[].userSelect=1")
	return json.dumps(built, ensure_ascii=False)


def build_create_order_payload_from_state(state: dict) -> dict:
	pickup = _require_selected_scene_item(state, scene=1)
	dropoff = _require_selected_scene_item(state, scene=2)
	estimate = _require_dict(state, "estimate", "estimate")
	timestamp_ms = generate_timestamp_ms()

	return {
		"seqId": generate_seq_id(timestamp_ms),
		"timestamp": timestamp_ms,
		"estimateKey": _require_non_empty(estimate.get("estimateKey"), "estimate.estimateKey"),
		"departureTime": timestamp_ms,
		"orderServiceType": 1,
		"fromLat": _require_number(pickup.get("point_latitude"), "pickup[0].point_latitude"),
		"fromLng": _require_number(pickup.get("point_longitude"), "pickup[0].point_longitude"),
		"fromName": _require_non_empty(_get_point_value(pickup, "point_name", "name"), "pickup[0].point_name"),
		"fromAddress": _require_non_empty(_get_point_value(pickup, "address", "point_name"), "pickup[0].address"),
		"productStr": build_product_str_from_estimate_products(estimate.get("products")),
		"toId": _require_non_empty(dropoff.get("poiid"), "dropoff[0].poiid"),
		"toLat": _require_number(dropoff.get("point_latitude"), "dropoff[0].point_latitude"),
		"toLng": _require_number(dropoff.get("point_longitude"), "dropoff[0].point_longitude"),
		"toName": _require_non_empty(_get_point_value(dropoff, "point_name", "name"), "dropoff[0].point_name"),
		"toAddress": _require_non_empty(_get_point_value(dropoff, "address", "point_name"), "dropoff[0].address"),
		"isNeedReEstimate": True,
	}


def sign(sk: str, params: dict) -> str:
	import hashlib

	parts = []
	for key in sorted(params.keys()):
		if key == "sign":
			continue
		val = params[key]
		if isinstance(val, bool):
			val = "true" if val else "false"
		elif val is None:
			val = "null"
		else:
			val = json.dumps(val, ensure_ascii=False).strip('"')
		parts.append(f"{key}{val}")
	meta = "".join(parts) + sk
	md5 = hashlib.md5()
	md5.update(meta.encode("UTF-8"))
	return md5.hexdigest()


def load_token(environ: Optional[dict] = None) -> str:
	del environ
	env_config = load_env_config()
	token = env_config.get("token", "")
	if isinstance(token, str) and token.strip():
		return token.strip()
	legacy_token = _load_legacy_token()
	if legacy_token:
		env_config["token"] = legacy_token
		save_env_config(env_config)
	return legacy_token


def build_headers(token: str) -> dict:
	return {"Content-Type": "application/json"}


def build_preflight_result(environ: Optional[dict] = None) -> dict:
	environ = os.environ if environ is None else environ
	python_ok = sys.version_info >= (3, 6)
	token = load_token(environ)
	env_config = load_env_config()
	resident_city = str(env_config.get("resident_city", "")).strip()
	resident_city_present = bool(resident_city)
	env_config["env"]["python"] = python_ok
	env_config["token"] = token
	try:
		save_env_config(env_config)
	except OSError:
		pass
	result = {
		"python_ok": python_ok,
		"python_version": sys.version.split()[0],
		"platform": platform.platform(),
		"token_present": bool(token),
		"resident_city": resident_city,
		"resident_city_present": resident_city_present,
		"next_actions": [],
	}
	if not python_ok:
		result["next_actions"].append("install_python")
	if not token:
		result["next_actions"].append("setup_token")
	if not resident_city_present:
		result["next_actions"].append("setup_resident_city")
	if python_ok and token and resident_city_present:
		result["next_actions"].append("ready")
	return result


def persist_token(token: str, config_file: Optional[str] = None) -> dict:
	env_file = _resolve_env_file_path(config_file)
	env_config = load_env_config(env_file=env_file)
	env_config["token"] = token.strip()
	written_file = save_env_config(env_config, env_file=env_file)
	return {"saved": True, "config_file": written_file}


def delete_token(config_file: Optional[str] = None) -> dict:
	env_file = _resolve_env_file_path(config_file)
	env_config = load_env_config(env_file=env_file)
	had_token = bool(str(env_config.get("token", "")).strip())
	env_config["token"] = ""
	written_file = save_env_config(env_config, env_file=env_file)
	legacy_removed = False
	if os.path.isfile(TOKEN_CONFIG_FILE):
		os.remove(TOKEN_CONFIG_FILE)
		legacy_removed = True
	return {"deleted": had_token or legacy_removed, "config_file": written_file}


def _normalize_city_name(city_name: str) -> str:
	city = city_name.strip()
	if not city:
		return ""
	if city.endswith("市"):
		return city
	return city + "市"


def set_resident_city(city_name: str, env_file: Optional[str] = None) -> dict:
	normalized_city = _normalize_city_name(city_name)
	if not normalized_city:
		raise ValueError("resident city is required")
	env_config = load_env_config(env_file=env_file)
	env_config["resident_city"] = normalized_city
	written_file = save_env_config(env_config, env_file=env_file)
	return {
		"updated": True,
		"resident_city": normalized_city,
		"env_file": written_file,
	}


def get_resident_city(env_file: Optional[str] = None) -> dict:
	env_config = load_env_config(env_file=env_file)
	resident_city = str(env_config.get("resident_city", "")).strip()
	return {
		"resident_city": resident_city,
		"resident_city_present": bool(resident_city),
		"env_file": _resolve_env_file_path(env_file),
	}


def delete_state_file(state_file: Optional[str] = None) -> dict:
	state_file = state_file or STATE_FILE_PATH
	removed = False
	if os.path.isfile(state_file):
		os.remove(state_file)
		removed = True
	return {"deleted": removed, "state_file": state_file}


def read_text_file(path: str) -> str:
	try:
		with open(path, "r", encoding="utf-8") as handle:
			return handle.read()
	except OSError:
		return ""


def parse_markdown_table_value(markdown_text: str, row_name: str) -> str:
	for line in markdown_text.splitlines():
		stripped = line.strip()
		if not stripped.startswith("|"):
			continue
		cells = [cell.strip() for cell in stripped.strip("|").split("|")]
		if len(cells) >= 2 and cells[0] == row_name:
			return cells[1]
	return ""


def resolve_city_name(city_name: str) -> str:
	if city_name.strip():
		return city_name.strip()
	resident_city_result = get_resident_city()
	resident_city = resident_city_result.get("resident_city", "")
	if isinstance(resident_city, str):
		return resident_city
	return ""


def build_poi_search_payload(args: argparse.Namespace) -> dict:
	if args.scene not in (0, 1, 2):
		raise ValueError("scene must be one of 0, 1, 2")
	return {
		"keyword": args.keyword,
		"region": resolve_city_name(args.city_name),
		"policy": SCENE_TO_POLICY[args.scene],
		"pageIndex": args.page_index,
		"pageSize": args.page_size,
	}


def build_get_on_points_payload(lat: float, lng: float) -> dict:
	return {
		"lat": lat,
		"lng": lng,
		"maxCount": 1,
		"appId": "0",
		"appChannelId": "0",
		"geoPointAsFallback": True,
		"geoPointWhenNoAbsorb": True,
	}


def build_get_drop_off_point_payload(poi_id: str, lat: float, lng: float) -> dict:
	return {
		"appId": "0",
		"appChannelId": "0",
		"poiId": poi_id,
		"endLat": lat,
		"endLng": lng,
		"checkSubPoi": True,
	}


def parse_suggestion_data_list(body) -> list:
	if not isinstance(body, dict):
		return []
	data = body.get("data", {})
	if not isinstance(data, dict):
		return []
	inner_data = data.get("data", {})
	if not isinstance(inner_data, dict):
		return []
	data_list = inner_data.get("dataList", [])
	return data_list if isinstance(data_list, list) else []


def extract_on_points_from_response(body) -> list:
	if not isinstance(body, dict):
		return []
	data = body.get("data", {})
	if not isinstance(data, dict):
		return []
	inner_data = data.get("data", {})
	if not isinstance(inner_data, dict):
		return []
	points = inner_data.get("points", [])
	if not isinstance(points, list) or not points:
		return []
	first = points[0]
	if not isinstance(first, dict):
		return []
	loc = first.get("location", {})
	if not isinstance(loc, dict):
		return []
	return [{
		"point_name": first.get("title", ""),
		"point_latitude": loc.get("lat", ""),
		"point_longitude": loc.get("lng", ""),
	}]


def extract_drop_off_points_from_response(body) -> list:
	if not isinstance(body, dict):
		return []
	data = body.get("data", {})
	if not isinstance(data, dict):
		return []
	inner_data = data.get("data", {})
	if not isinstance(inner_data, dict):
		return []
	parking = inner_data.get("parkingSuggestions", {})
	if not isinstance(parking, dict):
		parking = {}
	points = parking.get("points", [])
	if isinstance(points, list) and points:
		result = []
		for pt in points:
			if not isinstance(pt, dict):
				continue
			sub_points = pt.get("subPoints", [])
			if isinstance(sub_points, list) and sub_points:
				for sp in sub_points:
					if not isinstance(sp, dict):
						continue
					sp_loc = sp.get("location", {})
					result.append({
						"point_name": pt.get("title", "") + "-" + sp.get("title", ""),
						"point_latitude": sp_loc.get("lat", "") if isinstance(sp_loc, dict) else "",
						"point_longitude": sp_loc.get("lng", "") if isinstance(sp_loc, dict) else "",
					})
			else:
				loc = pt.get("location", {})
				result.append({
					"point_name": pt.get("title", ""),
					"point_latitude": loc.get("lat", "") if isinstance(loc, dict) else "",
					"point_longitude": loc.get("lng", "") if isinstance(loc, dict) else "",
				})
		if result:
			return result
	# Fallback: data.dropOffPoints (NOT parkingSuggestions.dropOffPoints)
	drop_off = inner_data.get("dropOffPoints", {})
	if not isinstance(drop_off, dict):
		return []
	point_list = drop_off.get("pointList", [])
	if isinstance(point_list, list) and point_list:
		first = point_list[0]
		if isinstance(first, dict):
			return [{
				"point_name": first.get("title", ""),
				"point_latitude": first.get("lat", ""),
				"point_longitude": first.get("lng", ""),
			}]
	return []


def flatten_poi_search_result(result: dict, page_index: int) -> dict:
	body = result.get("body")
	if not isinstance(body, dict):
		return result
	data_list = parse_suggestion_data_list(body)
	items = []
	for item in data_list:
		if not isinstance(item, dict):
			continue
		loc = item.get("location", {})
		items.append({
			"name": item.get("title", ""),
			"address": item.get("address", ""),
			"longitude": loc.get("lng", "") if isinstance(loc, dict) else "",
			"latitude": loc.get("lat", "") if isinstance(loc, dict) else "",
			"poiid": item.get("id", ""),
			"citycode": str(item.get("adcode", "")),
			"point_name": "",
			"point_longitude": "",
			"point_latitude": "",
		})
	body["items"] = items
	body["page_index"] = page_index
	return result


def normalize_city_code(city_code) -> str:
	text = str(city_code).strip()
	if len(text) == 6 and text.isdigit():
		return text[:4] + "00"
	return text


def transform_estimate_price_result(result: dict) -> dict:
	if not isinstance(result, dict):
		return result
	body = result.get("body")
	if not isinstance(body, dict):
		return result
	raw_data = body.get("data")
	if not isinstance(raw_data, dict):
		raw_data = {}

	# Surface inner business errors (e.g. code 21003 "当前城市未开通打车功能")
	inner_code = raw_data.get("code")
	if isinstance(inner_code, int) and inner_code != 0:
		inner_msg = raw_data.get("message") or raw_data.get("msg") or "unknown error"
		result_copy = dict(result)
		result_copy["body"] = dict(body)
		result_copy["body"]["error"] = {"code": inner_code, "message": inner_msg}
		return result_copy

	data = raw_data
	nested_data = raw_data.get("data")
	if isinstance(nested_data, dict) and not any(key in raw_data for key in ("estimateKey", "product", "cityStatus", "cityMessage", "distance", "estimateTime")):
		data = nested_data

	filtered_product = []
	product_list = data.get("product")
	if isinstance(product_list, list):
		for item in product_list:
			if not isinstance(item, dict):
				continue
			rider_info = item.get("riderInfo")
			if not isinstance(rider_info, dict):
				continue
			ride_type = rider_info.get("rideType")
			if ride_type not in ALLOWED_RIDE_TYPES:
				continue

			price_estimate_list = []
			raw_estimates = item.get("priceEstimate")
			if isinstance(raw_estimates, list):
				for raw_estimate in raw_estimates:
					if not isinstance(raw_estimate, dict):
						continue
					sp = raw_estimate.get("sp")
					if not isinstance(sp, dict):
						sp = {}
					price_estimate_list.append({
						"defaultChecked": raw_estimate.get("defaultChecked"),
						"discountAmount": raw_estimate.get("discountAmount"),
						"discountPercentage": raw_estimate.get("discountPercentage"),
						"discountType": raw_estimate.get("discountType"),
						"estimatePrice": raw_estimate.get("estimatePrice"),
						"priceEstimateKey": raw_estimate.get("priceEstimateKey"),
						"sp": {
							"aliasName": sp.get("aliasName"),
							"code": sp.get("code"),
							"name": sp.get("name"),
						},
					})

			filtered_product.append({
				"riderInfo": {
					"rideType": rider_info.get("rideType"),
					"riderClassify": rider_info.get("riderClassify"),
					"riderDesc": rider_info.get("riderDesc"),
				},
				"priceEstimate": price_estimate_list,
			})

	result["body"] = {
		"code": body.get("code"),
		"message": body.get("message"),
		"data": {
			"cityMessage": data.get("cityMessage"),
			"cityStatus": data.get("cityStatus"),
			"distance": data.get("distance"),
			"estimateKey": data.get("estimateKey"),
			"estimateTime": data.get("estimateTime"),
			"product": filtered_product,
		},
	}
	return result


def transform_query_ongoing_result(result: dict) -> dict:
	if not isinstance(result, dict):
		return result
	body = result.get("body")
	if not isinstance(body, dict):
		return result
	data = extract_query_ongoing_data(body)
	if not isinstance(data, dict):
		return result

	# fields we care about
	fields = [
		"hasOnGoingOrder",
		"cancelFee",
		"departureTime",
		"endAddress",
		"endLat",
		"endLng",
		"isTaxi",
		"licensePlates",
		"mainTips",
		"minorTips",
		"orderId",
		"orderDesc",
		"orderSerialInfo",
		"orderServiceType",
		"serialFlag",
		"startName",
		"startAddress",
		"status",
		"statusStr",
		"supplierId",
		"supplierLogo",
		"supplierName",
		"tencentOrderStatus",
		"tips",
		"unpaidFee",
		"vehicleColor",
		"endName",
	]

	filtered = {}
	for k in fields:
		if k in data:
			filtered[k] = data.get(k)

	# Place filtered fields directly under body.data for compatibility with existing callers/tests
	result["body"] = {
		"code": body.get("code"),
		"message": body.get("message"),
		"data": filtered,
		"orderId": filtered.get("orderId", ""),
	}
	return result


def extract_query_ongoing_data(body: dict) -> Optional[dict]:
	if not isinstance(body, dict):
		return None
	raw_data = body.get("data")
	if not isinstance(raw_data, dict):
		return None
	inner_data = raw_data.get("data")
	if isinstance(inner_data, dict):
		return inner_data
	return raw_data


def _safe_extract_nested_detail(body: dict) -> Optional[dict]:
	if not isinstance(body, dict):
		return None
	data = body.get("data")
	if not isinstance(data, dict):
		return None
	inner_data = data.get("data")
	if isinstance(inner_data, dict):
		detail = inner_data.get("detail")
		if isinstance(detail, dict):
			return detail
		return inner_data
	return data


def _to_datetime_text(value) -> str:
	if isinstance(value, str):
		return value
	if isinstance(value, bool) or not isinstance(value, (int, float)):
		return ""
	if value <= 0:
		return ""
	import datetime

	try:
		return datetime.datetime.fromtimestamp(float(value) / 1000.0).strftime("%Y-%m-%d %H:%M:%S")
	except (OverflowError, OSError, ValueError):
		return ""


def _to_number_or_default(value, default=0):
	if isinstance(value, bool):
		return default
	if isinstance(value, (int, float)):
		return value
	return default


def transform_query_order_result(result: dict) -> dict:
	if not isinstance(result, dict):
		return result
	body = result.get("body")
	if not isinstance(body, dict):
		return result
	data = _safe_extract_nested_detail(body)
	if not isinstance(data, dict):
		return result

	# Keep compatibility with the existing output contract used by the workflow docs.
	if all(key in data for key in ("orderId", "status", "statusDesc", "driver", "vehicle", "position")):
		return result

	from_address = data.get("fromAddress") if isinstance(data.get("fromAddress"), dict) else {}
	to_address = data.get("toAddress") if isinstance(data.get("toAddress"), dict) else {}
	from_location = from_address.get("location") if isinstance(from_address.get("location"), dict) else {}
	to_location = to_address.get("location") if isinstance(to_address.get("location"), dict) else {}
	driver = data.get("driver") if isinstance(data.get("driver"), dict) else {}
	vehicle_info = driver.get("vehicleInfo") if isinstance(driver.get("vehicleInfo"), dict) else {}

	mapped = {
		"orderId": normalize_order_id(data.get("orderId")),
		"status": data.get("status"),
		"statusDesc": data.get("statusDesc") or data.get("orderDesc") or "",
		"acceptTime": _to_datetime_text(data.get("acceptTime") or data.get("arrivedTime")),
		"cancelTime": _to_datetime_text(data.get("canceledTime")),
		"driver": {
			"name": driver.get("name", ""),
			"phone": driver.get("phone", ""),
			"avatar": driver.get("avatar", ""),
		},
		"vehicle": {
			"brand": vehicle_info.get("brand", ""),
			"color": vehicle_info.get("color", ""),
			"model": vehicle_info.get("model", ""),
			"plate": vehicle_info.get("plate", ""),
			"picture": vehicle_info.get("picture", ""),
		},
		"position": {
			"startName": from_address.get("name", ""),
			"startAddress": from_address.get("address", ""),
			"startLat": from_location.get("lat", ""),
			"startLng": from_location.get("lng", ""),
			"endName": to_address.get("name", ""),
			"endAddress": to_address.get("address", ""),
			"endLat": to_location.get("lat", ""),
			"endLng": to_location.get("lng", ""),
		},
		"estimateDistance": _to_number_or_default(data.get("estimateDistance"), _to_number_or_default(data.get("journeyDistance"), _to_number_or_default(data.get("totalDistance"), 0))),
		"estimateDuration": _to_number_or_default(data.get("estimateDuration"), _to_number_or_default(data.get("journeyDuration"), _to_number_or_default(data.get("totalTime"), 0))),
		"estimatePrice": _to_number_or_default(data.get("estimatePrice"), 0),
		"distance": _to_number_or_default(data.get("distance"), 0),
		"cost": {
			"totalAmount": _to_number_or_default(data.get("totalAmount"), _to_number_or_default(data.get("payAmount"), 0)),
			"refundAmount": _to_number_or_default(data.get("refundAmount"), _to_number_or_default(data.get("actualRefundAmount"), 0)),
		},
	}

	result["body"] = {
		"code": body.get("code"),
		"message": body.get("message"),
		"data": mapped,
	}
	return result


def build_query_order_payload(order_id: str) -> dict:
	return {"orderId": order_id}


def build_query_driver_location_payload(order_id: str, state_file: Optional[str] = None) -> dict:
	timestamp_ms = generate_timestamp_ms()
	state = load_state_file(state_file=state_file)
	route_id = state.get("routeId", 0)
	traffic_id = state.get("trafficId", 0)
	if not isinstance(route_id, int):
		route_id = 0
	if not isinstance(traffic_id, int):
		traffic_id = 0
	return {
		"seqId": generate_seq_id(timestamp_ms),
		"timestamp": timestamp_ms,
		"wxAppId": "wx65cc950f42e8fff1",
		"orderId": order_id,
		"routeId": route_id,
		"trafficId": traffic_id,
	}


def build_query_ongoing_order_payload(args: argparse.Namespace) -> dict:
	del args
	return {}


def transform_query_driver_location_result(result: dict) -> dict:
	if not isinstance(result, dict):
		return result
	body = result.get("body")
	if not isinstance(body, dict):
		return result

	data_wrapper = body.get("data", {})
	if not isinstance(data_wrapper, dict):
		data_wrapper = {}

	res_data = data_wrapper.get("resData", {})
	if not isinstance(res_data, dict):
		res_data = {}

	order_info = res_data.get("orderInfo", {})
	if not isinstance(order_info, dict):
		order_info = {}

	driver_display = res_data.get("driverPassengerDisplay", {})
	if not isinstance(driver_display, dict):
		driver_display = {}

	location_info = driver_display.get("driverLocationInfo", {})
	if not isinstance(location_info, dict):
		location_info = {}

	order_status = order_info.get("orderStatus")
	eta = location_info.get("eta")
	eda = location_info.get("eda")

	# Check if eta and eda are available
	if eta in (None, "") or eda in (None, ""):
		# If not available, check orderStatus
		if order_status not in (2, 3, 4):
			# Not in a state that supports driver location query
			result["body"] = {
				"code": body.get("code", -1),
				"message": body.get("message", "无法查询司机位置"),
				"data": {
					"orderStatus": order_status,
					"eta": None,
					"eda": None,
					"driverLocation": None,
				},
			}
			return result
		# If status is 2, 3, or 4 but no location info, return empty location
		location = ""
		result["body"] = {
			"code": body.get("code", 0),
			"message": body.get("message", "司机位置暂无"),
			"data": {
				"orderStatus": order_status,
				"eta": None,
				"eda": None,
				"driverLocation": None,
			},
		}
		return result

	# Extract location components
	location = location_info.get("location", "")
	loc_parts = location.split(",") if location else []
	try:
		location_lat = float(loc_parts[0]) if len(loc_parts) > 0 and loc_parts[0] else None
		location_lng = float(loc_parts[1]) if len(loc_parts) > 1 and loc_parts[1] else None
	except (ValueError, IndexError):
		location_lat = None
		location_lng = None

	result["body"] = {
		"code": body.get("code", 0),
		"message": body.get("message", "success"),
		"data": {
			"orderStatus": order_status,
			"eta": eta,
			"eda": eda,
			"driverLocation": {
				"location": location,
				"latitude": location_lat,
				"longitude": location_lng,
				"direction": location_info.get("direction"),
				"locationTime": location_info.get("locationTime"),
			},
		},
	}
	return result


def build_cancel_order_payload(order_id: str, confirm: bool, reason: str = "") -> dict:
	payload = {"orderId": order_id, "confirm": confirm}
	if reason.strip():
		payload["reason"] = reason.strip()
	return payload


def check_token(environ: dict, stderr) -> str:
	token = load_token(environ)
	if not token:
		stderr.write("Token is not configured. Run: save-token <token>\n")
	return token


def get_ongoing_order_id(environ: dict, stdout, stderr) -> Optional[str]:
	"""
	Internal helper: call query-ongoing-order to get the current order ID.
	Returns order ID if exists, None otherwise.
	"""
	token = load_token(environ)
	if not token:
		stderr.write("Token is not configured. Run: save-token <token>\n")
		return None
	
	payload = {}
	base_url = DEFAULT_API_BASE.strip()
	if not base_url:
		stderr.write("API base URL is not configured\n")
		return None
	
	headers = build_headers(token)
	try:
		result = post_request(
			base_url,
			DEFAULT_QUERY_ONGOING_ORDER_PATH,
			headers,
			payload,
			token=token,
			timeout_seconds=DEFAULT_HTTP_TIMEOUT_SECONDS,
		)
		
	except (urllib.error.HTTPError, urllib.error.URLError) as exc:
		stderr.write(f"Failed to query ongoing order: {exc}\n")
		return None

	body = result.get("body")
	if is_invalid_token_error(body):
		stderr.write("Token is invalid or expired\n")
		return None

	data = extract_query_ongoing_data(body)
	if not isinstance(data, dict):
		stderr.write("No ongoing order found\n")
		return None

	order_id = data.get("orderId")
	has_ongoing_order = data.get("hasOnGoingOrder")
	if has_ongoing_order is False:
		stderr.write("No ongoing order found\n")
		return None

	if order_id and isinstance(order_id, str) and order_id != "null" and order_id.strip() != "":
		return order_id.strip()

	stderr.write("No ongoing order found\n")
	return None


def post_cancel_order_payload(environ: dict, payload: dict, stderr) -> Tuple[Optional[dict], Optional[int]]:
	token = load_token(environ)
	if not token:
		stderr.write("Token is not configured. Run: save-token <token>\n")
		return None, 1

	base_url = DEFAULT_API_BASE.strip()
	if not base_url:
		stderr.write("API base URL is not configured\n")
		return None, 2

	headers = build_headers(token)
	try:
		result = post_request(
			base_url,
			DEFAULT_CANCEL_ORDER_PATH,
			headers,
			payload,
			token=token,
			timeout_seconds=DEFAULT_HTTP_TIMEOUT_SECONDS,
		)
	except urllib.error.HTTPError as exc:
		error_body = exc.read().decode("utf-8", errors="replace")
		try:
			error_body_json = json.loads(error_body)
		except json.JSONDecodeError:
			error_body_json = None
		if is_invalid_token_error(error_body_json):
			write_json(
				stderr,
				{
					"mode": "error",
					"status": exc.code,
					"body": error_body,
				},
			)
			return None, 1
		write_json(
			stderr,
			{
				"mode": "error",
				"status": exc.code,
				"body": error_body,
			},
		)
		return None, 3
	except urllib.error.URLError as exc:
		write_json(
			stderr,
			{
				"mode": "error",
				"reason": str(exc),
				"hint": "Request timed out after 60s",
			},
		)
		return None, 4

	body = result.get("body") if isinstance(result, dict) else None
	if is_invalid_token_error(body):
		write_json(
			stderr,
			{
				"mode": "error",
				"reason": "token is missing or invalid",
				"body": body,
			},
		)
		return None, 1
	return result, None


def build_parser() -> argparse.ArgumentParser:
	parser = argparse.ArgumentParser(description="Tencent travel ride-hailing skill CLI")
	subparsers = parser.add_subparsers(dest="command")

	preflight_parser = subparsers.add_parser("preflight", help="Check Python runtime and token availability")
	preflight_parser.set_defaults(handler=handle_preflight)

	save_token_parser = subparsers.add_parser("save-token", help="Persist token into config file")
	save_token_parser.add_argument("token", help="Token value to persist")
	save_token_parser.add_argument("--config-file", default=None, help="Explicit config file path (default: ~/.config/tms-takecar/env.json)")
	save_token_parser.set_defaults(handler=handle_save_token)

	delete_token_parser = subparsers.add_parser("delete-token", help="Remove saved token from env config")
	delete_token_parser.add_argument("--config-file", default=None, help="Explicit config file path")
	delete_token_parser.set_defaults(handler=handle_delete_token)

	set_resident_city_parser = subparsers.add_parser("set-resident-city", help="Set or update resident city in env config")
	set_resident_city_parser.add_argument("city_name", help="Resident city full name")
	set_resident_city_parser.add_argument("--env-file", dest="env_file", default=None, help="Explicit env file path (default: ~/.config/tms-takecar/env.json)")
	set_resident_city_parser.add_argument("--memory-file", dest="env_file", default=None, help=argparse.SUPPRESS)
	set_resident_city_parser.set_defaults(handler=handle_set_resident_city)

	get_resident_city_parser = subparsers.add_parser("get-resident-city", help="Get resident city from env config")
	get_resident_city_parser.add_argument("--env-file", dest="env_file", default=None, help="Explicit env file path (default: ~/.config/tms-takecar/env.json)")
	get_resident_city_parser.add_argument("--memory-file", dest="env_file", default=None, help=argparse.SUPPRESS)
	get_resident_city_parser.set_defaults(handler=handle_get_resident_city)

	delete_state_parser = subparsers.add_parser("delete-state", help="Remove state.json from config directory")
	delete_state_parser.add_argument("--state-file", default=None, help="Explicit state file path (default: ~/.config/tms-takecar/state.json)")
	delete_state_parser.set_defaults(handler=handle_delete_state)

	addr_keys_parser = subparsers.add_parser("addr-keys", help="Return all keys from addr.json")
	addr_keys_parser.add_argument("--addr-file", default=None, help="Explicit addr file path (default: ~/.config/tms-takecar/addr.json)")
	addr_keys_parser.set_defaults(handler=handle_addr_keys)

	addr_get_value_parser = subparsers.add_parser("addr-get-value", help="Get one value from addr.json by key")
	addr_get_value_parser.add_argument("key", help="Address alias key")
	addr_get_value_parser.add_argument("--addr-file", default=None, help="Explicit addr file path (default: ~/.config/tms-takecar/addr.json)")
	addr_get_value_parser.set_defaults(handler=handle_addr_get_value)

	addr_upsert_value_parser = subparsers.add_parser("addr-upsert-value", help="Create or update one value in addr.json by key")
	addr_upsert_value_parser.add_argument("key", help="Address alias key")
	addr_upsert_value_parser.add_argument("value_json", help="JSON object to store for the given key")
	addr_upsert_value_parser.add_argument("--addr-file", default=None, help="Explicit addr file path (default: ~/.config/tms-takecar/addr.json)")
	addr_upsert_value_parser.set_defaults(handler=handle_addr_upsert_value)

	addr_sync_state_parser = subparsers.add_parser("addr-sync-to-state", help="Sync one addr.json value into pickup/dropoff in state.json by key and scene")
	addr_sync_state_parser.add_argument("key", help="Address alias key")
	addr_sync_state_parser.add_argument("--scene", type=int, choices=[1, 2], required=True, help="1:pickup, 2:dropoff")
	addr_sync_state_parser.add_argument("--addr-file", default=None, help="Explicit addr file path (default: ~/.config/tms-takecar/addr.json)")
	addr_sync_state_parser.add_argument("--state-file", default=None, help="Explicit state file path (default: ~/.config/tms-takecar/state.json)")
	addr_sync_state_parser.set_defaults(handler=handle_addr_sync_to_state)

	short_cut_keys_parser = subparsers.add_parser("short-cut-keys", help="Return all keys from short-cut.json")
	short_cut_keys_parser.add_argument("--short-cut-file", default=None, help="Explicit short-cut file path (default: ~/.config/tms-takecar/short-cut.json)")
	short_cut_keys_parser.set_defaults(handler=handle_short_cut_keys)

	short_cut_get_value_parser = subparsers.add_parser("short-cut-get-value", help="Get one value from short-cut.json by key")
	short_cut_get_value_parser.add_argument("key", help="Normalized shortcut scene key")
	short_cut_get_value_parser.add_argument("--short-cut-file", default=None, help="Explicit short-cut file path (default: ~/.config/tms-takecar/short-cut.json)")
	short_cut_get_value_parser.set_defaults(handler=handle_short_cut_get_value)

	short_cut_upsert_value_parser = subparsers.add_parser("short-cut-upsert-value", help="Create or update one value in short-cut.json by key")
	short_cut_upsert_value_parser.add_argument("key", help="Normalized shortcut scene key")
	short_cut_upsert_value_parser.add_argument("value_json", help="JSON object to store for the given key")
	short_cut_upsert_value_parser.add_argument("--short-cut-file", default=None, help="Explicit short-cut file path (default: ~/.config/tms-takecar/short-cut.json)")
	short_cut_upsert_value_parser.set_defaults(handler=handle_short_cut_upsert_value)

	poi_search_parser = subparsers.add_parser("poi-search", help="Search POIs and optional on/off points by keyword")
	poi_search_parser.add_argument("--keyword", required=True, help="POI search keyword")
	poi_search_parser.add_argument("--city-name", default="", help="City name")
	poi_search_parser.add_argument("--page-size", type=int, default=3, help="Page size")
	poi_search_parser.add_argument("--page-index", type=int, default=1, help="Page index")
	poi_search_parser.add_argument("--scene", type=int, choices=[0, 1, 2], default=0, help="0:poi, 1:pickup, 2:dropoff")
	poi_search_parser.add_argument("--state-file", default=None, help="Explicit state file path (default: ~/.config/tms-takecar/state.json)")
	poi_search_parser.set_defaults(handler=handle_poi_search)

	static_map_url_parser = subparsers.add_parser("build-static-map-url", help="Build a Tencent static map URL from marker coordinates")
	static_map_url_parser.add_argument("--markers-json", required=True, help='JSON array, e.g. [{"latitude":39.9,"longitude":116.4,"marker":"起"}]')
	static_map_url_parser.set_defaults(handler=handle_build_static_map_url)

	estimate_price_parser = subparsers.add_parser("estimate-price", help="Estimate ride price from state.json")
	estimate_price_parser.add_argument("--state-file", default=None, help="Explicit state file path (default: ~/.config/tms-takecar/state.json)")
	estimate_price_parser.set_defaults(handler=handle_estimate_price)

	select_poi_parser = subparsers.add_parser("select-poi", help="Select one POI candidate by scene and poiid")
	select_poi_parser.add_argument("--poiid", required=True, help="POI ID selected by user")
	select_poi_parser.add_argument("--scene", type=int, choices=[1, 2], required=True, help="1:pickup, 2:dropoff")
	select_poi_parser.add_argument("--state-file", default=None, help="Explicit state file path (default: ~/.config/tms-takecar/state.json)")
	select_poi_parser.set_defaults(handler=handle_select_poi)

	create_order_parser = subparsers.add_parser("create-order", help="Create a ride order with risk verification from state.json")
	create_order_parser.add_argument("--state-file", default=None, help="Explicit state file path (default: ~/.config/tms-takecar/state.json)")
	create_order_parser.add_argument("--price-estimate-keys", default=None, help="JSON array of selected priceEstimateKeys; updates estimate.products[].userSelect before ordering")
	create_order_parser.add_argument("--user-prefer-labels", default=None, help="JSON array of userPreferLabel ints; updates estimate.userPreferLabels before ordering")
	create_order_parser.set_defaults(handler=handle_create_order)

	query_ongoing_order_parser = subparsers.add_parser("query-ongoing-order", help="Query whether current user has an ongoing order")
	query_ongoing_order_parser.set_defaults(handler=handle_query_ongoing_order)

	cancel_order_parser = subparsers.add_parser("cancel-order", help="Cancel an ongoing ride order")
	cancel_order_parser.add_argument("--confirm", action="store_true", default=False, help="Confirm cancellation after fee check")
	cancel_order_parser.add_argument("--reason", default="", help="Cancellation reason")
	cancel_order_parser.set_defaults(handler=handle_cancel_order)

	query_order_parser = subparsers.add_parser("query-order", help="Query ride order status, driver and vehicle info")
	query_order_parser.set_defaults(handler=handle_query_order)

	query_driver_location_parser = subparsers.add_parser("query-driver-location", help="Query real-time driver location for an order")
	query_driver_location_parser.set_defaults(handler=handle_query_driver_location)

	return parser


def write_json(stream, payload: dict) -> None:
	stream.write(json.dumps(payload, ensure_ascii=False, indent=2))
	stream.write("\n")


def handle_preflight(args: argparse.Namespace, environ: dict, stdout, stderr) -> int:
	del args, stderr
	result = build_preflight_result(environ)
	write_json(stdout, result)
	if result.get("next_actions") == ["ready"]:
		return 0
	return 1


def handle_save_token(args: argparse.Namespace, environ: dict, stdout, stderr) -> int:
	del environ, stderr
	write_json(stdout, persist_token(args.token, config_file=args.config_file))
	return 0


def handle_delete_token(args: argparse.Namespace, environ: dict, stdout, stderr) -> int:
	del environ, stderr
	write_json(stdout, delete_token(config_file=args.config_file))
	return 0


def handle_set_resident_city(args: argparse.Namespace, environ: dict, stdout, stderr) -> int:
	del environ
	try:
		payload = set_resident_city(args.city_name, env_file=args.env_file)
	except ValueError as exc:
		stderr.write(f"{exc}\n")
		return 2
	write_json(stdout, payload)
	return 0


def handle_get_resident_city(args: argparse.Namespace, environ: dict, stdout, stderr) -> int:
	del environ, stderr
	write_json(stdout, get_resident_city(env_file=args.env_file))
	return 0


def handle_delete_state(args: argparse.Namespace, environ: dict, stdout, stderr) -> int:
	del environ, stderr
	write_json(stdout, delete_state_file(state_file=args.state_file))
	return 0


def handle_addr_keys(args: argparse.Namespace, environ: dict, stdout, stderr) -> int:
	del environ, stderr
	write_json(stdout, get_addr_keys(addr_file=args.addr_file))
	return 0


def handle_addr_get_value(args: argparse.Namespace, environ: dict, stdout, stderr) -> int:
	del environ
	try:
		payload = get_addr_value_by_key(args.key, addr_file=args.addr_file)
	except ValueError as exc:
		stderr.write(f"{exc}\n")
		return 2
	write_json(stdout, payload)
	return 0


def handle_addr_upsert_value(args: argparse.Namespace, environ: dict, stdout, stderr) -> int:
	del environ
	try:
		value = _parse_json_object_arg(args.value_json, "addr value")
		payload = upsert_addr_value(args.key, value, addr_file=args.addr_file)
	except ValueError as exc:
		stderr.write(f"{exc}\n")
		return 2
	write_json(stdout, payload)
	return 0


def handle_addr_sync_to_state(args: argparse.Namespace, environ: dict, stdout, stderr) -> int:
	del environ
	try:
		payload = sync_addr_value_to_state(
			args.key,
			scene=args.scene,
			addr_file=args.addr_file,
			state_file=args.state_file,
		)
	except ValueError as exc:
		stderr.write(f"{exc}\n")
		return 2
	write_json(stdout, payload)
	return 0


def handle_short_cut_keys(args: argparse.Namespace, environ: dict, stdout, stderr) -> int:
	del environ, stderr
	write_json(stdout, get_short_cut_keys(short_cut_file=args.short_cut_file))
	return 0


def handle_short_cut_get_value(args: argparse.Namespace, environ: dict, stdout, stderr) -> int:
	del environ
	try:
		payload = get_short_cut_value_by_key(args.key, short_cut_file=args.short_cut_file)
	except ValueError as exc:
		stderr.write(f"{exc}\n")
		return 2
	write_json(stdout, payload)
	return 0


def handle_short_cut_upsert_value(args: argparse.Namespace, environ: dict, stdout, stderr) -> int:
	del environ
	try:
		value = _parse_json_object_arg(args.value_json, "short-cut value")
		payload = upsert_short_cut_value(args.key, value, short_cut_file=args.short_cut_file)
	except ValueError as exc:
		stderr.write(f"{exc}\n")
		return 2
	write_json(stdout, payload)
	return 0


def run_poi_search_api(environ, stdout, stderr, payload, scene, page_index, state_file=None, urlopen_func=urllib.request.urlopen):
	token = load_token(environ)
	base_url = DEFAULT_API_BASE.strip()
	if not base_url:
		write_json(stdout, {"mode": "blocked", "reason": "DEFAULT_API_BASE is not configured", "payload": payload})
		return 2

	headers = build_headers(token)

	# Step 1: Base suggestion search
	try:
		base_result = post_request(
			base_url,
			DEFAULT_POI_SUGGESTION_PATH,
			headers,
			payload,
			token=token,
			urlopen_func=urlopen_func,
			timeout_seconds=DEFAULT_HTTP_TIMEOUT_SECONDS,
		)
	except urllib.error.HTTPError as exc:
		error_body = exc.read().decode("utf-8", errors="replace")
		write_json(stderr, {"mode": "error", "status": exc.code, "body": error_body})
		return 3
	except urllib.error.URLError as exc:
		write_json(
			stderr,
			{
				"mode": "error",
				"reason": str(exc),
				"hint": "Request timed out after 60s",
			},
		)
		return 4

	base_body = base_result.get("body")
	if is_invalid_token_error(base_body):
		write_json(stderr, {"mode": "error", "reason": "token is missing or invalid", "body": base_body})
		return 1

	data_list = parse_suggestion_data_list(base_body)

	if scene == 0:
		result = flatten_poi_search_result(base_result, page_index)
		write_json(stdout, {"mode": "searched", "result": result})
		return 0

	# Step 2: For each base item, call secondary API
	all_items = []
	for data_item in data_list:
		if not isinstance(data_item, dict):
			continue
		loc = data_item.get("location", {})
		lat = loc.get("lat", 0) if isinstance(loc, dict) else 0
		lng = loc.get("lng", 0) if isinstance(loc, dict) else 0
		poi_id = str(data_item.get("id", ""))
		base_info = {
			"name": data_item.get("title", ""),
			"address": data_item.get("address", ""),
			"longitude": lng,
			"latitude": lat,
			"poiid": poi_id,
			"citycode": str(data_item.get("adcode", "")),
		}

		if scene == 1:
			secondary_payload = build_get_on_points_payload(lat, lng)
			secondary_path = DEFAULT_GET_ON_POINTS_PATH
		else:
			secondary_payload = build_get_drop_off_point_payload(poi_id, lat, lng)
			secondary_path = DEFAULT_GET_DROP_OFF_POINT_PATH

		try:
			secondary_result = post_request(
				base_url,
				secondary_path,
				headers,
				secondary_payload,
				token=token,
				urlopen_func=urlopen_func,
				timeout_seconds=DEFAULT_HTTP_TIMEOUT_SECONDS,
			)
		except (urllib.error.HTTPError, urllib.error.URLError):
			all_items.append({**base_info, "point_name": "", "point_longitude": "", "point_latitude": ""})
			continue

		secondary_body = secondary_result.get("body")

		if scene == 1:
			points = extract_on_points_from_response(secondary_body)
		else:
			points = extract_drop_off_points_from_response(secondary_body)

		if points:
			for pt in points:
				all_items.append({**base_info, **pt})
		else:
			all_items.append({**base_info, "point_name": "", "point_longitude": "", "point_latitude": ""})

	output_payload = {
		"mode": "searched",
		"result": {
			"status": base_result.get("status", 200),
			"body": {"items": all_items, "page_index": page_index},
		},
	}
	written_state_file = update_state_from_poi_search(scene=scene, items=all_items, state_file=state_file)
	if written_state_file:
		output_payload["state"] = {"state_file": written_state_file, "updated": True}
	write_json(stdout, output_payload)
	return 0


def handle_poi_search(args: argparse.Namespace, environ: dict, stdout, stderr) -> int:
	if not check_token(environ, stderr):
		return 1
	try:
		payload = build_poi_search_payload(args)
	except ValueError as exc:
		stderr.write(f"{exc}\n")
		return 2
	return run_poi_search_api(
		environ=environ,
		stdout=stdout,
		stderr=stderr,
		payload=payload,
		scene=args.scene,
		page_index=args.page_index,
		state_file=args.state_file,
		urlopen_func=urllib.request.urlopen,
	)


def handle_build_static_map_url(args: argparse.Namespace, environ: dict, stdout, stderr) -> int:
	try:
		markers = _parse_static_map_markers_json(args.markers_json)
		token = load_token(environ)
		if not token:
			stderr.write("Token is not configured. Run: save-token <token>\n")
			return 1
		url = build_static_map_url(
			markers=markers,
			token=token,
		)
	except ValueError as exc:
		stderr.write(f"{exc}\n")
		return 2
	write_json(stdout, {"url": url})
	return 0


def handle_select_poi(args: argparse.Namespace, environ: dict, stdout, stderr) -> int:
	del environ
	try:
		result = apply_select_poi(poiid=args.poiid, scene=args.scene, state_file=args.state_file)
	except ValueError as exc:
		stderr.write(f"{exc}\n")
		return 2
	write_json(stdout, result)
	return 0


def handle_estimate_price(args: argparse.Namespace, environ: dict, stdout, stderr) -> int:
	if not check_token(environ, stderr):
		return 1
	state = load_state_file(state_file=args.state_file)
	try:
		payload = build_estimate_price_payload_from_state(state)
		prefer_labels = _validate_user_prefer_labels(state.get("userPreferLabels", []))
	except ValueError as exc:
		stderr.write(f"{exc}\n")
		return 2

	def _write_json_with_state(stream, api_payload: dict) -> None:
		if stream is stdout and isinstance(api_payload, dict) and api_payload.get("mode") == "estimated":
			result_obj = api_payload.get("result")
			state_file = update_state_from_estimate_result(result_obj, user_prefer_labels=prefer_labels, state_file=args.state_file)
			if state_file:
				api_payload = dict(api_payload)
				api_payload["state"] = {"state_file": state_file, "updated": True}
		write_json(stream, api_payload)

	return run_json_api_command(
		environ=environ,
		stdout=stdout,
		stderr=stderr,
		payload=payload,
		api_path=DEFAULT_ESTIMATE_PRICE_PATH,
		success_mode="estimated",
		load_token_func=load_token,
		build_headers_func=build_headers,
		write_json_func=_write_json_with_state,
		default_api_base=DEFAULT_API_BASE,
		result_transform=transform_estimate_price_result,
		urlopen_func=urllib.request.urlopen,
	)


def handle_create_order(args: argparse.Namespace, environ: dict, stdout, stderr) -> int:
	if not check_token(environ, stderr):
		return 1
	state = load_state_file(state_file=args.state_file)
	state_modified = False
	if getattr(args, "price_estimate_keys", None):
		try:
			price_estimate_keys = _parse_price_estimate_keys_json(args.price_estimate_keys)
		except ValueError as exc:
			stderr.write(f"{exc}\n")
			return 2
		estimate = state.get("estimate")
		if isinstance(estimate, dict):
			products = estimate.get("products")
			if isinstance(products, list):
				key_set = set(price_estimate_keys)
				for item in products:
					if not isinstance(item, dict):
						continue
					key = item.get("priceEstimateKey")
					item["userSelect"] = 1 if (isinstance(key, str) and key in key_set) else 0
				state_modified = True
	if getattr(args, "user_prefer_labels", None):
		try:
			prefer_labels = _parse_prefer_labels_json(args.user_prefer_labels)
		except ValueError as exc:
			stderr.write(f"{exc}\n")
			return 2
		estimate = state.get("estimate")
		if isinstance(estimate, dict):
			estimate["userPreferLabels"] = prefer_labels
			state_modified = True
	if state_modified:
		save_state_file(state, state_file=args.state_file)
	try:
		payload = build_create_order_payload_from_state(state)
	except ValueError as exc:
		stderr.write(f"{exc}\n")
		return 2

	def _write_json_with_state(stream, api_payload: dict) -> None:
		if stream is stdout and isinstance(api_payload, dict) and api_payload.get("mode") == "ordered":
			result_obj = api_payload.get("result")
			state_file = update_state_from_create_order_result(result_obj, state_file=args.state_file)
			if state_file:
				api_payload = dict(api_payload)
				api_payload["state"] = {"state_file": state_file, "updated": True}
		write_json(stream, api_payload)

	return run_json_api_command(
		environ=environ,
		stdout=stdout,
		stderr=stderr,
		payload=payload,
		api_path=DEFAULT_CREATE_ORDER_PATH,
		success_mode="ordered",
		load_token_func=load_token,
		build_headers_func=build_headers,
		write_json_func=_write_json_with_state,
		default_api_base=DEFAULT_API_BASE,
		result_transform=transform_create_order_result,
		urlopen_func=urllib.request.urlopen,
	)


def handle_query_ongoing_order(args: argparse.Namespace, environ: dict, stdout, stderr) -> int:
	if not check_token(environ, stderr):
		return 1
	payload = build_query_ongoing_order_payload(args)
	return run_json_api_command(
		environ=environ,
		stdout=stdout,
		stderr=stderr,
		payload=payload,
		api_path=DEFAULT_QUERY_ONGOING_ORDER_PATH,
		success_mode="queried",
		load_token_func=load_token,
		build_headers_func=build_headers,
		write_json_func=write_json,
		result_transform=transform_query_ongoing_result,
		default_api_base=DEFAULT_API_BASE,
		urlopen_func=urllib.request.urlopen,
	)


def handle_cancel_order(args: argparse.Namespace, environ: dict, stdout, stderr) -> int:
	if not check_token(environ, stderr):
		return 1

	order_id = get_ongoing_order_id(environ, stdout, stderr)
	if not order_id:
		return 5

	if not args.confirm:
		fee_payload = build_cancel_order_payload(order_id, False, args.reason)
		fee_result, error_code = post_cancel_order_payload(environ, fee_payload, stderr)
		if error_code is not None:
			return error_code

		fee_body = fee_result.get("body") if isinstance(fee_result, dict) else None
		fee_data = fee_body.get("data") if isinstance(fee_body, dict) else None
		if not isinstance(fee_data, dict):
			write_json(
				stderr,
				{
					"mode": "error",
					"reason": "cancel fee response missing data",
					"body": fee_body,
				},
			)
			return 3

		waiver_fee = fee_data.get("waiverFee")
		amount = fee_data.get("amount", 0)
		if waiver_fee is False:
			amount_yuan = round((amount or 0) / 100, 2)
			write_json(
				stdout,
				{
					"mode": "cancel_fee_required",
					"amount": amount,
					"amount_yuan": amount_yuan,
					"message": f"取消订单需支付 {amount_yuan:.2f} 元取消费，确认取消请传入 --confirm",
					"result": fee_result,
				},
			)
			return 6
	
	payload = build_cancel_order_payload(order_id, True, args.reason)
	return run_json_api_command(
		environ=environ,
		stdout=stdout,
		stderr=stderr,
		payload=payload,
		api_path=DEFAULT_CANCEL_ORDER_PATH,
		success_mode="cancelled",
		load_token_func=load_token,
		build_headers_func=build_headers,
		write_json_func=write_json,
		default_api_base=DEFAULT_API_BASE,
		urlopen_func=urllib.request.urlopen,
	)


def handle_query_order(args: argparse.Namespace, environ: dict, stdout, stderr) -> int:
	if not check_token(environ, stderr):
		return 1

	order_id = get_ongoing_order_id(environ, stdout, stderr)
	if not order_id:
		return 5

	payload = build_query_order_payload(order_id)
	return run_json_api_command(
		environ=environ,
		stdout=stdout,
		stderr=stderr,
		payload=payload,
		api_path=DEFAULT_QUERY_ORDER_PATH,
		success_mode="queried",
		load_token_func=load_token,
		build_headers_func=build_headers,
		write_json_func=write_json,
		result_transform=transform_query_order_result,
		default_api_base=DEFAULT_API_BASE,
		urlopen_func=urllib.request.urlopen,
	)


def handle_query_driver_location(args: argparse.Namespace, environ: dict, stdout, stderr) -> int:
	if not check_token(environ, stderr):
		return 1

	order_id = get_ongoing_order_id(environ, stdout, stderr)
	if not order_id:
		return 5

	payload = build_query_driver_location_payload(order_id)
	return run_json_api_command(
		environ=environ,
		stdout=stdout,
		stderr=stderr,
		payload=payload,
		api_path=DEFAULT_QUERY_DRIVER_LOCATION_PATH,
		success_mode="queried",
		load_token_func=load_token,
		build_headers_func=build_headers,
		write_json_func=write_json,
		result_transform=transform_query_driver_location_result,
		default_api_base=DEFAULT_API_BASE,
		urlopen_func=urllib.request.urlopen,
	)


def main(argv: Optional[List[str]] = None, environ: Optional[dict] = None, stdout=None, stderr=None) -> int:
	environ = os.environ if environ is None else environ
	stdout = sys.stdout if stdout is None else stdout
	stderr = sys.stderr if stderr is None else stderr
	parser = build_parser()
	args = parser.parse_args(argv)
	if not hasattr(args, "handler"):
		parser.print_usage(stderr)
		stderr.write("tms_takecar.py: error: the following arguments are required: command\n")
		return 2
	return args.handler(args, environ, stdout, stderr)


if __name__ == "__main__":
	raise SystemExit(main())
