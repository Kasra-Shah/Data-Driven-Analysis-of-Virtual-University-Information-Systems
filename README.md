# Data-Driven-Analysis-of-Virtual-University-Information-Systems
Virtual Classroom Data Analysis System
A comprehensive data analysis project using Pandas and Matplotlib to process and visualize data from a university's virtual learning platform (Vopinar). The system generates detailed reports and insightful charts for students, professors, and courses based on raw Excel data.

![Linear Regression Results](https://github.com/Kasra-Shah/Data-Driven-Analysis-of-Virtual-University-Information-Systems/raw/main/virtual-calsses-data-analyses.png)

📖 Project Overview
This project simulates a backend analysis system for a university's e-learning platform. Given a structured Excel file containing sheets for students, professors, courses, and session timings, the program provides an interactive menu to generate various reports and visualizations. It demonstrates strong skills in data wrangling, aggregation, and visualization using Python's data science stack.

🛠️ Tech Stack
Language: Python

Libraries:

pandas - For data manipulation and analysis

numpy - For numerical operations

matplotlib - For generating plots and charts

Data Source: Multi-sheet Excel file (.xlsx)

📊 Data Structure
The program processes an Excel file with the following sheets:

Sheet1: Master list linking students, professors, and courses (Faculties, Groups, Professor Names/IDs, Course Names/Codes, Student Names/IDs, Credits).

Sheet2: Session details (Session ID, Date, Course Code, Start Time, End Time).

🚀 Features & Functionality
The system presents an interactive menu with the following options:

1. Professor Report: Input a Professor ID. Generates a per-course report including:
Total sessions taught
Total and average session duration
Longest and shortest session times

2. Student Performance Report: Input a Student ID. Generates a per-course report including:
Number of presences/absences
Total delay minutes (tardy entry)
Total early departure minutes
A calculated performance score (Score = (Presences * 90) - Delays - Early Departures)

3. Course Report: Input a Course ID. Provides statistics like:
Number of sessions held
Average/Max number of present/absent students per session
Total and average session duration

4. Session Duration Bar Chart: Input a Course ID. Plots a bar chart with session dates on the x-axis and session duration on the y-axis.

5. Professor's Course Pie Chart: Input a Professor ID. Creates a pie chart showing the ratio of (Total Session Time) / (Sessions Held * Credits * 45) for each course they teach.

6. Comparative Professor Bar Chart: Input a list of Professor IDs. Generates a stacked bar chart comparing the total session time per course for each professor.

7. Student Comparison Scatter Plot: Input a list of Student IDs. Creates a bubble chart for common courses:
Y-axis: Course names
X-axis: Student names
Bubble size: Total time present
Bubble color: Number of absences (Green: <4, Yellow: 4-7, Red: >=8)

8. Generate Excel Report: Creates a new Excel file (Report.xlsx) with two sheets:
Sheet1: List of students with more than 4 absences in any course.
Sheet2: List of professors who have not held any sessions.

🏃‍♂️ How to Run the Code
Clone the repository:
git clone https://github.com/Kasra-Shah/Data-Driven-Analysis-of-Virtual-University-Information-Systems.git
cd vopinar-data-analys
is
Install required packages: It is highly recommended to use a virtual environment.
pip install pandas numpy matplotlib openpyxl

Prepare your data: Place your Excel data file (e.g., database.xlsx) in the project directory.

Run the main script:
Data-Driven-Analysis-of-Virtual-University.py
Use the menu: Follow the interactive menu prompts in the terminal to generate reports and visualizations.

📁 Repository Structure
text
vopinar-data-analysis/
├── data/
│   └── database.xlsx                 # Input Excel data file (must be provided by user)
├── src/
│   ├── Data-Driven-Analysis-of-Virtual-University.py     # Main script with the interactive menu and function calls
├── output/
│   └── Report.xlsx               # Generated Excel report (created after running option 8)
└── README.md                     # This file
👨‍💻 Author
Kasra Shahriari

📜 License
This project was created for an academic assignment.
