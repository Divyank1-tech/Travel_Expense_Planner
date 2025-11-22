import time
import json
import os      # Used for checking if the data file exists

# --- Configuration ---
DATA_FILE_PATH = "travel_expenses.json"

# --- Global State ---
# Dictionary to hold expenses. Key: Category Name, Value: Total Amount Spent
EXPENSES = {
    "Accommodation": 0.0,
    "Transportation": 0.0,
    "Food & Dining": 0.0,
    "Activities & Sightseeing": 0.0,
    "Miscellaneous": 0.0
}

# Global variable for the total trip budget (Rupees)
BUDGET = 0.0

# --- Data Persistence Functions ---

def load_data():
    """
    Loads expenses and budget from the JSON file if it exists.
    Initializes global EXPENSES and BUDGET.
    """
    global EXPENSES, BUDGET
    if os.path.exists(DATA_FILE_PATH):
        try:
            with open(DATA_FILE_PATH, 'r') as f:
                data = json.load(f)
                
                # Load EXPENSES, merging with default categories if necessary
                loaded_expenses = data.get('expenses', {})
                
                # Update EXPENSES with loaded data, preserving default categories if missing
                # This handles cases where new categories were added in the previous session
                EXPENSES.clear()
                EXPENSES.update(loaded_expenses)
                
                # Load BUDGET
                BUDGET = data.get('budget', 0.0)
            
            print(f" Data loaded successfully from {DATA_FILE_PATH}. Budget: ₹{BUDGET:.2f}")
            print(f"Loaded {len(EXPENSES)} expense categories.")
            
        except (IOError, json.JSONDecodeError) as e:
            print(f" Warning: Could not read or decode existing data file. Starting fresh. Error: {e}")
            # Resetting to default state
            EXPENSES.update({
                "Accommodation": 0.0, "Transportation": 0.0, "Food & Dining": 0.0,
                "Activities & Sightseeing": 0.0, "Miscellaneous": 0.0
            })
            BUDGET = 0.0
    else:
        print(f"ℹ No existing data file found at {DATA_FILE_PATH}. Starting fresh.")

def save_data():
    """
    Saves the current expenses and budget to the JSON file.
    """
    global EXPENSES, BUDGET
    data = {
        'expenses': EXPENSES,
        'budget': BUDGET
    }
    try:
        with open(DATA_FILE_PATH, 'w') as f:
            json.dump(data, f, indent=4)
        print(f" All current data saved successfully to {DATA_FILE_PATH}.")
    except IOError as e:
        print(f" Error: Could not save data to file. Changes will be lost. Error: {e}")

# --- Input Utility Function ---

def _get_validated_input(prompt, data_type, min_val=None, max_val=None):
    while True:
        try:
            # Handle potential EOFError in restricted environments
            user_input = input(prompt)
        except EOFError:
            print("\nError: Input stream unavailable. Shutting down.")
            return None

        try:
            value = data_type(user_input)
            
            # Check constraints
            if min_val is not None and value < min_val:
                print(f"Input must be at least {min_val}.")
                continue
            if max_val is not None and value > max_val:
                print(f"Input must not exceed {max_val}.")
                continue
                
            return value
        except ValueError:
            type_name = "whole number" if data_type is int else "decimal number"
            print(f"Invalid input. Please enter a valid {type_name}.")

# --- Feature Handlers ---

def set_budget():
    """
    Allows the user to set or update the total trip budget.
    """
    global BUDGET
    print("\n--- Set Trip Budget ---")
    # Use ₹ currency symbol in the prompt
    new_budget = _get_validated_input("Enter the total trip budget (e.g., 50000.00): ₹", float, min_val=0.0)
    
    if new_budget is not None:
        BUDGET = new_budget
        print(f" Trip budget set to ₹{BUDGET:.2f}.")

