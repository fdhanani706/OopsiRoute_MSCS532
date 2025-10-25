import pandas as pd
import matplotlib.pyplot as plt

# Load CSV
df = pd.read_csv("phase3_results.csv")

# Plot 1: Time vs Nodes
plt.figure()
plt.plot(df["nodes"], df["time_seconds"], marker="o")
plt.xlabel("Number of Nodes")
plt.ylabel("Execution Time (s)")
plt.title("Execution Time vs Number of Nodes")
plt.grid(True)
plt.savefig("time_vs_nodes.png")

# Plot 2: Memory vs Nodes
plt.figure()
plt.plot(df["nodes"], df["memory_MB"], marker="o", color="orange")
plt.xlabel("Number of Nodes")
plt.ylabel("Memory Used (MB)")
plt.title("Memory Usage vs Number of Nodes")
plt.grid(True)
plt.savefig("memory_vs_nodes.png")

# Plot 3: Speedup Ratio vs Nodes (optional)
df["speedup"] = df["time_seconds"].iloc[0] / df["time_seconds"]
plt.figure()
plt.plot(df["nodes"], df["speedup"], marker="o", color="green")
plt.xlabel("Number of Nodes")
plt.ylabel("Speedup Ratio")
plt.title("Speedup vs Number of Nodes")
plt.grid(True)
plt.savefig("speedup_ratio.png")

print("Plots saved as PNG files!")
