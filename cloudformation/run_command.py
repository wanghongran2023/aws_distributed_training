import ray
import os

ray.init(address="auto")

python_file_content = """
import os
import socket

def main():
    print(f"Running on node: {socket.gethostname()} - OS: {os.uname()}")
    print("Hello from Ray Cluster!")

if __name__ == "__main__":
    main()
"""

@ray.remote
def create_and_run_file(file_name, content):
    with open(file_name, "w") as f:
        f.write(content)
    
    result = os.popen(f"python3 {file_name}").read()
    return f"Node: {os.uname().nodename}\n{result.strip()}"

nodes = ray.nodes()
node_ips = [node["NodeManagerAddress"] for node in nodes if node["Alive"]]

file_name = "remote_script.py"

results = ray.get([create_and_run_file.options(resources={f"node:{ip}": 0.01}).remote(file_name, python_file_content) for ip in node_ips])

for output in results:
    print(output)
