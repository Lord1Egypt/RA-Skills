#!/usr/bin/env python3
"""
Tính toán thuế, phí và ROI cho giao dịch bất động sản Việt Nam.

Cách dùng:
    python price-calculator.py --mode tax --price 3000000000
    python price-calculator.py --mode roi --price 3000000000 --rent 15000000 --years 5
    python price-calculator.py --mode cost --price 3000000000

Lưu ý: Các mức thuế/phí là tham khảo. Luôn web search để xác minh mức hiện hành.
"""

import argparse
import json
import sys


def format_vnd(amount):
    """Format số tiền VNĐ dễ đọc"""
    if amount >= 1_000_000_000:
        return f"{amount/1_000_000_000:.2f} tỷ"
    elif amount >= 1_000_000:
        return f"{amount/1_000_000:.1f} triệu"
    else:
        return f"{amount:,.0f} đồng"


def calc_tax(price):
    """Tính thuế và phí giao dịch BĐS"""
    # Thuế TNCN bên bán: 2% giá chuyển nhượng
    tncn = price * 0.02

    # Lệ phí trước bạ bên mua: 0.5%
    truoc_ba = price * 0.005

    # Phí công chứng (biểu phí tham khảo)
    if price <= 50_000_000:
        cong_chung = 50_000
    elif price <= 100_000_000:
        cong_chung = price * 0.001
    elif price <= 1_000_000_000:
        cong_chung = price * 0.001
    elif price <= 3_000_000_000:
        cong_chung = price * 0.001
    else:
        cong_chung = price * 0.001
    cong_chung = min(cong_chung, 10_000_000)  # Trần phí

    # Phí đăng bộ sang tên
    dang_bo = 100_000

    # Phí thẩm định
    tham_dinh = 100_000

    result = {
        "giá_bds": price,
        "bên_bán": {
            "thuế_tncn_2%": tncn,
            "tổng": tncn,
        },
        "bên_mua": {
            "lệ_phí_trước_bạ_0.5%": truoc_ba,
            "phí_công_chứng": cong_chung,
            "phí_đăng_bộ": dang_bo,
            "phí_thẩm_định": tham_dinh,
            "tổng": truoc_ba + cong_chung + dang_bo + tham_dinh,
        },
        "tổng_thuế_phí": tncn + truoc_ba + cong_chung + dang_bo + tham_dinh,
    }
    return result


def calc_roi(price, monthly_rent, years, annual_appreciation=0.05):
    """Tính ROI đầu tư BĐS"""
    # Thu nhập cho thuê
    annual_rent = monthly_rent * 12
    total_rent = annual_rent * years

    # Tỷ suất cho thuê
    rental_yield = (annual_rent / price) * 100

    # Tăng giá tài sản
    future_value = price * ((1 + annual_appreciation) ** years)
    capital_gain = future_value - price

    # Chi phí mua (thuế phí)
    buy_costs = calc_tax(price)["bên_mua"]["tổng"]

    # Chi phí bán (thuế TNCN trên giá bán tương lai)
    sell_costs = future_value * 0.02

    # Tổng lợi nhuận
    total_profit = total_rent + capital_gain - buy_costs - sell_costs

    # ROI
    total_investment = price + buy_costs
    roi = (total_profit / total_investment) * 100
    annual_roi = roi / years

    result = {
        "đầu_vào": {
            "giá_mua": price,
            "tiền_thuê_tháng": monthly_rent,
            "thời_gian_năm": years,
            "tốc_độ_tăng_giá_năm": f"{annual_appreciation*100}%",
        },
        "thu_nhập_cho_thuê": {
            "thu_nhập_năm": annual_rent,
            "tổng_thu_nhập": total_rent,
            "tỷ_suất_cho_thuê": f"{rental_yield:.2f}%/năm",
        },
        "tăng_giá_tài_sản": {
            "giá_trị_tương_lai": future_value,
            "lợi_nhuận_tăng_giá": capital_gain,
        },
        "chi_phí": {
            "chi_phí_mua": buy_costs,
            "thuế_khi_bán": sell_costs,
        },
        "kết_quả": {
            "tổng_lợi_nhuận": total_profit,
            "roi_tổng": f"{roi:.2f}%",
            "roi_năm": f"{annual_roi:.2f}%/năm",
        },
    }
    return result


def calc_total_cost(price, is_new_project=False):
    """Tính tổng chi phí mua BĐS"""
    tax = calc_tax(price)
    buyer_costs = tax["bên_mua"]["tổng"]

    result = {
        "giá_bds": price,
        "thuế_phí_mua": buyer_costs,
    }

    if is_new_project:
        vat = price * 0.08  # VAT 8%
        maintenance = price * 0.02  # Phí bảo trì 2%
        result["vat_8%"] = vat
        result["phí_bảo_trì_2%"] = maintenance
        result["tổng_chi_phí"] = price + buyer_costs + vat + maintenance
    else:
        result["tổng_chi_phí"] = price + buyer_costs

    return result


def print_result(data, indent=0):
    """In kết quả dễ đọc"""
    for key, value in data.items():
        prefix = "  " * indent
        label = key.replace("_", " ").title()
        if isinstance(value, dict):
            print(f"{prefix}{label}:")
            print_result(value, indent + 1)
        elif isinstance(value, (int, float)) and not isinstance(value, bool):
            if value > 100:  # Likely VND amount
                print(f"{prefix}{label}: {format_vnd(value)} ({value:,.0f} VNĐ)")
            else:
                print(f"{prefix}{label}: {value}")
        else:
            print(f"{prefix}{label}: {value}")


def main():
    parser = argparse.ArgumentParser(description="Tính toán BĐS Việt Nam")
    parser.add_argument("--mode", choices=["tax", "roi", "cost"], required=True,
                        help="tax: thuế phí | roi: lợi nhuận đầu tư | cost: tổng chi phí")
    parser.add_argument("--price", type=float, required=True, help="Giá BĐS (VNĐ)")
    parser.add_argument("--rent", type=float, default=0, help="Tiền thuê tháng (VNĐ)")
    parser.add_argument("--years", type=int, default=5, help="Số năm đầu tư")
    parser.add_argument("--appreciation", type=float, default=5, help="Tốc độ tăng giá (%/năm)")
    parser.add_argument("--new-project", action="store_true", help="Mua từ chủ đầu tư (có VAT)")
    parser.add_argument("--json", action="store_true", help="Xuất JSON")

    args = parser.parse_args()

    if args.mode == "tax":
        result = calc_tax(args.price)
    elif args.mode == "roi":
        if args.rent == 0:
            print("Lỗi: Cần --rent cho chế độ ROI")
            sys.exit(1)
        result = calc_roi(args.price, args.rent, args.years, args.appreciation / 100)
    elif args.mode == "cost":
        result = calc_total_cost(args.price, args.new_project)

    print("=" * 60)
    if args.mode == "tax":
        print("  BẢNG TÍNH THUẾ VÀ PHÍ GIAO DỊCH BĐS")
    elif args.mode == "roi":
        print("  PHÂN TÍCH LỢI NHUẬN ĐẦU TƯ BĐS")
    elif args.mode == "cost":
        print("  TỔNG CHI PHÍ MUA BĐS")
    print("=" * 60)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print_result(result)

    print("=" * 60)
    print("⚠️  Các mức thuế/phí là THAM KHẢO. Luôn xác minh mức hiện hành.")


if __name__ == "__main__":
    main()
