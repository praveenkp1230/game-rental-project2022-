# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high

# needed for google sheets api

import gspread
from google.oauth2.service_account import Credentials
import datetime
from pprint import pprint

# IAM config allowing user access
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("game_rental")


def make_choice():
    """Get choice of action as an input from user
    """
    while True:
        print("Do you want to:\n 1) Make a rental?\n 2) Return a rental?\n "
              "3) Print stock?\n 4) Add a new customer?\n "
              "5) Add a new title?\n 6) Update fines?\n")
        chosen_action = input("Please select from above numbers "
                              "and press Enter:\n")
       
        if validate_chosen_action(chosen_action):
            if int(chosen_action) == 6:
                get_overdue_items()
            elif int(chosen_action) == 5:
                add_game()
            elif int(chosen_action) == 4:
                add_customer()
            elif int(chosen_action) == 3:
                print_stock()
            elif int(chosen_action) == 2:
                input_data(2)
            elif int(chosen_action) == 1:
                input_data(1)
            break


def validate_chosen_action(chosen_action):
    """Checks chosen_action input was an integer between 1 and 6
    Args:
        chosen_action (int) : The input the user entered when choosing
        an action
    Raises:
        ValueError : If chosen_action is not a full number between 1 and 6
    Notes:
        Converts chosen_Action to a string before testing for inclusion
    """
    try:
        if int(chosen_action) not in {1, 2, 3, 4, 5, 6}:
            raise ValueError(
                "Must be a whole num between 1 and 6"
            )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again")
        return False

    return True


def input_data(choice):
    """Asks user for customers first name, last name, game title and
      its platform (INDENT????????????????????????????????)
      Calls the relevant function depending on wether choice was 1 or 2
    Args:
        choice (int) : The chosen action from make_choice function
    """
    fname = input("\nPlease enter the customer First Name:\n")
    lname = input("\nPlease enter the customer Last Name:\n")
    game = input("\nPlease enter the game title:\n")
    platform = input("\nPlease enter platform:\n")

    data = [fname, lname, game, platform]

    if validate_data(data):
        print(f"\nYou entered:\n First Name: {fname} \n Last Name: {lname} \n "
              f"Game: {game} \n Platform: {platform}")
        if choice == 1:
            is_game_in_sheet(fname, lname, game, platform)
        else:
            return_rental(fname, lname, game, platform)


def validate_data(data):
    """Checks all data has been entered and is valid
    Returns:
        bool : True if data validates, False if not
    """
    # print("line 408")
    while True:
        # print("line 410")
        if not all(data):
            print("Missing element, please try again")
            return False
        else:
            return True

def is_game_in_sheet(fname, lname, game, platform):
    """See if the game to be rented is in the games worksheet
    Args:
        fname (str) : Customers first name
        lname (str) : Customers last name
        game (str) : The game the customer is trying to rent
        platform (str) : The platform the customer is trying to rent
    """
    worksheet_games = SHEET.worksheet("games").col_values(1)
    if game in worksheet_games:
        check_stock(fname, lname, game, platform)
    else:
        print("Sorry, we do not stock that game")


def check_stock(fname, lname, game, platform):
    """Checks the game to be rented is in stock
    Args:
        fname (str) : Customers first name
        lname (str) : Customers last name
        game (str) : The game the customer is trying to rent
        platform (str) : The platform the customer is trying to rent
    """
    worksheet_stock = SHEET.worksheet("games").col_values(1)
    game_index = worksheet_stock.index(game) + 1
    worksheet_game_data = SHEET.worksheet("games").row_values(game_index)
    stock = worksheet_game_data[4]
    stock_int = int(stock)
    if stock_int <= 0:
        print("from 184, game not in stock")
    else:
        check_platform(fname, lname, game, platform, worksheet_game_data)


def check_platform(fname, lname, game, platform, worksheet_game_data):
    """Checks wether the correct data for the platform has been entered
    Args:
        fname (str) : Customers first name
        lname (str) : Customers last name
        game (str) : The game the customer is trying to rent
        platform (str) : The platform the customer is trying to rent
        worksheet_game_data (list) : The chosen games data from games worksheet
    """
    worksheet_platform = worksheet_game_data[1]
    if worksheet_platform == platform:
        check_customer_fname(fname, lname, game, platform, worksheet_game_data)
    else:
        print("wrong platform")


