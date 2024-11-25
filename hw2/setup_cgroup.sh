#!/bin/bash

# Define cgroup name
CGROUP_NAME="test_cgroup"

# Create cgroup
sudo cgcreate -g memory,cpu:/${CGROUP_NAME}

# Set memory limit (e.g., 100 MB)
sudo cgset -r memory.limit_in_bytes=100M ${CGROUP_NAME}

# Set CPU limit (e.g., 50% of one CPU)
sudo cgset -r cpu.cfs_quota_us=50000 ${CGROUP_NAME}

# Run Python script in cgroup
echo "Starting Python script in cgroup '${CGROUP_NAME}'..."
sudo cgexec -g memory,cpu:${CGROUP_NAME} python3 stress_test.py

