import Pyro4

@Pyro4.expose
class MasterNode:
    def __init__(self):
        self.file_locations = {}

    def upload_file(self, file_name, file_data):
        # For simplicity, use a round-robin strategy to choose worker nodes
        worker_nodes = self.get_worker_nodes()
        num_replicas = min(len(worker_nodes), 3)
        for i in range(num_replicas):
            worker = worker_nodes[i]
            worker.store_file(file_name, file_data)
            if file_name not in self.file_locations:
                self.file_locations[file_name] = []
            self.file_locations[file_name].append(worker._pyroUri)

        return f"File '{file_name}' uploaded and replicated to {num_replicas} nodes."

    def get_worker_nodes(self):
        with Pyro4.locateNS() as ns:
            worker_uris = ns.list(prefix="worker.")
            return [Pyro4.Proxy(uri) for uri in worker_uris.values()]

def start_master():
    daemon = Pyro4.Daemon()
    ns = Pyro4.locateNS()
    uri = daemon.register(MasterNode)
    ns.register("master.node", uri)
    print("Master node is running.")
    daemon.requestLoop()

if __name__ == "__main__":
    start_master()
