import sys
import Pyro4 

def upload_file(file_name):
    with open(file_name, 'rb') as f:
        file_data = f.read()
    
    # Debugging: Print the type and size of file_data
    print(f"Type of file_data: {type(file_data)}")
    print(f"Size of file_data: {len(file_data)} bytes")

    with Pyro4.locateNS() as ns:
        uri = ns.lookup("master.node")
        master = Pyro4.Proxy(uri)
        
        # Ensure file_data is explicitly converted to bytes
        file_data_bytes = bytes(file_data)
        
        response = master.upload_file(file_name, file_data_bytes)
        print(response)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python client.py <file_to_upload>")
        sys.exit(1)

    file_name = sys.argv[1]
    upload_file(file_name)
