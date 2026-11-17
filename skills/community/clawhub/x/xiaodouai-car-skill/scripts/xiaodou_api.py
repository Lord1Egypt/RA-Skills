#!/usr/bin/env python3
"""Xiaodou car rental API CLI.

Usage follows AWS CLI conventions:

    python3 scripts/xiaodou_api.py search-vehicle-v3 \
        --endpoint-url https://interface.xiaodouzuche.com/xiaodou/ \
        --user-id 2109548212126851074
"""

import argparse
import hashlib
import json
import sys
import time
from collections import defaultdict
import requests
import datetime


DEFAULT_ENDPOINT_URL = "https://interface.xiaodouzuche.com/xiaodou/"
DEFAULT_APP_KEY = "xzcxzfb"
DEFAULT_ORDER_CHANNEL = 3
DEFAULT_CHANNEL_ID = 11


def json_text(value):
    try:
        return json.loads(value)
    except json.JSONDecodeError as exc:
        raise argparse.ArgumentTypeError("expected valid JSON: %s" % exc.msg)


def json_object(value):
    value = json_text(value)
    if not isinstance(value, dict):
        raise argparse.ArgumentTypeError("expected a JSON object")
    return value


def make_sign(secret, timestamp):
    return hashlib.md5(("%s%s" % (secret, timestamp)).encode("utf-8")).hexdigest()


def request_json(url, payload, timeout, verify_ssl):
    #print(f"request param {payload}")
    response = requests.post(
        url,
        json=payload,
        headers={"Content-Type": "application/json;charset=UTF-8"},
        timeout=timeout,
        verify=verify_ssl,
    )
    response.raise_for_status()
    try:
        return response.json()
    except ValueError:
        return {"raw": response.text}


def clean(value):
    return {key: item for key, item in value.items() if item is not None}


def authentication(args):
    timestamp = int(time.time() * 1000)
    return {
        "appKey": args.app_key,
        "timeStamp": timestamp,
        "sign": args.sign or make_sign(args.sign_secret, timestamp),
        "orderChannel": args.order_channel,
        "channelId": args.channel_id,
        "xiaodouChannel": args.xiaodou_channel,
    }


def select_json_path(value, path):
    """Select a nested value using dot notation, with integers for list indexes."""
    if not path:
        return value

    current = value
    for part in path.split(r"."):
        if isinstance(current, dict) and part in current:
            current = current[part]
            continue
        if isinstance(current, list):
            try:
                index = int(part)
            except ValueError:
                raise KeyError(part)
            if -len(current) <= index < len(current):
                current = current[index]
                continue
        raise KeyError(part)
    return str(current).strip()

def location_third_store(args, prefix):
    payload = {
        "name": getattr(args, "%s_name" % prefix),
        "code": getattr(args, "%s_code" % prefix),
        "addressTypeName": getattr(args, "%s_address_type_name" % prefix),
        "closeTime": getattr(args, "%s_close_time" % prefix),
        "openTime": getattr(args, "%s_open_time" % prefix),
        "phone": getattr(args, "%s_phone" % prefix),
        "name": getattr(args, "%s_name" % prefix),
        "address": getattr(args, "%s_address" % prefix),
        "city": getattr(args, "%s_city" % prefix),
        "cityCode": getattr(args, "%s_city_code" % prefix),
        "districtName": getattr(args, "%s_district_name" % prefix),
        "lat": getattr(args, "%s_lat" % prefix),
        "lng": getattr(args, "%s_lng" % prefix),
        "date": getattr(args, "%s_date" % prefix),
    }
    payload["addressType"] = getattr(args, "%s_address_type" % prefix)
    payload["fenceCode"] = getattr(args, "%s_fence_code" % prefix)
    return clean(payload)

