class Person:
  def __init__(self, pid, name, age):
    self.pid = pid
    self.name = name
    self.age = age

class Student(Person):
  def __init__(self, pid, name, age, student_id):
    super().__init__(pid, name, age)
    self.student_id = student_id

class Staff(Person):
  def __init__(self, pid, name, age, staff_id):
    super().__init__(pid, name, age)
    self.student_id = staff_id

def main():
  student = Student('1234567890', 'pitcha', '18','0123')
  staff = Staff('1234567890', 'pitcha', '20','0123')
  print(f'Name {student.name}, Age {student.age}')
  print(f'Name {staff.name}, Age {staff.age}')

def get_person_info(person):
  return f'Name {person.name}, Age {person.age}'

if __name__ == "__main__":
    main()