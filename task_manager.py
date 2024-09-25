import datetime

# File names for user data and task data
filename_user = 'user.txt'
filename_tasks = 'tasks.txt'

# Dictionaries to store user data (username: password) and list to store task data
users = {}
tasks = []


# Function to read user data from the file
def read_user_data():
    try:
        with open(filename_user, 'r') as file:
            for line in file: 
                # Split each line by comma and stripping extra spaces to get username and password
                username, password = line.strip().split(', ')  
                users[username] = password  
    except FileNotFoundError:  
        print("User file not found.")


# Function to read task data from the file
def read_task_data():
    try:
        with open(filename_tasks, 'r') as file:
            for line in file: 
                # Split each line by comma and add to the tasks list
                tasks.append(line.strip().split(', '))
    except FileNotFoundError:  
        print("Tasks file not found.")


# Function for user login
def login():
    while True:
        username = input("Enter username: ")  
        password = input("Enter password: ")  
        if username in users and users[username] == password:  
            print("Login successful.")  
            return username  
        else:
            print("Invalid username or password.")


# Function to register a new user
def register_user(username, password):
    if username == 'admin' and password == 'adm1n':  
        new_username = input("Enter new username: ")  
        if new_username in users:  
            print("Username already exists.")  
        else:
            new_password = input("Enter new password: ")  
            confirm_password = input("Confirm password: ")  
            if new_password == confirm_password:  
                try:
                    with open(filename_user, 'a') as file:  
                        file.write(f"\n{new_username}, {new_password}")  
                    print("User registered successfully.")  
                    users[new_username] = new_password  
                except IOError:  
                    print("Error writing to user file.")
            else:
                print("Passwords do not match.")
    else:
        print("Only 'admin' can register users.")


# Function to add a new task
def add_task():
    username = input("Enter the username of the person the task is assigned to: ")
    title = input("Enter the title of the task: ")
    description = input("Enter the description of the task: ")
    due_date = input("Enter the due date of the task (YYYY-MM-DD): ")
    assigned_date = datetime.datetime.now().strftime("%Y-%m-%d")
    task_completed = "No"
    task = [username, title, description, assigned_date, due_date, task_completed]
    try:
        with open(filename_tasks, 'a') as file:
            # Write task details to file
            file.write(", ".join(task) + "\n")
        print("Task added successfully.")
    except IOError:
        print("Error writing to tasks file.")

def view_all_tasks():
    if not tasks:  # Check if tasks list is empty
        print("No tasks found.")  # Print message if no tasks found
    else:
        for task in tasks:  # Loop through each task in tasks list
            # Print task details: username, title, description, assigned date, due date, completion status
            print("\nAssigned to:", task[0])
            print("Title:", task[1])
            print("Description:", task[2])
            print("Assigned Date:", task[3])
            print("Due Date:", task[4])
            print("Completed:", task[5])
        


# Function to view tasks assigned to the logged-in user
def view_my_tasks():
    user_tasks = [task for task in tasks if task[0] == username]
    if not user_tasks:
        print("No tasks found for this user.")
    else:
        while True:
            print("\nYour Tasks:")
            for i, task in enumerate(user_tasks, 1):
                # Print task details: title, due date, and completion status
                print(f"{i}. Title: {task[1]}, Due Date: {task[4]}, Completed: {task[5]}")
            print("\nEnter the task number to interact with it, or '-1' to return to the main menu.")
            choice = input("Your choice: ")
            if choice == '-1':
                break
            elif choice.isdigit():
                choice = int(choice)
                if 1 <= choice <= len(user_tasks):
                    task_index = choice - 1
                    task = user_tasks[task_index]
                    print("\nSelected Task:")
                    print(f"Title: {task[1]}")
                    print(f"Description: {task[2]}")
                    print(f"Assigned Date: {task[3]}")
                    print(f"Due Date: {task[4]}")
                    print(f"Completed: {task[5]}")
                    print("\nOptions:")
                    print("1. Mark as Complete")
                    print("2. Edit Task")
                    option = input("Enter option number: ")
                    if option == '1':
                        if task[5] == 'No':
                            tasks[tasks.index(task)][5] = 'Yes'
                            print("Task marked as complete.")
                        else:
                            print("Task is already marked as complete.")
                    elif option == '2':
                        if task[5] == 'No':
                            new_username = input("Enter new username (leave blank to keep current): ")
                            new_due_date = input("Enter new due date (YYYY-MM-DD, leave blank to keep current): ")
                            if new_username:
                                tasks[tasks.index(task)][0] = new_username
                            if new_due_date:
                                tasks[tasks.index(task)][4] = new_due_date
                            print("Task edited successfully.")
                        else:
                            print("Task cannot be edited once marked as complete.")
                    else:
                        print("Invalid option.")
                else:
                    print("Invalid task number.")
            else:
                print("Invalid input. Please enter a number.")