def location_payload(args, prefix, address_type=False, fence_code=False):
    payload = {
        "address": getattr(args, "%s_address" % prefix),
        "city": getattr(args, "%s_city" % prefix),
        "cityCode": getattr(args, "%s_city_code" % prefix),
        "districtName": getattr(args, "%s_district_name" % prefix),
        "lat": getattr(args, "%s_lat" % prefix),
        "lng": getattr(args, "%s_lng" % prefix),
        "date": getattr(args, "%s_date" % prefix),
    }
    if address_type:
        payload["addressType"] = getattr(args, "%s_address_type" % prefix)
    if fence_code:
        payload["fenceCode"] = getattr(args, "%s_fence_code" % prefix)
    return clean(payload)

# 从搜车结果中 查找每个类别 最便宜的车
def filter_search_vehicle_result(raw_data, group_id):
    rlt = defaultdict(list)
    data = raw_data['data']['modelList']
    for item in data:
        # get top car, get closest store
        store_info = sorted(item['vehicleList'], key=lambda x:x.get('distance', float('inf')))[0]
        tmp = {
            "logo": item['logo'],
            "storeName": store_info.get('storeName', ''),
            "storeCode": store_info.get('storeCode', ''),
            "isFence": store_info.get("isFence", 0),
            "channel": store_info.get("channel", 2),
            "extendInfo": store_info.get("extendInfo", ""),
            "groupId": store_info.get("vehicle", {}).get('vehicle', {}).get("groupId", 0),
            "fenceCode": store_info.get("fenceCode", ""),
            "pickupStoreAddress": store_info.get('pickupStore', {}).get('address', ''),
            "seriesName": store_info.get('vehicle', {}).get('seriesName', ''),
            "modelName": store_info.get('vehicle', {}).get('modelName', ''),
            "modelCode": store_info.get('vehicle', {}).get('modelCode', ''),
            "groupName": store_info.get('vehicle', {}).get('groupName', ''),
            "afterDiscountAmount": store_info.get('feeInfo', {}).get('afterDiscountAmount', 0),
            "basicInsuranceFee": store_info.get('feeInfo', {}).get('basicInsuranceFee', 0),
            "serviceFee": store_info.get('feeInfo', {}).get('serviceFee', 0),
            "businessHours": store_info.get('businessHours', ''),
            "nightServiceFee": store_info.get('feeInfo', {}).get('nightServiceFee', 0),
            "doorToDoorSendCarFee": store_info.get('feeInfo', {}).get('doorToDoorSendCarFee', 0),
            "doorToDoorTakeCarFee": store_info.get('feeInfo', {}).get('doorToDoorTakeCarFee', 0),
            "standardTotalPrice": store_info.get('feeInfo', {}).get('standardTotalPrice', 0),
            "standardUnitPrice": store_info.get('feeInfo', {}).get('standardUnitPrice', 0),
        }
        rlt[tmp["groupName"]].append(tmp)
    if group_id == 0:
        new_rlt = [sorted(value, key=lambda x:x["afterDiscountAmount"])[0] for key, value in rlt.items()]
    else:
        new_rlt = list(rlt.items())[0][:5]

    return new_rlt

def call_search_vehicle_v3(args):
    #groupId含义： 8表示SUV，0表示全部，1411976467222749186跑车，1表示经济型，1603629764818853890表示新能源，14表示MPV，5表示豪华型
    # 
    # 1、筛选距离取还车地点5公里以内的
    # 2、从返回结果中 每个类型选最便宜的 [8,5,1,14,1603629764818853890]
    payload = authentication(args)
    payload.update(
        {
            "pickupInfo": location_payload(args, "pickup"),
            "returnInfo": location_payload(args, "return"),
            "filter": args.filter,
            "groupOrderId": args.group_order_id,
            #"userId": args.user_id,
            "xdChannel": args.xd_channel,
        }
    )
    raw = request_json(
        args.endpoint_url.rstrip("/") + "/searchVehicleV3",
        payload,
        args.timeout,
        not args.no_verify_ssl,
    )
    # 默认的数据结果太多，需要筛选其中的四款出来，
    return filter_search_vehicle_result(raw, args.filter['groupId'])

