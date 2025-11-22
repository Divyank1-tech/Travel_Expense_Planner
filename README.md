# Overview of the project
The Travel Expense Planner is a single, complete, command-line application written in python designed to track and manage trip finances. It features a menu-driven interface for logging expenses, setting budgets, and generating a detailed summary. Most importantly, it uses local JSON file handling to ensure data is saved automatically upon exit and loaded upon startup, providing state continuity for long-term trip planning.

# Features
While the implementation is in a single file, the code is logically divided into Three major functional areas to meet typical project requirements:
1. Data Input & Managment: Handels all user input validation, expense recording, category managment, and the setting of the globsl budget.
2. Data persistance (CRUD): Manages the reading and writing of the global state (EXPENSES and BUDGET) to the travel_expenses.json file. 
3. Reporting & Analytics: Calculates and formats the summary report, including total expense calculation, percentage breakdown, and budget variance tracking.

# Technologies/Tools Used 
1. Language: Python 3.x
2. Data Format: JSON (for data persistence)
3. Platform: Command Line Interface (CLI) 

# Non-Functional Requirements 
1. Usability: The system uses a simple, numbered menu system and clear currency symbol (%) for ease of use.
2. Error Handling: Input validation ( _get_validated_input ) prevents crashes from non-numeric or out-of-range data. File I/O operations include try...except blocks to handle errors during JSON readingMriting. 
3. Reliability: Data persistence ensures that no recorded expenses or the budget are lost when the program is properly exited, making the application reliable for long-duration trips.
4. Reliability: Data persistence ensures that no recorded expenses or the budget are lost when the program is properly exited, making the application reliable for long-duration trips. 

# Steps to Install & Run the Project 
1. Save File: Save the entire code block as
   
           travel_expense_planner.py 
   
3. Run: Open your command line or terminal, navigate to the directory where you saved the file, and execute:
   
            python travel_expense_planner.py
# Instructions for Testing 
Test the functional requirements, paying special attention to the persistence feature: 
1. Budget Test: Choose option 3 (Set Trip Budget) and enter 10000.
2. Expense Test: Choose option 1 (Add New Expense).
   Select 1. Accommodation and enter 4500.
   Select 3. Food & Dining andenter 1500. 
3. Summary Test: Choose option 2 (View Expense Summary). Verify the total is ₹6000.00.
4. Persistence Test (Crucial): Choose option 5 (Exit Planner). You should see a message confirming the data was saved to travel_expenses.json.
5. Rerun Test: Run the script again ( python travel_expense_planner .py ). The initial print message should confirm that the data (₹6000.00 expenses,₹10000.00 budget) was loaded successfully.
