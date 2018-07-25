import grpc
from concurrent import futures
import time

import message_db

import broadcast_pb2_grpc
import broadcast_pb2

class BroadcastServicerImpl(broadcast_pb2_grpc.BroadcastServicer):
    # Implement the methods in the service

    def __init__(self):
        self._db = message_db.MessageDB()

    def send(self, request, context):
        message = message_db.Message(request.message, request.category)
        self._db.add(message)
        return broadcast_pb2.BroadcastMessage(id = message.id, message = message.message, category = message.category)

    def subscribe(self, request, context):
        for message in self._db.stream(request.category):
            yield broadcast_pb2.BroadcastMessage(id = message.id, message = message.message, category = message.category)           


def await_server_termination(server):
    """
    Blocks the execution of the function until the server is 
    stopped using Ctrl+C.

    Args:
        server: server to stop when the keys are pressed.
    """
    try:
        while True:
            time.sleep(60 * 60 * 24)
    except KeyboardInterrupt:
        server.stop(0) 

if __name__ == '__main__':
    # Initialize gRPC server and start listening...
    server = grpc.server(futures.ThreadPoolExecutor(10))
    broadcast_pb2_grpc.add_BroadcastServicer_to_server(BroadcastServicerImpl(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    await_server_termination(server)