def call_get_price_detail_v3(args):
    payload = authentication(args)
    payload.update(
        {
            "modelCode": args.model_code,
            "storeCode": args.store_code,
            "fenceCode": args.fence_code,
            "orderType": args.order_type,
            "addedServices": args.added_services,
            "activitySubAmount": args.activity_sub_amount,
            "isBlindBoxOrder": args.is_blind_box_order,
            "isGroupOrder": args.is_group_order,
            "channel": args.channel,
            "extendInfo": args.extend_info,
            "pickupInfo": location_payload(args, "pickup", address_type=True),
            "returnInfo": location_payload(args, "return", address_type=True),
        }
    )
    return request_json(
        args.endpoint_url.rstrip("/") + "/getPriceDetailV3",
        payload,
        args.timeout,
        not args.no_verify_ssl,
    )


def call_create_order(args):
    payload = authentication(args)
    payload["extendInfo"] = args.extend_info
    payload.update(
        {
            "userId": args.user_id,
            "modelCode": args.model_code,
            "payAmount": args.pay_amount,
            "userInfo": {
                "name": args.driver_name,
                "idType": args.driver_id_type,
                "idNo": args.driver_id_no,
                "mobile": args.driver_mobile,
            },
            "orderSource": args.order_source,
            "isFence": args.is_fence,
            "activitySubAmount": args.activity_sub_amount,
            "addedServiceList": args.added_service_list,
            "addedServices": args.added_services,
            "doorToDoorSendCarFee": args.door_to_door_send_car_fee,
            "doorToDoorTakeCarFee": args.door_to_door_take_car_fee,
            "storeCode": args.store_code,
            "calendarPriceMap": args.calendar_price_map,
            "standardTotalPrice": args.standard_total_price,
            "channel": args.channel,
            "pickupInfo": location_payload(args, "pickup", True, True),
            "returnInfo": location_payload(args, "return", True, True),
            "channelMerchantDiscountsFee": args.channel_merchant_discounts_fee,
            "thirdStore": location_third_store(args, "third_store"),
        }
    )
    return request_json(
        args.endpoint_url.rstrip("/") + "/createOrder",
        payload,
        args.timeout,
        not args.no_verify_ssl,
    )


def call_order_detail(args):
    payload = authentication(args)
    payload["orderCode"] = args.order_code
    raw = request_json(
        args.endpoint_url.rstrip("/") + "/orderDetail",
        payload,
        args.timeout,
        not args.no_verify_ssl,
    )
    return raw


def call_cancel_order_query_v2(args):
    payload = authentication(args)
    payload["orderCode"] = args.order_code
    return request_json(
        args.endpoint_url.rstrip("/") + "/cancleOrdersV2",
        payload,
        args.timeout,
        not args.no_verify_ssl,
    )


def call_cancel_order_v2(args):
    pre_cancel = request_json(
        args.endpoint_url.rstrip("/") + "/cancleOrdersV2",
        {
            **authentication(args),
            "orderCode": args.order_code,
        },
        args.timeout,
        not args.no_verify_ssl,
    )

    payload = authentication(args)
    cancel_reason_id = args.cancel_reason_id
    if cancel_reason_id is None:
        cancel_reason_id = "1001" if pre_cancel.get("payments") == 0 else "1004"
    payload.update(
        {
            "orderCode": args.order_code,
            "refundReason": args.refund_reason,
            "cancelReasonId": cancel_reason_id,
            "otherReason": args.other_reason,
        }
    )
    if pre_cancel.get("payments") != 0:
        payload.update(
            {
                "deduction": pre_cancel.get("deduction"),
                "refundAmount": pre_cancel.get("refundAmount"),
                "groupCancels": pre_cancel.get("groupCancels", []),
            }
        )

    return request_json(
        args.endpoint_url.rstrip("/") + "/cancleOrderV2",
        payload,
        args.timeout,
        not args.no_verify_ssl,
    )


def call_check_store_go_out(args):
    payload = authentication(args)
    payload.update(
        {
            "pickupDate": args.pickup_date,
            "returnDate": args.return_date,
            "storeCode": args.store_code,
        }
    )
    return request_json(
        args.endpoint_url.rstrip("/") + "/checkStoreGoOut",
        payload,
        args.timeout,
        not args.no_verify_ssl,
    )


