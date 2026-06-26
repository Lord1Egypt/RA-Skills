def get_shipment_record(shipment_id: str):
    return {
        "shipment_id": "SUG-2026-014",
        "product": {
            "quantity_units": 2000,
            "net_weight_kg": 50000
        },
        "costs": {
            "product_cost": 28500,
            "ocean_freight": 4200,
            "cargo_insurance": 300,
            "customs_duty": 1450,
            "mpf": 165,
            "hmf": 90,
            "broker_fee": 250,
            "domestic_trucking": 875,
            "other_fees": 120
        }
    }


def calculate_landed_cost(shipment: dict):
    costs = shipment.get("costs", {})
    product = shipment.get("product", {})

    total = (
        costs.get("product_cost", 0)
        + costs.get("ocean_freight", 0)
        + costs.get("cargo_insurance", 0)
        + costs.get("customs_duty", 0)
        + costs.get("mpf", 0)
        + costs.get("hmf", 0)
        + costs.get("broker_fee", 0)
        + costs.get("domestic_trucking", 0)
        + costs.get("other_fees", 0)
    )

    return {
        "shipment_id": shipment.get("shipment_id"),
        "landed_cost": total,
        "cost_per_kg": total / product.get("net_weight_kg", 1),
        "cost_per_unit": total / product.get("quantity_units", 1)
    }