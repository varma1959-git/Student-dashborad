# utils/validators.py

def valid_name(name) -> bool:
    return bool(str(name).strip())

def valid_age(age) -> bool:
    try:
        return int(age) > 0
    except Exception:
        return False

def valid_score(score) -> bool:
    try:
        s = float(score)
    except Exception:
        return False
    return 0 <= s <= 100