def call_login_skill(args):
    return request_json(
        args.endpoint_url.rstrip("/") + "/loginSkill",
        {"phone": args.phone},
        args.timeout,
        not args.no_verify_ssl,
    )


def call_check_store_go_out_skill(args):
    payload = authentication(args)
    payload.update(
        {
            "pickupDate": args.pickup_date,
            "returnDate": args.return_date,
            "storeCode": args.store_code,
        }
    )
    return request_json(
        args.endpoint_url.rstrip("/") + "/checkStoreGoOutSkill",
        payload,
        args.timeout,
        not args.no_verify_ssl,
    )


def call_order_detail_skill(args):
    raw = request_json(
        args.endpoint_url.rstrip("/") + "/orderDetailSkill",
        clean({"phone": args.phone, "idNo": args.id_no}),
        args.timeout,
        not args.no_verify_ssl,
    )
    #print(f"raw {raw}")
    return ' '.join(raw['orderCodes'])


def call_user_order_list_skill(args):
    payload = authentication(args)
    payload.update(
        clean(
            {
                "userId": args.user_id,
                "startIndex": args.start_index,
                "endIndex": args.end_index,
                "orderState": args.order_state,
            }
        )
    )
    return request_json(
        args.endpoint_url.rstrip("/") + "/userOrderListSkill",
        payload,
        args.timeout,
        not args.no_verify_ssl,
    )

def add_common_options(parser, channelid=DEFAULT_CHANNEL_ID, order_channel=DEFAULT_ORDER_CHANNEL):
    parser.add_argument("--endpoint-url", default=DEFAULT_ENDPOINT_URL)
    parser.add_argument("--app-key", default=DEFAULT_APP_KEY)
    parser.add_argument("--sign")
    parser.add_argument("--sign-secret", default=DEFAULT_APP_KEY)
    parser.add_argument("--order-channel", type=int, default=order_channel)
    parser.add_argument("--channel-id", type=int, default=channelid)
    parser.add_argument("--xiaodou-channel", type=int, default=channelid)
    parser.add_argument("--timeout", type=float, default=30.0)
    parser.add_argument("--no-verify-ssl", action="store_true")
    parser.add_argument("--timestamp", type=int, default=int(datetime.datetime.now().timestamp()*1000))


def add_location_options(parser, prefix):
    parser.add_argument("--%s-address" % prefix, required=True)
    parser.add_argument("--%s-city" % prefix, required=True)
    parser.add_argument("--%s-city-code" % prefix, required=True)
    parser.add_argument("--%s-district-name" % prefix, required=True)
    parser.add_argument("--%s-lat" % prefix, type=str, required=True)
    parser.add_argument("--%s-lng" % prefix, type=str, required=True)
    parser.add_argument("--%s-date" % prefix, required=True)
    parser.add_argument("--%s-address-type" % prefix, required=True)
    parser.add_argument("--%s-fence-code" % prefix, default="")

def add_third_store_location_options(parser, prefix):
    parser.add_argument("--%s-address" % prefix, required=True)
    parser.add_argument("--%s-city" % prefix, required=True)
    parser.add_argument("--%s-code" % prefix, required=True)
    parser.add_argument("--%s-open-time" % prefix, required=True)
    parser.add_argument("--%s-close-time" % prefix, required=True)
    parser.add_argument("--%s-phone" % prefix, required=True)
    parser.add_argument("--%s-name" % prefix, required=True)
    parser.add_argument("--%s-city-code" % prefix, required=True)
    parser.add_argument("--%s-district-name" % prefix, required=True)
    parser.add_argument("--%s-lat" % prefix, type=str, required=True)
    parser.add_argument("--%s-lng" % prefix, type=str, required=True)
    parser.add_argument("--%s-date" % prefix, required=True)
    parser.add_argument("--%s-address-type" % prefix, required=True)
    parser.add_argument("--%s-address-type-name" % prefix, required=True)
    parser.add_argument("--%s-fence-code" % prefix, default="")