def manage_categories():
    """
    Allows the user to add new custom expense categories.
    """
    global EXPENSES
    print("\n--- Manage Categories ---")
    print("1. Add New Category")
    
    choice = _get_validated_input("Enter your choice (1 to Add, or 0 to cancel): ", int, min_val=0, max_val=1)
    
    if choice == 1:
        category_name = input("Enter the name of the new category (e.g., 'Souvenirs'): ").strip()
        
        if not category_name:
            print("Category name cannot be empty.")
            return

        if category_name in EXPENSES:
            print(f"Category '{category_name}' already exists.")
        else:
            EXPENSES[category_name] = 0.0
            print(f" Category '{category_name}' added successfully.")
    elif choice == 0:
        print("Category management cancelled.")

def add_expense():
    """
    Prompts the user to add an expense amount to a specific category.
    """
    global EXPENSES
    print("\n--- Add New Expense ---")
    
    # Display categories dynamically (includes newly added ones)
    categories = list(EXPENSES.keys())
    print("Available Categories:")
    for i, category in enumerate(categories):
        print(f"  {i+1}. {category}")

    # 1. Get Category Choice
    max_choice = len(categories)
    
    choice = _get_validated_input(
        f"Enter the number of the category (1-{max_choice}, or 0 to cancel): ",
        int,
        min_val=0,
        max_val=max_choice
    )
    
    if choice is None: return
    if choice == 0:
        print("Expense addition cancelled.")
        return

    category_name = categories[choice - 1]

    # 2. Get Amount
    amount = _get_validated_input(
        f"Enter the amount for {category_name} (e.g., 55.50): ₹", 
        float,
        min_val=0.0
    )
    
    if amount is None: return

    # Update the expense dictionary
    EXPENSES[category_name] += amount
    print(f"\n Added ₹{amount:.2f} to {category_name}.")

# --- Reporting Function ---

def show_summary():
    """
    Calculates and displays the total expenses, breakdown by category, and budget status.
    """
    global EXPENSES, BUDGET
    print("\n==================================")
    print("      TRAVEL EXPENSE SUMMARY      ")
    print("==================================")
    
    total_expense = sum(EXPENSES.values())
    
    if total_expense == 0:
        print("No expenses recorded yet.")
        if BUDGET > 0:
            print(f"Trip Budget Set: ₹{BUDGET:10.2f}")
        print("==================================\n")
        return

    # Display breakdown
    print("\n--- Breakdown by Category ---")
    for category, amount in EXPENSES.items():
        if amount > 0:
            percentage = (amount / total_expense) * 100
            # Display amount in Rupees
            print(f"{category:<25} : ₹{amount:10.2f} ({percentage:5.1f}%)")

    # Display total
    print("-" * 34)
    print(f"TOTAL SPENT EXPENSES: ₹{total_expense:10.2f}")
    
    # Budget Tracking Section
    if BUDGET > 0:
        remaining = BUDGET - total_expense
        print("\n--- Budget Tracking ---")
        print(f"Trip Budget Set:    ₹{BUDGET:10.2f}")
        
        if remaining >= 0:
            print(f"Amount Remaining:   ₹{remaining:10.2f} (Under Budget)")
        else:
            # Show the absolute value of the amount over budget
            print(f"Amount OVER Budget: ₹{abs(remaining):10.2f} (Over Budget)")

    print("==================================\n")

# --- Main Application Loop ---

def main_menu():
    """
    Main loop for the expense planner application.
    """
    print("Welcome to the Simple Travel Expense Planner!")
    load_data() # Load data when the application starts
        
    while True:
        time.sleep(0.5)
        print("\n--- Main Menu ---")
        print("1. Add New Expense")
        print("2. View Expense Summary")
        print("3. Set Trip Budget")
        print("4. Manage Categories")
        print("5. Exit Planner")
        
        choice = _get_validated_input("Enter your choice (1-5): ", int, min_val=1, max_val=5)

        if choice is None:
            choice = 5 # Treat input failure as exit
        
        if choice == 1:
            add_expense()
        elif choice == 2:
            show_summary()
        elif choice == 3:
            set_budget()
        elif choice == 4:
            manage_categories()
        elif choice == 5:
            save_data() # Save data when the user chooses to exit
            print("\nThank you for using the planner!")
            break

if __name__ == "__main__":
    main_menu()