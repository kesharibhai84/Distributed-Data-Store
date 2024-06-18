import Pyro4
import os

@Pyro4.expose
class WorkerNode:
    def __init__(self, node_id):
        self.node_id = node_id
        self.storage_path = f"storage_node_{node_id}"
        if not os.path.exists(self.storage_path):
            os.makedirs(self.storage_path)

    def store_file(self, file_name, file_data):
        file_path = os.path.join(self.storage_path, file_name)
        with open(file_path, 'wb') as file:
            file.write(file_data)
        print(f"File '{file_name}' stored in node {self.node_id}.")

def start_worker(node_id):
    daemon = Pyro4.Daemon()
    ns = Pyro4.locateNS()
    worker = WorkerNode(node_id)
    uri = daemon.register(worker)
    ns.register(f"worker.node{node_id}", uri)
    print(f"Worker node {node_id} is running.")
    daemon.requestLoop()

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python worker.py <node_id>")
        sys.exit(1)
    start_worker(int(sys.argv[1]))
