import os
import time
import matplotlib.pyplot as plt

# Path to the cgroup files for monitoring
CGROUP_PATH = "/sys/fs/cgroup"  # Adjust if cgroup v1/v2 is used
CGROUP_NAME = "test_cgroup"  # Match the name used in setup_cgroup.sh
CPU_STATS_FILE = f"{CGROUP_PATH}/cpu/{CGROUP_NAME}/cpuacct.usage"
MEMORY_USAGE_FILE = f"{CGROUP_PATH}/memory/{CGROUP_NAME}/memory.usage_in_bytes"
MEMORY_LIMIT_FILE = f"{CGROUP_PATH}/memory/{CGROUP_NAME}/memory.limit_in_bytes"

# Lists to store collected data
timestamps = []
cpu_usage = []
memory_usage = []

def read_cgroup_file(file_path):
    """Reads the content of a cgroup file."""
    try:
        with open(file_path, "r") as f:
            return int(f.read().strip())
    except FileNotFoundError:
        print(f"File {file_path} not found. Ensure the cgroup exists and is set up correctly.")
        return None

def format_bytes(size_in_bytes):
    """Converts bytes to a human-readable format."""
    kb = size_in_bytes / 1024
    mb = kb / 1024
    if mb >= 1:
        return f"{mb:.2f} MB"
    elif kb >= 1:
        return f"{kb:.2f} KB"
    else:
        return f"{size_in_bytes} Bytes"

def monitor_cgroup(interval=1, duration=60):
    """Monitors the cgroup resource usage, collects data, and generates graphs."""
    print(f"Monitoring cgroup '{CGROUP_NAME}' every {interval} second(s) for {duration} seconds...\n")
    print("Press Ctrl+C to stop early.\n")

    start_time = time.time()
    try:
        while time.time() - start_time < duration:
            current_time = time.time() - start_time

            # Read memory and CPU usage
            mem_usage = read_cgroup_file(MEMORY_USAGE_FILE)
            cpu = read_cgroup_file(CPU_STATS_FILE)

            if mem_usage is not None:
                memory_usage.append(mem_usage)
                print(f"Memory Usage: {format_bytes(mem_usage)}")

            if cpu is not None:
                cpu_usage.append(cpu)
                print(f"CPU Usage (nanoseconds): {cpu}")

            timestamps.append(current_time)
            time.sleep(interval)

        # Generate graphs
        generate_graphs()

    except KeyboardInterrupt:
        print("\nMonitoring stopped early.")
        generate_graphs()
    except Exception as e:
        print(f"Error: {e}")

def generate_graphs():
    """Generates and saves graphs for memory and CPU usage."""
    print("\nGenerating graphs...")
    
    # Create Memory Usage Graph
    plt.figure(figsize=(10, 5))
    plt.plot(timestamps, [usage / (1024 * 1024) for usage in memory_usage], label="Memory Usage (MB)")
    plt.title("Memory Usage Over Time")
    plt.xlabel("Time (s)")
    plt.ylabel("Memory Usage (MB)")
    plt.legend()
    plt.grid(True)
    plt.savefig("memory_usage.png")
    print("Memory usage graph saved as 'memory_usage.png'.")

    # Create CPU Usage Graph
    plt.figure(figsize=(10, 5))
    plt.plot(timestamps, cpu_usage, label="CPU Usage (nanoseconds)")
    plt.title("CPU Usage Over Time")
    plt.xlabel("Time (s)")
    plt.ylabel("CPU Usage (nanoseconds)")
    plt.legend()
    plt.grid(True)
    plt.savefig("cpu_usage.png")
    print("CPU usage graph saved as 'cpu_usage.png'.")

if __name__ == "__main__":
    monitor_cgroup(interval=1, duration=60)  # Collect data every 1 second for 60 seconds