# Function to display statistics
def display_statistics():
    total_tasks = len(tasks)  # Get total number of tasks
    total_users = len(users)  # Get total number of users
    print(f"Total number of tasks: {total_tasks}")  # Print total number of tasks
    print(f"Total number of users: {total_users}")  # Print total number of users

    try:
        with open('task_overview.txt', 'r') as file:  # Open task overview report file
            print("\nTask Overview Report:")
            print(file.read())  # Print contents of the report
    except FileNotFoundError:
        print("Task overview report not found.")

    try:
        with open('user_overview.txt', 'r') as file:  # Open user overview report file
            print("\nUser Overview Report:")
            print(file.read())  # Print contents of the report
    except FileNotFoundError:
        print("User overview report not found.")

# Function to generate reports
def generate_reports():
    total_tasks = len(tasks)  # Get total number of tasks
    total_completed_tasks = sum(1 for task in tasks if task[5] == 'Yes')  # Count total completed tasks
    total_incomplete_tasks = total_tasks - total_completed_tasks  # Calculate total incomplete tasks
    incomplete_percentage = (total_incomplete_tasks / total_tasks) * 100 if total_tasks > 0 else 0  # Calculate incomplete tasks percentage

    user_statistics = {}  # Initialize dictionary to store user statistics

    for user in users:  # Loop through each user
        user_tasks = [task for task in tasks if task[0] == user]  # Filter tasks assigned to the user
        total_user_tasks = len(user_tasks)  # Get total number of tasks assigned to the user
        total_user_completed_tasks = sum(1 for task in user_tasks if task[5] == 'Yes')  # Count total completed tasks for the user
        total_user_incomplete_tasks = total_user_tasks - total_user_completed_tasks  # Calculate total incomplete tasks for the user
        user_incomplete_percentage = (total_user_incomplete_tasks / total_user_tasks) * 100 if total_user_tasks > 0 else 0  # Calculate incomplete tasks percentage for the user
        user_completed_percentage = (total_user_completed_tasks / total_user_tasks) * 100 if total_user_tasks > 0 else 0  # Calculate completed tasks percentage for the user

        # Store user statistics in the dictionary
        user_statistics[user] = {
            'total_tasks': total_user_tasks,
            'incomplete_percentage': user_incomplete_percentage,
            'completed_percentage': user_completed_percentage,
        }

    with open('task_overview.txt', 'w') as file:  # Open file to write task overview
        file.write("Task Overview\n")
        file.write("--------------\n")
        file.write(f"Total number of tasks: {total_tasks}\n")
        file.write(f"Total number of completed tasks: {total_completed_tasks}\n")
        file.write(f"Total number of uncompleted tasks: {total_incomplete_tasks}\n")
        file.write(f"Percentage of tasks that are incomplete: {incomplete_percentage:.2f}%\n")

    with open('user_overview.txt', 'w') as file:  # Open file to write user overview
        file.write("User Overview\n")
        file.write("--------------\n")
        file.write(f"Total number of users: {len(users)}\n")
        for user, stats in user_statistics.items():  # Loop through user statistics
            file.write(f"\nUser: {user}\n")
            file.write(f"Total number of tasks assigned to {user}: {stats['total_tasks']}\n")
            file.write(f"Percentage of total tasks assigned to {user}: {(stats['total_tasks'] / total_tasks) * 100:.2f}%\n")
            file.write(f"Percentage of completed tasks for {user}: {stats['completed_percentage']:.2f}%\n")
            file.write(f"Percentage of incomplete tasks for {user}: {stats['incomplete_percentage']:.2f}%\n")



def main():
    read_user_data()  # Call function to read user data
    read_task_data()  # Call function to read task data
    global username  # Declare global variable for username
    username = login()  # Call function for user login

    while True:  
        # Display menu based on user type
        if username == 'admin':
            menu = input('''\nSelect one of the following options:
r - register a user
a - add task
va - view all tasks
vm - View mine                         
s - display statistics
gr - generate reports
e - exit
: ''').lower()  # Prompt user to select an option
        else:
            menu = input('''\nSelect one of the following options:
a - add task
va - view all tasks
vm - view mine
e - exit                         
: ''').lower()  # Prompt user to select an option

        if menu == 'r':  # Check if user chose to register a user
            register_user(username, users[username])  # Call function to register a user
        elif menu == 'a':  # Check if user chose to add a task
            add_task()  # Call function to add a task
        elif menu == 'va':  # Check if user chose to view all tasks
            view_all_tasks()  # Call function to view all tasks
        elif menu == 'vm':  # Check if user chose to view their tasks
            view_my_tasks()  # Call function to view user tasks
        elif menu == 's':  # Check if user chose to display statistics
            display_statistics()  # Call function to display statistics
        elif menu == 'gr':  # Check if user chose to generate reports
            generate_reports()  # Call function to generate reports
            print("Reports generated successfully.")  # Print reports generated successfully message
        elif menu == 'e':  # Check if user chose to exit
            print('Goodbye!!!')  # Print goodbye message
            break  # Exit the loop
        else:
            print("You have entered an invalid input. Please try again")  # Print message for invalid input

# Call main function
if __name__ == "__main__":
    main()
