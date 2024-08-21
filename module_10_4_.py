import time
from threading import Thread
import queue
from random import randint

guests_names = [
    'Maria', 'Oleg', 'Vakhtang', 'Sergey', 'Darya', 'Arman', 'Vitoria', 'Nikita', 'Galina', 'Pavel', 'Ilya',
    'Alexandra']


class Table:
    def __init__(self, number):
        self.number = number
        self.guest = None


class Guest(Thread):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def run(self):
        time.sleep(randint(3, 10))


class Cafe:
    def __init__(self, *tables):
        self.queue = queue.Queue()
        self.tables = tables

    def guest_arrival(self, *guest):
        for table in self.tables:
            if table.guest is None:
                table.guest = guest
                return guest.name, table.number
        self.queue.put(guest)
        return guest.name, None

    def discuss_guests(self):
        for table in self.tables:
            if table.guest is not None and not table.guest.is_alive():
                print(f'{table.guest.name} покушал(-а) и ушёл(ушла)')
                print(f'Стол номер {table.number} свободен')
                table.guest = None
                if not self.queue.empty():
                    next_guest = self.queue.get()
                    table.guest = next_guest
                    next_guest.start()
                    print(f'{next_guest.name} вышел(-ла) из очереди и сел(-а) за стол номер {table.number}')


guests = [Guest(name) for name in guests_names]

tables = [Table(number) for number in range(1, 6)]
cafe = Cafe(*tables)
cafe.guest_arrival(*guests)
cafe.discuss_guests()

