from pathlib import Path
import csv

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
RESULTS.mkdir(exist_ok=True)

# Processor assumptions
instruction_count = 1_000_000
clock_rate_hz = 3_000_000_000
base_cpi = 1.20
stall_cpi = 0.15

effective_cpi = base_cpi + stall_cpi
cycles = instruction_count * effective_cpi
execution_time_ms = (cycles / clock_rate_hz) * 1000

# Baseline
baseline_cpi = 1.50
baseline_cycles = instruction_count * baseline_cpi
baseline_time_ms = (baseline_cycles / clock_rate_hz) * 1000
speedup = baseline_time_ms / execution_time_ms

# Cache / memory assumptions
l1_hit_time = 1.0
l1_miss_rate = 0.05
l2_hit_time = 4.0
l2_miss_rate = 0.10
l3_hit_time = 12.0
l3_miss_rate = 0.20
dram_penalty = 80.0

amat_ns = l1_hit_time + l1_miss_rate * (
    l2_hit_time + l2_miss_rate * (
        l3_hit_time + l3_miss_rate * dram_penalty
    )
)

# Save processor results
with open(RESULTS / "performance_results.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Metric", "Baseline", "Optimized"])
    writer.writerow(["Instruction Count", instruction_count, instruction_count])
    writer.writerow(["CPI", baseline_cpi, effective_cpi])
    writer.writerow(["Clock Rate (GHz)", 3.0, 3.0])
    writer.writerow([
        "Execution Time (ms)",
        round(baseline_time_ms, 4),
        round(execution_time_ms, 4)
    ])
    writer.writerow(["Speedup", 1.0, round(speedup, 4)])

# Save memory results
with open(RESULTS / "memory_results.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Metric", "Value"])
    writer.writerow(["L1 Hit Rate", "95%"])
    writer.writerow(["L2 Local Hit Rate", "90%"])
    writer.writerow(["L3 Local Hit Rate", "80%"])
    writer.writerow(["AMAT (ns)", round(amat_ns, 4)])

print("========================================")
print("ENERGY-EFFICIENT PROCESSOR SIMULATION")
print("========================================")
print(f"Instruction Count : {instruction_count:,}")
print(f"Effective CPI     : {effective_cpi:.2f}")
print(f"Clock Cycles      : {cycles:,.0f}")
print(f"Execution Time    : {execution_time_ms:.4f} ms")
print(f"Baseline Time     : {baseline_time_ms:.4f} ms")
print(f"Speedup           : {speedup:.4f}x")
print("----------------------------------------")
print(f"L1 Hit Rate       : 95%")
print(f"L2 Hit Rate       : 90%")
print(f"L3 Hit Rate       : 80%")
print(f"AMAT              : {amat_ns:.4f} ns")
print("----------------------------------------")
print("Results saved successfully.")
print(f"Location          : {RESULTS}")
print("========================================")