def build_search_parser(subparsers):
    parser = subparsers.add_parser("search-vehicle-v3", help="search available vehicles")
    add_common_options(parser)
    add_location_options(parser, "pickup")
    add_location_options(parser, "return")
    parser.add_argument(
        "--filter",
        type=json_object,
        default={"groupId": 0, "transmissionType": 1},
        metavar="JSON",
    )
    parser.add_argument("--group-order-id")
    parser.add_argument("--user-id", required=False)
    parser.add_argument("--xd-channel", type=int)
    #parser.add_argument("--isPickupOndoor", type=int, default=0)
    #parser.add_argument("--isPickoffOndoor", type=int, default=0)
    parser.set_defaults(handler=call_search_vehicle_v3)
    parser.add_argument("--json-path")


def build_price_parser(subparsers):
    parser = subparsers.add_parser("get-price-detail-v3", help="get rental price details")
    add_common_options(parser)
    add_location_options(parser, "pickup")
    add_location_options(parser, "return")
    parser.add_argument("--model-code", required=True)
    parser.add_argument("--store-code", required=True)
    parser.add_argument("--fence-code")
    parser.add_argument("--order-type", type=int, default=0)
    parser.add_argument("--added-services", required=True)
    parser.add_argument("--activity-sub-amount", type=float)
    parser.add_argument("--is-blind-box-order", type=int, default=0)
    parser.add_argument("--is-group-order", type=int, default=0)
    parser.add_argument("--channel", type=int, required=True)
    parser.add_argument("--extend-info", required=True)
    parser.set_defaults(handler=call_get_price_detail_v3)
    parser.add_argument("--json-path")


def build_create_parser(subparsers):
    parser = subparsers.add_parser("create-order", help="create a rental order")
    add_common_options(parser, 50, 50)
    add_location_options(parser, "pickup")
    add_location_options(parser, "return")
    add_third_store_location_options(parser, "third-store")
    parser.add_argument("--user-id", required=True)
    parser.add_argument("--model-code", required=True)
    parser.add_argument("--pay-amount", type=float, required=True)
    parser.add_argument("--driver-name", required=True)
    parser.add_argument("--driver-id-type", type=int, required=True)
    parser.add_argument("--driver-id-no", required=True)
    parser.add_argument("--driver-mobile", required=True)
    parser.add_argument("--order-source", type=int, required=True)
    parser.add_argument("--is-fence", type=int)
    parser.add_argument("--activity-sub-amount", type=float)
    parser.add_argument("--added-service-list", type=json_text, required=True)
    parser.add_argument("--added-services", required=True)
    parser.add_argument("--door-to-door-send-car-fee", type=float)
    parser.add_argument("--door-to-door-take-car-fee", type=float)
    parser.add_argument("--store-code", required=True)
    parser.add_argument("--calendar-price-map", type=json_text, required=True)
    parser.add_argument("--standard-total-price", type=float)
    parser.add_argument("--channel", type=int, required=True)
    parser.add_argument("--extend-info", required=True)
    parser.add_argument("--channel-merchant-discounts-fee")
    #parser.add_argument("--third-store", required=True)
    parser.set_defaults(handler=call_create_order)
    parser.add_argument("--json-path")


def build_order_detail_parser(subparsers):
    parser = subparsers.add_parser("order-detail", help="get order details")
    add_common_options(parser)
    parser.add_argument("--order-code", required=True)
    parser.set_defaults(handler=call_order_detail)
    parser.add_argument("--json-path")


def build_cancel_parser(subparsers):
    parser = subparsers.add_parser(
        "cancel-order-v2",
        help="query payment state, then cancel an unpaid or paid order",
    )
    add_common_options(parser)
    parser.add_argument("--order-code", required=True)
    parser.add_argument("--refund-reason", default="skill渠道取消订单退款")
    parser.add_argument("--cancel-reason-id")
    parser.add_argument("--other-reason", default="")
    parser.add_argument("--json-path")
    parser.set_defaults(handler=call_cancel_order_v2)


