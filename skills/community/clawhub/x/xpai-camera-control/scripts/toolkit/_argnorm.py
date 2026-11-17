def coerce_str(value):
    if value is None or isinstance(value, bool):
        return value
    if isinstance(value, int):
        return str(value)
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return value
