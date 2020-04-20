from datetime import datetime

class Meeting():
    '''
        Meeting room with floor, room number and reservation details
        It will try book the meeting rooms between 9AM-6PM if any predefined time
        Predefined time is the time where user can only select specific timelines
    '''
    def __init__(self, floor, room_number, size, predefined_time=None):
        self.floor = floor
        self.room_number = room_number
        self.size = size
        self.bookings = []
        self.predefined_time = predefined_time
        self.day_start = datetime.strptime('9:00', "%H:%M")
        self.day_ends = datetime.strptime('18:00', "%H:%M")


class Reservation():

    def __init__(self, meeting_rooms, predefined_time=False):
        self.day_start = datetime.strptime('9:00', "%H:%M")
        self.day_ends = datetime.strptime('18:00', "%H:%M")
        self.predefined_time = predefined_time
        self.meeting_rooms = meeting_rooms

    '''
        To validate whether the start and end is fall under 9PM-6PM
    '''
    def validation(self, start, end):
        if start>end or not self.day_start <= start < self.day_ends or not self.day_start < end <= self.day_ends:
        # if start>end or not self.day_start <= start < self.day_ends:
            return False
        return True

    '''
        To validate whether the start and end is fall under predifned by the respective room
    '''
    def validate_predefined_time(self, start, end, room_id):
        predefined_time = self.meeting_rooms.get(room_id).predefined_time
        flag = True
        is_valid = False
        if start>end:
            return False
        for time in predefined_time:

            if flag and start == time:
                flag = False
            elif not flag and end == time:
                is_valid = True
        return is_valid

    '''
        Iterate each booking from each floor and books nearest available meeting room
    '''
    def reserve(self, floor, no_of_persons, start, end):
        start_t = datetime.strptime(start, "%H:%M")
        end_t = datetime.strptime(end, "%H:%M")

        # In case predefined time, we should validate for each floor
        # So setting True to continue further validate for each room incase of predifned_time
        is_valid = True if self.predefined_time else self.validation(start_t, end_t)

        if not is_valid:
            raise Exception('Requested Time is invalid')

        reservation_message = None

        near_by_rooms = self.get_near_by_rooms(floor, no_of_persons)

        if not near_by_rooms:
            reservation_message = "No rooms are available for {} persons".format(no_of_persons)

        for room in near_by_rooms:

            # In case predefined time, this will validate for each room
            # So setting True to continue further validate incase predifned_time is not provided
            is_valid = self.validate_predefined_time(start, end, room) if self.predefined_time else True

            if not is_valid:
                continue

            bookings = self.meeting_rooms.get(room).bookings

            previous = self.day_start

            conflict = False
            reserved = False

            for i in range(len(bookings)):
                time = bookings[i]
                st = datetime.strptime(time[0], "%H:%M")
                en = datetime.strptime(time[1], "%H:%M")

                if start_t >= previous and start_t<st:
                    if end_t <= st:
                        bookings.insert(i,[start,end])
                        reservation_message = "Reserved room " + str(room)
                        reserved = True
                        break
                    else:
                        reservation_message = 'No Rooms are available for Reservation';
                        conflict = True
                        break
                elif start_t >= en:
                    previous = en
                else:
                    reservation_message = 'No Rooms are available for Reservation';
                    conflict = True
                    break

            if not conflict and not reserved:
                bookings.append([start,end])
                reservation_message = "Reserved room {}".format(room)
                reserved = True

            if reserved:
                break;

        return reservation_message

    def print_booking(self):
        for me in self.meeting_rooms:
            print('Floor %s booking are %s' %(me, self.meeting_rooms.get(me).bookings))

    '''
        Find out the meeting rooms on the same floor whcih can accommodate requested persons
        Plus Find out the meeting rooms in the other floors near by the requested floor and can accommodate requested persons
        Ex: if user from 10th floor and if the floors are 7, 8, 9, 10, 11, 12
        Then it creates list like 10, 11, 9, 12, 8, 7
        It will add same floor first, and first top floor, first down floor, second top floor, second down floor and so on
    '''
    def get_near_by_rooms(self, floor, no_of_persons):
        near_by_rooms = {}
        me_rooms = [*self.meeting_rooms]

        me_rooms.sort()

        i = None
        j = None

        # Add the meeting rooms which are in the same floor and number of persons available to attend
        skip = False
        for room in me_rooms:

            if int(room) == floor:

                if self.meeting_rooms.get(room).size >= no_of_persons:
                    near_by_rooms.update({room: self.meeting_rooms.get(room)})
                if not i:
                    i = me_rooms.index(room)-1
                skip = True
            if skip:
                j = me_rooms.index(room)
                break

        # Add the meeting rooms which are in the same floor and number of persons available to attend
        while i >= 0 or j < len(me_rooms):
            if i >= 0:
                room = me_rooms[i]

                if self.meeting_rooms.get(room).size >= no_of_persons:
                    near_by_rooms.update({room: self.meeting_rooms.get(room)})
                i = i-1
            if j < len(me_rooms):
                room = me_rooms[j]

                if self.meeting_rooms.get(room).size >= no_of_persons:
                    near_by_rooms.update({room: self.meeting_rooms.get(room)})
                j = j+1
        return near_by_rooms
