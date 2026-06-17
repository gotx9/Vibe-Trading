"""Pre-cache CSI 300 constituents 7yr data to ~/.vibe-trading/cache/loaders/tushare/"""
import sys, os, time
from pathlib import Path

os.environ["VIBE_TRADING_DATA_CACHE"] = "1"

AGENT_DIR = Path(__file__).resolve().parent / "agent"
sys.path.insert(0, str(AGENT_DIR))

from dotenv import load_dotenv as _load_dotenv
for candidate in (Path.home() / ".vibe-trading" / ".env", AGENT_DIR / ".env", Path.cwd() / ".env"):
    if candidate.exists():
        _load_dotenv(candidate)
        print(f"[OK] Loaded config: {candidate}")
        break

# Step 1: Get CSI 300 constituents via akshare
print("\n[Step 1] Getting CSI 300 constituents...")
try:
    import akshare as ak
    df = ak.index_stock_cons("000300")
    codes_raw = sorted(df["品种代码"].tolist())
    def to_ts_code(c):
        c = c.strip()
        if c.startswith("6"):
            return f"{c}.SH"
        return f"{c}.SZ"
    codes = [to_ts_code(c) for c in codes_raw]
    print(f"[OK] Got {len(codes)} stocks")
except Exception as e:
    print(f"[WARN] akshare failed: {e}")
    print("Using hardcoded 30 major CSI 300 stocks...")
    codes = [
        "600519.SH","000858.SZ","601318.SH","600036.SH","000333.SZ",
        "601166.SH","600276.SH","600887.SH","002415.SZ","300750.SZ",
        "601012.SH","600030.SH","000001.SZ","002594.SZ","601888.SH",
        "600900.SH","000002.SZ","600585.SH","601398.SH","000651.SZ",
        "600031.SH","002475.SZ","300059.SZ","601899.SH","000568.SZ",
        "600809.SH","002714.SZ","601088.SH","000725.SZ","300124.SZ",
    ]

print(f"  Total: {len(codes)} stocks")

# Step 2: Fetch via Tushare loader (auto-caches to disk)
print(f"\n[Step 2] Fetching 2019-01-01 ~ 2025-12-31 via Tushare...")
from backtest.loaders.tushare import DataLoader
loader = DataLoader()

ok = 0
fail = 0
total = len(codes)
t0 = time.time()

for i, code in enumerate(codes):
    try:
        result = loader.fetch([code], "2019-01-01", "2025-12-31")
        if result:
            ok += 1
            rows = len(result[code])
            print(f"  [{i+1:03d}/{total}] OK {code} ({rows} bars)")
        else:
            fail += 1
            print(f"  [{i+1:03d}/{total}] -- {code} (no data)")
    except Exception as e:
        fail += 1
        print(f"  [{i+1:03d}/{total}] ERR {code}: {e}")
    # 10000-point tier: faster rate limit, 0.2s between calls
    time.sleep(0.2)

elapsed = time.time() - t0
print(f"\n{'='*50}")
print(f"DONE: {ok}/{total} success, {fail} failed, {elapsed:.0f}s")
print(f"Cache: {Path.home() / '.vibe-trading' / 'cache' / 'loaders' / 'tushare'}")
