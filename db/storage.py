# db/storage.py
import os
import pandas as pd
from config.constants import DATA_FILE, HISTORY_FILE, COLUMNS

def ensure_files():
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    if not os.path.exists(DATA_FILE):
        pd.DataFrame(columns=COLUMNS).to_csv(DATA_FILE, index=False)
    if not os.path.exists(HISTORY_FILE):
        cols = ["timestamp","action","name","age","score","old_value","new_value"]  # no user
        pd.DataFrame(columns=cols).to_csv(HISTORY_FILE, index=False)

def load_data():
    ensure_files()
    return pd.read_csv(DATA_FILE)

def save_data(df):
    ensure_files()
    df.to_csv(DATA_FILE, index=False)

def append_history(record: dict):
    ensure_files()
    header = not os.path.exists(HISTORY_FILE) or os.stat(HISTORY_FILE).st_size == 0
    pd.DataFrame([record]).to_csv(HISTORY_FILE, mode="a", header=header, index=False)