def check_customer_fname(fname, lname, game, platform, worksheet_game_data):
    """Checks the correct data for the customers first name has been entered
    Args:
        fname (str) : Customers first name
        lname (str) : Customers last name
        game (str) : The game the customer is trying to rent
        platform (str) : The platform the customer is trying to rent
        worksheet_game_data (list) : The chosen games data from games worksheet
    """
    worksheet_fnames = SHEET.worksheet("customers").col_values(1)
    if fname not in worksheet_fnames:
        print("No record of customers First Name")
    else:
        fname_index = worksheet_fnames.index(fname)
        check_customer_lname(fname, lname, game, platform, worksheet_game_data,
                             fname_index)


def check_customer_lname(fname, lname, game, platform, worksheet_game_data,
                         fname_index):
    """Checks the correct data for the customers last name has been entered
    Args:
        fname (str) : Customers first name
        lname (str) : Customers last name
        game (str) : The game the customer is trying to rent
        platform (str) : The platform the customer is trying to rent
        worksheet_game_data (list) : The chosen games data from games worksheet
        fname_index (int) : The row number of the customers first name
    """
    worksheet_lnames = SHEET.worksheet("customers").col_values(2)
    customer_lname = worksheet_lnames[fname_index]
    worksheet_dobs = SHEET.worksheet("customers").col_values(3)
    customer_dob = worksheet_dobs[fname_index]
    if customer_lname == lname:
        calculate_dates(fname, lname, game, platform, worksheet_game_data,
                        customer_dob)
    else:
        print("wrong last name")


def calculate_dates(fname, lname, game, platform, worksheet_game_data,
                    customer_dob):
    """Gets todays date and the customers date of birth in correct format
    Args:
        fname (str) : Customers first name
        lname (str) : Customers last name
        game (str) : The game the customer is trying to rent
        platform (str) : The platform the customer is trying to rent
        worksheet_game_data (list) : The chosen games data from games worksheet
        customer_dob (str) : The customers date of birth
    """
    today = datetime.datetime.now().date()
    today_string = datetime.datetime.strftime(today, "%d/%m/%Y")
    today_date = datetime.datetime.strptime(today_string, "%d/%m/%Y")
    dob_date = datetime.datetime.strptime(customer_dob, "%d/%m/%Y")
    check_age(fname, lname, game, platform, worksheet_game_data,
              today_date, dob_date)


def check_age(fname, lname, game, platform, worksheet_game_data,
              today_date, dob_date):
    """Checks if the customer is old enough to rent the selected game
    Args:
        fname (str) : Customers first name
        lname (str) : Customers last name
        game (str) : The game the customer is trying to rent
        platform (str) : The platform the customer is trying to rent
        worksheet_game_data (list) : The chosen games data from games worksheet
        today_date (datetime.datetime) : The date the programe is run
        dob_date (datetime.datetime) : The customers date of birth
    """
    today = datetime.date.today()
    age_in_years = today.year - dob_date.year
    if today.month < dob_date.month or (today.month == dob_date.month and
                                        today.day < dob_date.day):
        age_in_years -= 1
    if age_in_years >= int(worksheet_game_data[3]):
        calculate_return_date(fname, lname, game, platform,
                              worksheet_game_data)
    else:
        print("SORRY TOO YOUNG!!!!!!")


def calculate_return_date(fname, lname, game, platform, worksheet_game_data):
    """Adds three days to todays date
    Args:
        fname (str) : Customers first name
        lname (str) : Customers last name
        game (str) : The game the customer is trying to rent
        platform (str) : The platform the customer is trying to rent
        worksheet_game_data (list) : The chosen games data from games worksheet
    """
    today = datetime.datetime.now().date()
    return_date = today + datetime.timedelta(days=3)
    format_date = return_date.strftime("%d/%m/%Y")
    reduce_stock(fname, lname, game, platform, worksheet_game_data,
                 format_date)


