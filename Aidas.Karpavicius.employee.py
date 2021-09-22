# student name: Aidas Karpavicius
# student no: R00171054
# Program description
# Employee managing system, that uses file "employees.txt" for storing all data.
from employee import Employee  # Employee class
import sys, datetime  # sys library for proper exit in case "employees.txt" wrong format

# datetime library to get current year for bonus file name

DATA_FILE = "employees.txt"  # file name in which all data is stored
emp_data = []  # list of all employees
# menu_str - menu string
menu_str = '''
1. View all employees.
2. Find employee.
3. Edit the salary of an employee.
4. Add a new employee.
5. Delete an employee.
6. Give a bonus to each employee.
7. Generate a report.
8. Save and quit.

Choice: '''


def clear_screen():
    """Clears screen"""
    print("\n" * 60)


def load_data():
    """load data() loads employee list from "employees.txt"
    if file not formatted by convention "id, name, surname, email, salary"
    function detects file as corrupted and asks weather to overwrite it,
    also if "employees.txt not found one will be created"""
    # tries to read a file, if "employees.txt" doesnt exist
    # creates one
    try:
        file_Handle = open(DATA_FILE, "r")
    except FileNotFoundError:
        input(DATA_FILE + " not found, press enter to create a file... ")
        file_Handle = open(DATA_FILE, "w")
        file_Handle.close()
        return  # if file not found exits here
    # try block read file if its proper format
    # if it's not formatted properly askes user should it
    # be overwritten
    try:
        for entry in file_Handle:
            if entry:
                employee = [value.strip() for value in
                            entry.split(",")]  # splits every line in file and stores it in []
                # creates Employee object and appends it to emp_data
                emp_data.append(Employee(employee[0], employee[1], employee[2], employee[3], float(employee[4])))
    except IndexError:
        print(DATA_FILE + " appears to be corrupted...")
        # inp just if there's any value in it it will exit program preventing "employees.txt" deletion
        inp = input("Press enter to continue (current database will be overwritten) or \"N\" to cancel: ")
        if inp:
            sys.exit()
    finally:
        file_Handle.close()  # closes file and exits here if data was red in "employees.txt"


def show_menu():
    """"show_menu()" - displays menu in a loop, reads users input
    and calls appropriate function to users input"""
    while True:
        clear_screen()
        usr_inp = getInt(menu_str, 1)  # gets user input
        # if block - calls appropriate function depending on user input
        if usr_inp == "1":
            clear_screen()
            show_employees()
            input("Press enter to continue ... ")
        elif usr_inp == "2":
            clear_screen()
            show_employees(getInt("Please enter employees ID number ( 5 digits ): ", 5))
            input("Press enter to continue ... ")
        elif usr_inp == "3":
            clear_screen()
            change_salary(getInt("Please enter employees ID number ( 5 digits ): ", 5))
            input("Press enter to continue ... ")
        elif usr_inp == "4":
            clear_screen()
            add_employee()
            input("Press enter to continue ... ")
        elif usr_inp == "5":
            clear_screen()
            remove_employee(getInt("Please enter employees ID number ( 5 digits ): ", 5))
            input("Press enter to continue ... ")
        elif usr_inp == "6":
            clear_screen()
            generate_bonus_info()
            input("Press enter to continue ... ")
        elif usr_inp == "7":
            clear_screen()
            generate_reports()
            input("Press enter to continue ... ")
        elif usr_inp == "8":
            clear_screen()
            break
        else:
            input("Valid choice is (1-9). Press enter to continue")


def save_data():
    """"save_data()" saves all changes made to employee database and saves it
    to "employees.txt" file"""
    file_handle = open(DATA_FILE, "w")
    for employee in emp_data:
        print(employee, file=file_handle)
    print("Data saved")
    file_handle.close()


