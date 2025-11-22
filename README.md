# Overview of the project
The Travel Expense Planner is a single, complete, command-line application written in python designed to track and manage trip finances. It features a menu-driven interface for logging expenses, setting budgets, and generating a detailed summary. Most importantly, it uses local JSON file handling to ensure data is saved automatically upon exit and loaded upon startup, providing state continuity for long-term trip planning.

# Features ( Functional Requirements)
While the implementation is in a single file, the code is logically divided into Three major functional areas to meet typical project requirements:
1. Data Input & Managment: Handels all user input validation, expense recording, category managment, and the setting of the globsl budget.
2. Data persistance (CRUD): Manages the reading and writing of the global state (EXPENSES and BUDGET) to the travel_expenses.json file. 
