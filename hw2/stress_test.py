import threading
import os

def cpu_stress():
    """Perform endless heavy computations to stress CPU."""
    while True:
        result = sum([x ** 2 for x in range(100000)])  # Larger range for more CPU usage

def memory_stress():
    """Continuously allocate memory without releasing it."""
    data = []
    try:
        while True:
            # Allocate 10MB chunks of memory continuously
            data.append(' ' * 10**7)  # 10MB
    except MemoryError:
        print("Memory limit reached! Continuing stress...")

def io_stress():
    """Perform continuous disk I/O operations to stress I/O."""
    try:
        with open("temp_stress_file.txt", "w") as f:
            while True:
                # Write large chunks of random data to the file
                f.write("A" * 10**6)  # Write 1MB per iteration
                f.flush()
    except Exception as e:
        print(f"IO Stress failed: {e}")

def thread_stress():
    """Launch a large number of threads to stress multithreading capabilities."""
    threads = []
    for _ in range(100):  # Increase number of threads to 100
        t = threading.Thread(target=cpu_stress)
        threads.append(t)
        t.start()
    for t in threads:
        t.join()

if __name__ == "__main__":
    print(f"Starting maximum stress test in process {os.getpid()}...")
    # Start memory stress in a separate thread
    threading.Thread(target=memory_stress, daemon=True).start()

    # Start I/O stress in a separate thread
    threading.Thread(target=io_stress, daemon=True).start()

    # Stress CPU and threads
    thread_stress()

