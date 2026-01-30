from models.classroom import Classroom
from models.student import Student

oop = Classroom('OOP')
oop.add_student(Student(1, 'A', 20, 'A001'))
oop.add_student(Student(2, 'B', 20, 'A002'))
print(f'{len(oop)}')
oop.add_student(Student(3, 'C', 20, 'A003'))
print(f'{len(oop)}')
print(f'Student in the class:')
for i in range(len(oop)):
  print(oop[i])