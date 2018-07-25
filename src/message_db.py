import time
import threading
import uuid

class Message:
    """
    A representation of a message to be broadcasted.
    """
    def __init__(self, message, category):
        """Constructor.

        Args:
            message: the message content as a string.
            category: the broadcast_pb2.Category of the message.
        """
        self.id = str(uuid.uuid4())
        self.message = message
        self.category = category

class MessageDB:
    """
    The database which contains the messages to broadcast
    """
    def __init__(self):
        self._message_list = []
        self._semaphore = threading.Semaphore()

    def add(self, message):
        """Adds a new Message to the database.

        Args:
            message: the Message to add.
        """
        self._semaphore.acquire()
        self._message_list.append(message)
        self._semaphore.release()

    def stream(self, category):
        """Obtains an iterator over the contents of the database which
        is updated when new messages are added to the database. This iterator
        can be filtered by one concrete Category.

        Args:
            category: Category to filter (0 to opbtain all the messages)

        Returns:
            A iterator with the messages in the database.
        """
        # Keep the last index sent with the stream to avoid event duplication
        last_index = 0
        while True:
            # Read the messages since the last polling of the database
            self._semaphore.acquire()
            messages = self._message_list[last_index:]
            self._semaphore.release()
            # Send this messages in the iterator
            for message in messages:
                last_index = last_index + 1
                # Filter by category
                if category == 0 or category == message.category:
                    yield message
            # Await for the next poll
            time.sleep(0.5)