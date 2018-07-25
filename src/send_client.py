import sys
import grpc

import broadcast_pb2_grpc
import broadcast_pb2

if __name__ == "__main__":
    # Initialize a gRPC client stub
    channel = grpc.insecure_channel('localhost:50051')
    stub = broadcast_pb2_grpc.BroadcastStub(channel)
    
    # Invoke the remote method as if it were a local method
    request = broadcast_pb2.SendRequest()
    request.message = sys.argv[2]
    request.category = int(sys.argv[1])
    print(stub.send(request))
