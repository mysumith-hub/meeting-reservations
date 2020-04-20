import unittest
from meeting_reservation import Meeting, Reservation
'''
    This test cases to validate the reservation with no predifned.
    Means Reservation from 9PM-6PM
'''
class TestReservation(unittest.TestCase):

    # prepare the test data
    def prepare(self,array):
        meetings = {}
        for ar in array:
            id = float("{}.{}".format(ar.floor, ar.room_number))
            meetings.update({id:ar})
        return meetings

    def test_reserve(self):
        array = [
        Meeting(1, 511, 8),
        Meeting(2, 512, 9),
        Meeting(3, 513, 7),
        ]
        meeting_rooms = self.prepare(array)
        reservation = Reservation(meeting_rooms)
        message = reservation.reserve(1, 9,'10:30', '11:30')
        assert message == 'Reserved room 2.512'

    def test_reserve_start_time_unavailable(self):
        array = [
        Meeting(1, 511, 8),
        Meeting(2, 512, 9)
        ]
        meeting_rooms = self.prepare(array)
        reservation = Reservation(meeting_rooms)
        reservation.reserve(1, 9,'10:30', '11:30')
        message = reservation.reserve(2, 9,'10:30', '11:30')
        assert message == 'No Rooms are available for Reservation'

    def test_reserve_end_time_unavailable(self):
        array = [
        Meeting(1, 511, 8),
        Meeting(2, 512, 9)
        ]
        meeting_rooms = self.prepare(array)
        reservation = Reservation(meeting_rooms)
        reservation.reserve(1, 9,'10:30', '11:30')
        message = reservation.reserve(2, 9,'9:30', '11:30')
        assert message == 'No Rooms are available for Reservation'

    def test_reserve_more_people(self):
        array = [Meeting(1, 511, 8)]

        meeting_rooms = self.prepare(array)

        reservation = Reservation(meeting_rooms)
        message = reservation.reserve(1, 10,'10:30', '11:30')
        assert message == 'No rooms are available for 10 persons'

    def test_reserve_exception(self):
        array = [Meeting(1, 511, 8)]
        meeting_rooms = self.prepare(array)
        reservation = Reservation(meeting_rooms)

        with self.assertRaises(Exception) as e:
            assert str(e)==reservation.reserve(1, 8,'1:30', '11:30')
