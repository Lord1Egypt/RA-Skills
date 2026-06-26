"""Implementation of the data-processor spec."""


def process_data(input_data: dict) -> dict:
    """Process input data according to spec-b.yaml."""
    name = input_data["name"]
    value = input_data["value"]
    return {"result": value * 2}