def show_employees(id=""):
    """Prints one or all employees in emp_data[]"""
    output = []  # list that will be outputted to STD
    if id:  # if employee id was provided in parameter list
        if find_employee(id):
            output.append(find_employee(id))  # adds that employee to output
        else:  # in case employee not found exit function
            print("Employee not found")
            return
    else:
        output = emp_data  # else all employees added
    # table formatting
    table_l = longest("f_name") + longest("l_name") + longest("email") + 24  # overall width of the table
    print("Employee Data")  # title
    print(" "+"_" * table_l)  # top border
    # t_str string contains proper formatting for the table
    t_str = "|{}|{:>" + str(longest("f_name")) + "}|{:>" + str(longest("l_name")) + "}|{:>" + str(
        longest("email")) + "}|{:>15}|"
    # prints table attributes
    print(t_str.format("Em_No", "First Name", "Last Name", "Email", "Anual Salary"))
    # prints extra line under table attributes visual purposes only
    print(t_str.format("_" * 5, "_" * longest("f_name"), "_" * longest("l_name"), "_" * longest("email"), "_" * 15))
    # for loop outputs employee data from output[] to the table
    for employee in output:
        tmp = [value.strip() for value in str(employee).split(",")]
        print(t_str.format(tmp[0], tmp[1], tmp[2], tmp[3], tmp[4]))
    # bottom border
    print(t_str.format("_" * 5, "_" * longest("f_name"), "_" * longest("l_name"), "_" * longest("email"), "_" * 15))

def longest(emp_var):
    """longest check emp_data for longest values of individual employee
    for table formatting purposes only"""
    padding = 4  # adds extra padding to length of the employees field
    if emp_data:
        if emp_var == "f_name":
            length = max(len(employee.f_name) for employee in emp_data) + padding
        elif emp_var == "l_name":
            length = max(len(employee.l_name) for employee in emp_data) + padding
        elif emp_var == "email":
            length = max(len(employee.email) for employee in emp_data) + padding
    else:
        return 15  # in case no data in the table
    return length if length > 10 else 10  # condition in case very short value fro proper table formatting


def find_employee(id):
    """Returns pointer to employee object in a emp_data[] or None"""
    for employee in emp_data:
        if employee.em_no == id:
            return employee
    return None


def getPositiveFloat(prompt, max=0):
    """Gets input from user to get valid float max value optional"""
    while True:
        try:  # tries to convert input
            p_float = float(input(prompt))
            # if successful checks for bounds
            if p_float >= 0 and (p_float <= max or max == 0):
                return p_float  # returns input if more then 0 and under max or max was not set
            # for negative value or over max and if max was set continues to next cycle
            elif p_float < 0 or p_float > max and max != 0:
                print("Input must be a positive number of range ( 0 - ", end="")
                print(str(max) + " )" if max != 0 else "unlimited" + " )")  # formats string to accommodate possibility
                # max=0
                continue
        except ValueError:
            print("Input must be digits only...")


def change_salary(id=""):
    """Changes salary of employee"""
    emp = find_employee(id)  # finds employee
    if emp:
        print("Employee found:\n", emp)  # Displays employee found
        emp.salary = getPositiveFloat("Please enter new salary : ")  # Sets new salary
    else:
        print("Employee not found...")  # In case employee not found


def add_employee():
    """Adds new employee"""
    # Creates new employee object and adds it to the list em_data
    # Unic email generation in employee.py if email = ""
    emp_data.append(Employee(
        gen_id(),
        getString("Please enter employee's first name: ", 3, 15),
        getString("Please enter employee's surname: ", 3, 25),
        "", getPositiveFloat("Starting salary: ")
    ))


def remove_employee(id):
    """Removes one employee from emp_data[]"""
    t_emp = find_employee(id)  # Finds employee
    if t_emp:  # Tests if employee found
        print("Employee found:\n", t_emp)  # Prints employee found
        # Verifies if you still want to delete that employee
        sure = input("Delete this employee? (Y/N): ")
        if sure and sure.lower()[0] == "y":  # just 1st letter of sure variable matters any other value does nothing
            # to the emp_data
            emp_data.remove(t_emp)
            print("Employee deleted...")
        else:
            print("Process canceled")
    else:
        print("Employee not found...")  # in case employee not found


def generate_reports():
    """Generating Report"""
    print("Report")  # Title
    print("=" * 50)
    try:  # try block to catch division by zero
        print("Yearly salary average - {:0.2f} euro\n".format(
            sum(emp.salary for emp in emp_data) / len(emp_data)))  # gets sum of employee salary and divides by amount
        highest = ""  # highest salary output string
        h_salary = 0  # highest salary
        for emp in emp_data:  # cycle trough all employees
            if h_salary < emp.salary:  # if emp salary highest seen so far
                # sets h_salary to new high
                h_salary = emp.salary
                # adds that employee data to highest properly formatted also deletes previous value if any
                highest = "\t{:<10} {:<15} - {:<10.2f} euro\n".format(emp.f_name, emp.l_name, emp.salary)
            elif h_salary == emp.salary:  # in case one more employee has same salary as the highest one so far
                # adds one more employee to highest
                highest += "\t{:<10} {:<15} - {:<10.2f} euro\n".format(emp.f_name, emp.l_name, emp.salary)
        # One liner if for singular or multiple highest earners
        print("Highest earner:" if len(highest.split('\n')) == 2 else "Highest earners:")
        print(highest)  # outputs highest
    except ZeroDivisionError:
        print("No data found in employee database...")