def reduce_stock(fname, lname, game, platform, worksheet_game_data,
                 format_date):
    """Reduces stock number by one
    Args:
        fname (str) : Customers first name
        lname (str) : Customers last name
        game (str) : The game the customer is trying to rent
        platform (str) : The platform the customer is trying to rent
        worksheet_game_data (list) : The chosen games data from games worksheet
        format_date (str) : The date the item is due to be returned
    """
    current_stock = worksheet_game_data[4]
    updated_stock = int(current_stock) - 1
    worksheet_to_update = SHEET.worksheet("games")
    cell = worksheet_to_update.find(worksheet_game_data[0])
    worksheet_to_update.update(f"E{cell.row}", updated_stock)
    update_rental_worksheet(fname, lname, game, platform, format_date)


def update_rental_worksheet(fname, lname, game, platform, format_date):
    """Updates the rentals worksheet
    Args:
        fname (str) : Customers first name
        lname (str) : Customers last name
        game (str) : The game the customer is trying to rent
        platform (str) : The platform the customer is trying to rent
        format_date (datetime) : Due date back in dd/mm/YYYY format
    """
    print("Updating rentals worksheet...")
    rental_data = [fname, lname, game, platform, format_date]
    worksheet_to_update = SHEET.worksheet("rentals")
    worksheet_to_update.append_row(rental_data)
    print("Worksheet updated successfully")


def update_worksheet(data, worksheet):
    """Updates a worksheet
    Args:
        data (list) : The data to input into the worksheet
        worksheet (str) : Name of the worksheet to update
    Returns:
        data_type : Optional description of return value
        Extra lines are not indented
    """
    if worksheet == "games":
        data[3] = int(data[3])
        data[4] = int(data[4])
    print(f"\nUpdating {worksheet} worksheet...")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f"\n{worksheet} updated successfully.")


def return_rental(fname, lname, game, platform):
    """Deletes the returned item from the rentals worksheet
    Args:
        fname (str) : Customers first name
        lname (str) : Customers last name
        game (str) : The game the customer is trying to return
        platform (str) : The platform the customer is trying to return
    """
    rentals_worksheet = SHEET.worksheet("rentals")
    rentals_games = rentals_worksheet.col_values(3)
    game_index = rentals_games.index(game) + 2
    worksheet_rental_data = rentals_worksheet.row_values(game_index)
    if (worksheet_rental_data[0] == fname and
        worksheet_rental_data[1] == lname and
        worksheet_rental_data[2] == game and
        worksheet_rental_data[3] == platform):
            rentals_worksheet.delete_rows(game_index)
            add_to_stock(game, platform)
    else:
        print("NOT IN SHEET")


def add_to_stock(game, platform):
    """Adds 1 to the stock of the returned game in the games worksheet
    Args:
        game (str) : The game the customer is trying to return
        platform (str) : The platform the customer is trying to return
    """
    games_worksheet = SHEET.worksheet("games")
    games_titles = games_worksheet.col_values(1)
    game_index = games_titles.index(game) + 1
    worksheet_game_data = games_worksheet.row_values(game_index)
    if worksheet_game_data[0] == game and worksheet_game_data[1] == platform:
        int_stock = int(worksheet_game_data[4])
        new_stock = int_stock + 1
        games_worksheet.update_cell(game_index, 5, new_stock)
    else:
        print("Incorrect values")


def print_stock():
    """Pretty print the games worksheet to the terminal
    """
    stock = SHEET.worksheet("games").get_all_values()
    print("\n")
    pprint(stock)


def add_customer():
    """Gets user input for first name, last name, date of birth.
    Asks for confirmation of data.
    """
    while True:
        fname = input("\nAdd first name:\n")
        lname = input("\nAdd last name:\n")
        print("\nDate of birth must be in dd/mm/YYYY format")
        print("For example: 12/12/2006")
        dob = input("\nAdd date of birth\n")

        new_customer_info = [fname, lname, dob]

        if validate_add_customer(new_customer_info):
            print(f"\nYou entered...\n First Name: {fname}\n "
                  f"Last Name: {lname}\n "
                  f"Date of Birth: {dob}\n")
            print("Is this correct?\n")
            confirm = input("Enter Y for yes, N for No:\n")
            confirm_strip_lcase = confirm.strip().lower()
            if confirm_strip_lcase == "n":
                validate_add_customer(new_customer_info)
            elif confirm_strip_lcase == "y":
                update_worksheet(new_customer_info, "customers")
                break


