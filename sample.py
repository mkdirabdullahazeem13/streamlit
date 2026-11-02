import sys
import os

print("====================================")
print("🐍 PYTHON ENVIRONMENT TEST SCRIPT")
print("====================================")

# 1. Print the exact Python executable running this file
print(f"🎯 Current Python Path: {sys.executable}")

# 2. Check if you are inside a Virtual Environment (venv)
if sys.prefix != sys.base_prefix:
    print("✅ Status: Running inside a VIRTUAL ENVIRONMENT (.venv)")
else:
    print("⚠️ Status: Running inside the GLOBAL computer environment")

print("------------------------------------")

# 3. Simple Data Engineering math test
print("📊 Running quick processing math test...")
data_rows = [100, 250, 400, 650]
total_records = sum(data_rows)

print(f"🚀 Math Check: Processed {len(data_rows)} batches. Total rows = {total_records}")
print("====================================")
print("🎉 Script completed successfully!")
