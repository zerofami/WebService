def require(condition, exception):
    if not condition:
        raise exception
