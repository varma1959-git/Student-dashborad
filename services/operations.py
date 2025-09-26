# services/operations.py
import pandas as pd
from datetime import datetime
from db.storage import load_data, save_data, append_history

def add_entry(name: str, age: int, score: float) -> pd.DataFrame:
    df = load_data()
    new_row = pd.DataFrame([{"Name": name, "Age": age, "Score": score}])
    df = pd.concat([df, new_row], ignore_index=True)
    save_data(df)

    append_history({
        "timestamp": datetime.utcnow().isoformat(),
        "action": "add",
        "name": name,
        "age": age,
        "score": score,
        "old_value": "",
        "new_value": f"{name},{age},{score}",
    })
    return df

def get_summary(df: pd.DataFrame) -> dict:
    if df.empty:
        return {"count": 0, "avg_score": None, "max_score": None, "min_score": None}
    return {
        "count": int(df.shape[0]),
        "avg_score": float(df["Score"].mean()),
        "max_score": float(df["Score"].max()),
        "min_score": float(df["Score"].min()),
    }