def generate_bonus_info():
    """Requests bonus % for each employ in a list
    modifies ."""
    if emp_data:  # Checks if there is any data in emp_data
        # Creates file name string "bonus" and adds current year since its yearly bonus
        file_name = "bonus" + str(datetime.datetime.now().year)+".txt"
        bonus_file = open(file_name, "w")  # Opens file "bonusYYYY.txt"
        print("\t\tBonus year - " + str(datetime.datetime.now().year)+"\n", file=bonus_file)  # Title in a file
        #  Prints attributes to file of data that will be displayed in "bonusYYYY.txt"
        print("{:5} {:>15} {:>20} {:>20}".format("Em No", "First Name", "Last name", "Annual bonus"),
              file=bonus_file)
        # Cycle trough all employees
        for employee in emp_data:
            clear_screen()
            # Gets float value up 100 to each employee in emp_data[] and saves it in each object bonus field
            employee.bonus = getPositiveFloat(
                "Please enter bonus procentage (1 - 100%) for \nEmployee no: " + " " + employee.em_no +
                "\nEmployee name: " + employee.f_name + " " + employee.l_name + " " + \
                "\n>>> ", 100)
            # Properly formats output to file and converts % bonus to yearly earnings.
            print("{:5} {:>15} {:>20} {:>15.2f} euro".format(employee.em_no, employee.f_name,
                                                          employee.l_name, employee.bonus / 100 * employee.salary),
                  file=bonus_file)
        bonus_file.close()
        print(file_name + " file created...")  # Confirms that file with output was created
    else:
        print("No data found in employee database ...")


def gen_id():
    """Generates unic id and returns as a string"""
    t_id = 10000  # Sets temporary id to 10000
    while True:  # loops until unic id was found
        if str(t_id) not in (employee.em_no for employee in emp_data):  # check if this id used already returns it
            # if not
            return str(t_id)
        t_id += 1  # otherwise increases it by 1


def getInt(prompt, max):
    """This function gets valid int from STI, also max value is to make sure its certain length
    for example max = 1 then (0-9); max = 2 (10-99);
    Also int value is handled and return as a string, because it won't ever be used as a number.
    This way preventing redundant type conversions"""
    num = input(prompt)  # Gets input from STI
    while not (num.isdigit() and len(num) == max):  # Loops until input is digit only of length = max
        clear_screen()
        print(prompt)
        # Input string has one liner if statement to accommodate menu choice
        num = input("Input must be (1-8) digit: " if max == 1 else "Input must be " + str(max) + " digits: ")
    clear_screen()
    return num  # returns int as a string


def getString(prompt, min, max):
    """Gets string in bounds min max inclusive from STI and makes sure its only letters
    with one exception allowing one occurrence of "'" """
    t_str = input(prompt)
    # while loop until valid input received valid surname check and bound check
    while not (checkValidSurname(t_str) and len(t_str) >= min and len(t_str) <= max):
        t_str = input("Input must contain letters only and it's range has to be between ( " +
                      str(min) + " - " + str(max) + " )")
    return t_str


def checkValidSurname(surname):
    """This function checks if its valid surname containing "'" """
    if "'" in surname and len(surname.split("'")) == 2:  # if surname has "'" in it and only 1 occurrence of it.
        for part in surname.split("'"):  # cycle through parts of surname
            if part.isalpha():  # if part is letters only continues
                continue
            else:
                return False  # if any of the parts contains not characters returns false
    elif surname.isalpha():  # In case there was "'" none in a surname returns true
        return True
    else:
        return False  # for any other wrong value
    return True  # and true if there was two parts of surname between "'" all letters.


# main function


def main():
    """---Main ---"""

    # Loads data from file
    load_data()
    # show_menu() main program loop
    show_menu()
    # saves data
    save_data()


# main function call
main()
