from dotenv import load_dotenv
load_dotenv() # load all env variables
import streamlit as st 
import os 
import sqlite3 

import google.generativeai as genai 

## to configure api key

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load Google Gemini Model and Provide sql query as response

def get_gemini_response(question,prompt):
    model=genai.GenerativeModel('gemini-1.5-flash') 
    response=model.generate_content([prompt[0],question])
    return response.text


# Function to retrieve query from the sql database 

def read_sql_query(sql,db):
    conn=sqlite3.connect(db)
    cur=conn.cursor()
    cur.execute(sql)
    rows=cur.fetchall()
    conn.commit()
    conn.close()
    for row in rows : 
        print(row)
    return rows


prompt = [
    """
    You are an expert in converting English questions to SQL queries!  
    The SQL database is named SMARTSCHED and contains the following tables:

    1. **STUDENT** (RegisterNumber, Name, Degree, Specialization, PreferredStudyTimes, SleepSchedule, DateOfJoining)
    2. **COURSE** (CourseID, CourseName, Department, InstructorID, Credits)
    3. **ENROLLEDIN** (RegisterNumber, CourseID) [Tracks student-course enrollments]
    4. **TIMETABLE** (TimetableID, CourseID, StartTime, EndTime, EventName)
    5. **ASSIGNMENTS** (AssignmentID, CourseID, Weightage, DueDate)
    6. **REMINDERANDNOTIFICATIONS** (ReminderID, RegisterNumber, AssignmentID, StatusPending, ReminderTime, Message)

    The chatbot should generate **SQL queries** for retrieving, inserting, updating, and deleting records as per user requests.

    ### **Examples of Queries:**
    
    **-> Retrieving Data**
    
    - **"Show me all students in the Computer Science degree."**  
      → `SELECT * FROM STUDENT WHERE Degree = 'Computer Science';`

    - **"What assignments are due for a student named Rohan?"**  
      → `SELECT ASSIGNMENTS.AssignmentID, ASSIGNMENTS.CourseID, ASSIGNMENTS.DueDate FROM ASSIGNMENTS JOIN REMINDERANDNOTIFICATIONS ON ASSIGNMENTS.AssignmentID = REMINDERANDNOTIFICATIONS.AssignmentID JOIN STUDENT ON REMINDERANDNOTIFICATIONS.RegisterNumber = STUDENT.RegisterNumber WHERE STUDENT.Name = 'Rohan' AND REMINDERANDNOTIFICATIONS.StatusPending = TRUE ORDER BY ASSIGNMENTS.DueDate ASC;`

    **-> Adding Data**
    
    - **"Enroll Rohan in the Machine Learning course."**  
      → `INSERT INTO ENROLLEDIN (RegisterNumber, CourseID) VALUES ((SELECT RegisterNumber FROM STUDENT WHERE Name = 'Rohan'), (SELECT CourseID FROM COURSE WHERE CourseName = 'Machine Learning'));`

    - **"Add a new course called 'Blockchain Technology' under the Computer Science department with 4 credits."**  
      → `INSERT INTO COURSE (CourseName, Department, Credits) VALUES ('Blockchain Technology', 'Computer Science', 4);`

    **-> Updating Data**
    
    - **"Change Rohan’s specialization to 'Artificial Intelligence'."**  
      → `UPDATE STUDENT SET Specialization = 'Artificial Intelligence' WHERE Name = 'Rohan';`

    - **"Mark all assignments as completed for Rohan."**  
      → `UPDATE REMINDERANDNOTIFICATIONS SET StatusPending = FALSE WHERE RegisterNumber = (SELECT RegisterNumber FROM STUDENT WHERE Name = 'Rohan');`

    **->Deleting Data**
    
    - **"Remove Rohan from the Machine Learning course."**  
      → `DELETE FROM ENROLLEDIN WHERE RegisterNumber = (SELECT RegisterNumber FROM STUDENT WHERE Name = 'Rohan') AND CourseID = (SELECT CourseID FROM COURSE WHERE CourseName = 'Machine Learning');`

    - **"Delete all reminders for completed assignments."**  
      → `DELETE FROM REMINDERANDNOTIFICATIONS WHERE StatusPending = FALSE;`

    **Guidelines:**  
    - Ensure the output is **only the SQL query** (no markdown formatting, no backticks).  
    - Do not include the word "SQL" in the response.  
    - Maintain **referential integrity** when inserting, updating, or deleting records.  
    """
]

 #Stream Lit App 

st.set_page_config(page_title="Hey! I'm SmartSched")
st.header("Let me help you with your schedule : ) ")
question=st.text_input("Input: ",key="input")
submit=st.button("Ask the question : ")

# if submit is clicked 
if submit:
    response=get_gemini_response(question,prompt)
    print(response)
    data=read_sql_query(response,"smartsched.db")
    st.subheader("The Response is : ")
    for row in data : 
        print(row)
        st.header(row)