def validate_add_customer(new_customer_info):
    """Checks all data has been entered and is valid
    Returns:
        bool : True if data validates, False if not
    """
    while True:
        if not all(new_customer_info):
            print("Missing element, please try again")
            return False
        else:
            try:
                datetime.datetime.strptime(new_customer_info[2], "%d/%m/%Y")
            except:
                print("wrong date format!!!")
                return False
        return True


def add_game():
    """Adds new game data to games worksheet if data is verified
    """
    while True:
        title = input("\nAdd game title:\n")
        platform = input("\nAdd platform:\n")
        genre = input("\nAdd genre:\n")
        min_age = input("\nAdd minimum age:\n")
        quantity = input("\nAdd how many:\n")
        new_game_info = [title, platform, genre, min_age, quantity]
        if validate_add_game(new_game_info):
            print(f"\nYou entered...\n Title: {title}\n "
                  f"Platform: {platform}\n Genre: {genre}\n "
                  f"Genre: {genre}\n Minimum age: {min_age}\n "
                  f"How many: {quantity}\n")
            print("Is this correct?\n")
            confirm = input("Enter Y for yes, N for No\n")
            confirm_strip_lcase = confirm.strip().lower()
            if confirm_strip_lcase == "n":
                validate_add_game(new_game_info)
                print("from 435 confirm says no")
            elif confirm_strip_lcase == "y":
                update_worksheet(new_game_info, "games")
                break


def validate_add_game(new_game_info):
    """Checks all data has been entered and is valid
    Returns:
        bool : True if data validates, False if not
    """
    if not all(new_game_info):
        print("Missing element, please try again")
        return False
    if new_game_info[1] not in ("switch", "ps5", "xbox one"):
        print("Platform must be either switch, ps5 or xbox one. "
              f"You entered {new_game_info[1]}")
        print("Please enter info again")
        return False
    else:
        try:
            int(new_game_info[3])
        except:
            print("min age not a number, please try again")
        try:
            int(new_game_info[4])
        except:
            print("quantity not a number, please try again")
        try:
            if new_game_info[1] not in ("switch", "ps5", "xbox one"):
                return False
        except:
            print("Platform must be either switch, PS5 or xbox one. "
                  f"You entered {new_game_info[1]}")
        return True


def get_overdue_items():
    """Gets the row number of overdue items
    """
    overdue_items_row = []
    days_late_list = []
    today = datetime.datetime.now().date()
    today_string = datetime.datetime.strftime(today, "%d/%m/%Y")
    today_date = datetime.datetime.strptime(today_string, "%d/%m/%Y").date()
    rentals_worksheet = SHEET.worksheet("rentals")
    rentals_return_date = rentals_worksheet.col_values(5)
    rentals_return_date.pop(0)
    for date in rentals_return_date:
        return_date = datetime.datetime.strptime(date, "%d/%m/%Y").date()
        days_late = (today_date - return_date).days
        if days_late > 0:
            int_overdue_row = int(rentals_return_date.index(date)) + 2
            overdue_items_row.append(int_overdue_row)
            days_late_list.append(days_late)
            calculate_fine(overdue_items_row, days_late_list)


def calculate_fine(overdue_items_row, days_late_list):
    """Calculates the fine amount for overdue rentals
    Args:
        overdue_items_row (list) : The row number of overdue items
        days_late_list (list) : The number of days overdue
    """
    fines_list = []
    fine_per_day = 4
    for days in days_late_list:
        amount = days * fine_per_day
        fines_list.append(amount)
    add_fine(overdue_items_row, fines_list)


def add_fine(overdue_items_row, fines_list):
    """Adds the calculated fine to the rentals worksheet
    Args:
        overdue_items_row (list) : The row number of overdue items
        fines_list (list) : The amount of the fine
    """
    worksheet_to_update = SHEET.worksheet("rentals")
    for i in range(len(overdue_items_row)):
         worksheet_to_update.update_cell(overdue_items_row[i], 6, fines_list[i])


if __name__ == "__main__":
    """Calls make_choice to begin
    """
    make_choice()