def build_cancel_query_parser(subparsers):
    parser = subparsers.add_parser(
        "cancel-order-query-v2",
        help="query deduction and refund amount before canceling an order",
    )
    add_common_options(parser)
    parser.add_argument("--order-code", required=True)
    parser.add_argument("--json-path")
    parser.set_defaults(handler=call_cancel_order_query_v2)


def build_store_go_out_parser(subparsers):
    parser = subparsers.add_parser(
        "check-store-go-out", help="check whether pickup time overlaps store closed time"
    )
    add_common_options(parser)
    parser.add_argument("--pickup-date", required=True)
    parser.add_argument("--return-date", required=True)
    parser.add_argument("--store-code", required=True)
    parser.set_defaults(handler=call_check_store_go_out)
    parser.add_argument("--json-path")


def build_login_parser(subparsers):
    parser = subparsers.add_parser("login-skill", help="register or get a user id by phone")
    parser.add_argument("--endpoint-url", default=DEFAULT_ENDPOINT_URL)
    parser.add_argument("--timeout", type=float, default=30.0)
    parser.add_argument("--no-verify-ssl", action="store_true")
    parser.add_argument("--phone", required=True)
    parser.set_defaults(handler=call_login_skill)
    parser.add_argument("--json-path")


def build_check_store_parser(subparsers):
    parser = subparsers.add_parser(
        "check-store-go-out-skill", help="check whether store closed time overlaps rental time"
    )
    add_common_options(parser)
    parser.add_argument("--pickup-date", required=True)
    parser.add_argument("--return-date", required=True)
    parser.add_argument("--store-code", required=True)
    parser.set_defaults(handler=call_check_store_go_out_skill)
    parser.add_argument("--json-path")


def build_order_detail_skill_parser(subparsers):
    parser = subparsers.add_parser("order-detail-skill", help="get order codes by user identity")
    parser.add_argument("--endpoint-url", default=DEFAULT_ENDPOINT_URL)
    parser.add_argument("--timeout", type=float, default=30.0)
    parser.add_argument("--no-verify-ssl", action="store_true")
    parser.add_argument("--phone")
    parser.add_argument("--id-no")
    parser.set_defaults(handler=call_order_detail_skill)
    parser.add_argument("--json-path")


def build_user_order_list_parser(subparsers):
    parser = subparsers.add_parser(
        "user-order-list-skill", help="query refundable orders by user id"
    )
    add_common_options(parser)
    parser.add_argument("--user-id", required=True)
    parser.add_argument("--order-state", type=int, required=True)
    parser.add_argument("--start-index", type=int)
    parser.add_argument("--end-index", type=int)
    parser.set_defaults(handler=call_user_order_list_skill)
    parser.add_argument("--json-path")


def build_parser():
    parser = argparse.ArgumentParser(description="Xiaodou car rental API CLI")
    subparsers = parser.add_subparsers(dest="operation", required=True)
    build_search_parser(subparsers)
    build_price_parser(subparsers)
    build_create_parser(subparsers)
    build_order_detail_parser(subparsers)
    build_cancel_parser(subparsers)
    build_cancel_query_parser(subparsers)
    build_store_go_out_parser(subparsers)
    build_login_parser(subparsers)
    build_check_store_parser(subparsers)
    build_order_detail_skill_parser(subparsers)
    build_user_order_list_parser(subparsers)
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    #print(f"parsed args {args}")
    if args.operation == "order-detail-skill" and args.phone is None and args.id_no is None:
        print("--phone and --id-no: at least one is required", file=sys.stderr)
        return 2
    try:
        result = args.handler(args)
    except requests.RequestException as exc:
        print("request failed: %s" % exc, file=sys.stderr)
        return 1
    try:
        result = select_json_path(result, args.json_path)
    except (KeyError, TypeError, IndexError):
        print("json path not found: %s" % args.json_path, file=sys.stderr)
        return 2
    #print(json.dumps(result, ensure_ascii=False, indent=2))
    print(result)
    return 0


if __name__ == "__main__":
    sys.exit(main())
