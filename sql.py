import sqlite3

# Connecting to SQLite database
conn = sqlite3.connect('smartsched.db')
cursor = conn.cursor()

# Creating Student Table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Student (
    RegisterNumber INTEGER PRIMARY KEY,
    Name TEXT NOT NULL,
    Degree TEXT,
    Specialization TEXT,
    PreferredStudyTimes TEXT,
    SleepSchedule TEXT,
    DateOfJoining DATE
)
''')

# Creating Course Table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Course (
    CourseID INTEGER PRIMARY KEY,
    CourseName TEXT NOT NULL,
    Department TEXT,
    InstructorID INTEGER,
    Credits INTEGER
)
''')

# Creating EnrolledIn Table (Many-to-Many Relationship)
cursor.execute('''
CREATE TABLE IF NOT EXISTS EnrolledIn (
    RegisterNumber INTEGER,
    CourseID INTEGER,
    PRIMARY KEY (RegisterNumber, CourseID),
    FOREIGN KEY (RegisterNumber) REFERENCES Student(RegisterNumber) ON DELETE CASCADE,
    FOREIGN KEY (CourseID) REFERENCES Course(CourseID) ON DELETE CASCADE
)
''')

# Creating Timetable Table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Timetable (
    TimetableID INTEGER PRIMARY KEY,
    CourseID INTEGER,
    StartTime TIME,
    EndTime TIME,
    EventName TEXT,
    FOREIGN KEY (CourseID) REFERENCES Course(CourseID) ON DELETE CASCADE
)
''')

# Creating Assignments Table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Assignments (
    AssignmentID INTEGER PRIMARY KEY,
    CourseID INTEGER,
    Weightage INTEGER,
    DueDate DATE,
    FOREIGN KEY (CourseID) REFERENCES Course(CourseID) ON DELETE CASCADE
)
''')

# Creating Reminder and Notifications Table
cursor.execute('''
CREATE TABLE IF NOT EXISTS ReminderAndNotifications (
    ReminderID INTEGER PRIMARY KEY,
    RegisterNumber INTEGER,
    AssignmentID INTEGER,
    StatusPending BOOLEAN,
    ReminderTime DATETIME,
    Message TEXT,
    FOREIGN KEY (RegisterNumber) REFERENCES Student(RegisterNumber) ON DELETE CASCADE,
    FOREIGN KEY (AssignmentID) REFERENCES Assignments(AssignmentID) ON DELETE CASCADE
)
''')

# Inserting Data into Student Table
cursor.executemany('''
INSERT INTO Student (RegisterNumber, Name, Degree, Specialization, PreferredStudyTimes, SleepSchedule, DateOfJoining)
VALUES (?, ?, ?, ?, ?, ?, ?)
''', [
    (1, 'Krish', 'B.Tech', 'Data Science', 'Morning', 'Regular', '2022-08-01'),
    (2, 'Darius', 'B.Tech', 'Data Science', 'Evening', 'Irregular', '2022-08-01'),
    (3, 'Sudhanshu', 'B.Tech', 'DevOps', 'Afternoon', 'Regular', '2022-08-01'),
    (4, 'Vikash', 'B.Tech', 'Data Science', 'Night', 'Regular', '2022-08-01')
])

# Inserting Data into Course Table
cursor.executemany('''
INSERT INTO Course (CourseID, CourseName, Department, InstructorID, Credits)
VALUES (?, ?, ?, ?, ?)
''', [
    (101, 'Machine Learning', 'CSE', 1, 4),
    (102, 'Blockchain', 'CSE', 2, 3),
    (103, 'Cybersecurity', 'CSE', 3, 3),
    (104, 'Cloud Computing', 'CSE', 4, 3)
])

# Inserting Data into EnrolledIn Table
cursor.executemany('''
INSERT INTO EnrolledIn (RegisterNumber, CourseID)
VALUES (?, ?)
''', [
    (1, 101), (1, 102), 
    (2, 103), (3, 104), 
    (4, 101), (4, 103)
])

# Inserting Data into Timetable Table
cursor.executemany('''
INSERT INTO Timetable (TimetableID, CourseID, StartTime, EndTime, EventName)
VALUES (?, ?, ?, ?, ?)
''', [
    (1, 101, '10:00', '11:30', 'Lecture'),
    (2, 102, '12:00', '13:30', 'Lab'),
    (3, 103, '14:00', '15:30', 'Lecture'),
    (4, 104, '16:00', '17:30', 'Lab')
])

# Inserting Data into Assignments Table
cursor.executemany('''
INSERT INTO Assignments (AssignmentID, CourseID, Weightage, DueDate)
VALUES (?, ?, ?, ?)
''', [
    (1, 101, 20, '2023-03-10'),
    (2, 102, 30, '2023-03-15'),
    (3, 103, 25, '2023-03-20'),
    (4, 104, 40, '2023-03-25')
])

# Inserting Data into ReminderAndNotifications Table
cursor.executemany('''
INSERT INTO ReminderAndNotifications (ReminderID, RegisterNumber, AssignmentID, StatusPending, ReminderTime, Message)
VALUES (?, ?, ?, ?, ?, ?)
''', [
    (1, 1, 1, 1, '2023-03-08 10:00:00', 'Submit ML Assignment'),
    (2, 2, 2, 0, '2023-03-13 12:00:00', 'Blockchain Assignment Due'),
    (3, 3, 3, 1, '2023-03-18 14:00:00', 'Cybersecurity Assignment Pending'),
    (4, 4, 4, 0, '2023-03-23 16:00:00', 'Cloud Computing Submission')
])

# Display Data from Student Table
print("\n📌 Students Table:")
for row in cursor.execute('SELECT * FROM Student'):
    print(row)

# Display Data from Course Table
print("\n📌 Courses Table:")
for row in cursor.execute('SELECT * FROM Course'):
    print(row)

# Display Data from EnrolledIn Table
print("\n📌 EnrolledIn Table:")
for row in cursor.execute('SELECT * FROM EnrolledIn'):
    print(row)

# Display Data from Assignments Table
print("\n📌 Assignments Table:")
for row in cursor.execute('SELECT * FROM Assignments'):
    print(row)

# Display Data from Reminders Table
print("\n📌 ReminderAndNotifications Table:")
for row in cursor.execute('SELECT * FROM ReminderAndNotifications'):
    print(row)

# Commit and Close Connection
conn.commit()
conn.close()
