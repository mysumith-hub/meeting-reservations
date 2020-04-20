import unittest
from meeting_reservation import Meeting, Reservation

'''
    This test cases to validate the reservation with predifned time loads data from room.txt
'''
class TestReservationPre(unittest.TestCase):

    def prepare_data(self):

        meetings = {}
        with open('rooms.txt') as file:
            for room in file:
                details = room.strip().split(',')
                id = details[0]
                # predifned_time=
                meetings.update({float(id): Meeting(int(id.split('.')[0]), int(id.split('.')[1]), int(details[1]),[details[i] for i in range(2, len(details))])})
        return meetings

    def test_valid(self):
        meetings = self.prepare_data()

        reservation = Reservation(meetings, True)
        message = reservation.reserve(8, 5, '10:30','11:30')
        assert message == 'Reserved room 9.547'

    def test_unavailble(self):
        meetings = self.prepare_data()

        reservation = Reservation(meetings, True)
        reservation.reserve(8, 5, '10:30','11:30')
        message = reservation.reserve(8, 5, '10:30','11:30')
        assert message == 'No Rooms are available for Reservation'

    def test_reserve_more_people(self):
       array = [Meeting(1, 511, 8)]

       meeting_rooms = self.prepare_data()

       reservation = Reservation(meeting_rooms)
       message = reservation.reserve(8, 10,'10:30', '11:30')
       assert message == 'No rooms are available for 10 persons'
