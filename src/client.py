import grpc

import broadcast_pb2_grpc
import broadcast_pb2

if __name__ == "__main__":
    # Initialize the gRPC client stub and receive messages
    channel = grpc.insecure_channel('localhost:50051')
    stub = broadcast_pb2_grpc.BroadcastStub(channel)

    for message in stub.subscribe(broadcast_pb2.SubscribeRequest(category = broadcast_pb2.ANNOUNCEMENT)):
        print(message)
