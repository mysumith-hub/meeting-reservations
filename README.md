# meeting-reservations

### Test cases to validate reservations with meeting room available for booking between 9PM-6PM
/> python3 -m unittest test_reservation.py


### Test cases to validate reservations with meeting room available only for certain timings for booking between
ex:
7.11,8,9:00,9:15,14:30,15:00
8.23,6,10:00,11:00,14:00,15:00
8.43,7,11:30,12:30,17:00,17:30
9.511,9,9:30,10:30,12:00,12:15,15:15,16:15
9.527,4,9:00,11:00,14:00,16:00
9.547,8,10:30,11:30,13:30,15:30,16:30,17:30

/> python3 -m unittest test_reservation_predefined.py

Explanation:
- For testing purpose Creating Meeting room and feeding to Reservations
- Meeting rooms are having floor, room number and number of persons it can accommodate
- First validate whether the give requested time is valid or not
- Find the nearest meeting rooms first which can accommodate the requested no of persons
  Ex: if user from 10th floor and if the floors are 7, 8, 9, 10, 11, 12
    Then it creates list like 10, 11, 9, 12, 8, 7
    It will add same floor first, and first top floor, first down floor, second top floor, second down floor and so on
- Iterate each booking from each room and validate the requested time is available or not
- If any conflict occur for floor look for another nearest room and so on.
- If any meeting room is available then add to the booking send the room id and skip iteration
- If no rooms found then send message about unavailability 

Regarding splitting meeting rooms if the rooms are available, Had some idea but didn't complete this

- One idea is minimum 1hr meeting to look for splitting (or can be change)
- If any room are not available.
- Get the rooms which are having some time available between the requested time
- Split and book based on either of two
    1. Book the more time available rooms first instead looking near floors first
    2. Book nearest floor based on availability
